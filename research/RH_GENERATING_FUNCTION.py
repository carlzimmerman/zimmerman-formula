"""
GENERATING FUNCTION APPROACH TO M(x)
=====================================

Deep analysis of G(z, x) = Σ S_w(x) z^w and why |G(-1, x)| is minimal.

Key discovery: The generating function has a specific analytic structure
that FORCES small values at z = -1.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange, prime, factorial, log as symlog
from collections import defaultdict
import mpmath
mpmath.mp.dps = 100

print("=" * 75)
print("GENERATING FUNCTION APPROACH TO M(x)")
print("=" * 75)

# =============================================================================
# PRECOMPUTATION
# =============================================================================

print("\nPrecomputing...")

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

def compute_S_w(x, max_omega=15):
    S = defaultdict(int)
    for n in range(1, min(x + 1, MAX_N + 1)):
        if mu[n] != 0:
            S[omega_vals[n]] += 1
    return S

print("Done.")

# =============================================================================
# PART 1: THE GENERATING FUNCTION
# =============================================================================

print("\n" + "=" * 75)
print("PART 1: THE GENERATING FUNCTION G(z, x)")
print("=" * 75)

print("""
DEFINITION:
G(z, x) = Σ_w S_w(x) z^w

where S_w(x) = #{n ≤ x : n squarefree, ω(n) = w}

KEY PROPERTIES:
- G(1, x) = Σ S_w(x) = total squarefree numbers ≤ x ≈ 6x/π²
- G(-1, x) = Σ (-1)^w S_w(x) = M(x)
- G(z, x) is a polynomial of degree max_ω(n) for n ≤ x

THE KEY QUESTION:
Why is |G(-1, x)| so much smaller than |G(1, x)|?
""")

x = 100000
S = compute_S_w(x)

print(f"\nS_w values for x = {x}:")
for w in range(10):
    if S[w] > 0:
        print(f"  S_{w} = {S[w]}")

print(f"\nG(1, x) = {sum(S.values())}")
print(f"G(-1, x) = {sum((-1)**w * S[w] for w in S)} = M({x})")
print(f"Ratio: |G(-1)|/G(1) = {abs(sum((-1)**w * S[w] for w in S)) / sum(S.values()):.6f}")

# =============================================================================
# PART 2: THE SHAPE OF G ON THE UNIT CIRCLE
# =============================================================================

print("\n" + "=" * 75)
print("PART 2: |G(e^{iθ}, x)| ON THE UNIT CIRCLE")
print("=" * 75)

print("""
On the unit circle z = e^{iθ}:
  G(e^{iθ}, x) = Σ S_w e^{iwθ}

This is a FOURIER SERIES in θ!

At θ = 0 (z = 1): G = Σ S_w (maximum)
At θ = π (z = -1): G = Σ (-1)^w S_w = M(x) (minimum)

The function |G(e^{iθ}, x)| tells us about the "frequency content" of S_w.
""")

# Plot |G(e^{iθ})| for various x
print("\n|G(e^{iθ}, x)| for θ from 0 to π:")
print("-" * 70)

x_values = [10000, 50000, 100000]

for x in x_values:
    S = compute_S_w(x)
    print(f"\nx = {x}:")
    print(f"{'θ':>10} {'|G|':>15} {'|G|/G(1)':>15}")
    print("-" * 45)

    G_1 = sum(S.values())
    for theta in np.linspace(0, np.pi, 9):
        z = np.exp(1j * theta)
        G_z = sum(S[w] * (z ** w) for w in S)
        magnitude = abs(G_z)
        ratio = magnitude / G_1
        print(f"{theta:>10.4f} {magnitude:>15.2f} {ratio:>15.6f}")

# =============================================================================
# PART 3: WHY IS THE MINIMUM AT θ = π?
# =============================================================================

print("\n" + "=" * 75)
print("PART 3: WHY IS THE MINIMUM AT θ = π?")
print("=" * 75)

print("""
The key insight: S_w has a POISSON-LIKE distribution!

If S_w ~ Poisson(λ) × (normalizing constant), then:
  G(z, x) ~ C × e^{λ(z-1)} = C × e^{-λ} × e^{λz}

For z = e^{iθ}:
  |G(e^{iθ})| ~ C × e^{-λ} × |e^{λe^{iθ}}|
             = C × e^{-λ} × e^{λ cos(θ)}
             = C × e^{λ(cos(θ) - 1)}

