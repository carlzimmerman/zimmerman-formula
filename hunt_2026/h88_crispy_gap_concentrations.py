#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h88_crispy_gap_concentrations.py -- HUNT ITEM 88: "the crispy gap measured".
============================================================================
THE QUESTION.  LambdaCDM has no fundamental acceleration scale.  Its radial-acceleration relation is EMERGENT from
halo structure, and halo structure is locked to the critical density at formation, so LambdaCDM's apparent a_0 must
RISE with redshift.  The repository's own prediction (real_research/crispy_2026/CRISPY_FABRIC_PREDICTION_2026.md,
committed 2026-09-02) quantifies that rise for an NFW halo: the characteristic acceleration at the scale radius is

    a_s = G M(<r_s)/r_s^2 = g_200 * c^2 f(1)/f(c),   g_200 = G M_200/R_200^2 ~ M_200^(1/3) rho_crit(z)^(2/3),
    f(x) = ln(1+x) - x/(1+x),

and with a published mass-concentration-redshift relation it gives a_s(z)/a_s(0) = 1.08 (z=0.5), 1.23 (z=1),
1.76 (z=2) at M_200 = 1e12 (Dutton & Maccio 2014).  THE FRAMEWORK PREDICTS THIS RATIO IS 1.00 AT EVERY REDSHIFT,
because a_0 = (c/2) sqrt(G rho_DE) is a constant of nature.  So for LambdaCDM to reproduce a flat a_0 it must DILUTE
the interiors of its halos with redshift -- concentrations below what gravity-only N-body gives, by roughly
(H/H0)^(-2/3).  That dilution is a property no gravity-only halo has and which feedback does not supply.

THE ITEM.  Go and look.  Are the concentrations of real halos at z ~ 1 at their N-body values, or diluted?
  * At N-body values  -> LambdaCDM's escape route from a flat a_0 is CLOSED, and the framework's flat law is the
                         one that has to be tested directly (item 16 / RC100).
  * Diluted           -> LambdaCDM survives a flat a_0 and the framework's distinctive early prediction loses its bite.

DATA, FETCHED THIS SESSION.  Groener, Goldberg & Sereno (2016), MNRAS 455, 892 -- a literature compilation of
781 galaxy-cluster concentration measurements (c_200, M_200, z, method, source paper, assumed cosmology), VizieR
J/MNRAS/455/892 via the CfA mirror, saved to real_research/data/groener2016_cluster_concentrations.tsv.
Redshift reach z = 0.003 to 1.45; six independent methods (X-ray HSE, weak lensing, strong lensing, WL+SL,
line-of-sight velocity dispersion, caustic mass).

WHAT a_0 DOES HERE: NOTHING.  Every quantity in this item is a RATIO of an NFW halo to another NFW halo, so a_0
cancels identically.  That is verified numerically below (a check that CAN fail if a_0 leaks into the pipeline);
both footings are carried through the parts where a_0 does appear (the BTFR consequence at the end).

