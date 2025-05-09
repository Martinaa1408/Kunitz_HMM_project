
# Kunitz Domain Classifier using Profile HMM

This repository presents a comprehensive and reproducible pipeline to construct and evaluate a Profile Hidden Markov Model (HMM) aimed at recognizing Kunitz-type protease inhibitor domains (Pfam ID: PF00014) within protein sequences. These domains are well-conserved and are critical for inhibiting serine proteases, playing an important role in biological functions like inflammation, coagulation, and immune response regulation.

The project implements a binary classification system to distinguish proteins that contain a Kunitz domain from those that do not, leveraging both structural and sequence-based data.

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

-Set up the conda environment:
<pre><code>conda create -n hmm_kunitz python=3.10 
conda activate hmm_kunitz </code></pre>

-CD-HIT (version 4.8.1)
Purpose: clustering and redundancy reduction of protein sequences.
<pre><code> conda install -c bioconda cd-hit=4.8.1 </code></pre>

-HMMER (version 3.3.2)
Purpose: building and searching profile Hidden Markov Models (HMMs) for protein domain detection.
<pre><code> conda install -c bioconda hmmer=3.3.2 </code></pre>

-BLAST+ (blastpgp legacy 2.2.26)
Purpose: protein sequence similarity search using blastp.
<pre><code> conda install -c bioconda blast-legacy=2.2.26 </code></pre>

-Python packages
Required for parsing FASTA files and working with sequences.
<pre><code> pip install biopython </code></pre>

        
Web Tools:

- [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm) – used to perform structural alignment of PDB entries 
  containing the Kunitz domain. The resulting `.ali` file was the basis for building the HMM.
