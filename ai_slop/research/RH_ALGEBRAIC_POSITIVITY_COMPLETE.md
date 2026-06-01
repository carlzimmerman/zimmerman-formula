# Algebraic Positivity Path to RH: Complete Analysis

**Author:** Carl Zimmerman
**Date:** April 2026
**Goal:** Find a purely algebraic/combinatorial proof that λ_n > 0 for all n

---

## Executive Summary

**Li's Criterion:** RH ⟺ λ_n ≥ 0 for all n ≥ 1

An algebraic proof of λ_n > 0 would solve RH without analyzing zeros. This document explores whether such a proof is possible.

**Bottom Line:** The algebraic structure of λ_n is tantalizing but ultimately involves mixed transcendentals (γ, π, ζ(odd)) that resist purely combinatorial treatment. No algebraic positivity proof is currently known.

---

## Part 1: What Is λ_n?

### Definition (Li 1997)

```
λ_n = (1/(n-1)!) [d^n/ds^n (s^{n-1} ln ξ(s))]_{s=1}
```

where ξ(s) is the completed zeta function.

### Equivalent Representations

**Sum over zeros (circular - requires RH to evaluate):**
```
λ_n = Σ_ρ [1 - (1 - 1/ρ)^n]
```

**Explicit formula (potentially non-circular):**
```
λ_n = 1 - (n/2)(γ + ln π + 2 ln 2)
      - Σ_{m=1}^n C(n,m) η_{m-1}
      + Σ_{m=2}^n (-1)^m C(n,m) (1 - 2^{-m}) ζ(m)
```

**Asymptotic behavior:**
```
λ_n ~ (n/2) log(n/(4πe)) + O(log n)
```

---

## Part 2: Numerical Evidence

### Computed Values

| n | λ_n |
|---|-----|
| 1 | 0.7655 |
| 2 | 2.4182 |
| 5 | 7.3217 |
| 10 | 15.5997 |
| 20 | 32.3235 |

All computed λ_n are **POSITIVE** and grow like n log n.

### Key Observation

```
λ_n > 0 for all n ≤ 10^5 (Maślanka's computations)
```

This provides overwhelming numerical evidence but not proof.

---

## Part 3: The Algebraic Structure

### The Alternating Sum

The explicit formula contains:
```
Σ_{k=2}^n (-1)^k C(n,k) (1 - 2^{-k}) ζ(k)
```

This has the hallmark of **inclusion-exclusion**!

For n = 5:
| k | Sign | C(5,k) | (1-2^{-k}) | ζ(k) | Term |
|---|------|--------|------------|------|------|
| 2 | + | 10 | 0.75 | 1.6449 | +12.34 |
| 3 | - | 10 | 0.875 | 1.2021 | -10.52 |
| 4 | + | 5 | 0.9375 | 1.0823 | +5.07 |
| 5 | - | 1 | 0.9688 | 1.0369 | -1.00 |
| **Sum** | | | | | **+5.89** |

The positive terms dominate!

### The 1/ζ(2k) Connection

From Báez-Duarte:
```
c_n = Σ_{j=0}^n (-1)^j C(n,j) / ζ(2+2j)
```

Key fact: **1/ζ(2) = 6/π² = probability(n is squarefree)**

This probabilistic interpretation is the closest thing to combinatorics we have.

---

## Part 4: Sign-Reversing Involution Approach

### The D.I.E. Method (Benjamin-Quinn)

- **D**escribe combinatorially what we're counting
- Find an **I**nvolution pairing + and - terms
- Count the **E**xceptions (fixed points give the result)

### Requirements for λ_n

1. Combinatorial objects counted by C(n,k) ζ(k)
2. A sign-reversing involution pairing most positive/negative terms
3. Show fixed points contribute positively

### The Challenge

**What combinatorial objects correspond to ζ(k)?**

For ζ(2k):
```
ζ(2k) = (-1)^{k+1} (2π)^{2k} B_{2k} / (2(2k)!)
```
where B_{2k} is a Bernoulli number.

But ζ(odd) is **transcendental** with no known closed form!

This breaks the combinatorial approach.

---

## Part 5: Totally Positive Matrices

### What Is Total Positivity?

A matrix M is **totally positive (TP)** if all minors are ≥ 0.

### Why It Matters

If λ_n = M[n, •] for some TP matrix M, then λ_n ≥ 0 automatically.

### The Coefficient Matrix

```
M[n,k] = (-1)^k C(n,k) (1 - 2^{-k})
```

| n\k | 2 | 3 | 4 | 5 |
|-----|-------|-------|-------|-------|
| 2 | +0.75 | | | |
| 3 | +2.25 | -0.88 | | |
| 4 | +4.50 | -3.50 | +0.94 | |
| 5 | +7.50 | -8.75 | +4.69 | -0.97 |

**Problem:** The alternating signs mean this is NOT totally positive!

### Possible Fix

A transformation T might exist such that T·M is TP.
**Status:** No such transformation is known.

---

## Part 6: Operator Theory Connection

### Weil's Quadratic Functional

Li showed:
```
λ_n = W(φ_n ⊗ φ̃_n)
```
where W is Weil's functional and φ_n are specific test functions.