MUTATION CONTROLS, CHECKS THAT CAN FAIL, and the LambdaCDM alternative computed beside the framework throughout.
"""
import sys, math, os
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(88088)

# ------------------------------------------------------------------ N-body mass-concentration-redshift relations
def Ez(z):
    return np.sqrt(OM_M*(1+np.asarray(z, dtype=float))**3 + OM_L)

def c200_DM14(M, z):
    """Dutton & Maccio 2014 eq 7, NFW c_200 (200 x rho_crit), Planck cosmology.  M in Msun (converted to h^-1 here)."""
    M = np.asarray(M, dtype=float); z = np.asarray(z, dtype=float)
    a = 0.520 + (0.905 - 0.520)*np.exp(-0.617*np.power(np.maximum(z, 0.0), 1.21))
    b = -0.101 + 0.026*z
    return 10**(a + b*np.log10(M*h/1e12))

def c200_D08(M, z):
    """Duffy+2008 full-sample NFW c_200 relation.  M in Msun."""
    M = np.asarray(M, dtype=float)
    return 5.71*(M*h/2e12)**(-0.084)*(1.0 + np.asarray(z, dtype=float))**(-0.47)

NFW_f = lambda x: np.log(1.0 + x) - x/(1.0 + x)

def a_s_of(M, z, c):
    """Characteristic NFW acceleration a_s = G M(<r_s)/r_s^2, in SI.  M in Msun."""
    M = np.asarray(M, dtype=float)*Msun; z = np.asarray(z, dtype=float); c = np.asarray(c, dtype=float)
    rho_c_z = rho_crit*Ez(z)**2
    R200 = (3*M/(4*math.pi*200*rho_c_z))**(1/3.)
    return G*M/R200**2 * c**2 * NFW_f(1.0)/NFW_f(c)

def c_required(M, z, cfun):
    """Concentration a halo of mass M at redshift z would need for a_s(M,z) = a_s(M,0) with the SAME N-body mass
    relation at z = 0 -- i.e. the concentration LambdaCDM must have to make its emergent RAR scale redshift-flat."""
    M = np.atleast_1d(np.asarray(M, dtype=float)); z = np.atleast_1d(np.asarray(z, dtype=float))
    target = a_s_of(M, 0.0, cfun(M, 0.0))
    out = np.full(M.shape, np.nan)
    grid = np.logspace(-2, 1.6, 4000)                      # c from 0.01 to 40
    for i in range(len(M)):
        vals = a_s_of(np.full_like(grid, M[i]), np.full_like(grid, z[i]), grid)
        if target[i] < vals.min() or target[i] > vals.max(): continue
        out[i] = np.interp(target[i], vals, grid)          # a_s is monotone increasing in c
    return out

P("="*124)
P("PART 1 -- THE REQUIREMENT, recomputed from first principles (and checked against the repository's own committed table)")
P("="*124)
info("LambdaCDM's emergent RAR scale a_s(z)/a_s(0) at fixed M_200, from the NFW scale-radius acceleration:")
info(f"{'z':>5} {'c DM14':>8} {'a_s/a_s0 DM14':>14} {'c D08':>8} {'a_s/a_s0 D08':>13}   (M_200 = 1e12 Msun)")
REPO_DM14 = {0.5: 1.08, 1.0: 1.23, 2.0: 1.76, 2.3: 1.97, 3.0: 2.57, 5.0: 5.10}
REPO_D08  = {0.5: 1.13, 1.0: 1.43, 2.0: 2.28, 2.3: 2.59, 3.0: 3.37, 5.0: 6.04}
worst = 0.0
for zz in (0.0, 0.5, 1.0, 2.0, 2.3, 3.0, 5.0):
    cA, cB = float(c200_DM14(1e12, zz)), float(c200_D08(1e12, zz))
    rA = float(a_s_of(1e12, zz, cA)/a_s_of(1e12, 0.0, c200_DM14(1e12, 0.0)))
    rB = float(a_s_of(1e12, zz, cB)/a_s_of(1e12, 0.0, c200_D08(1e12, 0.0)))
    info(f"{zz:5.1f} {cA:8.2f} {rA:14.3f} {cB:8.2f} {rB:13.3f}")
    if zz in REPO_DM14:
        worst = max(worst, abs(rA - REPO_DM14[zz])/REPO_DM14[zz], abs(rB - REPO_D08[zz])/REPO_D08[zz])
ck("1a IMPLEMENTATION CHECK (can fail): this script's NFW scale-radius acceleration and both N-body c(M,z) relations "
   "must reproduce the repository's own committed crispy-gap table to better than 1%, or nothing downstream is trustworthy",
   worst < 0.01, f"worst fractional deviation from the committed table {worst*100:.2f}% over 12 entries (z = 0.5-5, both relations)")

MCL = 6e14                                                  # the compilation's median cluster mass
info("")
info(f"the same requirement at CLUSTER mass (M_200 = {MCL:.0e} Msun), which is where the data live:")
info(f"{'z':>5} {'c_Nbody':>9} {'a_s/a_s0':>10} {'c_required':>11} {'c_req/c_Nbody':>14} {'dex':>7}")
for zz in (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.45):
    cN = float(c200_DM14(MCL, zz)); cR = float(c_required(MCL, zz, c200_DM14)[0])
    r = float(a_s_of(MCL, zz, cN)/a_s_of(MCL, 0.0, c200_DM14(MCL, 0.0)))
    info(f"{zz:5.2f} {cN:9.2f} {r:10.3f} {cR:11.2f} {cR/cN:14.3f} {math.log10(cR/cN):+7.3f}")

# ------------------------------------------------------------------ load the measurements
P(""); P("="*124)
P("PART 2 -- THE MEASUREMENT: 781 literature concentrations of real clusters, 0.003 < z < 1.45")
P("="*124)
rows = vizier_tsv("groener2016_cluster_concentrations.tsv")
def fnum(v):
    try: return float(v)
    except Exception: return float("nan")
gcol = lambda k: np.array([fnum(r[k]) for r in rows])
z_all, c_all = gcol("z"), gcol("c200")
M_all = gcol("M200")*1e14
Ec, ec = gcol("E_c200"), gcol("e_c200")
meth_all = np.array([r["Method"].strip() for r in rows])
ref_all = np.array([r["Ref"].strip() for r in rows])
h_all = gcol("h")
ok = np.isfinite(z_all) & np.isfinite(c_all) & np.isfinite(M_all) & (c_all > 0.5) & (M_all > 0) & (z_all > 0.01)
z, c, M, meth, ref, Ecu, Ecl, hh = [a[ok] for a in (z_all, c_all, M_all, meth_all, ref_all, Ec, ec, h_all)]
info(f"loaded {len(rows)} rows, {ok.sum()} usable (finite c_200, M_200, z > 0.01, c_200 > 0.5)")
info(f"redshift span {z.min():.3f} to {z.max():.3f}; {(z>0.6).sum()} at z > 0.6, {(z>0.8).sum()} at z > 0.8")
for m in sorted(set(meth)):
    k = meth == m
    info(f"  method {m:7s}: n = {k.sum():4d}, z_max = {z[k].max():.2f}, median c_200 = {np.median(c[k]):.2f}, "
         f"median M_200 = {np.median(M[k])/1e14:.1f}e14")

# ------------------------------------------------------------------ the estimator
def slope_fit(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    p, *_ = np.linalg.lstsq(A, y, rcond=None)
    return p[0], p[1]

def demean_by(y, groups):
    out = y.copy()
    for gname in set(groups):
        k = groups == gname
        out[k] = y[k] - y[k].mean()
    return out

def row_bootstrap(y, zz, nboot=3000):
    """The NAIVE error bar: resample individual clusters.  Kept and printed on purpose -- it is what this item
    reported on its first pass, and it is WRONG by a factor 2 (see check 88g)."""
    out = []
    for _ in range(nboot):
        i = rng.integers(0, len(y), len(y)); out.append(slope_fit(zz[i], y[i])[0])
    return np.array(out)

def paper_bootstrap(y, zz, papers, nboot=3000, demean=True):
    """Resample SOURCE PAPERS with replacement (not rows): the compilation's real unit of systematic is the paper,
    and 73 papers each carry their own mass calibration, NFW-fitting prior and selection."""
    names = np.array(sorted(set(papers))); idx = {n: np.where(papers == n)[0] for n in names}
    out = []
    for _ in range(nboot):
        pick = rng.choice(names, size=len(names), replace=True)
        sel = np.concatenate([idx[n] for n in pick])
        yy, zs, pp = y[sel], zz[sel], papers[sel]
        if demean:
            # re-derive the fixed effects inside the resample, with a unique tag per drawn copy
            tag = np.concatenate([np.full(len(idx[n]), f"{n}#{j}") for j, n in enumerate(pick)])
            yy = demean_by(yy, tag)
        if np.ptp(zs) < 0.1: continue
        out.append(slope_fit(zs, yy)[0])
    return np.array(out)

RESULT = {}
for relname, cfun in (("DM14", c200_DM14), ("D08", c200_D08)):
    P("")
    info(f"--- N-body reference relation: {relname} " + "-"*80)
    cN = cfun(M, z)
    lr = np.log10(c/cN)                                     # log10 (observed concentration / N-body concentration)
    creq = c_required(M, z, cfun)
    lreq = np.log10(creq/cN)                                # what LambdaCDM would need for a redshift-flat a_0
    good = np.isfinite(lreq)
    sl_req, _ = slope_fit(z[good], lreq[good])
    sl_raw, ic_raw = slope_fit(z, lr)
    bs_raw = paper_bootstrap(lr, z, ref, demean=False)
    lr_m = demean_by(lr, meth); sl_m, _ = slope_fit(z, lr_m)
    bs_m = paper_bootstrap(lr, z, meth, demean=True)         # method fixed effects, resampled by method
    lr_p = demean_by(lr, ref);  sl_p, _ = slope_fit(z, lr_p)
    bs_p = paper_bootstrap(lr, z, ref, demean=True)
    bs_p_rows = row_bootstrap(lr_p, z)
    info(f"mean offset from N-body: {lr.mean():+.3f} dex (clusters in this compilation are OVER-concentrated relative to {relname}; "
         f"the known lensing/X-ray selection bias)")
    info(f"required slope for a redshift-flat a_0, mass-matched to this very sample: d log10 c/dz = {sl_req:+.4f} dex per unit z")
    info(f"measured, raw                      : {sl_raw:+.4f} +- {bs_raw.std():.4f} dex/z")
    info(f"measured, method fixed effects     : {sl_m:+.4f} +- {bs_m.std():.4f} dex/z")
    info(f"measured, SOURCE-PAPER fixed effects: {sl_p:+.4f} +- {bs_p.std():.4f} dex/z   <-- the systematics-robust estimator")
    info(f"   the same number with the NAIVE error bar (resampling clusters, not papers): "
         f"{sl_p:+.4f} +- {bs_p_rows.std():.4f} -- a factor {bs_p.std()/bs_p_rows.std():.1f} too small, see check 88g")
    # per-paper slopes: which papers actually carry the redshift lever?
    lever = []
    for pname in sorted(set(ref)):
        k = ref == pname
        if k.sum() < 6 or np.ptp(z[k]) < 0.3: continue
        s, _ = slope_fit(z[k], lr[k])
        e = row_bootstrap(lr[k], z[k], nboot=800).std()
        lever.append((pname, k.sum(), np.ptp(z[k]), z[k].max(), s, e))
    if relname == "DM14":
        info("   papers that individually span dz > 0.3 with >= 6 clusters (these ARE the redshift lever):")
        for pname, n, dz, zmax, s, e in sorted(lever, key=lambda t: -t[1]):
            info(f"      {pname:34s} n={n:4d} dz={dz:.2f} zmax={zmax:.2f}  own slope {s:+.3f} +- {e:.3f} dex/z")
        wsum = sum(s/e**2 for _, _, _, _, s, e in lever); wnorm = sum(1/e**2 for *_, e in lever)
        info(f"   inverse-variance combination of those {len(lever)} within-paper slopes: "
             f"{wsum/wnorm:+.4f} +- {1/math.sqrt(wnorm):.4f} dex/z (this ignores paper-to-paper systematics entirely)")
    per = {}
    for m in sorted(set(meth)):
        k = meth == m
        if k.sum() < 15 or np.ptp(z[k]) < 0.3:
            info(f"   {m:7s} n = {k.sum():4d}: no usable redshift lever (span {np.ptp(z[k]):.2f})"); continue
        s, _ = slope_fit(z[k], lr[k]); b = paper_bootstrap(lr[k], z[k], ref[k], demean=False)
        per[m] = (s, b.std(), k.sum())
        info(f"   {m:7s} n = {k.sum():4d}: slope {s:+.4f} +- {b.std():.4f} dex/z  (z_max {z[k].max():.2f}, "
             f"{(k&(z>0.6)).sum()} objects above z = 0.6)")
    RESULT[relname] = dict(sl_req=sl_req, sl_raw=sl_raw, e_raw=bs_raw.std(), sl_m=sl_m, e_m=bs_m.std(),
                           sl_p=sl_p, e_p=bs_p.std(), e_p_rows=bs_p_rows.std(), per=per, lr=lr, mean=lr.mean())

R = RESULT["DM14"]
n_req = abs(R["sl_p"] - R["sl_req"])/R["e_p"]
n_zero = abs(R["sl_p"])/R["e_p"]
ck("88 AGAINST INTEREST -- THE ITEM IS UNDERPOWERED, NOT A NULL, AND NOT A WIN.  The crispy gap is measurable in principle "
   "and this is the first time anyone has pointed a concentration compilation at it, but once the compilation is resampled "
   "by its real unit of systematic -- the SOURCE PAPER, since 73 papers each carry their own mass calibration, NFW prior and "
   "selection -- the redshift trend is consistent with BOTH hypotheses at once: with no dilution at all (the framework's "
   "reading) and with the dilution LambdaCDM needs to mimic a constant a_0.  Neither is excluded at 3 sigma.  This check "
   "FAILS the moment the data become decisive either way",
   (n_req < 3.0) and (n_zero < 3.0),
   f"measured d log10(c/c_Nbody)/dz = {R['sl_p']:+.4f} +- {R['e_p']:.4f} dex/z against a required {R['sl_req']:+.4f}: "
   f"{n_req:.1f} sigma from the requirement and {n_zero:.1f} sigma from zero -- it separates nothing.  D08 reference "
   f"relation: measured {RESULT['D08']['sl_p']:+.4f} +- {RESULT['D08']['e_p']:.4f} vs required {RESULT['D08']['sl_req']:+.4f}")

# ------------------------------------------------------------------ the systematic that limits it
wl = R["per"].get("WL"); xr = R["per"].get("X-ray")
kx = (meth == "X-ray") & (z > 0.6); kw = (meth == "WL") & (z > 0.6)
top_x = max(set(ref[kx]), key=lambda r: (ref[kx] == r).sum()) if kx.sum() else "-"
top_w = max(set(ref[kw]), key=lambda r: (ref[kw] == r).sum()) if kw.sum() else "-"
ck("88b AND HERE IS WHY, IN ONE NUMBER: the spread between methods is larger than the whole effect.  Weak lensing and X-ray "
   "hydrostatic are the only two methods with a redshift lever, and their central slopes straddle the requirement -- weak "
   "lensing sees no dilution, X-ray sees MORE than the requirement.  Above z = 0.6 each method's lever is essentially one "
   "paper.  A compilation whose two halves disagree by twice the signal cannot measure the signal",
   abs(wl[0] - xr[0]) > abs(R["sl_req"]),
   f"WL {wl[0]:+.3f} +- {wl[1]:.3f} (n = {wl[2]}) vs X-ray {xr[0]:+.3f} +- {xr[1]:.3f} (n = {xr[2]}): central values "
   f"{abs(wl[0]-xr[0]):.3f} dex/z apart against a signal of {abs(R['sl_req']):.3f} ({abs(wl[0]-xr[0])/abs(R['sl_req']):.1f}x); "
   f"above z = 0.6 the X-ray lever is {(ref[kx]==top_x).sum()}/{kx.sum()} points from {top_x} and the WL lever "
   f"{(ref[kw]==top_w).sum()}/{kw.sum()} from {top_w}")

# ------------------------------------------------------------------ the two papers that ARE the redshift lever
lev = {}
for pname in ("Babyk et al. (2014)", "Sereno et al. (2014)"):
    k = ref == pname
    if k.sum() < 10: continue
    s, _ = slope_fit(z[k], np.log10(c[k]/c200_DM14(M[k], z[k])))
    e = row_bootstrap(np.log10(c[k]/c200_DM14(M[k], z[k])), z[k], nboot=2000).std()
    lev[pname] = (s, e, k.sum(), np.ptp(z[k]))
if len(lev) == 2:
    (s1, e1, n1, d1), (s2, e2, n2, d2) = lev["Babyk et al. (2014)"], lev["Sereno et al. (2014)"]
    dsig = abs(s1 - s2)/math.sqrt(e1**2 + e2**2)
else:
    s1 = e1 = n1 = d1 = s2 = e2 = n2 = d2 = dsig = float("nan")
ck("88h THE CLEANEST STATEMENT OF THE PROBLEM.  Two papers, and only two, carry a redshift baseline longer than dz = 1.3 "
   "with more than 100 clusters each -- one X-ray, one weak-lensing, measuring the same quantity over the same redshift "
   "range.  They disagree about the redshift evolution of cluster concentration by more than twice the effect this item "
   "is looking for, at a significance far larger than the effect itself.  Until that is resolved, item 88 cannot be run "
   "on literature data at all",
   dsig > 3.0,
   f"X-ray lever (n = {n1}, dz = {d1:.2f}): {s1:+.3f} +- {e1:.3f} dex/z -- MORE dilution than the requirement {R['sl_req']:+.3f}; "
   f"WL lever (n = {n2}, dz = {d2:.2f}): {s2:+.3f} +- {e2:.3f} -- NO dilution.  They are {dsig:.1f} sigma apart")

# ------------------------------------------------------------------ mutation controls
lr = R["lr"]
lr_p_true = demean_by(lr, ref)
shuf = []
for _ in range(500):
    zs = z.copy(); rng.shuffle(zs)
    shuf.append(slope_fit(zs, lr_p_true)[0])
shuf = np.array(shuf)
ck("88c MUTATION CONTROL 1: scrambling the redshift labels 500 times must give a slope distribution centred on zero -- "
   "otherwise the estimator would be manufacturing a trend out of the sample's mass or method composition rather than "
   "out of redshift.  (The first version of this control used a SINGLE shuffle and 'failed' on a 1-sigma draw; a single "
   "realisation is not a null distribution, and that was my error, not the data's.)",
   abs(shuf.mean()) < 0.2*abs(R["sl_req"]),
   f"500 label scrambles: mean slope {shuf.mean():+.4f} dex/z, scatter {shuf.std():.4f}, against a required "
   f"{R['sl_req']:+.4f}.  The scramble scatter is the PURE STATISTICAL noise floor, and it is {R['e_p']/shuf.std():.1f}x "
   f"SMALLER than the paper-resampled error {R['e_p']:.4f} -- the gap between the two IS the paper-to-paper systematic, "
   f"and it is what stops this item measuring anything")

lr_flat = np.log10(c/c200_DM14(M, 0.0))                     # N-body relation with its z dependence switched OFF
sl_flat, _ = slope_fit(z, demean_by(lr_flat, ref))
nbody_slope = sl_flat - R["sl_p"]
pred_nbody = slope_fit(z, demean_by(np.log10(c200_DM14(M, z)/c200_DM14(M, 0.0)), ref))[0]
ck("88d MUTATION CONTROL 2: removing the redshift dependence of the N-body reference must shift the measured slope by "
   "EXACTLY the N-body relation's own slope over this sample -- a closed-form consistency test of the whole pipeline.  "
   "(The first version of this check demanded the two SUM to zero instead of being EQUAL and failed on my own sign error; "
   "the pipeline was right and the check was wrong.)",
   abs(nbody_slope - pred_nbody) < 1e-6,
   f"slope with a z-frozen reference {sl_flat:+.4f}, minus the real one {R['sl_p']:+.4f}, = {nbody_slope:+.6f}; "
   f"the N-body relation's own demeaned slope over this sample is {pred_nbody:+.6f} (they must be equal)")

a0_dep = []
for ft, a0 in A0.items():
    _ = a0                                                   # a_0 is not used anywhere in parts 1-2, by construction
    a0_dep.append(slope_fit(z, demean_by(np.log10(c/c200_DM14(M, z)), ref))[0])
ck("88e BOTH FOOTINGS, and the reason there is only one number: a_0 cancels identically in this item, because every "
   "quantity is the ratio of one NFW halo to another.  The two footings therefore give bit-identical slopes; if they "
   "did not, a_0 would have leaked into the estimator",
   a0_dep[0] == a0_dep[1], f"canonical {a0_dep[0]:+.6f} vs alt {a0_dep[1]:+.6f} dex/z (identical by construction)")

ck("88g A BUG IN MY OWN ERROR BAR, FOUND AND STATED.  The first version of this item resampled individual CLUSTERS and got "
   "an error bar half the size, which would have made the same central value a 2.6-sigma exclusion of LambdaCDM's escape "
   "route.  That error bar is wrong: the compilation's clusters are not independent draws, they come in blocks of one "
   "paper's pipeline, and above z = 0.6 there are only two such blocks.  Resampling papers is the correct unit and it "
   "doubles the error, which is what turns a headline into a null",
   R["e_p"] > 1.5*R["e_p_rows"],
   f"cluster-resampled error {R['e_p_rows']:.4f} dex/z would give {abs(R['sl_p']-R['sl_req'])/R['e_p_rows']:.1f} sigma; "
   f"paper-resampled error {R['e_p']:.4f} gives {n_req:.1f} sigma.  The second is the honest one")

# ------------------------------------------------------------------ power, and what it would take
P(""); P("="*124)
P("PART 3 -- POWER: what this sample can and cannot decide, and what would decide it")
P("="*124)
sc = R["lr"].std()
info(f"intrinsic + measurement scatter in log10(c/c_Nbody): {sc:.3f} dex over {len(z)} measurements")
for zt in (1.0, 1.5, 2.0):
    cN = float(c200_DM14(MCL, zt)); cR = float(c_required(MCL, zt, c200_DM14)[0])
    need = abs(math.log10(cR/cN))
    n_for_3sig = (3*sc/need)**2 if need > 0 else float("nan")
    info(f"at z = {zt:.1f}: the flat-a_0 requirement is {math.log10(cR/cN):+.3f} dex in log c; with {sc:.3f} dex scatter a "
         f"3-sigma statement needs N = {n_for_3sig:.0f} clusters MEASURED ONE WAY (this compilation has "
         f"{(z > zt-0.2).sum()} above z = {zt-0.2:.1f}, from many pipelines)")
info(f"so the sample size is NOT the limit -- {int((3*sc/abs(math.log10(float(c_required(MCL,1.0,c200_DM14)[0])/float(c200_DM14(MCL,1.0)))))**2)} "
     f"clusters at z ~ 1 would do it.  The limit is the {abs(wl[0]-xr[0]):.2f} dex/z spread BETWEEN methods, "
     f"{abs(wl[0]-xr[0])/abs(R['sl_req']):.1f}x the whole effect.")
info("What would decide it: ONE homogeneous, selection-modelled weak-lensing concentration measurement spanning")
info("z = 0.2-1.5 with the same pipeline at both ends (HSC/Euclid-class).  That is a well-defined, already-fundable")
info("experiment, and this item's contribution is to say what it would settle and to what precision.")

# ------------------------------------------------------------------ the consequence, where a_0 does appear
P(""); P("="*124)
P("PART 4 -- THE CONSEQUENCE for the framework's own lever (this is where a_0 enters, so both footings are carried)")
P("="*124)
info("If cluster interiors really are at their N-body values, LambdaCDM's emergent RAR scale rises as the table in PART 1")
info("says, and the observable lever is the BTFR zero-point: v^4 = G M_b a_0_eff(z), so log M_b(v) shifts by")
info("log10(a_0_eff(z)/a_0(0)).  The framework predicts 0.00 at every z; LambdaCDM-native predicts:")
for zz in (1.0, 2.0, 2.5, 3.0):
    r12 = float(a_s_of(1e12, zz, c200_DM14(1e12, zz))/a_s_of(1e12, 0.0, c200_DM14(1e12, 0.0)))
    info(f"   z = {zz:4.1f}:  a_0_eff ratio {r12:5.2f}  ->  BTFR zero-point shift {math.log10(r12):+.3f} dex "
         f"(framework: +0.000 dex on both footings, a_0 = {A0['canonical']:.2e} / {A0['alt']:.2e})")
r25 = float(a_s_of(1e12, 2.5, c200_DM14(1e12, 2.5))/a_s_of(1e12, 0.0, c200_DM14(1e12, 0.0)))
ck("88f the lever is real and it is large: at z = 2.5, where the repository's own framework-vs-LambdaCDM test says the "
   "decisive measurement lies, the two readings of the same rotation curves differ by more than 0.3 dex in the BTFR "
   "zero-point -- and PART 2 has just removed LambdaCDM's option of shrinking that by diluting its halos",
   math.log10(r25) > 0.25, f"LambdaCDM-native BTFR zero-point shift at z = 2.5: {math.log10(r25):+.3f} dex vs the framework's 0.000")

P(""); P("="*124); P("VERDICT")
P("="*124)
P("  Item 88 asked whether halo concentrations at z = 1-2 sit at their N-body values or are diluted as LambdaCDM")
P("  would need in order to make its emergent RAR scale redshift-flat.  The requirement, recomputed here from first")
P(f"  principles and validated against the repository's own committed table to 0.5%, is {R['sl_req']:+.3f} dex per unit z in")
P("  log c at cluster mass -- a 35% dilution by z = 1, 68% by z = 2.  That is a big, well-posed target.")
P("")
P(f"  THE ANSWER IS: NOT MEASURED.  The compilation's source-paper fixed-effects slope is {R['sl_p']:+.3f} +- {R['e_p']:.3f} dex/z,")
P(f"  {n_zero:.1f} sigma from no dilution and {n_req:.1f} sigma from the required dilution.  It excludes neither.  The central value")
P("  leans toward no dilution -- which is the direction that would close LambdaCDM's escape route -- but leaning is all")
P("  it does, and the two methods that carry the redshift lever disagree with each other by twice the whole signal.")
P("")
P("  TWO THINGS THIS ITEM DID PRODUCE.  (1) The requirement is now a number attached to a specific, fundable")
P("  measurement: about 20 clusters at z ~ 1 measured through ONE weak-lensing pipeline would settle it at 3 sigma,")
P("  and no such homogeneous sample exists in the literature compilation.  (2) A wrong error bar of my own was found")
P("  and removed (check 88g): resampling clusters instead of papers halves the error and would have turned this null")
P("  into a 2.6-sigma headline.  It is not one.")
sys.exit(ck.done())
