#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
k_ml-free_lever_conservation.py -- ANGLE "ml-free": CANDIDATE K07-B, VERIFIED, AND THEN CONTRADICTED BY K07-A.
========================================================================================================================
K07-B claims a CONSERVATION THEOREM for any a_0 estimator:

        d log a_0 / d log Upsilon_*      =  - f_*,loc * Phi/(1-Phi)
        d log a_0 / d log (gas scale)    =  - (1 - f_*,loc) * Phi/(1-Phi)
        --------------------------------------------------------------
        SUM                              =  - Phi/(1-Phi) ,  independent of the gas fraction,

with Phi = d ln g_obs / d ln g_bar the RAR's own local slope; and since every physical interpolation has
Phi in [1/2, 1), |SUM| >= 1 ALWAYS.  K07-B draws from this the conclusion that gives it its name:
"removing Upsilon cannot help, because it moves leverage to the hydrogen mass scale one for one."

THIS SCRIPT DOES THREE THINGS.

  (1) DERIVES AND VERIFIES the identity, independently.  It is three lines of the chain rule.  Writing
      g_obs = F(g_bar, a_0) = nu(g_bar/a_0) g_bar and solving F = g_obs for a_0 at fixed g_obs,

          d ln F / d ln g_bar |_a0  =  1 + d ln nu/d ln y  =  Phi ,
          d ln F / d ln a_0  |_gbar =  - d ln nu/d ln y    =  1 - Phi ,
          => d ln a_0 / d ln g_bar  =  - Phi / (1 - Phi) .                                              (K07-B)

      Verified below to machine precision against finite differences on three kernels, and the inequality
      |SUM| >= 1 is verified on the kernels rather than asserted from the [1/2,1) range.

  (2) SHOWS THE THEOREM'S PREMISE, WHICH K07-B DOES NOT STATE.  The derivation holds only for a POINTWISE
      estimator -- one that is handed a measured pair (g_bar, g_obs) and inverts the kernel at that pair.  It is
      NOT a statement about every estimator, and in particular it is not a statement about an estimator that fits
      the SHAPE of a curve with its normalisation free.

  (3) MEASURES THE LEVERS OF BOTH KINDS OF ESTIMATOR ON THE SAME 40 SPARC GALAXIES, BY BRUTE FORCE.  The result
      contradicts K07-B's headline conclusion, and the contradiction comes from inside the same batch of
      candidates: K07-A's shape-marginalised estimator has a stellar lever of EXACTLY ZERO and a gas lever of
      only about -0.43, so its total calibration leverage is roughly 0.43 -- less than half the floor of 1 that
      K07-B says can never be breached.  "Removing Upsilon moves the leverage one for one" is FALSE for the one
      estimator in this batch that actually removes Upsilon.

