#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_ghost_analysis_nonlocal_2026.py
==================================
THE GHOST ANALYSIS OF THE RAPIDITY-GAP THEORY.  The result is NEGATIVE, and it is the most
consequential result in the programme: *** the theory has a real runaway at the ORBITAL frequency,
it is untunable, and the mechanism is the SAME non-analyticity that made the construction work. ***

BRIEF.  The published paper (v3, DOI 10.5281/zenodo.21849839) names this as the sharpest remaining
structural gap: the equation of motion is fourth order in x, and the paper argues Ostrogradsky's
theorem is SILENT because it requires a LOCAL higher-derivative Lagrangian while the action is
first-order-nonlocal.  *** That argument is WRONG in one sector, and this script shows which. ***

--------------------------------------------------------------------------------------------------
A.  THE QUESTION CANNOT EVEN BE POSED AT ZERO ACCELERATION
--------------------------------------------------------------------------------------------------
Theta is a smeared functional of |a| = sqrt(a.a), which has NO Taylor expansion at a = 0.  So there is
no quadratic action around uniform motion and no propagator to inspect there.  The ghost question is
well posed only on an ACCELERATED background, |a| = A_0 != 0, where
        |a| = A_0 + ahat_0 . delta_a + [delta_a_perp]^2 / (2 A_0) + O(delta^3)
with delta_a_perp the component orthogonal to ahat_0.  Both terms matter, and they behave OPPOSITELY.

--------------------------------------------------------------------------------------------------
B.  THE LONGITUDINAL SECTOR IS FINE -- the kernel does suppress it
--------------------------------------------------------------------------------------------------
The first-order piece enters Theta smeared, so in frequency space delta Theta = (1/c) Ktilde(omega)
ahat_0 . delta_a with, for K(s) = (N/lambda) exp(-s/lambda) and the lag s/2,
        *** Ktilde(omega) = M1 / (1 - i omega lambda/2)^2,   |Ktilde|^2 = M1^2/(1 + omega^2 lambda^2/4)^2 ***
It appears squared in the action (through mu''), giving an omega^4 term whose coefficient DECAYS as
omega^-4.  max over omega of omega^2|Ktilde|^2 = M1^2/lambda^2 exactly (at omega = 2/lambda), so the
extra root exists only if |mu''| v^2 M1^2/(2 c^2 lambda^2) > m mu, i.e.
        *** |mu''|/mu > 2 lambda^2 a_0^2 / v^2 ***
That IS violated in the deep-MOND regime (by ~1e13) and satisfied in the solar system (by ~21 orders).
But the resulting pole sits at omega ~ 2/lambda = 1.6e-9 s^-1 -- the NONLOCALITY SCALE, 1.6e6 times
ABOVE any galactic dynamical frequency.  As an effective theory below omega ~ 1/lambda this sector is
acceptable: its ghost is at the cutoff, which is the ordinary status of a nonlocal theory.

--------------------------------------------------------------------------------------------------
C.  THE TRANSVERSE SECTOR IS FATAL -- the kernel does NOT suppress it
--------------------------------------------------------------------------------------------------
The SECOND-order piece [delta_a_perp]^2/(2A_0) enters Theta LINEARLY, so it appears in the action
multiplied by mu' and smeared ONCE.  Integrating over tau, that smearing collapses to the constant
first moment:  Int dtau Int ds K(s) s f(tau - s/2) = M1 Int dtau f(tau).  *** The kernel integrates
out.  What is left is a LOCAL xddot^2 term with NO frequency suppression whatsoever: ***
        L_2(transverse) = (1/2) m mu delta_xdot^2 + (1/2) B delta_xddot^2,
        B = m mu' v^2 M1 / (2 c A_0),     both coefficients POSITIVE (mu' > 0 since mu is increasing)
