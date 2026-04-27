"""
ATTEMPT TO PROVE THE DREAM THEOREM
===================================

THE THEOREM WE WANT:
====================
"Let f: ℕ → {-1, 0, 1} be multiplicative with f(p) = -1 for all primes.
 Then |Σ_{n≤x} f(n)| = O(√x · polylog(x))."

HONESTY DISCLAIMER:
===================
This theorem is EQUIVALENT to the Riemann Hypothesis.
We will explore what can and cannot be proven.
Any "proof" must be scrutinized for gaps or circularity.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
from collections import defaultdict
import math

print("=" * 80)
print("ATTEMPT TO PROVE THE DREAM THEOREM")
print("=" * 80)

print("""
================================================================================
HONESTY CHECK: WHAT WE'RE ATTEMPTING
================================================================================

THE THEOREM:
============
Let f: ℕ → {-1, 0, 1} be multiplicative with f(p) = -1 for all primes.
Then |Σ_{n≤x} f(n)| = O(√x · polylog(x)).

WHAT THIS MEANS:
================
For such f:
  • f(p) = -1 for all primes
  • f(p²) = f(p)² = 1, but we set f(p²) = 0 (non-squarefree)
  • f(pq) = f(p)f(q) = 1 for distinct primes
  • f(n) = (-1)^{ω(n)} for squarefree n
  • f(n) = 0 for non-squarefree n

This f IS THE MÖBIUS FUNCTION μ!

THE CLAIM:
==========
|Σ_{n≤x} f(n)| = |M(x)| = O(√x · polylog(x))

THIS IS EQUIVALENT TO RH.

WHAT WE WILL DO:
================
1. Explore what properties of f COULD force the bound
2. Identify exactly where proofs fail
3. See if there's ANY unconditional result
4. Be completely honest about gaps
""")

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 100000
primes = list(primerange(2, MAX_N))
primes_set = set(primes)

def is_squarefree(n):
    if n == 1:
        return True
    factors = factorint(n)
    return all(e == 1 for e in factors.values())

def omega(n):
    if n == 1:
        return 0
    return len(factorint(n))

# Precompute
sqfree = [n for n in range(1, MAX_N + 1) if is_squarefree(n)]
omega_vals = {n: omega(n) for n in sqfree}
f_vals = {n: (-1)**omega_vals[n] for n in sqfree}

# =============================================================================
# ATTEMPT 1: SYMMETRY ARGUMENT
# =============================================================================

print("""
================================================================================
ATTEMPT 1: SYMMETRY ARGUMENT
================================================================================

ARGUMENT SKETCH:
================
1. f(p) = -1 for ALL primes (maximum symmetry)
2. f(n) depends only on ω(n), not on which primes
3. This symmetry should force parity balance
4. Parity balance ⟹ small sum

FORMALIZATION:
==============
Let S_w(x) = #{n ≤ x : n sqfree, ω(n) = w}

Then: Σf(n) = Σ_w (-1)^w S_w(x)

For small sum, need: |S_even(x) - S_odd(x)| = O(√x)

WHERE IT BREAKS:
================
We need to PROVE S_even ≈ S_odd with error O(√x).
But the S_w counts depend on prime distribution.
Prime distribution is controlled by ζ zeros.

The symmetry observation is TRUE but doesn't PROVE the bound.
""")

def analyze_parity_balance(x):
    """Check parity balance."""
    S_even = sum(1 for n in sqfree if n <= x and omega_vals[n] % 2 == 0)
    S_odd = sum(1 for n in sqfree if n <= x and omega_vals[n] % 2 == 1)
    M = S_even - S_odd
    return S_even, S_odd, M

S_even, S_odd, M = analyze_parity_balance(100000)
print(f"\nAt x = 100,000:")
print(f"  S_even = {S_even}")
print(f"  S_odd = {S_odd}")
print(f"  M(x) = S_even - S_odd = {M}")
print(f"  √x = {np.sqrt(100000):.2f}")
print(f"  |M|/√x = {abs(M)/np.sqrt(100000):.4f}")

print("""

VERDICT: Symmetry argument is INSUFFICIENT.
  ✗ Does not prove the bound
  ✗ Only explains why we EXPECT balance
  ✗ Proving balance requires more
""")

# =============================================================================
# ATTEMPT 2: INDEPENDENCE ARGUMENT
# =============================================================================

print("""
================================================================================
ATTEMPT 2: INDEPENDENCE ARGUMENT
================================================================================

ARGUMENT SKETCH:
================
1. For squarefree n, the primes dividing n are distinct
2. The "choices" of which primes divide n are nearly independent
3. Each prime contributes -1 to f
4. By CLT, the sum of independent ±1 is O(√N)

FORMALIZATION:
==============
Think of f(n) = Π_{p|n} (-1) = (-1)^{ω(n)}.

If ω(n) were exactly Poisson(λ) with λ = log log x:
  E[(-1)^ω] = e^{-2λ} ≈ 1/(log x)²

