"""
GENERATING FUNCTION STRUCTURE ANALYSIS
======================================

The generating function G(z,x) = Σ_w z^w S_w(x) encodes all the information.
M(x) = G(-1, x).

Key insight: G(z,x) is a polynomial in z of degree ~ log x / log 2.
The coefficients S_w encode the ω distribution.

Can we find constraints on the S_w that force M(x) = G(-1,x) to be small?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange, symbols, expand, Poly
from collections import defaultdict
import math

print("=" * 80)
print("GENERATING FUNCTION STRUCTURE ANALYSIS")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 200000
primes = list(primerange(2, MAX_N))

# Precompute
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

# Precompute squarefree with omega
sqfree = [(n, omega(n)) for n in range(1, MAX_N + 1) if is_squarefree(n)]
print(f"Found {len(sqfree)} squarefree numbers up to {MAX_N}")

# =============================================================================
# PART 1: THE GENERATING FUNCTION AS A POLYNOMIAL
# =============================================================================

print("""
================================================================================
PART 1: G(z,x) AS A POLYNOMIAL
================================================================================

G(z,x) = Σ_{w≥0} S_w(x) z^w

where S_w(x) = #{n ≤ x : n squarefree, ω(n) = w}

Key properties:
  • G(1,x) = Q(x) = total squarefree numbers
  • G(-1,x) = M(x) = Mertens function (restricted to squarefree)
  • G(0,x) = S_0(x) = 1 (just n=1)

The polynomial has degree W_max = max ω(n) for n ≤ x.
""")

def compute_S_w(x):
    """Compute the S_w coefficients."""
    S_w = defaultdict(int)
    for n, w in sqfree:
        if n <= x:
            S_w[w] += 1
    return dict(S_w)

x = 100000
S_w = compute_S_w(x)

print(f"At x = {x}:")
print(f"  Degree of G(z,x): {max(S_w.keys())}")
print(f"  Coefficients S_w:")
for w in sorted(S_w.keys()):
    print(f"    S_{w} = {S_w[w]}")

Q = sum(S_w.values())
M = sum((-1)**w * S_w[w] for w in S_w)
print(f"\n  G(1,x) = Q = {Q}")
print(f"  G(-1,x) = M = {M}")

# =============================================================================
# PART 2: ROOTS OF G(z,x)
# =============================================================================

print("""

================================================================================
PART 2: ROOTS OF G(z,x)
================================================================================

G(z,x) is a polynomial. Where are its roots?

If G(-1,x) = M(x) is small, then z = -1 is CLOSE to a root.

The distance from -1 to the nearest root might control |M(x)|.
""")

def find_roots(S_w_dict):
    """Find roots of G(z,x)."""
    # Build polynomial coefficients
    max_w = max(S_w_dict.keys())
    coeffs = [S_w_dict.get(w, 0) for w in range(max_w + 1)]

    # Find roots
    roots = np.roots(coeffs[::-1])  # numpy wants highest degree first
    return roots

roots = find_roots(S_w)

# Real roots
real_roots = [r.real for r in roots if abs(r.imag) < 1e-10]
complex_roots = [(r.real, r.imag) for r in roots if abs(r.imag) >= 1e-10]

print(f"Found {len(roots)} roots of G(z,x):")
print(f"  Real roots: {len(real_roots)}")
if real_roots:
    real_roots.sort()
    print(f"    Smallest: {real_roots[0]:.6f}")
    print(f"    Largest: {real_roots[-1]:.6f}")

    # Distance from -1 to nearest real root
    dist_to_minus_1 = min(abs(r - (-1)) for r in real_roots)
    print(f"  Distance from -1 to nearest real root: {dist_to_minus_1:.6f}")

print(f"\n  Complex roots: {len(complex_roots)} (as conjugate pairs)")

# Find root closest to -1
nearest_root = min(roots, key=lambda r: abs(r - (-1)))
dist_nearest = abs(nearest_root - (-1))
print(f"\n  Nearest root to z = -1: {nearest_root:.6f}")
print(f"  Distance: {dist_nearest:.6f}")

# =============================================================================
# PART 3: THE CONSTRAINT FROM M(x) BEING SMALL
# =============================================================================

print("""

================================================================================
PART 3: WHAT DOES SMALL M(x) IMPLY?
================================================================================

If |M(x)| = |G(-1,x)| is small relative to |G(1,x)| = Q(x), then:

|G(-1,x)|/|G(1,x)| = |M(x)|/Q(x) << 1

This means the alternating sum of coefficients is much smaller
than the plain sum.

IMPLICATION:
============
The S_w coefficients must be "balanced" in a specific way.

Define:
  P_even = Σ_{w even} S_w / Q
  P_odd = Σ_{w odd} S_w / Q

Then: M(x)/Q(x) = P_even - P_odd

