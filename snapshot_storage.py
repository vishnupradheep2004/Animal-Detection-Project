"""
Snapshot Storage Module
Store and manage detection snapshots
"""

import cv2
import logging
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional
import os

logger = logging.getLogger(__name__)


class SnapshotManager:
    """Manage snapshot storage and organization"""
    
    def __init__(self, storage_dir: str = "snapshots"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.max_storage_gb = 10
        self._create_subdirectories()
    
    def _create_subdirectories(self):
        """Create subdirectories for organization"""
        subdirs = ["detections", "alerts", "archive", "temp"]
        for subdir in subdirs:
            (self.storage_dir / subdir).mkdir(exist_ok=True)
    
    def save_detection_snapshot(self, frame: any, class_name: str, 
                               confidence: float, coordinates: Tuple) -> Optional[str]:
        """Save detection snapshot with metadata"""
        try:
            # Create class subdirectory
            class_dir = self.storage_dir / "detections" / class_name
            class_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            confidence_str = f"{confidence:.2f}".replace(".", "_")
            filename = f"{class_name}_{timestamp}_{confidence_str}.jpg"
            filepath = class_dir / filename
            
            # Draw detection box on image
            x1, y1, x2, y2 = coordinates
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (int(x1), int(y1)), (int(x2), int(y2)), 
                         (0, 255, 0), 2)
            
            # Add text with class and confidence
            text = f"{class_name} {confidence:.2f}"
            cv2.putText(frame_copy, text, (int(x1), int(y1) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Save image
            cv2.imwrite(str(filepath), frame_copy)
            
            logger.info(f"Snapshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving snapshot: {str(e)}")
            return None
    
    def save_alert_snapshot(self, frame: any, class_name: str, 
                           confidence: float) -> Optional[str]:
        """Save alert snapshot"""
        try:
            alert_dir = self.storage_dir / "alerts"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"alert_{class_name}_{timestamp}.jpg"
            filepath = alert_dir / filename
            
            cv2.imwrite(str(filepath), frame)
            logger.info(f"Alert snapshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving alert snapshot: {str(e)}")
            return None
    
    def get_storage_usage(self) -> float:
        """Get total storage usage in GB"""
        try:
            total_size = 0
            for file in self.storage_dir.rglob("*"):
                if file.is_file():
                    total_size += file.stat().st_size
            return total_size / (1024**3)  # Convert to GB
        except Exception as e:
            logger.error(f"Error calculating storage: {str(e)}")
            return 0
    
    def cleanup_old_files(self, days: int = 7) -> int:
        """Remove snapshots older than specified days"""
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (days * 24 * 3600)
            
            deleted_count = 0
            for file in self.storage_dir.rglob("*.jpg"):
                if file.stat().st_mtime < cutoff_time:
                    file.unlink()
                    deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old snapshots")
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning up files: {str(e)}")
            return 0
    
    def get_snapshots_for_class(self, class_name: str, limit: int = 10) -> list:
        """Get recent snapshots for a specific class"""
        try:
            class_dir = self.storage_dir / "detections" / class_name
            if not class_dir.exists():
                return []
            
            snapshots = sorted(
                class_dir.glob("*.jpg"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:limit]
            
            return [str(s) for s in snapshots]
        except Exception as e:
            logger.error(f"Error retrieving snapshots: {str(e)}")
            return []
    
    def archive_old_snapshots(self, days: int = 30) -> int:
        """Archive old snapshots"""
        try:
            import time
            import shutil
            
            current_time = time.time()
            cutoff_time = current_time - (days * 24 * 3600)
            
            archive_dir = self.storage_dir / "archive"
            archived_count = 0
            
            for file in self.storage_dir.glob("detections/**/*.jpg"):
                if file.stat().st_mtime < cutoff_time:
                    destination = archive_dir / file.parent.name / file.name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), str(destination))
                    archived_count += 1
            
            logger.info(f"Archived {archived_count} snapshots")
            return archived_count
        except Exception as e:
            logger.error(f"Error archiving snapshots: {str(e)}")
            return 0
    
    def get_statistics(self) -> dict:
        """Get storage statistics"""
        try:
            stats = {
                "total_snapshots": 0,
                "total_size_gb": self.get_storage_usage(),
                "by_class": {},
                "by_date": {}
            }
            
            detection_dir = self.storage_dir / "detections"
            if detection_dir.exists():
                for class_dir in detection_dir.iterdir():
                    if class_dir.is_dir():
                        snapshots = list(class_dir.glob("*.jpg"))
                        stats["by_class"][class_dir.name] = len(snapshots)
                        stats["total_snapshots"] += len(snapshots)
            
            return stats
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {}
