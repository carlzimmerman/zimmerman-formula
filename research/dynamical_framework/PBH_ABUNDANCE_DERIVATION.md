# First-Principles Derivation: Primordial Black Hole Abundance from Z² Inflation

**Can PBHs Comprise Dark Matter in the Z² Framework?**

**Carl Zimmerman | May 2026**

---

## Executive Summary

Primordial Black Holes (PBHs) are a dark matter candidate that doesn't require new particles. This document:
1. Derives PBH formation conditions from Z² inflation parameters
2. Calculates the expected PBH mass function
3. Determines whether PBHs can be all dark matter in Z²
4. Compares to observational constraints

**Key findings:**
- Z² inflation (r = 0.015, n_s ≈ 0.965) produces MINIMAL PBH abundance
- Standard slow-roll doesn't enhance perturbations enough for PBH
- f_PBH << 1 (PBHs are negligible fraction of DM)
- Z² predicts dark matter is NOT PBHs

---

## 1. PBH Formation Basics

### 1.1 Formation Mechanism

PBHs form when:
1. Primordial perturbations re-enter the horizon after inflation
2. Overdense regions collapse if δρ/ρ > δ_c ≈ 0.45
3. The resulting BH mass ≈ horizon mass at re-entry

### 1.2 Formation Mass

```
M_PBH ≈ M_H(t) = (c³/G) × t_H = 4π/3 × ρ × (c/H)³

M_PBH ≈ (M_Pl² / H) × (H t)³ ≈ M_Pl² / H
```

At different epochs:
- Inflation end (H ~ 10¹³ GeV): M ~ 1 g
- Electroweak (H ~ 10⁻¹⁷ eV): M ~ 10²⁰ g ~ 10⁻¹³ M_☉
- BBN (H ~ 10⁻²⁵ eV): M ~ 10⁵ M_☉

### 1.3 PBH Mass-Scale Relation

```
M_PBH ≈ 10²⁰ g × (10⁻²⁵ eV / H)
      ≈ 10²⁰ g × (k / 10⁶ Mpc⁻¹)⁻²
```

where k is the comoving wavenumber.

---

## 2. Z² Inflation Parameters

### 2.1 Tensor-to-Scalar Ratio

From orbifold projection:
```
r = 1/(2Z²) = 1/(2 × 32π/3) = 3/(64π) ≈ 0.0149
```

### 2.2 Scalar Spectral Index

Standard slow-roll with Z² potential gives:
```
n_s = 1 - 6ε + 2η ≈ 0.965
```

