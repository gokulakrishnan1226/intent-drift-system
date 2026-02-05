import time
from data_logger import DataLogger 
from focus_tracker import FocusTracker
from drift_detector import DriftDetector
from activity_detector import ActivityDetector

class BackendController:
    def __init__(self):
        self.current_intent = "study"
        self.current_activity = None
        self.last_alert_activity = None
        
        # Initialize components
        self.focus_tracker = FocusTracker()
        self.drift_detector = DriftDetector()
        self.activity_detector = ActivityDetector()
        
        # Continuous distraction tracking
        self.distraction_threshold = 20  # 20 seconds
        self.continuous_distraction_time = 0
        self.last_check_time = time.time()

    def set_intent(self, intent):
        self.current_intent = intent
        self.focus_tracker.reset()
        self.last_alert_activity = None
        self.current_activity = None

    def reset_distraction_timer(self):
        """Reset continuous distraction tracking so next alert requires full threshold."""
        try:
            self.focus_tracker.distraction_start_time = time.time()
        except Exception:
            # If focus_tracker doesn't have the attribute, set it safely
            self.focus_tracker.distraction_start_time = None
        self.last_alert_activity = None

    def check_drift(self):
        """
        Checks for activity drift and returns activity only if:
        1. Activity is meaningful (not idle/unknown)
        2. Drift is detected
        3. Distraction has been continuous for >= 20 seconds
        4. It's not the same activity we already alerted about
        """
        activity = self.activity_detector.detect_activity()
        
        # Skip processing if activity is idle/unknown/None
        if activity in ["idle", "unknown", None]:
            self.focus_tracker.update(self.current_intent, activity)
            return None
        
        # Update focus tracker with current activity
        self.focus_tracker.update(self.current_intent, activity)
        
        # Check if drift is detected
        distracted = self.drift_detector.is_drift(self.current_intent, activity)
        
        # Only proceed if drift is detected
        if not distracted:
            return None
        
        # Get continuous distraction time
        continuous_distraction = self.focus_tracker.get_continuous_distraction_seconds()
        
        # Only trigger alert if distraction has been continuous for >= threshold
        # and it's not the same activity we already alerted about
        if (continuous_distraction >= self.distraction_threshold and
            activity != self.last_alert_activity):
            
            self.last_alert_activity = activity
            self.current_activity = activity
            return activity
        
        return None
    
    def get_current_window_title(self):
        """Returns the title of the currently active window/tab"""
        try:
            import pygetwindow as gw
            window = gw.getActiveWindow()
            return window.title if window else "Unknown"
        except:
            return "Unknown"