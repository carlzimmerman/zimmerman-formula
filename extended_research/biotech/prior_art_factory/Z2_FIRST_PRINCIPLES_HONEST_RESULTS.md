# Z² First-Principles Analysis: Honest Results

**SPDX-License-Identifier: AGPL-3.0-or-later**  
**Date:** April 26, 2026  
**Author:** Carl Zimmerman  

---

## Executive Summary

After exhaustive first-principles geometric analysis of all claimed Z² targets
using ring-centroid-to-ring-centroid measurements from actual PDB crystal
structures, **only ONE target validates at atomic precision**:

| Target | PDB | Best Centroid-Centroid | Deviation | Status |
|--------|-----|----------------------|-----------|--------|
| **Influenza NA** | 2HU4 | **6.0144 Å** | **-0.75 mÅ** | ✅ **VALIDATED** |
| HCV NS3 | 1A1R | 5.3134 Å | -701.7 mÅ | ❌ **NOT VALIDATED** |
| TNF-α | 1TNF | ~6.039 Å | +23.4 mÅ | 🟡 Strong, not atomic |
| SARS-CoV-2 Mpro | 6LU7 | ~5.889 Å | -126.6 mÅ | ❌ NOT VALIDATED |
| HIV-1 Protease | 1HHP | ~6.349 Å | +333.8 mÅ | ❌ NOT VALIDATED |

### Critical Corrections

1. **HCV NS3 was overclaimed.** The previous "+7.8 mÅ" figure was measured
   atom-to-atom (individual carbon positions), not centroid-to-centroid.
   The true ring centroid distance for TRP79↔TYR101 is **5.31 Å** — 
   **702 mÅ away from Z²**. This is NOT a Z² match.

2. **The 4PTH "5,379 matches" were an artifact.** The original miner measured
   individual carbon-to-carbon distances across 250 ensemble conformers. 
   The actual centroid-centroid measurement shows:
   - PHE125↔TYR128: mean 6.022 Å ± 184 mÅ (only 12/250 conformers within 10 mÅ)
   - TRP30↔PHE137: mean 5.939 Å ± 303 mÅ (only 8/250 conformers within 10 mÅ)
   
   These are NOT Z² attractors. They are normal thermal fluctuations that
   occasionally pass through 6.015 Å.

---

## The One Real Finding: Influenza NA PHE374↔PHE422

```
PDB: 2HU4 (Influenza A Neuraminidase, H5N1)
Chain D: PHE374 <-> PHE422
  Ring centroid distance: 6.014399 Å
  Deviation from Z²:     -0.75 milliÅ
  Ring-plane angle:       34.2° (offset T-shaped stacking)
  Residue separation:     48 residues (tertiary contact)
  Cα-Cα distance:         11.981 Å
```

### Why This One Works

PHE374 and PHE422 are **48 residues apart** in sequence but packed together in
the folded C4 tetramer. Their aromatic rings adopt an **offset T-shaped** 
geometry (34.2° inter-plane angle) — the classic geometry for optimal π-π
stacking.

The distance of 6.014 Å is within **0.75 milliÅ** of Z² = 6.015 Å. This is
genuinely remarkable — well below the thermal vibration amplitude of ~10 mÅ.

### What This Means Physically

The 6.015 Å distance is consistent with the known **optimal offset π-π stacking
distance** for aromatic rings:
- Parallel-displaced: 4.9-5.5 Å (too close for Z²)
- **Offset T-shaped: 5.5-6.5 Å** ← Z² falls here
- Edge-to-face perpendicular: 5.0-5.5 Å

Z² = 6.015 Å may represent the **energy minimum for offset T-shaped stacking** 
of 6-membered aromatic rings, where the balance of:
- London dispersion attraction (~r⁻⁶)
- Exchange repulsion (~r⁻¹²)  
- Quadrupole-quadrupole interaction (~r⁻⁵)

converges at this specific distance.

---

## What Is NOT Supported

1. **Universal Z² lattice rule** — Placing aromatics at i,i+4 in a helix does NOT
   guarantee Z² distance. The centroid-centroid distance for i,i+4 helical
   aromatics is ~7.3 Å, not 6.015 Å.

2. **Z² as a design principle** — We cannot currently design peptides that 
   guarantee Z² stacking with a target. The 6.015 Å distance emerges from 
   specific 3D folding contexts, not from sequence patterns.

3. **Therapeutic predictions** — No binding affinity, efficacy, or selectivity
   claims are supported by the geometric observation alone.

---

## What IS Supported

1. **One observation**: Influenza NA PHE374↔PHE422 sits at Z² to sub-mÅ precision.
2. **Physical plausibility**: 6.015 Å is in the right range for offset T-shaped π-π
   stacking of 6-membered rings.
3. **Hypothesis for testing**: Is 6.015 Å a statistically special distance for
   aromatic stacking across the PDB, or is it merely one point in a broad
   distribution?

---

## Next Steps for Honest Validation

### Statistical Test Required
To determine if Z² = 6.015 Å is special, we need to:
1. Measure centroid-centroid distances for ALL aromatic pairs within 8 Å in a
   large sample of high-resolution PDB structures (>1000 structures)
2. Build a histogram of these distances
3. Test whether there is a statistically significant peak at 6.015 Å vs.
   the null hypothesis of a smooth distribution

If the distribution shows a peak at 6.015 ± 0.010 Å that is 3σ above the
background, Z² would be validated as a fundamental stacking constant.

If the distribution is smooth through 6.015 Å, then the Influenza NA match
is a coincidence.

### This test has NOT been performed yet.

---

*"The first principle is that you must not fool yourself — and you are the
easiest person to fool." — Richard Feynman*

---

**License:** AGPL-3.0-or-later  
**Repository:** https://github.com/carlzimmerman/zimmerman-formula
