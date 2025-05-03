## Pipeline Overview

STEP 1 Input Collection [ UniProt / PDB ]

        ↓
        
STEP 2 Filtering and Redundancy Removal [ BLAST / CD-HIT ]

        ↓
        
STEP 3 Sequence and Structure Alignment [ MSA / PDBeFold ]

        ↓
        
STEP 4 HMM Construction [ HMMER - hmmbuild ]

        ↓
        
STEP 5 Domain Search [ HMMER - hmmsearch ]

        ↓
        
STEP 6 Model Evaluation [ Metrics Calculation ]

        ↓
        
STEP 7 Results and Visualization [ WebLogo plots - Structural overlays - Summary tables and metrics ]
