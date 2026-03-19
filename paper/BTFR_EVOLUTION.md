# Evolution of the Baryonic Tully-Fisher Relation with Redshift

**Carl Zimmerman**

*March 2026*

---

## Abstract

The Baryonic Tully-Fisher Relation (BTFR), M_bar ∝ v⁴, is one of the tightest correlations in extragalactic astronomy and a cornerstone of MOND. We derive its evolution with redshift from the Zimmerman Formula. Since a₀(z) = a₀(0) × E(z), the BTFR zero-point shifts as Δlog M_bar = -log E(z) at fixed rotation velocity. This predicts a **-0.47 dex shift at z = 2** — a unique, falsifiable signature that distinguishes Zimmerman from both ΛCDM (no shift) and constant-a₀ MOND (no shift). Current KMOS3D data show hints of this evolution. Future JWST and ELT observations will definitively test this prediction.

---

## 1. The Baryonic Tully-Fisher Relation

### 1.1 The Local Relation

The BTFR relates baryonic mass to rotation velocity:

$$M_{bar} = A \times v_{flat}^4$$

where A = 47 M☉/(km/s)⁴ for a₀ = 1.2×10⁻¹⁰ m/s².

Equivalently:
$$M_{bar} = \frac{v_{flat}^4}{G \times a_0}$$

### 1.2 Observed Properties

| Property | Value | Source |
|----------|-------|--------|
| Slope | 4.00 ± 0.05 | McGaugh 2012 |
| Scatter | 0.10 dex | Lelli+2016 |
| Zero-point | 47 M☉/(km/s)⁴ | SPARC |

### 1.3 Why It Matters

The BTFR:
- Has slope exactly 4 (MOND prediction)
- Has remarkably low scatter (<0.1 dex intrinsic)
- Holds for all disk galaxy types (spirals, dwarfs, LSBs)
- Is independent of surface brightness, gas fraction, or morphology

This is the primary evidence for MOND.

---

## 2. BTFR Evolution in Zimmerman

### 2.1 The Zimmerman Prediction

If a₀ evolves with redshift:
$$a_0(z) = a_0(0) \times E(z)$$

Then the BTFR becomes:
$$M_{bar}(z) = \frac{v_{flat}^4}{G \times a_0(z)} = \frac{v_{flat}^4}{G \times a_0(0) \times E(z)}$$

### 2.2 The Zero-Point Shift

At fixed v_flat:
$$\frac{M_{bar}(z)}{M_{bar}(0)} = \frac{1}{E(z)}$$

In logarithmic form:
$$\boxed{\Delta \log M_{bar} = -\log_{10} E(z)}$$

### 2.3 Numerical Predictions

| Redshift | E(z) | Δlog M_bar | Physical Meaning |
|----------|------|------------|------------------|
| z = 0 | 1.00 | 0.00 dex | Baseline |
| z = 0.5 | 1.28 | -0.11 dex | 23% lower M at fixed v |
| z = 1.0 | 1.70 | -0.23 dex | 47% lower M at fixed v |
| z = 1.5 | 2.30 | -0.36 dex | 60% lower M at fixed v |
| z = 2.0 | 2.96 | **-0.47 dex** | 67% lower M at fixed v |
| z = 3.0 | 4.65 | -0.67 dex | 78% lower M at fixed v |

---

## 3. Physical Interpretation

### 3.1 What the Shift Means

At z = 2, a galaxy with v_flat = 200 km/s:
- Local BTFR: M_bar = 3×10¹⁰ M☉
- z = 2 BTFR: M_bar = 1×10¹⁰ M☉

**The same rotation velocity corresponds to lower baryonic mass at high-z.**

### 3.2 Why This Happens

With higher a₀:
- MOND effects are stronger
- Less baryonic mass is needed to produce the same rotation curve
- Or: more baryonic mass produces higher rotation

### 3.3 Equivalent Interpretation

Alternatively, at fixed M_bar:
$$\Delta \log v_{flat} = +\frac{1}{4} \log_{10} E(z)$$

At z = 2:
$$\Delta \log v = +0.12 \text{ dex} \Rightarrow v_{z=2} = 1.32 \times v_{z=0}$$

**Same mass → 32% higher velocity at z = 2.**

---

## 4. Comparison to Other Models

### 4.1 ΛCDM Prediction

In ΛCDM, the BTFR arises from halo-baryon correlations:
- No fundamental reason for slope = 4
- Zero-point set by M★-M_halo relation
- **No evolution predicted** (same halo physics at all z)

### 4.2 Constant-a₀ MOND

In standard MOND with constant a₀:
- Slope = 4 exactly
- Zero-point fixed by a₀
- **No evolution predicted**

### 4.3 Zimmerman (Evolving a₀)

- Slope = 4 exactly (same as MOND)
- Zero-point evolves with E(z)
- **Unique prediction: -0.47 dex at z = 2**

