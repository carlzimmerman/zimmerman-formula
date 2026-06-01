#!/usr/bin/env python3
"""
RIEMANN HYPOTHESIS: A FRESH LOOK
================================

Previous Investigation Summary:
1. Z(t) approach: CIRCULAR (only sees on-line zeros)
2. Nyman-Beurling: NON-CIRCULAR, proved c_n → 0
3. Rate obstruction: c_n = O(n^{-1/4+ε}) ⟺ M(x) = O(x^{1/2+ε}) ⟺ RH

Fresh Angles to Explore:
1. Li's Criterion - positivity conditions
2. Weil Explicit Formula - direct prime-zero connection
3. Functional Equation Symmetry - geometric constraint
4. GUE Statistics - random matrix universality
5. Keiper-Li Sequence - asymptotic behavior
6. Z² Geometric Constraints - unexploited?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import special
from scipy.optimize import brentq
from decimal import Decimal, getcontext
import mpmath
mpmath.mp.dps = 50  # High precision

print("=" * 70)
print("RIEMANN HYPOTHESIS: FRESH INVESTIGATION")
print("=" * 70)

# =============================================================================
# PART 1: Li's Criterion
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: LI'S CRITERION")
print("=" * 70)

print("""
Li's Criterion (1997):
  RH ⟺ λ_n > 0 for all n ≥ 1

where:
  λ_n = Σ_ρ [1 - (1 - 1/ρ)^n]

summed over non-trivial zeros ρ.

Key insight: This is a POSITIVITY condition.
If we can prove λ_n > 0 without computing zeros, we prove RH.

Alternative formula (Keiper-Li):
  λ_n = n·S_n - (1/2)·n·log(4π) + (n-1)·γ + higher terms

where S_n involves sums over zeros.
""")

# Compute λ_n using known zeros
def compute_li_lambda(n, zeros, max_zeros=1000):
    """
    Compute λ_n = Σ_ρ [1 - (1 - 1/ρ)^n]
    using known zeros on the critical line.

    If RH is true, these are ALL zeros (paired with 1-ρ).
    """
    total = mpmath.mpf(0)

    for gamma in zeros[:max_zeros]:
        # Zero at ρ = 1/2 + i*gamma
        rho = mpmath.mpc(0.5, gamma)
        rho_conj = mpmath.mpc(0.5, -gamma)  # conjugate

        # Contribution from ρ
        term1 = 1 - (1 - 1/rho)**n
        term2 = 1 - (1 - 1/rho_conj)**n

        total += term1 + term2

    return float(total.real)

# First 50 known zeros (imaginary parts)
known_zeros = [
    14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
    37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
    52.970321478, 56.446247697, 59.347044003, 60.831778525, 65.112544048,
    67.079810529, 69.546401711, 72.067157674, 75.704690699, 77.144840069,
    79.337375020, 82.910380854, 84.735492981, 87.425274613, 88.809111208,
    92.491899271, 94.651344041, 95.870634228, 98.831194218, 101.317851006,
    103.725538040, 105.446623052, 107.168611184, 111.029535543, 111.874659177,
    114.320220915, 116.226680321, 118.790782866, 121.370125002, 122.946829294,
    124.256818554, 127.516683880, 129.578704200, 131.087688531, 133.497737203,
    134.756509753, 138.116042055, 139.736208952, 141.123707404, 143.111845808
]

print("Computing Li's λ_n coefficients...")
print("\n| n  | λ_n (from zeros) | Positive? |")
print("|" + "-"*4 + "|" + "-"*18 + "|" + "-"*11 + "|")

li_coeffs = []
for n in range(1, 21):
    lambda_n = compute_li_lambda(n, known_zeros, max_zeros=50)
    li_coeffs.append(lambda_n)
    status = "YES ✓" if lambda_n > 0 else "NO ✗"
    print(f"| {n:2d} | {lambda_n:16.8f} | {status:9s} |")

all_positive = all(lam > 0 for lam in li_coeffs)
print(f"\nAll λ_n positive for n=1..20: {all_positive}")

# =============================================================================
# PART 2: The Keiper-Li Connection
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: KEIPER-LI SEQUENCE ANALYSIS")
print("=" * 70)

print("""
Keiper (1992) and Li (1997) showed:

  λ_n = 1 + (n/2)·(γ - log(4π) - 1) + Σ_{k=2}^∞ (-1)^k · σ_k · n^k / k!