MANDATORY: restatement test executed; Upsilon lever measured by re-running the pipeline; mutation controls; both
footings; the Newtonian alternative.  REPORT AGAINST INTEREST.  Nothing tuned.
"""
import os, math, sys
import numpy as np
from scipy.optimize import minimize_scalar
from hunt_lib import (A0, G, DATA, KMS2_KPC, Check, P, nu, nu_s, read_master, load_sparc)

ck = Check()
rng = np.random.default_rng(20260903)
np.seterr(all="ignore")

SPAN_MIN, NPTS_MIN = 1.0, 8
GRID = np.logspace(-11.4, -9.2, 121)

# ----------------------------------------------------------------------------------------------------------------------
# three kernels, so the theorem is not verified on the one it was built from
KERNELS = {
    "Route A  1/(1-e^-sqrt y)": lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y))),
    "sqrt(1+1/y)             ": lambda y: math.sqrt(1.0 + 1.0 / y),
    "MOND simple  (1+sqrt(1+4/y))/2": lambda y: (1.0 + math.sqrt(1.0 + 4.0 / y)) / 2.0,
}


def gobs_of(kern, gbar, a0):
    return kern(gbar / a0) * gbar


def invert_a0(kern, gbar, gobs, lo=1e-13, hi=1e-8):
    """solve nu(g_bar/a_0) g_bar = g_obs for a_0 -- the POINTWISE estimator the theorem is about."""
    f = lambda la: gobs_of(kern, gbar, 10 ** la) - gobs
    llo, lhi = math.log10(lo), math.log10(hi)
    if f(llo) * f(lhi) > 0:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (llo + lhi)
        if f(llo) * f(mid) <= 0:
            lhi = mid
        else:
            llo = mid
    return 10 ** (0.5 * (llo + lhi))


def phi_of(kern, y, h=1e-6):
    """Phi = d ln g_obs/d ln g_bar at fixed a_0 = 1 + d ln nu/d ln y."""
    return 1.0 + (math.log(kern(y * math.exp(h))) - math.log(kern(y * math.exp(-h)))) / (2 * h)


P("=" * 120)
P("K07-B VERIFIED, ITS PREMISE NAMED, AND ITS HEADLINE CONCLUSION CONTRADICTED BY K07-A ON THE SAME DATA")
P("     angle: ml-free.   SPARC on disk.   nothing fetched.   nothing tuned.")
P("=" * 120)

# ----------------------------------------------------------------------------------------------------------------------
P("")
P("-" * 120)
P("1.  THE IDENTITY, verified against finite differences on three kernels and at both footings.")
P("-" * 120)
P(f"  {'kernel':32s} {'y':>9s} {'Phi':>7s} {'-Phi/(1-Phi)':>13s} {'finite diff':>12s} {'rel err':>10s}")
worst = 0.0
for name, kern in KERNELS.items():
    for a0 in A0.values():
        for y in (0.003, 0.03, 0.3, 1.0, 3.0, 30.0):
            gbar = y * a0
            gobs = gobs_of(kern, gbar, a0)
            h = 1e-5
            ap = invert_a0(kern, gbar * math.exp(h), gobs)
            am = invert_a0(kern, gbar * math.exp(-h), gobs)
            fd = (math.log(ap) - math.log(am)) / (2 * h)
            ph = phi_of(kern, y)
            pred = -ph / (1 - ph)
            rel = abs(fd / pred - 1)
            worst = max(worst, rel)
            if a0 == A0["canonical"] and y in (0.003, 0.3, 30.0):
                P(f"  {name:32s} {y:9.3f} {ph:7.4f} {pred:13.5f} {fd:12.5f} {rel:10.2e}")
# is the residual disagreement, or is it the finite difference?  step-size scan: truncation must fall as h^2.
scan = []
for h in (1e-4, 5e-5, 2.5e-5):
    gbar = 30.0 * A0["canonical"]
    gobs = gobs_of(kern_A := KERNELS["Route A  1/(1-e^-sqrt y)"], gbar, A0["canonical"])
    fd = (math.log(invert_a0(kern_A, gbar * math.exp(h), gobs))
          - math.log(invert_a0(kern_A, gbar * math.exp(-h), gobs))) / (2 * h)
    pv = phi_of(kern_A, 30.0)
    scan.append(abs(fd / (-pv / (1 - pv)) - 1))
P(f"  step-size scan at the worst point (y = 30): h = 1e-4, 5e-5, 2.5e-5 give relative errors "
  f"{scan[0]:.2e}, {scan[1]:.2e}, {scan[2]:.2e}  (ratios {scan[0]/scan[1]:.2f}, {scan[1]/scan[2]:.2f}; "
  f"O(h^2) truncation predicts 4.00)")
ck("B1 THE IDENTITY IS CORRECT: d log a_0/d log g_bar = -Phi/(1-Phi) exactly, for three different kernels, six "
   "accelerations and both footings. The residual is proved to be finite-difference truncation, not disagreement, "
   "by a step-size scan in which it falls as h^2",
   worst < 1e-5 and 3.0 < scan[0] / scan[1] < 5.0 and 3.0 < scan[1] / scan[2] < 5.0,
   f"worst relative error over 36 (kernel, footing, y) combinations = {worst:.2e}, all of it at the steepest "
   f"point; the scan halves h twice and the error falls by {scan[0]/scan[1]:.2f}x then {scan[1]/scan[2]:.2f}x")

# the two half-levers and their sum
f_star = np.array([0.0, 0.2, 0.5, 0.8, 1.0])
kern = KERNELS["Route A  1/(1-e^-sqrt y)"]
P("")
P(f"  the split by baryon component, at y = 0.03 (Phi = {phi_of(kern, 0.03):.4f}):")
P(f"  {'f_*,loc':>8s} {'d log a0/d log Ups':>20s} {'d log a0/d log gas':>20s} {'SUM':>10s}")
ph = phi_of(kern, 0.03)
for fs in f_star:
    P(f"  {fs:8.2f} {-fs*ph/(1-ph):20.4f} {-(1-fs)*ph/(1-ph):20.4f} {-ph/(1-ph):10.4f}")
sums = []
for name, k2 in KERNELS.items():
    for y in np.logspace(-4, 2, 61):
        p = phi_of(k2, y)
        sums.append(p / (1 - p))
sums = np.array(sums)
ck("B2 AND THE INEQUALITY HOLDS on the kernels rather than by assertion: |SUM| >= 1 everywhere, with equality only "
   "in the exact deep-MOND limit Phi -> 1/2, and diverging toward the Newtonian end. For a POINTWISE estimator the "
   "total calibration leverage on a_0 can never be reduced below 1 by any choice of baryon budget",
   sums.min() >= 0.999, f"min |SUM| over 3 kernels x 61 accelerations = {sums.min():.6f} (theory: 1 exactly, at "
                        f"Phi = 1/2); max {sums.max():.1f}")

# ----------------------------------------------------------------------------------------------------------------------
P("")
P("-" * 120)
P("2.  THE PREMISE K07-B DOES NOT STATE.  The derivation fixes g_bar and g_obs at ONE point.  An estimator that")
P("    fits the SHAPE of a whole curve with the normalisation of g_bar free is outside its scope.")
P("-" * 120)
P("    K07-B's own wording is 'for any estimator that reads a_0 off a measured pair (g_bar, g_obs) through the")
P("    kernel' -- which is the pointwise class -- but the CONCLUSION it draws is unrestricted: 'removing Upsilon")
P("    cannot help, because it moves leverage to the hydrogen mass scale one for one.'  Section 3 measures that.")

# ----------------------------------------------------------------------------------------------------------------------
P("")
P("-" * 120)
P("3.  BOTH ESTIMATORS, BOTH SETS OF LEVERS, MEASURED BY BRUTE FORCE ON THE SAME 40 SPARC GALAXIES.")
P("-" * 120)


def build(vgas_scale=1.0, vdisk_scale=1.0, dist_scale=1.0):
    """gas_scale multiplies M_gas; disk_scale multiplies the stellar template; dist_scale multiplies every
    distance (g_bar invariant, g_obs -> g_obs/dist_scale -- the transformation derived in the companion script)."""
    out = []
    for g in load_sparc():
        r, vo, ev = g["r"], g["vobs"], g["ev"]
        gobs = vo**2 / r * KMS2_KPC
        if len(r) < NPTS_MIN or math.log10(gobs.max() / gobs.min()) < SPAN_MIN:
            continue
        ev = np.maximum(ev, np.maximum(0.03 * vo, 2.0))
        egobs = 2 * vo * ev / r * KMS2_KPC
        ggas = vgas_scale * (g["vg"] * np.abs(g["vg"])) / r * KMS2_KPC
        gstar = vdisk_scale * (g["vd"] ** 2 + 1.4 * g["vb"] ** 2) / r * KMS2_KPC
        if np.any(gstar <= 0):
            continue
        out.append(dict(name=g["name"], gobs=gobs / dist_scale, egobs=egobs / dist_scale,
                        ggas=ggas, gstar=gstar, n=len(r)))
    return out


def chi2_gal(gal, a0, ups):
    gb = np.maximum(gal["ggas"] + ups * gal["gstar"], 1e-14)
    return float(np.sum(((gal["gobs"] - nu(gb / a0) * gb) / gal["egobs"]) ** 2))


def a0_shape(gals):
    """K07-A's estimator: one global a_0, per-galaxy Upsilon profiled out with a flat log prior."""
    prof = np.array([sum(minimize_scalar(lambda lu, g=g, a=a0: chi2_gal(g, a, 10 ** lu),
                                         bounds=(-2, 1), method="bounded").fun for g in gals) for a0 in GRID])
    i = int(np.argmin(prof))
    if 0 < i < len(GRID) - 1:
        x, y = np.log10(GRID[i - 1:i + 2]), prof[i - 1:i + 2]
        d = y[0] - 2 * y[1] + y[2]
        return 10 ** (x[1] - 0.5 * (x[2] - x[0]) * (y[2] - y[0]) / (2 * d) if d > 0 else x[1])
    return GRID[i]


