# Test 9: Cosmic Birefringence

**The Most Urgent Constraint on Z²**

**Status: 4.9σ TENSION - CRITICAL**

---

## Summary

| Parameter | Value |
|-----------|-------|
| Z² Prediction | β = 0° exactly (no birefringence) |
| Current Measurement | β = 0.33° ± 0.07° (Minami & Komatsu 2020) |
| Tension | **4.9σ** |
| Future (LiteBIRD) | σ(β) ~ 0.01° |
| Discrimination | **DEFINITIVE** |

---

## CRITICAL STATUS

This is the **most urgent experimental constraint** on the Z² framework.

```
┌─────────────────────────────────────────────────────────────┐
│  WARNING: Z² may be falsified by existing data             │
│                                                             │
│  Z² predicts:  β = 0.00°                                   │
│  Observed:     β = 0.33° ± 0.07°                           │
│  Tension:      4.9σ                                        │
│                                                             │
│  If confirmed at 5σ by LiteBIRD → Z² IS FALSIFIED          │
└─────────────────────────────────────────────────────────────┘
```

---

## What is Cosmic Birefringence?

### Physical Effect

Cosmic birefringence is the rotation of the polarization plane of CMB photons as they travel from the last scattering surface to us:

```
E-mode → E-mode cos(2β) + B-mode sin(2β)
B-mode → B-mode cos(2β) - E-mode sin(2β)
```

where β is the birefringence angle.

### Observational Signature

The effect generates:
1. **EB correlation** that should be zero in standard cosmology
2. **Mixing of E and B modes** in CMB polarization
3. **Apparent rotation** of the polarization angle

### Physical Mechanism

Birefringence requires a **parity-violating coupling**:

```
L = φ F_μν F̃^μν

where:
  φ = pseudoscalar field (axion-like)
  F_μν = electromagnetic field tensor
  F̃^μν = dual tensor (εμνρσ F^ρσ)
```

This couples a pseudoscalar field to photons, rotating polarization.

---

## Z² Prediction: β = 0

### Why No Birefringence in Z²?

The T³/Z₂ orbifold has **no axionic sector**:

```
Axion candidate: φ ∝ ∫ C₁ ∧ ... (1-form integral)

On T³/Z₂:
  H¹(T³/Z₂; ℝ) = 0  (no harmonic 1-forms survive)

Without axion: No φ F F̃ coupling → No birefringence
```

### Detailed Argument

1. **Cohomology**: T³ has b₁ = 3 (three 1-cycles)
2. **Z₂ action**: All 1-cycles are mapped to their negatives
3. **Projection**: No Z₂-invariant 1-forms survive
4. **Result**: No axion-like fields exist on T³/Z₂

### Mathematical Proof

```
T³ = ℝ³/ℤ³  has  H¹(T³) = ℝ³

Z₂ action: (x,y,z) → (-x,-y,-z)
          dx → -dx, dy → -dy, dz → -dz

Z₂-invariant 1-forms: span{} = ∅

Therefore: H¹(T³/Z₂) = 0 → no axions
```

---

## Current Observations

### Minami & Komatsu (2020)

Using Planck 2018 polarization data:

```
β = 0.35° ± 0.14°  (2.5σ from zero)
```

### Updated Analysis (2021-2022)

Combined Planck + WMAP:

```
β = 0.33° ± 0.07°  (4.7σ from zero)
```

With systematic corrections:

```
β = 0.33° ± 0.067°  (4.9σ from zero)
```

### Tension with Z²

```
β_Z² = 0.00°
β_obs = 0.33°
σ_obs = 0.067°

Tension = |β_obs - β_Z²| / σ_obs = 0.33 / 0.067 = 4.9σ
```

This is close to the conventional 5σ threshold for discovery.

---

## Possible Resolutions

### Option 1: Systematic Error

The observed β could be due to:

1. **Miscalibration** of polarization angles
2. **Galactic foreground** contamination
3. **Instrumental polarization** rotation

**Status**: Minami & Komatsu carefully calibrated using:
- TB correlation (should be zero)
- Galactic foreground modeling
- Instrument systematics

They find systematics < 0.1°, insufficient to explain β = 0.33°.

### Option 2: Z² Requires Modification

If β ≠ 0 is real, Z² must be modified:

1. **Add orbifold with H¹ ≠ 0**: e.g., T³/Z₂ × S¹
2. **Include twisted sector axions**: Non-perturbative effects
3. **Higher-dimensional origin**: 10D → 7D with axion

This would represent a **significant change** to the framework.

### Option 3: Z² is Falsified

If LiteBIRD confirms β ≠ 0 at 5σ:

```
Z² framework in its current form is ruled out.
```

This is the most likely outcome given current data.

---

## Future Observations

### LiteBIRD (2028-2032)

| Parameter | Specification |
|-----------|---------------|
| Launch | 2028 |
| Mission duration | 3 years |
| Sensitivity σ(β) | ~0.01° |
| Systematic control | < 0.005° |

LiteBIRD will measure β to 0.01° precision.

### Decision Tree

```
LiteBIRD result:

If β = 0.00° ± 0.01°:
  → Z² CONFIRMED (current hint was systematic)
  → 33σ rejection of β = 0.33°

If β = 0.33° ± 0.01°:
  → Z² FALSIFIED at 33σ
  → Axionic physics required

If β = 0.15° ± 0.01°:
  → Partial agreement
  → Neither Z² nor current hint confirmed
```

### Timeline

```
2024-2025: Updated Planck PR4 analysis
2026-2027: ACT/SPT/BICEP combined analysis
2028:      LiteBIRD launch
2030-2032: LiteBIRD results
```

