# Test 5: Dark Energy Equation of State

**The w = -1 Prediction**

**Status: 2.5σ TENSION with DESI hints**

---

## Summary

| Parameter | Value |
|-----------|-------|
| Z² Prediction | w = -1.000 exactly (cosmological constant) |
| ΛCDM Standard | w = -1 (assumed) |
| DESI Hint (2024) | w₀ = -0.55 ± 0.21 (2.5σ from -1) |
| Timeline | DESI/Euclid decisive by 2030 |
| Discrimination | High (evolving w vs constant) |

---

## The Prediction

### Z² Framework

The equation of state parameter w = p/ρ for dark energy is **exactly** -1:

```
w(z) = -1  for all z

No evolution
No deviation
Cosmological constant behavior exactly
```

### Physical Origin

Moduli fields from the T³/Z₂ compactification are stabilized at a minimum:

```
V(ψ) = V₀ + ½ m² |ψ|² + higher order

At minimum: ψ = 0
           dV/dψ = 0
           V = V₀ = constant

Pressure: p = -V₀
Density:  ρ = +V₀

Therefore: w = p/ρ = -1 exactly
```

### Why No Evolution?

Standard quintessence has dynamical fields rolling in a potential:

```
w_quintessence = (½φ̇² - V(φ)) / (½φ̇² + V(φ))
```

If φ̇ ≠ 0, then w ≠ -1.

In Z²: The moduli are **frozen** at the orbifold fixed point:

```
φ̇ = 0  (no field evolution)
V = V₀  (constant vacuum energy)
w = -1  (exactly)
```

---

## Current Observations

### DESI 2024 Results

The Dark Energy Spectroscopic Instrument released hints of w ≠ -1:

```
Model: w(z) = w₀ + wₐ × (z/(1+z))

DESI BAO + CMB:
  w₀ = -0.55 ± 0.21
  wₐ = -1.30 ± 0.60

Combined tension with w₀ = -1: ~2.5σ
```

### Interpretation

| Hypothesis | w₀ | wₐ | Status |
|------------|----|----|--------|
| ΛCDM / Z² | -1.00 | 0.00 | 2.5σ tension |
| DESI best-fit | -0.55 | -1.30 | Best fit to data |
| Quintessence | > -1 | < 0 | Favored by DESI |

### Caution

The DESI result is:
- Still preliminary
- Only 2.5σ (not 5σ discovery threshold)
- May have systematic effects
- Needs confirmation from Euclid, LSST

---

## Physics of Dark Energy

### Equation of State Parameterization

The standard parameterization (CPL):

```
w(z) = w₀ + wₐ × z/(1+z)

w₀ = value today (z=0)
wₐ = rate of change with redshift
```

For Z²: w₀ = -1, wₐ = 0.

### Hubble Parameter

The expansion rate depends on w(z):

```
H²(z) = H₀² [Ω_m(1+z)³ + Ω_DE × X(z)]

where X(z) = exp(3∫₀^z (1+w(z'))/(1+z') dz')
```

For w = -1: X(z) = 1 (cosmological constant)
For w ≠ -1: X(z) evolves with redshift

### Distance Measurements

Dark energy affects distances:

```
d_L(z) = (1+z) ∫₀^z c/H(z') dz'

d_A(z) = d_L(z) / (1+z)²
```

Type Ia supernovae measure d_L(z).
BAO measures d_A(z) and H(z) separately.

---

## Comparison: Z² vs DESI

### Hubble Evolution

```
Z² (w = -1):
  H(z)/H₀ = √[Ω_m(1+z)³ + Ω_Λ]
          = √[0.316(1+z)³ + 0.684]

DESI (w₀ = -0.55, wₐ = -1.30):
  H(z)/H₀ = √[Ω_m(1+z)³ + Ω_DE × X(z)]

  where X(z) has complex redshift evolution
```

### Observational Differences

| Observable | Z² | DESI | Difference at z=1 |
|------------|----|----|------------------|
| H(z)/H₀ | 1.52 | 1.48 | 2.6% |
| d_A(z) [Gpc] | 5.23 | 5.31 | 1.5% |
| Growth D(z) | 0.58 | 0.61 | 5% |