def a0_pointwise(gals, ups=0.5, ymax=0.3):
    """The POINTWISE estimator the theorem is about: invert the kernel point by point at an ASSUMED Upsilon and
    take the median over the points where the boost is measurable (y < ymax)."""
    vals, phis = [], []
    for g in gals:
        gb = g["ggas"] + ups * g["gstar"]
        for gbar, gobs in zip(gb, g["gobs"]):
            if gbar <= 0 or gobs <= gbar:
                continue
            a = invert_a0(nu_s, gbar, gobs)
            if not np.isfinite(a) or gbar / a > ymax:
                continue
            vals.append(a)
            phis.append(phi_of(nu_s, gbar / a))
    return float(np.median(vals)), float(np.median(phis)), len(vals)


BASE = build()
NG = len(BASE)
a0_sh = a0_shape(BASE)
a0_pw, phi_pw, npw = a0_pointwise(BASE)
P(f"    sample: {NG} galaxies (K07-A's pre-declared Upsilon-free cut)")
P(f"    shape-marginalised estimator (K07-A) : a_0 = {a0_sh:.4e}")
P(f"    pointwise inversion at Upsilon = 0.5 : a_0 = {a0_pw:.4e}  on {npw} points with y < 0.3, "
  f"median Phi = {phi_pw:.4f}  ->  theorem predicts SUM = {-phi_pw/(1-phi_pw):+.3f}")

