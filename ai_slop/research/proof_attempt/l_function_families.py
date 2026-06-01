#!/usr/bin/env python3
"""
L-FUNCTION FAMILIES AND KATZ-SARNAK PHILOSOPHY
===============================================

Direction 3: Study families of L-functions to understand RH constraints.

The Katz-Sarnak philosophy:
- L-functions come in natural families
- Each family has a symmetry type (U, Sp, SO(even), SO(odd))
- Statistics of zeros follow random matrix predictions for that type
- Family averages may constrain individual zeros

This script explores:
1. Dirichlet L-functions L(s, χ) for characters χ mod q
2. Low-lying zeros near the real axis
3. One-level density and symmetry type identification
4. Family averages and their RH implications

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from math import sqrt, log, pi, gcd, exp, cos, sin, floor, ceil
from scipy import special
from scipy.integrate import quad
from scipy.optimize import brentq
import cmath

print("=" * 75)
print("L-FUNCTION FAMILIES AND KATZ-SARNAK PHILOSOPHY")
print("=" * 75)

# =============================================================================
# PART 1: DIRICHLET CHARACTERS
# =============================================================================

print("\n" + "=" * 75)
print("PART 1: DIRICHLET CHARACTERS")
print("=" * 75)

def euler_phi(n):
    """Euler's totient function."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def primitive_root(p):
    """Find a primitive root mod p (p prime)."""
    if p == 2:
        return 1
    phi = p - 1
    # Find prime factors of phi
    factors = []
    n = phi
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)

    # Test candidates
    for g in range(2, p):
        is_primitive = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return g
    return None

def dirichlet_characters(q):
    """
    Generate all Dirichlet characters mod q.
    Returns list of (chi_values, is_primitive, is_even) tuples.
    """
    if q == 1:
        return [([1], True, True)]  # Trivial character

    characters = []
    phi_q = euler_phi(q)

    # For prime q, use primitive root
    if all(q % p != 0 for p in range(2, int(sqrt(q)) + 1)) and q > 1:
        g = primitive_root(q)
        # Generate characters using roots of unity
        for k in range(phi_q):
            chi = [0] * q
            chi[0] = 0  # χ(0) = 0

            # Build character from primitive root
            zeta = cmath.exp(2j * pi * k / phi_q)
            power = 1
            for j in range(phi_q):
                chi[pow(g, j, q)] = zeta ** j

            # Check if primitive (non-trivial and doesn't factor through smaller modulus)
            is_primitive = k > 0  # Simplified check

            # Check if even: χ(-1) = 1
            is_even = abs(chi[q - 1] - 1) < 0.01 if q > 1 else True

            characters.append((chi, is_primitive, is_even))
    else:
        # For composite q, use simplified approach
        # Just generate principal character and quadratic character if exists
        chi_principal = [1 if gcd(a, q) == 1 else 0 for a in range(q)]
        characters.append((chi_principal, False, True))

        # Quadratic character (Kronecker symbol)
        if q > 2:
            chi_quad = []
            for a in range(q):
                if gcd(a, q) != 1:
                    chi_quad.append(0)
                else:
                    # Simplified Jacobi symbol computation
                    chi_quad.append(jacobi_symbol(a, q))
            characters.append((chi_quad, True, jacobi_symbol(-1, q) == 1))

    return characters

def jacobi_symbol(a, n):
    """Compute Jacobi symbol (a/n)."""
    if n <= 0 or n % 2 == 0:
        return 0

    a = a % n
    result = 1

    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n

    return result if n == 1 else 0

print("""
Dirichlet characters χ: (Z/qZ)* → C*

Key properties:
- χ(ab) = χ(a)χ(b) (completely multiplicative)
- χ(a) = 0 if gcd(a,q) > 1
- There are φ(q) characters mod q
- χ is primitive if it doesn't factor through smaller modulus
- χ is even if χ(-1) = 1, odd if χ(-1) = -1

The L-function:
  L(s, χ) = Σ_{n=1}^∞ χ(n)/n^s = Π_p (1 - χ(p)/p^s)^{-1}
""")

