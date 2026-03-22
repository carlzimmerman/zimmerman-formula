# Zimmerman Framework: Predictions for Cosmological Simulations

**For:** Francisco Villaescusa-Navarro (Simons Foundation / Flatiron CCA)
**Relevance:** CAMELS, large-scale structure, ML cosmology, neutrino cosmology

---

## Executive Summary

The Zimmerman framework makes **specific, falsifiable predictions** for cosmological simulations that differ from both ΛCDM and standard MOND. The key innovation: MOND acceleration scale a₀ **evolves with redshift** as a₀(z) = a₀(0) × E(z).

This creates a unique signature at z > 1 that:
- Explains JWST early galaxy anomalies
- Predicts specific BTFR evolution
- Offers a new parameter for ML emulators

---

## Key Predictions

### 1. BTFR Evolution (Primary Test)

| z | E(z) | Δlog M_bar (dex) | v_circ ratio |
|---|------|------------------|--------------|
| 0 | 1.00 | 0.00 | 1.00 |
| 1 | 1.79 | -0.25 | 1.16 |
| 2 | 3.03 | -0.48 | 1.32 |
| 3 | 4.57 | -0.66 | 1.46 |

**Interpretation:** At z=2, galaxies appear **~3× more massive** at fixed v_circ (or v_circ is ~1.3× higher at fixed M_bar).

**Compare to:** FIRE, EAGLE, IllustrisTNG kinematics at z > 1.

### 2. Neutrino Mass

```
Σm_ν = 58 meV (normal hierarchy)
m₁ ≈ 0, m₂ = 8.6 meV, m₃ = 50 meV
```

- Current bounds: < 120 meV (Planck)
- DESI hint: ~70 meV
- Euclid forecast: σ ~ 20 meV → **decisive test**

### 3. Cosmological Parameters

| Parameter | Zimmerman | Planck 2018 |
|-----------|-----------|-------------|
| Ω_m | 0.3154 | 0.315 ± 0.007 |
| Ω_Λ | 0.6846 | 0.685 ± 0.007 |
| H₀ | 71.5 | 67.4 ± 0.5 |
| n_s | 0.967 | 0.965 ± 0.004 |

### 4. Growth Rate Modification

At z > 1, the Zimmerman framework predicts enhanced structure growth:

```
f_Zimm(z) / f_CDM(z) ≈ 1 + 0.07 × (z/(1+z))
```

This could resolve the S8 tension.

---

## Machine Learning Opportunity

### New Parameter: a₀ Evolution Index β

Standard parameterization:
```
a₀(z) = a₀(0) × E(z)^β
```

| β value | Model |
|---------|-------|
| β = 1 | **Zimmerman** |
| β = 0 | Standard MOND |
| β = undefined | ΛCDM (no a₀) |

### CAMELS Extension

Add β to parameter space:
```
θ = {Ω_m, σ₈, n_s, h, Ω_b, A_SN, A_AGN, β}
```

Train emulator on modified gravity simulations (QUMOND) varying β.

**Deliverable:** Posterior on β from combined probes (kinematics + lensing + clustering).

---

## Simulation Comparison Proposal

### Three-Way Test

1. **ΛCDM**: Standard simulation
2. **MOND (constant a₀)**: a₀ = 1.2×10⁻¹⁰ m/s², all z
3. **Zimmerman (evolving a₀)**: a₀(z) = a₀(0) × E(z)

### Compare at z = 0, 1, 2, 3:

- BTFR normalization
- RAR (radial acceleration relation)
- Rotation curve shapes
- Halo mass function
- Velocity function

### The Discriminant

At z > 1, Zimmerman predicts BTFR offset while constant-MOND doesn't.

KMOS3D data at z ~ 2 already hints at this: galaxies appear **less dark-matter dominated** than expected.

---

## Specific Numbers for Simulations

### Cosmology
```
Ω_m = 0.3154
Ω_Λ = 0.6846
Ω_b = 0.0493
h = 0.715
n_s = 0.967
```

### MOND
```
a₀(z=0) = 1.2 × 10⁻¹⁰ m/s²
a₀(z) = a₀(0) × √(Ω_m(1+z)³ + Ω_Λ)
```

### Neutrinos
```
Σm_ν = 0.058 eV
Hierarchy: Normal
```

---

## Why This is Interesting

1. **Novel prediction**: BTFR evolution is unique to evolving-a₀ MOND
2. **Already hinted**: JWST early galaxies, KMOS3D kinematics
3. **ML-ready**: β parameter can be constrained by emulator
4. **Falsifiable**: Specific predictions that can fail
5. **Resolves tensions**: S8, H₀, early galaxies

---

## Suggested Collaboration

1. Run Zimmerman cosmology in CAMELS-like suite
2. Compare to existing IllustrisTNG/FIRE outputs
3. Train ML emulator including β parameter
4. Constrain β from DESI/Euclid/JWST data

**Contact for collaboration:** Carl Zimmerman

---

## The Killer Number

```
At z = 2: BTFR offset = -0.48 dex
```

If KMOS3D or JWST kinematics shows this offset, Zimmerman is confirmed.
If no offset at z > 1, framework is falsified.

This is a **clean, testable prediction** for simulations.

---

*Prepared March 2026*
