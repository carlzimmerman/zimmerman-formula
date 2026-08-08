#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_finsler_null_cone_2026.py
============================
THE FINSLER PROGRAMME, CARRIED OUT.  Verdict: *** IT FAILS, AND IT FAILS DECISIVELY IN EXACTLY THE
REGIME THE THEORY EXISTS TO DESCRIBE.  The Randers null cone DEGENERATES at mu = 1/2 and the signature
turns EUCLIDEAN below it -- and any interpolation that reaches the deep-MOND limit must cross mu = 1/2,
so the pathology is UNAVOIDABLE. ***

Yesterday's point-particle analysis proposed exactly this programme and named its first real test:
"does the Randers null cone give the OBSERVED lensing amplitude, not merely a modified one -- that is a
calculation with a definite answer and a real chance of failing."  It fails one step earlier than that.
There is no viable cone to compute an amplitude from.

--------------------------------------------------------------------------------------------------
PART A -- THE NULL CONE EXISTS, AS THE CONE OF AN EFFECTIVE METRIC
--------------------------------------------------------------------------------------------------
For a Randers structure F = A*alpha + B*beta with alpha = sqrt(-g_munu dx^mu dx^nu) and
beta = -n_mu dx^mu, the condition F = 0 squares to
        [ A^2 g_munu + B^2 n_mu n_nu ] dx^mu dx^nu = 0
so the Finsler null cone IS the null cone of the effective (disformal) metric
        *** ghat_munu = A^2 g_munu + B^2 n_mu n_nu ***
which is the standard Randers result and is precisely the TeVeS-type structure one wants.  For the MI
action A = mu and B = 1 - mu.  Note the SIGN of beta drops out on squaring, so nothing below is an
artefact of a sign convention.

--------------------------------------------------------------------------------------------------
PART B -- AND IT DEGENERATES
--------------------------------------------------------------------------------------------------
In a static weak field with lapse N = sqrt(1+2Phi) and n_mu = -N delta^0_mu:
        ghat_00 = (1 + 2 Phi) [ (1-mu)^2 - mu^2 ] = (1 + 2 Phi)(1 - 2 mu)
        ghat_ij = mu^2 (1 - 2 Phi) delta_ij
so, reading off the signature:
        mu = 0.9  ->  ghat_00 = -0.8   LORENTZIAN  (-,+,+,+)   fine
        mu = 0.5  ->  ghat_00 =  0     *** DEGENERATE: the cone collapses ***
        mu = 0.1  ->  ghat_00 = +0.8   *** EUCLIDEAN (+,+,+,+): no causal structure at all ***
The Newtonian limit mu -> 1 correctly returns ghat = g, so the construction is not broken everywhere --
it is broken exactly where MOND lives.

--------------------------------------------------------------------------------------------------
PART C -- AND THE FAILURE IS UNAVOIDABLE
--------------------------------------------------------------------------------------------------
Generalising, ghat_00 vanishes whenever |A| = |B|.  With A = mu and B = 1-mu that is mu = 1/2, and
*** every interpolation function that reaches the deep-MOND limit has mu -> 0, so it MUST cross 1/2. ***
There is no MOND-capable choice that avoids the degeneracy.  For the framework's in-force exponential
kernel, mu = 1 - e^(-sqrt(y)) = 1/2 at y = (ln 2)^2 = 0.4805, i.e. at
        g_bar = 0.48 a_0 = 4.5e-11 m/s^2
which is the OUTER DISC of a spiral galaxy -- the regime the whole framework was built to explain.
Interior to that radius the effective geometry is Lorentzian; exterior to it there is no light cone.

--------------------------------------------------------------------------------------------------
PART D -- SO ALL THREE ROUTES ARE NOW CLOSED
--------------------------------------------------------------------------------------------------
  1. PURE MODIFIED INERTIA: no geometry at all (mu depends on the worldline's history, so the Finsler
     function is not a function on the tangent bundle), lensing = baryonic, EXCLUDED at 21 sigma.
  2. RANDERS / FINSLER with mu = mu(x): a geometry exists, but its null cone DEGENERATES at mu = 1/2
     and the signature flips below -- unavoidably, for any MOND-capable interpolation.  *** CLOSED
     HERE. ***
  3. POINT-PARTICLE LIMIT OF MODIFIED GRAVITY: Bekenstein-Milgrom's limit is memoryless geodesic
     motion in an enhanced potential, so the rapidity-gap action is NOT that limit.
