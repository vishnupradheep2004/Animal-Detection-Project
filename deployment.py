"""
Deployment Module
Handle deployment configuration and management
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class DeploymentConfig:
    """Manage deployment configuration"""
    
    def __init__(self, config_file: str = "deployment_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
        
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "name": "Animal Detection System",
            "version": "1.0.0",
            "environment": "production",
            "server": {
                "host": "0.0.0.0",
                "port": 5000,
                "debug": False
            },
            "camera": {
                "type": "webcam",
                "url": "",
                "fps": 30
            },
            "model": {
                "path": "runs/detect/train/weights/best.pt",
                "confidence": 0.6
            },
            "telegram": {
                "enabled": False,
                "bot_token": "",
                "chat_id": ""
            },
            "storage": {
                "snapshots_dir": "snapshots",
                "logs_dir": "logs",
                "max_storage_gb": 10
            },
            "alerts": {
                "enabled": True,
                "confidence_threshold": 0.7,
                "daily_limit": 50
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration"""
        def update_dict(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = update_dict(d.get(k, {}), v)
                else:
                    d[k] = v
            return d
        
        self.config = update_dict(self.config, updates)
        self.save_config()
        logger.info("Configuration updated")
    
    def get_value(self, path: str, default=None):
        """Get config value by dot notation path"""
        keys = path.split('.')
        value = self.config
        for key in keys:
            value = value.get(key, {}) if isinstance(value, dict) else default
        return value if value != {} else default


class SystemMonitor:
    """Monitor system resources and health"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.status = "running"
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        try:
            import psutil
            
            info = {
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory": {
                    "percent": psutil.virtual_memory().percent,
                    "used_mb": psutil.virtual_memory().used / (1024**2),
                    "available_mb": psutil.virtual_memory().available / (1024**2)
                },
                "disk": {
                    "percent": psutil.disk_usage('/').percent,
                    "used_gb": psutil.disk_usage('/').used / (1024**3),
                    "total_gb": psutil.disk_usage('/').total / (1024**3)
                }
            }
            return info
        except ImportError:
            logger.warning("psutil not installed, skipping system info")
            return {}
        except Exception as e:
            logger.error(f"Error getting system info: {str(e)}")
            return {}
    
    def get_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "status": self.status,
            "timestamp": datetime.now().isoformat(),
            "system_info": self.get_system_info()
        }


class DeploymentManager:
    """Manage deployment lifecycle"""
    
    def __init__(self, config_file: str = "deployment_config.json"):
        self.config = DeploymentConfig(config_file)
        self.monitor = SystemMonitor()
        self.deployment_log = []
    
    def start_deployment(self) -> bool:
        """Start the deployment"""
        try:
            self._log_event("Deployment started")
            logger.info("🚀 Deployment started")
            return True
        except Exception as e:
            logger.error(f"Error starting deployment: {str(e)}")
            self._log_event(f"Deployment start failed: {str(e)}")
            return False
    
    def stop_deployment(self) -> bool:
        """Stop the deployment"""
        try:
            self._log_event("Deployment stopped")
            logger.info("⛔ Deployment stopped")
            return True
        except Exception as e:
            logger.error(f"Error stopping deployment: {str(e)}")
            return False
    
    def health_check(self) -> bool:
        """Perform health check"""
        try:
            system_info = self.monitor.get_system_info()
            
            # Check if resources are within acceptable limits
            if system_info.get("cpu_percent", 0) > 90:
                logger.warning("CPU usage high")
                return False
            
            if system_info.get("memory", {}).get("percent", 0) > 85:
                logger.warning("Memory usage high")
                return False
            
            self._log_event("Health check passed")
            return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
    
    def _log_event(self, event: str):
        """Log deployment event"""
        self.deployment_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": event
        })
    
    def export_deployment_info(self, output_file: str = "deployment_info.json"):
        """Export deployment information"""
        try:
            info = {
                "config": self.config.config,
                "status": self.monitor.get_status(),
                "deployment_log": self.deployment_log
            }
            
            with open(output_file, 'w') as f:
                json.dump(info, f, indent=4, default=str)
            
            logger.info(f"Deployment info exported to {output_file}")
        except Exception as e:
            logger.error(f"Error exporting deployment info: {str(e)}")


# Docker support
def generate_dockerfile() -> str:
    """Generate Dockerfile for containerization"""
    return """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
"""


def generate_docker_compose() -> str:
    """Generate docker-compose.yml"""
    return """version: '3.8'

services:
  animal-detection:
    build: .
    volumes:
      - ./snapshots:/app/snapshots
      - ./logs:/app/logs
      - ./runs:/app/runs
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
    restart: always
    
  dashboard:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./dashboard:/usr/share/nginx/html
    depends_on:
      - animal-detection
"""


if __name__ == "__main__":
    # Create sample deployment files
    dockerfile = generate_dockerfile()
    docker_compose = generate_docker_compose()
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile)
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose)
    
    print("Deployment files created successfully!")
