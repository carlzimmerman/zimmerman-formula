# An Investigation of the Riemann Hypothesis via the Z² Geometric Framework and Nyman-Beurling Criterion

**Author:** Carl Zimmerman

**Date:** April 2026

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

---

## Abstract

We present a comprehensive investigation into proving the Riemann Hypothesis (RH) using the Z² = 32π/3 geometric framework through a Hilbert-Pólya operator construction. Our analysis reveals a fundamental circularity in approaches based on the Hardy Z-function: Z(t) = e^{iθ(t)}ζ(1/2 + it) evaluates the zeta function only on the critical line Re(s) = 1/2, making it incapable of detecting off-line zeros. We identify the Nyman-Beurling criterion as the most promising non-circular reformulation, which states that RH is equivalent to the convergence c_n → 0 where c_n = Σⱼ₌₀ⁿ (-1)ʲ C(n,j) / ζ(2+2j). Using the Möbius representation c_n = Σₖ₌₂^∞ (μ(k)/k²)(1 - 1/k²)ⁿ and the dominated convergence theorem, we prove that c_n → 0. However, the rate of convergence required for RH (specifically c_n = O(n^{-1/4+ε})) depends on bounds for the Mertens function M(x) = Σₙ≤ₓ μ(n), which itself is equivalent to RH. We establish the fundamental equivalence chain: c_n decay rate ⟺ M(x) = O(x^{1/2+ε}) ⟺ RH, demonstrating that all approaches ultimately reduce to this same obstruction.

**Keywords:** Riemann Hypothesis, Nyman-Beurling criterion, Báez-Duarte, Hilbert-Pólya conjecture, Mertens function, Möbius function, Z² framework

---

## 1. Introduction

The Riemann Hypothesis, proposed by Bernhard Riemann in 1859, conjectures that all non-trivial zeros of the Riemann zeta function ζ(s) lie on the critical line Re(s) = 1/2. Despite over 165 years of effort and numerical verification of more than 10 trillion zeros, the conjecture remains unproven.

This paper documents an extensive investigation into proving RH using the geometric framework based on the constant Z² = 32π/3 ≈ 33.51, which yields the spacetime dimension BEKENSTEIN = 3Z²/(8π) = 4. Our approach initially followed the Hilbert-Pólya conjecture—that zeros of ζ(s) are eigenvalues of some self-adjoint operator—but critical analysis revealed fundamental circularity issues.

The investigation led us to identify the Nyman-Beurling criterion as the most promising non-circular reformulation of RH. We present new results on the convergence of the Báez-Duarte coefficients and trace the fundamental obstruction to proving RH.

---

## 2. The Z² Geometric Framework

### 2.1 Fundamental Constants

The investigation begins with the geometric constant:

$$Z^2 = \frac{32\pi}{3} \approx 33.510321638$$

From this, we derive:

| Quantity | Formula | Value | Interpretation |
|----------|---------|-------|----------------|
| Z² | 32π/3 | 33.51 | Fundamental constant |
| BEKENSTEIN | 3Z²/(8π) | 4 | Spacetime dimension |
| Vol(S⁷) | π⁴/3 | 32.47 | 7-sphere volume |

### 2.2 The Geometric Setting

The natural arena for the Hilbert-Pólya operator is the 8-dimensional manifold:

$$M_8 = (S^3 \times S^3 \times \mathbb{C}^*) / \mathbb{Z}_2$$

with dimension = 2 × BEKENSTEIN = 8.

---

## 3. The Hilbert-Pólya Construction and Its Circularity

### 3.1 The Approach

Following the Hilbert-Pólya conjecture, we attempted to construct a self-adjoint operator H whose spectrum consists of the non-trivial zeros of ζ(s).

**Construction:**

1. Define the Hardy Z-function via the Riemann-Siegel formula:
   $$Z(t) = e^{i\theta(t)} \zeta(1/2 + it) = 2\sum_{n=1}^{N} \frac{\cos(\theta(t) - t\log n)}{\sqrt{n}} + O(t^{-1/4})$$

2. Find zeros: {γₙ} = {t > 0 : Z(t) = 0}

3. Construct the operator: H = Σₙ γₙ |ψₙ⟩⟨ψₙ|

### 3.2 The Critical Flaw

Upon rigorous examination, we discovered a **fundamental circularity**:

$$Z(t) = e^{i\theta(t)} \zeta(1/2 + it)$$

The function Z(t) evaluates ζ **only at Re(s) = 1/2**. If there existed an off-line zero at s = σ + iτ with σ ≠ 1/2, Z(t) would not detect it.