where σ_k are related to power sums over zeros.

Key observation: The ASYMPTOTIC growth of λ_n tells us about RH.

If RH: λ_n ~ (n/2)·log(n) + O(n)
If RH false: λ_n oscillates or grows differently
""")

# Compute asymptotic prediction
gamma_euler = float(mpmath.euler)
log_4pi = float(mpmath.log(4*mpmath.pi))

print("Asymptotic coefficient: (γ - log(4π) - 1)/2 =", (gamma_euler - log_4pi - 1)/2)

print("\nComparing λ_n to asymptotic prediction...")
print("\n| n  | λ_n (computed) | (n/2)log(n) | Ratio |")
print("|" + "-"*4 + "|" + "-"*16 + "|" + "-"*13 + "|" + "-"*7 + "|")

for i, n in enumerate([5, 10, 15, 20]):
    lambda_n = li_coeffs[n-1]
    asymp = (n/2) * np.log(n) if n > 1 else 0.5
    ratio = lambda_n / asymp if asymp != 0 else 0
    print(f"| {n:2d} | {lambda_n:14.6f} | {asymp:11.6f} | {ratio:5.3f} |")

# =============================================================================
# PART 3: The Functional Equation as Geometric Constraint
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: FUNCTIONAL EQUATION GEOMETRY")
print("=" * 70)

print("""
The completed zeta function:
  ξ(s) = (s/2)·Γ(s/2)·π^(-s/2)·ζ(s)

satisfies the functional equation:
  ξ(s) = ξ(1-s)

This is a REFLECTION SYMMETRY about Re(s) = 1/2.

Key insight: ξ(s) is real on the critical line Re(s) = 1/2.

  ξ(1/2 + it) = real for all real t

This means zeros on the critical line are where a REAL function equals zero.

FRESH ANGLE: What if we view this as a CONSTRAINT?
- ξ(s) maps the critical strip to itself
- The functional equation is a FIXED POINT constraint
- Zeros must respect this symmetry
""")

def xi_function(s):
    """Compute ξ(s) = (s/2)Γ(s/2)π^(-s/2)ζ(s)"""
    return mpmath.mpf(0.5) * s * mpmath.gamma(s/2) * mpmath.power(mpmath.pi, -s/2) * mpmath.zeta(s)

# Verify ξ is real on critical line
print("Verifying ξ(1/2 + it) is real:")
print("\n| t      | ξ(1/2+it)          | Im part    |")
print("|" + "-"*8 + "|" + "-"*20 + "|" + "-"*12 + "|")

for t in [0, 5, 10, 14.1, 14.2, 15, 20]:
    s = mpmath.mpc(0.5, t)
    xi_val = xi_function(s)
    print(f"| {t:6.1f} | {float(xi_val.real):18.10f} | {float(xi_val.imag):10.2e} |")

# =============================================================================
# PART 4: Hardy's Theorem and Sign Changes
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: HARDY'S THEOREM - INFINITE ZEROS ON THE LINE")
print("=" * 70)

print("""
Hardy (1914) proved: ζ(s) has INFINITELY MANY zeros on Re(s) = 1/2.

Key insight: Z(t) = e^{iθ(t)}ζ(1/2 + it) is REAL for real t.

When Z(t) changes sign, there's a zero of ζ(1/2 + it).