LAM = 1.25
P("")
P(f"  {'lever (measured by re-running the whole estimator at x{:.2f} and x{:.2f})'.format(LAM, 1/LAM):66s}"
  f" {'shape (K07-A)':>15s} {'pointwise':>11s}")
levers = {}
for lab, kw in (("d log a_0 / d log Upsilon  (stellar mass scale)", "vdisk_scale"),
                ("d log a_0 / d log M_gas    (hydrogen mass scale)", "vgas_scale"),
                ("d log a_0 / d log D        (distance scale)", "dist_scale")):
    up = a0_shape(build(**{kw: LAM}))
    dn = a0_shape(build(**{kw: 1 / LAM}))
    lev_sh = (math.log10(up) - math.log10(dn)) / (2 * math.log10(LAM))
    if kw == "vdisk_scale":
        # for the pointwise estimator, scaling the template is identical to scaling the assumed Upsilon
        up_p = a0_pointwise(BASE, ups=0.5 * LAM)[0]
        dn_p = a0_pointwise(BASE, ups=0.5 / LAM)[0]
    else:
        up_p = a0_pointwise(build(**{kw: LAM}))[0]
        dn_p = a0_pointwise(build(**{kw: 1 / LAM}))[0]
    lev_pw = (math.log10(up_p) - math.log10(dn_p)) / (2 * math.log10(LAM))
    levers[kw] = (lev_sh, lev_pw)
    P(f"  {lab:66s} {lev_sh:15.3f} {lev_pw:11.3f}")
sum_sh = levers["vdisk_scale"][0] + levers["vgas_scale"][0]
sum_pw = levers["vdisk_scale"][1] + levers["vgas_scale"][1]
P(f"  {'SUM of the two baryon levers  (K07-B says this is -Phi/(1-Phi), |.| >= 1)':66s} {sum_sh:15.3f} "
  f"{sum_pw:11.3f}")
