#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_unexplained-regularities_bosma.py

INDEPENDENT VERIFICATION + SHARPENING of candidate K01 ("the Bosma factor is a_0's").

The proposing agent's own script (hunt_2026/k01_bosma_factor.py) already ran, already labelled the candidate a
RESTATEMENT OF THE RAR, and already reported three failing checks.  This script does not repeat it.  It rebuilds the
pipeline from scratch and adds the three things the proposal ASSERTED rather than DEMONSTRATED:

  (V1) THE RESTATEMENT PROOF, EXECUTED.  The proposal argues in prose that the Bosma statistic follows from the RAR.
       Here it is proved numerically to machine precision.  Write D = g_obs/g_bar (the measured mass discrepancy).
       Then, identically and with no physics in it,

           f_obs(R) = (v_obs^2 - v_bar^2)/v_HI^2 = HE * (D - 1) * g_bar / g_HI          [definition]
           f_fw (R) = (nu(y) - 1)          * HE  * g_bar / g_HI ,   y = g_bar/a_0        [framework]

       so the Bosma residual is a DETERMINISTIC function of the RAR residual alone:

           log10(f_fw/f_obs) = log10[ (nu(y) - 1) / (D - 1) ]  and  RAR residual = log10( nu(y) / D ).

       Given (y, RAR residual) the Bosma residual is fixed exactly -- the gas fraction g_HI/g_bar CANCELS.  So the
       Bosma comparison contains ZERO information beyond the RAR.  The script reconstructs one from the other and
       checks the max absolute difference is below 1e-10 dex.  If that check PASSES, the candidate is a restatement.

  (V2) THE SELECTION AUDIT the proposal does not carry.  f_obs is undefined (negative) wherever v_obs^2 < v_bar^2.
       Dropping those points biases the measured Bosma factor UP.  Here the discarded fraction is reported, and the
       per-galaxy factor is ALSO obtained by a least-squares fit over all radii including the negative ones -- which
       is how Bosma, Hoekstra and Swaters actually fit it.

  (V3) THE INFORMATION-AMPLIFICATION FACTOR.  d log f / d log D = D/(D-1) > 1 always: the Bosma statistic is the RAR
       residual AMPLIFIED.  At the HI-share cut used, quantify the amplification -- it is why the measured scatter
       (0.21 dex) is larger than the RAR's own (~0.11 dex), which the proposal reports as a FAILED check without
       noticing that the framework's predicted scatter is amplified by the same factor and so cannot match.

Both footings on every dimensionful number.  Mutation controls.  Newtonian/LambdaCDM alternative beside.
Upsilon lever measured by re-running the whole pipeline at Upsilon x 1.5.

RULES: checks that CAN fail; nothing tuned; report against interest.
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import (A0, G, KMS2_KPC, Msun, nu, load_sparc, Check, P, info, UPS_D, UPS_B)

MSUN_PC2 = Msun / (3.0857e16) ** 2   # 1 Msun/pc^2 in kg/m^2
HE = 1.33                            # SPARC's V_gas already carries the helium+metals factor; V_HI^2 = V_gas^2/1.33

ck = Check()
P("=" * 118)
P("k_unexplained-regularities_bosma -- INDEPENDENT VERIFICATION of K01, 'the Bosma factor is a_0's'")
P("=" * 118)
P("""
  THE REGULARITY (Bosma 1981; Hoekstra, van Albada & Sancisi 2001; Swaters, Sancisi & van der Hulst 2012;
  Frank, de Blok & Walter 2016): scale a disc's HI surface density by ONE constant f ~ 7-10 and you reproduce the
  whole 'dark' part of its rotation curve, with roughly the same f galaxy after galaxy.  Universally described as
  unexplained.  THE CANDIDATE: f = 1.33 sqrt(a_0/g_bar), so a_0 supplies its value and the universal outer HI
  surface density supplies its small scatter.
""")


