import csv
import matplotlib.pyplot as plt
from datetime import datetime
import os


def show_graph(filename="focus_log.csv"):
    """Display focus score trends and session statistics."""
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Log file '{filename}' not found.")
    
    scores = []
    times = []
    intents = []
    activities = []
    focused_mins_list = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                raise ValueError("Log file is empty or corrupted.")
            
            for row in reader:
                if row.get("FocusScore"):
                    scores.append(float(row["FocusScore"]))
                    times.append(row.get("Time", "Unknown"))
                    intents.append(row.get("Intent", "N/A"))
                    activities.append(row.get("Activity", "N/A"))
                    if row.get("FocusedMinutes"):
                        focused_mins_list.append(float(row["FocusedMinutes"]))

    except (ValueError, KeyError) as e:
        raise ValueError(f"Error parsing log file: {str(e)}")

    if not scores:
        raise ValueError("No valid data to plot in log file.")

    # Create figure with subplots
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle("Intent Drift Alert System - Session Analytics", fontsize=16, fontweight="bold")
    
    # Plot 1: Focus Score Over Time
    ax1 = axes[0]
    sessions = list(range(1, len(scores) + 1))
    colors = ["#4CAF50" if s >= 70 else "#FF9800" if s >= 50 else "#F44336" for s in scores]
    ax1.bar(sessions, scores, color=colors, alpha=0.7, edgecolor="white")
    ax1.set_xlabel("Session Number", fontweight="bold")
    ax1.set_ylabel("Focus Score (%)", fontweight="bold")
    ax1.set_title("Focus Score per Session")
    ax1.set_ylim(0, 100)
    ax1.grid(axis="y", alpha=0.3)
    
    # Plot 2: Focused Time Trend
    ax2 = axes[1]
    if focused_mins_list:
        ax2.plot(sessions[:len(focused_mins_list)], focused_mins_list, 
                marker="o", linestyle="-", color="#1E88E5", linewidth=2, markersize=6)
        ax2.fill_between(sessions[:len(focused_mins_list)], focused_mins_list, alpha=0.3, color="#1E88E5")
        ax2.set_xlabel("Session Number", fontweight="bold")
        ax2.set_ylabel("Focused Time (minutes)", fontweight="bold")
        ax2.set_title("Focused Duration Trend")
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.style.use("dark_background")
    plt.show()