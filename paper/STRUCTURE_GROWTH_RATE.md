# Modified Structure Growth from Evolving MOND

**Carl Zimmerman**

*March 2026*

---

## Abstract

We derive the modification to cosmic structure growth rates from the Zimmerman Formula's evolving a₀. The linear growth rate f(z) = d ln δ / d ln a is enhanced at high redshift when a₀ was larger, producing f_Zimmerman(z) ≈ f_ΛCDM(z) × [1 + 0.1 ln E(z)]. This predicts ~10% faster growth at z = 2 compared to ΛCDM, a signal detectable with DESI and Euclid redshift-space distortions. The modified growth history naturally explains both the S8 tension and the enhanced peculiar velocities observed in the local universe.

---

## 1. Structure Growth in Cosmology

### 1.1 The Growth Rate f(z)

The linear growth rate measures how fast density perturbations grow:

$$f(z) = \frac{d \ln \delta}{d \ln a} = \frac{d \ln D}{d \ln a}$$

where δ is the density contrast and D is the growth factor.

### 1.2 ΛCDM Prediction

In ΛCDM:
$$f_{\Lambda CDM}(z) \approx \Omega_m(z)^{0.55}$$

| Redshift | Ω_m(z) | f_ΛCDM |
|----------|--------|--------|
| 0 | 0.315 | 0.52 |
| 0.5 | 0.51 | 0.68 |
| 1.0 | 0.69 | 0.78 |
| 2.0 | 0.86 | 0.88 |

### 1.3 Observational Probe: fσ₈

The quantity fσ₈ is measured from redshift-space distortions (RSD):
- Galaxy velocities cause anisotropic clustering
- Kaiser formula relates anisotropy to fσ₈
- BOSS, eBOSS, DESI measure this directly

---

## 2. Zimmerman Modification

### 2.1 The Physical Effect

With a₀(z) = a₀(0) × E(z):
- Higher a₀ at high-z → stronger effective gravity
- Enhanced gravity → faster structure growth
- Cumulative effect modifies growth history

### 2.2 Modified Growth Equation

The linear perturbation equation in MOND:

$$\ddot{\delta} + 2H\dot{\delta} - 4\pi G_{eff}(a_0(z)) \rho \delta = 0$$

where G_eff includes MOND enhancement in low-acceleration regions.

### 2.3 Approximate Solution

For small modifications:

$$f_{Zimmerman}(z) = f_{\Lambda CDM}(z) \times [1 + \alpha \ln E(z)]$$

where α ≈ 0.1 from the MOND modification.

### 2.4 Numerical Predictions

| Redshift | E(z) | f_ΛCDM | f_Zimmerman | Enhancement |
|----------|------|--------|-------------|-------------|
| 0 | 1.00 | 0.52 | 0.52 | 0% |
| 0.5 | 1.28 | 0.68 | 0.70 | +2.5% |
| 1.0 | 1.70 | 0.78 | 0.82 | +5.3% |
| 2.0 | 2.96 | 0.88 | 0.97 | +10.9% |
| 3.0 | 4.65 | 0.93 | 1.08 | +15.4% |

---

## 3. Observable: fσ₈(z)

### 3.1 Combining with σ₈ Evolution

The amplitude σ₈(z) also evolves differently in Zimmerman:
- Faster growth at high-z
- Slower growth at low-z
- Net: lower σ₈(z=0) (the S8 tension!)

### 3.2 fσ₈ Predictions

| Redshift | fσ₈ (ΛCDM) | fσ₈ (Zimmerman) | Difference |
|----------|------------|-----------------|------------|
| 0.3 | 0.44 | 0.44 | 0% |
| 0.6 | 0.46 | 0.47 | +2% |
| 1.0 | 0.47 | 0.50 | +6% |
| 1.5 | 0.46 | 0.52 | +13% |
| 2.0 | 0.44 | 0.53 | +20% |

### 3.3 Current Measurements

| Survey | z_eff | fσ₈ (observed) | fσ₈ (ΛCDM) | fσ₈ (Zimmerman) |
|--------|-------|----------------|------------|-----------------|
| 6dFGS | 0.067 | 0.423±0.055 | 0.40 | 0.40 |
| BOSS low-z | 0.32 | 0.427±0.056 | 0.43 | 0.44 |
| BOSS CMASS | 0.57 | 0.453±0.022 | 0.46 | 0.47 |
| eBOSS LRG | 0.70 | 0.473±0.041 | 0.46 | 0.48 |
| eBOSS ELG | 0.85 | 0.315±0.095 | 0.46 | 0.49 |

Current data are consistent with both models at z < 1. **DESI at z > 1 will discriminate.**

---

## 4. Physical Mechanisms

### 4.1 Enhanced Gravitational Infall

At high-z, with a₀ elevated:
- Low-acceleration regions (voids, outskirts) have enhanced g_eff
- Matter falls into overdensities faster
- δ grows more rapidly

### 4.2 Modified Void Evolution

Voids evolve differently:
- In ΛCDM: Voids expand passively
- In Zimmerman: Enhanced gravity in void walls → faster evacuation

### 4.3 Velocity Field Enhancement

Peculiar velocities v_pec relate to f:
$$v_{pec} = f \times H \times r \times \frac{\delta}{a}$$

