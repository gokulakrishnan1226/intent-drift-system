import csv
import matplotlib.pyplot as plt

def show_graph(filename="productivity.csv"):
    scores = []
    times = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            scores.append(float(row["FocusScore"]))
            times.append(row["Time"])

    if not scores:
        print("No data to plot.")
        return

    plt.figure(figsize=(10,5))
    plt.plot(scores)
    plt.title("Focus Score Over Time")
    plt.xlabel("Session")
    plt.ylabel("Focus Score (%)")
    plt.show()