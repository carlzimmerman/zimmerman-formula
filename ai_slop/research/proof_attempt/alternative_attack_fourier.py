"""
ALTERNATIVE ATTACK: FOURIER ANALYSIS
=====================================

The Möbius function μ(n) and Mertens function M(n) have rich
Fourier structure. Can we exploit this to get bounds?

Key ideas:
1. Fourier transform of μ(n) over Z/NZ
2. Exponential sums involving μ
3. Connection to Ramanujan sums
4. Character sums and L-functions

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, gcd, totient, divisors
from scipy.fft import fft, ifft
import cmath

print("=" * 80)
print("ALTERNATIVE ATTACK: FOURIER ANALYSIS")
print("=" * 80)

# Setup
MAX_N = 10000
M_array = [0] * (MAX_N + 1)
mu_array = [0] * (MAX_N + 1)

cumsum = 0
for n in range(1, MAX_N + 1):
    mu_array[n] = int(mobius(n))
    cumsum += mu_array[n]
    M_array[n] = cumsum

def M(x):
    return M_array[int(x)] if 1 <= int(x) <= MAX_N else 0

def mu(n):
    return mu_array[int(n)] if int(n) <= MAX_N else int(mobius(int(n)))

print("Setup complete.\n")

# =============================================================================
# PART 1: DISCRETE FOURIER TRANSFORM OF μ
# =============================================================================

print("=" * 60)
print("PART 1: DFT OF MOBIUS FUNCTION")
print("=" * 60)

print("""
Define the DFT of μ over [1, N]:
  μ_hat(k) = Σ_{n=1}^{N} μ(n) exp(-2πink/N)

The DFT at k=0 gives M(N) = Σ μ(n).
What about other frequencies?
""")

for N in [100, 500, 1000]:
    # Compute DFT
    mu_vec = np.array([mu(n) for n in range(1, N + 1)])
    mu_hat = fft(mu_vec)

    # Analyze the spectrum
    magnitudes = np.abs(mu_hat)
    phases = np.angle(mu_hat)

    print(f"\nN = {N}:")
    print(f"  μ_hat(0) = M(N) = {mu_hat[0].real:.2f}")
    print(f"  max|μ_hat(k)| = {np.max(magnitudes):.2f} at k = {np.argmax(magnitudes)}")
    print(f"  mean|μ_hat(k)| = {np.mean(magnitudes):.2f}")
    print(f"  Parseval: Σ|μ_hat|²/N = {np.sum(magnitudes**2)/N:.2f}")
    print(f"  (Should equal sum of mu(n)^2 = num sqfree <= N ~ 6N/pi^2)")

    # Expected from Parseval
    expected_parseval = 6 * N / (np.pi**2)
    print(f"  Expected: {expected_parseval:.2f}")

# =============================================================================
# PART 2: EXPONENTIAL SUMS WITH μ
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: EXPONENTIAL SUMS")
print("=" * 60)

print("""
The sum S(α) = Σ_{n≤N} μ(n) e(nα) where e(x) = exp(2πix)

For rational α = a/q:
  S(a/q) relates to Ramanujan sums!

Ramanujan sum: c_q(n) = Σ_{(a,q)=1} e(an/q) = μ(q/gcd(n,q)) φ(q)/φ(q/gcd(n,q))
""")

def exponential_sum(N, alpha):
    """Compute S(α) = Σ μ(n) e(nα)"""
    return sum(mu(n) * cmath.exp(2j * cmath.pi * n * alpha) for n in range(1, N + 1))

N = 1000
print(f"\nExponential sums for N = {N}:")

for alpha in [0, 0.5, 1/3, 1/4, 1/5, 1/7, np.sqrt(2)/10]:
    S = exponential_sum(N, alpha)
    print(f"  S({alpha:.4f}) = {S.real:.2f} + {S.imag:.2f}i, |S| = {abs(S):.2f}")

# =============================================================================
# PART 3: RAMANUJAN SUMS
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: RAMANUJAN SUMS CONNECTION")
print("=" * 60)

print("""
Ramanujan sum: c_q(n) = Σ_{1≤a≤q, gcd(a,q)=1} e(an/q)

Key identity: c_q(n) = μ(q/d) φ(q)/φ(q/d) where d = gcd(n,q)