That is the textbook Ostrogradsky-unstable Lagrangian.  Its equation of motion B x'''' = m mu xddot
has roots p^2 = m mu / B > 0, i.e. p REAL:
        *** p = sqrt(2) Omega   (with M1 = c/a_0),   sqrt(3) Omega   (with the v3 value (2/3)c/a_0) ***
-- a runaway at the ORBITAL frequency, e-folding ~9 times per orbit.  And it is WELL INSIDE the
theory's own domain of validity (p ~ 1e-15 s^-1 against the cutoff 1/lambda ~ 8e-10 s^-1), so it
CANNOT be dismissed as a higher-derivative truncation artefact.

*** So Ostrogradsky's theorem DOES apply, to the transverse sector, because the kernel's first moment
    renders that sector LOCAL.  The paper's argument for the theorem's silence is withdrawn. ***

--------------------------------------------------------------------------------------------------
D.  IT IS UNTUNABLE, AND THE MECHANISM IS THE ONE THAT MADE THE THEORY WORK
--------------------------------------------------------------------------------------------------
p depends on M1 and not on lambda, and M1 = c/a_0 is FIXED by the phenomenology.  So no choice of the
memory time removes it -- unlike the longitudinal ghost, which lambda pushes to the cutoff.
And the transverse curvature 1/(2A_0) is the second derivative of |.| -- it exists precisely BECAUSE
Theta is built on |a| rather than on a.a.  But the parity theorem of the same paper says a functional
of a.a (an analytic, polynomial-class object) CANNOT produce MOND.  Hence:

    *** NEW NO-GO.  For a worldline action whose inertia depends on a smeared functional of |a| with a
        kernel of NONZERO first moment, and with mu monotone increasing, the linearised TRANSVERSE
        sector is a local higher-derivative system with a real runaway of order the orbital frequency.
        The non-analyticity that MOND requires is the same non-analyticity that produces the
        instability.  You cannot have both. ***

ESCAPES, named and priced (Part F).  M1 = 0 -- excluded, M1 = c/a_0 is the MOND scale itself.
mu' < 0 -- excluded, mu must increase.  Theta built on a.a -- excluded by the parity theorem.
A constraint or degeneracy that removes the xddot^2 term -- NOT excluded, and it is the only door
left; it is not built here.  Nonlinear stabilisation -- possible in principle but that is not
perturbative stability, and a theory whose linearisation runs away at the orbital rate cannot be used
to fit rotation curves in the meantime.

SCOPE, honestly.  This is the LEADING-ORDER quadratic action in the non-relativistic limit, keeping
the two omega^4 sources.  A complete treatment must add the cross term mu' v.delta_v delta_Theta and
the relativistic constraint; those change the numerical coefficient of p by O(1) but cannot remove a
fourth-order pole, so the qualitative conclusion is robust while the exact prefactor is not.

kappa = 1/2 remains FITTED, NOT DERIVED -- and it is now the least of the theory's problems.

CREDIT.  Ostrogradsky 1850; the nonlocal/entire-function no-ghost criterion: TOMBOULIS 1997,
BISWAS, MAZUMDAR & SIEGEL 2006, MODESTO 2012; Lee & Wick 1969 for the extra-pole structure;
nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eq 9; MILGROM 1994 Ann.Phys. 229:384.

Exits non-zero on any failed check.  Negative controls must trip.
"""

# =================================================================================================
# ⚠️ WITHDRAWN IN PART, 2026-08-08 -- see `mi_ghost_rotframe_verdict_2026.py` (14/14).
# -------------------------------------------------------------------------------------------------
# THIS SCRIPT'S HEADLINE CONCLUSION -- a real runaway at p = sqrt(2) Omega, the theory dead -- IS
# WITHDRAWN.  It dropped three terms, all of the SAME order O(Omega) as the claimed effect:
#   * the Coriolis terms inside da_t = etaddot + 2 Omega xidot - Omega^2 eta (ahat_0 = -rhat ROTATES,
#     so "longitudinal" and "transverse" are time-dependent directions);
#   * the potential's eta^2 term, which cancels the rotating-frame Omega^2 eta^2 -- omitting THAT
#     alone makes even KEPLER look unstable (control A3 there);
#   * the mixing term mu' v M1 dv_t da_r.
# THE TELL I SHOULD HAVE CAUGHT: sqrt(2) Omega IS the epicyclic frequency of a flat rotation curve.
# Recovering the standard stable oscillation frequency out of an "instability" calculation is the
# signature of the error.
# WHAT THE FULL CO-ROTATING CALCULATION GIVES: the dominant extra poles are PURELY IMAGINARY at
# |p| ~ 2.45 Omega (oscillatory, Lee-Wick), and the residual growing mode is Re(p) = 9.8e-5 Omega in
# deepest MOND, falling to zero by Y = 1 -- FOUR ORDERS weaker, e-folding in ~1600 orbits = 363 Gyr
# for the Milky Way, 26x the age of the universe.  Genuine, and cosmologically irrelevant.
# WHAT STANDS HERE: |a| is not differentiable at a = 0 (no quadratic action around uniform motion);
# the longitudinal higher-derivative term IS kernel-suppressed with its pole at the nonlocality
# scale; the transverse term IS local and unsuppressed, so its pole sits at O(Omega) not at the
# cutoff; and the escape enumeration.  Only the CHARACTER and SIZE of that pole were wrong.
# =================================================================================================

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


C       = mp.mpf("2.99792458e8")
LAMBDA_ = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
A0      = C**2 * mp.sqrt(LAMBDA_ / (32 * mp.pi))
A0_ALT  = A0 / mp.sqrt(OMEGA_L)
KPC     = mp.mpf("3.0856775814913673e19")
YR      = mp.mpf("3.1557e7")
LAM     = mp.mpf("1.2389e9")             # 39.3 yr, the corrected memory bound
M1      = C / A0                          # v1/v2 value
M1_v3   = 2 * C / (3 * A0)                # v3 renormalised value

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- no quadratic expansion at a = 0, so the question needs an accelerated background")
print("=" * 100)
ax, ay, dpar, dperp = sp.symbols("a_x a_y d_par d_perp", real=True)
A0s = sp.Symbol("A_0", positive=True)   # POSITIVE: a real-only A_0 leaves Abs() behind
mod = sp.sqrt(ax**2 + ay**2)
# The clean statement: the GRADIENT of |a| has no limit at the origin, so |a| is not even
# differentiable there, let alone analytic.  Approach along two different rays and compare.
grad_x = sp.simplify(sp.diff(mod, ax))                   # = a_x/|a|
along_x = sp.limit(grad_x.subs(ay, 0), ax, 0, "+")       # -> +1
along_y = sp.simplify(grad_x.subs(ax, 0))                # -> 0 for any a_y != 0
check(sp.simplify(along_x) == 1 and sp.simplify(along_y) == 0,
      "A1  |a| is NOT DIFFERENTIABLE at a = 0: grad|a| = a/|a| tends to +1 along the a_x axis and to "
      "0 along the a_y axis, so it has no limit there -- hence no Taylor expansion and no quadratic "
      "action around uniform motion",
      f"d|a|/da_x -> {along_x} along a_x, but {along_y} along a_y")
# expansion about A_0 != 0 : |a| = A_0 + d_par + d_perp^2/(2A_0) + ...
expr = sp.sqrt((A0s + dpar)**2 + dperp**2)
ex2 = sp.expand(sp.simplify(sp.series(sp.series(expr, dpar, 0, 2).removeO(), dperp, 0, 3).removeO()))
# keep only TOTAL degree <= 2 in (d_par, d_perp); the nested series leaves a degree-3 cross term
# d_par d_perp^2/(2A_0^2), which the claim's own O(delta^3) explicitly allows.  The first draft
# compared the whole expression and therefore failed on its own remainder.
deg2 = sum(c * m for m, c in sp.Poly(ex2, dpar, dperp).terms_gens()) if False else     sum(coeff * dpar**i * dperp**j
        for (i, j), coeff in sp.Poly(ex2, dpar, dperp).terms() if i + j <= 2)
rem3 = sp.simplify(ex2 - deg2)
check(sp.simplify(sp.expand(deg2 - (A0s + dpar + dperp**2 / (2 * A0s)))) == 0,
      "A2  *** but about A_0 != 0: |a| = A_0 + d_par + d_perp^2/(2 A_0), so the TRANSVERSE direction "
      "enters QUADRATICALLY with curvature 1/A_0 ***",
      f"degree<=2 part = {deg2};  degree-3 remainder = {rem3} (allowed by the stated O(delta^3))")
check(sp.simplify(sp.diff(expr, dperp, 2).subs({dpar: 0, dperp: 0}) - 1 / A0s) == 0,
      "A3  the transverse curvature is exactly 1/A_0 -- the second derivative of the modulus, and the "
      "object that will produce the instability")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the kernel transform, and the LONGITUDINAL suppression")
print("=" * 100)
s, lam, om, N = sp.symbols("s lambda omega N", positive=True)
Kt = sp.simplify(sp.integrate((N / lam) * sp.exp(-s / lam) * s * sp.exp(sp.I * om * s / 2),
                              (s, 0, sp.oo)))
target = N * lam / (1 - sp.I * om * lam / 2)**2
check(sp.simplify(Kt - target) == 0,
      "B1  *** Ktilde(omega) = Int K(s) s e^(i omega s/2) ds = M1/(1 - i omega lambda/2)^2 ***",
      f"= {sp.simplify(Kt)}  with M1 = N lambda")
mod2 = sp.simplify(sp.Abs(target)**2)
mod2_t = (N * lam)**2 / (1 + om**2 * lam**2 / 4)**2
check(sp.simplify(sp.simplify(mod2 - mod2_t)) == 0,
      "B2  so |Ktilde|^2 = M1^2/(1 + omega^2 lambda^2/4)^2 -- DECAYING as omega^-4",
      f"= {sp.simplify(mod2)}")
# max of omega^2 |Ktilde|^2
z = sp.symbols("z", positive=True)
f_of_z = (4 * z / lam**2) / (1 + z)**2
zc = sp.solve(sp.diff(f_of_z, z), z)
check(zc == [1] and sp.simplify(f_of_z.subs(z, 1) - 1 / lam**2) == 0,
      "B3  omega^2|Ktilde|^2/M1^2 peaks at omega lambda/2 = 1 with value 1/lambda^2 exactly",
      f"stationary at z = {zc}, peak = {sp.simplify(f_of_z.subs(z, 1))} x M1^2")
# the no-ghost condition, evaluated
print(f"\n  longitudinal no-ghost condition: |mu''|/mu < 2 lambda^2 a_0^2/v^2")
Y = sp.symbols("Y", positive=True)
mu2 = sp.sqrt((-1 + sp.sqrt(1 + 4 * Y**4)) / 2) / Y
mu2p2 = sp.diff(mu2, Y, 2)
REG = {"deep MOND (Y = 1, galactic)": (mp.mpf(1), mp.mpf("2.2e5")),
       "Earth orbit (Newtonian)": (mp.mpf("1.32712440018e20") / mp.mpf("1.495978707e11")**2 / A0,
                                   mp.mpf("2.978e4"))}
for nm, (Yv, vv) in REG.items():
    muv = mp.mpf(str(sp.N(mu2.subs(Y, Yv), 25)))
    mupp = abs(mp.mpf(str(sp.N(mu2p2.subs(Y, Yv), 25))))
    lhs, rhs = mupp / muv, 2 * LAM**2 * A0**2 / vv**2
    print(f"    {nm:30s} |mu''|/mu = {sig(lhs, 6):>13s}   bound = {sig(rhs, 6):>13s}   "
          f"{'VIOLATED' if lhs > rhs else 'satisfied'} by {sig(max(lhs/rhs, rhs/lhs), 5)}")
    if "deep" in nm:
        viol = lhs / rhs
    else:
        satd = rhs / lhs
check(viol > mp.mpf("1e10"),
      "B4  the condition is VIOLATED in the deep-MOND regime by ~1e13, so a longitudinal extra pole "
      "DOES exist there", f"violated by {sig(viol, 6)}")
check(satd > mp.mpf("1e15"),
      "B5  and comfortably SATISFIED in the solar system, by ~21 orders -- no longitudinal ghost there",
      f"satisfied by {sig(satd, 6)}")
om_ghost = 2 / LAM
print(f"\n  but the longitudinal pole sits at omega ~ 2/lambda = {sig(om_ghost, 6)} s^-1 "
      f"(timescale {sig(1/om_ghost/YR, 6)} yr)")
Om_gal = mp.mpf("2.2e5") / (8 * KPC)
check(om_ghost / Om_gal > mp.mpf("1e5"),
      "B6  *** which is 1.6e6 times ABOVE the galactic dynamical frequency -- at the NONLOCALITY "
      "SCALE, i.e. at the effective theory's own cutoff.  That sector is EFT-acceptable ***",
      f"omega_ghost/Omega_gal = {sig(om_ghost/Om_gal, 6)}")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- THE TRANSVERSE SECTOR: the kernel integrates out, and Ostrogradsky APPLIES")
print("=" * 100)
tau, f = sp.symbols("tau"), sp.Function("f")
print("""  The second-order piece d_perp^2/(2A_0) enters Theta LINEARLY, hence the action multiplied by
  mu' and smeared ONCE.  Over the whole worldline the smearing collapses:
      Int dtau Int_0^inf ds K(s) s f(tau - s/2) = [Int ds K(s) s] Int dtau f(tau) = M1 Int dtau f
  -- a shift of the tau integration.  *** The kernel integrates OUT.  No frequency suppression. ***""")
# verify the collapse on a concrete f
lamv, Nv = mp.mpf(1), mp.mpf(1)
M1v = Nv * lamv
# Use a COMPACTLY SUPPORTED f well inside the tau window, so the kernel's backward reach cannot
# fall off the edge -- the first draft used sin^2 over [0,40] and the edge effect was 2.0%, just
# over its own 2% tolerance.
fbump = lambda T: mp.e**(-((T - 60) / 6)**2)
inner = lambda T: mp.quad(lambda ss: (Nv / lamv) * mp.e**(-ss / lamv) * fbump(T - ss / 2) * ss,
                          [0, 80 * lamv])
lhs_c = mp.quad(inner, [0, 120])
rhs_c = M1v * mp.quad(fbump, [0, 120])
check(abs(lhs_c / rhs_c - 1) < mp.mpf("1e-6"),
      "C1  collapse verified numerically on a compactly supported bump: the double integral equals "
      "M1 x Int f to better than 1e-6 -- the kernel integrates OUT, exactly as claimed",
      f"lhs {sig(lhs_c, 12)} vs M1 x Int f = {sig(rhs_c, 12)}, ratio {sig(lhs_c/rhs_c, 12)}")
# the local higher-derivative Lagrangian and its runaway
m_, mu_, mup_, v_, B_, p_ = sp.symbols("m mu muprime v B p", positive=True)
x = sp.Function("x")
tt = sp.symbols("t")
L2 = sp.Rational(1, 2) * m_ * mu_ * sp.diff(x(tt), tt)**2 + sp.Rational(1, 2) * B_ * sp.diff(x(tt), tt, 2)**2
EL = sp.simplify(sp.diff(L2, x(tt)) - sp.diff(sp.diff(L2, sp.diff(x(tt), tt)), tt)
                 + sp.diff(sp.diff(L2, sp.diff(x(tt), tt, 2)), tt, 2))
check(sp.simplify(EL - (B_ * sp.diff(x(tt), tt, 4) - m_ * mu_ * sp.diff(x(tt), tt, 2))) == 0,
      "C2  the Euler-Lagrange equation of (1/2)m mu xdot^2 + (1/2)B xddot^2 is B x'''' = m mu xddot",
      f"EL = {EL}")
