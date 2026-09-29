#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG179 S4 -- Q-swirl: how strong may a swirl of the Lambda-vacuum be?  (FROZEN_QUESTION.md W5, G8, G5.)  Seconds.

Swirl laws (each POSTULATED; scored separately, never pooled):
  S-F  Fresnel drag lambda_c = rho_b/(rho_b + rho_Lambda)            (declared rho_b = 0.08 and 1e-3 Msun/pc^3)
  S-u  universal drag lambda_c                                          (absorbed into the fitted law; bounded by G8 only)
  S-j  spin-scaled drag lambda_c,i = lambda (j_i/median j)^p, j = 2 R_d V_flat   (SPARC; p = 1 primary, 0.5 and 2 reported)
  S-L  Lambda-scale vorticity omega = lambda a0/c (tied at lambda = 1)
  S-a0 MOND-scale vorticity omega = lambda a0/V_flat
Bounds: the RAR intrinsic scatter (gate 1.02: 0.043 dex strict edge of the 95% band, 0.048 reported) on the galaxy-to-galaxy
scatter a swirl adds; G8 (declared): co-/counter-rotation contrast <= 10^0.043 - 1 = 10.4% at g ~ a0; G5: the Solar-System
frame rotation and Coriolis push at the bound.

Read-only inputs: real_research/data/SPARC_Lelli2016c.mrt and sparc_data/*_rotmod.dat.
MUTATE=1: the spin proxy is replaced by a constant (q == 1): S-j's scatter bound must disappear.
"""
import os, math
import numpy as np
from scipy.optimize import brentq
from cfg179_common import (Run, MUTATE, REPO, A0, FOOTS, C_SI, G_SI, MSUN, PC, KPC, YR, MAS_PER_RAD, SJ_EARTH,
                           RAR_SCATTER_95, rho_lambda)

R = Run("cfg179_s4_swirl_bounds")
DATA = os.path.join(REPO, "real_research", "data")
KMS_KPC_TO_MASYR = 1e3 / KPC * YR * MAS_PER_RAD
G8_BOUND = 10 ** RAR_SCATTER_95[0] - 1.0
R.P(f"G8 declared bound: co/counter contrast <= 10^{RAR_SCATTER_95[0]} - 1 = {G8_BOUND:.4f}  (gate 1.02's 95% intrinsic scatter)")

# ------------------------------------------------------------------------------------------------ SPARC
keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat",
        "eVflat", "Q")
tab = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1"):
    tok = line.split()
    if len(tok) != 19:
        continue
    try:
        vals = [float(t) for t in tok[1:18]]
    except ValueError:
        continue
    tab[tok[0]] = dict(zip(keys, vals))
gals = []
for nm, m in sorted(tab.items()):
    if not (m["Q"] <= 2 and m["Vflat"] > 0 and m["Rdisk"] > 0 and m["Inc"] >= 30):
        continue
    fpath = os.path.join(DATA, "sparc_data", f"{nm}_rotmod.dat")
    if not os.path.exists(fpath):
        continue
    d = np.genfromtxt(fpath, comments="#")
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    Rk, Vo, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 3], d[:, 4], d[:, 5]
    ok = (Rk > 0) & (Vo > 0)
    gobs = (Vo[ok] * 1e3) ** 2 / (Rk[ok] * KPC)
    gbar = ((Vg[ok] * np.abs(Vg[ok]) + 0.5 * Vd[ok] ** 2 + 0.7 * Vb[ok] ** 2) * 1e6) / (Rk[ok] * KPC)
    gals.append(dict(name=nm, Rd=m["Rdisk"], Vf=m["Vflat"], V=Vo[ok] * 1e3, gobs=gobs, gbar=gbar))
R.P(f"SPARC sample (Q <= 2, V_flat > 0, R_d > 0, i >= 30 deg, rotmod present): N = {len(gals)} galaxies, "
    f"{sum(len(g['V']) for g in gals)} points (g_bar with Upsilon_disk 0.5, Upsilon_bul 0.7: used only for S-a0's binning)")
R.check("C1 CONTROL: the SPARC sample is non-trivial (>= 100 galaxies) and every galaxy has a spin proxy", len(gals) >= 100,
        f"N = {len(gals)}")

# =============================================================================================== S-F
R.banner("S-F  FRESNEL DRAG: the river dragged in proportion to the matter density")
SF = {}
for foot in FOOTS:
    rl = rho_lambda(foot) * PC ** 3 / MSUN
    for rb in (0.08, 1e-3):
        lc = rb / (rb + rl)
        SF[f"{foot}|{rb}"] = dict(rho_L=rl, lambda_c=lc)
        R.P(f"  {foot:9s}: rho_Lambda = {rl:.3e} Msun/pc^3; rho_b = {rb:g} -> lambda_c = 1 - {1 - lc:.2e}.  Prograde balance leaves "
            f"gravity (1 - lambda_c) V^2/R; a retrograde tracer at speed u feels a_R = -lambda_c^2 V^2/R + (|u| + lambda_c V) "
            f"lambda_c V/R - g -> net OUTWARD for every |u| (no retrograde orbit exists)")
R.check("S-F [HEADLINE] a Fresnel-like drag is excluded: lambda_c exceeds 0.999 wherever galaxies have stars or gas, so bound "
        "retrograde or counter-rotating orbits could not exist -- yet they do (counter-rotating discs, retrograde halo stars; "
        "standard knowledge, not a committed dataset)", all(v["lambda_c"] > 0.999 for v in SF.values()),
        "; ".join(f"{k}: 1 - lambda_c = {1 - v['lambda_c']:.1e}" for k, v in SF.items()))
R.num("S_F", SF)

# =============================================================================================== S-u and G8
R.banner("S-u  UNIVERSAL DRAG and the G8 co/counter-rotation bound")
lam_u = G8_BOUND / 2.0
R.P(f"  a universal lambda_c only rescales every prograde disc's radial force by 1/(1 - lambda_c): it is absorbed into the fitted")
R.P(f"  law (SPARC cannot see it).  Co/counter contrast 2 lambda_c (1 + s) V^2/R <= {G8_BOUND:.4f} V^2/R at s = 0 -> lambda_c <= "
    f"{lam_u:.4f} (s = +0.1: {G8_BOUND / 2 / 1.1:.4f}; s = -0.1: {G8_BOUND / 2 / 0.9:.4f})")
R.num("S_u", dict(lambda_c_max=lam_u))

# =============================================================================================== S-j
R.banner("S-j  SPIN-SCALED DRAG against the RAR's intrinsic scatter")
j = np.array([2 * g["Rd"] * g["Vf"] for g in gals])
jmed = float(np.median(j))
R.P(f"  j = 2 R_d V_flat: median {jmed:.0f} kpc km/s, 5-95%: {np.percentile(j, 5):.0f} - {np.percentile(j, 95):.0f}; "
    f"std log10 j = {np.std(np.log10(j)):.2f} dex")
SJ = {}
for p in (1.0, 0.5, 2.0):
    qv = np.ones_like(j) if MUTATE else (j / jmed) ** p
    lam_top = 1.0 / qv.max() * (1 - 1e-12)

    def sig(lam):
        return float(np.std(-np.log10(1 - lam * qv), ddof=1))

    out = {}
    for bound in RAR_SCATTER_95:
        if sig(lam_top) < bound:
            lmax, by = lam_top, "lambda_c -> 1 in the most spinning galaxy (scatter never reaches the bound)"
        else:
            lmax, by = brentq(lambda L: sig(L) - bound, 1e-12, lam_top), "the RAR scatter"
        out[bound] = dict(lambda_max=lmax, set_by=by, lambda_c_median=lmax, lambda_c_max_gal=lmax * qv.max(),
                          lambda_c_MW=lmax * ((2 * 2.6 * 220.0 / jmed) ** p if not MUTATE else 1.0))
    SJ[p] = out
    o = out[RAR_SCATTER_95[0]]
    R.P(f"  p = {p:.1f}: lambda_max = {o['lambda_max']:.4f} (set by {o['set_by']}); median galaxy lambda_c = "
        f"{o['lambda_c_median']:.4f}, most spinning {o['lambda_c_max_gal']:.3f}, a Milky-Way disc (R_d 2.6, 220 km/s) "
        f"{o['lambda_c_MW']:.4f};  at 0.048: lambda_max {out[RAR_SCATTER_95[1]]['lambda_max']:.4f}")
R.num("S_j", {str(k): {str(b): v for b, v in d.items()} for k, d in SJ.items()})
o1 = SJ[1.0][RAR_SCATTER_95[0]]
R.check("S-j [HEADLINE] a drag that grows with the disc's spin (p = 1) is bounded by the RAR's tightness before it saturates: "
        "the scatter it adds reaches 0.043 dex at a median-galaxy lambda_c below the G8 bound", o1["set_by"] == "the RAR scatter"
        and o1["lambda_c_median"] < lam_u, f"lambda_max = {o1['lambda_max']:.4f} (median galaxy), Milky Way {o1['lambda_c_MW']:.4f}, "
        f"most spinning {o1['lambda_c_max_gal']:.3f}; G8's universal bound {lam_u:.4f}")

# =============================================================================================== S-L and S-a0
R.banner("S-L  LAMBDA-SCALE VORTICITY (omega = lambda a0/c) and  S-a0  MOND-SCALE VORTICITY (omega = lambda a0/V_flat)")
SL, SA = {}, {}
for foot in FOOTS:
    a0 = A0[foot]

    def sig_L(lam):
        per = []
        for g in gals:
            m = g["gobs"] < a0
            if m.sum() == 0:
                continue
            per.append(np.mean(np.log10(1 + lam * a0 * g["V"][m] / (C_SI * g["gobs"][m]))))
        return float(np.std(per, ddof=1)), float(np.mean(per)), len(per)

    s1, m1, n1 = sig_L(1.0)
    lmaxL = brentq(lambda L: sig_L(L)[0] - RAR_SCATTER_95[0], 1.0, 1e7)
    SL[foot] = dict(sig_at_1=s1, mean_at_1=m1, n=n1, lambda_max=lmaxL, omega_at_1=a0 / C_SI)
    R.P(f"  S-L  {foot:9s}: at lambda = 1 (tied, no new constant) the swirl adds {s1:.1e} dex of scatter (mean shift {m1:.1e} dex, "
        f"{n1} galaxies with g_obs < a0); lambda_max = {lmaxL:.0f}")

    # S-a0 uses only points with g_bar > 0 (negative gas terms make g_bar <= 0 at a few inner points; the first run crashed
    # on their logarithm before any S-a0 number was printed: cfg179_s4_swirl_bounds_firstrun_crash.out)
    GA = [dict(V=g["V"][g["gbar"] > 0], gobs=g["gobs"][g["gbar"] > 0], gbar=g["gbar"][g["gbar"] > 0], Vf=g["Vf"])
          for g in gals if np.any(g["gbar"] > 0)]
    allg = np.concatenate([g["gbar"] for g in GA])
    edges = np.arange(np.floor(np.log10(allg.min()) * 5) / 5, np.log10(allg.max()) + 0.2, 0.2)

    def sig_A(lam):
        dd = [np.log10(1 + lam * a0 * (g["V"] / (g["Vf"] * 1e3)) / g["gobs"]) for g in GA]
        allb = np.concatenate([np.log10(g["gbar"]) for g in GA])
        alld = np.concatenate(dd)
        idx = np.digitize(allb, edges)
        mean_bin = {k: alld[idx == k].mean() for k in np.unique(idx)}
        per = []
        for g, dv in zip(GA, dd):
            ib = np.digitize(np.log10(g["gbar"]), edges)
            per.append(np.mean(dv - np.array([mean_bin[k] for k in ib])))
        return float(np.std(per, ddof=1))

    sA1 = sig_A(0.052)
    try:
        lmaxA = brentq(lambda L: sig_A(L) - RAR_SCATTER_95[0], 1e-4, 1e3)
    except ValueError:
        lmaxA = float("inf")
    SA[foot] = dict(sig_at_G8=sA1, lambda_max_scatter=lmaxA, lambda_max_G8=G8_BOUND / 2.0)
    R.P(f"  S-a0 {foot:9s}: the part not absorbed by the law (bin-detrended) adds {sA1:.1e} dex at lambda = 0.052; the scatter alone "
        f"allows lambda <= {lmaxA:.2f}; G8 (contrast 2 lambda a0/g at g = a0) allows lambda <= {G8_BOUND / 2:.4f}")
R.check("S-L [HEADLINE] the tied Lambda-scale swirl (omega = a0/c) is invisible in galaxies: at lambda = 1 it adds < 1e-3 dex of "
        "scatter on both footings", all(v["sig_at_1"] < 1e-3 for v in SL.values()),
        "; ".join(f"{f}: {SL[f]['sig_at_1']:.1e} dex, lambda_max {SL[f]['lambda_max']:.0f}" for f in FOOTS))
R.check("S-a0 (reported) a MOND-scale swirl is mostly an a0-shaped boost the law absorbs: the scatter bound is weaker than G8's",
        all(SA[f]["lambda_max_scatter"] > SA[f]["lambda_max_G8"] for f in FOOTS),
        "; ".join(f"{f}: scatter lambda <= {SA[f]['lambda_max_scatter']:.2f} vs G8 {SA[f]['lambda_max_G8']:.4f}" for f in FOOTS),
        load_bearing=False)
R.num("S_L", SL)
R.num("S_a0", SA)

# =============================================================================================== G5 at the Sun
R.banner("G5  THE SUN'S ORBIT THROUGH THE GALAXY'S SWIRL (R0 = 8.2 kpc, V = 220 km/s)")
R0, V0, uE = 8.2, 220.0, 29.78e3
GPB = 16.4                                                             # mas/yr: |39.2 - 37.2| + 2 x 7.2 (from memory; flagged)
G5 = {}
laws = [("S-u at the G8 bound (lambda_c 0.052)", lam_u * V0 / R0 * 1e3 / KPC),
        (f"S-j at its scatter bound (Milky Way lambda_c {o1['lambda_c_MW']:.4f})", o1["lambda_c_MW"] * V0 / R0 * 1e3 / KPC),
        ("S-L tied (lambda = 1, omega = a0/c), canonical", A0["canonical"] / C_SI),
        (f"S-L at its scatter bound (lambda {SL['canonical']['lambda_max']:.0f}), canonical", SL["canonical"]["lambda_max"] * A0["canonical"] / C_SI),
        ("S-a0 at the G8 bound (lambda 0.052), canonical", G8_BOUND / 2 * A0["canonical"] / (V0 * 1e3))]
for nm, om in laws:
    OmL = 0.5 * om * YR * MAS_PER_RAD
    acc = uE * om
    G5[nm] = dict(omega=om, Omega_L_masyr=OmL, coriolis_earth=acc, over_SJ=acc / SJ_EARTH, over_GPB=OmL / GPB)
    R.P(f"  {nm:62s}: omega = {om:.2e} s^-1; frame rotation omega/2 = {OmL:.2e} mas/yr ({OmL / GPB:.1e} of GP-B's allowance); "
        f"Coriolis on Earth {acc:.1e} m/s^2 = {acc / SJ_EARTH:.1e} x the 2-sigma monopole bound")
R.P("  caveats (declared in the frozen question): a uniform Coriolis field equals a frame rotation at first order, which a planetary")
R.P("  fit could partly absorb, so the monopole comparison is an estimate; GP-B's allowance is quoted from memory (frame dragging")
R.P("  37.2 +- 7.2 mas/yr vs GR 39.2) and must be verified by the data chat before any use as a verdict.")
R.num("G5", G5)
tied = G5["S-L tied (lambda = 1, omega = a0/c), canonical"]
R.check("G5 (reported) the tied Lambda-scale swirl passes the Solar System on both tests (Coriolis below the monopole bound; frame "
        "rotation far below GP-B's allowance)", tied["over_SJ"] < 1 and tied["over_GPB"] < 1,
        f"Coriolis {tied['over_SJ']:.2f} x bound; frame rotation {tied['Omega_L_masyr']:.1e} mas/yr", load_bearing=False)

R.banner("VERDICT (W5, G8, G5)")
R.P("  Fresnel-like drag (the river dragged by matter density): excluded -- retrograde orbits could not exist.")
R.P(f"  A universal drag is invisible in SPARC and bounded only by counter-rotating tracers: lambda_c <= {lam_u:.3f} (G8, declared).")
R.P(f"  A spin-scaled drag is bounded by the RAR's tightness: median-galaxy lambda_c <= {o1['lambda_c_median']:.3f} (p = 1).")
R.P(f"  The only swirl with no new constant (omega = a0/c) is allowed everywhere and invisible (~{SL['canonical']['sig_at_1']:.0e} dex).")
R.finish()
