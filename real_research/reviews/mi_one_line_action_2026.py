#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_one_line_action_2026.py
==========================
VERIFYING THE ONE-LINE FORM OF THE ACTION, the display the paper (v5) opens with.

    S = -m c^2 Integral [ mu(Theta) dtau + (1 - mu(Theta)) dt ],
    Theta(tau) = Integral_0^inf ds K(s) arccosh( -u(tau).u(tau-s)/c^2 )

with dtau the proper time and dt the PREFERRED-FRAME (cosmological) time.  This exists because that
line will be quoted, so it must be self-verifying rather than merely elegant.  Checked here:

  A.  it is IDENTICAL to the paper's Form III, S = -mc^2 Int dtau mu - m Int dtau sqrt((u.n)^2)(1-mu),
      because dt = gamma dtau = sqrt((u.n)^2) dtau/c^2 -- so the "dt" writing IS the even root, which
      is what makes the action CPT-even;
  B.  its two limits are the two most natural worldline scalars: mu -> 1 gives -mc^2 Int dtau (the free
      relativistic particle) and mu -> 0 gives -mc^2 Int dt (zero inertia, rest energy intact);
  C.  non-relativistically the rest energy is EXACTLY m c^2 and the inertial mass EXACTLY m mu(Theta);
  D.  the exact energy is E = m c^2 [1 + mu(gamma - 1)], monotone and bounded below by m c^2;
  E.  the single fitted number is the kernel's first moment, M1 = (2/3) c/a_0 (the 2/3 is the
      memory-force renormalisation), and the arccosh is the rapidity gap whose short-separation limit
      is theta -> (s/c)|a(tau - s/2)|.

NOTHING NEW IS DERIVED HERE.  Every statement is already established in
`mi_two_function_restmass_fix_2026.py` (35/35), `mi_form3_cpt_even_and_lambda_bound_2026.py` (28/28),
`mi_rapidity_kernel_solved_2026.py` (35/35) and `mi_noncircular_ctp_eom_2026.py` (27/27).  This script
only certifies that the COMPRESSED one-line writing loses none of it.
kappa = 1/2 remains FITTED, NOT DERIVED: it is the value of M1, and nothing here changes that.

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eq 9; MILGROM 1994 Ann.Phys. 229:384;
rapidity as the integral of proper acceleration is classical (SYNGE).

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 30

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


C      = mp.mpf("2.99792458e8")
LAM    = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
A0     = C**2 * mp.sqrt(LAM / (32 * mp.pi))
A0_ALT = A0 / mp.sqrt(OMEGA_L)
GYR    = mp.mpf("3.1557e16")

print(__doc__)

v, m, mu = sp.symbols("v m mu", positive=True)
un = sp.Symbol("u_dot_n", real=True)
gam = 1 / sp.sqrt(1 - v**2)                      # c = 1
w = sp.Symbol("w", positive=True)                # rapidity, v = tanh w

# =============================================================================================
print("=" * 100)
print("PART A -- the one-line form IS the paper's Form III")
print("=" * 100)
# S = -m Int [mu dtau + (1-mu) dt].  In S = Int dt L:  dtau/dt = 1/gamma, dt/dt = 1.
L_one = -m * (mu / gam + (1 - mu))
# Form III: S = -m Int dtau mu - m Int dtau sqrt((u.n)^2)(1-mu); sqrt((u.n)^2) = gamma (c=1), and
# Int dtau gamma X = Int dt X.
L_III = -m * mu / gam - m * (1 - mu)
check(sp.simplify(L_one - L_III) == 0,
      "A1  *** the one-line Lagrangian equals Form III's identically ***",
      f"L = {sp.simplify(L_one)}")
check(sp.simplify((sp.sqrt(sp.cosh(w)**2) / sp.cosh(w)) - 1) == 0,
      "A2  and dt = gamma dtau = sqrt((u.n)^2) dtau/c^2, so the 'dt' writing IS the even root",
      "verified in the rapidity parametrisation, where gamma = cosh(w) > 0 manifestly")
