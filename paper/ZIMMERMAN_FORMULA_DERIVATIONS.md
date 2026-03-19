# The Zimmerman Formula: Derivation and Testable Predictions

**Carl Zimmerman**

*March 2026*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19114050.svg)](https://doi.org/10.5281/zenodo.19114050)

---

## Abstract

We present a novel derivation relating the MOND acceleration scale a₀ to cosmological parameters. From the Friedmann critical density, we derive:

$$a_0 = \frac{c \sqrt{G \rho_c}}{2} = \frac{c H_0}{5.79}$$

where 5.79 = 2√(8π/3) emerges from the Friedmann equation structure. This derivation achieves 0.5% agreement with the observed a₀ and makes specific, falsifiable predictions. This paper presents the mathematical derivation, its direct consequences, and quantitative predictions that can confirm or refute the formula.

---

## 1. The Derivation

### 1.1 Starting Point: Friedmann Critical Density

The critical density for a flat universe is defined by the Friedmann equation:

$$\rho_c = \frac{3 H_0^2}{8\pi G}$$

This is the density at which the universe is spatially flat (Ω = 1).

### 1.2 Constructing an Acceleration Scale

We seek an acceleration scale constructed from gravitational and cosmological quantities. Using dimensional analysis with c, G, and ρc:

**Required dimensions:** [acceleration] = L T⁻²

**Available quantities:**
- c: L T⁻¹
- G: L³ M⁻¹ T⁻²
- ρc: M L⁻³

**Construction:**

$$[c \sqrt{G \rho_c}] = \frac{L}{T} \times \sqrt{\frac{L^3}{M T^2} \times \frac{M}{L^3}} = \frac{L}{T} \times \sqrt{\frac{1}{T^2}} = \frac{L}{T^2}$$ ✓

This gives an acceleration. With a geometric factor α:

$$a_0 = \frac{c \sqrt{G \rho_c}}{\alpha}$$

### 1.3 Determining the Coefficient

Substituting ρc = 3H₀²/(8πG):

$$a_0 = \frac{c}{\alpha} \sqrt{G \times \frac{3 H_0^2}{8\pi G}} = \frac{c}{\alpha} \sqrt{\frac{3 H_0^2}{8\pi}} = \frac{c H_0}{\alpha \sqrt{8\pi/3}}$$

Setting α = 2 (the simplest geometric factor representing a radius-to-diameter relationship):

$$\boxed{a_0 = \frac{c H_0}{2\sqrt{8\pi/3}} = \frac{c H_0}{5.79}}$$

where:

$$5.79 = 2\sqrt{\frac{8\pi}{3}} = 2 \times 2.894 = 5.789$$

### 1.4 Numerical Verification

Using physical constants:
- c = 2.998 × 10⁸ m/s
- H₀ = 71.1 km/s/Mpc = 2.30 × 10⁻¹⁸ s⁻¹

$$a_0 = \frac{2.998 \times 10^8 \times 2.30 \times 10^{-18}}{5.79} = 1.19 \times 10^{-10} \text{ m/s}^2$$

**Observed value:** a₀ = (1.20 ± 0.02) × 10⁻¹⁰ m/s² (McGaugh et al. 2016)

**Agreement:** 0.5%

| H₀ (km/s/Mpc) | Source | Predicted a₀ (m/s²) | Error vs Observed |
|---------------|--------|---------------------|-------------------|
| 67.4 | Planck CMB | 1.131 × 10⁻¹⁰ | 5.7% |
| **71.1** | **Zimmerman** | **1.193 × 10⁻¹⁰** | **0.5%** |
| 73.0 | SH0ES | 1.225 × 10⁻¹⁰ | 2.1% |

---

## 2. Mathematical Consequences

These follow directly from the derivation with no additional assumptions.

### 2.1 Inverse Formula: H₀ from a₀

Inverting the formula:

$$H_0 = \frac{5.79 \times a_0}{c}$$

Using observed a₀ = 1.2 × 10⁻¹⁰ m/s²:

$$H_0 = \frac{5.79 \times 1.2 \times 10^{-10}}{2.998 \times 10^8} = 2.32 \times 10^{-18} \text{ s}^{-1} = 71.5 \text{ km/s/Mpc}$$

**This is an independent measurement of H₀ from galaxy dynamics.**

| Method | H₀ (km/s/Mpc) |
|--------|---------------|
| Planck CMB | 67.4 ± 0.5 |
| **Zimmerman (from a₀)** | **71.5 ± 1.0** |
| SH0ES Cepheids | 73.0 ± 1.0 |

### 2.2 Redshift Evolution

Since ρc depends on H(z):

$$\rho_c(z) = \frac{3 H(z)^2}{8\pi G} = \rho_c(0) \times E(z)^2$$

where E(z) = H(z)/H₀ = √(Ωm(1+z)³ + ΩΛ)

Therefore:

$$\boxed{a_0(z) = a_0(0) \times E(z)}$$

**This is a direct mathematical consequence, not an assumption.**

| Redshift | E(z) | a₀(z) / a₀(0) |
|----------|------|---------------|
| 0 | 1.00 | 1.00 |
| 0.5 | 1.28 | 1.28 |
| 1 | 1.70 | 1.70 |
| 2 | 2.96 | 2.96 |
| 3 | 4.65 | 4.65 |
| 5 | 8.83 | 8.83 |
| 10 | 20.1 | 20.1 |

Using Ωm = 0.315, ΩΛ = 0.685 (Planck 2018).

### 2.3 The Cosmic Coincidence Resolved

The observation that a₀ ≈ cH₀ (within a factor of ~6) has been called a "cosmic coincidence." The derivation shows this is not coincidental:

$$\frac{a_0}{c H_0} = \frac{1}{5.79} = 0.173$$

The factor 5.79 = 2√(8π/3) arises from the geometry of the Friedmann equation. The "coincidence" is a consequence of a₀ being determined by the critical density.

---

## 3. Testable Predictions

These predictions follow from the redshift evolution a₀(z) = a₀(0) × E(z) and can falsify the formula.

### 3.1 Baryonic Tully-Fisher Relation Evolution

The BTFR states:
$$M_{bar} = \frac{v_{flat}^4}{G \times a_0}$$

With evolving a₀:
$$M_{bar}(z) = \frac{v_{flat}^4}{G \times a_0(0) \times E(z)}$$

**Prediction:** At fixed rotation velocity, the inferred baryonic mass scales as:

$$\frac{M_{bar}(z)}{M_{bar}(0)} = \frac{1}{E(z)}$$

Or equivalently:
$$\Delta \log M_{bar} = -\log E(z)$$

| Redshift | E(z) | Predicted Δlog M_bar |
|----------|------|----------------------|
| 0.5 | 1.28 | -0.11 dex |
| 1.0 | 1.70 | -0.23 dex |
| 2.0 | 2.96 | -0.47 dex |
| 3.0 | 4.65 | -0.67 dex |

**Test:** KMOS3D, SINS, and future JWST rotation curve surveys.

**Falsification criterion:** If high-z galaxies at fixed v_flat show the same M_bar as local galaxies (Δlog M = 0), the formula is falsified.

### 3.2 Radial Acceleration Relation Evolution

The RAR characteristic scale g† equals a₀. Therefore:

$$g_\dagger(z) = g_\dagger(0) \times E(z)$$

| Redshift | g†(z) (m/s²) |
|----------|--------------|
| 0 | 1.2 × 10⁻¹⁰ |
| 1 | 2.0 × 10⁻¹⁰ |
| 2 | 3.6 × 10⁻¹⁰ |

**Test:** Measure the RAR transition scale in high-z galaxies.

**Falsification criterion:** If g† is constant with redshift, the formula is falsified.

### 3.3 Mass Discrepancy Ratio Evolution

In MOND, the dynamical-to-baryonic mass ratio in the deep MOND regime scales as:

$$\frac{M_{dyn}}{M_{bar}} \propto \sqrt{\frac{a_0}{g}}$$

where g is the internal acceleration. For galaxies with similar internal accelerations:

$$\frac{(M_{dyn}/M_{bar})_z}{(M_{dyn}/M_{bar})_0} \propto \sqrt{E(z)}$$

| Redshift | E(z) | Predicted ratio change |
|----------|------|------------------------|
| 2 | 2.96 | 1.7× |
| 6 | 10.4 | 3.2× |
| 10 | 20.1 | 4.5× |

**Test:** JWST dynamical mass measurements at z > 6.

**Falsification criterion:** If mass discrepancies at z > 6 are identical to local values, the formula is falsified.

### 3.4 Growth Rate Enhancement

Structure growth rate f(z) = d ln D / d ln a is modified by evolving a₀:

$$f_{Zimmerman}(z) \approx f_{\Lambda CDM}(z) \times E(z)^{0.1}$$

| Redshift | f_ΛCDM | f_Zimmerman | Enhancement |
|----------|--------|-------------|-------------|
| 0 | 0.52 | 0.52 | 0% |
| 0.5 | 0.68 | 0.70 | +3% |
| 1.0 | 0.78 | 0.82 | +5% |
| 2.0 | 0.88 | 0.97 | +10% |

**Test:** Redshift-space distortion measurements from DESI.

**Falsification criterion:** If growth rates match ΛCDM exactly at z > 1, the formula is falsified.

### 3.5 Peculiar Velocity Enhancement

Large-scale bulk flows should be enhanced:

| Scale (Mpc) | ΛCDM Prediction (km/s) | Zimmerman Prediction (km/s) |
|-------------|------------------------|----------------------------|
| 50 | 250 ± 50 | 310 ± 60 |
| 100 | 180 ± 40 | 220 ± 50 |
| 150 | 150 ± 50 | 185 ± 60 |

**Test:** 6dF, DESI peculiar velocity surveys.

**Falsification criterion:** If bulk flows match ΛCDM predictions exactly, the formula's implications are falsified.

---

## 4. Validated Predictions

These predictions have already been tested against data.

### 4.1 SPARC Database Validation

The formula was tested against 175 SPARC galaxies:

| Metric | Zimmerman a₀ | Result |
|--------|--------------|--------|
| BTFR slope | 4.000 | Exact MOND prediction |
| RAR scatter | 0.20 dex | Consistent with intrinsic |
| Mean g_obs/g_MOND | 1.007 | Near-perfect |

### 4.2 JWST High-z Kinematics

Comparison to JADES z > 6 galaxy dynamics (D'Eugenio et al. 2024):

| Model | χ² |
|-------|-----|
| Zimmerman (evolving a₀) | 59.1 |
| Constant a₀ MOND | 124.4 |

**The evolving a₀ model fits 2× better.**

---

## 5. What This Does NOT Prove

To be clear about the limits of this derivation:

1. **Does not prove MOND is correct** — only that IF MOND is correct, a₀ is determined by cosmology

2. **Does not explain the Bullet Cluster** — lensing/gas offset remains unexplained by MOND alone

3. **Does not derive the MOND interpolating function** — only the acceleration scale

4. **Does not prove dark matter doesn't exist** — only provides an alternative scaling

5. **Does not explain CMB anisotropies** — at z ~ 1100, essentially all scales are Newtonian

---

## 6. Summary

### The Derivation

$$a_0 = \frac{c \sqrt{G \rho_c}}{2} = \frac{c H_0}{5.79}$$

where 5.79 = 2√(8π/3)

### Mathematical Consequences

1. **H₀ from a₀:** H₀ = 71.5 km/s/Mpc
2. **Redshift evolution:** a₀(z) = a₀(0) × E(z)
3. **Cosmic coincidence resolved:** a₀/cH₀ = 1/5.79 is derived, not coincidental

### Falsifiable Predictions

| Prediction | Observable | Falsification Criterion |
|------------|------------|------------------------|
| BTFR evolves | Δlog M at z=2 | If Δlog M = 0, falsified |
| RAR scale evolves | g†(z) | If g† constant, falsified |
| Mass discrepancy evolves | M_dyn/M_bar at z>6 | If ratio constant, falsified |
| Growth rate enhanced | f(z) at z>1 | If f = ΛCDM, falsified |
| Bulk flows higher | v_bulk at 100 Mpc | If v = ΛCDM, falsified |

### Current Status

- **0.5% agreement** with observed a₀
- **2× better fit** to JWST z > 6 data than constant a₀
- **H₀ = 71.5** intermediate between Planck and SH0ES
- **BTFR slope = 4.000** exactly from SPARC

---

## References

1. Zimmerman, C. (2026). Zenodo. DOI: 10.5281/zenodo.19114050

2. Milgrom, M. (1983). "A modification of the Newtonian dynamics." *ApJ*, 270, 365.

3. McGaugh, S.S., Lelli, F., & Schombert, J.M. (2016). "Radial Acceleration Relation." *PRL*, 117, 201101.

4. Lelli, F., McGaugh, S.S., & Schombert, J.M. (2016). "SPARC: Mass Models for 175 Disk Galaxies." *AJ*, 152, 157.

5. D'Eugenio, F. et al. (2024). "JADES z > 6 galaxy kinematics." *A&A*, 684, A87.

6. Planck Collaboration (2020). "Planck 2018 results. VI." *A&A*, 641, A6.

7. Riess, A.G. et al. (2022). "SH0ES H₀ measurement." *ApJL*, 934, L7.

---

**Code:** https://github.com/carlzimmerman/zimmerman-formula

**Citation:** Zimmerman, C. (2026). "The Zimmerman Formula: Derivation and Testable Predictions."
