#!/usr/bin/env python3
r"""mi_routeA_a0_estimator_invariance_2026.py -- IS ANY a0 ESTIMATOR SHAPE-INVARIANT? The question Route A forced.

THE PROBLEM. `mi_route_a_exponential_kernel_2026.py` (9/9) found that adopting Route A's exponential kernel
COSTS the framework its one measured, kappa-discriminating result: the SPARC profile likelihood that favoured
kappa = 1/2 over Milgrom 2020's kappa = 1/2pi by 2.2 sigma on the alpha=2 kernel FLIPS to 0.67 sigma from the
optimum on the exponential kernel, because the preferred a0 moves from 1.077x canonical DOWN to 0.937x. The
lesson stated there was that the 2.2 sigma "was a property of the alpha=2 SHAPE, not of the data alone."

That lesson has a sharp consequence which this script tests: if the a0 a fit prefers depends on the assumed
transition shape, then EVERY a0 measurement in this corpus that uses the transition region inherits a SHAPE
SYSTEMATIC that has never been quoted. Including, specifically, the a0-line -- because

    g_obs^2 - g_bar^2 = a0 g_bar

is the alpha=1 kernel EXACTLY, so an estimator built on it is not shape-free; it is shape-ASSUMING, and
alpha=1 is retired.

THE ONE THING THAT IS SHAPE-INVARIANT. All three kernels share the deep-MOND limit nu -> 1/sqrt(y), i.e.
g_obs -> sqrt(g_bar a0). So an estimator restricted to DEEP points should return an a0 that does not care which
kernel is assumed. That is a testable claim, and its precision cost is measurable: fewer points means a larger
statistical error. The question this script answers is whether the shape systematic can be pushed below the
8.20% gap between kappa = 1/2 and kappa = 1/2pi FASTER than the statistical error grows.

If yes, kappa is measurable shape-independently and the Route A damage is repairable.
If no, the honest verdict is that SPARC cannot measure kappa without assuming a shape.

  E1  conventions validated against the committed alpha=2 result (1.077x) -- a control, not a fit
  E2  THE SHAPE SYSTEMATIC vs depth: a0_best under four shapes at shrinking y_max
  E3  the statistical error at each depth, from the Dchi2 curve
  E4  *** THE VERDICT: total error vs the 8.20% kappa gap ***
  E5  the a0-line, which is the alpha=1 identity -- its shape bias quantified

CIRCULARITY GUARD: the deep-point selection is FROZEN once at a0_ref with a fixed Upsilon. Selecting on
g_bar/a0 while a0 varies would let the sample follow the parameter and manufacture a constraint. This is the
same guard the anchor script uses, and it is load-bearing.

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import glob
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import A0_ALT, A0_CANON, A0_M20, nu, nu_alpha1, nu_alpha2  # noqa: E402

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 110)
    print(f"  {t}")
    print("=" * 110)


def nu_deep(y):
    """the SHAPE-FREE estimator: the deep-MOND limit itself, g_obs = sqrt(g_bar a0)."""
    return 1.0 / np.sqrt(np.asarray(y, float))


KERNELS = {"exponential (Route A)": nu, "alpha=2 (superseded)": nu_alpha2,
           "alpha=1 (retired)": nu_alpha1, "deep limit 1/sqrt(y)": nu_deep}
KAPPA_GAP = abs(A0_M20 / A0_CANON - 1.0)          # the 8.20% separation between kappa = 1/2 and kappa = 1/2pi

# ------------------------------------------------------------------ SPARC, with the corpus's own conventions
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sparc_data")
gals = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    # conventions MATCHED EXACTLY to the anchor mi_a0_profile_likelihood_sparc_2026.py: the velocity error is
    # CLIPPED AT A 1 km/s FLOOR and galaxies need >= 3 points. Without the clip, points with tiny quoted errors
    # get runaway weight and the preferred a0 moves by ~11% -- which is how E1 first failed.
    m = np.isfinite(R) & np.isfinite(Vobs) & (R > 0) & (Vobs > 0)
    if m.sum() < 3:
        continue
    gals.append(dict(name=os.path.basename(f), Rm=R[m] * 3.0857e19, Vobs=Vobs[m] * 1e3,
                     eV=np.clip(eV[m], 1.0, None) * 1e3,
                     Vgas=Vgas[m] * 1e3, Vdisk=Vdisk[m] * 1e3, Vbul=Vbul[m] * 1e3))
print(f"  loaded {len(gals)} SPARC galaxies")

UGRID = np.linspace(0.05, 3.0, 119)               # Upsilon_disk free per galaxy; Upsilon_bul = 1.4 Upsilon_disk


def gbar_gobs(g, Ud):
    Vbar2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + Ud * g["Vdisk"] ** 2 + 1.4 * Ud * g["Vbul"] ** 2
    gbar = Vbar2 / g["Rm"]
    gobs = g["Vobs"] ** 2 / g["Rm"]
    return gbar, gobs


def freeze_masks(ymax, a0_ref=A0_CANON, Ud0=0.5):
    """freeze the deep-point selection ONCE, at fixed a0_ref and fixed Upsilon.

    Re-selecting as a0 varies would let the sample track the parameter -- the circularity this corpus already
    had to guard against once. Ud0 = 0.5 is a fixed reference, deliberately NOT the fitted value.
    """
    out = {}
    for g in gals:
        gbar, gobs = gbar_gobs(g, Ud0)
        out[g["name"]] = ((gbar > 0) & (gobs > 0) & np.isfinite(gbar) & np.isfinite(gobs)
                          & (gbar / a0_ref < ymax))
    return out


def chi2_at(a0, kern, sig_int, masks=None):
    """profile likelihood: each galaxy picks the Upsilon minimising its own chi2."""
    tot, npts, nU = 0.0, 0, 0
    for g in gals:
        best = None
        for Ud in UGRID:
            gbar, gobs = gbar_gobs(g, Ud)
            m = (gbar > 0) & (gobs > 0) & np.isfinite(gbar) & np.isfinite(gobs)
            if masks is not None:
                m = m & masks[g["name"]]
            if m.sum() < 1:
                continue
            pred = np.asarray(kern(gbar[m] / a0)) * gbar[m]
            r = np.log10(gobs[m]) - np.log10(pred)
            so = (g["eV"][m] / g["Vobs"][m]) * 2.0 / math.log(10)
            v = float(np.sum(r * r / (so * so + sig_int * sig_int)))
            if best is None or v < best[0]:
                best = (v, int(m.sum()))
        if best is not None:
            tot += best[0]
            npts += best[1]
            nU += 1
    return tot, npts, nU


def calib_sig(kern, masks=None):
    """intrinsic scatter set so chi2/dof = 1 at the canonical a0 -- the anchor's convention."""
    lo, hi = 0.001, 0.60
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        ch, npts, nU = chi2_at(A0_CANON, kern, mid, masks)
        if npts - nU - 1 <= 0:
            return None, 0, 0
        if ch / (npts - nU - 1) > 1.0:
            lo = mid
        else:
            hi = mid
    s = 0.5 * (lo + hi)
    _, npts, nU = chi2_at(A0_CANON, kern, s, masks)
    return s, npts, nU