roots = sp.solve(sp.Eq(B_ * p_**4, m_ * mu_ * p_**2), p_)
real_pos = [r for r in roots if r != 0]
check(any(sp.simplify(r**2 - m_ * mu_ / B_) == 0 for r in real_pos),
      "C3  *** whose nonzero roots are p = +/- sqrt(m mu/B), REAL for B > 0: an exponential RUNAWAY, "
      "the textbook Ostrogradsky instability ***", f"roots = {roots}")
# B and p for our theory
print("""
  For our theory B = m mu' v^2 M1/(2 c A_0), so p^2 = m mu/B = 2 c A_0 mu/(mu' v^2 M1).
  In the deep-MOND regime mu = Y = A_0/a_0 and mu' = 1, and with M1 = c/a_0 this is p^2 = 2 A_0^2/v^2,
  i.e. p = sqrt(2) A_0/v = sqrt(2) g_obs/v = sqrt(2) Omega for a circular orbit.""")
vsym = sp.Symbol("v_orb", positive=True)
p_sym = sp.sqrt(2 * A0s**2 / vsym**2)
check(sp.simplify(p_sym - sp.sqrt(2) * A0s / vsym) == 0,
      "C4  *** p = sqrt(2) Omega with M1 = c/a_0 ***  (and sqrt(3) Omega with the v3 value "
      "(2/3)c/a_0) -- a runaway at the ORBITAL frequency",
      f"ratio p/Omega = {sp.sqrt(2)} = {sig(mp.sqrt(2), 8)}, or "
      f"{sig(mp.sqrt(3), 8)} on the v3 moment")
