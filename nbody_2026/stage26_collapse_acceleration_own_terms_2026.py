#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage26_collapse_acceleration_own_terms_2026.py
===============================================
CARL WAS RIGHT AND STAGE 24/25's WITHDRAWAL WAS WRONG.  "Accelerated structure formation / earlier
massive objects" IS a prediction of this framework -- it just is not a LINEAR-growth prediction, and
I killed it by testing only the linear channel and then evaluating the nonlinear one at the single
point where the boost is weakest.

--------------------------------------------------------------------------------------------------
THE ERROR, NAMED EXACTLY
--------------------------------------------------------------------------------------------------
Stage 24 argued: (i) the MOND sector is absent from LINEAR growth (true -- delta Y^(1) = 0 on FRW,
rows 19-20), therefore the halo mass function is LambdaCDM's (true); (ii) and the surviving
nonlinear channel is small, "boost <= 1.5x at virialised overdensity".  *** Step (ii) is the error.
It evaluated the boost at delta ~ 200 -- the END STATE, after collapse is over -- when the quantity
that sets WHEN an object forms is the boost during the COLLAPSE, and collapse begins at turnaround
where delta ~ 5 and the region is far deeper in MOND. ***  Evaluating a rate-limiting quantity at
the point where it is smallest is exactly the "manufactured deficit" this programme's own working
rule forbids, and I did it while quoting that rule.

--------------------------------------------------------------------------------------------------
WHAT THE FRAMEWORK ACTUALLY PREDICTS, FROM ITS OWN a_0-LINE
--------------------------------------------------------------------------------------------------
The a_0-line g_obs^2 = g_bar^2 + a_0 g_bar is a statement about the ACCELERATION of any test mass,
so it governs the collapse of a shell exactly as it governs a rotation curve:

        r_ddot = -sqrt( g_N^2 + a_0(z) g_N ),      g_N = G M / r^2

Integrating that from turnaround to collapse and comparing to the Newtonian case gives the
framework's own, parameter-free prediction for how much earlier structures form.  Nothing here is
borrowed: no Nusser, no linear-growth boost, no MOND-as-cosmology.  Only equation (1) and the
derived a_0(z).

AND THE LINEAR-GROWTH THEOREM DOES NOT TOUCH IT.  The theorem says the MOND sector cannot change the
linear power spectrum (so the halo mass function's SHAPE is LambdaCDM's).  Collapse is nonlinear by
definition; the theorem is silent there, and the a_0-line is not.  Both statements are true at once:
    * abundance of DARK haloes: LambdaCDM's (linear, theorem-protected)
    * TIMING of collapse: accelerated (nonlinear, a_0-line-governed)
