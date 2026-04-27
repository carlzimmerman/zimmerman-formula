"""
NEW APPROACHES TO THE RIEMANN HYPOTHESIS
=========================================

Exploring completely different angles:
1. Higher moment analysis
2. Large deviation theory
3. Self-consistency / contradiction approach
4. Functional equation symmetry
5. Concentration inequalities
6. Information-theoretic bounds
7. Extremal combinatorics

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange, log as symlog, exp as symexp
from sympy import Symbol, Sum, oo, factorial, binomial, sqrt as symsqrt
from collections import defaultdict
import math

print("=" * 80)
print("NEW APPROACHES TO THE RIEMANN HYPOTHESIS")
print("=" * 80)

# Precompute data
MAX_N = 200000
mu = [0] * (MAX_N + 1)
omega_vals = [0] * (MAX_N + 1)

mu[1] = 1
omega_vals[1] = 0

for n in range(2, MAX_N + 1):
    factors = factorint(n)
    omega_vals[n] = len(factors)
    if any(e > 1 for e in factors.values()):
        mu[n] = 0
    else:
        mu[n] = (-1) ** len(factors)

def get_stats(x):
    """Get statistics for squarefree n ≤ x."""
    S = defaultdict(int)
    for n in range(1, min(x+1, MAX_N+1)):
        if mu[n] != 0:
            S[omega_vals[n]] += 1
    Q = sum(S.values())
    M = sum(mu[n] for n in range(1, min(x+1, MAX_N+1)))
    return S, Q, M

# =============================================================================
# APPROACH 1: HIGHER MOMENT ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 1: HIGHER MOMENT ANALYSIS")
print("=" * 80)

print("""
IDEA: The variance is just E[ω²] - E[ω]². What about higher moments?

If we can characterize ALL moments of ω, we fully determine the distribution.
Maybe higher moments give additional constraints?

For Poisson(λ): E[ω^k] has a known formula involving Stirling numbers.
The deviation from Poisson moments might reveal structure.
""")

def compute_moments(x, max_moment=6):
    """Compute moments E[ω^k] for k = 1, ..., max_moment."""
    S, Q, M = get_stats(x)
    moments = []
    for k in range(1, max_moment + 1):
        moment_k = sum(w**k * S.get(w, 0) for w in S) / Q
        moments.append(moment_k)
    return moments

def poisson_moments(lam, max_moment=6):
    """Compute Poisson moments."""
    # E[X^k] for Poisson(λ) can be computed recursively
    # E[X^k] = λ(E[(X+1)^{k-1}]) = λ Σ_{j=0}^{k-1} C(k-1,j) E[X^j]
    moments = [0] * (max_moment + 1)
    moments[0] = 1  # E[X^0] = 1
    for k in range(1, max_moment + 1):
        # Use the formula: E[X^k] = Σ_{j=0}^{k-1} S(k,j+1) λ^{j+1}
        # where S(k,j) are Stirling numbers of the second kind
        # Simpler: use moment generating function
        pass

    # Direct computation for Poisson
    result = []
    for k in range(1, max_moment + 1):
        # E[X^k] = Σ_{n=0}^∞ n^k * λ^n e^{-λ} / n!
        moment = 0
        for n in range(50):
            if n > 0:
                moment += (n ** k) * (lam ** n) * np.exp(-lam) / math.factorial(n)
        result.append(moment)
    return result

x = 100000
lam = np.log(np.log(x))
actual_moments = compute_moments(x, 6)
poisson_mom = poisson_moments(lam, 6)

print(f"\nMoment comparison at x = {x:,}, λ = {lam:.4f}:")
print("-" * 60)
print(f"{'k':>4} | {'E[ω^k] actual':>15} | {'E[ω^k] Poisson':>15} | {'Ratio':>10}")
print("-" * 60)

for k in range(1, 7):
    actual = actual_moments[k-1]
    poisson = poisson_mom[k-1]
    ratio = actual / poisson if poisson != 0 else 0
    print(f"{k:>4} | {actual:>15.4f} | {poisson:>15.4f} | {ratio:>10.4f}")

# Centered moments (about mean)
print("\nCentered moments (about mean):")
S, Q, M = get_stats(x)
mean_actual = actual_moments[0]

centered_moments = []
for k in range(2, 7):
    centered = sum((w - mean_actual)**k * S.get(w, 0) for w in S) / Q
    centered_moments.append(centered)

print(f"  μ₂ (variance) = {centered_moments[0]:.6f}")
print(f"  μ₃ (skewness num) = {centered_moments[1]:.6f}")
print(f"  μ₄ (kurtosis num) = {centered_moments[2]:.6f}")

# Standardized moments
std = np.sqrt(centered_moments[0])
skewness = centered_moments[1] / (std ** 3)
kurtosis = centered_moments[2] / (std ** 4) - 3  # Excess kurtosis

print(f"\nStandardized moments:")
print(f"  Skewness = {skewness:.4f} (Poisson: {1/np.sqrt(lam):.4f})")
print(f"  Excess Kurtosis = {kurtosis:.4f} (Poisson: {1/lam:.4f})")

# =============================================================================
# APPROACH 2: LARGE DEVIATION ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 2: LARGE DEVIATION ANALYSIS")
print("=" * 80)

print("""
IDEA: What's the probability of extreme values?

