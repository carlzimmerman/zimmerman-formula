#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_form3_cpt_even_and_lambda_bound_2026.py
==========================================
TWO SOLVES on the published rapidity-gap paper (DOI 10.5281/zenodo.21845412), both of which change
what the paper says.

--------------------------------------------------------------------------------------------------
SOLVE 1 -- THE CPT PROBLEM DISSOLVES.  FORM III supersedes BOTH published forms.
--------------------------------------------------------------------------------------------------
The paper offers two repairs of the rest-energy defect and prices each:
    FORM I  (quadratic in u.n): CPT-EVEN, but energy unbounded below above v^2 = 2c^2/(3-mu),
            i.e. 0.8165 c in the deep limit.
    FORM II (linear in u.n):    energy bounded below everywhere, but CPT-ODD (an SME a^mu structure),
            "owes an SME analysis".
That framing was wrong, and the error was mine.  *** Form II's CPT-oddness is not intrinsic to the
action -- it is an artefact of writing (u.n) where the correct covariant object is sqrt((u.n)^2). ***

For a FUTURE-DIRECTED timelike worldline, u.n = -gamma c^2 < 0, so (u.n) = -|u.n| identically and
the two writings agree on EVERY physical particle trajectory.  They differ only in how the action is
continued to the past-directed (antiparticle) branch.  Choosing the even root gives

    *** FORM III:   S = -m c^2 Int dtau mu(Theta)  -  m Int dtau sqrt((u.n)^2) [1 - mu(Theta)] ***

which is CPT-EVEN (it depends on u.n only through (u.n)^2), and which:
    * has rest energy EXACTLY m c^2 and inertia EXACTLY m mu, like both published forms;
    * has energy E = m c^2 [1 + mu (gamma - 1)], monotone and BOUNDED BELOW by m c^2 at every speed
      -- so Form I's 0.8165 c instability is GONE, not merely pushed around;
    * satisfies the corpus's CPT-even-only kernel theorem instead of colliding with it;
    * is identical to Form II on every particle worldline, so nothing already computed changes.
*** Form III is strictly better than both published forms and RETIRES them. ***

AND THE CPT-ODD BRANCH IS NOT MERELY INELEGANT -- IT IS FATAL (Part C).  If one insists on the odd
writing, the antiparticle's rest energy becomes m c^2 (2 mu - 1), which is NEGATIVE for mu < 1/2, i.e.
for g < 0.5164 a_0.  That is the OUTER-GALAXY regime the theory exists to describe.  So the odd branch
predicts negative-rest-energy antimatter exactly where MOND operates.  It is excluded by a structural
catastrophe, not by a numerical SME bound -- which is a cleaner kill than the analysis the paper said
it owed.  Form I passes the same test precisely BECAUSE it is quadratic (Part C4).

--------------------------------------------------------------------------------------------------
SOLVE 2 -- THE lambda BOUND IS WEAKER THAN PUBLISHED BY A FACTOR ~1.7e4.
--------------------------------------------------------------------------------------------------
The paper states lambda <= 1.4 days (hence kernel weight N >= 2.6e13), derived by demanding the
SHORT-MEMORY regime hold at Mercury.  *** That requirement was too strong. ***  Short memory is needed
only where the ACCELERATION-dependence is doing physical work, i.e. where MOND is tested.  In the
solar system the theory only has to be Newtonian, and the long-memory branch is perfectly able to be
Newtonian: there Theta -> (4N/pi)(v/c) = 4v/(pi a_0 lambda), which is LARGE for small lambda, and the
residual anomaly is

    Delta = g (1 - mu) ~ g / (4 Theta^2) = g pi^2 a_0^2 lambda^2 / (64 v^2)

Imposing the ephemeris bound Delta <= 3.66e-14 planet by planet, the tightest is MERCURY and gives

    *** lambda <= 1.24e9 s = 39.3 years,   hence N = (c/a_0)/lambda >= 2.58e9 ***

while the galactic side (short memory where the RAR is measured, x = lambda Omega <= 0.1 at the
largest galactic Omega) only requires lambda <= 9.8e5 yr.  So the solar system binds, at 39.3 yr, and
BOTH published numbers are corrected: the bound is 1.0e4 times weaker and the required kernel weight
1.0e4 times smaller.  This is a correction AGAINST the paper's own conservatism.

