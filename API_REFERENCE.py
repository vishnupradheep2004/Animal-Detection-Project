"""
API Reference and Usage Examples
Animal Detection System v1.0
"""

# ============================================
# CAMERA MODULE USAGE EXAMPLES
# ============================================

"""
WEBCAM USAGE
"""
from camera import WebcamCamera

# Initialize and connect
webcam = WebcamCamera(camera_index=0)
if webcam.connect():
    print("✅ Webcam connected")
    
    # Get frames
    for i in range(100):
        frame = webcam.get_frame()
        if frame is not None:
            print(f"Frame {i} received: {frame.shape}")

# Cleanup
webcam.release()


"""
RTSP CAMERA USAGE
"""
from camera import RTSPCamera

# Initialize RTSP camera
rtsp_cam = RTSPCamera("rtsp://192.168.1.100:554/stream", buffer_size=2)

if rtsp_cam.connect():
    # Start streaming in background
    rtsp_cam.start_stream()
    print("✅ RTSP stream started")
    
    # Get frames
    for i in range(100):
        frame = rtsp_cam.get_frame()
        if frame is not None:
            print(f"Frame {i} received: {frame.shape}")

# Cleanup
rtsp_cam.stop_stream()


# ============================================
# DASHBOARD & STATISTICS USAGE
# ============================================

"""
BASIC DASHBOARD USAGE
"""
from dashboard import Dashboard, HTMLDashboard
import json

# Initialize dashboard
dashboard = Dashboard(stats_file="dashboard_stats.json")

# Record detections
dashboard.record_detection("Lion", 0.95, (100, 100, 200, 200))
dashboard.record_detection("Rabbit", 0.87, (300, 300, 350, 350))
dashboard.record_detection("Lion", 0.92, (150, 150, 250, 250))

# Get summary
summary = dashboard.get_summary()
print("Detection Summary:")
print(json.dumps(summary, indent=2))

# Get full statistics
stats = dashboard.get_statistics()
print(f"Total Detections: {stats['total_detections']}")
print(f"Animals: {stats['animals_detected']}")

# Generate HTML dashboard
html_content = HTMLDashboard.generate_html(stats)
with open("dashboard.html", "w") as f:
    f.write(html_content)

# Reset statistics
dashboard.reset_stats()


# ============================================
# TELEGRAM ALERTS USAGE
# ============================================

"""
BASIC TELEGRAM BOT
"""
from telegram_alerts import TelegramBot

# Initialize bot
bot = TelegramBot(
    bot_token="YOUR_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID"
)

# Test connection
if bot.test_connection():
    print("✅ Telegram connected")
    
    # Send message
    bot.send_message("🦁 System started!")
    
    # Send detection alert
    bot.alert_detection("Lion", 0.95, image_path="snapshot.jpg")
    
    # Send status update
    status = {
        "Lion": 5,
        "Rabbit": 3
    }
    bot.send_status_update(total_detections=8, animals_dict=status)


"""
ALERT MANAGER WITH THROTTLING
"""
from telegram_alerts import TelegramBot, AlertManager

bot = TelegramBot("BOT_TOKEN", "CHAT_ID")
alert_mgr = AlertManager(telegram_bot=bot)

# Configure thresholds
alert_mgr.set_confidence_threshold(0.7)
alert_mgr.set_daily_limit(100)

# Check if alert should be sent
detections = [
    ("Lion", 0.95),
    ("Lion", 0.92),
    ("Lion", 0.88),
]

for animal, confidence in detections:
    if alert_mgr.should_alert(confidence, animal):
        bot.alert_detection(animal, confidence)
        print(f"✅ Alert sent for {animal}")
    else:
        print(f"⏭️  Alert skipped for {animal} (throttled)")


# ============================================
# EVENT LOGGING USAGE
# ============================================

"""
BASIC EVENT LOGGING
"""
from event_logging import EventLogger
import json

# Initialize logger
logger = EventLogger(log_dir="logs")

# Log detections
detection_id = logger.log_detection(
    class_name="Lion",
    confidence=0.95,
    coordinates=(100, 100, 200, 200),
    image_path="snapshots/lion_123.jpg",
    alert_sent=True
)
print(f"Detection logged with ID: {detection_id}")

# Log events
logger.log_event(
    event_type="System",
    description="Detection system started",
    severity="INFO"
)

logger.log_event(
    event_type="Error",
    description="Camera disconnected",
    severity="WARNING"
)

# Retrieve history
history = logger.get_detection_history(limit=50)
print(f"Found {len(history)} recent detections")
for det in history[:5]:
    print(f"  - {det['class_name']}: {det['confidence']:.2%}")

# Get statistics
stats = logger.get_statistics(days=7)
print(f"\nStatistics (last 7 days):")
print(f"  Total: {stats['total']}")
print(f"  Unique Animals: {stats['unique_animals']}")
print(f"  Avg Confidence: {stats['avg_confidence']:.2%}")
print(f"  By Class: {stats['detections_by_class']}")

# Export to JSON
logger.export_to_json("export.json", limit=1000)


# ============================================
# SNAPSHOT STORAGE USAGE
# ============================================

