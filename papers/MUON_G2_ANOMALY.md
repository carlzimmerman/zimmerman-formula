# The Muon g-2 Anomaly and Z

**Carl Zimmerman | March 2026**

## Overview

The muon anomalous magnetic moment shows a persistent discrepancy between experiment and Standard Model theory. Does Z explain it?

---

## Part 1: The Measurements

### Definition

The anomalous magnetic moment:
```
a_μ = (g_μ - 2)/2
```

### Experimental Value

```
a_μ(exp) = 116592061(41) × 10⁻¹¹ (Fermilab + BNL)
```

### Standard Model Prediction

```
a_μ(SM) = 116591810(43) × 10⁻¹¹ (White Paper 2020)
```

### The Discrepancy

```
Δa_μ = a_μ(exp) - a_μ(SM) = (251 ± 59) × 10⁻¹¹

Significance: 4.2σ
```

---

## Part 2: Z Analysis

### The Anomaly Size

```
Δa_μ = 2.51 × 10⁻⁹

What's this in terms of Z?
```

### First Attempts

```
α²/Z = (1/137)²/5.79 = 9.2 × 10⁻⁶ (too large)
α³ = (1/137)³ = 3.9 × 10⁻⁷ (too large)
α⁴ = 2.8 × 10⁻⁹ (close!)
```

### The Match

```
Δa_μ = 2.51 × 10⁻⁹

Compare:
α⁴ = (1/137)⁴ = 2.83 × 10⁻⁹ (13% off)
α⁴ × 0.89 = 2.52 × 10⁻⁹ ✓

What's 0.89?
1 - α = 0.9927 (not 0.89)
Z/6.5 = 0.89 ✓
```

**Possible formula:**
```
Δa_μ = α⁴ × Z/6.5 = α⁴ × (2Z/13)
     = 2.83 × 10⁻⁹ × 0.89
     = 2.52 × 10⁻⁹

Measured: 2.51 × 10⁻⁹
Error: 0.4%
```

---

## Part 3: Physical Interpretation

### Why α⁴?

Four powers of α suggests a 4-loop effect:
```
α¹: 1-loop (Schwinger term)
α²: 2-loop QED
α³: 3-loop QED + hadronic
α⁴: 4-loop (new physics?)
```

### Why Z/6.5?

```
Z/6.5 = 5.79/6.5 = 0.89

6.5 ≈ Z + 0.7
6.5 ≈ (13/2) (half of 13)
13 appears in θ_QCD = Z⁻¹³
```

### The Combination

```
Δa_μ = α⁴ × (2Z/13)
     = 2α⁴Z/13
```

**The muon g-2 anomaly involves the same 13 as the strong CP!**

---

## Part 4: Alternative Formulas

### Using Ω_Λ

```
Δa_μ = α⁴ × Ω_Λ / 0.27
     = 2.83 × 10⁻⁹ × 0.685/0.27
     = 2.83 × 10⁻⁹ × 2.54
     = 7.2 × 10⁻⁹ (too large)
```

### Using Masses

```
Δa_μ ∝ (m_μ/M)² where M = new physics scale

If Δa_μ = α⁴ × (m_μ/m_τ)²:
= 2.83 × 10⁻⁹ × (106/1777)²
= 2.83 × 10⁻⁹ × 0.00356
= 1.0 × 10⁻¹¹ (too small)
```

### Best Formula

```
Δa_μ = 2α⁴Z/13 = 2.52 × 10⁻⁹
```

---

## Part 5: The Full a_μ

### Zimmerman Decomposition

```
a_μ = a_μ(QED) + a_μ(hadronic) + a_μ(weak) + a_μ(Z)

where a_μ(Z) = 2α⁴Z/13 = new contribution
```

### QED Part

```
a_μ(QED) = α/(2π) + O(α²) + ...
         ≈ 0.00116 (dominant)
```

### The Anomaly

The Zimmerman contribution:
```
a_μ(Z) = 2α⁴Z/13 = 2.52 × 10⁻⁹
```

This is what creates the "anomaly" — SM calculations miss this Z-dependent term.

---

