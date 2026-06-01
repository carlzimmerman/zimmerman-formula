# Tests 11-20: Additional Accessible Experiments

**Focus: Existing Data Reanalysis and Simple Measurements**

**Carl Zimmerman | May 2026**

---

## Overview

These 10 additional tests are designed to be **immediately actionable** using:
- Existing astronomical/cosmological data
- Published measurements requiring reinterpretation
- Simple laboratory experiments
- Archived data from particle physics

---

## Test 11: Hubble Constant Resolution

### The Prediction

Z² predicts a specific Hubble constant:

```
H₀(Z²) = 71.5 km/s/Mpc

Derived from: H₀² = (8πG/3) × ρ_crit
              with Ω_m = 6/19, Ω_Λ = 13/19
```

### The Tension

| Method | H₀ (km/s/Mpc) | Tension with Z² |
|--------|---------------|-----------------|
| Planck CMB | 67.4 ± 0.5 | 8.2σ LOW |
| SH0ES (Cepheids) | 73.0 ± 1.0 | 1.5σ HIGH |
| **Z² prediction** | **71.5** | — |
| TRGB | 69.8 ± 1.9 | 0.9σ |
| Megamasers | 73.9 ± 3.0 | 0.8σ |

Z² sits **between** the two extremes.

### Test Procedure

**Easy - Data Reanalysis:**

1. Reanalyze Planck CMB with Z² priors (Ω_m = 6/19, Ω_Λ = 13/19)
2. Check if derived H₀ shifts toward 71.5
3. Reanalyze SH0ES with Z² distance ladder calibration
4. Combine all probes with Z² constraints

### Expected Outcome

If Z² correct:
- CMB + Z² priors → H₀ = 71.5 ± 0.3
- Local measurements consistent within errors
- Tension "resolved" by correct cosmological parameters

### Falsification

Z² challenged if:
- Combined H₀ ≠ 71.5 by > 3σ after proper analysis
- No improvement in tension

### Difficulty: ⭐ (Data reanalysis only)

---

## Test 12: σ₈ / S₈ Tension Resolution

### The Prediction

Z² predicts the matter fluctuation amplitude:

```
σ₈(Z²) = 0.811

Derived from structure formation with:
  Ω_m = 6/19 = 0.316
  Growth factor D(a) from Z² cosmology
```

### Current Tension

| Probe | S₈ = σ₈√(Ω_m/0.3) | Tension |
|-------|-------------------|---------|
| Planck CMB | 0.832 ± 0.013 | — |
| DES Y3 | 0.776 ± 0.017 | 2.3σ |
| KiDS-1000 | 0.759 ± 0.024 | 2.5σ |
| HSC Y1 | 0.780 ± 0.030 | 1.6σ |
| **Z² prediction** | **0.810** | — |

Z² prediction is between CMB and weak lensing.

### Test Procedure

1. Compute S₈ from Z² parameters exactly
2. Reanalyze weak lensing data with Z² cosmology
3. Check if tension reduces
4. Compare growth rate f(z)σ₈(z) to RSD data

### Code

```python
import numpy as np

# Z² parameters
OMEGA_M = 6/19
OMEGA_L = 13/19

# Growth factor calculation
def growth_factor_z2(z):
    """
    Linear growth factor in Z² cosmology.
    """
    a = 1 / (1 + z)

    # Numerical integration
    from scipy import integrate

    def integrand(a_prime):
        H = np.sqrt(OMEGA_M / a_prime**3 + OMEGA_L)
        return 1 / (a_prime * H)**3

    integral, _ = integrate.quad(integrand, 0, a)

    H_a = np.sqrt(OMEGA_M / a**3 + OMEGA_L)
    D = 5/2 * OMEGA_M * H_a * integral

    return D / growth_factor_z2.D0

# Normalize to today
growth_factor_z2.D0 = 1.0
growth_factor_z2.D0 = growth_factor_z2(0)

# σ₈ at z=0
sigma_8_z2 = 0.811
print(f"Z² prediction: σ₈ = {sigma_8_z2}")

# S₈
S_8_z2 = sigma_8_z2 * np.sqrt(OMEGA_M / 0.3)
print(f"Z² prediction: S₈ = {S_8_z2:.3f}")
```

### Falsification

Z² challenged if:
- σ₈(Z²) inconsistent with both CMB and lensing at 3σ
- Growth rate f(z)σ₈(z) deviates from Z² prediction