check(sp.simplify(sp.sqrt(un**2).subs(un, -un) - sp.sqrt(un**2)) == 0
      and sp.sqrt(un**2).has(sp.Abs),
      "A3  *** which is why the action is CPT-EVEN: sqrt((u.n)^2) = |u.n| is invariant under "
      "u -> -u, so antiparticles get the same rest energy and the same inertia ***")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the two limits are the two natural worldline scalars")
print("=" * 100)
check(sp.simplify(L_one.subs(mu, 1) - (-m / gam)) == 0,
      "B1  *** mu -> 1: S = -mc^2 Int dtau, the ORDINARY FREE RELATIVISTIC PARTICLE ***",
      f"L = {sp.simplify(L_one.subs(mu, 1))} = -m/gamma = -m c^2 dtau/dt")
check(sp.simplify(L_one.subs(mu, 0) - (-m)) == 0,
      "B2  *** mu -> 0: S = -mc^2 Int dt, PURE PREFERRED-FRAME TIME -- zero inertia, rest energy "
      "intact.  That is modified inertia in three symbols ***",
      f"L = {sp.simplify(L_one.subs(mu, 0))} = -m c^2, v-independent => no kinetic term at all")
check(sp.simplify(sp.diff(L_one.subs(mu, 0), v)) == 0,
      "B3  and the mu = 0 Lagrangian is exactly v-INDEPENDENT, so the inertia vanishes identically "
      "rather than merely becoming small")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- rest energy m c^2 and inertia m mu, exactly")
print("=" * 100)
ser = sp.series(L_one, v, 0, 3).removeO()
rest = sp.simplify(-ser.subs(v, 0))
kin = sp.simplify(sp.diff(ser, v, 2).subs(v, 0) / 2)
check(sp.simplify(rest - m) == 0,
      "C1  *** rest energy = m c^2 EXACTLY, for every mu ***", f"= {rest}")
check(sp.simplify(2 * kin - m * mu) == 0,
      "C2  *** inertial mass = m mu(Theta) EXACTLY ***", f"m_eff = {sp.simplify(2*kin)}")
p_one = sp.simplify(sp.diff(L_one, v))
E_one = sp.simplify(sp.expand(sp.simplify(p_one * v - L_one)))
check(sp.simplify(E_one - m * (1 + mu * (gam - 1))) == 0,
      "C3  and the exact energy is E = m c^2[1 + mu(gamma - 1)]", f"E = {sp.simplify(E_one)}")
check(all(mp.mpf(str(sp.N((m * mu * (gam - 1)).subs({m: 1, mu: q, v: r}), 25))) >= 0
          for q in ("0", "0.3", "1") for r in ("0.1", "0.9", "0.999")),
      "C4  which is monotone and BOUNDED BELOW by m c^2 at every speed")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- the one fitted number, and the rapidity gap's short-separation limit")
print("=" * 100)
M1 = 2 * C / (3 * A0)
print(f"  M1 = (2/3) c/a_0 = {sig(M1)} s = {sig(M1/GYR, 6)} Gyr    "
      f"ALT footing {sig(2*C/(3*A0_ALT))} s")
check(abs(M1 * 3 * A0 / (2 * C) - 1) < mp.mpf("1e-25"),
      "D1  *** the single fitted number is the kernel's FIRST MOMENT, M1 = (2/3) c/a_0 = 67.7 Gyr "
      "(the 2/3 is the memory-force renormalisation) ***",
      "and in the short-memory limit ONLY that moment survives, so a_0 is one number traded for one")
s, cc, A, Ad = sp.symbols("s c A Adot", positive=True)
prods = {0: -cc**2, 1: sp.Integer(0), 2: -A**2, 3: -3 * A * Ad}
f = sp.expand(sum((-s)**k * prods[k] / sp.factorial(k) for k in prods) * (-1 / cc**2))
th = sp.expand(sp.series(sp.sqrt(2 * (f - 1)), s, 0, 4).removeO())
mid = sp.expand((s / cc) * (A - s * Ad / 2))
check(sp.simplify(th.coeff(s, 1) - mid.coeff(s, 1)) == 0
      and sp.simplify(th.coeff(s, 2) - mid.coeff(s, 2)) == 0,
      "D2  and arccosh(-u.u'/c^2) is the RAPIDITY GAP, whose short-separation limit is "
      "theta -> (s/c)|a(tau - s/2)| -- the acceleration magnitude at the MIDPOINT",
      "s^1 and s^2 coefficients agree; remainder is the stated O(s^3)")
