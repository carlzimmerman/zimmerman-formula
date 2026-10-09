#!/usr/bin/env python3
"""CFG506 scoring (FROZEN_CRITERIA.md sections 6-10; criteria commit 27a6c64ee).

Builds the native rulers from the per-box tables (cfg506_box.py), tabulates them on CFG503's (log M*, z, R) grid, validates each with the
photometric companion count (model-independent; LCDM is not required to fit), compares them with the LCDM-native terms (CFG503 E_nlz;
CFG504's committed E if present), and re-scores CFG377's stack P with every model's own profile (CFG503 tables, not edited) + the native ruler.
Verdicts on the 9 trusted bins (R <= 0.445 Mpc); 15 bins reported. Data handling, grouping and pstack copied from CFG503's cfg503_score.py.
MUTATE (CFG506_MUTATE=1, outputs *_MUTATE.*): SHUF (shuffled centres: no environment signal) and S0 (S0 ruler reproduces the LCDM-native term).
Run: nice -n 15 python3 cfg506_score.py ; CFG506_MUTATE=1 nice -n 15 python3 cfg506_score.py
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

MUTATE = os.environ.get("CFG506_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg506_work")
W503 = os.path.join(EXT, "cfg503_work")
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
FOOTS = ("canonical", "alt")
LH = 0.6736
LOG, CHK = [], {}
RES = {"lane": "CFG506", "script": "cfg506_score", "mutate": MUTATE}


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


# ------------------------------------------------------------------ data (CFG503 verbatim)
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
P(f"stack P {nL} lenses / {NG} groups; trusted bins (R <= 0.445 Mpc): {int(INN.sum())}")


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
    """per-group own vectors: (1 - f) full + f stripped (CFG503's W10 stripped tables), f on the (LMS, ZG) grid."""
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
    """Evec_*: per-group E vectors (NG x 15) under the Moster / Behroozi own path (identical for a native ruler)."""
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


# ------------------------------------------------------------------ C2: this code with CFG503's E and f reproduces CFG503's main stack-P chi2
J503 = json.load(open(os.path.join(LANES, "CFG503_two_halo_nonlinear", "cfg503_score_results.json")))["MAIN"]
E503m = env_vectors_from_grid(ET["E_moster_nlz_W10"]); E503b = env_vectors_from_grid(ET["E_behroozi_nlz_W10"])
S503 = score_rows(E503m, E503b, ET["moster_W10_f"], ET["behroozi_W10_f"], None, MODELS + REPORTED)
dmx = max(abs(S503[f][m]["chi2_15"] - J503["P"][f][m]["chi2"]) for f in FOOTS for m in MODELS + REPORTED)
check("C2 scoring code with CFG503's E_nlz and f reproduces CFG503's 14 stack-P chi2 (15 bins) within 0.01", dmx <= 0.01, f"max |d| {dmx:.4f}")
E503_P = pstack(E503m, gi, WW, ALLM)

# CFG504's committed E vector, if present
E504_P = None
f504 = os.path.join(LANES, "CFG504_smooth_halo_transition", "cfg504_score_results.json")
if os.path.exists(f504):
    try:
        J504 = json.load(open(f504))
        if "E_prim" in J504.get("MAIN", {}).get("pieces", {}):
            E504_P = np.array(J504["MAIN"]["pieces"]["E_prim"]); P("CFG504 committed E vector found: MAIN/pieces/E_prim (its primary smooth-window E, stack P, Moster)")
            RES["cfg504_reference_chi2_stackP"] = {f: {m: J504["MAIN"]["P"][f][m]["chi2"] for m in J504["MAIN"]["P"][f]} for f in ("canonical", "alt")}
    except Exception as ex_:
        P(f"CFG504 results unreadable ({ex_}); using CFG503 E_nlz as the LCDM-native reference")
EREF = E504_P if E504_P is not None else E503_P
EREF_NAME = "CFG504 E (committed)" if E504_P is not None else "CFG503 E_nlz (CFG504 E not committed when this ran)"
P(f"LCDM-native reference for MUTATE S0: {EREF_NAME}")

# ------------------------------------------------------------------ native rulers
CUR = "F"
VARIANTS = {"F": "frozen neighbour threshold (pool 5th percentile)", "P": "departure D1: pool-calibrated neighbour completeness"}
BOXSETS = {"canonical": ["TA512_can359", "TA512_can360"], "alt": ["TA512_alt359"], "DE": ["TA512_DEcan359"],
           "S0": ["S0512_359", "S0512_360"]}
ZN = np.array([0.15, 0.25, 0.35, 0.45])
JB = json.load(open(os.path.join(HERE, "cfg506_box_results.json")))


def load_box(key):
    Z = np.load(os.path.join(WORK, f"cfg506_box_{key}.npz"))
    return {k: Z[k] for k in Z.files}


def tables(B, tkey, wkey, loo=None):
    num = B[f"{CUR}_T_{tkey}"]; den = B[f"{CUR}_W_{wkey}"]
    if loo is None:
        n_, d_ = num.sum(0), den.sum(0)
    else:
        n_, d_ = num.sum(0) - num[loo], den.sum(0) - den[loo]
    return np.where(d_[..., None] > 0, n_ / np.maximum(d_[..., None], 1e-300), np.nan)      # (NB, 4, 40)


def to_grid(B, E):
    """E (NB, 4, 40) comoving z = 0 DeltaSigma [(Msun/h)/(Mpc/h)^2] at RM -> (51, 9, 120) physical Msun/Mpc^2 on (LMS, ZG, RG)."""
    VB = B["VB"]; RM = B["RM"]
    lmc = B[f"{CUR}_LMW"] / np.maximum(B[f"{CUR}_LMWW"], 1e-300)                                       # weighted bin centres (NB, 4)
    out_n = np.zeros((4, len(LMS), len(RG)))
    for n in range(4):
        xc = lmc[VB, n]; Ev = E[VB, n]                                                    # (nv, 40)
        Rp = RM / (LH * (1 + ZN[n])); Ep = Ev * LH * (1 + ZN[n]) ** 2
        Em = np.array([np.interp(LMS, xc, Ep[:, j]) for j in range(len(RM))]).T          # (51, 40), clamped outside
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


def f_grid(B, loo=None):
    FS = B[f"{CUR}_FS"].sum(0); W = B[f"{CUR}_W_all"].sum(0)
    fs = FS / np.maximum(W, 1e-300)
    VB = B["VB"]; lmc = B[f"{CUR}_LMW"] / np.maximum(B[f"{CUR}_LMWW"], 1e-300)
    gn = np.array([np.interp(LMS, lmc[VB, n], fs[VB, n]) for n in range(4)])                   # (4, 51)
    out = np.zeros((len(LMS), len(ZG)))
    for iz, z in enumerate(ZG):
        out[:, iz] = np.array([np.interp(z, ZN, gn[:, i]) for i in range(len(LMS))])
    return out


def ruler(name, keys, which=("E", "all")):
    """returns dict: Egrid, per-group vectors, stack-P 15-vector, jackknife covariance of the 15-vector, f grid, parts."""
    Bs = [load_box(k) for k in keys]
    grids, vecs, covs, fgs = [], [], [], []
    for B in Bs:
        Eg = to_grid(B, tables(B, *which))
        ev = env_vectors_from_grid(Eg); v15 = pstack(ev, gi, WW, ALLM)
        loo = []
        for k in range(27):
            if B[f"{CUR}_W_{which[1]}"][k].sum() <= 0:
                continue
            loo.append(pstack(env_vectors_from_grid(to_grid(B, tables(B, *which, loo=k))), gi, WW, ALLM))
        loo = np.array(loo); nk = len(loo)
        dev = loo - loo.mean(0); cov = (nk - 1) / nk * dev.T @ dev
        grids.append(Eg); vecs.append(ev); covs.append(cov); fgs.append(f_grid(B))
    nb = len(Bs)
    return dict(name=name, keys=keys, Egrid=sum(grids) / nb, ev=sum(vecs) / nb, v15=pstack(sum(vecs) / nb, gi, WW, ALLM),
                cov=sum(covs) / nb ** 2, fgrid=sum(fgs) / nb, boxes=Bs)


def companion_ratio(Bs, mlim_box):
    S = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
    iso = S["iso_idx"]; zl = S["z"][iso]; lml = S["logM"][iso]
    meas = S["cin"] - S["can"] * (math.pi * 0.25) / (math.pi * 20.0)
    wl = S["WW"][iso].sum(1)
    preds = []
    for B in Bs:
        ct = B[f"{CUR}_CT"].sum(0) / np.maximum(B[f"{CUR}_W_all"].sum(0), 1e-300)
        VB = B["VB"]; lmc = B[f"{CUR}_LMW"] / np.maximum(B[f"{CUR}_LMWW"], 1e-300)
        gn = np.array([np.interp(lml, lmc[VB, n], ct[VB, n]) for n in range(4)])           # (4, nlens)
        zc = np.clip(zl, ZN[0], ZN[-1]); k = np.clip(np.searchsorted(ZN, zc), 1, 3); t = (zc - ZN[k - 1]) / (ZN[k] - ZN[k - 1])
        preds.append((1 - t) * gn[k - 1, np.arange(len(zl))] + t * gn[k, np.arange(len(zl))])
    pred = sum(preds) / len(preds)
    sub = lml >= mlim_box
    r_sub = float((wl[sub] * meas[sub]).sum() / (wl[sub] * pred[sub]).sum())
    r_all = float((wl * meas).sum() / (wl * pred).sum())
    return dict(ratio=r_sub, ratio_all_lenses=r_all, meas_sub=float((wl[sub] * meas[sub]).sum() / wl[sub].sum()),
                pred_sub=float((wl[sub] * pred[sub]).sum() / wl[sub].sum()), frac_weight_sub=float(wl[sub].sum() / wl.sum()),
                meas_all=float((wl * meas).sum() / wl.sum()), pred_all=float((wl * pred).sum() / wl.sum()))


S2 = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
meas_all = float(((S2["WW"][S2["iso_idx"]].sum(1)) * (S2["cin"] - S2["can"] * 0.25 / 20.0)).sum() / S2["WW"][S2["iso_idx"]].sum())
J502 = json.load(open(os.path.join(LANES, "CFG502_two_halo_first_principles", "cfg502_env_results.json")))
check("C4 measured companion excess = CFG502's per-lens excess (stack-weighted 0.25)", abs(meas_all - 0.2537226181022062) < 1e-9,
      f"{meas_all:.10f}")

def run_variant(V):
    global CUR
    CUR = V
    RV = RES.setdefault(V, {"description": VARIANTS[V]})
    P(f"\n######################## VARIANT {V}: {VARIANTS[V]} ########################")
    avail = {k: os.path.exists(os.path.join(WORK, f"cfg506_box_{k}.npz")) for s_ in BOXSETS.values() for k in s_}
    P("boxes available: " + ", ".join(f"{k} {'yes' if v else 'NO'}" for k, v in avail.items()))
    RUL = {}
    for nm, keys in BOXSETS.items():
        if all(avail[k] for k in keys):
            t = time.time()
            RUL[nm] = ruler(nm, keys)
            mlb = max(float(JB[k]["sham"]["m_lim_box"]) for k in keys)
            RUL[nm]["m_lim_box"] = mlb
            RUL[nm]["companions"] = companion_ratio(RUL[nm]["boxes"], mlb)
            # weight of stack P below m_lim,box (clamped E)
            wP = np.array([WW[gi == g].sum() for g in range(NG)])
            RUL[nm]["stack_weight_below_mlim"] = float(wP[GS < mlb].sum() / wP.sum())
            P(f"ruler {nm}: boxes {keys}; m_lim,box {mlb:.2f} (stack-P weight below it, E clamped: {RUL[nm]['stack_weight_below_mlim']:.3f}); "
              f"built in {time.time() - t:.0f} s")
        else:
            P(f"ruler {nm}: boxes missing -> skipped")

    # ------------------------------------------------------------------ ruler comparison
    P("\n=============== RULER COMPARISON (stack P, Msun/pc^2) ===============")
    P("  R [Mpc]          : " + " ".join(f"{x:7.3f}" for x in Rm))
    P("  sigma_data       : " + " ".join(f"{x:7.3f}" for x in SIG))
    P("  CFG503 E_nlz     : " + " ".join(f"{x:7.3f}" for x in E503_P))
    if E504_P is not None:
        P("  CFG504 E         : " + " ".join(f"{x:7.3f}" for x in E504_P))
    CMP = {"R": Rm.tolist(), "sigma_data": SIG.tolist(), "E_cfg503_nlz": E503_P.tolist(), "E_cfg504": None if E504_P is None else E504_P.tolist()}
    for nm, Rr in RUL.items():
        v = Rr["v15"]; s = np.sqrt(np.diag(Rr["cov"]))
        P(f"  E_native {nm:9s}: " + " ".join(f"{x:7.3f}" for x in v))
        P(f"    jackknife sd   : " + " ".join(f"{x:7.3f}" for x in s))
        P(f"    native/CFG503  : " + " ".join(f"{x:7.2f}" for x in v / E503_P))
        P(f"    (nat-503)/sig  : " + " ".join(f"{x:+7.2f}" for x in (v - E503_P) / SIG))
        parts = {}
        for part, wk in (("E_cen", "cen"), ("E_sat", "sat"), ("E_src", "all")):
            vs = []
            for B in Rr["boxes"]:
                Et = tables(B, part, wk)
                if part in ("E_cen", "E_sat"):
                    Et = Et * (B[f"{CUR}_W_{wk}"].sum(0) / np.maximum(B[f"{CUR}_W_all"].sum(0), 1e-300))[..., None]   # contribution to E
                vs.append(pstack(env_vectors_from_grid(to_grid(B, Et)), gi, WW, ALLM))
            parts[part] = (sum(vs) / len(vs)).tolist()
        P(f"    centrals part  : " + " ".join(f"{x:7.3f}" for x in parts["E_cen"]))
        P(f"    leaked-sat part: " + " ".join(f"{x:7.3f}" for x in parts["E_sat"]))
        P(f"    S (phantom - draw) share: " + " ".join(f"{x:7.3f}" for x in parts["E_src"]))
        fP = pstack(np.repeat(np.clip(grid_interp(Rr["fgrid"], GS, GZ), 0, 1)[:, None], 15, 1), gi, WW, ALLM)[0]
        f503 = pstack(np.repeat(np.clip(grid_interp(ET["moster_W10_f"], GS, GZ), 0, 1)[:, None], 15, 1), gi, WW, ALLM)[0]
        P(f"    leaked-satellite fraction (stack-weighted): native {fP:.3f} vs CFG503 HOD {f503:.3f}")
        co = Rr["companions"]
        P(f"    companions (lenses log M* >= {Rr['m_lim_box']:.2f}, {co['frac_weight_sub']:.2f} of the weight): measured {co['meas_sub']:.4f}, "
          f"predicted {co['pred_sub']:.4f}, ratio {co['ratio']:.3f}  [all lenses: {co['meas_all']:.4f} / {co['pred_all']:.4f} = {co['ratio_all_lenses']:.3f}]")
        CMP[nm] = dict(E=v.tolist(), sd=s.tolist(), ratio_to_503=(v / E503_P).tolist(), diff_sigma=((v - E503_P) / SIG).tolist(), parts=parts,
                       f_native=float(fP), f_cfg503=float(f503), companions=co, m_lim_box=Rr["m_lim_box"],
                       stack_weight_below_mlim=Rr["stack_weight_below_mlim"])
        # box total (centrals, nothing removed), trusted only at R_com >= 2.5 cells
        vt = []
        for B in Rr["boxes"]:
            vt.append(pstack(env_vectors_from_grid(to_grid(B, tables(B, "TOT_cen", "cen"))), gi, WW, ALLM))
        vt = sum(vt) / len(vt)
        zmed = 0.30; rtr = 2.5 * float(Rr["boxes"][0]["dx"]) / (LH * (1 + zmed))
        P(f"    box TOTAL (centrals, own + env; trusted R >= {rtr:.2f} Mpc): " + " ".join(f"{x:7.3f}" for x in vt))
        CMP[nm]["box_total_centrals"] = vt.tolist(); CMP[nm]["box_total_trusted_R_min_Mpc"] = rtr
    if "S0" in RUL:
        P("  --- gravity part of the ruler difference: TA ruler vs S0 ruler (same pipeline, same galaxy-halo rule) ---")
        for nm in ("canonical", "alt", "DE"):
            if nm in RUL:
                v, v0 = RUL[nm]["v15"], RUL["S0"]["v15"]
                sdd = np.sqrt(np.diag(RUL[nm]["cov"]) + np.diag(RUL["S0"]["cov"]))
                P(f"    {nm:9s}/S0 ratio : " + " ".join(f"{x:7.3f}" for x in v / v0))
                P(f"    (TA-S0)/sig_data : " + " ".join(f"{x:+7.2f}" for x in (v - v0) / SIG))
                P(f"    (TA-S0)/sd_jk    : " + " ".join(f"{x:+7.2f}" for x in (v - v0) / sdd))
                CMP[nm]["ratio_to_S0"] = (v / v0).tolist(); CMP[nm]["diff_S0_sigma_data"] = ((v - v0) / SIG).tolist()
                CMP[nm]["diff_S0_sd_jk"] = ((v - v0) / sdd).tolist()
    RV["comparison"] = CMP

    if not MUTATE:
        # ------------------------------------------------------------------ re-score
        P("\n=============== KiDS RE-SCORE (stack P; own (CFG503 tables) + ruler; SHMR rank-one on own; ruler covariance added) ===============")
        SC = {}
        for nm, Rr in RUL.items():
            S_ = score_rows(Rr["ev"], Rr["ev"], Rr["fgrid"], Rr["fgrid"], Rr["cov"], MODELS + REPORTED)
            SC[nm] = S_
        S_ref = score_rows(E503m, E503b, ET["moster_W10_f"], ET["behroozi_W10_f"], None, MODELS + REPORTED)
        SC["LCDM_native_CFG503"] = S_ref
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
        RV["scores"] = SC
        # ------------------------------------------------------------------ verdicts
        P("\n=============== VERDICT (frozen rule) ===============")
        VER = {}
        for foot, rn in (("canonical", "canonical"), ("alt", "alt"), ("canonical", "DE")):
            if rn not in RUL:
                continue
            co = RUL[rn]["companions"]["ratio"]
            valid = 0.67 <= co <= 1.5
            sc = SC[rn][foot]
            per = {m: (("PASS" if sc[m]["p_inner9"] > 0.01 else "FAIL") if valid else "NO VERDICT (ruler INVALID)") for m in MODELS}
            fits = [m for m in FRAMEWORK if sc[m]["p_inner9"] > 0.01]
            VER[f"{rn}|{foot}"] = dict(ruler_valid=valid, companion_ratio=co, per_model=per, framework_fits_with_own_ruler=(bool(fits) if valid else None),
                                       framework_models_passing=fits if valid else None,
                                       chi2_inner9={m: sc[m]["chi2_inner9"] for m in MODELS + REPORTED},
                                       p_inner9={m: sc[m]["p_inner9"] for m in MODELS + REPORTED})
            P(f"  ruler {rn} [{foot}]: companion ratio {co:.3f} -> ruler {'VALID' if valid else 'INVALID'}; "
              + ", ".join(f"{m} {per[m]} (chi2 {sc[m]['chi2_inner9']:.2f}, p {sc[m]['p_inner9']:.3f})" for m in MODELS))
            if valid:
                P(f"    framework fits with its own ruler on the trusted bins: {'YES via ' + ', '.join(fits) if fits else 'NO'}")
            else:
                P(f"    framework-fit question: (reported only, ruler INVALID) passing on inner 9: {fits if fits else 'none'}")
        RV["verdicts"] = VER
    else:
        # ------------------------------------------------------------------ MUTATE SHUF and S0
        P("\n=============== MUTATE ===============")
        for nm in ("canonical", "alt", "DE", "S0"):
            if nm not in RUL:
                continue
            Rr = RUL[nm]
            def vec(tk, wk, B, loo=None):
                return pstack(env_vectors_from_grid(to_grid(B, tables(B, tk, wk, loo))), gi, WW, ALLM)
            sh, hs, en, hn, sds = [], [], [], [], []
            for B in Rr["boxes"]:
                # the box stores +DeltaSigma of the uniform rho_bar sphere (T_H / T_HSHUF); the hole H of the criteria is its negative
                # (fix 10-08: the first MUTATE run used +DeltaSigma as H, i.e. the wrong sign; kept in the README)
                sh.append(vec("SHUF", "shuf", B)); hs.append(-vec("HSHUF", "shuf", B)); en.append(vec("E", "all", B)); hn.append(-vec("H", "all", B))
                loo = np.array([vec("SHUF", "shuf", B, k) + vec("HSHUF", "shuf", B, k) for k in range(27)])
                dev = loo - loo.mean(0); sds.append(26 / 27 * (dev ** 2).sum(0))
            nb = len(Rr["boxes"])
            dsh = (sum(sh) - sum(hs)) / nb; den = (sum(en) - sum(hn)) / nb; sd = np.sqrt(sum(sds)) / nb
            okbin = (np.abs(dsh) < 3 * sd) | (np.abs(dsh) < 0.1 * SIG)
            rmean = float(np.mean(np.abs(dsh)) / max(np.mean(np.abs(den)), 1e-30))
            P(f"  [{nm}] E_shuf - H : " + " ".join(f"{x:+7.3f}" for x in dsh))
            P(f"  [{nm}] sd_jk      : " + " ".join(f"{x:7.3f}" for x in sd))
            P(f"  [{nm}] E_nat - H  : " + " ".join(f"{x:+7.3f}" for x in den))
            check(f"MUTATE SHUF [{V}] [{nm}]: shuffled centres carry no environment (every bin < 3 sd_jk or < 0.1 sigma_data; mean ratio < 0.1)",
                  bool(okbin.all() and rmean < 0.1), f"bins ok {int(okbin.sum())}/15; mean |E_shuf - H| / mean |E_nat - H| {rmean:.3f}",
                  lb=(nm == "canonical"))
            RV[f"SHUF_{nm}"] = dict(E_shuf_minus_H=dsh.tolist(), sd=sd.tolist(), E_nat_minus_H=den.tolist(), ratio=rmean)
        if "S0" in RUL:
            v = RUL["S0"]["v15"]
            okb = np.abs(v - EREF) <= np.maximum(0.3 * np.abs(EREF), SIG)
            P("  S0 native E : " + " ".join(f"{x:7.3f}" for x in v))
            P("  reference   : " + " ".join(f"{x:7.3f}" for x in EREF) + f"   ({EREF_NAME})")
            check(f"MUTATE S0 [{V}]: the ruler built from the S0 boxes reproduces the LCDM-native term (|dE| <= max(0.3|E_ref|, sigma_data) in >= 12/15 bins)",
                  int(okb.sum()) >= 12, f"{int(okb.sum())}/15 bins within; reference = {EREF_NAME}")
            RV["S0_vs_ref"] = dict(E_S0=v.tolist(), E_ref=EREF.tolist(), ref=EREF_NAME, bins_ok=int(okb.sum()))



for V_ in VARIANTS:
    run_variant(V_)

if not MUTATE:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(os.path.join(HERE, "figs"), exist_ok=True)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax_, V_ in zip(axs, VARIANTS):
        if V_ not in RES or "comparison" not in RES[V_]:
            continue
        c = RES[V_]["comparison"]
        ax_.fill_between(Rm, -SIG, SIG, color="0.85", label="+-1 sigma_data")
        ax_.plot(Rm, E503_P, "k-", lw=1.5, label="LCDM-native (CFG503 E_nlz)")
        for nm, col in (("canonical", "C0"), ("alt", "C1"), ("DE", "C2"), ("S0", "C3")):
            if nm in c:
                ax_.errorbar(Rm, c[nm]["E"], c[nm]["sd"], fmt="o-", ms=3, lw=1, color=col, label=f"native {nm}")
        ax_.set_xscale("log"); ax_.axhline(0, color="k", lw=0.5); ax_.axvline(0.445, color="k", ls=":", lw=0.8)
        ax_.set_xlabel("R [Mpc]"); ax_.set_title(f"variant {V_}: {VARIANTS[V_][:46]}", fontsize=8)
    axs[0].set_ylabel("environment term E, stack P [Msun/pc^2]"); axs[0].legend(fontsize=6.5)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "figs", "ruler_comparison.png"), dpi=110); plt.close(fig)

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg506_score_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg506_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
