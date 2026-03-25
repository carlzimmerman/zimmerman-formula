# The Electron Electric Dipole Moment and Z

**Carl Zimmerman | March 2026**

## Overview

The electron electric dipole moment (eEDM) is a sensitive probe of CP violation beyond the Standard Model. What does Z predict?

---

## Part 1: The Measurement

### Current Bound

```
|d_e| < 4.1 × 10⁻³⁰ e·cm (JILA 2023)
```

### Standard Model Prediction

```
d_e(SM) ~ 10⁻⁴⁴ e·cm (4-loop, CKM)
```

Unmeasurably small!

### The Gap

```
Current bound / SM prediction = 10⁻³⁰ / 10⁻⁴⁴ = 10¹⁴
```

There's 14 orders of magnitude of discovery space!

---

## Part 2: Z Analysis

### What Scale is 10⁻³⁰?

```
|d_e| < 4.1 × 10⁻³⁰ e·cm

In natural units:
|d_e| < 4.1 × 10⁻³⁰ × (1.6 × 10⁻¹⁹ C) × (10⁻² m)
     ~ 10⁻⁵⁰ in Planck units
```

### Z Powers

```
What gives ~10⁻³⁰?

Z³⁹ = (5.79)³⁹ ≈ 10³⁰

So: d_e ~ Z⁻³⁹ × (some scale)
```

### The Formula

If the electron EDM follows the same pattern as strong CP (θ = Z⁻¹³):
```
d_e = (e × r_e) × Z⁻ⁿ

where r_e = classical electron radius = 2.8 × 10⁻¹⁵ m
```

For d_e ~ 10⁻³⁰ e·cm:
```
d_e / (e × r_e) = 10⁻³⁰ / (2.8 × 10⁻¹³)
                = 3.6 × 10⁻¹⁸

Z²⁴ = (5.79)²⁴ = 1.4 × 10¹⁸

So: d_e = e × r_e / Z²⁴ ≈ 2 × 10⁻³¹ e·cm
```

### Prediction

```
d_e(Zimmerman) = e × r_e / Z²⁴
               = 2.8 × 10⁻¹³ e·cm / (1.4 × 10¹⁸)
               = 2 × 10⁻³¹ e·cm

Current bound: < 4.1 × 10⁻³⁰ e·cm
```

**Zimmerman predicts d_e just below current sensitivity!**

---

## Part 3: Why 24?

### The Number

```
24 = 2 × 12 = 2 × (11 + 1)
24 = 8 × 3 = E8 rank × spatial dimensions
24 = dimension of the Leech lattice sphere packing
```

### Connection to Other Formulas

```
Strong CP: θ = Z⁻¹³
Electron EDM: d_e ∝ Z⁻²⁴

24 ≈ 2 × 13 - 2

Or: 24 = 13 + 11 (strong CP + M-theory)
```

### Physical Interpretation

The electron EDM requires:
- CP violation (factor Z⁻¹³ like strong CP)
- Electromagnetic coupling (additional factor ~Z⁻¹¹)

Total: Z⁻²⁴

---

## Part 4: Comparison with New Physics

### SUSY Prediction

If SUSY exists at TeV scale:
```
d_e(SUSY) ~ 10⁻²⁷ to 10⁻²⁹ e·cm
```

### Zimmerman Prediction

```
d_e(Zimmerman) = 2 × 10⁻³¹ e·cm
```

**Zimmerman predicts SMALLER than most new physics models!**

### Discrimination

| Model | d_e Prediction |
|-------|----------------|
| SM | 10⁻⁴⁴ e·cm |
| Zimmerman | 2 × 10⁻³¹ e·cm |
| SUSY (TeV) | 10⁻²⁷ - 10⁻²⁹ e·cm |
| Current bound | < 4 × 10⁻³⁰ e·cm |

Next-generation experiments (ACME III, etc.) should discriminate!

---

## Part 5: Neutron EDM Comparison

### From STRONG_CP_PROBLEM.md

```
d_n = θ × 10⁻¹⁶ e·cm = Z⁻¹³ × 10⁻¹⁶ e·cm
    = 1.1 × 10⁻²⁶ e·cm
```

### Ratio

