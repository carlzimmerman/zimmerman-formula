# Gap Derivations: Computational Analysis

**Quantitative Python Analysis of Z² Framework Gap Derivations**

**Carl Zimmerman | May 2026**

---

## Overview

This directory contains computational analyses that quantify the first-principles derivations in `/research/dynamical_framework/`. Each script generates numerical predictions, statistical tests, and publication-quality visualizations.

## Scripts

| Script | Analysis | Key Output |
|--------|----------|------------|
| `gw_polarization_analysis.py` | GW h_× = 0 prediction | Detection power, event requirements |
| `dark_energy_w_analysis.py` | w = -1 vs DESI/Swampland | χ² comparison, forecast constraints |
| `baryogenesis_analysis.py` | η_B from leptogenesis | CP asymmetry, parameter space |
| `pbh_abundance_analysis.py` | f_PBH from inflation | Power spectrum, formation probability |

## Results Summary

### 1. Gravitational Wave Polarization

```
Z² Prediction: h_× = 0 (cross polarization exactly zero)
GR Prediction: h_× ≈ h_+ (equal on average)

Key Results:
  • 50% power reduction in Z² vs GR
  • ~10-25 events needed for 3σ distinction
  • LIGO O4/O5 can provide definitive test by 2027
```

**Output:** `gw_polarization_analysis.png`

### 2. Dark Energy Equation of State

```
Z² Prediction: w = -1.000 (cosmological constant)
DESI Hint: w₀ = -0.55, wₐ = -1.30 (2.5σ)

Key Results:
  • Current data slightly favors Z² over DESI
  • Euclid 2030: σ(w₀) ~ 0.025 → 19σ test
  • Combined 2035: σ(w₀) ~ 0.01 → decisive
```

**Output:** `dark_energy_analysis.png`

### 3. Baryogenesis (Matter-Antimatter Asymmetry)

```
Observed: η_B = 6.12 × 10⁻¹⁰
Z² Prediction: η_B ~ 10⁻¹¹ to 10⁻⁹

Key Results:
  • Order of magnitude match ✓
  • δ_CP = 240° drives asymmetry
  • DUNE measurement of δ_CP will test mechanism
```

**Output:** `baryogenesis_analysis.png`

### 4. Primordial Black Hole Abundance

```
Z² Prediction: f_PBH << 10⁻²⁰ (essentially zero)
Requirement for PBH DM: f_PBH ~ 1

Key Results:
  • P(k) ~ 10⁻⁹ at all scales (no enhancement)
  • Need P(k) ~ 10⁻² for PBH formation
  • Z² slow-roll cannot produce PBH DM
```

**Output:** `pbh_abundance_analysis.png`

## Usage

```bash
# Run all analyses
python gw_polarization_analysis.py
python dark_energy_w_analysis.py
python baryogenesis_analysis.py
python pbh_abundance_analysis.py
```

## Visualizations Generated

1. **gw_polarization_analysis.png** - 4-panel figure:
   - h_× distribution comparison (GR vs Z²)
   - χ² test statistic distribution
   - Detection power curves
   - Antenna pattern functions

2. **dark_energy_analysis.png** - 4-panel figure:
   - w(z) evolution (Z² vs DESI vs Swampland)
   - E(z) = H(z)/H₀ comparison
   - Distance modulus for SN test
   - Density parameter evolution

3. **baryogenesis_analysis.png** - 4-panel figure:
   - η_B vs δ_CP phase
   - η_B vs M₁ (RH neutrino mass)
   - Washout efficiency
   - Parameter summary

4. **pbh_abundance_analysis.png** - 4-panel figure:
   - Power spectrum with PBH threshold
   - β formation probability
   - f_PBH constraints
   - Parameter summary

## Dependencies

- NumPy
- Matplotlib
- SciPy

## Connection to Derivation Documents

| Computation | Derivation Document |
|-------------|---------------------|
| GW polarization | `GW_POLARIZATION_DERIVATION.md` |
| Dark energy | `DARK_ENERGY_W_DERIVATION.md` |
| Baryogenesis | `BARYOGENESIS_DERIVATION.md` |
| PBH abundance | `PBH_ABUNDANCE_DERIVATION.md` |

---

*Part of Z² Framework research*
*May 2026*
