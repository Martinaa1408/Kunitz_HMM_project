
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
- Run `performance.py` across multiple E-value thresholds to evaluate and optimize model performance (MCC, precision, recall, accuracy).

To see the complete implementation, refer to the Jupyter notebook:  
[Open the pipeline notebook](./kunitz_pipeline.ipynb)


## Project Structure and Content Description

The repository is organized to reflect a logical workflow and reproducibility of the full pipeline:

- `data/`: Contains all raw input data used to build and evaluate the model, including:
  - FASTA file containing both human and non-human protein sequences annotated with the Kunitz domain   
    (`all_kunitz.fasta`), used to define the initial set of positive examples.
  - A CSV report downloaded from the PDB using an advanced query.
    Filters used:
    PFAM domain = PF00014
    resolution ≤ 3.5 Å
    sequence length between 45 and 80 amino acids
    (`rcsb_pdb_custom_report_20250410062557.csv`) this file is used to select high-quality Kunitz 
    structures for model building. 
  - Complete Swiss-Prot protein dataset in FASTA format, used as a reference to extract both Kunitz 
    domain-containing sequences and non-Kunitz (negative) protein sets for comparative and classification 
    analyses (`uniprot_sprot.fasta`).
  - FASTA file containing all Kunitz domain sequences from Homo sapiens extracted from the comprehensive 
    reference dataset (all_kunitz.fasta) using an awk command that filters entries based on the species 
    annotation (`human_kunitz.fasta`).
  - FASTA file containing non-human Kunitz domain sequences,generated by removing all entries related to 
    Homo sapiens from the reference dataset (`nothuman_kunitz.fasta`).
    
- `alignments/`: Holds alignment files used for structural model construction:
  - The raw multi-structure alignment file downloaded from PDBeFold, containing structurally aligned PDB 
    chains with known Kunitz domains. This file preserves spatial conservation and reflects the 
    structural similarity among the selected representative domains (`pdb_kunitz_rp.ali`).
  - A reformatted version of the PDBeFold alignment, converted into a simplified FASTA-like format 
    required by hmmbuild from HMMER. Each sequence is shown in two lines: a header (starting with >) and 
    its corresponding aligned amino acid sequence in uppercase, without gaps or extra characters. This 
    ensures compatibility with downstream HMM construction (`pdb_kunitz_rp_formatted.ali`).
  - Contains the representative, non-redundant PDB sequences selected after CD-HIT clustering (90% 
    identity threshold). These sequences were chosen as structurally diverse exemplars of the Kunitz 
    domain and were submitted to PDBeFold to obtain the structural alignment used for building the HMM 
    (`pdb_kunitz_rp.fasta`).

- `scripts/`: Contains Bash and Python scripts that automate the pipeline:
  - Python script that extracts sequences from a FASTA file based on a list of UniProt IDs.
    Used to create positive and negative sets (`get_seq.py`).
  - Evaluates classification performance using .class files produced by hmmsearch (`performance.py`).

- `ids/`: Contains intermediate ID lists used for filtering and extraction:
  - Contains UniProt accession IDs of sequences in all_kunitz.fasta that show high similarity (≥95% 
    identity and ≥50% alignment coverage) to the PDB-derived sequences used in HMM construction. These 
    are removed from the positive dataset to avoid data leakage or circular validation (`to_remove.ids`).
  - The final cleaned list of UniProt IDs corresponding to Kunitz domain-containing proteins that are not 
    too similar to any sequence used in the structural model. These IDs were used to extract the true 
    positive set (ok_kunitz.fasta) (`to_keep.ids`).
  - A comprehensive list of all UniProt IDs extracted from the all_kunitz.fasta file, which includes both 
    human and non-human Kunitz proteins. This list serves as the initial universe of positive candidates 
    before BLAST filtering (`all_kunitz.id`).
  - IDs of the representative PDB sequences obtained after CD-HIT clustering of the structurally 
    characterized Kunitz domains. Each ID corresponds to one non-redundant structure used for building 
    the structural alignment and HMM (`pdb_kunitz_rp.ids`).
  - (`pos_1.ids`) List of sequence identifiers used in the pos_1.fasta file, representing proteins 
    expected to contain the Kunitz domain. Useful for tracking, filtering, or validating specific entries 
    in the positive training set.
  - (`pos_2.ids`) Sequence ID list corresponding to the second positive dataset (pos_2.fasta). Allows 
    consistent referencing or extraction of these sequences across other resources or analysis steps.
  - (`neg_1.ids`) Contains the IDs of the sequences included in neg_1.fasta. These are presumed not to 
    carry the Kunitz domain and are used for negative control evaluation.
  - (`neg_2.ids`) Sequence ID list for neg_2.fasta, representing a second negative dataset. The list may 
    be used to extract, rename, or align these entries from external databases.
    
