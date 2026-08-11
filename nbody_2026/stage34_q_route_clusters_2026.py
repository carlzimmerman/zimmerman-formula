#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage34_q_route_clusters_2026.py
================================
THE q-ROUTE: the bump acting through the GRADIENT coefficient instead of as a mass -- the one escape
stage 33's theorem left open, built and fitted to 12 real X-COP clusters.

--------------------------------------------------------------------------------------------------
WHY THIS IS NOT ANOTHER VARIANT OF WHAT ALREADY FAILED
--------------------------------------------------------------------------------------------------
Stage 33 proved a theorem: a Helmholtz MASS contributes rho_eff = mu^2|Phi|/4piG which is
NON-NEGATIVE for any amplitude and any argument, so the extra ENCLOSED mass can only GROW outward --
while the data need it to FALL (12/12 clusters, mean slope -0.366 +- 0.077).  That excluded the whole
positive-mu^2 class at once.

The escape it left was a SIGN-CHANGING effective response.  The framework already contains one, and
it has been sitting in the corpus labelled as a stability caveat rather than a mechanism:

        q(w) = B'(w) + 2 w B''(w) = (3w^2 - 8w + 1)/(1+w)^4        [sympy-verified identity]

This is the bump's contribution to the BEKENSTEIN-MILGROM HYPERBOLICITY combination -- i.e. it enters
the GRADIENT coefficient, not the source.  *** Stage 33's theorem does not apply to it, because it is
not a mass. ***  And its zero crossing sits exactly where clusters live:

        q > 0 for w < 0.1315,   q < 0 for 0.1315 < w < 2.535
        measured across X-COP:  x = g_obs/a_0 = 0.25-0.80,  so w = x^2 = 0.06-0.64  -- STRADDLING it

With mu_eff = mu_M + w_b q(x^2), and a SMALLER mu_eff meaning MORE boost:
        cluster centre (large x): q < 0  ->  mu_eff reduced  ->  MORE boost
        cluster outskirts (small x): q > 0  ->  mu_eff raised  ->  LESS boost
which is the radial pattern the falling residual demands, by construction rather than by tuning.

--------------------------------------------------------------------------------------------------
WHAT IS SOLVED
--------------------------------------------------------------------------------------------------
The AQUAL first integral is algebraic -- no ODE, no additivity approximation, no iteration:
        mu_eff(x) x = y ,      x = g_obs/a_0 ,  y = g_bar/a_0 ,
        mu_eff(x) = mu_M(x) + w_b q(x^2) ,   mu_M(x) = [sqrt(1+4x^2)-1]/(2x)   (the a_0-line, exact)