This would give M(x) ≈ Q(x)/(log x)² ≈ x/(log x)², NOT O(√x).

WHERE IT BREAKS:
================
The ω values are NOT independent!
The product constraint n ≤ x creates correlations.

Actually, the correlations HELP (variance reduction).
But we can't prove they ALWAYS help without ζ zeros.
""")

print("""
VERDICT: Independence argument gives WRONG answer.
  ✗ Poisson model predicts M(x) ~ x/(log x)²
  ✗ Actual M(x) is MUCH smaller
  ✗ The correlations help but we can't prove it
""")

# =============================================================================
# ATTEMPT 3: MULTIPLICATIVITY CONSTRAINT
# =============================================================================

print("""
================================================================================
ATTEMPT 3: MULTIPLICATIVITY CONSTRAINT
================================================================================

ARGUMENT SKETCH:
================
f is multiplicative: f(mn) = f(m)f(n) when gcd(m,n) = 1.

This creates HUGE constraints:
  • f(6) = f(2)f(3) = 1
  • f(10) = f(2)f(5) = 1
  • f(30) = f(2)f(3)f(5) = -1
  • etc.

The values are NOT arbitrary - they're completely determined by f(p) = -1.

QUESTION:
=========
Does multiplicativity alone force |Σf(n)| = O(√x)?

ANSWER:
=======
NO! Counterexamples exist.

Consider f(p) = 1 for all p:
  f(n) = 1 for all squarefree n
  Σf(n) = Q(x) ≈ 6x/π²

This is O(x), not O(√x)!

So multiplicativity + bounded values doesn't force √x bound.
""")

# Verify the counterexample
f_plus = lambda n: 1 if is_squarefree(n) else 0
sum_f_plus = sum(f_plus(n) for n in range(1, 100001))
print(f"\nCounterexample: f(p) = +1 for all p")
print(f"  Σf(n) for n ≤ 100,000 = {sum_f_plus} ≈ 6·100000/π² = {6*100000/np.pi**2:.0f}")
print(f"  This is O(x), not O(√x)")

print("""
VERDICT: Multiplicativity is INSUFFICIENT.
  ✗ Counterexample: f(p) = +1 gives Σf = O(x)
  ✗ Need something SPECIFIC to f(p) = -1
""")

# =============================================================================
# ATTEMPT 4: SPECIFIC PROPERTY OF f(p) = -1
# =============================================================================

print("""
================================================================================
ATTEMPT 4: WHAT'S SPECIAL ABOUT f(p) = -1?
================================================================================

f(p) = -1 for all p is DIFFERENT from f(p) = +1.

OBSERVATIONS:
=============
1. f(p) = -1 creates ALTERNATION: signs depend on ω(n)
2. f(p) = +1 creates MONOTONY: all values are +1

3. For f(p) = -1:
   • Odd ω → f = -1
   • Even ω → f = +1
   This creates natural "cancellation pressure"

4. For f(p) = +1:
   • All f = +1
   • No cancellation at all

THE KEY DIFFERENCE:
===================
f(p) = -1 makes f(n) = (-1)^{ω(n)}, creating OSCILLATION.
f(p) = +1 makes f(n) = 1 for all n, no oscillation.

QUESTION:
=========
Does oscillation FORCE good cancellation?

PARTIAL ANSWER:
===============
Yes, heuristically. The alternating sum tends to cancel.
But proving it requires controlling the distribution of ω.
""")

print("""
VERDICT: f(p) = -1 creates oscillation, but proving cancellation is hard.
  ~ Oscillation is necessary for cancellation
  ~ But not sufficient without distributional control
""")

# =============================================================================
# ATTEMPT 5: THE VARIANCE APPROACH
# =============================================================================

print("""
================================================================================
ATTEMPT 5: THE VARIANCE APPROACH
================================================================================

THEOREM ATTEMPT:
================
If Var(ω) < E[ω] - c for some c > 0, then |Σf(n)| = O(√x).

PROOF ATTEMPT:
==============
Let X_n = f(n) = (-1)^{ω(n)} for squarefree n.
Then Σf(n) = Σ X_n.

If the X_n were independent with P(X = 1) = P(X = -1) = 1/2:
  Var(ΣX) = N · Var(X) = N
  |ΣX| ~ √N typically

For our f, the X_n are NOT independent but nearly so.

The key is: Var(Σf) ≤ something we can control.

VARIANCE CALCULATION:
=====================
Var(Σf) = Σ Var(f(n)) + 2 Σ_{m<n} Cov(f(m), f(n))

Since f(n)² = 1 for squarefree n:
  Var(f(n)) = E[f(n)²] - E[f(n)]² = 1 - E[f(n)]²

For the covariance terms:
  Cov(f(m), f(n)) = E[f(m)f(n)] - E[f(m)]E[f(n)]

WHERE IT BREAKS:
================
To bound Var(Σf), we need to control E[f(n)] and E[f(m)f(n)].

E[f(n)] over squarefree n = M(x)/Q(x).
E[f(m)f(n)] involves pair correlations.