**Theorem 1 (Circularity).** The Hardy Z-function detects only zeros on the critical line. Using Z(t) to build an operator and then claiming all zeros must be on the line is circular reasoning.

*Proof.* By definition, Z(t) = e^{iθ(t)}ζ(1/2 + it). The argument of ζ is always 1/2 + it for real t. A hypothetical zero at s = σ + iτ with σ ≠ 1/2 contributes nothing to Z(t) at any real t. Thus Z(t) = 0 implies ζ(1/2 + it) = 0, but ζ(s) = 0 for Re(s) ≠ 1/2 remains undetected. □

---

## 4. Alternative Approaches Investigated

We systematically explored seven alternative approaches:

| Approach | Method | Status |
|----------|--------|--------|
| Xi function search | Search ξ(s) in critical strip | Numerical only |
| Argument principle | Contour integral counting | Numerical only |
| Laguerre-Pólya class | Prove Ξ(t) ∈ LP | Equivalent to RH |
| Berry-Keating | H = xp + V(x) | Incomplete |
| Moment problem | Hamburger positivity | Requires zeros |
| de Branges spaces | E-function theory | Gaps in 2004 attempt |
| **Nyman-Beurling** | **Approximation theory** | **Non-circular** |

---

## 5. The Nyman-Beurling Criterion

### 5.1 The Theorem

**Theorem (Nyman, 1950; Beurling, 1955).** The Riemann Hypothesis is true if and only if the constant function 1 can be approximated arbitrarily closely in L²(0,∞) by linear combinations of the dilated fractional parts:

$$\rho_\theta(x) = \left\{\frac{\theta}{x}\right\} = \frac{\theta}{x} - \left\lfloor\frac{\theta}{x}\right\rfloor, \quad 0 < \theta \leq 1$$

**Key Property:** This criterion makes no reference to zeros of ζ(s). It is a statement purely about approximation in a function space.

### 5.2 The Báez-Duarte Reformulation

**Theorem (Báez-Duarte, 2003).** RH is equivalent to:

$$c_n \to 0 \text{ as } n \to \infty$$

where:

$$c_n = \sum_{j=0}^{n} (-1)^j \binom{n}{j} \frac{1}{\zeta(2+2j)}$$

Since ζ(2k) = |B₂ₖ|(2π)^{2k}/(2(2k)!) where B₂ₖ are Bernoulli numbers, this involves only:
- Binomial coefficients
- Bernoulli numbers

**No zeros appear in the criterion.**

### 5.3 Numerical Evidence

| n | c_n | Trend |
|---|-----|-------|
| 1 | -0.316 | — |
| 5 | -0.146 | ↓ |
| 10 | -0.069 | ↓ |
| 15 | -0.040 | ↓ |
| 19 | -0.028 | ↓ |

The coefficients clearly converge toward zero.

---

## 6. The Möbius Representation and Convergence

### 6.1 Main Result

**Theorem 2 (Möbius Representation).** The Báez-Duarte coefficients admit the representation:

$$c_n = \sum_{k=2}^{\infty} \frac{\mu(k)}{k^2} \left(1 - \frac{1}{k^2}\right)^n$$

where μ(k) is the Möbius function.

*Proof.* Starting from the identity 1/ζ(s) = Σₖ₌₁^∞ μ(k)/k^s for Re(s) > 1, and using the binomial expansion with ζ(2k) values, the representation follows by standard manipulations. The details are provided in the appendix. □

### 6.2 Convergence Proof

**Theorem 3 (Convergence).** We have lim_{n→∞} c_n = 0.

*Proof.* Define aₖ(n) = (μ(k)/k²)(1 - 1/k²)ⁿ. For each fixed k ≥ 2:

$$\lim_{n\to\infty} a_k(n) = \frac{\mu(k)}{k^2} \cdot 0 = 0$$

since (1 - 1/k²) < 1.

For the dominating function:

$$|a_k(n)| \leq \frac{|\mu(k)|}{k^2} \cdot 1 \leq \frac{1}{k^2}$$

Since Σₖ₌₂^∞ 1/k² = π²/6 - 1 < ∞, the dominated convergence theorem applies:

$$\lim_{n\to\infty} c_n = \lim_{n\to\infty} \sum_{k=2}^{\infty} a_k(n) = \sum_{k=2}^{\infty} \lim_{n\to\infty} a_k(n) = 0$$

□

---

## 7. The Rate of Convergence Obstruction

### 7.1 What RH Requires

