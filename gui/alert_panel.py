"""
Alert panel for displaying detection notifications
"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
import datetime

class AlertPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Recent Alerts")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        self.layout.addWidget(title)
        
        # Add stretch to push alerts to the top
        self.layout.addStretch()
    
    def add_alert(self, message, alert_type):
        """Add a new alert to the panel"""
        try:
            # Remove stretch
            stretch_item = self.layout.itemAt(self.layout.count() - 1)
            if stretch_item:
                self.layout.removeItem(stretch_item)
            
            # Add new alert at the top
            alert = AlertMessage(message, alert_type, self)
            self.layout.insertWidget(1, alert)
            
            # Add stretch back
            self.layout.addStretch()
            
            # Remove old alerts if there are too many
            if self.layout.count() > 8:  # Keep 6 alerts + title + stretch
                item = self.layout.itemAt(7)
                if item and item.widget():
                    item.widget().deleteLater()
            
            # Schedule alert removal
            QTimer.singleShot(5000, lambda: self.remove_alert(alert))
            
        except Exception as e:
            print(f"Error adding alert: {str(e)}")
    
    def remove_alert(self, alert):
        """Remove an alert from the panel"""
        try:
            if alert and not alert.isHidden() and alert in self.findChildren(AlertMessage):
                alert.deleteLater()
        except Exception as e:
            print(f"Error removing alert: {str(e)}")

class AlertMessage(QFrame):
    def __init__(self, message, alert_type, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self._get_alert_color(alert_type)};
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        # Message
        msg_label = QLabel(message)
        msg_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(msg_label)
        
        # Timestamp
        time_label = QLabel(datetime.datetime.now().strftime("%H:%M:%S"))
        time_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        layout.addWidget(time_label)
    
    def _get_alert_color(self, alert_type):
        colors = {
            'motion': '#2196F3',  # Blue
            'weapon': '#f44336',  # Red
            'fire': '#FF9800',    # Orange
            'face': '#4CAF50',    # Green
            'crowd': '#9C27B0',   # Purple
            'accident': '#E91E63'  # Pink
        }
        return colors.get(alert_type, '#757575')