For |M|/Q to be O(1/√x), we need |P_even - P_odd| = O(1/√x).
""")

S_even = sum(S_w[w] for w in S_w if w % 2 == 0)
S_odd = sum(S_w[w] for w in S_w if w % 2 == 1)
P_even = S_even / Q
P_odd = S_odd / Q

print(f"At x = {x}:")
print(f"  P_even = {P_even:.6f}")
print(f"  P_odd = {P_odd:.6f}")
print(f"  P_even - P_odd = {P_even - P_odd:.6f}")
print(f"  M/Q = {M/Q:.6f}")
print(f"  1/√x = {1/np.sqrt(x):.6f}")

# =============================================================================
# PART 4: TAYLOR EXPANSION AROUND z = 1
# =============================================================================

print("""

================================================================================
PART 4: TAYLOR EXPANSION OF G(z,x) AROUND z = 1
================================================================================

G(z,x) = Σ_w S_w z^w

Expand around z = 1 by substituting z = 1 + u:
  G(1+u, x) = Σ_k G^{(k)}(1,x) / k! · u^k

At u = -2 (so z = -1):
  G(-1,x) = Σ_k G^{(k)}(1,x) / k! · (-2)^k

The derivatives at z = 1 are:
  G(1,x) = Q
  G'(1,x) = Σ_w w S_w = Q · E[ω]
  G''(1,x) = Σ_w w(w-1) S_w = Q · (E[ω²] - E[ω])
  etc.

So M(x) depends on ALL moments of ω!
""")

def compute_moments(S_w_dict):
    """Compute moments E[ω^k] for small k."""
    Q = sum(S_w_dict.values())
    moments = []
    for k in range(6):
        mom_k = sum(w**k * S_w_dict[w] for w in S_w_dict) / Q
        moments.append(mom_k)
    return moments

moments = compute_moments(S_w)
print(f"Moments of ω at x = {x}:")
for k, mom in enumerate(moments):
    print(f"  E[ω^{k}] = {mom:.6f}")

# Compute derivatives at z=1
G_derivs = []
Q = sum(S_w.values())
for k in range(6):
    # k-th derivative at z=1 is Σ_w w(w-1)...(w-k+1) S_w
    deriv = sum(math.prod(w - j for j in range(k)) * S_w.get(w, 0)
                for w in S_w if w >= k)
    G_derivs.append(deriv)

print(f"\nDerivatives at z = 1:")
for k, d in enumerate(G_derivs):
    print(f"  G^({k})(1,x) = {d}")

# Reconstruct M(x) from Taylor series
M_taylor = sum(G_derivs[k] / math.factorial(k) * ((-2)**k)
               for k in range(len(G_derivs)))
print(f"\nTaylor approximation of M(x) (using 6 terms): {M_taylor:.1f}")
print(f"Actual M(x): {M}")

# =============================================================================
# PART 5: THE CANCELLATION MECHANISM
# =============================================================================

print("""

================================================================================
PART 5: THE CANCELLATION MECHANISM
================================================================================

M(x) = Σ_k G^{(k)}(1,x)/k! · (-2)^k

The terms alternate in sign (for k even/odd).
The magnitude grows roughly as 2^k · Q · λ^k / k! (if ω were Poisson).

For small M(x), these terms must cancel!

Let's see the contribution from each term:
""")

print("Contribution from each Taylor term:")
print("-" * 60)
for k in range(len(G_derivs)):
    term = G_derivs[k] / math.factorial(k) * ((-2)**k)
    print(f"  k={k}: G^({k})/k! · (-2)^k = {term:>15.1f}")

print(f"\n  Sum = {sum(G_derivs[k]/math.factorial(k)*((-2)**k) for k in range(len(G_derivs))):.1f}")
print(f"  Actual M(x) = {M}")

# =============================================================================
# PART 6: MOMENT CONSTRAINTS
# =============================================================================

print("""

================================================================================
PART 6: MOMENT CONSTRAINTS FOR SMALL M(x)
================================================================================

If M(x) is small, the moments must satisfy certain constraints.

From the Taylor expansion, M(x) = 0 would require:
  Q - 2·Q·E[ω] + 2·Q·E[ω²] - 2·Q·E[ω] - 8/6·Q·(E[ω³]-3E[ω²]+2E[ω]) + ...

This is a system of constraints on the moments!

QUESTION:
=========
Do the actual moments satisfy these constraints naturally,
or is this something special about the primes?
""")

# What constraints would M = 0 impose?
# M = G(-1) = Σ_w (-1)^w S_w
# This equals Q · E[(-1)^ω]

E_minus1_omega = M / Q
print(f"E[(-1)^ω] = M/Q = {E_minus1_omega:.6f}")

# For Poisson(λ):
lam = np.log(np.log(x))
poisson_E = np.exp(-2*lam)
print(f"If ω ~ Poisson(λ), E[(-1)^ω] = e^(-2λ) = {poisson_E:.6f}")
print(f"Ratio (actual/Poisson) = {E_minus1_omega/poisson_E:.6f}")

# =============================================================================
# PART 7: THE KEY INSIGHT
# =============================================================================

print("""