# Show characters for small q
for q in [3, 5, 7, 8]:
    chars = dirichlet_characters(q)
    print(f"\nCharacters mod {q}: {len(chars)} total")
    for i, (chi, is_prim, is_even) in enumerate(chars[:3]):
        parity = "even" if is_even else "odd"
        prim = "primitive" if is_prim else "imprimitive"
        values = [chi[a] if isinstance(chi[a], (int, float)) else
                  f"{chi[a].real:.2f}+{chi[a].imag:.2f}i" if chi[a].imag >= 0 else
                  f"{chi[a].real:.2f}{chi[a].imag:.2f}i"
                  for a in range(1, min(q, 8))]
        print(f"  χ_{i}: {prim}, {parity}")

# =============================================================================
# PART 2: COMPUTING L-FUNCTION VALUES
# =============================================================================

print("\n" + "=" * 75)
print("PART 2: L-FUNCTION VALUES AND ZEROS")
print("=" * 75)

def L_function_partial(s, chi, q, num_terms=10000):
    """
    Compute L(s, χ) using partial sum.
    """
    result = 0
    for n in range(1, num_terms + 1):
        if gcd(n, q) == 1:
            chi_n = chi[n % q]
            if isinstance(chi_n, complex):
                result += chi_n / (n ** s)
            else:
                result += chi_n / (n ** s)
    return result

def L_function_euler(s, chi, q, max_prime=1000):
    """
    Compute L(s, χ) using Euler product (for Re(s) > 1).
    """
    result = 1.0
    # Sieve primes
    is_prime = [True] * (max_prime + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sqrt(max_prime)) + 1):
        if is_prime[i]:
            for j in range(i*i, max_prime + 1, i):
                is_prime[j] = False

    for p in range(2, max_prime + 1):
        if is_prime[p]:
            chi_p = chi[p % q]
            if isinstance(chi_p, complex):
                factor = 1 - chi_p / (p ** s)
            else:
                factor = 1 - chi_p / (p ** s)
            if abs(factor) > 1e-10:
                result *= 1 / factor

    return result

print("""
For real s > 1, we can compute L(s, χ) directly:

L(s, χ) = Σ χ(n)/n^s = Π_p (1 - χ(p)p^{-s})^{-1}

For the principal character χ_0:
  L(s, χ_0) = ζ(s) × Π_{p|q} (1 - p^{-s})
""")

# Compute some L-values
print("\nL-function values at s = 2:")
print("q  | χ      | L(2, χ) partial | L(2, χ) Euler")
print("-" * 55)

for q in [3, 5, 7, 11]:
    chars = dirichlet_characters(q)
    for i, (chi, is_prim, is_even) in enumerate(chars[:2]):
        L_partial = L_function_partial(2, chi, q, 5000)
        L_euler = L_function_euler(2, chi, q, 500)

        chi_name = f"χ_{i}"
        if isinstance(L_partial, complex):
            print(f"{q:2d} | {chi_name:6s} | {L_partial.real:+.6f}{L_partial.imag:+.6f}i | {L_euler.real:+.6f}{L_euler.imag:+.6f}i")
        else:
            print(f"{q:2d} | {chi_name:6s} | {L_partial:+.10f} | {L_euler:+.10f}")

# =============================================================================
# PART 3: SYMMETRY TYPES
# =============================================================================

print("\n" + "=" * 75)
print("PART 3: SYMMETRY TYPES IN RANDOM MATRIX THEORY")
print("=" * 75)

