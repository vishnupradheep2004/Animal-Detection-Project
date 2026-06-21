# 📚 ANIMAL DETECTION SYSTEM - COMPLETE INDEX

## 🎯 System Overview

This is a **production-ready animal detection system** using YOLOv8 with:
- ✅ Real-time RTSP/Webcam support
- ✅ Telegram alerts & notifications
- ✅ Web dashboard & statistics
- ✅ Comprehensive logging
- ✅ Snapshot management
- ✅ Docker deployment
- ✅ System monitoring

---

## 📖 Documentation Map

### 📋 **Getting Started**
1. **[QUICK_START.md](QUICK_START.md)** - Start here! Fast 5-minute setup
   - Installation steps
   - Running the system
   - Basic controls
   - Troubleshooting quick fixes

2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive setup guide
   - System architecture diagram
   - Feature descriptions
   - Installation instructions
   - Configuration options
   - Module documentation
   - Docker deployment
   - Monitoring & health checks

### 🔧 **Reference & Examples**
3. **[API_REFERENCE.py](API_REFERENCE.py)** - Complete API usage examples
   - Camera module examples
   - Dashboard usage
   - Telegram integration
   - Event logging
   - Snapshot management
   - Deployment configuration
   - Complete workflow example

4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project structure & analysis
   - Complete folder tree
   - Component descriptions
   - Integration flow
   - Database schema
   - Features summary
   - Performance metrics
   - Security considerations

### 🐛 **Troubleshooting**
5. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Issues & solutions
   - Common problems & fixes
   - Best practices
   - Performance optimization
   - Debugging tips
   - Learning resources

---

## 🗂️ File Structure

### Core Application Files
```
main.py                 Original detection script
main_integrated.py      ⭐ Main application (use this!)
model.py               Model utilities
camera.py              Camera module (RTSP + Webcam)
```

### Feature Modules
```
dashboard.py           Real-time dashboard & statistics
telegram_alerts.py     Telegram notifications
event_logging.py       Event & detection logging
snapshot_storage.py    Snapshot management
deployment.py          Configuration & monitoring
```

### Configuration Files
```
deployment_config.json Main configuration file
.env.example           Environment variables template
requirements.txt       Python dependencies
```

### Docker Files
```
Dockerfile            Container image
docker-compose.yml    Multi-container setup
nginx.conf           Web server config
```

### Documentation
```
SETUP_GUIDE.md        Detailed setup guide
QUICK_START.md        Quick reference
API_REFERENCE.py      Code examples
PROJECT_SUMMARY.md    Structure & overview
TROUBLESHOOTING.md    Issues & solutions
INDEX.md              This file!
```

---

## 🚀 Quick Start (5 minutes)

### 1. Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run
```bash
python main_integrated.py
```

### 4. Monitor
- Open `dashboard_output/index.html` in browser
- View logs: `tail -f logs/detection_*.log`
- Database: `sqlite3 logs/detections.db`

---

## 📊 Module Guide

### 🎥 **Camera Module** (`camera.py`)
```python
from camera import WebcamCamera, RTSPCamera

# Webcam
camera = WebcamCamera()
camera.connect()

# RTSP
rtsp = RTSPCamera("rtsp://192.168.1.100:554/stream")
rtsp.connect()
rtsp.start_stream()
```
- **Use for**: Camera input
- **Features**: Webcam, RTSP, threading, buffering
- **Config**: `camera.type`, `camera.url`, `camera.fps`

### 📊 **Dashboard Module** (`dashboard.py`)
```python
from dashboard import Dashboard

dashboard = Dashboard()
dashboard.record_detection("Lion", 0.95, (x1, y1, x2, y2))
stats = dashboard.get_statistics()
```
- **Use for**: Statistics tracking & HTML dashboard
- **Features**: Detection history, animal counts, auto-refresh
- **Output**: `dashboard_output/index.html`

### 🚨 **Telegram Module** (`telegram_alerts.py`)
```python
from telegram_alerts import TelegramBot, AlertManager

bot = TelegramBot("TOKEN", "CHAT_ID")
bot.alert_detection("Lion", 0.95, "snapshot.jpg")

alerts = AlertManager(bot)
alerts.set_confidence_threshold(0.7)
```
- **Use for**: Real-time notifications
- **Features**: Throttling, photo attachments, status updates
- **Config**: `telegram.bot_token`, `telegram.chat_id`

### 📝 **Logging Module** (`event_logging.py`)
```python
from event_logging import EventLogger

logger = EventLogger()
logger.log_detection("Lion", 0.95, coords)
logger.export_to_json("export.json")
```
- **Use for**: Comprehensive logging & analysis
- **Features**: SQLite DB, JSON export, statistics, queries
- **Output**: `logs/detections.db`, `logs/detection_*.log`

### 📸 **Storage Module** (`snapshot_storage.py`)
```python
from snapshot_storage import SnapshotManager

mgr = SnapshotManager()
path = mgr.save_detection_snapshot(frame, "Lion", 0.95, coords)
mgr.cleanup_old_files(days=7)
```
- **Use for**: Snapshot organization & management
- **Features**: Auto-organize, cleanup, archive, statistics
- **Output**: `snapshots/detections/`, `snapshots/alerts/`

### 🚀 **Deployment Module** (`deployment.py`)
```python
from deployment import DeploymentManager, DeploymentConfig

config = DeploymentConfig()
mgr = DeploymentManager()
mgr.health_check()
```
- **Use for**: Configuration & monitoring
- **Features**: Config management, system monitoring, Docker support
- **Config**: `deployment_config.json`

---

## ⚙️ Configuration Guide

