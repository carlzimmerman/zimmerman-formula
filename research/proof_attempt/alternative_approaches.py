"""
ALTERNATIVE APPROACHES TO BREAK THE CIRCULARITY
=================================================

The algebraic pairing doesn't break the circularity.
What OTHER approaches might work?

This investigation explores unconventional ideas.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, factorint, primerange, isprime
from collections import defaultdict
import math

print("=" * 80)
print("ALTERNATIVE APPROACHES TO BREAK THE CIRCULARITY")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 100000

print("Computing...")
M_array = [0] * (MAX_N + 1)
mu_array = [0] * (MAX_N + 1)
cumsum = 0
for n in range(1, MAX_N + 1):
    mu_array[n] = int(mobius(n))
    cumsum += mu_array[n]
    M_array[n] = cumsum

def M(x):
    x = int(x)
    if x < 1:
        return 0
    if x <= MAX_N:
        return M_array[x]
    return 0

def mu(n):
    if n <= MAX_N:
        return mu_array[n]
    return int(mobius(n))

primes = list(primerange(2, MAX_N))
print("Done.")

# =============================================================================
# APPROACH 1: PROBABILISTIC / RANDOM WALK
# =============================================================================

print("""

================================================================================
APPROACH 1: PROBABILISTIC / RANDOM WALK
================================================================================

IDEA: Prove μ(n) behaves "randomly enough" for CLT to apply.