print("""
KATZ-SARNAK PHILOSOPHY:
Different families of L-functions have different symmetry types,
determined by the low-lying zero statistics.

SYMMETRY TYPES AND THEIR SIGNATURES:

1. UNITARY (U):
   - No functional equation constraint
   - Pair correlation: R_2(x) = 1 - (sin πx / πx)²
   - One-level density: W_U(x) = 1
   - Example: Riemann zeta (single function, trivially unitary)

2. SYMPLECTIC (Sp):
   - Functional equation with + sign
   - One-level density: W_Sp(x) = 1 - sin(2πx)/(2πx)
   - Example: L-functions of even Dirichlet characters
   - Zeros repelled from central point

3. ORTHOGONAL (O):
   - Functional equation with - sign
   - Two subtypes based on central value behavior:

   3a. SO(even):
     - Central value L(1/2, f) ≠ 0
     - W_{SO(even)}(x) = 1 + sin(2πx)/(2πx)
     - Example: L-functions of odd characters, most elliptic curves

   3b. SO(odd):
     - Central value L(1/2, f) = 0 (forced zero)
     - W_{SO(odd)}(x) = 1 + sin(2πx)/(2πx) - 1 (delta at 0)
     - Example: Certain elliptic curve families

KEY INSIGHT:
The symmetry type is determined by the FAMILY structure,
not by individual L-functions.
""")

# One-level density kernels
def W_unitary(x):
    """One-level density for Unitary symmetry."""
    return 1.0

def W_symplectic(x):
    """One-level density for Symplectic symmetry."""
    if abs(x) < 1e-10:
        return 0.0  # 1 - 1 = 0 at x=0
    return 1 - np.sin(2 * np.pi * x) / (2 * np.pi * x)

def W_SO_even(x):
    """One-level density for SO(even) symmetry."""
    if abs(x) < 1e-10:
        return 2.0  # 1 + 1 = 2 at x=0
    return 1 + np.sin(2 * np.pi * x) / (2 * np.pi * x)

def W_SO_odd(x):
    """One-level density for SO(odd) symmetry."""
    # Has delta function at 0, so continuous part is same as SO(even)
    if abs(x) < 1e-10:
        return 2.0
    return 1 + np.sin(2 * np.pi * x) / (2 * np.pi * x)

# Plot comparison (numerical)
print("\nOne-level density W(x) at sample points:")
print("x     | W_U   | W_Sp  | W_SO(even)")
print("-" * 45)

for x in [0.0, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0]:
    print(f"{x:.2f}  | {W_unitary(x):.3f} | {W_symplectic(x):.3f} | {W_SO_even(x):.3f}")

# =============================================================================
# PART 4: LOW-LYING ZEROS OF DIRICHLET L-FUNCTIONS
# =============================================================================

print("\n" + "=" * 75)
print("PART 4: LOW-LYING ZEROS OF DIRICHLET L-FUNCTIONS")
print("=" * 75)

print("""
Low-lying zeros are those closest to the real axis (smallest |γ|).

For a family of L-functions {L(s, f)}, define:
  D_1(φ; f) = Σ_γ φ(γ × log(conductor) / 2π)

where γ runs over zeros of L(s, f) and φ is a test function.

The average over the family:
  <D_1(φ)> = ∫ φ(x) W(x) dx

where W(x) is the one-level density depending on symmetry type.

PREDICTION:
- Symplectic families: zeros repelled from x = 0
- Orthogonal families: zeros attracted to x = 0
""")

# We'll use known low-lying zeros data
# For now, generate synthetic data based on known distributions

def generate_low_lying_zeros_Sp(N, conductor):
    """
    Generate synthetic low-lying zeros for Symplectic family.
    Zeros repelled from origin.
    """
    # Use rejection sampling from W_Sp density
    zeros = []
    scale = log(conductor) / (2 * pi)

    while len(zeros) < N:
        # Sample from proposal distribution (uniform on [0, 2])
        x = np.random.uniform(0, 3)
        # Accept with probability proportional to W_Sp
        if np.random.random() < W_symplectic(x) / 2:
            zeros.append(x / scale)

    return np.array(sorted(zeros))

def generate_low_lying_zeros_SO(N, conductor):
    """
    Generate synthetic low-lying zeros for SO(even) family.
    Zeros attracted to origin.
    """
    zeros = []
    scale = log(conductor) / (2 * pi)

    while len(zeros) < N:
        x = np.random.uniform(0, 3)
        if np.random.random() < W_SO_even(x) / 2.5:
            zeros.append(x / scale)

    return np.array(sorted(zeros))