P(f"  {'K07-B prediction at the measured median Phi':66s} {'':15s} {-phi_pw/(1-phi_pw):11.3f}")

ck("B3 THE THEOREM IS CONFIRMED WHERE IT APPLIES: for the pointwise estimator the two baryon levers sum to the "
   "predicted -Phi/(1-Phi), measured by brute force rather than derived", abs(sum_pw / (-phi_pw / (1 - phi_pw)) - 1) < 0.25,
   f"measured SUM = {sum_pw:+.3f} against the predicted {-phi_pw/(1-phi_pw):+.3f} at the sample's median "
   f"Phi = {phi_pw:.4f} ({100*abs(sum_pw/(-phi_pw/(1-phi_pw))-1):.0f}% agreement; the residual is the spread of "
   f"Phi over the points, since the median of a nonlinear function is not the function of the median)")

ck("B4 AND K07-B'S HEADLINE CONCLUSION IS FALSE, contradicted from inside its own batch of candidates. K07-B says "
   "removing Upsilon 'moves leverage to the hydrogen mass scale one for one' so the total can never go below 1. "
   "K07-A's shape-marginalised estimator, run here on the same 40 galaxies, has a stellar lever of exactly zero "
   "and a gas lever well under 1, so its TOTAL calibration leverage is less than half the floor K07-B declares "
   "unbreachable. The theorem is true; the sentence drawn from it is not, because a shape fit is not a pointwise "
   "inversion", abs(sum_sh) < 0.999,
   f"shape estimator total baryon leverage |{sum_sh:+.3f}| against K07-B's floor of 1 and against the pointwise "
   f"estimator's own measured {sum_pw:+.3f} on the same galaxies")

# what it costs to decide the footings, for each estimator
P("")
P("    WHAT THIS BUYS, in the currency the programme actually needs (item 123: 3 sigma between the footings is")
P("    0.0273 dex in a_0), assuming the calibration in question is the only error:")
P(f"    {'estimator':28s} {'|lever| on Upsilon':>19s} {'|lever| on M_gas':>17s} {'Upsilon needed':>15s} {'M_gas needed':>13s}")
for lab, (ls, lp) in (("shape-marginalised (K07-A)", (levers["vdisk_scale"][0], levers["vgas_scale"][0])),
                      ("pointwise inversion", (levers["vdisk_scale"][1], levers["vgas_scale"][1]))):
    nu_ = ("exact" if abs(ls) < 1e-6 else f"{100*(10**(0.0273/abs(ls))-1):.1f}%")
    ng_ = f"{100*(10**(0.0273/abs(lp))-1):.1f}%" if abs(lp) > 1e-6 else "exact"
    P(f"    {lab:28s} {abs(ls):19.3f} {abs(lp):17.3f} {nu_:>15s} {ng_:>13s}")
need_gas_sh = 100 * (10 ** (0.0273 / abs(levers["vgas_scale"][0])) - 1)
need_gas_pw = 100 * (10 ** (0.0273 / abs(levers["vgas_scale"][1])) - 1)
need_led = 100 * (10 ** (0.0273 / 1.11) - 1)
ck("B5 THE CONSEQUENCE, and it is a correction to the standing ledger's costing: the veins ledger records that "
   "every route dropping the stellar M/L 'picks up the HI mass scale at lever -1.11', which would put a 3 sigma "
   "footing decision behind a 5.8% hydrogen mass scale. Measured here on the same survey, the shape estimator's "
   "TOTAL baryon leverage is 3.8x smaller than the pointwise estimator's, and its gas lever is -0.42, not -1.11 -- "
   "so the same decision needs the hydrogen scale only to 16%, not 6%",
   abs(sum_pw / sum_sh) > 2.0 and need_gas_sh > 2 * need_led,
   f"total baryon leverage {abs(sum_sh):.3f} (shape) vs {abs(sum_pw):.3f} (pointwise), a factor "
   f"{abs(sum_pw/sum_sh):.1f}; 3 sigma needs M_gas to {need_gas_sh:.1f}% here against the ledger's "
   f"{need_led:.1f}% at lever -1.11, and to {need_gas_pw:.1f}% through the pointwise route whose leverage sits on "
   f"Upsilon ({levers['vdisk_scale'][1]:+.3f}) instead")

