"""
Dataset preparation module
"""
from pathlib import Path
import shutil
from .dataset_config import DatasetConfig

def prepare_dataset(source_dir, output_dir, class_names):
    """Prepare dataset for YOLO training"""
    source_dir = Path(source_dir)
    output_dir = Path(output_dir)
    
    # Initialize dataset configuration
    config = DatasetConfig(output_dir.parent.parent)
    paths = config.get_dataset_paths(output_dir.name)
    
    # Create directory structure
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    
    # Copy files to train/val directories (80/20 split)
    image_files = list(source_dir.glob('*.jpg')) + list(source_dir.glob('*.png'))
    train_split = int(len(image_files) * 0.8)
    
    # Copy training files
    for img_path in image_files[:train_split]:
        shutil.copy2(img_path, paths['train_images'] / img_path.name)
        label_path = img_path.with_suffix('.txt')
        if label_path.exists():
            shutil.copy2(label_path, paths['train_labels'] / label_path.name)
    
    # Copy validation files
    for img_path in image_files[train_split:]:
        shutil.copy2(img_path, paths['val_images'] / img_path.name)
        label_path = img_path.with_suffix('.txt')
        if label_path.exists():
            shutil.copy2(label_path, paths['val_labels'] / label_path.name)
    
    # Create YAML configuration
    yaml_path = config.create_yaml_config(output_dir.name, class_names)
    
    return yaml_path