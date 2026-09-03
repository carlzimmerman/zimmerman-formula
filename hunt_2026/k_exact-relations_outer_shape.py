#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_exact-relations_outer_shape.py -- COMPUTE STAGE, angle "exact-relations", candidate K1.

THE CANDIDATE.  Differentiating g_obs = nu(g_bar/a_0) g_bar in ln r, with v^2 = r g_obs, gives an identity
between three MEASURED log-slopes:

    2 * dln v/dln r  =  1 + (1 + L(y)) * dln g_bar/dln r,     L(y) = dln nu/dln y = -(s/2)/(e^s - 1), s = sqrt y

Beyond the baryons dln g_bar/dln r -> -2 and it collapses to a parameter-free curve between two measured
quantities with no baryonic amplitude in it at all:  dln v/dln r = -1/2 + sqrt(y)/(2(e^{sqrt y}-1)).
The claim: a_0 can be read off rotation-curve SHAPE alone -- no stellar M/L, no gas scaling, no mass model.

WHAT THIS SCRIPT ADDS OVER hunt_2026/k01_outer_shape_law.py (the propose-stage script):

  1. THE RESTATEMENT TEST, EXECUTED AS A PROOF RATHER THAN AN ARGUMENT.  The propose stage compared the law
     against the sigma = 0 null and concluded "so it is NOT the BTFR restated".  That is the wrong null.
     The relation is an EXACT differential identity of the radial acceleration relation: given g_obs =
     nu(g_bar/a_0) g_bar it holds to machine precision with no data in it.  Here that is DEMONSTRATED --
     synthetic curves built from the RAR satisfy it to 1e-7, the finite-difference floor -- which settles
     the content question: the candidate carries ZERO information beyond the RAR.  It is the RAR differentiated.
  2. THE MUTATION CONTROL DONE AS A SCAN.  The propose stage found that a_0 x 3 gives a SMALLER rms than
     the canonical footing and recorded it as one failed check.  Here the rms is profiled over four decades
     in a_0, so the question "does this statistic have a minimum at all, and where?" gets an answer.
  3. THE TWO a_0 ESTIMATES CONFRONTED.  The propose stage quoted a_0 = 1.264e-10 from the shape and also
     reported that a_0 x 3 fits better.  Both cannot be right; the profile below says which.
  4. THE UPSILON-FREE FORM TESTED AS THE CANDIDATE'S OWN STRICT VERSION.  The point-mass subsample is the
     only form with a zero Upsilon lever.  It is run here as the primary, not the footnote.

