# 🔧 TROUBLESHOOTING & BEST PRACTICES GUIDE

## 🐛 Common Issues & Solutions

### 1. **Camera Connection Issues**

#### Problem: Camera fails to connect
```python
from camera import WebcamCamera
camera = WebcamCamera()
if not camera.connect():
    print("❌ Failed to connect")
```

**Solutions:**
- Check if camera device is available: `ls /dev/video*` (Linux) or Device Manager (Windows)
- Try different camera index: `WebcamCamera(camera_index=1)`
- Close other applications using the camera
- Check permissions: `sudo usermod -a -G video $USER` (Linux)
- Restart the computer

#### Problem: RTSP connection timeout
```python
from camera import RTSPCamera
rtsp_camera = RTSPCamera("rtsp://192.168.1.100:554/stream")
# May timeout if URL is incorrect or camera is offline
```

**Solutions:**
- Verify RTSP URL format: `rtsp://[IP]:[PORT]/[STREAM]`
- Check camera is powered on and connected
- Test URL with VLC: `File → Open Network Stream → paste URL`
- Verify network connectivity: `ping 192.168.1.100`
- Check firewall rules allow RTSP (port 554 by default)
- Try with credentials: `rtsp://user:pass@192.168.1.100:554/stream`

---

### 2. **Model Loading Issues**

#### Problem: Model weights not found
```
FileNotFoundError: runs/detect/train/weights/best.pt not found
```

**Solutions:**
```bash
# Verify file exists
ls -la runs/detect/train/weights/

# If missing, download or train model
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Use pretrained model
results = model.train(data='dataset.yaml', epochs=100)
```

#### Problem: GPU out of memory
```
RuntimeError: CUDA out of memory
```

**Solutions:**
```json
{
  "model": {
    "device": "cpu",
    "half_precision": true
  }
}
```

Or reduce batch size or image resolution.

#### Problem: Model inference is slow
```python
# Check device being used
from ultralytics import YOLO
model = YOLO('best.pt')
print(model.device)  # Should show GPU if available
```

**Solutions:**
- Enable GPU: Install CUDA/cuDNN
- Reduce image resolution
- Lower FPS in config
- Use lighter model (yolov8n instead of yolov8x)

---

### 3. **Telegram Integration Issues**

#### Problem: Bot token invalid
```
Telegram connection failed
```

**Solutions:**
1. Verify token format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`
2. Get new token from BotFather:
   - Chat with @BotFather
   - Command: `/newbot`
   - Copy token
3. Test connection:
```python
from telegram_alerts import TelegramBot
bot = TelegramBot("YOUR_TOKEN", "YOUR_CHAT_ID")
if bot.test_connection():
    print("✅ Connected")
```

#### Problem: Chat ID not found
```
Failed to send message
```

**Solutions:**
1. Get your chat ID:
   - Send any message to your bot
   - Visit: `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
   - Find your `"chat":{"id":123456789}`
2. Update `.env`:
```env
TELEGRAM_CHAT_ID=123456789
```

#### Problem: Messages not being sent
```python
# Check if message is being rate-limited
```

**Solutions:**
- Add delay between messages: `time.sleep(1)`
- Check alert thresholds aren't too restrictive
- Verify internet connection
- Check Telegram app is still receiving messages

---

### 4. **Storage & Performance Issues**

#### Problem: Disk space running out
```
No space left on device
```

**Solutions:**
```python
from snapshot_storage import SnapshotManager

manager = SnapshotManager()

# Cleanup old files
deleted = manager.cleanup_old_files(days=7)
print(f"Deleted {deleted} files")

# Check usage
usage = manager.get_storage_usage()
print(f"Storage: {usage:.2f} GB")

# Archive instead of delete
archived = manager.archive_old_snapshots(days=30)
```

Or update config:
```json
{
  "storage": {
    "max_storage_gb": 5,
    "retention_days": 3
  }
}
```