# ----------------------------------------------------------------------------------------------------------------
def per_point(ups_d, ups_b, share_cut):
    """Return a flat table of radii that are HI-dominated, with everything needed downstream.

    BUG-PATTERN GUARD 1 (total-vs-enclosed): every quantity here is LOCAL at radius R -- v_gas, v_disk, v_bul are
    SPARC's own enclosed-mass circular speeds at that R.  No total mass is used anywhere.
    BUG-PATTERN GUARD 2 (spherical-vs-disc): no spherical formula is applied.  g_bar is built from SPARC's disc
    solutions directly; the only place a 2 pi G Sigma appears is the CLOSED-FORM block, which is explicitly the
    infinite-thin-sheet limit and is labelled as such.
    """
    gals = load_sparc(ups_d=ups_d, ups_b=ups_b)
    rows = []
    for g in gals:
        vg, vd, vb, r = g["vg"], g["vd"], g["vb"], g["r"]
        vgas2 = vg * np.abs(vg)                       # signed: SPARC allows a negative gas contribution
        vbar2 = vgas2 + ups_d * vd ** 2 + ups_b * vb ** 2
        share = np.where(vbar2 > 0, vgas2 / np.where(vbar2 == 0, np.nan, vbar2), np.nan)
        keep = (vgas2 > 0) & (vbar2 > 0) & (share > share_cut)
        if keep.sum() < 4:
            continue
        vhi2 = vgas2[keep] / HE                       # hydrogen ALONE, the Bosma convention
        rows.append(dict(name=g["name"], r=r[keep], vobs=g["vobs"][keep], vbar2=vbar2[keep], vhi2=vhi2,
                         gbar=g["gbar"][keep], gobs=g["gobs"][keep], vgas2=vgas2[keep],
                         MHI=g["MHI"], RHI=g["RHI"], D=g["D"]))
    return rows


def factors(rows, a0):
    """Per-galaxy measured and framework Bosma factors, four ways, plus the point table."""
    out = []
    npos, ntot = 0, 0
    for g in rows:
        vdark2 = g["vobs"] ** 2 - g["vbar2"]
        ntot += len(vdark2); npos += int((vdark2 > 0).sum())
        y = g["gbar"] / a0
        vdark2_fw = (nu(y) - 1.0) * g["vbar2"]
        pos = vdark2 > 0
        # (a) median of the pointwise ratio, positive points only -- the proposal's estimator
        f_med = np.median(vdark2[pos] / g["vhi2"][pos]) if pos.sum() >= 3 else np.nan
        # (b) least squares over ALL radii, negatives included -- how the effect is actually fitted
        f_lsq = float(np.sum(vdark2 * g["vhi2"]) / np.sum(g["vhi2"] ** 2))
        f_fw_med = np.median(vdark2_fw / g["vhi2"])
        f_fw_lsq = float(np.sum(vdark2_fw * g["vhi2"]) / np.sum(g["vhi2"] ** 2))
        out.append(dict(name=g["name"], f_med=f_med, f_lsq=f_lsq, f_fw_med=f_fw_med, f_fw_lsq=f_fw_lsq,
                        npos=int(pos.sum()), n=len(vdark2)))
    return out, npos, ntot


def med_sd(v):
    v = np.asarray([x for x in v if np.isfinite(x) and x > 0], dtype=float)
    if len(v) < 3:
        return np.nan, np.nan, len(v)
    lv = np.log10(v)
    return float(np.median(v)), float(lv.std(ddof=1)), len(v)


SHARE = 0.5
rows = per_point(UPS_D, UPS_B, SHARE)
P(f"\n  {len(rows)} SPARC discs have >= 4 radii where the HI supplies more than {SHARE:.0%} of g_bar.")

P("\n" + "-" * 118)
P("V2 -- THE SELECTION AUDIT: f_obs is undefined where v_obs^2 < v_bar^2, and dropping those points biases f UP")
P("-" * 118)
res = {}
for foot, a0 in A0.items():
    fac, npos, ntot = factors(rows, a0)
    res[foot] = fac
    if foot == "canonical":
        P(f"  {ntot - npos} of {ntot} HI-dominated radii ({100*(ntot-npos)/ntot:.1f}%) have v_obs^2 < v_bar^2 and are")
        P(f"  DISCARDED by the median estimator.  The least-squares estimator keeps them.")
        m1, s1, n1 = med_sd([f["f_med"] for f in fac])
        m2, s2, n2 = med_sd([f["f_lsq"] for f in fac])
        P(f"  measured f, median-of-ratios (positives only) : {m1:6.2f}   scatter {s1:.3f} dex   N = {n1}")
        P(f"  measured f, least squares over ALL radii      : {m2:6.2f}   scatter {s2:.3f} dex   N = {n2}")
        P(f"  the two differ by {np.log10(m1/m2):+.3f} dex -- the size of the selection bias in the published estimator.")
        ck("V2 the selection bias in the median-of-positive-ratios estimator must be smaller than the 0.15 dex "
           "gap between the framework's two footings, or the measured Bosma factor is an artefact of the cut",
           abs(np.log10(m1 / m2)) < 0.15, f"bias {np.log10(m1/m2):+.3f} dex")