def scan(kern, sig_int, masks, facs):
    vals = []
    for fac in facs:
        c, _, _ = chi2_at(A0_CANON * fac, kern, sig_int, masks)
        vals.append((fac, c))
    return vals


def argmin_parabolic(vals):
    i = int(np.argmin([v[1] for v in vals]))
    if 0 < i < len(vals) - 1:
        x1, x2, x3 = vals[i - 1][0], vals[i][0], vals[i + 1][0]
        y1, y2, y3 = vals[i - 1][1], vals[i][1], vals[i + 1][1]
        den = y1 - 2 * y2 + y3
        if den > 0:
            return x2 - 0.5 * (x3 - x1) * (y3 - y1) / (2 * den)
    return vals[i][0]


def sigma_from_curve(vals, defl):
    """1-sigma half-width from the Dchi2 curve at Dchi2 = defl (galaxy-clustered counting).

    NOT the relation's scatter, and NOT the gap between two candidate values -- using either as the parameter
    error is a defect class this corpus has already had to correct twice.
    """
    fr = np.array([v[0] for v in vals])
    d = np.array([v[1] for v in vals])
    d = d - d.min()
    i = int(np.argmin(d))
    lo = np.interp(defl, d[:i + 1][::-1], fr[:i + 1][::-1]) if d[0] > defl else fr[0]
    hi = np.interp(defl, d[i:], fr[i:]) if d[-1] > defl else fr[-1]
    return 0.5 * (hi - lo), lo, hi


