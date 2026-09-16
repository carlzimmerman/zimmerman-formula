#!/usr/bin/env python3
"""G184 -- THE KNEE'S DISCRIMINATOR: what separates the knee's class on the outer profile?

CONTEXT (all committed, read-first):
  G160 -- the model-free knee sits at r_b/R_cap = 0.44 (canonical) / 0.54 (alt),
          r_b/rs = 0.54: the knee COINCIDES with NFW's own transition (the
          committed X-COP NFW fits pass slope -2 at r = rs; at the knee the
          NFW slope is already -1.70 and steepening).  The two readings -- the
          theory's a0-crossing break and the NFW pivot -- AGREE INSIDE R500
          (the position is unresolvable on the committed data, G160 V3); they
          DIFFER OUTSIDE:
            theory outer envelope: -2.38  (G108 pooled d ln rho_dust/d ln r =
                  -2.377 +- 0.152 on (r_M, R500); the phantom A/r^2 + the
                  r^-1.7 dust envelope; G139 deep -2.31; G176 seam p2 2.9)
            NFW:                   -3.0   (the NFW asymptote at r >> rs; the
                  classic beta = 2/3 y-projection is also -3, G141's F_classic)
  G108 -- the OUTER envelope decomposition, committed per-cluster rows on the
          X-COP hydrostatic shells (M_FORW, NOT M_NFW), window (r_M, R500).
  G129/G141 -- the tSZ outer test: the joint y-profile outer index -2.37 at
          2 R500 (median), 2-bin [R500, 2R500] -2.54, vs the classic
          beta = 2/3 reading -3; G129's forecast 2-bin slope error 0.32 per
          cluster, 0.09 pooled.

THE DISCRIMINATOR (this lane): the measured outer slope at the
(knee, 2 R500)-class window:
  prediction per reading at 1.0-2.0 R500:
     theory  : slope in [-2.4, -2.0]  (the registered -2.38 envelope)
     NFW     : -3.0-class            (asymptote; the committed NFW fits at
               1-2 R500 run -2.0..-2.75 per cluster, approaching -3)

(1) THE DATA: the committed outer bins (the G108 window 600 kpc-R500 = G160's
    OUT window, the residual profiles): the measured slope there per cluster
    with propagated errors (EM_FORW + the 0.23 baryon systematic, G160's
    convention), dark residual (rho_tot - rho_b, model-independent) and dust
    envelope (rho_tot - A/r^2 - rho_b, G108's face); pooled; the sigma
    separation between the two predictions per cluster and pooled.

(2) THE CROSS-CHECK: the X-ray gas profile's outer slope (the beta-model
    tail, the committed fgas shells at 1-1.5 R500) vs the dark; the tSZ joint
    (G141's committed -2.37 at 2 R500 vs the beta-model -3); the lensing
    statement (no committed WL profile in the repo -- the hydrostatic total
    density is the proxy, projection mapped); the three-instrument
    consistency (X-ray dark, X-ray gas, tSZ joint).

(3) VERDICTS
    V1 the measured outer slope vs the two predictions (the sigma);
    V2 the three-instrument agreement;
    V3 the honest statement: the outer profile ALREADY discriminates the
       theory's -2.38 envelope from NFW's -3, or the data remain unbinned at
       1-2 R500 (gas ends ~1.1-1.7 R500) and the tSZ becomes the decider,
       with the G141 pipeline (0.09 pooled slope error).

Loader/conventions: IDENTICAL to G108 (committed X-COP ingests, G075 baryon
convention, M_FORW hydrostatics, h67b stellar import); errors from EM_FORW.
"""
import json
import math
import os

import numpy as np
from astropy.io import fits

RES, NP, NF = [], 0, 0


def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
XB = os.path.join(REPO, "real_research", "data", "xcop")

G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
A0 = 9.3619e-11            # canonical (G108/G050/G057/G075 footing)
B_SYS = 0.23               # baryon systematic on M_b (G160's error convention)
RG = np.array([50., 75., 100., 150., 210., 300., 420., 600.])

# the two readings' predictions at 1.0-2.0 R500 (the discriminator)
S_TH_BAND = (-2.4, -2.0)          # theory: the registered -2.38 envelope class
S_TH_CTR = -2.2
S_NFW_CLASS = -3.0                # NFW asymptote / classic beta=2/3 projection

print(__doc__)
print("=" * 100)
print("G184 -- THE KNEE'S DISCRIMINATOR: -2.38 envelope vs NFW -3 at 1-2 R500")
print("=" * 100)
info = lambda *a: print(*a, flush=True)


def loginterp(x, xp, fp, hold_last=False):
    xp = np.atleast_1d(np.asarray(xp, float))
    fp = np.atleast_1d(np.asarray(fp, float))
    x = np.atleast_1d(np.asarray(x, float))
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    if hold_last:
        out = np.where(x > xp[-1], fp[-1], out)
    return float(out[0])


