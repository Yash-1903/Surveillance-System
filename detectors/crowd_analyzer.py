"""
Crowd analysis and people counting
"""
from ultralytics import YOLO
import cv2
import numpy as np
from .base_detector import BaseDetector

class CrowdAnalyzer(BaseDetector):
    def __init__(self, model_path='models/yolov8n.pt', confidence=0.5):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.person_class_id = 0  # COCO dataset person class ID
    
    def detect(self, frame):
        results = self.model(frame)[0]
        detections = []
        people_count = 0
        
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            
            if int(class_id) == self.person_class_id and score > self.confidence:
                people_count += 1
                detection = {
                    'box': [x1, y1, x2, y2],
                    'score': score,
                    'class': 'person'
                }
                detections.append(detection)
                
                # Draw detection with yellow color for people
                self.draw_detection(frame, detection['box'], 
                                 f"Person: {score:.2f}", 
                                 color=(0, 255, 255))
        
        # Add people count
        cv2.putText(frame, f'People Count: {people_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        return frame, people_count > 0, {'count': people_count, 'detections': detections}