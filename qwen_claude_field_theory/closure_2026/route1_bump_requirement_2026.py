#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route1_bump_requirement_2026.py
===============================
COMPANION TO route1_kernel_squeeze_verdict_2026.py -- the ANALYTIC form of the same question, so
that the variational optimum has an independent check that does not depend on any optimiser.

The slope identity  q = -Int_0^inf P(y) nu'(y) dy  with P < 0 gives  q = Int |P| dnu.  Above
y = e_N, |P| = (3/10) e_N^2 / sqrt(y) EXACTLY and is therefore strictly DECREASING.  So any
excursion above e_N in which nu RISES at y_b and FALLS again at y_f > y_b contributes

        + |P|(y_b) (nu_b - nu_S)  -  |P|(y_f) (nu_b - 1)      >  0,

i.e. a super-Newtonian BUMP is the ONLY structure that can cancel the RAR's negative q.  Its
required height follows in closed form.  Two empirical edges bracket where it may sit:

    y_S  = SPARC's HIGHEST measured acceleration            (nothing above it in the RAR)
    y_N  = g_N(Neptune)/a0                                   (nothing below it escapes EPM)

Between them lies an empirically EMPTY window of ~3 decades in acceleration.
Exit 0 = all checks pass.  Both footings.
"""
from __future__ import annotations
import math, sys
import numpy as np
from scipy.optimize import brentq

FAIL = []; N = [0]
def check(c, l, d=""):
    N[0] += 1; ok = bool(c)
    print(f"  [{'ok' if ok else 'FAIL'}] {l}" + (f"\n         {d}" if d else ""))
    if not ok: FAIL.append(l)
print(__doc__)

GM_SUN, AU = 1.32712440018e20, 1.495978707e11
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
Q2_CEIL = 5.2e-27
GEXT = 2.32e-10
G_BAR_MAX = 78.40310686208548 * 9.3619e-11        # SPARC's highest g_bar, from the verdict script
def pref(a0): return 3.0 * a0 ** 1.5 / (2.0 * math.sqrt(GM_SUN))
def nu_line(y): return math.sqrt(1.0 + 1.0 / y)

print(f"  {'footing':<11}{'e_N':>8}{'y_S (SPARC)':>13}{'y_N (Neptune)':>15}{'|q| RAR':>10}"
      f"{'|q| ceiling':>13}{'must cancel':>13}")
print("  " + "-" * 84)
ROW = {}
for fn, a0 in A0.items():
    et = GEXT / a0
    eN = brentq(lambda x: x * nu_line(x) - et, 1e-9, 1e6)
    yS = G_BAR_MAX / a0
    yN = (GM_SUN / (30.07 * AU) ** 2) / a0
    # |q| of a RAR-tracking kernel, and the piece of it already ABOVE y_S (analytic, nu-1 = 1/2y)
    Pc = 0.3 * eN ** 2
    qtail = Pc * (2.0 / 3.0) * 0.5 * yS ** -1.5     # Int_yS^inf |P| |nu'| dy for nu-1 = 1/(2y)
    qRAR = {"canonical": 0.19760, "alt": 0.17077}[fn]   # a0-line, from the verdict script's PART 1
    qc = Q2_CEIL / pref(a0)
    ROW[fn] = dict(eN=eN, yS=yS, yN=yN, Pc=Pc, qRAR=qRAR, qc=qc, C=qRAR - qc, qtail=qtail)
    print(f"  {fn:<11}{eN:>8.4f}{yS:>13.1f}{yN:>15.3e}{qRAR:>10.5f}{qc:>13.5f}{qRAR-qc:>13.5f}")
    check(qtail < 0.01 * qRAR,
          f"1  {fn:9s} the RAR-tracking kernel's own q is essentially all BELOW y_S, so the bump "
          "region is genuinely free real estate",
          f"|q| above y_S = {qtail:.3e} = {100*qtail/qRAR:.2f}% of the total")

print(f"""
  REQUIRED BUMP HEIGHT, with the FALL COSTED PROPERLY.
  Ellipticity of the AQUAL operator (equivalently strict convexity of the AQUAL functional, the
  corpus's own banked theorem) requires d[y nu(y)]/dy > 0, i.e. nu may DECLINE no faster than 1/y.
  So the fall back to nu = 1 cannot be a step: at best it saturates nu = H y_c / y from some y_c
  out to the ephemeris floor y_N, which forces y_c = y_N / H.  The rise itself is unconstrained
  (increases are always elliptic), so the cheapest structure is

      nu = nu_S  below y_a ;   RISE to H at y_a ;   FLAT at H to y_c = y_N/H ;   nu = H y_c/y to y_N.

  Its net contribution to q, with |P| = (3/10) e_N^2 / sqrt(y) exactly in this whole region, is

      NET(H) = |P|(y_a) (H - nu_S)  -  (2/3) |P|(y_N) (H^(3/2) - 1)          [derived below]

  and the escape needs NET(H) >= C.  The fall term is what an earlier version of this file omitted;
  including it RAISES the requirement, and the direction of that correction is AGAINST the escape.
""")
def net_of(H, Pa, PN, nuS):
    return Pa * (H - nuS) - (2.0 / 3.0) * PN * (H ** 1.5 - 1.0)
# verify the closed form against direct quadrature of Int |P| |dnu| along the saturating fall
for fn, a0 in A0.items():
    r = ROW[fn]; H = 3.0; yN = r["yN"]; yc = yN / H; Pc = r["Pc"]
    yy = np.geomspace(yc, yN, 200001)
    dnu = np.abs(np.diff(H * yc / yy))
    num = float(np.sum((Pc / np.sqrt(np.sqrt(yy[1:] * yy[:-1]))) * dnu))
    ana = (2.0 / 3.0) * (Pc / math.sqrt(yN)) * (H ** 1.5 - 1.0)
    check(abs(num - ana) / ana < 2e-4,
          f"3  {fn:9s} the fall-cost closed form (2/3)|P|(y_N)(H^3/2 - 1) matches direct quadrature "
          "of Int |P| |dnu| along the ellipticity-saturating fall",
          f"numeric {num:.8f} vs analytic {ana:.8f} at H = 3")
print(f"  {'footing':<11}{'y_a (rise)':>12}{'r_sun [AU]':>12}{'|P|(y_a)':>10}"
      f"{'H_min':>9}{'NET_max':>10}{'y_c = y_N/H':>13}{'r_c [AU]':>10}")
BEST = {}
for fn, a0 in A0.items():
    r = ROW[fn]; nuS = nu_line(r["yS"]); PN = r["Pc"] / math.sqrt(r["yN"])
    for ya in (r["yS"] * 1.02, 300.0, 1e3, 3e3, 6e3, 1e4, 2e4):
        Pa = r["Pc"] / math.sqrt(ya)
        # NET(H) is concave with a single maximum at H* = (Pa/PN)^2; the SMALLEST root of
        # NET = C is the minimum admissible bump height.  Bracket on [1, H*] explicitly -- a
        # naive [1, 1e6] bracket has NET < C at BOTH ends and brentq silently returns nothing.
        Hstar = (Pa / PN) ** 2
        NETmax = net_of(Hstar, Pa, PN, nuS)
        if NETmax < r["C"]:
            H = float("inf")     # no bump of ANY height can pay for the cancellation from here
        else:
            H = brentq(lambda h: net_of(h, Pa, PN, nuS) - r["C"], 1.0 + 1e-12, Hstar)
        yc = r["yN"] / H if np.isfinite(H) else float("nan")
        rs = math.sqrt(GM_SUN / (ya * a0)) / AU
        rc = math.sqrt(GM_SUN / (yc * a0)) / AU if np.isfinite(yc) and yc > 0 else float("nan")
        if abs(ya - r["yS"] * 1.02) < 1e-9: BEST[fn] = (H, ya, rs)
        print(f"  {fn:<11}{ya:>12.4g}{rs:>12.1f}{Pa:>10.5f}{H:>9.3f}{NETmax:>10.3f}"
              f"{yc:>13.4g}{rc:>10.1f}")
print(f"""
  THE WINDOW IS CLOSED ON BOTH SIDES.  NET(H) is concave with maximum at H* = (|P|(y_a)/|P|(y_N))^2,
  and NET_max falls as the bump is pushed to higher y_a, so above some y_a NO height whatever pays
  for the cancellation -- the ellipticity-limited fall then costs more than the rise buys.  Solving
  NET_max(y_a) = C gives the upper edge:""")
WIN = {}
for fn, a0 in A0.items():
    r = ROW[fn]; nuS = nu_line(r["yS"]); PN = r["Pc"] / math.sqrt(r["yN"])
    def netmax(ya):
        Pa = r["Pc"] / math.sqrt(ya)
        return net_of((Pa / PN) ** 2, Pa, PN, nuS) - r["C"]
    yhi = brentq(netmax, r["yS"], r["yN"])
    WIN[fn] = yhi
    print(f"  {fn:<11} {r['yS']:.1f} a0 < y < {yhi:.4g} a0   <=>   "
          f"{math.sqrt(GM_SUN/(yhi*a0))/AU:.0f} AU < r_sun < "
          f"{math.sqrt(GM_SUN/(r['yS']*a0))/AU:.0f} AU   <=>   "
          f"{r['yS']*a0:.2e} < g < {yhi*a0:.2e} m/s^2")
    check(r["yS"] < yhi < 1e4,
          f"3  {fn:9s} *** THE ESCAPE WINDOW IS BOUNDED ON BOTH SIDES: below y = {r['yS']:.0f} the "
          f"RAR forbids the bump; above y = {yhi:.4g} no height suffices ***",
          f"width = {math.log10(yhi/r['yS']):.2f} decades in acceleration")

for fn in A0:
    nub, yb, rs = BEST[fn]
    check(nub > 2.0,
          f"4  {fn:9s} *** THE CHEAPEST ESCAPE STILL NEEDS nu = {nub:.2f} -- gravity more than "
          f"DOUBLED -- at y = {yb:.0f} a0 (g = {yb*A0[fn]:.2e} m/s^2, r_sun = {rs:.0f} AU). That is "
          "the BEST case over the whole admissible class: the rise sits hard against SPARC's last "
          "data point (the largest |P| still unconstrained by the RAR) and the fall is the cheapest "
          "one AQUAL ellipticity permits ***",
          f"and the requirement climbs steeply with y_a -- see the table")


# ---------------------------------------------------------------------------------------------
# WHAT ACTUALLY LIVES IN THE WINDOW.  The window is empty OF THE DATA USED IN THIS TEST (SPARC
# stops at y = 78, the ephemerides start at y = 7e4).  It is NOT empty of astrophysics.  These are
# order-of-magnitude placements from M and r only -- no dynamical modelling, no adjudication.  They
# name the measurement that would decide the escape, and they are quoted AGAINST the escape.
PC = 3.0857e16
G_N = 6.674e-11
MSUN = 1.989e30
def y_of(M, r_pc, a0): return G_N * M * MSUN / (r_pc * PC) ** 2 / a0
SYS = [("47 Tuc, half-mass", 1.0e6, 4.0), ("omega Cen, half-mass", 4.0e6, 7.6),
       ("NGC 6397 core", 1.0e5, 0.5), ("M15 core", 5.0e5, 0.2),
       ("MW nuclear star cluster, 1 pc", 1.0e6, 1.0),
       ("MW nuclear disk, 30 pc", 1.0e8, 30.0),
       ("MW inner disk, 1 kpc", 1.0e10, 1000.0),
       ("MW solar circle, 8 kpc", 1.0e11, 8000.0)]
print("\n  WHAT LIVES INSIDE THE ESCAPE WINDOW (order-of-magnitude placement only)")
print(f"  {'system':<32}{'M [Msun]':>10}{'r [pc]':>9}{'y canon':>10}{'y alt':>9}{'in window?':>12}")
nin = 0
for nm, M, r_ in SYS:
    yc = y_of(M, r_, A0["canonical"]); ya = y_of(M, r_, A0["alt"])
    inw = ROW["canonical"]["yS"] < yc < WIN["canonical"]
    nin += int(inw)
    print(f"  {nm:<32}{M:>10.1e}{r_:>9.1f}{yc:>10.1f}{ya:>9.1f}{('YES' if inw else 'no'):>12}")
check(nin >= 3,
      "5  *** THE WINDOW IS NOT EMPTY OF ASTROPHYSICS, only of the data used in THIS test. Dense "
      "globular clusters (y ~ 90-600) and the Milky Way's nuclear star cluster and nuclear disk "
      "(y ~ 165-1500) sit INSIDE it.  Those systems are the standard evidence that dynamics is "
      "Newtonian at those accelerations, and the escape needs gravity there enhanced by 2.2x at "
      "minimum and by ~8x at the height the full variational optimum actually chose.  COMPUTING "
      "THAT IS THE DECIDING TEST AND IT IS NOT DONE HERE ***",
      f"{nin} of {len(SYS)} named systems fall inside {ROW['canonical']['yS']:.0f} < y < "
      f"{WIN['canonical']:.0f}")

print("""
  WHAT THE BUMP WOULD MEAN, stated plainly and NOT as a refutation (no calculation is offered here
  for any of these -- they are named as the tests that would decide it):
    * a SECOND acceleration scale a_1 ~ 100 a_0 ~ 1e-8 m/s^2, with a height, tuned to sit inside
      the observational window.  Two new parameters, neither derived from anything in the
      framework, where the framework's whole claim is that a_0 is not free.
    * gravity ENHANCED by 2.2x AT MINIMUM (and ~8x at the height the full variational search in
      route1_kernel_squeeze_verdict_2026.py actually chose) across 1.5-1.6 decades of acceleration.
      The table above shows what sits there.  Whether globular-cluster and Galactic-centre
      dynamics exclude it was NOT computed here; it is THE deciding test.
    * in the solar system the whole permitted window is r_sun = 145-899 AU -- outside every
      planet, inside the Oort cloud.  Carl's own comet-anisotropy front lives exactly there.
    * mu(x) = 1/nu becomes NON-MONOTONE with mu < 1 at HIGH acceleration.  Ellipticity of the AQUAL
      operator survives (it needs only d(y nu)/dy > 0, which the bump respects), so this is not a
      well-posedness kill -- it is a plausibility cost.
""")
print(f"  checks: {N[0]}, failures: {len(FAIL)}")
for f in FAIL: print("   FAIL:", f)
sys.exit(1 if FAIL else 0)
