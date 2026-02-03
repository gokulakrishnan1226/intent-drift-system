class DriftDetector:

    def __init__(self):
        self.rules = {
            "study": ["study", "coding"],
            "coding": ["coding"],
            "browsing": ["browsing"]
        }

    def is_drift(self, intent, activity):
        if intent not in self.rules:
            return False

        allowed = self.rules[intent]
        return activity not in allowed