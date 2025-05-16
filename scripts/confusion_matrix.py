import matplotlib
matplotlib.use('Agg')  # Usa backend non interattivo

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Confusion Matrix - Fold 1 (Set 1) ===
fold1 = pd.DataFrame(
    [[286417, 0],
     [2, 181]],
    index=["Actual Negative", "Actual Positive"],
    columns=["Predicted Negative", "Predicted Positive"]
)

# === Confusion Matrix - Fold 2 (Set 2) ===
fold2 = pd.DataFrame(
    [[286414, 3],
     [2, 181]],
    index=["Actual Negative", "Actual Positive"],
    columns=["Predicted Negative", "Predicted Positive"]
)

# === Plot Fold 1 with color bar and Blues colormap ===
plt.figure(figsize=(6, 5))
sns.heatmap(fold1, annot=True, fmt='d', cmap='Blues', linewidths=0.5, linecolor='gray', cbar=True)
plt.title("Confusion Matrix – Fold 1 (Set 1)", fontsize=13)
plt.xlabel("Predicted Class", fontsize=11)
plt.ylabel("Actual Class", fontsize=11)
plt.tight_layout()
plt.savefig("confusion_matrix_fold1_blues.png")
plt.close()

# === Plot Fold 2 with color bar and Greens colormap ===
plt.figure(figsize=(6, 5))
sns.heatmap(fold2, annot=True, fmt='d', cmap='Greens', linewidths=0.5, linecolor='gray', cbar=True)
plt.title("Confusion Matrix – Fold 2 (Set 2)", fontsize=13)
plt.xlabel("Predicted Class", fontsize=11)
plt.ylabel("Actual Class", fontsize=11)
plt.tight_layout()
plt.savefig("confusion_matrix_fold2_greens.png")
plt.close()

print("Confusion matrices saved: Set 1 = Blues, Set 2 = Greens")