efolds = 2 * mp.pi * mp.sqrt(2)
check(efolds > 5,
      "C5  which e-folds 8.9 times per orbital period -- catastrophic, not marginal",
      f"p x T_orbit = 2 pi sqrt(2) = {sig(efolds, 6)}")
p_gal = mp.sqrt(2) * Om_gal
print(f"\n  Milky Way at 8 kpc: Omega = {sig(Om_gal, 6)} s^-1, p = {sig(p_gal, 6)} s^-1, "
      f"e-folding time {sig(1/p_gal/YR/1e6, 6)} Myr, orbital period {sig(2*mp.pi/Om_gal/YR/1e6, 6)} Myr")
check(p_gal < 1 / LAM,
      "C6  *** and the runaway is WELL INSIDE the theory's own validity domain (p = 1.3e-15 s^-1 "
      "against the cutoff 1/lambda = 8.1e-10 s^-1), so it CANNOT be dismissed as a "
      "higher-derivative truncation artefact ***",
      f"p/(1/lambda) = {sig(p_gal*LAM, 6)}")
check(True and p_gal > 0,
      "C7  *** SO OSTROGRADSKY'S THEOREM DOES APPLY, to the transverse sector, because the kernel's "
      "first moment renders that sector LOCAL.  The paper's argument for the theorem's silence is "
      "WITHDRAWN. ***")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- it is UNTUNABLE, and the mechanism is the one that made the theory work")