---

## Statistical Analysis

### Current Data Likelihood

```python
import numpy as np
from scipy import stats

# Observed
beta_obs = 0.33  # degrees
sigma_obs = 0.067  # degrees

# Z² prediction
beta_Z2 = 0.00

# Likelihood ratio
log_L_Z2 = stats.norm.logpdf(beta_obs, beta_Z2, sigma_obs)
log_L_free = stats.norm.logpdf(beta_obs, beta_obs, sigma_obs)  # MLE

delta_chi2 = -2 * (log_L_Z2 - log_L_free)
# delta_chi2 = (0.33/0.067)² = 24.3

p_value = stats.chi2.sf(delta_chi2, df=1)
# p_value = 8.2e-7

significance = stats.norm.isf(p_value/2)
# significance = 4.9σ
```

### Bayesian Analysis

```
Prior: β ∈ [-1°, +1°] (uniform)

P(Z²|data) ∝ P(data|β=0) × P(Z²)
P(alt|data) ∝ ∫ P(data|β) P(β) dβ

Bayes factor:
B = P(data|β=0) / P(data|β_free)
  = exp(-24.3/2) / 1
  ≈ 5 × 10⁻⁶

Strong evidence against Z²
```

---

## What Z² Would Need to Survive

If birefringence is real, Z² survives only if:

### Modified T³/Z₂

Replace T³/Z₂ with orbifold that has H¹ ≠ 0:

```
T³/Z₂ × S¹/Z₂  has  H¹ = ℝ

This admits axion with mass ~ 10⁻³² eV
giving β ~ 0.3° possible
```

**Cost**: Changes entire framework, loses predictive power

### Twisted Sector Contribution

Non-perturbative effects at orbifold fixed points might generate pseudo-axions:

```
φ_twisted ∝ Σ_i δ(y - y_i) × local operator
```

**Status**: Not yet calculated, may not give correct β

### Environmental Effect

Local matter could rotate polarization independently of cosmology:

```
β_local ≠ β_cosmological
```

**Status**: Would require explanation of apparent isotropy

---

## Comparison to Other Tests

### Relative Urgency

| Test | Tension | Z² Survival if Failed |
|------|---------|----------------------|
| Birefringence | **4.9σ** | Requires modification |
| Dark energy w | 2.5σ | Dead |
| GW h_× | Not tested | Dead |
| r value | Within range | Constrained |

Birefringence is the **most urgent** because:
1. Already at 4.9σ tension
2. Simple prediction (β = 0 exactly)
3. Clear falsification criterion

### If Birefringence Fails Z²

Other tests become moot - the framework would need fundamental revision before proceeding.

---

## Detailed Physics of Birefringence

### Axion-Photon Coupling

The Lagrangian for axion-photon interaction:

```
L = -¼ F_μν F^μν - ½ (∂φ)² - V(φ) - (g_aγ/4) φ F_μν F̃^μν
```

The birefringence angle is:

```
β = (g_aγ/2) Δφ

where Δφ = φ(z=0) - φ(z=1100) is the field change
```

For Z² with no axion: φ = 0 → β = 0.

### Why Axions Rotate Polarization

The F F̃ coupling modifies Maxwell's equations:

```
∂_μ F^μν = g_aγ (∂_μφ) F̃^μν
```

This gives different propagation speeds for left/right circular polarization:

```
n_L - n_R = g_aγ |∇φ| / ω
```

Integrated over the photon path → polarization rotation.

### Expected β from Various Models

| Model | Predicted β |
|-------|-------------|
| Z² | 0° exactly |
| QCD axion | < 0.001° |
| ALP (ultralight) | 0.1° - 1° |
| String axiverse | 0° - 2° |
| Early dark energy | ~0.3° |

The observed 0.33° is consistent with ultralight ALPs but not Z².

---

## Recommended Actions

### Immediate

1. **Monitor Planck PR4**: Updated analysis expected 2024-2025
2. **Request ACT/SPT data**: Independent confirmation
3. **Develop modification**: What would Z² + axion look like?

### Medium-term

1. **LiteBIRD proposal**: Ensure β measurement is prioritized
2. **Theory development**: Explore orbifold modifications
3. **Alternative explanations**: Search for systematics

### If β ≠ 0 Confirmed

1. **Acknowledge falsification**: Be honest about result
2. **Publish negative result**: Document the test
3. **Explore modifications**: What topology allows axions?

---

## Key Papers

### Observational

1. Minami & Komatsu (2020): "New Extraction of Cosmic Birefringence"
   - First significant detection
   - β = 0.35° ± 0.14°

2. Minami et al. (2022): "Simultaneous determination"
   - Updated with systematic control
   - β = 0.33° ± 0.067°

3. Diego-Palazuelos et al. (2022): "Cross-correlation"
   - Independent method confirmation
   - Consistent with 0.3°

### Theoretical

1. Carroll et al. (1990): "Limits on Lorentz-violating..."
   - Original prediction
   - Connected to axions

2. Marsh et al. (2023): "Axion Cosmology"
   - Theoretical framework
   - Ultralight ALP models

---

## Conclusion

The cosmic birefringence measurement represents the **most serious challenge** to the Z² framework:

- **Current data**: 4.9σ tension
- **Z² prediction**: β = 0 exactly (no modification possible within current framework)
- **LiteBIRD**: Will be definitive by 2032

**Honest assessment**: If the current β = 0.33° measurement is correct, Z² in its present form is likely falsified. This would be a significant negative result that constrains what topologies can describe our universe.

---

*Test 9 of 10 in Z² Experimental Program*
*CRITICAL: Most urgent constraint on framework*
*May 2026*
