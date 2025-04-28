"""
Main window of the surveillance system
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QFrame)
from PyQt6.QtCore import Qt, QTimer
import cv2
from .feature_panel import FeaturePanel
from .alert_panel import AlertPanel
from .video_processor import VideoProcessor
from .detection_manager import DetectionManager
from detectors import (
    FrameProcessor, MotionDetector, FireDetector, 
    WeaponDetector, AccidentDetector, CrowdAnalyzer
)
from ai_agent.agent import SurveillanceAgent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Surveillance System")
        self.setMinimumSize(1200, 800)
        
        # Initialize components
        self._init_ui_components()
        self._init_detectors()
        self._init_processors()
        self._init_camera()
        self._setup_layout()
        self.ai_agent = SurveillanceAgent()

        def update_frame(self):
          """Update and process camera frame"""
        ret, frame = self.camera.read()
        if not ret or frame is None:
            return
        
        try:
            if self.video_processor.should_process_frame():
                processed_frame = self.video_processor.preprocess_frame(frame)
                if processed_frame is not None:
                    # Run detections
                    processed_frame, detections = self.detection_manager.process_detections(
                        processed_frame, 
                        self.detectors,
                        self.feature_panel
                    )
                    
                    # AI Agent analysis
                    analysis = self.ai_agent.analyze_frame(processed_frame, detections)
                    
                    # Update UI based on AI analysis
                    self._update_ui_with_analysis(analysis)
                    
                    # Handle any high-priority recommendations
                    self._handle_ai_recommendations(analysis['recommendations'])
                    
                    # Update status
                    threat_level = analysis['threat_level']
                    if threat_level > 0.7:
                        status = "HIGH THREAT LEVEL!"
                        color = "#f44336"  # Red
                    elif threat_level > 0.4:
                        status = "Elevated Risk Level"
                        color = "#ff9800"  # Orange
                    else:
                        status = "Normal Monitoring"
                        color = "#4caf50"  # Green
                    
                    self.status_label.setText(status)
                    self.status_label.setStyleSheet(f"color: {color}; padding: 5px;")
                    
                    # Display frame
                    pixmap = self.video_processor.convert_cv_to_qt(processed_frame)
                    if pixmap is not None:
                        self.camera_label.setPixmap(pixmap.scaled(
                            self.camera_label.size(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        ))
            
        except Exception as e:
            print(f"Error updating frame: {str(e)}")
            self.status_label.setText("Error processing frame")
            self.status_label.setStyleSheet("color: #f44336; padding: 5px;")
    
    def _update_ui_with_analysis(self, analysis):
        """Update UI components with AI analysis results"""
        # Update priority areas on video feed
        for area in analysis['priority_areas']:
            center = area['center']
            cv2.circle(frame, center, area['radius'], (0, 255, 255), 2)
            cv2.putText(frame, area['reason'], 
                       (center[0] - 50, center[1] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    def _handle_ai_recommendations(self, recommendations):
        """Handle AI agent recommendations"""
        for rec in recommendations:
            if rec['priority'] == 'HIGH':
                self.alert_panel.add_alert(
                    f"AI Alert: {rec['action']}", 
                    'ai_alert'
                )
    
    def _init_ui_components(self):
        """Initialize UI components"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        self.feature_panel = FeaturePanel()
        self.alert_panel = AlertPanel()
        
        self.camera_label = QLabel()
        self.camera_label.setMinimumSize(800, 600)
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setStyleSheet("background-color: #000000; border-radius: 5px;")
        
        self.status_label = QLabel("System Ready")
        self.status_label.setStyleSheet("color: white; padding: 5px;")
    
    def _init_detectors(self):
        """Initialize detection components"""
        self.detectors = {
            'motion': MotionDetector(),
            'fire': FireDetector(),
            'weapon': WeaponDetector(),
            'accident': AccidentDetector(),
            'crowd': CrowdAnalyzer()
        }
    
    def _init_processors(self):
        """Initialize processing components"""
        self.frame_processor = FrameProcessor()
        self.video_processor = VideoProcessor()
        self.detection_manager = DetectionManager(self.alert_panel)
    
    def _init_camera(self):
        """Initialize camera and frame timer"""
        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms refresh rate
    
    def _setup_layout(self):
        """Set up the window layout"""
        # Left panel (camera view)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #1E1E1E; border-radius: 10px; margin: 10px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self.camera_label)
        left_layout.addWidget(self.status_label)
        
        # Add panels to main layout
        self.main_layout.addWidget(left_panel)
        
        # Right panel
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.feature_panel)
        right_layout.addWidget(self.alert_panel)
        self.main_layout.addLayout(right_layout)
    
    def update_frame(self):
        """Update and process camera frame"""
        ret, frame = self.camera.read()
        if not ret or frame is None:
            return
        
        try:
            # Only process every nth frame for better performance
            if self.video_processor.should_process_frame():
                # Preprocess frame
                processed_frame = self.video_processor.preprocess_frame(frame)
                if processed_frame is not None:
                    # Run detections
                    processed_frame, detections = self.detection_manager.process_detections(
                        processed_frame, 
                        self.detectors,
                        self.feature_panel
                    )
                    
                    # Update status based on detections
                    if detections:
                        self.status_label.setText("Detection(s) in progress!")
                        self.status_label.setStyleSheet("color: #ff9800; padding: 5px;")
                    else:
                        self.status_label.setText("Monitoring...")
                        self.status_label.setStyleSheet("color: white; padding: 5px;")
                    
                    # Convert processed frame to Qt format and display
                    pixmap = self.video_processor.convert_cv_to_qt(processed_frame)
                    if pixmap is not None:
                        self.camera_label.setPixmap(pixmap.scaled(
                            self.camera_label.size(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        ))
            
        except Exception as e:
            print(f"Error updating frame: {str(e)}")
            self.status_label.setText("Error processing frame")
            self.status_label.setStyleSheet("color: #f44336; padding: 5px;")
    
    def closeEvent(self, event):
        """Clean up resources when closing the window"""
        self.timer.stop()
        if self.camera is not None:
            self.camera.release()
        event.accept()