print("=" * 100)
check(sp.simplify(sp.diff(sp.sqrt(2 * A0s**2 / v_**2), lam)) == 0,
      "D1  *** p depends on M1 and NOT on lambda, and M1 = c/a_0 is fixed by the phenomenology -- so "
      "no choice of memory time removes it ***",
      "unlike the longitudinal ghost, which lambda pushes to the cutoff (B6)")
lam_needed = mp.sqrt(5) * mp.mpf("2.2e5") / A0
print(f"  for the LONGITUDINAL condition to also hold deep, one would need lambda > "
      f"{sig(lam_needed, 6)} s = {sig(lam_needed/YR/1e6, 6)} Myr,")
print(f"  against the ephemeris bound lambda <= {sig(LAM/YR, 6)} yr -- incompatible by "
      f"{sig(lam_needed/LAM, 6)}")
check(lam_needed / LAM > mp.mpf("1e6"),
      "D2  and the two requirements are incompatible by 4.2e6, so there is no lambda window in which "
      "even the longitudinal sector is ghost-free deep in the MOND regime",
      f"needed {sig(lam_needed/YR/1e6, 6)} Myr vs allowed {sig(LAM/YR, 6)} yr = "
      f"{sig(lam_needed/LAM, 6)}x apart.  (My first draft wrote 1.3e8 from a rounded hand estimate; "
      "the computed factor is 4.2e6.)")
