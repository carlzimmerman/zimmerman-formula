#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG280 -- implied-a0 estimates (upper bounds or floors) from the PUBLISHED SINS/zC-SINF AO kinematics (Forster Schreiber+18 Tables 1 and 6): stars-only baryons (a lower limit) with PHIBSS CO gas on four rows; coverage only.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG280_sins_ao_published/FROZEN_CRITERIA.md (96d52c268).
  g_obs     V_c^2 / R_e with V_c = (V_rot^2 + 3.36 sigma0^2)^0.5 from the table (peak-to-peak, radius NOT recorded: r = R_e is a convention)
  g_bar     B0 = stars only (Table 1 M*, one exponential disc of scale R_e); B1 = stars + PHIBSS M_mol on four rows (class S); B2 = scaling gas (sensitivity)
  STAGE=A   the blind pre-flight: no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V_rot, sigma0, V_c x 2); STAGE=B SELFTEST=1 (fabricated V_c on the law at s = 2).
Run: STAGE=A python3 .../cfg280_sins_ao_published.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv, contextlib, re
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

TSTART = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

STAGE = os.environ.get("STAGE", "").strip().upper()
MUTATE = os.environ.get("MUTATE", "0") == "1"
SELFTEST = os.environ.get("SELFTEST", "0") == "1"
assert STAGE in ("A", "B"), "set STAGE=A or STAGE=B"
assert not ((MUTATE or SELFTEST) and STAGE == "A") and not (MUTATE and SELFTEST), "MUTATE / SELFTEST apply to stage B, one at a time"
SFX = f"_stage{STAGE}" + ("_MUTATE1" if MUTATE else "") + ("_SELFTEST" if SELFTEST else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: V_rot, sigma0 and V_c x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V_c on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
LOADVEL = (STAGE == "B") and not SELFTEST                                   # the SELFTEST never loads the real velocity-bearing columns
DA = os.path.join(REPO, "data_assembly")
SD = os.path.join(DA, "highz_literature_tables", "sins_ao")
T1P, T6P, T2P = (os.path.join(SD, f) for f in ("sins_ao_table1_sample.csv", "sins_ao_table6_kinematics.csv", "sins_ao_table2_observations.csv"))
PHP = os.path.join(DA, "kmos3d_phibss", "phibss13_joined.csv")
RCP = os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")
C196P = os.path.join(CFG, "CFG196_sins_ao_phibss_z22", "CFG196_preflight_results.json")
KMOS_SINS = ["K20-ID6", "K20-ID7", "GMASS-2303", "GMASS-2363", "ZC410041"]                # the five names shared with the KMOS3D lane (CFG270)
norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower())

t1 = pd.read_csv(T1P, usecols=["source", "z_Halpha", "Mstar_1e10Msun"]).set_index("source")
t6c = ["source", "Re_kpc", "Re_kpc_errlo", "Re_kpc_errhi", "sin_i", "disk_criteria"] + (["half_dv_obs_kms", "Vrot_kms", "Vrot_kms_errlo", "Vrot_kms_errhi", "sigma0_kms", "sigma0_kms_errlo", "sigma0_kms_errhi", "Vc_kms", "Vc_kms_errlo", "Vc_kms_errhi", "Mdyn_1e10Msun"] if LOADVEL else [])
t6 = pd.read_csv(T6P, usecols=t6c).set_index("source")
t2 = pd.read_csv(T2P, usecols=["source", "res_arcsec"]).set_index("source")
ph = pd.read_csv(PHP, usecols=["name", "comp", "type", "rh_opt_kpc", "rh_co_kpc", "mmol_msun", "mstar_msun", "co_upper_limit", "z_co", "fco_jykms", "fco_err"])
rc = pd.read_csv(RCP, usecols=["name", "z"])
c196 = json.load(open(C196P))["numbers"]["name_match"]["roles"]
P(f"tables: sins Table 1 {H.sha(T1P)}, Table 6 {H.sha(T6P)}, Table 2 {H.sha(T2P)}, PHIBSS {H.sha(PHP)}, RC100 names {H.sha(RCP)}; velocity-bearing columns loaded: {LOADVEL}")

SRC = list(t6.index)
N = len(SRC)
Z = np.array([float(t1.loc[s, "z_Halpha"]) for s in SRC])
MS = np.array([float(t1.loc[s, "Mstar_1e10Msun"]) * 1e10 for s in SRC]); LMS = np.log10(MS)
RE = np.array([float(t6.loc[s, "Re_kpc"]) for s in SRC]); RE_LO = np.array([float(t6.loc[s, "Re_kpc_errlo"]) for s in SRC]); RE_HI = np.array([float(t6.loc[s, "Re_kpc_errhi"]) for s in SRC])
CRIT = [str(t6.loc[s, "disk_criteria"]).strip() for s in SRC]
T1 = np.array([c == "1,2,3,4,5" for c in CRIT])
T2 = np.array([all(k in c.split(",") for k in ("1", "2", "3")) for c in CRIT])
T0 = np.ones(N, bool)
IRR = np.array([c == "Irr" for c in CRIT])
# cross-matches (flags only)
rc_n = {norm(r["name"]): float(r["z"]) for _, r in rc.iterrows()}
RC_M = np.array([(norm(s) in rc_n) and abs(rc_n[norm(s)] - Z[i]) <= 0.02 for i, s in enumerate(SRC)])
KM_M = np.isin(SRC, KMOS_SINS)
ph["key"] = ph["name"].map(norm)
PH_ROW = {s: ph[ph["key"] == norm(s)] for s in SRC}
PH_M = np.array([len(PH_ROW[s]) > 0 for s in SRC])
GASROWS = []
for s in SRC:
    p_ = PH_ROW[s]
    if len(p_) == 1 and int(p_["co_upper_limit"].iloc[0]) == 0 and (pd.isna(p_["comp"].iloc[0]) or str(p_["comp"].iloc[0]).strip() == ""):
        GASROWS.append(s)
