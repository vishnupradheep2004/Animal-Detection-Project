"""
Integrated main application
Combines camera input, YOLO model, dashboard, alerts, logging, and snapshot storage.
"""
import time
import threading
import logging
from pathlib import Path

from deployment import DeploymentConfig
from camera import RTSPCamera, WebcamCamera
from dashboard import Dashboard, HTMLDashboard
from telegram_alerts import TelegramBot, AlertManager
from event_logging import EventLogger, setup_logging
from snapshot_storage import SnapshotManager

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None

# Compatibility shim for Python versions where pkgutil.get_loader was removed
import pkgutil
import importlib.util
if not hasattr(pkgutil, 'get_loader'):
    def _compat_get_loader(name):
        try:
            spec = importlib.util.find_spec(name)
            return spec.loader if spec is not None else None
        except Exception:
            return None
    pkgutil.get_loader = _compat_get_loader

from flask import Flask, Response

setup_logging()
logger = logging.getLogger("main_integrated")


class IntegratedApp:
    def __init__(self, config_file: str = "deployment_config.json"):
        self.config = DeploymentConfig(config_file)
        cfg = self.config.config

        # components
        self.dashboard = Dashboard(stats_file="dashboard_stats.json")
        self.snapshot_mgr = SnapshotManager(storage_dir=cfg.get("storage", {}).get("snapshots_dir", "snapshots"))
        self.event_logger = EventLogger(log_dir=cfg.get("storage", {}).get("logs_dir", "logs"))

        # Telegram
        tg = cfg.get("telegram", {})
        if tg.get("enabled") and tg.get("bot_token") and tg.get("chat_id"):
            self.telegram = TelegramBot(tg.get("bot_token"), tg.get("chat_id"))
            self.alert_mgr = AlertManager(self.telegram)
        else:
            self.telegram = None
            self.alert_mgr = AlertManager(None)

        # model
        model_path = cfg.get("model", {}).get("path", "runs/detect/train/weights/best.pt")
        self.confidence = cfg.get("model", {}).get("confidence", 0.6)
        if YOLO is not None and Path(model_path).exists():
            self.model = YOLO(model_path)
            logger.info(f"Loaded model: {model_path}")
        else:
            self.model = None
            logger.warning("YOLO model not available or path missing")

        # camera
        cam_cfg = cfg.get("camera", {})
        if cam_cfg.get("type") == "rtsp" and cam_cfg.get("url"):
            self.camera = RTSPCamera(cam_cfg.get("url"))
            self.camera.connect()
            self.camera.start_stream()
        else:
            self.camera = WebcamCamera(camera_index=0)
            self.camera.connect()

        self.running = False

    def _process_frame(self, frame):
        """Run inference and handle results"""
        if frame is None:
            return

        if self.model is None:
            return

        try:
            results = self.model(frame)
        except Exception as e:
            logger.error(f"Model inference error: {e}")
            return

        for r in results:
            boxes = getattr(r, 'boxes', [])
            for box in boxes:
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
                conf = float(box.conf[0]) if hasattr(box, 'conf') else 0.0
                cls_idx = int(box.cls[0]) if hasattr(box, 'cls') else 0
                class_name = "unknown"
                try:
                    class_name = self.model.names[cls_idx]
                except Exception:
                    pass

                # record
                self.dashboard.record_detection(class_name, conf, (x1, y1, x2, y2))
                img_path = self.snapshot_mgr.save_detection_snapshot(frame, class_name, conf, (x1, y1, x2, y2))
                detection_id = self.event_logger.log_detection(class_name, conf, (x1, y1, x2, y2), image_path=img_path)

                # alerts
                if self.alert_mgr.should_alert(conf, class_name):
                    if self.telegram and img_path:
                        self.telegram.alert_detection(class_name, conf, image_path=img_path)
                    elif self.telegram:
                        self.telegram.alert_detection(class_name, conf, image_path=None)

    def detection_loop(self):
        self.running = True
        logger.info("Detection loop starting")
        while self.running:
            # get frame
            if hasattr(self.camera, 'get_frame'):
                frame = self.camera.get_frame()
            else:
                frame = None

            if frame is None and hasattr(self.camera, 'cap'):
                ret, frame = self.camera.cap.read()

            if frame is None:
                time.sleep(0.05)
                continue

            self._process_frame(frame)
            time.sleep(0.01)

        logger.info("Detection loop stopped")

    def start(self):
        t = threading.Thread(target=self.detection_loop, daemon=True)
        t.start()
        logger.info("Integrated app started")