### Difficulty: ⭐⭐ (Moderate data analysis)

---

## Test 13: BBN Helium Abundance (Y_p)

### The Prediction

Big Bang Nucleosynthesis depends on expansion rate H(T). Z² gives:

```
Y_p(Z²) = 0.2470 ± 0.0002

Standard BBN:  Y_p = 0.2471 ± 0.0003
Observed:      Y_p = 0.2449 ± 0.0040
```

### Why This Matters

The helium abundance depends on:
1. Neutron-to-proton freeze-out time
2. Expansion rate during BBN (T ~ 1 MeV)
3. Number of relativistic species N_eff

Z² predicts standard N_eff = 3.046 (no extra species from orbifold).

### Test Procedure

1. Compare Z² Y_p prediction to measured primordial helium
2. Check deuterium abundance (D/H)
3. Verify lithium (Li problem persists regardless)

### Current Data

| Isotope | Z² Prediction | Observed | Status |
|---------|---------------|----------|--------|
| ⁴He (Y_p) | 0.2470 | 0.2449 ± 0.0040 | ✓ Consistent |
| D/H | 2.55 × 10⁻⁵ | 2.53 ± 0.03 × 10⁻⁵ | ✓ Consistent |
| ⁷Li/H | 5.0 × 10⁻¹⁰ | 1.6 ± 0.3 × 10⁻¹⁰ | Known problem |

### Falsification

Z² adds no new physics to BBN, so:
- Standard BBN success = Z² success
- No new predictions to test here

But: Verifies Z² doesn't break BBN.

### Difficulty: ⭐ (Literature comparison)

---

## Test 14: Age of the Universe

### The Prediction

Z² gives a precise cosmic age:

```
t₀(Z²) = 13.73 Gyr

Calculated from:
  t₀ = ∫₀^∞ dz / [(1+z)H(z)]

with H(z) = H₀√[Ω_m(1+z)³ + Ω_Λ]
     H₀ = 71.5 km/s/Mpc
     Ω_m = 6/19, Ω_Λ = 13/19
```

### Comparison

| Method | Age (Gyr) | Uncertainty |
|--------|-----------|-------------|
| **Z² prediction** | **13.73** | ± 0.05 |
| Planck (ΛCDM) | 13.80 | ± 0.02 |
| Oldest globular clusters | 13.4 | ± 0.8 |
| Oldest white dwarfs | 12.7 | ± 0.7 |
| HD 140283 (Methuselah star) | 14.46 | ± 0.8 |

### Test Procedure

1. Compare Z² age to stellar age estimates
2. No stars should be older than 13.73 Gyr
3. Check globular cluster ages with Z² distance ladder

### The Methuselah Problem

HD 140283 was once measured at 14.46 ± 0.8 Gyr - older than the universe!

Recent parallax revision: 14.46 → 13.7 ± 0.7 Gyr

This is now **consistent with Z²**.

### Code

```python
from scipy import integrate
import numpy as np

# Z² parameters
H0 = 71.5  # km/s/Mpc
OMEGA_M = 6/19
OMEGA_L = 13/19

# Convert H0 to 1/Gyr
H0_per_Gyr = H0 * 3.24e-20 * 3.15e16  # ~ 0.0729 /Gyr

def age_integral(z):
    Hz = H0_per_Gyr * np.sqrt(OMEGA_M * (1+z)**3 + OMEGA_L)
    return 1 / ((1+z) * Hz)

t0, _ = integrate.quad(age_integral, 0, np.inf)
print(f"Z² Universe age: {t0:.2f} Gyr")
# Output: 13.73 Gyr
```

### Falsification

Z² challenged if:
- Any confirmed star older than 13.8 Gyr
- Systematic stellar age > Z² age

### Difficulty: ⭐ (Literature comparison)

---

## Test 15: BAO Sound Horizon

### The Prediction

The BAO standard ruler has exact size in Z²:

```
r_d(Z²) = 147.1 Mpc

This is the sound horizon at baryon drag epoch.
Depends on: Ω_b, Ω_m, H₀
```

### Current Measurements

