# Animal Detection with YOLOv8 - Complete System

A comprehensive animal detection system featuring real-time RTSP/Webcam support, Telegram alerts, web dashboard, event logging, and snapshot management.

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│         ANIMAL DETECTION SYSTEM v1.0                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📷 Camera Module               🔍 YOLO Model          │
│  ├─ Live RTSP Stream           └─ Detection & Tracking│
│  └─ Webcam Feed                                        │
│         │                                              │
│         └──────────────────┬──────────────────┐        │
│                            │                  │        │
│                      ┌─────▼─────┐      ┌────▼──┐     │
│                      │ Detection  │      │ Alert │     │
│                      │ Processing │      │ Check │     │
│                      └─────┬─────┘      └────┬──┘     │
│                            │                  │        │
│        ┌───────────────────┼──────────────────┤        │
│        │                   │                  │        │
│    ┌───▼──┐          ┌─────▼──┐        ┌────▼──┐      │
│    │ Event │          │Telegram│        │Storage │     │
│    │Logging│          │ Alert  │        │Snapshot │    │
│    └───────┘          └────────┘        └────────┘     │
│        │                   │                  │        │
│    ┌───▼──────────────────▼──────────────────▼──┐      │
│    │      Dashboard (HTML + Statistics)         │      │
│    └─────────────────────────────────────────────┘     │
│                                                         │
│    📊 Deployment Manager                              │
│    ├─ Configuration Management                        │
│    ├─ System Monitoring                               │
│    └─ Health Checks                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📦 Features

### 🎥 **Live RTSP Camera Module**
- RTSP stream support for IP cameras
- Webcam fallback support
- Configurable resolution and FPS
- Threaded frame buffering for smooth operation

### 📊 **Dashboard**
- Real-time statistics tracking
- Detection history (last 100 detections)
- Animal count breakdown
- HTML visualization
- Auto-refresh web interface

### 🚨 **Telegram Alerts**
- Real-time detection notifications
- Alert throttling to prevent spam
- Configurable confidence thresholds
- Photo attachments with detections
- Status updates and summaries

### 📝 **Event Logging**
- SQLite database for all detections
- Detailed event tracking
- Export to JSON format
- Statistical analysis
- Historical data retention

### 📸 **Snapshot Storage**
- Automatic detection snapshots
- Organized by animal class and date
- Configurable storage limits
- Auto-cleanup of old files
- Archive functionality

### 🚀 **Deployment**
- Configuration management (YAML/JSON)
- System health monitoring
- Docker support (Dockerfile + docker-compose)
- Resource tracking (CPU, Memory, Disk)
- Deployment logging

## 🛠️ Installation

### 1. **Clone Repository**
```bash
cd d:\RD\Animal_Detection_YOLOV8
```