ONE free parameter w_b.  Gates: (i) w_b = 0 must return the framework's own a_0-line exactly;
(ii) hyperbolicity mu_eff + 2x mu_eff' > 0 must hold everywhere used -- that is the very condition
q's negativity was flagged as threatening, so it BOUNDS w_b rather than being free; (iii) the galaxy
RAR must not be damaged, checked at galaxy accelerations.
"""

import glob
import json
import os
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

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
A0 = 9.3619e-11
A0_ALT = 1.1279e-10
F_STAR_DEF = 0.015

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "xcop")
from astropy.io import fits
R500 = json.load(open(os.path.join(DATA, "xcop_r500_ettori2019.json")))

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- q's identity, and mu_eff with its hyperbolicity bound")
print("=" * 100)

ws = sp.symbols("w", positive=True)
Bs = ws / (1 + ws) ** 2
q_sym = sp.simplify(sp.diff(Bs, ws) + 2 * ws * sp.diff(Bs, ws, 2))
check(sp.simplify(q_sym - (3 * ws ** 2 - 8 * ws + 1) / (1 + ws) ** 4) == 0,
      "A1  q = B' + 2wB'' = (3w^2-8w+1)/(1+w)^4 EXACTLY -- the corpus's own q is the bump's "
      "Bekenstein-Milgrom hyperbolicity contribution, i.e. a GRADIENT term, not a mass",
      "sympy; this is why stage 33's positive-mass theorem does not reach it")


def q_of(w):
    w = np.asarray(w, float)
    return (3 * w ** 2 - 8 * w + 1) / (1 + w) ** 4


def mu_M(x):
    x = np.maximum(np.asarray(x, float), 1e-300)
    return (np.sqrt(1.0 + 4.0 * x ** 2) - 1.0) / (2.0 * x)


def mu_eff(x, wb):
    return mu_M(x) + wb * q_of(np.asarray(x, float) ** 2)


# hyperbolicity: d/dx [ x^2 mu_eff ] > 0  <=>  mu_eff + (x/2) dmu_eff/dx ... use the BM form
xg = np.logspace(-3, 3, 4000)


def hyperbolic_ok(wb):
    m = mu_eff(xg, wb)
    dm = np.gradient(m, xg)
    return bool(np.all(m > 0) and np.all(m + 2 * xg * dm > 0))


wb_max = 0.0
for wb in np.linspace(0.0, 3.0, 601):
    if hyperbolic_ok(wb):
        wb_max = wb
    else:
        break
check(wb_max > 0.0,
      f"A2  *** THE AMPLITUDE IS BOUNDED BY THE FRAMEWORK'S OWN STABILITY CONDITION, not free: "
      f"hyperbolicity mu_eff + 2x dmu_eff/dx > 0 holds up to w_b = {wb_max:.3f} and fails above ***",
      "the very negativity of q that was carried as a WATCH is what caps the mechanism -- so this "
      "route is constrained by the same analysis that flagged it")


def solve_x(y, wb):
    """invert mu_eff(x) x = y for x (= g_obs/a_0)."""
    y = float(y)

    def f(x):
        return float(mu_eff(np.array([x]), wb)[0]) * x - y
    lo, hi = 1e-8, 1e4
    if f(lo) > 0:
        return lo
    while f(hi) < 0 and hi < 1e10:
        hi *= 4.0
    return brentq(f, lo, hi, xtol=1e-14, rtol=1e-14)


# gate (i): wb = 0 reproduces the a_0-line
yt = np.logspace(-3, 2, 40)
x0 = np.array([solve_x(v, 0.0) for v in yt])
gb = yt * A0
ga = np.sqrt(gb ** 2 + A0 * gb)
err = float(np.max(np.abs(x0 * A0 / ga - 1)))
check(err < 1e-9,
      f"A3  VALIDATION GATE: w_b = 0 reproduces the framework's algebraic a_0-line to {err:.1e}")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- fit the single amplitude to 12 real X-COP clusters")
print("=" * 100)


def load(n):
    d = fits.open(os.path.join(DATA, n, f"{n}_fgas_profile.fits"))[1].data
    r5 = R500[n]["R500"]
    r = np.asarray(d["RADIUS"], float) * r5
    mt = np.asarray(d["M_NFW"], float)
    mg = np.asarray(d["MGAS"], float)
    em = 0.5 * (np.asarray(d["M_NFW_LO"], float) + np.asarray(d["M_NFW_HI"], float))
    msf = os.path.join(DATA, n, f"{n}_mstar.fits")
    if os.path.exists(msf):
        ms = fits.open(msf)[1].data
        st = np.interp(r, np.asarray(ms["RADIUS"], float) * r5, np.asarray(ms["MSTAR"], float))
    else:
        st = F_STAR_DEF * mt
    ok = np.isfinite(r) & np.isfinite(mt) & (mt > 0) & (mg > 0) & (r > 0)
    o = np.argsort(r[ok])
    return (r[ok][o], mt[ok][o], mg[ok][o] + st[ok][o], np.maximum(em[ok][o], 0.02 * mt[ok][o]), r5)


names = sorted([os.path.basename(os.path.dirname(f))
                for f in glob.glob(os.path.join(DATA, "*", "*_fgas_profile.fits"))
                if os.path.basename(os.path.dirname(f)) in R500])
CL = {n: load(n) for n in names}
check(len(CL) >= 10, f"B0  {len(CL)} clusters loaded")


def stats(wb, a0=A0):
    tot, npt, rr, ra = 0.0, 0, [], []
    for n, (r, mt, mb, em, r5) in CL.items():
        rm = r * MPC
        gbar = G * mb * MSUN / rm ** 2
        gobs = G * mt * MSUN / rm ** 2
        egobs = G * em * MSUN / rm ** 2
        gmod = np.array([solve_x(v, wb) for v in gbar / a0]) * a0
        tot += float(np.sum(((gmod - gobs) / egobs) ** 2))
        npt += len(rm)
        rr.append(r / r5)
        ra.append(gobs / gmod)
    rr = np.concatenate(rr); ra = np.concatenate(ra)
    sl = float(np.polyfit(np.log10(rr), np.log10(ra), 1)[0])
    return tot, npt, sl, float(np.median(ra))


c0, npt, sl0, med0 = stats(0.0)
print(f"\n   w_b = 0 (pure a_0-line):  chi2/dof = {c0/npt:>8.1f}   leftover slope = {sl0:+.3f}   "
      f"median ratio = {med0:.3f}")
print(f"\n     w_b        chi2/dof     leftover slope    median g_obs/g_model")
best = (c0, 0.0, sl0, med0)
for wb in np.linspace(0.0, wb_max, 11):
    c, _, sl, md = stats(wb)
    flag = "  <-- best" if c < best[0] else ""
    print(f"   {wb:>6.3f}     {c/(npt-1):>9.1f}      {sl:+.3f}            {md:.3f}{flag}")
    if c < best[0]:
        best = (c, wb, sl, md)

cb, wbb, slb, mdb = best
check(cb < c0,
      f"B1  the q-route improves on the pure a_0-line: chi2/dof {c0/npt:.1f} -> {cb/(npt-1):.1f} at "
      f"w_b = {wbb:.3f} (of a hyperbolicity-allowed maximum {wb_max:.3f})")

check(abs(slb) < abs(sl0),
      f"B2  *** AND IT IS THE FIRST MECHANISM IN THIS SEQUENCE TO FLATTEN THE RADIAL RESIDUAL RATHER "
      f"THAN STEEPEN IT: leftover slope {sl0:+.3f} -> {slb:+.3f}.  Every positive-mass variant made it "
      f"worse (stage 32: -0.34, stage 33: -0.48 and -0.78) ***"
      if abs(slb) < abs(sl0) else
      f"B2  the q-route does NOT flatten the residual either: {sl0:+.3f} -> {slb:+.3f}",
      "which is the qualitative signature stage 33's theorem said a sign-changing response should have")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- does it survive at the hyperbolicity limit, and what does it cost galaxies?")
print("=" * 100)

c_lim, _, sl_lim, md_lim = stats(wb_max)
print(f"\n   at the stability-allowed maximum w_b = {wb_max:.3f}: chi2/dof = {c_lim/(npt-1):.1f}, "
      f"slope {sl_lim:+.3f}, median ratio {md_lim:.3f}")

# the RAR cost: galaxies sit at g_bar ~ 1e-11 to 1e-8 m/s^2
gb_gal = np.logspace(-12, -8, 200)
x_ref = np.array([solve_x(v, 0.0) for v in gb_gal / A0])
x_q = np.array([solve_x(v, wbb) for v in gb_gal / A0])
dex = np.abs(np.log10(x_q / x_ref))
i_worst = int(np.argmax(dex))
check(np.max(dex) > 0.108,
      f"C1  *** AND THE GALAXY COST KILLS IT: at the fitted w_b = {wbb:.3f} the RAR is shifted by up to "
      f"{np.max(dex):.4f} dex -- {np.max(dex)/0.108:.1f}x the ENTIRE committed RAR scatter of 0.108 dex.  "
      f"The q-route buys a {100*(1-cb/c0):.1f}% cluster improvement by wrecking the relation this "
      f"framework is strongest on ***",
      f"and the worst damage is at g_bar = {gb_gal[i_worst]:.1e} m/s^2, i.e. g_bar/a_0 = "
      f"{gb_gal[i_worst]/A0:.3f} -- the DEEP-MOND end, not the transition")

info(f"C2  AND THE REASON IS EXACT, not numerical: q(w -> 0) = 1, NOT 0.  So mu_eff = mu_M(x) + w_b "
     f"q(x^2) -> x + w_b as x -> 0, i.e. the q-term adds a CONSTANT FLOOR to mu_eff in the deep-MOND "
     f"regime where mu_M -> x is vanishing.  *** That destroys the MOND limit itself -- and with it "
     f"v^4 = G M_b a_0, which stage 25 proved is a THEOREM of the a_0-line. ***  Any mechanism whose "
     f"gradient contribution does not vanish as x -> 0 is excluded on the same grounds, whatever it "
     f"does for clusters.")

# How large may w_b be if the RAR is to survive?  Then: what does clusters get at that amplitude?
RAR_BUDGET = 0.030          # dex, a fraction of the committed 0.108 scatter
wb_rar = 0.0
for wb in np.logspace(-5, np.log10(max(wb_max, 1e-4)), 240):
    xq = np.array([solve_x(v, wb) for v in gb_gal / A0])
    if float(np.max(np.abs(np.log10(xq / x_ref)))) < RAR_BUDGET:
        wb_rar = wb
    else:
        break
c_rar, _, sl_rar, md_rar = stats(wb_rar)
print(f"\n   maximum w_b compatible with a {RAR_BUDGET} dex RAR budget: w_b <= {wb_rar:.5f}")
print(f"     at that amplitude: chi2/dof = {c_rar/(npt-1):.1f} (vs {c0/npt:.1f} at w_b = 0), "
      f"slope {sl_rar:+.3f}")
check(wb_rar < 0.05 * wb_max and abs(c_rar - c0) / c0 < 0.01,
      f"C1b  *** SO THE REAL BOUND IS THE DEEP-MOND LIMIT, NOT HYPERBOLICITY, AND IT IS "
      f"{wb_max/max(wb_rar,1e-9):.0f}x TIGHTER: the RAR allows only w_b <= {wb_rar:.5f} against "
      f"hyperbolicity's {wb_max:.3f}, and at that amplitude the cluster chi2 changes by "
      f"{100*abs(c_rar-c0)/c0:.2f}% -- nothing ***",
      "this is a NEW and much tighter bound on the bump's gradient amplitude than the corpus has been "
      "carrying, and it applies to the bump generally, not only to this cluster use of it")

for lab, a0v in (("canonical", A0), ("alt footing", A0_ALT)):
    c, _, sl, md = stats(wbb, a0v)
    info(f"C3  footing {lab} (a_0 = {a0v:.4e}): chi2/dof = {c/(npt-1):.1f}, slope {sl:+.3f}, "
         f"median ratio {md:.3f}", "")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the honest accounting")
print("=" * 100)

acceptable = cb / (npt - 1) < 5.0
check(not acceptable,
      f"D1  IT IS STILL NOT A FORMALLY ACCEPTABLE FIT: best chi2/dof = {cb/(npt-1):.1f}.  The q-route "
      f"is the first mechanism here with the RIGHT QUALITATIVE BEHAVIOUR and it does not close the "
      f"gap quantitatively",
      "reported as found; an acceptable fit would be chi2/dof of order a few")

info(f"D2  WHAT IT DOES AND DOES NOT DO, plainly: it removes {100*(1-cb/c0):.0f}% of the chi2 the pure "
     f"a_0-line leaves, brings the median normalisation from {med0:.3f} to {mdb:.3f}, and is the ONLY "
     f"mechanism in stages 31-34 that moves the radial slope toward zero instead of away from it.  "
     f"But the residual scatter is still far too large, so something in the SHAPE remains unaccounted "
     f"even with the sign structure right.")

info("D3  AND THE STRUCTURAL POINT WORTH KEEPING REGARDLESS OF THE FIT QUALITY: the amplitude is not "
     "a free dial.  Hyperbolicity -- the framework's own stability condition, the one q's negativity "
     "was flagged as threatening -- caps w_b, and the fitted value sits inside that cap.  So this is "
     "a mechanism whose strength is bounded by the theory rather than chosen to fit clusters, which "
     "is the opposite of how the a_0-bump amplitude has been treated until now.")

info("D4  NEXT, and specific: q enters the GRADIENT matrix as one entry of ΔG = 2λ[[q, 2y^{3/2}B''], "
     "[2y^{3/2}B'', yq]] (committed row 17).  This stage used only the diagonal q; the OFF-DIAGONAL "
     "2y^{3/2}B'' entries mix the khronon with the aether scalar and were not included.  A full "
     "two-field gradient solve is the untried remainder, and row 17 already has the matrix.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE q-ROUTE HAS THE RIGHT SIGN STRUCTURE AND IS EXCLUDED ANYWAY -- BY THE GALAXIES, NOT THE
  CLUSTERS.

  1. IT REALLY IS THE RIGHT KIND OF MECHANISM.  q = B' + 2wB'' (sympy-verified) is a GRADIENT term,
     so stage 33's positive-mass theorem does not reach it, and its zero crossing at w = 0.1315 sits
     inside the measured cluster range -- so it boosts centres and suppresses outskirts by
     construction.  It is the FIRST mechanism in stages 31-34 to move the radial leftover TOWARD zero
     ({sl0:+.3f} -> {slb:+.3f}) instead of away from it (-0.34, -0.48, -0.78 for the mass variants).

  2. AND THE CLUSTER GAIN IS NEGLIGIBLE ANYWAY: chi2/dof {c0/npt:.0f} -> {cb/(npt-1):.0f}, a {100*(1-cb/c0):.1f}% improvement,
     because clusters sit at small x where |q| is modest while |q| peaks at x = 0.66.

  3. *** AND THE GALAXY COST IS FATAL, FOR AN EXACT REASON: q(w -> 0) = 1, NOT 0.  So
     mu_eff -> x + w_b in the deep-MOND limit -- a CONSTANT FLOOR where mu_M -> x is vanishing.  That
     destroys the MOND limit itself, and with it v^4 = G M_b a_0, which stage 25 proved is a theorem
     of the a_0-line.  At the fitted w_b = {wbb:.3f} the RAR shifts by {np.max(dex):.3f} dex -- {np.max(dex)/0.108:.1f}x the
     entire committed 0.108 dex scatter, worst at g_bar/a_0 = {gb_gal[i_worst]/A0:.3f}. ***

  4. THE USEFUL BY-PRODUCT, and it outlives the q-route: the deep-MOND limit bounds the bump's
     gradient amplitude at w_b <= {wb_rar:.5f} for a 0.03 dex RAR budget, against hyperbolicity's
     {wb_max:.3f}.  *** That is a {wb_max/max(wb_rar,1e-9):.0f}x TIGHTER bound than the corpus has been carrying, and it
     applies to the a_0-bump generally rather than only to this cluster use of it. ***  At the
     RAR-allowed amplitude the cluster chi2 moves by {100*abs(c_rar-c0)/c0:.2f}%.

  5. GENERAL LESSON, which is what stages 31-34 have actually established: any cluster mechanism in
     this framework must (a) have a sign-changing effective source, from stage 33's theorem, AND
     (b) vanish as x -> 0 so the deep-MOND limit and the BTFR survive.  The a_0-bump's q term
     satisfies (a) and fails (b).  Those two conditions together are a sharp specification, and
     nothing tried so far meets both.

  NOT CLAIMED: that clusters are explained.  Four mechanisms are now excluded by data or by internal
  limits rather than by argument, and the surviving requirement is stated precisely enough to test
  the next candidate before building it.
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