# Generate samples
np.random.seed(42)
N_samples = 1000
conductor = 100

zeros_Sp = generate_low_lying_zeros_Sp(N_samples, conductor)
zeros_SO = generate_low_lying_zeros_SO(N_samples, conductor)

print(f"\nSynthetic low-lying zeros (conductor = {conductor}):")
print(f"\nSymplectic family (even characters):")
print(f"  Smallest 5 scaled zeros: {zeros_Sp[:5]}")
print(f"  Mean of first zero: {np.mean(zeros_Sp[:100]):.4f}")

print(f"\nOrthogonal family (odd characters):")
print(f"  Smallest 5 scaled zeros: {zeros_SO[:5]}")
print(f"  Mean of first zero: {np.mean(zeros_SO[:100]):.4f}")

# =============================================================================
# PART 5: ONE-LEVEL DENSITY COMPUTATION
# =============================================================================

print("\n" + "=" * 75)
print("PART 5: ONE-LEVEL DENSITY FROM ACTUAL ZETA ZEROS")
print("=" * 75)

print("""
Let's compute the one-level density using actual Riemann zeta zeros.

For the Riemann zeta function:
- Single function, so "family" is trivial
- Expected: Unitary statistics (W = 1)
- But individual zeros show GUE correlations

We'll also analyze what the FAMILY AVERAGE tells us.
""")

