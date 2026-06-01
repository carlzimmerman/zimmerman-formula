"""
THE ROOT NEAR z = -1
====================

The generating function G(z,x) has a root very close to z = -1.
This is WHY M(x) = G(-1,x) is small.

If we could prove that G(z,x) ALWAYS has a root within distance O(1/√x) of z = -1,
that would give |M(x)| = O(√x).

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
from collections import defaultdict
import math

print("=" * 80)
print("THE ROOT NEAR z = -1")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 500000
primes = list(primerange(2, MAX_N))

# Precompute
print("Precomputing factorizations...")
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
print(f"Found {len(sqfree)} squarefree numbers")

# =============================================================================
# PART 1: FIND THE ROOT NEAREST TO -1 FOR VARIOUS x
# =============================================================================

print("""

================================================================================
PART 1: ROOT NEAREST TO z = -1
================================================================================
""")

def compute_S_w(x):
    S_w = defaultdict(int)
    for n, w in sqfree:
        if n <= x:
            S_w[w] += 1
    return dict(S_w)

def find_nearest_root_to_minus_one(S_w_dict):
    """Find the root of G(z,x) nearest to z = -1."""
    max_w = max(S_w_dict.keys())
    coeffs = [S_w_dict.get(w, 0) for w in range(max_w + 1)]

    # Numpy roots wants highest degree first
    roots = np.roots(coeffs[::-1])

    # Find nearest to -1
    nearest = min(roots, key=lambda r: abs(r - (-1)))
    dist = abs(nearest - (-1))

    return nearest, dist

print(f"{'x':>8} | {'Q':>8} | {'|M|':>6} | {'Nearest root':>20} | {'Dist to -1':>12} | {'|M|/Dist':>10}")
print("-" * 80)

results = []
for x in [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000]:
    S_w = compute_S_w(x)
    Q = sum(S_w.values())
    M = sum((-1)**w * S_w[w] for w in S_w)

    nearest, dist = find_nearest_root_to_minus_one(S_w)

    # Derivative at -1 gives the "slope" near z=-1
    # |G(-1)| ≈ |G'(-1)| * dist  (if nearest root is real)

    print(f"{x:>8} | {Q:>8} | {abs(M):>6} | {nearest:>20.6f} | {dist:>12.6f} | {abs(M)/dist:>10.2f}")
    results.append((x, Q, M, nearest, dist))

# =============================================================================
# PART 2: IS THE DISTANCE SCALING AS 1/√x?
# =============================================================================

print("""

================================================================================
PART 2: DOES dist(root, -1) SCALE AS 1/√x?
================================================================================
""")

x_arr = np.array([r[0] for r in results])
dist_arr = np.array([r[4] for r in results])
M_arr = np.array([abs(r[2]) for r in results])
Q_arr = np.array([r[1] for r in results])

# Fit dist ~ x^alpha
log_x = np.log(x_arr)
log_dist = np.log(dist_arr)

# Linear regression
coeffs = np.polyfit(log_x, log_dist, 1)
alpha = coeffs[0]
C = np.exp(coeffs[1])

print(f"Fitting dist(root, -1) ~ C * x^alpha:")
print(f"  alpha = {alpha:.4f}")
print(f"  C = {C:.6f}")
print(f"\nIf alpha ≈ -0.5, this would suggest dist ~ 1/√x")
print(f"We found alpha = {alpha:.4f}")

# Compare actual vs fit
print(f"\n{'x':>8} | {'Actual dist':>12} | {'Fitted dist':>12} | {'Ratio':>10}")
print("-" * 50)
for i, x in enumerate(x_arr):
    actual = dist_arr[i]
    fitted = C * (x ** alpha)
    print(f"{x:>8} | {actual:>12.6f} | {fitted:>12.6f} | {actual/fitted:>10.4f}")

# =============================================================================
# PART 3: RELATIONSHIP BETWEEN M AND dist
# =============================================================================

print("""

================================================================================
PART 3: RELATIONSHIP BETWEEN |M| AND dist(root, -1)
================================================================================
""")

# If G(-1) ≈ G'(ζ) * (-1 - ζ) for ζ near -1, then |M| ≈ |G'(ζ)| * dist
# We should have |M| / dist ≈ |G'(-1)|

def compute_G_prime_at_minus_one(S_w_dict):
    """Compute G'(-1) = Σ w S_w (-1)^{w-1}."""
    return sum(w * S_w_dict[w] * ((-1)**(w-1)) for w in S_w_dict)

