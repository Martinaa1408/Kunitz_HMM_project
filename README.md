
# Kunitz Domain Classifier using Profile HMM

This repository presents a comprehensive and reproducible pipeline to construct and evaluate a Profile Hidden Markov Model (HMM) aimed at recognizing Kunitz-type protease inhibitor domains (Pfam ID: PF00014) within protein sequences. These domains are well-conserved and are critical for inhibiting serine proteases, playing an important role in biological functions like inflammation, coagulation, and immune response regulation.

The project implements a binary classification system to distinguish proteins that contain a Kunitz domain from those that do not, leveraging both structural and sequence-based data.

## Table of Contents

- [Overview](#overview)
- [Pipeline Overview](#pipeline-overview)
- [Project Structure and Content Description](#project-structure-and-content-description)
- [Project Objectives](#project-objectives)
- [Requirements](#requirements)
- [Author](#author)


## Overview

The classification strategy is based on building an HMM using curated, non-redundant sequences extracted from experimentally solved protein structures. These are aligned to preserve structural conservation, then used to generate a probabilistic model via HMMER. The model is tested and optimized using labeled protein sequences from the SwissProt database, with evaluation performed over a range of e-value thresholds.

Classification performance is assessed using standard metrics such as:
- Accuracy
- Precision
- Recall
- Matthews Correlation Coefficient (MCC)

The project ensures that training and test datasets are non-overlapping, with redundancy filtered via sequence identity and alignment coverage using BLAST.

## Pipeline Overview

#### STEP 1 Input Collection [ UniProt / PDB ]

        ↓
        
#### STEP 2 Filtering and Redundancy Removal [ BLAST / CD-HIT ]

        ↓
        
#### STEP 3 Sequence and Structure Alignment [ MSA / PDBeFold ]

        ↓
        
#### STEP 4 HMM Construction [ HMMER - hmmbuild ]

        ↓
        
#### STEP 5 Domain Search [ HMMER - hmmsearch ]

        ↓
        
#### STEP 6 Model Evaluation [ Metrics Calculation ]

        ↓
        
#### STEP 7 Results and Visualization [ WebLogo plots - Structural overlays - Summary tables and metrics ]


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
  - The multi-structure alignment obtained from PDBeFold.
    It will be used to generate a structure-based profile HMM. (`pdb_kunitz_rp.ali`)

- `scripts/`: Contains Bash and Python scripts that automate the pipeline:
  - The main pipeline script. It automates: HMM building from alignment, dataset preparation, hmmsearch execution, threshold optimization, performance evaluation, output saving (`create_hmm_build.sh`)
  - Python script that extracts sequences from a FASTA file based on a list of UniProt IDs.
    Used to create positive and negative sets (`get_seq.py`)
  - Extracts representative PDB IDs from the PDB CSV report, avoiding redundancy           
    (`cript_recover_representative_kunitz.sh`)
  - Evaluates classification performance using .class files produced by hmmsearch (`performance.py`)

- `results/`: Stores the output and evaluation results of the pipeline:
  - (`hmm_results.txt`)
    Final output file including:
    Optimal E-value thresholds (based on maximum MCC)
    Performance metrics for each test set
    Lists of false positives and false negatives

- `README.md`: Documentation and instructions.


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

To run this pipeline, the following software and packages must be installed:

-Set up the conda environment:
<pre><code>```conda create -n hmm_kunitz python=3.10 conda activate hmm_kunitz```</code></pre>

-CD-HIT (version 4.8.1)
Purpose: clustering and redundancy reduction of protein sequences.
```bash conda install -c bioconda cd-hit=4.8.1``` 

-HMMER (version 3.3.2)
Purpose: building and searching profile Hidden Markov Models (HMMs) for protein domain detection.
```bash conda install -c bioconda hmmer=3.3.2``` 

-BLAST+ (blastpgp legacy 2.2.26)
Purpose: protein sequence similarity search using blastp.
```bash conda install -c bioconda blast-legacy=2.2.26``` 

-Python packages
Required for parsing FASTA files and working with sequences.
```bash pip install biopython``` 

-Useful Linux commands for PDB_report.csv
These examples help preview and process the CSV file for extracting sequence information:

View the CSV with paging
```bash  less PDB_report.csv```

Remove quotes and preview selected columns
```bash cat PDB_report.csv | tr -d '"' | awk -F "," '{print $1, $2, $3}' | less```

Show only rows with non-empty values
```bash cat PDB_report.csv | tr -d '"' | awk -F "," '{if ($1!="") {print $1, $2, $3}}' | less```

Skip header and format entries as FASTA (chain ID + sequence)
```bash cat PDB_report.csv | tr -d '"' | tail -n +3 | awk -F "," '{if ($1!="") {print ">"$5"_"$3"\\n"$2}}' > pdb_seq.fasta```

Count number of sequences
```bash grep ">" pdb_seq.fasta | wc -l```

Show only PDB ID and chain
```bash cat PDB_report.csv | tr -d '"' | tail -n +3 | awk -F "," '{if ($1!="") {print $5, $3}}' | less```

Web Tools:
- [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm) – structural alignment between PDB entries  
- [InterPro](https://www.ebi.ac.uk/interpro/) – domain and family annotation (e.g., PF00014)  
- [UniProt ID Mapping](https://www.uniprot.org/uploadlists/) – map UniProt to PDB, RefSeq, etc.


## Author

Martina Castellucci  
MSc Student in Bioinformatics  
University of Bologna  
Email: martina.castellucci@studio.unibo.it


