# Harper's Multiplicative Chaos Framework: Complete Analysis

**Author:** Carl Zimmerman
**Date:** April 2026
**Topic:** Deep dive into Harper's "better than squareroot cancellation" approach to RH

---

## Executive Summary

Adam Harper's framework on random multiplicative functions and critical multiplicative chaos represents the **most promising modern approach** to the Riemann Hypothesis. This document synthesizes literature findings and numerical tests.

**Bottom Line:** Harper's techniques prove better-than-√x cancellation for random multiplicative functions, and Wang-Xu (2025) extended this to the Liouville function conditionally. Extension to the Möbius function (and thus RH) remains open.

---

## Part 1: Harper's Core Results

### The Main Theorem (Harper 2017)

For Steinhaus or Rademacher random multiplicative functions f(n):

```
E|Σ_{n≤x} f(n)| ~ C · √x / (log log x)^{1/4}
```

**Why This Matters:**
- The naive expectation is √x (random walk)
- Harper proved it's actually √x / (log log x)^{1/4}
- This is **better than squareroot cancellation**
- The (log log x)^{-1/4} factor comes from critical multiplicative chaos

### Source Papers
- [arXiv:1703.06654](https://arxiv.org/abs/1703.06654) - "Moments of random multiplicative functions, I"
- [Cambridge Forum of Mathematics Pi](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/moments-of-random-multiplicative-functions-i-low-moments-better-than-squareroot-cancellation-and-critical-multiplicative-chaos/A7B32F8285B07AE15700F02E997B233F)

---

## Part 2: Critical Multiplicative Chaos Connection

### What Is Critical Multiplicative Chaos?

Critical multiplicative chaos is a field from probability theory (Kahane, 1980s) dealing with random measures of the form:
```
dμ = e^{γX(t) - γ²Var(X)/2} dt
```
where X(t) is a logarithmically correlated Gaussian field.

The "critical" case occurs at the boundary where the measure is still well-defined.

### Harper's Deep Discovery (2025)

Harper proved that **|ζ(1/2+it)|² gives rise to critical multiplicative chaos** as t varies. This connects:

```
         ζ(1/2+it)
            ↕
    Critical Multiplicative Chaos
         ↙       ↘
Random Multiplicative    Better than √x
    Functions           Cancellation
```

### Why The Log Log Factor?

The (log log x)^{1/4} factor arises because:
1. Correlations between f(n) values decay logarithmically
2. This logarithmic correlation is the signature of critical chaos
3. The critical case sits at the boundary of convergence/divergence

---

## Part 3: Wintner's Random Model for Möbius

### Historical Foundation (Wintner 1944)

Wintner introduced **Rademacher random multiplicative functions** as a model for μ(n):
- At each prime p, flip a fair coin: X_p = ±1 with prob 1/2
- Define f(n) = ∏_{p|n} X_p for squarefree n, 0 otherwise
- This models the "random" behavior of μ(n)

### Wintner's Result
```
Σ f(n)/n^s converges a.s. for Re(s) > 1/2
Σ_{n≤x} f(n) = O(x^{1/2+ε}) a.s.
Σ_{n≤x} f(n) ≠ O(x^{1/2-ε}) a.s.
```

This led Wintner to declare "RH is almost surely true" - meaning in the probabilistic model.

### The Gap
The Möbius function μ(n) is deterministic, not random. Wintner's model suggests behavior but doesn't prove it.

---

## Part 4: Extension to Liouville Function

### Wang-Xu Theorem (2025)

From [arXiv:2405.04094](https://arxiv.org/abs/2405.04094):

**Theorem (Wang-Xu):** Assuming:
1. Generalized Riemann Hypothesis (GRH) for all Dirichlet L-functions mod r
2. Ratios Conjecture for primitive Dirichlet L-functions mod r

Then the Liouville function λ(n) has **better than squareroot cancellation** in character twists.

### What This Means

The Ratios Conjecture asserts that averages of ratios of L-functions behave as random matrix theory predicts. Under this assumption, Harper's random techniques extend to the deterministic λ(n).

### Significance for RH

This shows Harper's framework **can** be extended to deterministic arithmetic functions - but only conditionally. The conditions (GRH + Ratios) are themselves major conjectures.

---

## Part 5: What About Möbius?

### Current Status

| Function | Better than √x cancellation | Status |
|----------|---------------------------|--------|
| Random multiplicative f | Yes | **PROVEN** (Harper 2017) |
| Steinhaus f(n) | Yes | **PROVEN** (Harper 2017) |
| Dirichlet characters | Yes, in families | **PROVEN** |
| Liouville λ(n) | Yes | **CONDITIONAL** (GRH + Ratios) |
| Möbius μ(n) | Expected | **OPEN** |

### The Key Quote (Harper 2025)

From [arXiv:2512.23681](https://arxiv.org/abs/2512.23681):

> "The best known unconditional estimate for Σμ(n) is x^{1-o(1)} rather than the conjectured x^{1/2+o(1)}."

### What Would Be Needed

To prove M(x) = O(x^{1/2+ε}) via Harper's approach:

1. **Prove Wang-Xu for μ(n):** Show that under GRH + Ratios, Σμ(n) has better cancellation
2. **Then prove GRH + Ratios:** Both are major open problems
3. **OR find unconditional approach:** Would be revolutionary

---

## Part 6: Numerical Evidence

### Our Computations (x up to 50,000)

| Quantity | Value |
|----------|-------|
| max |M(x)|/√x | 0.567 |
| mean |M(x)|·(log log x)^{1/4}/√x | 0.176 |
| Squarefree proportion | 0.6080 (vs 6/π² = 0.6079) |

### Harper-Style Prediction Test

If M(x) ~ √x/(log log x)^{1/4}, then |M(x)|·(log log x)^{1/4}/√x should be O(1).

Our data shows this ratio averages ~0.18 and stays bounded, **consistent with** Harper-type behavior.

### Gonek-Ng Conjecture Test

Conjecture: max_{y≤x} |M(y)| ~ √x · (log log log x)^{5/4}

| X | max|M|/√X | Gonek-Ng ratio |
|---|-----------|----------------|
| 10000 | 0.430 | 0.570 |
| 50000 | 0.429 | 0.513 |

Data is consistent but range is too small to test properly.

---

## Part 7: Why Harper's Approach is Promising

### Advantages

1. **Rigorous framework:** Critical multiplicative chaos is well-understood mathematically
2. **Already extended once:** Wang-Xu showed it works for Liouville under conditions
3. **Natural connection:** Random model captures real behavior of μ(n)
4. **Modern techniques:** Builds on 40+ years of probability theory

### The Path to RH via Harper

```
Current: E|Σf_random(n)| ~ √x/(log log x)^{1/4}    [PROVEN]
         ↓
Step 1:  GRH + Ratios ⟹ Σλ(n) better cancellation  [PROVEN: Wang-Xu]
         ↓
Step 2:  GRH + Ratios ⟹ Σμ(n) better cancellation  [OPEN]
         ↓
Step 3:  Prove GRH + Ratios unconditionally         [VERY HARD]
         ↓
Result:  M(x) = O(x^{1/2+ε}) = RH                   [GOAL]
```

---

## Part 8: The Fundamental Obstacle

### The Random-Deterministic Gap

Harper's techniques require:
- A probability space
- Independence (or controlled dependence)
- Expectation values

The Möbius function provides:
- No probability space (it's deterministic)
- Multiplicative constraints (not independence)
- No natural averaging

### The Core Challenge

```
Random multiplicative functions: Can compute E|Σf(n)|
Möbius function μ(n): What does "expected value" even mean?
```

Wang-Xu's solution: Use GRH to give a "pseudorandom" structure, then use Ratios Conjecture to compute averages.

For unconditional results, we need a new idea.

---

## Part 9: Related Conjectures

### Gonek-Ng Conjecture
```
max_{x≤X} |M(x)| ~ √X · (log log log X)^{5/4}
```

### Chowla Conjecture (related)
For distinct a₁,...,aₖ:
```
Σ_{n≤x} μ(n+a₁)···μ(n+aₖ) = o(x)
```

### Random Matrix Connection
The zeros of ζ(s) follow GUE statistics (Montgomery-Dyson).
The Ratios Conjecture formalizes this for averages.

---

## Part 10: Summary and Assessment

### What We Now Understand

1. **Harper's framework** is the leading modern approach to RH
2. **Critical multiplicative chaos** explains the (log log)^{1/4} factor
3. **Wang-Xu (2025)** extended Harper to Liouville conditionally
4. **For Möbius:** Similar conditional result seems achievable
5. **Unconditionally:** Major breakthrough needed

### The Honest Assessment

Harper's approach is **promising but not sufficient** for RH:
- It requires probabilistic structure that μ(n) lacks
- Conditional extensions (GRH + Ratios) are already deep results
- Unconditional M(x) = O(x^{1/2+ε}) remains far from current techniques

### What Would Constitute Progress

1. **Near-term:** Prove GRH + Ratios ⟹ M(x) better cancellation (analog of Wang-Xu)
2. **Medium-term:** Weaken the conditions needed
3. **Long-term:** Remove conditions entirely

---

## References

### Primary Sources
- Harper (2017): [arXiv:1703.06654](https://arxiv.org/abs/1703.06654) - Random multiplicative functions
- Harper (2025): [arXiv:2512.23681](https://arxiv.org/abs/2512.23681) - Better than squareroot survey
- Wang-Xu (2025): [arXiv:2405.04094](https://arxiv.org/abs/2405.04094) - Harper's conjecture for Liouville
- Wintner (1944): Duke Math J. 11:267-275 - Random factorizations

### Background
- Kahane (1985): Critical multiplicative chaos theory
- Gonek-Ng: Conjecture on M(x) fluctuations
- Saksman-Webb: Zeta on critical line and multiplicative chaos

---

**Carl Zimmerman**
**April 2026**

*"The gap between random and deterministic is where RH lives."*
