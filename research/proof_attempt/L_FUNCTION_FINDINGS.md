# L-Function Families Analysis: Katz-Sarnak Philosophy

**Date:** April 2026
**Status:** Direction 3 of "Beyond Mertens Wall" investigation

---

## Executive Summary

We explored the Katz-Sarnak philosophy: L-functions come in families with symmetry types that determine their zero statistics. While this reveals deep structure, **family averages cannot prove RH** because averages don't constrain individual functions.

---

## Key Findings

### 1. Symmetry Types Verified

| Symmetry | Sign of FE | Zeros near origin | Example family |
|----------|------------|-------------------|----------------|
| **Unitary (U)** | N/A | Neutral | Single ζ(s) |
| **Symplectic (Sp)** | + | Repelled | Even Dirichlet χ |
| **SO(even)** | - | Attracted | Odd Dirichlet χ |
| **SO(odd)** | - | Forced zero | Certain EC families |

### 2. One-Level Density Functions

| x | W_U(x) | W_Sp(x) | W_SO(x) |
|---|--------|---------|---------|
| 0.0 | 1.000 | **0.000** | **2.000** |
| 0.1 | 1.000 | 0.065 | 1.935 |
| 0.2 | 1.000 | 0.243 | 1.757 |
| 0.5 | 1.000 | 1.000 | 1.000 |
| 1.0 | 1.000 | 1.000 | 1.000 |

**Key observation:** At x=0, Symplectic has W=0 (zeros repelled), while SO has W=2 (zeros attracted).

### 3. Synthetic Low-Lying Zeros

| Family Type | Mean first zero (scaled) |
|-------------|--------------------------|
| Symplectic | 0.553 |
| Orthogonal | 0.121 |

Orthogonal zeros are ~4.5x closer to origin than Symplectic.

### 4. L-Function Values Computed

For quadratic Dirichlet L-functions L(1, χ_d):

| d | L(1, χ_d) | Sign |
|---|-----------|------|
| -47 | +1.146 | Positive ✓ |
| -43 | +0.718 | Positive ✓ |
| -31 | +0.846 | Positive ✓ |
| -23 | +0.983 | Positive ✓ |
| -11 | +1.421 | Positive ✓ |

All positive, consistent with class number formula.

---

## What Families CAN Do

### Proven Results
1. **One-level density** for support < 2 (many families)
2. **Average rank** of elliptic curves (Bhargava et al.)
3. **Density of zeros** on critical line (= 100% in various senses)
4. **Zero-free regions** near Re(s) = 1

### Revealed Structure
- Symmetry types explain statistical differences
- Arithmetic factors emerge naturally
- Random matrix predictions match data

---

## What Families CANNOT Do

### The Fundamental Limitation

| Statement | Families can prove? |
|-----------|---------------------|
| "On average, zeros are on line" | ✓ Yes |
| "Most zeros are on line" | ✓ Yes |
| "All zeros are on line" | ✗ **No** |
| "Each L-function satisfies RH" | ✗ **No** |

### Why Not?

1. **Averages ≠ Individuals**: Even with perfect family statistics, a single exceptional function could violate RH

2. **Siegel Zero Problem**: We cannot rule out that some L(s, χ_d) has a zero near s = 1

3. **Probabilistic vs Deterministic**: Family methods give "with high probability" not "with certainty"

---

## The Ratios Conjecture

### Statement (Conrey-Farmer-Zirnbauer)

For family F:
```
<Π L(1/2 + αₖ) / Π L(1/2 + βⱼ)>_F = [explicit formula]
```

### Critical Issue

**The ratios conjecture ASSUMES RH in its formulation!**

It predicts statistics conditional on zeros being on the line. So:
- ✓ Useful for understanding structure
- ✗ Cannot be used to prove RH

---

## Connection to Other Directions

### Direction 1 (Spectral) + Direction 3 (Families)

| Aspect | Spectral | Families |
|--------|----------|----------|
| Focus | Individual operator | Statistical ensemble |
| Tool | Linear algebra | Averaging |
| Strength | Would prove RH | Reveals structure |
| Weakness | Can't find operator | Can't pin down individuals |

**Insight:** If we knew WHY GUE statistics appear, we might find the operator.

### Direction 2 (Function Field) + Direction 3 (Families)

| Aspect | Function Field | Families |
|--------|----------------|----------|
| Setting | F_q | Q |
| L-functions | Z(C/F_q, T) | L(s, χ) |
| Symmetry type | Determined by genus | Determined by parity |

**Katz's theorem:** For function field families, symmetry type follows from geometric structure.

---

## The Density Hypothesis

### Statement
N(σ, T) = #{ρ : Re(ρ) > σ, 0 < Im(ρ) < T}

**DH:** N(σ, T) << T^{2(1-σ)+ε}

### Current Status
- **Proven:** N(σ, T) << T^{(3/2)(1-σ)+ε}
- **Gap:** Factor of 3/2 vs 2

### Why DH ≠ RH
DH says zeros are "sparse" off-line, not "absent"
- DH: measure zero off line
- RH: exactly zero off line

---

## Numerical Experiments

### L(1/2 + it, χ) on Critical Line

| q | t=1 | t=5 | t=10 |
|---|-----|-----|------|
| 5 | 0.69 | 2.61 | 3.19 |
| 7 | 0.96 | 2.93 | 2.94 |
| 11 | 1.37 | 3.94 | 5.27 |
| 13 | 1.53 | 4.00 | 4.58 |

Average |L|² grows with conductor, as expected.

### Empirical One-Level Density (Zeta Zeros)

Using 100,000 Odlyzko zeros:
- Near x=0: density ~0 (GUE repulsion)
- At x=0.4: density ~0.5
- Matches W_U(x) = 1 asymptotically

---

## Why GUE for Zeta?

### The Mystery

GUE describes eigenvalues of random **unitary** matrices.
- Unitary eigenvalues lie on **unit circle**
- Zeta zeros lie on **vertical line**

These are related by:
```
ρ = 1/2 + iγ  ↔  e^{iγ} on unit circle
```

But this is a parametrization, not an explanation.

### What Would Explain It

If there exists a **unitary operator** U such that:
- Spec(U) = {e^{iγ} : ζ(1/2 + iγ) = 0}
- U is "random" in some natural sense

Then GUE statistics would follow. But:
- What is U?
- Why is it unitary (not just Hermitian)?
- This is the Hilbert-Pólya dream in unitary form

---

## Summary

### Direction 3 Verdict

| Criterion | Score |
|-----------|-------|
| Understanding gained | ★★★★★ |
| Tools developed | ★★★★☆ |
| Progress toward RH | ★★☆☆☆ |
| Can prove RH | ✗ No |

### Key Limitation

**Families reveal statistical structure but cannot prove individual properties.**

The gap between "almost all" and "all" is exactly where RH lives.

### Most Promising Aspect

Understanding WHY different families have different symmetry types might reveal the underlying operator.

---

## Files Created

| File | Content |
|------|---------|
| `l_function_families.py` | Full analysis script |
| `L_FUNCTION_FINDINGS.md` | This summary |

---

*Carl Zimmerman, April 2026*
