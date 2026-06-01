# Derivation Attempts for the Fine Structure Constant

**Carl Zimmerman | March 2026**

## The Formula

```
α = 1/(4Z² + 3) = 1/137.04

Measured: α = 1/137.035999... (0.004% error)
```

## The Mathematical Structure

```
α⁻¹ = 4Z² + 3

With Z² = 4 × (8π/3) = 32π/3:

α⁻¹ = 4 × 32π/3 + 3 = 128π/3 + 3 = (128π + 9)/3 = 137.04
```

**Notable:** 128 = 2⁷

---

## Approach 1: Dimensional Decomposition

### The Components

```
α⁻¹ = 4 × Z² + 3
```

| Component | Value | Physical Interpretation |
|-----------|-------|------------------------|
| **4** | 4 | Spacetime dimensions |
| **Z²** | 32π/3 | Gravitational geometry squared |
| **3** | 3 | ? |

### What Could 3 Represent?

**Option A: Spatial dimensions**
- 3 spatial + 1 time = 4 spacetime
- The "3" is the spatial part

**Option B: SU(2) generators**
- SU(2)_L has 3 generators (W¹, W², W³)
- The photon emerges from electroweak mixing

**Option C: Fermion generations**
- 3 generations of fermions
- Related to flavor structure

**Option D: Color**
- SU(3)_C has 3 colors
- But photon doesn't couple to color directly

**Most Likely:** SU(2) generators, since the photon emerges from electroweak symmetry breaking.

---

## Approach 2: Kaluza-Klein Compactification

### The Basic Idea

In Kaluza-Klein theory, the electromagnetic coupling emerges from geometry:
```
α = (compactification radius)² / (Planck length)²
```

Or equivalently:
```
α⁻¹ = V_internal / V_Planck
```

### Application

If the "internal volume" in Planck units is:
```
V_internal = 4Z² + 3 = 137
```

Then α = 1/V_internal.

### What Manifold Has Volume 4Z² + 3?

**Hypothesis:** The internal manifold is a product:
```
M_internal = S⁴ × S³ / discrete group
```

Where:
- S⁴ contributes 4Z² (4D sphere with radius ∝ Z)
- S³ contributes 3 (3D sphere with unit radius)

The division by a discrete group could normalize the volumes.

---

## Approach 3: Information-Theoretic

### The Formula as Information Count

```
α⁻¹ = N_spacetime × I_geometry + N_gauge
```

Where:
- N_spacetime = 4 (spacetime DoF)
- I_geometry = Z² (information per dimension from Friedmann geometry)
- N_gauge = 3 (SU(2) generators)

### Interpretation

The electromagnetic coupling represents the total "information capacity" of:
- 4 spacetime dimensions
- Each containing Z² bits of cosmological information
- Plus 3 internal gauge DoF

---

## Approach 4: E8 Connection

### The Number 128

```
α⁻¹ = (128π + 9)/3
```

128 = 2⁷ is significant in E8:
- E8 = SO(16) ⊕ 128 (adjoint representation decomposition)
- 128 is the dimension of the spinor representation of SO(16)

### E8 × E8 Structure

In heterotic string theory:
- Gauge group: E8 × E8
- Each E8 has 248 generators
- 248 = 120 + 128 (SO(16) + spinor)

**Hypothesis:** The 128π in α⁻¹ comes from the spinor sector of E8.

### The Factor of 3

The "+3" could come from:
- 3 generations (related to compactification)
- SU(2) (weak force, 3 generators)
- The division by 3 in (128π + 9)/3

---

## Approach 5: Running Coupling Analysis

### The Problem

The fine structure constant **runs** with energy:

| Scale | α⁻¹ |
|-------|-----|
| Thomson (0) | 137.04 (our formula) |
| M_Z | 128 |
| M_GUT | ~42 |

Our formula gives the **low-energy limit**.

### Why the IR Value?

**Hypothesis:** The formula α = 1/(4Z² + 3) represents the IR fixed point because:

1. **Z is cosmological:** Z comes from Friedmann equation, which describes the IR (large-scale) structure

2. **Maximum information:** At low energies, the electromagnetic field stores maximum information (137 bits per quantum)

3. **Ground state:** 137 is the "ground state" coupling; high-energy values are excited states

