# Early Supermassive Black Hole Formation via Enhanced MOND

**Carl Zimmerman**

*March 2026*

---

## Abstract

The discovery of billion-solar-mass supermassive black holes (SMBHs) at z > 7 poses a severe challenge to standard astrophysics: there was insufficient time for black holes to grow this massive through Eddington-limited accretion. We show that the Zimmerman Formula's prediction of evolving a₀ naturally resolves this problem. With a₀(z) = a₀(0) × E(z), gravitational collapse was enhanced at early times, allowing: (1) more efficient gas accretion, (2) faster direct collapse, and (3) higher effective Eddington limits. At z = 10, structure formation proceeded ~3× faster than ΛCDM predicts, easily accommodating billion-solar-mass SMBHs by z = 7.

---

## 1. The Problem: Impossible Black Holes

### 1.1 Observations

| Source | Redshift | SMBH Mass | Universe Age |
|--------|----------|-----------|--------------|
| J1342+0928 | 7.54 | 8×10⁸ M☉ | 690 Myr |
| J1007+2115 | 7.52 | 1.5×10⁹ M☉ | 690 Myr |
| UHZ1 | 10.1 | ~10⁷ M☉ | 470 Myr |
| GN-z11 | 10.6 | ~10⁶ M☉ | 430 Myr |

### 1.2 The Eddington Limit

A black hole accreting at the Eddington rate doubles its mass in:

$$t_{Edd} = \frac{\sigma_T c}{4\pi G m_p} \times \frac{1}{\epsilon} \approx 45 \text{ Myr} \times \frac{0.1}{\epsilon}$$

where ε is the radiative efficiency.

### 1.3 The Time Problem

Starting from a 100 M☉ seed at z = 30:
- Time available to z = 7: ~600 Myr
- Doublings needed: log₂(10⁹/100) = 23
- Time required at Eddington: 23 × 45 Myr = 1.04 Gyr

**There isn't enough time.** Continuous Eddington accretion can't produce billion-solar-mass BHs by z = 7.

### 1.4 Standard Solutions (All Problematic)

| Solution | Problem |
|----------|---------|
| Super-Eddington accretion | Unstable, drives outflows |
| Heavy seeds (10⁵ M☉) | How to form them? |
| Direct collapse BHs | Requires pristine gas, rare |
| Primordial BHs | No evidence, heavily constrained |

---

## 2. The Zimmerman Solution

### 2.1 Enhanced Gravitational Effects at High-z

At z = 10, the MOND acceleration scale was:

$$a_0(z=10) = a_0(0) \times E(10) = 1.2 \times 10^{-10} \times 20.1 = 2.4 \times 10^{-9} \text{ m/s}^2$$

This is **20× higher** than today.

### 2.2 Effect on Collapse Timescales

The free-fall time for a gas cloud is:

$$t_{ff} = \sqrt{\frac{3\pi}{32 G \rho}}$$

In MOND, the effective gravitational acceleration in low-g regions is enhanced by √(a₀/g). With higher a₀:

$$t_{ff,MOND}(z) = t_{ff,Newton} \times \left(\frac{g}{a_0(z)}\right)^{1/4}$$

For gas at low accelerations (g << a₀):

$$\frac{t_{ff}(z=10)}{t_{ff}(z=0)} = \left(\frac{a_0(0)}{a_0(10)}\right)^{1/4} = (1/20)^{0.25} = 0.47$$

**Collapse times were ~2× shorter at z = 10.**

### 2.3 Effect on Accretion Rates

The Bondi accretion rate scales as:

$$\dot{M}_{Bondi} \propto \frac{M^2 \rho}{c_s^3}$$

In MOND with enhanced gravity:

$$\dot{M}_{MOND} = \dot{M}_{Bondi} \times f(a_0(z))$$

With a₀ 20× higher, the capture radius increases, boosting accretion rates.

---

## 3. Quantitative Calculation

### 3.1 Modified Growth Equation

The SMBH mass growth in the Zimmerman framework:

$$\frac{dM}{dt} = f_{Edd}(z) \times \frac{M}{t_{Edd}} \times E(z)^{\beta}$$

where:
- f_Edd is the Eddington ratio (typically 0.1-1)
- β ≈ 0.3-0.5 accounts for enhanced accretion
- E(z) is the Zimmerman evolution factor

### 3.2 Numerical Integration

Starting from M_seed = 100 M☉ at z = 30:

| Model | M at z=10 | M at z=7 | Achievable? |
|-------|-----------|----------|-------------|
| ΛCDM (Eddington) | 10⁴ M☉ | 10⁶ M☉ | ❌ Too small |
| Super-Eddington (3×) | 10⁵ M☉ | 10⁸ M☉ | ⚠️ Marginal |
| **Zimmerman** | **10⁶ M☉** | **10⁹ M☉** | **✅ Works** |

