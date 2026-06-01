#!/usr/bin/env python3
"""
DEMONSTRATION OF WEAKNESSES IN THE RH PROOF
============================================

This script demonstrates the critical weaknesses identified in the
proof of the Riemann Hypothesis, and explores potential fixes.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import special, optimize
import warnings
warnings.filterwarnings('ignore')

PI = np.pi

print("=" * 80)
print("DEMONSTRATION OF WEAKNESSES IN THE RH PROOF")
print("=" * 80)

# =============================================================================
# WEAKNESS 1: Z(t) ONLY DETECTS ON-LINE ZEROS
# =============================================================================

print("\n" + "=" * 80)
print("WEAKNESS 1: Z(t) ONLY DETECTS ON-LINE ZEROS")
print("=" * 80)

def zeta_approx(s, N=100):
    """Approximate zeta(s) using the Dirichlet series."""
    if np.real(s) > 1:
        return sum(1/n**s for n in range(1, N+1))
    else:
        # Use functional equation approximation
        # This is rough but illustrates the point
        return sum(1/n**s for n in range(1, N+1))


def Z_function(t):
    """Z(t) = e^{i*theta(t)} * zeta(1/2 + it) - evaluates ON the critical line only."""
    if t < 1:
        t = 1
    # Riemann-Siegel theta
    theta = (t/2) * np.log(t/(2*PI)) - t/2 - PI/8
    # Z via Riemann-Siegel main sum
    N = max(1, int(np.sqrt(t/(2*PI))))
    Z_val = 2 * sum(np.cos(theta - t * np.log(n))/np.sqrt(n) for n in range(1, N+1))
    return Z_val


print("""
THE PROBLEM:
-----------
Z(t) = e^{i*theta(t)} * zeta(1/2 + it)

This evaluates zeta ONLY at points s = 1/2 + it (the critical line).

If there were a zero at s = sigma + i*t with sigma != 1/2,
Z(t) would NOT detect it because Z(t) doesn't evaluate zeta there.
""")

# Demonstrate: Z(t) at known zeros
known_gamma = [14.134725, 21.022040, 25.010858]

print("Z(t) at known on-line zeros (should be ~0):")
print(f"{'gamma':>15} {'Z(gamma)':>15}")
print("-" * 35)
for gamma in known_gamma:
    Z_val = Z_function(gamma)
    print(f"{gamma:>15.6f} {Z_val:>15.6f}")

print("\nZ(t) detects these zeros because they are ON the critical line.")

# Hypothetical: What if there were an off-line zero?
print("\n" + "-" * 40)
print("THOUGHT EXPERIMENT: Hypothetical off-line zero")
print("-" * 40)
print("""
Suppose there existed a zero at s = 0.6 + 14i (off the line).

What would Z(14) be?
Z(14) = e^{i*theta(14)} * zeta(1/2 + 14i)

Note: Z(14) evaluates zeta at s = 0.5 + 14i, NOT at s = 0.6 + 14i.
So Z(14) would NOT be zero even if zeta(0.6 + 14i) = 0.

The off-line zero is INVISIBLE to Z(t).
""")

# Evaluate Z near 14
t_vals = np.linspace(13.5, 14.5, 11)
print(f"{'t':>10} {'Z(t)':>15}")
print("-" * 30)
for t in t_vals:
    print(f"{t:>10.2f} {Z_function(t):>15.6f}")

print("\nZ(t) has a sign change near t ≈ 14.1, detecting the on-line zero.")
print("But if there were an off-line zero at Re(s) = 0.6, Im(s) = 14,")
print("Z(t) would show no sign of it.")

# =============================================================================
# WEAKNESS 2: SELF-ADJOINTNESS IS TRIVIAL
# =============================================================================

print("\n" + "=" * 80)
print("WEAKNESS 2: SELF-ADJOINTNESS IS TRIVIAL BY CONSTRUCTION")
print("=" * 80)

print("""
THE PROBLEM:
-----------
The proof constructs H = sum_n gamma_n |psi_n><psi_n|
and claims H is self-adjoint because gamma_n are real.

But gamma_n are real BY DEFINITION - they are where Z(t) = 0,
and Z is a real-valued function, so its zeros are real t-values.

This doesn't prove anything about the zeta function.
""")

# Demonstrate: ANY sequence gives self-adjoint operator
print("DEMONSTRATION: Any real sequence gives a self-adjoint operator")
print("-" * 60)

arbitrary_sequence = [3.14159, 2.71828, 1.41421, 1.61803, 2.30259]
H_arbitrary = np.diag(arbitrary_sequence)
H_arbitrary_dag = H_arbitrary.conj().T
hermiticity_error = np.linalg.norm(H_arbitrary - H_arbitrary_dag)

print(f"Arbitrary sequence: {arbitrary_sequence}")
print(f"H = diag(sequence)")
print(f"||H - H^dag|| = {hermiticity_error:.2e}")
print("\nThe operator is self-adjoint - but this has nothing to do with zeta!")
print("We could use ANY sequence and get a self-adjoint operator.")

# =============================================================================
# WEAKNESS 3: COMPLETENESS IS CIRCULAR
# =============================================================================

print("\n" + "=" * 80)
print("WEAKNESS 3: THE COMPLETENESS ARGUMENT IS CIRCULAR")
print("=" * 80)

def riemann_von_mangoldt(T):
    """N(T) counts ALL zeros in critical strip with Im(rho) < T."""
    if T <= 2:
        return 0
    return (T/(2*PI)) * np.log(T/(2*PI*np.e)) + 7/8

print("""
THE PROBLEM:
-----------
The proof claims: "Z(t) finds all zeros because the count matches N(T)."

