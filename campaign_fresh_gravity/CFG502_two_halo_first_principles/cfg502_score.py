#!/usr/bin/env python3
"""CFG502 scoring (FROZEN_CRITERIA.md sections 3, 6, 7; cacadd50d). Every model + the SAME frozen environment term E; no free parameter.

Models (per lens group, CFG377 grouping):
  (i)   LCDM   : CFG495's per-group LCDM vector (cfg495_pred_tables.npz; spot-checked against cfg495_lenslib, C2)
  (ii)  LAW_RTA: the law to r_ta (CFG413 x = 1; CFG487 kids_vec, cfg100 r_ta_law)
  (iii) EDGE   : the 5.85 r_M edge with present baryons (CFG487 edge_only_E1)
  (iv)  V1     : the CFG487 V1 clock taper to r_ta (= CFG498 V1_cap; cap inert on KiDS)
  (v)   F_DD   : the CFG495 drawdown F_nodd + PROP (cfg495_pred_tables.npz)
  reported: F_NODD, LAW_X05 (CFG413's best)
E: cfg502_env_table.npz (W = 10 for stack P; W = 30 for f30; ALL for the ALL stack).
MUTATE (CFG502_MUTATE=1, outputs *_MUTATE.*): M1 E = 0; M2 f_W = 0 (two-halo kept).
Run: nice -n 15 python3 cfg502_score.py ; CFG502_MUTATE=1 nice -n 15 python3 cfg502_score.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import math, json, time
import numpy as np
from scipy import stats
from scipy.interpolate import RegularGridInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(LANES, "CFG487_settled_fraction_switch"))
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
sys.path.insert(0, os.path.join(LANES, "CFG495_drawdown_shell"))
import cfg487_lib as LB                                                      # noqa: E402  (read-only)
import cfg100_lib as C                                                       # noqa: E402  (read-only)
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only)

MUTATE = os.environ.get("CFG502_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
FOOTS = ("canonical", "alt")
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG, CHK = [], {}
RES = {"lane": "CFG502", "script": "cfg502_score", "mutate": MUTATE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2


def esd_full_loo(WG, WW, patch, mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)


def groups(z, Mgal, logMs):
    lmg = np.log10(Mgal)
    key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
    _, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
    gi = gi.ravel()
    return gi, 10 ** (np.bincount(gi, weights=lmg) / cnt), np.bincount(gi, weights=z) / cnt, np.bincount(gi, weights=logMs) / cnt, cnt


def pstack(tab, gi, WW, mask):
    NG = tab.shape[0]; out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


# ------------------------------------------------------------------ environment tables
ET = np.load(os.path.join(WORK, "cfg502_env_table.npz"))
LMS, ZG, RG = ET["LMS"], ET["ZG"], ET["RG"]
LRG = np.log(RG)


def env_vectors(key, GM, GZ, GS):
    """per-group 15-bin pair-averaged E [Msun/pc^2]."""
    tab = ET[key]
    if MUTATE and key != "E_ALL":
        tab = np.zeros_like(tab) if MODE == "M1" else ET["E_W10_f0"] if key == "E_W10" else tab
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    Eg = f(np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZG[0], ZG[-1])])            # (NG, nR)
    out = np.zeros((len(GM), 15))
    for g in range(len(GM)):
        out[g] = LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), GM[g])
    return out


# ------------------------------------------------------------------ data: stack P, f30, ALL
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
z = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float); logMs = lens["logM"].astype(float)
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
f30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
nL = len(z); ALLM = np.ones(nL, bool)
gi, GM, GZ, GS, cnt = groups(z, Mgal, logMs)
NG = len(GM)
T495 = np.load(os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg495_work", "cfg495_pred_tables.npz")))
assert np.array_equal(T495["gi"], gi) and np.allclose(T495["GS"], GS)
d, Cv = esd_full_loo(WG, WW, patch, ALLM); h15 = hart(15)
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
dref = np.array(J377["primary"]["esd"]); Rm = np.array(J377["primary"]["meanR"])
check("C1 stack P data vector = CFG377 primary", np.max(np.abs(d / dref - 1)) < 1e-10, f"max rel {np.max(np.abs(d / dref - 1)):.1e}")
INN = Rm <= 0.445; OUT = ~INN
P(f"stack P: {nL} lenses, {NG} groups; inner bins {INN.sum()} (R <= 0.445 Mpc), outer {OUT.sum()}")
TT = np.array([C._finish(lambda R: R ** -0.8 * 1e12, GM[g]) for g in range(NG)])    # CFG377 template (diagnostic)

# ------------------------------------------------------------------ own-profile tables
SC = LB.ShellClock(Om=C.OM)
RHO_M0_MPC = C.OM * C.RHOC0


def m_profile(rho_ratio, a_obs):
    return SC.m_of_rho(rho_ratio, a_obs, conservative=False)[0]


def kids_vec(Mg, zl, a0, rout, mfun=None):          # CFG487's function, unchanged
    r = np.geomspace(1e-4, rout, 1500)
    Md = Mg * (C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) - 1.0)
    if mfun is not None:
        mm = mfun(r)
        dM = np.diff(np.concatenate([[0.0], Md]))
        mmid = np.concatenate([[mm[0]], 0.5 * (mm[1:] + mm[:-1])])
        Md = np.cumsum(mmid * dM)
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)


OWN = {}
t = time.time()
for foot in FOOTS:
    a0 = C.A0[foot]
    rows = {k: np.zeros((NG, 15)) for k in ("LAW_RTA", "EDGE", "V1", "LAW_X05")}
    for g in range(NG):
        Mg, zl = GM[g], GZ[g]; ao = 1.0 / (1.0 + zl)
        rta = C.r_ta_law(Mg, a0, zl)
        re1 = float(LB.r_edge(Mg, C.G_MPC, a0))
        rho1 = lambda r: Mg * C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) / (4 * math.pi / 3 * r ** 3) / RHO_M0_MPC
        rows["LAW_RTA"][g] = kids_vec(Mg, zl, a0, rta)
        rows["LAW_X05"][g] = kids_vec(Mg, zl, a0, 0.5 * rta)
        rows["EDGE"][g] = kids_vec(Mg, zl, a0, re1)
        rows["V1"][g] = kids_vec(Mg, zl, a0, rta, lambda r: m_profile(rho1(r), ao))
    rows["LCDM"] = T495[f"{foot}_lcdm"]
    rows["F_DD"] = T495[f"{foot}_nodd"] + T495[f"{foot}_prop"]
    rows["F_NODD"] = T495[f"{foot}_nodd"]
    OWN[foot] = rows
    P(f"  own-profile tables [{foot}] ({time.time() - t:.0f} s)")
# C2 spot check of the LCDM table against cfg495_lenslib
rng = np.random.default_rng(502)
spot = rng.choice(NG, 60, replace=False)
dev = max(float(np.max(np.abs(LL.esd_vectors(GM[g], GZ[g], GS[g], "canonical")[0]["lcdm"] / OWN["canonical"]["LCDM"][g] - 1))) for g in spot)
check("C2a LCDM table = cfg495_lenslib on 60 random groups (1e-6)", dev < 1e-6, f"max rel {dev:.1e}")
J495 = json.load(open(os.path.join(LANES, "CFG495_drawdown_shell", "cfg495_test_results.json")))
lc = pstack(OWN["canonical"]["LCDM"], gi, WW, ALLM)
two495 = np.array(J495["canonical"]["vectors"]["two"])
dev2 = float(np.max(np.abs((lc + two495) / np.array(J495["canonical"]["vectors"]["LCDM"]) - 1)))
check("C2b stacked LCDM (+ CFG495's frozen 2h) = CFG495's committed LCDM vector (1e-6)", dev2 < 1e-6, f"max rel {dev2:.1e}")


def chi2_free(dv, C_, h, m, t):
    Ci = np.linalg.inv(C_); r = dv - m
    A = float((t @ Ci @ r) / (t @ Ci @ t)); rr = r - A * t
    return float(h * rr @ Ci @ rr), A


def chi2(dv, C_, h, m):
    r = dv - m; return float(h * r @ np.linalg.inv(C_) @ r)


tm = pstack(TT, gi, WW, ALLM)
J413 = json.load(open(os.path.join(LANES, "CFG413_on_radius_kids_vs_growth", "cfg413_kids_results.json")))
J487 = json.load(open(os.path.join(LANES, "CFG487_settled_fraction_switch", "cfg487_data_results.json")))
J498 = json.load(open(os.path.join(LANES, "CFG498_clock_taper_capped", "cfg498_data_results.json")))
refs = {"LAW_RTA": lambda f: J413["primary"][f]["1.0"]["free"]["chi2"], "EDGE": lambda f: J487["kids"][f]["rows"]["edge_only_E1"]["chi2"],
        "V1": lambda f: J498["kids"][f]["rows"]["V1_cap"]["chi2"], "F_DD": lambda f: J495[f]["sensitivity"]["free_R08_2h"]["F_dd"]["chi2"],
        "LAW_X05": lambda f: J413["primary"][f]["0.5"]["free"]["chi2"]}
dmax = 0.0; msg = []
for foot in FOOTS:
    for k, fn in refs.items():
        c_, _ = chi2_free(d, Cv, h15, pstack(OWN[foot][k], gi, WW, ALLM), tm)
        dmax = max(dmax, abs(c_ - fn(foot))); msg.append(f"{foot[:3]} {k} {c_:.3f}/{fn(foot):.3f}")
check("C2c own profiles reproduce the record's free-template chi2 (CFG413 x = 1 / 0.5, CFG487 edge, CFG498 V1, CFG495 F_dd) within 0.01",
      dmax <= 0.01, f"max |diff| {dmax:.4f}; " + "; ".join(msg))

# ------------------------------------------------------------------ scoring
MODELS = ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD")
REPORTED = ("F_NODD", "LAW_X05")


def score_sample(dv, C_, mask, Evec, own, label):
    h = hart(15); out = {}
    for k in MODELS + REPORTED:
        m = pstack(own[k], gi, WW, mask) + Evec
        c_ = chi2(dv, C_, h, m)
        ci = chi2(dv[INN], C_[np.ix_(INN, INN)], hart(int(INN.sum())), m[INN])
        co = chi2(dv[OUT], C_[np.ix_(OUT, OUT)], hart(int(OUT.sum())), m[OUT])
        cf, A = chi2_free(dv, C_, h, m, pstack(TT, gi, WW, mask))
        out[k] = dict(chi2=c_, p=float(stats.chi2.sf(c_, 15)), chi2_inner9=ci, chi2_outer6=co, chi2_plus_free_R08=cf, A_extra_R08=A,
                      model=m.tolist())
    return out


MODES = ["M1", "M2"] if MUTATE else ["MAIN"]
for MODE in MODES:
    P(f"\n=============== {MODE} ===============")
    E10 = pstack(env_vectors("E_W10", GM, GZ, GS), gi, WW, ALLM)
    P("  R [Mpc]    : " + " ".join(f"{x:6.3f}" for x in Rm))
    P("  data       : " + " ".join(f"{x:6.3f}" for x in d))
    P("  sigma      : " + " ".join(f"{x:6.3f}" for x in np.sqrt(np.diag(Cv))))
    P("  E (W = 10) : " + " ".join(f"{x:6.3f}" for x in E10))
    R_ = {"E_W10": E10.tolist(), "data": d.tolist(), "sigma": np.sqrt(np.diag(Cv)).tolist(), "R": Rm.tolist()}
    for foot in FOOTS:
        sc = score_sample(d, Cv, ALLM, E10, OWN[foot], "P")
        R_[foot] = sc
        P(f"\n  [{foot}] stack P, frozen E, 15 bins (Hartlap {h15:.4f}); no free parameter")
        P("    model    | chi2 /15    p        | inner9  outer6 | (+ free R^-0.8 on top: chi2, A_extra)")
        for k in MODELS + REPORTED:
            s = sc[k]
            P(f"    {k:8s} | {s['chi2']:8.2f}  {s['p']:.2e} | {s['chi2_inner9']:6.2f} {s['chi2_outer6']:7.2f} | {s['chi2_plus_free_R08']:7.2f} {s['A_extra_R08']:+.3f}"
              + ("   (reported)" if k in REPORTED else ""))
        P("    LCDM+E    : " + " ".join(f"{x:6.3f}" for x in sc["LCDM"]["model"]))
    RES[MODE] = R_

if not MUTATE:
    R_ = RES["MAIN"]
    # ---------------- nulls
    P("\n=============== NULLS (reported, frozen) ===============")
    d30, C30 = esd_full_loo(WG, WW, patch, f30)
    E30 = pstack(env_vectors("E_W30", GM, GZ, GS), gi, WW, f30)
    N1 = {}
    for foot in FOOTS:
        N1[foot] = {k: v for k, v in score_sample(d30, C30, f30, E30, OWN[foot], "f30").items()}
    P(f"  N1 f30 ({f30.sum()} lenses), E at W = 30: LCDM chi2 {N1['canonical']['LCDM']['chi2']:.2f} (p {N1['canonical']['LCDM']['p']:.2e}); "
      + "; ".join(f"{foot[:3]}: " + ", ".join(f"{k} {N1[foot][k]['chi2']:.1f}" for k in MODELS[1:]) for foot in FOOTS))
    P("    data f30 : " + " ".join(f"{x:6.3f}" for x in d30))
    P("    E W30    : " + " ".join(f"{x:6.3f}" for x in E30))
    P("    LCDM+E   : " + " ".join(f"{x:6.3f}" for x in N1["canonical"]["LCDM"]["model"]))
    R_["N1_f30"] = dict(n=int(f30.sum()), data=d30.tolist(), sigma=np.sqrt(np.diag(C30)).tolist(), E=E30.tolist(), scores=N1)
    # N2 ALL
    S = np.load(os.path.join(WORK, "cfg502_stage.npz"))
    zA, MA, lA, WGA, WWA, pA = S["z"], S["Mgal"], S["logM"], S["WG"], S["WW"], S["patch_all"]
    giA, GMA, GZA, GSA, cntA = groups(zA, MA, lA)
    t = time.time()
    lcA = np.array([LL.esd_vectors(GMA[g], GZA[g], GSA[g], "canonical")[0]["lcdm"] for g in range(len(GMA))])
    EA_g = env_vectors("E_ALL", GMA, GZA, GSA)
    mA = np.ones(len(zA), bool)
    dA, CA = esd_full_loo(WGA, WWA, pA, mA)

    def pst(tab):
        out = np.zeros(15)
        for k in range(15):
            w = np.bincount(giA, weights=WWA[:, k], minlength=len(GMA)); out[k] = (w @ tab[:, k]) / w.sum()
        return out
    EA = pst(EA_g); lcAv = pst(lcA)
    mod = lcAv + EA
    cA = chi2(dA, CA, hart(15), mod)
    RmA = (WWA * np.sqrt(C.G_MPC * MA[:, None] / np.sqrt(C.GEDGE_K[:-1] * C.GEDGE_K[1:])[None, :])).sum(0) / WWA.sum(0)
    INA = RmA <= 0.445
    cAi = chi2(dA[INA], CA[np.ix_(INA, INA)], hart(int(INA.sum())), mod[INA]); cAo = chi2(dA[~INA], CA[np.ix_(~INA, ~INA)], hart(int((~INA).sum())), mod[~INA])
    P(f"  N2 ALL ({len(zA)} lenses, {len(GMA)} groups; {time.time() - t:.0f} s): LCDM + E(ALL) chi2 {cA:.2f} / 15 (p {stats.chi2.sf(cA, 15):.2e}); "
      f"inner {cAi:.2f}, outer {cAo:.2f}")
    P("    R ALL    : " + " ".join(f"{x:6.3f}" for x in RmA))
    P("    data ALL : " + " ".join(f"{x:6.3f}" for x in dA))
    P("    sigma    : " + " ".join(f"{x:6.3f}" for x in np.sqrt(np.diag(CA))))
    P("    E ALL    : " + " ".join(f"{x:6.3f}" for x in EA))
    P("    LCDM+E   : " + " ".join(f"{x:6.3f}" for x in mod))
    R_["N2_ALL"] = dict(n=int(len(zA)), R=RmA.tolist(), data=dA.tolist(), sigma=np.sqrt(np.diag(CA)).tolist(), E=EA.tolist(),
                        LCDM_model=mod.tolist(), chi2=cA, p=float(stats.chi2.sf(cA, 15)), chi2_inner=cAi, chi2_outer=cAo)

    # ---------------- gate, verdicts, clash
    P("\n=============== VERDICT (frozen rule) ===============")
    envj = json.load(open(os.path.join(HERE, "cfg502_env_results.json")))
    pmj = json.load(open(os.path.join(HERE, "cfg502_pm_results.json"))) if os.path.exists(os.path.join(HERE, "cfg502_pm_results.json")) else {}
    labels = [x for x in (envj.get("label_contamination"), pmj.get("label_2h") if pmj else "2h NOT CROSS-CHECKED (PM not run)") if x]
    lc = R_["canonical"]["LCDM"]
    gate = lc["p"] > 0.01
    R_["gate"] = dict(LCDM_chi2=lc["chi2"], LCDM_p=lc["p"], passed=gate)
    P(f"  GATE: LCDM + E on stack P: chi2 {lc['chi2']:.2f} / 15, p {lc['p']:.2e} -> {'PASSED' if gate else 'MODEL STILL INADEQUATE'}")
    per = {}; clash = {}
    for foot in FOOTS:
        best = min(MODELS, key=lambda k: R_[foot][k]["chi2"])
        dE = R_[foot]["EDGE"]["chi2"] - R_[foot][best]["chi2"]
        clash[foot] = dict(best=best, chi2_best=R_[foot][best]["chi2"], d_edge=dE)
        per[foot] = {k: ("PASS" if R_[foot][k]["p"] > 0.01 else "FAIL") if gate else "NO VERDICT (gate failed)" for k in MODELS}
        P(f"  [{foot}] best of (i)-(v): {best} chi2 {R_[foot][best]['chi2']:.2f}; edge - best = {dE:+.2f}; per model: "
          + ", ".join(f"{k} {per[foot][k]}" for k in MODELS))
    if not gate:
        cv = "NOT DECIDED (MODEL STILL INADEQUATE: the frozen environment term does not let LCDM fit)"
    elif all(clash[f]["d_edge"] <= 4 for f in FOOTS):
        cv = "RESOLVED"
    elif all(clash[f]["d_edge"] >= 9 for f in FOOTS):
        cv = "CONFIRMED"
    else:
        cv = "OPEN"
    R_["per_model"] = per; R_["clash"] = clash; R_["clash_verdict"] = cv; R_["labels"] = labels
    P(f"  CLASH (5.85 r_M edge vs lensing): {cv}" + (f"  [labels: {'; '.join(labels)}]" if labels else ""))
else:
    # MUTATE checks
    P("\n=============== MUTATE checks ===============")
    m1 = RES["M1"]
    d1 = max(abs(m1[f]["LAW_RTA"]["chi2"] - J413["primary"][f]["1.0"]["none"]["chi2"]) for f in FOOTS)
    d1e = max(abs(m1[f]["EDGE"]["chi2"] - J487["kids"][f]["rows"]["edge_only_E1"]["chi2_no2h"]) for f in FOOTS)
    check("M1 E = 0: law-to-r_ta chi2 = CFG413 A = 0 (241.29 / 180.51) and edge = CFG487 edge_only_E1 no-2h, within 0.01",
          d1 <= 0.01 and d1e <= 0.01, f"law {m1['canonical']['LAW_RTA']['chi2']:.3f} / {m1['alt']['LAW_RTA']['chi2']:.3f} (max |d| {d1:.4f}); "
          f"edge {m1['canonical']['EDGE']['chi2']:.3f} / {m1['alt']['EDGE']['chi2']:.3f} (max |d| {d1e:.4f})")
    main = json.load(open(os.path.join(HERE, "cfg502_score_results.json")))["MAIN"]
    m2 = RES["M2"]
    dd = abs(m2["canonical"]["LCDM"]["chi2_outer6"] - main["canonical"]["LCDM"]["chi2_outer6"])
    check("M2 f_W = 0: the LCDM outer-6-bin chi2 changes by > 4", dd > 4,
          f"outer6 {main['canonical']['LCDM']['chi2_outer6']:.2f} -> {m2['canonical']['LCDM']['chi2_outer6']:.2f} (|d| {dd:.2f}); "
          f"full {main['canonical']['LCDM']['chi2']:.2f} -> {m2['canonical']['LCDM']['chi2']:.2f}")

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg502_score_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg502_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