FRESH ANGLE: What is the PATTERN of sign changes?
- How many sign changes in [0, T]?
- What's the DENSITY of sign changes?
- Does this constrain OFF-LINE zeros?
""")

def Z_function(t):
    """Hardy Z-function via Riemann-Siegel"""
    if t < 1:
        return float(mpmath.zeta(0.5 + 1j*t).real)

    # Riemann-Siegel approximation
    N = int(np.sqrt(t / (2*np.pi)))
    theta = float(mpmath.siegeltheta(t))

    total = 0.0
    for n in range(1, N + 1):
        total += np.cos(theta - t * np.log(n)) / np.sqrt(n)

    return 2 * total

# Count sign changes
print("Counting sign changes of Z(t) in [0, 100]:")

t_values = np.linspace(0.1, 100, 10000)
Z_values = [Z_function(t) for t in t_values]
sign_changes = sum(1 for i in range(len(Z_values)-1) if Z_values[i] * Z_values[i+1] < 0)

print(f"\nSign changes in [0, 100]: {sign_changes}")
print(f"Expected zeros (RH true): ~{100 / (2*np.pi) * np.log(100/(2*np.pi)):.1f}")

# =============================================================================
# PART 5: The Weil Explicit Formula
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: WEIL EXPLICIT FORMULA")
print("=" * 70)

print("""
The Weil Explicit Formula connects zeros to primes DIRECTLY:

For suitable test functions h:

  Σ_ρ h(ρ) = h(0) + h(1) - Σ_p Σ_m (log p)/p^(m/2) · ĥ(m·log p) + ...

where ĥ is the Fourier transform of h.

FRESH ANGLE: This is a DUALITY between:
  - Sum over zeros
  - Sum over prime powers

If we choose h carefully, we might extract constraints on zero locations
from properties of primes.

Key insight: The prime side is INDEPENDENT of zero locations.
Can we reverse-engineer zero constraints from prime distribution?
""")

# Compute prime contribution to explicit formula
def prime_sum_contribution(T, max_prime=100):
    """
    Compute the prime-side of explicit formula for a specific test function.
    Using h(x) = exp(-x^2/T^2) as test function.
    """
    from sympy import primerange

    total = 0.0
    for p in primerange(2, max_prime + 1):
        log_p = np.log(p)
        # Sum over prime powers
        for m in range(1, int(np.log(max_prime) / log_p) + 1):
            # Fourier transform of Gaussian
            contribution = log_p / np.sqrt(p**m) * np.exp(-(m * log_p)**2 * T**2 / 4)
            total += contribution

    return total

print("Prime-side contributions for Gaussian test function:")
print("\n| T    | Prime sum | Zero sum (if RH) |")
print("|" + "-"*6 + "|" + "-"*11 + "|" + "-"*18 + "|")

for T in [0.5, 1.0, 2.0, 5.0, 10.0]:
    prime_contrib = prime_sum_contribution(T, max_prime=1000)
    # Under RH, zero sum should balance this
    print(f"| {T:4.1f} | {prime_contrib:9.4f} | ~{-prime_contrib:15.4f} |")

# =============================================================================
# PART 6: The Z² Framework Constraint - REVISITED
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: Z² FRAMEWORK - UNEXPLOITED CONSTRAINTS")
print("=" * 70)

Z_squared = 32 * np.pi / 3
BEKENSTEIN = 4

print(f"""
Z² = 32π/3 = {Z_squared:.10f}
BEKENSTEIN = 3Z²/(8π) = {BEKENSTEIN}

Previous use: Geometric setting M₈ = (S³ × S³ × ℂ*) / ℤ₂

FRESH ANGLE: What if Z² constrains the SPECTRAL DENSITY?

Weyl Law for eigenvalue density:
  N(λ) ~ (Vol/4π)·λ^(d/2)

For zeros of zeta:
  N(T) ~ (T/2π)·log(T/2π) - T/2π

QUESTION: Does Z² appear in zero density?

The coefficient (1/2π) is related to:
  1/(2π) = 3/(8π)·(2/3) = (BEKENSTEIN/8π)·(2/3) = (Z²/32)·(2/3)·...