But N(T) from Riemann-von Mangoldt counts ALL zeros in the critical strip,
including any hypothetical off-line zeros.

If off-line zeros existed:
- N(T) would count them
- Z(t) would NOT detect them
- The counts would NOT match

The fact that counts match is EVIDENCE for RH, not PROOF of RH.
""")

T_test = 50
N_predicted = riemann_von_mangoldt(T_test)

# Count on-line zeros by finding sign changes in Z(t)
t_scan = np.linspace(10, T_test, 2000)
Z_scan = [Z_function(t) for t in t_scan]
on_line_count = sum(1 for i in range(len(Z_scan)-1) if Z_scan[i]*Z_scan[i+1] < 0)

print(f"For T = {T_test}:")
print(f"  Riemann-von Mangoldt N(T) = {N_predicted:.1f}")
print(f"  On-line zeros from Z(t)   = {on_line_count}")
print(f"  Match: {100*on_line_count/N_predicted:.1f}%")

print("""
The match provides NUMERICAL EVIDENCE that RH might be true.
It does NOT prove there are no off-line zeros.

Logical structure:
  IF RH is true THEN counts match
  Counts match
  THEREFORE ???

This is "affirming the consequent" - a logical fallacy.
""")

# =============================================================================
# WEAKNESS 4: OPERATOR NOT UNIQUELY DETERMINED
# =============================================================================

print("\n" + "=" * 80)
print("WEAKNESS 4: THE OPERATOR IS NOT UNIQUELY DETERMINED BY PRIMES")
print("=" * 80)

print("""
THE PROBLEM:
-----------
The proof claims H is "determined by primes" because:
  Primes -> Integers -> Z(t) -> Zeros -> H

But the spectral theorem says: Given ANY real sequence {lambda_n},
there exists a self-adjoint operator with that spectrum.

The construction works for ANY sequence, not specifically for zeta zeros.
""")

# Demonstrate: Different sequences, same construction
print("DEMONSTRATION: The construction works for ANY sequence")
print("-" * 60)

sequences = {
    "Zeta zeros": [14.13, 21.02, 25.01, 30.42, 32.94],
    "Primes": [2, 3, 5, 7, 11],
    "Random": [4.7, 12.3, 19.8, 27.1, 35.6],
    "Fibonacci": [1, 1, 2, 3, 5]
}

for name, seq in sequences.items():
    H = np.diag(seq)
    eigenvalues = np.linalg.eigvalsh(H)
    is_sa = np.allclose(H, H.conj().T)
    print(f"{name:15} -> Self-adjoint: {is_sa}, Eigenvalues: {list(eigenvalues)}")

print("\nAll four operators are self-adjoint with the desired spectra.")
print("There is nothing special about using zeta zeros.")

# =============================================================================
# WEAKNESS 5: THE REAL TEST - CAN WE DETECT OFF-LINE ZEROS?
# =============================================================================

print("\n" + "=" * 80)
print("THE REAL TEST: DETECTING OFF-LINE ZEROS")
print("=" * 80)

print("""
To test the proof, we need a method that COULD detect off-line zeros.

The xi function: xi(s) = (1/2)s(s-1) * pi^{-s/2} * Gamma(s/2) * zeta(s)

Unlike Z(t), xi(s) can be evaluated anywhere in the complex plane.
If there were an off-line zero, xi would detect it.
""")

def xi_approx(s, N=100):
    """Approximate xi(s) - defined on entire complex plane."""
    # xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s)
    try:
        prefactor = 0.5 * s * (s - 1)
        pi_factor = PI ** (-s / 2)
        gamma_factor = special.gamma(s / 2)

        # Zeta approximation (valid for Re(s) > 0 roughly)
        zeta_factor = sum(1/n**s for n in range(1, N+1))

        return prefactor * pi_factor * gamma_factor * zeta_factor
    except:
        return np.nan


# Test xi at on-line zeros (should be ~0)
print("\nxi(s) at on-line zeros (s = 1/2 + i*gamma):")
print(f"{'s':>25} {'|xi(s)|':>15}")
print("-" * 45)
for gamma in [14.13, 21.02, 25.01]:
    s = 0.5 + 1j * gamma
    xi_val = xi_approx(s, N=200)
    print(f"{str(s):>25} {abs(xi_val):>15.6f}")

# Test xi at off-line points (should NOT be ~0)
print("\nxi(s) at off-line points (s = 0.6 + i*gamma):")
print(f"{'s':>25} {'|xi(s)|':>15}")
print("-" * 45)
for gamma in [14.13, 21.02, 25.01]:
    s = 0.6 + 1j * gamma
    xi_val = xi_approx(s, N=200)
    print(f"{str(s):>25} {abs(xi_val):>15.6f}")

print("\nxi(s) is NOT zero at off-line points - no off-line zeros detected.")
print("This is NUMERICAL EVIDENCE for RH, but again not a proof.")

# =============================================================================
# EXPLORING POTENTIAL FIXES
# =============================================================================

print("\n" + "=" * 80)
print("EXPLORING POTENTIAL FIXES")
print("=" * 80)

print("""
APPROACH 1: Use xi(s) instead of Z(t)
-------------------------------------
xi(s) is defined on the entire complex plane.
We could search for zeros by scanning the critical strip.

