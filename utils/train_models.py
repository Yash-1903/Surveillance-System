"""
Model training utility for YOLO models
"""
from ultralytics import YOLO
import os
from pathlib import Path

class ModelTrainer:
    def __init__(self, model_name, dataset_path):
        self.model_name = model_name
        self.dataset_path = Path(dataset_path)
        self.model = None
    
    def setup_model(self):
        """Initialize the model for training"""
        # Start with pretrained YOLOv8n
        self.model = YOLO('yolov8n.pt')
    
    def train(self, epochs=100, batch_size=16, patience=20):
        """Train the model on the dataset"""
        if self.model is None:
            self.setup_model()
        
        # Training configuration
        config = {
            'data': str(self.dataset_path / 'data.yaml'),
            'epochs': epochs,
            'batch': batch_size,
            'patience': patience,
            'device': 'cuda:0',  # Use GPU if available
            'project': 'runs',
            'name': self.model_name
        }
        
        # Start training
        print(f"Starting training for {self.model_name}...")
        self.model.train(**config)
        
        # Save the trained model
        output_path = f'models/{self.model_name}_trained.pt'
        self.model.save(output_path)
        print(f"Model saved to {output_path}")

def train_all_models():
    """Train all specialized detection models"""
    models = {
        'fire_detection': 'datasets/fire',
        'weapon_detection': 'datasets/weapon',
        'accident_detection': 'datasets/accident'
    }
    
    for model_name, dataset_path in models.items():
        trainer = ModelTrainer(model_name, dataset_path)
        trainer.train()

if __name__ == "__main__":
    train_all_models()