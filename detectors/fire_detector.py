"""
Fire and smoke detection using YOLO
"""
from ultralytics import YOLO
import cv2
from .base_detector import BaseDetector

class FireDetector(BaseDetector):
    def __init__(self, model_path='models/fire_detection_trained.pt', confidence=0.3):
        super().__init__()
        try:
            model_path = self.load_model(model_path, 'fire_detection')
            self.model = YOLO(model_path)
            print(f"Loaded fire detection model: {model_path}")
            # Custom fire_smoke classes
            self.fire_classes = {
                0: 'fire',
                1: 'smoke',
            }
        except Exception as e:
            print(f"Error loading fire detection model: {str(e)}")
            self.model = None
        self.confidence = confidence
    
    def detect(self, frame):
        if frame is None or self.model is None:
            return frame, False, []
            
        try:
            results = self.model(frame, verbose=False)[0]
            detections = []
            
            if hasattr(results, 'boxes') and hasattr(results.boxes, 'data'):
                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result
                    
                    if score > self.confidence:
                        class_name = results.names[int(class_id)]
                        detection = {
                            'box': [x1, y1, x2, y2],
                            'score': score,
                            'class': class_name
                        }
                        detections.append(detection)
                        
                        # Draw detection with red color for fire
                        self.draw_detection(frame, detection['box'], 
                                         f"{class_name}: {score:.2f}", 
                                         color=(0, 0, 255))
            
            return frame, len(detections) > 0, detections
            
        except Exception as e:
            print(f"Error in fire detection: {str(e)}")
            return frame, False, []