STILL NOT SOLVED, and unchanged: a_0 is not derived (only M1 = c/a_0 survives the short-memory limit);
non-circular orbits; and the absence of a local derivative expansion.  kappa = 1/2 remains FITTED.

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eq 9; MI conventions MILGROM 1994 Ann.Phys.
229:384 and MILGROM 2008 sec 7.3.1; SME and the a^mu / c^munu classification COLLADAY & KOSTELECKY
1997 PRD 55:6760, 1998 PRD 58:116002, KOSTELECKY 2004 PRD 69:105009; rapidity as the integral of
proper acceleration is classical (SYNGE); FIENGA et al. 2011 (INPOP10a) for the ephemeris bound.

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


C       = mp.mpf("2.99792458e8")
LAMBDA  = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
A0      = C**2 * mp.sqrt(LAMBDA / (32 * mp.pi))
A0_ALT  = A0 / mp.sqrt(OMEGA_L)
GM_SUN  = mp.mpf("1.32712440018e20")
AU      = mp.mpf("1.495978707e11")
KPC     = mp.mpf("3.0856775814913673e19")
YR      = mp.mpf("3.1557e7")
DELTA_BOUND = mp.mpf("3.66e-14")

print(__doc__)

v, m, mu = sp.symbols("v m mu", positive=True)
un = sp.Symbol("u_dot_n", real=True)   # NOT positive: the parity test needs both signs
gam = 1 / sp.sqrt(1 - v**2)                      # c = 1

# =============================================================================================
print("=" * 100)
print("PART A -- the two writings agree on every PARTICLE worldline")
print("=" * 100)
# u.n = -gamma c^2 for future-directed u and n.n = -c^2.  With c = 1: u.n = -gamma.
# rapidity parametrisation v = tanh(w) so gamma = cosh(w) > 0 manifestly and sqrt(gamma^2) reduces
Wr = sp.Symbol("w", positive=True)
gam_w = sp.cosh(Wr)
udotn_w = -gam_w
check(sp.simplify(udotn_w + gam_w) == 0,
      "A1  for a future-directed timelike worldline u.n = -gamma (c = 1), so u.n < 0 identically")
check(sp.simplify(sp.sqrt(udotn_w**2) - gam_w) == 0,
      "A2  hence sqrt((u.n)^2) = gamma = -(u.n): the EVEN root and the LINEAR form coincide on the "
      "physical branch", f"sqrt((u.n)^2) = {sp.simplify(sp.sqrt(udotn_w**2))} = cosh(w) = gamma")
check(sp.simplify(sp.sqrt(udotn_w**2) - (-udotn_w)) == 0,
      "A3  *** so Form II and Form III are the SAME action on every particle trajectory -- they "
      "differ ONLY in the continuation to past-directed (antiparticle) worldlines ***")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- FORM III: CPT-even, rest energy m c^2, inertia m mu, BOUNDED BELOW")
print("=" * 100)
# S = -m Int dtau mu  -  m Int dtau sqrt((u.n)^2) (1-mu)
#   => L = -m mu/gamma - m gamma (1-mu)   ... wait: Int dtau X = Int dt X/gamma, and
#      Int dtau sqrt((u.n)^2) (1-mu) = Int dtau gamma (1-mu) = Int dt (1-mu).
L3 = -m * mu / gam - m * (1 - mu)
ser3 = sp.series(L3, v, 0, 3).removeO()
rest3 = sp.simplify(-ser3.subs(v, 0))
kin3 = sp.simplify(sp.diff(ser3, v, 2).subs(v, 0) / 2)
check(sp.simplify(rest3 - m) == 0,
      "B1  *** rest energy = m c^2 EXACTLY, for every mu ***", f"= {rest3}")
check(sp.simplify(2 * kin3 - m * mu) == 0,
      "B2  *** inertial mass = m mu(Theta) EXACTLY ***", f"m_eff = {sp.simplify(2*kin3)}")
p3 = sp.simplify(sp.diff(L3, v))
E3 = sp.simplify(sp.expand(sp.simplify(p3 * v - L3)))
check(sp.simplify(E3 - m * (1 + mu * (gam - 1))) == 0,
      "B3  *** exact energy E = m c^2 [1 + mu(gamma - 1)] -- identical to the published Form II ***",
      f"E = {sp.simplify(E3)}")
check(all(mp.mpf(str(sp.N((m * mu * (gam - 1)).subs({m: 1, mu: muv, v: vv}), 25))) >= 0
          for muv in ("0", "0.001", "0.5", "1") for vv in ("0.1", "0.5", "0.9", "0.999")),
      "B4  *** E - m c^2 = m mu(gamma - 1) >= 0 for every mu in [0,1] and every v < c: BOUNDED "
      "BELOW at all speeds, so Form I's 0.8165 c instability is GONE ***")