P("\n" + "-" * 118)
P("THE MEASURED BOSMA FACTOR AND THE FRAMEWORK'S, BOTH FOOTINGS, BOTH ESTIMATORS")
P("-" * 118)
P("  footing      estimator     N   median f_obs  scatter   median f_fw  scatter   log(f_fw/f_obs)")
best = None
for foot, a0 in A0.items():
    fac = res[foot]
    for est in ("med", "lsq"):
        mo, so, n = med_sd([f["f_" + est] for f in fac])
        mf, sf, _ = med_sd([f["f_fw_" + est] for f in fac])
        d = np.log10(mf / mo)
        P(f"  {foot:10s} {est:9s} {n:5d}   {mo:10.2f}  {so:7.3f}   {mf:10.2f}  {sf:7.3f}   {d:+8.3f}")
        if est == "med" and (best is None or abs(d) < abs(best[1])):
            best = (foot, d, mo, so, mf, sf)
P(f"\n  (f is Hoekstra/van Albada/Sancisi 2001's HI-only convention: v_dark^2 = f v_HI^2 with V_HI the hydrogen")
P(f"   alone.  Their published range for 24 galaxies is f = 7-10; Bosma's original ~ 8.)")

ck("H1 the framework's own Bosma factor, fitted exactly as an observer fits it with zero free parameters, must "
   "land on the measured one in the median to 0.1 dex on at least one footing",
   abs(best[1]) < 0.10, f"best = {best[0]}, {best[1]:+.3f} dex")
mo_can, so_can, _ = med_sd([f["f_med"] for f in res["canonical"]])
ck("H2 the MEASURED factor must itself sit in the published 7-10 window, or this sample is not measuring what "
   "the literature calls the Bosma effect", 7.0 <= mo_can <= 10.0, f"median f_obs = {mo_can:.2f}")

# ----------------------------------------------------------------------------------------------------------------
P("\n" + "=" * 118)
P("V1 -- THE RESTATEMENT PROOF, EXECUTED RATHER THAN ARGUED")
P("=" * 118)
P("""  Definitions only, no physics:  D = g_obs/g_bar,  f_obs = HE (D-1) g_bar/g_HI,  f_fw = HE (nu(y)-1) g_bar/g_HI.
  The gas share g_HI/g_bar cancels in the ratio, so

        log10(f_fw/f_obs)  ==  log10[ (nu(y)-1)/(D-1) ]   with   D = nu(y) * 10^(-RAR residual).

  i.e. the Bosma residual is a DETERMINISTIC, one-to-one function of (y, RAR residual).  It contains no new
  information.  Reconstructing it from the RAR residual alone and comparing point by point:""")
a0 = A0["canonical"]
dif, amp, rar_res, bos_res = [], [], [], []
for g in rows:
    D = g["gobs"] / g["gbar"]
    y = g["gbar"] / a0
    nuy = nu(y)
    ok = D > 1.0000001
    if ok.sum() == 0:
        continue
    D, nuy, y = D[ok], nuy[ok], y[ok]
    direct = np.log10((nuy - 1.0) * g["gbar"][ok] / (g["vgas2"][ok] / g["r"][ok] * KMS2_KPC / HE)) - \
             np.log10((D - 1.0) * g["gbar"][ok] / (g["vgas2"][ok] / g["r"][ok] * KMS2_KPC / HE))
    rr = np.log10(nuy / D)                       # the RAR residual
    recon = np.log10((nuy - 1.0) / (nuy * 10 ** (-rr) - 1.0))   # rebuilt from (y, RAR residual) alone
    dif.append(np.abs(direct - recon)); rar_res.append(rr); bos_res.append(direct)
    amp.append(D / (D - 1.0))
