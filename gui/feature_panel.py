"""
Feature selection panel
"""
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QLabel, 
                            QScrollArea, QWidget, QHBoxLayout)
from PyQt6.QtCore import Qt
from .custom_widgets import ToggleSwitch

class FeaturePanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-radius: 10px;
                margin: 10px;
            }
            QLabel {
                color: white;
            }
        """)
        self.feature_switches = {}
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Detection Features")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(title)
        
        # Scroll area for features
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        # Container for feature switches
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        # Add feature switches
        features = [
            "Motion Detection",
            "Fire Detection",
            "Weapon Detection",
            "Accident Detection",
            "Crowd Analysis"
        ]
        
        for feature in features:
            feature_layout = QHBoxLayout()
            
            # Label
            label = QLabel(feature)
            label.setStyleSheet("font-size: 14px; padding: 5px;")
            feature_layout.addWidget(label)
            
            # Switch
            switch = ToggleSwitch()
            # switch.setChecked(True)  # Enable all features by default
            self.feature_switches[feature] = switch
            feature_layout.addWidget(switch)
            
            container_layout.addLayout(feature_layout)
        
        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
    
    def is_feature_enabled(self, feature_name):
        """Check if a feature is enabled"""
        switch = self.feature_switches.get(feature_name)
        return switch.isChecked() if switch else False