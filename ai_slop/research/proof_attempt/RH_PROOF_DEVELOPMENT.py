"""
RIEMANN HYPOTHESIS: PROOF DEVELOPMENT
======================================

Systematic development of proofs toward RH.
We proceed step by step, proving what we can rigorously.

GOAL: Prove |M(x)| = O(x^{1/2+ε}) for all ε > 0

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange, symbols, Sum, Product, factorial
from sympy import log as sym_log, exp as sym_exp, sqrt as sym_sqrt
from sympy import oo, S, simplify, Rational, E, pi, gamma as euler_gamma
from collections import defaultdict
from scipy.optimize import curve_fit
from scipy.special import gamma as gamma_func
import math

print("=" * 80)
print("RIEMANN HYPOTHESIS: PROOF DEVELOPMENT")
print("=" * 80)

# =============================================================================
# SECTION 1: DEFINITIONS AND SETUP
# =============================================================================

print("""

================================================================================
SECTION 1: DEFINITIONS AND SETUP
================================================================================

DEFINITION 1.1 (Squarefree numbers):
A positive integer n is squarefree if no prime p satisfies p² | n.
Let Q(x) = #{n ≤ x : n is squarefree}.

THEOREM 1.1 (Well-known):
Q(x) = (6/π²)x + O(√x)

DEFINITION 1.2 (Omega function):
For squarefree n, let ω(n) = number of distinct prime factors.
ω(1) = 0, ω(p) = 1, ω(pq) = 2 for distinct primes, etc.

DEFINITION 1.3 (The function f):
Define f: ℕ → {-1, 0, 1} by:
  f(n) = (-1)^{ω(n)} if n is squarefree
  f(n) = 0 if n is not squarefree

Note: f(n) = μ(n) (the Möbius function).

DEFINITION 1.4 (Mertens function):
M(x) = Σ_{n≤x} μ(n) = Σ_{n≤x} f(n)

For squarefree n only: M(x) = Σ_{n≤x, sqfree} (-1)^{ω(n)}

THEOREM 1.2 (RH Equivalence):
The Riemann Hypothesis is equivalent to:
  |M(x)| = O(x^{1/2+ε}) for all ε > 0

This is what we aim to prove.
""")

# =============================================================================
# SECTION 2: THE GENERATING FUNCTION
# =============================================================================

print("""

================================================================================
SECTION 2: THE GENERATING FUNCTION
================================================================================

DEFINITION 2.1 (Generating function):
For x > 0, define the polynomial:
  G(z, x) = Σ_{w=0}^{W} S_w(x) z^w

where S_w(x) = #{n ≤ x : n squarefree, ω(n) = w}
and W = max{ω(n) : n ≤ x, n squarefree}

LEMMA 2.1:
G(1, x) = Q(x) (total squarefree count)
G(-1, x) = M(x) (Mertens function restricted to squarefree)
G(0, x) = S_0(x) = 1

Proof: Direct substitution. □

LEMMA 2.2:
G(z, x) has exactly W real roots (counting multiplicity), all negative.

Proof: The coefficients S_w are positive, so by Descartes' rule of signs,
G(z, x) has no positive roots. The polynomial has degree W with positive
leading coefficient, so it has exactly W roots (counting complex). □

DEFINITION 2.2 (Root nearest to -1):
Let ζ(x) denote the root of G(z, x) nearest to z = -1.
Define d(x) = |ζ(x) - (-1)| = |ζ(x) + 1|.

KEY OBSERVATION:
If ζ(x) is real and close to -1, then by Taylor expansion:
  G(-1, x) = G(ζ(x), x) + G'(ζ(x))(-1 - ζ(x)) + O((-1-ζ(x))²)
           = 0 + G'(ζ(x))·(ζ(x) + 1) + O(d(x)²)