def create_dashboard_app(integrated: IntegratedApp):
    app = Flask(__name__)

    @app.route('/')
    def index():
        stats = integrated.dashboard.get_statistics()
        html = HTMLDashboard.generate_html(stats)
        return Response(html, mimetype='text/html')

    return app


def main():
    app = IntegratedApp()
    app.start()

    flask_app = create_dashboard_app(app)
    server_cfg = app.config.config.get('server', {})
    host = server_cfg.get('host', '0.0.0.0')
    port = server_cfg.get('port', 5000)
    debug = server_cfg.get('debug', False)

    flask_app.run(host=host, port=port, debug=debug, use_reloader=False)


if __name__ == '__main__':
    main()
"""
Animal Detection System - Main Application
Integrates YOLOv8 with real-time monitoring, alerts, and logging
"""

import cv2
import math
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

# Import custom modules
from camera import WebcamCamera, RTSPCamera
from dashboard import Dashboard, HTMLDashboard
from telegram_alerts import TelegramBot, AlertManager
from event_logging import EventLogger, setup_logging
from snapshot_storage import SnapshotManager
from deployment import DeploymentConfig, DeploymentManager

# Load environment variables
load_dotenv()

# Setup logging
setup_logging(logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
event_logger = EventLogger(log_dir="logs")
snapshot_manager = SnapshotManager(storage_dir="snapshots")
dashboard = Dashboard(stats_file="dashboard_stats.json")
deployment_config = DeploymentConfig(config_file="deployment_config.json")
deployment_manager = DeploymentManager(config_file="deployment_config.json")

# Initialize Telegram (optional)
telegram_bot = None
alert_manager = None

try:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN") or deployment_config.get_value("telegram.bot_token")
    chat_id = os.getenv("TELEGRAM_CHAT_ID") or deployment_config.get_value("telegram.chat_id")
    
    if bot_token and chat_id:
        telegram_bot = TelegramBot(bot_token, chat_id)
        alert_manager = AlertManager(telegram_bot)
        
        if telegram_bot.test_connection():
            logger.info("✅ Telegram bot connected")
            telegram_bot.send_message("🚀 Animal Detection System started!")
        else:
            logger.warning("⚠️ Telegram connection failed")
            telegram_bot = None
except Exception as e:
    logger.warning(f"Telegram initialization failed: {str(e)}")


def initialize_model():
    """Initialize YOLOv8 model"""
    try:
        from ultralytics import YOLO
        model_path = deployment_config.get_value("model.path", "runs/detect/train/weights/best.pt")
        model = YOLO(model_path)
        logger.info(f"✅ Model loaded from {model_path}")
        return model
    except Exception as e:
        logger.error(f"❌ Error loading model: {str(e)}")
        return None


def initialize_camera():
    """Initialize camera source"""
    try:
        camera_type = deployment_config.get_value("camera.type", "webcam")
        
        if camera_type == "rtsp":
            camera_url = deployment_config.get_value("camera.url")
            if not camera_url:
                logger.error("RTSP URL not configured")
                return None
            
            camera = RTSPCamera(camera_url)
            if camera.connect():
                camera.start_stream()
                logger.info(f"✅ RTSP Camera connected: {camera_url}")
                return camera
        else:
            camera = WebcamCamera()
            if camera.connect():
                logger.info("✅ Webcam connected")
                return camera
        
        return None
    except Exception as e:
        logger.error(f"❌ Error initializing camera: {str(e)}")
        return None


def draw_annotations(frame, detections, class_names):
    """Draw detection boxes and labels on frame"""
    for detection in detections:
        x1, y1, x2, y2 = detection['box']
        class_name = detection['class']
        confidence = detection['confidence']
        
        # Draw bounding box
        color = (0, 255, 0)  # Green
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        
        # Draw label
        label = f"{class_name} {confidence:.2%}"
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        
        # Draw background for label
        cv2.rectangle(frame, 
                     (int(x1), int(y1) - label_size[1] - 4),
                     (int(x1) + label_size[0], int(y1)),
                     color, -1)
        
        # Draw text
        cv2.putText(frame, label, (int(x1), int(y1) - 2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    return frame


def process_detections(frame, results, model_confidence_threshold):
    """Process model results and extract detections"""
    detections = []
    
    for r in results:
        boxes = r.boxes
        
        for box in boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            
            # Get confidence
            confidence = float(box.conf[0])
            
            # Skip low confidence detections
            if confidence < model_confidence_threshold:
                continue
            
            # Get class
            cls = int(box.cls[0])
            class_name = results[0].names[cls] if hasattr(results[0], 'names') else f"Class {cls}"
            
            detection = {
                'box': (x1, y1, x2, y2),
                'confidence': confidence,
                'class': class_name,
                'cls_id': cls
            }
            detections.append(detection)
            
            # Log detection
            event_logger.log_detection(
                class_name=class_name,
                confidence=confidence,
                coordinates=(x1, y1, x2, y2)
            )
            
            # Save snapshot
            snapshot_path = snapshot_manager.save_detection_snapshot(
                frame, class_name, confidence, (x1, y1, x2, y2)
            )
            
            # Update dashboard
            dashboard.record_detection(class_name, confidence, (x1, y1, x2, y2))
            
            # Handle alerts
            if alert_manager and alert_manager.should_alert(confidence, class_name):
                if telegram_bot:
                    telegram_bot.alert_detection(
                        class_name, confidence, snapshot_path
                    )
                logger.info(f"🚨 Alert sent for {class_name}")
    
    return detections


def save_dashboard_html():
    """Generate and save dashboard HTML"""
    try:
        stats = dashboard.get_statistics()
        html_content = HTMLDashboard.generate_html(stats)
        
        output_dir = Path("dashboard_output")
        output_dir.mkdir(exist_ok=True)
        
        html_file = output_dir / "index.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        logger.debug(f"Dashboard saved to {html_file}")
    except Exception as e:
        logger.error(f"Error saving dashboard: {str(e)}")


def main():
    """Main application loop"""
    logger.info("=" * 60)
    logger.info("🦁 ANIMAL DETECTION SYSTEM STARTED")
    logger.info("=" * 60)
    
    # Start deployment
    if not deployment_manager.start_deployment():
        logger.error("Failed to start deployment")
        return
    
    # Initialize model
    model = initialize_model()
    if model is None:
        logger.error("Failed to initialize model")
        event_logger.log_event("System", "Model initialization failed", "ERROR")
        return
    
    # Initialize camera
    camera = initialize_camera()
    if camera is None:
        logger.error("Failed to initialize camera")
        event_logger.log_event("System", "Camera initialization failed", "ERROR")
        return
    
    # Get configuration
    model_confidence = deployment_config.get_value("model.confidence", 0.6)
    
    logger.info("✅ System initialized successfully")
    logger.info("Press 'q' to quit")
    
    frame_count = 0
    
    try:
        while True:
            # Get frame
            if isinstance(camera, RTSPCamera):
                frame = camera.get_frame()
                if frame is None:
                    continue
            else:
                frame = camera.get_frame()
            
            if frame is None:
                logger.warning("Failed to read frame")
                continue
            
            frame_count += 1
            
            # Run inference
            results = model(frame, conf=model_confidence, verbose=False)
            
            # Process detections
            detections = process_detections(frame, results, model_confidence)
            
            # Draw annotations
            frame = draw_annotations(frame, detections, model.names if hasattr(model, 'names') else {})
            
            # Add frame info
            info_text = f"Frame: {frame_count} | Detections: {len(detections)}"
            cv2.putText(frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow("Animal Detection", frame)
            
            # Update dashboard every 30 frames
            if frame_count % 30 == 0:
                save_dashboard_html()
                
                # Periodic health check
                if frame_count % 300 == 0:
                    if not deployment_manager.health_check():
                        logger.warning("Health check failed")
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.info("Quit command received")
                break
            elif key == ord('s'):
                # Manual snapshot
                snapshot_manager.save_alert_snapshot(frame, "manual", 1.0)
                logger.info("Manual snapshot saved")
            elif key == ord('r'):
                # Reset statistics
                dashboard.reset_stats()
                logger.info("Statistics reset")
    
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
        event_logger.log_event("System", f"Error in main loop: {str(e)}", "ERROR")
    
    finally:
        # Cleanup
        logger.info("Cleaning up...")
        
        # Stop camera
        if isinstance(camera, RTSPCamera):
            camera.stop_stream()
        else:
            camera.release()
        
        # Close windows
        cv2.destroyAllWindows()
        
        # Send final status
        if telegram_bot:
            stats = dashboard.get_summary()
            message = f"🛑 System stopped\n"
            message += f"Total Detections: {stats['total_detections']}\n"
            for animal, count in stats['animals'].items():
                message += f"• {animal}: {count}\n"
            telegram_bot.send_message(message)
        
        # Stop deployment
        deployment_manager.stop_deployment()
        
        # Export logs
        event_logger.export_to_json("logs/final_export.json")
        
        # Export deployment info
        deployment_manager.export_deployment_info("deployment_final_info.json")
        
        logger.info("=" * 60)
        logger.info("🛑 SYSTEM SHUTDOWN COMPLETE")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
