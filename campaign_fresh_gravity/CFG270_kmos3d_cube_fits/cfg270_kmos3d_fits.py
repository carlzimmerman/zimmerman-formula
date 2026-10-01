#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG270 -- implied-a0 upper bounds (or floor / ceiling markers) from the 192 KMOS3D cube fits (z 2.00-2.68): stars-only baryons (a lower limit), class D (no gas).

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG270_kmos3d_cube_fits/FROZEN_CRITERIA.md (b35c2f5c3).
  r         2.2 r_d = 1.31 RHALF (the radius of the fit's V_22); g_obs = (V_22^2 + 4.4 sigma0^2) / r (pressure-corrected); g_bar  B0 = stars only (H-band RHALF exponential disc), B2 = scaling gas (sensitivity).
  STAGE=A   the blind pre-flight: no velocity column is loaded; no g_obs, D, delta or s* is formed.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V_22 and sigma0 x 2); STAGE=B SELFTEST=1 (fabricated V_22 on the law at s = 2).
Run: STAGE=A python3 .../cfg270_kmos3d_fits.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv, contextlib, re
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

TSTART = time.time()                                                        # (not T0: that name is the all-rows tier mask below)
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
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: every V_22 and sigma0 x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V_22 on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
DA = os.path.join(REPO, "data_assembly")
FITP = os.path.join(DA, "kmos3d_cubes", "k3d_fits_main_final_flags.csv")
CATP = os.path.join(DA, "kmos3d_phibss", "kmos3d_catalog.csv")
RCP = os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")
SINS6 = os.path.join(DA, "highz_literature_tables", "sins_ao", "sins_ao_table6_kinematics.csv")
FLAGC = ["ID", "Z", "OBSBAND", "cat_SN", "quality", "inc_deg", "rd", "rhalf", "chi2r", "edge", "status", "badchi", "notes", "rt_lo", "Va_hi", "Va_lo", "rt_hi", "sig_lo", "sig_hi", "pos", "other"]
VELC = ["V22", "eV22", "sig0", "esig0"]
LOADVEL = (STAGE == "B") and not SELFTEST                                   # the SELFTEST never loads the real velocity columns
fit = pd.read_csv(FITP, usecols=FLAGC + (VELC if LOADVEL else []))
catc = ["ID", "ID_TARGETED", "FLAG_PRIMARYTARG", "FLAG_ADDGALDET", "FLAG_ZQUALITY", "RA", "DEC", "FIELD", "PSF_FWHM", "SFR", "LMSTAR", "RHALF", "Q"]
cat = pd.read_csv(CATP, usecols=catc)
M = fit.merge(cat, on="ID", how="left", suffixes=("", "_cat"))
N = len(M)
P(f"fits {os.path.basename(FITP)} sha256 {H.sha(FITP)}; catalogue {os.path.basename(CATP)} sha256 {H.sha(CATP)}; velocity columns loaded: {LOADVEL}; rows {N}")
ID = M["ID"].values
Z = M["Z"].values.astype(float)
LMS = M["LMSTAR"].values.astype(float); MS = 10 ** LMS
RH_AS = M["RHALF"].values.astype(float)
KPA = np.array([H.kpc_per_arcsec(z) for z in Z])
RE = RH_AS * KPA
RD = RE / 1.68
R = 2.2 * RD
INC = M["inc_deg"].values.astype(float)
PSF = M["PSF_FWHM"].values.astype(float)
RD_AS = M["rd"].values.astype(float)
hs = (M["quality"] == "highSN").values
i_ok = (INC >= 30) & (INC <= 80)
chi_ok = (M["chi2r"].values <= 3)
nohit = ~(M["Va_hi"].values | M["Va_lo"].values | M["rt_hi"].values | M["sig_lo"].values | M["sig_hi"].values | M["pos"].values)
T1 = hs & i_ok & chi_ok & nohit
T2 = T1 & (M["FLAG_ADDGALDET"].values == 0) & (2.2 * RD_AS >= PSF / 2)
T0 = np.ones(N, bool)
z1c = np.percentile(Z[T1], [100 / 3, 200 / 3])
TZ = {"PT1z1": T1 & (Z < z1c[0]), "PT1z2": T1 & (Z >= z1c[0]) & (Z < z1c[1]), "PT1z3": T1 & (Z >= z1c[1])}
# cross-matches (flags only)
rc = pd.read_csv(RCP, usecols=["name", "z"])                               # names and redshifts only (no RC100 kinematic column is read)
norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower())
rc_n = {norm(r["name"]): float(r["z"]) for _, r in rc.iterrows()}
RC_M = np.zeros(N, bool)
for k in range(N):
    for key in (norm(M["ID"].iloc[k]), norm(M["ID_TARGETED"].iloc[k])):
        if key in rc_n and abs(rc_n[key] - Z[k]) <= 0.01:
            RC_M[k] = True