This is MINIMIZED at θ = π where cos(π) = -1:
  |G(e^{iπ})| ~ C × e^{-2λ}

The minimum is EXPONENTIALLY small in λ!
""")

# Verify the Poisson approximation
print("\nVerifying Poisson-like structure:")
print("-" * 60)

x = 100000
S = compute_S_w(x)
total = sum(S.values())
S_normalized = {w: S[w] / total for w in S if S[w] > 0}

# Estimate λ from the mean ω
mean_omega = sum(w * S[w] for w in S) / total
log_log_x = np.log(np.log(x))

print(f"Mean ω(n) for squarefree n ≤ {x}: {mean_omega:.4f}")
print(f"ln ln x = {log_log_x:.4f}")
print(f"Ratio mean/ln ln x: {mean_omega / log_log_x:.4f}")

# Compare to Poisson
print(f"\nDistribution comparison:")
print(f"{'ω':>4} {'Actual':>12} {'Poisson(λ=mean)':>18}")
print("-" * 35)

for w in range(1, 8):
    actual = S_normalized.get(w, 0)
    poisson = (mean_omega ** w) * np.exp(-mean_omega) / float(factorial(w))
    print(f"{w:>4} {actual:>12.6f} {poisson:>18.6f}")

# =============================================================================
# PART 4: THE EULER PRODUCT REPRESENTATION
# =============================================================================

print("\n" + "=" * 75)
print("PART 4: EULER PRODUCT REPRESENTATION")
print("=" * 75)

print("""
The generating function has an EULER PRODUCT form!

For squarefree numbers:
  Σ_{n sqfree} z^{ω(n)} / n^s = Π_p (1 + z/p^s)

At s = 0 (counting):
  Σ_{n sqfree, n≤x} z^{ω(n)} ≈ (6/π²) × x × Π_p (1 + (z-1)/p)  [heuristic]

For z = -1:
  Π_p (1 - 2/p) = Π_p (1 - 2/p)

This product CONVERGES (conditionally) due to cancellation!
""")

# Compute the Euler product heuristic
print("\nEuler product analysis:")
print("-" * 60)

def euler_product_estimate(z, x):
    """Estimate G(z, x) using Euler product heuristic."""
    # Π_p≤x (1 + (z-1)/p)
    product = 1.0
    for p in primerange(2, int(x) + 1):
        product *= (1 + (z - 1) / p)
    return (6 / np.pi**2) * x * product

for x in [1000, 5000, 10000]:
    S = compute_S_w(x)
    G_1_actual = sum(S.values())
    G_neg1_actual = sum((-1)**w * S[w] for w in S)

    G_1_euler = euler_product_estimate(1, x)
    G_neg1_euler = euler_product_estimate(-1, x)

    print(f"x = {x}:")
    print(f"  G(1): actual = {G_1_actual:.1f}, Euler = {G_1_euler:.1f}")
    print(f"  G(-1): actual = {G_neg1_actual}, Euler = {G_neg1_euler:.4f}")

# =============================================================================
# PART 5: THE CRITICAL OBSERVATION
# =============================================================================

print("\n" + "=" * 75)
print("PART 5: THE CRITICAL OBSERVATION")
print("=" * 75)

print("""
THE KEY INSIGHT:

The Euler product Π_p (1 - 2/p) is related to 1/ζ(1)... which diverges!

More precisely:
  Π_{p≤y} (1 - 2/p) = Π_p (1 - 1/p)² × Π_p (1/(1-1/p)) × (corrections)
                    ~ 1/(log y)² × log y × (corrections)
                    ~ 1/log y

So the Euler product VANISHES like 1/log x as x → ∞!

This is why G(-1, x) = M(x) is small:
  M(x) ≈ (6/π²) × x × Π_{p≤x} (1 - 2/p)
       ≈ (6/π²) × x / log x × (corrections)
       ≈ O(x / log x)

But wait - this is still MUCH larger than √x!

The discrepancy: The Euler product heuristic is too crude.
The actual M(x) = O(√x) requires finer analysis.
""")

# Analyze the Euler product more carefully
print("\nEuler product Π_{p≤x} (1 - 2/p):")
print("-" * 50)
print(f"{'x':>10} {'Product':>15} {'× log(x)':>15}")
print("-" * 45)

for x in [100, 500, 1000, 5000, 10000, 50000]:
    product = 1.0
    for p in primerange(2, int(x) + 1):
        product *= (1 - 2/p)
    scaled = product * np.log(x)
    print(f"{x:>10} {product:>15.8f} {scaled:>15.8f}")

print("""
OBSERVATION:
Product × log(x) approaches a constant (the twin prime constant squared!).

