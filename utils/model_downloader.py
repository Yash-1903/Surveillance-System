"""
Utility script to download and set up YOLO models
"""
import os
import torch
from ultralytics import YOLO
import requests
from tqdm import tqdm

def download_file(url, dest_path):
    """Download a file with progress bar"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    
    with open(dest_path, 'wb') as f, tqdm(
        desc=os.path.basename(dest_path),
        total=total_size,
        unit='iB',
        unit_scale=True
    ) as pbar:
        for data in response.iter_content(block_size):
            size = f.write(data)
            pbar.update(size)

def download_models():
    """Download required YOLO models"""
    os.makedirs('models', exist_ok=True)
    print("Downloading YOLO models...")
    
    # Base model URL - using latest stable release
    base_model_url = 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt'
    
    # Download base model first
    base_model_path = 'models/yolov8n.pt'
    if not os.path.exists(base_model_path):
        print("\nDownloading base YOLOv8n model...")
        try:
            download_file(base_model_url, base_model_path)
            # Verify model
            YOLO(base_model_path)
            print("Successfully downloaded and verified base model")
        except Exception as e:
            print(f"Error downloading base model: {str(e)}")
            if os.path.exists(base_model_path):
                os.remove(base_model_path)
            return
    
    # Create specialized models by copying base model
    specialized_models = [
        'fire_detection.pt',
        'weapon_detection.pt',
        'accident_detection.pt'
    ]
    
    for model_name in specialized_models:
        model_path = f'models/{model_name}'
        if not os.path.exists(model_path):
            print(f"\nCreating {model_name}...")
            try:
                # Copy base model for specialized use
                import shutil
                shutil.copy2(base_model_path, model_path)
                # Verify model
                YOLO(model_path)
                print(f"Successfully created {model_name}")
            except Exception as e:
                print(f"Error creating {model_name}: {str(e)}")
                if os.path.exists(model_path):
                    os.remove(model_path)
                continue
    
    print("\nModel setup complete!")
    print("\nNOTE: The specialized models (fire, weapon, accident detection)")
    print("are currently copies of the base model. For production use,")
    print("these models should be fine-tuned on specific datasets for")
    print("their respective tasks.")

if __name__ == "__main__":
    download_models()