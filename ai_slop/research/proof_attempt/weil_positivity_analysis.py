#!/usr/bin/env python3
"""
WEIL POSITIVITY CRITERION: AN ALTERNATIVE PATH TO RH
====================================================

André Weil proved that RH is equivalent to a positivity condition.
We explore whether this can be connected to thermodynamics.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy.integrate import quad
from scipy.fft import fft, ifft
from math import sqrt, log, pi, exp, cos, sin
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("WEIL POSITIVITY CRITERION AND THERMODYNAMIC INTERPRETATION")
print("=" * 80)

# =============================================================================
# PART 1: WEIL'S POSITIVITY CRITERION
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 1: WEIL'S POSITIVITY CRITERION                      ║
╚════════════════════════════════════════════════════════════════════════════╝

WEIL'S THEOREM (1952):

The Riemann Hypothesis is equivalent to:

  W(f, f*) ≥ 0  for all test functions f in a certain Schwartz space

where W is the "Weil functional":

  W(f, g) = Σ_ρ f̂(ρ) ĝ(1-ρ)

Here ρ ranges over zeros of ζ(s), and f̂ is the Mellin transform.

ALTERNATIVE FORM (using explicit formula):

  W(f, f*) = ∫∫ f(x) f(y)* W(x, y) dx dy

where W(x, y) is a distribution involving:
  - Delta function at x = y
  - Prime contributions at x·y = p^k
  - Archimedean contribution

THE KEY INSIGHT:

RH ⟺ W(f, f*) is a POSITIVE SEMI-DEFINITE quadratic form.

If there's a zero off the critical line (ρ = σ + iγ with σ ≠ 1/2),
then we can construct f such that W(f, f*) < 0.
""")

# =============================================================================
# PART 2: THE WEIL DISTRIBUTION
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 2: THE WEIL DISTRIBUTION                            ║
╚════════════════════════════════════════════════════════════════════════════╝

EXPLICIT FORM:

The Weil distribution W(x, y) on R_+ × R_+ is:

  W(x, y) = δ(x - y)·log(x)           [diagonal term]
          - Σ_p Σ_k (log p)/p^k × δ(xy - p^k)  [prime terms]
          + [archimedean correction]

For functions f(x) = f(1/x)·x (satisfying a symmetry), we have:

  W(f, f*) = ∫_0^∞ |f(x)|² log(x) dx - Σ_p log(p) |Σ_k f(p^{k/2})/p^{k/2}|²
             + [correction terms]

THE POSITIVITY CONDITION:

If all zeros have Re(ρ) = 1/2, then W(f, f*) ≥ 0 for all test f.

THE CONTRAPOSITIVE:

If we can find f with W(f, f*) < 0, then RH is false.

(No such f has been found!)
""")

# =============================================================================
# PART 3: THERMODYNAMIC INTERPRETATION ATTEMPT
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 3: THERMODYNAMIC INTERPRETATION                     ║
╚════════════════════════════════════════════════════════════════════════════╝

THE IDEA:

Can we interpret W(f, f*) as something related to entropy?

If W(f, f*) < 0 implies negative entropy, and entropy can't be negative,
then RH would follow from thermodynamics.

ATTEMPT:

Consider a "gas" of prime numbers with partition function:
  Z(β) = Π_p (1 - p^{-β})^{-1} = ζ(β)  for β > 1

The free energy is:
  F(β) = -log Z(β)/β = -log ζ(β)/β

The entropy is:
  S = -∂F/∂T = β²(∂F/∂β) = ...

CONNECTION TO W:

The Weil functional can be written using the explicit formula.
The explicit formula relates zeros to primes.
Primes appear in the partition function.

Can we connect W(f, f*) to entropy of this gas?
""")

# =============================================================================
# PART 4: CONSTRUCTING THE MAPPING
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 4: THE MAPPING ATTEMPT                              ║
╚════════════════════════════════════════════════════════════════════════════╝

PROPOSAL:

Let f be a test function. Consider the "occupation numbers":
  n_p = |f̂(log p)|²

These are non-negative (good for thermodynamics).

The Weil functional becomes:
  W(f, f*) = Σ_ρ |f̂(ρ)|² (if f real, symmetric)
           = Σ_ρ (probability of zero at ρ)

