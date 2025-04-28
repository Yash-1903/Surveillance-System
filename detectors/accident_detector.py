"""
Car accident detection using YOLO
"""
from ultralytics import YOLO
import cv2
import os
from .base_detector import BaseDetector

class AccidentDetector(BaseDetector):
    def __init__(self, model_path='models/accident_detection_trained.pt', confidence=0.2):
        super().__init__()
        try:
            # Check if model exists
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found at {model_path}")
                
            print(f"Loading accident detection model from: {os.path.abspath(model_path)}")
            self.model = YOLO(model_path)
            
            # Custom accident classes
            self.accident_classes = {
                0: 'accident',
                1: 'collision'
            }
            print(f"Loaded accident detection model successfully")
            print(f"Available classes: {self.accident_classes}")
            
        except Exception as e:
            print(f"Error loading accident detection model: {str(e)}")
            self.model = None
        self.confidence = confidence
        print(f"Confidence threshold set to: {self.confidence}")
    
    def detect(self, frame):
        if frame is None or self.model is None:
            return frame, False, []
            
        try:
            # Print frame info
            print(f"\nProcessing frame: {frame.shape}")
            
            results = self.model(frame, verbose=False)[0]
            detections = []
            
            if hasattr(results, 'boxes') and hasattr(results.boxes, 'data'):
                boxes_data = results.boxes.data.tolist()
                print(f"Found {len(boxes_data)} potential detections")
                
                for result in boxes_data:
                    x1, y1, x2, y2, score, class_id = result
                    class_id = int(class_id)
                    
                    print(f"Detection: class_id={class_id}, score={score:.2f}, box=[{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]")
                    
                    if score > self.confidence:
                        if class_id in self.accident_classes:
                            class_name = self.accident_classes[class_id]
                            detection = {
                                'box': [int(x1), int(y1), int(x2), int(y2)],
                                'score': score,
                                'class': class_name
                            }
                            detections.append(detection)
                            
                            # Draw detection with orange color for accidents
                            self.draw_detection(frame, detection['box'], 
                                             f"{class_name}: {score:.2f}", 
                                             color=(0, 165, 255))
                            print(f"Valid accident detection: {class_name} with confidence {score:.2f}")
                        else:
                            print(f"Class ID {class_id} not in accident classes")
                    else:
                        print(f"Detection score {score:.2f} below threshold {self.confidence}")
            
            print(f"Final detections: {len(detections)}")
            return frame, len(detections) > 0, detections
            
        except Exception as e:
            print(f"Error in accident detection: {str(e)}")
            import traceback
            traceback.print_exc()
            return frame, False, []