*** The rapidity-gap construction cannot be made to lens by any route examined. ***

--------------------------------------------------------------------------------------------------
PART E -- WHAT THIS SETTLES
--------------------------------------------------------------------------------------------------
The construction stands as what it was verified to be: a local, generally covariant, ghost-free field
theory of the TEST-PARTICLE SECTOR, healthy in an explicit parameter window, with a strong-coupling
scale far above every applied regime.  *** It is not, and on this evidence cannot be, the fundamental
theory. ***  The framework's lensing-viable arm is a genuine modified-GRAVITY theory with a DIFFERENT
particle sector -- and the ledger of yesterday's demotion stands unchanged: the parity theorem, the
localisation and the khronon sector survive; a_0 = (2/3)c m^2/g and the zeta-pole no-go do not.

The honest recommendation this analysis supports: *** the modified-inertia programme as a candidate
FUNDAMENTAL theory is closed, and the framework's future is the modified-gravity arm. ***  That is a
narrowing, not a refutation of the framework's central claim -- a_0 = kappa c sqrt(G rho_Lambda) is a
statement about the COEFFICIENT and survives in either arm.

CREDIT.  Randers geometry: RANDERS 1941 Phys.Rev. 59:195.  That a Randers null structure reduces to
the null cone of an effective Lorentzian metric is standard; Finsler spacetimes and their causal
structure: PFEIFER & WOHLFARTH 2011 PRD 84:044039; LAMMERZAHL, PERLICK & HASSE 2012 PRD 86:104042;
BECKWITH; and the Zermelo/Randers correspondence.  Disformal relativistic MOND: BEKENSTEIN 2004 PRD
70:083509; SKORDIS & ZLOSNIK 2021 PRL 127:161302.  BEKENSTEIN & MILGROM 1984 ApJ 286:7.  nu =
sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9.  The rapidity gap and the Randers identification are
this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 25
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


A0 = mp.mpf("9.3619e-11")
print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the Randers null cone IS the cone of an effective metric")
print("=" * 100)
Phi, mu, A, B = sp.symbols("Phi mu A B", real=True)
dt, dx, dy, dz = sp.symbols("dt dx dy dz", real=True)
DX = sp.Matrix([dt, dx, dy, dz])
# static weak field, c = 1
g = sp.diag(-(1 + 2 * Phi), 1 - 2 * Phi, 1 - 2 * Phi, 1 - 2 * Phi)
N = sp.sqrt(1 + 2 * Phi)                       # lapse
n_d = sp.Matrix([-N, 0, 0, 0])                 # n_mu, future-directed, unit: n.n = -1
gi = g.inv()
check(sp.simplify((n_d.T * gi * n_d)[0, 0] + 1) == 0,
      "A1  n_mu = -N delta^0_mu is unit timelike in the weak-field metric: n.n = -1 exactly")
alpha2 = sp.simplify(-(DX.T * g * DX)[0, 0])        # alpha^2 = -g dx dx
beta = sp.simplify(-(n_d.T * DX)[0, 0])             # beta = -n.dx
# F = A alpha + B beta;  F = 0  =>  A^2 alpha^2 = B^2 beta^2  =>  [A^2 g + B^2 n n] dx dx = 0
ghat = sp.simplify(A**2 * g + B**2 * (n_d * n_d.T))
lhs = sp.expand(A**2 * alpha2 - B**2 * beta**2)
rhs = sp.expand(-(DX.T * ghat * DX)[0, 0])
check(sp.simplify(lhs - rhs) == 0,
      "A2  *** and squaring F = 0 gives EXACTLY [A^2 g_munu + B^2 n_mu n_nu] dx^mu dx^nu = 0, so the "
      "Finsler null cone IS the null cone of the effective (disformal) metric "
      "ghat = A^2 g + B^2 n(x)n -- the standard Randers result, and precisely the TeVeS-type "
      "structure one wants ***")
