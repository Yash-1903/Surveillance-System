"""
Manages detection processes and alerts
"""
import time
import cv2
import numpy as np

class DetectionManager:
    def __init__(self, alert_panel):
        self.alert_panel = alert_panel
        self.last_alerts = {}
        self.alert_cooldown = 5  # seconds
        
    def process_detections(self, frame, detectors, feature_panel):
        """Process frame with enabled detectors"""
        detections = {}
        
        try:
            # Create a copy of the frame for processing
            processed_frame = frame.copy()
            
            if feature_panel.is_feature_enabled("Motion Detection"):
                processed_frame, detected, motion_data = detectors['motion'].detect(processed_frame)
                if detected:
                    self._handle_alert('motion', 'Motion Detected')
                    detections['motion'] = motion_data
            
            if feature_panel.is_feature_enabled("Fire Detection"):
                processed_frame, detected, fire_data = detectors['fire'].detect(processed_frame)
                if detected:
                    self._handle_alert('fire', 'Fire Detected!', high_priority=True)
                    detections['fire'] = fire_data
                    # Draw red overlay for fire detection
                    self._draw_alert_overlay(processed_frame, (0, 0, 255))
            
            if feature_panel.is_feature_enabled("Weapon Detection"):
                processed_frame, detected, weapon_data = detectors['weapon'].detect(processed_frame)
                if detected:
                    self._handle_alert('weapon', 'Weapon Detected!', high_priority=True)
                    detections['weapon'] = weapon_data
                    # Draw blue overlay for weapon detection
                    self._draw_alert_overlay(processed_frame, (255, 0, 0))
            
            if feature_panel.is_feature_enabled("Accident Detection"):
                processed_frame, detected, accident_data = detectors['accident'].detect(processed_frame)
                if detected:
                    self._handle_alert('accident', 'Accident Detected!', high_priority=True)
                    detections['accident'] = accident_data
                    # Draw orange overlay for accident detection
                    self._draw_alert_overlay(processed_frame, (0, 165, 255))
            
            if feature_panel.is_feature_enabled("Crowd Analysis"):
                processed_frame, detected, crowd_data = detectors['crowd'].detect(processed_frame)
                if detected and crowd_data.get('count', 0) > 10:
                    self._handle_alert('crowd', f"Large Crowd Detected: {crowd_data['count']} people")
                    detections['crowd'] = crowd_data
            
            return processed_frame, detections
            
        except Exception as e:
            print(f"Error processing detections: {str(e)}")
            return frame, {}
    
    def _handle_alert(self, alert_type, message, high_priority=False):
        """Handle alert creation with cooldown"""
        current_time = time.time()
        
        # Check cooldown period
        if alert_type in self.last_alerts:
            if current_time - self.last_alerts[alert_type] < self.alert_cooldown:
                return
        
        # Update last alert time and show alert
        self.last_alerts[alert_type] = current_time
        self.alert_panel.add_alert(message, alert_type)
    
    def _draw_alert_overlay(self, frame, color, alpha=0.3):
        """Draw a colored overlay on the frame for visual alerts"""
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), color, -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)