"""
SNAPSHOT MANAGEMENT
"""
from snapshot_storage import SnapshotManager
import cv2

# Initialize manager
snapshot_mgr = SnapshotManager(storage_dir="snapshots")

# Save detection snapshot
frame = cv2.imread("test_frame.jpg")
snapshot_path = snapshot_mgr.save_detection_snapshot(
    frame=frame,
    class_name="Lion",
    confidence=0.95,
    coordinates=(100, 100, 200, 200)
)
print(f"✅ Snapshot saved: {snapshot_path}")

# Save alert snapshot
alert_path = snapshot_mgr.save_alert_snapshot(
    frame=frame,
    class_name="Lion",
    confidence=0.95
)

# Get snapshots for a class
lion_snapshots = snapshot_mgr.get_snapshots_for_class("Lion", limit=10)
print(f"Found {len(lion_snapshots)} Lion snapshots")

# Check storage usage
storage_gb = snapshot_mgr.get_storage_usage()
print(f"Storage used: {storage_gb:.2f} GB")

# Get statistics
stats = snapshot_mgr.get_statistics()
print(f"Statistics: {stats}")

# Cleanup old files
deleted = snapshot_mgr.cleanup_old_files(days=7)
print(f"Deleted {deleted} old snapshots")

# Archive old snapshots
archived = snapshot_mgr.archive_old_snapshots(days=30)
print(f"Archived {archived} snapshots")


# ============================================
# DEPLOYMENT & CONFIGURATION USAGE
# ============================================

"""
CONFIGURATION MANAGEMENT
"""
from deployment import DeploymentConfig
import json

# Load configuration
config = DeploymentConfig("deployment_config.json")

# Get values
camera_type = config.get_value("camera.type", "webcam")
model_path = config.get_value("model.path")
confidence = config.get_value("model.confidence", 0.6)

print(f"Camera Type: {camera_type}")
print(f"Model: {model_path}")
print(f"Confidence: {confidence:.2%}")

# Update configuration
config.update_config({
    "model": {
        "confidence": 0.7
    },
    "alerts": {
        "daily_limit": 100
    }
})

print("✅ Configuration updated")


"""
SYSTEM MONITORING & DEPLOYMENT
"""
from deployment import DeploymentManager, SystemMonitor

# Initialize manager
mgr = DeploymentManager()

# Start deployment
if mgr.start_deployment():
    print("✅ Deployment started")
    
    # Get system info
    info = mgr.monitor.get_system_info()
    print(f"CPU: {info['cpu_percent']}%")
    print(f"Memory: {info['memory']['percent']}%")
    
    # Health check
    is_healthy = mgr.health_check()
    if is_healthy:
        print("✅ Health check passed")
    
    # Export deployment info
    mgr.export_deployment_info("deployment_info.json")
    print("✅ Deployment info exported")
    
    # Stop deployment
    mgr.stop_deployment()
    print("⛔ Deployment stopped")


# ============================================
# COMPLETE WORKFLOW EXAMPLE
# ============================================

"""
FULL INTEGRATION EXAMPLE
"""
import cv2
from ultralytics import YOLO
from camera import WebcamCamera
from dashboard import Dashboard
from telegram_alerts import TelegramBot, AlertManager
from event_logging import EventLogger
from snapshot_storage import SnapshotManager

def process_frame_workflow():
    """Complete detection workflow"""
    
    # Initialize components
    camera = WebcamCamera()
    model = YOLO("best.pt")
    dashboard = Dashboard()
    logger = EventLogger()
    snapshots = SnapshotManager()
    bot = TelegramBot("TOKEN", "CHAT_ID")
    alerts = AlertManager(bot)
    
    # Connect camera
    if not camera.connect():
        print("❌ Camera connection failed")
        return
    
    frame_count = 0
    
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        
        frame_count += 1
        
        # Run detection
        results = model(frame, conf=0.6)
        
        # Process results
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                confidence = float(box.conf[0])
                cls_id = int(box.cls[0])
                class_name = r.names[cls_id]
                
                # Log detection
                detection_id = logger.log_detection(
                    class_name=class_name,
                    confidence=confidence,
                    coordinates=(x1, y1, x2, y2)
                )
                
                # Save snapshot
                snapshot_path = snapshots.save_detection_snapshot(
                    frame, class_name, confidence, (x1, y1, x2, y2)
                )
                
                # Update dashboard
                dashboard.record_detection(
                    class_name, confidence, (x1, y1, x2, y2)
                )
                
                # Send alert if threshold met
                if alerts.should_alert(confidence, class_name):
                    bot.alert_detection(class_name, confidence, snapshot_path)
        
        # Update dashboard HTML every 30 frames
        if frame_count % 30 == 0:
            from dashboard import HTMLDashboard
            html = HTMLDashboard.generate_html(dashboard.get_statistics())
            with open("dashboard.html", "w") as f:
                f.write(html)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    camera.release()
    cv2.destroyAllWindows()
    logger.export_to_json("final_detections.json")

    print("✅ Workflow completed")


if __name__ == "__main__":
    print("Animal Detection System - API Reference")
    print("For examples, import and run the functions above")