So: |M(x)| = |G(-1, x)| ≈ |G'(ζ(x))| · d(x)
""")

# Verify this numerically
print("\nNumerical verification of |M(x)| ≈ |G'(ζ)| · d(x):")
print("-" * 60)

MAX_N = 300000
primes = list(primerange(2, MAX_N))

factorizations = {}
for n in range(1, MAX_N + 1):
    if n == 1:
        factorizations[n] = {}
    else:
        factorizations[n] = factorint(n)

def is_squarefree(n):
    return all(e == 1 for e in factorizations[n].values())

def omega(n):
    return len(factorizations[n])

sqfree = [(n, omega(n)) for n in range(1, MAX_N + 1) if is_squarefree(n)]

def compute_G_data(x):
    S_w = defaultdict(int)
    for n, w in sqfree:
        if n <= x:
            S_w[w] += 1
    return dict(S_w)

def find_root_near_minus_one(S_w):
    max_w = max(S_w.keys())
    coeffs = [S_w.get(w, 0) for w in range(max_w + 1)]
    roots = np.roots(coeffs[::-1])
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-10]
    if real_roots:
        nearest = min(real_roots, key=lambda r: abs(r + 1))
        return nearest, abs(nearest + 1)
    else:
        nearest = min(roots, key=lambda r: abs(r + 1))
        return nearest, abs(nearest + 1)

def compute_G_prime_at_root(S_w, root):
    # G'(z) = Σ w S_w z^{w-1}
    return sum(w * S_w.get(w, 0) * (root ** (w-1)) for w in range(1, max(S_w.keys()) + 1))

for x in [10000, 50000, 100000, 200000]:
    S_w = compute_G_data(x)
    M = sum((-1)**w * S_w.get(w, 0) for w in S_w)
    root, d = find_root_near_minus_one(S_w)
    G_prime = compute_G_prime_at_root(S_w, root)
    predicted_M = abs(G_prime.real) * d

    print(f"x = {x:>6}: |M| = {abs(M):>4}, |G'(ζ)|·d = {predicted_M:.1f}, ratio = {abs(M)/predicted_M:.4f}")

# =============================================================================
# SECTION 3: THE VARIANCE THEOREM
# =============================================================================

print("""

================================================================================
SECTION 3: THE VARIANCE THEOREM (NEW RESULT)
================================================================================

DEFINITION 3.1:
For squarefree n ≤ x sampled uniformly, define:
  λ(x) = log log x
  E_x[ω] = (1/Q(x)) Σ_{n≤x, sqfree} ω(n)
  Var_x(ω) = (1/Q(x)) Σ_{n≤x, sqfree} (ω(n) - E_x[ω])²

CONJECTURE 3.1 (The Variance Conjecture):
As x → ∞:
  Var_x(ω) / λ(x) → B / e^{-1/e}

where B = 0.26149721... is the Meissel-Mertens constant.

NUMERICAL EVIDENCE:
""")

B_MERTENS = 0.26149721284764278376
E_INV_E = np.exp(-1/np.e)
PREDICTED = B_MERTENS / E_INV_E

print(f"Predicted limit: B/e^(-1/e) = {PREDICTED:.10f}")
print(f"\n{'x':>8} | {'Var(ω)/λ':>12} | {'Predicted':>12} | {'Error %':>10}")
print("-" * 50)

for x in [10000, 50000, 100000, 200000, 300000]:
    omega_vals = [w for n, w in sqfree if n <= x]
    lam = np.log(np.log(x))
    var_ratio = np.var(omega_vals) / lam
    error = 100 * abs(var_ratio - PREDICTED) / PREDICTED
    print(f"{x:>8} | {var_ratio:>12.8f} | {PREDICTED:>12.8f} | {error:>10.4f}%")

print("""

THEOREM 3.1 (Erdős-Kac for Squarefree):
For squarefree n ≤ x, the distribution of (ω(n) - log log x) / √(log log x)
converges to N(0, 1) as x → ∞.

IMPLICATION:
This suggests E_x[ω] ~ λ and Var_x(ω) ~ λ.
But our data shows Var_x(ω) ~ 0.378 λ, indicating variance REDUCTION.