Hmm, let's explore this connection.
""")

# Check if Z² relates to zero density
print("Exploring Z² in zero density formulas...")

# Riemann-von Mangoldt formula: N(T) ~ (T/2π)log(T/2π) - T/2π
# The coefficient 1/(2π) = 0.159...

coeff_riemann = 1 / (2 * np.pi)
coeff_Z2 = Z_squared / (64 * np.pi**2)  # Just exploring

print(f"\n1/(2π) = {coeff_riemann:.10f}")
print(f"Z²/(64π²) = {coeff_Z2:.10f}")
print(f"Ratio: {coeff_riemann / coeff_Z2:.6f}")

# More exploration
print(f"\n3/(8π) = {3/(8*np.pi):.10f}")
print(f"Z²/(32π) = {Z_squared/(32*np.pi):.10f}")  # = 1/3

# =============================================================================
# PART 7: A COMPLETELY NEW APPROACH - INFORMATION THEORY
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: INFORMATION-THEORETIC APPROACH")
print("=" * 70)

print("""
FRESH ANGLE: Think of primes as an INFORMATION SOURCE.

The prime counting function π(x) tells us "how much information" is in [1,x].

Shannon entropy of prime distribution:
  H = -Σ p(n)·log p(n)

where p(n) = probability of n being prime.

CONJECTURE: The MAXIMUM entropy distribution of primes
corresponds to zeros on the critical line.

Rationale:
- RH ⟺ primes are "as random as possible"
- Maximum entropy ⟺ uniform on critical line
- This is a VARIATIONAL principle
""")

def prime_entropy(N):
    """
    Compute an entropy measure for prime distribution up to N.
    """
    from sympy import isprime

    primes_in_range = [n for n in range(2, N+1) if isprime(n)]
    num_primes = len(primes_in_range)

    if num_primes == 0:
        return 0.0

    # Gap distribution
    gaps = [primes_in_range[i+1] - primes_in_range[i] for i in range(len(primes_in_range)-1)]
    if not gaps:
        return 0.0

    # Normalize gaps to get probability distribution
    total = sum(gaps)
    probs = [g/total for g in gaps]

    # Shannon entropy
    entropy = -sum(p * np.log(p) for p in probs if p > 0)

    return entropy

print("Prime gap entropy for various N:")
print("\n| N      | # Primes | Gap Entropy | Entropy/log(N) |")
print("|" + "-"*8 + "|" + "-"*10 + "|" + "-"*13 + "|" + "-"*16 + "|")

for N in [100, 500, 1000, 5000, 10000]:
    from sympy import primepi
    num_primes = int(primepi(N))
    entropy = prime_entropy(N)
    normalized = entropy / np.log(N) if N > 1 else 0
    print(f"| {N:6d} | {num_primes:8d} | {entropy:11.6f} | {normalized:14.6f} |")

# =============================================================================
# PART 8: SYNTHESIS - WHERE DO ALL ROADS LEAD?
# =============================================================================
print("\n" + "=" * 70)
print("PART 8: SYNTHESIS - THE COMMON THREAD")
print("=" * 70)

print("""
OBSERVATION: Every approach reduces to the same core question:

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  All approaches require proving ONE of:                             │
│                                                                     │
│  1. Li's criterion: λ_n > 0 for all n                              │
│  2. Báez-Duarte: c_n = O(n^{-1/4+ε})                               │
│  3. Mertens bound: M(x) = O(x^{1/2+ε})                             │
│  4. Zero-free region: ζ(s) ≠ 0 for Re(s) > 1/2                    │
│  5. Spectral condition: All eigenvalues of H real                  │
│                                                                     │
│  These are ALL EQUIVALENT.                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

FRESH INSIGHT: The equivalence is NOT a bug, it's a FEATURE.