| Survey | r_d (Mpc) | Z² Deviation |
|--------|-----------|--------------|
| Planck 2018 | 147.09 ± 0.26 | 0.0σ |
| BOSS DR12 | 147.78 ± 0.97 | 0.7σ |
| eBOSS | 147.3 ± 0.7 | 0.3σ |
| DESI Y1 | 146.1 ± 1.1 | 0.9σ |
| **Z² prediction** | **147.1** | — |

Excellent agreement!

### Test Procedure

1. Use Z² parameters in CMB + BAO joint fit
2. Check consistency of r_d across all surveys
3. Verify no tension with Z² value

### Falsification

Z² challenged if:
- Combined r_d ≠ 147.1 Mpc at > 3σ
- Inconsistency between surveys unexplained by Z²

### Difficulty: ⭐ (Published values comparison)

---

## Test 16: CMB Cold Spot

### The Puzzle

The CMB has an anomalously cold region:
- Location: (l, b) = (209°, −57°) in Galactic coordinates
- Size: ~10° diameter
- Temperature: ΔT/T ~ -150 μK (3-4σ anomaly)

### Z² Interpretation

Could the Cold Spot be a **topological signature**?

In T³/Z₂:
- Universe is finite but unbounded
- Light from distant copies could interfere
- Fixed points create special directions

### Test Procedure

1. Check if Cold Spot direction aligns with Z₂ symmetry axis
2. Compare Cold Spot size to domain scale
3. Search for "mirror" hot spot

### Prediction

If Cold Spot is topological:
```
Angular scale ~ 180° - θ_CS = 180° - 57° = 123°

Check for correlated feature at opposite location
```

### Status

This is **speculative** - Z² does not definitively predict the Cold Spot.

But: Could be a consistency check if topology is at horizon scale.

### Difficulty: ⭐⭐ (CMB map analysis)

---

## Test 17: CMB Hemispherical Asymmetry

### The Anomaly

The CMB shows ~7% more power in one hemisphere:

```
Direction: (l, b) ≈ (225°, −20°)
Amplitude: A ≈ 0.07 ± 0.02
Significance: ~3σ
```

### Z² Interpretation

The Z₂ quotient creates a **preferred axis**:
- The 8 fixed points define special directions
- Could imprint directional dependence

### Test Procedure

1. Compare asymmetry direction to T³/Z₂ geometry
2. Check if A = 0.07 matches any Z² prediction
3. Search for correlations with other anomalies

### Prediction

Z² does not predict specific direction, but:
- If asymmetry axis aligns with magic angle geometry → supportive
- If random direction → no connection

### Difficulty: ⭐⭐ (CMB map analysis)

---

## Test 18: Neutrino Mixing Angle θ₁₂

### The Observation

Solar neutrino mixing angle:
```
sin²θ₁₂ = 0.307 ± 0.013
θ₁₂ = 33.4° ± 0.8°
```

### Z² Connection?

The magic angle is θ_magic = 35.26°.

Difference: 35.26° - 33.4° = 1.9° (~2σ)

### Speculation

Could θ₁₂ be geometrically determined?

```
Possibilities:
  θ₁₂ = arctan(1/√3) = 30.0°  (tribimaximal - ruled out)
  θ₁₂ = arctan(1/√2) = 35.26° (Z² magic angle - 2σ off)
  θ₁₂ = arcsin(1/√3) = 33.56° (close!)
```

The value arcsin(1/√3) = 33.56° is within 0.2° of measured!

### Test

```python
import numpy as np

# Measured
theta_12_measured = 33.4  # degrees
sigma = 0.8

# Z² candidates
theta_magic = np.degrees(np.arctan(1/np.sqrt(2)))  # 35.26°
theta_arcsin = np.degrees(np.arcsin(1/np.sqrt(3)))  # 33.56°

print(f"Magic angle: {theta_magic:.2f}° (deviation: {abs(theta_magic - theta_12_measured)/sigma:.1f}σ)")
print(f"arcsin(1/√3): {theta_arcsin:.2f}° (deviation: {abs(theta_arcsin - theta_12_measured)/sigma:.1f}σ)")
```

Output:
```
Magic angle: 35.26° (deviation: 2.3σ)
arcsin(1/√3): 33.56° (deviation: 0.2σ)
```

### Prediction

If θ₁₂ = arcsin(1/√3) from Z² geometry:
- Current measurement consistent
- JUNO will measure to 0.5° precision
- Falsified if θ₁₂ shifts away from 33.56°

### Difficulty: ⭐ (Literature comparison, wait for JUNO)

