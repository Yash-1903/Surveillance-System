"""
Split and organize dataset into train and validation sets
"""
import shutil
import random
from pathlib import Path

class DatasetSplitter:
    def __init__(self, source_dir, output_dir, train_ratio=0.8):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.train_ratio = train_ratio
        
        # Create directory structure
        self.train_img_dir = self.output_dir / 'train' / 'images'
        self.train_label_dir = self.output_dir / 'train' / 'labels'
        self.val_img_dir = self.output_dir / 'val' / 'images'
        self.val_label_dir = self.output_dir / 'val' / 'labels'
        
        self._create_directories()
    
    def _create_directories(self):
        """Create required directories"""
        for dir_path in [self.train_img_dir, self.train_label_dir, 
                        self.val_img_dir, self.val_label_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def split_dataset(self):
        """Split dataset into train and validation sets"""
        image_files = list(self.source_dir.glob('*.jpg')) + \
                     list(self.source_dir.glob('*.png'))
        
        # Shuffle files
        random.shuffle(image_files)
        
        # Split into train and validation
        split_idx = int(len(image_files) * self.train_ratio)
        train_files = image_files[:split_idx]
        val_files = image_files[split_idx:]
        
        # Copy files to respective directories
        self._copy_files(train_files, self.train_img_dir, self.train_label_dir)
        self._copy_files(val_files, self.val_img_dir, self.val_label_dir)
        
        return len(train_files), len(val_files)
    
    def _copy_files(self, files, img_dir, label_dir):
        """Copy images and their corresponding labels"""
        for img_path in files:
            # Copy image
            shutil.copy2(img_path, img_dir / img_path.name)
            
            # Copy label if exists
            label_path = img_path.with_suffix('.txt')
            if label_path.exists():
                shutil.copy2(label_path, label_dir / label_path.name)