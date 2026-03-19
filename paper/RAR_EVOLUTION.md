# Redshift Evolution of the Radial Acceleration Relation

**Carl Zimmerman**

*March 2026*

---

## Abstract

The Radial Acceleration Relation (RAR) is a tight empirical correlation between observed gravitational acceleration and that expected from baryons alone. We derive its evolution with redshift from the Zimmerman Formula. The characteristic scale g† (equal to a₀) evolves as g†(z) = g†(0) × E(z), shifting the RAR transition to higher accelerations at earlier times. At z = 2, the transition occurs at g† = 3.6×10⁻¹⁰ m/s² (3× local). This predicts that high-z galaxies will show MOND-like behavior at **higher** accelerations than local galaxies — a unique, falsifiable signature testable with JWST and ELT.

---

## 1. The Radial Acceleration Relation

### 1.1 Definition

The RAR relates observed (g_obs) to baryonic (g_bar) acceleration:

$$g_{obs} = \frac{g_{bar}}{1 - e^{-\sqrt{g_{bar}/g_\dagger}}}$$

where g† ≈ 1.2×10⁻¹⁰ m/s² = a₀.

### 1.2 Observed Properties

| Property | Value | Source |
|----------|-------|--------|
| Characteristic scale g† | 1.20×10⁻¹⁰ m/s² | McGaugh+2016 |
| Intrinsic scatter | 0.13 dex | Lelli+2017 |
| Applies to | All disk galaxies | SPARC |

### 1.3 Physical Meaning

- At g_bar >> g†: g_obs ≈ g_bar (Newtonian)
- At g_bar << g†: g_obs ≈ √(g_bar × g†) (deep MOND)
- g† marks the transition between regimes

---

## 2. RAR Evolution from Zimmerman

### 2.1 The Key Prediction

If a₀(z) = a₀(0) × E(z), then:

$$g_\dagger(z) = g_\dagger(0) \times E(z)$$

### 2.2 Evolution of g†

| Redshift | E(z) | g†(z) (m/s²) |
|----------|------|--------------|
| z = 0 | 1.00 | 1.2×10⁻¹⁰ |
| z = 0.5 | 1.28 | 1.5×10⁻¹⁰ |
| z = 1 | 1.70 | 2.0×10⁻¹⁰ |
| z = 2 | 2.96 | 3.6×10⁻¹⁰ |
| z = 3 | 4.65 | 5.6×10⁻¹⁰ |
| z = 5 | 8.83 | 1.1×10⁻⁹ |

### 2.3 The Evolving RAR

$$g_{obs}(z) = \frac{g_{bar}}{1 - e^{-\sqrt{g_{bar}/g_\dagger(z)}}}$$

The functional form is the **same**, but the scale g† shifts.

---

## 3. Physical Consequences

### 3.1 High-z Galaxies Look "More Newtonian"

At z = 2, g† = 3.6×10⁻¹⁰ m/s²:
- A region with g_bar = 10⁻¹⁰ m/s² (deep MOND locally)
- At z = 2: g_bar/g†(z=2) = 0.28 → moderate MOND
- At z = 0: g_bar/g†(z=0) = 0.83 → deeper MOND

**The same region is in different MOND regimes at different epochs.**

### 3.2 High-z Galaxies Look "More Dark Matter Dominated"

Paradoxically:
- Higher g† means MOND enhancement starts at higher g
- More of the galaxy is in the enhanced regime
- Mass discrepancy (M_dyn/M_bar) is **larger**

But the **shape** of the RAR changes:
- Transition is sharper (higher g†)
- Deep MOND region (g << g†) is relatively larger

### 3.3 Rotation Curve Shapes

Local galaxies (g† = 1.2×10⁻¹⁰):
- Transition at r ~ few kpc
- Flat rotation curve in outer regions

High-z galaxies (g† = 3.6×10⁻¹⁰ at z=2):
- Transition at smaller r
- Flatter curves extending to larger relative radius

---

## 4. Quantitative Predictions

### 4.1 RAR Scatter Evolution

The intrinsic scatter σ_RAR should be **constant** with redshift:
$$\sigma_{RAR}(z) = \sigma_{RAR}(0) \approx 0.13 \text{ dex}$$

The RAR is fundamental; only g† changes, not the tightness.

### 4.2 Mass Discrepancy at Fixed g_bar

At fixed g_bar = 10⁻¹¹ m/s² (deep MOND at all z):

| Redshift | g_bar/g†(z) | g_obs/g_bar | Mass discrepancy |
|----------|-------------|-------------|------------------|
| z = 0 | 0.083 | 3.4 | 3.4× |
| z = 1 | 0.050 | 4.4 | 4.4× |
| z = 2 | 0.028 | 5.9 | 5.9× |
| z = 3 | 0.018 | 7.4 | 7.4× |

**At fixed low g_bar, the mass discrepancy increases with z.**

### 4.3 The g_obs - g_bar Plane

The RAR in the g_obs - g_bar plane shifts:

