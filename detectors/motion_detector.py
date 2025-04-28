"""
Motion detection module using OpenCV
"""
import cv2
import numpy as np
from .base_detector import BaseDetector

class MotionDetector(BaseDetector):
    def __init__(self, threshold=30):
        self.threshold = threshold
        self.background = None
        self.kernel = np.ones((5, 5), np.uint8)
    
    def detect(self, frame):
        if frame is None:
            return frame, False, []
            
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Initialize background on first frame
        if self.background is None:
            self.background = gray.copy().astype("float")
            return frame, False, []
        
        # Calculate difference
        cv2.accumulateWeighted(gray, self.background, 0.5)
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.background))
        thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
        
        # Process the threshold image
        thresh = cv2.dilate(thresh, self.kernel, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                (x, y, w, h) = cv2.boundingRect(contour)
                detection = {
                    'box': [x, y, x + w, y + h],
                    'score': 1.0,
                    'class': 'motion'
                }
                detections.append(detection)
                
                # Draw detection with green color for motion
                self.draw_detection(frame, detection['box'], 
                                 "Motion", 
                                 color=(0, 255, 0))
        
        return frame, len(detections) > 0, detections