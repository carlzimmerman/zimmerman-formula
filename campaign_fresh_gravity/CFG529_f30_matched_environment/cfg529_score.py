#!/usr/bin/env python3
"""CFG529 stage 2 (FROZEN_CRITERIA.md, criteria commit 33969d1a7): the f30-matched environment term.
Constructions: A = CFG503 (sharp r_ta boundary, halofit x zeta two-halo, stripping, SHMR rank-one); B = CFG504 (smooth DK14 transition,
primary x_t).  The HOD leaked-satellite grid of each window K (W10 stack P, W30 f30, ALL) is rescaled to the MEASURED fraction (CFG519 JSON:
0.2234 / 0.1686 / parent 0.3134) by CFG520 part B's rule.  Gates G1m, G2f (required), G3m (reported, labelled); then, per valid construction,
the census edge on f30 (Delta vs the best sharp edge x >= 0.2 <= 4 AND p > 0.01) and the record's model set (p > 0.01), both footings.
Inputs: CFG503 / CFG504 env + own tables, CFG525 stage-1 tables (W10 sharp), this lane's cfg529_tables.npz, committed JSON (read-only).
MUTATE (CFG529_MUTATE=1, outputs *_MUTATE.*): T1 f_ret = 1 must fail; T2 stack-P environment reproduces CFG525's fixed-environment fail;
T3 mismatched (W10) environment on f30 visible; T4 zero leakage visible.
Run: nice -n 10 python3 cfg529_score.py ; CFG529_MUTATE=1 nice -n 10 python3 cfg529_score.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import json, time, warnings
import numpy as np
from scipy import stats
from scipy.interpolate import RegularGridInterpolator

warnings.filterwarnings("ignore", category=RuntimeWarning)                  # the known Accelerate matmul quirk; finiteness checked below
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
for p in (os.path.join(LANES, "CFG100_kids_mass_rederivation"), os.path.join(LANES, "CFG495_drawdown_shell")):
    sys.path.insert(0, p)
import cfg100_lib as C                                                       # noqa: E402  (read-only)
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only)
try:
    os.nice(10)
except OSError:
    pass
MUTATE = os.environ.get("CFG529_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
CONS = ("A", "B")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG, CHK = [], {}
RES = {"lane": "CFG529", "script": "cfg529_score", "mutate": MUTATE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
# ------------------------------------------------------------------ measured fractions (CFG519 JSON)
J519 = json.load(open(os.path.join(LANES, "CFG519_kids_gama_satellite_fraction", "cfg519_satfrac_results.json")))
F_MEAS = {"W10": J519["main"]["f_IC"], "W30": J519["main"]["f30"], "ALL": J519["main"]["f_ALL_parent"]}
SIG30 = float(np.hypot(J519["sigma_stat"]["f30"], J519["sigma_sys"]))
P(f"measured leaked fractions (CFG519): W10 {F_MEAS['W10']:.6f}, W30 {F_MEAS['W30']:.6f} (sigma_stat {J519['sigma_stat']['f30']:.5f}, "
  f"sigma_tot declared {SIG30:.5f}), ALL parent {F_MEAS['ALL']:.6f}")
RES["f_meas"] = F_MEAS; RES["sigma_tot_f30"] = SIG30

# ------------------------------------------------------------------ data (CFG503 / CFG504 verbatim)
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2


def esd_full_loo(WG_, WW_, patch_, mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch_[mask], weights=WG_[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch_[mask], weights=WW_[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)


lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
F30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
nL = len(lens["z"]); ALLM = np.ones(nL, bool)
ET3 = np.load(os.path.join(EXT, "cfg503_work", "cfg503_env_table.npz"))
OT3 = np.load(os.path.join(EXT, "cfg503_work", "cfg503_own_tables.npz"))
ET4 = np.load(os.path.join(EXT, "cfg504_work", "cfg504_env_table.npz"))
OT4 = np.load(os.path.join(EXT, "cfg504_work", "cfg504_own_tables.npz"))
TB = np.load(os.path.join(EXT, "cfg525_work", "cfg525_tables.npz"))
T29 = np.load(os.path.join(EXT, "cfg529_work", "cfg529_tables.npz"))
gi, GM, GZ, GS = OT3["gi"], OT3["GM"], OT3["GZ"], OT3["GS"]; NG = len(GM)
assert np.array_equal(gi, OT4["gi"]) and np.array_equal(GM, OT4["GM"])
S = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
WWA, WGA, pA = S["WW"], S["WG"], S["patch_all"]
giA, GMA, GZA, GSA = OT3["giA"], OT3["GMA"], OT3["GZA"], OT3["GSA"]
LMS, ZG, RG = ET3["LMS"], ET3["ZG"], ET3["RG"]; LRG = np.log(RG)
assert np.array_equal(LMS, ET4["LMS"]) and np.array_equal(ZG, ET4["ZG"]) and np.array_equal(RG, ET4["RG"])
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
Rm = np.array(J377["primary"]["meanR"]); INN = Rm <= 0.445
d, Cv = esd_full_loo(WG, WW, patch, ALLM)
dref = np.array(J377["primary"]["esd"])
check("K1 stack P data vector = CFG377 primary (1e-10)", np.max(np.abs(d / dref - 1)) < 1e-10, f"max rel {np.max(np.abs(d / dref - 1)):.1e}")
d30, C30 = esd_full_loo(WG, WW, patch, F30)
dA, CA = esd_full_loo(WGA, WWA, pA, np.ones(len(WWA), bool))
RmA = (WWA * np.sqrt(C.G_MPC * S["Mgal"][:, None] / np.sqrt(C.GEDGE_K[:-1] * C.GEDGE_K[1:])[None, :])).sum(0) / WWA.sum(0)
INA = RmA <= 0.445
SAMPLES = {"P": (d, Cv, INN), "f30": (d30, C30, INN), "ALL": (dA, CA, INA)}
SIG = {k: np.sqrt(np.diag(v[1])) for k, v in SAMPLES.items()}
GSEL = T29["GSEL"]
P(f"stack P {nL} lenses / {NG} groups; f30 {int(F30.sum())} lenses / {len(GSEL)} groups; ALL {len(WWA)} lenses / {len(GMA)} groups")
CAL = json.load(open(os.path.join(LANES, "CFG504_smooth_halo_transition", "cfg504_calib_results.json")))["primary"]
P(f"construction B: x_t primary {CAL['x_t']:.4f}")


# ------------------------------------------------------------------ group geometry and stacking
class GSet:
    def __init__(self, name, gi_, GM_, GZ_, GS_, WW_):
        self.name, self.gi, self.GM, self.GZ, self.GS, self.WW = name, gi_, GM_, GZ_, GS_, WW_
        self.NG = len(GM_)

    def interp(self, tab):
        f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
        return f(np.c_[np.clip(self.GS, LMS[0], LMS[-1]), np.clip(self.GZ, ZG[0], ZG[-1])])

    def stack(self, tab, mask=None):
        mask = np.ones(len(self.gi), bool) if mask is None else mask
        out = np.zeros(15)
        for k in range(15):
            w = np.bincount(self.gi[mask], weights=self.WW[mask, k], minlength=self.NG)
            out[k] = (w @ tab[:, k]) / w.sum()
        return out

    def fstack(self, fgrid, mask=None, conv="bin0"):
        fg = np.clip(self.interp(np.clip(fgrid, 0, 1)), 0, 1)
        mask = np.ones(len(self.gi), bool) if mask is None else mask
        wt = self.WW[mask, 0] if conv == "bin0" else self.WW[mask].sum(1)
        w = np.bincount(self.gi[mask], weights=wt, minlength=self.NG)
        return float(w @ fg / w.sum())


GP = GSet("P", gi, GM, GZ, GS, WW)
GA = GSet("ALL", giA, GMA, GZA, GSA, WWA)
SMP = {"P": (GP, ALLM, "W10"), "f30": (GP, F30, "W30"), "ALL": (GA, None, "ALL")}

# ------------------------------------------------------------------ environment grids
XF3 = {}
for s in SHMRS:
    for K in ("W10", "W30", "ALL"):
        f = ET3[f"{s}_{K}_f"]; E = ET3[f"E_{s}_nlz_{K}"]; H = ET3[f"{s}_HOLE"]; S2 = ET3[f"{s}_S2H_nlz"]; bc = ET3[f"{s}_{K}_bc"]
        assert np.all(f > 0)
        XF3[(s, K)] = (E - H - bc[..., None] * S2) / f[..., None]


def relmax(a, b): return float(np.max(np.abs(a - b) / (np.abs(b) + 1e3)))


def Egrid(cons, s, K, fg):
    f = np.clip(fg, 0, 1)[..., None]
    if cons == "A":
        return ET3[f"{s}_HOLE"] + ET3[f"{s}_{K}_bc"][..., None] * ET3[f"{s}_S2H_nlz"] + f * XF3[(s, K)]
    bc = ET4[f"{s}_{K}_bc"][..., None]; bh = ET4[f"{s}_{K}_bh"][..., None]; SS = ET4[f"{s}_SS_prim"]
    return ET4[f"{s}_HS_prim"] + (1 - f) * bc * SS + f * (ET4[f"{s}_{K}_Thost"] + bh * SS)


rb = 0.0
for s in SHMRS:
    for K in ("W10", "W30", "ALL"):
        rb = max(rb, relmax(Egrid("A", s, K, ET3[f"{s}_{K}_f"]), ET3[f"E_{s}_nlz_{K}"]))
check("K2a construction A with the HOD f rebuilds CFG503's committed E_nlz tables (W10 / W30 / ALL; 1e-9 rel, 1e3 floor)", rb < 1e-9, f"{rb:.1e}")
assert all(np.array_equal(ET3[f"{s}_{K}_f"], ET4[f"{s}_{K}_f"]) for s in SHMRS for K in ("W10", "W30", "ALL"))

_EC = {}


def evec(gset, cons, s, K, fg, tag):
    k = (gset.name, cons, s, K, tag)
    if k not in _EC:
        Eg = gset.interp(Egrid(cons, s, K, fg)); out = np.zeros((gset.NG, 15))
        for g in range(gset.NG):
            out[g] = LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), gset.GM[g])
        _EC[k] = out
    return _EC[k]


# ------------------------------------------------------------------ f-grid scenarios
def scaled(sample, s, fmeas, conv="bin0"):
    gset, mask, K = SMP[sample]
    f = ET3[f"{s}_{K}_f"]
    X = gset.fstack(f, mask, conv)
    sc = fmeas / X
    return np.clip(sc * f, 0, 1), sc, X


SCAL = {}
for sample, K in (("P", "W10"), ("f30", "W30"), ("ALL", "ALL")):
    for s in SHMRS:
        fg, sc, X = scaled(sample, s, F_MEAS[K])
        SCAL[(sample, s)] = dict(fg=fg, s=sc, X=X)
        P(f"  scaling {sample:4s} ({K}) {s:8s}: HOD stack-weighted f X = {X:.5f} -> s = {sc:.4f}; scaled f' = "
          f"{SMP[sample][0].fstack(fg, SMP[sample][1]):.6f}")
k7 = max(abs(SMP[smp][0].fstack(SCAL[(smp, s)]["fg"], SMP[smp][1]) - F_MEAS[SMP[smp][2]]) for smp in ("P", "f30", "ALL") for s in SHMRS)
check("K7 scaled grids give stack-weighted f' = f_meas within 1e-9 (no clipping bias)", k7 < 1e-9, f"max |d| {k7:.1e}")
RES["scaling"] = {f"{k[0]}|{k[1]}": dict(s=v["s"], X=v["X"]) for k, v in SCAL.items()}


# ------------------------------------------------------------------ own profiles
MODELS = ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD")
REPORTED = ("F_NODD", "LAW_X05")


def own_rec(cons, sample, foot, model, s, K, fg_own):
    """record model own vector per group: (1 - f) full + f tr_K."""
    gset = SMP[sample][0]
    fo = np.clip(gset.interp(np.clip(fg_own, 0, 1)), 0, 1)[:, None]

    def one(m):
        if sample == "ALL":
            base = "A|LCDM|" if cons == "A" else "A|LCDM|prim|"
        else:
            base = f"P|{foot}|{m}|" if cons == "A" else f"P|{foot}|{m}|prim|"
        OT = OT3 if cons == "A" else OT4
        return (1 - fo) * OT[base + f"full_{s}"] + fo * OT[base + f"tr_{s}_{K}"]
    if model == "F_DD":
        return one("F_NODD") + one("PROP")
    return one(model)


def edge_tabs(cons, foot, kind, idx, s, K):
    """census / node (index idx) / f_ret = 1 tables: returns (full, tr) per group for SHMR s and stripping window K."""
    if K == "W10" and cons == "A":                                            # CFG525's stage-1 tables
        if kind == "node":
            j = int(np.argmin(np.abs(TB["XN"] - T29["XN"][idx])))
            return TB[f"{foot}|node|full"][:, j, :], TB[f"{foot}|node|tr_{s}"][:, j, :]
        return TB[f"{foot}|dir|{kind}|full"], TB[f"{foot}|dir|{kind}|tr_{s}"]
    pre = f"{foot}|node|" if kind == "node" else f"{foot}|dir|{kind}|"
    sl = (slice(None), idx) if kind == "node" else (slice(None),)
    if cons == "A":
        return T29[pre + "full"][sl], T29[pre + f"tr_{s}_{K}"][sl]
    assert K == "W30"
    return T29[pre + f"prim_full_{s}"][sl], T29[pre + f"prim_tr_{s}_{K}"][sl]


def chi2c(dv_, C_, h, m, delta=None):
    Ct = C_ / h + (np.outer(delta, delta) if delta is not None else 0.0)
    r = dv_ - m
    return float(r @ np.linalg.solve(Ct, r))


def score_vecs(sample, mM, mB):
    dv_, C_, inn = SAMPLES[sample]; ou = ~inn
    dl = mB - mM
    c_ = chi2c(dv_, C_, hart(15), mM, dl)
    return dict(chi2=c_, p=float(stats.chi2.sf(c_, 15)),
                chi2_inner9=chi2c(dv_[inn], C_[np.ix_(inn, inn)], hart(int(inn.sum())), mM[inn], dl[inn]),
                chi2_outer6=chi2c(dv_[ou], C_[np.ix_(ou, ou)], hart(int(ou.sum())), mM[ou], dl[ou]),
                chi2_data_only_moster=chi2c(dv_, C_, hart(15), mM), model=mM.tolist(), model_behroozi=mB.tolist())


def env_cfg(cons, sample, fE, fO, tag, K=None):
    """an environment configuration: per SHMR the E-grid f and the own-mixing f; K = window of E / stripping."""
    return dict(cons=cons, sample=sample, fE=fE, fO=fO, tag=tag, K=K or SMP[sample][2])


def model_score(ec, model, foot):
    gset, mask, _ = SMP[ec["sample"]]; K = ec["K"]
    m = {}
    for s in SHMRS:
        E = evec(gset, ec["cons"], s, K, ec["fE"][s], ec["tag"] + f"|{K}")
        own = own_rec(ec["cons"], ec["sample"], foot, model, s, K, ec["fO"][s])
        m[s] = gset.stack(own + E, mask)
    return score_vecs(ec["sample"], m["moster"], m["behroozi"])


def edge_score(ec, foot, kind, idx=None):
    gset, mask, _ = SMP[ec["sample"]]; K = ec["K"]
    m = {}
    for s in SHMRS:
        E = evec(gset, ec["cons"], s, K, ec["fE"][s], ec["tag"] + f"|{K}")
        fo = np.clip(gset.interp(np.clip(ec["fO"][s], 0, 1)), 0, 1)[:, None]
        full, tr = edge_tabs(ec["cons"], foot, kind, idx, s, K)
        tab = (1 - fo) * full + fo * tr + E
        tab = np.where(np.isfinite(tab), tab, 0.0)                            # non-f30 groups carry NaN in the W30 tables (zero weight)
        m[s] = gset.stack(tab, mask)
    return score_vecs(ec["sample"], m["moster"], m["behroozi"])


NODES = T29["XN"]
SEL = [j for j, x in enumerate(NODES) if x >= 0.2 - 1e-12]


def edge_block(ec, foot, kinds=("census",)):
    nodes = [edge_score(ec, foot, "node", j) for j in SEL]
    jb = int(np.argmin([n["chi2"] for n in nodes]))
    out = dict(best_x=float(NODES[SEL[jb]]), chi2_best=nodes[jb]["chi2"], node_chi2={f"{NODES[j]:.2f}": nodes[i]["chi2"] for i, j in enumerate(SEL)},
               range_chi2=float(max(n["chi2"] for n in nodes) - min(n["chi2"] for n in nodes)))
    for kd in kinds:
        r_ = edge_score(ec, foot, kd)
        r_["Delta"] = r_["chi2"] - out["chi2_best"]
        r_["PASS"] = bool(r_["Delta"] <= 4.0 and r_["p"] > 0.01)
        out[kd] = r_
    return out


HOD = {smp: {s: ET3[f"{s}_{SMP[smp][2]}_f"] for s in SHMRS} for smp in ("P", "f30", "ALL")}
MEAS = {smp: {s: SCAL[(smp, s)]["fg"] for s in SHMRS} for smp in ("P", "f30", "ALL")}

# ------------------------------------------------------------------ controls K2-K6
P("\n== controls ==")
J503 = json.load(open(os.path.join(LANES, "CFG503_two_halo_nonlinear", "cfg503_score_results.json")))["MAIN"]
J504 = json.load(open(os.path.join(LANES, "CFG504_smooth_halo_transition", "cfg504_score_results.json")))["MAIN"]
J520 = json.load(open(os.path.join(LANES, "CFG520_native_ruler_recalibrated", "cfg520_partB_results.json")))["CFG503"]
J525 = json.load(open(os.path.join(LANES, "CFG525_kids_alt_footing_miss", "cfg525_score_results.json")))
for cons, J, tag, kname in (("A", J503, "hod", "K2"), ("B", J504, "hod", "K5")):
    dmx = 0.0
    for foot in FOOTS:
        for m in MODELS + REPORTED:
            dmx = max(dmx, abs(model_score(env_cfg(cons, "P", HOD["P"], HOD["P"], tag), m, foot)["chi2"] - J["P"][foot][m]["chi2"]))
    g2 = model_score(env_cfg(cons, "f30", HOD["f30"], HOD["f30"], tag), "LCDM", "canonical")["chi2"]
    g3 = model_score(env_cfg(cons, "ALL", HOD["ALL"], HOD["ALL"], tag), "LCDM", "canonical")["chi2"]
    d2, d3 = abs(g2 - J["f30"]["canonical"]["LCDM"]["chi2"]), abs(g3 - J["ALL"]["canonical"]["LCDM"]["chi2"])
    check(f"{kname} construction {cons} with the HOD f reproduces CFG50{3 if cons == 'A' else 4}'s 14 stack-P chi2, f30 and ALL LCDM within 0.01",
          max(dmx, d2, d3) <= 0.01, f"stack P max |d| {dmx:.4f}; f30 {g2:.3f} vs {J['f30']['canonical']['LCDM']['chi2']:.3f}; "
          f"ALL {g3:.3f} vs {J['ALL']['canonical']['LCDM']['chi2']:.3f}")
ecP_A = env_cfg("A", "P", MEAS["P"], MEAS["P"], "meas")
ref = J520["scaled (primary: E and own mixing)"]["scores"]
dmx = max(abs(model_score(ecP_A, m, f)["chi2"] - ref[f][m]["chi2"]) for f in FOOTS for m in MODELS + REPORTED)
dsc = max(abs(SCAL[("P", "moster")]["s"] - J520["scale_moster"]), abs(SCAL[("P", "behroozi")]["s"] - J520["scale_behroozi"]))
check("K3 construction A with the W10 measured scaling reproduces CFG520 part B's 14 scaled stack-P chi2 within 0.01 (s within 1e-4)",
      dmx <= 0.01 and dsc <= 1e-4, f"max |d| {dmx:.4f}; s diff {dsc:.1e}; LCDM {model_score(ecP_A, 'LCDM', 'canonical')['chi2']:.3f}")
K4 = {f: edge_block(ecP_A, f) for f in FOOTS}
k4 = max(max(abs(K4[f]["census"]["Delta"] - J525["direct"]["census"][f]["D_H3"]), abs(K4[f]["chi2_best"] - J525["best_x"][f"{f}|P"]["H3"]["chi2"]))
         for f in FOOTS)
check("K4 construction A, stack P, W10 measured: direct census Delta and best-x chi2 reproduce CFG525's H3 within 0.01", k4 <= 0.01,
      f"census Delta {K4['canonical']['census']['Delta']:+.3f} / {K4['alt']['census']['Delta']:+.3f} (CFG525 "
      f"{J525['direct']['census']['canonical']['D_H3']:+.3f} / {J525['direct']['census']['alt']['D_H3']:+.3f}); best x "
      f"{K4['canonical']['best_x']:.2f}/{K4['alt']['best_x']:.2f} chi2 {K4['canonical']['chi2_best']:.3f}/{K4['alt']['chi2_best']:.3f}")
RES["K4_stackP_constructionA"] = {f: {k: v for k, v in K4[f].items() if k != "node_chi2"} for f in FOOTS}
# K6 new tables vs CFG525 (sharp full / tr W10) and vs CFG504 EDGE prim
k6a = 0.0
for foot in FOOTS:
    for j, x in enumerate(NODES):
        jj = int(np.argmin(np.abs(TB["XN"] - x)))
        assert abs(TB["XN"][jj] - x) < 1e-12
        for v, vb in (("full", "full"), ("tr_moster_W10", "tr_moster"), ("tr_behroozi_W10", "tr_behroozi")):
            a = T29[f"{foot}|node|{v}"][GSEL, j]; b = TB[f"{foot}|node|{vb}"][GSEL, jj]
            k6a = max(k6a, float(np.max(np.abs(a - b) / (np.abs(b) + 1e-3))))
    for nm in ("census", "one"):
        for v, vb in (("full", "full"), ("tr_moster_W10", "tr_moster"), ("tr_behroozi_W10", "tr_behroozi")):
            a = T29[f"{foot}|dir|{nm}|{v}"][GSEL]; b = TB[f"{foot}|dir|{nm}|{vb}"][GSEL]
            k6a = max(k6a, float(np.max(np.abs(a - b) / (np.abs(b) + 1e-3))))
k6b = 0.0
for foot in FOOTS:
    for s in SHMRS:
        for v in (f"full_{s}", f"tr_{s}_W30"):
            a = T29[f"K6|{foot}|{v}"]; b = OT4[f"P|{foot}|EDGE|prim|{v}"][T29["K6G"]]
            k6b = max(k6b, float(np.max(np.abs(a - b) / np.abs(b))))
fin = all(np.all(np.isfinite(T29[k][GSEL])) for k in T29.files if "|node|" in k or "|dir|" in k)
check("K6 new tables: sharp full / tr_W10 rows = CFG525's (1e-9 rel, 1e-3 floor); windowing path on the 5.85 r_M EDGE = CFG504's "
      "EDGE|prim tables for 20 groups (1e-9 rel); all f30-group rows finite", k6a < 1e-9 and k6b < 1e-9 and fin,
      f"vs CFG525 {k6a:.1e}; vs CFG504 EDGE prim {k6b:.1e}; finite {fin}")

# ------------------------------------------------------------------ main run
EC30 = {c: env_cfg(c, "f30", MEAS["f30"], MEAS["f30"], "meas") for c in CONS}


def gates(cons):
    g1 = model_score(env_cfg(cons, "P", MEAS["P"], MEAS["P"], "meas"), "LCDM", "canonical")
    g2 = model_score(EC30[cons], "LCDM", "canonical")
    g3 = model_score(env_cfg(cons, "ALL", MEAS["ALL"], MEAS["ALL"], "meas"), "LCDM", "canonical")
    G = dict(G1m=dict(chi2=g1["chi2"], p=g1["p"], passed=g1["p"] > 0.01, inner9=g1["chi2_inner9"], outer6=g1["chi2_outer6"]),
             G2f=dict(chi2=g2["chi2"], p=g2["p"], passed=g2["p"] > 0.01, inner9=g2["chi2_inner9"], outer6=g2["chi2_outer6"]),
             G3m=dict(chi2=g3["chi2"], p=g3["p"], passed=g3["p"] > 0.001, inner9=g3["chi2_inner9"], outer6=g3["chi2_outer6"]))
    G["valid"] = bool(G["G1m"]["passed"] and G["G2f"]["passed"])
    return G, (g1, g2, g3)


def rescore(ec, label, verbose=True):
    """record models + census edge on the configuration's sample, both footings."""
    out = {}
    for foot in FOOTS:
        rows = {m: model_score(ec, m, foot) for m in MODELS + REPORTED}
        eb = edge_block(ec, foot)
        rows["CENSUS"] = eb["census"]
        best5 = min(MODELS, key=lambda k: rows[k]["chi2"])
        best6 = min(MODELS + ("CENSUS",), key=lambda k: rows[k]["chi2"])
        for m in rows:
            rows[m]["minus_best_i_v"] = rows[m]["chi2"] - rows[best5]["chi2"]
            rows[m]["minus_best_with_census"] = rows[m]["chi2"] - rows[best6]["chi2"]
            rows[m]["pass_p"] = bool(rows[m]["p"] > 0.01)
        out[foot] = dict(rows=rows, edge_ref=dict(best_x=eb["best_x"], chi2_best=eb["chi2_best"], range_chi2=eb["range_chi2"],
                                                  node_chi2=eb["node_chi2"]), best_i_v=best5, best_with_census=best6)
    if verbose:
        P(f"\n  --- {label} ---")
        for foot in FOOTS:
            o = out[foot]
            P(f"    [{foot}] best sharp edge x = {o['edge_ref']['best_x']:.2f} (chi2 {o['edge_ref']['chi2_best']:.2f}; node range "
              f"{o['edge_ref']['range_chi2']:.1f}); best of (i)-(v): {o['best_i_v']}")
            P("      model    | chi2/15 (p)          | inner9 outer6 | - best(i-v) | p>0.01")
            for m in ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD", "CENSUS", "F_NODD", "LAW_X05"):
                r_ = o["rows"][m]
                ex = f"  Delta vs best edge {r_['Delta']:+.2f} -> {'PASS' if r_['PASS'] else 'FAIL'}" if m == "CENSUS" else ""
                P(f"      {m:8s} | {r_['chi2']:8.2f} ({r_['p']:.2e}) | {r_['chi2_inner9']:6.2f} {r_['chi2_outer6']:6.2f} | "
                  f"{r_['minus_best_i_v']:+9.2f} | {'PASS' if r_['pass_p'] else 'FAIL'}{ex}" + ("   (reported)" if m in REPORTED else ""))
    return out


