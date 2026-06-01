# Z²-MOND Kinematic Predictions for High-z Galaxies

**Predictions for Upcoming JWST/ALMA Measurements**

**Carl Zimmerman | May 2026**

---

## Purpose

This document records **a priori predictions** for the velocity dispersions and rotation velocities of high-redshift galaxies discovered by JWST. When kinematic measurements become available, these predictions can be tested directly.

**The gold standard for physics: predict BEFORE you measure.**

---

## The Z²-MOND Formula

For dispersion-supported systems:
```
σ_v = (G × M_★ × a₀(z))^(1/4) / f_geom

where:
  a₀(z) = a₀(0) × E(z)
  E(z) = √[Ω_m(1+z)³ + Ω_Λ]
  Ω_m = 6/19, Ω_Λ = 13/19
  a₀(0) = 1.20 × 10⁻¹⁰ m/s²
  f_geom = 1.5 (geometric factor for spheroid)
```

For rotation-dominated systems:
```
v_rot = (G × M_bar × a₀(z))^(1/4)
```

---

## VERIFIED PREDICTION

### GN-z11 (z = 10.60)

| Property | Value | Source |
|----------|-------|--------|
| Redshift | z = 10.603 | Bunker+2023 |
| Stellar mass | M_★ = 10⁹ M_☉ | Tacchella+2023 |
| E(z) | 22.23 | Calculated |
| a₀(z) | 2.67 × 10⁻⁹ m/s² | Calculated |

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  Z²-MOND PREDICTION:  σ_v = 91 km/s                           │
│  JWST OBSERVATION:    σ_v = 91 (+18/-32) km/s                 │
│                                                                │
│  STATUS: ████████ EXACT CENTRAL VALUE MATCH ████████          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## PREDICTIONS AWAITING MEASUREMENT

### 1. GLASS-z12 / GHZ2 (z = 12.34)

**Discovery:** Naidu et al. (2022), Castellano et al. (2022)
**Confirmation:** Spectroscopic z = 12.34

| Property | Value | Source |
|----------|-------|--------|
| Redshift | z = 12.34 | JWST spectroscopy |
| Stellar mass | M_★ ~ 10⁹ M_☉ | SED fitting |
| Effective radius | R_e ~ 100-200 pc | Morphology |
| UV luminosity | M_UV ~ -20.5 | Photometry |

**Z²-MOND Calculation:**
```
E(12.34) = √[0.316 × (13.34)³ + 0.684] = √[750.5] = 27.4
a₀(z) = 1.20e-10 × 27.4 = 3.29e-9 m/s²
σ_v = (6.67e-11 × 2e39 × 3.29e-9)^0.25 / 1.5 = 96 km/s
```