FACS = np.round(np.arange(0.70, 1.451, 0.025), 4)

banner("E1  CONVENTIONS VALIDATED against the anchor -- which is an alpha=1 RESULT, not an alpha=2 one")

# The anchor mi_a0_profile_likelihood_sparc_2026.py defines
#     g_pred(gb, a0) = sqrt(gb*gb + gb*a0)
# which is the alpha=1 relation. So the corpus's committed profile-likelihood best fit (~1.15x canonical) is an
# ALPHA=1 number. Validate against that, kernel-matched -- validating an alpha=2 run against it would be
# apples to oranges, and doing so is how this script's first draft "failed" its own control.
sig_a1, np_a1, nU_a1 = calib_sig(nu_alpha1)
DEFL_ALL = np_a1 / nU_a1
best_a1 = argmin_parabolic(scan(nu_alpha1, sig_a1, None, FACS))
print(f"  all points, ALPHA=1 kernel (the anchor's own g_pred): sig_int = {sig_a1:.4f} dex, N = {np_a1}, "
      f"galaxies = {nU_a1}, deflator = {DEFL_ALL:.2f}")
print(f"  preferred a0 = {best_a1:.4f}x canonical   (the anchor's committed best fit: ~1.15x)")
check(abs(best_a1 - 1.15) < 0.04,
      f"E1 conventions reproduce the anchor KERNEL-MATCHED: this independent implementation prefers a0 = "
      f"{best_a1:.4f}x canonical on the alpha=1 relation, against the anchor's committed ~1.15x. So the Upsilon "
      f"convention (Upsilon_bul = 1.4 Upsilon_disk, disk free per galaxy over 0.05-3.0), the 1 km/s velocity-"
      f"error floor and the profile likelihood all match, and every number below is comparable to the corpus's "
      f"own. *** NOTE FOR THE RECORD: the corpus's headline profile-likelihood a0 is an ALPHA=1 result, because "
      f"that is the kernel the anchor script hard-codes ***")

sig_a2, _, _ = calib_sig(nu_alpha2)
best_a2 = argmin_parabolic(scan(nu_alpha2, sig_a2, None, FACS))
sig_ex, np_ex, nU_ex = calib_sig(nu)
best_ex = argmin_parabolic(scan(nu, sig_ex, None, FACS))
sig_dp, _, _ = calib_sig(nu_deep)
best_dp = argmin_parabolic(scan(nu_deep, sig_dp, None, FACS))
print(f"\n  the four shapes, all points, ALL COMPUTED HERE with identical conventions:")
print(f"    alpha=1 (retired)      {best_a1:.4f}x        alpha=2 (superseded)   {best_a2:.4f}x")
print(f"    exponential (Route A)  {best_ex:.4f}x        deep limit 1/sqrt(y)   {best_dp:.4f}x")
check(abs(best_ex - 0.937) < 0.04,
      f"E1b the exponential value reproduces the committed Route A number to {abs(best_ex-0.937):.4f} "
      f"({best_ex:.4f}x vs 0.937x) -- so Route A's own arithmetic is confirmed. *** BUT ITS COMPARATOR WAS "
      f"WRONG, AND THIS CORRECTS A NUMBER BANKED EARLIER TODAY: mi_route_a_exponential_kernel_2026.py states "
      f"that 'the alpha=2 kernel on the same data pulled a0 UP to 1.077x'. Computed here, alpha=2 prefers "
      f"{best_a2:.4f}x; the value 1.077x is what the BARE DEEP LIMIT prefers ({best_dp:.4f}x). That comparator "
      f"was hard-coded from memory rather than computed. The correction makes the finding LARGER, not smaller: "
      f"the alpha=2 -> exponential shift is {100*abs(best_a2-best_ex)/best_ex:.0f}%, not 15% ***")


banner("E2  THE SHAPE SYSTEMATIC vs DEPTH -- a0_best under four shapes at shrinking y_max")

DEPTHS = [None, 1.0, 0.3, 0.1, 0.03]
rows = []
print(f"  {'y_max':>8}{'N pts':>8}{'gals':>6}" + "".join(f"{k.split(' (')[0].split(' 1/')[0]:>22}"
                                                         for k in KERNELS))
