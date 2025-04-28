"""
Dataset configuration and path management
"""
from pathlib import Path

class DatasetConfig:
    def __init__(self, base_path):
        self.base_path = Path(base_path).resolve()  # Get absolute path
        
    def get_dataset_paths(self, dataset_name):
        """Get all relevant paths for a dataset"""
        return {
            'root': self.base_path / 'datasets' / dataset_name,
            'train_images': self.base_path / 'datasets' / dataset_name / 'train' / 'images',
            'train_labels': self.base_path / 'datasets' / dataset_name / 'train' / 'labels',
            'val_images': self.base_path / 'datasets' / dataset_name / 'val' / 'images',
            'val_labels': self.base_path / 'datasets' / dataset_name / 'val' / 'labels'
        }
    
    def create_yaml_config(self, dataset_name, class_names):
        """Create YAML configuration file for YOLO training"""
        dataset_dir = self.base_path / 'datasets' / dataset_name
        yaml_content = f"""
path: {dataset_dir.absolute()}  # Dataset root directory
train: train/images  # Train images relative to 'path'
val: val/images      # Val images relative to 'path'

nc: {len(class_names)}  # Number of classes
names: {class_names}    # Class names
"""
        yaml_path = dataset_dir / 'data.yaml'
        yaml_path.write_text(yaml_content.strip())
        return yaml_path