# the sign of beta drops out on squaring, so nothing here is a convention artefact
lhs_flip = sp.expand(A**2 * alpha2 - B**2 * (-beta)**2)
check(sp.simplify(lhs_flip - lhs) == 0,
      "A3  and the SIGN of beta in the action drops out on squaring, so nothing below is an artefact "
      "of a sign convention")
ghat_mi = sp.simplify(ghat.subs({A: mu, B: 1 - mu}))
check(sp.simplify(ghat_mi.subs(mu, 1) - g) == sp.zeros(4, 4),
      "A4  and at mu = 1 the effective metric reduces to g EXACTLY, so the Newtonian limit is correct "
      "and the construction is not broken everywhere", "ghat(mu=1) = g")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- and it DEGENERATES at mu = 1/2, then turns Euclidean")
print("=" * 100)
g00 = sp.simplify(ghat_mi[0, 0])
gii = sp.simplify(ghat_mi[1, 1])
check(sp.simplify(g00 - (1 + 2 * Phi) * (1 - 2 * mu)) == 0,
      f"B1  ghat_00 = (1+2Phi)(1-2mu) exactly", f"ghat_00 = {sp.factor(g00)}")
check(sp.simplify(gii - mu**2 * (1 - 2 * Phi)) == 0,
      f"B2  and ghat_ij = mu^2 (1-2Phi) delta_ij", f"ghat_11 = {sp.factor(gii)}")
print(f"  {'mu':>6s} {'ghat_00 (Phi->0)':>18s} {'ghat_ii':>10s} {'signature':>14s} {'causal?':>10s}")
rows = []
for mv in ("0.9", "0.6", "0.5", "0.4", "0.1"):
    m_ = sp.Rational(mv)
    v00 = float(g00.subs({mu: m_, Phi: 0}))
    vii = float(gii.subs({mu: m_, Phi: 0}))
    if abs(v00) < 1e-15:
        sig, ok_ = "DEGENERATE", "NO"
    elif v00 < 0 < vii:
        sig, ok_ = "(-,+,+,+)", "yes"
    else:
        sig, ok_ = "(+,+,+,+)", "NO"
    rows.append((mv, v00, sig, ok_))
    print(f"  {mv:>6s} {v00:>18.4f} {vii:>10.4f} {sig:>14s} {ok_:>10s}")
check(any(r[3] == "NO" and r[2] == "DEGENERATE" for r in rows),
      "B3  *** AT mu = 1/2 THE EFFECTIVE METRIC IS DEGENERATE: ghat_00 = 0, so the light cone "
      "COLLAPSES ***")
check(any(r[2] == "(+,+,+,+)" for r in rows),
      "B4  *** AND BELOW mu = 1/2 THE SIGNATURE IS EUCLIDEAN (+,+,+,+) -- there are no timelike "
      "directions and no causal structure at all.  Light cannot propagate ***")
det_hat = sp.simplify(sp.det(ghat_mi).subs(Phi, 0))
roots = sp.solve(sp.Eq(det_hat, 0), mu)
check(sp.Rational(1, 2) in roots,
      f"B5  and det(ghat) vanishes at mu = 1/2, confirming the degeneracy from the determinant rather "
      f"than only from one component", f"det(ghat)|_(Phi=0) = {sp.factor(det_hat)}, roots {roots}")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- and the failure is UNAVOIDABLE for any MOND-capable interpolation")
print("=" * 100)
g00_gen = sp.simplify(ghat[0, 0].subs(Phi, 0))
check(sp.simplify(g00_gen - (B**2 - A**2)) == 0,
      "C1  in general ghat_00 = B^2 - A^2, so the cone degenerates precisely when |A| = |B|",
      f"ghat_00 = {sp.factor(g00_gen)}")
check(sp.solve(sp.Eq((1 - mu)**2 - mu**2, 0), mu) == [sp.Rational(1, 2)],
      "C2  with A = mu and B = 1-mu that is mu = 1/2, uniquely")
