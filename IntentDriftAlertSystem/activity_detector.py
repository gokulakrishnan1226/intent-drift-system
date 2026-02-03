import win32gui
import win32process
import psutil

class ActivityDetector:
    def get_current_activity(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            app = process.name().lower()
            title = win32gui.GetWindowText(hwnd).lower()

            if "code" in app:
                return "coding"

            if "chrome" in app or "edge" in app or "firefox" in app:
                if any(x in title for x in ["youtube", "facebook", "instagram", "netflix"]):
                    return "social"
                elif any(x in title for x in ["github", "leetcode", "stackoverflow", "docs"]):
                    return "study"
                else:
                    return "browsing"

            return "other"

        except:
            return "unknown"