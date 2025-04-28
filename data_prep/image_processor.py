"""
Image processing utilities for dataset preparation
"""
import cv2
import numpy as np
from pathlib import Path

def resize_image(image_path, target_size=(640, 640)):
    """Resize image while maintaining aspect ratio"""
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    
    height, width = img.shape[:2]
    scale = min(target_size[0]/width, target_size[1]/height)
    new_size = (int(width*scale), int(height*scale))
    
    resized = cv2.resize(img, new_size)
    return resized

def augment_image(image):
    """Apply basic augmentations"""
    augmentations = []
    
    # Horizontal flip
    augmentations.append(cv2.flip(image, 1))
    
    # Brightness variation
    bright = cv2.convertScaleAbs(image, alpha=1.2, beta=10)
    dark = cv2.convertScaleAbs(image, alpha=0.8, beta=-10)
    augmentations.extend([bright, dark])
    
    return augmentations