SINS_MAP = {"GS4_33639": "K20-ID6", "GS4_29868": "K20-ID7", "GS4_40218": "GMASS-2303", "GS4_42930": "GMASS-2363", "COS4_08515": "ZC410041"}
SINS_M = np.isin(ID, list(SINS_MAP))                                       # RC100 flag = the frozen name recipe only (the data card's 22 also counts three matches made through SINS positions and one doubtful row, not reproducible by name)
TIERS = {"T1": T1, "T2": T2, "T0": T0}
P(f"tiers: T1 {int(T1.sum())}, T2 {int(T2.sum())}, T0 {N}; PT1 z terciles (cuts {z1c[0]:.3f}, {z1c[1]:.3f}): " + ", ".join(f"{k} {int(v.sum())}" for k, v in TZ.items()) + f"; RC100 matches {int(RC_M.sum())} (T1: {int((RC_M & T1).sum())}); SINS overlap {int(SINS_M.sum())}")


def mu_mol(z, logM):
    return 10 ** (0.06 - 3.3 * (np.log10(1 + z) - 0.65) ** 2 - 0.41 * (logM - 10.7))


def gbar(Ms, re, r, *, star_re=None, sph=False, gas=0.0):
    f = H.gsph if sph else H.gdisc
    sre = re if star_re is None else star_re
    return f(Ms, sre, r) + (f(Ms * gas, sre, r) if np.any(np.asarray(gas) > 0) else 0.0)


GB0 = np.array([float(gbar(MS[i], RE[i], R[i])) for i in range(N)])
MUV = mu_mol(Z, LMS)
GB2 = np.array([float(gbar(MS[i], RE[i], R[i], gas=MUV[i])) for i in range(N)])
Y0, Y2 = GB0 / A0C, GB2 / A0C
NUY0 = NU(Y0)

# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no velocity column is loaded; no g_obs, D, delta or s* is formed)")
    check("C1 CONTROL: 192 rows, one-to-one join, finite z / LMSTAR / RHALF / Q / PSF; T1 = 72 and T2 <= 69; z range 1.996-2.675", f"N {N}; T1 {int(T1.sum())}; T2 {int(T2.sum())}; z [{Z.min():.3f}, {Z.max():.3f}]; unique IDs {len(set(ID))}; rows with a catalogue match {int(np.isfinite(LMS).sum())}",
          N == 192 and len(set(ID)) == 192 and np.isfinite(np.c_[Z, LMS, RH_AS, PSF, M["Q"].values.astype(float)]).all() and int(T1.sum()) == 72 and int(T2.sum()) <= 69 and abs(Z.min() - 1.99577) < 1e-4 and abs(Z.max() - 2.67543) < 1e-4)
    yy = np.linspace(0.05, 40, 400000); hh = H.i0e(yy) * H.k0e(yy) - H.i1e(yy) * H.k1e(yy); peak = float(np.max(2 * yy ** 2 * hh)); farr = float(H.gdisc(1e11, 3.0, 150.0) / (H.G_KPC * 1e11 / 150.0 ** 2 * H.G2SI))
    src29 = open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score.py")).read(); seg = src29[src29.index("def disc_v2"):src29.index("P(__doc__")]
    ns29 = {"G_KPC": H.G_KPC, "XN": H.XN, "G2SI": H.G2SI, "i0e": H.i0e, "i1e": H.i1e, "k0e": H.k0e, "k1e": H.k1e, "math": math, "np": np}; exec(compile(seg, "cfg229_score.py", "exec"), ns29)
    rr_ = np.random.default_rng(1234); dmax = 0.0
    for _ in range(200):
        M_, Re_, Rr_ = 10 ** rr_.uniform(9, 12.5), rr_.uniform(0.5, 8), rr_.uniform(1, 20); dmax = max(dmax, abs(H.gdisc(M_, Re_, Rr_) / ns29["gdisc"](M_, Re_, Rr_) - 1))
    check("C2 CONTROL: Freeman's peak V^2 = 0.3872 G M / R_d to 0.003, g -> G M / r^2 far from a compact mass to 1e-3, and gdisc equals CFG229's on 200 random inputs to 1e-12", f"peak {peak:.4f}; far-field ratio {farr:.5f}; max deviation {dmax:.1e}", abs(peak / 0.3872 - 1) < 0.003 and abs(farr - 1) < 1e-3 and dmax < 1e-12)
    cnt = {c: int(M[c].sum()) for c in ("edge", "rt_lo", "Va_hi", "Va_lo", "rt_hi", "sig_lo", "sig_hi", "pos", "badchi")}
    check("C3 CONTROL (counts): the data chat's flag counts: edge 128, r_t lower 68, V_a upper 25, V_a lower 1, r_t upper 21, sigma0 lower 14, upper 3, position 12, badchi 4, highSN 120", f"{cnt}; highSN {int(hs.sum())}",
          cnt == dict(edge=128, rt_lo=68, Va_hi=25, Va_lo=1, rt_hi=21, sig_lo=14, sig_hi=3, pos=12, badchi=4) and int(hs.sum()) == 120)
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
    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; B0 = stars only at r = 2.2 r_d; ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    LEV, ILL = np.zeros(N), np.zeros(N, bool)
    for i in range(N):
        lv, fl = H.lever1(np.array([NUY0[i]]), np.array([GB0[i]])); LEV[i] = lv; ILL[i] = bool(fl or abs(lv) >= 10)
    for nm, m in (("T0", T0), ("T1", T1), ("T2", T2), ("PT1z1", TZ["PT1z1"]), ("PT1z2", TZ["PT1z2"]), ("PT1z3", TZ["PT1z3"])):
        P(f"    {nm}: n {int(m.sum())}, y(B0) 16/50/84 % {np.percentile(Y0[m], 16):.2f} / {np.median(Y0[m]):.2f} / {np.percentile(Y0[m], 84):.2f} (min {Y0[m].min():.2f}, max {Y0[m].max():.2f}); y(B2) median {np.median(Y2[m]):.2f}; "
          f"rows y < 0.3: {int((Y0[m] < 0.3).sum())}, y > 6: {int((Y0[m] > 6).sum())}, y > 8: {int((Y0[m] > 8).sum())}; ILL-CONDITIONED {int(ILL[m].sum())} ({100 * ILL[m].mean():.0f} %); T4 floor 3 sigma/sqrt(N) at sigma = 0.2 dex {3 * 0.2 / math.sqrt(m.sum()):.3f} dex")
    P(f"    PSF ratio 2.2 r_d / (PSF/2): T1 median {np.median((2.2 * RD_AS / (PSF / 2))[T1]):.2f}; rows with 2.2 r_d < PSF/2: T0 {int((2.2 * RD_AS < PSF / 2).sum())}, T1 {int((2.2 * RD_AS < PSF / 2)[T1].sum())} ({100 * (2.2 * RD_AS < PSF / 2)[T1].mean():.0f} %)")
    P(f"    RC100 overlap by the frozen name recipe: {int(RC_M.sum())} rows (T1: {int((RC_M & T1).sum())}; the data card's 22 also counts three matches made through SINS positions and one doubtful row, which the name recipe does not reproduce); SINS overlap by name: {int(SINS_M.sum())} rows (T1: {int((SINS_M & T1).sum())}, ids {[str(i) for i in ID[SINS_M]]})")
    P(f"    median log M* T1 {np.median(LMS[T1]):.2f}, r_d (kpc) median {np.median(RD[T1]):.2f}, r median {np.median(R[T1]):.2f} kpc; RC100 rows inside T1: {[str(i) for i in ID[RC_M & T1]]}")
    P("\nC6  COVERAGE (noiseless world on each row's B0 baryons; declared 0.15 dex on g_obs; declared 0.20 dex on M*; 100 mock datasets, B = 1,000; T1 rows only)")
    rng6 = np.random.default_rng(270); idx1 = np.where(T1)[0]; cv68 = np.zeros(len(idx1)); cv95 = np.zeros(len(idx1)); nd = np.zeros(len(idx1))
    for jj, i in enumerate(idx1):
        gob_true = GB0[i] * float(NU(np.array([Y0[i]]))[0])
        for it in range(100):
            Ms_o = MS[i] * 10 ** rng6.normal(0, 0.20); god = gob_true * 10 ** rng6.normal(0, 0.15); gobm = god * 10 ** rng6.normal(0, 0.15, 1000)
            Msd = Ms_o * 10 ** rng6.normal(0, 0.20, 1000); gbd = H.gdisc(Msd, RE[i], R[i])
            lsd, ud = H.AI.implied((gobm / gbd)[:, None], gbd[:, None], NU, A0C); q, fr = H.rooted_pct(lsd, ud)
            if np.isfinite(q[0]): nd[jj] += 1; cv68[jj] += (q[1] <= 0.0 <= q[3]); cv95[jj] += (q[0] <= 0.0 <= q[4])
    cv68, cv95 = cv68 / np.maximum(nd, 1), cv95 / np.maximum(nd, 1); ci = ~ILL[idx1]
    P(f"    T1 coverage 68 %: median {np.median(cv68):.2f} (conditioned rows {np.median(cv68[ci]):.2f}); 95 %: median {np.median(cv95):.2f} (conditioned {np.median(cv95[ci]):.2f})")
    check("C6 (reported; load-bearing for the conditioned rows): the median coverage of the conditioned T1 rows is >= 60 % (68 %) and >= 88 % (95 %)", f"conditioned T1 rows {int(ci.sum())}: 68 % {np.median(cv68[ci]):.2f}, 95 % {np.median(cv95[ci]):.2f}", bool(np.median(cv68[ci]) >= 0.60 and np.median(cv95[ci]) >= 0.88), load_bearing=False)
    P("\nA3  KNOB EFFECTS ON g_bar (dex relative to B0; T1 median / min / max)")
    kb = {"R_e x1.5": np.array([gbar(MS[i], RE[i], R[i], star_re=1.5 * RE[i]) for i in range(N)]), "R_e /1.5": np.array([gbar(MS[i], RE[i], R[i], star_re=RE[i] / 1.5) for i in range(N)]), "spherical": np.array([gbar(MS[i], RE[i], R[i], sph=True) for i in range(N)])}
    for k, v in kb.items():
        dd = np.log10(v / GB0)[T1]; P(f"    {k}: median {np.median(dd):+.3f}, min {dd.min():+.3f}, max {dd.max():+.3f}")
    P(f"    mu_mol (T1) median {np.median(MUV[T1]):.2f}, B2/B0 g_bar median {np.median((GB2 / GB0)[T1]):.2f}")
    pfd1 = all(ok for n, ok, lb in CHK if lb and not n.startswith("C6"))
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C5)")
    P(f"  PF-D2 ILL-CONDITIONED rows: T0 {int(ILL.sum())} of {N}, T1 {int(ILL[T1].sum())} of {int(T1.sum())}, T2 {int(ILL[T2].sum())} of {int(T2.sum())}")
    P(f"  PF-D3 DRAWABLE as an upper bound: T1 {int(((~ILL) & T1 & pfd1).sum())} of {int(T1.sum())} rows (every drawable row is an upper bound on s*, never a measurement)")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored (HE3-HE7 are scored at stage B):")
    he = {}
    he["HE1"] = int(T1.sum()) == 72 and 40 <= int(T2.sum()) <= 69 and 0.5 <= float(np.median(Y0[T1])) <= 3.0 and float((~ILL[T1]).mean()) >= 0.85
    he["HE2"] = float((2.2 * RD_AS < PSF / 2)[T1].mean()) <= 0.20
    for k, v in he.items(): P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(tiers={k: int(v.sum()) for k, v in {**TIERS, **TZ}.items()}, counts=cnt, rc100=int(RC_M.sum()), sins=int(SINS_M.sum()), hand_estimates=he, pf=dict(PF_D1=bool(pfd1), n_ill_T1=int(ILL[T1].sum())),
               y0=Y0.tolist(), y2=Y2.tolist(), lever=LEV.tolist(), ill=ILL.tolist(), cov68=cv68.tolist(), cov95=cv95.tolist())

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V_22 and sigma0 x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2700)
    if SELFTEST:
        gob = GB0 * NU(GB0 / (2.0 * A0C)) * 10 ** rngS.normal(0, 0.15, N)
        V22 = np.sqrt(gob * R / H.G2SI); EV22 = 0.10 * V22; SIG = np.zeros(N); ESIG = np.zeros(N)
        P("SELFTEST: V_22 fabricated from the law at s_true = 2 on each row's B0 baryons (+0.15 dex scatter), sigma0 = 0; the real velocity columns are not even loaded")
    else:
        V22 = M["V22"].values.astype(float); EV22 = M["eV22"].values.astype(float); SIG = M["sig0"].values.astype(float); ESIG = M["esig0"].values.astype(float)
    if MUTATE:
        V22 = 2.0 * V22; EV22 = 2.0 * EV22; SIG = 2.0 * SIG; ESIG = 2.0 * ESIG
    EV22 = np.where(np.isfinite(EV22), EV22, np.nanmedian(EV22)); ESIG = np.where(np.isfinite(ESIG), ESIG, np.nanmedian(ESIG)); SIG = np.where(np.isfinite(SIG), SIG, 0.0)
    A_P = 2.0 * (R / RD)                                                   # the exponential-disc asymmetric-drift coefficient 2 r/r_d (= 4.4 at r = 2.2 r_d)

    def gobs(i, vm="head", inc=0.0, V=None, S=None):
        Vv = V22[i] if V is None else V; Ss = SIG[i] if S is None else S
        V2 = {"head": Vv ** 2 + A_P[i] * Ss ** 2, "rot": Vv ** 2, "sins": Vv ** 2 + 3.36 * Ss ** 2}[vm]
        fac = 1.0 if inc == 0.0 else (math.sin(math.radians(INC[i])) / math.sin(math.radians(min(max(INC[i] + inc, 5.0), 89.9)))) ** 2
        return V2 * fac / R[i] * H.G2SI

    GO = np.array([gobs(i) for i in range(N)]); GO_ROT = np.array([gobs(i, "rot") for i in range(N)])
    DD = GO / GB0
    RES = {}
    KN_LIST = ["pressure: rotation only", "pressure: +3.36 sigma0^2", "inclination -5 deg", "inclination +5 deg", "R_e x1.5", "R_e /1.5", "spherical", "kernel P2"]
    KGR = {"pressure: rotation only": "pressure", "pressure: +3.36 sigma0^2": "pressure", "inclination -5 deg": "inclination", "inclination +5 deg": "inclination", "R_e x1.5": "geometry", "R_e /1.5": "geometry", "spherical": "geometry", "kernel P2": "kernel"}

    def variant(i, nm):
        if nm == "pressure: rotation only": return gobs(i, "rot"), GB0[i], NU
        if nm == "pressure: +3.36 sigma0^2": return gobs(i, "sins"), GB0[i], NU
        if nm == "inclination -5 deg": return gobs(i, inc=-5.0), GB0[i], NU
        if nm == "inclination +5 deg": return gobs(i, inc=+5.0), GB0[i], NU
        if nm == "R_e x1.5": return GO[i], float(gbar(MS[i], RE[i], R[i], star_re=1.5 * RE[i])), NU
        if nm == "R_e /1.5": return GO[i], float(gbar(MS[i], RE[i], R[i], star_re=RE[i] / 1.5)), NU
        if nm == "spherical": return GO[i], float(gbar(MS[i], RE[i], R[i], sph=True)), NU
        if nm == "kernel P2": return GO[i], GB0[i], NUP2

    for i in range(N):
        lab = str(ID[i])
        ls0, st0 = H.s_status(np.array([DD[i]]), np.array([GB0[i]]))
        ls2, st2 = H.s_status(np.array([GO[i] / GB2[i]]), np.array([GB2[i]]))
        rng = np.random.default_rng(zlib.crc32(("270|" + lab).encode()) % 100000)
        Vd = V22[i] + EV22[i] * rng.normal(size=B_MC); Sd = np.maximum(SIG[i] + ESIG[i] * rng.normal(size=B_MC), 0.0)
        god = (Vd ** 2 + A_P[i] * Sd ** 2) / R[i] * H.G2SI; Msd = MS[i] * 10 ** rng.normal(0, 0.20, B_MC); gbd = H.gdisc(Msd, RE[i], R[i])
        lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud); frc = float(np.mean(ud & ((god / gbd) > 1.0)))   # frc: draws whose own D > 1 but s* is above the bracket (CEILING draws)
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        dF0 = float(np.log10(GO[i] / (GB0[i] * float(NU(np.array([Y0[i]]))[0]))))
        bands = H.band_solutions(np.array([DD[i]]), np.array([GB0[i]]))
        star_b = {s_: H.s_star(np.array([GO[i] / (GB0[i] * 10 ** s_)]), np.array([GB0[i] * 10 ** s_])) for s_ in (-0.30, -0.15, 0.15, 0.30)}
        kn = {}
        for nm in KN_LIST:
            go_, gb_, nu_ = variant(i, nm); lk, uk = H.s_star(np.array([go_ / gb_]), np.array([gb_]), nu_)
            kn[nm] = None if (st0 != "root" or uk) else lk - ls0; kn[nm + "|root"] = (not uk)
        grp = {}
        for nm in KN_LIST:
            if kn[nm] is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        n_root = sum(1 for nm in KN_LIST if kn[nm + "|root"])
        lv_nl, lf_nl = H.lever1(np.array([NUY0[i]]), np.array([GB0[i]])); d1 = H.shift_to_s1(np.array([DD[i]]), np.array([GB0[i]]))
        RES[lab] = dict(id=lab, z=float(Z[i]), n=1, logMs=float(LMS[i]), r_kpc=float(R[i]), GO=float(GO[i]), GO_rot=float(GO_ROT[i]), GB=float(GB0[i]), D=float(DD[i]), y=float(Y0[i]), ls=ls0, status=st0, no_root=(st0 == "floor"), s=H.s_val_status(ls0, st0),
                        q=q, frac_mc_noroot=frn, frac_mc_ceiling=frc, delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], status_B2=st2, s_B2=H.s_val_status(ls2, st2), D_B2=float(GO[i] / GB2[i]),
                        bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, star_bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in star_b.items()},
                        knobs=kn, recipe_half=half, n_knobs_with_root=n_root, lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=H.delta_floor(np.array([DD[i]])), delta_to_s1=d1,
                        gas_to_star_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")), tier=("T1" if T1[i] else "T0"), t2=bool(T2[i]), rc100=bool(RC_M[i]), sins=bool(SINS_M[i]), edge=bool(M["edge"].iloc[i]))
    P(f"  per-galaxy rows computed ({time.time() - TSTART:.0f} s); status counts: " + ", ".join(f"{s}: {sum(1 for k in RES if RES[k]['status'] == s)}" for s in ("root", "floor", "ceiling")) + "; T1: " + ", ".join(f"{s}: {sum(1 for i in range(N) if T1[i] and RES[str(ID[i])]['status'] == s)}" for s in ("root", "floor", "ceiling")))
    # a short per-row listing for T1
    P("  T1 rows: id, z, log M*, r (kpc), g_obs/g_bar = D, delta_FLAT, y, status and bound (B0 = stars only) | B2 (scaling gas) status and s*")
    for i in np.where(T1)[0]:
        R_ = RES[str(ID[i])]
        b0 = (f"s* <= {10 ** R_['ls']:.3g}" if R_["status"] == "root" else ("FLOOR (D <= 1)" if R_["status"] == "floor" else "CEILING (s* > 1000)"))
        b2 = (f"s* = {R_['s_B2']:.3g}" if R_["status_B2"] == "root" else R_["status_B2"].upper())
        P(f"    {ID[i]:>11s} z {Z[i]:.2f} M* {LMS[i]:.2f} r {R[i]:5.2f} D {DD[i]:7.3f} dF {R_['delta_FLAT']:+.3f} y {Y0[i]:5.2f}  {b0:22s} | B2 {b2}" + (" RC100" if RC_M[i] else "") + (" SINS" if SINS_M[i] else "") + (" ILL" if R_["ill"] else "") + (" EDGE" if R_["edge"] else ""))
    # pooled rows
    POOL = {"PT1": T1, "PT2": T2, "PT0": T0, **TZ, "PT1_RC100": T1 & RC_M}
    for pn, m in POOL.items():
        Dp, GBp = DD[m], GB0[m]; zm = float(np.median(Z[m])); n_m = int(m.sum())
        ls0, st0 = H.s_status(Dp, GBp); rng = np.random.default_rng(zlib.crc32(("270|" + pn).encode()) % 100000)
        ib = rng.integers(0, n_m, size=(B_MC, n_m)); lsb, ub = H.AI.implied(Dp[ib], GBp[ib], NU, A0C); q, frn = H.rooted_pct(lsb, ub); qf = [float(v) for v in np.percentile(lsb, [2.5, 16, 50, 84, 97.5])]
        frc = float(np.mean(ub & (np.median(Dp[ib], axis=1) > 1.0)))
        bands = H.band_solutions(Dp, GBp); kn = {}
        for nm in KN_LIST:
            gos, gbs, nu_ = [], [], NU
            for i in np.where(m)[0]:
                go_, gb_, nu_ = variant(i, nm); gos.append(go_); gbs.append(gb_)
            lk, uk = H.s_star(np.array(gos) / np.array(gbs), np.array(gbs), nu_); kn[nm] = None if (st0 != "root" or uk) else lk - ls0
        grp = {}
        for nm in KN_LIST:
            if kn.get(nm) is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        d1 = H.shift_to_s1(Dp, GBp); l2, st2 = H.s_status(GO[m] / GB2[m], GB2[m])
        RES[pn] = dict(id=pn, z=zm, n=n_m, ls=ls0, status=st0, no_root=(st0 == "floor"), s=H.s_val_status(ls0, st0), q=qf, q_rooted=q, frac_mc_noroot=frn, frac_mc_ceiling=frc, median_D=float(np.median(Dp)), delta_floor=H.delta_floor(Dp),
                       bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, knobs=kn, recipe_half=half, delta_to_s1=d1, gas_to_star_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")), lever=H.lever1(Dp, GBp)[0],
                       median_dF=float(np.median(np.log10(GO[m] / (GB0[m] * NU(Y0[m]))))), status_B2=st2, s_B2=H.s_val_status(l2, st2))
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        P(f"  {pn:10s} (n {n_m:3d}, z_med {zm:.3f}): median D {np.median(Dp):.3f}  {st0.upper()}" + (f" s* <= {10 ** ls0:.3g}" if st0 == "root" else "") + f"; bootstrap 68 % [{10 ** qf[1]:.3g}, {10 ** qf[3]:.3g}] 95 % [{10 ** qf[0]:.3g}, {10 ** qf[4]:.3g}]; baryon +-0.15 [{b15[0]:.3g}, {b15[1]:.3g}] +-0.30 [{b30[0]:.3g}, {b30[1]:.3g}]; "
          f"Delta_floor {np.log10(np.median(Dp)):+.3f}; gas_req {RES[pn]['gas_to_star_req']:+.2f}; median delta_FLAT {RES[pn]['median_dF']:+.3f}; B2 {st2}" + (f" s* = {10 ** l2:.3g}" if st2 == "root" else "") + f"; recipe half-width {half:.3f}")
    P("\n  rotation-only (no pressure) pooled PT1: median D(rot) = %.3f vs headline %.3f; median log10(g_obs,head/g_obs,rot) over T1 = %+.3f dex" % (np.median((GO_ROT / GB0)[T1]), np.median(DD[T1]), np.median(np.log10(GO / GO_ROT)[T1])))
    NUM["rows"] = RES
    NUM["T1_stats"] = dict(n=int(T1.sum()), median_D=float(np.median(DD[T1])), floor_frac=float(np.mean([RES[str(ID[i])]["status"] == "floor" for i in np.where(T1)[0]])), median_pressure_dex=float(np.median(np.log10(GO / GO_ROT)[T1])))
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg270_stageB_results.json")))["numbers"]["rows"]
        def inv_nu(Dv):
            lo, hi = -25.0, 25.0
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if float(NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
                else: hi = mid
            return math.exp(0.5 * (lo + hi))
        bad = 0.0; nroot = 0
        for i in range(N):
            R_ = RES[str(ID[i])]
            if R_["status"] == "root": nroot += 1; bad = max(bad, abs(math.log10(R_["GB"] / inv_nu(R_["D"]) / A0C) - R_["ls"]))
        n_gt1_m = int(sum(1 for i in range(N) if RES[str(ID[i])]["D"] > 1)); n_gt1_0 = int(sum(1 for i in range(N) if main[str(ID[i])]["D"] > 1))
        check("M2 MUTATE=1 (reactivity; the count is of rows with D > 1, not of roots, because of the solver bracket): every V_22 and sigma0 x 2; rows with status ROOT satisfy the closed-form inversion of their own (D, g_bar) to 1e-6 dex and the number of rows with D > 1 is at least the main run's",
              f"rows with D > 1: mutated {n_gt1_m}, main {n_gt1_0}; rows with a root {nroot}; max |d log10 s*| against the independent inversion {bad:.1e}", bad < 1e-6 and n_gt1_m >= n_gt1_0)
    else:
        d1m = 0.0
        for i in range(N):
            R_ = RES[str(ID[i])]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array([R_["D"]]), np.array([R_["GB"]]), NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for i in range(N) if RES[str(ID[i])]['status'] == 'root')} galaxy rows with a root)", d1m < 1e-9)
        ok3 = RES["PT1"]["n"] == 72 and RES["PT0"]["n"] == 192 and RES["PT2"]["n"] <= 69 and sum(RES[k]["n"] for k in TZ) == 72
        check("M3 the tier memberships (PT1 72, PT0 192, PT2 <= 69) and the z terciles partition PT1", f"PT1 {RES['PT1']['n']}, PT2 {RES['PT2']['n']}, PT0 {RES['PT0']['n']}, terciles {[RES[k]['n'] for k in TZ]}, RC100 in T1 {RES['PT1_RC100']['n']}", ok3 or SELFTEST, load_bearing=not SELFTEST)
        if not SELFTEST:
            s6 = pd.read_csv(SINS6).set_index("source"); rat = {}
            for kid, nm in SINS_MAP.items():
                i = int(np.where(ID == kid)[0][0]); rat[kid] = float(V22[i]) / float(s6.loc[nm, "Vrot_kms"])
            n_ok = sum(1 for v in rat.values() if abs(v - 1) <= 0.30 + 1e-9); NUM["M5_ratios"] = rat
            check("M5 the five SINS-overlap galaxies' fitted V_22 against the published SINS V_rot within 30 % for at least 4 of 5 (the data chat's C1 reported 5 of 5; reproduction, not a blind test)", "; ".join(f"{k} {v:.2f}" for k, v in rat.items()) + f"; within 30 %: {n_ok} of 5", n_ok >= 4)
        else:
            tested = [str(ID[i]) for i in np.where(T0)[0] if RES[str(ID[i])]["status"] == "root" and not RES[str(ID[i])]["ill"]]
            if tested:
                inside = sum(1 for t in tested if RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4])
                check("SELFTEST: the conditioned rows with a root return the fabricated truth (s = 2) inside their 95 % interval in at least 80 % of cases", f"{inside} of {len(tested)}", inside >= 0.8 * len(tested))
            else: P("  SELFTEST: no conditioned row with a root: truth recovery not applicable")
    if not (MUTATE or SELFTEST):
        P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9; HE1, HE2 were scored at stage A) scored:")
        i1 = np.where(T1)[0]; p1 = RES["PT1"]; m5ok = bool([ok for n_, ok, lb in CHK if n_.startswith("M5")][0])
        he = {"HE3": bool(np.median(DD[T1]) > 2.0 and np.mean(DD[T1] <= 1.0) >= 0.10),
              "HE4": bool(p1["status"] == "root" and p1["s"] >= 1.0 and not any(RES[str(ID[i])]["status"] == "ceiling" for i in i1 if Y0[i] > 1.0)),
              "HE5": bool(np.log10(np.median(GO[T1]) / np.median(GO_ROT[T1])) >= 0.1),
              "HE6": bool(p1["status_B2"] != "root" or p1["s_B2"] <= p1["s"] / 3.0), "HE7": m5ok}
        P(f"    HE3: median D(B0) of T1 {np.median(DD[T1]):.3f} (needs > 2), T1 rows at D <= 1 {int((DD[T1] <= 1).sum())} of {int(T1.sum())} = {100 * np.mean(DD[T1] <= 1):.0f} % (needs >= 10 %): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
        P(f"    HE4: PT1 {p1['status']}, s* {'<= ' + format(p1['s'], '.3g') if p1['status'] == 'root' else p1['status']} (needs a root >= 1); CEILING rows among T1 with y > 1: {sum(1 for i in i1 if Y0[i] > 1.0 and RES[str(ID[i])]['status'] == 'ceiling')} (needs 0): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: log10 [median g_obs(headline) / median g_obs(rotation only)] over T1 = {np.log10(np.median(GO[T1]) / np.median(GO_ROT[T1])):+.3f} (needs >= 0.1; median of the per-row ratios {np.median(np.log10(GO / GO_ROT)[T1]):+.3f}): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: PT1 with B2: {p1['status_B2']}" + (f", s* = {p1['s_B2']:.3g} against the B0 bound {p1['s']:.3g}" if p1["status_B2"] == "root" else "") + f": {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        P(f"    HE7: M5 {'holds' if m5ok else 'fails'}: {'hit' if he['HE7'] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates_B"] = he
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling",
                              "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "gas_to_star_req", "s_B2", "status_B2", "status", "tier", "t2", "rc100_match", "sins_match", "edge", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    nan = float("nan"); rows = []
    keys = [str(i) for i in ID] + list(POOL)
    for lab in keys:
        R_ = RES[lab]; pooled = lab in POOL
        bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30); q = R_["q"]; st = R_["status"]
        if pooled: lo68, hi68, lo95, hi95 = 10 ** q[1], 10 ** q[3], 10 ** q[0], 10 ** q[4]
        else:
            empty = 1000.0 if st == "ceiling" else FLOOR                      # no draw with a root: a CEILING row's interval sits at the bracket's top, a FLOOR row's at the floor
            lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(R_["z"], lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]
        if not pooled:
            sb_ = {float(k): (v["ls"], v["unb"]) for k, v in R_["star_bands"].items()}; si = H.band_edges(sb_, -0.15, 0.15); so = H.band_edges(sb_, -0.30, 0.30)
            extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], si[0], si[1], so[0], so[1], R_["delta_floor"], R_["delta_to_s1"], R_["gas_to_star_req"], R_["s_B2"], R_["status_B2"], st, R_["tier"], int(R_["t2"]), int(R_["rc100"]), int(R_["sins"]), int(R_["edge"])]
            q_ = ("ILL-CONDITIONED; " if R_["ill"] else "") + {"root": "has a root with stars-only baryons: s* is an UPPER bound", "floor": "FLOOR: no root, D <= 1 (stars alone exceed the dynamics): robust against any added gas", "ceiling": f"CEILING: D = {R_['D']:.1f} > 1 but s* > 1000: vacuous upper bound, NOT a floor"}[st] + ("; edge fit" if R_["edge"] else "")
            n_k = R_["n_knobs_with_root"]; objname = f"KMOS3D {lab}"; gcl = "D (no gas; stars-only lower limit)"
        else:
            extra = [nan, R_["lever"], 0, R_["median_dF"], nan, nan, R_["median_D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], nan, nan, nan, nan, R_["delta_floor"], R_["delta_to_s1"], R_["gas_to_star_req"], R_["s_B2"], R_["status_B2"], st, "pooled", "", "", "", ""]
            q_ = f"pooled row ({R_['n']} fits), stars-only lower limit: " + {"root": "has a root: s* is an UPPER bound", "floor": "FLOOR (median D <= 1)", "ceiling": "CEILING (median D > 1, s* > 1000)"}[st] + "; class D: no law statement"; n_k = ""; objname = f"KMOS3D pooled {lab}"; gcl = "D (pooled; no gas)"
        sstar = R_["s"]
        rows.append(["CFG270", objname, gcl, f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", n_k,
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "baryons are a lower limit: s* is an upper bound", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg270_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg270_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg270{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg270{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