if MUTATE:
    P("\n== MUTATE ==")
    t1 = {}
    for c in CONS:
        for foot in FOOTS:
            eb = edge_block(EC30[c], foot, kinds=("one",))
            t1[(c, foot)] = eb["one"]["Delta"]
    check("T1 f_ret = 1 in the f30-matched environment FAILS (Delta > 4) on both footings in both constructions", all(v > 4 for v in t1.values()),
          "; ".join(f"{c} {f}: {v:+.2f}" for (c, f), v in t1.items()))
    t2 = all(K4[f]["census"]["Delta"] > 4 for f in FOOTS) and k4 <= 0.01
    check("T2 stack-P environment (W10, 0.2234) on stack P reproduces CFG525's fixed-environment census FAIL", t2,
          f"{K4['canonical']['census']['Delta']:+.3f} / {K4['alt']['census']['Delta']:+.3f}")
    # T3 mismatched window: W10 E + W10 stripping + 0.2234 scaling, on the f30 data (construction A; CFG525 tables for W10 rows)
    ecmis = env_cfg("A", "f30", MEAS["P"], MEAS["P"], "meas_mis", K="W10")
    lm_mis = model_score(ecmis, "LCDM", "canonical"); lm_ok = model_score(EC30["A"], "LCDM", "canonical")
    dmis = float(np.max(np.abs(np.array(lm_mis["model"]) - np.array(lm_ok["model"])) / SIG["f30"]))
    mis = {f: edge_block(ecmis, f) for f in FOOTS}
    check("T3 mismatched stack-P environment on f30 differs from the matched one by > 0.5 sigma_f30 in some LCDM bin", dmis > 0.5,
          f"max |dm| / sigma = {dmis:.2f}; mismatched: LCDM chi2 {lm_mis['chi2']:.2f} (matched {lm_ok['chi2']:.2f}); census Delta "
          f"{mis['canonical']['census']['Delta']:+.2f} / {mis['alt']['census']['Delta']:+.2f}")
    RES["T3_mismatched"] = dict(max_dsig=dmis, LCDM=lm_mis["chi2"], census={f: dict(Delta=mis[f]["census"]["Delta"], p=mis[f]["census"]["p"],
                                                                                    best_x=mis[f]["best_x"]) for f in FOOTS})
    zero = {s: np.zeros_like(ET3[f"{s}_W30_f"]) for s in SHMRS}
    RES["T4_zero_leakage"] = {}
    ok4 = True
    for c in CONS:
        ec0 = env_cfg(c, "f30", zero, zero, "zero")
        l0 = model_score(ec0, "LCDM", "canonical"); l1 = model_score(EC30[c], "LCDM", "canonical")
        dz = float(np.max(np.abs(np.array(l0["model"]) - np.array(l1["model"])) / SIG["f30"]))
        ok4 &= dz > 0.5
        ed = {f: edge_block(ec0, f) for f in FOOTS}
        RES["T4_zero_leakage"][c] = dict(max_dsig=dz, G2f_chi2=l0["chi2"], G2f_p=l0["p"], G2f_pass=l0["p"] > 0.01,
                                         census={f: dict(Delta=ed[f]["census"]["Delta"], p=ed[f]["census"]["p"], PASS=ed[f]["census"]["PASS"])
                                                 for f in FOOTS})
        P(f"  T4 [{c}] zero leakage: max |dm|/sigma {dz:.2f}; G2f LCDM chi2 {l0['chi2']:.2f} (p {l0['p']:.2e}) "
          f"{'PASS' if l0['p'] > 0.01 else 'FAIL'}; census Delta {ed['canonical']['census']['Delta']:+.2f} / {ed['alt']['census']['Delta']:+.2f} "
          f"({'PASS' if ed['canonical']['census']['PASS'] else 'FAIL'} / {'PASS' if ed['alt']['census']['PASS'] else 'FAIL'})")
    check("T4 zero leakage moves the f30 LCDM model by > 0.5 sigma_f30 in some bin (both constructions)", ok4,
          "; ".join(f"{c} {RES['T4_zero_leakage'][c]['max_dsig']:.2f}" for c in CONS))
    RES["T1"] = {f"{c}|{f}": v for (c, f), v in t1.items()}
    RES["mutate_detected"] = bool(all(CHK[k]["ok"] for k in CHK if k.startswith("T")))