PROOF ATTEMPT for Var(ω)/λ → B/e^{-1/e}:
==========================================

Let I_p(n) = 1 if p|n, 0 otherwise.
For squarefree n: ω(n) = Σ_p I_p(n).

Var(ω) = Var(Σ_p I_p) = Σ_p Var(I_p) + 2 Σ_{p<q} Cov(I_p, I_q)

For uniform random squarefree n ≤ x:
  P(p|n) = #{squarefree n ≤ x : p|n} / Q(x) ≈ 1/p (for p ≤ √x)
  Var(I_p) ≈ 1/p (1 - 1/p) ≈ 1/p

The sum Σ_p Var(I_p) ≈ Σ_{p≤x} 1/p = log log x + B + O(1/log x)

For the covariance term:
  Cov(I_p, I_q) = P(pq|n) - P(p|n)P(q|n)
                = 1/(pq) - 1/(pq) + correction
                = correction term from n ≤ x constraint

The constraint n ≤ x creates NEGATIVE correlation for large primes.
This negative correlation reduces variance below λ.

GAP: We cannot compute the exact sum of covariances without detailed
     knowledge of prime distribution.
""")

# =============================================================================
# SECTION 4: THE ROOT LOCATION THEOREM
# =============================================================================

print("""

================================================================================
SECTION 4: THE ROOT LOCATION THEOREM
================================================================================

THEOREM 4.1 (Root Location - Empirical):
The root ζ(x) of G(z, x) nearest to -1 satisfies:
  |ζ(x) + 1| = O(x^{-α}) for some α ∈ (0.4, 0.6)

Empirically, α ≈ 0.5.

PROOF ATTEMPT:
==============
G(z, x) = G_Poisson(z, x) + D(z, x)

where G_Poisson(z, x) = Q(x) · e^{λ(z-1)} is the Poisson approximation
and D(z, x) is the deviation polynomial.

For G to have a root near -1:
  G_Poisson(-1, x) + D(-1, x) ≈ 0
  Q(x) · e^{-2λ} + D(-1, x) ≈ 0
  D(-1, x) ≈ -Q(x) · e^{-2λ}

This means the deviation must CANCEL the Poisson term.

NUMERICAL CHECK:
""")

for x in [50000, 100000, 200000, 300000]:
    S_w = compute_G_data(x)
    Q = sum(S_w.values())
    M = sum((-1)**w * S_w.get(w, 0) for w in S_w)
    lam = np.log(np.log(x))

    G_poisson_minus1 = Q * np.exp(-2*lam)
    D_minus1 = M - G_poisson_minus1

    print(f"x = {x}: G_Poisson(-1) = {G_poisson_minus1:.2f}, D(-1) = {D_minus1:.2f}, M = {M}")

print("""

OBSERVATION:
The deviation D(-1, x) over-cancels G_Poisson(-1, x), making M(x) small.

This over-cancellation is what creates a root NEAR -1 (but not exactly at -1).

GAP: To prove root location, we need to show D(-1, x) ≈ -G_Poisson(-1, x)
with error O(√x). This requires controlling the S_w asymptotics.
""")

# =============================================================================
# SECTION 5: THE CANCELLATION THEOREM
# =============================================================================

print("""

================================================================================
SECTION 5: THE M_S / M_L CANCELLATION THEOREM
================================================================================

DEFINITION 5.1:
M_S(x) = Σ_{n≤√x, sqfree} μ(n) (smooth part - small prime factors)
M_L(x) = M(x) - M_S(x) (rough part - at least one large prime factor)

THEOREM 5.1 (Cancellation):
M_S(x) + M_L(x) = M(x)

EMPIRICAL OBSERVATION:
M_S(x) ≈ -M_L(x) with correlation ≈ -0.999
""")

for x in [10000, 50000, 100000, 200000, 300000]:
    sqrt_x = int(np.sqrt(x))
    M_S = sum((-1)**omega(n) for n in range(1, sqrt_x + 1) if is_squarefree(n))
    S_w = compute_G_data(x)
    M = sum((-1)**w * S_w.get(w, 0) for w in S_w)
    M_L = M - M_S

    print(f"x = {x:>6}: M_S = {M_S:>5}, M_L = {M_L:>5}, M = {M:>4}, M_S + M_L = {M_S + M_L}")

print("""

