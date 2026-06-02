#!/usr/bin/env python3
"""
Can eta_local(R^3/Z2) = 4*pi/3?  -- an actual computation, not an assertion.

The repo claims each Z2 fixed point contributes eta_local = 4*pi/3 to an
Atiyah-Patodi-Singer eta-invariant, with the model spectrum lambda = +-(l+1/2)
(V11_VERIFICATION_AUDIT.md). It also states (V11 line 341) that 4*pi/3 is
"the volume of the unit 3-ball B^3."

There is NO units obstruction: eta and 4*pi/3 are both dimensionless. So the
question is purely: does the eta-invariant of this spectrum actually come out
to 4*pi/3?  We test the two halves of the claim directly.
"""
import math
try:
    import sympy as sp
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False

PI = math.pi
target = 4 * PI / 3
print("=" * 74)
print(f"TARGET claimed:  eta_local = 4*pi/3 = {target:.10f}")
print("=" * 74)

# ---------------------------------------------------------------------------
# PART A.  Where 4*pi/3 genuinely DOES come from: the Weyl / heat-kernel
#          *volume* term.  Vol(unit 3-ball) = 4*pi/3.  This is real geometry --
#          but it is the LEADING, UV-DIVERGENT term of the heat-kernel
#          expansion, the piece that gets renormalized into the bulk vacuum
#          energy.  It is NOT the eta-invariant (the finite, odd-spectral part).
# ---------------------------------------------------------------------------
def ball_volume(n):
    return PI ** (n / 2) / math.gamma(n / 2 + 1)

print("\n[A] 4*pi/3 as a Weyl/heat-kernel VOLUME coefficient:")
print(f"    Vol(unit 3-ball) = pi^(3/2)/Gamma(5/2) = {ball_volume(3):.10f}  -> = 4*pi/3  YES")
print("    In K(t) ~ Vol/(4*pi*t)^(3/2) + ...  this is the t->0 DIVERGENT term.")
print("    It carries a factor of pi and is renormalized away. It is NOT eta.")

# ---------------------------------------------------------------------------
# PART B.  What the eta-invariant of lambda = +-(l+1/2) actually is.
#          eta(s) = sum sign(lambda) |lambda|^{-s}, continued to s=0.
#          For arithmetic-progression spectra this is built from the Hurwitz
#          zeta zeta(s, a).  At s = 0, -1, -2, ... Hurwitz zeta equals
#          -B_{n+1}(a)/(n+1)  -- a RATIONAL number (Bernoulli). Never a bare pi.
# ---------------------------------------------------------------------------
print("\n[B] eta from the model spectrum lambda = +-(l+1/2), via zeta-regularization:")
print("    Building block: Hurwitz zeta(s, 1/2) at non-positive integers.")
print("    Identity: zeta(-n, a) = -B_{n+1}(a)/(n+1).\n")

if HAVE_SYMPY:
    half = sp.Rational(1, 2)
    print(f"    {'s':>4} | {'zeta(s,1/2)':>16} | {'= numeric':>14} | rational?")
    print("    " + "-" * 56)
    for s in [0, -1, -2, -3, -4, -5]:
        val = sp.zeta(s, half)          # exact Hurwitz zeta
        val = sp.nsimplify(val)
        num = float(val)
        is_rat = val.is_rational
        print(f"    {s:>4} | {str(val):>16} | {num:>14.8f} | {bool(is_rat)}")
    print("\n    Every value is a pure rational. pi never enters.")

    # A representative eta-type sum with an angular multiplicity m_l = (2l+1):
    # eta_model = sum_{l>=0} (2l+1) * sign * (l+1/2)^{-s} | continued to s=0.
    # = 2*zeta(s-1, 1/2) + ... ; evaluate the regularized value at s=0.
    s = sp.symbols('s')
    eta_model = 2 * sp.zeta(s - 1, half) + 0 * sp.zeta(s, half)  # leading mult term
    reg = sp.nsimplify(eta_model.subs(s, 0))
    print(f"\n    Model with multiplicity (2l+1):  regularized eta(0) = {reg} "
          f"= {float(reg):.8f}  (rational)")
else:
    # Pure-python Bernoulli polynomials B_{n+1}(1/2): all rational.
    from fractions import Fraction as F
    def bernoulli_numbers(m):
        A = [F(0)] * (m + 1); B = []
        for n in range(m + 1):
            A[n] = F(1, n + 1)
            for j in range(n, 0, -1):
                A[j - 1] = j * (A[j - 1] - A[j])
            B.append(A[0])
        return B
    def bernoulli_poly_at_half(n):
        # B_n(1/2) = (2^{1-n} - 1) * B_n   (classic identity)
        Bn = bernoulli_numbers(n)[n]
        return (F(2) ** (1 - n) - 1) * Bn
    print(f"    {'s':>4} | {'zeta(s,1/2)=-B_{n+1}(1/2)/(n+1)':>32} | numeric")
    print("    " + "-" * 56)
    for s in [0, -1, -2, -3, -4, -5]:
        n = -s
        z = -bernoulli_poly_at_half(n + 1) / (n + 1)
        print(f"    {s:>4} | {str(z):>32} | {float(z):>12.8f}")
    print("\n    Every value is a pure rational. pi never enters.")

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
print("\n" + "=" * 74)
print("VERDICT")
print("=" * 74)
print(f"  4*pi/3 = {target:.6f} is TRANSCENDENTAL (a rational multiple of pi).")
print("  The eta-invariant of lambda=+-(l+1/2) via the claimed zeta method is")
print("  a RATIONAL number (Hurwitz-zeta/Bernoulli values at s<=0). A rational")
print("  cannot equal a nonzero rational multiple of pi. So eta_local != 4*pi/3,")
print("  for ANY choice of multiplicities, by the *type* of number produced.")
print()
print("  4*pi/3 is real -- it's Vol(B^3), the DIVERGENT Weyl/volume term -- but")
print("  that is a different term in the heat-kernel expansion than the finite")
print("  eta. Identifying the two is the error. (The repo's own")
print("  NEW_MATH_DIRECTIONS.md concedes: the finite piece is an Epstein-zeta")
print("  number, NOT 4*pi/3.)")
print("=" * 74)