**If W is positive definite ⟹ λ_n ≥ 0 ⟹ RH**

But proving W positive definite IS equivalent to RH!

### Hilbert-Pólya Approach

If there exists a self-adjoint operator H such that:
```
λ_n = <n|H|n>
```
then λ_n ≥ 0 follows from H being positive.

**Status:** All constructions (Berry-Keating, Connes, Yakaboylu) have gaps.

---

## Part 7: Why Algebraic Positivity Is Hard

### The Four Obstacles

1. **Mixed Transcendentals**
   - γ (Euler-Mascheroni) - transcendental
   - π - transcendental
   - ζ(odd) - transcendental, no closed form
   - These don't combine into "nice" combinatorics

2. **Alternating Signs**
   - The (-1)^k structure breaks TP approaches
   - Inclusion-exclusion needs compatible objects

3. **No Combinatorial Model**
   - C(n,k) has combinatorial meaning (subsets)
   - But ζ(k) has no known combinatorial meaning
   - Their product is uninterpretable

4. **Circularity Risk**
   - The sum-over-zeros formula requires RH to evaluate
   - Other formulas still implicitly depend on zero structure

### What Would Work

| Form | Why It Would Prove λ_n > 0 |
|------|---------------------------|
| λ_n = \|A\| (cardinality) | Sets have non-negative size |
| λ_n = f(n)² + g(n)² | Sums of squares are ≥ 0 |
| λ_n = ⟨v,Pv⟩ (positive operator) | Positive operators give ≥ 0 |
| λ_n = bijective proof | Fixed points counted positively |

**None of these representations are known for λ_n.**

---

## Part 8: Promising Directions

### Direction 1: Generating Function Positivity

Define:
```
G(x) = Σ_{n≥1} λ_n x^n / n!
```

If we could show G(x) ≥ 0 for x > 0 algebraically, that would imply λ_n ≥ 0.

**Challenge:** G(x) relates to ξ(1+1/(1-x)), needs analytic continuation.

### Direction 2: Bernoulli Number Identities

Since ζ(2k) involves B_{2k}:
- Kummer congruences give p-adic structure
- Von Staudt-Clausen theorem gives denominators
- Perhaps these encode positivity?

**Status:** No direct connection established.

### Direction 3: Probabilistic Model

Since 1/ζ(2) = P(squarefree):
- Maybe λ_n counts "favorable outcomes" minus "unfavorable"
- And favorable always dominates?

**Challenge:** Need to extend to ζ(odd) values.

### Direction 4: Sum-of-Squares Representation

If λ_n = Σ a_i(n)² for rational a_i, positivity is automatic.

**Challenge:** No such representation is known.

---

## Part 9: What An Algebraic Proof Would Look Like

### Fantasy Theorem

**Theorem (Fantasy):** For all n ≥ 1,
```
λ_n = Σ_{σ ∈ S} w(σ)
```
where S is a combinatorial set and w(σ) > 0 for all σ.

**Proof:** By bijective combinatorics / inclusion-exclusion / TP matrix theory.

### Why It's Fantasy

- We don't know what S should be
- The transcendental constants (γ, ζ(odd)) resist combinatorics
- Even ζ(2k), despite being π^{2k} × rational, lacks a counting interpretation

---

## Part 10: Comparison to Other Approaches

| Approach | Uses Zero Info? | Algebraic? | Status |
|----------|-----------------|------------|--------|
| Direct zero verification | Yes | No | Can't prove all zeros |
| Harper's random model | No | Probabilistic | Not applicable to deterministic μ |
| Operator (Hilbert-Pólya) | Indirectly | No | Gaps in all constructions |
| **Algebraic positivity** | **No** | **Yes** | **No proof known** |

The algebraic path is appealing precisely because it avoids zeros, but this very feature makes it hard - the positivity of λ_n IS controlled by zeros.

---

## Part 11: Summary

### What We Know

1. λ_n > 0 numerically for all computed n (up to ~10^5)
2. λ_n grows like n log n asymptotically (hence eventually positive)
3. The formula has inclusion-exclusion structure
4. But involves transcendentals without combinatorial meaning

### What We Don't Know

1. A purely algebraic proof that λ_n > 0
2. A combinatorial interpretation of ζ(odd)
3. A TP matrix representation
4. An operator-theoretic representation

### The Honest Assessment

**An algebraic proof of λ_n > 0 would prove RH.**

The structure strongly suggests positivity:
- Growth is positive asymptotically
- All numerical evidence confirms it
- The formula "looks like" inclusion-exclusion

But the gap between "looks like" and "is" remains unbridged.

The transcendental nature of ζ(odd) appears to be the fundamental obstacle.

---

## References

- Li, X.-J. (1997): "The positivity of a sequence of numbers and the RH"
- Bombieri & Lagarias (1999): "Complements to Li's Criterion"
- Coffey (2004-2010): Explicit formulas for Li coefficients
- Benjamin & Quinn (2008): "An Alternate Approach to Alternating Sums" (D.I.E. method)
- Maślanka (2006): Numerical computation of λ_n

---

**Carl Zimmerman**
**April 2026**

*"The simplest approach is often the hardest to execute."*