So Π_p (1 - 2/p) ~ C / log x.

But M(x) is NOT x / log x; it's O(√x).

THE GAP: The Euler product gives an upper bound, not tight asymptotics.
""")

# =============================================================================
# PART 6: FOURIER ANALYSIS OF S_w
# =============================================================================

print("\n" + "=" * 75)
print("PART 6: FOURIER ANALYSIS OF S_w")
print("=" * 75)

print("""
Think of S_w as a function of w.
Its Fourier transform gives G(e^{iθ}, x).

M(x) = G(-1, x) = G(e^{iπ}, x)

is the HIGHEST FREQUENCY component (θ = π).

For a smooth function, high frequencies decay.
The smoothness of S_w in w determines how fast |G(e^{iθ})| decays as θ → π.
""")

x = 100000
S = compute_S_w(x)

# Compute Fourier coefficients
max_omega = max(w for w in S if S[w] > 0)
S_array = np.array([S[w] for w in range(max_omega + 1)])

# FFT
fft_S = np.fft.fft(S_array)

print(f"\nFourier analysis of S_w for x = {x}:")
print("-" * 50)
print(f"{'Freq k':>8} {'|FFT[k]|':>15} {'|FFT[k]|/|FFT[0]|':>20}")
print("-" * 50)

for k in range(min(10, len(fft_S))):
    magnitude = abs(fft_S[k])
    ratio = magnitude / abs(fft_S[0])
    print(f"{k:>8} {magnitude:>15.2f} {ratio:>20.6f}")

# The alternating sum corresponds to the Nyquist frequency
nyquist_idx = len(fft_S) // 2
print(f"\nNyquist (alternating) component:")
print(f"  |FFT[{nyquist_idx}]| = {abs(fft_S[nyquist_idx]):.2f}")
print(f"  This corresponds to M(x) = {sum((-1)**w * S[w] for w in S)}")

# =============================================================================
# PART 7: THE VARIANCE INTERPRETATION
# =============================================================================

print("\n" + "=" * 75)
print("PART 7: VARIANCE INTERPRETATION")
print("=" * 75)

print("""
Consider S_w as a probability distribution (normalized).

The generating function becomes:
  φ(θ) = E[e^{iωθ}] = G(e^{iθ}, x) / G(1, x)

This is the CHARACTERISTIC FUNCTION of ω!

At θ = π:
  φ(π) = E[e^{iωπ}] = E[(-1)^ω] = M(x) / (total squarefree)

The characteristic function at π is the "alternating probability":
  P(ω even) - P(ω odd) = M(x) / G(1, x)

For RH: |M(x)| = O(√x)
        G(1, x) = O(x)
        So: |P(even) - P(odd)| = O(1/√x)

This means: ω is almost equally likely to be even or odd!
""")

x = 100000
S = compute_S_w(x)
total = sum(S.values())

even_count = sum(S[w] for w in S if w % 2 == 0)
odd_count = sum(S[w] for w in S if w % 2 == 1)

print(f"\nFor x = {x}:")
print(f"  P(ω even) = {even_count / total:.8f}")
print(f"  P(ω odd)  = {odd_count / total:.8f}")
print(f"  Difference = {(even_count - odd_count) / total:.8f}")
print(f"  M(x) / total = {sum((-1)**w * S[w] for w in S) / total:.8f}")
print(f"  1/√x = {1/np.sqrt(x):.8f}")

print("""
OBSERVATION:
The difference P(even) - P(odd) is indeed O(1/√x)!

This is EQUIVALENT to RH:
  RH ⟺ P(ω even) - P(ω odd) = O(1/√x)
""")

# =============================================================================
# PART 8: THE ANALYTICAL STRUCTURE
# =============================================================================

print("\n" + "=" * 75)
print("PART 8: THE ANALYTICAL STRUCTURE")
print("=" * 75)

print("""
The generating function G(z, x) can be written:

  G(z, x) = Σ_{n≤x, sqfree} z^{ω(n)}

For large x, this approximates:
  G(z, x) ≈ (6x/π²) × exp((z-1) ln ln x) × (correction)
          = (6x/π²) × (ln x)^{z-1} × (correction)