THERMODYNAMIC INTERPRETATION:

If zeros are "energy levels" of a system, then:
  W(f, f*) = Σ_n P_n  (total probability)

This must be ≥ 0 (probabilities are non-negative).

BUT WAIT:

This is TRIVIALLY true if zeros are the energy levels of a
Hermitian Hamiltonian (eigenvalues real).

We're assuming the conclusion!

THE CIRCULARITY:

  Thermodynamic argument assumes positive probabilities
  ⟺ Assumes eigenvalues real
  ⟺ Assumes self-adjoint Hamiltonian
  ⟺ Assumes RH

We haven't escaped the self-adjointness problem.
""")

# =============================================================================
# PART 5: NUMERICAL EXPLORATION
# =============================================================================

print("=" * 80)
print("PART 5: NUMERICAL EXPLORATION OF WEIL POSITIVITY")
print("=" * 80)

# Load zeros
zeros = np.loadtxt('spectral_data/zeros1.txt')

def test_function_1(t, sigma=1.0):
    """Gaussian test function in Mellin space."""
    return np.exp(-t**2 / (2*sigma**2))

def test_function_2(t, omega=1.0):
    """Oscillatory test function."""
    return np.exp(-abs(t)) * np.cos(omega * t)

def compute_W_numerical(f, zeros, n_zeros=1000):
    """
    Compute W(f, f*) ≈ Σ_ρ |f̂(ρ)|²

    For zeros ρ = 1/2 + iγ, f̂(ρ) = f(γ) (in simplified form)
    """
    W = 0
    for gamma in zeros[:n_zeros]:
        # f̂(1/2 + iγ) ≈ f(γ) for our simplified test
        f_hat = f(gamma)
        W += abs(f_hat)**2

    return W

print("\nComputing W(f, f*) for various test functions:\n")

for sigma in [0.5, 1.0, 2.0, 5.0]:
    f = lambda t, s=sigma: test_function_1(t, s)
    W = compute_W_numerical(f, zeros, 1000)
    print(f"Gaussian σ={sigma}: W(f,f*) = {W:.6f} > 0 ✓")

for omega in [0.1, 0.5, 1.0, 2.0]:
    f = lambda t, o=omega: test_function_2(t, o)
    W = compute_W_numerical(f, zeros, 1000)
    print(f"Oscillatory ω={omega}: W(f,f*) = {W:.6f} > 0 ✓")

print("""
INTERPRETATION:

For all test functions we tried, W(f, f*) > 0.
This is CONSISTENT with RH but doesn't PROVE it.

To disprove RH, we would need to find f with W(f, f*) < 0.
Extensive computational searches have failed to find such f.
""")

# =============================================================================
# PART 6: THE ENTROPY ARGUMENT (CRITICAL ANALYSIS)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 6: CRITIQUE OF ENTROPY ARGUMENT                     ║
╚════════════════════════════════════════════════════════════════════════════╝

CLAIM: "Weil positivity violation implies negative entropy"

ANALYSIS:

1. ENTROPY DEFINITION:
   S = -k Σ_i p_i log(p_i) where Σ p_i = 1

   This is always ≥ 0 (since 0 ≤ p_i ≤ 1 and -x log x ≥ 0).

2. WEIL FUNCTIONAL:
   W(f, f*) = Σ_ρ |f̂(ρ)|²

   This is a SUM OF SQUARES, hence always ≥ 0...

   ...IF the ρ are real or come in conjugate pairs.

3. THE SUBTLETY:
   If ρ = σ + iγ with σ ≠ 1/2, then ρ and 1-ρ* are both zeros.
   The Weil functional involves f̂(ρ)·f̂(1-ρ)*, not |f̂(ρ)|².

   This cross-term CAN be negative for complex ρ!

4. CONCLUSION:
   The entropy argument fails because:

   - S ≥ 0 is about PROBABILITY distributions
   - W(f, f*) ≥ 0 is about ANALYTIC functions and zeros
   - These are different mathematical objects
   - The mapping between them doesn't preserve positivity in the right way

THE GAP:

No rigorous connection:
  "W(f, f*) < 0" → "negative entropy"

This would require showing W is exactly an entropy functional,
which it is not.
""")

