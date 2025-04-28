"""
Main entry point for the Smart Surveillance System
"""
import sys
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show login window
    login = LoginWindow()
    login.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()