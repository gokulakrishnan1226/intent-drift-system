class DriftDetector:
    def __init__(self):
        # Define what activities are allowed for each intent
        self.rules = {
            "study": ["study", "coding"],  # Both study and coding are acceptable for study intent
            "coding": ["coding"],           # Only coding for coding intent
            "browsing": ["browsing"]        # Only browsing for browsing intent
        }

    def is_drift(self, intent, activity):
        """
        Detects if current activity drifts from the intended activity.
        Drift happens when:
        - Activity is social media (always a distraction)
        - Activity doesn't match the intent's allowed activities
        """
        # Social media is always a distraction
        if activity in ["social"]:
            return True
        
        if intent not in self.rules:
            return False
        
        # Check if current activity matches intent's allowed activities
        return activity not in self.rules[intent]