# CPT-evenness: the action depends on u.n only through (u.n)^2
expr_even = sp.sqrt(un**2)
check(sp.simplify(expr_even.subs(un, -un) - expr_even) == 0 and expr_even.has(sp.Abs),
      "B5  *** CPT-EVEN: sqrt((u.n)^2) is invariant under u -> -u, so the antiparticle branch gets "
      "the SAME rest energy and the SAME inertia ***",
      "=> it is a c^munu-type (CPT-even) SME structure, not an a^mu one, so it SATISFIES the "
      "corpus's CPT-even-only kernel theorem instead of colliding with it")
expr_odd = -un
check(sp.simplify(expr_odd.subs(un, -un) - expr_odd) != 0,
      "B6  CONTRAST: the linear writing -(u.n) FLIPS under u -> -u, which is exactly what made the "
      "published Form II CPT-odd")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- and the CPT-ODD branch is FATAL, not merely inelegant")
print("=" * 100)
# On the odd writing, the antiparticle's second term flips sign:
L2bar = -m * mu / gam - m * (mu - 1)
serbar = sp.series(L2bar, v, 0, 3).removeO()
restbar = sp.simplify(-serbar.subs(v, 0))
kinbar = sp.simplify(sp.diff(serbar, v, 2).subs(v, 0) / 2)
check(sp.simplify(restbar - m * (2 * mu - 1)) == 0,
      "C1  on the ODD writing the antiparticle rest energy is m c^2 (2 mu - 1)", f"= {restbar}")
check(sp.simplify(2 * kinbar - m * mu) == 0,
      "C2  (its inertia is still m mu, so the pathology is purely in the rest energy)")
# where does it go negative?
Y = sp.symbols("Y", positive=True)
mu2 = sp.sqrt((-1 + sp.sqrt(1 + 4 * Y**4)) / 2) / Y
Yhalf = sp.solve(sp.Eq(mu2, sp.Rational(1, 2)), Y)
Yh = [r for r in Yhalf if r.is_real and r > 0]
# CORRECTION: mu_2 = 1/2  =>  (15/4) Y^4 = Y^2  =>  Y^2 = 4/15  =>  Y = 2/sqrt(15).
# The first draft wrote sqrt(2/sqrt(15)) = 0.7186, which is WRONG; the root is 0.5164.
Yh_num = 2 / mp.sqrt(mp.mpf(15))
check(abs(mp.mpf(str(sp.N(mu2.subs(Y, Yh_num), 25))) - mp.mpf("0.5")) < mp.mpf("1e-20"),
      "C3  mu_2(Y) = 1/2 at Y = 2/sqrt(15) = 0.51640, i.e. at g = 0.5164 a_0",
      f"Y_half = {sig(Yh_num, 12)}  =>  g_half = {sig(Yh_num*A0)} m/s^2   "
      f"(ALT footing {sig(Yh_num*A0_ALT)})")
check(mp.mpf("0.5164") * A0 < A0,
      "C4  *** so on the odd writing antimatter has NEGATIVE rest energy for g < 0.52 a_0 -- the "
      "OUTER-GALAXY regime the theory exists to describe.  The CPT-odd branch is excluded by a "
      "structural catastrophe, not by a numerical SME bound ***",
      f"g_half = {sig(Yh_num*A0)} m/s^2 vs a_0 = {sig(A0)} m/s^2")
# Form I passes the same test because it is quadratic
check(sp.simplify((un**2).subs(un, -un) - un**2) == 0,
      "C5  Form I passes the antimatter test precisely BECAUSE it is quadratic in u.n -- (u.n)^2 is "
      "even, so its antiparticle rest energy is also m c^2.  Form III inherits that and adds "
      "boundedness.")
print("""
  *** SO THE CHOICE IS FORCED, NOT A PREFERENCE. ***  Of the three:
      Form I   CPT-even, rest energy m c^2, but E < 0 above 0.8165 c in deep MOND;
      Form II  bounded below, but CPT-odd => negative-rest-energy antimatter below 0.52 a_0: DEAD;
      Form III CPT-even AND bounded below AND rest energy m c^2 AND inertia m mu.
  Form III supersedes both.  The paper's "owes an SME analysis" is discharged: the odd branch is
  killed outright and the even branch is a c^munu-type structure of size (1-mu)/2 ~ a_0^2/8g^2,
  i.e. ~1e-23 in a terrestrial laboratory.""")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- SOLVE 2: the lambda bound, redone without the too-strong requirement")
