#!/usr/bin/env python3
"""CFG504 scoring (FROZEN_CRITERIA.md sections 5-7; criteria commit 333a5fce4). Data handling, grouping, stacking, models, SHMR
propagation, gates and verdict copied from CFG503's cfg503_score.py (not edited). The only change: the calibrated continuous transition
(window f_t(r / r_ta,LCDM), x_t from cfg504_calib.py) replaces the sharp r_ta truncation of every model's own profile and the sharp
hole / two-halo boundary of E, identically for every model.

PRIMARY: own 'prim' + E 'prim' (A = 1), stripping on, SHMR propagated.  Reported variants: lo / hi (x_t -+ sigma_tot), ext (x_t linear
in log M_ta), Acar (two-halo x mean PM A), Eonly (own sharp, E smooth), ownrta (framework own windowed in own r_ta,law units).
MUTATE (CFG504_MUTATE=1, outputs *_MUTATE.*): M0 sharp window through this code must reproduce CFG503's main chi2; C9 steep window.
Run: nice -n 15 python3 cfg504_score.py ; CFG504_MUTATE=1 nice -n 15 python3 cfg504_score.py
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

MUTATE = os.environ.get("CFG504_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg504_work"))
WORK2 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG, CHK = [], {}
RES = {"lane": "CFG504", "script": "cfg504_score", "mutate": MUTATE}
CAL = json.load(open(os.path.join(HERE, "cfg504_calib_results.json")))["primary"]


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}{'' if lb else ' (reported)'}: {msg}")


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


ET = np.load(os.path.join(WORK, "cfg504_env_table.npz"))
OT = np.load(os.path.join(WORK, "cfg504_own_tables.npz"))
LMS, ZG, RG = ET["LMS"], ET["ZG"], ET["RG"]
LRG = np.log(RG)


def grid_interp(tab, GS, GZ):
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    return f(np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZG[0], ZG[-1])])


def E_table(shmr, ev, key, A=1.0):
    if ev == "sharp":
        return ET[f"E_{shmr}_sharp_{key}"]
    f = np.clip(ET[f"{shmr}_{key}_f"], 0, 1)[..., None]
    bc = ET[f"{shmr}_{key}_bc"][..., None]; bh = ET[f"{shmr}_{key}_bh"][..., None]
    SS = ET[f"{shmr}_SS_{ev}"]
    return ET[f"{shmr}_HS_{ev}"] + A * (1 - f) * bc * SS + f * (ET[f"{shmr}_{key}_Thost"] + A * bh * SS)


_ECACHE = {}


def env_vectors(shmr, ev, key, A, GM, GZ, GS, tagname):
    ck = (shmr, ev, key, A, tagname)
    if ck in _ECACHE:
        return _ECACHE[ck]
    Eg = grid_interp(E_table(shmr, ev, key, A), GS, GZ)
    out = np.zeros((len(GM), 15))
    for g in range(len(GM)):
        out[g] = LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), GM[g])
    _ECACHE[ck] = out
    return out


lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
f30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
nL = len(lens["z"]); ALLM = np.ones(nL, bool)
gi, GM, GZ, GS = OT["gi"], OT["GM"], OT["GZ"], OT["GS"]
NG = len(GM)
d, Cv = esd_full_loo(WG, WW, patch, ALLM)
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
dref = np.array(J377["primary"]["esd"]); Rm = np.array(J377["primary"]["meanR"])
check("C1 stack P data vector = CFG377 primary", np.max(np.abs(d / dref - 1)) < 1e-10, f"max rel {np.max(np.abs(d / dref - 1)):.1e}")
INN = Rm <= 0.445
d30, C30 = esd_full_loo(WG, WW, patch, f30)
S = np.load(os.path.join(WORK2, "cfg502_stage.npz"))
WWA, WGA, pA = S["WW"], S["WG"], S["patch_all"]
giA, GMA, GZA, GSA = OT["giA"], OT["GMA"], OT["GZA"], OT["GSA"]
dA, CA = esd_full_loo(WGA, WWA, pA, np.ones(len(WWA), bool))
RmA = (WWA * np.sqrt(C.G_MPC * S["Mgal"][:, None] / np.sqrt(C.GEDGE_K[:-1] * C.GEDGE_K[1:])[None, :])).sum(0) / WWA.sum(0)
INA = RmA <= 0.445
P(f"stack P {nL} lenses / {NG} groups; f30 {f30.sum()}; ALL {len(WWA)} lenses / {len(GMA)} groups; x_t primary {CAL['x_t']:.4f} "
  f"(sigma_tot {CAL['sigma_tot']:.4f}); PM label: {'TRANSITION FORM POOR FIT ON PM' if CAL['label_poor_fit'] else 'none'}")

MODELS = ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD")
REPORTED = ("F_NODD", "LAW_X05")


def own_group(pref, foot, model, shmr, key, ov, GSx, GZx):
    def one(m):
        base = f"{pref}|{foot}|{m}|{ov}|" if pref == "P" else f"{pref}|{m}|{ov}|"
        full = OT[base + f"full_{shmr}"]
        f = np.clip(grid_interp(ET[f"{shmr}_{key}_f"], GSx, GZx), 0, 1)[:, None]
        return (1 - f) * full + f * OT[base + f"tr_{shmr}_{key}"]
    if model == "F_DD":
        return one("F_NODD") + one("PROP")
    return one(model)


def model_vec(sample, model, foot, shmr, cfg):
    ov, ev, A = cfg["own"], cfg["E"], cfg["A"]
    if sample == "ALL":
        own = own_group("A", None, "LCDM", shmr, "ALL", "prim" if ov == "own" else ov, GSA, GZA)
        E = env_vectors(shmr, ev, "ALL", A, GMA, GZA, GSA, "ALL")
        out = np.zeros(15)
        for k in range(15):
            w = np.bincount(giA, weights=WWA[:, k], minlength=len(GMA)); out[k] = (w @ (own[:, k] + E[:, k])) / w.sum()
        return out
    key, mask = ("W10", ALLM) if sample == "P" else ("W30", f30)
    own = own_group("P", foot, model, shmr, key, ov, GS, GZ)
    E = env_vectors(shmr, ev, key, A, GM, GZ, GS, "P")
    return pstack(own + E, gi, WW, mask)


def chi2c(dv_, C_, h, m, delta=None):
    Ct = C_ / h + (np.outer(delta, delta) if delta is not None else 0.0)
    r = dv_ - m
    return float(r @ np.linalg.solve(Ct, r))


SAMPLES = {"P": (d, Cv, INN), "f30": (d30, C30, INN), "ALL": (dA, CA, INA)}


def score(sample, model, foot, cfg):
    dv_, C_, inn = SAMPLES[sample]
    mM = model_vec(sample, model, foot, "moster", cfg)
    mB = model_vec(sample, model, foot, "behroozi", cfg)
    dl = mB - mM
    c_ = chi2c(dv_, C_, hart(15), mM, dl)
    ou = ~inn
    ci = chi2c(dv_[inn], C_[np.ix_(inn, inn)], hart(int(inn.sum())), mM[inn], dl[inn])
    co = chi2c(dv_[ou], C_[np.ix_(ou, ou)], hart(int(ou.sum())), mM[ou], dl[ou])
    return dict(chi2=c_, p=float(stats.chi2.sf(c_, 15)), chi2_inner9=ci, chi2_outer6=co,
                chi2_data_only_moster=chi2c(dv_, C_, hart(15), mM), chi2_data_only_behroozi=chi2c(dv_, C_, hart(15), mB),
                model=mM.tolist(), model_behroozi=mB.tolist())


def run_config(name, cfg, full=True, verbose=True):
    P(f"\n=============== {name}: own '{cfg['own']}', E '{cfg['E']}', A {cfg['A']:.3f}; stripping ON; SHMR propagated ===============")
    R_ = {"cfg": cfg}
    for sample in ("P", "f30", "ALL"):
        dv_, C_, inn = SAMPLES[sample]
        models = (MODELS + REPORTED) if (sample != "ALL" and full) else ("LCDM",)
        res = {}
        for foot in (FOOTS if sample != "ALL" else ("canonical",)):
            res[foot] = {m: score(sample, m, foot, cfg) for m in models}
        R_[sample] = res
        if verbose:
            P(f"  --- {sample} ---")
            P("    R      : " + " ".join(f"{x:6.3f}" for x in (Rm if sample != "ALL" else RmA)))
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


def table(R_, tag):
    P(f"  [{tag}] stack P chi2 (can / alt): " + "; ".join(
        f"{m} {R_['P']['canonical'][m]['chi2']:.2f} / {R_['P']['alt'][m]['chi2']:.2f}" for m in MODELS + REPORTED))


if not MUTATE:
    PRIM = dict(own="prim", E="prim", A=1.0)
    R_ = run_config("MAIN (primary transition)", PRIM)
    EP = pstack(env_vectors("moster", "prim", "W10", 1.0, GM, GZ, GS, "P"), gi, WW, ALLM)
    E0 = pstack(env_vectors("moster", "sharp", "W10", 1.0, GM, GZ, GS, "P"), gi, WW, ALLM)
    own_p = pstack(own_group("P", "canonical", "LCDM", "moster", "W10", "prim", GS, GZ), gi, WW, ALLM)
    own_s = pstack(own_group("P", "canonical", "LCDM", "moster", "W10", "sharp", GS, GZ), gi, WW, ALLM)
    P("\n  stack P pieces (Moster, Msun/pc^2):")
    P("    R [Mpc]          : " + " ".join(f"{x:6.3f}" for x in Rm))
    P("    E smooth (prim)  : " + " ".join(f"{x:6.3f}" for x in EP))
    P("    E sharp (CFG503) : " + " ".join(f"{x:6.3f}" for x in E0))
    P("    LCDM own smooth  : " + " ".join(f"{x:6.3f}" for x in own_p))
    P("    LCDM own sharp   : " + " ".join(f"{x:6.3f}" for x in own_s))
    P("    total smooth     : " + " ".join(f"{x:6.3f}" for x in own_p + EP))
    P("    total sharp      : " + " ".join(f"{x:6.3f}" for x in own_s + E0))
    P("    data             : " + " ".join(f"{x:6.3f}" for x in d))
    R_["pieces"] = dict(E_prim=EP.tolist(), E_sharp=E0.tolist(), own_prim=own_p.tolist(), own_sharp=own_s.tolist())
    RES["MAIN"] = R_

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
    labels = ["transition PM-calibrated at log M_ta >= 13.5 (z = 0, 512^3, mesh 0.39 Mpc/h) and extrapolated ~1 dex to KiDS masses "
              "assuming self-similarity in r / r_ta"]
    if CAL["label_poor_fit"]:
        labels.append("TRANSITION FORM POOR FIT ON PM")
    R_["valid"] = valid; R_["per_model"] = per; R_["clash"] = clash; R_["clash_verdict"] = cv; R_["labels"] = labels
    P(f"  VALIDATION: {'VALID' if valid else 'MODEL STILL INADEQUATE'}")
    P(f"  CLASH (5.85 r_M edge vs lensing): {cv}")
    P("  labels: " + "; ".join(labels))

    P("\n=============== REPORTED VARIANTS (none changes the verdict) ===============")
    VAR = {"lo": dict(own="lo", E="lo", A=1.0), "hi": dict(own="hi", E="hi", A=1.0), "ext": dict(own="ext", E="ext", A=1.0),
           "Acar": dict(own="prim", E="prim", A=float(CAL["A_mean"])), "Eonly": dict(own="sharp", E="prim", A=1.0),
           "ownrta": dict(own="own", E="prim", A=1.0)}
    RES["VARIANTS"] = {}
    for k, cfg in VAR.items():
        Rv = run_config(f"variant {k}", cfg, verbose=False)
        table(Rv, k)
        RES["VARIANTS"][k] = {"cfg": cfg, "gates": Rv["gates"],
                              "P": {f: {m: {q: Rv["P"][f][m][q] for q in ("chi2", "p", "chi2_inner9", "chi2_outer6")} for m in Rv["P"][f]}
                                    for f in FOOTS},
                              "pull_LCDM_P": ((d - np.array(Rv["P"]["canonical"]["LCDM"]["model"])) / np.sqrt(np.diag(Cv))).tolist()}
else:
    J503 = json.load(open(os.path.join(LANES, "CFG503_two_halo_nonlinear", "cfg503_score_results.json")))["MAIN"]
    R0 = run_config("M0 (sharp window through CFG504 code = CFG503 main)", dict(own="sharp", E="sharp", A=1.0))
    dmx = 0.0
    for foot in FOOTS:
        for m in MODELS + REPORTED:
            dmx = max(dmx, abs(R0["P"][foot][m]["chi2"] - J503["P"][foot][m]["chi2"]))
    d2 = abs(R0["f30"]["canonical"]["LCDM"]["chi2"] - J503["f30"]["canonical"]["LCDM"]["chi2"])
    d3 = abs(R0["ALL"]["canonical"]["LCDM"]["chi2"] - J503["ALL"]["canonical"]["LCDM"]["chi2"])
    check("M0 sharp window reproduces CFG503's 14 stack-P chi2 and G2 / G3 LCDM within 0.01", max(dmx, d2, d3) <= 0.01,
          f"max |d| stack P {dmx:.4f}; G2 {R0['f30']['canonical']['LCDM']['chi2']:.3f} vs {J503['f30']['canonical']['LCDM']['chi2']:.3f}; "
          f"G3 {R0['ALL']['canonical']['LCDM']['chi2']:.3f} vs {J503['ALL']['canonical']['LCDM']['chi2']:.3f}")
    RES["M0"] = R0
    Es = pstack(env_vectors("moster", "steep", "W10", 1.0, GM, GZ, GS, "P"), gi, WW, ALLM)
    E0 = pstack(env_vectors("moster", "sharp", "W10", 1.0, GM, GZ, GS, "P"), gi, WW, ALLM)
    dsg = float(np.max(np.abs(Es - E0) / np.sqrt(np.diag(Cv))))
    check("C9 steep window (beta 64, gamma 128, x_t 1) E vector within 0.05 sigma of the sharp one per stack-P bin", dsg < 0.05,
          f"max |dE| / sigma = {dsg:.3f}", lb=False)
    RES["C9"] = dict(E_steep=Es.tolist(), E_sharp=E0.tolist(), max_dsig=dsg)

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg504_score_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg504_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
