"""
Convert and process image labels for YOLO format
"""
import numpy as np
from pathlib import Path

def convert_to_yolo_format(bbox, img_width, img_height):
    """Convert bounding box to YOLO format"""
    x_min, y_min, x_max, y_max = bbox
    
    # Calculate center points and dimensions
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min
    
    # Normalize values
    x_center /= img_width
    y_center /= img_height
    width /= img_width
    height /= img_height
    
    return [x_center, y_center, width, height]

def create_yolo_label(class_id, bbox, img_width, img_height):
    """Create YOLO format label string"""
    yolo_bbox = convert_to_yolo_format(bbox, img_width, img_height)
    return f"{class_id} {' '.join(map(str, yolo_bbox))}"