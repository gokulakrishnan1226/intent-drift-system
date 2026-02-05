class DriftDetector:
    """
    Detects if user activity has drifted from their stated intent.
    Uses context-aware rules to avoid false positives.
    """
    
    def __init__(self):
        # Define which activities align with each intent
        self.allowed_activities = {
            "study": ["study", "coding", "neutral"],  # Study mode allows studying or coding
            "coding": ["coding", "study"],             # Coding mode allows both coding and study
            "browsing": ["browsing", "social", "neutral"],  # Browsing allows all
        }

    def is_drift(self, intent, activity):
        """
        Check if activity has drifted from intent.
        
        Args:
            intent: User's stated intent ('study', 'coding', 'browsing')
            activity: Detected activity ('study', 'social', 'coding', 'browsing', etc)
        
        Returns:
            True if activity is off-topic, False if aligned
        """
        
        # Neutral activity is never considered drift
        if activity == "neutral" or activity == "unknown":
            return False
        
        # If intent not recognized, don't flag drift
        if intent not in self.allowed_activities:
            return False
        
        # Check if activity aligns with intent
        allowed = self.allowed_activities[intent]
        
        # If activity is in allowed list, no drift
        if activity in allowed:
            return False
        
        # For study intent: coding and study are both acceptable
        if intent == "study" and activity in ["study", "coding"]:
            return False
        
        # For coding intent: both activities acceptable
        if intent == "coding" and activity in ["coding", "study"]:
            return False
        
        # Everything else is drift
        return True