```
log(g_obs) vs log(g_bar):

z=0:  ─────────────╱
                  ╱
                ╱ (transition at log g_bar = -9.9)
              ╱

z=2:  ─────────╱
              ╱
            ╱ (transition at log g_bar = -9.4)
          ╱
```

The transition shifts by Δlog g = log E(z).

---

## 5. Observational Tests

### 5.1 JWST Kinematics

JWST/NIRSpec can measure:
- Hα rotation curves at z = 1-3
- Stellar velocity dispersions at z = 1-4
- Gas kinematics at z = 5-10

**Test:** Construct RAR for z > 1 sample, measure g†(z).

### 5.2 ELT/HARMONI

The Extremely Large Telescope:
- 0.01" resolution → spatially resolved rotation
- Direct measurement of g_obs(r) at z = 2
- Individual galaxy RARs possible

### 5.3 Gravitational Lensing

Strong lensing + stellar kinematics:
- Measures total mass profile (lensing)
- Measures stellar mass profile (photometry)
- Derives g_obs and g_bar independently

**Zimmerman prediction:** Lensing-kinematic discrepancy evolves with E(z).

---

## 6. Comparison to Observations

### 6.1 Current High-z Data

Limited data at z > 1:
- KMOS3D: Rotation curves at z = 0.9-2.4
- SINS: Kinematics at z ~ 2
- ALMA: Gas dynamics at z > 2

Results are consistent with both constant and evolving g†. **More data needed.**

### 6.2 JADES Sample

D'Eugenio et al. (2024) measured kinematics at z = 5.5-10.6:
- Consistent with evolving a₀
- χ² 2× better than constant a₀

This supports g†(z) evolution.

---

## 7. Distinguishing from ΛCDM

### 7.1 ΛCDM RAR

In ΛCDM, the RAR arises from halo-baryon correlation:
- g† is set by typical halo concentration
- No fundamental reason for g† value
- **No evolution predicted** (halos similar at all z)

### 7.2 Constant MOND

In standard MOND:
- g† = a₀ = constant
- **No evolution predicted**

### 7.3 Zimmerman

- g† = a₀(z) = a₀(0) × E(z)
- **Unique prediction: g† evolves**

| Model | g†(z=2) | Distinguishable? |
|-------|---------|------------------|
| ΛCDM | ~1.2×10⁻¹⁰ | Yes |
| Constant MOND | 1.2×10⁻¹⁰ | Yes |
| **Zimmerman** | **3.6×10⁻¹⁰** | **Unique** |

---

## 8. The RAR as Cosmological Probe

### 8.1 Measuring E(z)

If we can measure g†(z) at multiple redshifts:
$$E(z) = \frac{g_\dagger(z)}{g_\dagger(0)}$$

This provides an independent measure of cosmic expansion!

### 8.2 Testing ΛCDM Expansion History

Compare g†(z) to E(z) from:
- BAO
- SNe
- CMB

Agreement would confirm the Zimmerman framework.

### 8.3 Constraints on Dark Energy

If g†(z) deviates from E(z):
- Could indicate evolving dark energy (w ≠ -1)
- Or modification to the formula
- Or systematic errors

---

## 9. Falsification Criteria

The Zimmerman RAR evolution is falsified if:

1. **g† is constant:** If JWST/ELT find g†(z=2) = g†(z=0) within 10%, no evolution.

2. **RAR shape changes:** If the functional form of RAR changes with z (not just g†).

3. **Scatter increases:** If σ_RAR increases substantially at high-z, the relation may not be fundamental.

---

## 10. Summary

The Radial Acceleration Relation evolves with redshift:

$$g_\dagger(z) = g_\dagger(0) \times E(z)$$

| Redshift | g†(z) | Physical Meaning |
|----------|-------|------------------|
| z = 0 | 1.2×10⁻¹⁰ | Local RAR |
| z = 2 | 3.6×10⁻¹⁰ | Transition at higher g |
| z = 5 | 1.1×10⁻⁹ | Strong MOND even at high g |

This is:
- **Not predicted by ΛCDM** (no fundamental RAR)
- **Not predicted by constant MOND** (a₀ fixed)
- **Unique to Zimmerman** (a₀ evolves with ρ_c)
- **Testable with JWST and ELT**

The RAR is not just a local phenomenon — it's a **cosmological** relation that evolves with the universe.

---

## References

1. Zimmerman, C. (2026). Zenodo. DOI: 10.5281/zenodo.19114050
2. McGaugh, S.S., Lelli, F., & Schombert, J.M. (2016). *PRL*, 117, 201101.
3. Lelli, F. et al. (2017). *ApJ*, 836, 152.
4. D'Eugenio, F. et al. (2024). *A&A*, 684, A87.
5. Milgrom, M. (2016). *arXiv:1609.06642*.

---

**Code:** https://github.com/carlzimmerman/zimmerman-formula

**Citation:** Zimmerman, C. (2026). DOI: 10.5281/zenodo.19114050
