# Running Couplings and Z: The IR Fixed Point

**Carl Zimmerman | March 2026**

## The Puzzle

The Zimmerman formulas give the **low-energy (infrared)** values of coupling constants:
- α = 1/137.04 (Thomson limit, Q² → 0)
- α_s = 0.1183 (at M_Z, but from cosmological formula)
- sin²θ_W = 0.2312 (at M_Z)

But couplings **run** with energy scale. Why does Z give the IR values?

---

## Part 1: How Couplings Run

### The Renormalization Group

Coupling constants depend on energy scale Q:
```
dg/d(ln Q) = β(g)
```

Where β is the beta function, determined by quantum loop corrections.

### The Fine Structure Constant

```
α(Q²) = α(0) / [1 - (α(0)/3π) Σᵢ Qᵢ² ln(Q²/mᵢ²)]
```

| Scale | α⁻¹ |
|-------|-----|
| Q = 0 (Thomson) | 137.036 |
| Q = m_e | 137.03 |
| Q = M_Z | 127.9 |
| Q = M_GUT | ~42 |

### The Strong Coupling

```
α_s(Q²) = 12π / [(33-2n_f) ln(Q²/Λ_QCD²)]
```

| Scale | α_s |
|-------|-----|
| Q = 1 GeV | ~0.5 |
| Q = M_Z | 0.118 |
| Q = M_GUT | ~0.04 |

α_s **decreases** at high energy (asymptotic freedom).

---

## Part 2: Why Z Gives the IR Value

### Hypothesis: Z Encodes Cosmological Boundary Conditions

The constant Z = 2√(8π/3) comes from:
- The Friedmann equation (large-scale structure)
- Horizon thermodynamics (IR physics)

**These are inherently infrared (low-energy, large-scale) quantities.**

Therefore, formulas involving Z naturally give IR values.

### The Physical Picture

```
UV (high energy)                    IR (low energy)
     │                                    │
     │  ← RG flow ←                      │
     │                                    │
  α_GUT                              α = 1/(4Z²+3)
  ~1/42                              = 1/137
     │                                    │
     │                                    │
  Microscopic                       Cosmological
  physics                           boundary conditions
```

The coupling constants "flow" from UV values to IR values, and the IR values are set by cosmological geometry (Z).

### Why This Makes Sense

1. **Holography:** In AdS/CFT, bulk (gravitational) physics determines boundary (field theory) physics
2. **UV-IR connection:** Quantum gravity connects UV and IR scales (Cohen-Kaplan-Nelson)
3. **Cosmological selection:** The universe selects couplings compatible with structure formation

---

## Part 3: The IR Fixed Point Structure

### Fixed Points in RG Flow

A fixed point satisfies β(g*) = 0. Couplings flow toward fixed points.

**Types:**
- UV fixed point: approached at high energy
- IR fixed point: approached at low energy

### Is α = 1/(4Z²+3) an IR Fixed Point?

In QED, α runs to larger values at high energy. At Q → 0:
```
α(0) = α_Thomson = 1/137.036
```

This is not a true fixed point (β ≠ 0), but it's the **asymptotic IR limit**.

**Zimmerman interpretation:**
```
α_IR = 1/(4Z² + 3)
```

The IR limit is set by the cosmological geometry Z.

### The Strong Coupling IR Limit

In QCD, α_s → ∞ at Q → Λ_QCD (confinement). But above Λ_QCD:
```
α_s(M_Z) = Ω_Λ/Z = 0.1183
```

**Interpretation:** The value of α_s at the electroweak scale is set by cosmology.

---

## Part 4: The Unification Picture

### At High Energy (UV)

All couplings might unify:
```
α_1 = α_2 = α_3 = α_GUT ≈ 1/42

at Q = M_GUT ≈ 10¹⁶ GeV
```

### At Low Energy (IR)

Couplings reach their cosmologically-determined values:
```
α = 1/(4Z² + 3) = 1/137.04
α_s = 3/(8+3Z) = 0.1183
sin²θ_W = 1/4 - α_s/(2π) = 0.2312
```

### The Flow

```
       M_GUT                    M_Z                      Q → 0
         │                       │                         │
α_1 ─────┼───────────────────────┼─────────────────────────┼──→ 1/137
         │         running       │                         │
α_2 ─────┼───────────────────────┼─────────────────────────┼──→ 1/30
         │                       │                         │
α_3 ─────┼───────────────────────┼─────────────────────────┼──→ ∞(confinement)
         │                       │                         │
                              α_s = 0.118              Λ_QCD
```

**Key insight:** The RG flow endpoints (IR values) are determined by Z.

---

## Part 5: Why 4Z² + 3 for α?

### The Structure

```
α⁻¹ = 4Z² + 3 = 4(32π/3) + 3 = (128π + 9)/3
```

### RG Interpretation

