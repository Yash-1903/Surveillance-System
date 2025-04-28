"""
Configuration settings for the Smart Surveillance System
"""

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = ""  # Add your email
SENDER_PASSWORD = ""  # Add your app password
RECEIVER_EMAIL = ""  # Add recipient email

# Detection Thresholds
MOTION_THRESHOLD = 30
FIRE_CONFIDENCE = 0.7
WEAPON_CONFIDENCE = 0.6
FACE_CONFIDENCE = 0.7
ACCIDENT_CONFIDENCE = 0.65

# Alert Settings
ALERT_COOLDOWN = 30  # seconds between alerts
ENABLE_SOUND_ALERT = True