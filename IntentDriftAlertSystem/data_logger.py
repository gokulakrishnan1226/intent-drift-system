import csv
import os
from datetime import datetime

class DataLogger:
    def _init_(self, filename="focus_log.csv"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Time", "Intent", "Activity", "FocusScore"])

    def log(self, intent, activity, score):
        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                intent,
                activity,
                score
            ])