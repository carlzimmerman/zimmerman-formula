#!/usr/bin/env python3
"""CFG520 validation and (if a ruler is VALID) KiDS re-score (FROZEN_CRITERIA.md sections 3, 4, 6; criteria commit 6d184c37d).

CFG506's cfg506_score.py, copied (data handling, grouping, pstack, own-profile mixing, chi2, tabulation, companion ratio, f grid), reading:
  - selection tables (cfg520_sel_<RULE>_<KEY>.npz) for the validation (companion ratio V-A, leaked fraction V-B);
  - DeltaSigma tables (cfg520_box_MAIN_<KEY>.npz) for the re-score, only for VALID rulers.
R0b: CFG506's own box files through this validation code reproduce CFG506's committed numbers. R0c: CFG506's own files through the re-score
code reproduce CFG506's committed canonical F chi2 (only if a re-score runs).
MUTATE (CFG520_MUTATE=1, outputs *_MUTATE.*): M2X validation (must be INVALID for the canonical ruler); SHUF on the MAIN rulers (if built);
S0-vs-reference reported.
Run: nice -n 10 python3 cfg520_score.py ; CFG520_MUTATE=1 nice -n 10 python3 cfg520_score.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
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
import cfg100_lib as C                                                       # noqa: E402,F401  (read-only)
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only)

MUTATE = os.environ.get("CFG520_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg520_work")
W506 = os.path.join(EXT, "cfg506_work")
W503 = os.path.join(EXT, "cfg503_work")
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
FOOTS = ("canonical", "alt")
LH = 0.6736
F_OBS, SIG_TOT = 0.22342746446430256, 0.004443624815041658       # CFG519 f_IC, sigma_tot (cfg519_satfrac_results.json)
LOG, CHK = [], {}
RES = {"lane": "CFG520", "script": "cfg520_score", "mutate": MUTATE}


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


ET = np.load(os.path.join(W503, "cfg503_env_table.npz"))
OT = np.load(os.path.join(W503, "cfg503_own_tables.npz"))
LMS, ZG, RG = ET["LMS"], ET["ZG"], ET["RG"]
LRG = np.log(RG)
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
nL = len(lens["z"]); ALLM = np.ones(nL, bool)
gi, GM, GZ, GS = OT["gi"], OT["GM"], OT["GZ"], OT["GS"]
NG = len(GM)
d, Cv = esd_full_loo(WG, WW, patch, ALLM)
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
dref = np.array(J377["primary"]["esd"]); Rm = np.array(J377["primary"]["meanR"])
check("C1 stack P data vector = CFG377 primary", np.max(np.abs(d / dref - 1)) < 1e-10, f"max rel {np.max(np.abs(d / dref - 1)):.1e}")
INN = Rm <= 0.445
SIG = np.sqrt(np.diag(Cv))


def grid_interp(tab, GSx, GZx):
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    return f(np.c_[np.clip(GSx, LMS[0], LMS[-1]), np.clip(GZx, ZG[0], ZG[-1])])


def env_vectors_from_grid(Etab):
    Eg = grid_interp(Etab, GS, GZ)
    out = np.zeros((NG, 15))
    for g in range(NG):
        out[g] = LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), GM[g])
    return out


MODELS = ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD")
REPORTED = ("F_NODD", "LAW_X05")
FRAMEWORK = ("F_DD", "EDGE", "LAW_RTA", "V1")


def own_group(foot, model, shmr, fgrid):
    f = np.clip(grid_interp(fgrid, GS, GZ), 0, 1)[:, None]
    def one(m):
        base = f"P|{foot}|{m}|"
        return (1 - f) * OT[base + f"full_{shmr}"] + f * OT[base + f"tr_{shmr}_W10"]
    if model == "F_DD":
        return one("F_NODD") + one("PROP")
    return one(model)


def chi2c(dv_, C_, h, m, extra=None):
    Ct = C_ / h + (extra if extra is not None else 0.0)
    r = dv_ - m
    return float(r @ np.linalg.solve(Ct, r))


def score_rows(Evec_m, Evec_b, fgrid_m, fgrid_b, Cr, models):
    out = {}
    for foot in FOOTS:
        out[foot] = {}
        for mdl in models:
            mM = pstack(own_group(foot, mdl, "moster", fgrid_m) + Evec_m, gi, WW, ALLM)
            mB = pstack(own_group(foot, mdl, "behroozi", fgrid_b) + Evec_b, gi, WW, ALLM)
            dl = mB - mM
            ex = np.outer(dl, dl) + (Cr if Cr is not None else 0.0)
            c15 = chi2c(d, Cv, hart(15), mM, ex)
            ci = chi2c(d[INN], Cv[np.ix_(INN, INN)], hart(9), mM[INN], ex[np.ix_(INN, INN)])
            out[foot][mdl] = dict(chi2_inner9=ci, p_inner9=float(stats.chi2.sf(ci, 9)), chi2_15=c15, p_15=float(stats.chi2.sf(c15, 15)),
                                  chi2_inner9_data_only=chi2c(d[INN], Cv[np.ix_(INN, INN)], hart(9), mM[INN]),
                                  chi2_15_data_only=chi2c(d, Cv, hart(15), mM), model=mM.tolist())
    return out


J503 = json.load(open(os.path.join(LANES, "CFG503_two_halo_nonlinear", "cfg503_score_results.json")))["MAIN"]
E503m = env_vectors_from_grid(ET["E_moster_nlz_W10"]); E503b = env_vectors_from_grid(ET["E_behroozi_nlz_W10"])
S503 = score_rows(E503m, E503b, ET["moster_W10_f"], ET["behroozi_W10_f"], None, MODELS + REPORTED)
dmx = max(abs(S503[f][m]["chi2_15"] - J503["P"][f][m]["chi2"]) for f in FOOTS for m in MODELS + REPORTED)
check("C2 scoring code with CFG503's E_nlz and f reproduces CFG503's 14 stack-P chi2 (15 bins) within 0.01", dmx <= 0.01, f"max |d| {dmx:.4f}")
E503_P = pstack(E503m, gi, WW, ALLM)
f503 = pstack(np.repeat(np.clip(grid_interp(ET["moster_W10_f"], GS, GZ), 0, 1)[:, None], 15, 1), gi, WW, ALLM)[0]

E504_P = None
f504 = os.path.join(LANES, "CFG504_smooth_halo_transition", "cfg504_score_results.json")
if os.path.exists(f504):
    J504 = json.load(open(f504))
    if "E_prim" in J504.get("MAIN", {}).get("pieces", {}):
        E504_P = np.array(J504["MAIN"]["pieces"]["E_prim"])
EREF = E504_P if E504_P is not None else E503_P
EREF_NAME = "CFG504 E (committed)" if E504_P is not None else "CFG503 E_nlz"

CUR = "F"
VARIANTS = {"F": "frozen neighbour threshold (pool 5th percentile)", "P": "CFG506 departure D1: pool-calibrated neighbour completeness"}
BOXSETS = {"canonical": ["TA512_can359", "TA512_can360"], "alt": ["TA512_alt359"], "DE": ["TA512_DEcan359"], "S0": ["S0512_359", "S0512_360"]}
ZN = np.array([0.15, 0.25, 0.35, 0.45])


def load_file(path):
    Z = np.load(path)
    return {k: Z[k] for k in Z.files}


def tables(B, tkey, wkey, loo=None):
    num = B[f"{CUR}_T_{tkey}"]; den = B[f"{CUR}_W_{wkey}"]
    if loo is None:
        n_, d_ = num.sum(0), den.sum(0)
    else:
        n_, d_ = num.sum(0) - num[loo], den.sum(0) - den[loo]
    return np.where(d_[..., None] > 0, n_ / np.maximum(d_[..., None], 1e-300), np.nan)


def to_grid(B, E):
    VB = B["VB"]; RM = B["RM"]
    lmc = B[f"{CUR}_LMW"] / np.maximum(B[f"{CUR}_LMWW"], 1e-300)
    out_n = np.zeros((4, len(LMS), len(RG)))
    for n in range(4):
        xc = lmc[VB, n]; Ev = E[VB, n]
        Rp = RM / (LH * (1 + ZN[n])); Ep = Ev * LH * (1 + ZN[n]) ** 2
        Em = np.array([np.interp(LMS, xc, Ep[:, j]) for j in range(len(RM))]).T
        for i in range(len(LMS)):
            v = np.interp(LRG, np.log(Rp), Em[i], left=Em[i, 0], right=0.0)
            v[RG > Rp[-1]] = 0.0
            out_n[n, i] = v
    out = np.zeros((len(LMS), len(ZG), len(RG)))
    for iz, z in enumerate(ZG):
        zc = min(max(z, ZN[0]), ZN[-1]); k = min(np.searchsorted(ZN, zc), 3); k = max(k, 1)
        t = (zc - ZN[k - 1]) / (ZN[k] - ZN[k - 1])
        out[:, iz] = (1 - t) * out_n[k - 1] + t * out_n[k]
    return out


def f_grid(B):
    FS = B[f"{CUR}_FS"].sum(0); W = B[f"{CUR}_W_all"].sum(0)
    fs = FS / np.maximum(W, 1e-300)
    VB = B["VB"]; lmc = B[f"{CUR}_LMW"] / np.maximum(B[f"{CUR}_LMWW"], 1e-300)
    gn = np.array([np.interp(LMS, lmc[VB, n], fs[VB, n]) for n in range(4)])
    out = np.zeros((len(LMS), len(ZG)))
    for iz, z in enumerate(ZG):
        out[:, iz] = np.array([np.interp(z, ZN, gn[:, i]) for i in range(len(LMS))])
    return out


S2 = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))


def companion_ratio(Bs, mlim_box):
    S = S2
    iso = S["iso_idx"]; zl = S["z"][iso]; lml = S["logM"][iso]
    meas = S["cin"] - S["can"] * (math.pi * 0.25) / (math.pi * 20.0)
    wl = S["WW"][iso].sum(1)
    preds = []
    for B in Bs:
        ct = B[f"{CUR}_CT"].sum(0) / np.maximum(B[f"{CUR}_W_all"].sum(0), 1e-300)
        VB = B["VB"]; lmc = B[f"{CUR}_LMW"] / np.maximum(B[f"{CUR}_LMWW"], 1e-300)
        gn = np.array([np.interp(lml, lmc[VB, n], ct[VB, n]) for n in range(4)])
        zc = np.clip(zl, ZN[0], ZN[-1]); k = np.clip(np.searchsorted(ZN, zc), 1, 3); t = (zc - ZN[k - 1]) / (ZN[k] - ZN[k - 1])
        preds.append((1 - t) * gn[k - 1, np.arange(len(zl))] + t * gn[k, np.arange(len(zl))])
    pred = sum(preds) / len(preds)
    sub = lml >= mlim_box
    return dict(ratio=float((wl[sub] * meas[sub]).sum() / (wl[sub] * pred[sub]).sum()), ratio_all_lenses=float((wl * meas).sum() / (wl * pred).sum()),
                meas_sub=float((wl[sub] * meas[sub]).sum() / wl[sub].sum()), pred_sub=float((wl[sub] * pred[sub]).sum() / wl[sub].sum()),
                frac_weight_sub=float(wl[sub].sum() / wl.sum()), meas_all=float((wl * meas).sum() / wl.sum()), pred_all=float((wl * pred).sum() / wl.sum()))


def f_stack(fg):
    return float(pstack(np.repeat(np.clip(grid_interp(fg, GS, GZ), 0, 1)[:, None], 15, 1), gi, WW, ALLM)[0])


meas_all = float(((S2["WW"][S2["iso_idx"]].sum(1)) * (S2["cin"] - S2["can"] * 0.25 / 20.0)).sum() / S2["WW"][S2["iso_idx"]].sum())
check("C4 measured companion excess = CFG502's per-lens excess (stack-weighted 0.25)", abs(meas_all - 0.2537226181022062) < 1e-9, f"{meas_all:.10f}")
JB506 = json.load(open(os.path.join(LANES, "CFG506_native_environment", "cfg506_box_results.json")))
JS506 = json.load(open(os.path.join(LANES, "CFG506_native_environment", "cfg506_score_results.json")))


def validate(files_of, label, mlims):
    """V-A and V-B for every ruler and both variants; returns {variant: {ruler: dict}}."""
    global CUR
    out = {}
    for V in VARIANTS:
        CUR = V; out[V] = {}
        for nm, keys in BOXSETS.items():
            fs_ = [files_of(k) for k in keys]
            if not all(os.path.exists(f) for f in fs_):
                continue
            Bs = [load_file(f) for f in fs_]
            mlb = max(mlims(k) for k in keys)
            co = companion_ratio(Bs, mlb)
            fn = f_stack(sum(f_grid(B) for B in Bs) / len(Bs))
            va = 0.67 <= co["ratio"] <= 1.5
            vb = abs(fn - F_OBS) <= 2 * SIG_TOT
            out[V][nm] = dict(companions=co, f_native=fn, m_lim_box=mlb, V_A=va, V_B=vb, valid=bool(va and vb),
                              f_within_0p03=bool(abs(fn - F_OBS) <= 0.03), f_minus_obs_in_sigtot=(fn - F_OBS) / SIG_TOT)
            P(f"  [{label}] [{V}] ruler {nm:9s}: companions measured {co['meas_sub']:.4f} / predicted {co['pred_sub']:.4f} = {co['ratio']:.3f} "
              f"(V-A {'ok' if va else 'FAIL'}; all lenses {co['ratio_all_lenses']:.3f}); leaked fraction {fn:.4f} vs {F_OBS:.4f} "
              f"({(fn - F_OBS) / SIG_TOT:+.1f} sigma_tot; V-B {'ok' if vb else 'FAIL'}; within 0.03: {abs(fn - F_OBS) <= 0.03}) -> "
              f"{'VALID' if va and vb else 'INVALID'}")
    return out


# ================================================================= R0b: CFG506's own files through this validation code
P("\n=============== R0b: CFG506's box files through the validation code ===============")
V506 = validate(lambda k: os.path.join(W506, f"cfg506_box_{k}.npz"), "CFG506", lambda k: float(JB506[k]["sham"]["m_lim_box"]))
dev = 0.0
for V in VARIANTS:
    for nm in V506[V]:
        c = JS506[V]["comparison"][nm]
        dev = max(dev, abs(V506[V][nm]["companions"]["ratio"] - c["companions"]["ratio"]), abs(V506[V][nm]["f_native"] - c["f_native"]))
check("R0b CFG506's files reproduce CFG506's committed companion ratios and f_native (F and P, every ruler) within 1e-9", dev < 1e-9, f"max |d| {dev:.1e}")

JBOX = json.load(open(os.path.join(HERE, "cfg520_box_results.json")))
def mlim_rule(rule):
    return lambda k: float(JBOX[f"sel|{k}"]["selection"][rule]["m_lim_box"])


if not MUTATE:
    # ================================================================= R0 rule (B = 17) through the CFG520 box path
    P("\n=============== R0 rule (B = 17, CFG506's occupation) via this lane's box path (reported; R0a is the load-bearing table check) ===============")
    RES["R0"] = validate(lambda k: os.path.join(WORK, f"cfg520_sel_R0_{k}.npz"), "R0", mlim_rule("R0"))
    # ================================================================= MAIN validation
    P("\n=============== VALIDATION of the recalibrated rulers (MAIN rule) ===============")
    CAL = json.load(open(os.path.join(HERE, "cfg520_calib_results.json")))
    P(f"  rule: {CAL['rule']}")
    VAL = validate(lambda k: os.path.join(WORK, f"cfg520_sel_MAIN_{k}.npz"), "MAIN", mlim_rule("MAIN"))
    RES["validation"] = VAL
    anyvalid = any(VAL["F"][nm]["valid"] for nm in VAL["F"])
    P(f"\n  frozen variant F: " + ", ".join(f"{nm} {'VALID' if VAL['F'][nm]['valid'] else 'INVALID'}" for nm in VAL["F"]))
    RES["any_valid_F"] = anyvalid

    have_ds = all(os.path.exists(os.path.join(WORK, f"cfg520_box_MAIN_{k}.npz")) for s_ in BOXSETS.values() for k in s_)
    if anyvalid and have_ds:
        # ---------------- ruler builder (CFG506's, copied)
        def ruler(name, files, which=("E", "all")):
            Bs = [load_file(f) for f in files]
            grids, vecs, covs, fgs = [], [], [], []
            for B in Bs:
                Eg = to_grid(B, tables(B, *which))
                ev = env_vectors_from_grid(Eg)
                loo = []
                for k in range(27):
                    if B[f"{CUR}_W_{which[1]}"][k].sum() <= 0:
                        continue
                    loo.append(pstack(env_vectors_from_grid(to_grid(B, tables(B, *which, loo=k))), gi, WW, ALLM))
                loo = np.array(loo); nk = len(loo)
                dev_ = loo - loo.mean(0); cov = (nk - 1) / nk * dev_.T @ dev_
                grids.append(Eg); vecs.append(ev); covs.append(cov); fgs.append(f_grid(B))
            nb = len(Bs)
            return dict(name=name, Egrid=sum(grids) / nb, ev=sum(vecs) / nb, v15=pstack(sum(vecs) / nb, gi, WW, ALLM),
                        cov=sum(covs) / nb ** 2, fgrid=sum(fgs) / nb, boxes=Bs)

        # ---------------- R0c: CFG506's files through the re-score code
        P("\n=============== R0c: CFG506's files through the re-score code ===============")
        CUR = "F"
        R6 = ruler("canonical", [os.path.join(W506, f"cfg506_box_{k}.npz") for k in BOXSETS["canonical"]])
        S6 = score_rows(R6["ev"], R6["ev"], R6["fgrid"], R6["fgrid"], R6["cov"], MODELS + REPORTED)
        ref = JS506["F"]["scores"]["canonical"]
        dev = max(max(abs(S6[f][m]["chi2_inner9"] - ref[f][m]["chi2_inner9"]), abs(S6[f][m]["chi2_15"] - ref[f][m]["chi2_15"]))
                  for f in FOOTS for m in MODELS + REPORTED)
        check("R0c CFG506's canonical F chi2 (7 rows, both footings, inner 9 and 15 bins) reproduced within 0.01", dev <= 0.01, f"max |d| {dev:.4f}")
        del R6
        for V in VARIANTS:
            CUR = V
            RV = RES.setdefault(V, {})
            P(f"\n######################## VARIANT {V}: {VARIANTS[V]} ########################")
            RUL = {}
            for nm, keys in BOXSETS.items():
                RUL[nm] = ruler(nm, [os.path.join(WORK, f"cfg520_box_MAIN_{k}.npz") for k in keys])
            CMP = {"R": Rm.tolist(), "sigma_data": SIG.tolist(), "E_cfg503_nlz": E503_P.tolist()}
            P("  R [Mpc]          : " + " ".join(f"{x:7.3f}" for x in Rm))
            P("  sigma_data       : " + " ".join(f"{x:7.3f}" for x in SIG))
            P("  CFG503 E_nlz     : " + " ".join(f"{x:7.3f}" for x in E503_P))
            for nm, Rr in RUL.items():
                v = Rr["v15"]; s = np.sqrt(np.diag(Rr["cov"]))
                P(f"  E_native {nm:9s}: " + " ".join(f"{x:7.3f}" for x in v))
                P(f"    jackknife sd   : " + " ".join(f"{x:7.3f}" for x in s))
                parts = {}
                for part, wk in (("E_cen", "cen"), ("E_sat", "sat"), ("E_src", "all")):
                    vs = []
                    for B in Rr["boxes"]:
                        Et = tables(B, part, wk)
                        if part in ("E_cen", "E_sat"):
                            Et = Et * (B[f"{CUR}_W_{wk}"].sum(0) / np.maximum(B[f"{CUR}_W_all"].sum(0), 1e-300))[..., None]
                        vs.append(pstack(env_vectors_from_grid(to_grid(B, Et)), gi, WW, ALLM))
                    parts[part] = (sum(vs) / len(vs)).tolist()
                P(f"    centrals part  : " + " ".join(f"{x:7.3f}" for x in parts["E_cen"]))
                P(f"    leaked-sat part: " + " ".join(f"{x:7.3f}" for x in parts["E_sat"]))
                P(f"    S share        : " + " ".join(f"{x:7.3f}" for x in parts["E_src"]))
                CMP[nm] = dict(E=v.tolist(), sd=s.tolist(), ratio_to_503=(v / E503_P).tolist(), diff_sigma=((v - E503_P) / SIG).tolist(), parts=parts)
            for nm in ("canonical", "alt", "DE"):
                v, v0 = RUL[nm]["v15"], RUL["S0"]["v15"]
                sdd = np.sqrt(np.diag(RUL[nm]["cov"]) + np.diag(RUL["S0"]["cov"]))
                P(f"    {nm:9s}/S0 ratio : " + " ".join(f"{x:7.3f}" for x in v / v0))
                P(f"    (TA-S0)/sig_data : " + " ".join(f"{x:+7.2f}" for x in (v - v0) / SIG))
                CMP[nm]["ratio_to_S0"] = (v / v0).tolist(); CMP[nm]["diff_S0_sigma_data"] = ((v - v0) / SIG).tolist()
                CMP[nm]["diff_S0_sd_jk"] = ((v - v0) / sdd).tolist()
            RV["comparison"] = CMP
            SC = {nm: score_rows(Rr["ev"], Rr["ev"], Rr["fgrid"], Rr["fgrid"], Rr["cov"], MODELS + REPORTED) for nm, Rr in RUL.items()}
            for nm, S_ in SC.items():
                P(f"  --- ruler {nm} ---")
                for foot in FOOTS:
                    if nm == "DE" and foot == "alt":
                        continue
                    P(f"    [{foot}] model    | inner9 chi2 (p)      | 15-bin chi2 (p)      | data-only inner9 / 15")
                    for mdl in MODELS + REPORTED:
                        s = S_[foot][mdl]
                        P(f"      {mdl:8s} | {s['chi2_inner9']:7.2f} ({s['p_inner9']:.2e}) | {s['chi2_15']:7.2f} ({s['p_15']:.2e}) | "
                          f"{s['chi2_inner9_data_only']:7.2f} / {s['chi2_15_data_only']:7.2f}" + ("   (reported)" if mdl in REPORTED else ""))
            RV["scores"] = {nm: {f: {m: {k: v for k, v in r.items() if k != "model"} for m, r in S_[f].items()} for f in S_} for nm, S_ in SC.items()}
            VER = {}
            for foot, rn in (("canonical", "canonical"), ("alt", "alt"), ("canonical", "DE")):
                valid = VAL[V][rn]["valid"]
                sc = SC[rn][foot]
                per = {m: (("PASS" if sc[m]["p_inner9"] > 0.01 else "FAIL") if valid else "NO VERDICT (ruler INVALID)") for m in MODELS}
                fits = [m for m in FRAMEWORK if sc[m]["p_inner9"] > 0.01]
                VER[f"{rn}|{foot}"] = dict(ruler_valid=valid, per_model=per, framework_fits_with_own_ruler=(bool(fits) if valid else None),
                                           framework_models_passing=fits if valid else None)
                P(f"  ruler {rn} [{foot}] {'VALID' if valid else 'INVALID'}: " + ", ".join(
                    f"{m} {per[m]} (chi2 {sc[m]['chi2_inner9']:.2f}, p {sc[m]['p_inner9']:.3f})" for m in MODELS))
                if valid and V == "F":
                    P(f"    framework fits with its own ruler on the trusted bins: {'YES via ' + ', '.join(fits) if fits else 'NO'}")
            RV["verdicts"] = VER
    elif anyvalid:
        P("\n  a ruler is VALID but the DeltaSigma-stage files are missing: run cfg520_box.py KEY ds MAIN for all six boxes, then re-run.")
        RES["rescore"] = "PENDING (DeltaSigma stage not run)"
    else:
        P("\n  NO recalibrated ruler is VALID (frozen variant F): no re-score verdict; no DeltaSigma stage is needed.")
        RES["rescore"] = "NOT RUN (no VALID ruler)"
else:
    P("\n=============== MUTATE M2X: calibration to 2x the measured parent fraction ===============")
    CM = json.load(open(os.path.join(HERE, "cfg520_calib_results_MUTATE.json")))
    P(f"  rule: {CM['rule']}")
    VM = validate(lambda k: os.path.join(WORK, f"cfg520_sel_M2X_{k}.npz"), "M2X", mlim_rule("M2X"))
    RES["M2X"] = VM
    can_valid = VM["F"]["canonical"]["valid"]
    check("MUTATE M2X: calibrating to 2x the measured parent fraction makes the canonical ruler INVALID (frozen variant F)", not can_valid,
          f"canonical companion ratio {VM['F']['canonical']['companions']['ratio']:.3f}, leaked fraction {VM['F']['canonical']['f_native']:.4f}")
    RES["label"] = None if not can_valid else "VALIDATION WITHOUT POWER"

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg520_score_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg520_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