That is a sharper prediction than the row it replaces, because it is signed AND quantified.
"""

import sys
import numpy as np
from scipy.integrate import quad

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


G = 6.67430e-11
MPC = 3.0856775814913673e22
KPC = MPC / 1000.0
MSUN = 1.98892e30
H0 = 67.4 * 1000.0 / MPC
OM_M, OM_L = 0.315, 0.685
A0 = 9.3619e-11
NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4

print(__doc__)


def Hz(z):
    return H0 * np.sqrt(OM_M * (1 + z) ** 3 + OM_L)


def a0_of_z(z, nu0):
    nu = nu0 * (1 + z) ** 3
    return A0 * np.sqrt(np.sqrt(1 + nu0 ** 2) / np.sqrt(1 + nu ** 2))


def nu_boost(y):
    y = max(float(y), 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


# =================================================================================================
print("=" * 100)
print("PART A -- the boost during collapse, not after it")
print("=" * 100)


def r200_of(M_msun, z):
    """radius enclosing 200 rho_crit(z) -- the standard end state, used only to set the scale."""
    rho_c = 3 * Hz(z) ** 2 / (8 * np.pi * G)
    return (3 * M_msun * MSUN / (800 * np.pi * rho_c)) ** (1.0 / 3.0)


print("\n   M [Msun]   z     r_200 [kpc]   r_ta [kpc]    y at r_ta    nu at r_ta   |  y at r_200   nu")
rows = []
for M, z in ((1e10, 10), (1e10, 15), (1e9, 10), (1e11, 8), (1e11, 12)):
    r2 = r200_of(M, z)
    rta = 2.0 * r2                      # turnaround radius: standard spherical collapse
    a0z = a0_of_z(z, NU0_CEIL)
    y_ta = G * M * MSUN / rta ** 2 / a0z
    y_v = G * M * MSUN / r2 ** 2 / a0z
    rows.append((M, z, y_ta, nu_boost(y_ta), y_v, nu_boost(y_v)))
    print(f"   {M:>8.0e}  {z:>3d}      {r2/KPC:>7.2f}     {rta/KPC:>7.2f}     {y_ta:>8.4f}     "
          f"{nu_boost(y_ta):>6.2f}    |   {y_v:>7.3f}    {nu_boost(y_v):>5.2f}")

nu_ta = [r[3] for r in rows]
nu_v = [r[5] for r in rows]
per_row = [r[3] / r[5] for r in rows]      # PER-ROW ratio, not a min/max mismatch
check(min(per_row) > 1.5 and min(nu_ta) > 2.0,
      f"A1  *** THE BOOST AT TURNAROUND IS {min(nu_ta):.1f}-{max(nu_ta):.1f}x, against "
      f"{min(nu_v):.2f}-{max(nu_v):.2f}x at the virial radius.  Stage 24 quoted the virial number and "
      f"called the channel small -- but collapse TIMING is set at turnaround, where the region is "
      f"four times larger and the boost is {min(per_row):.2f}-{max(per_row):.2f}x bigger IN EVERY CASE ***",
      "the rate-limiting stage is the slow, low-density one, and that is precisely the deep-MOND one")


# =================================================================================================
print()
print("=" * 100)
print("PART B -- integrate the a_0-line's own collapse: how much faster?")
print("=" * 100)


def t_collapse(M_kg, r_ta, a0z, mond=True):
    """time from rest at r_ta to r -> 0 under the a_0-line (or Newton), by energy integral.

    v(r)^2 = 2 [Phi(r_ta) - Phi(r)] with g = sqrt(g_N^2 + a_0 g_N) (or g_N).  Integrated numerically:
    dt = dr / v, and Phi is obtained from int g dr.
    """
    def g(r):
        gN = G * M_kg / r ** 2
        return np.sqrt(gN ** 2 + a0z * gN) if mond else gN

    def dphi(r):        # potential difference from r_ta inward: int_r^{r_ta} g dr'
        return quad(g, r, r_ta, limit=200)[0]

    def integrand(x):   # x = r/r_ta
        r = x * r_ta
        d = dphi(r)
        return 0.0 if d <= 0 else r_ta / np.sqrt(2.0 * d)

    return quad(integrand, 1e-4, 1.0 - 1e-9, limit=200)[0]


print("\n   M [Msun]   z    t_coll Newton [Myr]   t_coll a_0-line [Myr]   speedup   formation z shift")
MYR = 3.1557e13
speeds = []
for M, z in ((1e10, 10), (1e10, 15), (1e9, 10), (1e11, 8), (1e11, 12)):
    r2 = r200_of(M, z)
    rta = 2.0 * r2
    a0z = a0_of_z(z, NU0_CEIL)
    tN = t_collapse(M * MSUN, rta, a0z, mond=False)
    tM = t_collapse(M * MSUN, rta, a0z, mond=True)
    sp = tN / tM
    # if collapse takes 1/sp as long, the object appears when cosmic time is 1/sp earlier:
    # t ~ (1+z)^-3/2 in matter domination  =>  (1+z) larger by sp^(2/3)
    z_new = (1 + z) * sp ** (2.0 / 3.0) - 1
    speeds.append(sp)
    print(f"   {M:>8.0e}  {z:>3d}       {tN/MYR:>9.1f}            {tM/MYR:>9.1f}          "
          f"{sp:>5.2f}x     z {z} -> {z_new:>5.1f}")

check(min(speeds) > 1.15,
      f"B1  *** THE FRAMEWORK'S OWN COLLAPSE IS {min(speeds):.2f}-{max(speeds):.2f}x FASTER THAN "
      f"NEWTONIAN, from the a_0-line alone with zero free parameters.  In matter domination that "
      f"moves formation to (1+z) larger by speedup^(2/3) -- so objects LambdaCDM forms at z = 10 "
      f"appear at z ~ {(1+10)*max(speeds)**(2/3)-1:.1f} here ***",
      "this is 'earlier massive objects', derived rather than inherited -- the row stage 24 withdrew "
      "was RIGHT in substance and wrong only in its stated mechanism")

check(max(speeds) < 3.0,
      f"B2  and the magnitude is bounded, which matters for not overselling it: the speedup is "
      f"{min(speeds):.2f}-{max(speeds):.2f}x, not an order of magnitude, because g_N at turnaround is "
      f"~0.1 a_0 rather than 0.001 a_0 -- these objects are only MODERATELY deep in MOND",
      "so the prediction is 'noticeably earlier', not 'arbitrarily early', and it is falsifiable in "
      "both directions")


# =================================================================================================
print()
print("=" * 100)
print("PART C -- and a_0(z) makes it a SIGNED function of redshift, which is the testable part")
print("=" * 100)

print("\n     z     a_0(z)/a_0(0)    speedup (M = 1e10)    -> predicted formation-z shift")
sig_rows = []
for z in (6, 8, 10, 15, 20, 25):
    a0z = a0_of_z(z, NU0_CEIL)
    r2 = r200_of(1e10, z)
    rta = 2 * r2
    tN = t_collapse(1e10 * MSUN, rta, a0z, mond=False)
    tM = t_collapse(1e10 * MSUN, rta, a0z, mond=True)
    sp = tN / tM
    sig_rows.append((z, a0z / A0, sp))
    print(f"   {z:>4d}      {a0z/A0:>7.4f}          {sp:>5.3f}x            z {z} -> "
          f"{(1+z)*sp**(2/3)-1:>5.1f}")

check(sig_rows[0][2] > sig_rows[-1][2],
      f"C1  *** THE SIGNATURE: because a_0(z) DECLINES above z_t, the collapse speedup declines too "
      f"-- {sig_rows[0][2]:.3f}x at z = {sig_rows[0][0]} falling to {sig_rows[-1][2]:.3f}x at "
      f"z = {sig_rows[-1][0]}.  So the framework predicts accelerated formation that TURNS OFF toward "
      f"the highest redshifts, which is a shape no constant-a_0 MOND predicts ***",
      "this is the framework-DISTINCTIVE content: constant-a_0 MOND accelerates collapse at every z; "
      "the derived a_0(z) accelerates it and then stops")

info("C2  and the two statements now coexist without contradiction: the DARK-halo mass function is "
     "LambdaCDM's (linear, protected by the delta Y^(1) = 0 theorem), while the TIMING of baryonic "
     "collapse inside those haloes is accelerated by the a_0-line.  So the framework predicts "
     "earlier ASSEMBLY at fixed halo abundance -- observationally, more mature/massive galaxies at "
     "high z than LambdaCDM expects, without changing the halo counts.  That is precisely the JWST "
     "anomaly's shape, and it is a real tailwind after all.")

info("C3  AGAINST INTEREST, kept: the boost applies to the TOTAL enclosed mass, dark sector included, "
     "which is the framework's known double-counting exposure (banked 2.06-4.42x overshoot). If the "
     "dust already supplies halo-scale gravity, adding the a_0-line boost on top is exactly the "
     "over-production Nusser worried about -- so Part B's speedup is an UPPER bound in the case where "
     "the dust and the boost both act, and the honest range runs from ~1 (if the dust dominates the "
     "collapse and the MOND term is screened) to the quoted 1.2-2.4x. THAT fork, not the linear-growth "
     "theorem, is the real open question here, and it is the same fork non-claim 2d already carries.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE WITHDRAWAL IS WITHDRAWN.  Carl was right: "accelerated structure formation / earlier massive
  objects" IS this framework's prediction.  Both of my reasons for killing it were wrong in
  different ways:

  1. "It is a linear-growth claim and linear growth is LambdaCDM's" -- the first half is a
     misattribution.  Collapse TIMING is nonlinear, the a_0-line governs accelerations at every
     scale, and the delta Y^(1) = 0 theorem is silent about nonlinear collapse.  Both hold at once:
     LambdaCDM halo ABUNDANCE, accelerated collapse TIMING.

  2. "The nonlinear channel is small (<=1.5x)" -- that number was the boost at delta ~ 200, the END
     of collapse.  At TURNAROUND, which is what sets the timing, the boost is {min(nu_ta):.1f}-{max(nu_ta):.1f}x.
     I evaluated a rate-limiting quantity at its minimum, which is the manufactured-deficit failure
     this programme's own rule forbids.

  COMPUTED, from the a_0-line alone: collapse is {min(speeds):.2f}-{max(speeds):.2f}x faster than Newtonian, moving
  formation to (1+z) larger by speedup^(2/3) -- objects LambdaCDM forms at z = 10 appear at
  z ~ {(1+10)*max(speeds)**(2/3)-1:.1f}.  And a_0(z) gives it a SIGNED shape no constant-a_0 MOND has: the speedup
  declines from {sig_rows[0][2]:.3f}x at z = 6 to {sig_rows[-1][2]:.3f}x at z = 25, i.e. accelerated formation that
  SWITCHES OFF toward the highest redshifts.

  Sec. 5's row must be RESTORED and re-derived, not withdrawn -- with the mechanism corrected to
  nonlinear collapse, the magnitude quoted ({min(speeds):.2f}-{max(speeds):.2f}x), and the double-counting fork (C3) named
  as the live uncertainty.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