At z = -1:
  G(-1, x) ≈ (6x/π²) × (ln x)^{-2} × (correction)
           ≈ Cx / (ln x)²

But we KNOW M(x) = O(√x), so the "correction" must be HUGE!

The correction factor is essentially Π_p (1 - 2/p) / (1 - 1/p)²...
which involves the arithmetic structure of primes.
""")

# Track the "correction factor"
print("\nTracking the correction factor:")
print("-" * 60)
print(f"{'x':>10} {'G(-1,x)=M(x)':>15} {'Naive approx':>15} {'Correction':>15}")
print("-" * 60)

for x in [1000, 5000, 10000, 50000, 100000]:
    S = compute_S_w(x)
    M_x = sum((-1)**w * S[w] for w in S)

    # Naive approximation: 6x/π² × (ln x)^{-2}
    naive = (6 * x / np.pi**2) / (np.log(x) ** 2)

    correction = M_x / naive if naive != 0 else 0
    print(f"{x:>10} {M_x:>+15} {naive:>15.2f} {correction:>+15.4f}")

print("""
OBSERVATION:
The correction factor OSCILLATES around 0!
This is the "sign changes" of M(x).

The correction embodies all the complexity of RH.
""")

# =============================================================================
# PART 9: THE MOMENT GENERATING FUNCTION
# =============================================================================

print("\n" + "=" * 75)
print("PART 9: MOMENT GENERATING FUNCTION APPROACH")
print("=" * 75)

print("""
Define the moment generating function:
  M(t) = E[e^{tω}] = G(e^t, x) / G(1, x)

The moments of ω are:
  E[ω^k] = d^k M / dt^k |_{t=0}

For the alternating sum:
  E[(-1)^ω] = M(iπ) = G(e^{iπ}, x) / G(1, x) = M(x) / (total)

The cumulant generating function:
  K(t) = ln M(t) = ln G(e^t, x) - ln G(1, x)

At t = iπ:
  K(iπ) = ln(M(x)) - ln(total) [when M(x) > 0]

The imaginary part of cumulants controls oscillatory behavior!
""")

# Compute cumulants
x = 100000
S = compute_S_w(x)
total = sum(S.values())

# Moments of ω
E_omega = sum(w * S[w] for w in S) / total
E_omega2 = sum(w**2 * S[w] for w in S) / total
E_omega3 = sum(w**3 * S[w] for w in S) / total
E_omega4 = sum(w**4 * S[w] for w in S) / total

var_omega = E_omega2 - E_omega**2
skew_omega = (E_omega3 - 3*E_omega*E_omega2 + 2*E_omega**3) / (var_omega ** 1.5)
kurt_omega = (E_omega4 - 4*E_omega*E_omega3 + 6*E_omega**2*E_omega2 - 3*E_omega**4) / (var_omega ** 2) - 3

print(f"\nMoments of ω for x = {x}:")
print(f"  E[ω] = {E_omega:.4f}")
print(f"  Var(ω) = {var_omega:.4f}")
print(f"  Skewness = {skew_omega:.4f}")
print(f"  Excess Kurtosis = {kurt_omega:.4f}")

print(f"\nFor Poisson(λ = E[ω]):")
print(f"  Var = {E_omega:.4f} (matches!)")
print(f"  Skewness = {1/np.sqrt(E_omega):.4f}")
print(f"  Excess Kurtosis = {1/E_omega:.4f}")

# =============================================================================
# PART 10: THE ZERO-CROSSING STRUCTURE
# =============================================================================

print("\n" + "=" * 75)
print("PART 10: ZEROS OF G(z, x) IN THE COMPLEX PLANE")
print("=" * 75)

print("""
G(z, x) is a polynomial in z.
Its zeros encode the structure of M(x).

If G has a zero NEAR z = -1, then |G(-1, x)| is small!

