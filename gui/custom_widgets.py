"""
Custom widgets for the surveillance system GUI
"""
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor

class ToggleSwitch(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(60)
        self.setMinimumHeight(30)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        if self.isChecked():
            painter.setBrush(QColor("#2196F3"))  # Blue when ON
        else:
            painter.setBrush(QColor("#808080"))  # Gray when OFF
            
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        
        # Draw switch
        if self.isChecked():
            switch_x = self.width() - 28
        else:
            switch_x = 4
            
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(switch_x, 4, 22, 22)