| Model | Slope | Zero-point evolution |
|-------|-------|---------------------|
| ΛCDM | ~3.5-4 | None |
| Constant MOND | 4.00 | None |
| **Zimmerman** | **4.00** | **-0.47 dex at z=2** |

**This is the key distinguishing prediction.**

---

## 5. Current Observational Evidence

### 5.1 KMOS3D Survey

The KMOS3D survey (Übler et al. 2017) measured rotation curves at z = 0.9-2.4:

| Observation | Value |
|-------------|-------|
| Sample | 240 star-forming galaxies |
| Redshift range | 0.9 < z < 2.4 |
| Median z | 2.3 |
| BTFR offset | -0.3 ± 0.15 dex |

**Zimmerman prediction at z = 2.3: -0.51 dex**

The observed offset is consistent within 1.4σ.

### 5.2 SINS Survey

The SINS survey (Cresci et al. 2009) at z ~ 2:
- Found TFR evolution consistent with higher M/L
- Could also be interpreted as BTFR shift

### 5.3 Caveats

Current observations are limited by:
- Selection effects (bright, massive galaxies)
- Resolution (beam smearing)
- Baryonic mass estimates (uncertain M/L)

---

## 6. Future Tests

### 6.1 JWST/NIRSpec

JWST can measure Hα kinematics at z = 2-4:
- Higher spatial resolution than ground-based
- Larger samples at z > 2
- Access to lower-mass galaxies

**Target precision:** 0.1 dex on BTFR offset → 5σ detection of Zimmerman evolution.

### 6.2 ELT/HARMONI

The Extremely Large Telescope with HARMONI:
- 0.01" resolution at near-IR
- Individual rotation curves at z = 2-3
- Direct measurement of v_flat

### 6.3 Roman Space Telescope

Wide-field grism spectroscopy:
- Large samples (10,000+ at z = 1-2)
- Statistical measurement of BTFR evolution
- Control of systematic errors

---

## 7. Systematic Considerations

### 7.1 Stellar Mass Estimates

Baryonic mass = stellar mass + gas mass.

At high-z:
- Gas fractions are higher (~50% at z = 2 vs ~10% locally)
- M★ from SED fitting has ~0.2 dex uncertainty
- Gas mass from molecular line observations

These uncertainties are comparable to the predicted shift but can be controlled statistically.

### 7.2 Selection Effects

High-z samples are biased toward:
- High SFR (emission-line selected)
- High mass (flux-limited)
- Compact morphology (surface brightness selection)

Need matched samples at low-z for fair comparison.

### 7.3 Beam Smearing

Ground-based seeing (~0.5-1") smears rotation curves:
- Underestimates v_flat
- Especially problematic for compact high-z galaxies

Correction possible with forward modeling.

---

## 8. Falsification Criterion

The Zimmerman BTFR evolution is falsified if:

**Future high-z observations find Δlog M_bar ≈ 0 at z > 1.**

Specifically:
- If JWST/ELT find BTFR zero-point within 0.1 dex of local value at z = 2
- With properly controlled systematics
- The formula predicts -0.47 dex, so |Δlog M| < 0.15 would be a >3σ rejection

---

## 9. Summary

| Quantity | z = 0 | z = 2 | Evolution |
|----------|-------|-------|-----------|
| a₀ | 1.2×10⁻¹⁰ | 3.6×10⁻¹⁰ | 3× higher |
| BTFR slope | 4.00 | 4.00 | No change |
| BTFR zero-point | 47 M☉/(km/s)⁴ | 16 M☉/(km/s)⁴ | -0.47 dex |
| M_bar at 200 km/s | 3×10¹⁰ M☉ | 1×10¹⁰ M☉ | 3× lower |

The Zimmerman Formula makes a **unique, quantitative prediction**:

$$\Delta \log M_{bar} = -\log_{10} E(z) = -0.47 \text{ dex at } z = 2$$

This is:
- **Not predicted by ΛCDM** (no fundamental BTFR)
- **Not predicted by constant MOND** (a₀ doesn't evolve)
- **Testable with current/near-future facilities**

If confirmed, this would be strong evidence for the cosmological origin of MOND.

---

## References

1. Zimmerman, C. (2026). Zenodo. DOI: 10.5281/zenodo.19114050
2. McGaugh, S.S. (2012). *AJ*, 143, 40.
3. Lelli, F., McGaugh, S.S., & Schombert, J.M. (2016). *ApJL*, 816, L14.
4. Übler, H. et al. (2017). *ApJ*, 842, 121.
5. Cresci, G. et al. (2009). *ApJ*, 697, 115.
6. Wisnioski, E. et al. (2019). *ApJ*, 886, 124.

---

**Code:** https://github.com/carlzimmerman/zimmerman-formula

**Citation:** Zimmerman, C. (2026). DOI: 10.5281/zenodo.19114050
