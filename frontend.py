import tkinter as tk
from tkinter import ttk

class FrontendUI:
    def __init__(self, root, backend):
        self.backend = backend
        self.root = root
        self.root.title("Intent Drift Alert System")
        self.root.geometry("500x400")
        self.create_ui()

    def create_ui(self):
        ttk.Label(self.root, text="Intent Drift Alert System", font=("Segoe UI", 16, "bold")).pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack()

        ttk.Label(frame, text="Select Intent").grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Button(frame, text="Study", command=lambda: self.backend.set_intent("study")).grid(row=1, column=0, padx=10)
        
        ttk.Button(frame, text="Browsing", command=lambda: self.backend.set_intent("browsing")).grid(row=1, column=2, padx=10)

        self.status_label = ttk.Label(self.root, text="Current Intent: None")
        self.status_label.pack(pady=10)

        self.monitor_label = ttk.Label(self.root, text="Monitoring: Active", foreground="green")
        self.monitor_label.pack()

        
    def update_status(self, intent):
        self.status_label.config(text=f"Current Intent: {intent}")


    def update_monitoring(self, paused):
        if paused:
            self.monitor_label.config(text="Monitoring: Paused", foreground="red")
        else:
            self.monitor_label.config(text="Monitoring: Active", foreground="green")