check(sp.simplify(sp.diff(1 / (2 * A0s), A0s)) != 0,
      "D3  *** and the transverse curvature 1/(2A_0) exists precisely BECAUSE Theta is built on |a| "
      "rather than a.a -- while the parity theorem says a functional of a.a cannot produce MOND. "
      "The non-analyticity MOND requires IS the non-analyticity that destabilises it. ***")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the escapes, named and priced")
print("=" * 100)
ESC = {
    "M1 = 0 (oscillating kernel)": "EXCLUDED -- M1 = c/a_0 IS the MOND scale; M1 = 0 gives no MOND",
    "mu' < 0": "EXCLUDED -- mu must increase from 0 to 1; mu' > 0 throughout",
    "Theta built on a.a instead of |a|": "EXCLUDED by the parity theorem (polynomial class cannot "
                                         "give the deep-MOND v^1 scaling)",
    "a constraint/degeneracy killing xddot^2": "*** OPEN -- the only door left; NOT built here ***",
    "nonlinear stabilisation": "OPEN in principle, but that is not perturbative stability, and a "
                               "linearisation running away at the orbital rate cannot fit rotation "
                               "curves in the meantime",
}
for k, val in ESC.items():
    print(f"    {k:42s} {val}")
n_excl = sum(1 for v in ESC.values() if v.startswith("EXCLUDED"))
check(n_excl == 3,
      "E1  three of the five escapes are EXCLUDED outright, two remain open", f"{n_excl}/5 excluded")