else:
    P("\n== 4a environment validation (LCDM, SHMR-propagated) ==")
    RES["gates"] = {}
    for c in CONS:
        G, (g1, g2, g3) = gates(c)
        RES["gates"][c] = G
        P(f"  [{c}] G1m stack P (0.2234) chi2 {G['G1m']['chi2']:.2f} (p {G['G1m']['p']:.3f}) {'PASS' if G['G1m']['passed'] else 'FAIL'}; "
          f"G2f f30 (0.1686) chi2 {G['G2f']['chi2']:.2f} (p {G['G2f']['p']:.3f}) {'PASS' if G['G2f']['passed'] else 'FAIL'}; "
          f"G3m ALL (0.3134) chi2 {G['G3m']['chi2']:.2f} (p {G['G3m']['p']:.1e}; inner9 {G['G3m']['inner9']:.1f} outer6 {G['G3m']['outer6']:.1f}) "
          f"{'PASS' if G['G3m']['passed'] else 'FAIL (reported)'} -> ENVIRONMENT {'VALID' if G['valid'] else 'INVALID'} ({c})")
        P("    f30 LCDM pull: " + " ".join(f"{x:+5.2f}" for x in (d30 - np.array(g2["model"])) / SIG["f30"]))
        for sg in (-1, 1):
            fg = {s: scaled("f30", s, F_MEAS["W30"] + sg * SIG30)[0] for s in SHMRS}
            gv = model_score(env_cfg(c, "f30", fg, fg, f"sig{sg}"), "LCDM", "canonical")
            G[f"G2f_{'minus' if sg < 0 else 'plus'}1sig"] = dict(chi2=gv["chi2"], p=gv["p"])
            P(f"    (reported) G2f at f30 {'-' if sg < 0 else '+'}1 sigma_tot ({F_MEAS['W30'] + sg * SIG30:.4f}): chi2 {gv['chi2']:.2f} (p {gv['p']:.3f})")
    validC = [c for c in CONS if RES["gates"][c]["valid"]]
    g3fail = any(not RES["gates"][c]["G3m"]["passed"] for c in CONS)
    ENV = "VALID" if validC else "INVALID"
    labels = []
    if g3fail:
        labels.append("G3 (ALL) FAILS - environment validated for isolated samples only; CFG504's three-gate rule not met")
    labels.append("transition PM-calibrated at log M_ta >= 13.5 and extrapolated ~1 dex (construction B, CFG504)")
    labels.append("nonlinear 2h NOT CROSS-CHECKED BY PM (CFG503)")
    P(f"  ENVIRONMENT {ENV} (valid constructions: {validC if validC else 'none'})")

    P("\n== 4b/4c re-score on f30 (measured f30 leakage; " + ("verdict" if validC else "INFORMATION ONLY - environment invalid") + ") ==")
    RS = {c: rescore(EC30[c], f"construction {c} ({'VALID' if c in validC else 'INVALID - information only'})") for c in CONS}
    RES["rescore_f30"] = RS
    EDGEV = {}
    for foot in FOOTS:
        res_ = [RS[c][foot]["rows"]["CENSUS"]["PASS"] for c in validC]
        if not validC:
            EDGEV[foot] = "NO VERDICT (environment invalid)"
        elif all(res_):
            EDGEV[foot] = "PASS"
        elif not any(res_):
            EDGEV[foot] = "FAIL"
        else:
            EDGEV[foot] = "CONSTRUCTION-DEPENDENT"
    PERM = {c: {f: {m: ("PASS" if RS[c][f]["rows"][m]["pass_p"] else "FAIL") for m in MODELS + ("CENSUS",)} for f in FOOTS} for c in validC}

    P("\n== reported variants (no verdict weight) ==")
    VAR = {}
    for c in CONS:
        for nm, fE, fO in (("f30 -1 sigma_tot", {s: scaled("f30", s, F_MEAS["W30"] - SIG30)[0] for s in SHMRS}, None),
                           ("f30 +1 sigma_tot", {s: scaled("f30", s, F_MEAS["W30"] + SIG30)[0] for s in SHMRS}, None),
                           ("sum-of-bins scaling convention", {s: scaled("f30", s, F_MEAS["W30"], "sum")[0] for s in SHMRS}, None),
                           ("E-only scaling (own mixing at HOD f)", MEAS["f30"], HOD["f30"]),
                           ("HOD f (unscaled; CFG503/504 N1)", HOD["f30"], HOD["f30"])):
            ec = env_cfg(c, "f30", fE, fO if fO is not None else fE, f"var|{nm}")
            lc = model_score(ec, "LCDM", "canonical")
            eb = {f: edge_block(ec, f) for f in FOOTS}
            VAR[f"{c}|{nm}"] = dict(G2f_chi2=lc["chi2"], G2f_p=lc["p"],
                                    census={f: dict(Delta=eb[f]["census"]["Delta"], p=eb[f]["census"]["p"], PASS=eb[f]["census"]["PASS"],
                                                    best_x=eb[f]["best_x"]) for f in FOOTS})
            P(f"  [{c}] {nm:38s}: G2f LCDM {lc['chi2']:.2f} (p {lc['p']:.3f}); census Delta {eb['canonical']['census']['Delta']:+.2f} / "
              f"{eb['alt']['census']['Delta']:+.2f}, p {eb['canonical']['census']['p']:.3f} / {eb['alt']['census']['p']:.3f}; best x "
              f"{eb['canonical']['best_x']:.2f} / {eb['alt']['best_x']:.2f}")
    RES["variants"] = VAR

    P("\n== VERDICT (frozen rule) ==")
    P(f"  ENVIRONMENT {ENV}; valid constructions: {validC}")
    for foot in FOOTS:
        P(f"  census edge [{foot}]: {EDGEV[foot]}  (" + "; ".join(
            f"{c}: Delta {RS[c][foot]['rows']['CENSUS']['Delta']:+.2f}, chi2 {RS[c][foot]['rows']['CENSUS']['chi2']:.2f}, p {RS[c][foot]['rows']['CENSUS']['p']:.3f}"
            + ("" if c in validC else " [invalid construction]") for c in CONS) + ")")
    for c in validC:
        for foot in FOOTS:
            P(f"  per-model [{c}, {foot}]: " + ", ".join(f"{m} {PERM[c][foot][m]}" for m in MODELS + ("CENSUS",)))
    P("  labels: " + "; ".join(labels))
    RES["verdict"] = dict(environment=ENV, valid_constructions=validC, edge=EDGEV, per_model=PERM, labels=labels)

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg529_score_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg529_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
