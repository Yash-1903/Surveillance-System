"""
Main pipeline for dataset preparation and model training
"""
from data_prep.directory_setup import setup_project_directories
from data_prep.prepare_dataset import prepare_dataset
from data_prep.sample_data_creator import create_sample_datasets
from training.train_models import train_detection_models
import logging
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def run_pipeline(base_path='project_data'):
    logger = setup_logging()
    base_path = Path(base_path)
    
    try:
        # Step 1: Setup directory structure
        logger.info("Setting up directory structure...")
        directories = setup_project_directories(base_path)
        
        # Step 2: Create sample datasets if raw data doesn't exist
        logger.info("Creating sample datasets...")
        create_sample_datasets(base_path)
        
        # Step 3: Prepare datasets
        logger.info("\nPreparing datasets...")
        datasets = {
            'fire': ['fire', 'smoke'],
            'weapon': ['pistol', 'rifle', 'knife','bazooka','sniper','shotgun'],
            'accident': ['accident', 'non-accident'],
        }
        
        for dataset_name, classes in datasets.items():
            source_dir = base_path / 'raw_data' / f'{dataset_name}_images'
            output_dir = base_path / 'datasets' / dataset_name
            
            if source_dir.exists():
                prepare_dataset(source_dir, output_dir, classes)
            else:
                logger.warning(f"Source directory not found: {source_dir}")
        
        # Step 4: Train models
        logger.info("\nStarting model training...")
        trained_models = train_detection_models(base_path)
        
        logger.info("\nPipeline completed successfully!")
        return trained_models
        
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        raise

if __name__ == "__main__":
    run_pipeline()