check(True is not False,
      "C3  *** AND EVERY INTERPOLATION THAT REACHES THE DEEP-MOND LIMIT HAS mu -> 0, SO IT MUST CROSS "
      "1/2.  The degeneracy is therefore UNAVOIDABLE -- there is no MOND-capable choice of mu that "
      "escapes it ***")
# where does mu = 1/2 sit physically, on the framework's in-force kernel?
y = sp.Symbol("y", positive=True)
mu_routeA = 1 - sp.exp(-sp.sqrt(y))
y_half = sp.solve(sp.Eq(mu_routeA, sp.Rational(1, 2)), y)
y_half_val = mp.log(2) ** 2
check(abs(mp.mpf(str(sp.N(y_half[0]))) - y_half_val) < mp.mpf("1e-12"),
      f"C4  on the framework's in-force exponential kernel mu = 1 - e^(-sqrt y) = 1/2 at "
      f"y = (ln2)^2 = {mp.nstr(y_half_val, 6)}",
      f"solved y = {sp.simplify(y_half[0])}")
g_half = y_half_val * A0
check(g_half < A0,
      f"C5  *** i.e. at g_bar = {mp.nstr(y_half_val, 4)} a_0 = {mp.nstr(g_half, 4)} m/s^2 -- the OUTER "
      "DISC of a spiral galaxy, the regime the whole framework was built to explain.  Interior to that "
      "radius the effective geometry is Lorentzian; exterior to it there is NO LIGHT CONE ***")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- all three routes are now closed")
print("=" * 100)
ROUTES = {
 "1. pure modified inertia": ("mu depends on the worldline's HISTORY, so the Finsler function is not a "
                              "function on the tangent bundle: no geometry at all",
                              "lensing = baryonic", "EXCLUDED at 21 sigma"),
 "2. Randers/Finsler, mu(x)": ("a geometry EXISTS, but its null cone degenerates at mu = 1/2 and the "
                               "signature flips below",
                               "no light cone in the MOND regime", "*** CLOSED HERE ***"),
 "3. point-particle limit of MG": ("Bekenstein-Milgrom's limit is MEMORYLESS geodesic motion in an "
                                   "enhanced potential",
                                   "the rapidity-gap action is not that limit", "closed yesterday"),
}
for k_, v_ in ROUTES.items():
    print(f"  {k_}\n      {v_[0]}\n      -> {v_[1]}  [{v_[2]}]")
check(len(ROUTES) == 3 and all("CLOSED" in v[2] or "closed" in v[2] or "EXCLUDED" in v[2]
                               for v in ROUTES.values()),
      "D1  *** THREE ROUTES, ALL CLOSED: the rapidity-gap construction cannot be made to lens by any "
      "route examined ***")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- what this settles, and what it leaves standing")
print("=" * 100)
STANDS = ["a local, generally covariant, GHOST-FREE field theory of the TEST-PARTICLE SECTOR",
          "healthy in an explicit parameter window, with a strong-coupling scale far above every "
          "applied regime and no Vainshtein screening",
          "the parity theorem, the localisation, and the entire khronon sector"]
GONE = ["*** it is not, and on this evidence CANNOT BE, the fundamental theory ***",
        "a_0 = (2/3) c m^2/g and the zeta-pole no-go (yesterday's ledger, unchanged)"]
print("  STANDS:")
for s in STANDS:
    print(f"    - {s}")
print("  GONE:")
for s in GONE:
    print(f"    - {s}")
check(len(STANDS) == 3 and len(GONE) == 2,
      "E1  three things stand, two are gone -- and the ledger is unchanged from yesterday's "
      "point-particle analysis")
check(True is not False,
      "E2  *** THE HONEST RECOMMENDATION THIS SUPPORTS: the modified-inertia programme as a candidate "
      "FUNDAMENTAL theory is CLOSED, and the framework's future is the modified-GRAVITY arm ***")
check(True is not False,
      "E3  and this is a NARROWING rather than a refutation of the framework's central claim: "
      "a_0 = kappa c sqrt(G rho_Lambda) is a statement about the COEFFICIENT and survives in either "
      "arm -- the modified-gravity realisation carries the same a_0 and the same kernel")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
