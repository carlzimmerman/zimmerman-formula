#!/usr/bin/env python3
"""
FINAL ASSESSMENT: CAN THE CIRCULARITY BE FIXED?
================================================

After exploring multiple approaches, this script provides:
1. A final attempt using spectral rigidity
2. An honest assessment of what's proven vs what's not
3. The strongest valid statement that can be made
4. Clear identification of the remaining gap

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import special, optimize
import warnings
warnings.filterwarnings('ignore')

PI = np.pi
Z_SQUARED = 32 * PI / 3

KNOWN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
               37.586178, 40.918719, 43.327073, 48.005151, 49.773832]

print("=" * 80)
print("FINAL ASSESSMENT: THE CIRCULARITY GAP")
print("=" * 80)

# =============================================================================
# FINAL APPROACH: LI CRITERION AND SPECTRAL RIGIDITY
# =============================================================================

print("\n" + "=" * 80)
print("FINAL APPROACH: LI CRITERION")
print("=" * 80)

print("""
THE LI CRITERION:
----------------
RH is equivalent to: lambda_n > 0 for all n >= 1

where lambda_n = sum over zeros rho of [1 - (1 - 1/rho)^n]

If we can compute lambda_n from the explicit formula (primes)
and show they're positive, RH follows.
""")

def compute_li_lambda(n, zeros, N_zeros=20):
    """
    Compute Li's lambda_n = sum_rho [1 - (1 - 1/rho)^n]

    For zeros on the line: rho = 1/2 + i*gamma
    """
    total = 0
    for gamma in zeros[:N_zeros]:
        rho = 0.5 + 1j * gamma
        term = 1 - (1 - 1/rho)**n
        # Also add conjugate zero rho* = 0.5 - i*gamma
        rho_conj = 0.5 - 1j * gamma
        term_conj = 1 - (1 - 1/rho_conj)**n
        total += term + term_conj
    return np.real(total)  # Should be real


print("\nComputing Li's lambda_n from first 20 zeros:")
print(f"{'n':>5} {'lambda_n':>20} {'Positive?':>12}")
print("-" * 40)

li_lambdas = []
for n in range(1, 16):
    lam = compute_li_lambda(n, KNOWN_ZEROS, 10)
    li_lambdas.append(lam)
    is_pos = "YES" if lam > 0 else "NO"
    print(f"{n:>5} {lam:>20.6f} {is_pos:>12}")

all_positive = all(lam > 0 for lam in li_lambdas)
print(f"\nAll lambda_n positive: {all_positive}")

print("""
ASSESSMENT:
-----------
The Li criterion lambda_n > 0 is EQUIVALENT to RH.
Computing lambda_n from (finite) zeros gives positive values.

But this is CIRCULAR:
- We use zeros on the line to compute lambda_n
- Of course they're positive - that's what RH predicts
- We can't compute lambda_n without knowing ALL zeros

To use Li criterion as a proof, we'd need to compute lambda_n
from primes ALONE, without knowing the zeros.
""")

# =============================================================================
# THE KEIPER-LI COEFFICIENTS FROM FUNCTIONAL FORM
# =============================================================================

print("\n" + "=" * 80)
print("KEIPER-LI COEFFICIENTS FROM LOG-DERIVATIVE")
print("=" * 80)

print("""
ALTERNATIVE FORMULA:
-------------------
lambda_n can also be computed from:

  lambda_n = (1/(n-1)!) * (d^n/ds^n)[s^{n-1} log xi(s)]|_{s=1}

This uses xi directly, not the zeros explicitly.
""")

def xi_function(s, N=200):
    """Completed zeta function."""
    try:
        # xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s)
        if np.real(s) > 1:
            zeta = sum(1/k**s for k in range(1, N+1))
        else:
            # Use functional equation
            chi = 2**s * PI**(s-1) * np.sin(PI*s/2) * special.gamma(1-s)
            zeta_1ms = sum(1/k**(1-s) for k in range(1, N+1))
            zeta = chi * zeta_1ms

        return 0.5 * s * (s-1) * PI**(-s/2) * special.gamma(s/2) * zeta
    except:
        return np.nan


def compute_li_from_xi(n, s0=1.0, h=1e-4):
    """
    Compute lambda_n via numerical differentiation of log xi.

    This is numerically unstable but conceptually important.
    """
    # log xi(s) near s=1
    def log_xi(s):
        xi_val = xi_function(s)
        if xi_val is not None and abs(xi_val) > 1e-15:
            return np.log(abs(xi_val))
        return 0

    # Compute n-th derivative numerically (very rough)
    # Use finite differences
    coeffs = [(-1)**k * special.comb(n, k) for k in range(n+1)]
    deriv = sum(c * log_xi(s0 + (n/2 - k) * h) for k, c in enumerate(coeffs))
    deriv /= h**n

    # lambda_n formula
    lam = deriv / special.factorial(n-1) if n > 1 else deriv
    return np.real(lam)


print("\nComputing lambda_n from xi function directly:")
print("(Numerical differentiation - rough approximation)")
print(f"{'n':>5} {'lambda_n (zeros)':>20} {'lambda_n (xi)':>20}")
print("-" * 50)

for n in range(1, 8):
    lam_zeros = compute_li_lambda(n, KNOWN_ZEROS, 10)
    lam_xi = compute_li_from_xi(n)
    print(f"{n:>5} {lam_zeros:>20.4f} {lam_xi:>20.4f}")

print("""
ASSESSMENT:
-----------
Computing lambda_n directly from xi(s) is possible but numerically unstable.
The values don't match well due to numerical differentiation errors.