- `models/`: Stores the generated HMM model:
  - The final Profile Hidden Markov Model (HMM) generated using hmmbuild (HMMER). It is constructed from 
    the structurally aligned and reformatted sequences of representative Kunitz domains obtained via 
    PDBeFold. This model captures the conserved structural features of the Kunitz domain and is 
    used for scanning query protein sequences to detect similar domain architectures with hmmsearch 
    (`structural_model.hmm`).

- `results/`: Stores the output and evaluation results of the pipeline:
  - **Positive Dataset Files**--> These files contain sequences known or expected to include the Kunitz 
    domain, and are used to evaluate the model's sensitivity (true positive rate):
     - (`pos_1.fasta`) A FASTA file with a first curated set of protein sequences that are experimentally 
       validated or strongly predicted to contain the Kunitz-type protease inhibitor domain. These 
       sequences represent the positive class used for testing the model.
     - (`pos_1.out`) The output file generated by HMMER after scanning pos_1.fasta using the trained 
       Kunitz HMM profile. It contains domain hits, E-values, alignment scores, start/end positions of 
       matches, and other match-specific data.
     - (`pos_1.class`) A tabular file reporting the classification result for each sequence in 
       pos_1.fasta. Based on the HMMER scores and thresholding (e.g., E-value cut-off), each sequence is 
       marked as detected (1) or not detected (0).
     - (`pos_2.fasta`) A second FASTA dataset containing additional Kunitz-positive sequences, possibly 
       from a different taxonomic group, experimental source, or validation stage.
     - (`pos_2.out`) HMMER search results on the pos_2.fasta sequences. Structured similarly to pos_1.out.
     - (`pos_2.class`) Classification output for pos_2.fasta, reporting detection outcomes and allowing 
       evaluation of model generalizability on a distinct positive set.
  - **Negative Dataset Files**--> These files correspond to protein sequences not expected to contain the 
    Kunitz domain, and are used to evaluate the model’s specificity and false positive rate:
     - (`neg_1.fasta`) A FASTA file containing the first set of negative control sequences. These 
       proteins were selected to be unrelated to the Kunitz family and serve to test the model's 
       robustness against spurious hits.
     - (`neg_1.out`) HMMER search output obtained by scanning neg_1.fasta with the trained HMM. Any 
       unexpected hits in this file may suggest false positives.
     - (`neg_1.class`) Classification result summarizing whether each sequence in neg_1.fasta was 
       (incorrectly) matched by the model. Ideally, all entries should be classified as negative (0).
     - (`neg_1_hits.class`) A filtered list of sequences from neg_1.fasta that produced significant 
       matches in neg_1.out, i.e., likely false positives. This file helps quantify the model's false 
       discovery rate.
     - (`neg_2.fasta`) A second set of background sequences, potentially more taxonomically or 
       functionally diverse than neg_1.fasta, to further challenge the model’s specificity.
     - (`neg_2.out`) HMMER results obtained from scanning neg_2.fasta.
     - (`neg_2.class`) Classification results for the neg_2 dataset, with binary predictions per sequence.
     - (`neg_2_hits.class`) Lists false positives detected in the neg_2 set. An important file for 
       comparative evaluation of error rates across different negative backgrounds.
  - Output file from a BLASTP search comparing the non-redundant PDB Kunitz sequences (used to build the 
    HMM) against the full set of Kunitz domain-containing sequences (all_kunitz.fasta).
    This step identifies sequences in UniProt that are too similar to the structural training set (e.g., 
    ≥95% identity and ≥50% alignment coverage), in order to exclude them from the positive dataset and 
    prevent bias in model evaluation (`pdb_kunitz_nr_23.blast`).
  - A high-quality, manually curated set of protein sequences confirmed to contain the Kunitz domain. 
    This dataset may have been used for training the profile HMM, validating model predictions, or as a 
    reference standard during benchmarking (`ok_kunitz.fasta`).

- `figures/`: All the graphical outputs and visualizations generated during the project:
  - An overlay of the predicted false positive structure aligned against known Kunitz domains. Generated 
    with Chimera or ChimeraX to visualize structural similarity (`superimposition.png`).
  - Visual representation of the conserved motifs in the Kunitz domain, created from the multiple 
    sequence alignment used to build the profile HMM.
  - 

- `reference/`: Includes optional external reference models:
  - Profile HMM downloaded from Pfam, useful for comparative analysis against the custom-built structural 
    model (`PF00014.hmm`).
    
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

