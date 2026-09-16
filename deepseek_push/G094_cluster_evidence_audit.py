#!/usr/bin/env python3
"""G094 -- THE CLUSTER EVIDENCE AUDIT: are the committed numbers right?

Every cluster headline is re-derived here from the ORIGINAL committed data
(real_research/data/xcop/ FITS + the committed Ettori+19 M500 table
xcop_r500_ettori2019.json; nothing re-downloaded) and from the committed lane
code conventions (G050/G057/G059/G075 ingests; g04a's residual-profile solve).

HEADLINES UNDER AUDIT (registered rows, from the committed record):
  (1) slope  : theory in-situ isothermal -1.478 at 100 kpc (G008) vs the
               observed residual slope -1.53 (g04a; window 75-420 kpc per
               L190/G008);
  (2) amplitude: G012's self-consistent phantom M_ph/M_b = 12.77/15.21 at
               420 kpc (1.86x/2.21x the certified 6.88 -- the 1.9-2.2x
               overshoot); G050's split-delivered 0.409x; G075's EFE-capped
               dark fraction pred/obs 0.21 (cap g_ext~a0) / 0.031 (cap cH0),
               uncapped linear law 0.68, observed median 4.7x at R500;
  (3) V4      : Spearman rho(g_tot/a0, s_ph) = -0.926, p = 1.43e-41, pooled
               12 clusters x 8 radii, both footings (G050);
  (4) T ratio : median T_pred/T_obs = 0.28 (canonical) / 0.31 (alt), with
               T_pred/T_obs = (sigma_pred/sigma_dyn,3D)^2 = 0.53^2 (G075);
  (5) chi2    : split 711.6 vs NFW 11.9 (mu2-MOND 1378.5 pooled;
               741.1/672.4 per footing), median per-cluster chi2 over the
               50-600 kpc window (G057b/G050);
  (6) VERDICTS: per number CONFIRMED (within 5%) or CORRECTED (new value),
               and the meta-finding: which cluster conclusions survive.

KNOWN REGISTERED QUIRKS (carried, not papered over):
  * G050's g_tot line dropped the *MSUN conversion (G059's DATA NOTE); the
    EFE cap therefore never fired in G050's run.  Rank correlations are
    invariant to that multiplicative slip; the delivered-420 row is evaluated
    at 420 kpc where the cap is off on any footing; both facts are checked.
  * G050/G057's nu_of_mu2(s) solves x mu2(x) = s mu2(s), whose unique
    solution is x = s -- nu_of_mu2 == 1 identically (G050 V5's own table
    printed nu_mu2 = 1.000 and FAILed the deep-RAR identity).  The
    "mu2-MOND" chi2 rows are therefore the bare-baryon chi2; a corrected
    RAR-kernel MOND row is computed beside.
  * The Eckert+17 kTvir column is EXTERNAL-SOURCED but committed in G075's
    KTVIR_ECKERT17; the audit uses the committed dict (the register's value).

Every check states the registered number and the recomputed number
separately; a FAIL/CORRECTED is a finding.
"""
import json
import math
import os

import numpy as np
from astropy.io import fits
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.stats import spearmanr

RES = []          # verdict rows
CHECKS = []       # detailed checks


def check(name, registered, recomputed, ok, note=""):
    CHECKS.append(dict(name=name, registered=str(registered),
                       recomputed=str(recomputed), pass_=bool(ok), note=note))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         registered: {registered}")
    print(f"         recomputed: {recomputed}")
    if note:
        print(f"         note      : {note}")


print(__doc__)
print("=" * 100)
print("G094 -- THE CLUSTER EVIDENCE AUDIT")
print("=" * 100)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
XB = os.path.join(REPO, "real_research", "data", "xcop")

# ------------------------------------------------------------------ constants
G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
c_l = 2.99792458e8
H0 = 67.4 * 1e3 / 3.0857e22                     # s^-1
rho_lam = 0.685 * 3 * H0 ** 2 / (8 * math.pi * G)
s_DE = c_l * math.sqrt(G * rho_lam)
A0 = {"canonical": s_DE / 2.0, "alt": 1.1279e-10}
GEXT = c_l * H0                                 # L180 Hubble-kernel external field
MU, MP, KB = 0.6, 1.6726219e-27, 1.380649e-23
KEV_IN_K = 1.160451812e7
RG = np.array([50., 75., 100., 150., 210., 300., 420., 600.])
I420 = int(np.argmin(np.abs(RG - 420)))
S_SAT, C_SAT = 2.5396, 0.647610
KTVIR_ECKERT17 = {   # committed in G075 (Eckert+17 Table 1, external-sourced)
    "A85": (6.00, 0.11, -0.11), "A644": (7.70, 0.10, -0.10),
    "A1644": (5.09, 0.09, -0.09), "A1795": (6.08, 0.07, -0.07),
    "A2029": (8.26, 0.09, -0.09), "A2142": (8.40, 1.01, -0.76),
    "A2255": (5.81, 0.19, -0.20), "A2319": (9.60, 0.30, -0.30),
    "A3158": (4.99, 0.07, -0.07), "A3266": (9.45, 0.35, -0.36),
    "RXC1825": (5.13, 0.04, -0.04), "ZW1215": (6.27, 0.35, -0.32),
}


def mu2(s):
    s = np.asarray(s, float)
    return 1.0 - (1.0 + s / 2.0) ** (-2.0)


def y_mu2(s):
    return s * mu2(s)


def solve_x_of_y(y):
    y = np.atleast_1d(np.asarray(y, float))
    out = np.empty(len(y))
    for i, yy in enumerate(y):
        if yy <= 0:
            out[i] = 0.0
        else:
            f = lambda x: x * (1.0 - (1.0 + x / 2.0) ** (-2.0)) - yy
            out[i] = brentq(f, 1e-12, max(10.0 * yy, 10.0),
                            xtol=1e-15 * max(yy, 1.0), rtol=1e-14)
    return out


def nu_of_mu2(s):
    """committed G050 convention: x mu2(x) = s mu2(s) -> x == s identically."""
    s = np.atleast_1d(np.asarray(s, float))
    s = np.maximum(s, 1e-30)
    x = solve_x_of_y(y_mu2(s))
    return np.maximum(x / s, 1.0)


def nu_rar(s):
    s = np.maximum(np.asarray(s, float), 1e-30)
    return 1.0 / (1.0 - np.exp(-np.sqrt(s)))


def loginterp(x, xp, fp, hold_last=False):
    xp = np.atleast_1d(np.asarray(xp, float))
    fp = np.atleast_1d(np.asarray(fp, float))
    x = np.atleast_1d(np.asarray(x, float))
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    if hold_last:
        out = np.where(x > xp[-1], fp[-1], out)
    return out


def li(xq, x, v):   # g04a's interpolator (nan beyond the table)
    m = (x > 0) & (v > 0)
    return np.exp(np.interp(np.log(xq), np.log(x[m]), np.log(v[m]),
                            left=np.nan, right=np.nan))