#### Problem: High memory usage
```
Python process consuming 80%+ memory
```

**Solutions:**
1. Reduce frame buffer size:
```python
rtsp_camera = RTSPCamera(url, buffer_size=1)  # Smaller buffer
```

2. Lower resolution:
```json
{
  "camera": {
    "resolution": {"width": 480, "height": 360}
  }
}
```

3. Reduce FPS:
```json
{
  "camera": {
    "fps": 15
  }
}
```

4. Use Python memory profiler:
```python
from memory_profiler import profile

@profile
def process_frame():
    # Code here
    pass
```

#### Problem: CPU usage at 100%
```
System unresponsive
```

**Solutions:**
1. Reduce model complexity:
```python
model = YOLO('yolov8n.pt')  # nano model
```

2. Lower detection frequency:
```python
if frame_count % 3 == 0:  # Process every 3rd frame
    results = model(frame)
```

3. Reduce resolution or FPS
4. Use threading for non-blocking operations

---

### 5. **Database Issues**

#### Problem: SQLite database locked
```
database is locked
```

**Solutions:**
```python
# Close existing connections
# Check if another process is using database

# Temporary workaround - enable timeout
import sqlite3
conn = sqlite3.connect('logs/detections.db', timeout=10.0)
```

#### Problem: Database file corrupt
```
database disk image is malformed
```

**Solutions:**
```python
import sqlite3

try:
    conn = sqlite3.connect('logs/detections.db')
    conn.execute('PRAGMA integrity_check')
except Exception as e:
    print(f"❌ Database corrupt: {e}")
    # Backup old and create new
    import shutil
    shutil.copy('logs/detections.db', 'logs/detections.db.backup')
    # System will create new database on next run
```

---

### 6. **Docker Issues**

#### Problem: Container won't start
```
docker-compose up fails
```

**Solutions:**
```bash
# Check logs
docker-compose logs animal-detection

# Check if port is already in use
lsof -i :5000

# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up
```

#### Problem: GPU not available in container
```
CUDA not available in Docker
```

**Solutions:**
```yaml
# docker-compose.yml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

Ensure NVIDIA Docker runtime is installed.

#### Problem: Volume permission denied
```
Permission denied: /app/logs
```

**Solutions:**
```bash
# Check volume permissions
docker-compose exec animal-detection ls -la /app/logs

# Fix permissions
sudo chown -R $(id -u):$(id -g) ./logs ./snapshots
```

---

## ✅ Best Practices

### 1. **Configuration Management**

✅ **DO:**
```python
# Use configuration file
config = DeploymentConfig("deployment_config.json")
confidence = config.get_value("model.confidence", 0.6)
```

❌ **DON'T:**
```python
# Hardcode values
confidence = 0.6  # What if you want to change it?
```

### 2. **Error Handling**

✅ **DO:**
```python
try:
    camera = WebcamCamera()
    if camera.connect():
        # Use camera
        pass
except Exception as e:
    logger.error(f"Camera error: {str(e)}")
    # Fallback logic
```

❌ **DON'T:**
```python
camera = WebcamCamera()
camera.connect()  # No error checking
frame = camera.get_frame()
```

### 3. **Logging**

✅ **DO:**
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Detection completed")
logger.warning("Confidence low")
logger.error("Camera failed")

# Also log to database
event_logger.log_event("Detection", "Found lion", "INFO")
```

❌ **DON'T:**
```python
print("Detection: Lion")  # Not searchable, not timestamped
```

### 4. **Resource Management**

✅ **DO:**
```python
camera = WebcamCamera()
try:
    # Use camera
    pass
finally:
    camera.release()  # Always cleanup
```

❌ **DON'T:**
```python
camera = WebcamCamera()
# Use camera
# Forget to cleanup - resource leak
```

### 5. **Testing**

