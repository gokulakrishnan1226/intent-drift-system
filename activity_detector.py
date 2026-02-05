import pygetwindow as gw


class ActivityDetector:
    """Detect user activity from active window title."""
    
    # Keywords that indicate studying/focus activities
    STUDY_KEYWORDS = [
        "lecture", "tutorial", "course", "lesson",
        "python", "java", "c++", "cpp", "javascript", "js",
        "os", "dbms", "database", "sql",
        "gate", "engineering", "programming", "code", "coding",
        "algorithm", "data structure", "math", "mathematics",
        "physics", "chemistry", "biology", "science",
        "education", "learning", "udemy", "coursera", "edx"
    ]
    
    # Keywords that indicate social/entertainment activities
    SOCIAL_KEYWORDS = [
        "facebook", "instagram", "tiktok", "snapchat",
        "twitter", "x.com", "reddit", "imgur",
        "twitch", "stream", "gaming", "game",
        "funny", "meme", "joke", "viral", "trending",
        "news feed", "home feed", "explore",
        "shorts", "reels", "video"
    ]
    
    def __init__(self):
        pass

    def get_current_activity(self):
        """
        Detect current activity from active window.
        Returns: 'study', 'browsing', 'social', 'coding', 'neutral', or 'unknown'
        """
        try:
            window = gw.getActiveWindow()
            if not window:
                return "unknown"

            title = window.title.lower()

            # ---------- YOUTUBE LOGIC (CONTEXT-AWARE) ----------
            if "youtube" in title:
                # Home page or no specific video
                if title.strip() == "youtube" or "home" in title:
                    return "neutral"

                # Check for study content
                if any(word in title for word in self.STUDY_KEYWORDS):
                    return "study"
                
                # Check for entertainment/social
                if any(word in title for word in self.SOCIAL_KEYWORDS):
                    return "social"
                
                # Default to studying if searching for educational-sounding content
                if "search" in title or "?" in title:
                    return "study"  # Assume research by default
                
                return "study"  # Default YouTube to study

            # ---------- STUDY APPS ----------
            if any(x in title for x in [
                "word", "pdf", "notepad", "powerpoint",
                "visual studio", "pycharm", "code", "ide",
                "github", "gitlab", "jupyter", "python",
                "document", "presentation"
            ]):
                return "study"

            # ---------- CODING TOOLS ----------
            if any(x in title for x in [
                "vs code", "visual studio", "terminal", "cmd",
                "powershell", "bash", "git", "github"
            ]):
                return "coding"

            # ---------- BROWSERS ----------
            if any(x in title for x in [
                "chrome", "edge", "firefox", "safari", "browser"
            ]):
                return "browsing"

            # ---------- SOCIAL/ENTERTAINMENT ----------
            if any(x in title for x in self.SOCIAL_KEYWORDS):
                return "social"

            return "other"

        except Exception:
            return "unknown"
    
    def is_study_related(self, title_text):
        """Check if window title indicates study activity."""
        title = title_text.lower()
        return any(word in title for word in self.STUDY_KEYWORDS)