# Statement of Work: Therapeutic Peptide Synthesis & Validation

**Document Version:** 1.0 (DRAFT - Awaiting MD Results)
**Date:** April 21, 2026
**Sponsor:** Carl Zimmerman
**Prepared By:** Carl Zimmerman

---

## 1. Executive Summary

This Statement of Work (SOW) requests synthesis and in vitro validation of computationally-designed therapeutic peptides. All candidates have undergone rigorous computational validation including:

- Explicit solvent molecular dynamics (Amber14/TIP3P, 310K)
- RMSD stability analysis over 10+ nanoseconds
- Structural integrity assessment

Peptides listed below have passed the **STABLE** threshold (RMSD drift < 0.2 nm/ns, mean RMSD < 0.3 nm) and are ready for wet-lab validation.

---

## 2. Peptide Specifications

### 2.1 Lead Candidate: [PENDING MD RESULTS]

| Property | Value |
|----------|-------|
| **Compound ID** | ZIM-XXX-XXX |
| **Sequence** | [To be filled after overnight run] |
| **N-Terminal Cap** | Acetyl (Ac-) |
| **C-Terminal Cap** | Amide (-NH₂) |
| **Molecular Weight** | [Calculated] Da |
| **Net Charge (pH 7.4)** | [Calculated] |
| **Purity Required** | ≥ 95% (HPLC) |
| **Quantity** | 10 mg (initial), 100 mg (if active) |

### 2.2 Backup Candidates

| Rank | Compound ID | Sequence | MW (Da) | Stability Verdict |
|------|-------------|----------|---------|-------------------|
| 1 | [PENDING] | - | - | - |
| 2 | [PENDING] | - | - | - |
| 3 | [PENDING] | - | - | - |

---

## 3. Computational Evidence Package

### 3.1 Molecular Dynamics Summary

```
[TO BE FILLED FROM md_stability_results.json]

Simulation Parameters:
  Force Field: Amber14SB + TIP3P
  Temperature: 310 K (NPT ensemble)
  Pressure: 1 atm
  Ionic Strength: 0.15 M NaCl
  Production Length: XX ns

Stability Metrics:
  Mean RMSD: X.XX ± X.XX nm
  RMSD Drift: X.XX nm/ns
  Final Temperature: 310.X ± X.X K
  Final Density: 0.998 ± 0.00X g/cm³
```

### 3.2 Attached Files

- [ ] `{compound_id}_trajectory.dcd` - Full trajectory
- [ ] `{compound_id}_rmsd.csv` - RMSD time series
- [ ] `{compound_id}_state.csv` - Thermodynamic state data
- [ ] `{compound_id}_final_structure.pdb` - Equilibrated structure
- [ ] `{compound_id}_rmsd_plot.png` - RMSD visualization

---

## 4. Synthesis Requirements

### 4.1 Synthesis Method

**Preferred:** Solid-Phase Peptide Synthesis (SPPS) using Fmoc chemistry

### 4.2 Modifications

| Modification | Position | Purpose |
|--------------|----------|---------|
| Acetylation | N-terminus | Block charge, increase stability |
| Amidation | C-terminus | Block charge, increase stability |
| [If cyclic] | Head-to-tail | Cyclization via lactam bridge |

### 4.3 Quality Control

| Test | Specification | Method |
|------|---------------|--------|
| Identity | Matches target MW ± 1 Da | MALDI-TOF MS |
| Purity | ≥ 95% | Analytical HPLC (C18) |
| Sequence | Confirmed | MS/MS fragmentation |
| Endotoxin | < 1 EU/mg | LAL assay |
| Sterility | Sterile | Membrane filtration |

---

## 5. In Vitro Validation Assays

### 5.1 Primary Target Binding

| Assay | Target | Readout | Success Criterion |
|-------|--------|---------|-------------------|
| SPR (Biacore) | [Target protein] | KD (nM) | KD < 1000 nM |
| ITC | [Target protein] | ΔG (kcal/mol) | ΔG < -6 kcal/mol |
| Fluorescence Polarization | [Target protein] | EC50 | EC50 < 10 μM |

### 5.2 Safety Panel

| Assay | Purpose | Threshold |
|-------|---------|-----------|
| hERG Patch Clamp | Cardiac toxicity | IC50 > 30 μM |
| CYP450 Inhibition | Drug interactions | IC50 > 10 μM |
| Plasma Stability | Half-life | t½ > 30 min |
| Cell Viability (MTT) | Cytotoxicity | CC50 > 100 μM |

### 5.3 Disease-Specific Functional Assays

