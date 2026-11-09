
import os
import pandas as pd
import matplotlib.pyplot as plt

project_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

data_dir = os.path.join(
    project_dir, "data", "B2_consensus_logs"
)

figures_dir = os.path.join(
    project_dir, "results", "figures"
)

os.makedirs(figures_dir, exist_ok=True)

plt.figure(figsize=(9, 5))

for i in range(1, 5):
    name = f"epuck{i}"

    df = pd.read_csv(
        os.path.join(data_dir, f"B2_{name}.csv")
    )

    plt.plot(
        df["iteration"],
        df["consensus_value"],
        marker="o",
        markersize=3,
        label=name
    )

    print(
        name,
        "| Final value:",
        df["consensus_value"].iloc[-1],
        "| Final error:",
        df["absolute_error"].iloc[-1]
    )

plt.axhline(
    25,
    color="black",
    linestyle="--",
    label="Target average = 25"
)

plt.xlabel("Consensus Iteration")
plt.ylabel("Consensus Value")
plt.title("B2: Distributed Average Consensus")
plt.legend()
plt.grid(True)
plt.tight_layout()

output = os.path.join(
    figures_dir, "B2_consensus_convergence.png"
)

plt.savefig(output, dpi=300)
plt.close()

print("Saved:", output)
