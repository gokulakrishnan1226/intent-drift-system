import time

class FocusTracker:
    def __init__(self):
        self.start_time = time.time()
        self.focused_time = 0
        self.distracted_time = 0

    def activity_matches_intent(self, intent, activity):
        rules = {
            "study": ["study", "coding"],
            "coding": ["coding"],
            "browsing": ["browsing"]
        }
        if intent not in rules:
            return True
        return activity in rules[intent]

    def update(self, intent, activity):
        elapsed = time.time() - self.start_time
        self.start_time = time.time()

        if self.activity_matches_intent(intent, activity):
            self.focused_time += elapsed
        else:
            self.distracted_time += elapsed

    def get_focus_score(self):
        total = self.focused_time + self.distracted_time
        if total == 0:
            return 100
        return round((self.focused_time / total) * 100, 2)