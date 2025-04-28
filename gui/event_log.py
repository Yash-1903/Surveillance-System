"""
Event logging panel for the surveillance system
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class EventLog:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Event Log", padding="5")
        
        self.log_text = tk.Text(self.frame, height=10, width=50)
        self.log_text.grid(row=0, column=0, pady=5)
        
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", 
                                command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
    
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)