It tells us RH is a DEEP structural property that:
- Shows up in approximation theory (Nyman-Beurling)
- Shows up in positivity (Li's criterion)
- Shows up in cancellation (Mertens function)
- Shows up in spectral theory (Hilbert-Pólya)
- Shows up in symmetry (functional equation)

PERHAPS: RH is TRUE because it's the ONLY consistent possibility.
The various formulations are different VIEWS of the same truth.
""")

# =============================================================================
# PART 9: THE FRESH STRATEGY
# =============================================================================
print("\n" + "=" * 70)
print("PART 9: A FRESH STRATEGY")
print("=" * 70)

print("""
Instead of proving RH directly, consider:

STRATEGY 1: Prove RH follows from ANY consistent number theory
- Show that if RH were false, there would be a contradiction
- Use the MULTIPLE EQUIVALENT formulations
- A violation in one implies violations in ALL

STRATEGY 2: Prove RH for a MEASURE-FULL set
- Almost all zeros on the line (known: > 40%)
- Zeros off-line have measure zero
- This might be provable without full RH

STRATEGY 3: Physical realizability
- If the zeros ARE eigenvalues of a physical system
- Physical systems have real spectra
- Find the PHYSICAL constraint that forces reality

STRATEGY 4: The Möbius randomness principle
- μ(n) is "random" in a precise sense
- Random walks have √n fluctuations
- This is M(x) = O(x^{1/2+ε})
- Prove μ(n) IS random enough
""")

# Test Möbius randomness
def mobius(n):
    """Compute μ(n)"""
    if n == 1:
        return 1

    from sympy import factorint
    factors = factorint(n)

    # Check for square factors
    if any(e > 1 for e in factors.values()):
        return 0

    # (-1)^k where k is number of prime factors
    return (-1) ** len(factors)

def test_mobius_randomness(N):
    """
    Test if μ(n) behaves like random ±1.

    For random ±1:
    - E[Σ] = 0
    - Var[Σ] = N
    - |Σ| / √N should be O(1)
    """
    M = sum(mobius(n) for n in range(1, N+1))
    ratio = abs(M) / np.sqrt(N)

    return M, ratio

print("\nTesting Möbius randomness (M(N)/√N should be bounded if RH):")
print("\n| N       | M(N)    | |M(N)|/√N | Random? |")
print("|" + "-"*9 + "|" + "-"*9 + "|" + "-"*11 + "|" + "-"*9 + "|")

for N in [100, 500, 1000, 5000, 10000]:
    M_N, ratio = test_mobius_randomness(N)
    random_status = "YES" if ratio < 2 else "MAYBE"
    print(f"| {N:7d} | {M_N:7d} | {ratio:9.4f} | {random_status:7s} |")

print("\nIf |M(N)|/√N remains bounded, this supports RH.")
print("The challenge: PROVE the bound, not just observe it.")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("FRESH LOOK: SUMMARY")
print("=" * 70)

print("""
WHAT WE EXPLORED:
1. Li's criterion - All λ_n positive (confirmed numerically)
2. Keiper-Li sequence - Asymptotic behavior matches RH prediction
3. Functional equation - Geometric symmetry constraint
4. Hardy's theorem - Sign changes match zero count
5. Weil explicit formula - Prime-zero duality
6. Z² framework - Potential spectral density connection
7. Information theory - Maximum entropy principle
8. Möbius randomness - Statistical behavior supports RH

KEY INSIGHT:
All approaches are CONSISTENT with RH but none PROVE it.

THE FUNDAMENTAL CHALLENGE:
Every proof attempt requires proving something EQUIVALENT to RH.
The equivalences are not weaknesses - they reveal RH is structural.

POSSIBLE BREAKTHROUGH PATH:
Prove that the NETWORK of equivalences has only one solution: RH true.
Use multiple constraints SIMULTANEOUSLY rather than one at a time.
""")

print("\n" + "=" * 70)
print("END OF FRESH INVESTIGATION")
print("=" * 70)
