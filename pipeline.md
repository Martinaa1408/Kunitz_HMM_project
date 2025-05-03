## Pipeline Overview

```mermaid
graph TD
    A[Input collection:\nretrieve UniProt sequences and PDB structures] --> B[Preprocessing:\nremove redundancy (BLAST), cluster sequences (CD-HIT)]
    B --> C[Alignment stage:\ngenerate MSA with MUSCLE or structural alignment with PDBeFold]
    C --> D[HMM construction:\nbuild profile HMMs using HMMER (hmmbuild)]
    D --> E[Domain search:\nscan benchmark sequences using hmmsearch]
    E --> F[Model evaluation:\ncalculate MCC, F1-score, accuracy, and confusion matrix]
    F --> G[Final outputs:\nvisualize results with WebLogo, structure overlays, and summary plots]
