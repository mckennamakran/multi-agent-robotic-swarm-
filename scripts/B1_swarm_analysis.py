import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA_DIR = os.path.join(PROJECT_DIR, "data", "B1_swarm_logs")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

robots = {}

for i in range(1, 5):
    name = f"epuck{i}"
    path = os.path.join(DATA_DIR, f"B1_{name}.csv")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing log: {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(f"No data in {path}")

    df = df.sort_values("time_s").reset_index(drop=True)
    robots[name] = df

plt.figure(figsize=(8, 7))

for name, df in robots.items():
    positions = df.dropna(subset=["x", "y"])

    if positions.empty:
        continue

    plt.plot(
        positions["x"],
        positions["y"],
        label=name,
        linewidth=1.5
    )

    plt.scatter(
        positions["x"].iloc[0],
        positions["y"].iloc[0],
        marker="o",
        s=45
    )

    plt.scatter(
        positions["x"].iloc[-1],
        positions["y"].iloc[-1],
        marker="x",
        s=70
    )

plt.title("B1: Swarm Robot Trajectories")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(FIGURES_DIR, "B1_swarm_trajectories.png"),
    dpi=300
)
plt.close()

plt.figure(figsize=(9, 5))

for name, df in robots.items():
    plt.plot(
        df["time_s"],
        df["messages_received"],
        label=name
    )

plt.title("B1: Swarm Communication")
plt.xlabel("Simulation Time (s)")
plt.ylabel("Messages Received")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(FIGURES_DIR, "B1_communication.png"),
    dpi=300
)
plt.close()

plt.figure(figsize=(9, 5))

for name, df in robots.items():
    plt.plot(
        df["time_s"],
        df["front_left"],
        label=f"{name} left",
        alpha=0.75
    )

plt.axhline(
    80,
    color="red",
    linestyle="--",
    label="Front obstacle threshold"
)

plt.title("B1: Front-Left Proximity Sensor Readings")
plt.xlabel("Simulation Time (s)")
plt.ylabel("Sensor Reading")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(FIGURES_DIR, "B1_proximity_sensors.png"),
    dpi=300
)
plt.close()

plt.figure(figsize=(9, 5))

for name, df in robots.items():
    plt.plot(
        df["time_s"],
        df["escape_remaining"],
        label=name
    )

plt.title("B1: Obstacle Escape Manoeuvres")
plt.xlabel("Simulation Time (s)")
plt.ylabel("Escape Steps Remaining")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(FIGURES_DIR, "B1_obstacle_escapes.png"),
    dpi=300
)
plt.close()

summary = []

for name, df in robots.items():
    positions = df.dropna(subset=["x", "y"])

    if len(positions) > 1:
        dx = np.diff(positions["x"].to_numpy())
        dy = np.diff(positions["y"].to_numpy())
        distance = float(np.sum(np.hypot(dx, dy)))
    else:
        distance = np.nan

    escape_values = df["escape_remaining"].fillna(0).to_numpy()

    escape_starts = int(
        np.sum(
            (escape_values > 0)
            & (np.r_[0, escape_values[:-1]] == 0)
        )
    )

    summary.append({
        "robot": name,
        "duration_s": round(
            float(df["time_s"].iloc[-1] - df["time_s"].iloc[0]),
            3
        ),
        "messages_sent": int(df["messages_sent"].iloc[-1]),
        "messages_received": int(df["messages_received"].iloc[-1]),
        "distance_travelled_m": round(distance, 4),
        "logged_escape_sequences": escape_starts,
        "maximum_front_left": round(
            float(df["front_left"].max()),
            2
        ),
        "maximum_front_right": round(
            float(df["front_right"].max()),
            2
        )
    })

summary_df = pd.DataFrame(summary)

summary_path = os.path.join(
    RESULTS_DIR,
    "B1_swarm_evaluation.csv"
)

summary_df.to_csv(summary_path, index=False)

print("\nCOMPONENT B1 - SWARM EVALUATION")
print(summary_df.to_string(index=False))
print("\nSaved evaluation:", summary_path)
print("Saved figures:", FIGURES_DIR)
print("\nB1 analysis complete.")