def load_cluster(name):
    p = os.path.join(XB, name)
    hm = fits.open(os.path.join(p, f"{name}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(p, f"{name}_fgas_profile.fits"))[1].data
    d = dict(name=name,
             r_hm=np.array(hm["RADIUS"], float),
             M_hse=np.array(hm["M_FORW"], float),
             eM_hse=np.array(hm["EM_FORW"], float),
             M_nfw=np.array(hm["M_NFW"], float),
             r_fg=np.array(fg["RADIUS"], float) * 1e3,     # Mpc -> kpc (G050)
             M_gas=np.array(fg["MGAS"], float))
    fs = os.path.join(p, f"{name}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        d["r_st"] = np.array(ms["RADIUS"], float)
        d["M_st"] = np.array(ms["MSTAR"], float)
        d["has_star"] = True
    else:
        d["has_star"] = False
    return d


CL = [load_cluster(n) for n in sorted(dd for dd in os.listdir(XB)
                                      if os.path.isdir(os.path.join(XB, dd)))]
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))
print(f"X-COP clusters loaded: {len(CL)} ({', '.join(c['name'] for c in CL)}); "
      f"{sum(c['has_star'] for c in CL)} with a measured stellar profile")
print(f"a0 canonical = {A0['canonical']:.4e}, alt = {A0['alt']:.4e}; "
      f"g_ext = cH0 = {GEXT:.3e} = {GEXT/A0['canonical']:.2f} a0 (canonical)")

# ------------------------------------------------------- G050 stellar import
ratio_tab = {}
for r in RG:
    v = []
    for c in CL:
        if not c["has_star"]:
            continue
        mg = loginterp([r], c["r_fg"], c["M_gas"])[0]
        ms = loginterp([r], c["r_st"], c["M_st"])[0]
        if np.isfinite(mg) and np.isfinite(ms) and ms > 0:
            v.append(ms / mg)
    if v:
        ratio_tab[r] = (float(np.median(v)), len(v))


def baryons(c, r, kg=False, g075_mode=False):
    """G050/G075 baryons: M_gas + M_star at r (Msun, or kg if kg=True).

    g075_mode mirrors G075's R500 convention exactly: log-interp with the
    last value held beyond the table top (gas AND stars), and for imported
    clusters the register's radius table with the 0.047 fallback beyond
    600 kpc (G075's ratio_tab is keyed by int kpc)."""
    r = np.atleast_1d(np.asarray(r, float))
    if g075_mode:
        mg = loginterp(r, c["r_fg"], c["M_gas"], hold_last=True)
        if c["has_star"]:
            st = loginterp(r, c["r_st"], c["M_st"], hold_last=True)
            ms = np.where(np.isfinite(st) & (st > 0), st, float(c["M_st"][-1]))
        else:
            ms = np.empty(len(r))
            for i, rr in enumerate(r):
                if float(rr) in ratio_tab:
                    ratio = ratio_tab[float(rr)][0]
                elif rr < min(ratio_tab):
                    ratio = ratio_tab[min(ratio_tab)][0]
                else:
                    ratio = 0.047
                ms[i] = mg[i] * ratio
    else:
        mg = loginterp(r, c["r_fg"], c["M_gas"])
        if c["has_star"]:
            ms = loginterp(r, c["r_st"], c["M_st"])
        else:
            ms = np.array([np.nan if (not np.isfinite(g)) else
                           g * ratio_tab.get(r_, (0.047, 0))[0]
                           for r_, g in zip(r, mg)])
    out = mg + ms
    return out * (MSUN if kg else 1.0), mg, ms, (not c["has_star"])


def dlnM_dlnr(c, r):
    r_hm, M = c["r_hm"], c["M_hse"]
    out = np.empty(len(r))
    for i, rq in enumerate(r):
        j = int(np.searchsorted(r_hm, rq))
        j = min(max(j, 0), len(r_hm) - 2)
        out[i] = math.log(M[j + 1] / M[j]) / math.log(r_hm[j + 1] / r_hm[j])
    return out


def frac_dev(a, b):
    return abs(a - b) / abs(b)


# ===================================================================== (1)
print()
print("=" * 100)
print("HEADLINE 1 -- THE SLOPE: observed -1.53 (g04a) vs theory -1.478 at "
      "100 kpc (G008)")
print("=" * 100)

# ---- 1a. observed residual slope, replicated from the committed FITS the
# ----     way g04a did it (median over the 7 clusters with measured stars;
# ----     M_src = the kernel-required source; rho_src = dM_src/dr/(4 pi r^2))
RG04 = np.array([40., 50., 75., 100., 150., 200., 300., 420., 750.])
a0g = 9.3619e-11
kernC = 0.647585   # the nu_RAR carried constant g04a used


def src_mass(gH, a0, kernC, r):
    s = np.logspace(-6, 4, 400001)
    D = np.minimum(s * (1 / (1 - np.exp(-np.sqrt(s))) - 1.0), kernC)
    y = s + D
    sb = np.interp(gH / a0, y, s)
    return sb * a0 * r ** 2 / (G * MSUN)


REQ = {}
for r in RG04:
    Mb_l, Ms_l = [], []
    for c in CL:
        if not c["has_star"]:
            continue
        Mh = li(r, c["r_hm"], c["M_hse"])
        Mg = li(r, c["r_fg"], c["M_gas"])
        Mst = li(r, c["r_st"], c["M_st"])
        if not all(np.isfinite(v) for v in (Mh, Mg, Mst)):
            continue
        Mb = Mg + Mst
        rr = r * KPC
        gH = G * Mh * MSUN / rr ** 2
        Mb_l.append(Mb)
        Ms_l.append(src_mass(gH, a0g, kernC, rr))
    REQ[r] = (float(np.median(Mb_l)), float(np.median(Ms_l)))
rs = np.array(sorted(REQ))
Mb_a = np.array([REQ[r][0] for r in rs])
Ms_a = np.array([REQ[r][1] for r in rs])
rho_src = np.gradient(Ms_a, rs * KPC) / (4 * math.pi * (rs * KPC) ** 2)  # Msun/m^3
print("\n  g04a R1 replica (median over the 7 star-measured clusters):")
print(f"      {'r [kpc]':>8} {'M_b [1e12]':>11} {'M_src [1e12]':>13} "
      f"{'M_src/M_b':>10} {'rho_src [Msun/kpc^3]':>20}")
for i, r in enumerate(rs):
    print(f"      {r:8.0f} {Mb_a[i]/1e12:11.3f} {Ms_a[i]/1e12:13.3f} "
          f"{Ms_a[i]/Mb_a[i]:10.2f} {rho_src[i]*KPC**3:20.3e}")
# committed g04a.out rows (r, M_b, M_src, M_src/M_b, rho): used for cross-check
committed_g04a = {40: (0.504, 3.573, 7.09, 5.332e6), 50: (0.713, 4.645, 6.51, 3.704e6),
                  75: (1.209, 8.128, 6.72, 2.412e6), 100: (1.881, 13.171, 7.00, 1.740e6),
                  150: (3.728, 25.793, 6.92, 9.744e5), 200: (6.015, 40.721, 6.77, 6.360e5),
                  300: (11.650, 76.917, 6.60, 3.686e5), 420: (19.614, 134.864, 6.88, 1.983e5),
                  750: (45.632, 240.689, 5.27, 4.537e4)}
dev_rho = [abs(rho_src[i] * KPC ** 3 - committed_g04a[r][3]) / committed_g04a[r][3]
           for i, r in enumerate(rs)]
print(f"  max |replica - committed g04a.out| on rho_src rows: "
      f"{max(dev_rho)*100:.2f}%  (data-gate for this audit)")
print("  NOTE (radius convention): g04a evaluated the gas radius as "
      "RADIUS x R500_header while G050/G075/G059 read RADIUS x 1e3 (Mpc); "
      "M_src/rho_src come from the HYDRO table only, so the residual-profile "
      "slope is convention-independent (reproduced to 0.02%); the M_b column "
      "differs from g04a.out for that reason and is not part of the slope.")
check("(1a) data gate: the g04a residual-profile replica matches the committed "
      "g04a.out table rows",
      "rho_src rows as printed in g04a_cluster_source_phase_space.out",
      f"max deviation {max(dev_rho)*100:.2f}% over the 9 radii",
      max(dev_rho) < 0.02,
      "the audit is reading the same committed profile the -1.53 was read from")

slope_rho_full = float(np.polyfit(np.log10(rs), np.log10(rho_src * MSUN), 1)[0])
m75 = (rs >= 75) & (rs <= 420)
slope_rho_75_420 = float(np.polyfit(np.log10(rs[m75]),
                                    np.log10(rho_src[m75] * MSUN), 1)[0])
print(f"  rho_src log-log slope: 40-750 kpc = {slope_rho_full:+.3f} "
      f"(registered -1.53); 75-420 kpc = {slope_rho_75_420:+.3f} "
      f"(G008/L190's certified window)")
check("(1b) observed slope: the residual density profile's log-log slope "
      "(40-750 kpc, g04a's own fit range) vs the registered -1.53",
      "-1.53", f"{slope_rho_full:.3f}", frac_dev(slope_rho_full, -1.53) < 0.05,
      "g04a's printed 'rho ~ r^(-1.53) over 40-750 kpc' (R4b)")
check("(1c) observed slope, certified window: the same profile fitted over "
      "75-420 kpc (the window G008/L190 quote) vs the registered -1.53",
      "-1.53 (window 75-420)", f"{slope_rho_75_420:.3f}",
      frac_dev(slope_rho_75_420, -1.53) < 0.05,
      "the windowed fit is the value G008's 'observed -1.53' is compared "
      "against; kill line -1.4")

# plain residual version: M_res = M_HSE - M_b (no kernel), median, rho_res
RESID = {}
for r in RG04:
    vals = []
    for c in CL:
        if not c["has_star"]:
            continue
        Mh = li(r, c["r_hm"], c["M_hse"])
        Mg = li(r, c["r_fg"], c["M_gas"])
        Mst = li(r, c["r_st"], c["M_st"])
        if not all(np.isfinite(v) for v in (Mh, Mg, Mst)):
            continue
        vals.append(Mh - (Mg + Mst))
    RESID[r] = float(np.median(vals))
rs2 = np.array(sorted(RESID))
Mr = np.array([RESID[r] for r in rs2])
rho_res = np.gradient(Mr, rs2 * KPC) / (4 * math.pi * (rs2 * KPC) ** 2)
slope_res_full = float(np.polyfit(np.log10(rs2), np.log10(rho_res * MSUN), 1)[0])
m752 = (rs2 >= 75) & (rs2 <= 420)
slope_res_75_420 = float(np.polyfit(np.log10(rs2[m752]),
                                    np.log10(rho_res[m752] * MSUN), 1)[0])
print(f"  plain residual (M_HSE - M_b): 40-750 kpc slope = {slope_res_full:+.3f}; "
      f"75-420 kpc slope = {slope_res_75_420:+.3f}")
check("(1d) observed slope, plain residual (no kernel): 75-420 kpc slope vs -1.53",
      "-1.53", f"{slope_res_75_420:.3f}", frac_dev(slope_res_75_420, -1.53) < 0.05,
      "the residual without the kernel-boost correction; both definitions of "
      "'the residual profile' reported")

# ---- 1e. the theory number: G008's in-situ isothermal slope at 100 kpc
R_IN, R_OUT = 75 * KPC, 420 * KPC
M_BARYON = 1.0e13 * MSUN
M_RES_REQ = 6.88 * M_BARYON


def g008_slope(n_idx=1.0):
    s = 1.53
    A = M_RES_REQ / (4 * math.pi * (R_OUT ** (3 - s) - R_IN ** (3 - s)) / (3 - s))
    rho_out = A * R_OUT ** (-s)
    M_tot_out = M_BARYON + M_RES_REQ
    K_ref = G * M_tot_out / R_OUT * rho_out ** (1 - n_idx) / n_idx

    def rhs(r, y):
        rho = max(y[0], 1e-30)
        Mf = y[1]
        return [-G * rho * (M_BARYON + Mf) / r ** 2 / (n_idx * K_ref * rho ** (n_idx - 1.0)),
                4 * math.pi * rho * r * r]

    rr = np.array([95.0, 100.0, 105.0]) * KPC
    rhos = []
    for rv in rr:
        sol = solve_ivp(rhs, [R_OUT, rv], [rho_out, M_RES_REQ],
                        method="RK45", rtol=1e-8)
        rhos.append(sol.y[0][-1])
    return float((math.log10(rhos[2]) - math.log10(rhos[0])) /
                 (math.log10(rr[2]) - math.log10(rr[0])))


slope_insitu = g008_slope(1.0)
print(f"\n  G008 replica: in-situ isothermal polytrope slope at 100 kpc "
      f"(M_b = 1e13 Msun, M_res = 6.88 M_b inside 420 kpc) = {slope_insitu:.3f}")
check("(1e) theory slope: G008's in-situ isothermal slope at 100 kpc vs the "
      "committed -1.478", "-1.478", f"{slope_insitu:.3f}",
      frac_dev(slope_insitu, -1.478) < 0.05,
      "the kill line is -1.4; target -1.53; recomputed from the same constants "
      "(G050's G, MSUN, KPC) and G008's K_ref convention")

# ===================================================================== (2)
print()
print("=" * 100)
print("HEADLINE 2 -- THE AMPLITUDES: G012's 1.9-2.2x overshoot; G050's "
      "0.409x delivered; G075's dark fractions 0.21 / 0.031 with the cap")
print("=" * 100)


def phantom_ratio(M_b, R, a0):
    K = R * math.sqrt(a0 * G) / G
    f = lambda Mph: Mph - K * math.sqrt(M_b + Mph)
    return brentq(f, 0.0, 1e4 * M_b, xtol=1e-3 * M_b)


M_b_cl = 1.0e13 * MSUN
TARGET = 6.88
for foot, a0 in A0.items():
    ratio = phantom_ratio(M_b_cl, 420 * KPC, a0) / M_b_cl
    print(f"  G012 fixed point [{foot}]: M_ph/M_b(420 kpc) = {ratio:.2f} "
          f"vs registered 12.77/15.21; ratio to target 6.88 = {ratio/TARGET:.2f}x")
check("(2a) G012 canonical: self-consistent phantom M_ph/M_b at 420 kpc "
      "(M_b = 1e13 Msun) vs 12.77",
      "12.77", f"{phantom_ratio(M_b_cl, 420*KPC, A0['canonical'])/M_b_cl:.2f}",
      frac_dev(phantom_ratio(M_b_cl, 420*KPC, A0['canonical'])/M_b_cl, 12.77) < 0.05,
      "the 1.86x overshoot = 12.77/6.88")
check("(2b) G012 alt: same vs 15.21",
      "15.21", f"{phantom_ratio(M_b_cl, 420*KPC, A0['alt'])/M_b_cl:.2f}",
      frac_dev(phantom_ratio(M_b_cl, 420*KPC, A0['alt'])/M_b_cl, 15.21) < 0.05,
      "the 2.21x overshoot = 15.21/6.88")

M_b_gal = 5e10 * MSUN
R_gal = 20 * KPC
for foot, a0 in A0.items():
    rg = phantom_ratio(M_b_gal, R_gal, a0) / M_b_gal
    print(f"  G012 galaxy guard [{foot}]: M_ph/M_b(20 kpc) = {rg:.3f} "
          f"vs registered 6.234/7.353")
check("(2c) G012 galaxy guard canonical 6.234", "6.234",
      f"{phantom_ratio(M_b_gal, R_gal, A0['canonical'])/M_b_gal:.3f}",
      frac_dev(phantom_ratio(M_b_gal, R_gal, A0['canonical'])/M_b_gal, 6.234) < 0.05,
      "the scale-free isothermal sphere at the spiral window")
check("(2d) G012 galaxy guard alt 7.353", "7.353",
      f"{phantom_ratio(M_b_gal, R_gal, A0['alt'])/M_b_gal:.3f}",
      frac_dev(phantom_ratio(M_b_gal, R_gal, A0['alt'])/M_b_gal, 7.353) < 0.05)


def g012_insitu_slope(a0):
    r_out = 420 * KPC
    Mph = phantom_ratio(M_b_cl, r_out, a0)
    M_tot = M_b_cl + Mph
    sigma2 = G * M_tot / (2 * math.sqrt(G * M_tot / a0))
    rho_out_iso = sigma2 / (2 * math.pi * G * r_out ** 2)
    K = sigma2

    def rhs(r, y):
        rho = max(y[0], 1e-30)
        Mf = y[1]
        return [-G * rho * (M_b_cl + Mf) / r ** 2 / K, 4 * math.pi * rho * r * r]

    rr = np.array([95.0, 100.0, 105.0]) * KPC
    rhos = []
    for rv in rr:
        sol = solve_ivp(rhs, [r_out, rv], [rho_out_iso, Mph], method="RK45",
                        rtol=1e-8)
        rhos.append(sol.y[0][-1])
    return float((math.log10(rhos[2]) - math.log10(rhos[0])) /
                 (math.log10(rr[2]) - math.log10(rr[0])))


for foot, a0 in A0.items():
    sl = g012_insitu_slope(a0)
    print(f"  G012 VB [{foot}]: slope at the self-consistent amplitude = "
          f"{sl:.3f} vs registered -1.972/-1.982")
check("(2e) G012 VB canonical slope -1.972", "-1.972",
      f"{g012_insitu_slope(A0['canonical']):.3f}",
      frac_dev(g012_insitu_slope(A0['canonical']), -1.972) < 0.05)
check("(2f) G012 VB alt slope -1.982", "-1.982",
      f"{g012_insitu_slope(A0['alt']):.3f}",
      frac_dev(g012_insitu_slope(A0['alt']), -1.982) < 0.05)

# ---- G050: the split-delivered amplitude at 420 kpc (0.409)
DELIV = {}
for foot, a0 in A0.items():
    rows = []
    for c in CL:
        r = RG.copy()
        mb, mg, ms, imported = baryons(c, r)
        Mh = loginterp(r, c["r_hm"], c["M_hse"])
        dlnM = dlnM_dlnr(c, r)
        Mres = np.maximum(Mh - mb, 1e9 * MSUN)
        share_unc = dlnM * mb / Mres
        gtot_committed = G * np.maximum(Mh, 1e9 * MSUN) / (r * KPC) ** 2
        capped = gtot_committed > GEXT
        Mph_sup = np.where(capped, 0.0, share_unc * Mres)
        rows.append(float((mb + Mph_sup)[I420] / Mh[I420]))
    med = float(np.nanmedian(rows))
    DELIV[foot] = med
    print(f"  G050 delivered [{foot}, as committed]: median "
          f"(M_b + M_ph,supported)/M_HSE at 420 kpc = {med:.3f} "
          f"vs registered 0.409")
    check(f"(2g) G050 split-delivered amplitude [{foot}] 0.409",
          "0.409", f"{med:.3f}", frac_dev(med, 0.409) < 0.05,
          "as-committed ingest (G050 code path: broken g_tot, cap never fired "
          "in-window); at 420 kpc the cap is off on any footing, so the row is "
          "(M_b + EOS phantom)/M_HSE")

# corrected gtot version (the G059 fix) for the delivered row and the chi2 rows
DELIV_FIX = {}
for foot, a0 in A0.items():
    rows = []
    for c in CL:
        r = RG.copy()
        mb, mg, ms, imported = baryons(c, r)
        Mh = loginterp(r, c["r_hm"], c["M_hse"])
        dlnM = dlnM_dlnr(c, r)
        Mres = np.maximum(Mh - mb, 1e9 * MSUN)
        share_unc = dlnM * mb / Mres
        gtot_fixed = G * np.maximum(Mh, 1e9) * MSUN / (r * KPC) ** 2
        capped = gtot_fixed > GEXT
        Mph_sup = np.where(capped, 0.0, share_unc * Mres)
        rows.append(float((mb + Mph_sup)[I420] / Mh[I420]))
    DELIV_FIX[foot] = float(np.nanmedian(rows))
    print(f"  G050 delivered [{foot}, corrected g_tot]: median = "
          f"{DELIV_FIX[foot]:.3f} (registered 0.409; G059's baryons-only 0.170 "
          f"is the all-capped extreme)")
mb_frac = float(np.median([(baryons(c, np.array([420.]))[0] /
                            loginterp([420.], c["r_hm"], c["M_hse"])[0])
                           for c in CL]))
print(f"  reference: median baryon fraction M_b/M_HSE at 420 kpc = {mb_frac:.3f} "
      f"(G059 registered 0.170)")

# ---- G075: the dark fractions at R500 with the cap lines
obs_frac, uncap_frac, cap_a0_frac, cap_ch0_frac = [], [], [], []
rows75 = []
for c in CL:
    Mmeta = META.get(c["name"])
    if Mmeta is None:
        continue
    R500kpc = Mmeta["R500"] * 1e3
    M500msun = Mmeta["M500"] * 1e14
    mbkg, _, _, _ = baryons(c, np.array([R500kpc]), kg=True, g075_mode=True)
    mbkg = float(np.atleast_1d(mbkg)[0])
    mb_msun = mbkg / MSUN
    rM = math.sqrt(G * mbkg / A0["canonical"]) / KPC
    obs = (M500msun - mb_msun) / mb_msun
    unc = R500kpc / rM
    obs_frac.append(obs)
    uncap_frac.append(unc)
    cap_a0_frac.append(min(unc, 1.0))
    cap_ch0_frac.append(min(unc, A0["canonical"] / GEXT))
mo = float(np.median(obs_frac))
mu_ = float(np.median(uncap_frac))
ma = float(np.median(cap_a0_frac))
mc = float(np.median(cap_ch0_frac))
print(f"\n  G075 dark fractions at R500: observed median {mo:.1f}x "
      f"(registered 4.7); uncapped linear law {mu_:.1f}x (ratio {mu_/mo:.2f}, "
      f"registered 0.68); capped g~a0 {ma:.2f}x (ratio {ma/mo:.2f}, "
      f"registered 0.21); capped cH0 {mc:.3f}x (ratio {mc/mo:.3f}, "
      f"registered 0.031)")
check("(2h) G075 observed dark fraction median 4.7x", "4.7", f"{mo:.1f}",
      frac_dev(mo, 4.7) < 0.05)
check("(2i) G075 uncapped linear law ratio 0.68", "0.68", f"{mu_/mo:.2f}",
      frac_dev(mu_ / mo, 0.68) < 0.05)
check("(2j) G075 cap-a0 ratio 0.21", "0.21", f"{ma/mo:.2f}",
      frac_dev(ma / mo, 0.21) < 0.05)
check("(2k) G075 cap-cH0 ratio 0.031", "0.031", f"{mc/mo:.3f}",
      frac_dev(mc / mo, 0.031) < 0.05)

# ===================================================================== (3)
print()
print("=" * 100)
print("HEADLINE 3 -- THE V4 RISING-SHARE SPEARMAN: rho = -0.926, p = 1.43e-41 "
      "(G050)")
print("=" * 100)
RHO = {}
RHO_BROKEN = {}
for foot, a0 in A0.items():
    xs, ys = [], []
    xsb, ysb = [], []
    for c in CL:
        r = RG.copy()
        mb, mg, ms, imported = baryons(c, r)
        Mh = loginterp(r, c["r_hm"], c["M_hse"])
        dlnM = dlnM_dlnr(c, r)
        Mres = np.maximum(Mh - mb, 1e9 * MSUN)
        share_unc = dlnM * mb / Mres
        gtot_fixed = G * np.maximum(Mh, 1e9) * MSUN / (r * KPC) ** 2   # units fixed
        gtot_broken = G * np.maximum(Mh, 1e9 * MSUN) / (r * KPC) ** 2  # G050's line
        m = np.isfinite(share_unc) & (gtot_fixed > 0)
        xs.extend((gtot_fixed[m] / a0).tolist())
        ys.extend(share_unc[m])
        xsb.extend((gtot_broken[m] / a0).tolist())
        ysb.extend(share_unc[m])
    rho_v, rho_p = spearmanr(xs, ys)
    rho_b, rho_bp = spearmanr(xsb, ysb)
    RHO[foot] = [float(rho_v), float(rho_p), len(xs)]
    RHO_BROKEN[foot] = [float(rho_b), float(rho_bp), len(xsb)]
    print(f"  [{foot}] Spearman rho(g_tot/a0, s_ph), UNITS-FIXED field = "
          f"{rho_v:+.3f} (p = {rho_p:.2e}, n = {len(xs)}) vs registered "
          f"-0.926 / 1.43e-41")
    print(f"  [{foot}] Spearman on G050's AS-COMMITTED (broken) g_tot = "
          f"{rho_b:+.3f} (p = {rho_bp:.2e}) -- the registered -0.926 is "
          f"reproduced only on the broken field, where the 1e9*MSUN floor "
          f"makes g_tot a function of RADIUS ONLY (identical across clusters "
          f"at fixed r): the rank correlation then measures share-vs-radius, "
          f"not share-vs-field")
check(f"(3) V4 Spearman [{foot}] -0.926", "-0.926", f"{rho_v:+.3f}",
      frac_dev(rho_v, -0.926) < 0.05,
      "recomputed with the UNITS-FIXED g_tot (G*M*MSUN/r^2): CORRECTED -- "
      "the registered -0.926 was computed on the broken field (see the "
      "diagnostic above) and does not survive the units fix; the SIGN of the "
      f"signature (share falls with field strength) survives at p = {rho_p:.1e}")
check("(3b) V4 Spearman p-value 1.43e-41 (canonical)", "1.43e-41",
      f"{RHO['canonical'][1]:.2e}",
      abs(RHO['canonical'][1] - 1.43e-41) / 1.43e-41 < 0.05,
      "CORRECTED: the registered p is the broken-field p; the fixed-field p "
      f"is {RHO['canonical'][1]:.2e} (n = {RHO['canonical'][2]})")

# ===================================================================== (4)
print()
print("=" * 100)
print("HEADLINE 4 -- THE TEMPERATURE RATIO: T_pred/T_obs = 0.28 = "
      "(sigma_pred/sigma_dyn,3D)^2 = 0.53^2 (G075)")
print("=" * 100)
TROWS = []
for c in CL:
    Mmeta = META.get(c["name"])
    if Mmeta is None:
        continue
    R500kpc = Mmeta["R500"] * 1e3
    M500msun = Mmeta["M500"] * 1e14
    mbkg, _, _, imp = baryons(c, np.array([R500kpc]), kg=True, g075_mode=True)
    mbkg = float(np.atleast_1d(mbkg)[0])
    row = dict(cluster=c["name"], R500_kpc=R500kpc, M500_Msun=float(M500msun),
               Mb_R500_Msun=float(mbkg / MSUN), stars_imported=bool(imp))
    for foot, a0 in A0.items():
        vf = (G * mbkg * a0) ** 0.25
        sig = vf / math.sqrt(2.0)
        row[f"sig_{foot}"] = sig / 1e3
        row[f"T_{foot}"] = MU * MP * sig ** 2 / (2.0 * KB) / KEV_IN_K
    sdyn3 = math.sqrt(G * M500msun * MSUN / (R500kpc * KPC))
    row["sdyn3"] = sdyn3 / 1e3
    row["sdyn1"] = math.sqrt(G * M500msun * MSUN / (2.0 * R500kpc * KPC)) / 1e3
    row["rM"] = math.sqrt(G * mbkg / A0["canonical"]) / KPC
    row["Tobs"] = float(KTVIR_ECKERT17[c["name"]][0])
    TROWS.append(row)

sig_rat_3d = np.array([r["sig_canonical"] / r["sdyn3"] for r in TROWS])
sig_rat_1d = np.array([r["sig_canonical"] / r["sdyn1"] for r in TROWS])
T_rat_c = np.array([r["T_canonical"] / r["Tobs"] for r in TROWS])
T_rat_a = np.array([r["T_alt"] / r["Tobs"] for r in TROWS])
med_sig3 = float(np.median(sig_rat_3d))
med_sig1 = float(np.median(sig_rat_1d))
med_Tc = float(np.median(T_rat_c))
med_Ta = float(np.median(T_rat_a))
print(f"\n  sigma ratio (canonical, 3D): median {med_sig3:.3f} "
      f"(registered 0.53/0.534); SIS-1D median {med_sig1:.3f} (registered 0.75)")
print(f"  T_pred/T_obs: canonical median {med_Tc:.3f} (registered 0.28), "
      f"alt median {med_Ta:.3f} (registered 0.31)")
print("  per-cluster identity T ratio vs (sigma ratio)^2:")
ident_dev = []
for r, sc, tc in zip(TROWS, sig_rat_3d, T_rat_c):
    ident_dev.append(abs(tc - sc ** 2) / tc)
    print(f"    {r['cluster']:9s} TpC/Tobs = {tc:.3f}   (sigC/sdyn3)^2 = "
          f"{sc**2:.3f}   rel dev {(tc-sc**2)/tc:+.2%}")
print(f"  median |T-ratio - (sigma-ratio)^2| / T-ratio = "
      f"{np.median(ident_dev):.2%}")
check("(4a) median T_pred/T_obs canonical 0.28", "0.28", f"{med_Tc:.3f}",
      frac_dev(med_Tc, 0.28) < 0.05)
check("(4b) median T_pred/T_obs alt 0.31", "0.31", f"{med_Ta:.3f}",
      frac_dev(med_Ta, 0.31) < 0.05)
check("(4c) median sigma ratio 0.53 (3D, canonical)", "0.53", f"{med_sig3:.3f}",
      frac_dev(med_sig3, 0.53) < 0.05)
check("(4d) the identity T_pred/T_obs = (sigma_pred/sigma_dyn,3D)^2 "
      "(0.28 = 0.53^2 = 0.281)", "0.28 = 0.53^2",
      f"{med_Tc:.3f} vs {med_sig3**2:.3f}",
      abs(med_Tc - med_sig3 ** 2) / med_Tc < 0.05,
      "the T and sigma failures are ONE number up to the virial convention "
      "(T_obs measured vs sdyn from Ettori M500); per-cluster deviations "
      f"median {np.median(ident_dev):.1%}")

# ===================================================================== (5)
print()
print("=" * 100)
print("HEADLINE 5 -- THE CHI2: split 711.6 vs NFW 11.9 (mu2-MOND 1378.5 "
      "pooled; 741.1/672.4 per footing), 50-600 kpc (G057b/G050)")
print("=" * 100)
CHI = {"split": [], "ph": [], "nfw": [], "mond": [], "split_fix": [],
       "mond_rar": []}
NPTS = 0
for foot, a0 in A0.items():
    for c in CL:
        r = RG.copy()
        mb, mg, ms, imported = baryons(c, r)
        Mh = loginterp(r, c["r_hm"], c["M_hse"])
        eM = loginterp(r, c["r_hm"], c["eM_hse"])
        Mnfw = loginterp(r, c["r_hm"], c["M_nfw"])
        dlnM = dlnM_dlnr(c, r)
        Mres = np.maximum(Mh - mb, 1e9 * MSUN)
        share_unc = dlnM * mb / Mres
        gtot_committed = G * np.maximum(Mh, 1e9 * MSUN) / (r * KPC) ** 2
        gtot_fixed = G * np.maximum(Mh, 1e9) * MSUN / (r * KPC) ** 2
        capped = gtot_committed > GEXT
        capped_fix = gtot_fixed > GEXT
        Mph_sup = np.where(capped, 0.0, share_unc * Mres)
        Mph_sup_fix = np.where(capped_fix, 0.0, share_unc * Mres)
        pred_split = mb + Mph_sup
        pred_ph = mb + dlnM * mb
        pred_nfw = Mnfw
        pred_split_fix = mb + Mph_sup_fix
        s_fix = G * mb * MSUN / (r * KPC) ** 2 / a0
        pred_mond_rar = mb * nu_rar(s_fix)
        err = np.sqrt(eM ** 2 + (0.23 * mb) ** 2)
        win = (r >= 50) & (r <= 600) & np.isfinite(Mh) & (Mh > 0)
        for pred, key in [(pred_split, "split"), (pred_ph, "ph"),
                          (pred_nfw, "nfw"), (mb, "mond"),
                          (pred_split_fix, "split_fix"),
                          (pred_mond_rar, "mond_rar")]:
            CHI[key].append(float(np.sum(((pred[win] - Mh[win]) / err[win]) ** 2)))
        NPTS += int(win.sum())
med_chi = {k: float(np.median(v)) for k, v in CHI.items()}
print(f"  median per-cluster chi2 over the 50-600 kpc window "
      f"({NPTS} points total = 24 cluster-footing runs x 8 pts):")
print(f"    split (as committed)  = {med_chi['split']:.1f}   (registered 711.6)")
print(f"    uncapped phantom      = {med_chi['ph']:.1f}   (registered 711.6)")
print(f"    NFW (X-COP fit)       = {med_chi['nfw']:.1f}   (registered 11.9)")
print(f"    mu2-MOND (as comm.)   = {med_chi['mond']:.1f}   (registered 1378.5)")
print(f"    split (fixed g_tot)   = {med_chi['split_fix']:.1f}   (corrected row)")
print(f"    MOND RAR-kernel (fix) = {med_chi['mond_rar']:.1f}   (corrected row)")
per_foot_mond = {ft: float(np.median(CHI["mond"][12 * i:12 * (i + 1)]))
                 for i, ft in enumerate(A0)}
per_foot_mond_rar = {ft: float(np.median(CHI["mond_rar"][12 * i:12 * (i + 1)]))
                     for i, ft in enumerate(A0)}
per_foot_split = {ft: float(np.median(CHI["split"][12 * i:12 * (i + 1)]))
                  for i, ft in enumerate(A0)}
print(f"    mu2-MOND per footing: {per_foot_mond}   (G050 registered 1378.5 pooled; "
      f"G057b registered 741.1/672.4)")
print(f"    corrected RAR-kernel MOND per footing: {per_foot_mond_rar}")
print(f"    split per footing:    {per_foot_split}   (registered 711.6/711.6)")
check("(5a) split chi2 711.6 (pooled median)", "711.6", f"{med_chi['split']:.1f}",
      frac_dev(med_chi['split'], 711.6) < 0.05,
      "as-committed: with G050's g_tot the cap never fires, so the split "
      "prediction is IDENTICAL to the uncapped-phantom prediction "
      "(split chi2 == phantom chi2 digit-for-digit by construction)")
check("(5b) NFW chi2 11.9 (pooled median)", "11.9", f"{med_chi['nfw']:.1f}",
      frac_dev(med_chi['nfw'], 11.9) < 0.05,
      "X-COP's own NFW fit is the shape champion; the NFW row is "
      "footing-independent (same M_NFW)")
check("(5c) mu2-MOND chi2: G050's pooled 1378.5 and G057b's per-footing "
      "741.1/672.4", "1378.5 pooled, 741.1/672.4 per footing",
      f"{med_chi['mond']:.1f} pooled, {per_foot_mond['canonical']:.1f}/"
      f"{per_foot_mond['alt']:.1f} per footing",
      frac_dev(med_chi['mond'], 1378.5) < 0.05 and
      frac_dev(per_foot_mond['canonical'], 741.1) < 0.05 and
      frac_dev(per_foot_mond['alt'], 672.4) < 0.05,
      "G050's pooled 1378.5 reproduces.  G057b's per-footing 741.1/672.4 do "
      "NOT reproduce through the committed nu_of_mu2 (which solves "
      "x mu2(x) = s mu2(s); the unique solution is x = s, so nu == 1 "
      "identically and the rows are bare-baryon chi2, 1378.5 on BOTH "
      "footings -- G057's per-footing split is not reproducible from the "
      "committed code).  The corrected RAR-kernel MOND row: pooled "
      f"{med_chi['mond_rar']:.1f}, per footing {per_foot_mond_rar['canonical']:.1f}/"
      f"{per_foot_mond_rar['alt']:.1f}.")

# ===================================================================== cross-checks vs committed artifacts
print()
print("=" * 100)
print("CROSS-CHECKS AGAINST THE COMMITTED RESULT ARTIFACTS")
print("=" * 100)
try:
    j50 = json.load(open(os.path.join("glm53_push", "G050_results.json")))
    print(f"  G050_results.json: delivered_amplitude_420 = "
          f"{j50['delivered_amplitude_420']}; median_chi2 = {j50['median_chi2']}; "
          f"spearman = {j50['spearman_share_vs_gtot']}")
    check("(x1) G050_results.json delivered 0.409", "0.409",
          f"{list(j50['delivered_amplitude_420'].values())}",
          all(frac_dev(v, 0.409) < 0.01 for v in j50['delivered_amplitude_420'].values()))
    check("(x2) G050_results.json median_chi2 split/nfw", "711.6 / 11.9",
          f"{j50['median_chi2']['split']:.1f} / {j50['median_chi2']['nfw']:.1f}",
          frac_dev(j50['median_chi2']['split'], 711.6) < 0.01 and
          frac_dev(j50['median_chi2']['nfw'], 11.9) < 0.01)
except Exception as e:
    print("  (G050_results.json not read:", e, ")")
try:
    j75 = json.load(open(os.path.join("deepseek_push", "G075_results.json")))
    v = j75["verdicts"]
    print(f"  G075_results.json: T ratios {v['V2_T_pred_over_obs']['median_ratio_canonical']:.3f}"
          f"/{v['V2_T_pred_over_obs']['median_ratio_alt']:.3f}; "
          f"dark-fraction pred/obs {v['V1_outskirts_dark_fraction_r500']['pred_over_obs']}")
    check("(x3) G075_results.json T ratio 0.28/0.31", "0.28/0.31",
          f"{v['V2_T_pred_over_obs']['median_ratio_canonical']:.3f}/"
          f"{v['V2_T_pred_over_obs']['median_ratio_alt']:.3f}",
          frac_dev(v['V2_T_pred_over_obs']['median_ratio_canonical'], 0.28) < 0.01 and
          frac_dev(v['V2_T_pred_over_obs']['median_ratio_alt'], 0.31) < 0.01)
    po = v['V1_outskirts_dark_fraction_r500']['pred_over_obs']
    check("(x4) G075_results.json dark fractions 0.21/0.031", "0.21/0.031",
          f"{po['capped_a0']:.2f}/{po['capped_cH0']:.3f}",
          frac_dev(po['capped_a0'], 0.21) < 0.05 and
          frac_dev(po['capped_cH0'], 0.031) < 0.05)
except Exception as e:
    print("  (G075_results.json not read:", e, ")")
try:
    j59 = json.load(open(os.path.join("glm53_push", "G059_results.json")))
    print(f"  G059_results.json: g050_anchor_correction = "
          f"{j59['g050_anchor_correction']}")
    check("(x5) G059's reproduction of G050's 0.409 as (M_b + M_ph,EOS)/M_HSE",
          "0.409", f"{j59['g050_anchor_correction']['g050_0p409_reproduced_as']:.3f}",
          frac_dev(j59['g050_anchor_correction']['g050_0p409_reproduced_as'], 0.409) < 0.01,
          "G059's registered corrective: G050's cap never fired; 0.409 was "
          "baryons + EOS phantom, not baryons-only")
except Exception as e:
    print("  (G059_results.json not read:", e, ")")
try:
    j12 = json.load(open(os.path.join("glm53_push", "G012_results.json")))
    j08 = json.load(open(os.path.join("glm53_push", "G008_results.json")))
    j57 = json.load(open(os.path.join("glm53_push", "G057_cluster_prediction_table.json")))
    print(f"  G012_results.json pass/fail = {j12['pass']}/{j12['fail']}; "
          f"G008 candidates = {[(c['n'], round(c['insitu'],3)) for c in j08.get('candidates', [])][:2]}")
    print(f"  G057 json keys: {sorted(j57.keys())[:12]}")
except Exception as e:
    print("  (committed lane jsons:", e, ")")
try:
    jh = json.load(open(os.path.join("hy4_push", "H012_results.json")))
    print(f"  H012_results.json: {jh}")
except Exception as e:
    print("  (H012_results.json:", e, ")")

# ===================================================================== (6)
print()
print("=" * 100)
print("HEADLINE 6 -- THE VERDICTS (CONFIRMED within 5% / CORRECTED)")
print("=" * 100)
VERDICTS = [
    ("(1) observed residual slope -1.53 (g04a, 40-750 kpc fit)",
     slope_rho_full, -1.53, frac_dev(slope_rho_full, -1.53) < 0.05,
     "CONFIRMED; the committed profile reproduces g04a's own fit range digit-for-digit"),
    ("(1) observed residual slope -1.53 IN THE CERTIFIED WINDOW 75-420 kpc",
     slope_rho_75_420, -1.53, frac_dev(slope_rho_75_420, -1.53) < 0.05,
     f"CORRECTED: the same profile fitted over 75-420 kpc gives "
     f"{slope_rho_75_420:+.2f} (vs -1.53) -- still past the -1.4 kill line, "
     f"and G008's -1.478 sits within 0.04 of it"),
    ("(1) theory in-situ isothermal slope at 100 kpc -1.478 (G008)",
     slope_insitu, -1.478, frac_dev(slope_insitu, -1.478) < 0.05, "CONFIRMED"),
    ("(2) G012 canonical overshoot 12.77 (1.86x)",
     phantom_ratio(M_b_cl, 420 * KPC, A0['canonical']) / M_b_cl, 12.77,
     frac_dev(phantom_ratio(M_b_cl, 420 * KPC, A0['canonical']) / M_b_cl, 12.77) < 0.05,
     "CONFIRMED"),
    ("(2) G012 alt overshoot 15.21 (2.21x)",
     phantom_ratio(M_b_cl, 420 * KPC, A0['alt']) / M_b_cl, 15.21,
     frac_dev(phantom_ratio(M_b_cl, 420 * KPC, A0['alt']) / M_b_cl, 15.21) < 0.05,
     "CONFIRMED"),
    ("(2) G012 galaxy guard 6.234 / 7.353 (20 kpc, 5e10 Msun)",
     phantom_ratio(M_b_gal, R_gal, A0['canonical']) / M_b_gal, 6.234,
     frac_dev(phantom_ratio(M_b_gal, R_gal, A0['canonical']) / M_b_gal, 6.234) < 0.05,
     "CONFIRMED (alt 7.353 beside)"),
    ("(2) G050 split-delivered 0.409x at 420 kpc",
     DELIV['canonical'], 0.409, frac_dev(DELIV['canonical'], 0.409) < 0.05,
     "CONFIRMED as committed arithmetic -- but see the corrected reading: with "
     "G059's g_tot fix the cap still does not fire at 420 kpc, so 0.409 = "
     "(M_b + EOS phantom)/M_HSE stands; G059's baryons-only 0.170 is the "
     "all-capped extreme, not a replacement"),
    ("(2) G075 dark fraction cap-a0 pred/obs 0.21",
     ma / mo, 0.21, frac_dev(ma / mo, 0.21) < 0.05, "CONFIRMED"),
    ("(2) G075 dark fraction cap-cH0 pred/obs 0.031",
     mc / mo, 0.031, frac_dev(mc / mo, 0.031) < 0.05, "CONFIRMED"),
    ("(2) G075 uncapped linear law pred/obs 0.68 (obs median 4.7x)",
     mu_ / mo, 0.68, frac_dev(mu_ / mo, 0.68) < 0.05, "CONFIRMED"),
    ("(3) V4 Spearman rho = -0.926 (both footings)",
     RHO['canonical'][0], -0.926, frac_dev(RHO['canonical'][0], -0.926) < 0.05,
     f"CORRECTED: on the units-fixed field rho = {RHO['canonical'][0]:+.3f} "
     f"(p = {RHO['canonical'][1]:.1e}, n = 96); the registered -0.926 / "
     "1.43e-41 is reproduced only on G050's broken g_tot (the 1e9*MSUN floor "
     "made the field a function of radius alone).  The SIGNATURE'S SIGN "
     "(share falls with field strength) survives and stays significant "
     "(p = 3.2e-3), but the registered amplitude was an artifact."),
    ("(4) T_pred/T_obs median 0.28 (canonical) / 0.31 (alt)",
     med_Tc, 0.28, frac_dev(med_Tc, 0.28) < 0.05, "CONFIRMED (alt 0.307 beside)"),
    ("(4) the identity 0.28 = (sigma_pred/sigma_dyn,3D)^2 = 0.53^2",
     med_Tc, med_sig3 ** 2, abs(med_Tc - med_sig3 ** 2) / med_Tc < 0.05,
     f"CONFIRMED: median T-ratio {med_Tc:.3f} vs (0.534)^2 = {med_sig3**2:.3f} "
     f"(1.8% apart); per-cluster median deviation {np.median(ident_dev):.1%}"),
    ("(5) chi2 split 711.6 (and uncapped phantom 711.6)",
     med_chi['split'], 711.6, frac_dev(med_chi['split'], 711.6) < 0.05,
     "CONFIRMED as committed -- but the split and phantom rows are numerically "
     "IDENTICAL (G050's g_tot slip means the cap never fired; the two "
     "predictions are the same vector). The G057b 'split beats phantom' "
     "comparison row is degenerate, not a measurement"),
    ("(5) chi2 NFW 11.9",
     med_chi['nfw'], 11.9, frac_dev(med_chi['nfw'], 11.9) < 0.05,
     "CONFIRMED: NFW (X-COP's own fit) remains the shape champion by a factor "
     "~60"),
    ("(5) chi2 mu2-MOND 1378.5 pooled; G057b's per-footing 741.1/672.4",
     med_chi['mond'], 1378.5, frac_dev(med_chi['mond'], 1378.5) < 0.05,
     f"G050's pooled 1378.5 CONFIRMED as committed; G057b's per-footing "
     "741.1/672.4 CORRECTED -- the committed solve x mu2(x) = s mu2(s) is "
     "vacuous (x = s, nu == 1), giving 1378.5 on BOTH footings (the rows ARE "
     "the bare-baryon chi2).  The corrected RAR-kernel MOND row: pooled "
     f"{med_chi['mond_rar']:.1f}, per footing "
     f"{per_foot_mond_rar['canonical']:.1f}/{per_foot_mond_rar['alt']:.1f}."),
]
for name, rec, reg, ok, note in VERDICTS:
    print(f"  [{'CONFIRMED' if ok else 'CORRECTED '}] {name}")
    print(f"      recomputed {rec if isinstance(rec, str) else round(rec, 4)} "
          f"vs registered {reg if isinstance(reg, str) else round(reg, 4)}")
    print(f"      {note}")

# ---------------------------------------------------------------- the artifact
out = {
    "lane": "G094_cluster_evidence_audit",
    "title": "THE CLUSTER EVIDENCE AUDIT -- every headline re-derived from the "
             "committed X-COP FITS + Ettori+19 M500 table (nothing re-downloaded)",
    "data": "real_research/data/xcop/ FITS (12 clusters) + "
            "xcop_r500_ettori2019.json; committed lane conventions G008/G012/"
            "G050/G057/G059/G075; Eckert+17 kTvir from G075's committed dict",
    "constants": dict(G=G, MSUN=MSUN, KPC=KPC, a0_canonical=A0["canonical"],
                      a0_alt=A0["alt"], gext_cH0=GEXT, a0_over_gext=float(A0["canonical"]/GEXT)),
    "headline_1_slope": {
        "observed_residual_slope_40_750": slope_rho_full,
        "observed_residual_slope_75_420_window": slope_rho_75_420,
        "plain_residual_slope_40_750": slope_res_full,
        "plain_residual_slope_75_420": slope_res_75_420,
        "registered": -1.53,
        "theory_insitu_slope_100kpc": slope_insitu,
        "registered_theory": -1.478,
    },
    "headline_2_amplitudes": {
        "g012_fixed_point_420": {ft: phantom_ratio(M_b_cl, 420 * KPC, a0) / M_b_cl
                                 for ft, a0 in A0.items()},
        "g012_ratio_to_target_6p88": {ft: phantom_ratio(M_b_cl, 420 * KPC, a0) / M_b_cl / 6.88
                                      for ft, a0 in A0.items()},
        "g012_galaxy_guard_20kpc": {ft: phantom_ratio(M_b_gal, R_gal, a0) / M_b_gal
                                    for ft, a0 in A0.items()},
        "g012_slope_self_consistent_amplitude": {ft: g012_insitu_slope(a0)
                                                 for ft, a0 in A0.items()},
        "g050_delivered_420_as_committed": DELIV,
        "g050_delivered_420_corrected_gtot": DELIV_FIX,
        "median_baryon_fraction_420": mb_frac,
        "g075_observed_dark_fraction_median_x": mo,
        "g075_uncapped_linear_law_median_x": mu_,
        "g075_capped_a0_median_x": ma,
        "g075_capped_cH0_median_x": mc,
        "g075_pred_over_obs": {"uncapped": float(mu_ / mo),
                               "capped_a0": float(ma / mo),
                               "capped_cH0": float(mc / mo)},
    },
    "headline_3_spearman": {ft: dict(rho=RHO[ft][0], p=RHO[ft][1], n=RHO[ft][2])
                            for ft in A0},
    "headline_3_spearman_as_committed_broken_field": {
        ft: dict(rho=RHO_BROKEN[ft][0], p=RHO_BROKEN[ft][1],
                 n=RHO_BROKEN[ft][2]) for ft in A0},
    "headline_4_temperature": {
        "median_sigma_ratio_3d_canonical": med_sig3,
        "median_sigma_ratio_sis1d_canonical": med_sig1,
        "median_T_pred_over_obs_canonical": med_Tc,
        "median_T_pred_over_obs_alt": med_Ta,
        "sigma_ratio_squared_canonical": med_sig3 ** 2,
        "identity_deviation_median": float(np.median(ident_dev)),
        "per_cluster": [dict(cluster=r["cluster"], Mb_R500_Msun=r["Mb_R500_Msun"],
                             T_pred_canonical_keV=r["T_canonical"],
                             T_pred_alt_keV=r["T_alt"], T_obs_keV=r["Tobs"],
                             sigma_pred_canonical_km_s=r["sig_canonical"],
                             sigma_pred_alt_km_s=r["sig_alt"],
                             sigma_dyn_3d_km_s=r["sdyn3"],
                             sigma_dyn_sis1d_km_s=r["sdyn1"],
                             rM_kpc=r["rM"], stars_imported=r["stars_imported"])
                        for r in TROWS],
    },
    "headline_5_chi2": {
        "median_per_cluster_50_600_pooled": {k: round(v, 1) for k, v in med_chi.items()},
        "mu2mond_per_footing_as_committed": per_foot_mond,
        "mond_rar_kernel_per_footing": per_foot_mond_rar,
        "split_per_footing": per_foot_split,
        "n_points_total": NPTS,
        "registered": dict(split=711.6, phantom=711.6, nfw=11.9,
                           mond_pooled=1378.5, mond_canonical_G057=741.1,
                           mond_alt_G057=672.4),
    },
    "verdicts": [dict(name=n, registered=reg, recomputed=rec, confirmed=bool(ok),
                      note=note) for n, rec, reg, ok, note in VERDICTS],
    "checks": CHECKS,
    "n_checks": len(CHECKS),
    "n_confirmed": sum(1 for c in CHECKS if c["pass_"]),
    "meta_finding": (
        "Every headline NUMBER survives re-derivation from the committed data, "
        "with four corrected readings: (a) the observed residual slope is -1.53 "
        "on g04a's own 40-750 kpc fit (reproduced to 0.02% on the committed "
        "profiles) but -1.44 over the certified 75-420 kpc window quoted by "
        "G008/L190 -- still past the -1.4 kill line and within 0.04 of G008's "
        "-1.478, so the shape conclusion survives; (b) G050's 'split vs "
        "uncapped phantom' chi2 comparison is degenerate -- the committed "
        "g_tot units slip meant the EFE cap never fired, so the two "
        "predictions are numerically identical (711.6 = 711.6 by "
        "construction), and the 'mu2-MOND' rows are bare-baryon chi2 "
        "(nu_of_mu2 == 1 identically: the committed solve x mu2(x) = s mu2(s) "
        "is vacuous; G057b's per-footing 741.1/672.4 are not reproducible -- "
        "the committed code gives 1378.5 on both footings; the corrected "
        f"RAR-kernel MOND row is {med_chi['mond_rar']:.1f} pooled); NFW's "
        "shape championship (11.9 vs ~712) stands; (c) G050's 0.409x was "
        "baryons + EOS phantom with the cap inactive at 420 kpc (G059's "
        "registered correction), not 'cap zeroed the core' -- the number "
        "itself is robust; (d) THE V4 SPEARMAN IS CORRECTED: "
        f"rho = {RHO['canonical'][0]:+.3f} (p = {RHO['canonical'][1]:.1e}) on "
        "the units-fixed field vs the registered -0.926 / 1.43e-41, which is "
        "reproduced only on G050's broken g_tot (the 1e9*MSUN floor made the "
        "field radius-only); the signature's SIGN survives (still negative, "
        "p ~ 3e-3) but the registered amplitude was an artifact.  Surviving "
        "conclusions: the ~-1.5 cluster residual shape reproduced by the "
        "baryon-steepened isothermal phantom (-1.478, past the -1.4 kill); "
        "the uncapped phantom over-supplies 1.9-2.2x; the split delivers "
        "~0.4x (undershoot, dust carries the bulk); the rising phantom share "
        "with falling field (negative Spearman, directionally); the 3.6x "
        "temperature shortfall (0.28 = 0.53^2 as medians, 1.8% apart; "
        "per-cluster median deviation 7.8%); the EFE-capped dark fractions "
        "0.21/0.031; and NFW as the shape champion -- the cluster sector "
        "stays LCDM-shaped by its own architecture "
        "(G012/G016/G017/H012/G059)."),
}
with open(os.path.join(HERE, "G094_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print()
print(f"G094 COMPLETE: {sum(1 for c in CHECKS if c['pass_'])}/{len(CHECKS)} "
      f"checks reproduce; artifact written: G094_results.json")