- [Pfam – PF00014](http://pfam.xfam.org/family/PF00014) – reference source for domain profile, seed 
  alignments, and biological information on the Kunitz-type protease inhibitor domain.
- [InterPro](https://www.ebi.ac.uk/interpro/) – used to confirm domain annotations and explore family 
  relationships related to PF00014.
- [UniProt Downloads](https://www.uniprot.org/downloads) – used to obtain the complete Swiss-Prot protein 
  dataset in FASTA format for positive and negative sequence extraction.
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
- Identify Swiss-Prot sequences without Kunitz domains (`sp_negs.ids`).
- Extract corresponding sequences to build the negative set (`sp_negs.fasta`).

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

The repository is organized to reflect a logical workflow and reproducibility of the full pipeline:

- `data/`: Contains all raw input data used to build and evaluate the model, including:
  - FASTA file containing both human and non-human protein sequences annotated with the 
    Kunitz domain (`all_kunitz.fasta`), used to define the initial set of positive examples.
  - A CSV report downloaded from the PDB using an advanced query.
    Filters used: (PFAM domain = PF00014) AND (resolution ≤ 3.5 Å) AND (sequence length 
    between 45 and 80 amino acids) (`rcsb_pdb_custom_report_20250410062557.csv`).
  - Complete Swiss-Prot protein dataset in FASTA format, used as a reference to extract both 
    Kunitz domain-containing sequences and non-Kunitz (negative) protein sets for 
    comparative and classification analyses (`uniprot_sprot.fasta`).
  - FASTA file containing all Kunitz domain sequences from Homo sapiens extracted from the 
    comprehensive reference dataset (all_kunitz.fasta) using an awk command that filters 
    entries based on the species annotation (`human_kunitz.fasta`).
  - FASTA file containing non-human Kunitz domain sequences,generated by removing all 
    entries related to Homo sapiens from the reference dataset (`nothuman_kunitz.fasta`).
    
- `alignments/`: Holds alignment files used for structural model construction:
  - The raw multi-structure alignment file downloaded from PDBeFold, containing structurally 
    aligned PDB chains with known Kunitz domains (`pdb_kunitz_rp.ali`).
  - A reformatted version of the PDBeFold alignment, converted into a simplified FASTA-like 
    format required by hmmbuild from HMMER. Each sequence is shown in two lines: a header 
    (starting with >) and its corresponding aligned amino acid sequence in uppercase, 
    without gaps or extra characters (`pdb_kunitz_rp_formatted.ali`).
  - Contains the representative, non-redundant PDB sequences selected after CD-HIT 
    clustering (90% identity threshold) (`pdb_kunitz_rp.fasta`).

- `scripts/`: Contains Bash and Python scripts that automate the pipeline:
  - Python script that extracts sequences from a FASTA file based on a list of UniProt IDs.
    Used to create positive and negative sets (`get_seq.py`).
  - Evaluates classification performance using (`.class`) files produced by hmmsearch 
    (`performance.py`).
  - (`MMC_plot.py`) Plots MCC values across different E-value thresholds for Set 1 and Set 
    2 to visualize threshold-dependent classification performance.
  - (`ROC_curve.py`) Generates ROC curves from -log10 (e-value) scores and computes AUC for 
    both sets to assess discriminative performance.

- `ids/`: Contains intermediate ID lists used for filtering and extraction:
  - Contains UniProt accession IDs of sequences in all_kunitz.fasta that show high 
    similarity (≥95% identity and ≥50% alignment coverage) to the PDB-derived sequences used 
    in HMM construction (`to_remove.ids`).
  - The final cleaned list of UniProt IDs corresponding to Kunitz domain-containing proteins 
    that are not too similar to any sequence used in the structural model (`to_keep.ids`).
  - A comprehensive list of all UniProt IDs extracted from the all_kunitz.fasta file, which 
    includes both human and non-human Kunitz proteins (`all_kunitz.id`).
  - IDs of the representative PDB sequences obtained after CD-HIT clustering of the 
    structurally characterized Kunitz domains (`pdb_kunitz_rp.ids`).
  - (`pos_1.ids`) List of sequence identifiers used in the pos_1.fasta file, representing 
    proteins expected to contain the Kunitz domain.
  - (`pos_2.ids`) Sequence ID list corresponding to the second positive dataset 
    (pos_2.fasta).
  - (`neg_1.ids`) Contains the IDs of the sequences included in neg_1.fasta.
  - (`neg_2.ids`) Sequence ID list for neg_2.fasta, representing a second negative dataset.
    
- `models/`: Stores the generated HMM model:
  - The final Profile Hidden Markov Model (HMM) generated using hmmbuild (HMMER). It is 
    constructed from the structurally aligned and reformatted sequences of representative 
    Kunitz domains obtained via PDBeFold (`structural_model.hmm`).

- `results/`: Stores the output and evaluation results of the pipeline:
 - **Positive Dataset Files**-->These files contain sequences expected to include the Kunitz 
   domain and are used to assess sensitivity (true positive rate):
   - (`pos_1.fasta`): Curated set of validated or highly predicted Kunitz-positive sequences 
     (used as test set).
   - (`pos_1.out`): HMMER output after scanning pos_1.fasta with the trained HMM profile. 
     Includes domain hits, E-values, alignment details, and scores.
   - (`pos_1.class`): Classification table showing each sequence’s detection status (1 = 
     detected, 0 = not detected).
   - (`pos_2.fasta`): A second independent set of Kunitz-positive sequences (e.g., from 
     different species or validation source).
   - (`pos_2.out`): HMMER results for pos_2.fasta.
   - (`pos_2.class`): Classification file for pos_2.fasta, useful for testing model 
     generalization.

 - **False Negative Analysis**--> These files help identify misclassified positive sequences 
   with unexpectedly high E-values:
   - (`fn_pos1.txt`): Sequences from pos_1.class labeled as positives but with E-value > 1e- 
     5 (false negatives).
   - (`fn_pos2.txt`): Same analysis applied to pos_2.class. They help in understanding 
     limitations of the model and guiding refinement.
     
 - (`set_1.class`),(`set_2.class`): Final evaluation files combining positives and negatives 
   (used as input for performance scoring).
  
 - **Negative Dataset Files**-->These files contain sequences not expected to include the 
   Kunitz domain and are used to evaluate specificity and false positive rate:
   - (`neg_1.fasta`): First background set of non-Kunitz Swiss-Prot sequences.
   - (`neg_1.out`): HMMER search results against neg_1.fasta.
   - (`neg_1.class`): Classification output (ideally all entries are 0 = negative).
   - (`neg_1_hits.class`): Subset of neg_1.class with false positive matches (E-value below 
     threshold).
   - (`neg_2.fasta`): A second, potentially more diverse, negative dataset.
   - (`neg_2.out`): HMMER results for neg_2.fasta.
   - (`neg_2.class`): Classification summary for neg_2.
   - (`neg_2_hits.class`): False positives detected in neg_2.

 - **BLAST Filtering and Clean Positive Dataset**-->These files are used to avoid redundancy 
   or bias in evaluation by removing highly similar sequences:
   - (`pdb_kunitz_nr_23.blast`): BLASTP result comparing the 23 PDB sequences (used to build 
     the HMM) against all known Kunitz entries (all_kunitz.fasta). Used to detect sequences 
     with ≥95% identity and ≥50% alignment coverage.
   - (`ok_kunitz.fasta`): Cleaned set of true positive sequences, excluding highly similar 
     ones. This file represents the final non-redundant positive dataset used in training 
     and testing.

 - **Performance Evaluation Files**-->These text files summarize the model’s performance at 
   fixed and variable E-value thresholds, measuring precision, recall, F1 score, accuracy, 
   and MCC:
   - (`performance_set1.txt`),(`performance_set2.txt`): Evaluation results on set_1.class 
     and set_2.class at fixed threshold (e.g., 1e-5).
   - (`performance_set1_thresholds.txt`),(`performance_set2_thresholds.txt`): Metrics 
     computed over multiple thresholds (e.g., 1e-3 to 1e-10), allowing selection of the 
     optimal cutoff (based on MCC or F1 score).

- `figures/`: All the graphical outputs and visualizations generated during the project:
  - An overlay of the predicted false positive structure (P84555, P0DQR0, P0DQQ9, P0DQR1) 
    aligned against known Kunitz domains (3TGI). Generated with ChimeraX to visualize 
    structural similarity (`superimposition.png`).
  - (`logo_skylign.png`) logo generated from the HMM profile using Skylign; shows emission 
    probabilities and highlights 4 conserved cysteines. Skylign captures functional 
    constraints better.
  - (`Weblogo.png`) logo from the structural alignment (pdb_kunitz_rp_formatted.ali) via 
    WebLogo; shows residue frequencies across aligned positions. WebLogo is useful for 
    quickly spotting conserved motifs.


- `reference/`: Includes optional external reference models:
  - Profile HMM downloaded from Pfam, useful for comparative analysis against the custom- 
    built structural model (`PF00014.hmm`).
    
- `README.md`: Documentation and instructions.

- The `.gitattributes` file ensures correct tracking of large files via LFS (Large File Storage).

## Author

Martina Castellucci  
MSc Student in Bioinformatics  
University of Bologna  
Email: martina.castellucci@studio.unibo.it

## Acknowledgements

This project was developed as part of a [Laboratory of Bioinformatics 1 (LAB1)](https://www.unibo.it/en/study/course-units-transferable-skills-moocs/course-unit-catalogue/course-unit/2024/504333) course during my MSc in Bioinformatics at the University of Bologna. assignment during my MSc in Bioinformatics at the University of Bologna.
The goal of the project was to integrate structural bioinformatics, sequence analysis, and statistical evaluation of predictive models.
This research was carried out under the guidance of **Professor Emidio Capriotti**, Associate Professor at the University of Bologna.

