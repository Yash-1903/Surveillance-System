"""
Control panel for the surveillance system
"""
import tkinter as tk
from tkinter import ttk

class ControlPanel:
    def __init__(self, parent, start_cmd, stop_cmd, add_face_cmd):
        self.frame = ttk.LabelFrame(parent, text="Controls", padding="5")
        
        ttk.Button(self.frame, text="Start", 
                  command=start_cmd).grid(row=0, column=0, padx=5)
        ttk.Button(self.frame, text="Stop", 
                  command=stop_cmd).grid(row=0, column=1, padx=5)
        ttk.Button(self.frame, text="Add Face", 
                  command=add_face_cmd).grid(row=0, column=2, padx=5)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)