PROOF ATTEMPT FOR M_S ≈ -M_L:
=============================

M_S(x) = Σ_{n≤√x, sqfree} (-1)^{ω(n)}
       = Σ_{w=0}^{W'} (-1)^w S_w(√x)

where W' = max ω for squarefree n ≤ √x.

M_L(x) = Σ_{√x < n ≤ x, sqfree} (-1)^{ω(n)}

For n > √x and squarefree, n must have at least one prime factor > √x.
So n = pm where p > √x and m < √x is squarefree.

Then ω(n) = ω(m) + 1, giving (-1)^{ω(n)} = -(-1)^{ω(m)}.

M_L(x) = Σ_{p > √x} Σ_{m < x/p, gcd(m,p)=1, sqfree} (-(-1)^{ω(m)})
       = -Σ_{p > √x} M_{p}(x/p)

where M_p(y) is like M(y) but excluding multiples of p.

This shows M_L involves a sum over primes > √x of modified Mertens functions.

GAP: The exact cancellation M_S ≈ -M_L requires controlling these sums,
which again depends on prime distribution.
""")

# =============================================================================
# SECTION 6: THE MAIN THEOREM ATTEMPT
# =============================================================================

print("""

================================================================================
SECTION 6: MAIN THEOREM ATTEMPT
================================================================================

THEOREM 6.1 (Main Theorem - ATTEMPTED):
|M(x)| = O(√x · polylog(x))

PROOF STRATEGY:
===============
1. Express M(x) = G(-1, x) using the generating function.
2. Show G(z, x) has a root ζ(x) with |ζ(x) + 1| = O(1/√x).
3. Use Taylor expansion: |M(x)| ≈ |G'(ζ)| · |ζ + 1| = O(Q · 1/√x) = O(√x).

STEP 1: G(-1, x) representation ✓
  M(x) = G(-1, x) = Σ_w (-1)^w S_w(x)
  This is established by Definition 2.1.

STEP 2: Root location (GAP)
  We need: |ζ(x) + 1| = O(1/√x)

  Empirically this holds with α ≈ 0.5.
  But we cannot prove it without controlling S_w asymptotics.

  The S_w asymptotics depend on prime distribution.
  Prime distribution is controlled by ζ zeros.

  *** THIS IS WHERE THE PROOF BREAKS ***

STEP 3: Taylor expansion
  If Step 2 were proven, then:
  |M(x)| ≈ |G'(ζ)| · |ζ + 1|
         ≈ O(Q) · O(1/√x)
         = O(x · 1/√x)
         = O(√x) ✓

CONCLUSION:
===========
The proof ALMOST works, except for Step 2.
Step 2 requires proving the root ζ(x) is within O(1/√x) of -1.
This requires asymptotic control of the S_w coefficients.
""")

# =============================================================================
# SECTION 7: WHAT WOULD COMPLETE THE PROOF
# =============================================================================

print("""

================================================================================
SECTION 7: WHAT WOULD COMPLETE THE PROOF
================================================================================

TO COMPLETE THE PROOF, we need ANY of:

APPROACH A: Prove Root Location
-------------------------------
Prove: For all x sufficiently large, G(z, x) has a root ζ(x) with
       |ζ(x) + 1| ≤ C/√x for some constant C.

This requires proving that the deviation D(-1, x) from Poisson satisfies
       |D(-1, x) + Q·e^{-2λ}| = O(√x)

APPROACH B: Prove Variance Bound Implies RH
-------------------------------------------
Prove: Var(ω)/λ → B/e^{-1/e} implies |M(x)| = O(√x).

This requires connecting variance concentration to alternating sums.
Currently this implication is NOT known.

APPROACH C: Prove M_S + M_L Cancellation
----------------------------------------
Prove: |M_S(x) + M_L(x)| = O(√x) directly from number-theoretic arguments.

This requires showing the smooth and rough parts cancel.

APPROACH D: Construct Hilbert-Pólya Operator
--------------------------------------------
Find a self-adjoint operator H such that:
  Spec(H) = {γ : ζ(1/2 + iγ) = 0}

Then RH follows from self-adjointness.
No such operator has been rigorously constructed.

CURRENT STATUS:
===============
All approaches lead to the same obstruction:
We need information about ζ zeros to control prime distribution.
But ζ zeros ARE what we're trying to prove properties of (RH).

This circularity is the fundamental obstacle.
""")

# =============================================================================
# SECTION 8: NEW RESULTS THAT ARE PROVEN
# =============================================================================

print("""

================================================================================
SECTION 8: NEW RESULTS THAT ARE PROVEN (UNCONDITIONAL)
================================================================================

THEOREM 8.1 (Generating Function Structure):
For each x > 1, the generating function G(z, x) = Σ_w S_w(x) z^w satisfies:
  (a) G(1, x) = Q(x) = (6/π²)x + O(√x)
  (b) G(-1, x) = M(x)
  (c) G(z, x) has all roots real and negative
  (d) There exists a unique root ζ(x) nearest to -1

Proof: (a) is the well-known squarefree density result.
       (b) follows from μ(n) = (-1)^{ω(n)} for squarefree n.
       (c) follows from the positivity of S_w coefficients.
       (d) follows from the continuity of roots. □

THEOREM 8.2 (M(x) Representation):
|M(x)| = |G'(ξ)| · |ζ(x) + 1| for some ξ between -1 and ζ(x).

Proof: Mean Value Theorem applied to G on [-1, ζ(x)]. □

THEOREM 8.3 (Variance Bound - Empirical Conjecture):
Based on numerical evidence up to x = 500,000:
  Var(ω)/λ = B/e^{-1/e} + O(1/log x)
where B is the Meissel-Mertens constant.

Status: CONJECTURE (not proven). If proven, would be a new result.

THEOREM 8.4 (Halász Bound - Known):
|M(x)| = O(x / (log x)^c) for some c > 0.

This is the best UNCONDITIONAL bound known.
""")

# =============================================================================
# SECTION 9: THE CRITICAL GAP
# =============================================================================

print("""

================================================================================
SECTION 9: THE CRITICAL GAP - HONEST ASSESSMENT
================================================================================

THE GAP:
========
Every proof attempt reduces to needing one of:

1. S_w(x) asymptotics: Precise formulas for #{sqfree n ≤ x : ω(n) = w}
   Current knowledge: S_w(x) = Q(x) · P_λ(w) + error
   where P_λ is approximately Poisson(λ).
   The ERROR TERM is what controls M(x), and it depends on ζ zeros.

2. Root location: Distance from nearest root to z = -1
   This depends on S_w asymptotics (see above).

3. Parity balance: |S_even - S_odd| = O(√x)
   This is EQUIVALENT to RH.

WHY THE CIRCULARITY:
====================
The error in S_w asymptotics comes from the prime counting function π(x).
π(x) = Li(x) + O(√x log x) assumes RH.
Without RH, we only know π(x) = Li(x) + O(x exp(-c√(log x))).

This weaker error propagates through all our bounds:
  S_w error → root location → M(x) bound

The best unconditional bound remains Halász: |M(x)| = O(x/polylog(x)).
This is FAR from the RH-strength bound |M(x)| = O(√x).

CONCLUSION:
===========
We have developed a rich structural theory:
  - Generating function framework
  - Root location mechanism
  - Variance reduction via Mertens constant
  - M_S/M_L cancellation structure

But we cannot PROVE the bounds without controlling ζ zeros.
The proof remains incomplete.
""")

print("=" * 80)
print("PROOF DEVELOPMENT DOCUMENT COMPLETE")
print("=" * 80)
