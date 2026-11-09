
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(BASE, "data", "B4_neural_logs")
RESULTS = os.path.join(BASE, "results")
FIGURES = os.path.join(RESULTS, "figures")

os.makedirs(FIGURES, exist_ok=True)

summary = []

plt.figure(figsize=(9, 7))

for i in range(1, 5):
    name = f"epuck{i}"
    path = os.path.join(DATA, f"B4_{name}.csv")

    df = pd.read_csv(path)

    print(name, "Rows:", len(df))

    plt.plot(df["x"], df["y"], label=name)

    summary.append({
        "robot": name,
        "duration_s": round(float(df["time_s"].max()), 2),
        "samples": len(df),
        "obstacle_samples": int(df["obstacle_detected"].sum()),
        "forward": int((df["prediction"] == 0).sum()),
        "left": int((df["prediction"] == 1).sum()),
        "right": int((df["prediction"] == 2).sum())
    })

plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("B4: Neural Network Robot Trajectories")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()

figure_path = os.path.join(
    FIGURES, "B4_neural_trajectories.png"
)

plt.savefig(figure_path, dpi=300)
plt.close()

result = pd.DataFrame(summary)

csv_path = os.path.join(
    RESULTS, "B4_neural_evaluation.csv"
)

result.to_csv(csv_path, index=False)

print("\nB4 EVALUATION")
print(result.to_string(index=False))
print("\nSAVED:", figure_path)
print("SAVED:", csv_path)
