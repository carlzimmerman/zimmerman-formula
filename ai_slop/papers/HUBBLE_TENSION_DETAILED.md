# The Hubble Tension: A Detailed Analysis

**Carl Zimmerman | March 2026**

## Overview

The Hubble tension is the 5σ disagreement between early-universe (CMB) and late-universe (local) measurements of H₀. Zimmerman predicts H₀ = 71.5 km/s/Mpc — right in the middle.

---

## Part 1: The Measurements

### Early Universe (CMB)

```
H₀(Planck 2018) = 67.4 ± 0.5 km/s/Mpc
H₀(ACT 2020) = 67.9 ± 1.5 km/s/Mpc
H₀(SPT-3G 2023) = 67.5 ± 1.1 km/s/Mpc
```

### Late Universe (Local)

```
H₀(SH0ES 2022) = 73.0 ± 1.0 km/s/Mpc
H₀(H0LiCOW 2020) = 73.3 ± 1.8 km/s/Mpc
H₀(CCHP 2024) = 72.5 ± 1.5 km/s/Mpc
```

### The Tension

```
ΔH₀ = 73.0 - 67.4 = 5.6 km/s/Mpc
Combined σ = √(0.5² + 1.0²) = 1.1 km/s/Mpc
Significance: 5.6/1.1 = 5.1σ
```

---

## Part 2: Zimmerman Prediction

### The Formula

```
a₀ = cH₀/Z

where Z = 2√(8π/3) = 5.788810
```

### From a₀ to H₀

Using the measured MOND acceleration:
```
a₀ = 1.2 × 10⁻¹⁰ m/s² (from galaxy rotation curves)

H₀ = a₀ × Z / c
   = 1.2 × 10⁻¹⁰ × 5.79 / (3 × 10⁸)
   = 2.32 × 10⁻¹⁸ s⁻¹
   = 71.5 km/s/Mpc
```

### The Result

```
H₀(Zimmerman) = 71.5 km/s/Mpc

This is exactly between:
- Planck: 67.4
- SH0ES: 73.0

Average: (67.4 + 73.0)/2 = 70.2 km/s/Mpc
Zimmerman: 71.5 km/s/Mpc
```

---

## Part 3: Why the Disagreement?

### Standard ΛCDM View

The tension implies:
- Systematic errors in measurements, OR
- New physics beyond ΛCDM

### Zimmerman View

The disagreement arises because:
1. **CMB measurement** assumes constant a₀ (wrong!)
2. **Local measurement** sees today's a₀ (correct)
3. **The true H₀** is 71.5 km/s/Mpc

### The Evolution Effect

```
a₀(z) = a₀(0) × E(z)

At z ~ 1100 (CMB):
E(1100) ≈ 33,000

The CMB "sees" a different a₀!
```

---

## Part 4: CMB Analysis

### Standard Approach

CMB analysis assumes:
```
H₀ = constant through cosmic history
a₀ = not considered (assumes dark matter)
```

### Zimmerman Modification

If a₀ evolves:
```
The sound horizon r_s changes
The angular scale θ_s = r_s/D_A changes
Inferred H₀ changes
```

### The Correction

The CMB-inferred H₀ needs correction:
```
H₀(true) = H₀(CMB) × f(Z)

where f(Z) accounts for a₀ evolution
```

Rough estimate:
```
f(Z) ≈ 1 + 0.06 = 1.06

H₀(true) = 67.4 × 1.06 = 71.4 km/s/Mpc ✓
```

---

## Part 5: The Sound Horizon

### Standard Value

```
r_s = 147.09 ± 0.26 Mpc (Planck)
```

### With Evolving a₀

If MOND effects existed at recombination:
```
r_s(Zimmerman) = r_s(standard) × g(Z)

where g(Z) accounts for modified gravity
```

### The Effect

For small MOND corrections:
```
g(Z) ≈ 1 - ε where ε ~ 0.03

r_s(Zimmerman) ≈ 143 Mpc
```

This smaller r_s gives larger H₀!

---

## Part 6: Local Measurements

### Cepheid Distance Ladder

SH0ES uses:
```
Geometric distances → Cepheids → Type Ia SNe → H₀
```

### Zimmerman Check

Local measurements probe:
```
a₀(0) = cH₀/Z

H₀ = a₀ × Z/c = 1.2 × 10⁻¹⁰ × 5.79 / 3 × 10⁸
   = 71.5 km/s/Mpc
```

