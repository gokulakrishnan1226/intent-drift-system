class DriftDetector:
    def __init__(self):
        self.rules = {
            "study": ["study"],
            "browsing": ["browsing"],
            "coding": ["study"]
        }

    def is_drift(self, intent, activity):
        if activity == "neutral":
            return False
        if intent not in self.rules:
            return False
        return activity not in self.rules[intent]