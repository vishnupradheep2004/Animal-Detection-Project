"""
Telegram Alerts Module
Send notifications to Telegram bot
"""

import requests
import logging
import time
from typing import Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TelegramBot:
    """Send alerts via Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram bot
        Args:
            bot_token: Telegram bot token from BotFather
            chat_id: Target chat ID for messages
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self.last_alert_time = {}
        self.alert_cooldown = 30  # seconds
        
    def send_message(self, message: str) -> bool:
        """Send text message to Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload, timeout=5)
            
            if response.status_code == 200:
                logger.info(f"Message sent to Telegram: {message[:50]}")
                return True
            else:
                logger.error(f"Failed to send message: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
            return False
    
    def send_photo(self, image_path: str, caption: str = "") -> bool:
        """Send photo to Telegram"""
        try:
            url = f"{self.api_url}/sendPhoto"
            with open(image_path, 'rb') as f:
                files = {'photo': f}
                payload = {
                    "chat_id": self.chat_id,
                    "caption": caption,
                    "parse_mode": "Markdown"
                }
                response = requests.post(url, files=files, data=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Photo sent to Telegram")
                return True
            else:
                logger.error(f"Failed to send photo: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending photo: {str(e)}")
            return False
    
    def alert_detection(self, class_name: str, confidence: float, 
                       image_path: Optional[str] = None) -> bool:
        """Send detection alert"""
        # Check cooldown
        if class_name in self.last_alert_time:
            if time.time() - self.last_alert_time[class_name] < self.alert_cooldown:
                return False
        
        message = f"🚨 *Detection Alert*\n"
        message += f"*Animal:* {class_name}\n"
        message += f"*Confidence:* {confidence:.2%}\n"
        message += f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        if image_path:
            self.send_photo(image_path, caption=message)
        else:
            self.send_message(message)
        
        self.last_alert_time[class_name] = time.time()
        return True
    
    def send_status_update(self, total_detections: int, animals_dict: dict) -> bool:
        """Send status update"""
        message = "📊 *Status Update*\n"
        message += f"*Total Detections:* {total_detections}\n\n"
        message += "*Animals Detected:*\n"
        
        for animal, count in animals_dict.items():
            message += f"• {animal}: {count}\n"
        
        message += f"\n*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """Test Telegram connection"""
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info("Telegram connection successful")
                return True
            else:
                logger.error("Telegram connection failed")
                return False
        except Exception as e:
            logger.error(f"Error testing Telegram connection: {str(e)}")
            return False


class AlertManager:
    """Manage alert thresholds and frequency"""
    
    def __init__(self, telegram_bot: Optional[TelegramBot] = None):
        self.bot = telegram_bot
        self.alert_thresholds = {
            "confidence_min": 0.6,
            "daily_limit": 50,
            "hourly_limit": 10
        }
        self.daily_count = 0
        self.hourly_count = 0
        self.last_hour_reset = datetime.now()
        self.last_day_reset = datetime.now()
    
    def should_alert(self, confidence: float, class_name: str) -> bool:
        """Determine if alert should be sent"""
        # Check confidence threshold
        if confidence < self.alert_thresholds["confidence_min"]:
            return False
        
        # Check hourly limit
        current_time = datetime.now()
        if current_time - self.last_hour_reset >= timedelta(hours=1):
            self.hourly_count = 0
            self.last_hour_reset = current_time
        
        if self.hourly_count >= self.alert_thresholds["hourly_limit"]:
            return False
        
        # Check daily limit
        if current_time - self.last_day_reset >= timedelta(days=1):
            self.daily_count = 0
            self.last_day_reset = current_time
        
        if self.daily_count >= self.alert_thresholds["daily_limit"]:
            return False
        
        self.hourly_count += 1
        self.daily_count += 1
        return True
    
    def set_confidence_threshold(self, threshold: float):
        """Set minimum confidence for alerts"""
        self.alert_thresholds["confidence_min"] = threshold
        logger.info(f"Confidence threshold set to {threshold:.2%}")
    
    def set_daily_limit(self, limit: int):
        """Set daily alert limit"""
        self.alert_thresholds["daily_limit"] = limit
        logger.info(f"Daily alert limit set to {limit}")