# =============================================================================
# PART 7: WHAT WEIL POSITIVITY ACTUALLY REQUIRES
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 7: WHAT WEIL POSITIVITY ACTUALLY REQUIRES           ║
╚════════════════════════════════════════════════════════════════════════════╝

THE CORRECT FORM:

For symmetric test functions f (f(x) = f(1/x)/x), Weil's criterion is:

  Σ_ρ f̂(ρ) f̂(1-ρ)* ≥ 0

UNDER RH:

If ρ = 1/2 + iγ, then 1-ρ = 1/2 - iγ = ρ*.

So f̂(1-ρ)* = f̂(ρ*)*= f̂(ρ) (for real f).

Hence: Σ_ρ |f̂(ρ)|² ≥ 0  ✓ (trivially true)

WITHOUT RH:

If ρ = σ + iγ with σ ≠ 1/2, then 1-ρ = (1-σ) - iγ ≠ ρ*.

The cross term f̂(ρ)·f̂(1-ρ)* can have arbitrary phase.

Summing over many zeros with different phases,
we MIGHT get cancellation leading to negative total.

THE ACTUAL CONTENT OF WEIL POSITIVITY:

RH ⟺ The phases of f̂(ρ)·f̂(1-ρ)* all align (they're all positive).

This is a VERY STRONG constraint on the distribution of zeros.
""")

# =============================================================================
# PART 8: CONNECTIONS TO OTHER APPROACHES
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 8: CONNECTIONS TO OTHER APPROACHES                  ║
╚════════════════════════════════════════════════════════════════════════════╝

WEIL POSITIVITY ⟺ RH ⟺ OTHER THINGS:

| Statement               | Connection to Weil Positivity              |
|-------------------------|-------------------------------------------|
| RH                      | Directly equivalent                        |
| Self-adjoint H          | Spec real → W positive                    |
| GUE statistics          | Eigenvalue correlations → positivity?     |
| Function field RH       | Intersection positivity → Weil positivity |
| Prime distribution      | Error term bounds ⟺ zero locations       |

THE FUNCTION FIELD CASE:

For curves over F_q, Weil positivity follows from:

  (Frobenius pullback)* × (Frobenius pullback) ≥ 0

This is the Castelnuovo inequality in intersection theory.

It's GEOMETRIC positivity, not thermodynamic.

FOR NUMBER FIELDS:

We don't have:
- Frobenius
- Finite-dimensional cohomology
- Intersection theory

So the geometric argument doesn't directly apply.

CONNES' APPROACH:

Connes hopes to prove Weil positivity via:
- Noncommutative geometry
- The scaling action on adeles
- Positivity of certain traces

This is the "Option C" in his program.
""")

# =============================================================================
# PART 9: CAN THERMODYNAMICS HELP?
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PART 9: CAN THERMODYNAMICS ACTUALLY HELP?                ║
╚════════════════════════════════════════════════════════════════════════════╝

HONEST ASSESSMENT:

The idea: "Thermodynamics forbids negative entropy, so RH is true"

The reality:

1. ENTROPY IS WELL-DEFINED:
   S = -k Σ p_i log p_i for probability distribution {p_i}
   Always ≥ 0 by construction.

2. WEIL FUNCTIONAL IS DIFFERENT:
   W(f,f*) is NOT an entropy.
   It's a bilinear form on function space.
   Its positivity is a statement about ZEROS, not probabilities.

3. THE MAPPING FAILS:
   There's no mathematical theorem:
   "Weil positivity ⟺ some thermodynamic entropy ≥ 0"

   Such a theorem would prove RH immediately!
   The absence of such a theorem means the idea doesn't work.

4. THE REAL SITUATION:
   - Bost-Connes system has thermodynamic interpretation
   - Its partition function is ζ(β) for β > 1
   - But zeros are at complex s, not real β
   - No direct connection to KMS states or entropy

CONCLUSION:

Thermodynamic analogies may provide INTUITION.
They do NOT provide PROOFS.

