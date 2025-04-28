# Smart Surveillance System

A comprehensive surveillance system with advanced detection capabilities including motion, fire, face recognition, and more.

## Features

- Fire and Smoke Detection
- Face Recognition
- Motion Detection
- Weapon Detection
- Crowd Analytics
- Car Accident Detection
- Email Alert System

## Requirements

- Python 3.8+
- OpenCV
- NumPy
- YOLO v8
- Face Recognition
- SMTPlib
- Tkinter

## Installation

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure email settings in `config.py`

3. Download YOLO models and place them in the `models` directory

## Usage

Run the main application:
```bash
python main.py
```

## Project Structure

- `main.py`: Main application entry point
- `config.py`: Configuration settings
- `detectors/`: Detection modules
  - `motion_detector.py`: Motion detection
  - `fire_detector.py`: Fire and smoke detection
- `utils/`: Utility modules
  - `email_service.py`: Email notification service

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request