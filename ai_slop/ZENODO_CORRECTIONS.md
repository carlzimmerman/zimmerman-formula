# Zenodo Publication Corrections

**Date:** April 21, 2026
**Author:** Carl Zimmerman

---

## Critical Correction Notice

### Z² = 32π/3 Geometric Hypothesis: FALSIFIED

On April 21, 2026, rigorous bootstrap statistical analysis definitively falsified the Z² = 32π/3 geometric hypothesis for protein topology.

#### Statistical Evidence

| Metric | Value |
|--------|-------|
| Sample Size (N) | 24,830 H1 topological death radii |
| Empirical Mean | 6.04 Å |
| 95% Confidence Interval | [6.02, 6.05] Å |
| √(Z²) Prediction | 5.79 Å |
| Z-Score | **30.31** |
| Verdict | **OUTSIDE 95% CI** |

A Z-score of 30.31 is astronomically significant. For reference:
- Z = 2 is typically considered significant
- Z = 5 is a "six-sigma" event
- Z = 30 indicates the hypothesis is definitively wrong

---

## Affected Publications

### 1. Protein Folding Paper

**Original Claim:** Z² = 32π/3 governs protein topological death radii, with √(Z²) ≈ 5.79 Å as the universal length scale.

**Correction:** This claim is empirically falsified. The true empirical mean is 6.04 Å, not 5.79 Å. The apparent match in early small-sample testing (N=22, mean=5.85 Å) was a statistical artifact that disappeared when scaled to N=24,830.

**Recommended Action:**
- Retract the protein topology sections that depend on Z² geometric claims
- Preserve the topological data analysis methodology (persistent homology via ripser)
- Update conclusions to reflect empirical findings

### 2. Therapeutic Peptide Papers

**Original Claim:** Peptide geometries optimized to Z² = 9.14 Å or √(Z²) = 5.79 Å would have enhanced binding.

**Correction:**
- The 9.14 Å value was an algebraic error
- The √(Z²) = 5.79 Å value does not match empirical protein topology
- Peptide designs based on these geometric constraints are not validated

**New Approach:**
We have pivoted to first-principles thermodynamics:
- Explicit solvent molecular dynamics (OpenMM + Amber14)
- Umbrella sampling for absolute binding free energy (ΔG)
- No geometric axioms - only Gibbs Free Energy as the arbiter

**Status of Therapeutic Peptides:**
The 11 designed peptides (Ac-FPF-NH2, c[HGPGAGPG], etc.) still have sound biophysical logic (aromatic stacking, steric hindrance), but must be re-validated using thermodynamic methods. Geometric claims should be removed.

---

## What Remains Valid

1. **Topological Data Analysis Methodology**
   - Persistent homology via ripser is a valid technique
   - H1 death radii extraction is mathematically sound
   - Our 24,830-sample dataset is scientifically rigorous

2. **Statistical Framework**
   - Bootstrap confidence intervals
   - Z-score calculations
   - BIC-optimized GMM clustering

3. **Peptide Biophysics (Non-Geometric)**
   - Aromatic stacking interactions
   - Proline kink formation
   - Steric exclusion mechanisms
   - These do not depend on Z² geometry

---

## New Validation Pipeline

All future work uses the thermodynamic pipeline in:
```
extended_research/biotech/medicine/validated_pipeline/
```

Key scripts:
- `val_08_explicit_solvent_md.py` - Structural stability via MD
- `val_09_umbrella_sampling_pmf.py` - Binding free energy (ΔG)
- `res_01_empirical_topology.py` - GMM clustering of true length scales
- `res_07_herg_safety_check.py` - Cardiac safety validation
- `res_09_cro_sow_generator.py` - Wet-lab translation protocols

---

## Recommended Zenodo Updates

### For Each Affected DOI:

1. **Add Correction Notice**
   - Link to this document
   - State: "Z² geometric hypothesis falsified on 2026-04-21"
   - Link to falsification evidence (bootstrap proof results)

2. **Update Abstract**
   - Remove claims about Z² as a fundamental constant
   - Add disclaimer about geometric hypothesis status

3. **Supplementary Material**
   - Add `FINAL_AGGREGATE_BOOTSTRAP_RESULTS.json` showing falsification
   - Add corrected methodology using thermodynamics

---

## Closing Statement

This correction demonstrates scientific integrity. We:
- Did not cherry-pick favorable data
- Scaled the analysis from 22 to 24,830 samples
- Built a statistical guillotine and let it fall on our own hypothesis
- Published the falsification alongside the original work

The Z² framework was a beautiful geometric idea. It was also wrong. We now proceed with pure thermodynamics.

---

**Contact:** [Carl Zimmerman]
**Repository:** https://github.com/carlzimmerman/zimmerman-formula
**License:** AGPL-3.0-or-later