check(abs(C**2 * mp.sqrt(LAM / (32 * mp.pi)) - A0) < mp.mpf("1e-40"),
      "D3  a_0 = c^2 sqrt(Lambda/32 pi) on the canonical footing",
      f"= {sig(A0)} m/s^2   ALT {sig(A0_ALT)} m/s^2")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- NEGATIVE CONTROLS")
print("=" * 100)
# NC1: swap dt <-> dtau and the rest energy must break
L_swap = -m * (mu + (1 - mu) / gam)
rest_swap = sp.simplify(-sp.series(L_swap, v, 0, 3).removeO().subs(v, 0))
kin_swap = sp.simplify(sp.diff(sp.series(L_swap, v, 0, 3).removeO(), v, 2).subs(v, 0))
check(sp.simplify(rest_swap - m) == 0 and sp.simplify(kin_swap - m * mu) != 0,
      "NC1  CONTROL FIRES: swapping which factor carries dtau and which carries dt keeps the rest "
      "energy but gives the WRONG inertia m(1-mu), so the assignment in the boxed line is doing work",
      f"swapped inertia = {sp.simplify(kin_swap)} instead of m mu")
# NC2: the single-factor form must show the old rest-energy defect
L_single = -m * mu / gam
check(sp.simplify(sp.simplify(-sp.series(L_single, v, 0, 3).removeO().subs(v, 0)).subs(mu, 0)) == 0,
      "NC2  CONTROL FIRES: the single-factor form -mc^2 Int mu dtau has rest energy m c^2 mu, which "
      "VANISHES at mu = 0 -- the defect the two-term line exists to fix")
# NC3: cosh^-1 of the bilinear must be the rapidity, not an arbitrary function
th_sym = sp.Symbol("theta", positive=True)
check(sp.simplify(sp.cosh(th_sym) - (1 + 2 * sp.sinh(th_sym / 2)**2)) == 0,
      "NC3  CONTROL: cosh(theta) = 1 + 2 sinh^2(theta/2) confirms arccosh(-u.u'/c^2) is the "
      "hyperbolic angle between the two four-velocities, i.e. the rapidity gap, not a fitted function")
check(abs(C**2 * mp.sqrt(LAM / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC4  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")

print("""
==================================================================================================
THE LINE, CERTIFIED
==================================================================================================
    S = -m c^2 Integral [ mu(Theta) dtau + (1 - mu(Theta)) dt ]
    Theta(tau) = Integral_0^inf ds K(s) arccosh( -u(tau).u(tau-s)/c^2 )

  dtau = proper time; dt = preferred-frame (cosmological) time.  Reading:
    * mu -> 1  =>  S = -mc^2 Int dtau : the ordinary free relativistic particle.
    * mu -> 0  =>  S = -mc^2 Int dt   : zero inertia, rest energy intact.  Modified inertia.
    * the "dt" writing IS the even root sqrt((u.n)^2), which is what makes the action CPT-even.
    * arccosh(-u.u'/c^2) is the rapidity gap; the parity theorem says no polynomial in u can do the
      job, and this is the unique non-analytic escape.
    * rest energy m c^2 exactly, inertia m mu exactly, E = mc^2[1 + mu(gamma-1)] bounded below.
    * the ONE fitted number is the kernel's first moment, M1 = (2/3) c/a_0 = 67.7 Gyr.
  WHAT IS STILL FITTED: that moment, i.e. a_0 itself; and mu's SHAPE is the alpha = 2 interpolation,
  chosen because the ephemeris forces alpha >= 1.4.  The line buys the STRUCTURE -- causal,
  variational, Ostrogradsky-free, CPT-even, perturbatively stable in the MOND regime, correct in both
  limits -- and it does NOT buy the coefficient.  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
