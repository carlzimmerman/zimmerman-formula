#!/usr/bin/env python3
"""CFG304 -- which HI flux scale is right for MIGHTEE-HI COSMOS: the published catalogue's S_HI, or the raw r1p0
cube fluxes of CFG302 (about 0.50 of the catalogue for detections)?  Arbiter: the single-dish Arecibo ALFALFA
alpha.100 integrated flux S21 (3.5 arcmin beam; does not resolve flux out, can be confused by neighbours).

Frozen criteria: FROZEN_CRITERIA.md, committed 336b36f8f before any per-galaxy flux was read.

A flux-calibration check, not an a0 measurement.  The only a0 numbers are a REPORTED consequence: CFG301's committed
pooled baryon-band rows interpolated at the measured flux offset (CFG301 is not re-run).  kappa = 1/2 is FITTED.
No knob scans, no downloads, no other lane's file is written.

Usage (from anywhere):
    python3 cfg304_flux_scale_alfalfa.py              # main run
    MUTATE=a python3 cfg304_flux_scale_alfalfa.py     # catalogue S_HI x 0.5 (the brief's literal mutation)
    MUTATE=b python3 cfg304_flux_scale_alfalfa.py     # ALFALFA S21 x 0.5 (flip test from 'catalogue confirmed')
    MUTATE=c python3 cfg304_flux_scale_alfalfa.py     # ALFALFA S21 x 2   (flip test from 'cube confirmed')
Outputs (named by mode): cfg304_flux_scale_alfalfa[_MUTATE_x].out / _results.json, cfg304_matched_pairs[_MUTATE_x].csv
"""
import hashlib
import json
import math
import os
import re
import sys
import time

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CAT = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv")
C302 = os.path.join(REPO, "campaign_fresh_gravity", "CFG302_mightee_cube_raw_widths", "cfg302_per_galaxy.csv")
ALF = os.path.join(REPO, "data_assembly", "alfalfa_sdss_local_control", "alfalfa_sdss.csv")
D301 = os.path.join(REPO, "campaign_fresh_gravity", "CFG301_mightee_hi_catalogue_width_chain")
J301 = os.path.join(D301, "cfg301_stageB_results.json")
O301 = os.path.join(D301, "cfg301_stageA.out")
FROZEN = "336b36f8f"

MUT = os.environ.get("MUTATE", "").strip().lower()
if MUT not in ("", "a", "b", "c"):
    sys.exit("MUTATE must be empty, a, b or c")
TAG = f"_MUTATE_{MUT}" if MUT else ""
OUT = os.path.join(HERE, f"cfg304_flux_scale_alfalfa{TAG}.out")
JOUT = os.path.join(HERE, f"cfg304_flux_scale_alfalfa{TAG}_results.json")
POUT = os.path.join(HERE, f"cfg304_matched_pairs{TAG}.csv")

# ---------------------------------------------------------------- frozen constants (FROZEN_CRITERIA.md)
C_KMS = 299792.458
NU0_HZ = 1420.40575177e6
R_MATCH = 60.0          # arcsec, M1
DV_MATCH = 300.0        # km/s, M2
R_CONF = 210.0          # arcsec (3.5 arcmin), section 3
DV_CONF_ADD = 200.0     # km/s added to W50_t, section 3
B_BOOT = 10000
SEED_BOOT = 304
SEED_SHUF = 3041
K_SHUF = 200
SHUF_ARCMIN = 10.0
ALF_SHA = "c790a7ec68c45b66a86be1bc6317b9b29da6b8736baa013e97af21fb40599ed2"
CAT_SHA_PREFIX = "bcf9e8558bc56448"
ORCH_COUNT = 23
TOL_CAT, TOL_CUBE = 0.10, 0.15                 # decision thresholds (dex)
NMIN_CAT, NMIN_CUBE = 8, 5                     # primary set minimum sizes
NMIN_CAT_CLEAN, NMIN_CUBE_CLEAN = 5, 3         # CLEAN-C1 votes only above these
PH2_SNR = 2.48                                 # CFG302's post hoc calibrated 5 sigma (variant only)
FG_301 = None                                  # CFG301 pooled median gas fraction (parsed below)

LINES = []
CHECKS = []


def P(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s, flush=True)


def check(name, detail, ok):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def rel(p):
    return os.path.relpath(p, REPO)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tobool(s):
    if s.dtype == bool:
        return s.values
    return s.astype(str).str.strip().str.lower().isin(("true", "1", "1.0")).values


def angsep_arcsec(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    h = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(h, 0, 1)))) * 3600.0


def offset(ra, de, pa, d_arcmin):
    """exact spherical destination of a d_arcmin step at position angle pa (radians, east of north)"""
    d = math.radians(d_arcmin / 60.0)
    la1, lo1 = np.radians(de), np.radians(ra)
    la2 = np.arcsin(np.sin(la1) * np.cos(d) + np.cos(la1) * np.sin(d) * np.cos(pa))
    lo2 = lo1 + np.arctan2(np.sin(pa) * np.sin(d) * np.cos(la1), np.cos(d) - np.sin(la1) * np.sin(la2))
    return np.degrees(lo2) % 360.0, np.degrees(la2)


def candidates(mra, mde, mcz, ara, ade, acz):
    sep = angsep_arcsec(mra[:, None], mde[:, None], ara[None, :], ade[None, :])
    dcz = mcz[:, None] - acz[None, :]
    ok = (sep <= R_MATCH) & (np.abs(dcz) <= DV_MATCH)
    im, ja = np.nonzero(ok)
    return im, ja, sep[im, ja], dcz[im, ja]