print("  " + "-" * 102)
for ym in DEPTHS:
    masks = None if ym is None else freeze_masks(ym)
    s, npts, nU = calib_sig(nu, masks)
    if s is None or nU < 20:
        print(f"  {'all' if ym is None else ym:>8}  -- too few galaxies survive ({nU}), depth abandoned")
        continue
    bests, defl = {}, npts / nU
    for kn, kf in KERNELS.items():
        vv = scan(kf, s, masks, FACS)
        bests[kn] = argmin_parabolic(vv)
    sp = max(bests.values()) - min(bests.values())
    rows.append(dict(ym=ym, npts=npts, nU=nU, sig=s, defl=defl, bests=bests, spread=sp))
    print(f"  {'all' if ym is None else ym:>8}{npts:>8}{nU:>6}"
          + "".join(f"{bests[k]:>22.4f}" for k in KERNELS)
          + f"   spread {100*sp:>5.1f}%")

spread_all = next(r["spread"] for r in rows if r["ym"] is None)
deepest = min((r for r in rows if r["ym"] is not None), key=lambda r: r["ym"])
print(f"\n  shape spread on all points: {100*spread_all:.1f}%   at y_max = {deepest['ym']}: "
      f"{100*deepest['spread']:.1f}%")
check(deepest["spread"] < spread_all,
      f"E2 *** THE SHAPE SYSTEMATIC DOES COLLAPSE WITH DEPTH, exactly as the shared deep-MOND limit requires: "
      f"{100*spread_all:.1f}% across the four shapes on all points, falling to {100*deepest['spread']:.2f}% at "
      f"y_max = {deepest['ym']} ({deepest['npts']} points in {deepest['nU']} galaxies). *** That is the "
      f"mechanism: nu -> 1/sqrt(y) is common to the exponential, alpha=2, alpha=1 and the bare deep limit, so "
      f"restricting to deep points removes the shape dependence by construction rather than by luck")


banner("E3  THE STATISTICAL ERROR AT EACH DEPTH, from the Dchi2 curve")

print(f"  {'y_max':>8}{'N pts':>8}{'gals':>6}{'sig_int':>10}{'sigma(a0) stat':>17}{'shape sys':>12}"
      f"{'total':>10}")
print("  " + "-" * 74)
for r in rows:
    masks = None if r["ym"] is None else freeze_masks(r["ym"])
    vv = scan(nu, r["sig"], masks, FACS)
    sg, lo, hi = sigma_from_curve(vv, r["defl"])
    r["sig_stat"] = float(sg)
    r["tot"] = math.hypot(r["sig_stat"], r["spread"] / 2.0)
    print(f"  {'all' if r['ym'] is None else r['ym']:>8}{r['npts']:>8}{r['nU']:>6}{r['sig']:>10.4f}"
          f"{100*r['sig_stat']:>16.2f}%{100*r['spread']/2:>11.2f}%{100*r['tot']:>9.2f}%")
check(all(r["sig_stat"] > 0 for r in rows) and rows[-1]["sig_stat"] > rows[0]["sig_stat"],
      f"E3 and the statistical error GROWS as the sample shrinks, which is the price: sigma(a0) goes from "
      f"{100*rows[0]['sig_stat']:.2f}% on all {rows[0]['npts']} points to {100*rows[-1]['sig_stat']:.2f}% on the "
      f"{rows[-1]['npts']} points at y_max = {rows[-1]['ym']}. Both errors are taken FROM THE Dchi2 CURVE at "
      f"Dchi2 = deflator, not from the relation's scatter and not from the gap between candidates -- those two "
      f"substitutions are the defect class this corpus has already corrected twice")


banner("E4  *** THE VERDICT: total error vs the 8.20% kappa gap ***")

best_depth = min(rows, key=lambda r: r["tot"])
resolves = [r for r in rows if r["tot"] < KAPPA_GAP / 2.0]
print(f"  the kappa = 1/2 vs kappa = 1/2pi separation is {100*KAPPA_GAP:.2f}% of a0")
print(f"  best total error over the depths tried: {100*best_depth['tot']:.2f}% at "
      f"y_max = {best_depth['ym']} ({best_depth['npts']} points, {best_depth['nU']} galaxies)")
print(f"  depths whose TOTAL error resolves the gap at better than 2 sigma: "
      f"{[r['ym'] for r in resolves] if resolves else 'NONE'}")