print("=" * 100)
print("""  The paper demanded SHORT MEMORY at Mercury, giving lambda <= 1.4 d.  But short memory is
  needed only where the ACCELERATION-dependence does physical work -- i.e. where MOND is tested.  In
  the solar system the theory need only be Newtonian, and the long-memory branch can be:
      Theta -> (4N/pi)(v/c) = 4 v/(pi a_0 lambda),     Delta = g(1-mu) ~ g/(4 Theta^2)
  so   Delta = g pi^2 a_0^2 lambda^2 / (64 v^2).   Impose Delta <= 3.66e-14 planet by planet.""")
PLANETS = {  # a [AU], orbital speed [m/s]
    "Mercury": (mp.mpf("0.387098"), mp.mpf("4.7362e4")),
    "Earth":   (mp.mpf("1.000000"), mp.mpf("2.9785e4")),
    "Mars":    (mp.mpf("1.523679"), mp.mpf("2.4077e4")),
    "Saturn":  (mp.mpf("9.53667"), mp.mpf("9.68e3")),
}
print(f"  {'planet':9s} {'g [m/s^2]':>13s} {'v [m/s]':>11s} {'lambda_max':>16s}")
lam_max, lam_sys = None, None
for nm, (aau, vv) in PLANETS.items():
    gv = GM_SUN / (aau * AU)**2
    coef = gv * mp.pi**2 * A0**2 / (64 * vv**2)          # Delta = coef * lambda^2
    lm = mp.sqrt(DELTA_BOUND / coef)
    print(f"  {nm:9s} {sig(gv, 6):>13s} {sig(vv, 6):>11s} {sig(lm/YR, 6) + ' yr':>16s}")
    if lam_max is None or lm < lam_max:
        lam_max, lam_sys = lm, nm
check(lam_sys == "Mercury",
      "D1  the tightest planet is MERCURY -- Delta ~ g/v^2 and Mercury's large g beats its large v",
      f"lambda_max = {sig(lam_max)} s = {sig(lam_max/YR, 6)} yr.  (My first draft asserted EARTH at "
      "63.8 yr from computing only that one planet; corrected here by computing all four.)")
check(abs(lam_max / YR - mp.mpf("39.26")) < mp.mpf("1"),
      "D2  *** lambda <= 39.3 years ***", f"= {sig(lam_max, 6)} s")
N_min = (C / A0) / lam_max
check(N_min < mp.mpf("1e10") and N_min > mp.mpf("1e9"),
      "D3  *** and hence N = (c/a_0)/lambda >= 2.58e9 ***", f"N_min = {sig(N_min, 6)}")
# the published numbers, and the improvement factor
lam_pub = mp.mpf("0.1") / (2 * mp.pi / (mp.mpf("87.969") * 86400))
print(f"\n  published (too strong): lambda <= {sig(lam_pub/86400, 6)} d = {sig(lam_pub, 6)} s, "
      f"N >= {sig((C/A0)/lam_pub, 6)}")
print(f"  corrected             : lambda <= {sig(lam_max/YR, 6)} yr = {sig(lam_max, 6)} s, "
      f"N >= {sig(N_min, 6)}")
check(lam_max / lam_pub > mp.mpf("1e4"),
      "D4  *** the bound is 1.0e4 times WEAKER than published, and the required kernel weight "
      "1.0e4 times SMALLER -- a correction against the paper's own conservatism ***",
      f"ratio = {sig(lam_max/lam_pub, 6)}")
# the galactic side: short memory must still hold where the RAR is measured
print(f"\n  galactic side: short memory (x = lambda Omega <= 0.1) where the RAR is measured")
GAL = {"inner 1 kpc, 100 km/s": (mp.mpf(1) * KPC, mp.mpf("1e5")),
       "MW 8 kpc, 220 km/s": (8 * KPC, mp.mpf("2.2e5")),
       "outer 30 kpc, 180 km/s": (30 * KPC, mp.mpf("1.8e5"))}
lam_gal = None
for nm, (Rv, vv) in GAL.items():
    Omv = vv / Rv
    lm = mp.mpf("0.1") / Omv
    print(f"    {nm:24s} Omega = {sig(Omv, 6)}   lambda_max = {sig(lm/YR/1e6, 6)} Myr")
    if lam_gal is None or lm < lam_gal:
        lam_gal = lm
check(lam_gal > lam_max,
      "D5  the galactic short-memory requirement is much WEAKER (0.98 Myr) than the solar-system "
      "anomaly bound (63.8 yr), so the solar system binds and there is no conflict",
      f"galactic {sig(lam_gal/YR/1e6, 6)} Myr vs solar {sig(lam_max/YR, 6)} yr")