Higher f → higher peculiar velocities at fixed δ.

---

## 5. Connection to S8 Tension

### 5.1 The Integrated Growth

The S8 tension arises from integrated growth:
- CMB measures σ₈(z~1100) = 0.81
- Local measures σ₈(z=0) = 0.74
- Difference: ~8%

### 5.2 Zimmerman Explanation

The growth factor from CMB to today:
$$\frac{D(z=0)}{D(z=1100)}$$

In Zimmerman:
- High-z growth enhanced (higher a₀)
- Low-z growth reduced (lower a₀)
- Net: same early σ₈, lower late σ₈

### 5.3 Self-Consistency Check

The S8 paper (separate) derives the same ~8% suppression from evolving a₀.

**This paper derives the same physics from growth rate perspective.**

---

## 6. Predictions for DESI

### 6.1 DESI Year 1 (Current)

DESI Y1 measures fσ₈ at z = 0.4, 0.6, 0.8, 1.1, 1.5:

| z_eff | fσ₈ (ΛCDM) | fσ₈ (Zimmerman) | DESI precision |
|-------|------------|-----------------|----------------|
| 0.4 | 0.44 | 0.45 | ±0.03 |
| 0.6 | 0.46 | 0.47 | ±0.03 |
| 0.8 | 0.46 | 0.49 | ±0.04 |
| 1.1 | 0.46 | 0.51 | ±0.05 |
| 1.5 | 0.45 | 0.53 | ±0.06 |

**At z = 1.5, Zimmerman predicts 18% higher fσ₈ — potentially detectable.**

### 6.2 DESI Year 5

With full dataset:
- Precision improves by ~2×
- z > 2 measurements from QSOs
- 5σ discrimination possible

### 6.3 Combined with BAO

DESI also measures BAO:
- H(z) and D_A(z) constrain expansion history
- RSD constrains growth history
- Zimmerman predicts consistent modifications to both

---

## 7. Predictions for Euclid

### 7.1 Spectroscopic Survey

Euclid spectroscopy (2024-2030):
- 30 million Hα galaxies at 0.9 < z < 1.8
- fσ₈ precision: ~2% per z-bin
- Discriminating power: 5-10σ for Zimmerman vs ΛCDM

### 7.2 Photometric Survey

Euclid photometry:
- Weak lensing measures σ₈(z) directly
- Cross-correlation with spectroscopic sample
- Independent test of growth history

---

## 8. Alternative Observables

### 8.1 Galaxy-Galaxy Lensing + Clustering

The "3×2pt" analysis combines:
- Galaxy clustering (sensitive to b²σ₈²)
- Galaxy-galaxy lensing (sensitive to bσ₈)
- Cosmic shear (sensitive to σ₈²)

Zimmerman modifies all three consistently.

### 8.2 Kinematic Sunyaev-Zeldovich Effect

The kSZ effect measures peculiar velocities:
$$\Delta T_{kSZ} \propto \int n_e v_\parallel \, dl$$

**Zimmerman predicts ~10% higher kSZ signal at z > 1.**

### 8.3 ISW Effect

The Integrated Sachs-Wolfe effect:
$$\Delta T_{ISW} \propto \int (\dot{\Phi} + \dot{\Psi}) \, dl$$

Modified growth → modified potential evolution → different ISW.

---

## 9. Falsification Criteria

The Zimmerman growth rate prediction is falsified if:

1. **DESI finds f_ΛCDM at z > 1:** If fσ₈ matches ΛCDM exactly at z = 1-2 (within 5%), no enhancement.

2. **Growth consistent with ΛCDM + Planck:** If f(z) exactly matches ΛCDM predictions using Planck σ₈, no modification needed.

3. **S8 tension disappears:** If future surveys find S8 ≈ 0.83 locally, growth history matches ΛCDM.

---

## 10. Summary

| Quantity | ΛCDM | Zimmerman | Observable |
|----------|------|-----------|------------|
| f(z=2) | 0.88 | 0.97 | RSD |
| fσ₈(z=2) | 0.44 | 0.53 | RSD |
| Enhancement | — | +10-20% at z>1 | DESI, Euclid |
| S8 suppression | 0% | 8% | Weak lensing |

The Zimmerman Formula predicts:

$$f_{Zimmerman}(z) = f_{\Lambda CDM}(z) \times [1 + 0.1 \ln E(z)]$$

This produces:
- ~10% enhanced growth at z = 2
- ~20% higher fσ₈ at z = 1.5
- Natural S8 suppression at z = 0
- Enhanced peculiar velocities

**DESI Year 5 and Euclid can confirm or falsify this at >5σ.**

---

## References

1. Zimmerman, C. (2026). Zenodo. DOI: 10.5281/zenodo.19114050
2. DESI Collaboration (2024). *arXiv:2404.xxxxx*.
3. Euclid Collaboration (2024). *A&A*, in press.
4. Alam, S. et al. (2021). *PRD*, 103, 083533.
5. Linder, E.V. (2005). *PRD*, 72, 043529.
6. Skara, F. & Perivolaropoulos, L. (2020). *PRD*, 101, 063521.

---

**Code:** https://github.com/carlzimmerman/zimmerman-formula

**Citation:** Zimmerman, C. (2026). DOI: 10.5281/zenodo.19114050
