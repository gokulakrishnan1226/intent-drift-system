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
        1. Drift is detected
        2. Activity is not idle/unknown
        3. Distraction has been continuous for >= 20 seconds
        """
        activity = self.activity_detector.detect_activity()
        
        # Update focus tracker with current activity
        self.focus_tracker.update(self.current_intent, activity)
        
        # Check if drift is detected
        distracted = self.drift_detector.is_drift(self.current_intent, activity)
        
        # Get continuous distraction time
        continuous_distraction = self.focus_tracker.get_continuous_distraction_seconds()
        
        # Only trigger alert if:
        # 1. Drift is detected
        # 2. Activity is meaningful (not idle/unknown)
        # 3. Distraction has lasted >= 20 seconds
        # 4. It's not the same activity we already alerted about
        if (distracted and 
            activity not in ["idle", "unknown", None] and
            continuous_distraction >= self.distraction_threshold and
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