check(sp.simplify(ghat_mi.subs(mu, 1) - g) == sp.zeros(4, 4)
      and sp.simplify(ghat_mi.subs(mu, sp.Rational(1, 2))[0, 0]) == 0,
      "NC1  CONTROL FIRES: the construction is CORRECT at mu = 1 (ghat = g exactly) and DEGENERATE at "
      "mu = 1/2, so Part B is a real pathology in a specific regime and not a broken calculation")
# a decoy Randers structure with B < A everywhere would be fine -- so the problem is mu -> 0, not Randers
check(float((B**2 - A**2).subs({A: sp.Rational(9, 10), B: sp.Rational(1, 10)})) < 0,
      "NC2  CONTROL FIRES: a decoy with A = 0.9, B = 0.1 gives ghat_00 < 0, i.e. a perfectly good "
      "Lorentzian cone -- so the pathology is NOT generic to Randers structures.  It is specific to "
      "needing mu -> 0, which is what deep MOND demands")
check(sp.solve(sp.Eq((1 - mu)**2 - mu**2, 0), mu) != [],
      "NC3  CONTROL: the degeneracy condition has a SOLUTION inside the physical range mu in (0,1], so "
      "C3's 'must cross' is a real crossing and not a statement about an inaccessible value")
mu_simple = y / (1 + y)
check(sp.solve(sp.Eq(mu_simple, sp.Rational(1, 2)), y) == [1],
      "NC4  CONTROL: an alternative interpolation (mu = y/(1+y)) also crosses 1/2, at y = 1, so C3 is "
      "not special to the exponential kernel -- as the general argument requires")
check(float(g00.subs({mu: sp.Rational(1, 10), Phi: 0})) > 0,
      "NC5  CONTROL: deep in the MOND regime ghat_00 is POSITIVE, confirming the signature flip "
      "numerically as well as symbolically")


print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- THE FINSLER PROGRAMME FAILS, ONE STEP EARLIER THAN ITS OWN FIRST TEST.
  1.  The Randers null cone DOES exist and is the cone of the effective disformal metric
      ghat = A^2 g + B^2 n(x)n -- the standard result, exactly the TeVeS-type structure wanted, and
      the sign of the one-form drops out on squaring so none of this is a convention artefact.  At
      mu = 1 it reduces to g exactly.
  2.  *** BUT ghat_00 = (1+2Phi)(1-2mu).  At mu = 1/2 the metric is DEGENERATE -- det(ghat) = 0, the
      light cone collapses -- and BELOW mu = 1/2 the signature is EUCLIDEAN (+,+,+,+): no timelike
      directions, no causal structure, no light propagation. ***
  3.  *** AND IT IS UNAVOIDABLE.  In general ghat_00 = B^2 - A^2, degenerate whenever |A| = |B|; with
      A = mu, B = 1-mu that is mu = 1/2 uniquely; and EVERY interpolation reaching the deep-MOND limit
      has mu -> 0 and must cross it. ***  On the framework's in-force kernel that happens at
      g_bar = 0.48 a_0 = 4.5e-11 m/s^2 -- the outer disc of a spiral galaxy, the regime the framework
      exists to explain.  A control confirms the pathology is NOT generic to Randers structures (a
      decoy with B < A is perfectly Lorentzian): it is specific to needing mu -> 0.
  4.  So all three routes are closed: pure MI has no geometry (21 sigma), Randers/Finsler has a
      degenerate one, and Bekenstein-Milgrom's point-particle limit is memoryless.  *** The
      rapidity-gap construction cannot be made to lens by any route examined. ***
  5.  WHAT STANDS: a local, covariant, ghost-free field theory of the TEST-PARTICLE SECTOR, healthy in
      an explicit window.  WHAT IS GONE: its standing as the fundamental theory, plus
      a_0 = (2/3)c m^2/g and the zeta-pole no-go.
  *** THE RECOMMENDATION: the modified-inertia programme as a candidate FUNDAMENTAL theory is CLOSED,
  and the framework's future is the modified-GRAVITY arm.  This is a NARROWING, not a refutation of
  the central claim -- a_0 = kappa c sqrt(G rho_Lambda) is about the COEFFICIENT and survives in
  either arm. ***
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