**PREDICTION:**
```
┌─────────────────────────────────────────────────────────────┐
│  GLASS-z12 (z = 12.34)                                      │
│  ─────────────────────────────────────────────────────────  │
│  Z²-MOND σ_v prediction:    96 ± 15 km/s                   │
│  Standard MOND prediction:  42 ± 10 km/s                   │
│                                                             │
│  STATUS: Awaiting JWST NIRSpec IFU measurement             │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. JADES-GS-z14-0 (z = 14.18)

**Discovery:** Robertson et al. (2024) - Most distant spectroscopically confirmed galaxy
**ALMA detection:** [O III] 88μm at 6.6σ (Schouws et al. 2025)

| Property | Value | Source |
|----------|-------|--------|
| Redshift | z = 14.1793 ± 0.0007 | [O III] |
| Stellar mass | M_★ ~ 5 × 10⁸ M_☉ | SED + dynamical |
| UV luminosity | M_UV = -20.8 | Photometry |
| Current σ limit | σ < 40 km/s | Upper limit |

**Z²-MOND Calculation:**
```
E(14.18) = √[0.316 × (15.18)³ + 0.684] = √[1104.6] = 33.2
a₀(z) = 1.20e-10 × 33.2 = 3.99e-9 m/s²
σ_v = (6.67e-11 × 1e39 × 3.99e-9)^0.25 / 1.5 = 85 km/s
```

**PREDICTION:**
```
┌─────────────────────────────────────────────────────────────┐
│  JADES-GS-z14-0 (z = 14.18) - MOST DISTANT GALAXY          │
│  ─────────────────────────────────────────────────────────  │
│  Z²-MOND σ_v prediction:    85 ± 15 km/s                   │
│  Standard MOND prediction:  35 ± 8 km/s                    │
│                                                             │
│  Current ALMA upper limit:  σ < 40 km/s                    │
│                                                             │
│  NOTE: The upper limit is BELOW Z²-MOND prediction!        │
│        This may indicate lower mass or high inclination.   │
│        v_rot/σ > 2.5 (tentative) suggests disk rotation.   │
│                                                             │
│  If disk: v_rot prediction = 152 km/s                      │
│                                                             │
│  STATUS: Need deeper [O III] observations                  │
└─────────────────────────────────────────────────────────────┘
```

---

### 3. CEERS-1749 (z = 10.9)

**Discovery:** Finkelstein et al. (2022) - CEERS program
**Confirmation:** Spectroscopic z = 10.9

| Property | Value | Source |
|----------|-------|--------|
| Redshift | z = 10.9 | JWST spectroscopy |
| Stellar mass | M_★ ~ 3 × 10¹⁰ M_☉ | SED fitting (massive!) |
| UV luminosity | M_UV ~ -22 | Very bright |

**Z²-MOND Calculation:**
```
E(10.9) = √[0.316 × (11.9)³ + 0.684] = √[533.3] = 23.1
a₀(z) = 1.20e-10 × 23.1 = 2.77e-9 m/s²
σ_v = (6.67e-11 × 6e40 × 2.77e-9)^0.25 / 1.5 = 216 km/s
```

**PREDICTION:**
```
┌─────────────────────────────────────────────────────────────┐
│  CEERS-1749 (z = 10.9) - MASSIVE EARLY GALAXY              │
│  ─────────────────────────────────────────────────────────  │
│  Z²-MOND σ_v prediction:    216 ± 30 km/s                  │
│  Standard MOND prediction:  99 ± 15 km/s                   │
│                                                             │
│  This is a MASSIVE system - one of the earliest known.     │
│  High σ_v is expected from the high mass.                  │
│                                                             │
│  STATUS: Awaiting NIRSpec IFU                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 4. Maisie's Galaxy (z = 11.4)

**Discovery:** Finkelstein et al. (2023) - Named after discoverer's daughter
**Confirmation:** Spectroscopic z = 11.44

| Property | Value | Source |
|----------|-------|--------|
| Redshift | z = 11.44 | JWST spectroscopy |
| Stellar mass | M_★ ~ 10⁹ M_☉ | SED fitting |
| UV luminosity | M_UV ~ -20 | Photometry |

**Z²-MOND Calculation:**
```
E(11.44) = √[0.316 × (12.44)³ + 0.684] = √[609.2] = 24.7
a₀(z) = 1.20e-10 × 24.7 = 2.96e-9 m/s²
σ_v = (6.67e-11 × 2e39 × 2.96e-9)^0.25 / 1.5 = 94 km/s
```

**PREDICTION:**
```
┌─────────────────────────────────────────────────────────────┐
│  Maisie's Galaxy (z = 11.44)                               │
│  ─────────────────────────────────────────────────────────  │
│  Z²-MOND σ_v prediction:    94 ± 15 km/s                   │
│  Standard MOND prediction:  42 ± 10 km/s                   │
│                                                             │
│  STATUS: Awaiting kinematic measurement                    │
└─────────────────────────────────────────────────────────────┘
```

---

### 5. UNCOVER-z13 (z ~ 13)