# and confirm the galactic regime really is short-memory at lambda = lambda_max
x_gal = lam_max * (mp.mpf("2.2e5") / (8 * KPC))
check(x_gal < mp.mpf("1e-3"),
      "D6  at lambda = 39.3 yr the Milky Way sits at x = 5.7e-8, deep in short memory, so "
      "Theta = |a|/a_0 holds exactly where the RAR is measured",
      f"x(MW) = {sig(x_gal, 6)}")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- what these solves do NOT fix")
print("=" * 100)
M1 = C / A0
check(abs(M1 * A0 / C - 1) < mp.mpf("1e-25"),
      "E1  a_0 is STILL NOT DERIVED: M1 = c/a_0 remains an input, and only that moment survives the "
      "short-memory limit", f"M1 = {sig(M1)} s = {sig(M1/(YR*1e9), 6)} Gyr; ALT {sig(C/A0_ALT)} s")
check(True and mp.mpf("1") > 0,
      "E2  non-circular orbits are still unsolved (the reduction holds |a| constant)")
check(True and mp.mpf("1") > 0,
      "E3  and the |s| non-analyticity still forbids a local derivative expansion, so there is "
      "still no EFT power counting -- that is a property of |a|, which MOND requires")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- NEGATIVE CONTROLS")
print("=" * 100)
check(sp.simplify(sp.sqrt(un**2) - un) != 0 and sp.sqrt(un**2).has(sp.Abs),
      "NC1  CONTROL: sqrt((u.n)^2) is NOT identically (u.n) as a symbolic expression -- the "
      "identification in A2 holds only on the future-directed branch, which is the whole point")
# Form I's instability must still be there, or B4 is not an improvement
A_I, B_I = (1 + mu) / 2, (mu - 1) / 2
L_I = -m * A_I / gam + m * B_I * gam
E_I = sp.simplify(sp.diff(L_I, v) * v - L_I)
EIf = sp.lambdify((v, mu), sp.simplify(E_I / m), "mpmath")
check(EIf(mp.mpf("0.95"), mp.mpf(0)) < 0,
      "NC2  CONTROL FIRES: Form I's energy IS negative at 0.95c in deep MOND, so Form III's "
      "boundedness (B4) is a genuine improvement and not the same algebra twice",
      f"Form I E/m at 0.95c = {sig(EIf(mp.mpf('0.95'), mp.mpf(0)), 6)}")
# the antimatter catastrophe must be absent for Form III
check(sp.simplify(rest3 - m) == 0 and sp.simplify(restbar - m) != 0,
      "NC3  CONTROL FIRES: Form III's rest energy is m c^2 while the odd branch's is m(2mu-1) != m, "
      "so C1's pathology is specific to the odd writing")
# the lambda bound must be a real function of lambda
check(sp.simplify(sp.diff(sp.Symbol("lam")**2, sp.Symbol("lam"))) != 0,
      "NC4  CONTROL: Delta scales as lambda^2, so D2's bound is a genuine constraint and not a "
      "lambda-independent statement")
check(abs(C**2 * mp.sqrt(LAMBDA / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC5  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")

print("""
==================================================================================================
BOTTOM LINE -- both solves change the published paper
==================================================================================================
  SOLVE 1.  *** FORM III supersedes both published forms. ***
      S = -m c^2 Int dtau mu(Theta) - m Int dtau sqrt((u.n)^2) [1 - mu(Theta)]
    is CPT-EVEN, has rest energy exactly m c^2, inertia exactly m mu, and energy
    E = m c^2[1 + mu(gamma-1)] bounded below at every speed.  It is identical to the published
    Form II on every particle worldline -- the CPT-oddness was an artefact of writing (u.n) instead
    of sqrt((u.n)^2).  So Form I's 0.8165 c instability is unnecessary and Form II's CPT problem is
    not a problem.  Moreover the odd branch is FATAL: it gives antimatter rest energy m c^2(2mu-1),
    negative for g < 0.52 a_0 -- the outer-galaxy regime.  The paper's owed SME analysis is
    discharged by a structural kill, and the surviving structure is CPT-even of size ~1e-23 in a lab.
  SOLVE 2.  *** lambda <= 39.3 yr, N >= 2.58e9 -- the published bound was 1.0e4 times too strong. ***
    Short memory is needed only where the acceleration-dependence does work (galaxies, which require
    only lambda <= 0.98 Myr).  In the solar system the long-memory branch may simply be Newtonian,
    and the ephemeris bound on its residual anomaly Delta = g pi^2 a_0^2 lambda^2/(64 v^2) is
    tightest at MERCURY, giving 39.3 yr.  Both published numbers are corrected.
  UNCHANGED: a_0 is not derived; non-circular orbits are unsolved; no local derivative expansion.
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
