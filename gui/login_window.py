"""
Login window for the surveillance system
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
                            QPushButton, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from .main_window import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Surveillance - Login")
        self.setFixedSize(400, 500)
        self.setup_ui()
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Smart Surveillance")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Username field
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #2196F3;
                border-radius: 6px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.username)
        
        # Password field
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(self.username.styleSheet())
        layout.addWidget(self.password)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        
        # Error message
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #f44336;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
    def login(self):
        # Simple authentication (replace with proper authentication)
        if self.username.text() == "admin" and self.password.text() == "admin":
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            self.error_label.setText("Invalid username or password")