If μ(n) were i.i.d. random ±1 (among squarefree n), then:
  M(x) = Σ μ(n) would be a random walk
  |M(x)| ~ √(# squarefree ≤ x) ~ √(6x/π²) ~ √x

The question: Can we prove sufficient "randomness" without ζ zeros?

Key observation: μ(n) is DETERMINISTIC, not random!
But it might be "pseudorandom" in a provable sense.

SARNAK CONJECTURE: For any "deterministic" sequence a(n),
  Σ μ(n)a(n) = o(x)

This says μ is orthogonal to all "structured" sequences.
If true, it implies RH-like behavior.

STATUS: Open conjecture, would imply RH.
""")

# Check "randomness" of μ by computing autocorrelation
print("Autocorrelation of μ(n) among squarefree:")
sqfree = [n for n in range(1, 10001) if mu(n) != 0]
mu_values = [mu(n) for n in sqfree]

for lag in [1, 2, 3, 5, 10]:
    if lag < len(mu_values):
        corr = np.corrcoef(mu_values[:-lag], mu_values[lag:])[0, 1]
        print(f"  Lag {lag}: correlation = {corr:.6f}")

# =============================================================================
# APPROACH 2: ENTROPY / INFORMATION THEORY
# =============================================================================

print("""

================================================================================
APPROACH 2: ENTROPY / INFORMATION THEORY
================================================================================

IDEA: The distribution of μ(n) values might be constrained by entropy.

Among squarefree n ≤ x:
  - About half have μ(n) = +1 (even ω)
  - About half have μ(n) = -1 (odd ω)

This is maximum entropy for a ±1 distribution!

QUESTION: Does maximum entropy imply |M(x)| = O(√x)?

For i.i.d. ±1 with p(+1) = p(-1) = 1/2:
  Var(sum) = n × Var(single) = n × 1 = n
  Std(sum) = √n

So maximum entropy → O(√n) behavior for random sums.

But μ(n) isn't independent! The constraint is:
  μ(nm) = μ(n)μ(m) for gcd(n,m) = 1

Does this constraint reduce variance below √n? Or keep it at √n?
""")

# Check: Is Var(M(x)) ~ x?
x_values = list(range(1000, 50001, 100))
M_values = [M(x) for x in x_values]
M_squared = [m*m for m in M_values]

# Fit Var ~ x^alpha
log_x = np.log(x_values)
log_M2 = np.log([max(1, m2) for m2 in M_squared])

# Linear regression
slope, intercept = np.polyfit(log_x, log_M2, 1)

print(f"Empirical: log(M²) ≈ {slope:.4f} × log(x) + {intercept:.4f}")
print(f"This suggests M² ~ x^{slope:.4f}, so |M| ~ x^{slope/2:.4f}")
print(f"RH predicts |M| ~ x^0.5, i.e., slope = 1.0")

# =============================================================================
# APPROACH 3: DYNAMICAL SYSTEMS / ERGODIC THEORY
# =============================================================================

print("""

================================================================================
APPROACH 3: DYNAMICAL SYSTEMS / ERGODIC THEORY
================================================================================

IDEA: View μ(n) as arising from a dynamical system.

Consider the "Möbius flow" on the space of integers:
  - Each prime p defines a "direction"
  - Multiplying by p moves in that direction
  - μ(n) = (-1)^(# of steps taken)

The SARNAK CONJECTURE connects this to:
  - Möbius orthogonality to zero-entropy systems
  - Chowla conjecture on correlations

BOURGAIN-SARNAK-ZIEGLER (2013): Partial results on Möbius randomness.

If we could prove μ is "sufficiently mixing", we'd get bounds.
But current ergodic methods don't give O(√x).
""")

# =============================================================================
# APPROACH 4: SPECTRAL / OPERATOR THEORY
# =============================================================================

print("""

================================================================================
APPROACH 4: SPECTRAL / OPERATOR THEORY (HILBERT-PÓLYA)
================================================================================

IDEA: Find a self-adjoint operator H whose eigenvalues are ζ zeros.

If such H exists:
  - Eigenvalues are real (self-adjoint)
  - ζ(1/2 + iγ) = 0 ⟹ γ is eigenvalue
  - RH follows from spectral theory!

APPROACHES:
1. BERRY-KEATING: H = xp + px (position × momentum)
2. CONNES: Noncommutative geometry, "absorption spectrum"
3. SIERRA-TOWNSEND: Hamiltonian from xp

The challenge: Constructing H rigorously.

OUR FINDING: The generating function G(z,x) = Σ S_w z^w has roots.
Could these roots be eigenvalues of some operator?
""")

# Analyze the generating function structure
def compute_S_w(x, max_w=15):
    """Count squarefree n ≤ x by number of prime factors."""
    S = defaultdict(int)
    for n in range(1, x + 1):
        if mu(n) != 0:
            w = len(factorint(n))
            S[w] += 1
    return S

x = 10000
S_w = compute_S_w(x)
print(f"\nS_w distribution at x = {x}:")
for w in range(8):
    print(f"  S_{w} = {S_w[w]}")

# The generating function G(z) = Σ S_w z^w
# G(1) = Q(x), G(-1) = M(x)
G_1 = sum(S_w.values())
G_minus1 = sum((-1)**w * S_w[w] for w in S_w)
print(f"\nG(1) = {G_1} (should be Q(x) = {sum(1 for n in range(1, x+1) if mu(n) != 0)})")
print(f"G(-1) = {G_minus1} (should be M(x) = {M(x)})")

# =============================================================================
# APPROACH 5: ALGEBRAIC GEOMETRY (WEIL CONJECTURES)
# =============================================================================

print("""

================================================================================
APPROACH 5: ALGEBRAIC GEOMETRY (WEIL CONJECTURES)
================================================================================

IDEA: RH for function fields was proved by Deligne (1974).

For curves over finite fields F_q:
  - The zeta function has all zeros on Re(s) = 1/2
  - Proof uses étale cohomology and Lefschetz trace formula

QUESTION: Can this be "lifted" to the integers?

CHALLENGES:
1. ℤ is not a finite field
2. The "curve" would be Spec(ℤ), which behaves differently
3. No clear cohomological interpretation for Riemann ζ

ARAKELOV GEOMETRY: Attempts to treat ℤ like a curve.
But a full proof hasn't emerged from this direction.

The Weil approach gives HOPE but no direct path.
""")

# =============================================================================
# APPROACH 6: COMBINATORIAL CONSTRAINTS
# =============================================================================

print("""

================================================================================
APPROACH 6: COMBINATORIAL CONSTRAINTS
================================================================================

IDEA: The multiplicative structure might force bounds combinatorially.

KEY CONSTRAINT: μ(nm) = μ(n)μ(m) for gcd(n,m) = 1

This means:
  - μ is determined by μ(p) = -1 for all primes
  - The ω(n) values are constrained by factorization

QUESTION: Does this constraint FORCE |M(x)| = O(√x)?

Let's explore: How many "degrees of freedom" does μ have?
""")

# Count how μ values are determined
primes_up_to = [p for p in range(2, 101) if isprime(p)]
print(f"Primes up to 100: {len(primes_up_to)}")
print(f"Squarefree numbers up to 100: {sum(1 for n in range(1, 101) if mu(n) != 0)}")

# Each squarefree n is a product of distinct primes
# μ(n) is determined by the NUMBER of prime factors (parity)
# This is a HUGE constraint!

print("""
OBSERVATION: μ(n) is completely determined by ω(n) mod 2.

But ω(n) is determined by the prime factorization.
The "randomness" comes from HOW primes combine, not from μ itself.

The constraint is: "half of products of k distinct primes have even k"

This is trivially true but doesn't bound partial sums!
""")

# =============================================================================
# APPROACH 7: FOURIER ANALYSIS ON MULTIPLICATIVE GROUPS
# =============================================================================

print("""

================================================================================
APPROACH 7: FOURIER ANALYSIS / CHARACTER SUMS
================================================================================

IDEA: Use Fourier analysis on (ℤ/nℤ)* to understand μ.

The Möbius function can be written as:
  μ(n) = Σ_χ χ(n) × (something involving L(s,χ))

Character sums over Dirichlet characters give:
  Σ μ(n)χ(n) related to L'/L(s,χ)

POLYA-VINOGRADOV: Bounds character sums by O(√q log q).

QUESTION: Can character sum bounds be improved to give M(x) bounds?

Current bounds give: |M(x)| = O(x / (log x)^c) (Halász-type)
We need: |M(x)| = O(√x)

The gap is the "log factor" problem.
""")

# =============================================================================
# APPROACH 8: PHYSICAL ANALOGIES
# =============================================================================

print("""

================================================================================
APPROACH 8: PHYSICAL ANALOGIES
================================================================================

OBSERVATIONS from physics:

1. RANDOM MATRIX THEORY (Montgomery-Odlyzko):
   - ζ zeros statistics match GUE eigenvalues
   - Suggests deep connection to quantum mechanics
   - But this is NUMERICAL, not a proof

2. QUANTUM CHAOS:
   - Berry-Keating: ζ zeros as spectrum of chaotic Hamiltonian
   - The "Riemann dynamics" would be classically chaotic
   - No rigorous construction yet

3. STATISTICAL MECHANICS:
   - The prime zeta function Σ 1/p^s has physical interpretations
   - Connections to Lee-Yang zeros, partition functions
   - Could thermodynamic constraints help?

4. RENORMALIZATION GROUP:
   - The multi-scale structure M_p(y) = Σ M(y/p^k) is RG-like
   - Could fixed-point analysis give bounds?
""")

# Check the "RG flow" structure
p = 2
y = 50000

print(f"\n'RG flow' of M_p at y = {y}:")
print(f"Scale k | M(y/2^k) | Cumulative M_p")
cumul = 0
for k in range(12):
    ypk = y // (2**k)
    if ypk < 1:
        break
    Mk = M(ypk)
    cumul += Mk
    print(f"  {k:>5} | {Mk:>8} | {cumul:>12}")

# =============================================================================
# APPROACH 9: REVERSE MATHEMATICS
# =============================================================================

print("""

================================================================================
APPROACH 9: REVERSE MATHEMATICS / LOGIC
================================================================================

IDEA: Determine what axioms are needed for RH.

QUESTIONS:
1. Is RH provable in Peano Arithmetic (PA)?
2. Is RH independent of PA? (like Goodstein's theorem)
3. What axiom, if added to PA, would make RH provable?

KNOWN:
- RH is a Π₁ statement (can be written as ∀n P(n) for decidable P)
- If RH is false, it's provably false (just find a counterexample)
- If RH is true but unprovable in PA, it's true in all models

SPECULATION: Maybe RH requires an axiom about "prime regularity"
that isn't captured by PA.

This is a long shot but theoretically interesting.
""")

# =============================================================================
# APPROACH 10: COMPUTATIONAL PATTERNS
# =============================================================================

print("""

================================================================================
APPROACH 10: COMPUTATIONAL PATTERN DISCOVERY
================================================================================

IDEA: Find new patterns that suggest proof approaches.

Our discoveries so far:
1. M(y)/M(y/p) ≈ -1 (ratio)
2. M(y) = Σ (-1)^k D(y/2^k) (recursive)
3. Var(ω)/λ → B/e^{-1/e} (variance constant)
4. 89.7% cancellation in M_p sums

QUESTION: Are there MORE patterns we haven't found?
""")

# Look for new patterns
print("Searching for new patterns...")

# Pattern 1: M(y) vs M(y+1)
consecutive_diffs = [M(y+1) - M(y) for y in range(1, 1000)]
print(f"\nM(y+1) - M(y) statistics:")
print(f"  Values: {set(consecutive_diffs)}")  # Should be {-1, 0, 1}

# Pattern 2: Sign changes in M
sign_changes = sum(1 for y in range(2, 10001) if M(y) * M(y-1) < 0)
print(f"  Sign changes in M(1..10000): {sign_changes}")

# Pattern 3: M(p) for primes
M_at_primes = [M(p) for p in primes[:100]]
print(f"\n|M(p)| for first 100 primes:")
print(f"  Mean: {np.mean(np.abs(M_at_primes)):.2f}")
print(f"  Max: {max(np.abs(M_at_primes))}")

# Pattern 4: Relation between M(x) and π(x)
pi_values = [sum(1 for p in primes if p <= x) for x in range(100, 10001, 100)]
M_values_sample = [M(x) for x in range(100, 10001, 100)]
corr_M_pi = np.corrcoef(M_values_sample, pi_values)[0, 1]
print(f"\nCorrelation between M(x) and π(x): {corr_M_pi:.4f}")

# =============================================================================
# APPROACH 11: THE VARIANCE BOUND APPROACH
# =============================================================================

print("""

================================================================================
APPROACH 11: VARIANCE BOUND APPROACH (NEW IDEA)
================================================================================

IDEA: Instead of bounding M(x) directly, bound Var(M(x)) over x.

Define: V(X) = (1/X) Σ_{x≤X} M(x)²

If we can prove V(X) = O(X), then |M(x)| = O(√X) for "most" x.

The multiplicative structure might constrain V(X) directly!

Let's check the variance empirically:
""")

for X in [1000, 5000, 10000, 50000]:
    M_squared_sum = sum(M(x)**2 for x in range(1, X + 1))
    V_X = M_squared_sum / X
    print(f"X = {X}: V(X) = {V_X:.2f}, V(X)/X = {V_X/X:.6f}")

print("""
If V(X) ~ c×X, then Var(M) ~ X, suggesting |M| ~ √X on average.

QUESTION: Can we prove V(X) = O(X) algebraically?

The identity M(y)² = [Σ (-1)^k D(y/2^k)]² expands to cross-terms.
Bounding these cross-terms might be easier than bounding M directly.
""")

# =============================================================================
# APPROACH 12: THE "SMOOTHED" MERTENS APPROACH
# =============================================================================

print("""

================================================================================
APPROACH 12: THE SMOOTHED MERTENS FUNCTION
================================================================================

IDEA: Study M_smooth(x) = Σ μ(n) × smooth_weight(n/x) instead of M(x).

Smooth weights (like Gaussian, or (1 - n/x)^k) give better analytic properties.

The Mellin transform of M_smooth relates to ζ(s) in a controlled way.

KNOWN: Smooth sums ARE easier to bound, giving M_smooth = O(√x).

QUESTION: Can we "de-smooth" to get bounds on M(x)?

The gap: Smoothing loses information. De-smoothing requires that information.
""")

# =============================================================================
# SUMMARY
# =============================================================================

print("""

================================================================================
SUMMARY: POTENTIAL APPROACHES TO BREAK CIRCULARITY
================================================================================

MOST PROMISING:

1. PROBABILISTIC (Sarnak Conjecture)
   - If μ is "random enough", CLT gives √x
   - Sarnak's work on Möbius randomness is partial but advancing
   - STATUS: Active research, partial results

2. SPECTRAL (Hilbert-Pólya)
   - Construct operator with ζ zeros as eigenvalues
   - Berry-Keating and Connes have concrete proposals
   - STATUS: No rigorous construction yet

3. VARIANCE BOUNDS
   - Bound Var(M(x)) instead of |M(x)|
   - The multiplicative structure might constrain variance
   - STATUS: Worth exploring further

LESS LIKELY BUT INTERESTING:

4. ALGEBRAIC GEOMETRY
   - Lift Weil-Deligne methods to ℤ
   - Arakelov geometry attempts this
   - STATUS: Major technical obstacles

5. LOGIC/REVERSE MATHEMATICS
   - Determine what axioms RH requires
   - STATUS: Theoretical interest only

6. PHYSICAL ANALOGIES
   - Random matrix theory, quantum chaos
   - STATUS: Suggests structure but no proofs

THE FUNDAMENTAL CHALLENGE:

All approaches ultimately need to show that μ(n) values "balance" to O(√x).
This balance is controlled by ζ zeros.
Breaking the circularity means proving the balance WITHOUT using zeros.

The most promising direction seems to be:
PROVE THAT μ IS "SUFFICIENTLY RANDOM" USING ONLY ITS MULTIPLICATIVE STRUCTURE.

This is essentially the Sarnak program.
""")

print("=" * 80)
print("ALTERNATIVE APPROACHES ANALYSIS COMPLETE")
print("=" * 80)
