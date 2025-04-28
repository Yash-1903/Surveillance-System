"""
Create sample dataset directories and dummy data for testing
"""
import os
from pathlib import Path
import shutil

def create_sample_datasets(base_path='project_data'):
    """Create sample dataset directories with placeholder data"""
    base_path = Path(base_path)
    
    # Create raw_data directory structure
    datasets = {
        'fire_images': ['fire', 'smoke'],
        'weapon_images': ['pistol', 'rifle', 'knife'],
        'accident_images': ['accident', 'collision']
    }
    
    raw_data_path = base_path / 'raw_data'
    raw_data_path.mkdir(parents=True, exist_ok=True)
    
    # Create placeholder files
    for dataset, classes in datasets.items():
        dataset_path = raw_data_path / dataset
        dataset_path.mkdir(exist_ok=True)
        
        # Create placeholder image and label files
        for class_name in classes:
            # Create dummy image file
            (dataset_path / f'{class_name}_sample.jpg').touch()
            
            # Create corresponding label file
            with open(dataset_path / f'{class_name}_sample.txt', 'w') as f:
                f.write(f"0 0.5 0.5 0.3 0.3")  # Sample YOLO format label
    
    print(f"Created sample datasets in {raw_data_path}")
    return raw_data_path