#### For α-Synuclein Disruptors (Parkinson's):
- ThT Fluorescence Aggregation Assay
- Transmission Electron Microscopy (TEM) of fibrils
- Success: ≥ 50% reduction in fibril formation

#### For nAChR Modulators (Non-addictive Analgesic):
- Electrophysiology (α3β4 vs α4β2 selectivity)
- Calcium flux assay
- Success: >10x selectivity for α3β4

#### For PD-1/PD-L1 Disruptors (Immuno-oncology):
- ELISA blocking assay
- T-cell activation assay (IL-2 release)
- Success: IC50 < 1 μM in blocking assay

---

## 6. Deliverables

### From CRO:

1. **Synthesis Report**
   - Synthetic route
   - HPLC chromatograms
   - Mass spectrometry data
   - Certificate of Analysis

2. **Lyophilized Peptide**
   - Quantity: As specified above
   - Storage: -20°C, desiccated
   - Reconstitution: Sterile water or DMSO

3. **Binding Data**
   - Raw sensorgrams (SPR) or thermograms (ITC)
   - Fitted KD values with error
   - Stoichiometry (n)

4. **Safety Data**
   - hERG IC50
   - Plasma stability curve
   - Cytotoxicity dose-response

---

## 7. Timeline

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Synthesis | 2-3 weeks | Peptide delivered |
| QC/Analytics | 1 week | CoA issued |
| Binding Assays | 2 weeks | KD determined |
| Safety Panel | 2 weeks | hERG cleared |
| Functional Assays | 2-3 weeks | Efficacy confirmed |
| **Total** | **8-10 weeks** | Go/No-Go decision |

---

## 8. Budget Estimate

| Item | Unit Cost | Quantity | Total |
|------|-----------|----------|-------|
| Custom Peptide Synthesis (≤10 AA) | $200-500 | 3 | $600-1,500 |
| HPLC Purification | $100 | 3 | $300 |
| MS Characterization | $150 | 3 | $450 |
| SPR Binding (single target) | $500 | 3 | $1,500 |
| hERG Assay | $1,500 | 3 | $4,500 |
| Aggregation Assay | $800 | 1 | $800 |
| **Total Estimate** | | | **$8,000 - $10,000** |

*Note: Prices are estimates. Request formal quotes from CROs.*

---

## 9. Recommended CROs

### Peptide Synthesis:
- **GenScript** (global, fast turnaround)
- **LifeTein** (competitive pricing)
- **Bachem** (GMP-capable for scale-up)
- **AnaSpec** (specialty modifications)

### Binding Assays:
- **Reaction Biology** (SPR, ITC)
- **Eurofins DiscoverX** (cell-based)

### Safety:
- **Charles River** (hERG, ADMET)
- **Cyprotex** (comprehensive safety panel)

---

## 10. Acceptance Criteria

A peptide is considered **VALIDATED** for advancement if:

1. ✓ Synthesis successful (≥95% purity)
2. ✓ Target binding confirmed (KD < 1 μM or ΔG < -8 kcal/mol)
3. ✓ hERG IC50 > 30 μM (no cardiac liability)
4. ✓ Plasma stability t½ > 30 min
5. ✓ Functional assay shows >50% efficacy vs control

Failure at any gate = compound deprioritized.

---

## 11. Contact Information

**Sponsor:**
Carl Zimmerman
[Contact details]

**Computational Support:**
Zimmerman Lab Computational Pipeline
[Repository URL]

---

## Appendix A: Computational Methods

### Force Field
- Amber14SB for protein/peptide
- TIP3P for explicit water
- Joung-Cheatham ion parameters

### Simulation Protocol
1. Energy minimization (steepest descent, 1000 steps)
2. NVT equilibration (1 ns, 310 K)
3. NPT equilibration (2 ns, 310 K, 1 atm)
4. Production MD (10-50 ns)

### Analysis
- RMSD calculated with center-of-mass alignment
- Stability verdict: STABLE (<0.3 nm), MARGINAL (0.3-0.5 nm), UNSTABLE (>0.5 nm)

---

## Appendix B: SMILES Notation

| Compound | SMILES |
|----------|--------|
| [To be filled] | [To be filled] |

---

## Appendix C: Regulatory Considerations

For IND-enabling studies:
- GLP synthesis required
- Full ADMET package
- Rodent PK studies
- 14-day tox in two species

*This SOW covers discovery-phase validation only.*

---

**Document Status:** DRAFT
**Next Action:** Fill in empirical data from overnight MD runs
**Expected Update:** April 22, 2026 (morning)

---

*This document was generated by the Zimmerman Lab Computational Pipeline.*
*No geometric axioms. Pure thermodynamics. Gibbs Free Energy is the only arbiter.*