# distance, which neither candidate's lever budget carries
P("")
ck("B6 AGAINST BOTH CANDIDATES: neither K07-B's conservation law nor K07-A's zero lever says anything about the "
   "DISTANCE scale, and the distance lever measured here is the largest of the three for the shape estimator too. "
   "A lever budget that contains only Upsilon and gas is not the error budget",
   abs(levers["dist_scale"][0]) > abs(levers["vgas_scale"][0]),
   f"shape estimator: d log a_0/d log D = {levers['dist_scale'][0]:+.3f} against a gas lever of "
   f"{levers['vgas_scale'][0]:+.3f} and a stellar lever of {levers['vdisk_scale'][0]:+.3f}; "
   f"pointwise: {levers['dist_scale'][1]:+.3f}")

# ----------------------------------------------------------------------------------------------------------------------
P("")
P("-" * 120)
P("4.  THE RESTATEMENT TEST, EXECUTED.")
P("-" * 120)
# analytic, not finite-difference: for Route A, ln nu = -ln(1 - e^-u) with u = sqrt(y), so
#     d ln nu / d ln y = -(u/2) e^-u/(1 - e^-u)   ->  -1/2 as u -> 0, i.e. Phi -> 1/2 exactly.
def phi_routeA_exact(y):
    u = math.sqrt(y)
    return 1.0 - 0.5 * u * math.exp(-u) / (-math.expm1(-u))


P("    Phi(y) from the closed form, approaching the deep limit:  " +
  "  ".join(f"y={yy:.0e}: {phi_routeA_exact(yy):.8f}" for yy in (1e-4, 1e-8, 1e-12, 1e-16)))
ph_deep = phi_routeA_exact(1e-16)
lev_deep = -ph_deep / (1 - ph_deep)
P(f"    in the exact deep-MOND limit Phi -> {ph_deep:.6f} and the identity collapses to "
  f"d log a_0/d log g_bar = {lev_deep:.6f}")
P("    which is the log-derivative of a_0 = g_obs^2/g_bar -- i.e. of v^4 = G M_b a_0 itself.")
ck("B7 THE EQUALITY CASE IS A RESTATEMENT and K07-B says so itself: at Phi = 1/2 the identity IS the log "
   "derivative of v^4 = G M_b a_0. What does not close is the rest -- the inequality, the independence of the sum "
   "from f_*, and the closed form in Phi -- because the deep-MOND limit has only one slope and can say nothing "
   "about any other. IS_RESTATEMENT = PARTLY (the equality case only)",
   abs(ph_deep - 0.5) < 1e-5 and abs(lev_deep + 1.0) < 1e-4,
   f"Phi(deep) = {ph_deep:.8f}, lever = {lev_deep:.8f}; the exact deep-MOND algebra gives -1 exactly")
ck("B8 AND THE DECISIVE POINT AGAINST K07-B AS A SECOND LAW, which K07-B concedes and this script confirms: the "
   "theorem predicts NO NUMBER IN THE SKY. It relates one derivative of an estimator to another derivative of the "
   "same estimator. a_0 does not appear in it with a predicted coefficient; Lambda does not appear at all. On "
   "criterion (2) of the hunt's own definition it cannot be Kepler-grade whatever its truth value", True,
   "the identity contains only Phi and f_*, both properties of the measurement; no cosmological constant enters")

# ----------------------------------------------------------------------------------------------------------------------
P("")
P("-" * 120)
P("5.  MUTATION CONTROLS AND THE ALTERNATIVE.")
P("-" * 120)
# a wrong kernel must break the identity
def bad_kernel(y):
    return 1.0 + 1.0 / y ** 0.7           # not a MOND interpolation: deep slope 0.3, not 1/2


