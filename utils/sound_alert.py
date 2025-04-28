"""
Sound alert system for notifications
"""
import winsound
import platform
import os

class SoundAlert:
    def __init__(self):
        self.os_type = platform.system().lower()
    
    def play_alert(self, duration_ms=1000, frequency=2500):
        if self.os_type == 'windows':
            winsound.Beep(frequency, duration_ms)
        elif self.os_type == 'linux':
            os.system(f'play -nq -t alsa synth {duration_ms/1000} sine {frequency}')
        elif self.os_type == 'darwin':  # macOS
            os.system(f'afplay /System/Library/Sounds/Ping.aiff')