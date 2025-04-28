"""
Frame processing optimization module
"""
import cv2
import numpy as np
from threading import Lock

class FrameProcessor:
    def __init__(self):
        self.processing_lock = Lock()
        self.frame_count = 0
        self.skip_frames = 2  # Process every 3rd frame
        
    def preprocess_frame(self, frame):
        """Preprocess frame for faster detection"""
        if frame is None:
            return None
            
        try:
            # Resize frame for faster processing while maintaining aspect ratio
            height, width = frame.shape[:2]
            target_width = 640
            ratio = target_width / width
            target_height = int(height * ratio)
            
            # Apply preprocessing
            processed = cv2.resize(frame, (target_width, target_height))
            
            # Optional: Add noise reduction if needed
            # processed = cv2.GaussianBlur(processed, (3, 3), 0)
            
            return processed
            
        except Exception as e:
            print(f"Error preprocessing frame: {str(e)}")
            return None
        
    def should_process_frame(self):
        """Determine if frame should be processed"""
        with self.processing_lock:
            self.frame_count += 1
            return self.frame_count % (self.skip_frames + 1) == 0