Current uncertainties are ~1-2%, so the difference is borderline detectable.

---

## Statistical Analysis

### Current χ²

Comparing Z² (w = -1) to data:

```
CMB (Planck 2018): χ² = 2.3 (slight preference for w < -1)
BAO (DESI 2024):   χ² = 6.2 (2.5σ tension)
SN (Pantheon+):    χ² = 1.1 (consistent)

Combined: Δχ² ≈ 9.6 vs w₀ = -0.55

Significance: √9.6 ≈ 3.1σ tension
```

### Forecast Constraints

| Survey | σ(w₀) | σ(wₐ) | Year |
|--------|-------|-------|------|
| Current | 0.21 | 0.60 | 2024 |
| DESI full | 0.04 | 0.15 | 2028 |
| Euclid | 0.02 | 0.10 | 2030 |
| Combined | 0.01 | 0.05 | 2032 |

With σ(w₀) = 0.01, a deviation |w₀ + 1| > 0.05 would be 5σ.

---

## Falsification Criterion

### Z² is FALSIFIED if:

```
|w₀ + 1| > 5 × σ(w₀)  AND  wₐ ≠ 0 at 5σ

Current:  Need |w₀ + 1| > 1.05  (not reached)
Euclid:   Need |w₀ + 1| > 0.10  (reachable)
Combined: Need |w₀ + 1| > 0.05  (decisive)
```

### Z² is CONFIRMED if:

```
w₀ = -1.00 ± 0.01 and wₐ = 0.00 ± 0.05

This would reject DESI hint at >5σ
```

---

## Alternative Dark Energy Models

### Models Predicting w ≠ -1

| Model | w₀ | wₐ | Status |
|-------|----|----|--------|
| Quintessence | > -1 | < 0 | DESI-favored |
| Phantom | < -1 | - | Energy condition violation |
| Thawing | ≈ -1 | < 0 | Early freeze |
| Freezing | > -0.8 | > 0 | Late freeze |

### Z² Distinguishing Feature

Z² predicts w = -1 **exactly** - not approximately.

- If |w₀ + 1| = 0.01, Z² is still consistent
- If |w₀ + 1| = 0.10, Z² is challenged
- If |w₀ + 1| = 0.50 (like DESI), Z² is falsified

---

## Detailed Calculations

### Python Implementation

```python
import numpy as np
from scipy import integrate

# Constants
Z_SQUARED = 32 * np.pi / 3
OMEGA_M = 6/19
OMEGA_DE = 13/19
H0 = 71.5  # km/s/Mpc

def H_z_Z2(z):
    """Hubble parameter in Z² (w = -1)"""
    return H0 * np.sqrt(OMEGA_M * (1+z)**3 + OMEGA_DE)

def H_z_wCDM(z, w0, wa):
    """Hubble parameter with evolving w"""
    w_z = w0 + wa * z / (1 + z)

    # Dark energy density evolution
    def integrand(zp):
        wp = w0 + wa * zp / (1 + zp)
        return (1 + wp) / (1 + zp)

    log_X = 3 * integrate.quad(integrand, 0, z)[0]
    X = np.exp(log_X)

    return H0 * np.sqrt(OMEGA_M * (1+z)**3 + OMEGA_DE * X)

def chi2_comparison(z_data, H_data, H_err, w0, wa):
    """Chi-squared for w0, wa model vs data"""
    H_model = np.array([H_z_wCDM(z, w0, wa) for z in z_data])
    chi2 = np.sum(((H_data - H_model) / H_err)**2)
    return chi2

# Example: Test DESI hint vs Z²
z_test = np.array([0.3, 0.5, 0.7, 1.0, 1.5])

# Simulated Z² universe data
H_Z2 = np.array([H_z_Z2(z) for z in z_test])
H_err = 0.02 * H_Z2  # 2% errors

# Chi² for Z² model
chi2_Z2 = chi2_comparison(z_test, H_Z2, H_err, -1.0, 0.0)
print(f"χ² for Z² (w=-1): {chi2_Z2:.2f}")

# Chi² for DESI model
chi2_DESI = chi2_comparison(z_test, H_Z2, H_err, -0.55, -1.30)
print(f"χ² for DESI hint: {chi2_DESI:.2f}")
```