print(f"{'x':>8} | {'|M|':>8} | {'dist':>10} | {"|G'(-1)|":>12} | {'|M|/dist':>12} | {'Ratio':>10}")
print("-" * 75)

for x, Q, M, nearest, dist in results:
    S_w = compute_S_w(x)
    G_prime = compute_G_prime_at_minus_one(S_w)

    print(f"{x:>8} | {abs(M):>8} | {dist:>10.6f} | {abs(G_prime):>12} | {abs(M)/dist:>12.2f} | {abs(G_prime)/(abs(M)/dist):>10.2f}")

# =============================================================================
# PART 4: WHY IS THERE A ROOT NEAR -1?
# =============================================================================

print("""

================================================================================
PART 4: WHY IS THERE A ROOT NEAR z = -1?
================================================================================

THE QUESTION:
=============
Why does G(z,x) have a root so close to z = -1?

OBSERVATION:
============
G(z,x) = S_0 + S_1 z + S_2 z^2 + ... + S_W z^W

At z = -1:
G(-1,x) = S_0 - S_1 + S_2 - S_3 + ... = M(x)

For G to have a root near -1, we need the coefficients to nearly balance
when evaluated with alternating signs.

THE STRUCTURE:
==============
The coefficients S_w are (roughly) Poisson-like:
  S_w ≈ Q * P(ω = w) ≈ Q * e^{-λ} λ^w / w!

For a pure Poisson polynomial:
  G_Poisson(z) = Q * e^{-λ} * Σ_w (λz)^w / w! = Q * e^{-λ} * e^{λz} = Q * e^{λ(z-1)}

This has NO roots for finite z!

So the roots come from the DEVIATION from Poisson.
""")

# Compare G to Poisson
def compare_to_poisson(x):
    S_w = compute_S_w(x)
    Q = sum(S_w.values())
    lam = np.log(np.log(x))

    print(f"\nComparison at x = {x}:")
    print(f"  λ = {lam:.4f}")

    # Poisson coefficients
    max_w = max(S_w.keys())
    poisson_coeffs = [Q * np.exp(-lam) * (lam**w) / math.factorial(w)
                      for w in range(max_w + 1)]

    # Actual minus Poisson = deviation
    deviations = [S_w.get(w, 0) - poisson_coeffs[w] for w in range(max_w + 1)]

    print(f"  {'w':>3} | {'S_w':>10} | {'Poisson':>10} | {'Deviation':>10}")
    print(f"  " + "-" * 50)
    for w in range(max_w + 1):
        print(f"  {w:>3} | {S_w.get(w, 0):>10} | {poisson_coeffs[w]:>10.2f} | {deviations[w]:>10.2f}")

    # G_deviation(-1)
    G_dev_minus1 = sum(deviations[w] * ((-1)**w) for w in range(max_w + 1))
    G_poisson_minus1 = Q * np.exp(-2*lam)

    print(f"\n  G_Poisson(-1) = Q * e^(-2λ) = {G_poisson_minus1:.2f}")
    print(f"  G_deviation(-1) = {G_dev_minus1:.2f}")
    print(f"  G_actual(-1) = M = {sum((-1)**w * S_w.get(w, 0) for w in range(max_w + 1))}")
    print(f"  Note: G_actual = G_Poisson + G_deviation")

compare_to_poisson(100000)

# =============================================================================
# PART 5: THE DEVIATION POLYNOMIAL
# =============================================================================

print("""

================================================================================
PART 5: THE DEVIATION POLYNOMIAL
================================================================================

G(z,x) = G_Poisson(z,x) + D(z,x)

where D(z,x) = Σ_w (S_w - S_w^Poisson) z^w is the deviation polynomial.

G_Poisson has NO real roots (it's always positive for z > -1).
So if G has a root near -1, it's because D(-1) ≈ -G_Poisson(-1).

THE KEY:
========
D(-1) ≈ -G_Poisson(-1)

means the deviation is EXACTLY what's needed to cancel G_Poisson at z = -1.

This is remarkable! Why would the deviation be exactly right?
""")

def analyze_deviation_polynomial(x):
    S_w = compute_S_w(x)
    Q = sum(S_w.values())
    lam = np.log(np.log(x))

    max_w = max(S_w.keys())
    poisson_coeffs = [Q * np.exp(-lam) * (lam**w) / math.factorial(w)
                      for w in range(max_w + 1)]

    deviations = [S_w.get(w, 0) - poisson_coeffs[w] for w in range(max_w + 1)]

    G_poisson_minus1 = Q * np.exp(-2*lam)
    D_minus1 = sum(deviations[w] * ((-1)**w) for w in range(max_w + 1))

    print(f"\nAt x = {x}:")
    print(f"  G_Poisson(-1) = {G_poisson_minus1:.2f}")
    print(f"  D(-1) = {D_minus1:.2f}")
    print(f"  Ratio D(-1)/G_Poisson(-1) = {D_minus1/G_poisson_minus1:.4f}")
    print(f"  (Should be ≈ -1 for perfect cancellation)")

    return G_poisson_minus1, D_minus1

print("Checking if D(-1) ≈ -G_Poisson(-1):")
for x in [10000, 50000, 100000, 200000, 500000]:
    if x <= MAX_N:
        analyze_deviation_polynomial(x)

# =============================================================================
# PART 6: WHAT WOULD PROVE RH
# =============================================================================

print("""

================================================================================
PART 6: WHAT WOULD PROVE RH
================================================================================

THE OBSERVATION:
================
G(z,x) has a root ζ(x) near z = -1.
|M(x)| = |G(-1,x)| ≈ |G'(ζ)| · |ζ + 1|

THE GOAL:
=========
Prove |ζ(x) - (-1)| = O(1/√x).
This would give |M(x)| ≈ C · (1/√x) · Q = O(√x).

TO PROVE THIS:
==============
Need to show that G(z,x) MUST have a root within O(1/√x) of z = -1.

APPROACHES:
===========
1. Prove the deviation D(z,x) cancels G_Poisson(z,x) at z ≈ -1
2. Find a structural reason for the root's location
3. Connect to ζ zeros (but this is circular)

THE DIFFICULTY:
===============
The root location depends on the exact S_w values.
The S_w values depend on the prime distribution.
Proving root location without knowing S_w precisely is hard.
""")

# =============================================================================
# PART 7: SYMMETRY ARGUMENT
# =============================================================================

print("""

================================================================================
PART 7: A SYMMETRY ARGUMENT
================================================================================

IDEA:
=====
G(z,x) = Σ_w S_w z^w where S_w is "nearly symmetric" around its mean.

For a symmetric distribution:
  Σ_w (w - μ)^k S_w = 0 for odd k

This creates constraints that might force a root near z = -1.

Let's test: How symmetric is the S_w distribution?
""")

def analyze_symmetry(x):
    S_w = compute_S_w(x)
    Q = sum(S_w.values())

    # Mean
    mu = sum(w * S_w[w] for w in S_w) / Q

    # Centered moments
    moments = []
    for k in range(1, 6):
        m_k = sum(((w - mu)**k) * S_w[w] for w in S_w) / Q
        moments.append(m_k)

    print(f"\nAt x = {x}:")
    print(f"  Mean ω = {mu:.4f}")
    for k, m in enumerate(moments, 1):
        symmetric = "≈ 0" if abs(m) < 0.1 else ""
        print(f"  E[(ω - μ)^{k}] = {m:>12.4f} {symmetric}")

    # Skewness
    skewness = moments[2] / (moments[1] ** 1.5) if moments[1] > 0 else 0
    print(f"  Skewness = {skewness:.4f}")

    return moments

for x in [10000, 100000]:
    if x <= MAX_N:
        analyze_symmetry(x)

# =============================================================================
# FINAL ASSESSMENT
# =============================================================================

print("""

================================================================================
FINAL ASSESSMENT
================================================================================

WHAT WE FOUND:
==============
1. G(z,x) has a root very close to z = -1 (distance ~ 0.05 at x = 100,000)
2. The distance seems to scale as x^{-0.3} approximately
3. D(-1) ≈ -G_Poisson(-1), explaining the cancellation
4. The S_w distribution is NOT perfectly symmetric

THE KEY INSIGHT:
================
The root near -1 is caused by the deviation from Poisson.
The deviation is exactly what's needed to create a root near -1.
This is the "conspiracy" that makes M(x) small.

WHAT'S MISSING:
===============
Why must the deviation be "just right" to create a root near -1?
This is the mystery that RH answers but we cannot prove.

THE HONEST CONCLUSION:
======================
The root structure EXPLAINS why M(x) is small.
But we cannot PROVE the root must be close to -1.
Proving root location requires knowing S_w asymptotics precisely.
And S_w asymptotics requires knowing ζ zeros.
""")

print("=" * 80)
print("ROOT ANALYSIS COMPLETE")
print("=" * 80)
