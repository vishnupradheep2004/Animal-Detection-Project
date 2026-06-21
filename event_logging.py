"""
Event Logging Module
Comprehensive logging of all detection events
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import sqlite3

logger = logging.getLogger(__name__)


class EventLogger:
    """Log all detection events to file and database"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup file logging
        self.log_file = self.log_dir / f"detection_{datetime.now().strftime('%Y%m%d')}.log"
        self.setup_file_logging()
        
        # Setup database
        self.db_path = self.log_dir / "detections.db"
        self.setup_database()
    
    def setup_file_logging(self):
        """Configure file logging"""
        try:
            file_handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(file_handler)
            logger.info("File logging configured")
        except Exception as e:
            logger.error(f"Error setting up file logging: {str(e)}")
    
    def setup_database(self):
        """Create SQLite database for events"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    class_name TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    x1 INTEGER,
                    y1 INTEGER,
                    x2 INTEGER,
                    y2 INTEGER,
                    image_path TEXT,
                    alert_sent BOOLEAN DEFAULT 0
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT NOT NULL,
                    description TEXT,
                    severity TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Error setting up database: {str(e)}")
    
    def log_detection(self, class_name: str, confidence: float, 
                     coordinates: tuple, image_path: str = None, 
                     alert_sent: bool = False) -> int:
        """Log detection to database"""
        try:
            x1, y1, x2, y2 = coordinates
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO detections 
                (timestamp, class_name, confidence, x1, y1, x2, y2, image_path, alert_sent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                class_name,
                confidence,
                int(x1), int(y1), int(x2), int(y2),
                image_path,
                alert_sent
            ))
            
            conn.commit()
            detection_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"Detection logged: {class_name} ({confidence:.2%})")
            return detection_id
        except Exception as e:
            logger.error(f"Error logging detection: {str(e)}")
            return -1
    
    def log_event(self, event_type: str, description: str, severity: str = "INFO"):
        """Log general event"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO events (timestamp, event_type, description, severity)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                event_type,
                description,
                severity
            ))
            
            conn.commit()
            conn.close()
            
            logger.log(
                getattr(logging, severity),
                f"{event_type}: {description}"
            )
        except Exception as e:
            logger.error(f"Error logging event: {str(e)}")
    
    def get_detection_history(self, limit: int = 100) -> list:
        """Retrieve detection history"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM detections 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving history: {str(e)}")
            return []
    
    def get_statistics(self, days: int = 1) -> Dict[str, Any]:
        """Get detection statistics"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Get detection count
            cursor.execute("""
                SELECT COUNT(*) as total,
                       COUNT(DISTINCT class_name) as unique_animals,
                       AVG(confidence) as avg_confidence,
                       MAX(confidence) as max_confidence
                FROM detections
                WHERE timestamp > datetime('now', '-' || ? || ' days')
            """, (days,))
            
            stats = dict(zip(
                [desc[0] for desc in cursor.description],
                cursor.fetchone()
            ))
            
            # Get detections by class
            cursor.execute("""
                SELECT class_name, COUNT(*) as count
                FROM detections
                WHERE timestamp > datetime('now', '-' || ? || ' days')
                GROUP BY class_name
                ORDER BY count DESC
            """, (days,))
            
            stats['detections_by_class'] = dict(cursor.fetchall())
            
            conn.close()
            return stats
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {}
    
    def export_to_json(self, output_file: str, limit: int = 1000):
        """Export detection logs to JSON"""
        try:
            detections = self.get_detection_history(limit)
            with open(output_file, 'w') as f:
                json.dump(detections, f, indent=4)
            logger.info(f"Data exported to {output_file}")
        except Exception as e:
            logger.error(f"Error exporting to JSON: {str(e)}")


def setup_logging(log_level=logging.INFO):
    """Setup global logging configuration"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