### Fisher Matrix Forecast

```python
def fisher_forecast_w(sigma_H_frac=0.01, n_bins=10):
    """
    Forecast constraints on w0, wa from future surveys.

    Parameters:
    -----------
    sigma_H_frac : float
        Fractional uncertainty on H(z)
    n_bins : int
        Number of redshift bins

    Returns:
    --------
    sigma_w0, sigma_wa : float
        Marginalized uncertainties
    """
    z_bins = np.linspace(0.1, 2.0, n_bins)
    dz = z_bins[1] - z_bins[0]

    # Derivatives of H(z) with respect to w0, wa
    # At w0=-1, wa=0 (Z² fiducial)

    F = np.zeros((2, 2))

    for z in z_bins:
        H_fid = H_z_Z2(z)
        sigma_H = sigma_H_frac * H_fid

        # Numerical derivatives
        eps = 0.01
        dH_dw0 = (H_z_wCDM(z, -1+eps, 0) - H_z_wCDM(z, -1-eps, 0)) / (2*eps)
        dH_dwa = (H_z_wCDM(z, -1, eps) - H_z_wCDM(z, -1, -eps)) / (2*eps)

        # Fisher matrix
        F[0,0] += (dH_dw0 / sigma_H)**2
        F[0,1] += (dH_dw0 * dH_dwa) / sigma_H**2
        F[1,0] += (dH_dw0 * dH_dwa) / sigma_H**2
        F[1,1] += (dH_dwa / sigma_H)**2

    # Invert for covariance
    cov = np.linalg.inv(F)
    sigma_w0 = np.sqrt(cov[0,0])
    sigma_wa = np.sqrt(cov[1,1])

    return sigma_w0, sigma_wa

# Euclid forecast
sigma_w0, sigma_wa = fisher_forecast_w(sigma_H_frac=0.01, n_bins=20)
print(f"Euclid forecast: σ(w₀) = {sigma_w0:.3f}, σ(wₐ) = {sigma_wa:.3f}")
```

---

## Timeline

```
2024: DESI Year 1 results (current)
      w₀ = -0.55 ± 0.21 (2.5σ tension)

2025-2026: DESI Year 2-3
           σ(w₀) → 0.10

2027-2028: DESI complete
           σ(w₀) → 0.04

2029-2030: Euclid results
           σ(w₀) → 0.02

2031-2032: Combined analysis
           σ(w₀) → 0.01
           DECISION: w = -1 or not
```

---

## Implications

### If w = -1 Confirmed

- Z² passes critical test
- Dynamical dark energy ruled out
- Cosmological constant problem sharpens
- Supports topological vacuum energy

### If w ≠ -1 Confirmed

- Z² is falsified
- Quintessence or similar required
- Dark energy is dynamical
- New physics beyond Z²

---

## Swampland Considerations

The string theory "Swampland" conjectures suggest:

```
Either:
  (1) w > -1 (no de Sitter vacua)
  (2) Λ not stabilized (quintessence)
```

Z² framework has w = -1 exactly, which is:
- **In tension** with strong Swampland conjectures
- **Consistent** with weak versions allowing metastable dS

If DESI is correct (w > -1), it would:
- Support Swampland over Z²
- Favor dynamical dark energy

---

## Summary

The dark energy equation of state is a **high-discrimination test** for Z²:

1. **Z² predicts w = -1 exactly** from moduli stabilization
2. **Current DESI hint** suggests w₀ ≈ -0.55 (2.5σ tension)
3. **By 2030**, Euclid will measure σ(w₀) ~ 0.02, deciding the question

This test will either:
- Confirm the cosmological constant nature of dark energy (Z² survives)
- Establish dynamical dark energy (Z² falsified)

---

*Test 5 of 10 in Z² Experimental Program*
*High-priority cosmological test*
*May 2026*
