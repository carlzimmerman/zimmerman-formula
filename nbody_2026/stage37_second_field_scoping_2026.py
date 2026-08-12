#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage37_second_field_scoping_2026.py
====================================
THE SECOND FIELD, SCOPED FROM THE DATA -- one coupling class killed outright, one genuine opening
identified, and the price named.  This is a SPECIFICATION, not a built mechanism, and it says so.

--------------------------------------------------------------------------------------------------
WHY A SECOND FIELD IS THE ONLY ROUTE LEFT
--------------------------------------------------------------------------------------------------
Stage 36 closed the a_0-bump on a derivation: the action's A B(Y/Acal)(Q-Q_0)^2 term generates a MASS
coefficient carrying B (excluded by stage 33's theorem) and a GRADIENT coefficient carrying B' (wrong
sign, wrong radial direction, and B'(0) = 1 breaks the BTFR theorem).  The profile that WOULD generate
the working mechanism, C' = -B, has C(0) = -1 and so makes the bump's own kinetic addition 2AC
negative -- a ghost.

*** But that ghost constraint is specific to a term ADDED TO THE EXISTING SECTOR, where the kinetic
addition must not spoil the khronon's.  A SECOND FIELD carries its OWN kinetic term, so 2AC is not
the relevant condition.  That is the structural opening, and it is the same escape stage 9 left for
the galaxy problem. ***

--------------------------------------------------------------------------------------------------
WHAT THE DATA REQUIRE OF IT -- AND THE COUPLING CLASS THAT IS NOW DEAD
--------------------------------------------------------------------------------------------------
Extracting the required effective density directly, rho_req = (1/4pi r^2) dM_req/dr with
M_req = M_obs - M_a0line, across 12 X-COP clusters:

        rho_req ~ rho_gas^n     with   n = 1.745 +- 0.124,   n > 1 in 12/12

Superlinear.  That looks like an invitation to a LOCAL density coupling -- and it is a trap, which is
the main result of this stage:

        cluster gas at R500 (measured here):   2.96e-25 kg/m^3
        galaxy disk gas (n_H = 0.1-10 cm^-3):  1.7e-22 to 1.7e-20 kg/m^3  =  565x to 5.7e4 x DENSER
   =>   a local rho_gas^1.745 law is 6e4 to 2e8 times STRONGER in a galaxy than in a cluster

*** So the n = 1.745 slope is a WITHIN-cluster radial statement and NOT a usable coupling law.  Any
second field that couples to LOCAL BARYON DENSITY superlinearly is excluded by 4 to 8 orders of
magnitude, in the direction that destroys galaxies. ***

--------------------------------------------------------------------------------------------------
WHAT IS LEFT, AND WHAT IT COSTS
--------------------------------------------------------------------------------------------------
The discriminant must be LARGER in clusters than in galaxies.  Of the candidates the corpus has
tabulated, only the JOINT one works: clusters are unique in being simultaneously DEEP
(|Phi|/c^2 = 2.2e-5 vs 9e-7) and AT the transition (g ~ a_0).  Potential depth alone fails against the
cosmic web (1e-5, only 2.2x below clusters); acceleration alone fails against galaxies (which sit
HIGHER, 0.83 a_0 vs 0.45).  So the second field must carry the same joint selection the corpus
already identified -- with its own kinetic term supplying the health the bump could not.

THE PRICE, stated rather than buried: a new field with its own kinetic term, potential and coupling is
a MINIMUM of two new parameters and one new function.  The dark sector goes from FOUR numbers to six
or more, and Sec. 3's "four against LambdaCDM's two" becomes "six or more against two".  That is the
framework's own strongest structural argument being spent to buy clusters.
"""

import glob
import json
import os
import sys

import numpy as np

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
MSUN = 1.98892e30
MPC = 3.0856775814913673e22
MH = 1.6735e-27
A0 = 9.3619e-11
PHI_CL, PHI_GAL, PHI_WEB = 2.2e-5, 9.0e-7, 1.0e-5      # committed five-environment potentials
G_CL, G_GAL, G_WEB = 0.45, 0.83, 3.0e-3                # committed g/a_0

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "xcop")
from astropy.io import fits
R500 = json.load(open(os.path.join(DATA, "xcop_r500_ettori2019.json")))

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- extract the required density law from 12 real clusters")
print("=" * 100)

slopes, rho_cl = [], []
for f in sorted(glob.glob(os.path.join(DATA, "*", "*_fgas_profile.fits"))):
    n = os.path.basename(os.path.dirname(f))
    if n not in R500:
        continue
    d = fits.open(f)[1].data
    r5 = R500[n]["R500"]
    x = np.asarray(d["RADIUS"], float)
    r = x * r5 * MPC
    mt = np.asarray(d["M_NFW"], float) * MSUN
    mg = np.asarray(d["MGAS"], float) * 1.015 * MSUN
    o = np.argsort(r)
    r, mt, mg, x = r[o], mt[o], mg[o], x[o]
    gb = G * mg / r ** 2
    mk = np.sqrt(gb ** 2 + A0 * gb) * r ** 2 / G
    rr = np.gradient(mt - mk, r) / (4 * np.pi * r ** 2)
    rg = np.gradient(mg, r) / (4 * np.pi * r ** 2)
    ok = (rr > 0) & (rg > 0) & np.isfinite(rr) & np.isfinite(rg) & (x > 0.15) & (x < 1.5)
    if ok.sum() >= 8:
        slopes.append(float(np.polyfit(np.log10(rg[ok]), np.log10(rr[ok]), 1)[0]))
    okg = (rg > 0) & np.isfinite(rg)
    if x[okg].min() <= 1.0 <= x[okg].max():
        rho_cl.append(float(np.interp(1.0, x[okg], rg[okg])))

slopes = np.array(slopes)
RHO_CL = float(np.median(rho_cl))
sem = slopes.std(ddof=1) / np.sqrt(len(slopes))
check(slopes.mean() > 1.0 and int((slopes > 1).sum()) == len(slopes),
      f"A1  the required effective density is SUPERLINEAR in gas density: "
      f"n = {slopes.mean():+.3f} +- {sem:.3f} (scatter {slopes.std(ddof=1):.3f}), n > 1 in "
      f"{int((slopes>1).sum())}/{len(slopes)} clusters",
      "which is the centrally-concentrated behaviour the falling M_req/M_bar demands")

check(RHO_CL > 0,
      f"A2  and the cluster gas density at R500, measured from the same profiles: "
      f"{RHO_CL:.3e} kg/m^3",
      "this is the number Part B compares against galaxies")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE KILL: a local baryon-density coupling is excluded by 4-8 orders")
print("=" * 100)

print("\n     galaxy ISM              rho_gas [kg/m^3]   x cluster    (rho ratio)^n at n = 1.745")
worst = 0.0
for nH, lab in ((0.1, "diffuse outer disk"), (1.0, "typical disk"), (10.0, "inner/molecular")):
    rg = nH * 1e6 * MH
    ratio = rg / RHO_CL
    amp = ratio ** slopes.mean()
    worst = max(worst, amp)
    print(f"   {lab:<22s}  {rg:>10.2e}       {ratio:>8.3g}      {amp:>10.2e}")

check(worst > 1e4,
      f"B1  *** A LOCAL SUPERLINEAR BARYON-DENSITY COUPLING IS CATASTROPHICALLY EXCLUDED: galaxy gas "
      f"is 10^2-10^4 x DENSER than cluster gas, so the same law is {worst:.0e} x STRONGER in a galaxy "
      f"than in a cluster -- the exact opposite of what is required ***",
      "so A1's n = 1.745 is a WITHIN-cluster radial statement and must NOT be read as a coupling law; "
      "reading it as one would have been the most natural next step and it is a trap")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- which discriminant survives, on the corpus's own five-environment numbers")
print("=" * 100)

print("\n     discriminant            cluster    galaxy    cosmic web    verdict")
rows = [
    ("|Phi|/c^2", PHI_CL, PHI_GAL, PHI_WEB),
    ("g/a_0", G_CL, G_GAL, G_WEB),
]
for lab, cl, gal, web in rows:
    ok_gal = cl / gal > 3
    ok_web = cl / web > 3
    v = "works" if (ok_gal and ok_web) else ("fails vs galaxies" if not ok_gal else "fails vs web")
    print(f"   {lab:<22s} {cl:>9.3g} {gal:>9.3g} {web:>12.3g}    {v}")

B = lambda w: w / (1 + w) ** 2
joint = {k: B(v ** 2) * p for k, (v, p) in
         {"cluster": (G_CL, PHI_CL), "galaxy": (G_GAL, PHI_GAL), "web": (G_WEB, PHI_WEB)}.items()}
print(f"\n   JOINT  B(g^2/a_0^2) x |Phi| :  cluster {joint['cluster']:.3e}, "
      f"galaxy {joint['galaxy']:.3e} ({joint['galaxy']/joint['cluster']:.3f}x), "
      f"web {joint['web']:.3e} ({joint['web']/joint['cluster']:.2e}x)")

check(joint["galaxy"] / joint["cluster"] < 0.5 and joint["web"] / joint["cluster"] < 0.1,
      f"C1  *** ONLY THE JOINT SELECTION WORKS, and it is the corpus's own: potential depth alone "
      f"fails against the cosmic web ({PHI_CL/PHI_WEB:.1f}x only), acceleration alone fails against "
      f"galaxies (which sit HIGHER, {G_GAL:.2f} vs {G_CL:.2f} a_0), and the product B(g^2/a_0^2) x |Phi| "
      f"suppresses galaxies to {joint['galaxy']/joint['cluster']:.3f} and the web to "
      f"{joint['web']/joint['cluster']:.1e} of the cluster response ***",
      "so the second field must carry the SAME selection the five-environment analysis already "
      "identified -- the discriminant was never the problem")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the opening, and the price")
print("=" * 100)

info("D1  THE OPENING IS REAL AND STRUCTURAL. Stage 36's obstruction was that the profile C with "
     "C' = -B has C(0) = -1, so the BUMP's kinetic addition 2AC goes negative -- a ghost. That "
     "condition exists only because the term is added to the EXISTING sector, where its kinetic "
     "contribution must not spoil the khronon's. A SECOND FIELD supplies its own kinetic term, so "
     "2AC is not the constraint it must satisfy. *** The mechanism stage 35 showed WORKS "
     "phenomenologically is therefore not excluded in a two-field realisation -- only in a one-field "
     "one. ***")

info("D2  AND THE PRICE, stated rather than buried: a new field with its own kinetic term, potential "
     "and matter coupling is a MINIMUM of two new parameters and one new function. The dark sector "
     "goes from FOUR numbers (M, I_0, mu, A_b, with Lambda_D fixed by beta = 1) to SIX or more, and "
     "Sec. 3's headline -- 'four against LambdaCDM's two' -- becomes 'six or more against two'. That "
     "is the framework's own strongest structural argument being spent to buy one front.")

info("D3  WHAT WOULD HAVE TO BE SHOWN, so this is a specification and not a hope: (i) a healthy "
     "kinetic term for the new field (no ghost, subluminal, c_T = 1 preserved); (ii) a coupling whose "
     "quasi-static limit reproduces mu_eff = mu_M - w_b B(x^2)(|Phi|/Phi_ref), which is the form the "
     "data selected; (iii) no cosmological contribution -- the web suppression of C1 is necessary but "
     "the field's own background energy density must also be shown negligible; (iv) the CMB pass and "
     "the lensing result must survive its addition. Items (i) and (ii) are the hard ones and neither "
     "is attempted here.")

info("D4  MY RECOMMENDATION, and it is a judgement rather than a result: do NOT spend the parameter "
     "count yet. The framework's position today is strong precisely because it is parsimonious -- "
     "four dark numbers, a_0(z) derived, the CMB and lensing and RAR and BTFR all passing. Carrying "
     "clusters as ONE NAMED OPEN PROBLEM is a defensible stance that costs nothing; adding a sixth "
     "and seventh parameter to close it invites the response 'so it is LambdaCDM with extra steps'. "
     "The second field is worth BUILDING when there is an independent reason to want it -- and stage "
     "9's galaxy-sector escape may yet supply one, in which case clusters come along free.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE SECOND FIELD IS SCOPED, NOT BUILT.  Three results:

  1. WHAT THE DATA REQUIRE, measured: rho_req ~ rho_gas^n with n = {slopes.mean():.3f} +- {sem:.3f}, superlinear
     in 12/12 clusters -- the centrally-concentrated profile the falling residual demands.

  2. *** AND THE OBVIOUS READING OF THAT IS A TRAP, WHICH IS THIS STAGE'S MAIN RESULT: a LOCAL
     superlinear baryon-density coupling is excluded by {worst:.0e}x, because galaxy gas is 10^2-10^4
     times DENSER than cluster gas.  The n = 1.745 slope is a within-cluster radial statement and is
     NOT a coupling law. ***

  3. The only surviving discriminant is the JOINT one the corpus already had: B(g^2/a_0^2) x |Phi|,
     which suppresses galaxies to {joint['galaxy']/joint['cluster']:.3f} and the cosmic web to {joint['web']/joint['cluster']:.1e} of the cluster response.
     Potential depth alone fails against the web; acceleration alone fails against galaxies.

  4. THE OPENING IS GENUINE: stage 36's ghost came from the BUMP's kinetic addition 2AC < 0, a
     constraint that exists only for a term bolted onto the existing sector.  A second field brings
     its own kinetic term, so the mechanism stage 35 showed works is NOT excluded in a two-field
     realisation -- only in a one-field one.

  5. THE PRICE IS THE FRAMEWORK'S BEST ARGUMENT: four dark-sector numbers become six or more, and
     "four against LambdaCDM's two" becomes "six against two".  My recommendation is to carry
     clusters as one named open problem instead, and to build the second field only if stage 9's
     galaxy-sector escape gives an independent reason to want it -- in which case clusters come free.

  NOT CLAIMED: that the second field works, or that it has been built.  What is established is which
  couplings are dead, which discriminant is forced, and exactly what a working construction would
  have to demonstrate.
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
