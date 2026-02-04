import tkinter as tk
import time
from activity_detector import ActivityDetector
from frontend import FrontendUI

detector = ActivityDetector()

class BackendController:
    def __init__(self, root):
        self.root = root
        self.current_intent = None
        self.monitoring_paused = False
        self.popup_open = False
        self.distraction_start = None
        self.focus_score = 100

    def set_intent(self, intent):
        self.current_intent = intent
        self.monitoring_paused = False
        self.ui.update_status(intent)
        self.ui.update_monitoring(False)

    def pause_monitoring(self):
        self.monitoring_paused = True
        self.ui.update_monitoring(True)

def show_intent_selector():
    win = tk.Toplevel(root)
    win.title("Select New Intent")
    win.geometry("250x200")

    tk.Label(win, text="Select New Intent").pack(pady=10)

    tk.Button(win, text="Study", command=lambda: select_new("study", win)).pack(pady=5)
    
    tk.Button(win, text="Browsing", command=lambda: select_new("browsing", win)).pack(pady=5)

def select_new(intent, win):
    backend.set_intent(intent)
    win.destroy()

def handle_choice(choice, popup):
    backend.popup_open = False
    backend.distraction_start = None

    if choice == "ignore":
        backend.pause_monitoring()

    elif choice == "change":
        popup.destroy()
        show_intent_selector()
        return

    popup.destroy()

def show_alert(activity):
    backend.popup_open = True

    popup = tk.Toplevel(root)
    popup.title("Distraction Detected")
    popup.geometry("320x220")
    popup.lift()
    popup.attributes("-topmost", True)

    tk.Label(popup, text="You are distracted!", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(popup, text=f"Activity: {activity}").pack()

    tk.Button(popup, text="Continue", width=15, command=lambda: handle_choice("continue", popup)).pack(pady=5)
    tk.Button(popup, text="Ignore", width=15, command=lambda: handle_choice("ignore", popup)).pack(pady=5)
    tk.Button(popup, text="Change Intent", width=15, command=lambda: handle_choice("change", popup)).pack(pady=5)

def auto_check():
    if backend.monitoring_paused or backend.current_intent is None:
        root.after(5000, auto_check)
        return

    activity = detector.get_current_activity()

    distracted = backend.current_intent == "study" and activity in ["social", "browsing", "other"]

    if distracted:
        if backend.distraction_start is None:
            backend.distraction_start = time.time()
        elif time.time() - backend.distraction_start >= 15:
            if not backend.popup_open:
                show_alert(activity)
    else:
        backend.distraction_start = None

    root.after(5000, auto_check)

root = tk.Tk()
backend = BackendController(root)
ui = FrontendUI(root, backend)
backend.ui = ui

auto_check()
root.mainloop()