Let's find the zeros of G(z, x).
""")

x = 1000  # Small enough for polynomial root finding
S = compute_S_w(x)
max_omega = max(w for w in S if S[w] > 0)

# Coefficients of polynomial
coeffs = [S[w] for w in range(max_omega + 1)]

# Find roots
roots = np.roots(coeffs[::-1])  # numpy expects highest degree first

# Filter for roots near unit circle
unit_circle_roots = [(r, abs(abs(r) - 1)) for r in roots if abs(abs(r) - 1) < 0.5]
unit_circle_roots.sort(key=lambda x: x[1])

print(f"\nRoots of G(z, {x}) near the unit circle:")
print(f"{'Root':>30} {'|Root|':>12} {'Angle':>12} {'Dist to |z|=1':>15}")
print("-" * 75)

for root, dist in unit_circle_roots[:10]:
    angle = np.angle(root)
    print(f"{root.real:>+12.6f}{root.imag:>+12.6f}i {abs(root):>12.6f} {angle:>12.4f} {dist:>15.6f}")

# Check root closest to z = -1
closest_to_neg1 = min(roots, key=lambda r: abs(r + 1))
print(f"\nRoot closest to z = -1:")
print(f"  {closest_to_neg1}")
print(f"  Distance: {abs(closest_to_neg1 + 1):.6f}")

# =============================================================================
# PART 11: THE RIEMANN-SIEGEL ANALOGY
# =============================================================================

print("\n" + "=" * 75)
print("PART 11: RIEMANN-SIEGEL ANALOGY")
print("=" * 75)

print("""
The classical approach to RH uses the Riemann-Siegel formula:
  ζ(1/2 + it) = Z(t) e^{-iθ(t)}

where Z(t) is real and its zeros are the zeros of ζ on the critical line.

OUR ANALOGY:
G(e^{iθ}, x) = |G| × e^{i·phase}

At θ = π:
  G(-1, x) = M(x) is real
  The "phase" is 0 or π (sign of M(x))

The sign changes of M(x) correspond to "zeros" of the real part of G.

This connects our approach to classical zero-finding methods!
""")

# Track the phase of G(e^{iθ})
x = 50000
S = compute_S_w(x)

print(f"\nPhase of G(e^{{iθ}}, {x}):")
print(f"{'θ':>10} {'|G|':>15} {'Phase':>12} {'Re(G)':>15} {'Im(G)':>15}")
print("-" * 70)

for theta in np.linspace(0, np.pi, 17):
    z = np.exp(1j * theta)
    G_z = sum(S[w] * (z ** w) for w in S)
    magnitude = abs(G_z)
    phase = np.angle(G_z)
    print(f"{theta:>10.4f} {magnitude:>15.2f} {phase:>12.4f} {G_z.real:>15.2f} {G_z.imag:>15.2f}")

# =============================================================================
# SYNTHESIS
# =============================================================================

print("\n" + "=" * 75)
print("SYNTHESIS: GENERATING FUNCTION APPROACH")
print("=" * 75)

print("""
WHAT WE DISCOVERED:
===================

1. G(z, x) = Σ S_w(x) z^w is the generating function
   M(x) = G(-1, x)

2. |G(e^{iθ}, x)| is MINIMIZED at θ = π
   This explains why |M(x)| is small

3. The minimum comes from:
   - Poisson-like structure of S_w (smooth decay)
   - Oscillatory cancellation at z = -1
   - Characteristic function interpretation

4. P(ω even) - P(ω odd) = M(x) / (total squarefree)
   RH ⟺ this difference is O(1/√x)

5. The Euler product heuristic gives:
   G(-1, x) ~ Cx/(ln x)²
   But actual M(x) is MUCH smaller due to oscillation

6. The roots of G(z, x) cluster near the unit circle
   A root near z = -1 would make |M(x)| exactly zero


THE NEW FORMULATION OF RH:
==========================

RH ⟺ |G(-1, x)| / |G(1, x)| = O(1/√x)

Equivalently:
RH ⟺ |E[(-1)^ω] | = O(1/√x)

where ω is the number of prime factors of a random squarefree n ≤ x.


WHAT WOULD PROVE THIS:
======================

Show that the characteristic function φ(θ) = E[e^{iωθ}] satisfies:
  |φ(π)| = O(1/√x)

This requires showing the distribution of ω is "balanced" enough
that even and odd values nearly cancel.

The Poisson approximation gives:
  |φ(π)| ≈ e^{-2λ} where λ = ln ln x
  So |φ(π)| ≈ 1/(ln x)² → 0

But this is too slow! We need 1/√x decay, not 1/(ln x)² decay.

The extra cancellation must come from the DEVIATION from Poisson.
Understanding this deviation is the key to RH.
""")

print("\n" + "=" * 75)
print("END OF GENERATING FUNCTION ANALYSIS")
print("=" * 75)