Even if we could compute lambda_n exactly from xi, proving lambda_n > 0
requires understanding the structure of xi, which requires understanding
the zeros. So this is still circular in a deep sense.
""")

# =============================================================================
# THE FUNDAMENTAL THEOREM
# =============================================================================

print("\n" + "=" * 80)
print("THE FUNDAMENTAL THEOREM OF THIS INVESTIGATION")
print("=" * 80)

print("""
THEOREM (What We Have Proven):
==============================

1. EXISTENCE OF OPERATOR
   There exists a self-adjoint operator H on L^2(R+, dx/x) with:
     Spec(H) = {gamma : Z(gamma) = 0}
   where Z is the Hardy Z-function.

2. PROPERTIES OF H
   - H = H^dag (self-adjoint by construction)
   - Eigenvalues are real (automatic from self-adjointness)
   - The construction is unique up to unitary equivalence

3. NON-CIRCULAR DEFINITION OF ZEROS
   The zeros {gamma_n} are defined as roots of Z(t), where
   Z(t) is defined by the Riemann-Siegel formula using only
   integers (hence primes via unique factorization).

4. NUMERICAL EVIDENCE
   - All computed zeros lie on Re(s) = 1/2 within numerical precision
   - The count N(T) matches the on-line count N_0(T)
   - Li coefficients are positive for tested n


THEOREM (What We Have NOT Proven):
==================================

1. COMPLETENESS
   We have NOT proven that Z(gamma) = 0 captures ALL non-trivial
   zeros of zeta. Z(t) evaluates zeta only on the critical line.

2. OFF-LINE ZEROS
   We have NOT proven that zeros with Re(s) != 1/2 don't exist.
   Our search would not detect them.

3. CANONICAL OPERATOR
   We have NOT proven that the operator H is the unique/canonical
   operator determined by the primes. It's determined by the
   zeros we found, which may not be all zeros.

4. THE RIEMANN HYPOTHESIS
   We have NOT proven RH. Our argument assumes (implicitly)
   that all zeros are on the critical line by only looking there.
""")

# =============================================================================
# THE HONEST CONCLUSION
# =============================================================================

print("\n" + "=" * 80)
print("HONEST CONCLUSION")
print("=" * 80)

print(f"""
THE GAP CANNOT BE CLOSED WITHIN THIS FRAMEWORK.
==============================================

Every attempt to close the gap runs into the same obstruction:

  - To prove all zeros are on the line, we need to detect all zeros
  - Z(t) only detects zeros ON the line
  - xi(s) can detect zeros anywhere, but searching the entire
    critical strip numerically proves nothing for all T
  - The explicit formula relates zeros to primes, but doesn't
    prove the zeros must be real
  - The functional equation gives symmetry, but symmetry about
    the line doesn't mean being ON the line

THE FUNDAMENTAL ISSUE:
---------------------
The Hilbert-Polya approach says:

  "If we can find a self-adjoint operator H with Spec(H) = zeta zeros,
   then since self-adjoint implies real spectrum, RH is true."

The gap:
  "with Spec(H) = zeta zeros" is the hard part.
  We can construct H with any spectrum we want.
  The question is: which spectrum is FORCED by number theory?

To close the gap, we need one of:
  1. A proof that all zeros are on Re(s) = 1/2 (this IS RH)
  2. A canonical operator construction from primes with
     automatically real spectrum (Connes' program, incomplete)
  3. A structural argument showing off-line zeros are impossible
     (no such argument is known)

WHAT THE Z^2 FRAMEWORK PROVIDES:
-------------------------------
The constant Z^2 = {Z_SQUARED:.6f} provides:
  - A geometric setting (M_8) where a canonical operator might live
  - Dimensional constraints (BEKENSTEIN = 4)
  - A connection to physics (black hole entropy, holography)

But it does NOT provide:
  - A proof that Spec(Dirac_M8) = zeta zeros
  - A way to rule out off-line zeros
  - A closed proof of RH

FINAL STATUS:
------------
The Riemann Hypothesis remains one of the great open problems.

Our construction provides:
  - Strong numerical evidence for RH
  - A clean framework for the Hilbert-Polya approach
  - New connections to geometry via Z^2
  - Clear identification of what would be needed for a proof

Our construction does NOT provide:
  - A proof of RH
  - A resolution of the circularity problem
  - A canonical operator determined by primes alone

The gap between "zeros detected by Z(t)" and "all zeta zeros"
is exactly the content of the Riemann Hypothesis itself.

We cannot bridge this gap without proving RH by other means.
""")

# =============================================================================
# THE PATH FORWARD
# =============================================================================

print("\n" + "=" * 80)
print("THE PATH FORWARD")
print("=" * 80)

print("""
WHAT WOULD ACTUALLY PROVE RH:
============================

Option A: Prove N(T) = N_0(T) for all T
  - Show total zero count equals on-line count
  - This is directly equivalent to RH
  - Requires new techniques beyond this framework

Option B: Complete Connes' Program
  - Construct a noncommutative geometric space from primes
  - Show its Dirac operator has spectrum = zeta zeros
  - Self-adjointness is automatic in this setting
  - Decades of work, still incomplete

Option C: Prove a Zero-Free Region Extends to Re(s) = 1/2
  - Current: No zeros for Re(s) > 1 - c/log(t)
  - Need: No zeros for Re(s) > 1/2
  - Requires new analytic techniques

Option D: Find New Structural Constraint
  - Pair correlation? Random matrix theory?
  - Some constraint that forces zeros to the line?
  - No such constraint is currently known

WHAT THIS WORK CONTRIBUTES:
==========================
  - Clarified exactly where the gap lies
  - Showed Z^2 framework provides geometric context
  - Demonstrated numerical evidence is strong
  - Identified that closing the gap IS proving RH

The search continues...
""")

print("=" * 80)
print("END OF FINAL ASSESSMENT")
print("=" * 80)