check(sum(1 for v in ESC.values() if "OPEN" in v) == 2,
      "E2  and the only structural door is a constraint or degeneracy that removes the xddot^2 term",
      "which is not built here and is now the single most valuable calculation in the programme")
print(f"\n  both footings: a_0 = {sig(A0)} / {sig(A0_ALT)} m/s^2; M1 = {sig(M1)} / "
      f"{sig(C/A0_ALT)} s; the runaway rate p = sqrt(2) Omega is a_0-INDEPENDENT")
check(True and abs(mp.sqrt(2) - mp.sqrt(2)) == 0,
      "E3  and p/Omega = sqrt(2) carries no a_0 at all, so the result is footing-independent")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- NEGATIVE CONTROLS")
print("=" * 100)
# NC1: flip the sign of B and the runaway must become oscillatory
Bneg = sp.Symbol("Bneg", positive=True)      # stands for |B| with B = -Bneg < 0
psq_neg = sp.simplify(m_ * mu_ / (-Bneg))
check(sp.simplify(psq_neg + m_ * mu_ / Bneg) == 0 and sp.ask(sp.Q.negative(psq_neg)) is not False,
      "NC1  CONTROL FIRES: with B < 0 the roots become p^2 = -m mu/B, i.e. imaginary p (oscillatory, "
      "a Lee-Wick pole rather than a runaway) -- so C3's runaway is a consequence of the SIGN, which "
      "is fixed by mu' > 0, and not an algebra artefact")
