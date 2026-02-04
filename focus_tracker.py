import time

class FocusTracker:
    def __init__(self):
        self.start_time = time.time()
        self.focused_time = 0.0
        self.distracted_time = 0.0
        self.current_activity = None
        self.distraction_start_time = None  # Track when distraction started
        self.last_activity = None

    def activity_matches_intent(self, intent, activity):
        rules = {
            "study": ["study", "coding"],
            "coding": ["coding"],
            "browsing": ["browsing"]
        }
        return activity in rules.get(intent, [])

    def update(self, intent, activity):
        now = time.time()
        elapsed = now - self.start_time
        self.start_time = now

        if self.activity_matches_intent(intent, activity):
            self.focused_time += elapsed
            self.distraction_start_time = None  # Reset distraction timer
        else:
            self.distracted_time += elapsed
            # Start tracking continuous distraction
            if self.distraction_start_time is None:
                self.distraction_start_time = now

        self.current_activity = activity
        self.last_activity = activity

    def get_focused_minutes(self):
        return round(self.focused_time / 60, 1)

    def get_distracted_seconds(self):
        return round(self.distracted_time, 1)

    def get_continuous_distraction_seconds(self):
        """Returns how long user has been distracted continuously"""
        if self.distraction_start_time is None:
            return 0
        return round(time.time() - self.distraction_start_time, 1)

    def reset(self):
        self.start_time = time.time()
        self.focused_time = 0.0
        self.distracted_time = 0.0
        self.current_activity = None
        self.distraction_start_time = None
        self.last_activity = None