✅ **DO:**
```python
def test_camera_connection():
    camera = WebcamCamera()
    assert camera.connect(), "Camera connection failed"
    frame = camera.get_frame()
    assert frame is not None, "Failed to read frame"
    camera.release()

def test_telegram_connection():
    bot = TelegramBot("TOKEN", "CHAT_ID")
    assert bot.test_connection(), "Telegram failed"

test_camera_connection()
test_telegram_connection()
print("✅ All tests passed")
```

❌ **DON'T:**
```python
# No testing
# Hope it works
```

### 6. **Monitoring**

✅ **DO:**
```python
monitor = SystemMonitor()
while True:
    info = monitor.get_system_info()
    if info['cpu_percent'] > 90:
        logger.warning("High CPU usage")
    if info['memory']['percent'] > 85:
        logger.warning("High memory usage")
    # Take action
```

❌ **DON'T:**
```python
# Ignore system resources
# System crashes due to OOM
```

### 7. **Data Management**

✅ **DO:**
```python
# Regularly backup
snapshot_manager.archive_old_snapshots(days=30)
snapshot_manager.cleanup_old_files(days=7)

# Export periodically
event_logger.export_to_json("exports/weekly_export.json")
```

❌ **DON'T:**
```python
# Accumulate everything
# Eventually run out of disk space
```

### 8. **Security**

✅ **DO:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
# Token is now in environment, not in code
```

❌ **DON'T:**
```python
telegram_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
# Exposed in source code!
```

---

## 🚀 Performance Optimization Tips

### 1. **FPS vs Accuracy Trade-off**
```json
{
  "fast_mode": {
    "camera": {"fps": 10},
    "model": {"confidence": 0.8}
  },
  "accurate_mode": {
    "camera": {"fps": 30},
    "model": {"confidence": 0.5}
  }
}
```

### 2. **Batch Processing**
```python
# Instead of processing every frame
if frame_count % 3 == 0:  # Every 3rd frame
    results = model(frame)
    # Process detections
```

### 3. **Caching**
```python
# Cache model results
from functools import lru_cache

@lru_cache(maxsize=128)
def get_class_name(cls_id):
    return model.names[cls_id]
```

### 4. **Async Operations**
```python
import threading
from queue import Queue

# Process alerts in background
alert_queue = Queue()

def process_alerts():
    while True:
        alert = alert_queue.get()
        telegram_bot.send_alert(alert)

alert_thread = threading.Thread(target=process_alerts, daemon=True)
alert_thread.start()
```

---

## 📊 Monitoring Dashboard

### Key Metrics to Track
1. **Detection Rate**: Detections per hour
2. **Accuracy**: Average confidence of detections
3. **System Health**: CPU, Memory, Disk
4. **Alert Activity**: Alerts sent per day
5. **Storage Usage**: GB used
6. **Uptime**: Hours since start

```python
from deployment import SystemMonitor

monitor = SystemMonitor()
stats = monitor.get_system_info()

print(f"CPU: {stats['cpu_percent']}%")
print(f"Memory: {stats['memory']['percent']}%")
print(f"Disk: {stats['disk']['percent']}%")
```

---

## 🔍 Debugging Tips

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Add Debug Prints
```python
frame_count = 0
for frame in frames:
    frame_count += 1
    if frame_count % 100 == 0:
        print(f"Processed {frame_count} frames")
```

### Use Python Debugger
```python
import pdb

# Set breakpoint
pdb.set_trace()

# Commands:
# n - next line
# c - continue
# p variable - print variable
# h - help
```

---

## 🎓 Learning Resources

- **YOLOv8 Docs**: https://docs.ultralytics.com
- **OpenCV Tutorials**: https://docs.opencv.org
- **SQLite Guide**: https://sqlite.org/docs.html
- **Python Logging**: https://docs.python.org/3/library/logging.html
- **Telegram Bot API**: https://core.telegram.org/bots/api

---

**Last Updated**: 2024
**Status**: ✅ Complete
