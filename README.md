
# Kunitz Domain Classifier using Profile HMM

This repository presents a comprehensive and reproducible pipeline to construct and evaluate a Profile Hidden Markov Model (HMM) aimed at recognizing Kunitz-type protease inhibitor domains (Pfam ID: PF00014) within protein sequences. These domains are well-conserved and are critical for inhibiting serine proteases, playing an important role in biological functions like inflammation, coagulation, and immune response regulation.

The project implements a binary classification system to distinguish proteins that contain a Kunitz domain from those that do not, by leveraging structural data for model training and sequence data for classification.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Pipeline Overview](#pipeline-overview)
- [Project Structure and Content Description](#project-structure-and-content-description)
- [Author](#author)
- [Acknowledgements](#acknowledgements)


## Overview

The classification strategy is based on building an HMM using curated, non-redundant sequences extracted from experimentally solved protein structures. These are aligned to preserve structural conservation, then used to generate a probabilistic model via HMMER. The model is tested and optimized using labeled protein sequences from the SwissProt database, with evaluation performed over a range of e-value thresholds.

Classification performance is assessed using standard metrics such as:
- Accuracy
- Precision
- Recall
- Matthews Correlation Coefficient (MCC)

The project ensures that training and test datasets are non-overlapping, with redundancy filtered via sequence identity and alignment coverage using BLAST.

## Requirements

To run this pipeline, the following software and packages must be installed:

-Set up the **conda environment**:
<pre><code>conda create -n hmm_kunitz python 
conda activate hmm_kunitz </code></pre>

-**CD-HIT** 
Purpose: clustering and redundancy reduction of protein sequences.
<pre><code> conda install -c bioconda cd-hit </code></pre>

-**HMMER**
Purpose: building and searching profile Hidden Markov Models (HMMs) for protein domain detection.
<pre><code> conda install -c bioconda hmmer </code></pre>

-**BLAST+**
Purpose: protein sequence similarity search using blastp.
<pre><code> conda install -c bioconda blast-legacy </code></pre>

-**Python packages**
Required for parsing FASTA files and working with sequences.
<pre><code> pip install biopython </code></pre>

**Python Libraries Used**

- **sys** --> Used to read command-line arguments (`sys.argv`).

- **math** --> Provides basic mathematical functions (e.g., `log`, `sqrt`).

- **matplotlib** / **matplotlib.pyplot** --> Used to generate and save plots and figures.

- **pandas** --> Used to manage tabular data and read/write CSV files.

- **numpy** --> Supports numerical arrays and vectorized computations.

- **sklearn.metrics** --> Used for performance evaluation (e.g., ROC curve, AUC).

- **Bio.SeqIO** (Biopython) --> Used to parse FASTA/FASTQ files and biological sequences.
  
- **Seaborn** --> To visualize the confusion matrix for model evaluation.

        
**Web Tools**:

- [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm) – used to perform structural alignment of PDB entries 
  containing the Kunitz domain. The resulting `.ali` file was the basis for building the HMM.
- [Pfam – PF00014](http://pfam.xfam.org/family/PF00014) – reference source for domain profile, seed 
  alignments, and biological information on the Kunitz-type protease inhibitor domain.
- [InterPro](https://www.ebi.ac.uk/interpro/) – used to confirm domain annotations and explore family 
  relationships related to PF00014.
- [UniProt Downloads](https://www.uniprot.org/downloads) – used to obtain the complete Swiss-Prot 
  protein dataset in FASTA format for positive and negative sequence extraction.
- [Skylign / WebLogo](https://skylign.org/) – used to generate sequence logo visualizations from the 
  multiple sequence alignment used in HMM construction.

## Pipeline Overview

### 1. Data Collection & Preprocessing
- Download Swiss-Prot and extract all Kunitz-domain proteins (`all_kunitz.fasta`).
- Split into human (`human_kunitz.fasta`) and non-human (`nothuman_kunitz.fasta`) sequences.
- Download PDB-annotated sequences using a custom query (PF00014, 45–80 aa, resolution ≤ 3.5 Å).

### 2. Structural Dataset Construction
- Extract sequences from the PDB CSV into FASTA.
- Cluster sequences with CD-HIT (90% identity) to reduce redundancy.
- Extract representative sequences (`pdb_kunitz_rp.fasta`).

### 3. Structural Alignment & HMM Building
- Submit representative sequences to PDBeFold and download the structural alignment (`.ali`).
- Reformat the alignment for HMMER compatibility.
- Build the structural HMM using `hmmbuild`.

### 4. Filtering for Model Evaluation
- Run BLAST between PDB-based sequences and all Kunitz entries.
- Remove highly similar sequences (≥95% identity and ≥50% coverage).
- Extract the final non-redundant positive set (`ok_kunitz.fasta`).

### 5. Negative Dataset Generation
- Negative sequences were selected from sp_negs.ids: a file generated by removing all known Kunitz- 
  domain proteins from the Swiss-Prot database.
- Two balanced subsets were then randomly sampled: (`neg_1.ids`) and (`neg_2.ids`).

### 6. Train/Test Set Preparation
- Randomly split positive and negative sets into training and test subsets.
- Extract FASTA files: `pos_1.fasta`, `pos_2.fasta`, `neg_1.fasta`, `neg_2.fasta`.

### 7. Domain Search and Evaluation
- Use `hmmsearch` with `--max` and `-Z 1000` on all sets.
- Generate `.class` files for each dataset.
- Run `performance.py` across multiple E-value thresholds to evaluate and optimize model 
performance (MCC, precision, recall, accuracy).

To see the complete implementation, refer to the Jupyter notebook:  
[Open the pipeline notebook](./kunitz_pipeline.ipynb)


## Project Structure and Content Description

The repository is structured by function and data type to ensure clarity and reproducibility across all pipeline stages:

- `data/`- Raw Input Files
  Includes all initial datasets:
  - Swiss-Prot full set (`uniprot_sprot.fasta`)
  - Kunitz-positive sequences (`all_kunitz.fasta`), split by species
  - PDB report from RCSB query (`rcsb_pdb_custom_report_20250410062557.csv`)
    
- `alignments/`– Structural Alignments
  Contains structural alignment files:
  - PDBeFold output (`pdb_kunitz_rp.ali`)
  - Reformatted version for HMMER (`pdb_kunitz_rp_formatted.ali`)
  - Non-redundant representative sequences (`pdb_kunitz_rp.fasta`)
    
- `scripts/`– Automation Tools
  Python and Bash scripts to automate processing:
  - Sequence extraction (`get_seq.py`), classification scoring (`performance.py`)
  - Plotting utilities for MCC (`MCC_plot.py`) and ROC curves (`ROC_curve.py`)
  - Generates confusion matrices for Fold 1 and Fold 2 (`confusion_matrix.py`)
  - Visualizes the RMSD vs Q-score for Kunitz domain structures (`rmsd.py`)

- `ids/`– Sequence ID Lists
  Intermediate and final ID lists for:
  - Filtering redundancy (`to_remove.ids`, `to_keep.ids`)
  - Dataset composition (`pos_1.ids`, `neg_1.ids`, etc.)
  - PDB clustering (`pdb_kunitz_rp.ids`)
    
- `models/`– HMM Profiles
  - Final Profile Hidden Markov Model built from PDB alignment (`structural_model.hmm`)

- `results/`– Output and Evaluation Results
  Organized into thematic sections:
  
  -(`set_1_finale.class`),(`set_2_finale.class`): Final evaluation sets obtained by concatenating .class 
   files from pos_1, neg_1 and pos_2, neg_2 after hmmsearch
  
  - Positive Dataset Files
      - (`pos_1.fasta`),(`pos_2.fasta`): Curated test sets
      - (`*.out`),(`*.class`): HMMER scan results and classification tables

  - Negative Dataset Files
      - (`neg_1.fasta`),(`neg_2.fasta`): Swiss-Prot negatives
      - (`*.out`),(`*.class`),(`*_real.class`): HMMER outputs and false positives

  - False Negative Analysis
      - (`fn_pos1.txt`),(`fn_pos2.txt`): Misclassified true positives with E-value > 1e-6
        
  - BLAST Filtering and Clean Positive Dataset
      - (`pdb_kunitz_nr_23.blast`): BLASTP hits vs training set
      - (`ok_kunitz.fasta`): Final non-redundant positive set

  - Performance Evaluation Files
      - (`performance_set*_real.txt`): Precision, recall, F1, MCC across E-value cutoff
 
- `figures/`– Visualizations
  - Structural overlays (`superimposition.png`) with session panel and Matchmaker summary     
    (`details_chimera.png`)
  - Domain logos (`logo_skylign.png`),(`Weblogo.png`)
  - Performance plots (`roc_curve_evalue_sets.png`),(`mcc_thresholds_.png`)
  - Confusion matrices (`confusion_matrix_fold1_blues.png`),(`confusion_matrix_fold2_greens.png`)
  - Scatter plot showing structural alignment of candidate domains (`kunitz_structures_scatter.png`)

- `reference/`– External Benchmark
  - Pfam HMM used for comparison (`PF00014.hmm`)
  - (`set_1_pfam.class`) / (`set_2_pfam.class`): Ground truth labels and e-values for evaluation on Set1        and Set2.
  - (`results_set1.txt`) / (`results_set2.txt`): Performance metrics computed at   
    multiple thresholds for each test set.
    
- `final report/`– Final Report
  - Contains the complete scientific report (`Lab1report_Castellucci.pdf`) detailing the methodology,   
    results, and conclusions.
    
- `README.md` and `.gitattributes`
  - Project documentation and Git LFS tracking for large files

- `.gitignore`
  - The .gitignore file excludes temporary files, generated outputs, and notebook checkpoints from 
    version control.
    
- `Diagram.png`
  - The graphical pipeline used in the report was created with [draw.io](https://www.drawio.com/)

 
## Author

Martina Castellucci  
MSc Student in Bioinformatics  
University of Bologna  
Email: martina.castellucci@studio.unibo.it

## Acknowledgements

This project was developed as part of a [Laboratory of Bioinformatics 1 (LAB1)](https://www.unibo.it/en/study/course-units-transferable-skills-moocs/course-unit-catalogue/course-unit/2024/504333) course assignment during my MSc in Bioinformatics at the University of Bologna.
The goal of the project was to integrate structural bioinformatics, sequence analysis, and statistical evaluation of predictive models.
This research was carried out under the guidance of **Professor Emidio Capriotti**, Associate Professor at the University of Bologna.

