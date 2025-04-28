"""
Email notification service for the surveillance system
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import config

class EmailAlert:
    def __init__(self):
        self.server = None
        self.last_alert_time = {}  # Track last alert time for each alert type
    
    def connect(self):
        try:
            self.server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
            self.server.starttls()
            self.server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
            return True
        except Exception as e:
            print(f"Email connection error: {e}")
            return False
    
    def send_alert(self, alert_type, image=None):
        current_time = datetime.now()
        
        # Check cooldown period
        if alert_type in self.last_alert_time:
            time_diff = (current_time - self.last_alert_time[alert_type]).seconds
            if time_diff < config.ALERT_COOLDOWN:
                return False
        
        msg = MIMEMultipart()
        msg['Subject'] = f'Alert: {alert_type} Detected!'
        msg['From'] = config.SENDER_EMAIL
        msg['To'] = config.RECEIVER_EMAIL
        
        body = f"""
        Security Alert!
        
        Type: {alert_type}
        Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
        
        Please check the surveillance system immediately.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        if image is not None:
            img_attachment = MIMEImage(image)
            msg.attach(img_attachment)
        
        if self.connect():
            try:
                self.server.send_message(msg)
                self.last_alert_time[alert_type] = current_time
                return True
            except Exception as e:
                print(f"Failed to send email: {e}")
                return False
            finally:
                self.server.quit()
        return False