### 2. **Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Configure Environment**
Create a `.env` file in the project root:
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Optional: Camera Configuration
RTSP_URL=rtsp://ip:port/stream
CAMERA_TYPE=webcam  # or rtsp
```

## 🚀 Usage

### Basic Usage
```bash
python main_integrated.py
```

### With Configuration File
Create `deployment_config.json`:
```json
{
  "name": "Animal Detection System",
  "version": "1.0.0",
  "environment": "production",
  "camera": {
    "type": "webcam",
    "fps": 30
  },
  "model": {
    "path": "runs/detect/train/weights/best.pt",
    "confidence": 0.6
  },
  "telegram": {
    "enabled": true,
    "bot_token": "YOUR_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  },
  "alerts": {
    "confidence_threshold": 0.7,
    "daily_limit": 50
  }
}
```

### Keyboard Controls
- `q` - Quit application
- `s` - Save manual snapshot
- `r` - Reset statistics

## 📂 Project Structure

```
Animal_Detection_YOLOV8/
├── main_integrated.py          # Main application
├── camera.py                   # Camera module (RTSP/Webcam)
├── dashboard.py                # Dashboard & statistics
├── telegram_alerts.py          # Telegram notifications
├── event_logging.py            # Event & detection logging
├── snapshot_storage.py         # Snapshot management
├── deployment.py               # Deployment & config
├── model.py                    # Model utilities
├── requirements.txt            # Dependencies
├── deployment_config.json      # Configuration file
├── logs/                       # Log files
├── snapshots/                  # Stored snapshots
│   ├── detections/
│   ├── alerts/
│   └── archive/
├── runs/                       # Training/detection runs
├── Dockerfile                  # Docker containerization
└── docker-compose.yml          # Docker compose config
```

## 📊 Module Documentation

### Camera Module (`camera.py`)
```python
from camera import WebcamCamera, RTSPCamera

# Webcam
camera = WebcamCamera()
camera.connect()
frame = camera.get_frame()

# RTSP
rtsp_camera = RTSPCamera("rtsp://192.168.1.100:554/stream")
rtsp_camera.connect()
rtsp_camera.start_stream()
frame = rtsp_camera.get_frame()
```

### Dashboard Module (`dashboard.py`)
```python
from dashboard import Dashboard, HTMLDashboard

dashboard = Dashboard()
dashboard.record_detection("Lion", 0.95, (100, 100, 200, 200))
stats = dashboard.get_statistics()

# Generate HTML
html = HTMLDashboard.generate_html(stats)
```

### Telegram Alerts (`telegram_alerts.py`)
```python
from telegram_alerts import TelegramBot, AlertManager

bot = TelegramBot("BOT_TOKEN", "CHAT_ID")
bot.test_connection()
bot.alert_detection("Lion", 0.95, "snapshot.jpg")

# With alert management
alert_manager = AlertManager(bot)
alert_manager.set_confidence_threshold(0.7)
if alert_manager.should_alert(0.95, "Lion"):
    bot.alert_detection("Lion", 0.95)
```

### Event Logging (`event_logging.py`)
```python
from event_logging import EventLogger

logger = EventLogger("logs")
logger.log_detection("Lion", 0.95, (100, 100, 200, 200))
logger.log_event("Detection", "Lion detected", "INFO")

history = logger.get_detection_history(limit=50)
stats = logger.get_statistics(days=7)
logger.export_to_json("export.json")
```

### Snapshot Storage (`snapshot_storage.py`)
```python
from snapshot_storage import SnapshotManager

manager = SnapshotManager("snapshots")
path = manager.save_detection_snapshot(frame, "Lion", 0.95, coords)
snapshots = manager.get_snapshots_for_class("Lion", limit=10)

# Cleanup
manager.cleanup_old_files(days=7)
manager.archive_old_snapshots(days=30)
stats = manager.get_statistics()
```

### Deployment (`deployment.py`)
```python
from deployment import DeploymentConfig, DeploymentManager

config = DeploymentConfig()
config.update_config({"model": {"confidence": 0.7}})

manager = DeploymentManager()
manager.start_deployment()
info = manager.monitor.get_system_info()
manager.health_check()
manager.export_deployment_info()
```

## 🐳 Docker Deployment

### Build and Run
```bash
docker-compose up -d
```

### Stop
```bash
docker-compose down
```

## 📈 Monitoring

### View Logs
```bash
# Real-time logs
tail -f logs/detection_YYYYMMDD.log

# Database query
sqlite3 logs/detections.db "SELECT * FROM detections LIMIT 10;"
```

### Dashboard
- Auto-generated HTML dashboard at `dashboard_output/index.html`
- Auto-refreshes every 5 seconds
- Shows real-time statistics and detection history

### System Health
```python
from deployment import SystemMonitor

monitor = SystemMonitor()
info = monitor.get_system_info()
print(f"CPU: {info['cpu_percent']}%")
print(f"Memory: {info['memory']['percent']}%")
```

## ⚙️ Configuration Options

### Camera Settings
- `type`: "webcam" or "rtsp"
- `url`: RTSP stream URL (if type=rtsp)
- `fps`: Frame rate (default: 30)

### Model Settings
- `path`: Path to YOLOv8 weights file
- `confidence`: Detection confidence threshold (0.0-1.0)

### Alert Settings
- `confidence_threshold`: Minimum confidence for alerts
- `daily_limit`: Maximum alerts per day
- `hourly_limit`: Maximum alerts per hour

### Storage Settings
- `snapshots_dir`: Directory for snapshots
- `logs_dir`: Directory for logs
- `max_storage_gb`: Maximum storage before cleanup

## 🔧 Troubleshooting

### Camera Connection Issues
```python
# Test camera connection
camera = WebcamCamera()
if camera.connect():
    print("✅ Camera connected")
else:
    print("❌ Camera failed to connect")
```

### Telegram Not Sending Messages
```python
bot = TelegramBot(TOKEN, CHAT_ID)
if bot.test_connection():
    print("✅ Telegram connected")
else:
    print("❌ Telegram connection failed")
```

### Model Loading Errors
- Ensure weights file exists at specified path
- Check YOLOv8 installation: `pip install --upgrade ultralytics`
- Verify PyTorch installation: `pip install torch torchvision`

### Memory Issues
- Reduce frame resolution in config
- Reduce FPS
- Enable automatic cleanup: `manager.cleanup_old_files(days=3)`

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

Created for real-time animal detection and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Last Updated:** 2024
**Status:** ✅ Production Ready
