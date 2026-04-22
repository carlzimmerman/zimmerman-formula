# ZUGF Systematic Computational Biology Framework

**Author:** Carl Zimmerman
**License:** AGPL-3.0-or-later
**Version:** 1.0.0
**Date:** April 22, 2026

---

## CORE PRINCIPLES

### 1. No Slop
- Every number must be traceable to real data or physics-based calculation
- No heuristic scores presented as binding affinities
- No "better than X" claims without proper comparison

### 2. Negative Controls Required
- Every peptide candidate compared to random baseline
- If random scores similarly, the scoring is broken
- Minimum 100 random peptides per target for statistical power

### 3. Clear Validation Tiers
```
TIER 0: Literature/Database (not our work)
TIER 1: Chemically Valid (RDKit sanitizes)
TIER 2: Structurally Predicted (ESMFold/AlphaFold)
TIER 3: Docked (AutoDock Vina score)
TIER 4: MD Stable (50ns RMSD < 3Å)
TIER 5: Binding Energy (MM-PBSA ΔG)
TIER 6: Experimentally Validated (SPR/ITC data)
```

### 4. Open Source Only
All tools must be freely available and reproducible.

### 5. Honest Reporting
- State what was computed vs assumed
- Include confidence intervals
- Report failures alongside successes

---