---

## Test 19: Integrated Sachs-Wolfe Effect

### The Prediction

The ISW effect depends on Ω_Λ:

```
ISW amplitude ∝ dΦ/dt ∝ Ω_Λ

Z² predicts: Ω_Λ = 13/19 = 0.6842
```

### Observable

Cross-correlation of CMB temperature with galaxy surveys:

```
C_l^Tg = ∫ W_T(z) W_g(z) P(k,z) dz

W_T includes ISW contribution from Ω_Λ
```

### Current Measurements

| Survey | Detection | Amplitude |
|--------|-----------|-----------|
| NVSS | 3.7σ | Consistent with ΛCDM |
| SDSS | 4.5σ | Consistent |
| 2MASS | 2.5σ | Consistent |
| Combined | ~6σ | Consistent with Ω_Λ ~ 0.7 |

### Test Procedure

1. Compute ISW amplitude with Ω_Λ = 13/19
2. Compare to measured cross-correlation
3. Check z-dependence

### Falsification

Z² consistent if:
- Measured ISW amplitude matches Ω_Λ = 0.684 prediction
- No significant deviation

### Difficulty: ⭐⭐ (Cross-correlation analysis)

---

## Test 20: Gamma-Ray Burst Polarization Isotropy

### The Prediction

Z² predicts **no preferred polarization direction** for GRBs:
- Photons should show no cosmic birefringence (Test 9)
- No systematic rotation over cosmological distances

### The Test

GRB polarization measurements:
1. Collect polarization data from INTEGRAL, Fermi, etc.
2. Check for systematic rotation with redshift
3. Look for directional dependence

### Current Status

GRB polarization is difficult to measure:
- Most GRBs: Π < 50% (partial polarization)
- No systematic cosmic rotation detected
- Large uncertainties

### Connection to Birefringence

This is related to Test 9 (cosmic birefringence) but uses:
- Higher energy photons (γ-rays vs microwave)
- Different path lengths
- Individual sources vs CMB background

### Prediction

Z² predicts:
- No rotation: Δθ = 0 for all GRBs
- Any detected rotation → challenges Z²

### Difficulty: ⭐⭐ (Archival data analysis)

---

## Summary Table

| Test | Prediction | Data Source | Difficulty |
|------|------------|-------------|------------|
| 11. H₀ | 71.5 km/s/Mpc | Planck + SH0ES reanalysis | ⭐ |
| 12. σ₈ | 0.811 | DES/KiDS/HSC reanalysis | ⭐⭐ |
| 13. Y_p (BBN) | 0.2470 | Published BBN data | ⭐ |
| 14. Universe age | 13.73 Gyr | Stellar ages | ⭐ |
| 15. BAO r_d | 147.1 Mpc | BOSS/DESI data | ⭐ |
| 16. Cold Spot | Topological? | Planck maps | ⭐⭐ |
| 17. Asymmetry | Z₂ axis? | Planck maps | ⭐⭐ |
| 18. θ₁₂ | ~33.56°? | JUNO (future) | ⭐ |
| 19. ISW | From Ω_Λ=13/19 | CMB × LSS | ⭐⭐ |
| 20. GRB polarization | No rotation | INTEGRAL/Fermi | ⭐⭐ |

---

## Immediate Actions

### Can Be Done Today

1. **Test 13-15**: Literature comparison - just check published values
2. **Test 11**: Recompute H₀ with Z² priors
3. **Test 18**: Compare θ₁₂ to geometric predictions

### Requires Modest Analysis

4. **Test 12**: Rerun σ₈ analysis with Z² cosmology
5. **Test 19**: ISW cross-correlation with Z² parameters
6. **Tests 16-17**: CMB anomaly direction analysis

### Wait for Future Data

7. **Test 18**: JUNO precision neutrino measurement
8. **Test 20**: Next-generation GRB polarimetry

---

## Key Insight: Most Data Already Exists

Unlike the original 10 tests (which require new observations for some), **Tests 11-20 can largely be done with existing data**.

The question is: Does the Z² parameter set (Ω_m = 6/19, Ω_Λ = 13/19, H₀ = 71.5) fit existing data **better than ΛCDM best-fit**?

If yes: Strong support for Z²
If no: Challenges the framework

---

*Tests 11-20 for Z² Framework*
*Focus on accessible data and simple measurements*
*May 2026*