### The Running Equation

Standard QED running:
```
1/α(μ) = 1/α(0) + (2/3π) × N_f × ln(μ/m_e)
```

Where N_f is the number of light fermion species.

At μ = M_Z with appropriate fermion counting:
```
1/α(M_Z) ≈ 137 - 9 = 128 ✓
```

The "-9" comes from fermion loops. Note: 9 = 3² (generations squared?).

---

## Approach 6: Comparison to Historical Attempts

### Wyler (1969)

```
α⁻¹ = (9/8π⁴) × (π⁵/2⁴·5!) × (8π²/4!)² = 137.0361
```

Accuracy: 0.0001%

Based on: Volume ratios in projective geometry.

### Eddington

```
α⁻¹ = 137 (exactly, or later 136)
```

Based on: Number of independent spinor components in his "fundamental theory."

### Zimmerman (This Work)

```
α⁻¹ = 4Z² + 3 = 137.04
```

Accuracy: 0.004%

Based on: Cosmological geometry (Z from Friedmann + thermodynamics).

**Advantage over Wyler:** Zimmerman formula connects to other constants (Ω_Λ, α_s, lepton masses) through Z.

---

## Approach 7: The Full Structure

### All Terms Involving Z

```
α⁻¹ = 4Z² + 3 = 4(32π/3) + 3 = (128π + 9)/3
```

Breaking this down:
```
128π/3 = 4 × 32π/3 = 4 × Z²

where Z² = 32π/3 = (2)² × (8π/3)
                  = 4 × (8π/3)
```

The factor 8π/3 is from Friedmann: ρ_c = 3H²/(8πG).

### The Architecture

```
FRIEDMANN: 8π/3
     ↓
Z² = 4 × (8π/3) = 32π/3
     ↓
4Z² = 16 × (8π/3) = 128π/3 ≈ 134
     ↓
4Z² + 3 = 137.04 = α⁻¹
```

The factor of 4 appears twice:
- Once in Z² = 4 × (8π/3)
- Once in 4 × Z²

So α⁻¹ = 16 × (8π/3) + 3 = (128π + 9)/3

---

## Proposed Derivation

### The Conjecture

```
α⁻¹ = D_spacetime × Z² + n_SU(2)

Where:
- D_spacetime = 4 (spacetime dimensions)
- Z² = gravitational geometry from Friedmann
- n_SU(2) = 3 (weak isospin generators)
```

### Why This Structure?

The photon is the unbroken U(1) after electroweak symmetry breaking:
```
SU(2)_L × U(1)_Y → U(1)_EM
```

The electromagnetic coupling inherits:
- Geometric structure from gravity (Z²)
- Multiplied by spacetime dimensions (4)
- Plus the SU(2) structure it emerged from (3)

### The Missing Piece

To complete this, we need to show:
1. Why the spacetime dimensions enter multiplicatively with Z²
2. Why SU(2) generators enter additively
3. The physical mechanism connecting gravity to electromagnetism

---

## Summary

### What We Know:
- α = 1/(4Z² + 3) achieves 0.004% accuracy
- The formula gives the IR (Thomson) limit
- The structure (4, Z², 3) has suggestive interpretations

### Most Likely Interpretation:
```
α⁻¹ = (spacetime dim) × (Friedmann geometry)² + (SU(2) generators)
    = 4 × Z² + 3
    = 4 × 32π/3 + 3
    = 137.04
```

### What's Missing:
- Rigorous derivation from gauge-gravity duality
- Explanation of why IR limit takes this form
- Connection to running (why 137 at low energy?)

---

## Connection to Other Formulas

The fine structure constant connects to the rest of the framework:

```
Z = 2√(8π/3)          ← Friedmann + thermodynamics
       ↓
Z² = 32π/3
       ↓
α = 1/(4Z² + 3)       ← Electromagnetic
       ↓
6Z² = 64π = 8×8π      ← Lepton masses (m_μ/m_e)
       ↓
Ω_Λ = 3Z/(8+3Z)       ← Dark energy
       ↓
α_s = Ω_Λ/Z           ← Strong force
```

All roads lead back to Z = 2√(8π/3).

---

*Carl Zimmerman, March 2026*
