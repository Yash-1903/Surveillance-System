"""
Dataset preparation utilities for YOLO training
"""
import os
import shutil
from pathlib import Path
import random

class DatasetPreparator:
    def __init__(self, dataset_name, base_path='datasets'):
        self.dataset_name = dataset_name
        self.base_path = Path(base_path) / dataset_name
        self.train_ratio = 0.8
        
        # Create directory structure
        self.create_directories()
    
    def create_directories(self):
        """Create the required directory structure"""
        dirs = [
            self.base_path / 'train' / 'images',
            self.base_path / 'train' / 'labels',
            self.base_path / 'val' / 'images',
            self.base_path / 'val' / 'labels'
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def split_dataset(self, images_path):
        """Split dataset into train and validation sets"""
        images = list(Path(images_path).glob('*.jpg')) + \
                list(Path(images_path).glob('*.png'))
        
        # Shuffle images
        random.shuffle(images)
        
        # Split into train and validation
        split_idx = int(len(images) * self.train_ratio)
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        # Move images and their corresponding labels
        for img in train_images:
            self._move_sample(img, 'train')
        
        for img in val_images:
            self._move_sample(img, 'val')
    
    def _move_sample(self, img_path, subset):
        """Move an image and its label to the appropriate subset folder"""
        # Move image
        dest_img = self.base_path / subset / 'images' / img_path.name
        shutil.copy2(img_path, dest_img)
        
        # Move corresponding label if it exists
        label_path = img_path.with_suffix('.txt')
        if label_path.exists():
            dest_label = self.base_path / subset / 'labels' / label_path.name
            shutil.copy2(label_path, dest_label)
    
    def create_data_yaml(self, class_names):
        """Create data.yaml configuration file"""
        yaml_content = f"""
path: {self.base_path}
train: train/images
val: val/images

nc: {len(class_names)}
names: {class_names}
"""
        
        with open(self.base_path / 'data.yaml', 'w') as f:
            f.write(yaml_content.strip())

def prepare_dataset(name, source_path, class_names):
    """Prepare a dataset for training"""
    prep = DatasetPreparator(name)
    prep.split_dataset(source_path)
    prep.create_data_yaml(class_names)
    print(f"Dataset {name} prepared successfully!")