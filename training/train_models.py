"""
Model training orchestration
"""
from pathlib import Path
import logging
from .model_trainer import YOLOTrainer

def train_detection_models(base_path='project_data'):
    """Train all specialized detection models"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    base_path = Path(base_path).resolve()  # Get absolute path
    
    # Define models and their datasets
    models = {
        'fire_detection': 'fire',
        'weapon_detection': 'weapon',
        'accident_detection': 'accident'
    }
    
    trained_models = {}
    
    for model_name, dataset_name in models.items():
        try:
            logger.info(f"\nTraining {model_name}...")
            dataset_path = base_path / 'datasets' / dataset_name
            
            if not dataset_path.exists():
                logger.error(f"Dataset path not found: {dataset_path}")
                continue
                
            trainer = YOLOTrainer(model_name, dataset_path)
            model_path = trainer.train()
            trained_models[model_name] = model_path
            logger.info(f"Successfully trained {model_name}")
            
        except Exception as e:
            logger.error(f"Error training {model_name}: {str(e)}")
    
    return trained_models