#!/usr/bin/env python3
"""CFG503 scoring (FROZEN_CRITERIA.md sections 4-7; f56e146a1). Data handling, grouping, stacking and the five models copied from
CFG502's cfg502_score.py (not edited). Every model + the SAME frozen environment term E; stripping by the same r_t rule for every model.

PRIMARY: E with halofit xi_NL x Tinker+05 zeta (mode nlz), leaked satellites' own profiles stripped at the Jacobi radius, Moster+13,
         chi2 with the SHMR difference (Behroozi+13 - Moster+13) as a rank-one covariance term: r^T (C / h + d d^T)^-1 r.
Gates: G1 LCDM stack P p > 0.01; G2 LCDM f30 p > 0.01; G3 LCDM ALL p > 0.001.
MUTATE (CFG503_MUTATE=1, outputs *_MUTATE.*): M0 all upgrades off (CFG502 path) must reproduce CFG502; MH halofit off (CAMB linear);
MS stripping off (inner bins must move).
Inputs: _external_data/cfg503_work/cfg503_env_table.npz, cfg503_own_tables.npz (cfg503_env.py, cfg503_own.py).
Run: nice -n 15 python3 cfg503_score.py ; CFG503_MUTATE=1 nice -n 15 python3 cfg503_score.py
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
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
sys.path.insert(0, os.path.join(LANES, "CFG495_drawdown_shell"))
import cfg100_lib as C                                                       # noqa: E402  (read-only)
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only)

MUTATE = os.environ.get("CFG503_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
WORK2 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG, CHK = [], {}
RES = {"lane": "CFG503", "script": "cfg503_score", "mutate": MUTATE}


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


def pstack(tab, gi, WW, mask):
    NG = tab.shape[0]; out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


# ------------------------------------------------------------------ tables
ET = np.load(os.path.join(WORK, "cfg503_env_table.npz"))
OT = np.load(os.path.join(WORK, "cfg503_own_tables.npz"))
LMS, ZG, RG = ET["LMS"], ET["ZG"], ET["RG"]
LRG = np.log(RG)


def grid_interp(tab, GS, GZ):
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    return f(np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZG[0], ZG[-1])])


_ECACHE = {}


def env_vectors(key, GM, GZ, GS, tagname):
    ck = (key, tagname)
    if ck in _ECACHE:
        return _ECACHE[ck]
    Eg = grid_interp(ET[key], GS, GZ)
    out = np.zeros((len(GM), 15))
    for g in range(len(GM)):
        out[g] = LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), GM[g])
    _ECACHE[ck] = out
    return out


# ------------------------------------------------------------------ data: stack P, f30, ALL (CFG502 verbatim)
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
f30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
nL = len(lens["z"]); ALLM = np.ones(nL, bool)
gi, GM, GZ, GS = OT["gi"], OT["GM"], OT["GZ"], OT["GS"]
NG = len(GM)
d, Cv = esd_full_loo(WG, WW, patch, ALLM); h15 = hart(15)
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
dref = np.array(J377["primary"]["esd"]); Rm = np.array(J377["primary"]["meanR"])
check("C1 stack P data vector = CFG377 primary", np.max(np.abs(d / dref - 1)) < 1e-10, f"max rel {np.max(np.abs(d / dref - 1)):.1e}")
INN = Rm <= 0.445; OUT = ~INN
d30, C30 = esd_full_loo(WG, WW, patch, f30)
S = np.load(os.path.join(WORK2, "cfg502_stage.npz"))
WWA, WGA, pA = S["WW"], S["WG"], S["patch_all"]
giA, GMA, GZA, GSA = OT["giA"], OT["GMA"], OT["GZA"], OT["GSA"]
mA = np.ones(len(WWA), bool)
dA, CA = esd_full_loo(WGA, WWA, pA, mA)
RmA = (WWA * np.sqrt(C.G_MPC * S["Mgal"][:, None] / np.sqrt(C.GEDGE_K[:-1] * C.GEDGE_K[1:])[None, :])).sum(0) / WWA.sum(0)
INA = RmA <= 0.445
P(f"stack P {nL} lenses / {NG} groups; f30 {f30.sum()}; ALL {len(WWA)} lenses / {len(GMA)} groups")

# C2a: unstripped Moster LCDM / F tables = CFG495's committed per-group tables
T495 = np.load(os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg495_work", "cfg495_pred_tables.npz")))
assert np.array_equal(T495["gi"], gi)
dv = 0.0
for foot in FOOTS:
    dv = max(dv, float(np.max(np.abs(OT[f"P|{foot}|LCDM|full_moster"] / T495[f"{foot}_lcdm"] - 1))),
             float(np.max(np.abs((OT[f"P|{foot}|F_NODD|full_moster"] + OT[f"P|{foot}|PROP|full_moster"]) /
                                 (T495[f"{foot}_nodd"] + T495[f"{foot}_prop"]) - 1))))
check("C2a unstripped Moster LCDM and F_dd per-group tables = CFG495's committed tables (1e-6)", dv < 1e-6, f"max rel {dv:.1e}")

MODELS = ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD")
REPORTED = ("F_NODD", "LAW_X05")


def own_group(pref, foot, model, shmr, key, strip, GSx, GZx):
    """per-group own vectors: (1 - f) full + f tr (strip) or full."""
    def one(m):
        base = f"{pref}|{foot}|{m}|" if pref == "P" else f"{pref}|{m}|"
        full = OT[base + f"full_{shmr}"]
        if not strip:
            return full
        f = np.clip(grid_interp(ET[f"{shmr}_{key}_f"], GSx, GZx), 0, 1)[:, None]
        return (1 - f) * full + f * OT[base + f"tr_{shmr}_{key}"]
    if model == "F_DD":
        return one("F_NODD") + one("PROP")
    return one(model)


def model_vec(sample, model, foot, shmr, mode, strip):
    if sample == "P":
        key, mask, Ekey = "W10", ALLM, "W10"
    elif sample == "f30":
        key, mask, Ekey = "W30", f30, "W30"
    else:
        key, Ekey = "ALL", "ALL"
    if sample == "ALL":
        own = own_group("A", None, "LCDM", shmr, key, strip, GSA, GZA)
        E = env_vectors(f"E_{shmr}_{mode}_{Ekey}", GMA, GZA, GSA, "ALL")
        out = np.zeros(15)
        for k in range(15):
            w = np.bincount(giA, weights=WWA[:, k], minlength=len(GMA)); out[k] = (w @ (own[:, k] + E[:, k])) / w.sum()
        return out
    own = own_group("P", foot, model, shmr, key, strip, GS, GZ)
    E = env_vectors(f"E_{shmr}_{mode}_{Ekey}", GM, GZ, GS, "P")
    return pstack(own + E, gi, WW, mask)


def chi2c(dv_, C_, h, m, delta=None):
    Ct = C_ / h + (np.outer(delta, delta) if delta is not None else 0.0)
    r = dv_ - m
    return float(r @ np.linalg.solve(Ct, r))


SAMPLES = {"P": (d, Cv, INN), "f30": (d30, C30, INN), "ALL": (dA, CA, INA)}


def score(sample, model, foot, mode, strip, prop):
    dv_, C_, inn = SAMPLES[sample]
    mM = model_vec(sample, model, foot, "moster", mode, strip)
    mB = model_vec(sample, model, foot, "behroozi", mode, strip) if mode != "eh" else mM * np.nan   # eh: Moster only (M0)
    dl = (mB - mM) if prop else None
    c_ = chi2c(dv_, C_, hart(15), mM, dl)
    ou = ~inn
    ci = chi2c(dv_[inn], C_[np.ix_(inn, inn)], hart(int(inn.sum())), mM[inn], None if dl is None else dl[inn])
    co = chi2c(dv_[ou], C_[np.ix_(ou, ou)], hart(int(ou.sum())), mM[ou], None if dl is None else dl[ou])
    return dict(chi2=c_, p=float(stats.chi2.sf(c_, 15)), chi2_inner9=ci, chi2_outer6=co,
                chi2_data_only_moster=chi2c(dv_, C_, hart(15), mM), chi2_data_only_behroozi=chi2c(dv_, C_, hart(15), mB),
                model=mM.tolist(), model_behroozi=mB.tolist())


def run_config(name, mode, strip, prop, full=True):
    P(f"\n=============== {name}: E mode '{mode}', stripping {'ON' if strip else 'OFF'}, "
      f"{'SHMR propagated (Moster primary + Behroozi rank-one)' if prop else 'Moster only, data covariance only'} ===============")
    R_ = {"mode": mode, "strip": strip, "prop": prop}
    for sample in ("P", "f30", "ALL"):
        dv_, C_, inn = SAMPLES[sample]
        models = (MODELS + REPORTED) if (sample != "ALL" and full) else ("LCDM",)
        res = {}
        for foot in (FOOTS if sample != "ALL" else ("canonical",)):
            res[foot] = {m: score(sample, m, foot, mode, strip, prop) for m in models}
        R_[sample] = res
        P(f"  --- {sample} ---")
        P("    data   : " + " ".join(f"{x:6.3f}" for x in dv_))
        P("    sigma  : " + " ".join(f"{x:6.3f}" for x in np.sqrt(np.diag(C_))))
        P("    LCDM   : " + " ".join(f"{x:6.3f}" for x in res["canonical"]["LCDM"]["model"]) + "   (own + E, Moster)")
        P("    pull   : " + " ".join(f"{x:+6.2f}" for x in (dv_ - np.array(res['canonical']['LCDM']['model'])) / np.sqrt(np.diag(C_))))
        for foot in res:
            P(f"    [{foot}] model    | chi2/15 (p)          | inner9 outer6 | data-only chi2 Moster / Behroozi")
            for m in res[foot]:
                s = res[foot][m]
                P(f"      {m:8s} | {s['chi2']:8.2f} ({s['p']:.2e}) | {s['chi2_inner9']:6.2f} {s['chi2_outer6']:6.2f} | "
                  f"{s['chi2_data_only_moster']:8.2f} / {s['chi2_data_only_behroozi']:8.2f}" + ("   (reported)" if m in REPORTED else ""))
    g1 = R_["P"]["canonical"]["LCDM"]; g2 = R_["f30"]["canonical"]["LCDM"]; g3 = R_["ALL"]["canonical"]["LCDM"]
    R_["gates"] = dict(G1=dict(chi2=g1["chi2"], p=g1["p"], passed=g1["p"] > 0.01), G2=dict(chi2=g2["chi2"], p=g2["p"], passed=g2["p"] > 0.01),
                       G3=dict(chi2=g3["chi2"], p=g3["p"], passed=g3["p"] > 0.001))
    P(f"  GATES: G1 stack P LCDM chi2 {g1['chi2']:.2f} (p {g1['p']:.2e}) {'PASS' if g1['p'] > 0.01 else 'FAIL'}; "
      f"G2 f30 {g2['chi2']:.2f} (p {g2['p']:.2e}) {'PASS' if g2['p'] > 0.01 else 'FAIL'}; "
      f"G3 ALL {g3['chi2']:.2f} (p {g3['p']:.2e}) {'PASS' if g3['p'] > 0.001 else 'FAIL'}")
    return R_


if not MUTATE:
    R_ = run_config("MAIN", "nlz", True, True)
    # diagnostics (reported): E variants for LCDM on stack P
    P("\n  reported E variants for LCDM (stack P / f30 / ALL, propagated chi2): ")
    diag = {}
    for mode in ("nl", "lin", "eh"):
        if mode == "eh":
            continue                                  # eh exists for Moster only; it is the M0 MUTATE path
        diag[mode] = {s: score(s, "LCDM", "canonical", mode, True, True)["chi2"] for s in ("P", "f30", "ALL")}
        P(f"    E mode {mode:4s} + stripping: " + ", ".join(f"{s} {v:.2f}" for s, v in diag[mode].items()))
    R_["diag_E_modes"] = diag
    # E vector itself (stack P, Moster)
    EP = pstack(env_vectors("E_moster_nlz_W10", GM, GZ, GS, "P"), gi, WW, ALLM)
    EP0 = pstack(env_vectors("E_moster_eh_W10", GM, GZ, GS, "P"), gi, WW, ALLM)
    P("    R [Mpc]         : " + " ".join(f"{x:6.3f}" for x in Rm))
    P("    E nlz (W10)     : " + " ".join(f"{x:6.3f}" for x in EP))
    P("    E CFG502 (W10)  : " + " ".join(f"{x:6.3f}" for x in EP0))
    own_s = pstack(own_group("P", "canonical", "LCDM", "moster", "W10", True, GS, GZ), gi, WW, ALLM)
    own_f = pstack(own_group("P", "canonical", "LCDM", "moster", "W10", False, GS, GZ), gi, WW, ALLM)
    P("    LCDM own strip  : " + " ".join(f"{x:6.3f}" for x in own_s))
    P("    LCDM own full   : " + " ".join(f"{x:6.3f}" for x in own_f))
    R_["E_nlz_P"] = EP.tolist(); R_["E_cfg502_P"] = EP0.tolist(); R_["LCDM_own_strip_P"] = own_s.tolist(); R_["LCDM_own_full_P"] = own_f.tolist()
    RES["MAIN"] = R_

    # ---------------- verdict
    P("\n=============== VERDICT (frozen rule) ===============")
    G = R_["gates"]
    valid = G["G1"]["passed"] and G["G2"]["passed"] and G["G3"]["passed"]
    per = {}; clash = {}
    for foot in FOOTS:
        sc = R_["P"][foot]
        best = min(MODELS, key=lambda k: sc[k]["chi2"])
        dE = sc["EDGE"]["chi2"] - sc[best]["chi2"]
        clash[foot] = dict(best=best, chi2_best=sc[best]["chi2"], d_edge=dE)
        per[foot] = {k: ("PASS" if sc[k]["p"] > 0.01 else "FAIL") if valid else "NO VERDICT (gate failed)" for k in MODELS}
        P(f"  [{foot}] best of (i)-(v): {best} chi2 {sc[best]['chi2']:.2f}; edge - best = {dE:+.2f}; "
          + ", ".join(f"{k} {per[foot][k]}" for k in MODELS))
    if not valid:
        cv = "NOT DECIDED (MODEL STILL INADEQUATE: " + ", ".join(g for g in ("G1", "G2", "G3") if not G[g]["passed"]) + " failed)"
    elif all(clash[f]["d_edge"] <= 4 for f in FOOTS):
        cv = "RESOLVED"
    elif all(clash[f]["d_edge"] >= 9 for f in FOOTS):
        cv = "CONFIRMED"
    else:
        cv = "OPEN"
    labels = ["nonlinear 2h NOT CROSS-CHECKED BY PM"]
    R_["valid"] = valid; R_["per_model"] = per; R_["clash"] = clash; R_["clash_verdict"] = cv; R_["labels"] = labels
    P(f"  VALIDATION: {'VALID' if valid else 'MODEL STILL INADEQUATE'}")
    P(f"  CLASH (5.85 r_M edge vs lensing): {cv}  [label: {labels[0]}]")
else:
    J502 = json.load(open(os.path.join(LANES, "CFG502_two_halo_first_principles", "cfg502_score_results.json")))["MAIN"]
    R0 = run_config("M0 (all upgrades off = CFG502 path)", "eh", False, False)
    dmx = 0.0; msg = []
    for foot in FOOTS:
        for m in MODELS + REPORTED:
            dd = abs(R0["P"][foot][m]["chi2_data_only_moster"] - J502[foot][m]["chi2"]); dmx = max(dmx, dd)
    d1 = abs(R0["f30"]["canonical"]["LCDM"]["chi2_data_only_moster"] - J502["N1_f30"]["scores"]["canonical"]["LCDM"]["chi2"])
    d2 = abs(R0["ALL"]["canonical"]["LCDM"]["chi2_data_only_moster"] - J502["N2_ALL"]["chi2"])
    check("M0 halofit off (CFG502 colossus EH, zeta = 1), stripping off, Moster only: reproduces CFG502's 14 stack-P chi2 and N1 / N2 LCDM "
          "within 0.01", max(dmx, d1, d2) <= 0.01,
          f"max |d| stack P {dmx:.4f}; N1 {R0['f30']['canonical']['LCDM']['chi2']:.3f} vs {J502['N1_f30']['scores']['canonical']['LCDM']['chi2']:.3f}; "
          f"N2 {R0['ALL']['canonical']['LCDM']['chi2']:.3f} vs {J502['N2_ALL']['chi2']:.3f}")
    RES["M0"] = R0
    RES["MH"] = run_config("MH (halofit off: CAMB linear xi, zeta = 1; stripping + SHMR on)", "lin", True, True)
    RES["MS"] = run_config("MS (stripping off; halofit + zeta + SHMR on)", "nlz", False, True)
    main = json.load(open(os.path.join(HERE, "cfg503_score_results.json")))["MAIN"]
    a = main["P"]["canonical"]["LCDM"]; b = RES["MS"]["P"]["canonical"]["LCDM"]
    di = abs(a["chi2_inner9"] - b["chi2_inner9"])
    sig = np.sqrt(np.diag(Cv))
    mv = float(np.max(np.abs(np.array(a["model"])[INN] - np.array(b["model"])[INN]) / sig[INN]))
    check("MS stripping off moves the inner bins (LCDM inner-9 chi2 |d| > 2 or an inner bin moves > 0.5 sigma)", di > 2 or mv > 0.5,
          f"inner9 {a['chi2_inner9']:.2f} (main) vs {b['chi2_inner9']:.2f} (off), |d| {di:.2f}; max inner-bin shift {mv:.2f} sigma")

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg503_score_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg503_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
