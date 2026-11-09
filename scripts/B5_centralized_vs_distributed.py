
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS = os.path.join(BASE, "results")
FIGURES = os.path.join(RESULTS, "figures")

os.makedirs(FIGURES, exist_ok=True)

DATA = os.path.join(BASE, "data", "B2_consensus_logs")

robots = []

for i in range(1, 5):
    df = pd.read_csv(os.path.join(DATA, f"B2_epuck{i}.csv"))
    robots.append(df)

initial = np.array([10.0, 20.0, 30.0, 40.0])
centralized = np.mean(initial)

iterations = sorted(
    set.intersection(
        *[set(df["iteration"]) for df in robots]
    )
)

distributed = np.array([
    [
        float(df.loc[
            df["iteration"] == iteration,
            "consensus_value"
        ].iloc[0])
        for df in robots
    ]
    for iteration in iterations
])

centralized_values = np.full(len(iterations), centralized)

distributed_mean = distributed.mean(axis=1)
distributed_error = np.mean(
    np.abs(distributed - centralized), axis=1
)

plt.figure(figsize=(9, 5))

plt.plot(
    iterations,
    centralized_values,
    "--",
    label="Centralized average"
)

plt.plot(
    iterations,
    distributed_mean,
    label="Distributed swarm average"
)

plt.xlabel("Iteration")
plt.ylabel("Consensus Value")
plt.title("B5: Centralized vs Distributed Consensus")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(FIGURES, "B5_centralized_vs_distributed.png"),
    dpi=300
)
plt.close()

plt.figure(figsize=(9, 5))

plt.plot(iterations, distributed_error)

plt.xlabel("Iteration")
plt.ylabel("Mean Absolute Error")
plt.title("B5: Distributed Consensus Error")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(FIGURES, "B5_distributed_error.png"),
    dpi=300
)
plt.close()

summary = pd.DataFrame([
    {
        "approach": "Centralized",
        "final_average": centralized,
        "final_error": 0.0,
        "communication": "Central coordinator required",
        "failure_risk": "Single point of failure"
    },
    {
        "approach": "Distributed",
        "final_average": distributed_mean[-1],
        "final_error": distributed_error[-1],
        "communication": "Robot-to-robot messages",
        "failure_risk": "No central coordinator"
    }
])

summary.to_csv(
    os.path.join(RESULTS, "B5_comparison.csv"),
    index=False
)

print("\nB5 COMPARISON")
print(summary.to_string(index=False))
print("\nB5 COMPLETE")
