## Pipeline Overview

```mermaid
graph TD
    A[Input collection:<br/>retrieve UniProt sequences and PDB structures] --> B[Preprocessing:<br/>remove redundancy (BLAST), cluster sequences (CD-HIT)]
    B --> C[Alignment stage:<br/>generate MSA with MUSCLE or structural alignment with PDBeFold]
    C --> D[HMM construction:<br/>build profile HMMs using HMMER (hmmbuild)]
    D --> E[Domain search:<br/>scan benchmark sequences using hmmsearch]
    E --> F[Model evaluation:<br/>calculate MCC, F1-score, accuracy, and confusion matrix]
    F --> G[Final outputs:<br/>visualize results with WebLogo, structure overlays, and summary plots]
```
