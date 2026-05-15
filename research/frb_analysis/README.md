# Fast Radio Burst Analysis for Z² Framework

**Carl Zimmerman | May 2026**

---

## Overview

Computational analysis of Fast Radio Burst (FRB) data from CSIRO's Murchison Radio-astronomy Observatory (ASKAP/CRAFT) and CHIME surveys to search for Z² framework patterns.

## Data Sources

### ASKAP/CRAFT (Murchison Radio-astronomy Observatory)
- **Location:** Inyarrimanha Ilgari Bundara, Western Australia
- **Archive:** [CASDA](https://data.csiro.au/domain/casda)
- **Publications:** Shannon et al. 2018, Macquart et al. 2020, arXiv:2505.17497
- **Sample:** 42 FRBs (23 with host galaxy redshifts)

### CHIME/FRB
- **Catalog:** [chime-frb-open-data.github.io](https://chime-frb-open-data.github.io/catalog/)
- **Database:** [chime-frb.ca](https://www.chime-frb.ca/catalog)
- **Sample:** 40 FRBs (representative sample from Catalog 1)

### Blinkverse Database
- **URL:** [blinkverse.zero2x.org](https://blinkverse.zero2x.org/)
- **Total:** 8,007 bursts from 813 sources (as of May 2024)

## Key Findings

### 1. DM Median ≈ 12 × Z²

```
Observed DM median: 388 pc/cm³
12 × Z² = 12 × 33.51 = 402 pc/cm³
Ratio: 0.964 (3.6% deviation)
```

This is an interesting coincidence but likely astrophysical rather than fundamental - DM depends on line-of-sight electron column density.

### 2. DM-z Relation

The Z² framework predicts slightly lower DM at fixed redshift due to enhanced structure formation from evolving a₀(z):

| Redshift | Standard DM | Z² DM | Difference |
|----------|-------------|-------|------------|
| z = 0.5  | 427 pc/cm³  | 418 pc/cm³ | -2.1% |
| z = 1.0  | 885 pc/cm³  | 845 pc/cm³ | -4.5% |
| z = 2.0  | 1760 pc/cm³ | 1650 pc/cm³ | -6.3% |

**Current data is insufficient to distinguish the models.** Need more FRBs at z > 0.5.

### 3. Repeater Population

- Repeater fraction: 15% (6/40 CHIME sample)
- Repeaters have lower average DM (423 vs 521 pc/cm³)
- Consistent with repeaters being at lower redshift
- KS test p-value: 0.097 (not significant)

## Files

| File | Description |
|------|-------------|
| `csiro_frb_z2_analysis.py` | Main analysis script |
| `frb_z2_visualizations.py` | Publication-quality figures |
| `frb_dm_z_relation.png` | DM-z relation plot |
| `frb_dm_distribution.png` | DM distribution with Z² multiples |
| `frb_z2_predictions.png` | Z² predictions for future observations |
| `frb_integer_analysis.png` | Integer multiple analysis |

## Z² Framework Predictions

### Testable with FRBs:

1. **DM-z deviation at z > 1**
   - Z² predicts 3-5% lower DM
   - Testable with >100 localized FRBs at z > 0.5

2. **Host galaxy dynamics**
   - σ = v_flat / Z for FRB host galaxies
   - Mass discrepancy ∝ √(a₀(z))

3. **CGM profiles**
   - MOND phantom DM ≠ NFW halo
   - Different DM vs impact parameter

## Future Observations

| Facility | Timeline | FRBs Expected |
|----------|----------|---------------|
| DSA-2000 | 2027+ | ~1000 localized/year |
| CHORD | 2026+ | High-z localizations |
| ASKAP Upgrade | Ongoing | Improved precision |

**Definitive Z² test possible by 2028-2030** with sufficient high-z sample.

## Usage

```bash
# Run main analysis
python csiro_frb_z2_analysis.py

# Generate visualizations
python frb_z2_visualizations.py
```

## References

- Macquart et al. 2020, "A census of baryons in the Universe from localized fast radio bursts"
- Shannon et al. 2018, "The dispersion-brightness relation for fast radio bursts"
- CHIME/FRB Collaboration 2021, "The First CHIME/FRB Fast Radio Burst Catalog"
- arXiv:2505.17497 - "High-time-resolution properties of 35 fast radio bursts detected by CRAFT"

---

*Part of the Z² Framework research project*
