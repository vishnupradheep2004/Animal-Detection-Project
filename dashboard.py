"""
Dashboard Module
Web-based dashboard for monitoring and visualization
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class Dashboard:
    """Real-time dashboard for monitoring detections"""
    
    def __init__(self, stats_file: str = "dashboard_stats.json"):
        self.stats_file = stats_file
        self.detections = []
        self.stats = {
            "total_detections": 0,
            "animals_detected": {},
            "detection_history": [],
            "uptime": 0,
            "last_detection": None
        }
        self._load_stats()
    
    def _load_stats(self):
        """Load statistics from file"""
        try:
            if Path(self.stats_file).exists():
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
                logger.info("Loaded dashboard statistics")
        except Exception as e:
            logger.error(f"Error loading stats: {str(e)}")
    
    def _save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=4, default=str)
        except Exception as e:
            logger.error(f"Error saving stats: {str(e)}")
    
    def record_detection(self, class_name: str, confidence: float, box_coords: tuple):
        """Record a detection event"""
        detection = {
            "timestamp": datetime.now().isoformat(),
            "class": class_name,
            "confidence": float(confidence),
            "coordinates": box_coords
        }
        
        self.detections.append(detection)
        self.stats["total_detections"] += 1
        self.stats["last_detection"] = detection["timestamp"]
        
        # Update animal count
        if class_name not in self.stats["animals_detected"]:
            self.stats["animals_detected"][class_name] = 0
        self.stats["animals_detected"][class_name] += 1
        
        # Keep history limited to last 100 detections
        self.stats["detection_history"] = self.stats["detection_history"][-99:] + [detection]
        
        self._save_stats()
        logger.info(f"Detection recorded: {class_name} ({confidence:.2f})")
    
    def get_summary(self) -> Dict:
        """Get dashboard summary"""
        return {
            "total_detections": self.stats["total_detections"],
            "animals": self.stats["animals_detected"],
            "recent_detections": self.stats["detection_history"][-10:],
            "last_detection": self.stats["last_detection"]
        }
    
    def get_statistics(self) -> Dict:
        """Get detailed statistics"""
        return self.stats
    
    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            "total_detections": 0,
            "animals_detected": {},
            "detection_history": [],
            "uptime": 0,
            "last_detection": None
        }
        self._save_stats()
        logger.info("Dashboard statistics reset")


class HTMLDashboard:
    """Generate HTML dashboard"""
    
    @staticmethod
    def generate_html(stats: Dict) -> str:
        """Generate HTML dashboard content"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Animal Detection Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .header {{
                    color: white;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .dashboard {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-bottom: 20px;
                }}
                .card {{
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .card h3 {{
                    color: #333;
                    margin-bottom: 15px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                }}
                .stat {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
                .stat-label {{
                    color: #666;
                }}
                .stat-value {{
                    font-weight: bold;
                    color: #667eea;
                    font-size: 1.2em;
                }}
                .detection-item {{
                    padding: 10px;
                    margin: 5px 0;
                    background: #f5f5f5;
                    border-left: 4px solid #667eea;
                    border-radius: 4px;
                }}
                .time {{
                    font-size: 0.9em;
                    color: #999;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🦁 Animal Detection Dashboard</h1>
                    <p>Real-time monitoring system</p>
                </div>
                
                <div class="dashboard">
                    <div class="card">
                        <h3>📊 Statistics</h3>
                        <div class="stat">
                            <span class="stat-label">Total Detections</span>
                            <span class="stat-value">{stats['total_detections']}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Last Detection</span>
                            <span class="stat-value">{stats['last_detection'] or 'None'}</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h3>🦁 Animals Detected</h3>
        """
        
        for animal, count in stats.get('animals_detected', {}).items():
            html += f"""
                        <div class="stat">
                            <span class="stat-label">{animal}</span>
                            <span class="stat-value">{count}</span>
                        </div>
            """
        
        html += """
                    </div>
                    
                    <div class="card" style="grid-column: span 2;">
                        <h3>🕐 Recent Detections</h3>
        """
        
        for detection in stats.get('detection_history', [])[-10:]:
            html += f"""
                        <div class="detection-item">
                            <strong>{detection['class']}</strong> - {detection['confidence']:.2%}
                            <div class="time">{detection.get('timestamp', 'N/A')}</div>
                        </div>
            """
        
        html += """
                    </div>
                </div>
            </div>
            <script>
                setInterval(function() {{
                    location.reload();
                }}, 5000);
            </script>
        </body>
        </html>
        """
        return html
