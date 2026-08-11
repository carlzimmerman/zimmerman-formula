#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage25_cosmic_dawn_own_terms_2026.py
=====================================
COSMIC DAWN FROM THE FRAMEWORK'S OWN TWO EQUATIONS -- no Nusser, no LambdaCDM growth equation, no
borrowed surface-density threshold, no "does it survive someone else's test".  Stage 24 answered
other people's questions about this framework.  This stage asks what the framework ITSELF predicts,
and derives every number from its own content.

THE ONLY TWO INPUTS, both the framework's own:

  (1) THE a_0-LINE (the framework's own interpolation, not McGaugh's nu, not Milgrom's mu):
          g_obs^2 = g_bar^2 + a_0 g_bar        <=>       g_obs^2 - g_bar^2 = a_0 g_bar

  (2) THE DERIVED a_0(z) (stage 17, from the action -- the MOND scale IS the dark sector's pressure):
          a_0^2(Q) = kappa^2 G (-K(Q)),   K = -M^4 sqrt(1 - mu^2 u^2/M^4),  beta = 1
      =>  a_0(z)/a_0(0) = [ sqrt(1+nu_0^2) / sqrt(1+nu_0^2 (1+z)^6) ]^(1/2),   nu_0 in [2.14e-5, 1.77e-4]

Everything below is those two lines and nothing else.  a_0(0) = kappa c sqrt(G rho_Lambda) with
kappa = 1/2 (FITTED, measured 0.551 +- 0.043 -- never quoted as derived).

--------------------------------------------------------------------------------------------------
WHAT THE FRAMEWORK PREDICTS FOR COSMIC DAWN, IN ITS OWN VARIABLES
--------------------------------------------------------------------------------------------------
Part A derives the BTFR zero point from the a_0-line alone (no fitting, no external relation):
        v^4 = G M_b a_0        is an EXACT consequence of equation (1) in its low-g_bar limit,
so the framework's prediction for any rotation-supported baryonic system at any redshift is
        v(z) / v(0) = [a_0(z)/a_0(0)]^(1/4)     at fixed baryonic mass.
That is a ZERO-PARAMETER prediction curve for cosmic dawn, and Part B computes it.

Part C derives the framework's OWN transition threshold from equation (1) -- Sigma_dagger = a_0/(pi G)
= 214 M_sun/pc^2, which is 2x the number usually quoted, because the usual one comes from a
different interpolation.  Using someone else's threshold on this framework is a category error, and
stage 24 committed it.

Part D states the falsification: where the predicted deviation exceeds the measurement floor, and
therefore at what redshift the framework's a_0 transition becomes a real, scoreable test.
"""

import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 25
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


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# ---- the framework's own constants ---------------------------------------------------------------
C_SI = mp.mpf("2.99792458e8")
G_SI = mp.mpf("6.67430e-11")
MPC = mp.mpf("3.0856775814913673e22")
PC = MPC / 10 ** 6
MSUN = mp.mpf("1.98892e30")
KAPPA = mp.mpf("0.5")                     # FITTED (measured 0.551 +- 0.043), never derived
A0 = mp.mpf("9.3619e-11")                 # = kappa c sqrt(G rho_Lambda), canonical footing
A0_ALT = mp.mpf("1.1279e-10")             # the alt footing, carried per the working rule
NU0_FLOOR, NU0_CEIL = mp.mpf("2.14e-5"), mp.mpf("1.77e-4")

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the BTFR is a THEOREM of the a_0-line, derived here, not imported")
print("=" * 100)

gb, a0s, r, M, v, Gs = sp.symbols("g_bar a_0 r M v G", positive=True)
g_obs = sp.sqrt(gb ** 2 + a0s * gb)                      # THE a_0-LINE, the framework's own
deep = sp.series(g_obs, gb, 0, 1).removeO()              # low-g_bar limit
check(sp.simplify(deep - sp.sqrt(a0s * gb)) == 0,
      "A1  the a_0-line's low-acceleration limit is g_obs = sqrt(a_0 g_bar) EXACTLY -- from the "
      "framework's own interpolation, with no reference to any other kernel",
      "sympy series of sqrt(g_bar^2 + a_0 g_bar)")

# v^2/r = sqrt(a_0 G M / r^2)  =>  v^4 = G M a_0
btfr = sp.solve(sp.Eq(v ** 2 / r, sp.sqrt(a0s * Gs * M / r ** 2)), v)
v_sol = [s for s in btfr if s.is_positive is not False][0]
check(sp.simplify(v_sol ** 4 - Gs * M * a0s) == 0,
      "A2  *** and that gives v^4 = G M_b a_0 EXACTLY: the baryonic Tully-Fisher relation is a "
      "THEOREM of the framework's own a_0-line, r drops out identically, and no free parameter "
      "enters ***",
      "so the framework's high-z prediction is fixed the moment a_0(z) is fixed -- nothing else to "
      "choose")

check(sp.simplify(sp.diff(v_sol, a0s) * a0s / v_sol - sp.Rational(1, 4)) == 0,
      "A3  and the sensitivity is exactly 1/4: d ln v / d ln a_0 = 1/4, so "
      "v(z)/v(0) = [a_0(z)/a_0(0)]^(1/4) at fixed baryonic mass",
      "the framework's cosmic-dawn prediction is the FOURTH ROOT of its own derived a_0(z)")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the prediction curve: the framework's own BTFR zero point through cosmic dawn")
print("=" * 100)


def a0_ratio(z, nu0):
    nu = nu0 * (1 + mp.mpf(z)) ** 3
    return mp.sqrt(mp.sqrt(1 + nu0 ** 2) / mp.sqrt(1 + nu ** 2))


print("\n     z     a_0(z)/a_0(0)          v(z)/v(0) at fixed M_b        deficit in v")
print("            floor    ceil          floor      ceil            floor     ceil")
rows = {}
for z in (2, 5, 8, 10, 12, 15, 20, 25, 30, 40):
    af, ac = a0_ratio(z, NU0_FLOOR), a0_ratio(z, NU0_CEIL)
    vf, vc = af ** mp.mpf("0.25"), ac ** mp.mpf("0.25")
    rows[z] = (vf, vc)
    print(f"   {z:>4d}    {sig(af,4):>7s}  {sig(ac,4):>7s}      {sig(vf,5):>7s}   {sig(vc,5):>7s}      "
          f"{sig(100*(1-vf),3):>6s}%  {sig(100*(1-vc),3):>6s}%")

check(1 - rows[5][1] < mp.mpf("0.001"),
      f"B1  *** THE FRAMEWORK'S SHARP PREDICTION: at fixed baryonic mass, rotation velocities lie on "
      f"TODAY'S BTFR to better than {sig(100*(1-rows[5][1]),2)}% all the way to z = 5, across the "
      f"WHOLE allowed nu_0 window.  Zero free parameters. ***",
      "any measured BTFR zero-point offset below z = 5 larger than ~0.1% in velocity falsifies the "
      "derived law -- this is the sharp null stage 21 identified, now in observable variables")

check(1 - rows[20][1] > mp.mpf("0.05") and 1 - rows[10][1] < mp.mpf("0.02"),
      f"B2  and the TRANSITION SHOWS UP as a velocity DEFICIT at fixed baryonic mass: "
      f"{sig(100*(1-rows[10][1]),3)}% at z = 10, {sig(100*(1-rows[15][1]),3)}% at z = 15, "
      f"{sig(100*(1-rows[20][1]),3)}% at z = 20, {sig(100*(1-rows[30][1]),3)}% at z = 30 (ceiling "
      f"nu_0; the floor is flatter)",
      "the framework predicts high-z rotators are SLOWER than today's BTFR at fixed M_b -- a signed, "
      "parameter-free direction")

info(f"B3  FOOTING NOTE (working rule): the ratio a_0(z)/a_0(0) is footing-INDEPENDENT -- the "
     f"canonical {sig(A0,5)} and alt {sig(A0_ALT,5)} m/s^2 differ only in the z = 0 anchor, which "
     f"cancels in v(z)/v(0).  So Part B's curve is the same on both footings; only the absolute BTFR "
     f"zero point moves, by {sig((A0_ALT/A0)**mp.mpf('0.25'),4)}x in velocity.")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the framework's OWN transition threshold (stage 24 borrowed someone else's)")
print("=" * 100)

# transition where g_bar = a_0; for M inside r: g_bar = GM/r^2, Sigma = M/(pi r^2)
Sig = sp.symbols("Sigma", positive=True)
sol = sp.solve(sp.Eq(Gs * (Sig * sp.pi * r ** 2) / r ** 2, a0s), Sig)[0]
check(sp.simplify(sol - a0s / (sp.pi * Gs)) == 0,
      "C1  from the a_0-line's own transition condition g_bar = a_0, the framework's surface-density "
      "threshold is Sigma_dagger = a_0/(pi G) -- derived from equation (1), not adopted",
      "the usual a_0/(2 pi G) belongs to a different interpolation and should not be applied here")

Sig_dag = A0 / (mp.pi * G_SI)
Sig_dag_msun_pc2 = Sig_dag / (MSUN / PC ** 2)
Sig_borrowed = A0 / (2 * mp.pi * G_SI) / (MSUN / PC ** 2)
check(abs(Sig_dag_msun_pc2 / Sig_borrowed - 2) < mp.mpf("0.01"),
      f"C2  numerically Sigma_dagger = {sig(Sig_dag_msun_pc2,4)} M_sun/pc^2, exactly 2x the "
      f"{sig(Sig_borrowed,4)} stage 24 borrowed -- so stage 24's 'the JWST objects are 11x above "
      f"threshold' becomes {sig(mp.mpf('1177')/Sig_dag_msun_pc2,3)}x above the framework's own "
      f"threshold.  Same conclusion, correct number",
      "the conclusion survives the correction; the number did not, and it was not the framework's")

info(f"C3  and the threshold inherits the derived a_0(z): Sigma_dagger(z) = Sigma_dagger(0) x "
     f"a_0(z)/a_0(0), so at z = 20 it is {sig(Sig_dag_msun_pc2*a0_ratio(20,NU0_CEIL),4)} M_sun/pc^2 "
     f"and at z = 30, {sig(Sig_dag_msun_pc2*a0_ratio(30,NU0_CEIL),4)} -- the framework predicts the "
     f"MOND regime SHRINKS toward high z, so early systems are MORE Newtonian than today's at the "
     f"same surface density.  That is its own statement, not an imported one.")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- what would falsify it, in the framework's own observable")
print("=" * 100)

FLOOR_DEX = mp.mpf("0.06")                # published high-z BTFR systematic floor, in mass
floor_v = (10 ** (FLOOR_DEX / 4) - 1)     # -> velocity, since v^4 ~ M
info(f"D1  the committed high-z BTFR systematic floor is {sig(FLOOR_DEX,2)} dex in baryonic mass, "
     f"which is {sig(100*floor_v,3)}% in velocity (because v^4 ~ M by A2).  So the framework's "
     f"predicted deficit becomes detectable where it exceeds that.")

z_detect = None
for z in range(5, 45):
    d = 1 - a0_ratio(z, NU0_CEIL) ** mp.mpf("0.25")
    if d > floor_v and z_detect is None:
        z_detect = z
check(z_detect is not None and z_detect > 12,
      f"D2  *** THE FRAMEWORK'S OWN COSMIC-DAWN TEST: its predicted BTFR velocity deficit first "
      f"exceeds the measurement floor at z ~ {z_detect} (ceiling nu_0).  Below that the prediction is "
      f"'exactly today's BTFR' and any detected offset kills it; above it, the prediction is a "
      f"specific declining curve that a measurement can trace ***",
      "so cosmic dawn is not a liability for this framework -- it is where its derived a_0(z) becomes "
      "measurable for the first time")

info("D3  AND WHAT IS NOT PREDICTED, stated so nothing is oversold: this stage says nothing about "
     "the ABUNDANCE of early objects.  The framework's own theorem (stages 18/22: Y = 0 on FRW, "
     "delta Y^(1) = 0, the promoted term starting at third order) removes the MOND sector from linear "
     "growth entirely, so the halo mass function is the dark sector's and is LambdaCDM-like.  The "
     "framework predicts the KINEMATICS of early rotators, not how many there are -- and THE_COMPLETION "
     "Sec. 5's 'accelerated structure formation / earlier massive objects' row claims the latter, "
     "which its own field theory does not deliver.  That row is still owed a withdrawal (v9).")

info("D4  the honest testability status: the prediction of Part B is sharp and parameter-free, but "
     "the objects that would test it at z > 12 are rotation-supported systems with resolved "
     "kinematics AND baryonic-mass measurements at cosmic dawn.  ALMA [CII] and JWST are reaching "
     "z ~ 4-7 rotators now; z > 12 kinematics do not exist yet.  So this is a pre-registered forecast "
     "for the 2030s, not a test available today -- and it should be filed as such rather than "
     "quoted as support.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  COSMIC DAWN, FROM THE FRAMEWORK'S OWN TWO EQUATIONS:

  1. The BTFR v^4 = G M_b a_0 is a THEOREM of the a_0-line (Part A, sympy) -- not an imported
     relation.  Its sensitivity to a_0 is exactly 1/4.

  2. So the derived a_0(z) makes a ZERO-PARAMETER prediction for every rotation-supported system:
     v(z)/v(0) = [a_0(z)/a_0(0)]^(1/4) at fixed baryonic mass.  Numerically, high-z rotators sit on
     TODAY'S BTFR to better than {sig(100*(1-rows[5][1]),2)}% out to z = 5, then fall away:
     {sig(100*(1-rows[10][1]),3)}% at z = 10, {sig(100*(1-rows[15][1]),3)}% at z = 15, {sig(100*(1-rows[20][1]),3)}% at z = 20, {sig(100*(1-rows[30][1]),3)}% at z = 30.
     Footing-independent (the anchor cancels in the ratio).

  3. The framework's OWN threshold is Sigma_dagger = a_0/(pi G) = {sig(Sig_dag_msun_pc2,4)} M_sun/pc^2, exactly
     twice the value stage 24 borrowed from a different interpolation -- and it SHRINKS toward high
     z with a_0, so the framework says early systems are MORE Newtonian, not less.

  4. THE TEST: the predicted deficit clears the {sig(100*floor_v,3)}% velocity floor at z ~ {z_detect}.  Below z = 5 the
     prediction is "exactly today's BTFR" and any robust offset kills it; above z ~ {z_detect} it is a
     specific curve to trace.  Cosmic dawn is where this framework's derived a_0(z) becomes
     MEASURABLE -- the opposite of the liability it was filed as.

  5. NOT predicted, and still owed: the ABUNDANCE of early objects.  Sec. 5's row claims it; the
     framework's own linear-growth theorem forbids it.  Withdrawal owed in v9.
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
