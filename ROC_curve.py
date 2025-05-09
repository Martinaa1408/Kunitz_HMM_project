#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')  # per evitare problemi su sistemi senza GUI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc

# Carica i dati dei due set
set1_df = pd.read_csv("/home/martina_caste/Kunitz_HMM_project/results/set_1.class", sep=None, engine="python", header=None)
set2_df = pd.read_csv("/home/martina_caste/Kunitz_HMM_project/results/set_2.class", sep=None, engine="python", header=None)

# Assegna nomi alle colonne
set1_df.columns = ["ID", "real_class", "evalue", "pred_class"]
set2_df.columns = ["ID", "real_class", "evalue", "pred_class"]

# Converte tipi
set1_df["real_class"] = set1_df["real_class"].astype(int)
set2_df["real_class"] = set2_df["real_class"].astype(int)
set1_df["evalue"] = set1_df["evalue"].astype(float)
set2_df["evalue"] = set2_df["evalue"].astype(float)

# Funzione per costruire ROC da un dataframe
def get_roc_data(df):
    y_true = df["real_class"]
    # Evita -inf nel log: sostituisci e-value 0 con un valore molto piccolo
    score = -np.log10(df["evalue"].replace(0, 1e-300))
    fpr, tpr, _ = roc_curve(y_true, score)
    roc_auc = auc(fpr, tpr)
    return fpr, tpr, roc_auc

# Calcola ROC per ciascun set
fpr1, tpr1, auc1 = get_roc_data(set1_df)
fpr2, tpr2, auc2 = get_roc_data(set2_df)

# Crea la figura
plt.figure(figsize=(8, 6))
plt.plot(fpr1, tpr1, label=f'Set 1 (AUC = {auc1:.3f})', color='steelblue')
plt.plot(fpr2, tpr2, label=f'Set 2 (AUC = {auc2:.3f})', color='darkorange')
plt.plot([0, 1], [0, 1], 'k--', lw=1)

# Etichette e layout
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve from e-value Scores')
plt.legend(loc='lower right')
plt.grid(True)
plt.tight_layout()

# Salva l'immagine
plt.savefig("roc_curve_evalue_sets.png", dpi=300)