P(|M(x)| > x^{1/2+δ}) should be very small under RH.

If we can prove this probability is 0 for all δ > 0, that would be RH!

Large deviation theory gives exponential bounds on tail probabilities.
""")

# Compute distribution of |M(x)| / √x for various x
print("\nDistribution of M(x)/√x across different x:")
print("-" * 50)
print(f"{'x':>10} | {'M(x)':>10} | {'M/√x':>12} | {'|M|/√x':>12}")
print("-" * 50)

m_over_sqrt_x = []
for x_test in [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]:
    _, Q, M = get_stats(x_test)
    ratio = M / np.sqrt(x_test)
    m_over_sqrt_x.append((x_test, M, ratio))
    print(f"{x_test:>10} | {M:>+10} | {ratio:>+12.4f} | {abs(ratio):>12.4f}")

# Statistics of M/√x
ratios = [r[2] for r in m_over_sqrt_x]
print(f"\nStatistics of M(x)/√x:")
print(f"  Mean = {np.mean(ratios):+.4f}")
print(f"  Std = {np.std(ratios):.4f}")
print(f"  Max |M/√x| = {max(abs(r) for r in ratios):.4f}")

print("""
OBSERVATION:
|M(x)|/√x appears to be O(1), consistent with RH.
But this is numerical evidence, not a proof.

To prove RH via large deviations, we would need:
  P(|M(x)| > C√x · log(x)^k) → 0 for all C, k

This requires understanding the TAIL of the distribution.
""")

# =============================================================================
# APPROACH 3: SELF-CONSISTENCY / CONTRADICTION
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 3: SELF-CONSISTENCY / CONTRADICTION")
print("=" * 80)

print("""
IDEA: Assume RH is FALSE. Derive a contradiction.

If there exists a zero ρ₀ = β₀ + iγ₀ with β₀ > 1/2:

1. The explicit formula gives:
   M(x) = -2 + x^{ρ₀}/(ρ₀ζ'(ρ₀)) + Σ_{ρ≠ρ₀} x^ρ/(ρζ'(ρ)) + O(1)

2. The term x^{ρ₀} has size x^{β₀} > x^{1/2}

3. For M(x) to remain O(√x), this term must cancel with others

4. But zeros come in conjugate pairs: if ρ₀, then also ρ₀*
   These would REINFORCE, not cancel!

Let's explore this more carefully...
""")

# The functional equation gives ρ → 1-ρ pairing
# If ρ = β + iγ is a zero, so is 1 - β - iγ (different zero)
# And also β - iγ (conjugate)

# For a zero off the critical line with β > 1/2:
# - ρ = β + iγ (the zero)
# - ρ* = β - iγ (conjugate zero)
# - 1-ρ = (1-β) - iγ (functional equation pair)
# - (1-ρ)* = (1-β) + iγ (conjugate of that)

print("""
ZERO STRUCTURE:
===============
If ρ = β + iγ is a zero with β > 1/2:
  - ρ = β + iγ (the zero)
  - ρ* = β - iγ (conjugate, also a zero)
  - 1-ρ = (1-β) - iγ (functional equation pair, also a zero)
  - (1-ρ)* = (1-β) + iγ (conjugate of that)

So zeros come in QUADRUPLES off the critical line.