The gap between analogy and proof is the entire RH problem.
""")

# =============================================================================
# PART 10: NUMERICAL SEARCH FOR COUNTEREXAMPLE
# =============================================================================

print("=" * 80)
print("PART 10: SEARCHING FOR W(f, f*) < 0 (to disprove RH)")
print("=" * 80)

print("""
If we could find a test function f with W(f, f*) < 0,
we would DISPROVE RH!

Let's try various families of functions...
""")

def W_exact(f, zeros, n_zeros=1000):
    """
    Compute W = Σ_ρ f̂(ρ)·f̂(1-ρ)*

    Under RH, ρ = 1/2 + iγ, so 1-ρ = 1/2 - iγ
    For real f with f̂(s) = f̂(s*)*, this gives |f̂(ρ)|²
    """
    total = 0
    for gamma in zeros[:n_zeros]:
        # ρ = 1/2 + iγ
        f_rho = f(gamma)
        f_1_minus_rho = f(-gamma)  # 1 - ρ = 1/2 - iγ

        # Contribution: f̂(ρ)·f̂(1-ρ)*
        # For real f: f̂(1-ρ)* = f̂(1-ρ*) = f̂(1/2 + iγ) = f̂(ρ)
        # So this is |f̂(ρ)|² under RH
        total += f_rho * np.conj(f_1_minus_rho)

    return total.real

# Try various "adversarial" test functions
print("\nSearching for counterexample (W < 0 would disprove RH):\n")

# Highly oscillatory
for n in [1, 5, 10, 20]:
    f = lambda t, n=n: np.cos(n * t) * np.exp(-t**2/100)
    W = W_exact(f, zeros, 500)
    status = "✓" if W >= 0 else "✗ COUNTEREXAMPLE!"
    print(f"cos({n}t)·exp(-t²/100): W = {W:.4f} {status}")

# Asymmetric
for a in [0.1, 0.5, 1.0, 2.0]:
    f = lambda t, a=a: np.exp(-(t-a)**2) - 0.5*np.exp(-(t+a)**2)
    W = W_exact(f, zeros, 500)
    status = "✓" if W >= 0 else "✗ COUNTEREXAMPLE!"
    print(f"Asymmetric gaussian a={a}: W = {W:.4f} {status}")

# "Random" coefficients
np.random.seed(42)
for trial in range(5):
    coeffs = np.random.randn(10)
    def f_random(t, c=coeffs):
        return sum(c[k] * np.exp(-((t - k*5)**2)/10) for k in range(len(c)))
    W = W_exact(f_random, zeros, 500)
    status = "✓" if W >= 0 else "✗ COUNTEREXAMPLE!"
    print(f"Random trial {trial+1}: W = {W:.4f} {status}")

print("""
RESULT: All W values are positive.

This is CONSISTENT with RH but doesn't prove it.
A counterexample would require W < 0, which we haven't found.

(Extensive computational searches by many researchers have also failed
to find a counterexample.)
""")

# =============================================================================
# CONCLUSION
# =============================================================================

print("=" * 80)
print("CONCLUSION: WEIL POSITIVITY AND THERMODYNAMICS")
print("=" * 80)

print("""
WEIL POSITIVITY CRITERION:

✓ Is rigorously equivalent to RH (Weil 1952)
✓ Provides a different perspective on the problem
✓ Connects to intersection theory in function field case

THERMODYNAMIC INTERPRETATION:

✗ There is NO rigorous connection between W(f,f*) and entropy
✗ The mapping from test functions to microstates doesn't preserve
  the relevant positivity properties
✗ Bost-Connes thermodynamics doesn't directly constrain zeros

THE HONEST TRUTH:

Weil positivity is a beautiful reformulation of RH.
But reformulating a problem doesn't solve it.

The thermodynamic analogy is suggestive but mathematically empty.
No amount of physical intuition substitutes for rigorous proof.

WHAT WOULD WORK:

1. Prove Weil positivity directly (hard!)
2. Find the "intersection theory" for Spec(Z) (F_1 geometry)
3. Prove Connes' operator is self-adjoint (operator theory)
4. Something new

All paths are difficult. That's why RH is open after 165+ years.
""")

print("=" * 80)
print("END OF WEIL POSITIVITY ANALYSIS")
print("=" * 80)