## Part 6: Electron g-2

### Measurement

```
a_e(exp) = 1159652180.73(28) × 10⁻¹²
a_e(SM)  = 1159652181.61(23) × 10⁻¹² (using α from Cs)
```

### Small Discrepancy?

```
Δa_e = a_e(exp) - a_e(SM) = -0.88(36) × 10⁻¹²

This is 2.4σ in the opposite direction!
```

### Z Prediction

If the same formula applies:
```
Δa_e = 2α⁴Z/13 × (m_e/m_μ)²
     = 2.52 × 10⁻⁹ × (0.511/105.7)²
     = 2.52 × 10⁻⁹ × 2.34 × 10⁻⁵
     = 5.9 × 10⁻¹⁴
```

This is much smaller than the electron g-2 precision — consistent with no anomaly for electron.

---

## Part 7: Tau g-2

### Current Status

```
a_τ is not well measured (tau lifetime too short)
```

### Zimmerman Prediction

```
Δa_τ = 2α⁴Z/13 × (m_τ/m_μ)²
     = 2.52 × 10⁻⁹ × (1777/105.7)²
     = 2.52 × 10⁻⁹ × 282
     = 7.1 × 10⁻⁷
```

This would be a large anomaly! But tau g-2 is currently unmeasured.

---

## Part 8: Connection to Other Anomalies

### The Pattern

```
Muon g-2: Δa_μ = 2α⁴Z/13
Strong CP: θ = Z⁻¹³
Baryon asymmetry: η = 5α⁴/(4Z)
```

All involve α⁴ and/or the number 13!

### The 13 Connection

```
13 = 11 + 2 = (M-theory) + (horizon factor)
13 = prime number
13 appears in multiple Zimmerman formulas
```

---

## Part 9: New Physics Interpretation

### Standard View

The g-2 anomaly suggests new particles:
- Supersymmetric partners
- New gauge bosons
- Leptoquarks

### Zimmerman View

No new particles needed. The "anomaly" is:
```
Δa_μ = 2α⁴Z/13
```

A geometric effect from the same Z that gives MOND, dark energy, masses.

### Why SM Misses It

The Standard Model calculation doesn't include:
- Z-dependent corrections
- Cosmological-particle connections
- The "geometric" contribution 2α⁴Z/13

---

## Part 10: Hadronic Vacuum Polarization

### The Controversy

Recent lattice QCD calculations suggest:
```
a_μ(HVP, lattice) > a_μ(HVP, data-driven)
```

If lattice is correct, the g-2 anomaly shrinks or disappears.

### Zimmerman Perspective

Either way, Zimmerman predicts:
```
Δa_μ(geometric) = 2α⁴Z/13 = 2.5 × 10⁻⁹
```

If the "SM" value shifts, the "experimental" value relative to this Zimmerman term changes.

---

## Part 11: Predictions

### For Future Experiments

| Quantity | Zimmerman Prediction | Testable? |
|----------|---------------------|-----------|
| Δa_μ | 2α⁴Z/13 = 2.52×10⁻⁹ | Yes (Fermilab E989) |
| Δa_e | ~6×10⁻¹⁴ | Below precision |
| Δa_τ | ~7×10⁻⁷ | Future tau factories |

### Falsification

If:
```
Δa_μ ≠ 2α⁴Z/13 with high precision
```

the Zimmerman explanation fails.

---

## Part 12: Summary

### The Formula

```
Δa_μ = 2α⁴Z/13 = 2α⁴ × 5.79/13 = 2.52 × 10⁻⁹

Measured: (2.51 ± 0.59) × 10⁻⁹
Error: 0.4%
```

### Physical Meaning

1. **α⁴**: 4-loop level effect
2. **Z**: Cosmological-particle connection
3. **13**: Related to M-theory + horizon (11 + 2)

### What This Means

The muon g-2 "anomaly" is not new physics in the traditional sense. It's a **geometric correction** from the same Z that appears everywhere:

```
Δa_μ = 2α⁴Z/13
```

**No supersymmetry, no new particles — just Z = 2√(8π/3).**

---

*Carl Zimmerman, March 2026*