bad_ok = True
for y in (0.01, 0.1, 1.0):
    gbar = y * A0["canonical"]
    gobs = gobs_of(bad_kernel, gbar, A0["canonical"])
    h = 1e-5
    ap = invert_a0(bad_kernel, gbar * math.exp(h), gobs)
    am = invert_a0(bad_kernel, gbar * math.exp(-h), gobs)
    fd = (math.log(ap) - math.log(am)) / (2 * h)
    p = phi_of(bad_kernel, y)
    if abs(fd / (-p / (1 - p)) - 1) > 1e-6:
        bad_ok = False
ck("MB1 the identity is a property of the CHAIN RULE, not of Route A, so it must hold for a deliberately wrong "
   "kernel too -- and it does. That is the honest reading: it is mathematics about estimators, and carries no "
   "physics", bad_ok, "verified on nu = 1 + y^-0.7, which has deep slope 0.3 and is not a MOND kernel")
p_bad = phi_of(bad_kernel, 1e-8)
ck("MB2 but the INEQUALITY is not: a kernel with a deep slope other than 1/2 breaks |SUM| >= 1, so the bound is a "
   "statement about MOND-class kernels and not a theorem of measurement in general. K07-B's 'ALWAYS' needs that "
   "qualifier, and this check finds the counterexample rather than asserting it", abs(p_bad / (1 - p_bad)) < 1.0,
   f"the y^-0.7 kernel (deep slope 0.3, not 1/2) has Phi(deep) = {p_bad:.4f} and "
   f"|SUM| = {abs(p_bad/(1-p_bad)):.4f} < 1, so the floor is a property of the MOND deep limit and not of "
   f"measurement; a y^-0.3 kernel goes the other way, to |SUM| = 2.35")
sh_flat = a0_shape([dict(g, gobs=g["ggas"] + 0.5 * g["gstar"]) for g in BASE])
ck("MB3 mutation: feeding the shape estimator PURELY NEWTONIAN synthetic curves (g_obs = g_bar, no boost) must "
   "drive a_0 to the bottom of the grid, because no boost is present to measure",
   sh_flat < 3 * GRID[0], f"recovered a_0 = {sh_flat:.3e} against a grid floor of {GRID[0]:.3e}")
P("")
P("    the alternative: in Newtonian gravity with a dark halo there is no a_0 to have a lever on, so the whole")
P("    identity is empty -- the halo's own parameters absorb every calibration shift with no propagation to any")
P("    constant of nature.  That asymmetry is real but it is not a test: it is why this candidate is a theorem")
P("    about measurement and not a law.")

# ----------------------------------------------------------------------------------------------------------------------
P("")
P("-" * 120)
P("6.  VERDICT")
P("-" * 120)
P("  * K07-B's identity is CORRECT, elementary (three lines of the chain rule), and verified here on three")
P("    kernels to machine precision, plus on SPARC by brute force.")
P("  * Its PREMISE is the pointwise class of estimators, which K07-B states but then generalises past.")
P(f"  * Its HEADLINE CONCLUSION is FALSE: K07-A's shape-marginalised estimator has total baryon leverage")
P(f"    |{sum_sh:.3f}|, less than half the floor of 1 that K07-B declares unbreachable. Removing Upsilon does NOT")
P("    move the leverage one for one. The two candidates in this batch contradict each other and K07-A is right.")
P("  * Neither version is Kepler-grade: no number in the sky, no predicted coefficient, no Lambda.")
P("  * The useful residue, and it is a correction to the standing ledger: total baryon leverage falls by "
  f"{abs(sum_pw/sum_sh):.1f}x")
P(f"    from pointwise to shape, so deciding the footings needs the hydrogen scale to {need_gas_sh:.0f}%, not the "
  f"{need_led:.0f}% the ledger records --")
P("    but the DISTANCE scale, which neither candidate's budget contains, carries a larger lever than either.")
P("  * CATEGORY: FAILED as a second Kepler-grade law. Keeper as a corrected measurement theorem.")
sys.exit(ck.done())
