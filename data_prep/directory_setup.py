"""
Directory structure setup for dataset organization
"""
from pathlib import Path
import logging

class DirectorySetup:
    def __init__(self, base_path):
        """
        Initialize directory setup with base path
        
        Args:
            base_path (str): Base directory path for dataset
        """
        self.base_path = Path(base_path)
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for directory operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_dataset_structure(self):
        """Create the complete dataset directory structure"""
        directories = {
            'raw': self.base_path / 'raw_data',
            'processed': {
                'train': {
                    'images': self.base_path / 'datasets' / 'train' / 'images',
                    'labels': self.base_path / 'datasets' / 'train' / 'labels'
                },
                'val': {
                    'images': self.base_path / 'datasets' / 'val' / 'images',
                    'labels': self.base_path / 'datasets' / 'val' / 'labels'
                }
            },
            'models': self.base_path / 'models',
            'logs': self.base_path / 'logs'
        }
        
        try:
            # Create raw data directory
            directories['raw'].mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created raw data directory: {directories['raw']}")
            
            # Create processed data directories
            for split in ['train', 'val']:
                for subdir in ['images', 'labels']:
                    directories['processed'][split][subdir].mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Created {split}/{subdir} directory: {directories['processed'][split][subdir]}")
            
            # Create model and log directories
            directories['models'].mkdir(parents=True, exist_ok=True)
            directories['logs'].mkdir(parents=True, exist_ok=True)
            self.logger.info("Created model and log directories")
            
            return directories
            
        except Exception as e:
            self.logger.error(f"Error creating directory structure: {str(e)}")
            raise

def setup_project_directories(base_path):
    """
    Convenience function to set up all project directories
    
    Args:
        base_path (str): Base directory path for the project
    
    Returns:
        dict: Dictionary containing all created directory paths
    """
    setup = DirectorySetup(base_path)
    return setup.create_dataset_structure()

if __name__ == "__main__":
    # Example usage
    project_dirs = setup_project_directories("project_data")
    print("Directory structure created successfully!")