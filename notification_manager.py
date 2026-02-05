"""
Windows Notification Manager - Sends system toast notifications and sounds
"""
import threading
import winsound
from win10toast import ToastNotifier
from pathlib import Path


class NotificationManager:
    """Manages system notifications and alert sounds."""
    
    def __init__(self):
        self.toaster = ToastNotifier()
        self.sound_file = Path(__file__).parent / "alert_sound.wav"
    
    def send_notification(self, title, message, duration=5):
        """
        Send a Windows 10+ toast notification.
        
        Args:
            title: Notification title
            message: Notification message
            duration: Display duration in seconds (default: 5)
        """
        def show():
            try:
                self.toaster.show_toast(
                    title=title,
                    msg=message,
                    duration=duration,
                    threaded=True
                )
            except Exception as e:
                print(f"Notification error: {e}")
        
        threading.Thread(target=show, daemon=True).start()
    
    def play_alert_sound(self, sound_type="warning"):
        """
        Play system alert sound.
        
        Args:
            sound_type: 'warning' (beep), 'error' (buzzer), 'info' (ding)
        """
        def play():
            try:
                if sound_type == "warning":
                    # Double beep
                    winsound.Beep(1000, 300)
                    winsound.Beep(1000, 300)
                elif sound_type == "error":
                    # Low buzzer
                    winsound.Beep(500, 500)
                    winsound.Beep(500, 500)
                elif sound_type == "info":
                    # Single ding
                    winsound.Beep(1200, 200)
            except Exception as e:
                print(f"Sound error: {e}")
        
        threading.Thread(target=play, daemon=True).start()
    
    def send_alert(self, title, message, activity, motivation, sound=True):
        """
        Send complete alert with notification + sound + voice.
        
        Args:
            title: Alert title
            message: Alert message
            activity: Detected activity
            motivation: Motivation message
            sound: Whether to play alert sound
        """
        # Send system notification
        full_msg = f"{message}\nActivity: {activity}\n{motivation}"
        self.send_notification(title, full_msg, duration=8)
        
        # Play alert sound
        if sound:
            self.play_alert_sound("warning")