## WORKFLOW ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                    DISEASE/TARGET INPUT                         │
│         "Parkinson's Disease - α-synuclein aggregation"         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 1: TARGET RESEARCH                        │
│  • UniProt: Protein sequence, function, disease association     │
│  • PDB: Available structures, resolution, ligands               │
│  • ChEMBL: Known binders, assay data, IC50/Kd values            │
│  • PubMed: Recent publications, clinical trials                  │
│  • DrugBank: Approved drugs, mechanisms                          │
│  OUTPUT: target_profile.json (all data with sources)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 2: STRUCTURE PREPARATION                  │
│  • Download PDB or predict with ESMFold                         │
│  • Fix missing atoms (PDBFixer)                                 │
│  • Add hydrogens, assign protonation states (pH 7.4)            │
│  • Energy minimize (OpenMM, 1000 steps steepest descent)        │
│  OUTPUT: target_prepared.pdb (clean structure)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 3: BINDING SITE ANALYSIS                  │
│  • fpocket: Identify druggable pockets                          │
│  • Literature: Known binding sites from PDB ligands             │
│  • Allosteric: Check for secondary sites                        │
│  OUTPUT: binding_sites.json (ranked by druggability)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 4: PEPTIDE DESIGN                         │
│  • Constraint-based generation (length, charge, hydrophobicity) │
│  • Z² geometric optimization (optional)                         │
│  • RDKit validation (chemistry check)                           │
│  • NEGATIVE CONTROLS: 100 random peptides same length           │
│  OUTPUT: candidates.json (designed + controls, all TIER 1)      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 5: STRUCTURE PREDICTION                   │
│  • ESMFold: Fast structure prediction for all peptides          │
│  • pLDDT filter: Only keep >70 confidence                       │
│  • Ramachandran check: >90% in allowed regions                  │
│  OUTPUT: peptide_structures/*.pdb (TIER 2 validated)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 6: MOLECULAR DOCKING                      │
│  • AutoDock Vina: Rigid docking to binding site                 │
│  • HADDOCK: Flexible protein-peptide docking (if needed)        │
│  • Score distribution: Compare to negative controls             │
│  • REJECT if designed peptides don't outperform random          │
│  OUTPUT: docking_results.json (TIER 3, with control comparison) │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 7: MOLECULAR DYNAMICS                     │
│  • OpenMM: 50ns NPT simulation at 310K                          │
│  • AMBER14/TIP3P force field                                    │
│  • RMSD analysis: Stable if <3Å from starting structure         │
│  • Hydrogen bond persistence: Key interactions maintained?       │
│  OUTPUT: md_results.json (TIER 4, stability metrics)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 8: BINDING FREE ENERGY                    │
│  • MM-PBSA: ΔG calculation from MD trajectory                   │
│  • Component analysis: ΔG_elec, ΔG_vdw, ΔG_solv                 │
│  • Error estimation: Block averaging, bootstrap CI              │
│  OUTPUT: binding_energy.json (TIER 5, ΔG with uncertainty)      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 9: ADMET PREDICTION                       │
│  • Solubility: ESOL model                                       │
│  • Permeability: Lipinski/Veber rules                           │
│  • Toxicity: AMES, hERG liability                               │
│  • Metabolism: CYP450 interactions                              │
│  OUTPUT: admet_profile.json (predicted properties)              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MODULE 10: SYNTHESIS SOW                         │
│  • Only peptides passing TIER 1-5 get SOW                       │
│  • RDKit: Final chemistry validation                            │
│  • Mass spec: Theoretical isotope pattern                       │
│  • CRO-ready document with all QC specs                         │
│  OUTPUT: SOW_*.txt (ready for synthesis order)                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## OPEN SOURCE TOOL REQUIREMENTS

### Required (Must Install)
| Tool | Purpose | Install |
|------|---------|---------|
| RDKit | Chemistry | `pip install rdkit` |
| BioPython | Sequences | `pip install biopython` |
| OpenMM | MD simulations | `pip install openmm` |
| PDBFixer | Structure prep | `pip install pdbfixer` |
| MDTraj | Trajectory analysis | `pip install mdtraj` |
| NumPy/SciPy | Numerics | `pip install numpy scipy` |

### Optional (Enhances Pipeline)
| Tool | Purpose | Install |
|------|---------|---------|
| AutoDock Vina | Docking | `conda install -c bioconda autodock-vina` |
| fpocket | Pocket detection | `conda install -c bioconda fpocket` |
| ESMFold | Structure prediction | API or local install |
| PyMOL | Visualization | `conda install -c schrodinger pymol` |

### Web APIs (No Install)
| Service | Purpose | URL |
|---------|---------|-----|
| RCSB PDB | Structures | rcsb.org |
| UniProt | Sequences | uniprot.org |
| ChEMBL | Bioactivity | ebi.ac.uk/chembl |
| ESMFold | Structure pred | esmatlas.com |
| SwissADME | ADMET | swissadme.ch |

---

## VALIDATION GATES

Each module has explicit pass/fail criteria:

### Module 1: Target Research
- ✅ PASS: UniProt entry found, structure available (PDB or predictable)
- ❌ FAIL: No protein sequence, no structural data possible

### Module 2: Structure Preparation
- ✅ PASS: Clean PDB, no steric clashes, energy minimized
- ❌ FAIL: Unresolvable missing regions, structure collapse on minimization

### Module 3: Binding Site
- ✅ PASS: Druggable pocket identified (fpocket score >0.5)
- ❌ FAIL: No pockets, or all pockets shallow/hydrophilic

### Module 4: Peptide Design
- ✅ PASS: RDKit validates all peptides, controls generated
- ❌ FAIL: Chemistry errors, invalid sequences

### Module 5: Structure Prediction
- ✅ PASS: pLDDT >70, Ramachandran >90% allowed
- ❌ FAIL: Low confidence, bad geometry

### Module 6: Docking
- ✅ PASS: Designed peptides score >1σ better than random controls
- ❌ FAIL: No statistical separation from random (scoring is broken)

### Module 7: MD Stability
- ✅ PASS: RMSD <3Å over 50ns, no unfolding
- ❌ FAIL: Peptide unfolds, dissociates, or aggregates

### Module 8: Binding Energy
- ✅ PASS: ΔG < -5 kcal/mol (weak binder minimum)
- ⚠️ UNCERTAIN: -5 to -10 kcal/mol (moderate)
- ✅ STRONG: ΔG < -10 kcal/mol (strong binder)

### Module 9: ADMET
- ✅ PASS: Soluble, permeable, no hERG flag, no AMES+
- ⚠️ FLAG: One or more concerns noted for optimization

### Module 10: Synthesis
- ✅ PASS: Only TIER 4+ peptides get SOW
- OUTPUT: CRO-ready document

---

## HONEST OUTPUT FORMAT

Every result file must include:

```json
{
  "peptide_id": "ZIM-XXX-001",
  "sequence": "WFFY",
  "validation_tier": 4,
  "validation_details": {
    "tier_1_chemistry": {"passed": true, "rdkit_valid": true},
    "tier_2_structure": {"passed": true, "plddt": 85.2},
    "tier_3_docking": {"passed": true, "vina_score": -7.2, "random_mean": -4.1, "zscore": 2.8},
    "tier_4_md": {"passed": true, "rmsd_mean": 1.8, "rmsd_std": 0.4},
    "tier_5_binding": {"passed": false, "reason": "MM-PBSA not run"}
  },
  "comparison_to_controls": {
    "n_random_controls": 100,
    "random_mean_score": -4.1,
    "random_std": 1.1,
    "peptide_zscore": 2.8,
    "p_value": 0.0026
  },
  "honest_claims": [
    "Chemically synthesizable (RDKit validated)",
    "Predicted to fold stably (ESMFold pLDDT 85)",
    "Docks better than random (p=0.003)",
    "MD stable over 50ns (RMSD 1.8±0.4 Å)"
  ],
  "cannot_claim": [
    "Binding affinity (no MM-PBSA)",
    "Therapeutic efficacy (no experimental data)",
    "Safety (no toxicity testing)"
  ],
  "data_sources": {
    "target_structure": "PDB:1XQ8",
    "target_sequence": "UniProt:P37840",
    "known_binders": "ChEMBL:CHEMBL1234"
  }
}
```

---

## DIRECTORY STRUCTURE

```
validated_pipeline/
├── framework/
│   ├── __init__.py
│   ├── m01_target_research.py
│   ├── m02_structure_prep.py
│   ├── m03_binding_site.py
│   ├── m04_peptide_design.py
│   ├── m05_structure_prediction.py
│   ├── m06_docking.py
│   ├── m07_molecular_dynamics.py
│   ├── m08_binding_energy.py
│   ├── m09_admet.py
│   ├── m10_synthesis_sow.py
│   └── orchestrator.py
├── projects/
│   ├── parkinsons_asyn/
│   ├── alzheimers_tau/
│   ├── hiv_envelope/
│   └── preterm_labor/
└── results/
    └── [project_name]/
        ├── target_profile.json
        ├── binding_sites.json
        ├── candidates.json
        ├── docking_results.json
        ├── md_results.json
        └── final_report.json
```

---

## USAGE

```bash
# Start new disease investigation
python orchestrator.py --disease "Parkinson's Disease" \
                       --target "alpha-synuclein" \
                       --uniprot P37840 \
                       --pdb 1XQ8

# Resume from specific module
python orchestrator.py --project parkinsons_asyn \
                       --resume-from docking

# Generate synthesis SOW for validated peptides
python orchestrator.py --project parkinsons_asyn \
                       --generate-sow --min-tier 4
```

---

## WHAT THIS FRAMEWORK DOES NOT DO

1. **Claim therapeutic efficacy** - only computational predictions
2. **Replace experimental validation** - SPR/ITC still required
3. **Generate fake binding energies** - only physics-based calculations
4. **Skip negative controls** - every result compared to random
5. **Hide failures** - unsuccessful candidates documented

---

## NEXT STEPS TO IMPLEMENT

1. Create m01_target_research.py (UniProt/PDB/ChEMBL fetching)
2. Create m04_peptide_design.py with negative control generation
3. Create m06_docking.py with AutoDock Vina integration
4. Create orchestrator.py to chain modules
5. Test on ZIM-SYN-004 (simplest existing candidate)

---

**This framework exists to do computational biology honestly.**

*No slop. No heuristics pretending to be physics. No claims without evidence.*