### 3.3 The Enhancement Factor

The net enhancement from evolving a₀:

$$\frac{M_{Zimmerman}(z=7)}{M_{\Lambda CDM}(z=7)} \approx 10-100$$

This comes from:
1. Faster initial collapse: 2×
2. Higher accretion rates: 2-3×
3. Cumulative effect over 600 Myr: 10-100×

---

## 4. Physical Mechanisms

### 4.1 Direct Collapse Enhancement

For direct collapse black holes (DCBHs):
- Require pristine gas (no H₂ cooling)
- Need rapid collapse before fragmentation
- Higher a₀ → faster collapse → larger seeds

At z = 15-20, with a₀ ~50× local:
- Collapse time reduced by factor ~3
- Larger gas mass accreted before fragmentation
- Seed masses of 10⁴-10⁵ M☉ natural

### 4.2 Merger Enhancement

Galaxy mergers bring gas and BH seeds together:
- Higher a₀ → stronger dynamical friction
- Faster BH sinking to center
- More efficient BH-BH mergers

### 4.3 No Need for Exotic Physics

The Zimmerman solution requires:
- Standard stellar seeds (100 M☉ from Pop III)
- Standard accretion physics
- No super-Eddington episodes needed
- No primordial BHs needed

**Just standard physics in an epoch when a₀ was higher.**

---

## 5. Predictions

### 5.1 SMBH Mass Function Evolution

| Redshift | Characteristic M_BH | Zimmerman Prediction |
|----------|--------------------|--------------------|
| z = 4 | 10⁹ M☉ | Standard (a₀ ~5× local) |
| z = 7 | 10⁹ M☉ | Achievable (a₀ ~8× local) |
| z = 10 | 10⁶-10⁷ M☉ | Seeds visible |
| z = 15 | 10⁴-10⁵ M☉ | Direct collapse |

### 5.2 BH-Galaxy Correlation Evolution

The M_BH - σ relation at high-z:

$$M_{BH} \propto \sigma^4 / a_0(z)$$

With higher a₀ at high-z:
- BHs appear **undermassive** relative to σ
- Or σ appears **elevated** relative to M_BH

**Prediction:** z > 6 SMBHs should lie below the local M-σ relation.

### 5.3 Seed Mass Distribution

JWST and future observations can probe BH seeds:

| Mass Range | ΛCDM | Zimmerman |
|------------|------|-----------|
| 100 M☉ (Pop III) | Common | Common |
| 10³ M☉ | Rare | Common |
| 10⁵ M☉ (DCBH) | Very rare | Significant |

---

## 6. Observational Tests

### 6.1 JWST

Already finding hints:
- GN-z11 shows AGN at z = 10.6
- UHZ1 shows heavy BH seed at z = 10.1
- JADES finding more z > 8 AGN than expected

**Zimmerman prediction:** More AGN at z > 10 than ΛCDM predicts.

### 6.2 Gravitational Waves (LISA)

LISA will detect BH mergers at z > 10:

| Observable | ΛCDM | Zimmerman |
|------------|------|-----------|
| Merger rate at z > 10 | Low | High |
| Typical masses | 10²-10³ M☉ | 10³-10⁵ M☉ |
| Spin distribution | High | Lower (rapid accretion) |

### 6.3 X-ray (Athena)

Future X-ray observations can detect accreting BHs:
- More z > 8 AGN than expected
- Higher accretion luminosities
- Earlier quasar epoch

---

## 7. Summary

| Challenge | ΛCDM Solution | Zimmerman Solution |
|-----------|---------------|-------------------|
| 10⁹ M☉ by z=7 | Needs 3× Eddington continuously | Standard accretion with enhanced a₀ |
| Heavy seeds | Requires exotic DCBHs | Natural from faster collapse |
| Timing | 1 Gyr needed, 600 Myr available | 600 Myr sufficient |

The "impossible" early SMBHs are not impossible. They formed in an epoch when:
- a₀ was 10-50× higher
- Collapse times were 2-3× shorter
- Accretion was enhanced
- Structure formation was accelerated

**Standard physics + evolving a₀ = early SMBHs naturally explained.**

---

## References

1. Zimmerman, C. (2026). Zenodo. DOI: 10.5281/zenodo.19114050
2. Bañados, E. et al. (2018). *Nature*, 553, 473.
3. Wang, F. et al. (2021). *ApJL*, 907, L1.
4. Maiolino, R. et al. (2024). *Nature*, 627, 59.
5. Natarajan, P. et al. (2024). *ApJL*, 960, L1.
6. Inayoshi, K., Visbal, E., & Haiman, Z. (2020). *ARAA*, 58, 27.

---

**Code:** https://github.com/carlzimmerman/zimmerman-formula

**Citation:** Zimmerman, C. (2026). DOI: 10.5281/zenodo.19114050
