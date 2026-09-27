#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG4 (part 3 of 5) -- CLUSTERS AND MERGERS: the collisionless mass the data require beyond the galaxy law, in units of the
baryons, and how it must be distributed.  Twelve X-COP clusters (the record's corrected hydrostatic audit, the rows L7 reads)
and the Bullet cluster (Clowe et al. 2006 Table 2, as the record transcribes it).

THE BASE.  a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED, flat in z; footings 9.3603e-11 / 1.1312e-10 m/s^2 (FP0).
The galaxy law of part 1 (P2 and nu_mono) applied to the cluster baryons in the spherical reading M_law(<r) =
nu(g_bar/a0) M_b(<r); a cluster's external field is negligible against its own (y_ext << y).  Where a dark component is
needed it is the framework's own field (not a particle species), and a mass is still required.

DATA (read-only): qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json (the corrected X-COP
audit: g_HSE and g_bar per radius, twelve clusters, two footings, the rows fable_independent_2026/L7_cosmic_ratio.py reads);
real_research/data/xcop/xcop_r500_ettori2019.json (R500, M500); opus_48_extended_research/reviews/bullet/bullet_data_table.py
(Clowe et al. 2006 Table 2 verbatim: positions, 100-kpc aperture plasma and stellar masses, mean convergences).  Planck 2018
Omega_c h^2 = 0.1200, Omega_b h^2 = 0.02237 for the cosmic share.

PRE-DECLARED (written before any run of this script):
  H1 CONTROLS.  (a) L7_cosmic_ratio.py, exec'd read-only, is reproduced exactly by this lane's own code on the same rows:
     twelve clusters at the outermost audited radius (median 1000 kpc = 0.80 R500), f_bar median 0.149, Newtonian
     M_dark/M_bar median 5.73 +- 0.68, the framework residual (L7's saturated nu_RAR) 3.09 +- 0.71 (canonical) / 2.76 (alt);
     (b) the record's Bullet table script, exec'd read-only, gives the offsets this lane recomputes from the same coordinates.
     EXPECT TRUE.
  H2 [HEADLINE] THE CLUSTERS NEED A DARK COMPONENT BEYOND THE LAW, AND IT IS THE COSMIC SHARE.  With the adopted kernels (P2,
     nu_mono) on both footings, the law alone falls short of X-COP's masses at the outermost audited radius by
     eta = M_HSE/M_law >= 1.5 (median), a residual M_x = M_HSE - M_law of 2-4 M_b, far from zero (>= 8 sigma on the median).
     The 'identity' reading -- the cold component carries the cosmic share Omega_c/Omega_b of the baryons and supplies the
     phantom wherever it can, so the dark mass is max(M_phantom, (Omega_c/Omega_b) M_b) -- reproduces X-COP's measured mass
     at that radius within 20% (median) on both footings for both kernels.  EXPECT TRUE.
  H3 THE DISTRIBUTION.  The residual's density falls as r^s with s in [-1.8, -1.2] over 40-750 kpc (the record's g04a -1.53,
     L41 -1.42): more concentrated than the gas.  The law removes a minority of the Newtonian dark mass at 0.8 R500 (the record
     carries both '74-89%' and '~32% at R500'; this lane measures it).  EXPECT TRUE for the slope; UNCERTAIN for the removed
     fraction.
  H4 THE HYDROSTATIC BIAS.  For b in [0, 0.2] (M_true = M_HSE/(1 - b); X-COP's own non-thermal share ~6% at R500) the
     residual stays above 1.5 M_b; no admissible b removes it (the record's L18: a rescue needs b < 0).  EXPECT TRUE.
  H5 THE BULLET.  The lensing peaks sit on the galaxies, offset from the plasma by ~150-200 kpc (main and sub), while the
     plasma apertures hold MORE baryons than the galaxy apertures; the mean-convergence contrast Delta kappa-bar at the galaxies
     implies a collisionless projected mass there of several times the aperture baryons.  EXPECT TRUE.
MUTATE=1 removes the cold component from the clusters (the dark mass is the law's phantom only): the headline H2 must FAIL
(rc = 1).

SCOPE.  Spherical hydrostatic masses as audited by the record; no temperature re-analysis; the Bullet from published aperture
numbers (no lensing map re-analysis); Sigma_crit for the Bullet from the record's own convention (z_l = 0.296, z_s = 1.0,
flat LCDM h = 0.7, Omega_m = 0.3) -- the mean-convergence DIFFERENCE is used, which the mass-sheet degeneracy does not move.

Run from the repository root:  python3 campaign_fresh_gravity/CFG4_clusters.py      (MUTATE=1 for the control run)
"""
import os
import re
import sys
import math
import json
import time
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG4_common as C
import numpy as np
from scipy.integrate import quad

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
R = C.Run("CFG4_clusters")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("PRE-DECLARED")[0].strip())
P("\nPRE-DECLARED" + __doc__.split("PRE-DECLARED")[1].split("SCOPE.")[0].rstrip())
if C.MUTATE:
    P("\n  *** MUTATE=1: the cold component is removed from the clusters (dark mass = the law's phantom only) -- H2 must FAIL ***")
A0 = C.A0
OMC_H2, OMB_H2 = 0.1200, 0.02237
COSMIC = OMC_H2 / OMB_H2                                                   # 5.364
FB_COSMIC = OMB_H2 / (OMB_H2 + OMC_H2)

# ================================================================================================ K1 L7
banner("K1  CONTROL: L7_cosmic_ratio.py (exec'd read-only) and this lane's own code on the same audited X-COP rows")
L7P = os.path.join(C.REPO, "fable_independent_2026", "L7_cosmic_ratio.py")
L7, txt7 = C.exec_slices(L7P, [(None, 'print(f"\\nRESULT:')], name="l7_readonly")     # L7 ends in sys.exit(0): stop before it
out7 = open(os.path.join(C.REPO, "fable_independent_2026", "L7_cosmic_ratio.out")).read()
AUD = json.load(open(os.path.join(C.REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026", "results.json")))
A0_AUD = AUD["a0_m_s2"]                                                    # the audit's own footings (9.3619e-11 / 1.1279e-10)
R500 = {d["name"]: d["own_R500_kpc"] for d in AUD["radius_audit"]}
G7, MS7, KPC7 = 6.674e-11, 1.989e30, 3.0857e19                             # L7's constants
ROWS = {}
for rw in AUD["rows"]:
    foot = rw.get("footing", "canonical")
    ROWS.setdefault(foot, {}).setdefault(rw["cluster"], []).append((float(rw["r_kpc"]), float(rw["g_baryon_over_a0"]) * A0_AUD[foot],
                                                                   float(rw["g_hse_over_a0"]) * A0_AUD[foot]))


def delta_l7(s):
    s = np.asarray(s, float)
    d = np.where(s > 0, s / np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)


mine7 = {}
for foot in sorted(ROWS):
    a0 = A0_AUD[foot]
    rN, rF, fb = [], [], []
    for name, pts in ROWS[foot].items():
        p_ = np.array(sorted(pts)); r = p_[:, 0] * KPC7; gb = p_[:, 1]; gh = p_[:, 2]
        Mb = gb * r ** 2 / G7; Mh = gh * r ** 2 / G7; Mk = (gb + a0 * delta_l7(gb / a0)) * r ** 2 / G7
        i = len(r) - 1
        rN.append((Mh[i] - Mb[i]) / Mb[i]); rF.append((Mh[i] - Mk[i]) / Mb[i]); fb.append(Mb[i] / Mh[i])
    mine7[foot] = dict(fb=float(np.median(fb)), fb_rng=[float(min(fb)), float(max(fb))], rN=float(np.median(rN)),
                       rN_sd=float(np.std(rN, ddof=1)), rF=float(np.median(rF)), rF_sd=float(np.std(rF, ddof=1)), n=len(rN))
m_c = re.search(r"canonical: 12 clusters.*?f_bar\s*: median ([0-9.]+).*?M_dark/M_bar\s*: median ([0-9.]+)\s*\+/- ([0-9.]+).*?M_resid/M_bar\s*: median ([0-9.]+)\s*\+/- ([0-9.]+)", out7, re.S)
ref7 = tuple(float(m_c.group(i)) for i in range(1, 6))
c7 = mine7["canonical"]
P(f"    L7 committed .out (canonical): f_bar {ref7[0]:.3f}, Newtonian {ref7[1]:.2f} +- {ref7[2]:.2f}, framework residual {ref7[3]:.2f} +- "
  f"{ref7[4]:.2f}; this lane: f_bar {c7['fb']:.3f} [{c7['fb_rng'][0]:.3f}, {c7['fb_rng'][1]:.3f}], Newtonian {c7['rN']:.2f} +- "
  f"{c7['rN_sd']:.2f}, residual {c7['rF']:.2f} +- {c7['rF_sd']:.2f} ({c7['n']} clusters); alt residual {mine7['alt']['rF']:.2f}")
L7N = {f_: float(np.median([x["ratio_N"] for x in L7["SUM"][f_]])) for f_ in L7["SUM"]}
k1 = (abs(round(c7["fb"], 3) - ref7[0]) < 1e-9 and abs(round(c7["rN"], 2) - ref7[1]) < 1e-9 and abs(round(c7["rN_sd"], 2) - ref7[2]) < 1e-9
      and abs(round(c7["rF"], 2) - ref7[3]) < 1e-9 and abs(round(c7["rF_sd"], 2) - ref7[4]) < 1e-9 and abs(round(mine7["alt"]["rF"], 2) - 2.76) < 1e-9
      and all(abs(L7N[f_] - mine7[f_]["rN"]) < 1e-12 for f_ in L7N))
check("K1 CONTROL: L7_cosmic_ratio.py (exec'd read-only) and this lane's independent code on the same audited X-COP rows agree to "
      "machine precision, and both reproduce L7's committed output (f_bar 0.149; Newtonian 5.73 +- 0.68; framework residual 3.09 +- "
      "0.71 canonical / 2.76 alt)", f"this lane: {c7['fb']:.4f}, {c7['rN']:.4f} +- {c7['rN_sd']:.4f}, {c7['rF']:.4f} +- {c7['rF_sd']:.4f}, "
      f"alt {mine7['alt']['rF']:.4f}; L7 namespace medians {L7N}", k1)
R.num("K1", dict(mine=mine7, committed_canonical=ref7))

# ================================================================================================ K2 Bullet table
banner("K2  CONTROL: the record's Bullet table (Clowe et al. 2006 Table 2, exec'd read-only) and this lane's offsets")
BT = os.path.join(C.REPO, "opus_48_extended_research", "reviews", "bullet", "bullet_data_table.py")
BNS, txtb = C.exec_slices(BT, [(None, None)], name="bullet_readonly")
KPC_AS = BNS["KPC_PER_ARCSEC"]
T2 = {lab: dict(ra=15 * (r_[0] + r_[1] / 60 + r_[2] / 3600), dec=-(abs(d_[0]) + d_[1] / 60 + d_[2] / 3600), MX=mx, eMX=emx, Ms=ms, eMs=ems,
                kb=kb, ekb=ekb) for lab, r_, d_, mx, emx, ms, ems, kb, ekb in BNS["TABLE2"]}


def sep(a, b):
    d0 = math.radians(0.5 * (T2[a]["dec"] + T2[b]["dec"]))
    dra = (T2[a]["ra"] - T2[b]["ra"]) * math.cos(d0) * 3600
    ddec = (T2[a]["dec"] - T2[b]["dec"]) * 3600
    return math.hypot(dra, ddec) * KPC_AS


off_main, off_sub = sep("Main cluster BCG", "Main cluster plasma"), sep("Subcluster BCG", "Subcluster plasma")
k2 = abs(off_main - BNS["kpc_main"]) < 1e-9 and abs(off_sub - BNS["kpc_sub"]) < 1e-9
P(f"    offsets (lensing peak = BCG/galaxies vs plasma): main {off_main:.1f} kpc (record {BNS['kpc_main']:.1f}), sub {off_sub:.1f} kpc "
  f"(record {BNS['kpc_sub']:.1f}); plate scale {KPC_AS} kpc/arcsec")
check("K2 CONTROL: the record's Bullet table script (exec'd read-only) and this lane's recomputation from the same Table 2 coordinates "
      "give the same galaxy-plasma offsets", f"main {off_main:.2f} / {BNS['kpc_main']:.2f}, sub {off_sub:.2f} / {BNS['kpc_sub']:.2f} kpc", k2)

# ================================================================================================ the law on the clusters
banner("C  THE LAW ON TWELVE X-COP CLUSTERS: eta = M_HSE/M_law, the residual beyond the law, the Newtonian dark mass, the cosmic share")
NEWT_ONLY = C.MUTATE


def cluster_table(kfun, foot, bias=0.0):
    """per cluster at the outermost audited radius: M_b, M_HSE/(1 - b), the law's mass, the residual, the removed fraction,
    and the identity reading's prediction max(phantom, cosmic share)."""
    a0 = A0[foot]
    out = []
    for name, pts in ROWS[foot].items():
        p_ = np.array(sorted(pts)); r = p_[:, 0] * C.KPC; gb = p_[:, 1]; gh = p_[:, 2] / (1.0 - bias)
        Mb = gb * r ** 2 / C.G_SI; Mh = gh * r ** 2 / C.G_SI
        Ml = kfun(gb / a0) * Mb
        Mph = Ml - Mb
        Mdark_id = Mph if NEWT_ONLY else np.maximum(Mph, COSMIC * Mb)
        Mid = Mb + Mdark_id
        i = len(r) - 1
        # residual density slope over 40-750 kpc: rho_x = dM_x/dr / (4 pi r^2)
        Mx = Mh - Ml
        rk = p_[:, 0]
        m = (rk >= 40) & (rk <= 750)
        slope = float("nan")
        if m.sum() >= 5:
            dMx = np.gradient(Mx, r)
            rho = dMx / (4 * math.pi * r ** 2)
            okr = m & (rho > 0)
            if okr.sum() >= 5:
                slope = float(np.polyfit(np.log10(rk[okr]), np.log10(rho[okr]), 1)[0])
        rhob = np.gradient(Mb, r) / (4 * math.pi * r ** 2)
        okb = m & (rhob > 0)
        slope_b = float(np.polyfit(np.log10(rk[okb]), np.log10(rhob[okb]), 1)[0]) if okb.sum() >= 5 else float("nan")
        out.append(dict(name=name, r_kpc=float(rk[i]), frac_R500=float(rk[i] / R500.get(name, np.nan)), eta=float(Mh[i] / Ml[i]),
                        resid=float((Mh[i] - Ml[i]) / Mb[i]), newt=float((Mh[i] - Mb[i]) / Mb[i]), fb=float(Mb[i] / Mh[i]),
                        removed=float((Ml[i] - Mb[i]) / (Mh[i] - Mb[i])), id_ratio=float(Mid[i] / Mh[i]), slope=slope, slope_b=slope_b,
                        phantom_over_Mb=float(Mph[i] / Mb[i])))
    return out


def summ(rows, key):
    v = np.array([r_[key] for r_ in rows], float)
    v = v[np.isfinite(v)]
    return float(np.median(v)), float(np.std(v, ddof=1)), float(np.std(v, ddof=1) / math.sqrt(len(v)))


TAB = {}
for foot in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        for b in (0.0, 0.06, 0.1, 0.2):
            TAB[(foot, kn, b)] = cluster_table(kf, foot, b)
for foot in C.FOOTS:
    for kn in ("P2", "nu_mono"):
        rows = TAB[(foot, kn, 0.0)]
        e_, r_, n_, rm_, idr_, sl_, slb_, ph_ = (summ(rows, k) for k in ("eta", "resid", "newt", "removed", "id_ratio", "slope", "slope_b",
                                                                       "phantom_over_Mb"))
        P(f"    {foot:9s} {kn:8s} (b = 0): at {np.median([x['r_kpc'] for x in rows]):.0f} kpc ({np.median([x['frac_R500'] for x in rows]):.2f} "
          f"R500): eta = {e_[0]:.3f} +- {e_[1]:.3f}; the law's phantom {ph_[0]:.2f} M_b; residual beyond the law {r_[0]:.2f} +- {r_[1]:.2f} M_b "
          f"({r_[0] / r_[2]:.0f} sigma on the median); Newtonian dark {n_[0]:.2f} +- {n_[1]:.2f} M_b (cosmic {COSMIC:.2f}); the law removes "
          f"{100 * rm_[0]:.0f}% of the Newtonian dark mass; identity reading / measured = {idr_[0]:.3f} +- {idr_[1]:.3f}; residual density "
          f"slope {sl_[0]:+.2f} +- {sl_[1]:.2f} (baryons {slb_[0]:+.2f})")
        for b in (0.06, 0.1, 0.2):
            rb = TAB[(foot, kn, b)]
            P(f"    {'':19s} b = {b:.2f}: eta {summ(rb, 'eta')[0]:.3f}, residual {summ(rb, 'resid')[0]:.2f} M_b, identity/measured "
              f"{summ(rb, 'id_ratio')[0]:.3f}")
worst = {}
for foot in C.FOOTS:
    for kn in ("P2", "nu_mono"):
        rows = TAB[(foot, kn, 0.0)]
        e_, r_, idr_ = summ(rows, "eta"), summ(rows, "resid"), summ(rows, "id_ratio")
        worst[(foot, kn)] = dict(eta=e_[0], resid=r_[0], resid_sig=r_[0] / r_[2], id_ratio=idr_[0], id_sd=idr_[1])
h2 = all(v["eta"] >= 1.5 and v["resid_sig"] >= 8 and abs(v["id_ratio"] - 1) <= 0.20 for v in worst.values())
check("H2 [HEADLINE] THE CLUSTERS NEED A DARK COMPONENT BEYOND THE LAW, AND THE COSMIC SHARE SUPPLIES IT: the law alone falls short of "
      "X-COP (median eta >= 1.5, the residual >= 8 sigma from zero on the median) while the identity reading -- dark mass = max(phantom, "
      "(Omega_c/Omega_b) M_b) -- reproduces the measured mass within 20% (median), both footings, both kernels",
      "; ".join(f"{k[0][:3]}/{k[1]}: eta {v['eta']:.2f}, residual {v['resid']:.2f} M_b ({v['resid_sig']:.0f} sigma), identity/measured "
                f"{v['id_ratio']:.3f} +- {v['id_sd']:.3f}" for k, v in worst.items()), h2)
R.num("C", {f"{k[0]}|{k[1]}|b{k[2]}": rows for k, rows in TAB.items()})
R.num("H2", {f"{k[0]}|{k[1]}": v for k, v in worst.items()})

# H3 distribution and the removed fraction
sl_all = {k: summ(TAB[(k[0], k[1], 0.0)], "slope") for k in worst}
rm_all = {k: summ(TAB[(k[0], k[1], 0.0)], "removed") for k in worst}
h3 = all(-1.8 <= v[0] <= -1.2 for v in sl_all.values())
check("H3 THE DISTRIBUTION: the residual's density falls as r^s with s in [-1.8, -1.2] over 40-750 kpc (steeper than a cored "
      "phantom, like the galaxies and the record's g04a -1.53 / L41 -1.42); the law removes the printed share of the Newtonian dark mass",
      "; ".join(f"{k[0][:3]}/{k[1]}: slope {v[0]:+.2f} +- {v[1]:.2f}, removed {100 * rm_all[k][0]:.0f}%" for k, v in sl_all.items()), h3,
      load_bearing=False,
      reading="the record carries two numbers for the removed share ('74-89%' in the category-search index line, '~32% at R500' in its "
              "body); on X-COP at 0.8 R500 with the adopted kernels it is the printed value")
R.num("H3", dict(slope={f"{k[0]}|{k[1]}": v for k, v in sl_all.items()}, removed={f"{k[0]}|{k[1]}": v for k, v in rm_all.items()}))
# H4 the hydrostatic bias
h4v = {k: summ(TAB[(k[0], k[1], 0.2)], "resid")[0] for k in worst}
h4 = all(v >= 1.5 for v in h4v.values())
check("H4 THE HYDROSTATIC BIAS: for b up to 0.2 the residual beyond the law stays >= 1.5 M_b (a positive b RAISES the true mass; no "
      "admissible b removes the residual)", "; ".join(f"{k[0][:3]}/{k[1]}: residual at b = 0.2 {v:.2f} M_b" for k, v in h4v.items()), h4,
      load_bearing=False)

# ================================================================================================ H5 the Bullet
banner("H5  THE BULLET: lensing on the galaxies, plasma offset, and the collisionless mass the contrast requires")


def DA_flat(z1, z2, Om=0.3, h=0.7):
    Hk = 100 * h / 299792.458                                                 # 1/Mpc
    chi = lambda z: quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0] / Hk
    return (chi(z2) - chi(z1)) / (1 + z2)


zl, zs = 0.296, 1.0
Dl, Ds, Dls = DA_flat(0, zl), DA_flat(0, zs), DA_flat(zl, zs)
SIGCR = C.C_SI ** 2 / (4 * math.pi * C.G_SI) * Ds / (Dl * Dls * C.MPC) / (C.MSUN / C.KPC ** 2)       # Msun/kpc^2
AP = math.pi * 100.0 ** 2
BUL = {}
for grp, gal, pla in (("main", "Main cluster BCG", "Main cluster plasma"), ("sub", "Subcluster BCG", "Subcluster plasma")):
    g_, p_ = T2[gal], T2[pla]
    dk = g_["kb"] - p_["kb"]; edk = math.hypot(g_["ekb"], p_["ekb"])
    Mb_g = (g_["MX"] + g_["Ms"]) * 1e12; Mb_p = (p_["MX"] + p_["Ms"]) * 1e12
    dM = dk * SIGCR * AP
    BUL[grp] = dict(dkappa=dk, edkappa=edk, sig=dk / edk, Mb_gal_ap=Mb_g, Mb_plasma_ap=Mb_p, dM_proj=dM, dM_over_Mb_gal=dM / Mb_g,
                    baryon_contrast=(Mb_g - Mb_p) / Mb_p, offset_kpc=off_main if grp == "main" else off_sub)
    P(f"    {grp:4s}: kappa-bar galaxies {g_['kb']:.2f} +- {g_['ekb']:.2f}, plasma {p_['kb']:.2f} +- {p_['ekb']:.2f} -> contrast {dk:+.2f} +- {edk:.2f} "
      f"({dk / edk:.1f} sigma) while the aperture baryons are {Mb_g:.2e} (galaxies) vs {Mb_p:.2e} (plasma), contrast {100 * (Mb_g - Mb_p) / Mb_p:+.0f}%; "
      f"projected mass contrast {dM:.2e} Msun = {dM / Mb_g:.1f} x the galaxy aperture's baryons (Sigma_crit {SIGCR:.3e} Msun/kpc^2)")
comb = math.hypot(BUL["main"]["sig"], BUL["sub"]["sig"])
h5 = all(100 <= v["offset_kpc"] <= 250 and v["baryon_contrast"] < 0 and v["dM_over_Mb_gal"] > 2 for v in BUL.values())
check("H5 THE BULLET: the lensing peaks sit on the galaxies ~100-250 kpc from the plasma, the plasma apertures hold MORE baryons, and "
      "the convergence contrast implies a collisionless projected mass at the galaxies of > 2x the aperture baryons (main and sub)",
      "; ".join(f"{k}: offset {v['offset_kpc']:.0f} kpc, contrast {v['sig']:.1f} sigma, collisionless {v['dM_over_Mb_gal']:.1f} x M_b(ap)"
                for k, v in BUL.items()) + f"; combined aperture contrast {comb:.1f} sigma (Clowe et al.'s full-map offset: 8 sigma)",
      h5, load_bearing=False,
      reading="the law's phantom follows the baryons, which the plasma dominates; the lensing follows the galaxies, so the component "
              "that supplies it is collisionless and rides with the galaxies through the collision")
R.num("H5", dict(bullet=BUL, Sigma_crit_Msun_kpc2=SIGCR, combined_sigma=comb))

# ================================================================================================ W ledger
banner("W  THE LEDGER: part 3 (clusters and mergers)")
wc = worst[("canonical", "nu_mono")]; wa = worst[("alt", "nu_mono")]
R.ledger("X1", "MEASURED", f"X-COP at 0.8 R500: the law alone short by eta = {wc['eta']:.2f} / {wa['eta']:.2f} (nu_mono, can/alt); "
         f"residual {wc['resid']:.2f} / {wa['resid']:.2f} M_b", "H2")
R.ledger("X2", "MEASURED", f"the Newtonian dark mass {c7['rN']:.2f} +- {c7['rN_sd']:.2f} M_b = {c7['rN'] / COSMIC:.2f} x the cosmic "
         f"Omega_c/Omega_b = {COSMIC:.2f}; f_b {c7['fb']:.3f} vs cosmic {FB_COSMIC:.3f}", "K1")
R.ledger("X3", "CONSTRAINT", f"the residual is distributed as rho_x ~ r^{sl_all[('canonical', 'nu_mono')][0]:.2f} (40-750 kpc), "
         f"collisionless (the Bullet: lensing on the galaxies, offsets {off_main:.0f} / {off_sub:.0f} kpc)", "H3, H5")
R.ledger("X4", "DERIVED", f"identity reading (dark = max(phantom, cosmic share)) / measured = {wc['id_ratio']:.3f} / {wa['id_ratio']:.3f}", "H2")
check("W (reported) the ledger of part 3", f"{len(R.OUT['ledger'])} rows", True, load_bearing=False)
sys.exit(R.finish())
