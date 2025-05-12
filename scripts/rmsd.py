import matplotlib
matplotlib.use('Agg')  # Ensure compatibility in environments without a GUI

import pandas as pd
import matplotlib.pyplot as plt

# === Data: PDB ID, RMSD, Q-score ===
data = [
    ["5nx1:C", 0.4107, 0.5090],
    ["6bx8:B", 0.4000, 0.5002],
    ["4bqd:A", 0.3730, 0.3535],
    ["1yc0:I", 0.3357, 0.4190],
    ["4dtg:K", 0.4430, 0.4567],
    ["1f5r:I", 0.6203, 0.4711],
    ["1zr0:B", 0.4310, 0.4355],
    ["3wny:A", 0.6027, 0.4806],
    ["1bun:B", 0.7111, 0.4346],
    ["3m7q:B", 0.5230, 0.4455],
    ["6q61:A", 0.4646, 0.4635],
    ["4ntw:B", 0.7731, 0.4376],
    ["5yv7:A", 0.5173, 0.4532],
    ["1dtx:A", 0.5102, 0.4612],
    ["3byb:A", 0.4520, 0.4720],
    ["4u30:X", 0.5816, 0.4997],
    ["6yhy:A", 0.4311, 0.4650],
    ["1knt:A", 0.5897, 0.4902],
    ["5jb7:A", 0.5488, 0.4838],
    ["5m4v:A", 0.4397, 0.4809],
    ["1yld:B", 0.5875, 0.4815],
    ["1fak:I", 0.4866, 0.4960],
    ["4u32:X", 0.3114, 0.5130],
    ["5jbt:Y", 2.9166, 0.3788],  # outlier
]

# Create DataFrame
df = pd.DataFrame(data, columns=["PDB ID", "RMSD", "Q-score"])

# === Plot ===
plt.figure(figsize=(10, 6))
plt.scatter(df["RMSD"], df["Q-score"], color="mediumseagreen", s=80)

# Highlight outliers (RMSD > 2)
outliers = df[df["RMSD"] > 2]
for _, row in outliers.iterrows():
    plt.annotate(row["PDB ID"], (row["RMSD"], row["Q-score"]),
                 textcoords="offset points", xytext=(-10, 10),
                 ha='center', color='red', fontsize=9)

# Labels and title
plt.xlabel("RMSD (Å)")
plt.ylabel("Q-score")
plt.title("Structural Alignment of Kunitz Domains (RMSD vs Q-score)")
plt.grid(True)
plt.tight_layout()

# Save the plot
plt.savefig("kunitz_structures_scatter.png")
print("Scatter plot saved as: kunitz_structures_scatter.png")
