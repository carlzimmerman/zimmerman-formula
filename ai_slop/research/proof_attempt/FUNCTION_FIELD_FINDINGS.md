# Function Field RH Analysis: Why Weil's Proof Works

**Date:** April 2026
**Status:** Direction 2 of "Beyond Mertens Wall" investigation

---

## Executive Summary

We implemented and verified the **proven** Riemann Hypothesis for function fields (elliptic curves over finite fields) and analyzed what makes Weil's proof work. The goal: identify what integer analogues might unlock the classical RH.

---

## Key Findings

### 1. Hasse-Weil Bound VERIFIED

For elliptic curve E: y² = x³ + x + 1 over F_p:

| Prime p | #E(F_p) | a_p = p+1-#E | Bound 2√p | |a_p| ≤ 2√p |
|---------|---------|--------------|-----------|------------|
| 5 | 9 | -3 | 4.47 | ✓ |
| 7 | 5 | 3 | 5.29 | ✓ |
| 11 | 14 | -2 | 6.63 | ✓ |
| 13 | 9 | 5 | 7.21 | ✓ |
| 17 | 18 | 0 | 8.25 | ✓ |
| 23 | 24 | 0 | 9.59 | ✓ |
| 97 | 108 | -10 | 19.70 | ✓ |

**All 23 primes tested satisfy the bound.** This IS the RH for function fields.

### 2. Frobenius Eigenvalues Have Exact Magnitude √p

| p | |α| | √p | Ratio |
|---|-----|-----|-------|
| 5 | 2.236 | 2.236 | 1.000000 |
| 7 | 2.646 | 2.646 | 1.000000 |
| 11 | 3.317 | 3.317 | 1.000000 |
| 13 | 3.606 | 3.606 | 1.000000 |

**The eigenvalue constraint |α| = √p is EXACT.** This is the spectral interpretation of RH.

### 3. Zeta Function Structure

For elliptic curves, the zeta function factors as:

```
Z(E/F_p, T) = (1 - a_p·T + p·T²) / ((1-T)(1-p·T))
```

- **Numerator**: encodes Frobenius eigenvalues (H¹ contribution)
- **Denominator**: H⁰ and H² contributions
- **Functional equation**: Z(1/pT) relates to Z(T)

### 4. WHY THE PROOF WORKS

| Component | Function Field | Integer Analogue |
|-----------|----------------|------------------|
| Base object | Curve C over F_q | Spec(Z) |
| Frobenius | φ: x → x^q (canonical!) | ??? |
| Cohomology | H¹(C) finite-dim (= 2g) | H¹(Spec Z) = ??? |
| Eigenvalues | 2g total (finite!) | Infinitely many zeros |
| Pairing | Weil pairing → |α| = √q | No known analogue |

**The fundamental obstruction:**
- Function fields: Frobenius has finitely many eigenvalues
- ζ(s): Infinitely many zeros (continuous spectrum problem)

---

## Candidate Integer Frobenius Analogues

### Explored Candidates

| Candidate | Description | Status |
|-----------|-------------|--------|
| Multiplication by n | φ_n: x → n·x | Doesn't capture primes |
| Hecke operators T_p | Act on modular forms | Part of established theory |
| Adelic scaling (Connes) | R₊* action on adeles | Gives flow, not discrete map |
| Galois action | Gal(Q̄/Q) on roots of unity | Frobenius at p exists |
| Squaring map | x → x² mod n | Has Frobenius-like orbits |

### Möbius as "Frobenius Sign"

A compelling observation:

```
μ(p) = -1 for all primes (always!)
μ(n) = (-1)^{ω(n)} for squarefree n (product of signs)
```

If we construct "eigenvalue" α_p = -√p (using μ(p) = -1):
- |α_p| = √p ✓ (matches function field RH)
- Sign encodes μ(p) ✓

But this is suggestive, not a proof.

---

## The Finite vs Infinite Problem

### Function Fields (Solved)
```
Curve C of genus g over F_q
  → H¹(C) has dimension 2g
  → Frobenius has 2g eigenvalues α₁, ..., α_{2g}
  → Linear algebra: det, trace, Weil pairing
  → FORCES |αᵢ| = √q
```

### Integers (Unsolved)
```
"Curve" Spec(Z)
  → H¹(Spec Z) = ??? (not well-defined)
  → Infinitely many zeta zeros ρ₁, ρ₂, ...
  → No finite-dimensional linear algebra
  → Cannot directly force Re(ρ) = 1/2
```

---

## Advanced Perspectives

### F_1 (Field with One Element)

Hypothetical picture:
- Spec(Z) is a "curve over F_1"
- ζ(s) is the zeta function of this curve
- Would need "Frobenius at ∞"

**Status:** Several approaches (Connes, Borger), none yet prove RH.

### Arakelov Geometry

- Treats Spec(Z) as complete curve with archimedean place
- Product formula Π_v |x|_v = 1 is like Weil's theorem
- RH ↔ bounding arithmetic intersection numbers

### Connection to Spectral Findings

From Direction 1 (Spectral Analysis):
- Number variance suppressed by factor 0.35
- Zeros MORE correlated than pure GUE

**Interpretation:** The "missing cohomology" imposes extra constraints on zeros, visible as the suppressed variance.

---

## Comparison: What Would Prove RH

| Method | What's Needed | Difficulty |
|--------|---------------|------------|
| Hilbert-Pólya | Find Hermitian operator H with Spec = zeros | Continuous spectrum problem |
| Connes | Complete adelic trace formula | Technical barriers |
| F_1 | Rigorous "field with one element" | Foundational issues |
| Direct | New insight for infinite zeros | Unknown |

---

## Summary: Lessons from Function Fields

### What Works
1. **Canonical Frobenius** - unique, natural map
2. **Finite cohomology** - linear algebra applies
3. **Weil pairing** - forces eigenvalue magnitudes
4. **Functional equation** - follows from duality

### What's Missing for Z
1. **No canonical Frobenius** - must construct something
2. **Infinite zeros** - not finite-dimensional
3. **No known pairing** - need replacement
4. **Cohomology undefined** - H¹(Spec Z) unclear

### The Optimistic Path

If we could construct:
1. A Frobenius-like operator on some space for Z
2. Acting on finite-dimensional (or regularized) cohomology
3. With a Weil-like pairing

Then RH would follow by the function field method.

### The Sobering Reality

The integers are fundamentally different:
- Characteristic 0 vs characteristic p
- One infinite place vs none
- Infinitely many primes with different roles

A proof may require entirely new methods.

---

## Files Created

| File | Content |
|------|---------|
| `function_field_rh.py` | Full elliptic curve implementation |
| `frobenius_analogue_search.py` | Integer Frobenius candidates |
| `FUNCTION_FIELD_FINDINGS.md` | This summary |

---

## Next Steps

### Most Promising Directions
1. **Connes' adelic approach** - closest to function fields
2. **Trace formula methods** - connect spectral to arithmetic
3. **Motivic cohomology** - universal cohomology theory

### Possible Direction 3
L-function families and Katz-Sarnak density theorems - understand symmetry types.

---

*Carl Zimmerman, April 2026*