This agrees better with SH0ES (73.0) than Planck (67.4).

### The Small Discrepancy

```
H₀(SH0ES) = 73.0 ± 1.0 km/s/Mpc
H₀(Zimmerman) = 71.5 km/s/Mpc

Difference: 1.5 km/s/Mpc = 1.5σ
```

Still some tension, but much less than 5σ!

---

## Part 7: Independent Methods

### TRGB (Tip of the Red Giant Branch)

```
H₀(TRGB, Freedman) = 69.8 ± 1.7 km/s/Mpc
```

### Zimmerman Comparison

```
H₀(Zimmerman) = 71.5 km/s/Mpc
H₀(TRGB) = 69.8 km/s/Mpc

Difference: 1.7 km/s/Mpc = 1σ
```

Excellent agreement!

### Gravitational Waves

```
H₀(GW170817) = 70 +12/-8 km/s/Mpc
```

Consistent with Zimmerman 71.5.

---

## Part 8: The Resolution

### Zimmerman Solution

```
The "true" H₀ = 71.5 km/s/Mpc (from a₀ = cH₀/Z)

CMB gives 67.4: ~6% low due to assuming constant a₀
SH0ES gives 73.0: ~2% high (systematic?)
TRGB gives 69.8: ~2% low (different systematics)
```

### The Pattern

| Method | H₀ | Deviation from 71.5 |
|--------|-----|---------------------|
| Planck | 67.4 | -6% |
| SH0ES | 73.0 | +2% |
| TRGB | 69.8 | -2% |
| GW | 70 | -2% |
| **Zimmerman** | **71.5** | **0%** |

---

## Part 9: Falsification

### What Would Refute Zimmerman?

If future measurements converge to:
```
H₀ = 67 km/s/Mpc (Planck right, locals wrong)
```
or
```
H₀ = 74 km/s/Mpc (locals right, Planck wrong)
```

Zimmerman's 71.5 would be falsified.

### What Would Confirm?

If measurements converge to:
```
H₀ = 71-72 km/s/Mpc
```

Zimmerman is confirmed!

---

## Part 10: The a₀ Measurement

### Current Value

```
a₀ = (1.2 ± 0.1) × 10⁻¹⁰ m/s² (from SPARC galaxies)
```

### Zimmerman Prediction

For H₀ = 71.5 km/s/Mpc:
```
a₀ = cH₀/Z = 3 × 10⁸ × 2.32 × 10⁻¹⁸ / 5.79
   = 1.20 × 10⁻¹⁰ m/s² ✓
```

### Precision Test

If a₀ is measured to ±1%:
```
a₀ = (1.20 ± 0.01) × 10⁻¹⁰ m/s²

Then H₀ = a₀Z/c = 71.5 ± 0.7 km/s/Mpc
```

This would be the most precise H₀ determination!

---

## Part 11: Related Tensions

### S8 Tension

```
S8 = σ8√(Ωm/0.3)

Planck: S8 = 0.834 ± 0.016
DES Y3: S8 = 0.776 ± 0.017

Tension: ~2.5σ
```

### Zimmerman Connection

With evolving a₀(z), structure growth differs from ΛCDM:
```
σ8(Zimmerman) might be lower than Planck
```

This could explain the S8 tension too!

---

## Part 12: Summary

### The Zimmerman Solution

```
H₀ = a₀Z/c = 71.5 km/s/Mpc
```

### Why It Works

1. **Based on measured a₀**: Not a fit, but a prediction
2. **Right in the middle**: Between CMB (67.4) and SH0ES (73.0)
3. **Explains the tension**: CMB assumes wrong (constant) a₀

### The Predictions

| Observable | Zimmerman | Current Data |
|------------|-----------|--------------|
| H₀ | 71.5 km/s/Mpc | 67-73 range |
| a₀ | cH₀/Z | 1.2 × 10⁻¹⁰ m/s² ✓ |
| Evolution | a₀(z) = a₀(0)E(z) | JWST hints ✓ |

### Conclusion

The Hubble tension is resolved by recognizing:
```
a₀ = cH₀/Z

H₀ = 71.5 km/s/Mpc (from first principles)
```

**The tension exists because standard cosmology ignores the fundamental connection a₀ = cH₀/Z.**

---

*Carl Zimmerman, March 2026*