def greedy(im, ja, sep, dcz):
    """M4: one-to-one, sorted by separation, ties by |dcz|"""
    order = np.lexsort((np.abs(dcz), sep))
    um, ua, out = set(), set(), []
    for k in order:
        if im[k] in um or ja[k] in ua:
            continue
        um.add(int(im[k])); ua.add(int(ja[k])); out.append((int(im[k]), int(ja[k]), float(sep[k]), float(dcz[k])))
    lost = sorted(set(int(i) for i in im) - um)
    return out, lost, len(set(int(i) for i in im))


def robust(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if x.size == 0:
        return dict(n=0, median=np.nan, mean=np.nan, robust_scatter=np.nan)
    med = float(np.median(x))
    return dict(n=int(x.size), median=med, mean=float(np.mean(x)), robust_scatter=float(1.4826 * np.median(np.abs(x - med))))


def boot(x, ss):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if x.size < 2:
        return dict(p16=np.nan, p84=np.nan, p2_5=np.nan, p97_5=np.nan)
    rng = np.random.default_rng(ss)
    meds = np.median(x[rng.integers(0, x.size, (B_BOOT, x.size))], axis=1)
    q = np.percentile(meds, [16, 84, 2.5, 97.5])
    return dict(p16=float(q[0]), p84=float(q[1]), p2_5=float(q[2]), p97_5=float(q[3]))


def decide(rc, rk, nc, nk, nmc=NMIN_CAT, nmk=NMIN_CUBE):
    if nc < nmc or nk < nmk or not (np.isfinite(rc) and np.isfinite(rk)):
        return "undecided (insufficient pairs)"
    if abs(rc) <= TOL_CAT and rk <= -TOL_CUBE:
        return "catalogue scale confirmed"
    if abs(rk) <= TOL_CAT and rc >= TOL_CUBE:
        return "cube scale confirmed"
    if abs(rc) > TOL_CAT and abs(rk) > TOL_CAT:
        return "neither"
    return "undecided"


def strength(dec, bc, bk):
    if dec == "catalogue scale confirmed":
        return "firm" if (bc["p16"] >= -TOL_CAT and bc["p84"] <= TOL_CAT and bk["p84"] <= -TOL_CUBE) else "marginal"
    if dec == "cube scale confirmed":
        return "firm" if (bk["p16"] >= -TOL_CAT and bk["p84"] <= TOL_CAT and bc["p16"] >= TOL_CUBE) else "marginal"
    if dec == "neither":
        out = lambda b: b["p16"] > TOL_CAT or b["p84"] < -TOL_CAT
        return "firm" if (out(bc) and out(bk)) else "marginal"
    return "n/a"


def conv(S, nu_hz, mode):
    if mode == "OPT":
        return S * C_KMS * NU0_HZ / nu_hz ** 2
    if mode == "REST":
        return S * C_KMS / nu_hz
    if mode == "RADIO":
        return S * C_KMS / NU0_HZ
    raise ValueError(mode)


# ================================================================== load
def load():
    cat = pd.read_csv(CAT)
    c302 = pd.read_csv(C302)
    alf = pd.read_csv(ALF, dtype={"sdss_objid": "string", "name_oc": "string"})
    return cat, c302, alf


def bookkeeping_checks(cat, c302, alf, shas):
    P("\nBOOKKEEPING CHECKS (raw, unmutated inputs)")
    check("K1 input sha256 (ALFALFA exact; MIGHTEE prefix)", f"ALFALFA {shas['alfalfa'][:16]}...; MIGHTEE {shas['mightee'][:16]}...",
          shas["alfalfa"] == ALF_SHA and shas["mightee"].startswith(CAT_SHA_PREFIX))
    nu = cat.freq_MHz.values * 1e6
    dz = np.abs(cat.z_HI.values - (NU0_HZ / nu - 1))
    check("K2 catalogue z_HI = nu0/freq - 1 to <= 1e-5 (all rows)", f"max |dz| {np.nanmax(dz):.2e} over {len(cat)} rows", np.nanmax(dz) <= 1e-5)
    j = c302.merge(cat[["ID_catalogue", "S_HI_Jy_Hz"]], left_on="ID", right_on="ID_catalogue", how="left")
    rr = np.abs(j.S_cat.values / j.S_HI_Jy_Hz.values - 1)
    check("K3 CFG302 S_cat equals the catalogue S_HI_Jy_Hz (relative <= 1e-6)", f"{np.isfinite(rr).sum()} of {len(j)} joined; max rel {np.nanmax(rr):.2e}",
          np.isfinite(rr).all() and np.nanmax(rr) <= 1e-6)
    good = (cat.S_HI_Jy_Hz > 0) & (cat.D_L_Mpc > 0)
    du = cat.log_M_HI[good].values - np.log10(49.7 * cat.D_L_Mpc[good].values ** 2 * cat.S_HI_Jy_Hz[good].values)
    zz = cat.z_HI[good].values
    # informational: the (1+z) power that would best absorb the residual
    pw = float(np.median(du / np.log10(1 + zz))) if np.all(zz > 0) else np.nan
    check("K4 U1 log_M_HI vs log10(49.7 D_L^2 S_HI): median |delta| <= 0.03 dex", f"n {good.sum()}; median |delta| {np.median(np.abs(du)):.4f}; signed median {np.median(du):+.4f}; "
          f"max |delta| {np.max(np.abs(du)):.4f}; residual / log(1+z) median {pw:+.2f} (information)", np.median(np.abs(du)) <= 0.03)
    return dict(K2_max_dz=float(np.nanmax(dz)), K3_max_rel=float(np.nanmax(rr)), U1_median_abs=float(np.median(np.abs(du))),
                U1_signed_median=float(np.median(du)), U1_max_abs=float(np.max(np.abs(du))), U1_resid_over_log1pz=pw)


def mutate(cat, alf, mode):
    cat, alf = cat.copy(), alf.copy()
    if mode == "a":
        cat["S_HI_Jy_Hz"] = cat.S_HI_Jy_Hz * 0.5; cat["S_HI_Jy_Hz_err"] = cat.S_HI_Jy_Hz_err * 0.5
    elif mode == "b":
        alf["s21_jykms"] = alf.s21_jykms * 0.5; alf["e_s21_jykms"] = alf.e_s21_jykms * 0.5
    elif mode == "c":
        alf["s21_jykms"] = alf.s21_jykms * 2.0; alf["e_s21_jykms"] = alf.e_s21_jykms * 2.0
    return cat, alf


# ================================================================== the analysis (one call per data state)
SET_ORDER = ["C1", "ALL", "C2", "CLEAN_C1", "CLEAN_ALL", "GOLDEN_C1", "MFLAG0_C1"]
CUBE_ORDER = ["C1", "ALL", "CLEAN_C1", "CLEAN_ALL", "PH2_C1"]


def analyse(cat, c302, alf, verbose=True, pos="hi"):
    p = P if verbose else (lambda *a: None)
    cz = C_KMS * cat.z_HI.values
    mra, mde = cat.RA_deg.values, cat.Dec_deg.values
    rac, dec_ = ("ra_hi_deg", "dec_hi_deg") if pos == "hi" else ("ra_oc_deg", "dec_oc_deg")
    lo_ra, hi_ra, lo_de, hi_de = mra.min() - 1, mra.max() + 1, mde.min() - 1, mde.max() + 1
    box = alf[np.isfinite(alf[rac]) & np.isfinite(alf[dec_]) & np.isfinite(alf.vhel_kms)
              & alf[rac].between(lo_ra, hi_ra) & alf[dec_].between(lo_de, hi_de)].reset_index(drop=True)
    im, ja, sep, dcz = candidates(mra, mde, cz, box[rac].values, box[dec_].values, box.vhel_kms.values)
    pairs, lost, n_cand = greedy(im, ja, sep, dcz)
    p(f"\nMATCHING ({'ALFALFA HI centroid' if pos == 'hi' else 'ALFALFA optical counterpart (M6 variant)'}; theta <= {R_MATCH:.0f} arcsec, |dcz| <= {DV_MATCH:.0f} km/s, one-to-one)")
    p(f"  ALFALFA rows in the 1-degree-margin box around the catalogue: {len(box)}; candidate pairs {len(im)}; MIGHTEE sources with >= 1 candidate {n_cand}; "
      f"pairs after M4 {len(pairs)}; LOST {len(lost)} {[cat.ID_catalogue.iloc[i] for i in lost]}")

    # confusion among the full catalogue
    S_mm = angsep_arcsec(mra[:, None], mde[:, None], mra[None, :], mde[None, :])
    D_mm = np.abs(cz[:, None] - cz[None, :])
    w50 = cat.W_50_km_s.values
    golden = ((cat.low_confidence_flag == 0) & (cat.blended_flag == 0) & (cat.confused_flag == 0)
              & (cat.bad_ellipse_flag == 0) & (cat.contaminated_source_flag == 0)).values
    c3 = c302.set_index("ID")
    c3_primary, c3_det, c3_wdef = tobool(c302.primary), tobool(c302.detected), tobool(c302.W50_defined)
    c3f = pd.DataFrame(dict(primary=c3_primary, detected=c3_det, W50_defined=c3_wdef), index=c302.ID.values)

    rows = []
    for i, j, s, d in pairs:
        a = box.iloc[j]; r = cat.iloc[i]; nu = r.freq_MHz * 1e6
        nb = [k for k in range(len(cat)) if k != i and S_mm[i, k] <= R_CONF and D_mm[i, k] <= w50[i] + DV_CONF_ADD]
        # beam-summed: all MIGHTEE within 210" of the ALFALFA centroid and in the ALFALFA window, target always in
        sa = angsep_arcsec(a[rac], a[dec_], mra, mde)
        win = (sa <= R_CONF) & (np.abs(cz - a.vhel_kms) <= (a.w50_kms / 2 + 100 if np.isfinite(a.w50_kms) else 100))
        win[i] = True
        S_sum = float(np.sum(conv(cat.S_HI_Jy_Hz.values[win], cat.freq_MHz.values[win] * 1e6, "OPT")))
        rec = dict(ID=r.ID_catalogue, RA_deg=r.RA_deg, Dec_deg=r.Dec_deg, z_HI=r.z_HI, cz_kms=cz[i], freq_MHz=r.freq_MHz,
                   agc=int(a.agc), ra_A=a[rac], dec_A=a[dec_], sep_arcsec=s, vhel_kms=a.vhel_kms, dcz_kms=d, hi_code=a.hi_code,
                   snr_A=a.snr, s21_jykms=a.s21_jykms, e_s21_jykms=a.e_s21_jykms, w50_A=a.w50_kms, e_w50_A=a.e_w50_kms,
                   S_HI_Jy_Hz=r.S_HI_Jy_Hz, S_HI_err_Jy_Hz=r.S_HI_Jy_Hz_err, W50_cat=r.W_50_km_s, W50_cat_err=r.W_50_km_s_err,
                   SNR_3D=r.SNR_3D, log_M_HI=r.log_M_HI, CONF=int(len(nb) > 0), n_conf=len(nb), conf_IDs=";".join(cat.ID_catalogue.iloc[nb]),
                   blended_flag=int(r.blended_flag), confused_flag=int(r.confused_flag), golden=int(golden[i]),
                   n_sum=int(win.sum()), S_sum_opt=S_sum)
        for m in ("OPT", "REST", "RADIO"):
            rec[f"S_cat_{m}"] = conv(r.S_HI_Jy_Hz, nu, m)
        rec["S_cat_err_OPT"] = conv(r.S_HI_Jy_Hz_err, nu, "OPT")
        in3 = r.ID_catalogue in c3.index
        rec["in_cfg302"] = int(in3)
        if in3:
            q = c3.loc[r.ID_catalogue]; f = c3f.loc[r.ID_catalogue]
            rec.update(cfg302_primary=int(f.primary), cfg302_detected=int(f.detected), snr_L=q.snr_L, S_win_Jy_Hz=q.S_win_Jy_Hz,
                       S_win_err_Jy_Hz=q.S_win_err_Jy_Hz, W50_cube_obs=q.W50_obsframe_kms, W50_cube_defined=int(f.W50_defined))
            for m in ("OPT", "REST", "RADIO"):
                rec[f"S_win_{m}"] = conv(q.S_win_Jy_Hz, nu, m)
            rec["S_win_err_OPT"] = conv(q.S_win_err_Jy_Hz, nu, "OPT")
        else:
            rec.update(cfg302_primary=0, cfg302_detected=0, snr_L=np.nan, S_win_Jy_Hz=np.nan, S_win_err_Jy_Hz=np.nan, W50_cube_obs=np.nan,
                       W50_cube_defined=0, S_win_OPT=np.nan, S_win_REST=np.nan, S_win_RADIO=np.nan, S_win_err_OPT=np.nan)
        rows.append(rec)
    df = pd.DataFrame(rows)
    fv = (df.s21_jykms > 0) & (df.s21_jykms < 900) & (df.S_HI_Jy_Hz > 0)
    for m in ("OPT", "REST", "RADIO"):
        df[f"R_cat_{m}"] = np.where(fv, np.log10(df[f"S_cat_{m}"] / df.s21_jykms), np.nan)
        okc = fv & (df[f"S_win_{m}"] > 0)
        df[f"R_cube_{m}"] = np.where(okc, np.log10(df[f"S_win_{m}"].where(okc, 1.0) / df.s21_jykms), np.nan)
    df["R_sum_OPT"] = np.where(fv, np.log10(df.S_sum_opt / df.s21_jykms), np.nan)
    df["logW50_cat_A"] = np.log10(df.W50_cat / df.w50_A)
    df["logW50_cube_A"] = np.where(df.W50_cube_defined == 1, np.log10(df.W50_cube_obs / df.w50_A), np.nan)
    df["pull_cat"] = (df.S_cat_OPT - df.s21_jykms) / np.sqrt(df.S_cat_err_OPT ** 2 + df.e_s21_jykms ** 2)
    df["pull_cube"] = (df.S_win_OPT - df.s21_jykms) / np.sqrt(df.S_win_err_OPT ** 2 + df.e_s21_jykms ** 2)
    df["flux_valid"] = fv.astype(int)
    cube_det = (df.cfg302_primary == 1) & (df.cfg302_detected == 1) & (df.S_win_Jy_Hz > 0)
    cube_ph2 = (df.cfg302_primary == 1) & (df.snr_L >= PH2_SNR) & (df.S_win_Jy_Hz > 0)
    df["cube_set"] = cube_det.astype(int)

    c1, c2 = df.hi_code == 1, df.hi_code == 2
    allc = c1 | c2
    clean = df.CONF == 0
    sets = dict(C1=c1, ALL=allc, C2=c2, CLEAN_C1=c1 & clean, CLEAN_ALL=allc & clean, GOLDEN_C1=c1 & (df.golden == 1),
                MFLAG0_C1=c1 & (df.blended_flag == 0) & (df.confused_flag == 0))
    csets = dict(C1=c1 & cube_det, ALL=allc & cube_det, CLEAN_C1=c1 & clean & cube_det, CLEAN_ALL=allc & clean & cube_det, PH2_C1=c1 & cube_ph2)
    seeds = np.random.SeedSequence(SEED_BOOT).spawn(len(SET_ORDER) * 3 + len(CUBE_ORDER) * 6 + 8)
    si = iter(seeds)
    res = dict(n_box=len(box), n_candidate_pairs=int(len(im)), n_with_candidate=int(n_cand), n_pairs=len(pairs),
               lost=[cat.ID_catalogue.iloc[i] for i in lost], cat={}, cube={}, paired={}, w50={}, w50_cube={}, sum={})
    p("\nCATALOGUE / ALFALFA  R_cat = log10(S_cat / S21)  [median; bootstrap 68 % / 95 % of the median; robust scatter; pull outliers > 3]")
    for k in SET_ORDER:
        m = sets[k]
        res["cat"][k] = {}
        for cv in ("OPT", "REST", "RADIO"):
            x = df.loc[m, f"R_cat_{cv}"].values
            st = robust(x); st.update(boot(x, next(si)))
            if cv == "OPT":
                st["pull_outliers"] = int(np.sum(np.abs(df.loc[m, "pull_cat"].values) > 3))
            res["cat"][k][cv] = st
        s = res["cat"][k]["OPT"]
        p(f"  {k:10s} N {s['n']:3d}  OPT {s['median']:+.3f} (68 % {s['p16']:+.3f}..{s['p84']:+.3f}; 95 % {s['p2_5']:+.3f}..{s['p97_5']:+.3f}) "
          f"scat {s['robust_scatter']:.3f} pulls>3 {s.get('pull_outliers', 0)} | REST {res['cat'][k]['REST']['median']:+.3f} | RADIO {res['cat'][k]['RADIO']['median']:+.3f}")
    p("\nCUBE / ALFALFA  R_cube = log10(S_win / S21) on CFG302 frozen detections (S/N_L >= 5, primary, S_win > 0) that match")
    for k in CUBE_ORDER:
        m = csets[k]
        res["cube"][k] = {}
        for cv in ("OPT", "REST", "RADIO"):
            x = df.loc[m, f"R_cube_{cv}"].values
            st = robust(x); st.update(boot(x, next(si)))
            if cv == "OPT":
                st["pull_outliers"] = int(np.sum(np.abs(df.loc[m, "pull_cube"].values) > 3))
            res["cube"][k][cv] = st
        # paired on the same galaxies
        xc = df.loc[m, "R_cat_OPT"].values; xk = df.loc[m, "R_cube_OPT"].values
        pc = robust(xc); pc.update(boot(xc, next(si)))
        pdlt = robust(xk - xc); pdlt.update(boot(xk - xc, next(si)))
        res["paired"][k] = dict(R_cat_same=pc, diff=pdlt)
        s = res["cube"][k]["OPT"]
        p(f"  {k:10s} N {s['n']:3d}  OPT {s['median']:+.3f} (68 % {s['p16']:+.3f}..{s['p84']:+.3f}; 95 % {s['p2_5']:+.3f}..{s['p97_5']:+.3f}) "
          f"scat {s['robust_scatter']:.3f} pulls>3 {s.get('pull_outliers', 0)} | REST {res['cube'][k]['REST']['median']:+.3f} | "
          f"same galaxies R_cat {pc['median']:+.3f}; paired R_cube - R_cat {pdlt['median']:+.3f} (68 % {pdlt['p16']:+.3f}..{pdlt['p84']:+.3f})")
    # all CFG302-primary matched (incl. non-detections): linear median ratio
    mall = c1 & (df.cfg302_primary == 1) & fv
    lin = (df.loc[mall, "S_win_OPT"] / df.loc[mall, "s21_jykms"]).values
    res["cube_all_primary_C1_linear"] = dict(n=int(mall.sum()), median_ratio=float(np.median(lin)) if lin.size else np.nan)
    p(f"  all CFG302-primary C1 matches (non-detections included), median linear S_win/S21: {res['cube_all_primary_C1_linear']['median_ratio']:.3f} (N {mall.sum()})")

    p("\nWIDTHS  log10(W50_cat / W50_ALFALFA) [catalogue as published]; log10(W50_cube,obs / W50_ALFALFA) [cube sets, width-defined]")
    for k in SET_ORDER:
        x = df.loc[sets[k], "logW50_cat_A"].values
        st = robust(x); st.update(boot(x, next(si))) if k in ("C1", "ALL", "CLEAN_C1") else None
        res["w50"][k] = st
    for k in CUBE_ORDER:
        x = df.loc[csets[k], "logW50_cube_A"].values
        st = robust(x)
        res["w50_cube"][k] = st
    for k in ("C1", "ALL", "CLEAN_C1"):
        s = res["w50"][k]; sc = res["w50_cube"][k]
        p(f"  {k:10s} catalogue N {s['n']:3d} median {s['median']:+.4f} (68 % {s.get('p16', np.nan):+.4f}..{s.get('p84', np.nan):+.4f}) scat {s['robust_scatter']:.3f} | "
          f"cube N {sc['n']:3d} median {sc['median']:+.4f} scat {sc['robust_scatter']:.3f}")
    p("\nBEAM-SUMMED VARIANT  R_sum = log10(sum of MIGHTEE S_HI within 210\" of the ALFALFA centroid and its window / S21)")
    for k in ("C1", "ALL"):
        x = df.loc[sets[k], "R_sum_OPT"].values
        st = robust(x); res["sum"][k] = st
        p(f"  {k:10s} N {st['n']:3d} median {st['median']:+.3f} scat {st['robust_scatter']:.3f}; pairs with > 1 source summed: {int((df.loc[sets[k], 'n_sum'] > 1).sum())}")
    m = c1 & fv
    if m.sum() >= 4:
        rs = spearmanr(df.loc[m, "snr_A"], df.loc[m, "R_cat_OPT"]); rz = spearmanr(df.loc[m, "z_HI"], df.loc[m, "R_cat_OPT"])
        res["spearman_C1"] = dict(R_cat_vs_snrA=[float(rs[0]), float(rs[1])], R_cat_vs_z=[float(rz[0]), float(rz[1])])
        p(f"  Spearman on C1: R_cat vs ALFALFA S/N rho {rs[0]:+.2f} (p {rs[1]:.2g}); R_cat vs z rho {rz[0]:+.2f} (p {rz[1]:.2g})")
    res["match_quality_C1"] = dict(median_abs_dcz=float(np.median(np.abs(df.loc[c1, "dcz_kms"]))) if c1.sum() else np.nan,
                                   median_sep=float(np.median(df.loc[c1, "sep_arcsec"])) if c1.sum() else np.nan)
    p(f"  match quality C1: median |dcz| {res['match_quality_C1']['median_abs_dcz']:.1f} km/s, median separation {res['match_quality_C1']['median_sep']:.1f} arcsec; "
      f"CONF flagged {int(df.loc[c1, 'CONF'].sum())} of {int(c1.sum())} (ALL {int(df.loc[allc, 'CONF'].sum())} of {int(allc.sum())})")

    # decisions
    D = {}
    def dd(kc, kk, cv, nmc=NMIN_CAT, nmk=NMIN_CUBE):
        a, b = res["cat"][kc][cv], res["cube"][kk][cv]
        dec = decide(a["median"], b["median"], a["n"], b["n"], nmc, nmk)
        return dict(decision=dec, strength=strength(dec, a, b), R_cat=a["median"], R_cube=b["median"], N_cat=a["n"], N_cube=b["n"])
    D["C1_OPT"] = dd("C1", "C1", "OPT")
    D["CLEAN_C1_OPT"] = dd("CLEAN_C1", "CLEAN_C1", "OPT", NMIN_CAT_CLEAN, NMIN_CUBE_CLEAN)
    if D["CLEAN_C1_OPT"]["decision"].startswith("undecided (insufficient"):
        D["CLEAN_C1_OPT"]["decision"] = "insufficient (no vote)"
    D["C1_REST"] = dd("C1", "C1", "REST")
    D["ALL_OPT"] = dd("ALL", "ALL", "OPT")
    D["C1_RADIO"] = dd("C1", "C1", "RADIO")
    D["CLEAN_ALL_OPT"] = dd("CLEAN_ALL", "CLEAN_ALL", "OPT", NMIN_CAT_CLEAN, NMIN_CUBE_CLEAN)
    voters = [D["C1_REST"]["decision"]] + ([] if D["CLEAN_C1_OPT"]["decision"].startswith("insufficient") else [D["CLEAN_C1_OPT"]["decision"]])
    prim = D["C1_OPT"]["decision"]
    head = prim if (prim.startswith("undecided (insufficient") or all(v == prim for v in voters)) else "undecided (depends on confusion / convention)"
    D["HEADLINE"] = head
    res["decisions"] = D
    res["df"] = df
    res["sets_n"] = {k: int(v.sum()) for k, v in sets.items()}
    res["csets_n"] = {k: int(v.sum()) for k, v in csets.items()}
    p("\nDECISIONS (frozen rule: catalogue confirmed iff |R_cat| <= 0.10 & R_cube <= -0.15; cube confirmed iff |R_cube| <= 0.10 & R_cat >= +0.15; neither iff both |R| > 0.10)")
    for k in ("C1_OPT", "CLEAN_C1_OPT", "C1_REST", "ALL_OPT", "CLEAN_ALL_OPT", "C1_RADIO"):
        v = D[k]
        p(f"  {k:14s} {v['decision']:32s} [{v['strength']}]  R_cat {v['R_cat']:+.3f} (N {v['N_cat']}), R_cube {v['R_cube']:+.3f} (N {v['N_cube']})"
          + ("   <- PRIMARY" if k == "C1_OPT" else ("   (votes)" if k in ("CLEAN_C1_OPT", "C1_REST") else "   (reported)")))
    p(f"  HEADLINE: {head}")
    return res


def shuffle_control(cat, alf):
    cz = C_KMS * cat.z_HI.values
    mra, mde = cat.RA_deg.values, cat.Dec_deg.values
    box = alf[np.isfinite(alf.ra_hi_deg) & np.isfinite(alf.dec_hi_deg) & np.isfinite(alf.vhel_kms)
              & alf.ra_hi_deg.between(mra.min() - 1, mra.max() + 1) & alf.dec_hi_deg.between(mde.min() - 1, mde.max() + 1)]
    ara, ade, acz = box.ra_hi_deg.values, box.dec_hi_deg.values, box.vhel_kms.values
    rng = np.random.default_rng(SEED_SHUF)
    counts, cands = [], []
    for _ in range(K_SHUF):
        pa = rng.uniform(0, 2 * np.pi, len(cat))
        sra, sde = offset(mra, mde, pa, SHUF_ARCMIN)
        im, ja, sep, dcz = candidates(sra, sde, cz, ara, ade, acz)
        pairs, lost, nc = greedy(im, ja, sep, dcz)
        counts.append(len(pairs)); cands.append(nc)
    counts = np.array(counts)
    return dict(K=K_SHUF, mean=float(counts.mean()), max=int(counts.max()), n_zero=int((counts == 0).sum()),
                hist={int(v): int((counts == v).sum()) for v in np.unique(counts)})


def cfg301_consequence(Rc, b68):
    j = json.load(open(J301))["numbers"]["results"]["pooled"]
    s0, a00 = j["s"], j["a0"]; a0c = a00 / s0; bands = j["bands"]
    nodes = np.array([-0.30, -0.15, 0.0, 0.15, 0.30])
    logs = np.log10([bands["-0.30"], bands["-0.15"], s0, bands["+0.15"], bands["+0.30"]])
    txt = open(O301).read()
    mm = re.search(r"pooled:.*?gas fraction median ([0-9.]+)", txt)
    fg = float(mm.group(1))

    def amap(t):
        if not np.isfinite(t) or abs(t) > 0.30 + 1e-12:
            return None
        s = 10 ** float(np.interp(t, nodes, logs)); return dict(tau=float(t), s=s, a0=s * a0c)

    def teff(t):
        return float(np.log10(fg * 10 ** t + 1 - fg))
    tau = -Rc; tlo, thi = -b68["p84"], -b68["p16"]
    out = dict(a0_canonical=a0c, s_pooled=s0, a0_pooled=a00, nodes=nodes.tolist(), log_s_nodes=logs.tolist(), f_gas=fg, tau=tau,
               A=dict(central=amap(tau), lo=amap(tlo), hi=amap(thi)),
               B=dict(tau_eff=teff(tau), central=amap(teff(tau)), lo=amap(teff(tlo)), hi=amap(teff(thi))),
               chart_note=dict(A_at_minus030=amap(-0.30), B_tau_eff_at_minus030=teff(-0.30), B_at_minus030=amap(teff(-0.30))))
    return out


def fmt_a(x):
    return "outside the band rows (not extrapolated)" if x is None else f"{x['a0']:.3e} (s* {x['s']:.3f}, tau {x['tau']:+.3f})"


# ================================================================== main
def main():
    P(f"CFG304 -- MIGHTEE-HI COSMOS flux scale vs ALFALFA alpha.100 (frozen criteria {FROZEN}); mode: {'MAIN' if not MUT else 'MUTATE=' + MUT}")
    P("A flux-calibration check, not an a0 measurement; kappa = 1/2 is FITTED; no knob scans; no downloads.")
    shas = dict(mightee=sha256(CAT), cfg302=sha256(C302), alfalfa=sha256(ALF), cfg301_json=sha256(J301))
    for k, v in shas.items():
        P(f"  sha256 {k}: {v}")
    P(f"  inputs: {rel(CAT)}; {rel(C302)}; {rel(ALF)}; {rel(J301)}; {rel(O301)}")
    cat, c302, alf = load()
    P(f"  rows: MIGHTEE {len(cat)}; CFG302 {len(c302)}; ALFALFA {len(alf)}")
    NUM = dict(mode=MUT or "main", frozen_commit=FROZEN, sha256=shas)
    NUM["bookkeeping"] = bookkeeping_checks(cat, c302, alf, shas)

    if MUT:
        P("\n==== UNMUTATED reference (in memory; printed in full in the main run) ====")
        ref = analyse(cat, c302, alf, verbose=False)
        P(f"  unmutated C1-OPT: {ref['decisions']['C1_OPT']['decision']} (R_cat {ref['decisions']['C1_OPT']['R_cat']:+.4f}, R_cube {ref['decisions']['C1_OPT']['R_cube']:+.4f}); HEADLINE {ref['decisions']['HEADLINE']}")
        cat_m, alf_m = mutate(cat, alf, MUT)
        P(f"\n==== MUTATED DATA: {dict(a='catalogue S_HI x 0.5', b='ALFALFA S21 x 0.5', c='ALFALFA S21 x 2')[MUT]} ====")
    else:
        ref, cat_m, alf_m = None, cat, alf
    res = analyse(cat_m, c302, alf_m, verbose=True)
    oc = analyse(cat_m, c302, alf_m, verbose=False, pos="oc")
    P(f"\nM6 VARIANT (ALFALFA optical-counterpart positions): pairs {oc['n_pairs']} (C1 {oc['sets_n']['C1']}); C1-OPT R_cat {oc['cat']['C1']['OPT']['median']:+.3f} "
      f"(N {oc['cat']['C1']['OPT']['n']}), R_cube {oc['cube']['C1']['OPT']['median']:+.3f} (N {oc['cube']['C1']['OPT']['n']}): {oc['decisions']['C1_OPT']['decision']}")
    shuf = shuffle_control(cat_m, alf_m)
    P(f"\nSHUFFLED-POSITION CONTROL: {shuf['K']} shuffles, every source moved 10 arcmin at a random position angle: mean pairs {shuf['mean']:.3f}, max {shuf['max']}, "
      f"zero in {shuf['n_zero']} of {shuf['K']}; histogram {shuf['hist']}")

    D = res["decisions"]; c1 = res["cat"]["C1"]["OPT"]
    cons = cfg301_consequence(c1["median"], c1)
    P("\nCONSEQUENCE FOR CFG301 (reported; CFG301 not re-run): pooled baryon-band rows interpolated in log s* at tau = -median R_cat (C1, OPT)")
    P(f"  pooled s* {cons['s_pooled']:.4f} (a0 {cons['a0_pooled']:.4e}); nodes tau {cons['nodes']} -> s* {[round(10 ** v, 4) for v in cons['log_s_nodes']]}; f_gas {cons['f_gas']:.2f}")
    P(f"  (A) total-baryon reading: a0 {fmt_a(cons['A']['central'])}; 68 % of R_cat -> {fmt_a(cons['A']['lo'])} .. {fmt_a(cons['A']['hi'])}")
    P(f"  (B) gas-only reading (tau_eff {cons['B']['tau_eff']:+.4f}): a0 {fmt_a(cons['B']['central'])}; 68 % -> {fmt_a(cons['B']['lo'])} .. {fmt_a(cons['B']['hi'])}")
    P(f"  chart note: the cube-scale hollow diamond at tau = -0.30: (A) {fmt_a(cons['chart_note']['A_at_minus030'])}; (B, tau_eff {cons['chart_note']['B_tau_eff_at_minus030']:+.4f}) {fmt_a(cons['chart_note']['B_at_minus030'])}")

    P("\nCHECKS")
    mq = res["match_quality_C1"]
    check("K5 match quality on C1: median |dcz| <= 50 km/s and median theta <= 40 arcsec", f"{mq['median_abs_dcz']:.1f} km/s, {mq['median_sep']:.1f} arcsec",
          mq["median_abs_dcz"] <= 50 and mq["median_sep"] <= 40)
    check("K6 MIGHTEE sources with >= 1 candidate within 2 of the orchestrator's 23", f"{res['n_with_candidate']}", abs(res["n_with_candidate"] - ORCH_COUNT) <= 2)
    w = res["w50"]["C1"]
    check("C-W50 (control i) |median log(W50_cat / W50_ALFALFA)| <= 0.05 dex on C1", f"{w['median']:+.4f} dex (N {w['n']}, scatter {w['robust_scatter']:.3f})", abs(w["median"]) <= 0.05)
    wc = res["w50_cube"]["C1"]
    check("C-W50cube (sanity) |median log(W50_cube,obs / W50_ALFALFA)| <= 0.07 dex on the C1 cube set", f"{wc['median']:+.4f} dex (N {wc['n']})",
          np.isfinite(wc["median"]) and abs(wc["median"]) <= 0.07)
    check("C-SHUF (control ii) shuffled mean pairs <= 1.0 and max <= 3", f"mean {shuf['mean']:.3f}, max {shuf['max']}", shuf["mean"] <= 1.0 and shuf["max"] <= 3)
    check("D-MIN primary set size: N_cat >= 8 and N_cube >= 5", f"N_cat {c1['n']}, N_cube {res['cube']['C1']['OPT']['n']}",
          c1["n"] >= NMIN_CAT and res["cube"]["C1"]["OPT"]["n"] >= NMIN_CUBE)

    mut = {}
    if MUT:
        rD = ref["decisions"]["C1_OPT"]["decision"]; nD = D["C1_OPT"]["decision"]
        if MUT == "a":
            sh = [res["cat"][k][cv]["median"] - ref["cat"][k][cv]["median"] for k in SET_ORDER for cv in ("OPT", "REST", "RADIO")
                  if np.isfinite(ref["cat"][k][cv]["median"])]
            un = [res["cube"][k][cv]["median"] - ref["cube"][k][cv]["median"] for k in CUBE_ORDER for cv in ("OPT", "REST", "RADIO")
                  if np.isfinite(ref["cube"][k][cv]["median"])]
            dev = max(abs(s - math.log10(0.5)) for s in sh); dun = max(abs(u) for u in un)
            check("MUTATE-a every set's median R_cat moves by log10(0.5) = -0.30103 (to 1e-9)", f"max deviation {dev:.2e} over {len(sh)} set/convention medians", dev <= 1e-9)
            check("MUTATE-a every median R_cube unchanged (to 1e-12)", f"max change {dun:.2e} over {len(un)}", dun <= 1e-12)
            check("MUTATE-a the C1-OPT decision differs from the unmutated one", f"unmutated '{rD}' -> mutated '{nD}' (frozen prediction from a catalogue-confirmed state: 'neither')", nD != rD)
            mut = dict(max_shift_dev=dev, max_cube_change=dun, unmutated=rD, mutated=nD)
        elif MUT == "b":
            if rD == "catalogue scale confirmed":
                check("MUTATE-b (flip test) arbiter x 0.5 turns 'catalogue scale confirmed' into 'cube scale confirmed'", f"unmutated '{rD}' -> mutated '{nD}'", nD == "cube scale confirmed")
            else:
                P(f"  [N/A] MUTATE-b flip test not defined from '{rD}' (reported: mutated '{nD}')")
            mut = dict(unmutated=rD, mutated=nD)
        elif MUT == "c":
            if rD == "cube scale confirmed":
                check("MUTATE-c (flip test) arbiter x 2 turns 'cube scale confirmed' into 'catalogue scale confirmed'", f"unmutated '{rD}' -> mutated '{nD}'", nD == "catalogue scale confirmed")
            else:
                P(f"  [N/A] MUTATE-c flip test not defined from '{rD}' (reported: mutated '{nD}')")
            mut = dict(unmutated=rD, mutated=nD)

    # hand estimates (information, scored as they fall)
    P("\nHAND ESTIMATES (frozen section 9; information, not checks)")
    he = {}
    if not MUT:
        n = res["sets_n"]; nc = res["csets_n"]
        he["HE1"] = (21 <= res["sets_n"]["ALL"] <= 24 and 15 <= n["C1"] <= 21 and 8 <= n["CLEAN_C1"] <= 17 and 6 <= nc["C1"] <= 15,
                     f"N ALL {n['ALL']}, C1 {n['C1']}, CLEAN-C1 {n['CLEAN_C1']}, C1 cube {nc['C1']}")
        he["HE2"] = (-0.12 <= c1["median"] <= 0.05, f"R_cat {c1['median']:+.3f} in [-0.12, +0.05]")
        rk = res["cube"]["C1"]["OPT"]["median"]
        he["HE3"] = (-0.45 <= rk <= -0.20, f"R_cube {rk:+.3f} in [-0.45, -0.20]")
        he["HE4"] = (D["C1_OPT"]["decision"] == "catalogue scale confirmed", f"decision '{D['C1_OPT']['decision']}' (headline '{D['HEADLINE']}')")
        he["HE5"] = (-0.05 <= w["median"] <= 0.03 and np.isfinite(wc["median"]) and -0.08 <= wc["median"] <= 0.02, f"W50 cat {w['median']:+.3f}, cube {wc['median']:+.3f}")
        he["HE6"] = (shuf["mean"] <= 0.5, f"shuffled mean {shuf['mean']:.3f}")
        aA, aB = cons["A"]["central"], cons["B"]["central"]
        he["HE8"] = (aA is not None and aB is not None and 0.95e-10 <= aA["a0"] <= 1.20e-10 and 0.98e-10 <= aB["a0"] <= 1.15e-10,
                     f"(A) {fmt_a(aA)}; (B) {fmt_a(aB)}")
        cb = cons["chart_note"]["B_at_minus030"]
        he["HE9"] = (cb is not None and 1.6e-10 <= cb["a0"] <= 1.8e-10, f"(B) at tau -0.30: {fmt_a(cb)}")
        he["HE10"] = (NUM["bookkeeping"]["U1_median_abs"] <= 0.01, f"U1 median |delta| {NUM['bookkeeping']['U1_median_abs']:.4f}")
        P("  HE7 (MUTATE outcomes) is scored in the MUTATE outputs")
    elif MUT == "a":
        he["HE7a"] = (D["C1_OPT"]["decision"] == "neither", f"MUTATE-a decision '{D['C1_OPT']['decision']}' (predicted 'neither')")
    elif MUT == "b":
        he["HE7b"] = (D["C1_OPT"]["decision"] == "cube scale confirmed", f"MUTATE-b decision '{D['C1_OPT']['decision']}' (predicted 'cube scale confirmed')")
    for k, (ok, txt) in he.items():
        P(f"  {k}: {'hit' if ok else 'MISS'} -- {txt}")

    npass = sum(c["ok"] for c in CHECKS)
    P(f"\n{npass}/{len(CHECKS)} checks pass")
    P(f"runtime {time.time() - T0:.1f} s")

    # outputs
    df = res.pop("df"); oc.pop("df")
    df.to_csv(POUT, index=False, float_format="%.10g")
    NUM.update(results=res, m6_oc=dict(n_pairs=oc["n_pairs"], sets_n=oc["sets_n"], cat_C1=oc["cat"]["C1"], cube_C1=oc["cube"]["C1"], decisions=oc["decisions"]),
               shuffle=shuf, cfg301=cons, mutate=mut, hand_estimates={k: dict(hit=bool(v[0]), detail=v[1]) for k, v in he.items()})
    if ref is not None:
        ref.pop("df")
        NUM["unmutated_reference"] = dict(decisions=ref["decisions"], cat=ref["cat"], cube=ref["cube"])

    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.bool_):
            return bool(o)
        return o
    json.dump(dict(stage="CFG304", mode=MUT or "main", checks=CHECKS, numbers=clean(NUM)), open(JOUT, "w"), indent=1, sort_keys=False)
    with open(OUT, "w") as f:
        f.write("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
