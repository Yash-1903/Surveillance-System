"""
Base detector class with common functionality
"""
import cv2
import os
from pathlib import Path

class BaseDetector:
    def __init__(self):
        self.model = None
        
    def load_model(self, model_path, model_name):
        """Load YOLO model with fallback options"""
        # First check if models directory exists
        models_dir = Path('models')
        if not models_dir.exists():
            models_dir.mkdir(parents=True, exist_ok=True)
            
        # Check if model exists
        if os.path.exists(model_path):
            print(f"Loading model from {model_path}")
            return model_path
            
        # Try downloading base model if specialized one doesn't exist
        try:
            from ultralytics import YOLO
            print(f"Downloading base YOLO model for {model_name}")
            model = YOLO('yolov8n.pt')
            save_path = models_dir / f"{model_name}.pt"
            model.save(str(save_path))
            print(f"Saved model to {save_path}")
            return str(save_path)
        except Exception as e:
            print(f"Error downloading model: {str(e)}")
            raise FileNotFoundError(f"No suitable model found for {model_name}")

    def draw_detection(self, frame, box, label, color=(0, 255, 0)):
        """Draw detection box and label on frame"""
        try:
            x1, y1, x2, y2 = [int(coord) for coord in box]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Add label with background
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(frame, (x1, y1 - 20), (x1 + text_size[0], y1), color, -1)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        except Exception as e:
            print(f"Error drawing detection: {str(e)}")
    
    def detect(self, frame):
        """Base detect method, should be overridden by subclasses"""
        return frame, False, []