### Main Config File (`deployment_config.json`)
```json
{
  "camera": {
    "type": "webcam",           // or "rtsp"
    "fps": 30,
    "resolution": {"width": 640, "height": 480}
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
    "daily_limit": 50,
    "hourly_limit": 10
  }
}
```

### Environment Variables (`.env`)
```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_id_here
CAMERA_TYPE=webcam
RTSP_URL=rtsp://...
MODEL_CONFIDENCE=0.6
```

---

## 🎮 Keyboard Controls

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `s` | Save manual snapshot |
| `r` | Reset statistics |

---

## 📈 Monitoring & Maintenance

### View Statistics
```python
from dashboard import Dashboard
dashboard = Dashboard()
print(dashboard.get_summary())
```

### View Logs
```bash
# Real-time
tail -f logs/detection_*.log

# Database queries
sqlite3 logs/detections.db
> SELECT class_name, COUNT(*) FROM detections GROUP BY class_name;
```

### Cleanup & Archival
```python
from snapshot_storage import SnapshotManager

mgr = SnapshotManager()
deleted = mgr.cleanup_old_files(days=7)        # Delete old files
archived = mgr.archive_old_snapshots(days=30)  # Archive old files
```

### Health Check
```python
from deployment import SystemMonitor

monitor = SystemMonitor()
info = monitor.get_system_info()
print(f"CPU: {info['cpu_percent']}%")
print(f"Memory: {info['memory']['percent']}%")
```

---

## 🐳 Docker Deployment

### Build & Run
```bash
docker-compose up -d
```

### Stop
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f animal-detection
```

### Access Dashboard
```
http://localhost:8080
```

---

## 🔐 Security Checklist

- [ ] Sensitive data in `.env` (not committed)
- [ ] Telegram token in environment variable
- [ ] RTSP password in URL if needed
- [ ] Database in secure location
- [ ] Firewall rules configured
- [ ] Docker secrets for production
- [ ] Regular backups enabled

---

## ⚠️ Common Issues & Quick Fixes

| Issue | Solution |
|-------|----------|
| Camera not connecting | Check permissions, try different index |
| Telegram not working | Verify token & chat ID |
| High CPU usage | Reduce FPS or resolution |
| Disk full | Run cleanup: `mgr.cleanup_old_files()` |
| Database locked | Close other connections |
| Model not loading | Verify file path exists |

**See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.**

---

## 📚 Learning Path

### Beginner
1. Read [QUICK_START.md](QUICK_START.md)
2. Run the system: `python main_integrated.py`
3. Check the dashboard
4. Review logs and database

### Intermediate
1. Read [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Review [API_REFERENCE.py](API_REFERENCE.py)
3. Customize configuration
4. Set up Telegram alerts
5. Deploy with Docker

### Advanced
1. Study [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. Understand database schema
3. Optimize performance
4. Implement custom modules
5. Production deployment

---

## 🔗 External Resources

- **YOLOv8 Documentation**: https://docs.ultralytics.com
- **OpenCV Guide**: https://docs.opencv.org
- **SQLite Reference**: https://sqlite.org
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Docker Docs**: https://docs.docker.com

---

## 📞 Support & Help

### Debug Information
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Also check:
# - logs/detection_*.log
# - logs/detections.db
# - System monitor: SystemMonitor().get_system_info()
```

### Common Questions

**Q: How do I use RTSP camera?**
A: Set `camera.type` to "rtsp" and provide RTSP URL in `.env` or config.

**Q: How do I get Telegram bot token?**
A: Chat @BotFather on Telegram, use `/newbot` command.

**Q: How do I reduce memory usage?**
A: Lower resolution, reduce FPS, use smaller model.

**Q: Can I run on GPU?**
A: Set `model.device` to "cuda" if NVIDIA GPU available.

**Q: How do I export data?**
A: Use `EventLogger().export_to_json()` or query SQLite directly.

---

## ✅ Deployment Checklist

- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created and configured
- [ ] Model weights downloaded
- [ ] Camera tested and working
- [ ] Telegram bot token obtained (if using alerts)
- [ ] Configuration reviewed
- [ ] Directories created (logs, snapshots, dashboard_output)
- [ ] First test run successful
- [ ] Dashboard accessible
- [ ] Logs being written
- [ ] Database populated
- [ ] Docker image built (if using Docker)

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Lines of Code | ~3,000+ |
| Modules | 6 feature modules |
| Database Tables | 2 (detections, events) |
| API Endpoints | 10+ |
| Configuration Options | 20+ |
| Documentation Pages | 5 |
| Code Examples | 50+ |

---

## 🎯 Key Features Summary

✅ **Real-time Detection**
- RTSP/Webcam support
- YOLOv8 inference
- Configurable thresholds

✅ **Monitoring & Alerts**
- Telegram notifications
- Alert throttling
- Status updates

✅ **Data Management**
- SQLite logging
- JSON export
- Snapshot storage
- Auto-cleanup

✅ **Dashboard & Analytics**
- Real-time statistics
- HTML visualization
- Detection history
- Storage analytics

✅ **Deployment**
- Docker support
- Configuration management
- System monitoring
- Health checks

✅ **Documentation**
- Setup guides
- API reference
- Troubleshooting
- Best practices

---

## 📝 Version Information

- **System**: Animal Detection System v1.0
- **Python**: 3.9+
- **YOLOv8**: 8.1.29+
- **Status**: ✅ Production Ready
- **Last Updated**: 2024

---

## 🙏 Next Steps

1. **Start**: Read [QUICK_START.md](QUICK_START.md)
2. **Run**: Execute `python main_integrated.py`
3. **Monitor**: View dashboard at `dashboard_output/index.html`
4. **Optimize**: Adjust configuration based on needs
5. **Deploy**: Use Docker for production

---

**Made with ❤️ for animal detection and monitoring**

*Questions? See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or check logs.*