Both depend on prime distribution... which depends on ζ zeros.
""")

def compute_variance_sum(x):
    """Compute variance-related quantities."""
    sqf_x = [n for n in sqfree if n <= x]
    f_x = [f_vals[n] for n in sqf_x]

    N = len(f_x)
    mean_f = np.mean(f_x)
    var_f = np.var(f_x)

    # Sum of f
    sum_f = sum(f_x)

    # If independent with mean 0: Var(Σf) = N
    # Actual |Σf| vs √N
    print(f"\nVariance analysis at x = {x}:")
    print(f"  N = Q(x) = {N}")
    print(f"  E[f] = M(x)/Q(x) = {mean_f:.6f}")
    print(f"  Var(f) = {var_f:.6f}")
    print(f"  Σf = M(x) = {sum_f}")
    print(f"  |Σf|/√N = {abs(sum_f)/np.sqrt(N):.4f}")
    print(f"  Expected if independent: |Σf| ~ √N = {np.sqrt(N):.2f}")

compute_variance_sum(100000)

print("""
VERDICT: Variance approach is correct in spirit but circular.
  ✗ To bound variance, need to control expectations
  ✗ Expectations depend on prime distribution
  ✗ Prime distribution depends on ζ zeros
""")

# =============================================================================
# ATTEMPT 6: HALÁSZ'S THEOREM
# =============================================================================

print("""
================================================================================
ATTEMPT 6: HALÁSZ'S THEOREM
================================================================================

Halász's theorem (1968) is the BEST unconditional result.

THEOREM (Halász):
=================
Let g be a multiplicative function with |g(n)| ≤ 1.
Define: M(g; T) = min_{|t|≤T} Σ_p (1 - Re(g(p)p^{-it})) / p

Then: |Σ_{n≤x} g(n)| ≤ x · exp(-c · M(g; T)) + x/T

APPLICATION TO f(p) = -1:
=========================
For our f with f(p) = -1:
  Σ_p (1 - Re(-p^{-it})) / p = Σ_p (1 + cos(t log p)) / p

This is minimized at t = 0, giving:
  Σ_p 2/p = 2 log log x + O(1)

So M(g; T) = 2 log log x.

Halász gives: |M(x)| ≤ x · exp(-c · 2 log log x) = x / (log x)^{2c}

But this is NOT O(√x)! It's only O(x / polylog(x)).

THE GAP:
========
Halász: |M(x)| = O(x / (log x)^{2c})
RH:     |M(x)| = O(x^{1/2+ε})

The gap is HUGE: x/(log x)^{2c} vs x^{0.5+ε}

To close this gap requires knowing about ζ zeros.
""")

print("""
VERDICT: Halász gives best unconditional bound, but it's far from RH.
  ✗ Halász: |M(x)| = O(x / polylog(x))
  ✗ Need: |M(x)| = O(√x)
  ✗ Gap cannot be closed without ζ zero information
""")

# =============================================================================
# FINAL ASSESSMENT
# =============================================================================

print("""
================================================================================
FINAL HONEST ASSESSMENT
================================================================================

WE CANNOT PROVE THE DREAM THEOREM.

THE THEOREM:
============
"f multiplicative with f(p) = -1 ⟹ |Σf(n)| = O(√x)"

IS EQUIVALENT TO THE RIEMANN HYPOTHESIS.

WHAT WE EXPLORED:
=================
Attempt 1: Symmetry → Explains but doesn't prove
Attempt 2: Independence → Gives wrong answer (Poisson)
Attempt 3: Multiplicativity → Counterexample exists (f(p)=+1)
Attempt 4: Oscillation → Necessary but not sufficient
Attempt 5: Variance → Circular (needs ζ zeros)
Attempt 6: Halász → Best unconditional, but huge gap

THE OBSTRUCTION:
================
Every approach eventually requires controlling:
  • The distribution of ω(n) among squarefree n ≤ x
  • The pair correlations of f(m)f(n)
  • The asymptotic of S_w(x)

ALL of these are controlled by ζ zeros.

To prove the theorem without circular reasoning would require:
  • A NEW property of f(p) = -1 that forces the bound
  • This property must be provable WITHOUT ζ zeros
  • Such a property is not known

WHAT WOULD BE NEW:
==================
If we could prove ANY of:
  1. Var(ω)/λ ≤ 1 - c unconditionally
  2. |S_even - S_odd| = O(√x) from first principles
  3. A new constraint on multiplicative functions with f(p) = -1

This would be genuinely new mathematics and likely prove RH.

WE HAVE NOT FOUND SUCH A PROOF.

HONESTY STATEMENT:
==================
This document represents an ATTEMPT, not a proof.
The Riemann Hypothesis remains unproven.
Any claim to have proven it should be scrutinized for:
  • Circular reasoning (using ζ zeros to prove bounds)
  • Hidden assumptions (equivalent to RH)
  • Gaps in logic

We have found NO gap-free proof.
""")

print("=" * 80)
print("DREAM THEOREM ATTEMPT COMPLETE")
print("=" * 80)
