import pygetwindow as gw

class ActivityDetector:
    def __init__(self):
        # Define app categories
        self.study_apps = ["docs", "pdf", "ppt", "csv", "word", "pycharm", "vscode", "notes", "notepad", "excel", "powerpoint"]
        self.browsing_apps = ["chrome", "edge", "firefox", "opera", "safari"]
        self.social_apps = ["youtube", "whatsapp", "facebook", "twitter", "instagram", "telegram", "discord"]
        self.coding_apps = ["pycharm", "vscode", "code", "visual studio", "intellij", "atom", "sublime"]

    def detect_activity(self):
        """
        Detects current active window/tab and categorizes activity.
        Returns: study, coding, social, browsing, idle, browsing (if unknown app)
        """
        try:
            window = gw.getActiveWindow()
            if not window:
                return "idle"

            title = window.title.lower()
            
            # Check if the window is desktop or idle
            if any(k in title for k in ["desktop", "program manager", "explorer", "shell", "windows", "taskbar"]):
                return "idle"

            # Check for coding first
            if any(k in title for k in self.coding_apps):
                return "coding"
            
            # Check for study apps
            if any(k in title for k in self.study_apps):
                return "study"
            
            # Check for social media (distraction)
            if any(k in title for k in self.social_apps):
                return "social"
            
            # Check for browsing
            if any(k in title for k in self.browsing_apps):
                return "browsing"
            
            # Check for specific keywords that indicate study
            if any(k in title for k in ["lecture", "course", "class", "tutorial", "documentation"]):
                return "study"

            # If it's an unknown app (not idle, not recognized), treat as browsing activity
            # This way it will be detected as drift when user should be studying/coding
            return "browsing"

        except Exception as e:
            print(f"Activity detection error: {e}")
            return "unknown"