================================================================================
PART 7: THE KEY INSIGHT
================================================================================

THE STRUCTURE:
==============
G(z,x) = Σ_w S_w z^w is completely determined by the S_w.
The S_w are determined by the prime distribution.
M(x) = G(-1,x) is small because S_w are "balanced".

WHAT "BALANCED" MEANS:
======================
The alternating sum Σ(-1)^w S_w is small compared to Σ S_w.

Equivalently:
  |E[(-1)^ω]| << 1

For Poisson(λ), E[(-1)^ω] = e^{-2λ} ~ (log x)^{-2}.
Actual |E[(-1)^ω]| ~ x^{-1/2} << (log x)^{-2}.

This SUPPRESSION of E[(-1)^ω] is the mystery!

THE QUESTION:
=============
Why is |E[(-1)^ω]| much smaller for squarefree n ≤ x
than the Poisson prediction?

ANSWER:
=======
The primes are NOT independent. The constraint n ≤ x creates correlations.
These correlations cause the parity to balance better than Poisson.

But we can't PROVE this balance without knowing about ζ zeros.
""")

# Compare at multiple x values
print("\nComparison at different x:")
print(f"{'x':>8} | {'|M/Q|':>10} | {'e^(-2λ)':>10} | {'Ratio':>10}")
print("-" * 45)

for x_test in [1000, 5000, 10000, 50000, 100000, 200000]:
    S = compute_S_w(x_test)
    Q_t = sum(S.values())
    M_t = sum((-1)**w * S[w] for w in S)
    lam_t = np.log(np.log(x_test))
    poisson_t = np.exp(-2*lam_t)

    actual = abs(M_t/Q_t)
    if actual > 0:
        ratio = poisson_t / actual
    else:
        ratio = float('inf')

    print(f"{x_test:>8} | {actual:>10.6f} | {poisson_t:>10.6f} | {ratio:>10.1f}x")

# =============================================================================
# PART 8: FOURIER PERSPECTIVE
# =============================================================================

print("""

================================================================================
PART 8: FOURIER PERSPECTIVE
================================================================================

G(e^{2πiθ}, x) = Σ_w S_w e^{2πiwθ}

This is the Fourier series of the measure on [0,1] with mass S_w/Q at w/W_max.

G(-1,x) = G(e^{iπ}, x) = value at θ = 1/2.

If G(e^{2πiθ}, x) is smooth, then Fourier coefficient at high frequency
(like θ = 1/2) should be small.

But θ = 1/2 corresponds to w → (-1)^w, which is the HIGHEST frequency!

The fact that G(-1,x) is small means the measure is very "smooth"
when viewed as a distribution - it has little power at high frequencies.
""")

# Compute |G(e^{2πiθ}, x)| for various θ
theta_vals = np.linspace(0, 1, 101)
G_vals = []

for theta in theta_vals:
    z = np.exp(2j * np.pi * theta)
    G_theta = sum(S_w[w] * (z ** w) for w in S_w)
    G_vals.append(abs(G_theta))

# Find where |G| is minimized
min_idx = np.argmin(G_vals)
min_theta = theta_vals[min_idx]
min_G = G_vals[min_idx]

print(f"At x = {x}:")
print(f"  |G(1,x)| = G(1,x) = Q = {Q}")
print(f"  |G(-1,x)| = |M| = {abs(M)}")
print(f"  |G(i,x)| = {abs(sum(S_w[w] * (1j ** w) for w in S_w)):.1f}")
print(f"  Minimum |G(exp(2*pi*i*theta),x)| at theta = {min_theta:.3f}: {min_G:.1f}")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("""

================================================================================
FINAL SUMMARY
================================================================================

WHAT THE GENERATING FUNCTION TELLS US:
======================================

1. G(z,x) is a polynomial with positive coefficients S_w
2. G(1,x) = Q (sum of coefficients)
3. G(-1,x) = M (alternating sum)
4. |M|/Q is much smaller than predicted by Poisson

THE MYSTERY:
============
The coefficients S_w are arranged so that their alternating sum cancels.
This arrangement comes from the prime distribution.
The prime distribution is controlled by ζ zeros.

TO PROVE RH:
============
We would need to prove that for ANY prime distribution satisfying PNT,
the resulting S_w must have |Σ(-1)^w S_w| = O(√x).

This seems hard because:
  • Different prime arrangements give different S_w
  • Only the ACTUAL primes give the specific cancellation
  • The cancellation is too precise to be generic

WHAT'S SPECIAL:
===============
The actual primes create S_w with:
  • Near-perfect parity balance (S_even ≈ S_odd)
  • Deviation from Poisson that improves balance
  • Correlation structure that suppresses |M|

Understanding WHY requires knowing about ζ zeros.
""")

print("=" * 80)
print("GENERATING FUNCTION ANALYSIS COMPLETE")
print("=" * 80)
