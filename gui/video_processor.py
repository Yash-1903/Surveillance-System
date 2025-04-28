"""
Video processing and frame handling
"""
import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt

class VideoProcessor:
    def __init__(self):
        self.frame_count = 0
        self.process_every_n_frames = 3  # Process every 3rd frame for better performance
        
    def convert_cv_to_qt(self, cv_frame):
        """Convert OpenCV frame to QPixmap for display"""
        if cv_frame is None:
            return None
            
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(cv_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            
            # Create QImage from RGB data
            qt_image = QImage(rgb_frame.data, w, h, w * ch, QImage.Format.Format_RGB888)
            
            # Convert to QPixmap and scale to fit the label
            return QPixmap.fromImage(qt_image)
        except Exception as e:
            print(f"Error converting frame: {str(e)}")
            return None
    
    def should_process_frame(self):
        """Determine if the current frame should be processed"""
        self.frame_count += 1
        return self.frame_count % self.process_every_n_frames == 0
    
    def preprocess_frame(self, frame):
        """Preprocess frame for detection"""
        if frame is None:
            return None
            
        try:
            # Resize for faster processing while maintaining aspect ratio
            height, width = frame.shape[:2]
            target_width = 640
            ratio = target_width / width
            target_height = int(height * ratio)
            
            return cv2.resize(frame, (target_width, target_height))
        except Exception as e:
            print(f"Error preprocessing frame: {str(e)}")
            return None