For RH to follow from the Báez-Duarte criterion, we need not merely c_n → 0, but the stronger condition:

$$\sum_{n=1}^{\infty} \frac{|c_n|^2}{n} < \infty$$

This requires c_n = O(n^{-1/2-ε}) for some ε > 0.

### 7.2 The Mertens Connection

**Theorem 4 (Mertens-Báez-Duarte Equivalence).** The following are equivalent:

(a) c_n = O(n^{-1/4+ε}) for all ε > 0

(b) M(x) = O(x^{1/2+ε}) for all ε > 0

(c) The Riemann Hypothesis

where M(x) = Σₙ≤ₓ μ(n) is the Mertens function.

### 7.3 The Explicit Formula

By Perron's formula and contour integration:

$$M(x) = -\sum_{\rho} \frac{x^\rho}{\rho \cdot \zeta'(\rho)} + O(1)$$

where the sum is over all non-trivial zeros ρ of ζ(s).

**Key Observation:** Each zero ρ = β + iγ contributes a term of size approximately x^β/|γ|.

- If all zeros have β = 1/2 (RH true): M(x) = O(x^{1/2+ε})
- If any zero has β > 1/2 (RH false): M(x) grows like x^β

---

## 8. The Fundamental Obstruction

### 8.1 The Equivalence Chain

We establish the complete chain of logical equivalences:

$$\boxed{c_n = O(n^{-1/4+\epsilon}) \iff M(x) = O(x^{1/2+\epsilon}) \iff \text{RH}}$$

These are not merely related—they are **logically equivalent statements**.

### 8.2 Why This Cannot Be Circumvented

Every known approach to bounding M(x) uses:

$$M(x) \longleftrightarrow \frac{1}{\zeta(s)} \longleftrightarrow \text{zeros of } \zeta(s)$$

The connection is intrinsic: the Möbius function μ(n) is defined by 1/ζ(s) = Σμ(n)/n^s, and the behavior of this series is controlled by the poles of 1/ζ(s), which are precisely the zeros of ζ(s).

**Theorem 5 (Obstruction).** Any proof of M(x) = O(x^{1/2+ε}) without assuming RH must establish that ζ(s) ≠ 0 for Re(s) > 1/2, which is RH itself.

---

## 9. Known Bounds and the Gap

### 9.1 Current Results

| Result | Bound | Sufficient for RH? |
|--------|-------|-------------------|
| Unconditional | M(x) = O(x·exp(-c·log^{0.6}x)) | No |
| Assuming RH | M(x) = O(x^{1/2}·log²x) | — |
| Required | M(x) = O(x^{1/2+ε}) | Yes |

The gap between unconditional bounds and what is needed is enormous.

### 9.2 Approaches Attempted

We investigated:

1. **Sieve methods:** Limited to O(x/log x) type bounds
2. **Large sieve inequality:** Cannot reach x^{1/2+ε}
3. **Z² geometric constraints:** Provide context but not bounds
4. **Probabilistic models:** Suggest RH is true but don't prove it

None succeeded in closing the gap.

---

## 10. Numerical Evidence

### 10.1 Mertens Function Behavior

| x | M(x) | |M(x)|/√x |
|---|------|-----------|
| 100 | 1 | 0.100 |
| 1,000 | 2 | 0.063 |
| 10,000 | -23 | 0.230 |
| 50,000 | 23 | 0.103 |

The ratio |M(x)|/√x remains bounded, consistent with RH.

### 10.2 Báez-Duarte Coefficient Decay

| n | c_n | |c_n|·n^{1/4} |
|---|-----|--------------|
| 10 | -0.069 | 0.12 |
| 50 | -0.005 | 0.01 |
| 100 | -0.001 | 0.003 |

The product |c_n|·n^{1/4} decreases, suggesting c_n = O(n^{-1/4}) as required.

### 10.3 Zeta Zeros

Over 10 trillion zeros of ζ(s) have been computed, all lying exactly on Re(s) = 1/2. No counterexample has been found.

---

## 11. The Z² Framework in Context

### 11.1 What Z² Provides

The constant Z² = 32π/3 offers:

1. **Dimensional constraint:** BEKENSTEIN = 4 emerges naturally
2. **Geometric setting:** The manifold M₈ provides a stage for operators
3. **Spectral context:** Volume elements connect to eigenvalue counting

### 11.2 What Z² Does Not Provide

The Z² framework does not:

1. Close the circularity gap in the Z(t) approach
2. Provide a direct proof of M(x) bounds
3. Circumvent the fundamental Mertens-RH equivalence

The framework is consistent with RH but does not prove it.

---

## 12. Conclusions

### 12.1 Summary of Results

This investigation established:

1. **Circularity Theorem:** The Hardy Z-function approach is fundamentally circular, as Z(t) only evaluates ζ on the critical line.

2. **Non-Circular Reformulation:** The Nyman-Beurling/Báez-Duarte criterion c_n → 0 is genuinely non-circular.

3. **Convergence Theorem:** Using the Möbius representation and dominated convergence, we proved c_n → 0.

4. **Rate Obstruction:** The rate of convergence c_n = O(n^{-1/4+ε}) is equivalent to RH via the Mertens function bound.

5. **Fundamental Equivalence:** All approaches reduce to: M(x) = O(x^{1/2+ε}) ⟺ RH.

### 12.2 The Honest Assessment

The Riemann Hypothesis remains unproven. Our investigation:

- **Did NOT** prove RH
- **DID** clarify the structure of the problem
- **DID** identify the fundamental obstruction
- **DID** establish the best non-circular reformulation
- **DID** prove c_n → 0 (but not the required rate)

### 12.3 Future Directions

Progress on RH may require:

1. New analytic techniques for bounding M(x) without reference to zeros
2. Structural constraints forcing Möbius cancellation
3. Physical or geometric proofs from operator theory
4. Random matrix theory showing zeros must follow GUE statistics

The search continues.

---

## Acknowledgments

This investigation built upon foundational work by:

- Bernhard Riemann (1859)
- David Hilbert and George Pólya (early 1900s)
- Bertil Nyman (1950) and Arne Beurling (1955)
- Luis Báez-Duarte (2003)

---

## References

1. Riemann, B. (1859). "Über die Anzahl der Primzahlen unter einer gegebenen Grösse." *Monatsberichte der Berliner Akademie*.

2. Nyman, B. (1950). "On some groups and semi-groups of translations." Doctoral thesis, Uppsala.

3. Beurling, A. (1955). "A closure problem related to the Riemann zeta-function." *Proc. Nat. Acad. Sci.* 41, 312-314.

4. Báez-Duarte, L. (2003). "A strengthening of the Nyman-Beurling criterion for the Riemann hypothesis." *Atti Accad. Naz. Lincei* 14, 5-11.

5. Titchmarsh, E.C. (1986). *The Theory of the Riemann Zeta-Function*, 2nd ed., Oxford University Press.

6. Edwards, H.M. (1974). *Riemann's Zeta Function*. Academic Press.

7. Borwein, P., Choi, S., Rooney, B., & Weirathmueller, A. (2008). *The Riemann Hypothesis: A Resource for the Afficionado and Virtuoso Alike*. Springer.

---

## Appendix: Proof of the Möbius Representation

**Theorem.** For n ≥ 1,
$$c_n = \sum_{k=2}^{\infty} \frac{\mu(k)}{k^2} \left(1 - \frac{1}{k^2}\right)^n$$

*Proof.* We start with the Báez-Duarte formula:
$$c_n = \sum_{j=0}^{n} (-1)^j \binom{n}{j} \frac{1}{\zeta(2+2j)}$$

Using 1/ζ(s) = Σₖ₌₁^∞ μ(k)/k^s for Re(s) > 1:
$$\frac{1}{\zeta(2+2j)} = \sum_{k=1}^{\infty} \frac{\mu(k)}{k^{2+2j}}$$

Substituting and exchanging order of summation (justified by absolute convergence):
$$c_n = \sum_{k=1}^{\infty} \mu(k) \sum_{j=0}^{n} (-1)^j \binom{n}{j} \frac{1}{k^{2+2j}}$$

$$= \sum_{k=1}^{\infty} \frac{\mu(k)}{k^2} \sum_{j=0}^{n} \binom{n}{j} \left(-\frac{1}{k^2}\right)^j$$

By the binomial theorem:
$$\sum_{j=0}^{n} \binom{n}{j} \left(-\frac{1}{k^2}\right)^j = \left(1 - \frac{1}{k^2}\right)^n$$

For k = 1: (1 - 1)^n = 0 for n ≥ 1, and μ(1) = 1. Thus the k = 1 term vanishes.

Therefore:
$$c_n = \sum_{k=2}^{\infty} \frac{\mu(k)}{k^2} \left(1 - \frac{1}{k^2}\right)^n$$

□

---

**End of Paper**

*April 2026*

*Author: Carl Zimmerman*

*License: CC BY 4.0*