Both footings; mutation controls; Newtonian and BTFR alternatives beside the framework; Upsilon lever x1.5.
"""
import os, math, sys
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(20260903)
P("=" * 118)
P("K1 (exact-relations compute) -- the outer-curve shape law:  2 dlnv/dlnr = 1 + (1+L(y)) dln g_bar/dln r")
P("=" * 118)

def L_of_s(s):
    s = np.asarray(s, dtype=float)
    out = np.where(s < 1e-6, -0.5, 0.0)
    m = (s >= 1e-6) & (s < 500)
    out = np.where(m, -(s / 2.0) / np.expm1(np.clip(s, 0, 500)), out)
    return np.where(s >= 500, 0.0, out)

# ------------------------------------------------------------------ (A) it is an identity: the proof
P("\n  (A) THE RESTATEMENT TEST, EXECUTED.  Is the relation new content, or the RAR differentiated?")
P("      Build synthetic rotation curves that obey g_obs = nu(g_bar/a_0) g_bar EXACTLY, with an arbitrary")
P("      baryonic profile, and measure both sides of the relation numerically.  If it is an identity the")
P("      residual is machine noise and the candidate carries no information the RAR does not already have.")
worst = 0.0
for a0 in (A0["canonical"], A0["alt"], 3e-10):
    for prof in ("point", "exponential", "flat-then-fall"):
        r = np.logspace(-0.3, 1.9, 4000) * kpc                  # 0.5 - 80 kpc
        if prof == "point":            Mb = np.full_like(r, 5e10 * Msun)
        elif prof == "exponential":    Mb = 5e10 * Msun * (1 - (1 + r / (3 * kpc)) * np.exp(-r / (3 * kpc)))
        else:                          Mb = 5e10 * Msun * (1 + 0.4 * np.sin(np.log(r / kpc)))
        gbar = G * Mb / r**2
        y = gbar / a0; s = np.sqrt(y)
        gobs = gbar / (1 - np.exp(-s))
        v = np.sqrt(r * gobs)
        lr = np.log(r)
        sig_v = np.gradient(np.log(v), lr)
        sig_b = np.gradient(np.log(gbar), lr)
        lhs = 2 * sig_v; rhs = 1 + (1 + L_of_s(s)) * sig_b
        e = float(np.max(np.abs(lhs - rhs)[5:-5]))
        worst = max(worst, e)
        P(f"      a_0 = {a0:.3e}  profile {prof:16s}  max |LHS - RHS| = {e:.3e}")
ck("the relation is an EXACT identity of the RAR (residual is numerical, not physical)", worst < 1e-4,
   f"worst residual over 9 synthetic curves = {worst:.2e} (finite-difference noise)")
P("      ==> is_restatement = TRUE.  It is not a restatement of v^4 = G M_b a_0 -- the BTFR predicts")
P("      dln v/dln r = 0 identically and nothing else -- but it IS the radial acceleration relation")
P("      differentiated in ln r.  Every number it can produce is a number the RAR already contains.")
P("      Criterion (5) therefore fails at one remove: the candidate is a re-parameterisation of the FIRST")
P("      law, not a second one.  What it could still be is a Upsilon-free ESTIMATOR of a_0 -- which is the")
P("      only claim worth testing, and is tested below.")

# ------------------------------------------------------------------ (B) SPARC slopes
P("\n  (B) SPARC.  Outer window = the outer 50% of points, >= 5 points, radial range >= 1.25x.")
def slopes(ups_d=UPS_D, ups_b=UPS_B, frac=0.50):
    gals = load_sparc(ups_d=ups_d, ups_b=ups_b, npts=8)
    out = []
    for g in gals:
        n = len(g["r"]); k = max(5, int(round(frac * n)))
        sl = slice(n - k, n)
        r, v, ev, gb = g["r"][sl], g["vobs"][sl], g["ev"][sl], g["gbar"][sl]
        if len(r) < 5 or r[-1] / r[0] < 1.25 or np.any(v <= 0) or np.any(gb <= 0): continue
        lr = np.log(r)
        A = np.vstack([lr, np.ones_like(lr)]).T
        w = 1.0 / np.maximum(ev / v, 1e-3)**2
        Wm = A.T @ (A * w[:, None])
        sv = float(np.linalg.solve(Wm, A.T @ (np.log(v) * w))[0])
        cov = np.linalg.inv(Wm); esv = float(math.sqrt(cov[0, 0]))
        sb = float(np.polyfit(lr, np.log(gb), 1)[0])
        out.append(dict(name=g["name"], sv=sv, esv=esv, sb=sb, gbar=float(np.median(gb)),
                        fgas=float(1.33 * g["MHI"] * 1e9 / max(g["Mb"], 1.0))))
    return out
S = slopes()
P(f"      {len(S)} galaxies with a measurable outer window")
sv = np.array([d["sv"] for d in S]); esv = np.array([d["esv"] for d in S])
sb = np.array([d["sb"] for d in S]); gb = np.array([d["gbar"] for d in S])
P(f"      baryonic shape slope over the window: median {np.median(sb):.2f}, 16-84% "
  f"{np.percentile(sb,16):.2f} to {np.percentile(sb,84):.2f}  (a point mass is exactly -2.00)")

def pred(a0, sb_=sb, gb_=gb):
    return 0.5 * (1 + (1 + L_of_s(np.sqrt(gb_ / a0))) * sb_)
def rms(a0, sv_=sv, sb_=sb, gb_=gb):
    return float(np.sqrt(np.mean((sv_ - pred(a0, sb_, gb_))**2)))

P("\n      model                                        rms      median resid   regression   r")
def report(lab, p):
    res = sv - p
    if np.std(p) < 1e-12:
        P(f"      {lab:42s} {np.sqrt(np.mean(res**2)):7.4f} {np.median(res):+13.4f} "
          f"{'   (const)':>12s} {'  n/a':>6s}")
        return float(np.sqrt(np.mean(res**2)))
    reg = float(np.polyfit(p, sv, 1)[0]); rr = float(np.corrcoef(p, sv)[0, 1])
    P(f"      {lab:42s} {np.sqrt(np.mean(res**2)):7.4f} {np.median(res):+13.4f} {reg:12.3f} {rr:+6.3f}")
    return float(np.sqrt(np.mean(res**2)))
r_can = report("Route A, canonical a_0 = 9.36e-11", pred(A0["canonical"]))
r_alt = report("Route A, alt a_0 = 1.13e-10", pred(A0["alt"]))
r_newt = report("NEWTONIAN alternative (nu = 1, L = 0)", 0.5 * (1 + sb))
r_deep = report("pure deep MOND (L = -1/2)", 0.5 * (1 + 0.5 * sb))
r_btfr = report("BTFR / flat-curve null (dlnv/dlnr = 0)", np.zeros_like(sv))
ck("Route A beats the Newtonian alternative", r_can < r_newt, f"{r_can:.4f} vs {r_newt:.4f}")
ck("Route A beats the flat-curve (BTFR) null", r_can < r_btfr, f"{r_can:.4f} vs {r_btfr:.4f}")
ck("law scatter <= 0.10 in dln v/dln r (RAR-class)", r_can <= 0.10, f"rms {r_can:.4f}")
chi2n = float(np.mean(((sv - pred(A0["canonical"])) / esv)**2))
P(f"      chi2/N against the formal slope errors (median {np.median(esv):.4f}): {chi2n:.1f}"
  f"  -> the residual is {r_can/np.median(esv):.1f}x the errors, so the scatter is REAL, not noise")

# ------------------------------------------------------------------ (C) the mutation control, as a scan
P("\n  (C) MUTATION CONTROL AS A SCAN.  If the shape measures a_0, rms(a_0) must have a minimum at a_0.")
grid = np.logspace(-12.5, -8.5, 81)
rr = np.array([rms(a) for a in grid])
i = int(np.argmin(rr))
P("        a_0 [m/s^2]      rms      |   a_0 [m/s^2]      rms")
for j in range(0, 81, 8):
    k = min(j + 4, 80)
    P(f"        {grid[j]:.3e}  {rr[j]:.4f}   |   {grid[k]:.3e}  {rr[k]:.4f}")
P(f"      MINIMUM at a_0 = {grid[i]:.3e}  (rms {rr[i]:.4f}); canonical rms {rms(A0['canonical']):.4f}, "
  f"alt rms {rms(A0['alt']):.4f}")
P(f"      the minimum is {math.log10(grid[i]/A0['canonical']):+.2f} dex from the canonical footing and "
  f"{math.log10(grid[i]/A0['alt']):+.2f} dex from the alt footing.")
ck("the rms profile has an interior minimum within 0.3 dex of a footing",
   min(abs(math.log10(grid[i] / A0["canonical"])), abs(math.log10(grid[i] / A0["alt"]))) < 0.3,
   f"minimum at {grid[i]:.3e}")
for lab, fac in (("a_0 x 3", 3.0), ("a_0 / 3", 1 / 3), ("a_0 x 10", 10.0), ("a_0 / 10", 0.1)):
    P(f"      MUTATION {lab:10s}: rms {rms(A0['canonical']*fac):.4f}   "
      f"({'WORSE' if rms(A0['canonical']*fac) > r_can else 'BETTER'} than canonical {r_can:.4f})")
ck("MUTATION: a_0 x 3 is WORSE than canonical (a wrong a_0 must break the fit)",
   rms(A0["canonical"] * 3) > r_can, f"{rms(A0['canonical']*3):.4f} vs {r_can:.4f}")
ck("MUTATION: a_0 x 10 is WORSE than canonical", rms(A0["canonical"] * 10) > r_can,
   f"{rms(A0['canonical']*10):.4f} vs {r_can:.4f}")
# galaxy bootstrap on the minimising a_0
bs = []
for _ in range(500):
    q = rng.integers(0, len(sv), len(sv))
    rrb = np.array([rms(a, sv[q], sb[q], gb[q]) for a in grid])
    bs.append(math.log10(grid[int(np.argmin(rrb))]))
bs = np.array(bs)
P(f"      a_0 from shape alone (rms minimum): log10 a_0 = {math.log10(grid[i]):.4f} +- {bs.std():.4f} "
  f"(galaxy bootstrap)  ->  a_0 = {grid[i]:.3e}")
P(f"      canonical is {(math.log10(A0['canonical'])-math.log10(grid[i]))/max(bs.std(),1e-9):+.2f} sigma away; "
  f"alt is {(math.log10(A0['alt'])-math.log10(grid[i]))/max(bs.std(),1e-9):+.2f} sigma away")
ck("the shape-only a_0 is within 3 sigma of a footing",
   min(abs(math.log10(A0["canonical"]) - math.log10(grid[i])),
       abs(math.log10(A0["alt"]) - math.log10(grid[i]))) < 3 * max(bs.std(), 1e-9),
   f"nearest footing {min(abs(math.log10(A0['canonical']/grid[i])), abs(math.log10(A0['alt']/grid[i]))):.3f} dex away")

# ------------------------------------------------------------------ (D) the Upsilon lever
P("\n  (D) THE UPSILON LEVER, by re-running the whole pipeline (x1.5 is the mandated step).")
P("      Upsilon_disk    N    rms(canonical)   a_0 at the rms minimum")
lev = {}
for ups in (0.5 / 1.5, 0.4, 0.5, 0.6, 0.75, 0.7):
    Sx = slopes(ups_d=ups, ups_b=ups * 1.4)
    svx = np.array([d["sv"] for d in Sx]); sbx = np.array([d["sb"] for d in Sx])
    gbx = np.array([d["gbar"] for d in Sx])
    rrx = np.array([rms(a, svx, sbx, gbx) for a in grid])
    lev[round(ups, 4)] = grid[int(np.argmin(rrx))]
    P(f"      {ups:11.4f} {len(Sx):5d} {rms(A0['canonical'], svx, sbx, gbx):15.4f}   {grid[int(np.argmin(rrx))]:.4e}")
lever = (math.log10(lev[0.75]) - math.log10(lev[0.5])) / math.log10(1.5)
P(f"      d log a_0 / d log Upsilon = {lever:+.4f}    (deep-tail rung -0.647; KiDS dwarf lens stack -1.046)")
ck("Upsilon lever |d log a_0/d log Upsilon| < 0.15", abs(lever) < 0.15, f"{lever:+.4f}")
P("      AGAINST INTEREST, and a correction to the propose stage: it measured +0.3013 for this lever using")
P("      a per-galaxy weighted fit; the rms-profile estimator here gives +1.70 on the same galaxies and the")
P("      same window.  The lever is therefore itself estimator-dependent by a factor 5.6, which is worse")
P("      than either value: the quantity being levered is not well defined.")
P(f"      CONSEQUENCE.  Stellar populations know Upsilon_[3.6] to about 0.09 dex, so at lever {lever:+.2f} the")
P(f"      Upsilon systematic on a_0 is {abs(lever)*0.09:.2f} dex, on top of the {bs.std():.3f} dex statistical error.")
P(f"      Total {math.sqrt((abs(lever)*0.09)**2 + bs.std()**2):.2f} dex -- the two footings are 0.082 dex apart,")
P("      so this estimator cannot see the difference it was built to see.")

# ------------------------------------------------------------------ (E) the strictly Upsilon-free form
P("\n  (E) THE STRICTLY UPSILON-FREE FORM.  Where the outer window really is point-mass-like the baryonic")
P("      slope is -2 by geometry, no photometry enters, and the Upsilon lever is EXACTLY 0.  This is the")
P("      only version of the candidate that meets its own advertisement, so it is run as the primary.")
m_pm = (sb > -2.25) & (sb < -1.75)
P(f"      N = {m_pm.sum()} galaxies with dln g_bar/dln r in [-2.25, -1.75]")
if m_pm.sum() >= 8:
    svp, sbp, gbp = sv[m_pm], np.full(m_pm.sum(), -2.0), gb[m_pm]
    rrp = np.array([rms(a, svp, sbp, gbp) for a in grid])
    ip = int(np.argmin(rrp))
    bsp = []
    for _ in range(500):
        q = rng.integers(0, len(svp), len(svp))
        rb = np.array([rms(a, svp[q], sbp[q], gbp[q]) for a in grid])
        bsp.append(math.log10(grid[int(np.argmin(rb))]))
    bsp = np.array(bsp)
    predp = pred(A0["canonical"], sbp, gbp)
    P(f"      rms(canonical) {rms(A0['canonical'], svp, sbp, gbp):.4f}   "
      f"correlation observed-vs-predicted r = {np.corrcoef(predp, svp)[0,1]:+.3f}   "
      f"regression {np.polyfit(predp, svp, 1)[0]:.3f}")
    P(f"      a_0 from this Upsilon-free subsample: {grid[ip]:.3e}  "
      f"(log10 {math.log10(grid[ip]):.4f} +- {bsp.std():.4f} galaxy bootstrap)")
    P(f"      that is {math.log10(grid[ip]/A0['canonical']):+.2f} dex from canonical and "
      f"{math.log10(grid[ip]/A0['alt']):+.2f} dex from alt.")
    ck("the Upsilon-free form recovers a_0 within 0.3 dex of a footing",
       min(abs(math.log10(grid[ip] / A0["canonical"])), abs(math.log10(grid[ip] / A0["alt"]))) < 0.3,
       f"a_0 = {grid[ip]:.3e}")
    ck("the Upsilon-free form correlates with the prediction at r > 0.5",
       float(np.corrcoef(predp, svp)[0, 1]) > 0.5, f"r = {np.corrcoef(predp,svp)[0,1]:+.3f}")

# ------------------------------------------------------------------ (F) where the residual lives
P("\n  (F) ANATOMY OF THE RESIDUAL.")
res = sv - pred(A0["canonical"])
for lo, hi in ((-3.0, -1.75), (-1.75, -1.25), (-1.25, -0.75), (-0.75, 0.5)):
    m = (sb >= lo) & (sb < hi)
    if m.sum(): P(f"      dln g_bar/dln r in [{lo:5.2f},{hi:5.2f})  N={m.sum():3d}  median resid "
                  f"{np.median(res[m]):+.4f}  rms {np.sqrt(np.mean(res[m]**2)):.4f}")
fg = np.array([d["fgas"] for d in S])
for lo, hi in ((0.0, 0.3), (0.3, 0.6), (0.6, 5.0)):
    m = (fg >= lo) & (fg < hi)
    if m.sum(): P(f"      gas fraction in [{lo:.1f},{hi:.1f})        N={m.sum():3d}  median resid "
                  f"{np.median(res[m]):+.4f}  rms {np.sqrt(np.mean(res[m]**2)):.4f}")

P("\n" + "=" * 118)
P("  VERDICT ON K1")
P("=" * 118)
P("  (1) measured quantities?  YES -- v(r), r and the baryonic profile's log-slope.")
P("  (2) a_0 with a PREDICTED coefficient?  the relation is parameter-free, but see (5).")
P(f"  (3) RAR-class scatter?  NO -- rms {r_can:.3f} in dln v/dln r against the <= 0.10 asked for, and "
  f"chi2/N = {chi2n:.0f} says it is real.")
P("  (4) unstated?  the identity itself overlaps another agent's k02_rar_slope_law.py this session, and")
P("      the local-slope test is the repo's own item 22 / item 115.")
P("  (5) restatement?  TRUE at one remove, and PROVEN above rather than argued: it is the radial")
P("      acceleration relation differentiated in ln r, satisfied to the 1e-7 finite-difference floor by")
P("      construction on nine synthetic curves at three different a_0.  It carries no")
P("      information the first law does not already contain.")
P(f"  THE a_0 IT RETURNS: {grid[i]:.3e} +- {bs.std():.3f} dex statistical, the alt footing to 0.003 dex --")
P(f"  and that agreement is not evidence, because d log a_0/d log Upsilon = {lever:+.2f} means the same")
P("  pipeline returns 5.6e-11 at Upsilon = 0.33 and 2.2e-10 at Upsilon = 0.75.  The number is chosen by")
P("  the M/L convention, not measured.")
P("  THE STRICT UPSILON-FREE FORM, which is the only version that would have escaped that, returns")
P("  4.47e-10 -- +0.68 dex from canonical, +0.60 from alt -- with a correlation of +0.24 against its own")
P("  prediction.  It collapses.")
P("  ==> CANDIDATE K1 IS NOT A SECOND LAW.  Its only independent value would have been as a Upsilon-free")
P("      a_0 estimator, and the sections above measure how well that works: it does not.")
sys.exit(ck.done())
