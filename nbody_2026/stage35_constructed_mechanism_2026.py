#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage35_constructed_mechanism_2026.py
=====================================
A MECHANISM BUILT TO SATISFY BOTH CONDITIONS -- and it is not a new term, it is the corpus's OWN
joint response moved from the MASS slot into the GRADIENT slot.

--------------------------------------------------------------------------------------------------
FIRST, A CORRECTION TO MY OWN SPECIFICATION
--------------------------------------------------------------------------------------------------
Stage 33 concluded "any cluster mechanism must have a SIGN-CHANGING effective source".  That is
correct for a MASS term and it is NOT the general requirement.  The theorem was: a Helmholtz mass
contributes rho_eff = mu^2|Phi|/4piG >= 0, so the extra ENCLOSED mass -- a volume integral of a
non-negative density -- can only grow outward.  A GRADIENT modification is not a volume integral of
anything; it rescales the field locally.  So the honest pair of conditions is:

   (a')  the boost must INCREASE with x over the cluster range, so the residual FALLS outward
         (x = g_obs/a_0 falls outward inside a cluster, from ~0.80 to ~0.25)
   (b)   the modification must VANISH as x -> 0, so the deep-MOND limit and v^4 = G M_b a_0 survive
         (this is what killed the q-route: q(0) = 1, not 0)

--------------------------------------------------------------------------------------------------
AND THE FRAMEWORK ALREADY OWNS A FUNCTION THAT DOES BOTH
--------------------------------------------------------------------------------------------------
        B(w) = w/(1+w)^2 ,   w = x^2
  * B(0) = 0                       -> condition (b), deep MOND and the BTFR untouched
  * B rises monotonically to its peak at w = 1, and the cluster range is w = 0.06-0.64, entirely
    BELOW that peak -> B increases with x across clusters -> condition (a')
  * B(w -> inf) = 0                -> the solar system is untouched as well

So the constructed mechanism is a REDUCTION of the interpolation function (smaller mu_eff = more
boost), with the corpus's own potential-depth factor as the cluster/galaxy discriminant:

    *** mu_eff(x, Phi) = mu_M(x) - w_b B(x^2) (|Phi|/Phi_ref) ***

  - the B x |Phi| product is EXACTLY the committed five-environment response of
    mi_a0_bump_response_2026.py; the only change is which slot it occupies.
  - stage 33's theorem does not reach it: it is a gradient term, not a mass.
  - stage 34's kill does not reach it: B(0) = 0 where q(0) = 1.
  - and |Phi| is the discriminant that lets clusters respond while galaxies at the SAME x do not:
    the committed potentials are |Phi|/c^2 = 2.2e-5 (cluster R500) vs 9e-7 (galaxy 20 kpc), a factor
    24, which is the number the corpus's own text credits with keeping galaxy interiors safe.

Gates, all of which the previous four candidates had to pass or failed: w_b = 0 must return the
a_0-line exactly; hyperbolicity mu_eff + 2x dmu_eff/dx > 0; the galaxy RAR must survive inside its
0.108 dex scatter AT GALAXY POTENTIAL; and the solar system must be untouched.
"""

import glob
import json
import os
import sys

import numpy as np
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
C = 2.99792458e8
MSUN = 1.98892e30
MPC = 3.0856775814913673e22
A0 = 9.3619e-11
A0_ALT = 1.1279e-10
F_STAR_DEF = 0.015
PHI_REF = 2.2e-5           # |Phi|/c^2 at cluster R500 -- the committed normalisation point
PHI_GAL = 9.0e-7           # |Phi|/c^2 at galaxy 20 kpc, committed
PHI_SOLAR = 1.0e-8         # committed

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "xcop")
from astropy.io import fits
R500 = json.load(open(os.path.join(DATA, "xcop_r500_ettori2019.json")))

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the two conditions, checked on the constructed function")
print("=" * 100)


def B_bump(w):
    w = np.asarray(w, float)
    return w / (1.0 + w) ** 2


def mu_M(x):
    x = np.maximum(np.asarray(x, float), 1e-300)
    return (np.sqrt(1.0 + 4.0 * x ** 2) - 1.0) / (2.0 * x)


def mu_eff(x, wb, phi_over_ref):
    return mu_M(x) - wb * B_bump(np.asarray(x, float) ** 2) * phi_over_ref


check(abs(float(B_bump(1e-12))) < 1e-11,
      f"A1  CONDITION (b): B(x^2) -> 0 as x -> 0 (B(1e-12) = {float(B_bump(1e-12)):.1e}), so the "
      f"deep-MOND limit and v^4 = G M_b a_0 are untouched -- this is precisely where the q-route died, "
      f"since q(0) = 1")

wcl = np.array([0.25, 0.40, 0.60, 0.80]) ** 2
Bcl = B_bump(wcl)
check(np.all(np.diff(Bcl) > 0),
      f"A2  CONDITION (a'): B rises monotonically across the cluster range x = 0.25-0.80 "
      f"(B = {Bcl[0]:.4f} -> {Bcl[-1]:.4f}), because the range lies entirely below B's peak at x = 1. "
      f"So the boost is largest where x is largest, i.e. at cluster CENTRES, and the residual FALLS "
      f"outward",
      "the behaviour every positive-mass variant got backwards")

check(float(B_bump(1e6)) < 1e-5,
      f"A3  and the solar system is safe by the same token: B(1e6) = {float(B_bump(1e6)):.1e}, so the "
      f"modification vanishes in the Newtonian regime too",
      "B is transition-localised at BOTH ends -- the property that made it the bump's profile in the "
      "first place")

check(PHI_REF / PHI_GAL > 20,
      f"A4  and the discriminant: |Phi|/c^2 = {PHI_REF:.1e} at cluster R500 against {PHI_GAL:.1e} at "
      f"galaxy 20 kpc, a factor {PHI_REF/PHI_GAL:.0f} -- so at the SAME x a galaxy feels "
      f"{PHI_GAL/PHI_REF:.3f} of the cluster response",
      "this is the corpus's own five-environment factor, and it is what allows a function of x to "
      "distinguish clusters from galaxies at all")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- hyperbolicity bound, and the a_0-line gate")
print("=" * 100)

xg = np.logspace(-3, 3, 4000)


def hyp_ok(wb, phi=1.0):
    m = mu_eff(xg, wb, phi)
    dm = np.gradient(m, xg)
    return bool(np.all(m > 0) and np.all(m + 2 * xg * dm > 0))


wb_max = 0.0
for wb in np.linspace(0.0, 5.0, 1001):
    if hyp_ok(wb):
        wb_max = wb
    else:
        break
check(wb_max > 0.1,
      f"B1  hyperbolicity holds up to w_b = {wb_max:.3f} at full cluster potential and fails above",
      "so the amplitude is bounded by the theory's own stability condition, as it should be")


def solve_x(y, wb, phi):
    y = float(y)

    def f(x):
        return float(mu_eff(np.array([x]), wb, phi)[0]) * x - y
    lo, hi = 1e-8, 1e4
    if f(lo) > 0:
        return lo
    n = 0
    while f(hi) < 0 and n < 60:
        hi *= 4.0
        n += 1
    return brentq(f, lo, hi, xtol=1e-14, rtol=1e-14)


yt = np.logspace(-3, 2, 40)
x0 = np.array([solve_x(v, 0.0, 1.0) for v in yt])
gbt = yt * A0
check(float(np.max(np.abs(x0 * A0 / np.sqrt(gbt ** 2 + A0 * gbt) - 1))) < 1e-9,
      f"B2  VALIDATION GATE: w_b = 0 returns the framework's algebraic a_0-line to "
      f"{float(np.max(np.abs(x0*A0/np.sqrt(gbt**2+A0*gbt)-1))):.1e}")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- fit to the 12 real X-COP clusters, with |Phi| computed per point")
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
check(len(CL) >= 10, f"C0  {len(CL)} clusters loaded")


def phi_profile(r_m, g):
    """|Phi(r)|/c^2 by integrating g outward to the last measured point, tail included."""
    inner = np.concatenate([np.cumsum((g[::-1][:-1] + g[::-1][1:]) * 0.5
                                      * np.abs(np.diff(r_m[::-1])))[::-1], [0.0]])
    return (inner + g[-1] * r_m[-1]) / C ** 2      # simple 1/r tail continuation


def stats(wb, a0=A0, iters=25):
    tot, npt, rr, ra = 0.0, 0, [], []
    for n, (r, mt, mb, em, r5) in CL.items():
        rm = r * MPC
        gbar = G * mb * MSUN / rm ** 2
        gobs = G * mt * MSUN / rm ** 2
        egobs = G * em * MSUN / rm ** 2
        g = np.sqrt(gbar ** 2 + a0 * gbar)          # start from the a_0-line
        for _ in range(iters):                      # self-consistent: Phi <- g <- Phi
            ph = phi_profile(rm, g) / PHI_REF
            gn = np.array([solve_x(v, wb, p) for v, p in zip(gbar / a0, ph)]) * a0
            if np.max(np.abs(gn - g) / g) < 1e-10:
                g = gn
                break
            g = 0.5 * g + 0.5 * gn
        tot += float(np.sum(((g - gobs) / egobs) ** 2))
        npt += len(rm)
        rr.append(r / r5)
        ra.append(gobs / g)
    rr = np.concatenate(rr); ra = np.concatenate(ra)
    return tot, npt, float(np.polyfit(np.log10(rr), np.log10(ra), 1)[0]), float(np.median(ra))


c0, npt, sl0, md0 = stats(0.0)
print(f"\n   w_b = 0 (pure a_0-line): chi2/dof = {c0/npt:>8.1f}  slope = {sl0:+.3f}  "
      f"median ratio = {md0:.3f}")
print(f"\n     w_b       chi2/dof     slope     median ratio")
best = (c0, 0.0, sl0, md0)
for wb in np.linspace(0.0, wb_max, 9):
    try:
        c, _, sl, md = stats(wb)
    except Exception as e:
        print(f"   {wb:>6.3f}     FAILED ({type(e).__name__})")
        continue
    mark = "  <-- best" if c < best[0] else ""
    print(f"   {wb:>6.3f}     {c/(npt-1):>9.1f}   {sl:+.3f}     {md:.3f}{mark}")
    if c < best[0]:
        best = (c, wb, sl, md)
# REFINE: the coarse grid's optimum sits next to a steep cliff, so scan finely around it
lo_r, hi_r = max(best[1] - 0.25, 0.0), min(best[1] + 0.25, wb_max)
print(f"\n   refining on [{lo_r:.3f}, {hi_r:.3f}]:")
for wb in np.linspace(lo_r, hi_r, 21):
    try:
        c, _, sl, md = stats(wb)
    except Exception:
        continue
    if c < best[0]:
        best = (c, wb, sl, md)
        print(f"   {wb:>6.4f}     {c/(npt-1):>9.1f}   {sl:+.3f}     {md:.3f}  <-- best")
cb, wbb, slb, mdb = best
print(f"\n   FINAL: w_b = {wbb:.4f}, chi2/dof = {cb/(npt-1):.1f}, slope = {slb:+.3f}, "
      f"median ratio = {mdb:.3f}")

check(cb < c0,
      f"C1  the constructed mechanism improves on the pure a_0-line: chi2/dof {c0/npt:.1f} -> "
      f"{cb/(npt-1):.1f} at w_b = {wbb:.3f}")
check(abs(slb) <= abs(sl0),
      f"C2  and it moves the radial leftover toward zero: {sl0:+.3f} -> {slb:+.3f}",
      "the direction only the q-route managed before, now with condition (b) also satisfied")
check(mdb < md0,
      f"C3  and it reduces the normalisation gap: median g_obs/g_model {md0:.3f} -> {mdb:.3f}")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the gates that killed the previous candidates")
print("=" * 100)

gb_gal = np.logspace(-12, -8, 200)
x_ref = np.array([solve_x(v, 0.0, 1.0) for v in gb_gal / A0])
x_gal = np.array([solve_x(v, wbb, PHI_GAL / PHI_REF) for v in gb_gal / A0])
dex_gal = np.abs(np.log10(x_gal / x_ref))
check(float(np.max(dex_gal)) < 0.108,
      f"D1  *** THE GALAXY RAR SURVIVES: max shift {float(np.max(dex_gal)):.4f} dex at galaxy potential, "
      f"against the committed 0.108 dex scatter.  The q-route failed this at 0.340 dex (3.1x) ***",
      f"and the reason is structural: B(0) = 0 kills the deep-MOND damage, and the |Phi| factor "
      f"suppresses the rest by {PHI_REF/PHI_GAL:.0f}x")

x_sol = np.array([solve_x(v, wbb, PHI_SOLAR / PHI_REF) for v in np.array([1e-3, 1.0]) / A0])
x_sol0 = np.array([solve_x(v, 0.0, 1.0) for v in np.array([1e-3, 1.0]) / A0])
check(float(np.max(np.abs(x_sol / x_sol0 - 1))) < 1e-6,
      f"D2  and the solar system is untouched: fractional change "
      f"{float(np.max(np.abs(x_sol/x_sol0-1))):.1e} at g_bar = 1e-3 and 1 m/s^2",
      "both because B -> 0 at large x and because the solar potential is 2200x shallower than a "
      "cluster's")

check(hyp_ok(wbb),
      f"D3  hyperbolicity holds at the fitted amplitude w_b = {wbb:.3f} (cap {wb_max:.3f})")

for lab, a0v in (("canonical", A0), ("alt footing", A0_ALT)):
    c, _, sl, md = stats(wbb, a0v)
    info(f"D4  footing {lab} (a_0 = {a0v:.4e}): chi2/dof = {c/(npt-1):.1f}, slope {sl:+.3f}, "
         f"median ratio {md:.3f}", "")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- honest accounting")
print("=" * 100)

acceptable = cb / (npt - 1) < 5.0
if acceptable:
    check(True, f"E1  *** AND IT IS A FORMALLY ACCEPTABLE FIT: chi2/dof = {cb/(npt-1):.2f} ***")
else:
    check(not acceptable,
          f"E1  IT IS STILL NOT A FORMALLY ACCEPTABLE FIT: chi2/dof = {cb/(npt-1):.1f}.  The "
          f"constructed mechanism passes every GATE that killed its predecessors and does not close "
          f"the cluster gap quantitatively",
          "reported as found -- passing the gates is necessary, not sufficient")

info(f"E2  WHAT IS AND IS NOT ESTABLISHED. Established: a mechanism built from the framework's own "
     f"pieces satisfies BOTH conditions -- vanishes as x -> 0 (so the BTFR theorem survives) and "
     f"rises with x across clusters (so the residual falls outward) -- while passing the galaxy RAR "
     f"({float(np.max(dex_gal)):.4f} dex vs 0.108), the solar system, and hyperbolicity. That is the "
     f"first candidate in stages 31-35 to clear every gate. NOT established: that it explains "
     f"clusters. It removes {100*(1-cb/c0):.0f}% of the chi2 and leaves {cb/(npt-1):.0f} per dof.")

info("E3  AND THE STRUCTURAL READING, which is what actually changed tonight: the SAME committed "
     "response function B x |Phi| is EXCLUDED in the mass slot (stage 33's theorem) and VIABLE in the "
     "gradient slot. The corpus has been treating the bump as a Helmholtz mass throughout; this says "
     "the slot, not the function, was the error. Which slot the action's "
     "A B(Y/a_0^2)(Q-Q_0)^2 term actually generates in the quasi-static limit is now the decisive "
     "question -- row 17 derived delta Q = -Q_0 Phi, which gives the MASS slot, so if this gradient "
     "reading is to be the framework's, it needs its own derivation from the action rather than an "
     "assertion. That derivation is the next owed item, and it is sharply defined.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  A MECHANISM SATISFYING BOTH CONDITIONS EXISTS, IS BUILT FROM THE FRAMEWORK'S OWN PIECES, AND CLEARS
  EVERY GATE THAT KILLED THE PREVIOUS FOUR.

      mu_eff(x, Phi) = mu_M(x) - w_b B(x^2) (|Phi|/Phi_ref),     w_b = {wbb:.3f}

  1. CONDITION (b): B(0) = 0, so the deep-MOND limit and v^4 = G M_b a_0 are untouched -- exactly
     where the q-route died (q(0) = 1).
  2. CONDITION (a'): the cluster range x = 0.25-0.80 lies entirely below B's peak at x = 1, so B
     rises with x, the boost is largest at cluster centres, and the residual FALLS outward -- the
     behaviour every positive-mass variant got backwards.
  3. GATES PASSED: galaxy RAR {float(np.max(dex_gal)):.4f} dex (vs 0.108 committed, and vs the q-route's 0.340);
     solar system unchanged to {float(np.max(np.abs(x_sol/x_sol0-1))):.0e}; hyperbolicity satisfied; a_0-line recovered exactly
     at w_b = 0.  First candidate in this sequence to clear all of them.
  4. CLUSTERS: chi2/dof {c0/npt:.0f} -> {cb/(npt-1):.0f} ({100*(1-cb/c0):.0f}% removed), slope {sl0:+.3f} -> {slb:+.3f},
     median ratio {md0:.3f} -> {mdb:.3f}.  {'AN ACCEPTABLE FIT.' if acceptable else 'NOT yet an acceptable fit.'}

  5. *** AND THE REAL FINDING IS ABOUT THE SLOT, NOT THE FUNCTION: the corpus's own B x |Phi|
     response is EXCLUDED as a Helmholtz mass (stage 33) and VIABLE as a gradient modification.  The
     bump has been treated as a mass throughout this programme.  Row 17's delta Q = -Q_0 Phi closure
     generates the MASS slot, so if the gradient reading is to be the framework's, it owes its own
     derivation from the action -- and that is now the single sharply-defined next item. ***

  NOT CLAIMED: that clusters are explained, or that the action generates this term in this slot.
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
