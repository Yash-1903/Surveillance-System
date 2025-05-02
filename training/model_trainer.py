"""
YOLO model training module
"""
from ultralytics import YOLO
import logging
from pathlib import Path
import torch
import shutil

class YOLOTrainer:
    def __init__(self, model_name, dataset_path):
        self.model_name = model_name
        self.dataset_path = Path(dataset_path)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def train(self, epochs=30, batch_size=32, patience=200):
        """Train the YOLO model"""
        try:
            # Initialize model
            model = YOLO('yolov8n.pt')  # Start with pretrained model
            
            # Determine device
            device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
            
            # Training configuration
            config = {
                'data': str(self.dataset_path / 'data.yaml'),
                'epochs': epochs,
                'batch': batch_size,
                'patience': patience,
                'device': device,
                'name': self.model_name
            }
            
            # Start training
            self.logger.info(f"Starting training for {self.model_name} on {device}")
            results = model.train(**config)

            # Get the best model path from training
            best_model_path = str(Path(results.save_dir) / 'weights' / 'best.pt')
            
            # Save the trained model
            output_path = f'models/{self.model_name}_trained.pt'
            shutil.copy2(best_model_path, output_path)
            # results.model.save(output_path)
            self.logger.info(f"Model saved to {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Training error: {str(e)}")
            raise