"""
Configuration settings for the Smart Surveillance System
"""

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "yash.gupta.5087@gmail.com"  # Add your email
SENDER_PASSWORD = "admin"  # Add your app password
RECEIVER_EMAIL = "zephyrr.1925@gmail.com"  # Add recipient email

# Detection Thresholds
MOTION_THRESHOLD = 30
FIRE_CONFIDENCE = 0.2   #0.6
WEAPON_CONFIDENCE = 0.9 #0.6
FACE_CONFIDENCE = 0.2   #0.7
ACCIDENT_CONFIDENCE = 0.2   #0.65

# Alert Settings
ALERT_COOLDOWN = 30  # seconds between alerts
ENABLE_SOUND_ALERT = True