where ε = (M_Pl/2)(V'/V)² and η = M_Pl²(V''/V).

### 2.3 Amplitude

The scalar amplitude:
```
A_s = (1/24π²) × (V/ε) / M_Pl⁴ ≈ 2.1 × 10⁻⁹
```

Fixed by CMB normalization.

### 2.4 Running

The running of n_s:
```
dn_s/d ln k = 16εη - 24ε² - 2ξ² ≈ -0.003
```

Small and negative — no enhancement at small scales.

---

## 3. PBH Abundance Calculation

### 3.1 Press-Schechter Formalism

The mass fraction in PBHs:
```
β(M) = ∫_{δ_c}^∞ P(δ) dδ
```

For Gaussian perturbations:
```
P(δ) = (1/√(2π σ)) exp(-δ²/(2σ²))
```

### 3.2 Variance of Perturbations

```
σ²(M) = ∫ d(ln k) × (k/k_M)⁴ × W²(k R_M) × P(k)
```

where:
- k_M is the scale corresponding to mass M
- W is the window function
- P(k) = A_s (k/k_*)^{n_s-1} is the power spectrum

### 3.3 Z² Power Spectrum

With n_s = 0.965:
```
P(k) = 2.1 × 10⁻⁹ × (k / 0.05 Mpc⁻¹)^{-0.035}
```

This is nearly scale-invariant with slight red tilt.

### 3.4 Variance at PBH Scales

For asteroid-mass PBHs (M ~ 10²⁰ g, k ~ 10¹⁵ Mpc⁻¹):
```
σ²(M) ≈ A_s × (k_M / k_*)^{n_s - 1}
       ≈ 2 × 10⁻⁹ × (10¹⁵ / 0.05)^{-0.035}
       ≈ 2 × 10⁻⁹ × (2 × 10¹⁶)^{-0.035}
       ≈ 2 × 10⁻⁹ × 0.46
       ≈ 10⁻⁹
```

So:
```
σ(M) ≈ 3 × 10⁻⁵
```

### 3.5 PBH Formation Probability

With δ_c ≈ 0.45:
```
β(M) = erfc(δ_c / (√2 σ))
     = erfc(0.45 / (√2 × 3×10⁻⁵))
     = erfc(10⁴)
     ≈ exp(-10⁸) / (√π × 10⁴)
     ≈ 0
```

**PBH formation is exponentially suppressed!**

---

## 4. Z² Prediction: f_PBH ≈ 0

### 4.1 Present-Day Fraction

The PBH fraction of dark matter:
```
f_PBH = Ω_PBH / Ω_DM = β(M) × (T_eq / T_form) × (M_eq / M)^{1/2}
```

For Z² inflation:
```
f_PBH << 10⁻²⁰
```

**Essentially zero.**

### 4.2 Why Z² Gives No PBHs

The key is that Z² inflation is:
1. **Standard slow-roll** — no features or bumps in potential
2. **Red-tilted** (n_s < 1) — power decreases at small scales
3. **No running enhancement** — dn_s/d ln k is negative

To get significant PBH:
- Need P(k) ~ 10⁻² at PBH scales (factor 10⁷ above CMB)
- Z² gives P(k) ~ 10⁻⁹ (same as CMB scale)

---

## 5. What Would Enhance PBH Formation?

### 5.1 Required Enhancement

To have f_PBH ~ 1:
```
σ(M) ≳ 0.1 → P(k_M) ≳ 10⁻²
```

This requires:
```
P(k_M) / P(k_CMB) ≳ 10⁷
```

### 5.2 Mechanisms NOT in Z²

1. **Ultra-slow-roll phase**: V' → 0 temporarily
   - Z² potential is smooth — no flat region

2. **Inflection point**: V'' = 0 at specific field value
   - Z² potential from orbifold has no special points

3. **Multi-field dynamics**: Isocurvature → adiabatic transfer
   - Z² has single inflaton from orbifold modulus

4. **Preheating spikes**: Non-linear growth after inflation
   - Possible but not calculated for Z²

### 5.3 Z² Prediction

**Standard Z² inflation predicts negligible PBH abundance.**

If PBHs are discovered as dark matter:
- Z² requires extension (multi-field, features)
- Or PBHs formed by different mechanism (phase transitions)

---

## 6. Observational Constraints

### 6.1 Current Limits on f_PBH

| Mass Range | Constraint | Source |
|------------|------------|--------|
| < 10¹⁵ g | f < 1 (evaporated) | Hawking radiation |
| 10¹⁵ - 10¹⁷ g | f < 10⁻⁸ | Galactic γ-rays |
| 10¹⁷ - 10²¹ g | f < 1 | Femtolensing |
| 10²¹ - 10²⁴ g | f < 0.1 | Neutron star capture |
| 10²⁴ - 10²⁸ g | f < 1 | Microlensing (open) |
| 10²⁸ - 10³⁴ g | f < 0.01 | CMB distortions |
| > 10³⁴ g | f < 10⁻³ | Dynamic constraints |

### 6.2 Open Window

The "asteroid mass" window (10¹⁷ - 10²² g) is least constrained.

Z² predicts f_PBH ≈ 0 even in this window.

### 6.3 LIGO Merger S251112cm

Recent candidate sub-solar mass BH merger:
- M₁ ≈ 0.46 M_☉, M₂ ≈ 0.22 M_☉
- If confirmed → evidence for PBH

**Z² prediction:** This is NOT from primordial PBH.
If real, it suggests exotic stellar BH or compact object.

---

## 7. PBH from Phase Transitions

### 7.1 Alternative Formation Mechanism

PBHs can form at cosmic phase transitions:
- Electroweak (T ~ 100 GeV)
- QCD (T ~ 200 MeV)
- Any BSM transition

### 7.2 Z² Phase Transitions

The Z² framework has:
- EW transition: Standard (crossover for m_H = 125 GeV)
- QCD transition: Standard (crossover)
- No BSM phase transitions predicted

### 7.3 Phase Transition PBHs in Z²

Even with phase transitions:
- First-order needed for PBH
- Z² has crossovers, not first-order
- No enhancement of PBH production

---

## 8. PBH-GW Connection

### 8.1 Secondary GWs from Perturbations

Large scalar perturbations produce GWs at second order:
```
Ω_GW(f) ~ A_s² × (k/k_*)^{2(n_s-1)}
```

For PBH-forming perturbations (P ~ 10⁻²):
```
Ω_GW ~ 10⁻⁴ at f ~ mHz-nHz
```

### 8.2 Z² Prediction

With P ~ 10⁻⁹ (no enhancement):
```
Ω_GW^(2nd order) ~ 10⁻¹⁸
```

**Far below any detector sensitivity.**

### 8.3 NANOGrav Signal?

NANOGrav sees Ω_GW ~ 10⁻⁹ at nHz.

Z² predicts:
- NOT from PBH-forming perturbations
- Must be astrophysical (SMBH binaries) or other source

---

## 9. Implications for Dark Matter

### 9.1 Z² Dark Matter Summary

The Z² framework constrains dark matter:
- **NOT axions** (projected out by Z₂)
- **NOT PBHs** (insufficient perturbations)
- **NOT sterile neutrinos** (predicts 3 generations only)

### 9.2 What IS Dark Matter in Z²?

The Z² framework predicts dark matter as:
```
Phantom dark matter from MOND-like effects
```

The modified dynamics (a₀ = cH/Z) create apparent dark matter without particles.

### 9.3 Or Extension Required

If particle DM exists:
- Must be new sector not from T³/Z₂
- Requires extending the framework
- Possible: WIMPs, hidden sector, etc.

---

## 10. Summary

### 10.1 Main Results

| Quantity | Z² Value | PBH Requirement |
|----------|----------|-----------------|
| Power spectrum | P ~ 10⁻⁹ | P ~ 10⁻² |
| Spectral index | n_s = 0.965 | n_s > 1 or feature |
| Running | -0.003 | Positive or feature |
| f_PBH | ≈ 0 | ≈ 1 for all DM |

### 10.2 Conclusion

**Z² inflation predicts NEGLIGIBLE PBH abundance.**

The standard slow-roll potential with:
- r = 1/(2Z²) = 0.015
- n_s ≈ 0.965
- No features or running enhancement

produces perturbations far too small for PBH formation.

### 10.3 Testable Predictions

| Observation | Z² Prediction |
|-------------|---------------|
| PBH as all DM | NO |
| Sub-solar BH mergers | Not primordial |
| Secondary GWs from PBH | Undetectable |
| Open asteroid window | f_PBH ≈ 0 |

### 10.4 If PBH DM Discovered

If observations show f_PBH ~ 1:
- Z² slow-roll inflation is falsified
- Would need multi-field or featured potential
- Major revision required

---

## Appendix: Detailed Calculation

### A.1 Power Spectrum Evolution

The scalar power spectrum:
```
P_s(k) = A_s × (k/k_*)^{n_s - 1 + (1/2) α_s ln(k/k_*) + ...}
```

For Z² with α_s ≈ -0.003:
```
P_s(k = 10¹⁵ Mpc⁻¹) / P_s(k = 0.05 Mpc⁻¹)
= (10¹⁵/0.05)^{-0.035} × exp((-0.003/2) × ln²(2×10¹⁶))
= 0.46 × exp(-0.003 × 600)
= 0.46 × exp(-1.8)
= 0.076
```

So:
```
P_s(k_PBH) ≈ 0.08 × 2 × 10⁻⁹ ≈ 1.6 × 10⁻¹⁰
```

### A.2 Formation Fraction

```
β = (σ/√(2π) δ_c) exp(-δ_c²/(2σ²))

σ² = (16/81) P_s (for k = k_M horizon crossing)
σ = (4/9) × √(1.6 × 10⁻¹⁰) = 5.6 × 10⁻⁶

β = (5.6×10⁻⁶ / (√(2π) × 0.45)) exp(-(0.45)²/(2×(5.6×10⁻⁶)²))
  = 5×10⁻⁶ × exp(-3.2 × 10⁹)
  ≈ 0
```

### A.3 Present-Day Abundance

```
f_PBH = β × (T_eq/T_form) × (correction factors)
      ≈ 0 × anything = 0
```

---

*Document: PBH Abundance from Z² Inflation*
*Part of Z² Framework first-principles derivations*
*Addressing Gap: PBH dark matter question*