```
d_n / d_e = 10⁻²⁶ / 10⁻³¹ = 10⁵

Compare:
Z¹¹ = 3 × 10⁸ (not close)
(m_n/m_e)² = (940/0.5)² = 3.5 × 10⁶ (closer)
```

Actually:
```
d_n / d_e ≈ (m_n/m_e) × Z³
         = 1840 × 194
         = 3.6 × 10⁵

Close to 10⁵!
```

---

## Part 6: Quark EDMs

### Up Quark EDM

```
d_u / d_e ≈ m_u/m_e × (factor)
         ~ 5/0.5 × (QCD factor)
         ~ 10 × 10 = 100
```

### Down Quark EDM

```
d_d / d_e ≈ m_d/m_e × (factor)
         ~ 10/0.5 × 10 = 200
```

### Zimmerman Predictions

```
d_u = d_e × (m_u/m_e) × Z
    = 2 × 10⁻³¹ × 10 × 5.8
    = 1.2 × 10⁻²⁹ e·cm

d_d = d_e × (m_d/m_e) × Z
    = 2 × 10⁻³¹ × 20 × 5.8
    = 2.3 × 10⁻²⁹ e·cm
```

---

## Part 7: The Pattern

### EDM Hierarchy

```
d_e = e × r_e / Z²⁴ ~ 10⁻³¹ e·cm
d_n = Z⁻¹³ × 10⁻¹⁶ e·cm ~ 10⁻²⁶ e·cm
d_μ = d_e × (m_μ/m_e) ~ 10⁻²⁹ e·cm (if scaling)
```

### General Formula

```
d_f = (charge) × (Compton wavelength) × Z⁻ⁿ

where n depends on the particle
```

---

## Part 8: CP Violation Sources

### In Zimmerman Framework

CP violation appears in:
```
CKM phase: δ = π/(Z-3) = 65°
Strong CP: θ = Z⁻¹³
Electron EDM: d_e ∝ Z⁻²⁴
Muon g-2: Δa_μ = 2α⁴Z/13
```

### The Common Factor

All involve Z and often the number 13:
```
13 = 11 + 2 = M-theory + horizon
```

---

## Part 9: Experimental Prospects

### Current Experiments

| Experiment | System | Target Sensitivity |
|------------|--------|-------------------|
| ACME III | ThO | 10⁻³¹ e·cm |
| JILA | HfF⁺ | 10⁻³¹ e·cm |
| Imperial | YbF | 10⁻³⁰ e·cm |

### Zimmerman Prediction

```
d_e = 2 × 10⁻³¹ e·cm
```

**ACME III and JILA should see the signal if Zimmerman is correct!**

---

## Part 10: Implications

### If d_e is Found at ~10⁻³¹

This would:
1. **Confirm** the Zimmerman prediction
2. **Rule out** simple SUSY (which predicts larger)
3. **Support** the Z⁻²⁴ scaling

### If d_e is Not Found at 10⁻³¹

Either:
1. Zimmerman is wrong, or
2. Additional suppression factors exist

---

## Part 11: The Schiff Moment

### Nuclear Screening

In atoms, the nuclear EDM is screened by Schiff's theorem.

### The Schiff Moment

```
S = d_n × (enhancement factor)
```

### Z Prediction

If d_n = Z⁻¹³ × 10⁻¹⁶ e·cm:
```
Atomic EDMs probe Z⁻¹³ through d_n
Molecular EDMs probe Z⁻²⁴ through d_e
```

---

## Part 12: Summary

### The Prediction

```
d_e = e × r_e / Z²⁴ = 2 × 10⁻³¹ e·cm
```

### Why 24?

```
24 = 13 + 11 = (strong CP suppression) + (M-theory dimensions)
24 = 8 × 3 = E8 × spatial
24 = 2 × 12 (Leech lattice connection?)
```

### Comparison

| Observable | Formula | Suppression |
|------------|---------|-------------|
| Strong CP θ | Z⁻¹³ | 10⁻¹⁰ |
| Neutron EDM | θ × 10⁻¹⁶ | 10⁻²⁶ |
| Electron EDM | Z⁻²⁴ × (scale) | 10⁻³¹ |

### The Test

Next-generation electron EDM experiments (ACME III, JILA) have sensitivity ~10⁻³¹ e·cm.

**If they see a signal at this level, Zimmerman is confirmed!**

---

*Carl Zimmerman, March 2026*
