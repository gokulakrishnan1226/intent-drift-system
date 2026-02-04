import pygetwindow as gw

class ActivityDetector:
    def get_current_activity(self):
        try:
            window = gw.getActiveWindow()
            if not window:
                return "unknown"

            title = window.title.lower()

            # ---------- YOUTUBE LOGIC ----------
            if "youtube" in title:
                # Case 1: Home page or no video selected
                if title.strip() == "youtube":
                    return "neutral"   # <-- IMPORTANT

                study_keywords = [
                    "lecture", "tutorial", "course", "lesson",
                    "python", "java", "c++", "os", "dbms",
                    "gate", "engineering", "programming"
                ]

                if any(word in title for word in study_keywords):
                    return "study"
                else:
                    return "social"

            # ---------- STUDY APPS ----------
            if any(x in title for x in [
                "word", "pdf", "notepad", "powerpoint",
                "visual studio", "pycharm", "code"
            ]):
                return "study"

            # ---------- BROWSERS ----------
            if any(x in title for x in [
                "chrome", "edge", "firefox"
            ]):
                return "browsing"

            return "other"

        except Exception:
            return "unknown"