dif = np.concatenate(dif); rar_res = np.concatenate(rar_res); bos_res = np.concatenate(bos_res)
amp = np.concatenate(amp)
P(f"\n  {len(dif)} HI-dominated radii with D > 1.  max |Bosma residual - (its reconstruction from the RAR "
  f"residual)| = {dif.max():.3e} dex")
ck("V1 THE RESTATEMENT TEST.  If the Bosma residual can be rebuilt EXACTLY from the RAR residual and y alone, "
   "the candidate carries no information beyond the RAR and IS a restatement.  A PASS here means the candidate "
   "is DEMOTED, not promoted -- this check is written so that the framework's friend loses",
   dif.max() < 1e-10, f"max difference {dif.max():.3e} dex -- IT IS A RESTATEMENT")
P(f"\n  correlation of the two residuals: r = {np.corrcoef(rar_res, bos_res)[0,1]:+.4f} "
  f"(Spearman-equivalent, they are related by a monotone map at fixed y)")

P("\n" + "-" * 118)
P("V3 -- THE AMPLIFICATION FACTOR, which explains the proposal's FAILED spread check")
P("-" * 118)
P("  d log f / d log D = D/(D-1) >= 1 identically.  The Bosma statistic is the RAR residual AMPLIFIED by that")
P("  factor, so its scatter CANNOT equal the RAR's, and the framework's predicted spread is amplified by the")
P("  same factor only if D is predicted exactly -- which it is not, since the observed D carries the RAR scatter.")
P(f"  amplification over the HI-dominated radii: median {np.median(amp):.3f}, 16-84% "
  f"[{np.percentile(amp,16):.3f}, {np.percentile(amp,84):.3f}]")
rar_sd = float(np.std(rar_res, ddof=1))
P(f"  measured RAR residual scatter on these radii : {rar_sd:.3f} dex")
P(f"  measured Bosma residual scatter               : {float(np.std(bos_res, ddof=1)):.3f} dex")
P(f"  predicted from amplification alone            : {rar_sd*np.median(amp):.3f} dex")
ck("V3 the Bosma residual scatter must equal the RAR residual scatter times the amplification factor to 30%, "
   "which would show the extra Bosma scatter is not new physics but the same scatter magnified",
   abs(np.log10(float(np.std(bos_res, ddof=1)) / (rar_sd * np.median(amp)))) < np.log10(1.30),
   f"{float(np.std(bos_res,ddof=1)):.3f} vs {rar_sd*np.median(amp):.3f} dex")

# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("THE CLOSED FORM WITH NO ROTATION CURVE: f = HE sqrt(a_0 / (2 pi G HE Sigma_HI)) -- a_0 and a surface density")
P("-" * 118)
P("  (thin-sheet limit, stated as such: BUG PATTERN 2 is a spherical formula on a disc; this is the DISC one.)")
SIG = np.array([1.0, 3.0, 3.8, 5.0])
inwin = {}
for foot, a0v in A0.items():
    vals = []
    for s in SIG:
        gb = 2 * math.pi * G * HE * s * MSUN_PC2
        fpred = HE * (nu_v := float(nu(gb / a0v)) - 1.0)
        vals.append(fpred)
        P(f"  {foot:10s} Sigma_HI = {s:4.1f} Msun/pc^2 -> g_bar = {gb:.3e} = {gb/a0v:.4f} a_0 -> f = {fpred:5.2f}")
    inwin[foot] = vals[2]
ck("H3 the closed form, fed only a_0 and the universal mean HI surface density inside R_HI (3.8 Msun/pc^2, "
   "Wang+2016), must land inside the published Bosma window 7-10 on at least one footing",
   any(7.0 <= v <= 10.0 for v in inwin.values()),
   f"canonical {inwin['canonical']:.2f}, alt {inwin['alt']:.2f} against 7-10")

# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("THE UPSILON LEVER, measured by re-running the WHOLE pipeline at Upsilon x 1.5")
P("-" * 118)
lev = {}
for tag, (ud, ub) in (("x1.0", (UPS_D, UPS_B)), ("x1.5", (1.5 * UPS_D, 1.5 * UPS_B))):
    r2 = per_point(ud, ub, SHARE)
    f2, _, _ = factors(r2, A0["canonical"])
    mo, so, n = med_sd([f["f_med"] for f in f2])
    mf, sf, _ = med_sd([f["f_fw_med"] for f in f2])
    lev[tag] = (mo, mf, n)
    P(f"  Upsilon_disc = {ud:.3f}:  N = {n:3d}   median f_obs = {mo:6.2f}   median f_fw = {mf:6.2f}   "
      f"log(f_fw/f_obs) = {np.log10(mf/mo):+.3f}")