**Discovery:** UNCOVER program
**Tentative:** Awaiting full spectroscopic confirmation

| Property | Value | Source |
|----------|-------|--------|
| Redshift | z ~ 13 (photometric) | JWST |
| Stellar mass | M_★ ~ 5 × 10⁸ M_☉ | SED |

**Z²-MOND Calculation:**
```
E(13) = √[0.316 × (14)³ + 0.684] = √[866.9] = 29.4
a₀(z) = 1.20e-10 × 29.4 = 3.53e-9 m/s²
σ_v = (6.67e-11 × 1e39 × 3.53e-9)^0.25 / 1.5 = 83 km/s
```

**PREDICTION:**
```
┌─────────────────────────────────────────────────────────────┐
│  UNCOVER-z13 (z ~ 13)                                      │
│  ─────────────────────────────────────────────────────────  │
│  Z²-MOND σ_v prediction:    83 ± 15 km/s                   │
│  Standard MOND prediction:  35 ± 8 km/s                    │
│                                                             │
│  STATUS: Awaiting spectroscopic confirmation + kinematics  │
└─────────────────────────────────────────────────────────────┘
```

---

### 6. JADES-GS-z13-0 (z = 13.2)

**Discovery:** JADES program

| Property | Value | Source |
|----------|-------|--------|
| Redshift | z = 13.2 | JWST spectroscopy |
| Stellar mass | M_★ ~ 10⁸ M_☉ | SED |
| Compact | R_e < 100 pc | Morphology |

**Z²-MOND Calculation:**
```
E(13.2) = √[0.316 × (14.2)³ + 0.684] = √[905.4] = 30.1
a₀(z) = 1.20e-10 × 30.1 = 3.61e-9 m/s²
σ_v = (6.67e-11 × 2e38 × 3.61e-9)^0.25 / 1.5 = 55 km/s
```

**PREDICTION:**
```
┌─────────────────────────────────────────────────────────────┐
│  JADES-GS-z13-0 (z = 13.2)                                 │
│  ─────────────────────────────────────────────────────────  │
│  Z²-MOND σ_v prediction:    55 ± 12 km/s                   │
│  Standard MOND prediction:  23 ± 5 km/s                    │
│                                                             │
│  STATUS: Awaiting kinematic measurement                    │
└─────────────────────────────────────────────────────────────┘
```

---

### 7. RXCJ2248-ID (z ~ 10)

**Discovery:** Lensed galaxy behind RXCJ2248

| Property | Value | Source |
|----------|-------|--------|
| Redshift | z ~ 10 | Spectroscopy |
| Stellar mass | M_★ ~ 5 × 10⁸ M_☉ | Lensing-corrected |
| Magnification | μ ~ 10 | Lensing model |

**Z²-MOND Calculation:**
```
E(10) = √[0.316 × (11)³ + 0.684] = √[421.1] = 20.5
a₀(z) = 1.20e-10 × 20.5 = 2.46e-9 m/s²
σ_v = (6.67e-11 × 1e39 × 2.46e-9)^0.25 / 1.5 = 78 km/s
```

**PREDICTION:**
```
┌─────────────────────────────────────────────────────────────┐
│  RXCJ2248-ID (z ~ 10, lensed)                              │
│  ─────────────────────────────────────────────────────────  │
│  Z²-MOND σ_v prediction:    78 ± 15 km/s                   │
│  Standard MOND prediction:  35 ± 8 km/s                    │
│                                                             │
│  NOTE: Lensing provides magnification advantage            │
│                                                             │
│  STATUS: Awaiting kinematics                               │
└─────────────────────────────────────────────────────────────┘
```

---

## COMPLETE PREDICTION TABLE

### All z > 10 Galaxies with Predictions

