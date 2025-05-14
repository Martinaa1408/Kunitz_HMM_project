import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend (no GUI)

import matplotlib.pyplot as plt

# Thresholds ordered from 1e-10 (most stringent) to 0.1 (least stringent)
thresholds = ['1e-10', '1e-9', '1e-8', '1e-7', '1e-6', '1e-5', '0.0001', '0.001', '0.01', '0.1']

# MCC values extracted from the performance files
mcc_set1 = [0.9918, 0.9918, 0.9918, 0.9918, 0.9945, 0.9945, 0.9973, 0.9973, 1.0, 1.0]
mcc_set2 = [0.989, 0.9918, 0.9918, 0.9918, 0.9945, 0.9945, 0.9945, 1.0, 1.0, 1.0]

# Identify the best MCC value for Set 1
best_index = mcc_set1.index(max(mcc_set1))
best_threshold = thresholds[best_index]
best_mcc = mcc_set1[best_index]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(thresholds, mcc_set1, marker='o', label='Set 1', color='blue')
plt.plot(thresholds, mcc_set2, marker='s', label='Set 2', color='orange')

# Highlight the best point for Set 1
plt.scatter(best_threshold, best_mcc, color='red', zorder=5)
plt.text(best_threshold, best_mcc + 0.001, f'Best: {best_threshold}', color='red', ha='center')

# Axis labels and layout
plt.xlabel('E-value Threshold')
plt.ylabel('MCC (Matthews Correlation Coefficient)')
plt.title('MCC Values for Different E-value Thresholds (Set 1 vs Set 2)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the figure
plt.savefig("mcc_thresholds_best_marked_updated.png")
print("Saved as: mcc_thresholds_best_marked_updated.png")
