
import os
import pandas as pd
import matplotlib.pyplot as plt

project_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

data_dir = os.path.join(project_dir, "data", "B3_pso_logs")
figures_dir = os.path.join(project_dir, "results", "figures")

os.makedirs(figures_dir, exist_ok=True)

robots = {}

for i in range(1, 5):
    name = f"epuck{i}"

    robots[name] = pd.read_csv(
        os.path.join(data_dir, f"B3_{name}.csv")
    )

plt.figure(figsize=(9, 5))

for name, df in robots.items():
    plt.plot(
        df["time_s"],
        df["swarm_best_fitness"],
        label=name
    )

plt.xlabel("Simulation Time (s)")
plt.ylabel("Best Distance to Target (m)")
plt.title("B3: PSO Swarm Best Fitness Convergence")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(figures_dir, "B3_pso_convergence.png"),
    dpi=300
)
plt.close()

plt.figure(figsize=(8, 7))

for name, df in robots.items():
    plt.plot(
        df["x"],
        df["y"],
        label=name
    )

plt.scatter(
    [0.0],
    [1.0],
    marker="*",
    s=220,
    color="black",
    label="Target"
)

plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("B3: PSO Robot Search Trajectories")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(figures_dir, "B3_pso_trajectories.png"),
    dpi=300
)
plt.close()

summary = []

for name, df in robots.items():
    summary.append({
        "robot": name,
        "final_distance_to_target_m": round(
            float(df["current_fitness"].iloc[-1]), 4
        ),
        "best_swarm_fitness_m": round(
            float(df["swarm_best_fitness"].iloc[-1]), 4
        ),
        "messages_received": int(
            df["messages_received"].iloc[-1]
        ),
        "obstacle_detection_samples": int(
            df["obstacle_detected"].sum()
        )
    })

summary_df = pd.DataFrame(summary)

summary_path = os.path.join(
    project_dir,
    "results",
    "B3_pso_evaluation.csv"
)

summary_df.to_csv(summary_path, index=False)

print("\nB3 PSO EVALUATION")
print(summary_df.to_string(index=False))
print("\nSaved figures and evaluation successfully.")
