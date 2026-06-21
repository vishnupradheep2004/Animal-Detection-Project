"""
Live RTSP Camera Module
Handles camera input from RTSP streams and webcam
"""

import cv2
import logging
from threading import Thread
from queue import Queue
import time

logger = logging.getLogger(__name__)


class RTSPCamera:
    """Handle RTSP camera streams"""
    
    def __init__(self, rtsp_url: str, buffer_size: int = 1):
        self.rtsp_url = rtsp_url
        self.cap = None
        self.frame_queue = Queue(maxsize=buffer_size)
        self.is_running = False
        self.thread = None
        
    def connect(self) -> bool:
        """Connect to RTSP camera"""
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)
            if not self.cap.isOpened():
                logger.error(f"Failed to connect to RTSP: {self.rtsp_url}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            logger.info(f"Connected to RTSP: {self.rtsp_url}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to RTSP: {str(e)}")
            return False
    
    def start_stream(self):
        """Start streaming in background thread"""
        if self.cap is None:
            self.connect()
        
        self.is_running = True
        self.thread = Thread(target=self._stream_reader, daemon=True)
        self.thread.start()
        logger.info("RTSP stream started")
    
    def _stream_reader(self):
        """Read frames from camera continuously"""
        while self.is_running:
            ret, frame = self.cap.read()
            
            if not ret:
                logger.warning("Failed to read frame from RTSP")
                time.sleep(1)
                continue
            
            # Remove old frames if queue is full
            if self.frame_queue.full():
                try:
                    self.frame_queue.get_nowait()
                except:
                    pass
            
            self.frame_queue.put(frame)
    
    def get_frame(self):
        """Get latest frame from queue"""
        if not self.frame_queue.empty():
            return self.frame_queue.get()
        return None
    
    def stop_stream(self):
        """Stop streaming"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        if self.cap:
            self.cap.release()
        logger.info("RTSP stream stopped")


class WebcamCamera:
    """Handle webcam input"""
    
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap = None
        self.is_running = False
        
    def connect(self) -> bool:
        """Connect to webcam"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                logger.error(f"Failed to open webcam {self.camera_index}")
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            logger.info(f"Connected to webcam {self.camera_index}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to webcam: {str(e)}")
            return False
    
    def get_frame(self):
        """Get frame from webcam"""
        if self.cap is None or not self.cap.isOpened():
            return None
        
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def release(self):
        """Release webcam"""
        if self.cap:
            self.cap.release()
            logger.info("Webcam released")