# Load Odlyzko zeros if available
try:
    zeros_data = np.loadtxt('spectral_data/zeros1.txt')
    print(f"\nLoaded {len(zeros_data)} Riemann zeta zeros")

    # Normalize zeros (scale by log(γ/2π) to get unit mean spacing)
    mean_spacing = np.mean(np.diff(zeros_data[:1000]))
    normalized_zeros = zeros_data[:1000] / mean_spacing

    # Compute empirical one-level density
    # Use histogram in bins
    n_bins = 50

    # Low-lying zeros: first 100
    low_lying = normalized_zeros[:100]

    # Scale to [0, 2] range
    scaled_zeros = low_lying / low_lying[-1] * 2

    hist, bin_edges = np.histogram(scaled_zeros, bins=n_bins, range=(0, 2), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    print("\nEmpirical one-level density (first 100 zeros, scaled):")
    print("x range    | Empirical | W_U  | W_Sp | W_SO")
    print("-" * 55)

    for i in range(0, n_bins, 10):
        x = bin_centers[i]
        emp = hist[i]
        print(f"[{bin_edges[i]:.2f},{bin_edges[i+1]:.2f}] | {emp:.3f}     | {W_unitary(x):.3f} | {W_symplectic(x):.3f} | {W_SO_even(x):.3f}")

except FileNotFoundError:
    print("\n(Zeta zeros file not found, using synthetic data)")

# =============================================================================
# PART 6: FAMILY AVERAGES AND RH
# =============================================================================

print("\n" + "=" * 75)
print("PART 6: FAMILY AVERAGES AND RH IMPLICATIONS")
print("=" * 75)

print("""
THE CENTRAL QUESTION:
Can family averages constrain individual zeros to lie on Re(s) = 1/2?

WHAT WE KNOW:

1. DENSITY THEOREMS (Proven):
   - Most zeros lie close to Re(s) = 1/2
   - Zero-free regions exist (narrow, but real)
   - 100% of zeros are on critical line (various senses)

2. FAMILY AVERAGES:
   - Average over family often easier than individual
   - Katz-Sarnak: family average matches random matrix
   - But: average properties don't prove individual properties!

3. THE GAP:
   - Family: "On average, zeros behave like RMT"
   - Individual: "Each zero has Re(ρ) = 1/2"

   These are NOT equivalent!

POTENTIAL APPROACHES:

A. MOLLIFICATION:
   - Weight zeros to emphasize central point
   - Show no zeros can escape critical line
   - Used in partial results (positive proportion on line)

B. AMPLIFICATION:
   - Construct special families that detect off-line zeros
   - Show such families can't exist

C. UNIVERSALITY:
   - If symmetry type forces statistics
   - And statistics force zero locations
   - Then RH follows

   Problem: RMT doesn't force exact locations, only statistics.
""")

# =============================================================================
# PART 7: EXPLICIT FAMILY COMPUTATIONS
# =============================================================================

print("\n" + "=" * 75)
print("PART 7: EXPLICIT FAMILY COMPUTATIONS")
print("=" * 75)

print("""
Let's explicitly compute statistics for the family of
quadratic Dirichlet L-functions L(s, χ_d) where χ_d = (d/·).

This family has SYMPLECTIC symmetry.
""")

def quadratic_char_L_value(d, s, num_terms=5000):
    """
    Compute L(s, χ_d) where χ_d is the Kronecker symbol (d/·).
    """
    result = 0.0
    for n in range(1, num_terms + 1):
        chi_n = jacobi_symbol(d, n) if n % 2 == 1 else 0
        # Extend Jacobi to Kronecker for proper handling
        if gcd(n, abs(d)) == 1:
            result += chi_n / (n ** s)
    return result

# Compute for fundamental discriminants
def is_fundamental_discriminant(d):
    """Check if d is a fundamental discriminant."""
    if d == 1:
        return False
    if d % 4 == 0:
        m = d // 4
        if m % 4 in [2, 3]:
            return False
        # Check squarefree
        for p in range(2, int(abs(m)**0.5) + 1):
            if m % (p*p) == 0:
                return False
        return True
    else:
        if d % 4 not in [1]:
            return False
        for p in range(2, int(abs(d)**0.5) + 1):
            if d % (p*p) == 0:
                return False
        return True

# Get fundamental discriminants
fund_disc = [d for d in range(-50, 51) if d != 0 and is_fundamental_discriminant(d)]
print(f"\nFundamental discriminants in [-50, 50]: {len(fund_disc)}")
print(f"Examples: {fund_disc[:10]}...")

# Compute L(1, χ_d) for class number formula
print("\nL(1, χ_d) values (related to class number):")
print("d     | L(1, χ_d) | Expected sign")
print("-" * 40)

for d in fund_disc[:12]:
    if d < -4:
        L_val = quadratic_char_L_value(d, 1.0, 3000)
        # For d < 0: L(1, χ_d) = 2πh(d)/(w√|d|) where h = class number, w = roots of unity
        print(f"{d:5d} | {L_val:+.6f} | {'positive' if d < 0 else '?'}")
    elif d > 0:
        L_val = quadratic_char_L_value(d, 1.0, 3000)
        print(f"{d:5d} | {L_val:+.6f} | {'positive' if d > 0 else '?'}")

# =============================================================================
# PART 8: THE DENSITY HYPOTHESIS
# =============================================================================

print("\n" + "=" * 75)
print("PART 8: THE DENSITY HYPOTHESIS")
print("=" * 75)

print("""
THE DENSITY HYPOTHESIS (DH):
Let N(σ, T) = #{ρ = β + iγ : β > σ, 0 < γ < T}

DH: N(σ, T) << T^{2(1-σ)+ε} for all ε > 0

IMPLICATIONS:
- DH would give almost as strong results as RH for many applications
- DH says zeros are "sparse" away from critical line
- Proven: N(σ, T) << T^{(3/2)(1-σ)+ε} (current best)

CONNECTION TO FAMILIES:
- Family averages can prove "average" density results
- But can't rule out exceptional zeros in individual functions

THE KEY LIMITATION:
Even if we prove:
  (1/|Family|) × Σ_{f ∈ Family} N_f(σ, T) << T^{small}

This doesn't prove N_f(σ, T) << T^{small} for EACH f!

An individual L-function could have many off-line zeros
while the family average is still small.
""")

# =============================================================================
# PART 9: RATIOS CONJECTURE
# =============================================================================

print("\n" + "=" * 75)
print("PART 9: RATIOS CONJECTURE")
print("=" * 75)

print("""
THE RATIOS CONJECTURE (Conrey-Farmer-Zirnbauer):

For a family F of L-functions, the ratios conjecture predicts:

  <Π L(1/2 + α_k, f) / Π L(1/2 + β_j, f)>_F

in terms of explicit arithmetic factors and random matrix terms.

WHY THIS MATTERS FOR RH:

1. If ratios conjecture is true, it constrains zero behavior
2. It connects arithmetic (L-values) to random matrices
3. The poles at β_j = zero of L encode zero statistics

PROVEN RESULTS:
- One-level density: proven for many families (support < 2)
- Two-level density: proven in some cases
- Full ratios: conjectural but matches numerics

LIMITATION FOR RH:
The ratios conjecture ASSUMES RH in its formulation!
It predicts statistics conditional on zeros being on the line.
So it can't be used to prove RH directly.
""")

# =============================================================================
# PART 10: WHAT FAMILIES CAN AND CANNOT DO
# =============================================================================

print("\n" + "=" * 75)
print("PART 10: WHAT FAMILIES CAN AND CANNOT DO")
print("=" * 75)

print("""
WHAT FAMILIES CAN DO:

1. PROVE AVERAGE RESULTS:
   - Average rank of elliptic curves
   - Average number of zeros in intervals
   - Proportion of L-functions satisfying some property

2. PROVE DENSITY RESULTS:
   - Most zeros are on critical line (density 1)
   - Zero-free regions for individual functions

3. REVEAL STRUCTURE:
   - Symmetry types explain why statistics differ
   - Arithmetic factors emerge from family averages
   - Connections to random matrices become visible

WHAT FAMILIES CANNOT DO (so far):

1. PROVE RH FOR INDIVIDUAL L-FUNCTIONS:
   - Family average ≠ individual behavior
   - Exception sets can exist even with good averages

2. RULE OUT EXCEPTIONAL ZEROS:
   - The Siegel zero problem remains open
   - A single L-function could violate RH while average is fine

3. GIVE EXACT LOCATIONS:
   - Random matrix gives statistics, not specific γ_n
   - Even with perfect symmetry type match, zeros aren't determined

THE FUNDAMENTAL BARRIER:

Family methods are PROBABILISTIC in nature.
They say "most" or "on average" but not "all" or "each".

To prove RH, we need a deterministic argument:
Either find the Hilbert-Pólya operator, or something new.
""")

# =============================================================================
# PART 11: HYBRID APPROACH IDEAS
# =============================================================================

print("\n" + "=" * 75)
print("PART 11: HYBRID APPROACH IDEAS")
print("=" * 75)

print("""
Can we COMBINE the three directions?

DIRECTION 1 (Spectral) + DIRECTION 2 (Function Field):
- The function field Frobenius IS a Hermitian operator
- Can we take a limit as characteristic → 1?
- This is essentially the F_1 approach

DIRECTION 1 (Spectral) + DIRECTION 3 (Families):
- Family symmetry type = which RMT ensemble
- If we knew WHY the ensemble, might find the operator
- The symmetry must come from some underlying Hamiltonian

DIRECTION 2 (Function Field) + DIRECTION 3 (Families):
- Families of curves over F_q give families of L-functions
- Katz proved theorems for function field families
- The Frobenius on these families has known symmetry

ALL THREE TOGETHER:
- Start with function field family (Frobenius known)
- Identify the Hermitian operator (spectral approach)
- Take "limit" to number field (F_1 or similar)
- Hope operator structure survives

BIGGEST CHALLENGE:
The limit from F_q to Z is not well-defined!
- F_q has characteristic p
- Z has characteristic 0
- There's no continuous path between them
""")

# =============================================================================
# PART 12: NUMERICAL EXPERIMENT - FAMILY AVERAGING
# =============================================================================

print("\n" + "=" * 75)
print("PART 12: NUMERICAL EXPERIMENT - FAMILY AVERAGING")
print("=" * 75)

print("""
Let's do a numerical experiment:
Compute L(1/2 + it, χ) for various t and average over characters.

If RH is true, L(1/2 + it, χ) ≠ 0 for t ≠ 0 (if χ ≠ χ_0).
""")

def L_function_on_line(t, chi, q, num_terms=2000):
    """Compute L(1/2 + it, χ) approximately."""
    s = 0.5 + 1j * t
    result = 0.0 + 0.0j

    for n in range(1, num_terms + 1):
        chi_n = chi[n % q]
        if chi_n != 0:
            result += chi_n / (n ** s)

    return result

# For q = 5, compute L(1/2 + it, χ) for various t
q = 5
chars = dirichlet_characters(q)
print(f"\nL-functions mod {q} on critical line:")
print("t     | |L(1/2+it, χ_0)| | |L(1/2+it, χ_1)|")
print("-" * 50)

for t in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 14.13]:
    L_values = []
    for chi, _, _ in chars[:2]:
        L_val = L_function_on_line(t, chi, q, 2000)
        L_values.append(abs(L_val))
    print(f"{t:5.2f} | {L_values[0]:16.6f} | {L_values[1]:16.6f}")

