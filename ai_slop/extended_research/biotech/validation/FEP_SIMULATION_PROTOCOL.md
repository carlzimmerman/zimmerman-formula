# Free Energy Perturbation (FEP) Protocol
## Converting Heuristic Scores to Real Binding Energies

**Date**: April 20, 2026
**Purpose**: Replace heuristic Kd predictions with physics-based ΔG_bind

---

## Overview

The peptide candidates have **heuristic scores**, not real binding affinities.
To convert these to actual ΔG_bind values, we need FEP simulations.

---

## Prerequisites

### Software Required
```bash
# GROMACS (free, open source)
conda install -c conda-forge gromacs

# or Amber (academic license)
# or OpenMM (Python-based, free)
pip install openmm

# For topology generation
pip install acpype  # AMBER force field conversion
pip install pdbfixer  # Structure cleaning
```

### Input Files Needed
1. **Receptor structure** (PDB from RCSB or AlphaFold)
2. **Peptide structure** (from ESMFold or docking)
3. **Complex structure** (peptide docked into receptor)

---

## Protocol

### Step 1: Prepare Structures

```bash
# Download receptor (example: GLP-1R)
wget https://files.rcsb.org/download/6X18.pdb

# Clean structure
pdbfixer 6X18.pdb --output=receptor_clean.pdb --add-atoms=all

# Get peptide structure (use ESMFold output)
cp validation/structures/GLP1R_lead.pdb peptide.pdb
```

### Step 2: Generate Topology

```bash
# GROMACS approach
gmx pdb2gmx -f receptor_clean.pdb -o receptor.gro -water tip3p

# For peptide with non-standard residues
acpype -i peptide.pdb -c bcc
```

### Step 3: Build Complex

```bash
# Combine receptor and peptide
gmx editconf -f peptide.gro -o peptide_box.gro -c
gmx insert-molecules -f receptor.gro -ci peptide_box.gro -nmol 1 -o complex.gro
```

### Step 4: Solvate and Add Ions

```bash
gmx solvate -cp complex.gro -cs spc216.gro -o solvated.gro -p topol.top
gmx genion -s ions.tpr -o system.gro -p topol.top -pname NA -nname CL -neutral
```

### Step 5: Energy Minimization

```bash
gmx grompp -f minim.mdp -c system.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em
```

### Step 6: Equilibration

```bash
# NVT (temperature equilibration)
gmx grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt

# NPT (pressure equilibration)
gmx grompp -f npt.mdp -c nvt.gro -p topol.top -o npt.tpr
gmx mdrun -deffnm npt
```

### Step 7: FEP Production Runs

For each lambda window (typically 20-40 windows):

```bash
# Lambda = 0 (peptide fully coupled)
# Lambda = 1 (peptide fully decoupled)

for lambda in $(seq 0 0.05 1); do
  gmx grompp -f fep_${lambda}.mdp -c npt.gro -p topol.top -o fep_${lambda}.tpr
  gmx mdrun -deffnm fep_${lambda}
done
```

### Step 8: Analyze with MBAR/BAR

```bash
# Use alchemlyb for analysis
pip install alchemlyb

python << 'EOF'
from alchemlyb.parsing.gmx import extract_dHdl, extract_u_nk
from alchemlyb.estimators import MBAR, BAR
import pandas as pd

# Load all lambda windows
u_nk = pd.concat([extract_u_nk(f'fep_{l:.2f}.xvg', T=300)
                  for l in np.arange(0, 1.05, 0.05)])

# Calculate ΔG with MBAR
mbar = MBAR()
mbar.fit(u_nk)

print(f"ΔG_bind = {mbar.delta_f_.iloc[0, -1]:.2f} ± {mbar.d_delta_f_.iloc[0, -1]:.2f} kJ/mol")
EOF
```

---

## Expected Outputs

| Quantity | Units | How to Convert |
|----------|-------|----------------|
| ΔG_bind | kJ/mol | From MBAR/BAR analysis |
| Kd | nM | Kd = exp(ΔG/RT) |
| Error | kJ/mol | Bootstrap or MBAR error |

### Conversion Formula
```python
import numpy as np

R = 8.314e-3  # kJ/(mol·K)
T = 300  # K

def dG_to_Kd(dG_kJ_mol):
    """Convert ΔG (kJ/mol) to Kd (M)."""
    return np.exp(dG_kJ_mol / (R * T))

def Kd_to_nM(Kd_M):
    """Convert Kd (M) to Kd (nM)."""
    return Kd_M * 1e9

# Example
dG = -50  # kJ/mol (strong binder)
Kd = Kd_to_nM(dG_to_Kd(dG))
print(f"ΔG = {dG} kJ/mol → Kd = {Kd:.2f} nM")
```

---

## Recommended Workflow

### For Top 10 Candidates

| Candidate | Target | Heuristic Kd* | FEP Status |
|-----------|--------|---------------|------------|
| METAB_GLP1R_002 | GLP-1R | 0.011 nM* | TODO |
| NEURO_GBA1_001 | GBA1 | 0.10 nM* | TODO |
| NONADD_CRF1_001 | CRF1 | 0.25 nM* | TODO |
| PED_CFTR_001 | CFTR | 22.6 nM* | TODO |
| PED_F8_001 | Factor VIII | 0.07 nM* | TODO |

### Estimated Compute Time

| Step | Time per System |
|------|-----------------|
| Structure prep | 1-2 hours |
| Energy minimization | 10 minutes |
| Equilibration | 2-4 hours |
| FEP production (40 windows) | 24-48 GPU hours |
| Analysis | 30 minutes |

**Total**: ~2-3 days per peptide on a single GPU

---

## Alternative: Faster Methods

If FEP is too slow, consider:

1. **MM-PBSA/GBSA** (faster, less accurate)
   - ~4 hours per system
   - Error: ±2-4 kcal/mol

2. **Molecular Docking** (fastest, least accurate)
   - AutoDock Vina: 10 minutes per system
   - Error: ±2-3 kcal/mol

3. **Machine Learning** (fast, varies)
   - Gnina, DeepDock, etc.
   - Requires training data

---

## Validation Criteria

A prediction is considered VALIDATED when:

| Criterion | Threshold |
|-----------|-----------|
| FEP ΔG error | < 1 kcal/mol |
| Kd within 10x of prediction | Yes |
| Experimental confirmation | SPR/BLI assay |

---

## Files

This protocol assumes the following directory structure:

```
fep_simulations/
├── GLP1R/
│   ├── receptor/
│   │   └── 6X18_clean.pdb
│   ├── peptide/
│   │   └── GLP1R_lead.pdb
│   ├── complex/
│   │   └── complex.gro
│   └── fep/
│       ├── lambda_0.00/
│       ├── lambda_0.05/
│       └── ...
├── GBA1/
└── ...
```

---

## References

1. Shirts MR, Chodera JD. J Chem Phys. 2008;129(12):124105. (MBAR)
2. Mobley DL, Gilson MK. Annu Rev Biophys. 2017;46:531-558. (FEP review)
3. Abraham MJ et al. SoftwareX. 2015;1-2:19-25. (GROMACS)

---

*Protocol created: April 20, 2026*
*Status: Ready for implementation*
*Note: All current Kd values are HEURISTIC until FEP is complete*
