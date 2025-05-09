
#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')  # usa un backend non interattivo
import matplotlib.pyplot as plt

# Soglie (ordinate come nei tuoi file)
thresholds = ['1e-10', '1e-9', '1e-8', '1e-7', '1e-6', '1e-5', '1e-1', '1e-2', '1e-3', '1e-4']

# MCC estratti da performance_set1_thresholds.txt
mcc_set1 = [1.0, 1.0, 0.9973, 0.9973, 0.9945, 0.9945, 0.9918, 0.9918, 0.9918, 0.9918]

# MCC estratti da performance_set2_thresholds.txt
mcc_set2 = [1.0, 1.0, 1.0, 0.9945, 0.9945, 0.9945, 0.9918, 0.9918, 0.9918, 0.989]

# Crea il grafico
plt.figure(figsize=(10, 6))
plt.plot(thresholds, mcc_set1, marker='o', label='Set 1')
plt.plot(thresholds, mcc_set2, marker='s', label='Set 2')

# Etichette e layout
plt.xlabel('E-value Threshold')
plt.ylabel('MCC (Matthews Correlation Coefficient)')
plt.title('MCC Values for Different E-value Thresholds (Set 1 vs Set 2)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Salva il grafico
plt.savefig("mcc_plot_from_threshold_files.png", dpi=300)
plt.show()


#%%