T2Z = float(np.median(Z[T2]))
POOLS = {"PT1": T1, "PT2": T2, "PT0": T0, "PT2z1": T2 & (Z < T2Z), "PT2z2": T2 & (Z >= T2Z), "PT2_new": T2 & ~RC_M & ~KM_M}
P(f"tiers: T1 {int(T1.sum())}, T2 {int(T2.sum())}, T0 {N}; pooled sizes " + ", ".join(f"{k} {int(v.sum())}" for k, v in POOLS.items()) + f"; RC100 name matches {int(RC_M.sum())} (T1 {int((RC_M & T1).sum())}, T2 {int((RC_M & T2).sum())}); KMOS3D five {int(KM_M.sum())}; PHIBSS name matches {int(PH_M.sum())}; R1 gas rows {GASROWS}")


def mu_mol(z, logM):
    return 10 ** (0.06 - 3.3 * (np.log10(1 + z) - 0.65) ** 2 - 0.41 * (logM - 10.7))


def gbar(Ms, re, r, *, star_re=None, sph=False, gas=0.0):
    f = H.gsph if sph else H.gdisc
    sre = re if star_re is None else star_re
    return f(Ms, sre, r) + (f(Ms * gas, sre, r) if np.any(np.asarray(gas) > 0) else 0.0)


GB0 = np.array([float(gbar(MS[i], RE[i], RE[i])) for i in range(N)])
MUV = mu_mol(Z, LMS)
GB2 = np.array([float(gbar(MS[i], RE[i], RE[i], gas=MUV[i])) for i in range(N)])
Y0, Y2 = GB0 / A0C, GB2 / A0C
NUY0 = NU(Y0)
# PHIBSS gas rows (class S): M_mol, its flux-error dex
GR = {}
for s in GASROWS:
    p_ = ph[ph["key"] == norm(s)].iloc[0]; i = SRC.index(s)
    fe = float(p_["fco_err"]) / float(p_["fco_jykms"])
    GR[s] = dict(i=i, Mmol=float(p_["mmol_msun"]), sig=fe / math.log(10.0), type=str(p_["type"]), rh_co=float(p_["rh_co_kpc"]) if np.isfinite(float(p_["rh_co_kpc"])) else float("nan"), mstar_phibss=float(p_["mstar_msun"]))
    GR[s]["gb1"] = float(H.gdisc(MS[i] + GR[s]["Mmol"], RE[i], RE[i])); GR[s]["gg"] = float(H.gdisc(GR[s]["Mmol"], RE[i], RE[i])); GR[s]["gs"] = float(H.gdisc(MS[i], RE[i], RE[i]))

# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed)")
    t1_ids, t6_ids = set(t1.index), set(t6.index)
    check("C1 CONTROL (counts): Tables 1 and 6 hold the same 38 sources (35 galaxies + the three component rows ZC400569N, ZC407376N, ZC407376S), unique; z range 1.446-2.521; log M* range 9.36-11.50; tiers T1 11, T2 18, T0 38; six PHIBSS name matches and four R1 gas rows; RC100 name matches 12 (T1 5); the KMOS3D five all present",
          f"Table 1 {len(t1_ids)}, Table 6 {len(t6_ids)}, equal {t1_ids == t6_ids}, unique {len(set(SRC)) == N}; z [{Z.min():.4f}, {Z.max():.4f}]; log M* [{LMS.min():.3f}, {LMS.max():.3f}]; T1 {int(T1.sum())}, T2 {int(T2.sum())}; PHIBSS matches {int(PH_M.sum())} {[s for s in SRC if PH_M[SRC.index(s)]]}; gas rows {GASROWS}; RC100 {int(RC_M.sum())} (T1 {int((RC_M & T1).sum())}); KMOS3D five present {int(KM_M.sum())}",
          N == 38 and t1_ids == t6_ids and len(set(SRC)) == N and abs(Z.min() - 1.4457) < 1e-4 and abs(Z.max() - 2.5209) < 1e-4 and abs(LMS.min() - 9.362) < 2e-3 and abs(LMS.max() - 11.4997) < 2e-3 and int(T1.sum()) == 11 and int(T2.sum()) == 18
          and int(PH_M.sum()) == 6 and sorted(GASROWS) == sorted(["ZC406690", "Q2343-BX610", "Q1623-BX599", "Q2343-BX513"]) and int(RC_M.sum()) == 12 and int((RC_M & T1).sum()) == 5 and int(KM_M.sum()) == 5)
    yy = np.linspace(0.05, 40, 400000); hh = H.i0e(yy) * H.k0e(yy) - H.i1e(yy) * H.k1e(yy); peak = float(np.max(2 * yy ** 2 * hh)); farr = float(H.gdisc(1e11, 3.0, 150.0) / (H.G_KPC * 1e11 / 150.0 ** 2 * H.G2SI))
    src29 = open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score.py")).read(); seg = src29[src29.index("def disc_v2"):src29.index("P(__doc__")]
    ns29 = {"G_KPC": H.G_KPC, "XN": H.XN, "G2SI": H.G2SI, "i0e": H.i0e, "i1e": H.i1e, "k0e": H.k0e, "k1e": H.k1e, "math": math, "np": np}; exec(compile(seg, "cfg229_score.py", "exec"), ns29)
    rr_ = np.random.default_rng(1234); dmax = 0.0
    for _ in range(200):
        M_, Re_, Rr_ = 10 ** rr_.uniform(9, 12.5), rr_.uniform(0.5, 8), rr_.uniform(1, 20); dmax = max(dmax, abs(H.gdisc(M_, Re_, Rr_) / ns29["gdisc"](M_, Re_, Rr_) - 1))
    check("C2 CONTROL: Freeman's peak V^2 = 0.3872 G M / R_d to 0.003, g -> G M / r^2 far from a compact mass to 1e-3, and gdisc equals CFG229's on 200 random inputs to 1e-12", f"peak {peak:.4f}; far-field ratio {farr:.5f}; max deviation {dmax:.1e}", abs(peak / 0.3872 - 1) < 0.003 and abs(farr - 1) < 1e-3 and dmax < 1e-12)
    ok3, d3 = True, []
    for s in ("Q1623-BX599", "Q2343-BX389", "Q2343-BX513", "Q2343-BX610", "Q2346-BX482", "ZC406690"):
        p_ = ph[ph["key"] == norm(s)]; c = c196[s]
        mine = dict(comp="" if pd.isna(p_["comp"].iloc[0]) else str(p_["comp"].iloc[0]).strip(), type=str(p_["type"].iloc[0]), co_upper_limit=int(p_["co_upper_limit"].iloc[0]), R1=(s in GASROWS))
        same = mine["comp"] == c["comp"] and mine["type"] == c["type"] and mine["co_upper_limit"] == c["co_upper_limit"] and mine["R1"] == c["R1"]; ok3 = ok3 and same; d3.append(f"{s}: {mine} vs CFG196 {dict(comp=c['comp'], type=c['type'], co_upper_limit=c['co_upper_limit'], R1=c['R1'])} {'=' if same else 'DIFFERS'}")
    check("C3 CONTROL: the six PHIBSS rows' comp, type, co_upper_limit and the rule R1 equal CFG196's committed roles", "; ".join(d3), ok3)
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read(); seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}; exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr_ = np.random.default_rng(1234); same = True
    for _ in range(200):
        Dq = 10 ** rr_.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr_.uniform(-11, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = H.AI.implied(Dq, gq, NU, A0C); same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
    check("C4 CONTROL: the imported estimator equals CFG223's original bit for bit on 200 random sets", f"identical {same}", bool(same))
    d5 = 0.0
    for i in range(N):
        for st in (0.5, 1.0, 2.5):
            ls, unb = H.s_star(NU(np.array([GB0[i] / (A0C * st)])), np.array([GB0[i]])); d5 = max(d5, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C5 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every galaxy's stars-only baryon side", f"max |d log10 s| {d5:.1e}", d5 < 1e-6)
    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; B0 = stars only at r = R_e; ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    LEV, ILL = np.zeros(N), np.zeros(N, bool)
    for i in range(N):
        lv, fl = H.lever1(np.array([NUY0[i]]), np.array([GB0[i]])); LEV[i] = lv; ILL[i] = bool(fl or abs(lv) >= 10)
    for nm, m in (("T0", T0), ("T1", T1), ("T2", T2), ("PT2z1", POOLS["PT2z1"]), ("PT2z2", POOLS["PT2z2"]), ("PT2_new", POOLS["PT2_new"])):
        P(f"    {nm}: n {int(m.sum())}, y(B0) 16/50/84 % {np.percentile(Y0[m], 16):.2f} / {np.median(Y0[m]):.2f} / {np.percentile(Y0[m], 84):.2f} (min {Y0[m].min():.2f}, max {Y0[m].max():.2f}); y(B2) median {np.median(Y2[m]):.2f}; "
          f"rows y < 0.3: {int((Y0[m] < 0.3).sum())}, y > 6: {int((Y0[m] > 6).sum())}, y > 8: {int((Y0[m] > 8).sum())}; ILL-CONDITIONED {int(ILL[m].sum())} ({100 * ILL[m].mean():.0f} %); T4 floor 3 sigma/sqrt(N) at sigma = 0.2 dex {3 * 0.2 / math.sqrt(m.sum()):.3f} dex")
    P(f"    rows with 0.3 <= y(B0) <= 6: {int(((Y0 >= 0.3) & (Y0 <= 6)).sum())} of {N} ({100 * ((Y0 >= 0.3) & (Y0 <= 6)).mean():.0f} %)")
    P("    per row: source z log M* R_e(kpc) y(B0) lever tier criteria RC100 KMOS3D PHIBSS")
    for i in range(N):
        P(f"      {SRC[i]:13s} z {Z[i]:.3f} M* {LMS[i]:.2f} R_e {RE[i]:4.1f} y {Y0[i]:6.2f} lever {LEV[i]:+7.1f} {'ILL' if ILL[i] else '   '} {'T1' if T1[i] else ('T2' if T2[i] else '  ')} [{CRIT[i]:9s}]{' RC100' if RC_M[i] else ''}{' KMOS3D' if KM_M[i] else ''}{' PHIBSS' if PH_M[i] else ''}{' (R1 gas row)' if SRC[i] in GASROWS else ''}")
    P("\nA3  KNOB EFFECTS ON g_bar (dex relative to B0; median / min / max over all 38)")
    kb = {"R_e,* x1.5": np.array([gbar(MS[i], RE[i], RE[i], star_re=1.5 * RE[i]) for i in range(N)]), "R_e,* /1.5": np.array([gbar(MS[i], RE[i], RE[i], star_re=RE[i] / 1.5) for i in range(N)]), "spherical": np.array([gbar(MS[i], RE[i], RE[i], sph=True) for i in range(N)]),
          "radius 1.5 R_e": np.array([gbar(MS[i], RE[i], 1.5 * RE[i]) for i in range(N)]), "radius 2 R_e": np.array([gbar(MS[i], RE[i], 2.0 * RE[i]) for i in range(N)])}
    for k, v in kb.items():
        dd = np.log10(v / GB0); P(f"    {k}: median {np.median(dd):+.3f}, min {dd.min():+.3f}, max {dd.max():+.3f}")
    P("\nA4  mu_mol AND THE B2 / B0 RATIO (z ~ 2.2 is inside the range the relation was calibrated on)")
    P(f"    mu_mol (T2) median {np.median(MUV[T2]):.2f}; B2/B0 g_bar median {np.median((GB2 / GB0)[T2]):.2f}; all 38: {np.median(MUV):.2f}")
    P("\nA5  THE PHIBSS GAS ROWS (class S; Galactic alpha_CO 4.36 incl. He; same disc and R_e as the stars)")
    for s, g in GR.items():
        i = g["i"]; P(f"    {s:13s} [{g['type']}] M_mol {g['Mmol']:.2e} (flux error {g['sig']:.3f} dex), M* (Table 1) {MS[i]:.2e} vs PHIBSS {g['mstar_phibss']:.2e}, R_e {RE[i]:.1f}; y(B0) {Y0[i]:.2f} -> y(B1) {g['gb1'] / A0C:.2f}")
    P("    not gas rows: Q2346-BX482 (the CO is the companion BX482se's) and Q2343-BX389 (a 3-sigma upper limit)")
    P("\nA5b CROSS-MATCH SIZES (so no galaxy is counted twice): " + f"PT2 {int(T2.sum())}; PT2 rows with an RC100 name match {int((T2 & RC_M).sum())}; with a KMOS3D match {int((T2 & KM_M).sum())}; either {int((T2 & (RC_M | KM_M)).sum())}; PT2_new {int(POOLS['PT2_new'].sum())}; T1 rows with a match {int((T1 & (RC_M | KM_M)).sum())} of {int(T1.sum())}")
    P("\nA6  R_e AGAINST THE AO RESOLUTION (Table 2 res_arcsec FWHM; the component rows take their host's value)")
    host = {"ZC400569N": "ZC400569", "ZC407376N": "ZC407376", "ZC407376S": "ZC407376"}
    kpa = np.array([H.kpc_per_arcsec(z) for z in Z]); fw = np.array([float(t2.loc[host.get(s, s), "res_arcsec"]) * kpa[i] for i, s in enumerate(SRC)])
    small = RE < fw
    P(f"    R_e < AO PSF FWHM (kpc): T0 {int(small.sum())} of {N}; T2 {int((small & T2).sum())} of {int(T2.sum())}; median R_e/FWHM (T2) {np.median((RE / fw)[T2]):.2f}")
    P("\nC6  COVERAGE (noiseless world on each conditioned T2 row's B0 baryons; a declared 0.15 dex on g_obs; the declared 0.20 dex on M*; the published R_e errors; 100 mocks, B = 1,000)")
    rng6 = np.random.default_rng(280); idx2 = [i for i in np.where(T2)[0] if not ILL[i]]; cv68 = []; cv95 = []
    for i in idx2:
        gob_true = GB0[i] * float(NU(np.array([Y0[i]]))[0]); c68 = c95 = nd = 0
        for it in range(100):
            Ms_o = MS[i] * 10 ** rng6.normal(0, 0.20); god = gob_true * 10 ** rng6.normal(0, 0.15); gobm = god * 10 ** rng6.normal(0, 0.15, 1000)
            Msd = Ms_o * 10 ** rng6.normal(0, 0.20, 1000); Red = H.split_normal(rng6, RE[i], RE_HI[i], RE_LO[i], 1000).clip(0.3); gbd = H.gdisc(Msd, Red, Red)
            lsd, ud = H.AI.implied((gobm / gbd)[:, None], gbd[:, None], NU, A0C); q, fr = H.rooted_pct(lsd, ud)
            if np.isfinite(q[0]): nd += 1; c68 += (q[1] <= 0.0 <= q[3]); c95 += (q[0] <= 0.0 <= q[4])
        cv68.append(c68 / max(nd, 1)); cv95.append(c95 / max(nd, 1))
    cv68, cv95 = np.array(cv68), np.array(cv95)
    P(f"    conditioned T2 rows {len(idx2)} of {int(T2.sum())}: median 68 % coverage {np.median(cv68):.2f}, 95 % {np.median(cv95):.2f}")
    check("C6 (reported; load-bearing for the conditioned T2 rows): the median coverage of the conditioned T2 rows is >= 60 % (68 %) and >= 88 % (95 %)", f"conditioned T2 rows {len(idx2)}: 68 % {np.median(cv68):.2f}, 95 % {np.median(cv95):.2f}", bool(np.median(cv68) >= 0.60 and np.median(cv95) >= 0.88), load_bearing=False)
    pfd1 = all(ok for n, ok, lb in CHK if lb and not n.startswith("C6"))
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C5)")
    P(f"  PF-D2 ILL-CONDITIONED rows: T0 {int(ILL.sum())} of {N}, T1 {int(ILL[T1].sum())} of {int(T1.sum())}, T2 {int(ILL[T2].sum())} of {int(T2.sum())}")
    P(f"  PF-D3 DRAWABLE as an estimate: T2 {int(((~ILL) & T2 & pfd1).sum())} of {int(T2.sum())}; T0 {int(((~ILL) & pfd1).sum())} of {N} (every drawable stars-only row is an upper bound on s*, never a measurement)")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored (HE4-HE9 are scored at stage B):")
    he = {}
    he["HE1"] = bool(0.5 <= float(np.median(Y0[T1])) <= 3.0 and float(ILL[T1].mean()) <= 0.25)
    he["HE2"] = bool(float(((Y0 >= 0.3) & (Y0 <= 6)).mean()) >= 0.60)
    he["HE3"] = bool(int(RC_M.sum()) == 12 and int((RC_M & T1).sum()) >= 4 and int(KM_M.sum()) == 5)
    for k, v in he.items(): P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(tiers={k: int(v.sum()) for k, v in {"T1": T1, "T2": T2, "T0": T0, **POOLS}.items()}, rc100=int(RC_M.sum()), kmos3d=int(KM_M.sum()), phibss=int(PH_M.sum()), gas_rows=GASROWS, hand_estimates=he, pf=dict(PF_D1=bool(pfd1), n_ill_T2=int(ILL[T2].sum())),
               y0=Y0.tolist(), y2=Y2.tolist(), lever=LEV.tolist(), ill=ILL.tolist(), src=SRC, rc100_flags=RC_M.tolist(), kmos3d_flags=KM_M.tolist(), cov68=cv68.tolist(), cov95=cv95.tolist())

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V_rot, sigma0, V_c x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2800)
    if SELFTEST:
        gob = GB0 * NU(GB0 / (2.0 * A0C)) * 10 ** rngS.normal(0, 0.15, N)
        VC = np.sqrt(gob * RE / H.G2SI); EVC_HI = EVC_LO = 0.10 * VC; VROT = VC.copy(); SIG0 = np.zeros(N)
        P("SELFTEST: V_c fabricated from the law at s_true = 2 on each galaxy's B0 baryons (+0.15 dex scatter), V_rot = V_c, sigma0 = 0; the real velocity-bearing columns are not even loaded")
    else:
        mult = 2.0 if MUTATE else 1.0
        VC = mult * t6["Vc_kms"].reindex(SRC).values.astype(float); EVC_LO = mult * t6["Vc_kms_errlo"].reindex(SRC).values.astype(float); EVC_HI = mult * t6["Vc_kms_errhi"].reindex(SRC).values.astype(float)
        VROT = mult * t6["Vrot_kms"].reindex(SRC).values.astype(float); SIG0 = mult * t6["sigma0_kms"].reindex(SRC).values.astype(float)
    EVC_LO = np.where(np.isfinite(EVC_LO), EVC_LO, np.nanmedian(EVC_LO)); EVC_HI = np.where(np.isfinite(EVC_HI), EVC_HI, np.nanmedian(EVC_HI))
    GO = VC ** 2 / RE * H.G2SI; GO_ROT = VROT ** 2 / RE * H.G2SI
    DD = GO / GB0
    RES = {}
    KN_LIST = ["rotation only (V_rot)", "radius 1.5 R_e (V_c fixed)", "radius 2 R_e (V_c fixed)", "R_e,* x1.5", "R_e,* /1.5", "spherical", "kernel P2"]
    KGR = {"rotation only (V_rot)": "pressure", "radius 1.5 R_e (V_c fixed)": "radius", "radius 2 R_e (V_c fixed)": "radius", "R_e,* x1.5": "geometry", "R_e,* /1.5": "geometry", "spherical": "geometry", "kernel P2": "kernel"}

    def variant(i, nm, gas=None):
        """(g_obs, g_bar, kernel) for galaxy i; gas = (Mmol, scale_kpc or None) adds gas in the same disc"""
        def gb(re_star=None, sph=False, r=None):
            r = RE[i] if r is None else r; base = float(gbar(MS[i], RE[i], r, star_re=re_star, sph=sph))
            if gas is not None: base += float(gbar(gas[0], RE[i] if gas[1] is None else gas[1], r, star_re=None, sph=sph))
            return base
        if nm == "rotation only (V_rot)": return GO_ROT[i], gb(), NU
        if nm == "radius 1.5 R_e (V_c fixed)": return VC[i] ** 2 / (1.5 * RE[i]) * H.G2SI, gb(r=1.5 * RE[i]), NU
        if nm == "radius 2 R_e (V_c fixed)": return VC[i] ** 2 / (2.0 * RE[i]) * H.G2SI, gb(r=2.0 * RE[i]), NU
        if nm == "R_e,* x1.5": return GO[i], gb(re_star=1.5 * RE[i]), NU
        if nm == "R_e,* /1.5": return GO[i], gb(re_star=RE[i] / 1.5), NU
        if nm == "spherical": return GO[i], gb(sph=True), NU
        if nm == "kernel P2": return GO[i], gb(), NUP2

    def mc_gal(i, label, gas=None, B=B_MC):
        rng = np.random.default_rng(zlib.crc32(("280|" + label).encode()) % 100000)
        Vd = H.split_normal(rng, VC[i], EVC_HI[i], EVC_LO[i], B); Red = H.split_normal(rng, RE[i], RE_HI[i], RE_LO[i], B).clip(0.3)
        Msd = MS[i] * 10 ** rng.normal(0, 0.20, B)
        god = Vd ** 2 / Red * H.G2SI; gbd = H.gdisc(Msd, Red, Red)
        if gas is not None: gbd = gbd + H.gdisc(gas[0] * 10 ** rng.normal(0, gas[2], B), Red, Red)
        Dd = god / gbd; lsd, ud = H.AI.implied(Dd[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud); frc = float(np.mean(ud & (Dd > 1.0)))
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        return q, frn, frc, dq

    def base_row(i, label, gb0, gas=None):
        D0 = GO[i] / gb0; ls0, st0 = H.s_status(np.array([D0]), np.array([gb0]))
        q, frn, frc, dq = mc_gal(i, label, gas=gas)
        dF0 = float(np.log10(GO[i] / (gb0 * float(NU(np.array([gb0 / A0C]))[0]))))
        kn = {}
        for nm in KN_LIST:
            go_, gb_, nu_ = variant(i, nm, gas=(gas[0], None) if gas is not None else None); lk, sk = H.s_status(np.array([go_ / gb_]), np.array([gb_]), nu_)
            kn[nm] = None if (st0 != "root" or sk != "root") else lk - ls0; kn[nm + "|status"] = sk
        if gas is not None and np.isfinite(gas[3] if gas[3] is not None else float("nan")):
            go_, gb_, nu_ = GO[i], float(gbar(MS[i], RE[i], RE[i])) + float(gbar(gas[0], gas[3], RE[i])), NU; lk, sk = H.s_status(np.array([go_ / gb_]), np.array([gb_]), nu_)
            kn["gas scale = CO size"] = None if (st0 != "root" or sk != "root") else lk - ls0; kn["gas scale = CO size|status"] = sk
        grp = {}
        for nm, v in kn.items():
            if "|status" in nm or v is None: continue
            grp.setdefault(KGR.get(nm, "gas"), []).append(abs(v))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        lv_nl, lf_nl = H.lever1(NU(np.array([gb0 / A0C])), np.array([gb0])); d1 = H.shift_to_s1(np.array([D0]), np.array([gb0]))
        return dict(D=D0, ls=ls0, status=st0, s=H.s_val_status(ls0, st0), q=q, frac_mc_noroot=frn, frac_mc_ceiling=frc, delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], knobs=kn, recipe_half=half, n_knobs_with_root=sum(1 for nm in kn if nm.endswith("|status") and kn[nm] == "root"),
                    lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=H.delta_floor(np.array([D0])), delta_to_s1=d1, gas_to_star_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")))

    for i in range(N):
        lab = SRC[i]; R_ = base_row(i, lab, GB0[i])
        l2, s2 = H.s_status(np.array([GO[i] / GB2[i]]), np.array([GB2[i]]))
        bands = H.band_solutions(np.array([DD[i]]), np.array([GB0[i]])); star_b = {s_: H.s_star(np.array([GO[i] / (GB0[i] * 10 ** s_)]), np.array([GB0[i] * 10 ** s_])) for s_ in (-0.30, -0.15, 0.15, 0.30)}
        R_.update(label=lab, kind="galaxy", z=float(Z[i]), logMs=float(LMS[i]), Re=float(RE[i]), GO=float(GO[i]), GO_rot=float(GO_ROT[i]), GB=float(GB0[i]), y=float(Y0[i]), status_B2=s2, s_B2=H.s_val_status(l2, s2), D_B2=float(GO[i] / GB2[i]), mu=float(MUV[i]),
                  bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, star_bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in star_b.items()},
                  tier=("T1" if T1[i] else ("T2" if T2[i] else "T0")), criteria=CRIT[i], rc100=bool(RC_M[i]), kmos3d=bool(KM_M[i]), phibss=bool(PH_M[i]), irr=bool(IRR[i]), gcls="D (no gas; stars-only lower limit)", branch="stars only")
        RES[lab] = R_
    for s, g in GR.items():                                                  # PHIBSS gas rows (class S)
        i = g["i"]; lab = f"{s} [stars+CO]"
        R_ = base_row(i, lab, g["gb1"], gas=(g["Mmol"], None, g["sig"], (g["rh_co"] if np.isfinite(g["rh_co"]) else None)))
        def corner(sg, ss):
            gbp = g["gs"] * 10 ** ss + g["gg"] * 10 ** sg; l_, s_t = H.s_status(np.array([GO[i] / gbp]), np.array([gbp])); return H.s_val_status(l_, s_t), s_t
        band = {}
        for lvl, (sg, ss) in (("inner", (0.213, 0.15)), ("outer", (0.671, 0.30))):
            cm, cp = corner(-sg, -ss), corner(+sg, +ss); band[lvl] = dict(lo=min(cm[0], cp[0]), hi=max(cm[0], cp[0]), noroot=int(cm[1] != "root" or cp[1] != "root"))
        R_.update(label=lab, kind="gas", z=float(Z[i]), logMs=float(LMS[i]), Re=float(RE[i]), GO=float(GO[i]), GO_rot=float(GO_ROT[i]), GB=float(g["gb1"]), y=float(g["gb1"] / A0C), status_B2="n/a", s_B2=float("nan"), D_B2=float("nan"), mu=float("nan"), gasband=band,
                  tier=("T1" if T1[i] else ("T2" if T2[i] else "T0")), criteria=CRIT[i], rc100=bool(RC_M[i]), kmos3d=bool(KM_M[i]), phibss=True, irr=bool(IRR[i]), gcls=f"S (PHIBSS CO, {g['type']}; Galactic alpha_CO)", branch="stars + CO")
        RES[lab] = R_
    nst = {s_: sum(1 for k in SRC if RES[k]["status"] == s_) for s_ in ("root", "floor", "ceiling")}
    P(f"  per-galaxy rows computed ({time.time() - TSTART:.0f} s); status counts (38 stars-only rows): {nst}; T2: " + ", ".join(f"{s_}: {sum(1 for i in np.where(T2)[0] if RES[SRC[i]]['status'] == s_)}" for s_ in ("root", "floor", "ceiling")) + "; T1: " + ", ".join(f"{s_}: {sum(1 for i in np.where(T1)[0] if RES[SRC[i]]['status'] == s_)}" for s_ in ("root", "floor", "ceiling")))
    P("  rows (T2 and the gas rows): source, z, log M*, R_e, D, delta_FLAT, y, status and bound (B0 or B1) | B2")
    for i in range(N):
        R_ = RES[SRC[i]]
        if not (T2[i]): continue
        b0 = (f"s* <= {10 ** R_['ls']:.3g}" if R_["status"] == "root" else ("FLOOR (D <= 1)" if R_["status"] == "floor" else "CEILING (s* > 1000)")); b2 = (f"s* = {R_['s_B2']:.3g}" if R_["status_B2"] == "root" else R_["status_B2"].upper())
        P(f"    {SRC[i]:13s} z {Z[i]:.2f} M* {LMS[i]:.2f} R_e {RE[i]:4.1f} D {R_['D']:7.3f} dF {R_['delta_FLAT']:+.3f} y {Y0[i]:5.2f}  {b0:22s} | B2 {b2}{' T1' if T1[i] else ''}{' RC100' if RC_M[i] else ''}{' KMOS3D' if KM_M[i] else ''}{' PHIBSS' if PH_M[i] else ''}{' ILL' if R_['ill'] else ''}")
    for s, g in GR.items():
        R_ = RES[f"{s} [stars+CO]"]; b0 = (f"s* <= {10 ** R_['ls']:.3g}" if R_["status"] == "root" else ("FLOOR (D <= 1)" if R_["status"] == "floor" else "CEILING (s* > 1000)"))
        P(f"    {R_['label']:24s} D {R_['D']:7.3f} dF {R_['delta_FLAT']:+.3f} y {R_['y']:5.2f}  {b0:22s} (stars-only row: {RES[s]['status']}{' s* <= ' + format(RES[s]['s'], '.3g') if RES[s]['status'] == 'root' else ''}; D {RES[s]['D']:.3f}) gas band inner [{R_['gasband']['inner']['lo']:.3g}, {R_['gasband']['inner']['hi']:.3g}] outer [{R_['gasband']['outer']['lo']:.3g}, {R_['gasband']['outer']['hi']:.3g}]{' ILL' if R_['ill'] else ''}")
    # pooled rows
    for pn, m in POOLS.items():
        Dp, GBp = DD[m], GB0[m]; zm = float(np.median(Z[m])); n_m = int(m.sum())
        ls0, st0 = H.s_status(Dp, GBp); rng = np.random.default_rng(zlib.crc32(("280|" + pn).encode()) % 100000)
        ib = rng.integers(0, n_m, size=(B_MC, n_m)); lsb, ub = H.AI.implied(Dp[ib], GBp[ib], NU, A0C); q, frn = H.rooted_pct(lsb, ub); qf = [float(v) for v in np.percentile(lsb, [2.5, 16, 50, 84, 97.5])]
        frc = float(np.mean(ub & (np.median(Dp[ib], axis=1) > 1.0)))
        bands = H.band_solutions(Dp, GBp); kn = {}
        for nm in KN_LIST:
            gos, gbs, nu_ = [], [], NU
            for i in np.where(m)[0]:
                go_, gb_, nu_ = variant(i, nm); gos.append(go_); gbs.append(gb_)
            lk, sk = H.s_status(np.array(gos) / np.array(gbs), np.array(gbs), nu_); kn[nm] = None if (st0 != "root" or sk != "root") else lk - ls0
        grp = {}
        for nm in KN_LIST:
            if kn.get(nm) is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        d1 = H.shift_to_s1(Dp, GBp); l2, s2 = H.s_status(GO[m] / GB2[m], GB2[m])
        RES[pn] = dict(label=pn, kind="pooled", n=n_m, z=zm, ls=ls0, status=st0, s=H.s_val_status(ls0, st0), q=qf, q_rooted=q, frac_mc_noroot=frn, frac_mc_ceiling=frc, median_D=float(np.median(Dp)), delta_floor=H.delta_floor(Dp),
                       bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, knobs=kn, recipe_half=half, delta_to_s1=d1, gas_to_star_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")), lever=H.lever1(Dp, GBp)[0],
                       median_dF=float(np.median(np.log10(GO[m] / (GB0[m] * NU(Y0[m]))))), status_B2=s2, s_B2=H.s_val_status(l2, s2), median_y=float(np.median(Y0[m])), ill_frac=float("nan"))
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        P(f"  {pn:8s} (n {n_m:3d}, z_med {zm:.3f}): median D {np.median(Dp):.3f}  {st0.upper()}" + (f" s* <= {10 ** ls0:.3g}" if st0 == "root" else "") + f"; bootstrap 68 % [{10 ** qf[1]:.3g}, {10 ** qf[3]:.3g}] 95 % [{10 ** qf[0]:.3g}, {10 ** qf[4]:.3g}]; baryon +-0.15 [{b15[0]:.3g}, {b15[1]:.3g}] +-0.30 [{b30[0]:.3g}, {b30[1]:.3g}]; "
          f"Delta_floor {np.log10(np.median(Dp)):+.3f}; gas_req {RES[pn]['gas_to_star_req']:+.2f}; median delta_FLAT {RES[pn]['median_dF']:+.3f}; B2 {s2}" + (f" s* = {10 ** l2:.3g}" if s2 == "root" else "") + f"; recipe half-width {half:.3f}")
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg280_stageB_results.json")))["numbers"]["rows"]
        def inv_nu(Dv):
            lo, hi = -25.0, 25.0
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if float(NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
                else: hi = mid
            return math.exp(0.5 * (lo + hi))
        bad = 0.0; nroot = 0
        for k in SRC:
            R_ = RES[k]
            if R_["status"] == "root": nroot += 1; bad = max(bad, abs(math.log10(R_["GB"] / inv_nu(R_["D"]) / A0C) - R_["ls"]))
        n_gt1_m = int(sum(1 for k in SRC if RES[k]["D"] > 1)); n_gt1_0 = int(sum(1 for k in SRC if main[k]["D"] > 1))
        check("M2 MUTATE=1 (reactivity; the count is of rows with D > 1, not of roots, because of the solver bracket): V_rot, sigma0 and V_c x 2; rows with status ROOT satisfy the closed-form inversion of their own (D, g_bar) to 1e-6 dex and the number of rows with D > 1 is at least the main run's",
              f"rows with D > 1: mutated {n_gt1_m}, main {n_gt1_0}; rows with a root {nroot}; max |d log10 s*| against the independent inversion {bad:.1e}", bad < 1e-6 and n_gt1_m >= n_gt1_0)
    else:
        d1m = 0.0
        for k in SRC:
            R_ = RES[k]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array([[R_["D"]]]), np.array([[R_["GB"]]]), NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every galaxy row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for k in SRC if RES[k]['status'] == 'root')} rows with a root)", d1m < 1e-9)
        ok3 = [RES[k]["n"] for k in ("PT1", "PT2", "PT0")] == [11, 18, 38] and RES["PT2z1"]["n"] + RES["PT2z2"]["n"] == 18 and RES["PT2_new"]["n"] == int((T2 & ~RC_M & ~KM_M).sum())
        check("M3 the tier memberships and the pooled sizes (PT1 11, PT2 18, PT0 38; the z halves partition PT2; PT2_new is T2 without any RC100 or KMOS3D match)", f"{[(k, RES[k]['n']) for k in POOLS]}", ok3)
        check("M7 (reported) the cross-match counts of stage A are unchanged", f"RC100 {int(RC_M.sum())}, KMOS3D {int(KM_M.sum())}, PHIBSS {int(PH_M.sum())}, gas rows {len(GR)}", int(RC_M.sum()) == 12 and int(KM_M.sum()) == 5 and int(PH_M.sum()) == 6 and len(GR) == 4, load_bearing=False)
        if not SELFTEST:
            vc_calc = np.sqrt(VROT ** 2 + 3.36 * SIG0 ** 2); r5 = np.abs(vc_calc / VC - 1)
            check("M5 V_c^2 = V_rot^2 + 3.36 sigma0^2 (FS+18's own formula) reproduces the table's V_c for every row to within 2 % (the table prints integers)", f"max relative difference {r5.max():.4f} ({SRC[int(np.argmax(r5))]}); rows above 2 %: {[SRC[j] for j in np.where(r5 > 0.02)[0]]}; median {np.median(r5):.4f}", bool((r5 <= 0.02).all()))
            md = t6["Mdyn_1e10Msun"].reindex(SRC).values.astype(float); md_calc = 2.0 * RE * VC ** 2 / H.G_KPC / 1e10; r6 = np.abs(md_calc / md - 1)
            check("M6 M_dyn = 2 R_e V_c^2 / G reproduces the table's M_dyn to within 5 % (the table prints two to three digits)", f"max relative difference {np.nanmax(r6):.4f} ({SRC[int(np.nanargmax(r6))]}); rows above 5 %: {[SRC[j] for j in np.where(r6 > 0.05)[0]]}; median {np.nanmedian(r6):.4f}", bool((r6[np.isfinite(r6)] <= 0.05).all()))
        else:
            tested = [k for k in SRC if RES[k]["status"] == "root" and not RES[k]["ill"] and T2[SRC.index(k)]]
            if tested:
                inside = sum(1 for t in tested if np.isfinite(RES[t]["q"][0]) and RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4])
                check("SELFTEST: the conditioned T2 rows with a root return the fabricated truth (s = 2) inside their 95 % interval in at least 80 % of cases", f"{inside} of {len(tested)}; pooled PT2 s* {RES['PT2']['s']:.3g} ({RES['PT2']['status']}), 95 % [{10 ** RES['PT2']['q'][0]:.3g}, {10 ** RES['PT2']['q'][4]:.3g}]", inside >= 0.8 * len(tested))
            else: P("  SELFTEST: no conditioned T2 row with a root: truth recovery not applicable")
    if not (MUTATE or SELFTEST):
        P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9; HE1-HE3 were scored at stage A) scored:")
        t2r = [RES[SRC[i]] for i in np.where(T2)[0]]; dmed = float(np.median([r["D"] for r in t2r])); flo = float(np.mean([r["status"] == "floor" for r in t2r])); p2, pn_ = RES["PT2"], RES["PT2_new"]
        gB = RES["Q2343-BX610 [stars+CO]"]; others = [RES[f"{k} [stars+CO]"] for k in GASROWS if k != "Q2343-BX610"]
        m56 = [ok for n_, ok, lb in CHK if n_.startswith("M5") or n_.startswith("M6")]
        he = {"HE4": bool(1.0 <= dmed <= 3.0 and 0.10 <= flo <= 0.40), "HE5": bool(p2["status"] == "root" and 1.0 <= p2["s"] <= 6.0),
              "HE6": bool(p2["status_B2"] != "root" or (p2["status"] == "root" and p2["s_B2"] <= p2["s"] / 3.0)),
              "HE7": bool(gB["status"] == "floor" and any(r["status"] == "root" for r in others)),
              "HE8": bool(pn_["status"] == p2["status"] and (p2["status"] != "root" or (0.5 <= pn_["s"] / p2["s"] <= 2.0))),
              "HE9": bool(len(m56) == 2 and all(m56))}
        P(f"    HE4: median D(B0) of T2 {dmed:.3f} (needs 1.0-3.0), T2 rows at the floor {100 * flo:.0f} % (needs 10-40 %): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: PT2 {p2['status']}" + (f", s* <= {p2['s']:.3g}" if p2["status"] == "root" else "") + f" (needs a root in 1-6): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: PT2 with B2: {p2['status_B2']}" + (f", s* = {p2['s_B2']:.3g} against the B0 bound {p2['s']:.3g}" if p2["status_B2"] == "root" else "") + f": {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        P(f"    HE7: BX610 [stars+CO] {gB['status']} (D {gB['D']:.3f}); the other gas rows: " + ", ".join(f"{r['label']} {r['status']}" for r in others) + f": {'hit' if he['HE7'] else 'MISS (kept as it falls)'}")
        P(f"    HE8: PT2_new {pn_['status']}" + (f" s* <= {pn_['s']:.3g}" if pn_["status"] == "root" else "") + f" against PT2 {p2['status']}" + (f" s* <= {p2['s']:.3g}" if p2["status"] == "root" else "") + f": {'hit' if he['HE8'] else 'MISS (kept as it falls)'}")
        P(f"    HE9: M5 and M6 {'hold' if he['HE9'] else 'do not both hold'}: {'hit' if he['HE9'] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates_B"] = he
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling",
                              "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "gas_to_star_req", "s_B2", "status_B2", "status", "tier", "criteria", "phibss_match", "kmos3d_match", "rc100_match", "branch", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    nan = float("nan"); rows = []
    keys = SRC + [f"{s} [stars+CO]" for s in GR] + list(POOLS)
    for lab in keys:
        R_ = RES[lab]; pooled = R_["kind"] == "pooled"; gasrow = R_["kind"] == "gas"; st = R_["status"]; q = R_["q"]
        if gasrow:
            b15 = (R_["gasband"]["inner"]["lo"], R_["gasband"]["inner"]["hi"], R_["gasband"]["inner"]["noroot"]); b30 = (R_["gasband"]["outer"]["lo"], R_["gasband"]["outer"]["hi"], R_["gasband"]["outer"]["noroot"])
        else:
            bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}; b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        empty = 1000.0 if st == "ceiling" else FLOOR
        if pooled: lo68, hi68, lo95, hi95 = 10 ** q[1], 10 ** q[3], 10 ** q[0], 10 ** q[4]
        else: lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(R_["z"], lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]
        if not pooled:
            sb_ = ({float(k): (v["ls"], v["unb"]) for k, v in R_["star_bands"].items()} if not gasrow else None)
            si, so = (H.band_edges(sb_, -0.15, 0.15), H.band_edges(sb_, -0.30, 0.30)) if sb_ else ((nan, nan, 0), (nan, nan, 0))
            extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], si[0], si[1], so[0], so[1], R_["delta_floor"], R_["delta_to_s1"], R_["gas_to_star_req"], R_["s_B2"], R_["status_B2"], st,
                     R_["tier"], R_["criteria"], int(R_["phibss"]), int(R_["kmos3d"]), int(R_["rc100"]), R_["branch"]]
            q_ = ("ILL-CONDITIONED; " if R_["ill"] else "") + {"root": "has a root: " + ("an UPPER bound (stars-only lower limit)" if not gasrow else "stars + PHIBSS CO (class S): an upper bound only if the gas is right"), "floor": "FLOOR: no root, D <= 1" + (" (robust against any added gas)" if not gasrow else " (robust against added stars, not against a lower alpha_CO)"),
                                                                                "ceiling": f"CEILING: D = {R_['D']:.1f} > 1 but s* > 1000: vacuous"}[st] + ("; irregular kinematics (rotation assumed)" if R_["irr"] else "") + ("; overlaps RC100" if R_["rc100"] else "") + ("; overlaps the KMOS3D lane" if R_["kmos3d"] else "") + "; V_c is a peak-to-peak velocity at an unrecorded radius (r = R_e a convention)"
            n_k = R_["n_knobs_with_root"]; objname = f"SINS {lab}"; gcl = R_["gcls"]
        else:
            extra = [R_["median_y"], R_["lever"], 0, R_["median_dF"], nan, nan, R_["median_D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], nan, nan, nan, nan, R_["delta_floor"], R_["delta_to_s1"], R_["gas_to_star_req"], R_["s_B2"], R_["status_B2"], st, "pooled", "", "", "", "", "stars only"]
            q_ = f"pooled row ({R_['n']} rows), stars-only lower limit: " + {"root": "has a root: s* is an UPPER bound", "floor": "FLOOR (median D <= 1)", "ceiling": "CEILING (median D > 1, s* > 1000)"}[st] + ("; overlap-free (no RC100 or KMOS3D match)" if lab == "PT2_new" else "") + "; coverage only (CFG196 D0 NON-DIAGNOSTIC); class D: no law statement"; n_k = ""; objname = f"SINS pooled {lab}"; gcl = "D (pooled; no gas)"
        sstar = R_["s"]
        rows.append(["CFG280", objname, gcl, f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", n_k,
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "baryons are a lower limit (stars only) or class S: not a measurement", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg280_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg280_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg280{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg280{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