The Möbius function appears in Ramanujan sums!
Can we use this to bound M(N)?
""")

def ramanujan_sum(q, n):
    """Compute c_q(n)"""
    d = gcd(q, n)
    if q % d != 0:
        return 0
    return mu(q // d) * totient(q) // totient(q // d)

# Verify the formula
print("Verification of Ramanujan sum formula:")
for q in [6, 10, 12]:
    for n in [1, 2, 3, 4, 5, 6]:
        # Direct computation
        direct = sum(cmath.exp(2j * cmath.pi * a * n / q)
                    for a in range(1, q + 1) if gcd(a, q) == 1)
        # Formula
        formula = ramanujan_sum(q, n)
        print(f"  c_{q}({n}) = {direct.real:.2f} (direct), {formula} (formula)")

# =============================================================================
# PART 4: LARGE SIEVE INEQUALITY
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: LARGE SIEVE APPROACH")
print("=" * 60)

print("""
The Large Sieve Inequality:

  Σ_{q≤Q} Σ_{a mod q, (a,q)=1} |Σ_{n≤N} a_n e(an/q)|²
    ≤ (N + Q²) Σ_{n≤N} |a_n|²

For a_n = μ(n):
  Σ|a_n|² = #{squarefree ≤ N} ≈ 6N/π²

This bounds AVERAGES of exponential sums, not individual values.
Can we extract pointwise bounds?
""")

N = 1000
# Compute the average exponential sum squared
Q_values = [10, 20, 50]
for Q in Q_values:
    total = 0
    count = 0
    for q in range(1, Q + 1):
        for a in range(1, q + 1):
            if gcd(a, q) == 1:
                S = exponential_sum(N, a/q)
                total += abs(S)**2
                count += 1

    avg = total / count if count > 0 else 0
    large_sieve_bound = (N + Q**2) * (6 * N / np.pi**2)

    print(f"Q = {Q}: avg|S|² = {avg:.2f}, Large Sieve bound = {large_sieve_bound:.2f}")

# =============================================================================
# PART 5: PARTIAL SUMS AS FOURIER COEFFICIENTS
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: M(n) AS CONVOLUTION")
print("=" * 60)

print("""
M(n) = Σ_{k≤n} μ(k) = (μ * 1)(n) in summatory sense

In Fourier space:
  M_hat(ξ) = μ_hat(ξ) × (something related to partial sums)

Can we bound M via Fourier techniques?
""")

# Look at the "derivative" μ(n) = M(n) - M(n-1)
# In Fourier space, differentiation is multiplication

N = 500
mu_vec = np.array([mu(n) for n in range(1, N + 1)])
M_vec = np.array([M(n) for n in range(1, N + 1)])

mu_hat = fft(mu_vec)
M_hat = fft(M_vec)

# The relationship: M_hat(k) = μ_hat(k) / (1 - e^{-2πik/N}) for k ≠ 0
print(f"\nFourier relationship for N = {N}:")
print(f"  M_hat(0) = Σ M(n) = {M_hat[0].real:.2f}")
print(f"  μ_hat(0) = M(N) = {mu_hat[0].real:.2f}")

# Check the relationship for a few k values
print("\n  Checking M_hat(k) vs μ_hat(k) / (1 - e^{-2πik/N}):")
for k in [1, 2, 5, 10, 50]:
    if k < N:
        factor = 1 - cmath.exp(-2j * cmath.pi * k / N)
        predicted = mu_hat[k] / factor if abs(factor) > 1e-10 else 0
        actual = M_hat[k]
        print(f"    k={k}: predicted = {abs(predicted):.2f}, actual = {abs(actual):.2f}")

# =============================================================================
# PART 6: VARIANCE VIA FOURIER
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: VARIANCE ANALYSIS VIA FOURIER")
print("=" * 60)

print("""
By Parseval:
  Σ|M_hat(k)|²/N = Σ M(n)²/N = V(N)

Can we bound individual |M_hat(k)|?
""")

N = 2000
M_vec = np.array([M(n) for n in range(1, N + 1)])
M_hat = fft(M_vec)

magnitudes = np.abs(M_hat)

print(f"For N = {N}:")
print(f"  Σ|M_hat|²/N = {np.sum(magnitudes**2)/N:.2f}")
print(f"  Σ M(n)²/N = {np.sum(M_vec**2)/N:.2f} (direct)")
print(f"  max|M_hat(k)| = {np.max(magnitudes):.2f}")

# Where are the large Fourier coefficients?
top_k = np.argsort(magnitudes)[-10:][::-1]
print(f"\n  Top 10 Fourier coefficients:")
for k in top_k:
    print(f"    k = {k}: |M_hat| = {magnitudes[k]:.2f}")

# =============================================================================
# PART 7: DIRICHLET CHARACTERS
# =============================================================================

print("\n" + "=" * 60)
print("PART 7: DIRICHLET CHARACTERS")
print("=" * 60)

print("""
For a Dirichlet character χ mod q:
  L(s, χ) = Σ χ(n)/n^s
  M(x, χ) = Σ_{n≤x} χ(n)μ(n)

