# Z² Framework: Pending Measurements (No Data Yet)

**Generated:** May 2, 2026

This document lists all Z² predictions that are awaiting experimental measurements.

---

## Critical Future Tests (Tier 1)

| # | Experiment | Parameter | Z² Prediction | Expected Data | Falsification Threshold |
|---|------------|-----------|---------------|---------------|-------------------------|
| 1 | **LiteBIRD** | Tensor-to-scalar ratio r | 0.015 ± 0.005 | 2028-2029 | r < 0.005 or r > 0.03 |
| 2 | **MOLLER (JLab)** | sin²θ_W (low Q²) | 0.23077 | 2026-2027 | \|measured - 0.23077\| > 0.001 |
| 3 | **JUNO** | Δm²₂₁ | 7.5×10⁻⁵ eV² | 2025-2026 | Outside ±1σ with small errors |
| 4 | **Euclid** | Ω_Λ | 0.6842105... | 2024-2030 | \|Ω_Λ - 0.6842\| > 0.01 |
| 5 | **DESI Y5** | w₀ | -1.000 | 2028 | \|w₀ + 1\| > 0.05 |
| 6 | **Gaia DR4** | MOND in wide binaries | MOND boost present | 2025-2026 | Pure Newtonian at high S/N |
| 7 | **Roman Space Telescope** | w₀ | -1.000 | 2027+ | \|w₀ + 1\| > 0.05 |
| 8 | **CMB-S4** | Ω_m | 0.3158 | 2028+ | Outside 3σ of 6/19 |

---

## Galaxy Dynamics Future Tests (Tier 2)

| # | Experiment | Parameter | Z² Prediction | Notes |
|---|------------|-----------|---------------|-------|
| 9 | **WALLABY Pilot** | a₀ | 1.20×10⁻¹⁰ m/s² | ~1800 HI sources, rotation curves |
| 10 | **WALLABY Full Survey** | μ(x) form | x/(1+x) | Test MOND interpolating function |
| 11 | **Gaia DR4 + WALLABY** | RAR scatter | < 0.13 dex | Combined astrometry + HI |

---

## What is WALLABY Pilot?

### Overview

**WALLABY** = **W**idefield **A**SKAP **L**-band **L**egacy **A**ll-sky **B**lind surve**Y**

It's a radio astronomy survey using the **Australian Square Kilometre Array Pathfinder (ASKAP)** telescope to map neutral hydrogen (HI) in galaxies via the 21-cm emission line.

### Why It Matters for Z²

WALLABY measures **galaxy rotation curves** from HI observations. This directly tests:
1. **MOND acceleration scale a₀** = cH₀/Z
2. **MOND interpolating function** μ(x) = x/(1+x)
3. **Radial Acceleration Relation (RAR)** scatter
4. **Baryonic Tully-Fisher Relation** slope = 4

### Data Releases

| Phase | Date | Coverage | Sources |
|-------|------|----------|---------|
| Pilot Phase 1 | 2022 | ~180 deg² | ~600 galaxies |
| Pilot Phase 2 | Sept 2024 | ~180 deg² | ~1800 HI sources |
| Full Survey | 2022-ongoing | All-sky | Expected 500,000+ |

### Recent Results (2024-2025)

From [arxiv.org/abs/2411.06993](https://arxiv.org/abs/2411.06993v1):
- **236 kinematic models** from pilot data
- **148 galaxies** with HI size, rotational velocity, angular momentum
- Largest uniformly-observed HI sample to date

From [arxiv.org/abs/2505.04299](https://arxiv.org/abs/2505.04299):
- **17% of detections** are low surface brightness galaxies (LSBGs)
- **3% are optically "dark"** (HI detected but no optical counterpart)
- 75% of LSBGs were **previously uncatalogued**

### How WALLABY Tests MOND/Z²

1. **Rotation curves**: Each galaxy provides v(r) at multiple radii
2. **Acceleration relation**: Plot g_obs vs g_bar
3. **Test μ(x)**: Compare Z² prediction μ = x/(1+x) vs other forms
4. **Mass discrepancy**: Check if "missing mass" follows MOND, not DM halos

### Links

- Official website: [wallaby-survey.org](https://wallaby-survey.org/)
- Data portal: [wallaby-survey.org/data](https://wallaby-survey.org/data/)
- Phase 1 paper: [arxiv.org/abs/2211.07094](https://arxiv.org/abs/2211.07094)
- Pilot DR2: Available via CSIRO (September 2024)

---

## Cryptographically Locked Predictions

The following predictions are **cryptographically committed** with hash:
```
13b7705fdee049d28e2cd050a2371de8b72a6a1863b151ab576062c38f4f6aee
```

| Prediction | Value | Experiment | Timeline |
|------------|-------|------------|----------|
| r | 0.015 ± 0.005 | LiteBIRD | 2028-2029 |
| sin²θ_W | 0.23077 ± 0.00001 | MOLLER | 2026-2027 |
| Δm²₂₁ | 7.5×10⁻⁵ eV² | JUNO | 2025-2026 |
| Ω_Λ | 0.6842 ± 0.001 | Euclid | ongoing |
| w₀ | -1.000 ± 0.02 | DESI Y5 | 2028 |
| MOND signal | present | Gaia DR4 | 2025-2026 |

---

## Immediate Falsification Conditions

If ANY of these occur, Z² is **immediately falsified**:

| Condition | Status | Current Best |
|-----------|--------|--------------|
| WIMP detection | Not met | LZ: σ < 9.2×10⁻⁴⁸ cm² |
| Axion detection | Not met | ADMX: null |
| w ≠ -1 at 5σ | Not met | DESI: w = -0.99 ± 0.15 |
| Ω_Λ ≠ 13/19 at 3σ | Not met | Planck: 0.685 ± 0.007 |
| MOND fails in wide binaries | Contested | Chae vs Banik dispute |
| r outside [0.01, 0.02] | Pending | LiteBIRD 2028 |

---

## Summary Statistics

| Category | Total Targets | With Data | Awaiting Data |
|----------|---------------|-----------|---------------|
| Cosmology | 20 | 17 | 3 |
| Galaxy Dynamics | 20 | 19 | 1 |
| DM Null Results | 20 | 20 | 0 |
| Particle Physics | 20 | 18 | 2 |
| QG/Relativity | 20 | 20 | 0 |
| **TOTAL** | **100** | **94** | **6** |

---

*Pending Measurements Summary*
*Z² Framework v7.0*
*May 2, 2026*