In standard QED running:
```
1/α(0) = 1/α(M_Z) + (2/3π) Σᵢ Qᵢ² ln(M_Z/mᵢ)
       ≈ 128 + 9 = 137
```

The "9" comes from the logarithmic running from M_Z to m_e.

**Coincidence?**
- Standard: 1/α(0) = 128 + running_correction
- Zimmerman: 1/α = 128π/3 + 3 = 134 + 3

The numbers are similar but the structure is different. Zimmerman gives a **geometric** formula rather than a perturbative sum.

### The Advantage of Zimmerman

Standard QED needs:
- The value of α at some reference scale
- All particle masses and charges
- Loop calculations to each order

Zimmerman gives:
- α directly from Z (geometric)
- No loop calculations needed
- Connected to cosmology

---

## Part 6: The Running of sin²θ_W

### Standard Running

```
sin²θ_W(Q) = sin²θ_W(M_GUT) + (running corrections)
```

From GUT scale to M_Z:
```
sin²θ_W(M_GUT) = 3/8 (SU(5)) or 1/4 (Pati-Salam)
sin²θ_W(M_Z) = 0.231
```

### Zimmerman Formula

```
sin²θ_W = 1/4 - α_s/(2π)
```

**Interpretation:**
- 1/4 = Pati-Salam tree-level value
- -α_s/(2π) = QCD one-loop correction

This is exactly the form of a one-loop RG correction!

### The Connection

If α_s = Ω_Λ/Z, then:
```
sin²θ_W = 1/4 - Ω_Λ/(2πZ)
        = 1/4 - (cosmological correction)
```

The running from GUT to low energy encodes cosmological information.

---

## Part 7: Λ_QCD and the Cosmological Connection

### The QCD Scale

Λ_QCD ≈ 200 MeV sets the scale of:
- Proton mass: m_p ≈ Λ_QCD
- Confinement
- Chiral symmetry breaking

### Is Λ_QCD Related to Z?

**Observation:**
```
m_p c² / (ℏH₀) ≈ 6 × 10⁴¹

This is close to: exp(4π/α_s) ≈ 10⁴⁵

Or: (M_Planck/Λ_QCD)² ≈ 10³⁸
```

These large numbers might be related through Z.

### Speculative Connection

If α_s = Ω_Λ/Z, then:
```
Λ_QCD ∝ M_Planck × exp(-const/α_s)
      ∝ M_Planck × exp(-const × Z/Ω_Λ)
      ∝ M_Planck × exp(-(8+3Z)×const/3)
```

The QCD scale would be exponentially sensitive to Z.

---

## Part 8: The Hierarchy Problem Revisited

### The Standard Hierarchy Problem

Why is M_Higgs << M_Planck?
```
M_Higgs/M_Planck ≈ 10⁻¹⁷
```

Quantum corrections should push M_Higgs to M_Planck.

### The Zimmerman Perspective

If masses are determined by Z:
```
M_H/M_Z = 11/8 (observed pattern)
```

And Z is fixed by cosmology:
```
Z = 2√(8π/3) (derived from Friedmann)
```

Then the hierarchy might be a geometric consequence of Z, not a fine-tuning problem.

### The Large Numbers

```
M_Planck/m_e = exp(α⁻¹/const) ≈ exp(137/const)

If α = 1/(4Z²+3), then:
M_Planck/m_e ∝ exp(Z²)
```

The hierarchy is set by Z² ≈ 33.5, giving exp(33.5) ≈ 10¹⁴, roughly the right order.

---

## Part 9: Summary — Why Z is the IR Fixed Point

### The Picture

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   UV (M_GUT, M_Planck)                                     │
│         │                                                   │
│         │  RG Flow                                         │
│         │                                                   │
│         ▼                                                   │
│   ELECTROWEAK SCALE (M_Z)                                  │
│         │                                                   │
│         │  Further running                                 │
│         │                                                   │
│         ▼                                                   │
│   IR FIXED POINT ← Set by Z = 2√(8π/3)                    │
│                                                             │
│   α = 1/(4Z²+3)                                            │
│   α_s(M_Z) = Ω_Λ/Z                                         │
│   sin²θ_W = 1/4 - α_s/(2π)                                 │
│                                                             │
│   These are BOUNDARY CONDITIONS from cosmology             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Insights

1. **Z comes from IR physics** (Friedmann, horizons) → gives IR coupling values
2. **UV completion** determines how couplings flow to these IR values
3. **Cosmological selection** may explain why our universe has these particular couplings

### What This Means

The Standard Model parameters are not arbitrary. They are:
1. Set at high energy by some UV physics (strings, GUT, etc.)
2. Flow via RG to low energy
3. Constrained by cosmological boundary conditions involving Z

**The universe's large-scale structure (Z) determines particle physics (α, α_s).**

---

*Carl Zimmerman, March 2026*