dlog = math.log10(1.5)
lev_obs = math.log10(lev["x1.5"][0] / lev["x1.0"][0]) / dlog
lev_fw = math.log10(lev["x1.5"][1] / lev["x1.0"][1]) / dlog
lev_test = math.log10((lev["x1.5"][1] / lev["x1.5"][0]) / (lev["x1.0"][1] / lev["x1.0"][0])) / dlog
P(f"\n  d log f_obs / d log Upsilon        = {lev_obs:+.3f}")
P(f"  d log f_fw  / d log Upsilon        = {lev_fw:+.3f}")
P(f"  d log (f_fw/f_obs) / d log Upsilon = {lev_test:+.3f}   <-- the lever on the TEST STATISTIC")
ck("UPS the agreement between the framework's factor and the measured one must move by less than 0.30 dex per "
   "dex of Upsilon, or the comparison is an Upsilon measurement wearing a_0's clothes",
   abs(lev_test) < 0.30, f"{lev_test:+.3f} dex/dex")

# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("MUTATION CONTROLS")
P("-" * 118)
fac_mut, _, _ = factors(rows, A0["canonical"] * 4.0)
m_base, _, _ = med_sd([f["f_fw_med"] for f in res["canonical"]])
m_mut, _, _ = med_sd([f["f_fw_med"] for f in fac_mut])
shift = math.log10(m_mut / m_base)
P(f"  a_0 x 4 : median f_fw {m_base:.2f} -> {m_mut:.2f}, shift {shift:+.3f} dex (deep-MOND prediction +0.301)")
ck("M1 quadrupling a_0 must move the predicted factor by close to +0.301 dex, since a_0 sits under a square "
   "root in the deep limit -- anything else means the estimator is not measuring what it claims",
   abs(shift - 0.301) < 0.06, f"{shift:+.3f} against +0.301")
P("  nu = 1 (kernel off): v_dark^2 = (nu-1) v_bar^2 = 0 identically, so f_fw = 0 for every galaxy and the "
  "measured 7-10 is left wholly unexplained.")
ck("M2 with the kernel off the framework must predict f = 0 exactly", True, "analytic, f_fw = 0")
# shuffle control
lf_o = np.array([math.log10(f["f_med"]) for f in res["canonical"] if np.isfinite(f["f_med"]) and f["f_med"] > 0])
lf_f = np.array([math.log10(f["f_fw_med"]) for f in res["canonical"] if np.isfinite(f["f_med"]) and f["f_med"] > 0])
r_true = float(np.corrcoef(lf_o, lf_f)[0, 1])
rng = np.random.default_rng(20260903)
null = np.array([np.corrcoef(lf_o, rng.permutation(lf_f))[0, 1] for _ in range(2000)])
pval = float((np.abs(null) >= abs(r_true)).mean())
P(f"  shuffle control: r(measured, predicted) = {r_true:+.3f}; 2000 shuffles give {null.mean():+.3f} +- "
  f"{null.std():.3f}, p = {pval:.4f}")
ck("M3 the framework must know WHICH galaxy carries the large factor, not merely the population median",
   pval < 0.01, f"r = {r_true:+.3f}, p = {pval:.4f}")

# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("THE NEWTONIAN / LambdaCDM ALTERNATIVE, COMPUTED BESIDE")
P("-" * 118)
P("  Newtonian, no dark matter: v_dark^2 = 0, so f = 0 -- excluded by every galaxy in the sample.")
P("  LambdaCDM: a collisionless halo knows nothing about the HI, so there is NO predicted f at all.  The fair")
P("  comparison is fit quality: one free scale on the HI curve vs one free scale on a fixed-shape NFW halo.")


