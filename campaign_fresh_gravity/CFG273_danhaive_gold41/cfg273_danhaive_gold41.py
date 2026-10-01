#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG273 -- implied-a0 upper bounds (or no-root floors) for the 41 Danhaive+25 "gold" JADES discs (z 3.80-5.82): stars-only baryons (a lower limit), class D (no gas).

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG273_danhaive_gold41/FROZEN_CRITERIA.md (92a868901).
  g_obs     G M_dyn / (1.8 r_e^2) at r = r_e from the authors' M_dyn (pressure included once); g_bar  B0 = stars only, one thin exponential disc with R_e,* = r_e; B2 = scaling-relation gas (sensitivity).
  STAGE=A   the blind pre-flight: M_dyn, sigma0 and v/sigma0 are NOT loaded; no g_obs, D, delta or s* is formed.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (M_dyn x 4); STAGE=B SELFTEST=1 (fabricated M_dyn on the law at s = 2).
Run: STAGE=A python3 .../cfg273_danhaive_gold41.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv, contextlib
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

T0 = time.time()
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
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: every M_dyn x 4 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED M_dyn on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
CSVP = os.path.join(REPO, "data_assembly", "arxiv_tables", "danhaive2025_gold.csv")
allc = list(pd.read_csv(CSVP, nrows=0).columns)
VEL = ("v_over_sigma0", "sigma0", "logMdyn")
usec = allc if STAGE == "B" else [c for c in allc if not any(v in c for v in VEL)]
D_ = pd.read_csv(CSVP, usecols=usec)
N = len(D_)
P(f"{os.path.basename(CSVP)} sha256 {H.sha(CSVP)}; {N} rows; kinematic columns loaded: {STAGE == 'B'}")
ID = D_["jades_id"].astype(int).values
Z = D_["z"].values.astype(float)
LMS, EMSH, EMSL = D_["logMstar"].values.astype(float), D_["logMstar_errhi"].values.astype(float), D_["logMstar_errlo"].values.astype(float)
RE = D_["re_kpc"].values.astype(float)
MS = 10 ** LMS
CRIS08 = [1088814, 1077545, 1086406]
KNOWN_LOW = [1082948, 1009935, 1015956, 1085659]
IS_C08 = np.isin(ID, CRIS08)
if STAGE == "B":
    LMD, EMDH, EMDL = D_["logMdyn"].values.astype(float), D_["logMdyn_errhi"].values.astype(float), D_["logMdyn_errlo"].values.astype(float)
    VOS, SIG = D_["v_over_sigma0"].values.astype(float), D_["sigma0_kms"].values.astype(float)
    S0LIM = D_["sigma0_kms_lim"].astype(str).str.strip().isin(["<"]).values
    n_nan_err = int(np.sum(~np.isfinite(EMDH) | ~np.isfinite(EMDL)))
    fb = float(np.nanmedian(np.concatenate([EMDH, EMDL])))
    EMDH = np.where(np.isfinite(EMDH), EMDH, fb); EMDL = np.where(np.isfinite(EMDL), EMDL, fb)
    P(f"sigma0 limits: {int(S0LIM.sum())}; log M_dyn errors missing in {n_nan_err} rows (replaced by the median {fb:.3f} dex)")
ZB = {"Pz1": (Z >= 3.8) & (Z < 4.2), "Pz2": (Z >= 4.2) & (Z < 5.0), "Pz3": Z >= 5.0}


def mu_mol(z, logM):
    return 10 ** (0.06 - 3.3 * (np.log10(1 + z) - 0.65) ** 2 - 0.41 * (logM - 10.7))


def gbar(Ms, re, *, stars_re=None, sph=False, gas=0.0):
    f = H.gsph if sph else H.gdisc
    sre = re if stars_re is None else stars_re
    return f(Ms, sre, re) + (f(Ms * gas, sre, re) if np.any(np.asarray(gas) > 0) else 0.0)


