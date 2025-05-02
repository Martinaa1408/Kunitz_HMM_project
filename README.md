
# Kunitz Domain Classifier using Profile HMM

This repository presents a comprehensive and reproducible pipeline to construct and evaluate a Profile Hidden Markov Model (HMM) aimed at recognizing Kunitz-type protease inhibitor domains (Pfam ID: PF00014) within protein sequences. These domains are well-conserved and are critical for inhibiting serine proteases, playing an important role in biological functions like inflammation, coagulation, and immune response regulation.

The project implements a binary classification system to distinguish proteins that contain a Kunitz domain from those that do not, leveraging both structural and sequence-based data.

## Overview

The classification strategy is based on building an HMM using curated, non-redundant sequences extracted from experimentally solved protein structures. These are aligned to preserve structural conservation, then used to generate a probabilistic model via HMMER. The model is tested and optimized using labeled protein sequences from the SwissProt database, with evaluation performed over a range of e-value thresholds.

Classification performance is assessed using standard metrics such as:
- Accuracy
- Precision
- Recall
- Matthews Correlation Coefficient (MCC)

The project ensures that training and test datasets are non-overlapping, with redundancy filtered via sequence identity and alignment coverage using BLAST.

## Project Structure and Content Description

The repository is organized to reflect a logical workflow and reproducibility of the full pipeline:

- `data/`: Contains all raw input data, including:
  - FASTA files with Kunitz-containing proteins (`all_kunitz.fasta`)
  - Non-redundant sequences from PDB (`pdb_kunitz_nr.fasta`)
  - The SwissProt database (`uniprot_sprot.fasta`)
  - ID lists for filtering (`*.ids`)

- `models/`: Includes HMMs trained using `hmmbuild`.

- `scripts/`: Contains Bash and Python scripts for:
  - Running the pipeline (`run_pipeline.sh`)
  - Extracting sequences by ID (`get_seq.py`)
  - Extracting best BLAST/HMM hits (`get_best_hits.sh`)
  - Evaluating classification (`performance.py`)

- `results/`: Stores all intermediate and final outputs from BLAST, HMMER, and evaluation steps.

- `README.md`: Documentation and instructions.

- `.gitignore`: List of files to exclude from version control.

## Project Objectives

1. Build the HMM:
   - Download structural Kunitz sequences from PDB (PF00014).
   - Filter redundancy with CD-HIT (≥90% identity).
   - Align sequences and clean the MSA.
   - Train the HMM using `hmmbuild`.

2. Prepare datasets:
   - Merge human and non-human Kunitz sequences.
   - Remove similar sequences using `blastp`.
   - Define positive and negative sets from SwissProt.
   - Generate independent training and test sets.

3. Run classification:
   - Use `hmmsearch` to scan all test sequences.
   - Extract best hits and format `.class` files with ID, label, e-value.

4. Evaluate performance:
   - Use `performance.py` to calculate precision, recall, accuracy, and MCC.
   - Optimize classification threshold.
   - Analyze and interpret false positives and negatives.

5. Annotate SwissProt:
   - Apply the optimized HMM to full SwissProt.
   - Compare predictions with annotations.

## Requirements

- HMMER ≥ 3.3 (`hmmbuild`, `hmmsearch`)
- BLAST+ ≥ 2.13 (`makeblastdb`, `blastp`)
- CD-HIT
- Python ≥ 3.10
- Standard Unix tools: `awk`, `grep`, `cut`, `sort`, `comm`

## Sample Output (Classification Metrics)

Example result using the optimized threshold:

```
Input file: set_1.class
Threshold: 1e-5

True Positives: 182
False Positives: 0
True Negatives: 286286
False Negatives: 2

Accuracy: 0.9999
Precision: 1.0000
Recall: 0.9891
MCC: 0.9803
```

## Author

Martina Castellucci  
MSc Student in Bioinformatics  
University of Bologna  
Email: martina.castellucci@studio.unibo.it