CONTRIBUTION TO M(x):
=====================
The pair {ρ, ρ*} contributes:
  x^ρ/(ρζ'(ρ)) + x^{ρ*}/(ρ*ζ'(ρ*))
  = 2 Re(x^ρ/(ρζ'(ρ)))
  = 2 x^β Re(e^{iγ log x}/(ρζ'(ρ)))
  ~ x^β cos(γ log x + φ)

This oscillates but has amplitude ~x^β.

PROBLEM WITH CONTRADICTION:
===========================
The functional equation pairs at 1-β give terms ~x^{1-β}.
For β > 1/2, we have 1-β < 1/2.

The large term ~x^β oscillates. It's possible (though unlikely)
that these oscillations somehow average out in M(x).

Without knowing the EXACT values of ζ'(ρ), we can't prove
the terms don't cancel.
""")

# =============================================================================
# APPROACH 4: FUNCTIONAL EQUATION IN GENERATING FUNCTION
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 4: FUNCTIONAL EQUATION SYMMETRY")
print("=" * 80)

print("""
IDEA: The functional equation ζ(s) = χ(s)ζ(1-s) creates symmetry.

How does this symmetry appear in our generating function framework?

OBSERVATION:
============
G(z, x) = Σ_w S_w(x) z^w

At z = -1: G(-1,x) = M(x) = Σ(-1)^w S_w(x)
At z = +1: G(+1,x) = Q(x) = Σ S_w(x)

The ratio G(-1,x)/G(1,x) = M(x)/Q(x) is what we want to bound.

FUNCTIONAL EQUATION CONNECTION:
===============================
The zeros of ζ(s) control M(x) via the explicit formula.
The functional equation pairs ρ ↔ 1-ρ.

On the critical line (β = 1/2), both ρ and 1-ρ have the same
real part, so their contributions have the same amplitude.

Off the critical line, the amplitudes differ.
""")

# Let's look at the generating function more carefully
x = 100000
S, Q, M = get_stats(x)

print(f"\nGenerating function analysis at x = {x:,}:")
print("-" * 60)

# G(z) on unit circle
for theta in [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]:
    z = np.exp(1j * theta)
    G_z = sum(S.get(w, 0) * (z ** w) for w in S)
    print(f"  G(e^{{i·{theta/np.pi:.2f}π}}) = {abs(G_z):>10.2f} ∠ {np.angle(G_z):>+.4f}")

# =============================================================================
# APPROACH 5: CONCENTRATION INEQUALITIES
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 5: CONCENTRATION INEQUALITIES")
print("=" * 80)

print("""
IDEA: Modern probability has powerful concentration bounds.

If we view M(x) = Σ μ(n) as a sum of bounded random variables,
can we apply concentration inequalities?

CHALLENGE:
==========
The μ(n) are NOT independent. They're deterministic!

But we can think of choosing n uniformly from [1, x] and looking at μ(n).
Then μ(n) is a random variable with:
  - P(μ(n) = +1) = Q_even(x) / x
  - P(μ(n) = -1) = Q_odd(x) / x
  - P(μ(n) = 0) = 1 - Q(x)/x

The sum M(x) = Σ μ(n) is then a sum over this process.

BOUNDED DIFFERENCES:
====================
For i.i.d. bounded random variables X_i ∈ [-1, 1]:
  P(|Σ X_i - E[Σ X_i]| > t) ≤ 2 exp(-t²/(2n))

This gives √n concentration, which matches RH!

But μ(n) are NOT independent...
""")

# Check if μ(n) has any independence structure
print("\nChecking correlation structure of μ(n):")

# Correlation between μ(n) and μ(n+1)
corr_data = []
for n in range(2, 10000):
    if mu[n] != 0 and mu[n+1] != 0:
        corr_data.append((mu[n], mu[n+1]))

if corr_data:
    mu_n = [c[0] for c in corr_data]
    mu_n1 = [c[1] for c in corr_data]
    corr = np.corrcoef(mu_n, mu_n1)[0, 1]
    print(f"  Correlation(μ(n), μ(n+1)) = {corr:.6f}")

# Correlation for coprime n, m
print("\nCorrelation for coprime pairs:")
coprime_corr = []
for n in range(2, 1000):
    for m in range(n+1, 1000):
        if math.gcd(n, m) == 1 and mu[n] != 0 and mu[m] != 0:
            coprime_corr.append((mu[n], mu[m]))

if coprime_corr:
    mu_n = [c[0] for c in coprime_corr[:10000]]
    mu_m = [c[1] for c in coprime_corr[:10000]]
    corr = np.corrcoef(mu_n, mu_m)[0, 1]
    print(f"  Correlation(μ(n), μ(m)) for gcd=1 = {corr:.6f}")

# =============================================================================
# APPROACH 6: INFORMATION-THEORETIC BOUNDS
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 6: INFORMATION-THEORETIC BOUNDS")
print("=" * 80)

print("""
IDEA: The entropy of the ω distribution might give constraints.

For a Poisson(λ) distribution:
  H(Poisson) ≈ (1/2) log(2πeλ) for large λ

If the actual distribution has LOWER entropy than Poisson,
it means the distribution is more concentrated.
""")

x = 100000
S, Q, M = get_stats(x)
lam = np.log(np.log(x))

# Compute entropy of actual distribution
p_actual = np.array([S.get(w, 0) / Q for w in range(max(S.keys()) + 1)])
p_actual = p_actual[p_actual > 0]  # Remove zeros
H_actual = -np.sum(p_actual * np.log(p_actual))

# Entropy of Poisson(λ)
p_poisson = np.array([lam**w * np.exp(-lam) / math.factorial(w) for w in range(20)])
p_poisson = p_poisson[p_poisson > 1e-10]
H_poisson = -np.sum(p_poisson * np.log(p_poisson))

print(f"\nEntropy comparison at x = {x:,}:")
print(f"  H(actual) = {H_actual:.4f} nats")
print(f"  H(Poisson) = {H_poisson:.4f} nats")
print(f"  Ratio = {H_actual / H_poisson:.4f}")
print(f"  Entropy reduction = {H_poisson - H_actual:.4f} nats")

print("""
OBSERVATION:
The actual distribution has LOWER entropy than Poisson,
confirming it's more concentrated.

But entropy bounds don't directly give variance bounds.
""")

# =============================================================================
# APPROACH 7: EXTREMAL COMBINATORICS
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 7: EXTREMAL COMBINATORICS")
print("=" * 80)

print("""
IDEA: What's the MAXIMUM possible value of |M(x)|/√x?

If we could prove max |M(x)|/√x is bounded, that would be RH!

APPROACH:
=========
Consider all possible assignments of μ(n) ∈ {-1, 0, +1}
subject to:
  1. μ(n) = 0 if n has a squared factor
  2. μ is multiplicative: μ(mn) = μ(m)μ(n) for gcd(m,n) = 1
  3. μ(p) = -1 for all primes p

These constraints DETERMINE μ completely!
The question is: given these constraints, what's max |M(x)|?

PROBLEM:
========
The constraints determine μ(n) uniquely, so there's no optimization.
The value M(x) is what it is.
""")

# But we can ask: among random multiplicative functions, what's typical?
print("\nComparing to random multiplicative functions:")
print("(Harper's result: E|Σf(n)| ≈ √x / (log log x)^{1/4})")
print()

# For μ specifically:
lam = np.log(np.log(100000))
harper_prediction = np.sqrt(100000) / (lam ** 0.25)
actual_M = abs(M)

print(f"At x = 100,000:")
print(f"  |M(x)| = {actual_M}")
print(f"  √x = {np.sqrt(100000):.1f}")
print(f"  Harper prediction: √x / (log log x)^{{1/4}} = {harper_prediction:.1f}")
print(f"  Actual / Harper = {actual_M / harper_prediction:.4f}")

# =============================================================================
# APPROACH 8: THE TWIN PRIME CONNECTION
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 8: TWIN PRIME CONNECTION")
print("=" * 80)

print("""
IDEA: RH is connected to many other conjectures. Maybe we can
find a SIMPLER equivalent that's easier to prove?

TWIN PRIME CONJECTURE is NOT equivalent to RH, but both
involve the distribution of primes.

What about GOLDBACH? ALSO not equivalent.

But there ARE simple equivalents:

EQUIVALENT TO RH:
=================
1. M(x) = O(x^{1/2+ε}) for all ε > 0 [classical]

2. Σ_{n≤x} μ(n)/n = O(x^{-1/2+ε}) [our formulation]

3. |P_even - P_odd| = O(x^{-1/2+ε}) [our formulation]

4. π(x) - Li(x) = O(√x log x) [prime counting]

5. The Chebyshev bias disappears in a precise sense

None of these are obviously easier to prove than RH itself.
""")

# =============================================================================
# APPROACH 9: NUMERICAL PATTERNS
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 9: SEARCHING FOR PATTERNS")
print("=" * 80)

print("""
IDEA: Look for numerical patterns that might suggest a proof.

Let's examine M(x)/√x more carefully...
""")

# Detailed analysis of M(x)/√x
print("\nDetailed behavior of M(x)/√x:")
print("-" * 70)
print(f"{'x':>10} | {'M(x)':>8} | {'M/√x':>10} | {'M/√x log':>12} | {'Phase':>10}")
print("-" * 70)

# The "phase" comes from the first zeta zero γ₁ ≈ 14.13
gamma_1 = 14.134725

for x_test in range(1000, 100001, 1000):
    _, Q, M_test = get_stats(x_test)
    ratio = M_test / np.sqrt(x_test)
    ratio_log = M_test / (np.sqrt(x_test) * np.log(x_test))
    phase = (gamma_1 * np.log(x_test)) % (2 * np.pi)
    if x_test % 10000 == 0:
        print(f"{x_test:>10} | {M_test:>+8} | {ratio:>+10.4f} | {ratio_log:>+12.6f} | {phase:>10.4f}")

# =============================================================================
# APPROACH 10: THE MÖBIUS RANDOMNESS LAW
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 10: MÖBIUS RANDOMNESS LAW")
print("=" * 80)

print("""
THE MÖBIUS RANDOMNESS LAW (Conjecture):
=======================================
μ(n) behaves like a random ±1 sequence in many ways.

Specifically, for "nice" functions f:
  Σ μ(n) f(n) = o(Σ |f(n)|)

This is a form of "pseudorandomness."

PROVED CASES:
=============
- f(n) = 1: This is M(x) = o(x), which is TRUE (PNT)
- f(n) = e^{2πinα} for irrational α: TRUE (Davenport)
- f(n) = n^{it}: TRUE (Vinogradov-Korobov for t small)

WHAT WOULD PROVE RH:
====================
If we could prove μ(n) is "random enough" that
  Σ μ(n) = O(√n) with high probability
then we'd have RH.

But "random enough" is exactly what we can't prove!
""")

# =============================================================================
# FINAL SYNTHESIS
# =============================================================================

print("\n" + "=" * 80)
print("FINAL SYNTHESIS: NEW APPROACHES")
print("=" * 80)

print("""
SUMMARY OF NEW APPROACHES:
==========================

1. HIGHER MOMENTS
   - Actual moments differ from Poisson
   - Skewness and kurtosis show concentration
   - But moments don't give direct bound on M(x)

2. LARGE DEVIATIONS
   - |M(x)|/√x appears bounded
   - But we can't prove tail bounds without RH

3. CONTRADICTION
   - Off-line zeros would create large oscillations
   - But can't prove they don't cancel without knowing ζ'(ρ)

4. FUNCTIONAL EQUATION
   - Creates ρ ↔ 1-ρ symmetry
   - On critical line: equal contributions
   - Off critical line: asymmetric
   - Doesn't directly give contradiction

5. CONCENTRATION INEQUALITIES
   - Would give √n bounds if μ(n) were independent
   - But μ(n) is deterministic, not independent

6. INFORMATION THEORY
   - Actual entropy < Poisson entropy
   - Confirms concentration
   - Doesn't give direct variance bound

7. EXTREMAL COMBINATORICS
   - μ is uniquely determined by constraints
   - No optimization possible

8. CONNECTIONS TO OTHER PROBLEMS
   - All known equivalents are equally hard

9. NUMERICAL PATTERNS
   - Phase structure visible (from γ₁)
   - Doesn't suggest proof method

10. MÖBIUS RANDOMNESS
    - μ behaves "randomly" in many ways
    - But not random enough to apply probabilistic bounds

CONCLUSION:
===========
Every new approach either:
- Reduces to known methods (→ ζ zeros)
- Requires independence we don't have
- Gives evidence but not proof

The fundamental obstruction persists:
μ(n) is DETERMINISTIC, and its statistics are controlled by ζ zeros.

We need genuinely new mathematics to prove RH.
""")

print("=" * 80)
print("NEW APPROACHES ANALYSIS COMPLETE")
print("=" * 80)