GB0 = np.array([float(gbar(MS[i], RE[i])) for i in range(N)])
MUv = mu_mol(Z, LMS)
GB2 = np.array([float(gbar(MS[i], RE[i], gas=MUv[i])) for i in range(N)])
Y0, Y2 = GB0 / A0C, GB2 / A0C
NUY0 = NU(Y0)
P(f"z bins: Pz1 {int(ZB['Pz1'].sum())}, Pz2 {int(ZB['Pz2'].sum())}, Pz3 {int(ZB['Pz3'].sum())}; CRISTAL-08 z-candidates in the table: {[int(i) for i in ID[IS_C08]]}")

# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (M_dyn, sigma0 and v/sigma0 are not loaded; no g_obs, D, delta or s* is formed)")
    c235 = json.load(open(os.path.join(CFG, "CFG235_break_search", "CFG235_00_sample_results.json")))["counts"]
    check("C1 CONTROL: 41 rows, finite z, M*, r_e and M* errors, z bins 21 / 12 / 8, the CRISTAL-08 candidates present", f"N {N}; bins {[int(v.sum()) for v in ZB.values()]}; candidates {[int(i) for i in ID[IS_C08]]}",
          N == 41 and np.isfinite(np.c_[Z, LMS, RE, EMSH, EMSL]).all() and [int(v.sum()) for v in ZB.values()] == [21, 12, 8] and IS_C08.sum() == 3)
    yy = np.linspace(0.05, 40, 400000); hh = H.i0e(yy) * H.k0e(yy) - H.i1e(yy) * H.k1e(yy); peak = float(np.max(2 * yy ** 2 * hh)); farr = float(H.gdisc(1e11, 3.0, 150.0) / (H.G_KPC * 1e11 / 150.0 ** 2 * H.G2SI))
    src29 = open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score.py")).read(); seg = src29[src29.index("def disc_v2"):src29.index("P(__doc__")]
    ns29 = {"G_KPC": H.G_KPC, "XN": H.XN, "G2SI": H.G2SI, "i0e": H.i0e, "i1e": H.i1e, "k0e": H.k0e, "k1e": H.k1e, "math": math, "np": np}; exec(compile(seg, "cfg229_score.py", "exec"), ns29)
    rr_ = np.random.default_rng(1234); dmax = 0.0
    for _ in range(200):
        M_, Re_, Rr_ = 10 ** rr_.uniform(9, 12.5), rr_.uniform(0.5, 8), rr_.uniform(1, 20); dmax = max(dmax, abs(H.gdisc(M_, Re_, Rr_) / ns29["gdisc"](M_, Re_, Rr_) - 1))
    check("C2 CONTROL: Freeman's peak V^2 = 0.3872 G M / R_d to 0.003, g -> G M / r^2 far from a compact mass to 1e-3, and gdisc equals CFG229's on 200 random inputs to 1e-12", f"peak {peak:.4f}; far-field ratio {farr:.5f}; max deviation {dmax:.1e}", abs(peak / 0.3872 - 1) < 0.003 and abs(farr - 1) < 1e-3 and dmax < 1e-12)
    check("C3 CONTROL (counts only): CFG235's committed sample counts 41 Danhaive rows", f"CFG235 counts {c235}", c235.get("D") == 41)
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
    check("C5 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every row's stars-only baryon side", f"max |d log10 s| {d5:.1e}", d5 < 1e-6)
    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; B0 = stars only at r = r_e; ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    LEV, ILL = np.zeros(N), np.zeros(N, bool)
    for i in range(N):
        lv, fl = H.lever1(np.array([NUY0[i]]), np.array([GB0[i]])); LEV[i] = lv; ILL[i] = bool(fl or abs(lv) >= 10)
    P(f"    y(B0): min {Y0.min():.2f}, 16/50/84% {np.percentile(Y0, 16):.2f} / {np.median(Y0):.2f} / {np.percentile(Y0, 84):.2f}, max {Y0.max():.2f};  y(B2) median {np.median(Y2):.2f}")
    P(f"    rows with y < 0.3: {int((Y0 < 0.3).sum())}; y > 6: {int((Y0 > 6).sum())}; y > 8: {int((Y0 > 8).sum())}; ILL-CONDITIONED: {int(ILL.sum())} (ids {[int(i) for i in ID[ILL]]}; log M* {[round(float(v), 2) for v in LMS[ILL]]})")
    for nm, m in (("PALL", np.ones(N, bool)), ("Pz1", ZB["Pz1"]), ("Pz2", ZB["Pz2"]), ("Pz3", ZB["Pz3"])):
        P(f"    {nm}: n {int(m.sum())}, y(B0) median {np.median(Y0[m]):.2f} (min {Y0[m].min():.2f}, max {Y0[m].max():.2f}), ILL {int(ILL[m].sum())}, T4 floor 3 sigma/sqrt(N) at sigma = 0.2 dex: {3 * 0.2 / math.sqrt(m.sum()):.3f} dex (calibration f free)")
    P("    per row: id z log M* r_e y(B0) nu(y) lever ILL mu_mol B2/B0")
    for i in range(N):
        P(f"      {ID[i]:8d} z {Z[i]:.2f} M* {LMS[i]:.2f} r_e {RE[i]:.2f} y {Y0[i]:6.2f} nu {NUY0[i]:.3f} lever {LEV[i]:+7.1f} {'ILL' if ILL[i] else '   '} mu {MUv[i]:.2f} B2/B0 {GB2[i] / GB0[i]:.2f}{' CRISTAL-08?' if IS_C08[i] else ''}{' KNOWN-LOW' if ID[i] in KNOWN_LOW else ''}")
    P("\nC6  COVERAGE (noiseless world on each row's B0 baryons; declared 0.15 dex error on log M_dyn; the published M* errors; 200 mock datasets, B = 1,000)")
    rng6 = np.random.default_rng(273); c68 = np.zeros(N); c95 = np.zeros(N); nd = np.zeros(N); sd = np.zeros(N)
    for i in range(N):
        sds = []
        gob_true = GB0[i] * float(NU(np.array([Y0[i]]))[0])
        for it in range(200):
            Ms_o = MS[i] * 10 ** H.split_normal(rng6, 0.0, EMSH[i], EMSL[i], 1)[0]
            god = gob_true * 10 ** rng6.normal(0, 0.15)
            gobm = god * 10 ** rng6.normal(0, 0.15, 1000)
            Msd = Ms_o * 10 ** H.split_normal(rng6, 0.0, EMSH[i], EMSL[i], 1000)
            gbd = H.gdisc(Msd, RE[i], RE[i])
            lsd, ud = H.AI.implied((gobm / gbd)[:, None], gbd[:, None], NU, A0C); q, fr = H.rooted_pct(lsd, ud)
            if np.isfinite(q[0]):
                nd[i] += 1; c68[i] += (q[1] <= 0.0 <= q[3]); c95[i] += (q[0] <= 0.0 <= q[4]); sds.append(0.5 * (q[3] - q[1]))
        sd[i] = np.median(sds) if sds else np.nan
    cv68, cv95 = c68 / np.maximum(nd, 1), c95 / np.maximum(nd, 1)
    P(f"    coverage 68 %: median {np.median(cv68):.2f} (min {cv68.min():.2f}); 95 %: median {np.median(cv95):.2f} (min {cv95.min():.2f}); median 68 % half-width {np.nanmedian(sd):.2f} dex; for the conditioned rows: 68 % median {np.median(cv68[~ILL]):.2f}, 95 % median {np.median(cv95[~ILL]):.2f}")
    okc = bool(np.median(cv68[~ILL]) >= 0.60 and np.median(cv95[~ILL]) >= 0.88) if (~ILL).any() else True
    check("C6 (reported; load-bearing for the conditioned rows): the median coverage of the conditioned rows is >= 60 % (68 %) and >= 88 % (95 %)", f"conditioned rows {int((~ILL).sum())}: 68 % {np.median(cv68[~ILL]):.2f}, 95 % {np.median(cv95[~ILL]):.2f}", okc, load_bearing=False)
    P("\nA3  KNOB EFFECTS ON g_bar (dex relative to B0; baryon side only; median / min / max over the 41 rows)")
    kb = {"compact stars r_e/1.58": np.array([gbar(MS[i], RE[i], stars_re=RE[i] / 1.58) for i in range(N)]), "R_e x1.5": np.array([gbar(MS[i], RE[i], stars_re=1.5 * RE[i]) for i in range(N)]),
          "R_e /1.5": np.array([gbar(MS[i], RE[i], stars_re=RE[i] / 1.5) for i in range(N)]), "spherical": np.array([gbar(MS[i], RE[i], sph=True) for i in range(N)])}
    for k, v in kb.items():
        dd = np.log10(v / GB0); P(f"    {k}: median {np.median(dd):+.3f}, min {dd.min():+.3f}, max {dd.max():+.3f}")
    pfd1 = all(ok for n, ok, lb in CHK if lb and not n.startswith("C6"))
    n_ill = int(ILL.sum())
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C5)")
    P(f"  PF-D2 ILL-CONDITIONED rows ({n_ill} of {N}): ids {[int(i) for i in ID[ILL]]}")
    P(f"  PF-D3 DRAWABLE as an upper bound: {int(((~ILL) & pfd1).sum())} of {N} rows (every drawable row is an upper bound on s*, never a measurement)")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored (HE3-HE7 are scored at stage B):")
    he = {}
    he["HE1"] = 0.7 <= float(np.median(Y0)) <= 4.0 and int((~ILL).sum()) >= 33 and bool(np.all(LMS[ILL] >= 10.0)) if ILL.any() else (0.7 <= float(np.median(Y0)) <= 4.0 and int((~ILL).sum()) >= 33)
    he["HE2"] = int((Y0 < 0.3).sum()) >= 3
    for k, v in he.items(): P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(inputs=dict(id=[int(i) for i in ID], z=Z.tolist(), logMs=LMS.tolist(), re=RE.tolist(), y0=Y0.tolist(), y2=Y2.tolist(), lever=LEV.tolist(), ill=ILL.tolist(), mu=MUv.tolist()),
               coverage=dict(c68=cv68.tolist(), c95=cv95.tolist(), nd=nd.tolist()), hand_estimates=he, pf=dict(PF_D1=bool(pfd1), n_ill=n_ill), counts_c235=c235)

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: M_dyn x 4)" if MUTATE else ""))
    rngS = np.random.default_rng(2730)
    if SELFTEST:
        gob = GB0 * NU(GB0 / (2.0 * A0C)) * 10 ** rngS.normal(0, 0.15, N)
        LMD = np.log10(gob / H.G2SI * 1.8 * RE ** 2 / H.G_KPC); EMDH = EMDL = np.full(N, 0.10)
        SIG = np.full(N, 50.0); VOS = np.sqrt(np.maximum(H.G_KPC * 10 ** LMD / (1.8 * RE) - 3.36 * SIG ** 2, 1.0)) / SIG; S0LIM = np.zeros(N, bool)
        P("SELFTEST: log M_dyn fabricated from the law at s_true = 2 on each row's B0 baryons (+0.15 dex scatter); the real kinematics are not used")
    if MUTATE:
        LMD = LMD + math.log10(4.0)
    GO = H.G_KPC * 10 ** LMD / (1.8 * RE ** 2) * H.G2SI
    DD = GO / GB0
    RES = {}
    KN_LIST = ["compact stars r_e/1.58", "R_e x1.5", "R_e /1.5", "spherical", "kernel P2", "rebuilt V = (v/sigma0) sigma0"]
    KGR = {"compact stars r_e/1.58": "geometry", "R_e x1.5": "geometry", "R_e /1.5": "geometry", "spherical": "geometry", "kernel P2": "kernel", "rebuilt V = (v/sigma0) sigma0": "velocity"}
    LMD1 = np.log10(1.8 * RE * ((VOS * SIG) ** 2 + 3.36 * SIG ** 2) / H.G_KPC)
    GO1 = H.G_KPC * 10 ** LMD1 / (1.8 * RE ** 2) * H.G2SI

    def variant(i, nm):
        if nm == "compact stars r_e/1.58": gb = float(gbar(MS[i], RE[i], stars_re=RE[i] / 1.58)); return GO[i], gb, NU
        if nm == "R_e x1.5": gb = float(gbar(MS[i], RE[i], stars_re=1.5 * RE[i])); return GO[i], gb, NU
        if nm == "R_e /1.5": gb = float(gbar(MS[i], RE[i], stars_re=RE[i] / 1.5)); return GO[i], gb, NU
        if nm == "spherical": gb = float(gbar(MS[i], RE[i], sph=True)); return GO[i], gb, NU
        if nm == "kernel P2": return GO[i], GB0[i], NUP2
        if nm == "rebuilt V = (v/sigma0) sigma0": return (GO1[i] if (not S0LIM[i] and np.isfinite(GO1[i])) else None), GB0[i], NU

    for i in range(N):
        lab = str(int(ID[i]))
        ls0, u0 = H.s_star(np.array([DD[i]]), np.array([GB0[i]]))
        lsb2, ub2 = H.s_star(np.array([GO[i] / GB2[i]]), np.array([GB2[i]]))
        rng = np.random.default_rng(zlib.crc32(("273|" + lab).encode()) % 100000)
        lMd = H.split_normal(rng, LMD[i], EMDH[i], EMDL[i], B_MC); lMs = H.split_normal(rng, LMS[i], EMSH[i], EMSL[i], B_MC)
        god = H.G_KPC * 10 ** lMd / (1.8 * RE[i] ** 2) * H.G2SI; gbd = H.gdisc(10 ** lMs, RE[i], RE[i])
        lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud)
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        dF0 = float(np.log10(GO[i] / (GB0[i] * float(NU(np.array([Y0[i]]))[0]))))
        bands = H.band_solutions(np.array([DD[i]]), np.array([GB0[i]]))
        star_b = {s_: H.s_star(np.array([GO[i] / (GB0[i] * 10 ** s_)]), np.array([GB0[i] * 10 ** s_])) for s_ in (-0.30, -0.15, 0.15, 0.30)}
        kn = {}
        for nm in KN_LIST:
            go_, gb_, nu_ = variant(i, nm)
            if go_ is None: continue
            lk, uk = H.s_star(np.array([go_ / gb_]), np.array([gb_]), nu_)
            kn[nm] = None if (u0 or uk) else lk - ls0; kn[nm + "|root"] = (not uk)
        grp = {}
        for nm in KN_LIST:
            if nm in kn and kn[nm] is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        n_root = sum(1 for nm in KN_LIST if nm in kn and kn[nm + "|root"]); n_k = sum(1 for nm in KN_LIST if nm in kn)
        lv_nl, lf_nl = H.lever1(np.array([NUY0[i]]), np.array([GB0[i]]))
        d1 = H.shift_to_s1(np.array([DD[i]]), np.array([GB0[i]]))
        RES[lab] = dict(id=int(ID[i]), z=float(Z[i]), n=1, logMs=float(LMS[i]), re=float(RE[i]), GO=float(GO[i]), GB=float(GB0[i]), D=float(DD[i]), y=float(Y0[i]), ls=ls0, no_root=u0, s=H.s_val(ls0, u0), q=q, frac_mc_noroot=frn,
                        delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], s_B2=H.s_val(lsb2, ub2), noroot_B2=ub2, D_B2=float(GO[i] / GB2[i]), bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()},
                        star_bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in star_b.items()}, knobs=kn, recipe_half=half, n_knobs_with_root=n_root, n_knobs=n_k, lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)),
                        delta_floor=H.delta_floor(np.array([DD[i]])), delta_to_s1=d1, gas_to_star_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")), s0lim=bool(S0LIM[i]), c08=bool(IS_C08[i]), known_low=bool(ID[i] in KNOWN_LOW))
        R_ = RES[lab]
        P(f"  {lab:>8s} z {Z[i]:.2f} M* {LMS[i]:.2f} r_e {RE[i]:.2f}  g_obs {GO[i]:.2e}  g_bar {GB0[i]:.2e}  D {DD[i]:.3f}  dF {dF0:+.3f}  y {Y0[i]:.2f}  " + ("NO ROOT" if u0 else f"s* <= {10 ** ls0:.3g}") + f"  B2: D {GO[i] / GB2[i]:.3f} " + ("NO ROOT" if ub2 else f"s* = {10 ** lsb2:.3g}")
          + f"  MC rooted 68 % [{10 ** q[1] if np.isfinite(q[1]) else float('nan'):.3g}, {10 ** q[3] if np.isfinite(q[3]) else float('nan'):.3g}] (no root {frn:.2f})  gas_req {R_['gas_to_star_req']:+.2f}{' ILL' if R_['ill'] else ''}{' sig0<' if S0LIM[i] else ''}{' C08?' if IS_C08[i] else ''}{' KNOWN-LOW' if ID[i] in KNOWN_LOW else ''}")
    # pooled rows
    POOL = {"PALL": np.ones(N, bool), "PDET": ~S0LIM, **ZB, "P38": ~IS_C08}
    for pn, m in POOL.items():
        Dp, GBp = DD[m], GB0[m]; zm = float(np.median(Z[m]))
        ls0, u0 = H.s_star(Dp, GBp); rng = np.random.default_rng(zlib.crc32(("273|" + pn).encode()) % 100000)
        ib = rng.integers(0, int(m.sum()), size=(B_MC, int(m.sum()))); lsb, ub = H.AI.implied(Dp[ib], GBp[ib], NU, A0C); q, frn = H.rooted_pct(lsb, ub)
        # the full-distribution percentiles (floor draws included) for the pooled interval, as CFG223
        qf = [float(v) for v in np.percentile(lsb, [2.5, 16, 50, 84, 97.5])]
        bands = H.band_solutions(Dp, GBp)
        kn = {}
        for nm in KN_LIST:
            if nm == "rebuilt V = (v/sigma0) sigma0":
                mm = m & ~S0LIM; D1 = GO1[mm] / GB0[mm]; lk, uk = H.s_star(D1, GB0[mm]); l00, u00 = H.s_star(DD[mm], GB0[mm]); kn[nm] = None if (u00 or uk) else lk - l00; continue
            gos, gbs, nu_ = [], [], NU
            for i in np.where(m)[0]:
                go_, gb_, nu_ = variant(i, nm); gos.append(go_); gbs.append(gb_)
            lk, uk = H.s_star(np.array(gos) / np.array(gbs), np.array(gbs), nu_); kn[nm] = None if (u0 or uk) else lk - ls0
        grp = {}
        for nm in KN_LIST:
            if kn.get(nm) is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        d1 = H.shift_to_s1(Dp, GBp)
        RES[pn] = dict(id=pn, z=zm, n=int(m.sum()), ls=ls0, no_root=u0, s=H.s_val(ls0, u0), q=qf, q_rooted=q, frac_mc_noroot=frn, median_D=float(np.median(Dp)), delta_floor=H.delta_floor(Dp),
                       bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, knobs=kn, recipe_half=half, delta_to_s1=d1, gas_to_star_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")), lever=H.lever1(Dp, GBp)[0],
                       median_dF=float(np.median(np.log10(GO[m] / (GB0[m] * NU(Y0[m]))))))
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        # B2 pooled
        l2, u2 = H.s_star(GO[m] / GB2[m], GB2[m]); RES[pn]["s_B2"] = H.s_val(l2, u2); RES[pn]["noroot_B2"] = u2
        P(f"  {pn:5s} (n {int(m.sum()):2d}, z_med {zm:.3f}): median D {np.median(Dp):.3f}  " + ("NO ROOT" if u0 else f"s* <= {10 ** ls0:.3g}") + f"; bootstrap 68 % [{10 ** qf[1]:.3g}, {10 ** qf[3]:.3g}] 95 % [{10 ** qf[0]:.3g}, {10 ** qf[4]:.3g}] (resamples without a root {frn:.2f}); baryon +-0.15 [{b15[0]:.3g}, {b15[1]:.3g}] +-0.30 [{b30[0]:.3g}, {b30[1]:.3g}]; "
          f"Delta_floor {np.log10(np.median(Dp)):+.3f}; gas_req {RES[pn]['gas_to_star_req']:+.2f}; median delta_FLAT {RES[pn]['median_dF']:+.3f}; B2 " + ("NO ROOT" if u2 else f"s* = {10 ** l2:.3g}") + f"; recipe half-width {half:.3f}")
    # M5: rebuilt V against the published M_dyn on the sigma0-detected rows
    det = ~S0LIM
    dM = LMD1[det] - LMD[det] if not MUTATE else LMD1[det] - (LMD[det] - math.log10(4.0))
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg273_stageB_results.json")))["numbers"]["rows"]
        def inv_nu(Dv):
            lo, hi = -25.0, 25.0
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if float(NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
                else: hi = mid
            return math.exp(0.5 * (lo + hi))
        bad = 0.0; nm_ = 0; n0 = sum(1 for i in ID if not main[str(int(i))]["no_root"])
        for i in ID:
            R_ = RES[str(int(i))]
            if not R_["no_root"]: nm_ += 1; bad = max(bad, abs(math.log10(R_["GB"] / inv_nu(R_["D"]) / A0C) - R_["ls"]))
        check("M2 MUTATE=1 (reactivity without needing a main-run root): every M_dyn x 4; rows with a root satisfy the closed-form inversion of their own (D, g_bar) to 1e-6 dex and their number is at least the main run's", f"rows with a root: mutated {nm_}, main {n0}; max |d log10 s*| against the independent inversion {bad:.1e}", bad < 1e-6 and nm_ >= n0)
    else:
        d1m = 0.0
        for i in ID:
            R_ = RES[str(int(i))]
            if R_["no_root"]: continue
            la, ua = H.AI.implied(np.array([R_["D"]]), np.array([R_["GB"]]), NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for i in ID if not RES[str(int(i))]['no_root'])} rows with a root)", d1m < 1e-9)
        ok3 = [RES[k]["n"] for k in ("PALL", "PDET", "Pz1", "Pz2", "Pz3", "P38")] == [41, 24, 21, 12, 8, 38] and RES["Pz1"]["n"] + RES["Pz2"]["n"] + RES["Pz3"]["n"] == 41
        check("M3 the pooled memberships are 41, 24, 21, 12, 8, 38 and the z bins partition PALL", f"{[RES[k]['n'] for k in ('PALL', 'PDET', 'Pz1', 'Pz2', 'Pz3', 'P38')]}", ok3 or SELFTEST, load_bearing=not SELFTEST)
        if not SELFTEST:
            check("M5 the rebuilt V = (v/sigma0) sigma0 with v_c^2 = V^2 + 3.36 sigma0^2 reproduces the published M_dyn on the 24 sigma0-detected rows to a median |Delta log M_dyn| <= 0.02 dex (CFG197 found +0.008)", f"median |d| {np.median(np.abs(dM)):.4f}, median signed {np.median(dM):+.4f}, max |d| {np.max(np.abs(dM)):.3f} (n {int(det.sum())})", float(np.median(np.abs(dM))) <= 0.02)
        else:
            tested = [str(int(i)) for k_, i in enumerate(ID) if not RES[str(int(i))]["ill"] and not RES[str(int(i))]["no_root"]]
            if tested:
                inside = sum(1 for t in tested if RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4])
                check("SELFTEST: the conditioned rows with a root return the fabricated truth (s = 2) inside their 95 % interval in at least 80 % of cases", f"{inside} of {len(tested)}", inside >= 0.8 * len(tested))
            else:
                P("  SELFTEST: no conditioned row with a root: truth recovery not applicable")
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot",
                              "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "gas_to_star_req", "s_B2", "noroot_B2", "sigma0_limit", "cristal08_candidate", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    nan = float("nan"); rows = []
    for lab in [str(int(i)) for i in ID] + list(POOL):
        R_ = RES[lab]; pooled = lab in POOL
        bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30); q = R_["q"]
        if pooled:
            lo68, hi68, lo95, hi95 = 10 ** q[1], 10 ** q[3], 10 ** q[0], 10 ** q[4]
        else:
            lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (FLOOR, FLOOR); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (FLOOR, FLOOR)
        fl = H.flags_for(R_["z"], lo95, hi95, b15[:2], b30[:2], not R_["no_root"]); half = R_["recipe_half"]
        if not pooled:
            sb_ = {float(k): (v["ls"], v["unb"]) for k, v in R_["star_bands"].items()}; si = H.band_edges(sb_, -0.15, 0.15); so = H.band_edges(sb_, -0.30, 0.30)
            extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], si[0], si[1], so[0], so[1], R_["delta_floor"], R_["delta_to_s1"], R_["gas_to_star_req"], R_["s_B2"], int(R_["noroot_B2"]), int(R_["s0lim"]), int(R_["c08"])]
            q_ = ("ILL-CONDITIONED (|lever| >= 10); " if R_["ill"] else "") + ("NO ROOT with stars-only baryons (a lower limit): robust against any added gas" if R_["no_root"] else "has a root with stars-only baryons: s* is an UPPER bound") + ("; sigma0 upper limit (M_dyn at face value)" if R_["s0lim"] else "") + ("; CRISTAL-08 z-candidate" if R_["c08"] else "") + ("; known low-M_dyn row" if R_["known_low"] else "")
            n_k = R_["n_knobs_with_root"]; gcl = "D (no gas; stars-only lower limit)"; objname = f"Danhaive JADES {lab}"
        else:
            extra = [nan, R_["lever"], 0, R_["median_dF"], nan, nan, R_["median_D"], R_["frac_mc_noroot"], nan, nan, nan, nan, R_["delta_floor"], R_["delta_to_s1"], R_["gas_to_star_req"], R_["s_B2"], int(R_["noroot_B2"]), "", ""]
            q_ = f"pooled row ({R_['n']} discs), stars-only lower limit: " + ("NO ROOT (median D <= 1)" if R_["no_root"] else "has a root: s* is an UPPER bound") + "; class D: no law statement"; n_k = ""; gcl = "D (pooled; no gas)"; objname = f"Danhaive pooled {lab}"
        rows.append(["CFG273", objname, gcl, f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(R_["no_root"]), f"{R_['s']:.6g}", f"{R_['s'] * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{R_['s'] * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{R_['s'] * 10 ** half:.6g}" if np.isfinite(half) else "nan", n_k,
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "baryons are a lower limit: s* is an upper bound", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg273_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg273_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg273{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg273{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