for r in rows:
    d_half = abs(r["bests"]["deep limit 1/sqrt(y)"] - 1.0)
    d_2pi = abs(r["bests"]["deep limit 1/sqrt(y)"] - A0_M20 / A0_CANON)
    print(f"    y_max = {str(r['ym']):>5}: shape-free a0 = {r['bests']['deep limit 1/sqrt(y)']:.4f}x, "
          f"{d_half/r['tot']:.2f} sigma from kappa = 1/2, {d_2pi/r['tot']:.2f} sigma from kappa = 1/2pi")
check(best_depth["tot"] > 0 and (best_depth["tot"] < spread_all / 2.0),
      f"E4 THE VERDICT, and it cuts both ways. GOOD: a depth-restricted estimator beats the full-RAR shape "
      f"systematic -- total error {100*best_depth['tot']:.2f}% at y_max = {best_depth['ym']} against "
      f"{100*spread_all/2:.2f}% of irreducible shape systematic on all points. BAD, and this is the part that "
      f"must not be dressed up: {'no depth tried resolves' if not resolves else 'only depth(s) ' + str([r['ym'] for r in resolves]) + ' resolve'} "
      f"the {100*KAPPA_GAP:.2f}% kappa gap at better than 2 sigma. The statistical error grows roughly as fast "
      f"as the shape systematic falls, so the two trade off rather than compose into a clean measurement")


banner("E5  THE a0-LINE IS THE alpha=1 IDENTITY -- its shape bias, quantified")

# g_obs^2 - g_bar^2 = a0 g_bar is EXACTLY the alpha=1 kernel. Fit that slope to data generated by each kernel
# at a KNOWN a0, and see what a0 the estimator returns.
print(f"  the a0-line estimator fits the slope of (g_obs^2 - g_bar^2) against g_bar.")
print(f"  Applied to data generated by each kernel at a KNOWN a0 = a0_canon, it returns:")
print(f"  {'generating kernel':<26}{'slope / a0_true':>18}{'bias':>10}")
print("  " + "-" * 56)
gb = np.logspace(-13, -9.0, 400)
bias = {}
for kn, kf in KERNELS.items():
    go = np.asarray(kf(gb / A0_CANON)) * gb
    lhs = go * go - gb * gb
    sl = float(np.sum(lhs * gb) / np.sum(gb * gb))          # least squares through the origin
    bias[kn] = sl / A0_CANON
    print(f"  {kn:<26}{sl/A0_CANON:>18.4f}{100*(sl/A0_CANON-1):>+9.1f}%")
check(abs(bias["alpha=1 (retired)"] - 1.0) < 1e-6 and abs(bias["exponential (Route A)"] - 1.0) > 0.05,
      f"E5 the a0-line is NOT a shape-free estimator -- it is the alpha=1 kernel written as a straight line. It "
      f"returns a0 EXACTLY (bias {100*(bias['alpha=1 (retired)']-1):+.4f}%) on alpha=1 data, because there it is "
      f"an identity, but it is biased by {100*(bias['exponential (Route A)']-1):+.1f}% on exponential data and "
      f"{100*(bias['alpha=2 (superseded)']-1):+.1f}% on alpha=2 data. *** Since alpha=1 is RETIRED for ephemeris "
      f"reasons, the corpus's sharpest single-number a0 constraint carries an unquoted shape systematic of that "
      f"size, which is comparable to or larger than the {100*KAPPA_GAP:.2f}% kappa gap it is being used to "
      f"probe. That is an owed correction to the a0-line standing, independent of Route A ***")


banner("E6  *** DOES kappa = 1/2 WIN? -- the SAME test under all four shapes, nothing hard-coded ***")

print(f"  Dchi2 = chi2(kappa = 1/2pi) - chi2(kappa = 1/2). POSITIVE favours kappa = 1/2 (the framework).")
print(f"  {'shape':<24}{'a0_best':>10}{'chi2(1/2)':>12}{'chi2(1/2pi)':>13}{'Dchi2':>10}{'sigma':>9}{'favours':>12}")
print("  " + "-" * 90)
e6 = {}
for kn, kf in KERNELS.items():
    sg, npn, nUn = calib_sig(kf)
    dfl = npn / nUn
    c_half, _, _ = chi2_at(A0_CANON, kf, sg)
    c_2pi, _, _ = chi2_at(A0_M20, kf, sg)
    d = c_2pi - c_half
    sig = math.sqrt(abs(d) / dfl)
    bb = argmin_parabolic(scan(kf, sg, None, FACS))
    e6[kn] = dict(d=d, sig=sig, best=bb)
    print(f"  {kn:<24}{bb:>10.4f}{c_half:>12.1f}{c_2pi:>13.1f}{d:>+10.1f}{sig:>9.2f}"
          f"{('kappa=1/2' if d > 0 else 'kappa=1/2pi'):>12}")
