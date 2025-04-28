"""
Detection options panel for the surveillance system
"""
import tkinter as tk
from tkinter import ttk

class DetectionOptions:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Detection Options", padding="5")
        
        # Initialize detection flags
        self.enable_motion = tk.BooleanVar(value=True)
        self.enable_fire = tk.BooleanVar(value=True)
        self.enable_face = tk.BooleanVar(value=True)
        self.enable_weapon = tk.BooleanVar(value=True)
        self.enable_crowd = tk.BooleanVar(value=True)
        self.enable_accident = tk.BooleanVar(value=True)
        
        self.setup_options()
    
    def setup_options(self):
        ttk.Checkbutton(self.frame, text="Motion Detection", 
                       variable=self.enable_motion).grid(row=0, column=0)
        ttk.Checkbutton(self.frame, text="Fire Detection", 
                       variable=self.enable_fire).grid(row=0, column=1)
        ttk.Checkbutton(self.frame, text="Face Recognition", 
                       variable=self.enable_face).grid(row=0, column=2)
        ttk.Checkbutton(self.frame, text="Weapon Detection", 
                       variable=self.enable_weapon).grid(row=1, column=0)
        ttk.Checkbutton(self.frame, text="Crowd Analysis", 
                       variable=self.enable_crowd).grid(row=1, column=1)
        ttk.Checkbutton(self.frame, text="Accident Detection", 
                       variable=self.enable_accident).grid(row=1, column=2)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)