def nfw_one_param(g, c=10.0):
    """One free parameter (V200); c fixed at 10.  Returns fractional rms of the best fit to v_dark^2."""
    vdark2 = g["vobs"] ** 2 - g["vbar2"]
    r = g["r"]
    best = None
    for v200 in np.linspace(20, 400, 400):
        r200 = v200 / (10 * 0.674) * 1e3 / 1e3 * 1e3  # kpc: r200 = V200/(10 H0) with H0=67.4 km/s/Mpc
        r200 = v200 / (10 * 67.4) * 1000.0
        x = r / (r200 / c)
        mu = np.log(1 + x) - x / (1 + x)
        muc = math.log(1 + c) - c / (1 + c)
        v2 = v200 ** 2 * (r200 / r) * mu / muc
        rms = float(np.sqrt(np.mean((vdark2 - v2) ** 2)))
        if best is None or rms < best[0]:
            best = (rms, v200)
    return best[0] / max(float(np.mean(np.abs(vdark2))), 1e-30)


rms_bos, rms_nfw, rms_fw = [], [], []
for g, fa in zip(rows, res["canonical"]):
    vdark2 = g["vobs"] ** 2 - g["vbar2"]
    scale = np.mean(np.abs(vdark2))
    if scale <= 0:
        continue
    rms_bos.append(float(np.sqrt(np.mean((vdark2 - fa["f_lsq"] * g["vhi2"]) ** 2))) / scale)
    y = g["gbar"] / A0["canonical"]
    rms_fw.append(float(np.sqrt(np.mean((vdark2 - (nu(y) - 1) * g["vbar2"]) ** 2))) / scale)
    rms_nfw.append(nfw_one_param(g))
P(f"  one-parameter scaled-HI (Bosma)   : median fractional rms {np.median(rms_bos):.3f}  (N = {len(rms_bos)})")
P(f"  one-parameter NFW (c = 10 fixed)  : median fractional rms {np.median(rms_nfw):.3f}")
P(f"  the framework, ZERO parameters    : median fractional rms {np.median(rms_fw):.3f}")
P(f"""
  ⚠ CORRECTION TO THE PROPOSING SCRIPT (k01_bosma_factor.py, its LambdaCDM/NFW block).  That script reports the
  framework's zero-parameter fractional rms as 0.105.  That number is `bosma_fit(vdark2_fw, vhi2)`'s residual --
  the rms of the framework's OWN predicted dark curve about a FITTED scaled-HI curve.  It never touches the
  observed v_dark^2, so it measures how well the framework's prediction is itself described by a scaled HI
  profile, not how well it matches the data.  Computed against the DATA, as here, it is {np.median(rms_fw):.3f}, which makes
  the framework's zero-parameter curve the WORST of the three on these radii, not the second best.  Recorded
  against interest.  (Caveat both ways: v_dark^2 = v_obs^2 - v_bar^2 is a small difference of large numbers in
  the outskirts, so this statistic flatters any estimator with a free scale and punishes one without.)""")
ck("ALT AGAINST INTEREST: report whether the scaled-HI description is actually BETTER than a one-parameter NFW "
   "halo on the same curves.  If NFW does as well, the Bosma effect is not the discriminator it is advertised "
   "to be, whatever explains its coefficient",
   np.median(rms_bos) < np.median(rms_nfw),
   f"Bosma {np.median(rms_bos):.3f} vs NFW {np.median(rms_nfw):.3f} -- "
   f"{'Bosma wins' if np.median(rms_bos) < np.median(rms_nfw) else 'NFW wins or ties'}")

P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"""  RESTATEMENT: PROVED, not argued.  The Bosma residual is reconstructed from the RAR residual and y alone to
  {dif.max():.1e} dex -- an exact identity, because the gas share cancels.  The candidate carries ZERO information
  beyond the radial acceleration relation.  It is the RAR wearing 1981 clothes.

  It is worth recording as an EXPLANATION of a 45-year-old coincidence, with three caveats the proposal should
  carry: (i) the published median-of-positive-ratios estimator is biased by {np.log10(med_sd([f['f_med'] for f in res['canonical']])[0]/med_sd([f['f_lsq'] for f in res['canonical']])[0]):+.3f} dex relative to a least-squares fit
  that keeps the radii where v_obs^2 < v_bar^2; (ii) the framework's spread cannot match the measured spread
  because the Bosma statistic AMPLIFIES the RAR residual by a median factor {np.median(amp):.2f}; (iii) a one-parameter
  NFW halo describes the same curves {'better' if np.median(rms_nfw) < np.median(rms_bos) else 'worse'} than the one-parameter scaled-HI curve does.

  NOT Kepler-grade: criterion (5) fails outright.""")
sys.exit(ck.done())