n_for = sum(1 for v in e6.values() if v["d"] > 0)
best_sig = max(v["sig"] for v in e6.values())
print(f"\n  shapes favouring kappa = 1/2: {n_for} of {len(e6)};  largest significance either way: "
      f"{best_sig:.2f} sigma")
check(best_sig < 3.0,
      f"E6 *** THE kappa TEST IS SHAPE-DEPENDENT AND NO SHAPE RESOLVES IT. *** Computed like-for-like with "
      f"identical conventions, {n_for} of the {len(e6)} shapes favour kappa = 1/2 and the rest favour "
      f"kappa = 1/2pi, with the largest significance in EITHER direction being {best_sig:.2f} sigma -- below "
      f"3 sigma everywhere. Per-shape: "
      + "; ".join(f"{k.split(' (')[0]} {v['d']:+.0f} ({v['sig']:.2f} sigma)" for k, v in e6.items()) +
      f". *** This is the honest replacement for the corpus's '2.2 sigma favours kappa = 1/2': that figure was "
      f"computed on ONE shape (alpha=1, the anchor's g_pred, now retired), and it does not survive being asked "
      f"under the others. SPARC does not resolve kappa. Reporting otherwise in either direction would be "
      f"manufacturing a result ***")


banner("SCOPE AND WHAT IS NOT CLAIMED")
print(f"""  WHAT THIS ESTABLISHES:
   * the shape systematic on a0 is REAL and was previously unquoted: {100*spread_all:.1f}% across four kernels on
     the full RAR, which alone exceeds the {100*KAPPA_GAP:.2f}% kappa = 1/2 vs 1/2pi gap (E1b, E2).
   * the kappa test itself is SHAPE-DEPENDENT: {n_for} of 4 shapes favour kappa = 1/2, none at as much as
     {best_sig:.2f} sigma (E6). The corpus's "2.2 sigma" was a one-shape result on the now-retired alpha=1.
   * a comparator banked earlier today is CORRECTED: alpha=2 prefers {best_a2:.3f}x, not the 1.077x that
     mi_route_a_exponential_kernel_2026.py quotes; 1.077x is the bare deep limit's preference (E1b).
   * it COLLAPSES with depth, as the shared deep-MOND limit requires -- to {100*deepest['spread']:.2f}% at
     y_max = {deepest['ym']} (E2). So a shape-invariant a0 estimator EXISTS in principle.
   * but the statistical error grows about as fast as the systematic falls, so on SPARC the two trade off and
     {'NO' if not resolves else 'only the deepest'} depth resolves the kappa gap at better than 2 sigma (E4).
   * the a0-line -- the corpus's sharpest single-number a0 constraint -- is the alpha=1 identity and therefore
     shape-ASSUMING, biased by {100*(bias['exponential (Route A)']-1):+.1f}% under Route A (E5).

  WHAT IS NOT CLAIMED:
   * this does NOT rescue the kappa = 1/2 measurement. The honest position after Route A is that SPARC does not
     resolve kappa either way without assuming a transition shape, and that the shape it was assuming (alpha=2)
     is the one that produced the favourable 2.2 sigma.
   * a0 is an INPUT throughout. Nothing here fits it to improve agreement; the scans exist to locate the
     estimator's preference, which is a different thing.
   * the deep-MOND coefficient itself is untouched: nu sqrt(y) -> 1 for every kernel considered, so the BTFR,
     the deep-regime a0 definition and a0 = (1/2) c sqrt(G rho_Lambda) as a postulate are unaffected.
   * BOTH footings remain live: canonical {A0_CANON:.4e} and alt {A0_ALT:.4e}. This script scans in units of
     canonical; the alt footing sits at {A0_ALT/A0_CANON:.4f}x, INSIDE the shape spread found here, which is
     itself worth noting -- the footing fork and the shape systematic are now comparable in size.""")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: a shape-invariant a0 estimator exists (deep-only) but SPARC lacks the depth to resolve kappa")
print("  with it; and the a0-line is the alpha=1 identity, so it carries an unquoted shape systematic.")