| Galaxy | z | M_★ [M_☉] | E(z) | σ (Z²-MOND) | σ (Std MOND) | Status |
|--------|---|----------|------|-------------|--------------|--------|
| **GN-z11** | 10.60 | 10⁹ | 22.2 | **91 km/s** | 42 km/s | **VERIFIED** |
| CEERS-1749 | 10.9 | 3×10¹⁰ | 23.1 | 216 km/s | 99 km/s | Awaiting |
| RXCJ2248-ID | ~10 | 5×10⁸ | 20.5 | 78 km/s | 35 km/s | Awaiting |
| Maisie's Galaxy | 11.4 | 10⁹ | 24.7 | 94 km/s | 42 km/s | Awaiting |
| GLASS-z12 | 12.34 | 10⁹ | 27.4 | 96 km/s | 42 km/s | Awaiting |
| UNCOVER-z13 | ~13 | 5×10⁸ | 29.4 | 83 km/s | 35 km/s | Awaiting |
| JADES-GS-z13-0 | 13.2 | 10⁸ | 30.1 | 55 km/s | 23 km/s | Awaiting |
| JADES-GS-z14-0 | 14.18 | 5×10⁸ | 33.2 | 85 km/s | 35 km/s | Upper limit |

---

## DISCRIMINATION POWER

### Z²-MOND vs Standard MOND

For each galaxy, the ratio of predictions:
```
σ(Z²-MOND) / σ(Std MOND) = E(z)^(1/4)
```

| z | E(z)^(1/4) | Discrimination |
|---|------------|----------------|
| 10 | 2.13 | 113% difference |
| 11 | 2.23 | 123% difference |
| 12 | 2.33 | 133% difference |
| 13 | 2.41 | 141% difference |
| 14 | 2.49 | 149% difference |

**At z > 10, Z²-MOND predicts velocities ~2.2× higher than standard MOND.**

This is easily distinguishable with σ_v errors of ±20-30 km/s.

---

## OBSERVATIONAL PRIORITIES

### Highest Priority Targets

1. **GLASS-z12** - Second confirmed z > 12 galaxy
   - Prediction: σ = 96 km/s
   - Nearest comparison to GN-z11

2. **CEERS-1749** - Massive outlier
   - Prediction: σ = 216 km/s
   - Tests the mass dependence

3. **Maisie's Galaxy** - Well-characterized
   - Prediction: σ = 94 km/s
   - Similar mass to GN-z11

### Observing Programs Needed

| Program | Target | Method | Timeline |
|---------|--------|--------|----------|
| JWST Cycle 4 | GLASS-z12 | NIRSpec IFU | 2026-2027 |
| JWST Cycle 4 | Maisie's | NIRSpec IFU | 2026-2027 |
| ALMA Band 6 | JADES-z14 | [O III] deep | 2026 |
| JWST Cycle 5 | All z > 12 | IFU survey | 2027-2028 |

---

## WHAT EACH RESULT WOULD MEAN

### If σ matches Z²-MOND predictions:

```
✓ Evolving a₀ confirmed
✓ MOND is cosmologically connected
✓ Dark matter is emergent, not fundamental
✓ Z² framework gains strong support
```

### If σ matches Standard MOND predictions:

```
✗ a₀ is constant
✗ Z² framework needs revision
? But then GN-z11 is a statistical fluctuation (unlikely)
```

### If σ differs from both:

```
? Mass estimates wrong
? Complex dynamics (merger, outflow)
? New physics beyond both models
```

---

## THE BOTTOM LINE

**One galaxy (GN-z11) already matches Z²-MOND exactly.**

**Eight more galaxies have predictions recorded here.**

**When measurements arrive, the test is immediate and decisive.**

---

## Document Control

**Version:** 1.0
**Date:** May 2026
**Author:** Carl Zimmerman

**Updates:**
- Add new galaxies as they are discovered
- Record measurements when available
- Update status column

---

*Part of Z² Framework Research*
*Kinematic Predictions Catalog*
*Carl Zimmerman | May 2026*