The twisted Mertens function!
If we could bound M(x, χ) for all χ, we'd have information about M(x).
""")

# Compute M(x, χ) for principal character mod q
def twisted_mertens(x, q):
    """M(x) restricted to n coprime to q."""
    return sum(mu(n) for n in range(1, int(x) + 1) if gcd(n, q) == 1)

print("\nTwisted Mertens M(N, χ_0) for principal character:")
N = 1000
for q in [2, 3, 6, 10, 30]:
    M_twisted = twisted_mertens(N, q)
    phi_q = totient(q)
    print(f"  q = {q}: M({N}, χ_0) = {M_twisted}, φ(q) = {phi_q}")

# =============================================================================
# PART 8: SPECTRAL INTERPRETATION
# =============================================================================

print("\n" + "=" * 60)
print("PART 8: SPECTRAL INTERPRETATION")
print("=" * 60)

print("""
The Fourier spectrum of M(n) shows where the "energy" is.

If M(n) = O(√n), then most energy should be at low frequencies.
Let's check the energy distribution across frequency bands.
""")

N = 2000
M_vec = np.array([M(n) for n in range(1, N + 1)])
M_hat = fft(M_vec)
power = np.abs(M_hat)**2

# Energy in frequency bands
bands = [(0, N//100), (N//100, N//10), (N//10, N//2), (N//2, N)]
print(f"\nEnergy distribution for N = {N}:")
total_power = np.sum(power)
for low, high in bands:
    band_power = np.sum(power[low:high])
    print(f"  k ∈ [{low}, {high}): {100*band_power/total_power:.1f}% of energy")

# =============================================================================
# PART 9: ATTEMPTING A FOURIER BOUND
# =============================================================================

print("\n" + "=" * 60)
print("PART 9: ATTEMPTING A FOURIER BOUND")
print("=" * 60)

print("""
IDEA: If we can bound |M_hat(k)| for k ≠ 0, we can bound M(n).

By inverse DFT:
  M(n) = (1/N) Σ_k M_hat(k) e(nk/N)

So:
  |M(n)| ≤ (1/N) Σ_k |M_hat(k)|

We need |M_hat(k)| to be small enough that the sum is O(√N).

If |M_hat(k)| = O(1) for all k: |M(n)| ≤ O(1) - TOO STRONG (false)
If |M_hat(k)| = O(√N): |M(n)| ≤ O(√N) - PLAUSIBLE?
""")

N = 2000
M_vec = np.array([M(n) for n in range(1, N + 1)])
M_hat = fft(M_vec)
magnitudes = np.abs(M_hat)

sqrt_N = np.sqrt(N)
count_large = np.sum(magnitudes > sqrt_N)
max_M_hat = np.max(magnitudes)

print(f"For N = {N}:")
print(f"  √N = {sqrt_N:.2f}")
print(f"  max|M_hat| = {max_M_hat:.2f}")
print(f"  Count k where |M_hat(k)| > sqrt(N): {count_large}")
print(f"  max|M_hat|/N = {max_M_hat/N:.4f}")

# The bound |M(n)| ≤ (1/N) Σ|M_hat| gives:
sum_M_hat = np.sum(magnitudes)
fourier_bound = sum_M_hat / N
actual_max_M = np.max(np.abs(M_vec))

print(f"\n  Fourier bound on |M(n)|: {fourier_bound:.2f}")
print(f"  Actual max|M(n)|: {actual_max_M}")
print(f"  √N: {sqrt_N:.2f}")

# =============================================================================
# PART 10: HONEST ASSESSMENT
# =============================================================================

print("\n" + "=" * 60)
print("PART 10: HONEST ASSESSMENT")
print("=" * 60)

print("""
FOURIER ANALYSIS FINDINGS:

1. DFT of μ: Parseval gives Σ|μ_hat|²/N ≈ 6/π² (energy in squarefrees)

2. Exponential sums: S(a/q) connects to Ramanujan sums and L-functions

3. Large Sieve: Bounds AVERAGES of exponential sums, not pointwise

4. M_hat relationship: M_hat(k) = μ_hat(k) / (1 - e^{-2πik/N})

5. Energy distribution: Most energy at low frequencies (good sign)

WHY THIS DOESN'T GIVE A PROOF:

The Fourier transform of M(n) is well-understood analytically via
the Mellin transform / Perron's formula:

  M(x) = (1/2πi) ∫ (x^s / sζ(s)) ds

The Fourier properties of M encode information about ζ zeros!
Bounding |M_hat(k)| requires knowing ζ has no zeros off the critical line.

The Fourier approach is EQUIVALENT to the analytic approach, not independent.

POSSIBLE VALUE:

The spectral decomposition might reveal structure that could be exploited
with new ideas. But as a direct proof technique, it doesn't bypass RH.
""")

print("=" * 80)
print("FOURIER ANALYSIS COMPLETE")
print("=" * 80)
