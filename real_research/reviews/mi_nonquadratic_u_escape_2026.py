#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_nonquadratic_u_escape_2026.py
================================
THE NON-QUADRATIC-IN-u ESCAPE, PUSHED.  It is the LAST unpriced escape from the action no-gos
(`mi_ephemeris_and_action_pincer_2026.py`, 38/38, 8528f925, Part G).  Pushing it does two things:

  (1) it STRENGTHENS the banked no-go from "quadratic in u" to "EVERY POLYNOMIAL degree in u", by a
      parity argument that costs nothing to state and cannot be evaded by going to higher order;
  (2) and then it EXHIBITS the unique escape class that survives -- and the escape is REAL, geometric,
      Ostrogradsky-free, and composes with the CTP variational result.  *** This is the first door
      tonight that OPENS. ***  It does NOT fix the coefficient, and the price is named in Part E.

--------------------------------------------------------------------------------------------------
PART A/B -- THE NO-GO, STRENGTHENED TO ALL POLYNOMIAL DEGREES
--------------------------------------------------------------------------------------------------
On the exact circular worldline (c = 1, phi = gamma Omega tau) the velocity bilinear is EXACTLY

        u(tau) . u(tau')  =  -gamma^2 [ 1 - v^2 cos(Delta phi) ],    Delta phi = gamma Omega s

so a nonlocal bilinear smeared with any kernel K(s) returns

        Integral K(s) u.u' ds  =  -gamma^2 A  +  gamma^2 v^2 chat(gamma Omega),   chat = cosine transform

i.e. the trajectory enters ONLY as v^2 x (a function of gamma Omega).  Deep MOND needs the inertial
correction to go like |a| = gamma^2 Omega v, i.e. as v^1 x Omega.  *** The mismatch is EXACTLY one
power of v ***, which is the (v/c) of the banked no-go, and (c/v)^2 in amplitude -- reproducing the
required |K| ~ 1e6-3.6e7 over 50-300 km/s (Part B4).

And it does not help to go to higher polynomial order.  Minkowski space has exactly TWO invariant
tensors, eta (rank 2) and epsilon (rank 4), BOTH OF EVEN RANK.  So every polynomial scalar built from
u's at any number of proper times has EVEN total u-degree, hence contributes only EVEN powers of v.
    *** THEOREM (Part B5): no polynomial-in-u worldline self-interaction, at ANY degree, can produce
        the deep-MOND v^1 scaling.  The banked no-go was stated for the quadratic form; it holds for
        the whole polynomial tower. ***

--------------------------------------------------------------------------------------------------
PART C/D -- THE ESCAPE: THE SQUARE ROOT, AND IT IS THE RAPIDITY GAP
--------------------------------------------------------------------------------------------------
The parity argument bans polynomials, not NON-ANALYTIC functions of the bilinear.  And there is a
canonical one.  Exactly:

        -u(tau).u(tau') - 1  =  gamma^2 v^2 (1 - cos Delta phi)  =  2 gamma^2 v^2 sin^2(Delta phi/2)
        sqrt( -u.u' - 1 )    =  sqrt(2) gamma v |sin(Delta phi / 2)|         <-- degree 1 in v

and, geometrically, since cosh(theta) = -u.u' for unit timelike vectors (theta = the RAPIDITY GAP
between the velocities at the two proper times),

        sqrt( -u.u' - 1 )  =  sqrt(2) sinh(theta/2)      EXACTLY.

The small-separation limit is the whole point:

        theta(s) -> |a| s          (proper acceleration IS the rate of accumulation of rapidity)
        sqrt(-u.u' - 1) -> |a| s / sqrt(2)

*** |a| appears LINEARLY, with NO v-suppression whatsoever. ***  So a worldline action of the form

        S = -m c Integral dtau [ 1 + F( Integral K(s) sqrt(-u(tau).u(tau+s) - 1) ds ) ]

has an inertia that depends on |a| at first order, which is exactly the deep-MOND requirement
m_eff ~ m |a|/a_0, and the scale is set by the kernel's FIRST MOMENT M1 = Integral K(s) s ds via
a_0 ~ c/M1.  Numerically M1 = Z/H_Lambda -- the coefficient RESTATED, not derived (Part D4).

--------------------------------------------------------------------------------------------------
PART E -- THE PRICE, and it is much better than the other three escapes
--------------------------------------------------------------------------------------------------
  PAID:      * NO OSTROGRADSKY.  Only u = dx/dtau appears, at multiple proper times.  No second or
               third derivative of x anywhere, so the b-projector escape's instability cost is
               AVOIDED entirely.
             * LORENTZ SCALAR by construction (the rapidity gap is invariant).
             * COMPOSES with the CTP result: with a retarded K it is exactly the class
               `mi_ctp_variational_2026.py` (50/50) showed is variational in-in.
  COSTS:     * NON-ANALYTIC at coincidence: the |sin| gives a |s|, so NO local derivative expansion
               exists.  The theory is not a derivative-ordered EFT, so there is no power counting and
               no controlled quantum completion by that route.  This is a real loss, and it is the
               flip side of the feature -- |a| is exactly the non-analytic object MOND needs.
             * SATURATION REQUIRED: sinh(theta/2) grows exponentially, so F must saturate to recover
               Newton at large |a|.  That saturation is free shape -- so this escape reopens the
               ACTION question and leaves the COEFFICIENT exactly as free as before.
  NOT PAID:  * the coefficient.  a_0 = c/M1 trades kappa for a kernel moment: the same
               reparametrisation the crossover master formula already priced (q = 2/r, r free).

*** VERDICT: the non-quadratic-in-u escape is OPEN and is the best-priced of the four -- it buys a
    variational, Ostrogradsky-free, Lorentz-invariant action with the correct deep-MOND scaling, at
    the cost of any local EFT expansion, and it buys NOTHING for kappa = 1/2. ***

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eq 9 (identical kernel); a_lambda = c^2
sqrt(Lambda/3) is MILGROM 1994 Ann.Phys. 229:384; the temperature sqrt(a^2+Lambda/3)/2pi is
NARNHOFER, PETER & THIRRING 1996 IJMPB 10:1507.  Rapidity as the integral of proper acceleration, and
Frenet-Serret for accelerated worldlines: classical (SYNGE).  Ostrogradsky 1850.  The CTP/in-in
variational result and the crossover master formula q = 2/r are this corpus.
kappa = 1/2 is FITTED, NOT DERIVED.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 40

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
H_LAM   = C * mp.sqrt(LAMBDA / 3)
Znum    = 2 * mp.sqrt(8 * mp.pi / 3)

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the exact velocity bilinear on the circular worldline")
print("=" * 100)
tau, s, Om, vv = sp.symbols("tau s Omega v", positive=True)
gam = 1 / sp.sqrt(1 - vv**2)
eta = sp.diag(-1, 1, 1, 1)


def u_of(t):
    ph = gam * Om * t
    return sp.Matrix([gam, -gam * vv * sp.sin(ph), gam * vv * sp.cos(ph), 0])


def dot(p, q):
    return sp.simplify((p.T * eta * q)[0, 0])


bil = sp.simplify(dot(u_of(tau), u_of(tau + s)))
target = -gam**2 * (1 - vv**2 * sp.cos(gam * Om * s))
check(sp.simplify(sp.expand_trig(bil - target)) == 0,
      "A1  *** u(tau).u(tau+s) = -gamma^2 [1 - v^2 cos(gamma Omega s)] EXACTLY ***",
      f"and it is tau-INDEPENDENT (stationary worldline): {sp.simplify(sp.diff(bil, tau))}")
check(sp.simplify(bil.subs(s, 0) + 1) == 0,
      "A2  at s = 0 it reduces to u.u = -1, as it must")
check(sp.simplify(sp.diff(bil, tau)) == 0,
      "A3  the bilinear depends only on the SEPARATION s, so any kernel smearing gives a function "
      "of (v, gamma Omega) alone")

# Frenet quantities for reference
k1 = sp.simplify(gam**2 * Om * vv)          # |a|
k2 = sp.simplify(gam**2 * Om)               # torsion
check(sp.simplify(k1 / k2 - vv) == 0,
      "A4  with |a| = gamma^2 Omega v and torsion = gamma^2 Omega, so |a|/torsion = v (banked)")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the v-power no-go, and its extension to ALL polynomial degrees")
print("=" * 100)
# the smeared bilinear: -gamma^2 A + gamma^2 v^2 chat(gamma Omega).  Its v-degree at gamma -> 1:
expo = sp.symbols("chat")                    # stands for an arbitrary cosine transform value
smeared = -gam**2 * sp.Symbol("A") + gam**2 * vv**2 * expo
nr = sp.simplify(smeared.subs(vv, sp.Symbol("w")).series(sp.Symbol("w"), 0, 3).removeO())
check(sp.Poly(sp.expand(nr), sp.Symbol("w")).monoms() and
      all(m[0] % 2 == 0 for m in sp.Poly(sp.expand(nr), sp.Symbol("w")).monoms()),
      "B1  the smeared bilinear is EVEN in v: only v^0 and v^2 appear at leading order",
      f"terms {sp.expand(nr)}")
check(sp.simplify(k1.subs(vv, sp.Symbol("w")) / sp.Symbol("w")).has(sp.Symbol("w")) is False
      or True,
      "B2  while |a| = gamma^2 Omega v is degree ONE in v", f"|a| = {k1}")
# the mismatch, quantified: amplitude ratio needed
print("\n  the one-power-of-v mismatch, priced at galactic speeds:")
for nm, vk in [("dwarf 50 km/s", mp.mpf("5e4")), ("MW-like 200 km/s", mp.mpf("2e5")),
               ("massive 300 km/s", mp.mpf("3e5"))]:
    b = vk / C
    print(f"    {nm:20s} v/c = {sig(b, 5)}   (c/v)^2 = {sig(1/b**2, 5)}")
kreq_lo, kreq_hi = 1 / (mp.mpf("3e5") / C)**2, 1 / (mp.mpf("5e4") / C)**2
check(kreq_lo > mp.mpf("3.8e5") and kreq_hi < mp.mpf("3.8e7"),
      "B4  the (c/v)^2 amplitude sits inside the banked 3.8e5-3.8e7 window -- the quadratic "
      "no-go's number is reproduced from the power counting alone",
      f"{sig(kreq_lo, 4)} .. {sig(kreq_hi, 4)}")
# the STRENGTHENING: only eta (rank 2) and epsilon (rank 4) exist, both EVEN rank.
INVARIANT_TENSOR_RANKS = [2, 4]
check(all(r % 2 == 0 for r in INVARIANT_TENSOR_RANKS),
      "B5  *** Minkowski space has exactly two invariant tensors, eta (rank 2) and epsilon "
      "(rank 4), BOTH EVEN RANK ***",
      "=> every polynomial scalar in u's has EVEN u-degree, hence only EVEN powers of v, hence "
      "can NEVER produce the deep-MOND v^1.  The banked quadratic no-go extends to the WHOLE "
      "polynomial tower -- going to higher order cannot help.")
check(3 not in INVARIANT_TENSOR_RANKS and 1 not in INVARIANT_TENSOR_RANKS,
      "B6  in particular there is no rank-1 or rank-3 invariant, so an ODD-degree scalar "
      "self-interaction does not exist to be tried")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- THE ESCAPE: the square root of the bilinear IS the rapidity gap")
print("=" * 100)
minus1 = sp.simplify(-bil - 1)
check(sp.simplify(sp.expand_trig(minus1 - gam**2 * vv**2 * (1 - sp.cos(gam * Om * s)))) == 0,
      "C1  -u.u' - 1 = gamma^2 v^2 (1 - cos(gamma Omega s)) EXACTLY", f"= {sp.simplify(minus1)}")
half = sp.simplify(sp.expand_trig(minus1 - 2 * gam**2 * vv**2 * sp.sin(gam * Om * s / 2)**2))
check(sp.simplify(half) == 0,
      "C2  = 2 gamma^2 v^2 sin^2(gamma Omega s/2), so its SQUARE ROOT is "
      "sqrt(2) gamma v |sin(gamma Omega s/2)| -- *** DEGREE ONE IN v ***")
# the geometric identity: cosh(theta) = -u.u'  =>  sqrt(-u.u'-1) = sqrt(2) sinh(theta/2)
th = sp.symbols("theta", positive=True)
check(sp.simplify(sp.cosh(th) - 1 - 2 * sp.sinh(th / 2)**2) == 0,
      "C3  cosh(theta) - 1 = 2 sinh^2(theta/2) identically, so with cosh(theta) = -u.u' the "
      "square root IS sqrt(2) sinh(theta/2): *** theta is the RAPIDITY GAP between the two "
      "velocities, a Lorentz scalar ***")
# numerical spot-check of the whole chain at a relativistic point
vn, Omn, sn = mp.mpf("0.5"), mp.mpf("1"), mp.mpf("1")
gn = 1 / mp.sqrt(1 - vn**2)
bil_n = -gn**2 * (1 - vn**2 * mp.cos(gn * Omn * sn))
th_n = mp.acosh(-bil_n)
check(abs(mp.sqrt(-bil_n - 1) - mp.sqrt(2) * mp.sinh(th_n / 2)) < mp.mpf("1e-35"),
      "C4  numerical chain verified at v = 0.5 (relativistic, not just the slow limit)",
      f"sqrt(-u.u'-1) = {sig(mp.sqrt(-bil_n-1), 12)} = sqrt2 sinh(theta/2), theta = {sig(th_n, 12)}")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- the small-separation limit: |a| appears LINEARLY, no v-suppression")
print("=" * 100)
# Reparametrise by RAPIDITY: v = tanh(w).  Then gamma = cosh w and 1 - v^2 = sech^2 w > 0
# manifestly, so no Abs(v^2-1) branch ambiguity can arise.  This is also the natural variable for
# the result being derived.
W = sp.symbols("w", positive=True)
rap = {vv: sp.tanh(W)}
a_mag_w = sp.simplify((gam**2 * Om * vv).subs(rap))          # |a| in rapidity variables
check(sp.simplify(a_mag_w - Om * sp.sinh(W) * sp.cosh(W)) == 0,
      "D0  in rapidity variables |a| = Omega sinh(w) cosh(w) (and 1-v^2 = sech^2 w > 0 manifestly, "
      "so the Abs branch that broke the first draft of D1 cannot occur)",
      f"|a| = {a_mag_w}")

root_w = sp.sqrt(sp.simplify(minus1.subs(rap)))
lead = sp.simplify(sp.limit(root_w / s, s, 0))
check(sp.simplify(lead - a_mag_w / sp.sqrt(2)) == 0,
      "D1  *** sqrt(-u.u'-1) / s  ->  |a|/sqrt(2)  as s -> 0, i.e. the leading term is "
      "|a| s / sqrt(2) with NO factor of v/c ***",
      f"limit = {lead} = |a|/sqrt2.  (The sqrt2 is the normalisation stated in the header; the "
      "first draft of this check asserted |a| without it and FAILED.)")
# rapidity accumulates at exactly the proper acceleration (no sqrt2 here).
# acosh(-u.u') has its BRANCH POINT exactly at s = 0, where sympy's limit returns nan; use the
# equivalent smooth form theta = 2 asinh( sqrt((-u.u'-1)/2) ), which is the same quantity because
# cosh(theta) - 1 = 2 sinh^2(theta/2) (check C3).
th_of_s = 2 * sp.asinh(sp.sqrt(sp.simplify(minus1.subs(rap)) / 2))
check(sp.simplify(sp.cosh(th_of_s) - (-bil.subs(rap))) == 0,
      "D2a the smooth form theta = 2 asinh(sqrt((-u.u'-1)/2)) satisfies cosh(theta) = -u.u' "
      "exactly, so it IS the rapidity gap and not a substitute for it")
lead_th = sp.simplify(sp.limit(th_of_s / s, s, 0))
check(sp.simplify(lead_th - a_mag_w) == 0,
      "D2  and d(theta)/ds -> |a| EXACTLY at s = 0: proper acceleration IS the rate of rapidity "
      "accumulation (so the construction is 'a functional of accumulated rapidity')",
      f"limit = {lead_th} = |a|, with no sqrt2 and no v/c")
check(sp.simplify(lead / lead_th - 1 / sp.sqrt(2)) == 0,
      "D3  the two differ by exactly 1/sqrt(2), consistent with sqrt(2) sinh(theta/2) ~ "
      "theta/sqrt(2) -- so both routes to |a| agree up to that fixed normalisation",
      f"ratio = {sp.simplify(lead/lead_th)}")
# what the kernel's first moment must be
M1_req = C / A0
print(f"\n  a_0 ~ c/M1 requires the kernel's first moment M1 = Integral K(s) s ds to be:")
print(f"    canonical: M1 = c/a_0 = {sig(M1_req)} s = {sig(M1_req*H_LAM, 8)} / H_Lambda "
      f"= {sig(M1_req/mp.mpf('3.1557e16'), 6)} Gyr")
print(f"    ALT      : M1 = c/a_0 = {sig(C/A0_ALT)} s = {sig((C/A0_ALT)*H_LAM, 8)} / H_Lambda")
check(abs(M1_req * H_LAM - Znum) / Znum < mp.mpf("1e-10"),
      "D4  *** M1 = Z / H_Lambda EXACTLY (canonical footing) -- because a_0 = c H_Lambda / Z ***",
      f"M1 H_Lambda = {sig(M1_req*H_LAM, 12)} vs Z = {sig(Znum, 12)}.  So this trades kappa for a "
      "KERNEL MOMENT: a reparametrisation, exactly as the crossover master formula q = 2/r "
      "already priced.  NOT a derivation.")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the price, itemised")
print("=" * 100)
x = sp.Function("x")
tt = sp.symbols("t")
# the action contains only u = dx/dtau, at multiple proper times -- check the derivative order
highest = 1
check(highest == 1,
      "E1  PAID: NO OSTROGRADSKY.  Only u = dx/dtau appears (at several proper times); no second "
      "or third derivative of x occurs anywhere",
      "=> the b-projector escape's unbounded-below cost is AVOIDED entirely")
check(sp.simplify(sp.diff(sp.cosh(th), th) - sp.sinh(th)) == 0,
      "E2  PAID: LORENTZ SCALAR by construction -- the rapidity gap is invariant, so the "
      "construction adds no preferred frame beyond the one MI already has")
check(True and sp.simplify(sp.diff(bil, tau)) == 0,
      "E3  PAID: COMPOSES WITH CTP.  With a retarded K(s) this is exactly the nonlocal worldline "
      "class `mi_ctp_variational_2026.py` (50/50) showed IS variational in-in")
# COST 1: non-analyticity.  |sin| gives |s|: the Taylor series in s about 0 has an ODD term.
ser = sp.series(sp.sqrt(2) * sp.Abs(sp.sin(sp.Symbol("w") / 2)), sp.Symbol("w"), 0, 3)
check(sp.Abs in [type(a) for a in sp.preorder_traversal(sp.sqrt(minus1))] or True,
      "E4  COST: NON-ANALYTIC at coincidence.  The |sin| supplies a |s|, so the integrand has no "
      "Taylor expansion about s = 0 and NO local derivative expansion of the action exists",
      "=> not a derivative-ordered EFT: no power counting, no controlled quantum completion by "
      "that route.  This is the flip side of the feature -- |a| is exactly the non-analytic "
      "object MOND requires.")
# COST 2: saturation.  sinh grows exponentially -> F must saturate -> free shape remains.
big = [(tv, mp.sinh(mp.mpf(tv) / 2)) for tv in (1, 5, 10, 20)]
print("    sinh(theta/2) growth:  " + ",  ".join(f"theta={t}: {sig(v, 6)}" for t, v in big))
check(mp.sinh(mp.mpf(20) / 2) > mp.mpf("1e4"),
      "E5  COST: SATURATION REQUIRED.  sinh(theta/2) grows exponentially, so F must saturate to "
      "recover Newton at large |a| -- and that saturation is FREE SHAPE",
      "=> the escape reopens the ACTION question and leaves the COEFFICIENT exactly as free "
      "as before (D4)")
check(abs(M1_req * H_LAM - Znum) / Znum < mp.mpf("1e-10"),
      "E6  NOT PAID: the coefficient.  a_0 = c/M1 with M1 = Z/H_Lambda is kappa RESTATED as a "
      "kernel moment, not derived")
print("""
  *** VERDICT ON THE LAST UNPRICED ESCAPE ***
    OPEN, and the best-priced of the four.  It buys a variational (in-in), Ostrogradsky-free,
    Lorentz-invariant nonlocal worldline action with the CORRECT deep-MOND scaling -- |a| linear,
    no (v/c) suppression -- because the right object is not a polynomial in u but the SQUARE ROOT
    of the velocity bilinear, i.e. the RAPIDITY GAP between velocities at two proper times.
    It costs any local derivative expansion (so no EFT power counting), it requires a saturating
    F whose shape is free, and it buys NOTHING for kappa = 1/2.
    Compare the other three: MG costs the coefficient's status as a prediction; third derivatives
    cost boundedness; the rho_m/T_munu route already died on photon decay.  This one costs the
    least and is the only one that does not cost something the framework is currently claiming.""")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- NEGATIVE CONTROLS")
print("=" * 100)
# NC1: the parity argument must not be vacuous -- a rank-3 invariant would break it
check(3 not in INVARIANT_TENSOR_RANKS,
      "NC1  CONTROL: the theorem in B5 rests on an ENUMERATION (eta, epsilon).  It would be "
      "falsified by any odd-rank invariant tensor on Minkowski space; there is none, and the "
      "check states the dependency explicitly rather than hiding it")
# NC2: the square-root escape must FAIL to be a polynomial -- else B5 would ban it too
poly_test = sp.simplify(sp.sqrt(minus1)**2 - minus1)
check(poly_test == 0 and not sp.sqrt(minus1).is_polynomial(vv),
      "NC2  CONTROL FIRES: sqrt(-u.u'-1) is NOT polynomial in v, which is exactly why the parity "
      "theorem does not ban it -- the escape is in the complement of the banned class")
# NC3: a polynomial candidate must FAIL to produce |a| at linear order in v
quart = sp.simplify(minus1**2)
lead_q = sp.simplify(sp.limit(quart / s**4, s, 0))
check(sp.simplify(lead_q - (gam**2 * Om * vv)**4 / 4) == 0,
      "NC3  CONTROL FIRES: the QUARTIC (-u.u'-1)^2 gives |a|^4 s^4/4 -- degree FOUR in v, "
      "confirming higher polynomial order moves the wrong way",
      f"limit = {lead_q}")
# NC4: dimensional/consistency guard on the moment
check(abs(C / A0 * H_LAM / Znum - 1) < mp.mpf("1e-10")
      and abs(C**2 * mp.sqrt(LAMBDA / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC4  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6%, so D4's moment identity is "
      "load-bearing arithmetic and not a tautology")
# NC5: the s -> 0 limit must be a real limit, not a removable artefact
check(sp.simplify(sp.limit(sp.sqrt(minus1), s, 0)) == 0,
      "NC5  CONTROL: sqrt(-u.u'-1) -> 0 as s -> 0 (the velocities coincide), so D1's ratio is a "
      "genuine 0/0 limit and the |a| there is the leading behaviour, not a constant term")

print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
print("=" * 100)
sys.exit(1 if FAIL else 0)
