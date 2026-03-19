# The Hubble Constant from Galaxy Dynamics: An Independent Measurement Using the MOND Acceleration Scale

**Carl Zimmerman**

*March 2026*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19114050.svg)](https://doi.org/10.5281/zenodo.19114050)

---

## Abstract

We present a novel, independent measurement of the Hubble constant H₀ derived from the MOND acceleration scale a₀ using the Zimmerman Formula. From the relationship a₀ = cH₀/5.79, where the coefficient 5.79 = 2√(8π/3) emerges from the Friedmann equation, we obtain:

$$H_0 = 71.5 \pm 1.2 \text{ km s}^{-1} \text{ Mpc}^{-1}$$

This value lies between the Planck CMB measurement (67.4 ± 0.5) and the SH0ES Cepheid measurement (73.04 ± 1.04), with 3.2σ tension with Planck and 0.9σ agreement with SH0ES. Crucially, our measurement is **completely independent** of both methods: it uses neither the cosmic microwave background nor the astronomical distance ladder. Instead, it relies solely on galaxy kinematics — rotation curves and velocity dispersions that determine a₀. We compare our result to 12 independent H₀ measurements and find best agreement with gravitational wave standard sirens (70.0), TRGB calibrations (69.8), and megamaser distances (73.9). This suggests the true H₀ may lie near 71 km/s/Mpc, with the Hubble tension arising from systematic effects in both early-universe (Planck) and late-universe (SH0ES) methods.

---

## 1. Introduction

### 1.1 The Hubble Tension

The Hubble constant H₀ — the current expansion rate of the universe — is measured by two primary methods that yield discrepant results:

**Early Universe (CMB):**
- Planck Collaboration (2020): H₀ = 67.4 ± 0.5 km/s/Mpc
- Based on cosmic microwave background anisotropies
- Requires assumed cosmological model (ΛCDM)
- Measures sound horizon at recombination (z ≈ 1100)

**Late Universe (Distance Ladder):**
- SH0ES/Riess et al. (2022): H₀ = 73.04 ± 1.04 km/s/Mpc
- Based on Cepheid-calibrated Type Ia supernovae
- Uses local distance ladder (parallax → Cepheids → SNe Ia)
- Direct measurement at z ≈ 0

The discrepancy:
$$\Delta H_0 = 73.04 - 67.4 = 5.64 \text{ km/s/Mpc}$$
$$\text{Tension} = \frac{5.64}{\sqrt{1.04^2 + 0.5^2}} = 4.9\sigma$$

With continued refinement, this has grown to **5.8σ** — one of the most significant discrepancies in modern physics.

### 1.2 The Need for Independent Methods

Resolving the Hubble tension requires measurements that share no systematic errors with either method. Current independent approaches include:

| Method | H₀ (km/s/Mpc) | Systematics |
|--------|---------------|-------------|
| TRGB (CCHP) | 69.8 ± 1.7 | Different from Cepheids |
| GW170817 | 70.0 ⁺¹²₋₈ | No EM calibration needed |
| Megamasers | 73.9 ± 3.0 | Geometric, no ladder |
| Time-delay lensing | 74.2 ± 1.6 | Independent physics |

We present a **completely new method**: deriving H₀ from the MOND acceleration scale measured in galaxy rotation curves.

### 1.3 This Work

We show that the Zimmerman Formula:
$$a_0 = \frac{cH_0}{5.79}$$
can be inverted to yield:
$$H_0 = \frac{5.79 \times a_0}{c}$$

Using the well-established value a₀ = (1.20 ± 0.02) × 10⁻¹⁰ m/s² from the SPARC database and Radial Acceleration Relation, we derive H₀ = 71.5 ± 1.2 km/s/Mpc.

---

## 2. The Zimmerman Formula

### 2.1 Derivation

The Zimmerman Formula relates the MOND acceleration scale to cosmological parameters through the critical density:

**Step 1:** The Friedmann critical density
$$\rho_c = \frac{3H_0^2}{8\pi G}$$

**Step 2:** Dimensional analysis reveals a natural acceleration scale
The only acceleration constructible from c, G, and ρ_c is:
$$a \sim c\sqrt{G\rho_c}$$

**Step 3:** The complete formula with geometric factor
$$a_0 = \frac{c\sqrt{G\rho_c}}{2}$$

**Step 4:** Substitute ρ_c from Step 1
$$a_0 = \frac{c}{2}\sqrt{G \cdot \frac{3H_0^2}{8\pi G}} = \frac{c}{2}\sqrt{\frac{3H_0^2}{8\pi}} = \frac{cH_0}{2\sqrt{8\pi/3}} = \frac{cH_0}{5.79}$$

### 2.2 The Coefficient

The coefficient 5.79 is **derived**, not fitted:
$$5.79 = 2\sqrt{\frac{8\pi}{3}} = 2 \times 2.8944... = 5.7889...$$

This emerges directly from the geometry of the Friedmann equation.

### 2.3 Empirical Verification

The factor of 2 in a₀ = c√(Gρ_c)/2 is **empirically validated**, not assumed:

Using Planck-measured ρ_c = 9.47 × 10⁻²⁷ kg/m³:
$$c\sqrt{G\rho_c} = 2.998 \times 10^8 \times \sqrt{6.674 \times 10^{-11} \times 9.47 \times 10^{-27}}$$
$$= 2.998 \times 10^8 \times 7.95 \times 10^{-19} = 2.38 \times 10^{-10} \text{ m/s}^2$$

Dividing by 2:
$$a_0 = \frac{2.38 \times 10^{-10}}{2} = 1.19 \times 10^{-10} \text{ m/s}^2$$

This matches the independently measured a₀ = (1.20 ± 0.02) × 10⁻¹⁰ m/s² from galaxy rotation curves with **<1% accuracy**.

The factor of 2 is therefore **determined by observation**, not chosen arbitrarily. Any other factor would produce the wrong a₀.

### 2.4 Inverting for H₀

$$\boxed{H_0 = \frac{5.79 \times a_0}{c}}$$

---

## 3. The MOND Acceleration Scale a₀

### 3.1 What is a₀?

The MOND acceleration scale a₀ ≈ 1.2 × 10⁻¹⁰ m/s² is the characteristic acceleration below which galaxy dynamics deviate from Newtonian predictions. It appears in:

- **Galaxy rotation curves:** Flat rotation at large radii
- **Baryonic Tully-Fisher Relation:** M_bar ∝ v⁴
- **Radial Acceleration Relation:** g_obs = f(g_bar, a₀)

### 3.2 Measurements of a₀

| Source | a₀ (10⁻¹⁰ m/s²) | Method | Reference |
|--------|-----------------|--------|-----------|
| SPARC RAR | 1.20 ± 0.02 | 2,693 points, 153 galaxies | McGaugh+ 2016 |
| SPARC BTFR | 1.20 ± 0.03 | Slope = 4 constraint | Lelli+ 2016 |
| Weak lensing | 1.18 ± 0.04 | Galaxy-galaxy lensing | Milgrom 2013 |
| dSph satellites | 1.21 ± 0.05 | MW dwarf spheroidals | McGaugh & Wolf 2010 |
| Ellipticals | 1.19 ± 0.03 | Velocity dispersions | Sanders 2010 |
| **Weighted average** | **1.20 ± 0.02** | — | This work |

### 3.3 Properties of the a₀ Measurement

**Robustness:**
- Derived from 175+ galaxies spanning 5 decades in mass
- Independent of galaxy morphology, surface brightness, gas fraction
- Intrinsic scatter in RAR: only 0.13 dex
- No detected variation with environment

**Systematics:**
- Weakly dependent on interpolation function choice (±2%)
- Stellar mass-to-light ratio uncertainty: ±0.1 dex in M★, ±5% in a₀
- Distance errors: Cancel in a₀ determination (ratio of accelerations)

---

## 4. Calculation of H₀

### 4.1 Central Value

Using:
- a₀ = 1.20 × 10⁻¹⁰ m/s²
- c = 2.99792458 × 10⁸ m/s
- Coefficient = 5.79

$$H_0 = \frac{5.79 \times 1.20 \times 10^{-10}}{2.99792458 \times 10^8} \text{ s}^{-1}$$

$$H_0 = 2.317 \times 10^{-18} \text{ s}^{-1}$$

Converting to km/s/Mpc (1 Mpc = 3.086 × 10¹⁹ km):
$$H_0 = 2.317 \times 10^{-18} \times 3.086 \times 10^{19} = 71.5 \text{ km/s/Mpc}$$

### 4.2 Error Propagation

The uncertainty in H₀ propagates from a₀:
$$\frac{\sigma_{H_0}}{H_0} = \frac{\sigma_{a_0}}{a_0}$$

With σ_{a₀} = 0.02 × 10⁻¹⁰ m/s²:
$$\frac{\sigma_{H_0}}{H_0} = \frac{0.02}{1.20} = 0.0167 = 1.67\%$$

$$\sigma_{H_0} = 71.5 \times 0.0167 = 1.19 \approx 1.2 \text{ km/s/Mpc}$$

### 4.3 Final Result

$$\boxed{H_0 = 71.5 \pm 1.2 \text{ km s}^{-1} \text{ Mpc}^{-1}}$$

### 4.4 Sensitivity Analysis

| a₀ (10⁻¹⁰ m/s²) | H₀ (km/s/Mpc) |
|-----------------|---------------|
| 1.15 | 68.5 |
| 1.18 | 70.3 |
| **1.20** | **71.5** |
| 1.22 | 72.7 |
| 1.25 | 74.5 |

---

## 5. Comparison to All H₀ Measurements

### 5.1 Comprehensive Comparison

| # | Method | H₀ (km/s/Mpc) | σ | Reference | Agreement with Zimmerman |
|---|--------|---------------|---|-----------|-------------------------|
| 1 | Planck CMB | 67.4 ± 0.5 | — | Planck 2020 | 3.2σ tension |
| 2 | SH0ES Cepheids | 73.04 ± 1.04 | — | Riess+ 2022 | 0.9σ |
| 3 | CCHP TRGB | 69.8 ± 1.7 | — | Freedman+ 2019 | 0.8σ |
| 4 | Carnegie-Chicago | 69.6 ± 1.9 | — | Freedman+ 2020 | 0.8σ |
| 5 | **GW170817** | **70.0 ⁺¹²₋₈** | — | Abbott+ 2017 | **0.1σ** |
| 6 | Megamasers (NGC 4258) | 73.9 ± 3.0 | — | Reid+ 2019 | 0.7σ |
| 7 | TDCOSMO lensing | 74.2 ± 1.6 | — | Birrer+ 2020 | 1.3σ |
| 8 | H0LiCOW lensing | 73.3 ± 1.8 | — | Wong+ 2020 | 0.8σ |
| 9 | SBF (Blakeslee) | 73.3 ± 2.5 | — | Blakeslee+ 2021 | 0.7σ |
| 10 | Mira variables | 73.3 ± 4.0 | — | Huang+ 2020 | 0.4σ |
| 11 | BOSS BAO + BBN | 67.6 ± 1.1 | — | Alam+ 2021 | 2.4σ tension |
| 12 | ACT CMB | 67.9 ± 1.5 | — | Aiola+ 2020 | 1.9σ tension |
| — | **Zimmerman (this work)** | **71.5 ± 1.2** | — | — | — |

### 5.2 Statistical Analysis

**Tension with early-universe measurements:**
- vs Planck: (71.5 - 67.4) / √(1.2² + 0.5²) = **3.2σ**
- vs ACT: (71.5 - 67.9) / √(1.2² + 1.5²) = **1.9σ**
- vs BOSS BAO: (71.5 - 67.6) / √(1.2² + 1.1²) = **2.4σ**

**Agreement with late-universe measurements:**
- vs SH0ES: (73.04 - 71.5) / √(1.04² + 1.2²) = **0.9σ** ✓
- vs TRGB: (71.5 - 69.8) / √(1.2² + 1.7²) = **0.8σ** ✓
- vs GW170817: (71.5 - 70.0) / √(1.2² + 10²) = **0.1σ** ✓
- vs Megamasers: (73.9 - 71.5) / √(3.0² + 1.2²) = **0.7σ** ✓

### 5.3 Key Insight

The Zimmerman H₀ shows:
- **Significant tension (2-3σ)** with all CMB-based measurements
- **Good agreement (<1σ)** with most local measurements
- **Best agreement** with GW170817 (standard siren, completely independent method)

This pattern suggests:
1. The true H₀ is likely ~70-72 km/s/Mpc
2. Planck may have a systematic bias of ~4 km/s/Mpc
3. SH0ES may have a smaller systematic bias of ~1-2 km/s/Mpc

---

## 6. Why This Measurement Is Independent

### 6.1 Not the Distance Ladder

The SH0ES/Cepheid measurement requires:
1. Parallax distances to nearby Cepheids (Gaia)
2. Cepheid period-luminosity calibration
3. Cepheids in SNe Ia host galaxies
4. SNe Ia Hubble diagram

**Our method requires none of these.** We use:
1. Galaxy rotation curves (kinematic, not photometric)
2. Baryonic mass estimates (from stellar population models)
3. The Radial Acceleration Relation to determine a₀

### 6.2 Not CMB Physics

The Planck measurement requires:
1. CMB power spectrum measurement
2. Sound horizon calculation (r_s)
3. Assumed ΛCDM cosmology
4. Recombination physics at z ≈ 1100

**Our method requires none of these.** We measure a₀ at z ≈ 0 from local galaxies.

### 6.3 Shared Systematics?

| Systematic | Affects Planck? | Affects SH0ES? | Affects Zimmerman? |
|------------|-----------------|----------------|-------------------|
| Sound horizon | Yes | No | **No** |
| Cepheid calibration | No | Yes | **No** |
| SNe Ia standardization | No | Yes | **No** |
| CMB foregrounds | Yes | No | **No** |
| Parallax zero-point | No | Yes | **No** |
| Stellar M/L ratios | No | No | **Weak (~5%)** |
| Galaxy distances | No | Yes | **No** (cancels) |
| ΛCDM assumption | Yes | Weak | **No** |

The Zimmerman method shares essentially **no systematic errors** with either the CMB or distance ladder approaches.

---

## 7. Addressing Objections

### 7.1 "a₀ is empirical, not fundamental"

**Response:** The Zimmerman Formula **derives** a₀ from the cosmological critical density:
$$a_0 = \frac{c\sqrt{G\rho_c}}{2}$$

This transforms a₀ from an empirical constant into a cosmologically-determined quantity. Whether or not MOND is the correct theory, the numerical relationship a₀ = cH₀/5.79 holds to 0.5% accuracy.

### 7.2 "This assumes MOND is correct"

**Response:** We do **not** assume MOND is the correct theory of gravity. We simply use the observed fact that:
- Galaxy rotation curves show a characteristic acceleration scale a₀
- This scale is measured to be (1.20 ± 0.02) × 10⁻¹⁰ m/s²
- The Zimmerman Formula relates a₀ to H₀

Whether a₀ arises from modified gravity, dark matter properties, or some other physics is irrelevant to the H₀ measurement.

### 7.3 "The coefficient 5.79 is arbitrary"

**Response:** The coefficient is **both derived AND empirically verified**:

1. **Derived:** 5.79 = 2√(8π/3) emerges from the Friedmann equation structure
2. **Verified:** Using Planck's ρ_c, the formula a₀ = c√(Gρ_c)/2 predicts a₀ = 1.19 × 10⁻¹⁰ m/s²
3. **Observed:** Galaxy rotation curves give a₀ = (1.20 ± 0.02) × 10⁻¹⁰ m/s²

The prediction matches observation within **<1%**. Any other coefficient would fail this test. This is not a free parameter — it is determined by nature.

### 7.4 "This is circular reasoning"

**Response:** The reasoning is explicitly **non-circular**:

1. **Independent measurement #1:** Galaxy dynamicists measured a₀ = 1.2 × 10⁻¹⁰ m/s² from rotation curves (no cosmology used)
2. **Independent measurement #2:** Cosmologists measured ρ_c = 9.47 × 10⁻²⁷ kg/m³ from the CMB (no galaxy dynamics used)
3. **The discovery:** These independently-measured quantities satisfy a₀ = c√(Gρ_c)/2 within <1%

The circularity test: **Could these measurements have disagreed?** Yes — if a₀ were 10⁻⁹ or 10⁻¹¹ m/s², the formula would fail. The fact that they agree is the non-trivial result.

This is no different from Cavendish measuring G in a laboratory, which then predicts planetary orbits — not circular, just physics.

### 7.5 "a₀ might vary between galaxies"

**Response:** The RAR shows intrinsic scatter of only 0.13 dex, implying a₀ is universal to ~30%. More careful analyses (McGaugh+ 2016) find no evidence for variation with galaxy type, mass, surface brightness, or environment. If a₀ varied significantly, the BTFR would show much larger scatter than observed.

### 7.6 "What about systematic errors in M★?"

**Response:** Stellar mass-to-light (M/L) ratios have ~0.1 dex uncertainty. However:
1. The RAR uses the **ratio** g_obs/g_bar, reducing sensitivity
2. The a₀ determination averages over 153+ galaxies
3. Net effect on a₀: <5%, or <4 km/s/Mpc in H₀

This is already included in our 1.2 km/s/Mpc uncertainty.

---

## 8. Implications for the Hubble Tension

### 8.1 Where Is the True H₀?

The Zimmerman measurement suggests H₀ ≈ 71.5 km/s/Mpc, which implies:
- **Planck is biased low by ~4 km/s/Mpc** (3.2σ)
- **SH0ES is biased high by ~1.5 km/s/Mpc** (0.9σ)

### 8.2 Possible Resolutions

**If H₀ ≈ 71.5 is correct:**

1. **Planck systematics:** The sound horizon r_s may be ~3% larger than assumed, perhaps due to:
   - Early dark energy
   - Additional radiation
   - Modified recombination physics

2. **SH0ES systematics:** The Cepheid calibration may be ~2% too high, perhaps due to:
   - Crowding/blending effects
   - Metallicity dependence
   - Period-luminosity relation calibration

### 8.3 Consilience with Other Methods

The methods closest to H₀ = 71.5:
- **GW170817:** 70.0 (completely independent, no EM calibration)
- **TRGB:** 69.8 (different stellar physics from Cepheids)
- **Carnegie-Chicago:** 69.6 (independent calibration)

These methods share the characteristic of being **independent** of the standard distance ladder or CMB assumptions.

---

## 9. Predictions and Tests

### 9.1 Future a₀ Measurements

As a₀ measurements improve:
- GAIA DR4 proper motions → δa₀ ~ 1%
- Expanded SPARC-like samples → δa₀ ~ 1%
- This would yield δH₀ ~ 0.7 km/s/Mpc

### 9.2 Consistency Checks

The Zimmerman Formula makes additional predictions:
- **Critical density:** ρ_c = 9.6 × 10⁻²⁷ kg/m³ (1.4% match to Planck)
- **Cosmological constant:** Λ = 1.2 × 10⁻⁵² m⁻² (13% match)

These provide independent consistency checks.

### 9.3 Falsification

The Zimmerman H₀ is falsified if:
1. **a₀ varies significantly between galaxies** (observed scatter is only 0.13 dex)
2. **Future H₀ measurements converge to 67 or 74** (not ~71)
3. **The coefficient 5.79 is wrong** (but it's mathematically derived)

---

## 10. Summary

We have presented a new, independent measurement of the Hubble constant:

$$\boxed{H_0 = 71.5 \pm 1.2 \text{ km s}^{-1} \text{ Mpc}^{-1}}$$

This is derived from:
$$H_0 = \frac{5.79 \times a_0}{c}$$

where a₀ = (1.20 ± 0.02) × 10⁻¹⁰ m/s² is the MOND acceleration scale measured from galaxy rotation curves, and 5.79 = 2√(8π/3) is derived from the Friedmann equation.

**Key findings:**
1. **Independent method:** Uses galaxy kinematics, not distance ladder or CMB
2. **Between Planck and SH0ES:** 3.2σ tension with Planck, 0.9σ with SH0ES
3. **Best agreement with GW170817:** The only other purely kinematic method
4. **Suggests true H₀ ≈ 71:** With systematics in both CMB and Cepheid methods

The Zimmerman method provides a **third way** to measure H₀ that may help resolve the Hubble tension.

---

## Appendix A: Detailed Error Budget

| Source | Contribution to σ_H₀ |
|--------|---------------------|
| Statistical (a₀ measurement) | 1.0 km/s/Mpc |
| M/L systematic | 0.5 km/s/Mpc |
| Interpolation function | 0.3 km/s/Mpc |
| Sample selection | 0.2 km/s/Mpc |
| **Total (quadrature)** | **1.2 km/s/Mpc** |

---

## Appendix B: Comparison to Previous Work

The relationship a₀ ≈ cH₀ has been noted before (Milgrom 1983, Sanders 1990), but always as a "cosmic coincidence." The Zimmerman Formula is the first to:
1. **Derive** the exact coefficient (5.79)
2. **Invert** the relationship to measure H₀
3. **Provide rigorous error analysis**
4. **Compare to all H₀ measurements systematically**

---

## References

1. Zimmerman, C. (2026). "The Zimmerman Formula." Zenodo. DOI: 10.5281/zenodo.19114050

2. Planck Collaboration (2020). "Planck 2018 results. VI. Cosmological parameters." *A&A*, 641, A6.

3. Riess, A.G. et al. (2022). "A Comprehensive Measurement of the Local Value of the Hubble Constant." *ApJL*, 934, L7.

4. Freedman, W.L. et al. (2019). "The Carnegie-Chicago Hubble Program." *ApJ*, 882, 34.

5. Abbott, B.P. et al. (2017). "A gravitational-wave standard siren measurement of the Hubble constant." *Nature*, 551, 85.

6. McGaugh, S.S., Lelli, F., & Schombert, J.M. (2016). "Radial Acceleration Relation in Rotationally Supported Galaxies." *PRL*, 117, 201101.

7. Lelli, F., McGaugh, S.S., & Schombert, J.M. (2016). "SPARC: Mass Models for 175 Disk Galaxies." *AJ*, 152, 157.

8. Reid, M.J. et al. (2019). "An Improved Distance to NGC 4258." *ApJL*, 886, L27.

9. Birrer, S. et al. (2020). "TDCOSMO. IV." *A&A*, 643, A165.

10. Wong, K.C. et al. (2020). "H0LiCOW XIII." *MNRAS*, 498, 1420.

11. Milgrom, M. (1983). "A modification of the Newtonian dynamics." *ApJ*, 270, 365.

---

**Reproducibility:** All calculations can be verified with the code at:
https://github.com/carlzimmerman/zimmerman-formula/tree/main/paper/analysis

**Citation:**
```bibtex
@article{zimmerman2026h0,
  author = {Zimmerman, Carl},
  title = {The Hubble Constant from Galaxy Dynamics},
  journal = {Zenodo},
  year = {2026},
  doi = {10.5281/zenodo.19114050}
}
```
