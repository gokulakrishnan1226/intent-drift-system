import time
from drift_detector import DriftDetector
from activity_detector import ActivityDetector
from focus_tracker import FocusTracker
from data_logger import DataLogger 

class BackendController:
    def __init__(self):
        self.current_intent = None
        self.monitoring_paused = False
        self.popup_open = False
        self.distraction_start = None
        self.logger = DataLogger()
        self.focus_tracker = FocusTracker()
        self.detector = ActivityDetector()
        self.drift_detector = DriftDetector()
    
    def get_focus_score(self):
        return self.focus_tracker.get_focus_score()

    def log_event(self, activity, motivation):
        self.logger.log(
            self.current_intent,
            activity,
            self.get_focused_minutes(),
            self.get_focus_score(),
            motivation
        )
    
    def get_focused_minutes(self):
        return round(self.focus_tracker.focused_time / 60, 2)

    def set_intent(self, intent):
        self.current_intent = intent
        self.monitoring_paused = False

    def get_activity(self):
        return self.detector.get_current_activity()

    def check_drift(self):
        if self.monitoring_paused or self.current_intent is None:
            return None

        activity = self.get_activity()
        self.focus_tracker.update(self.current_intent, activity)
        distracted = self.drift_detector.is_drift(self.current_intent, activity)
        
        if distracted:
            if self.distraction_start is None:
                self.distraction_start = time.time()
            elif time.time() - self.distraction_start >= 20:
                if not self.popup_open:
                    return activity
        else:
            self.distraction_start = None

        return None