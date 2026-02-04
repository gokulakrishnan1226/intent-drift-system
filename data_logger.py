import csv
import os
from datetime import datetime

class DataLogger:
    def __init__(self, filename="focus_log.csv"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Time",
                    "Intent",
                    "Activity",
                    "FocusedMinutes",
                    "FocusScore",
                    "Motivation"
                ])

    def log(self, intent, activity, focused_minutes, focus_score, motivation):
        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                intent,
                activity,
                focused_minutes,
                focus_score,
                motivation
            ])