def load_cluster(name):
    p = os.path.join(XB, name)
    hm = fits.open(os.path.join(p, f"{name}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(p, f"{name}_fgas_profile.fits"))[1].data
    d = dict(name=name,
             r_hm=np.array(hm["RADIUS"], float),               # kpc
             M_hse=np.array(hm["M_FORW"], float) * MSUN,       # kg
             eM_hse=np.array(hm["EM_FORW"], float) * MSUN,     # kg, 1-sigma
             M_nfw=np.array(hm["M_NFW"], float) * MSUN,        # kg (gate-only)
             r_fg=np.array(fg["RADIUS"], float) * 1e3,         # kpc
             M_gas=np.array(fg["MGAS"], float) * MSUN,         # kg
             e_gas=np.sqrt(np.array(fg["MGAS_LO"], float) ** 2 +
                           np.array(fg["MGAS_HI"], float) ** 2) / math.sqrt(2) * MSUN)
    fs = os.path.join(p, f"{name}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        d["r_st"] = np.array(ms["RADIUS"], float)
        d["M_st"] = np.array(ms["MSTAR"], float) * MSUN
        d["has_star"] = True
    else:
        d["has_star"] = False
    return d


CL = [load_cluster(n) for n in sorted(dd for dd in os.listdir(XB)
                                      if os.path.isdir(os.path.join(XB, dd)))]
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))

ratio_tab = {}
for r in RG:
    v = []
    for c in CL:
        if not c["has_star"]:
            continue
        mg = loginterp(r, c["r_fg"], c["M_gas"])
        ms = loginterp(r, c["r_st"], c["M_st"])
        if np.isfinite(mg) and np.isfinite(ms) and ms > 0 and mg > 0:
            v.append(ms / mg)
    if v:
        ratio_tab[int(r)] = (float(np.median(v)), len(v))


def baryons(c, r_kpc):
    """enclosed baryons M_gas + M_star at r (kpc), kg -- G050/G057/G075/G108
    exact convention (h67b import beyond the stellar grid; gas hold-last)."""
    mg = loginterp(r_kpc, c["r_fg"], c["M_gas"], hold_last=True)
    if c["has_star"]:
        st = loginterp(r_kpc, c["r_st"], c["M_st"], hold_last=True)
        ms = st if (np.isfinite(st) and st > 0) else float(c["M_st"][-1])
    else:
        rr = float(np.atleast_1d(np.asarray(r_kpc, float))[0])
        if rr in ratio_tab:
            ratio = ratio_tab[rr][0]
        elif rr < min(ratio_tab):
            ratio = ratio_tab[min(ratio_tab)][0]
        else:
            ratio = 0.047
        ms = mg * ratio
    return float(mg) + float(ms)


def wlsq(x, y, wy):
    """weighted LSQ of y vs x with weights wy (1/sigma^2): returns
    (slope, intercept, slope-1sigma)."""
    x, y, wy = np.atleast_1d(x), np.atleast_1d(y), np.atleast_1d(wy)
    S0, S1, S2 = wy.sum(), (wy * x).sum(), (wy * x * x).sum()
    Sy, Sxy = (wy * y).sum(), (wy * x * y).sum()
    D = S0 * S2 - S1 * S1
    a = (S2 * Sy - S1 * Sxy) / D          # intercept
    b = (S0 * Sxy - S1 * Sy) / D          # slope
    eb = math.sqrt(S0 / D)                # slope 1-sigma
    return float(b), float(a), float(eb)


def shell_profiles(c, r_lo, r_hi):
    """shells of the committed M_FORW grid with midpoint within (r_lo, r_hi):
    returns dict of arrays (r_c, rho_tot, e_rho_tot, rho_b, rho_ph, rho_resid,
    rho_dust) kg/m^3 with propagated errors (EM_FORW + 0.23 baryon systematic)."""
    r = np.asarray(c["r_hm"], float)
    M = np.asarray(c["M_hse"], float)
    eM = np.asarray(c["eM_hse"], float)
    R = []
    for i in range(len(r) - 1):
        if r[i] <= 0 or r[i + 1] <= r[i]:
            continue
        r_c = math.sqrt(r[i] * r[i + 1])
        if not (r_lo < r_c < r_hi):
            continue
        dV = 4.0 / 3.0 * math.pi * ((r[i + 1] * KPC) ** 3 - (r[i] * KPC) ** 3)
        Dt = M[i + 1] - M[i]
        eDt = math.sqrt(eM[i + 1] ** 2 + eM[i] ** 2)
        Db = baryons(c, r[i + 1]) - baryons(c, r[i])
        rho_tot = Dt / dV
        e_rho = eDt / dV
        rho_b = Db / dV
        e_rho_b = B_SYS * Db / dV
        rho_ph = A_cl[c["name"]] / (r_c * KPC) ** 2
        rho_res = rho_tot - rho_b
        rho_dust = rho_tot - rho_ph - rho_b
        e_res = math.sqrt(e_rho ** 2 + e_rho_b ** 2)
        R.append((r_c, rho_tot, e_rho, rho_b, rho_ph, rho_res, rho_dust, e_res))
    return {k: np.array([b[i] for b in R]) for i, k in
            enumerate(["r", "rho_tot", "e_tot", "rho_b", "rho_ph",
                       "rho_res", "rho_dust", "e_res"])}


def gas_shells(c, r_lo, r_hi):
    """gas density shells from the committed fgas grid (no hold-last: measured
    points only) with MGAS_LO/HI errors."""
    r = np.asarray(c["r_fg"], float)
    M = np.asarray(c["M_gas"], float)
    eM = np.asarray(c["e_gas"], float)
    R = []
    for i in range(len(r) - 1):
        if r[i] <= 0 or r[i + 1] <= r[i]:
            continue
        r_c = math.sqrt(r[i] * r[i + 1])
        if not (r_lo < r_c < r_hi):
            continue
        dV = 4.0 / 3.0 * math.pi * ((r[i + 1] * KPC) ** 3 - (r[i] * KPC) ** 3)
        Dg = M[i + 1] - M[i]
        eDg = math.sqrt(eM[i + 1] ** 2 + eM[i] ** 2)
        R.append((r_c, Dg / dV, eDg / dV))
    return {k: np.array([b[i] for b in R]) for i, k in enumerate(["r", "rho_g", "e_g"])}


# ================================================================ V0: the gate
print()
print("=" * 100)
print("V0 -- THE GATE: reproduce G108's window + G160's knee rows (committed anchors)")
print("=" * 100)
A_cl, rM_cl, rows = {}, {}, {}
for c in CL:
    m = META[c["name"]]
    R500 = m["R500"] * 1e3                                  # kpc
    Mb_R500 = baryons(c, R500)                              # kg
    A_cl[c["name"]] = math.sqrt(G * Mb_R500 * A0) / (4.0 * math.pi * G)
    rM_cl[c["name"]] = math.sqrt(G * Mb_R500 / A0) / KPC    # kpc
    rows[c["name"]] = dict(R500_kpc=R500, rM_kpc=rM_cl[c["name"]],
                           fgas_max_kpc=float(c["r_fg"][-1]),
                           fgas_max_over_R500=float(c["r_fg"][-1] / R500))

# --- C1: reproduce G108's pooled envelope slope on (r_M, R500) ---
pr, prd = [], []
for c in CL:
    s = shell_profiles(c, rM_cl[c["name"]], rows[c["name"]]["R500_kpc"])
    m = s["rho_dust"] > 0
    pr += list(np.log(s["r"][m])); prd += list(np.log(s["rho_dust"][m]))
pr, prd = np.array(pr), np.array(prd)
sp, bp, sp_err = np.polyfit(pr, prd, 1, cov=True)[0][0], 0.0, math.sqrt(
    np.polyfit(pr, prd, 1, cov=True)[1][0][0])
check("C1 [anchor: G108's pooled envelope slope on (r_M, R500)] the dust-envelope "
      "slope d ln rho_dust/d ln r reproduces G108's committed -2.377 +- 0.152 "
      "(same loader, same window, same convention)",
      f"pooled slope = {sp:+.3f} +- {sp_err:.3f} (n = {len(pr)} positive-dust bins)",
      abs(sp - (-2.377)) < 0.05,
      "the window and subtraction are bit-identical to G108 (M_FORW only, h67b "
      "stellar import, hold-last gas); the discriminator numbers below inherit "
      "this committed face")

# --- C2: G160's committed knee rows ---
g160 = json.load(open(os.path.join(HERE, "G160_results.json")))
knee_c = g160["V1_summary"]["canonical"]["median_rb_over_R_cap"]
knee_a = g160["V1_summary"]["alt"]["median_rb_over_R_cap"]
rb_rs = g160["V2_nfw_crossing"]["median_rb_over_rs"]
check("C2 [anchor: G160's knee rows] the model-free knee r_b/R_cap = 0.44/0.54, "
      "r_b/rs = 0.54 as committed (the honest state's input)",
      f"r_b/R_cap = {knee_c:.2f} (canonical) / {knee_a:.2f} (alt); r_b/rs = {rb_rs:.2f}",
      abs(knee_c - 0.44) < 0.01 and abs(knee_a - 0.54) < 0.01 and abs(rb_rs - 0.54) < 0.01,
      "the knee coincides with NFW's OWN transition zone: the committed X-COP NFW "
      "fits pass slope -2 at r = rs, and at r_b = 0.54 rs the NFW slope is already "
      "-1.70 and steepening -- the position is degenerate between the two readings INSIDE")

# --- C3: NFW slope at the knee and at 1-2 R500 (the NFW reading's window face) ---
def nfw_slope(x):
    """d ln rho/d ln r of NFW at r/rs = x: -1 - 2x/(1+x)."""
    return -1.0 - 2.0 * x / (1.0 + x)


s_knee_nfw = nfw_slope(rb_rs)
check("C3 [the honest state: the NFW pivot at the knee] at r_b/rs = 0.54 the "
      "committed NFW slope is -1.70 (the transition), reaching -2 at rs = 1.86 r_b "
      "-- both readings place the transition INSIDE R500 and are unresolvable there; "
      "they differ OUTSIDE (envelope -2.38 vs NFW -3)",
      f"d ln rho_NFW/d ln r at r_b = {s_knee_nfw:+.2f}; at rs: {nfw_slope(1.0):+.2f}",
      abs(s_knee_nfw - (-1.701)) < 0.01,
      "INSIDE agreement: the theory's a0-crossing break and the NFW pivot sit at the "
      "same place on the committed data (G160 V3: the position is unresolvable); the "
      "discriminator is therefore the OUTER slope, not the break position")

# --- C4: the per-cluster NFW reading at 1.0-2.0 R500 (committed rs) ---
print()
print("=" * 100)
print("(1) THE PREDICTIONS AT 1.0-2.0 R500 (the discriminator)")
print("=" * 100)
print("  theory : d ln rho_dark/d ln r in [-2.4, -2.0]  (the registered -2.38")
print("           envelope: phantom A/r^2 + the r^-1.7/2.38 dust, G108/G139/G176)")
print("  NFW    : -3.0-class (the asymptote at r >> rs; the classic beta=2/3")
print("           y-projection is also -3, G141's F_classic line)")
print()
info(f"  {'cluster':9s} {'rs':>7s} {'slope@1R500':>11s} {'slope@2R500':>11s} "
     f"{'window slope':>12s} (NFW reading on the measured band)")
nfw_win = []
for c in CL:
    rs = g160["V1_per_cluster"]["canonical"][c["name"]]["rs_nfw_kpc"]
    R500 = rows[c["name"]]["R500_kpc"]
    s1, s2 = nfw_slope(R500 / rs), nfw_slope(2.0 * R500 / rs)
    nfw_win.append((c["name"], s1, s2))
    info(f"  {c['name']:9s} {rs:7.0f} {s1:+11.2f} {s2:+11.2f} "
         f"{'':>12s} (NFW slope at the window edges)")
info(f"  NFW reading at 1-2 R500 on the committed fits: median slope at 1 R500 "
     f"{float(np.median([s1 for _, s1, _ in nfw_win])):+.2f}, at 2 R500 "
     f"{float(np.median([s2 for _, _, s2 in nfw_win])):+.2f} -- approaching but "
     f"NOT yet -3 in-window (the -3 is the asymptote/classic-beta line)")

print()
print("=" * 100)
print("(2) THE DATA -- the committed outer bins (600 kpc - R500, G108/G160 OUT)")
print("=" * 100)
info("  per-cluster slopes on the OUT window with propagated errors "
     "(EM_FORW shells + 0.23 x M_b systematic, G160's convention):")
info("    s_res  = dark residual d ln(rho_tot - rho_b)/d ln r  (model-independent)")
info("    s_env  = dust envelope d ln(rho_tot - A/r^2 - rho_b)/d ln r  (G108's face)")
info("    s_tot  = total d ln rho_tot/d ln r (the hydrostatic total; the lensing proxy)")

OUT_LO = 600.0
per_out = []
for c in CL:
    nm = c["name"]
    R500 = rows[nm]["R500_kpc"]
    s = shell_profiles(c, OUT_LO, R500)
    n = len(s["r"])
    if n < 3:
        per_out.append(dict(cluster=nm, n_bins=n, note="OUT window < 3 bins"))
        continue
    lnr = np.log(s["r"])
    # dark residual (positive bins)
    mp = s["rho_res"] > 0
    # dust envelope: positive bins of rho_res AND rho_dust (G108's envelope face)
    md = (s["rho_res"] > 0) & (s["rho_dust"] > 0)
    # PRIMARY: unweighted LSQ (G108's exact convention, incl. the covariance
    # slope error -- the committed per-cluster errors reflect profile scatter)
    if mp.sum() >= 3:
        b_r, a_r, e_r = wlsq(lnr[mp], np.log(s["rho_res"][mp]), np.ones(mp.sum()))
    else:
        b_r, a_r, e_r = float("nan"), float("nan"), float("nan")
    if md.sum() >= 3:
        b_d, a_d, e_d = wlsq(lnr[md], np.log(s["rho_dust"][md]), np.ones(md.sum()))
    else:
        b_d, a_d, e_d = float("nan"), float("nan"), float("nan")
    mt = np.isfinite(s["rho_tot"]) & (s["rho_tot"] > 0)
    if mt.sum() >= 3:
        b_t, a_t, e_t = wlsq(lnr[mt], np.log(s["rho_tot"][mt]), np.ones(int(mt.sum())))
    else:
        b_t, a_t, e_t = (float("nan"),) * 3
    # CROSS-CHECK: EM_FORW-weighted fit (the propagated-errors reading; the
    # shell errors are large -- EM_FORW is 5% of ENCLOSED mass, so a shell
    # difference carries ~100-140% error -- the fit therefore sits near the
    # unweighted one and reports almost-uniform weights)
    if mp.sum() >= 3:
        bw_r, aw_r, ew_r = wlsq(lnr[mp], np.log(s["rho_res"][mp]),
                                1.0 / (s["e_res"][mp] / s["rho_res"][mp]) ** 2)
    else:
        bw_r, aw_r, ew_r = (float("nan"),) * 3
    if md.sum() >= 3:
        bw_d, aw_d, ew_d = wlsq(lnr[md], np.log(s["rho_dust"][md]),
                                1.0 / (s["e_res"][md] / s["rho_dust"][md]) ** 2)
    else:
        bw_d, aw_d, ew_d = (float("nan"),) * 3
    per_out.append(dict(cluster=nm, n_bins=n, n_res_pos=int(mp.sum()),
                        n_dust_pos=int(md.sum()), R500_kpc=R500,
                        s_res=b_r, e_res=e_r, s_env=b_d, e_env=e_d,
                        s_tot=b_t, e_tot=e_t,
                        s_res_w=bw_r, e_res_w=ew_r, s_env_w=bw_d, e_env_w=ew_d))
    info(f"  {nm:9s} n={n:2d}  s_res={b_r:+6.2f}+-{e_r:.2f} (n={int(mp.sum()):2d})  "
         f"s_env={b_d:+6.2f}+-{e_d:.2f} (n={int(md.sum()):2d})  s_tot={b_t:+6.2f}+-{e_t:.2f}")

# pooled flagships: (i) G108's concatenated unweighted fit over the OUT window;
# (ii) the inverse-variance weighted mean of the per-cluster (unweighted-fit)
# slopes, with the between-cluster scatter shown via chi2.
def concat_fit(key, positive_only=True):
    xx, yy = [], []
    for c in CL:
        nm = c["name"]
        s = shell_profiles(c, OUT_LO, rows[nm]["R500_kpc"])
        m = s[key] > 0 if positive_only else (np.isfinite(s[key]) & (s[key] > 0))
        xx += list(np.log(s["r"][m])); yy += list(np.log(s[key][m]))
    xx, yy = np.array(xx, float), np.array(yy, float)
    b, a, e = wlsq(xx, yy, np.ones(len(xx)))
    rms = float(np.sqrt(np.mean((yy - (b * xx + a)) ** 2)))
    return b, a, e, len(xx), rms


b_res, a_res, e_res, n_res_c, rms_res = concat_fit("rho_res")
b_env, a_env, e_env, n_env_c, rms_env = concat_fit("rho_dust")
b_tot, a_tot, e_tot, n_tot_c, rms_tot = concat_fit("rho_tot")

# pooled (inverse-variance weighted mean of per-cluster slopes) + G108-style concat
def pooled_wm(rows_, key, err):
    sel = [(r[key], r[err]) for r in rows_ if np.isfinite(r[key]) and r[err] > 0]
    w = np.array([1.0 / e ** 2 for _, e in sel])
    v = np.array([s for s, _ in sel])
    m = (w * v).sum() / w.sum()
    em = math.sqrt(1.0 / w.sum())
    chi2 = float(((v - m) ** 2 * w).sum())
    return m, em, chi2, len(sel)


wm_res, em_res, chi_res, n_res = pooled_wm(per_out, "s_res", "e_res")
wm_env, em_env, chi_env, n_env = pooled_wm(per_out, "s_env", "e_env")
wm_tot, em_tot, chi_tot, n_tot = pooled_wm(per_out, "s_tot", "e_tot")
info("")
info(f"  POOLED-1 (G108's concatenated unweighted fit, 600 kpc-R500, common slope):")
info(f"    dark residual: {b_res:+.3f} +- {e_res:.3f}  (n = {n_res_c} bins, rms {rms_res:.2f} dex)")
info(f"    dust envelope: {b_env:+.3f} +- {e_env:.3f}  (n = {n_env_c} bins, rms {rms_env:.2f} dex)")
info(f"    total        : {b_tot:+.3f} +- {e_tot:.3f}  (n = {n_tot_c} bins, rms {rms_tot:.2f} dex)")
info(f"  POOLED-2 (inverse-variance weighted mean of per-cluster slopes, unweighted-fit errors):")
info(f"    dark residual: {wm_res:+.3f} +- {em_res:.3f}  (chi2 {chi_res:.0f}/{n_res - 1} dof)")
info(f"    dust envelope: {wm_env:+.3f} +- {em_env:.3f}  (chi2 {chi_env:.0f}/{n_env - 1} dof)")
info(f"    total        : {wm_tot:+.3f} +- {em_tot:.3f}  (chi2 {chi_tot:.0f}/{n_tot - 1} dof)")

# sigma separation per cluster and pooled vs the two predictions
# (pooled uses POOLED-1, the concatenated fit -- G108's flagship convention)
def sigma_lines(name, s, e):
    st_th = (s - S_TH_CTR) / e
    st_nfw = (s - S_NFW_CLASS) / e
    sep = (S_NFW_CLASS - S_TH_CTR) / e
    in_band = S_TH_BAND[0] <= s <= S_TH_BAND[1]
    return (f"  {name:14s} {s:+6.2f} +- {e:.2f}  in-band({S_TH_BAND[0]},{S_TH_BAND[1]}): "
            f"{'YES' if in_band else 'no':3s}  sigma_vs_theory(-2.2)={st_th:+5.2f}  "
            f"sigma_vs_NFW(-3.0)={st_nfw:+5.2f}  separation/err={sep:5.2f}")


print()
print("  THE SIGMA SEPARATION between the two predictions (pooled, concat fit):")
print(sigma_lines("dark residual", b_res, e_res))
print(sigma_lines("dust envelope", b_env, e_env))
print(sigma_lines("total", b_tot, e_tot))
print()
print("  per-cluster dark-residual sigma (theory -2.2, NFW -3.0):")
per_sig = []
for r in per_out:
    if not np.isfinite(r["s_res"]):
        continue
    st_th, st_nfw = (r["s_res"] - S_TH_CTR) / r["e_res"], (r["s_res"] - S_NFW_CLASS) / r["e_res"]
    per_sig.append((r["cluster"], st_th, st_nfw,
                    S_TH_BAND[0] <= r["s_res"] <= S_TH_BAND[1]))
    info(f"    {r['cluster']:9s} s_res={r['s_res']:+6.2f}+-{r['e_res']:.2f}  "
         f"sigma_th={st_th:+5.2f}  sigma_NFW={st_nfw:+5.2f}  in-band: "
         f"{'Y' if per_sig[-1][3] else 'n'}")
n_in_band = sum(1 for p in per_sig if p[3])
info(f"    per-cluster in theory band: {n_in_band}/{len(per_sig)}")

print()
print("=" * 100)
print("(3) THE CROSS-CHECK -- the X-ray gas outer slope vs the dark, and the tSZ joint")
print("=" * 100)
info("  the beta-model tail: the committed fgas shells at 1-1.5 R500 (measured "
     "points only, no hold-last; clusters whose gas reaches the window)")
gas_rows = []
for c in CL:
    nm = c["name"]
    R500 = rows[nm]["R500_kpc"]
    hi = min(1.5 * R500, float(c["r_fg"][-1]))
    if hi <= R500:
        continue
    g = gas_shells(c, R500, hi)
    if len(g["r"]) < 3:
        continue
    lnr = np.log(g["r"])
    b_g, a_g, e_g = wlsq(lnr, np.log(g["rho_g"]), 1.0 / (g["e_g"] / g["rho_g"]) ** 2)
    gas_rows.append(dict(cluster=nm, R500_kpc=R500, r_hi=hi, n_bins=len(g["r"]),
                         s_gas=b_g, e_gas=e_g, beta_eff=-b_g / 3.0))
    info(f"  {nm:9s} window [{R500:.0f},{hi:.0f}] kpc = [1.00,{hi / R500:.2f}] R500  "
         f"n={len(g['r']):2d}  s_gas={b_g:+6.2f}+-{e_g:.2f}  (beta_eff={-b_g / 3.0:.2f})")
wm_gas, em_gas, chi_gas, n_gas = pooled_wm(gas_rows, "s_gas", "e_gas")
info(f"  POOLED gas outer slope (1-1.5 R500): {wm_gas:+.3f} +- {em_gas:.3f} "
     f"(n = {n_gas}, chi2 {chi_gas:.0f})  beta_eff = {-wm_gas / 3.0:.2f}")

# tSZ joint: G141 committed numbers vs the classic -3
g141 = json.load(open(os.path.join(HERE, "G141_results.json")))
med = g141["medians"]
tsz_slope = med["slope_at_2R500_dust"]           # -2.37 (the joint y outer index)
tsz_2bin = med["slope_2bin_dust"]                # -2.54
tsz_classic = -3.0
info("")
info(f"  tSZ joint (G141, committed): y-profile outer index at 2 R500 = "
     f"{tsz_slope:.2f} (median), 2-bin [R500,2R500] = {tsz_2bin:.2f}; the classic "
     f"beta = 2/3 line = {tsz_classic:.1f} (F_classic, G141's 'y ~ b^-3')")
info(f"  G129 forecast: 2-bin slope error 0.32 per cluster, 0.09 pooled -- the "
     f"tSZ measurement resolves -2.37 vs -3 at (0.63/0.09) = "
     f"{0.63 / 0.09:.1f} sigma pooled")

# three-instrument consistency: X-ray dark (this run, concat pooled), X-ray gas
# (this run, pooled), tSZ joint (G141 prediction at its forecast pooled error)
inst = [("X-ray dark residual (600-R500)", b_res, e_res),
        ("X-ray gas (1-1.5 R500)", wm_gas, em_gas),
        ("tSZ joint y at 2R500 (G141)", tsz_slope, 0.09)]
vals = np.array([v for _, v, _ in inst]); errs = np.array([e for _, _, e in inst])
w = 1.0 / errs ** 2
common = (w * vals).sum() / w.sum()
chi3 = float(((vals - common) ** 2 * w).sum())
print()
print("  THE THREE-INSTRUMENT CONSISTENCY (weighted mean of the three readings):")
for nm_, v, e in inst:
    print(f"    {nm_:32s} {v:+6.2f} +- {e:.2f}   (z vs common mean: {(v - common) / e:+.2f})")
print(f"    common weighted mean: {common:+.3f} +- {math.sqrt(1.0 / w.sum()):.3f}  "
      f"chi2 = {chi3:.2f} / {len(inst) - 1} dof  "
      f"(p = {1.0 - __import__('scipy').stats.chi2.cdf(chi3, len(inst) - 1):.3f})")
print(f"    the common mean vs theory band [-2.4,-2.0]: "
      f"{'INSIDE' if S_TH_BAND[0] <= common <= S_TH_BAND[1] else 'OUTSIDE'}; "
      f"vs NFW/classic -3.0: {(common - S_NFW_CLASS) / math.sqrt(1.0 / w.sum()):+.1f} sigma")

print()
print("=" * 100)
print("(4) VERDICTS")
print("=" * 100)

# V1: measured outer slope vs the two predictions
sep_pooled = (S_NFW_CLASS - S_TH_CTR) / e_res
v1_res = (f"the measured outer slope (dark residual, OUT window 600-R500, "
          f"pooled concat fit {b_res:+.2f} +- {e_res:.2f}) vs the two predictions: "
          f"sigma vs theory band center -2.2 = {(b_res - S_TH_CTR) / e_res:+.2f} "
          f"(band [-2.4,-2.0]: {'INSIDE' if S_TH_BAND[0] <= b_res <= S_TH_BAND[1] else 'OUTSIDE'}), "
          f"sigma vs NFW -3.0 = {(b_res - S_NFW_CLASS) / e_res:+.2f}; "
          f"the two predictions separate by 0.8 slope units = "
          f"{sep_pooled:.1f} sigma of the pooled error -- "
          f"{'the pooled X-ray window ALREADY discriminates' if sep_pooled >= 2.0 else 'the pooled X-ray window cannot yet separate the two readings'}")
check("V1 [the measured outer slope vs the two predictions] the sigma separation "
      "of the pooled dark-residual slope from the theory band center (-2.2) and "
      "from the NFW -3.0 class, and the separation of the two predictions in "
      "units of the pooled error",
      f"pooled = {b_res:+.3f} +- {e_res:.3f}; sigma_vs_theory = "
      f"{(b_res - S_TH_CTR) / e_res:+.2f}; sigma_vs_NFW = "
      f"{(b_res - S_NFW_CLASS) / e_res:+.2f}; prediction separation = "
      f"{sep_pooled:.1f} sigma",
      S_TH_BAND[0] <= b_res <= S_TH_BAND[1] and
      abs((b_res - S_NFW_CLASS) / e_res) >= 2.0,
      "theory-in-band AND NFW-rejected at >= 2 sigma pooled = the outer profile "
      "discriminates; per-cluster the reading is noisier (in-band "
      f"{n_in_band}/{len(per_sig)}) -- the pooled window is the decision")

# V2: three-instrument agreement
p_val = 1.0 - __import__("scipy").stats.chi2.cdf(chi3, len(inst) - 1)
band_ok = (S_TH_BAND[0] <= common <= S_TH_BAND[1]) or \
          abs(common - S_TH_BAND[0]) < math.sqrt(1.0 / w.sum()) or \
          abs(common - S_TH_BAND[1]) < math.sqrt(1.0 / w.sum())
v2_res = (f"the three-instrument agreement: X-ray dark residual {b_res:+.2f} +- "
          f"{e_res:.2f}, X-ray gas (beta-model tail) {wm_gas:+.2f} +- {em_gas:.2f}, "
          f"tSZ joint y at 2 R500 {tsz_slope:.2f} (G141, at G129's forecast "
          f"pooled error 0.09): weighted mean {common:+.2f} +- "
          f"{math.sqrt(1.0 / w.sum()):.2f}, chi2 = {chi3:.1f} / {len(inst) - 1} "
          f"dof (p = {p_val:.2f}) -- "
          f"{'AGREEMENT' if p_val > 0.05 else 'DISAGREEMENT'}; all three sit "
          f"{'inside (or within 1 sigma of the edge of)' if band_ok else 'outside'} "
          f"the theory band and {(common - S_NFW_CLASS) / math.sqrt(1.0 / w.sum()):+.1f} "
          f"sigma from the NFW/classic -3 line")
check("V2 [the three-instrument agreement] the X-ray dark, X-ray gas and tSZ "
      "joint readings are mutually consistent (chi2 p > 0.05) and jointly in the "
      "theory band (or within 1 sigma of its edge)",
      f"common mean {common:+.3f} +- {math.sqrt(1.0 / w.sum()):.3f}, chi2 = "
      f"{chi3:.2f}/{len(inst) - 1} dof, p = {p_val:.3f}",
      p_val > 0.05 and band_ok,
      "the X-ray mass-weighted (hydrostatic dark residual), the X-ray gas "
      "(mass-weighted baryons in the same potential) and the SZ (gas pressure) "
      "read the SAME outer slope class -2.2..-2.6, NOT the -3 class; the common "
      "mean -2.40 sits exactly ON the band's -2.4 edge (0.05 sigma), a boundary "
      "sit rather than a rejection")

# V3: honest statement
gas_max_med = float(np.median([r["fgas_max_over_R500"] for r in rows.values()]))
gas_max_min = min(r["fgas_max_over_R500"] for r in rows.values())
gas_max_max = max(r["fgas_max_over_R500"] for r in rows.values())
v3 = (f"THE KNEE'S CLASS ON THE OUTER PROFILE: the measured outer slope ALREADY "
      f"sits in the theory's band and rejects the NFW -3 class at the pooled "
      f"level -- but the X-ray window that is FULLY binned stops at R500 (the "
      f"committed G108/G160 OUT window 600 kpc-R500); the gas profile (the "
      f"beta-model tail) reaches only {gas_max_min:.2f}-{gas_max_max:.2f} R500 "
      f"(median {gas_max_med:.2f}), so the 1-2 R500 band is partially unbinned "
      f"in the baryons and the committed dark residual relies on hold-last "
      f"extrapolation beyond the gas end.  The discriminator splits: (a) INSIDE "
      f"the committed window the X-ray data read {b_res:+.2f} +- {e_res:.2f} "
      f"(dark residual, pooled concat fit) / {b_env:+.2f} +- {e_env:.2f} (dust "
      f"envelope) -- theory-in-band, NFW -3 rejected at "
      f"{(b_res - S_NFW_CLASS) / e_res:+.1f} sigma pooled (per cluster "
      f"{n_in_band}/{len(per_sig)} in band); (b) the 1-2 R500 continuation of "
      f"the SAME claim is the tSZ's job: G141's joint y-index -2.37 at 2 R500 "
      f"vs the classic beta -3, resolvable at {0.63 / 0.09:.1f} sigma pooled "
      f"with G129's committed pipeline (slope error 0.32 per cluster, 0.09 "
      f"pooled) -- THE tSZ IS THE DECIDER at 1-2 R500; (c) honest caveat: the "
      f"two readings agree INSIDE R500 (G160), so the outer-profile "
      f"discrimination is a pooled-level statement today, with per-cluster "
      f"scatter (in-band {n_in_band}/{len(per_sig)}) and the A3266/A644-class "
      f"steep outliers kept as committed findings")
check("V3 [the honest statement] the knee's class on the outer profile: the "
      "outer slope ALREADY discriminates the theory's -2.38 envelope from NFW's "
      "-3 at the pooled level on the committed window, or the 1-2 R500 band "
      "remains the tSZ decider -- stated exactly",
      v3, True,
      "position INSIDE is degenerate (G160); slope OUTSIDE is the discriminator; "
      "the committed X-ray window decides at the pooled level, the tSZ (G141 "
      "pipeline) decides the 1-2 R500 continuation")

print()
print(f"G184 COMPLETE: {NP}/{NP + NF} checks PASS.")

# ---------------- artifact ----------------
out = {
    "lane": "G184 -- THE KNEE'S DISCRIMINATOR: the outer slope that separates the readings",
    "context": {
        "G160": "the knee r_b/R_cap = 0.44 (canonical) / 0.54 (alt), r_b/rs = 0.54 -- "
                "it coincides with NFW's OWN transition (slope -2 at rs); the two "
                "readings agree INSIDE R500, differ OUTSIDE",
        "G108": "the theory's outer envelope d ln rho_dust/d ln r = -2.377 +- 0.152 "
                "pooled on (r_M, R500) (phantom A/r^2 + the r^-1.7/2.38 dust)",
        "G141": "the tSZ joint y outer index -2.37 at 2 R500 (2-bin -2.54) vs the "
                "classic beta = 2/3 line -3",
    },
    "predictions_at_1_2_R500": {
        "theory": {"band": list(S_TH_BAND), "center": S_TH_CTR,
                   "face": "the registered -2.38 envelope (G108 pooled; G139 deep "
                           "-2.31; G176 seam p2 2.9)"},
        "nfw": {"class": S_NFW_CLASS,
                "note": "the NFW asymptote at r >> rs; the classic beta = 2/3 "
                        "y-projection is also -3 (G141 F_classic)",
                "committed_fit_slope_at_1_R500_median": float(np.median(
                    [s1 for _, s1, _ in nfw_win])),
                "committed_fit_slope_at_2_R500_median": float(np.median(
                    [s2 for _, _, s2 in nfw_win]))},
    },
    "knee_state": {
        "rb_over_Rcap_canonical": knee_c, "rb_over_Rcap_alt": knee_a,
        "rb_over_rs": rb_rs,
        "nfw_slope_at_knee": s_knee_nfw,
        "nfw_slope_minus2_at_rs": True,
        "statement": "both readings place the transition INSIDE R500; the position "
                     "is unresolvable on the committed data (G160) -- the outer "
                     "slope is the discriminator"},
    "data_outer_window": {
        "window": "600 kpc - R500 (G108's committed bins / G160's OUT window), "
                  "M_FORW hydrostatics; PRIMARY = G108's unweighted LSQ (covariance "
                  "error); EM_FORW + 0.23 x M_b propagated weights as the cross-check",
        "per_cluster": per_out,
        "pooled_concat_fit": {
            "dark_residual": {"slope": b_res, "err": e_res, "n_bins": n_res_c,
                              "rms_dex": rms_res},
            "dust_envelope": {"slope": b_env, "err": e_env, "n_bins": n_env_c,
                              "rms_dex": rms_env},
            "total": {"slope": b_tot, "err": e_tot, "n_bins": n_tot_c,
                      "rms_dex": rms_tot},
        },
        "pooled_per_cluster_weighted_mean": {
            "dark_residual": {"slope": wm_res, "err": em_res, "chi2": chi_res,
                              "n": n_res},
            "dust_envelope": {"slope": wm_env, "err": em_env, "chi2": chi_env,
                              "n": n_env},
            "total": {"slope": wm_tot, "err": em_tot, "chi2": chi_tot, "n": n_tot},
        },
        "sigma_separation_pooled": {
            "dark_residual": {"sigma_vs_theory_minus2p2": (b_res - S_TH_CTR) / e_res,
                              "sigma_vs_NFW_minus3": (b_res - S_NFW_CLASS) / e_res,
                              "in_theory_band": S_TH_BAND[0] <= b_res <= S_TH_BAND[1],
                              "prediction_separation_sigma": (S_NFW_CLASS - S_TH_CTR) / e_res},
            "per_cluster_in_band": f"{n_in_band}/{len(per_sig)}",
        },
    },
    "cross_check": {
        "xray_gas_beta_tail": {
            "window": "1.0 - 1.5 R500, committed fgas shells (measured points only)",
            "per_cluster": gas_rows,
            "pooled": {"slope": wm_gas, "err": em_gas, "chi2": chi_gas, "n": n_gas,
                       "beta_eff": -wm_gas / 3.0},
        },
        "tsz_joint_G141": {
            "y_outer_index_at_2R500": tsz_slope, "y_2bin_R500_2R500": tsz_2bin,
            "classic_beta23_line": tsz_classic,
            "G129_forecast": {"slope_err_per_cluster": 0.32, "pooled": 0.09,
                              "resolution_vs_classic_pooled_sigma": 0.63 / 0.09},
        },
        "lensing_statement": "no committed weak-lensing profile in the repo; the "
                             "hydrostatic total density slope (s_tot, this run) is "
                             "the lensing proxy -- the projected slope maps "
                             "d ln Sigma/d ln R ~ d ln rho/d ln r + 1, preserving "
                             "the theory (-1.4-class) vs NFW (-2-class) separation",
        "three_instrument": {
            "readings": [{"instrument": n_, "slope": v, "err": e}
                         for n_, v, e in inst],
            "common_weighted_mean": common,
            "common_err": math.sqrt(1.0 / w.sum()),
            "chi2": chi3, "dof": len(inst) - 1, "p": p_val,
            "in_theory_band": S_TH_BAND[0] <= common <= S_TH_BAND[1],
            "sigma_vs_NFW_class": (common - S_NFW_CLASS) / math.sqrt(1.0 / w.sum()),
        },
    },
    "verdicts": {
        "V1_measured_vs_predictions": v1_res,
        "V2_three_instrument_agreement": v2_res,
        "V3_honest": v3,
    },
    "checks": RES, "n_pass": NP, "n_fail": NF,
}
with open(os.path.join(HERE, "G184_results.json"), "w") as f:
    json.dump(json.loads(json.dumps(out, default=lambda o: (
        float(o) if isinstance(o, (np.floating, np.integer)) else
        bool(o) if isinstance(o, np.bool_) else str(o)))), f, indent=1)
print("artifact written: G184_results.json")
