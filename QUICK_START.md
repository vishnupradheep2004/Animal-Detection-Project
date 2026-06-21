# Animal Detection System - Quick Start Guide

## 📦 Installation & Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment
Copy `.env.example` to `.env` and fill in your settings:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- TELEGRAM_BOT_TOKEN: Your Telegram bot token
- TELEGRAM_CHAT_ID: Your Telegram chat ID
- CAMERA_TYPE: "webcam" or "rtsp"

### Step 3: Verify Model
Ensure the YOLOv8 model weights exist at:
```
runs/detect/train/weights/best.pt
```

## 🚀 Running the System

### Local Execution
```bash
python main_integrated.py
```

### Docker Execution
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f animal-detection

# Stop
docker-compose down
```

## 🎮 Controls

Press these keys while the application is running:
- **q** - Quit application
- **s** - Save manual snapshot
- **r** - Reset statistics

## 📊 Monitoring

### View Dashboard
Open `dashboard_output/index.html` in a web browser, or:
```bash
docker-compose up dashboard-server
# Visit http://localhost:8080
```

### View Logs
```bash
# Recent logs
tail -f logs/detection_*.log

# Database queries
sqlite3 logs/detections.db
> SELECT * FROM detections LIMIT 10;
> SELECT class_name, COUNT(*) FROM detections GROUP BY class_name;
```

### View Statistics
```python
from dashboard import Dashboard
dashboard = Dashboard()
print(dashboard.get_statistics())
```

## ⚙️ Configuration

### Edit Config File
Edit `deployment_config.json` to customize:
- Camera settings (type, FPS, resolution)
- Model confidence threshold
- Alert configuration
- Storage limits
- Telegram settings

Example configuration change:
```json
{
  "model": {
    "confidence": 0.7
  },
  "alerts": {
    "daily_limit": 100
  }
}
```

## 🐛 Troubleshooting

### Camera Not Working
```python
from camera import WebcamCamera
camera = WebcamCamera()
if camera.connect():
    print("✅ Camera OK")
    frame = camera.get_frame()
else:
    print("❌ Camera failed")
```

### Telegram Not Sending
```python
from telegram_alerts import TelegramBot
bot = TelegramBot("TOKEN", "CHAT_ID")
if bot.test_connection():
    print("✅ Telegram OK")
else:
    print("❌ Telegram failed - check token and chat ID")
```

### Model Not Loading
```bash
# Verify model exists
ls -la runs/detect/train/weights/best.pt

# Reinstall YOLOv8
pip install --upgrade ultralytics
```

### High Memory Usage
- Reduce resolution in config
- Lower FPS setting
- Enable snapshot cleanup: `manager.cleanup_old_files(days=3)`

## 📈 Performance Optimization

### For Faster Performance
```json
{
  "camera": {
    "resolution": {"width": 480, "height": 360},
    "fps": 15
  },
  "model": {
    "confidence": 0.7
  }
}
```

### For Better Detection
```json
{
  "camera": {
    "resolution": {"width": 1280, "height": 720},
    "fps": 30
  },
  "model": {
    "confidence": 0.5
  }
}
```

## 🔐 Security

1. Never commit `.env` file with real tokens
2. Use environment variables in production
3. Enable firewall rules for dashboard access
4. Rotate Telegram tokens regularly
5. Limit API access in deployment_config.json

## 📚 Additional Resources

- YOLOv8 Documentation: https://docs.ultralytics.com
- OpenCV Documentation: https://docs.opencv.org
- Telegram Bot API: https://core.telegram.org/bots/api

## 💡 Tips

1. **Test Camera Connection First**
   ```python
   from camera import WebcamCamera
   camera = WebcamCamera()
   camera.connect()
   ```

2. **Test Telegram Connection**
   ```python
   from telegram_alerts import TelegramBot
   bot = TelegramBot(TOKEN, CHAT_ID)
   bot.test_connection()
   ```

3. **Monitor Resource Usage**
   ```python
   from deployment import SystemMonitor
   monitor = SystemMonitor()
   print(monitor.get_system_info())
   ```

4. **Export Data for Analysis**
   ```python
   from event_logging import EventLogger
   logger = EventLogger()
   logger.export_to_json("analysis.json")
   ```

## 📞 Support

For issues:
1. Check logs: `logs/detection_*.log`
2. Check database: `sqlite3 logs/detections.db`
3. Review configuration: `deployment_config.json`
4. Check system resources: Use `SystemMonitor`

## ✅ Checklist

Before running:
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Model weights exist
- [ ] Camera is connected
- [ ] Telegram token is valid (if using alerts)
- [ ] Directories created (logs, snapshots)

## 🎯 Next Steps

1. Run the system: `python main_integrated.py`
2. Monitor dashboard: Open `dashboard_output/index.html`
3. Check logs: `tail -f logs/detection_*.log`
4. Fine-tune configuration based on results

---

**Status**: ✅ Ready for Production