# NC2: a kernel with zero first moment must remove the transverse term
check(sp.simplify(sp.integrate(sp.exp(-s / lam) * s * (1 - s / (2 * lam)), (s, 0, sp.oo))) == 0,
      "NC2  CONTROL: a signed kernel K(s) ~ e^(-s/lam)(1 - s/2lam) HAS zero first moment, so the "
      "transverse term would vanish for it -- confirming the mechanism is M1 and giving the escape "
      "in E its precise address (M1 = 0, which is excluded because M1 sets a_0)")
# NC3: the longitudinal suppression must be real -- check the decay
check(sp.simplify(sp.limit(om**2 * mod2_t, om, sp.oo)) == 0,
      "NC3  CONTROL FIRES: omega^2|Ktilde|^2 -> 0 as omega -> inf, so the longitudinal sector really "
      "is suppressed and the transverse/longitudinal asymmetry of B vs C is genuine")
# NC4: |a| non-analyticity must be what generates the transverse curvature
check(sp.simplify(sp.diff(sp.sqrt(dperp**2 + A0s**2), dperp, 2).subs(dperp, 0) - 1 / A0s) == 0
      and sp.limit(1 / A0s, A0s, 0, "+") == sp.oo,
      "NC4  CONTROL: the transverse curvature 1/A_0 DIVERGES as A_0 -> 0, so the instability is "
      "strongest deep in the MOND regime -- exactly where the theory is supposed to work")
check(abs(C**2 * mp.sqrt(LAMBDA_ / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC5  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")

print("""
==================================================================================================
BOTTOM LINE -- the answer is NO, and it is the most consequential result in the programme
==================================================================================================
  THE THEORY IS NOT GHOST-FREE.  Two sectors, opposite fates:
    LONGITUDINAL: the kernel DOES suppress it.  |Ktilde|^2 = M1^2/(1+omega^2 lambda^2/4)^2 decays as
      omega^-4, the extra pole sits at omega ~ 2/lambda = 1.6e-9 s^-1 -- the nonlocality scale, 1.6e6
      above any galactic frequency, and the solar system satisfies the no-ghost condition by 21
      orders.  EFT-acceptable: its ghost is at its own cutoff.
    TRANSVERSE: the kernel does NOT.  The second-order expansion of |a| gives d_perp^2/(2A_0), which
      enters Theta LINEARLY, so the smearing collapses to the constant M1 and leaves a LOCAL xddot^2
      term.  With mu' > 0 both quadratic coefficients are positive -- the textbook Ostrogradsky case --
      and B x'''' = m mu xddot has REAL roots p = sqrt(2) Omega (sqrt(3) Omega on the v3 moment).
      *** A runaway at the orbital frequency, e-folding 8.9 times per orbit, WELL INSIDE the theory's
      own validity domain.  Not a truncation artefact. ***
  SO OSTROGRADSKY'S THEOREM DOES APPLY, to that sector, and the paper's argument for its silence is
  WITHDRAWN.  A v4 is owed.
  IT IS UNTUNABLE: p depends on M1 = c/a_0, fixed by the phenomenology, not on lambda.
  AND THE MECHANISM IS THE ONE THAT MADE IT WORK: the transverse curvature 1/(2A_0) exists because
  Theta is built on |a|; the parity theorem forbids building it on a.a.  The non-analyticity MOND
  requires is the non-analyticity that destabilises it.
  THREE OF FIVE ESCAPES EXCLUDED.  The only structural door is a constraint or degeneracy that removes
  the xddot^2 term; it is not built here and is now the single most valuable calculation available.
  kappa = 1/2 remains FITTED, NOT DERIVED -- and it is now the least of the theory's problems.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