# Average |L|² over characters
print("\nFamily average |L(1/2+it)|² over all non-trivial χ mod q:")
print("q  | t=1      | t=5      | t=10")
print("-" * 40)

for q in [5, 7, 11, 13]:
    chars = dirichlet_characters(q)
    avgs = []
    for t in [1.0, 5.0, 10.0]:
        sum_L2 = 0.0
        count = 0
        for chi, is_prim, _ in chars:
            if is_prim:
                L_val = L_function_on_line(t, chi, q, 1000)
                sum_L2 += abs(L_val) ** 2
                count += 1
        avg = sum_L2 / count if count > 0 else 0
        avgs.append(avg)
    print(f"{q:2d} | {avgs[0]:.4f}   | {avgs[1]:.4f}   | {avgs[2]:.4f}")

# =============================================================================
# PART 13: SUMMARY
# =============================================================================

print("\n" + "=" * 75)
print("SUMMARY: DIRECTION 3 - L-FUNCTION FAMILIES")
print("=" * 75)

print("""
WHAT WE LEARNED:

1. KATZ-SARNAK PHILOSOPHY WORKS:
   - Families have symmetry types (U, Sp, SO)
   - Statistics match random matrix predictions
   - Verified in many cases

2. SYMMETRY TYPES ENCODE STRUCTURE:
   - Sp: even characters, zeros repelled from center
   - SO: odd characters, zeros attracted to center
   - The sign of functional equation determines type

3. FAMILY AVERAGES ARE COMPUTABLE:
   - One-level density proven for many families
   - Ratios conjecture makes predictions
   - Matches numerical data

4. BUT CANNOT PROVE RH:
   - Averages don't constrain individuals
   - Exceptional zeros could exist
   - Need deterministic, not probabilistic, argument

KEY INSIGHT:
Families reveal the STATISTICAL structure of zeros.
This is necessary but not sufficient for RH.

THE PATTERN:
Direction 1 (Spectral): Find operator → prove self-adjoint → RH
Direction 2 (Function Field): Has operator → but wrong setting
Direction 3 (Families): Has statistics → but can't pin down individuals

WHAT'S MISSING:
A bridge that converts:
  "Statistics are GUE" → "Each zero has Re(ρ) = 1/2"

This would require:
  - GUE statistics ONLY occur for Hermitian operators
  - The Hermitian condition IMPLIES Re(eigenvalue) = 1/2

But this isn't quite true! GUE is about unitary matrices,
and eigenvalues lie on the unit circle, not a line.

The mystery remains: why do zeta zeros follow GUE?
""")

print("=" * 75)
print("END OF L-FUNCTION FAMILIES EXPLORATION")
print("=" * 75)