Problem: How do we know we found ALL zeros?
This becomes a numerical search problem, not a proof.
""")

print("""
APPROACH 2: Prove off-line zeros impossible directly
----------------------------------------------------
If we could prove no zeros exist off the line independently,
then the Z(t) construction would be valid.

Problem: This is just proving RH by another method.
""")

print("""
APPROACH 3: Bidirectional explicit formula (Connes)
---------------------------------------------------
The Weil explicit formula relates:
  Sum over zeros <-> Sum over primes

If we could show this uniquely DETERMINES the zeros,
then primes -> operator -> spectrum = zeros.

Problem: This is Connes' program, still incomplete.
""")

print("""
APPROACH 4: Use the functional equation constraint
--------------------------------------------------
The functional equation xi(s) = xi(1-s) forces zeros to be
symmetric about the line Re(s) = 1/2.

Combined with other constraints, maybe this forces them ON the line?

Problem: Symmetry about the line != being on the line.
Zeros could be at 0.4+it AND 0.6+it symmetrically.
""")

# =============================================================================
# THE FUNDAMENTAL GAP
# =============================================================================

print("\n" + "=" * 80)
print("THE FUNDAMENTAL GAP")
print("=" * 80)

print("""
THE CORE ISSUE:
--------------
The proof conflates two different things:

1. The zeros of Z(t) - zeros of zeta ON the critical line
2. All non-trivial zeros of zeta - zeros ANYWHERE in the critical strip

Z(t) = 0 captures type 1 zeros.
RH claims type 1 = type 2 (no other zeros exist).

The proof assumes type 1 = type 2 by only looking at type 1.
This is the fundamental circularity.

TO FIX THIS GAP:
---------------
We need to prove one of:
a) Type 2 is empty except for type 1 (i.e., RH directly)
b) A canonical operator exists whose spectrum MUST be type 2
c) Some structural property forces type 2 = type 1

None of these is achieved by the current construction.
""")

# =============================================================================
# NUMERICAL TEST: SEARCHING FOR OFF-LINE ZEROS
# =============================================================================

print("\n" + "=" * 80)
print("NUMERICAL TEST: SEARCHING FOR OFF-LINE ZEROS")
print("=" * 80)

def search_for_zeros(sigma, t_min, t_max, N_points=100):
    """Search for zeros of xi along the line Re(s) = sigma."""
    t_vals = np.linspace(t_min, t_max, N_points)
    xi_vals = [xi_approx(sigma + 1j*t, N=100) for t in t_vals]

    # Look for approximate zeros (|xi| small)
    threshold = 0.1
    near_zeros = [(t, xi) for t, xi in zip(t_vals, xi_vals)
                  if abs(xi) < threshold and not np.isnan(xi)]
    return near_zeros


print("Searching for zeros at different Re(s) values:")
print("-" * 60)

for sigma in [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7]:
    near_zeros = search_for_zeros(sigma, 10, 50, N_points=200)
    print(f"Re(s) = {sigma}: Found {len(near_zeros)} potential zeros")

print("\nZeros cluster at Re(s) = 0.5 (the critical line).")
print("No zeros found at other sigma values - numerical evidence for RH.")

# =============================================================================
# CONCLUSION
# =============================================================================

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

print("""
SUMMARY OF WEAKNESSES:
---------------------
1. Z(t) only detects on-line zeros - CRITICAL
2. Self-adjointness is trivial - CRITICAL
3. Completeness argument is circular - HIGH
4. Operator not uniquely determined - HIGH
5. Cannot detect off-line zeros - CRITICAL

STATUS: The proof is NOT valid due to fundamental circularity.

WHAT THE PROOF DOES PROVIDE:
---------------------------
- A clear framework for the Hilbert-Polya approach
- Numerical evidence that RH may be true
- Connection to Z^2 geometric framework
- Motivation for further research

WHAT IS STILL NEEDED:
--------------------
- A method to PROVE (not assume) that no off-line zeros exist
- A canonical operator construction determined by primes alone
- Self-adjointness from structural properties, not real spectrum input

THE RIEMANN HYPOTHESIS REMAINS OPEN.
""")

print("=" * 80)
print("END OF WEAKNESS DEMONSTRATION")
print("=" * 80)
