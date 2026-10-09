#!/usr/bin/env python3
"""CFG515 (a) KiDS isolated lenses with the census edge (FROZEN_CRITERIA.md 2bbe75602, sections 1-3a).
  (a1) CFG413 harness: CFG377 stack P, free R^-0.8 two-halo amplitude profiled; PASS iff chi2 - chi2_best(CFG413) <= 4, both footings.
  (a2) CFG503 frozen environment (E nlz + stripping W10 + SHMR rank-one; Moster primary), inner 9 bins (R <= 0.445 Mpc):
       PASS iff chi2_inner9 - min(CFG503's five frozen models) <= 4, both footings.  CFG503's G1/G3 gates FAILED (label carried).
Model: nu_mono phantom of the group's present baryons M_gal, fully settled, out to min(r_edge, r_ta), frozen beyond, + point mass.
r_edge = r_M / ln(1 + f_ret f_b/(1 - f_b)); f_ret from cfg515_lib (census = CFG416 fret_of, self-consistent; bracket 0.07 / 0.18).
MUTATE (CFG515_MUTATE=1): f_ret = 1 and 0.01 instead (outputs *_MUTATE.*).
CFG503's cfg503_own (functions, tables) and cfg100_lib / cfg495_lenslib are imported read-only; CFG413/CFG487/CFG503 scoring code copied.
Run: nice -n 15 python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_kids.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import math, json, time, contextlib, io
import numpy as np
import multiprocessing as MP
from scipy.interpolate import RegularGridInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
for p in (HERE, os.path.join(LANES, "CFG503_two_halo_nonlinear"), os.path.join(LANES, "CFG487_settled_fraction_switch"),
          os.path.join(LANES, "CFG100_kids_mass_rederivation"), os.path.join(LANES, "CFG495_drawdown_shell")):
    sys.path.insert(0, p)
import cfg515_lib as L                                                       # noqa: E402
import cfg100_lib as C                                                       # noqa: E402  (read-only)
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only)
with contextlib.redirect_stdout(io.StringIO()):
    import cfg503_own as OWN                                                 # noqa: E402  (read-only; __main__-guarded)
try:
    os.nice(15)
except OSError:
    pass
MUTATE = os.environ.get("CFG515_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
MODES = L.modes()
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
LOG, CHK = [], {}
RES = {"lane": "CFG515", "script": "cfg515_kids", "mutate": MUTATE, "modes": list(MODES)}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
if MUTATE:
    P("\n  *** CFG515_MUTATE=1: f_ret = 1 (PM value on real galaxies) and 0.01 (unphysically depleted) ***")

WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
ET = OWN.ET
OT = np.load(os.path.join(WORK, "cfg503_own_tables.npz"))
LMS, ZG, RG = ET["LMS"], ET["ZG"], ET["RG"]
LRG = np.log(RG)
gi, GM, GZ, GS = OT["gi"], OT["GM"], OT["GZ"], OT["GS"]
NG = len(GM)


# ------------------------------------------------------------------ per-group model vectors (worker)
def work(args):
    Mg, zl, lms = args
    W = {s: OWN.rt_weights(f"{s}_W10", lms, zl) for s in SHMRS}
    out = {}
    for foot in FOOTS:
        a0 = C.A0[foot]
        rta = C.r_ta_law(Mg, a0, zl)
        out[f"{foot}|rta"] = rta
        for x in (0.5, 1.0):                                                 # K3 (CFG413's sharp edges)
            r, Md = OWN.kids_Md(Mg, zl, a0, x * rta)
            out[f"{foot}|K3_{x}"] = OWN.kids_fin(Mg, r, Md)
        for mode in MODES:
            f = L.fret(mode, Mg)
            re = L.r_edge_pm(Mg, C.G_MPC, a0, f)
            rout = min(re, rta)
            r, Md = OWN.kids_Md(Mg, zl, a0, rout)
            out[f"{foot}|{mode}|fret"] = f
            out[f"{foot}|{mode}|xedge"] = re / rta
            out[f"{foot}|{mode}|full"] = OWN.kids_fin(Mg, r, Md)
            for s in SHMRS:
                out[f"{foot}|{mode}|tr_{s}"] = OWN.kids_fin(Mg, r, OWN.truncate(r, Md, W[s]))
    return out


# ------------------------------------------------------------------ data (CFG377 stack P; CFG413 / CFG487 / CFG503 copies)
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
nL = len(lens["z"]); ALLM = np.ones(nL, bool)


def esd_full_loo(mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)


def pstack(tab):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi, weights=WW[:, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


def chi2_413(d_, C_, h, m, t, mode="free"):
    Ci = np.linalg.inv(C_); r = d_ - m
    if mode == "none":
        return float(h * r @ Ci @ r), 0.0
    A = float((t @ Ci @ r) / (t @ Ci @ t))
    rr = r - A * t
    return float(h * rr @ Ci @ rr), A


def grid_interp(tab):
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    return f(np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZG[0], ZG[-1])])


def env_vec(shmr):
    Eg = grid_interp(ET[f"E_{shmr}_nlz_W10"])
    out = np.zeros((NG, 15))
    for g in range(NG):
        out[g] = LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), GM[g])
    return out


def chi2c(dv_, C_, h, m, delta=None):
    Ct = C_ / h + (np.outer(delta, delta) if delta is not None else 0.0)
    r = dv_ - m
    return float(r @ np.linalg.solve(Ct, r))


d, Cv = esd_full_loo(ALLM); h15 = hart(15)
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
Rm = np.array(J377["primary"]["meanR"])
INN = Rm <= 0.445
check("C0 stack P data vector = CFG377 primary", np.max(np.abs(d / np.array(J377["primary"]["esd"]) - 1)) < 1e-10, "exact")
TT = np.array([C._finish(lambda R: R ** -0.8 * 1e12, GM[g]) for g in range(NG)])
tm = pstack(TT)
J413 = json.load(open(os.path.join(LANES, "CFG413_on_radius_kids_vs_growth", "cfg413_kids_results.json")))
BEST = {f: J413["vs_best_x_reported"][f]["chi2_best"] for f in FOOTS}
X1 = {f: J413["primary"][f]["1.0"]["free"]["chi2"] for f in FOOTS}
X05 = {f: J413["primary"][f]["0.5"]["free"]["chi2"] for f in FOOTS}
J503 = json.load(open(os.path.join(LANES, "CFG503_two_halo_nonlinear", "cfg503_score_results.json")))["MAIN"]
EV = {s: env_vec(s) for s in SHMRS}
FW = {s: np.clip(grid_interp(ET[f"{s}_W10_f"]), 0, 1)[:, None] for s in SHMRS}


def a2_score(full, tr):
    """CFG503 MAIN scoring of one model's per-group tables: dict full/tr per shmr."""
    m = {s: pstack((1 - FW[s]) * full[s] + FW[s] * tr[s] + EV[s]) for s in SHMRS}
    dl = m["behroozi"] - m["moster"]
    c_ = chi2c(d, Cv, h15, m["moster"], dl)
    ci = chi2c(d[INN], Cv[np.ix_(INN, INN)], hart(int(INN.sum())), m["moster"][INN], dl[INN])
    return dict(chi2=c_, chi2_inner9=ci, model=m["moster"].tolist())


# K4: re-score CFG503's committed own tables for its frozen models
FROZ5 = ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD")
RESC = {}
k4 = 0.0
for foot in FOOTS:
    RESC[foot] = {}
    for mdl in FROZ5:
        def one(mm, s, kind):
            return OT[f"P|{foot}|{mm}|{kind}"]
        full = {s: (one("F_NODD", s, f"full_{s}") + one("PROP", s, f"full_{s}")) if mdl == "F_DD" else one(mdl, s, f"full_{s}") for s in SHMRS}
        tr = {s: (one("F_NODD", s, f"tr_{s}_W10") + one("PROP", s, f"tr_{s}_W10")) if mdl == "F_DD" else one(mdl, s, f"tr_{s}_W10") for s in SHMRS}
        RESC[foot][mdl] = a2_score(full, tr)
        for q in ("chi2", "chi2_inner9"):
            k4 = max(k4, abs(RESC[foot][mdl][q] - J503["P"][foot][mdl][q]))
check("K4 CFG503: re-scoring its committed own tables reproduces its committed chi2 (full and inner-9) for all five frozen models within 0.01",
      k4 <= 0.01, f"max |diff| {k4:.2e}; inner-9 can: " + ", ".join(f"{m} {RESC['canonical'][m]['chi2_inner9']:.2f}" for m in FROZ5)
      + "; alt: " + ", ".join(f"{m} {RESC['alt'][m]['chi2_inner9']:.2f}" for m in FROZ5))
MIN5 = {f: min(RESC[f][m]["chi2_inner9"] for m in FROZ5) for f in FOOTS}
ARG5 = {f: min(FROZ5, key=lambda m: RESC[f][m]["chi2_inner9"]) for f in FOOTS}

# ------------------------------------------------------------------ build
t = time.time()
with MP.get_context("fork").Pool(4) as pool:
    res = pool.map(work, list(zip(GM, GZ, GS)), chunksize=8)
TAB = {k: np.array([r_[k] for r_ in res]) for k in res[0]}
P(f"\nper-group tables built for {NG} groups x {len(MODES)} modes x 2 footings ({time.time() - t:.0f} s)")

k3 = max(max(abs(chi2_413(d, Cv, h15, pstack(TAB[f"{f}|K3_0.5"]), tm)[0] - X05[f]),
             abs(chi2_413(d, Cv, h15, pstack(TAB[f"{f}|K3_1.0"]), tm)[0] - X1[f])) for f in FOOTS)
check("K3 KiDS harness: m = 1 sharp edges at x = 0.5 and 1.0 reproduce CFG413's committed chi2 within 0.01", k3 <= 0.01, f"max |diff| {k3:.5f}")

# K1-lite: closed-form edge = numeric nu_mono root (point mass), several f_ret
k1 = 0.0
from scipy.optimize import brentq                                            # noqa: E402
for f in (1.0, 0.18, 0.07, 0.01):
    for Mb in (1e9, 10 ** 10.7, 1e12):
        a0 = C.A0["canonical"]; re = L.r_edge_pm(Mb, C.G_MPC, a0, f)
        g = lambda lr: Mb * (float(C.nu_mono(C.G_MPC * Mb / (10 ** lr) ** 2 / a0)) - 1.0) - L.COLD_PER_B * Mb / f
        rn = 10 ** brentq(g, math.log10(re) - 2, math.log10(re) + 2, xtol=1e-14)
        k1 = max(k1, abs(rn / re - 1))
check("K1 closed-form point-mass edge = numeric nu_mono root of M_ph(<r) = 5.364 M_b / f_ret (f_ret 1, 0.18, 0.07, 0.01) to 1e-6",
      k1 <= 1e-6, f"max rel {k1:.1e} (nu_mono is FP1's table)")

# ------------------------------------------------------------------ score
P("\n(a1) CFG413 harness (free two-halo)  |  (a2) CFG503 environment, inner 9 bins (R <= 0.445 Mpc)")
P(f"  CFG413 best (x = 0.5): {BEST['canonical']:.3f} / {BEST['alt']:.3f};  CFG503 inner-9 best of five: "
  f"{ARG5['canonical']} {MIN5['canonical']:.2f} / {ARG5['alt']} {MIN5['alt']:.2f};  LAW_RTA inner-9 "
  f"{RESC['canonical']['LAW_RTA']['chi2_inner9']:.2f} / {RESC['alt']['LAW_RTA']['chi2_inner9']:.2f}")
OUTR = {}
for mode in MODES:
    OUTR[mode] = {}
    for foot in FOOTS:
        fr = TAB[f"{foot}|{mode}|fret"]; xe = TAB[f"{foot}|{mode}|xedge"]
        wl = np.bincount(gi, weights=WW.sum(1), minlength=NG)               # lensing weight per group
        o = np.argsort(xe); cw = np.cumsum(wl[o]) / wl.sum()
        xw = lambda q: float(xe[o][np.searchsorted(cw, q)])
        m = pstack(TAB[f"{foot}|{mode}|full"])
        c, A = chi2_413(d, Cv, h15, m, tm)
        c0, _ = chi2_413(d, Cv, h15, m, tm, "none")
        mx05 = pstack(TAB[f"{foot}|K3_0.5"])
        drop = []
        for kb in range(15):
            sel = np.array([i for i in range(15) if i != kb])
            cd, _ = chi2_413(d[sel], Cv[np.ix_(sel, sel)], hart(14), m[sel], tm[sel])
            cx, _ = chi2_413(d[sel], Cv[np.ix_(sel, sel)], hart(14), mx05[sel], tm[sel])
            drop.append(cd - cx)
        inner_free, _ = chi2_413(d[INN], Cv[np.ix_(INN, INN)], hart(int(INN.sum())), m[INN], tm[INN])
        a2 = a2_score({s: TAB[f"{foot}|{mode}|full"] for s in SHMRS}, {s: TAB[f"{foot}|{mode}|tr_{s}"] for s in SHMRS})
        r_ = dict(fret_median=float(np.median(fr)), fret_p10=float(np.percentile(fr, 10)), fret_p90=float(np.percentile(fr, 90)),
                  fret_lensweighted_median=float(fr[np.argsort(fr)][np.searchsorted(np.cumsum(wl[np.argsort(fr)]) / wl.sum(), 0.5)]),
                  xedge_lensweighted=dict(p16=xw(0.16), p50=xw(0.5), p84=xw(0.84)), frac_capped_at_rta=float(np.sum(wl * (xe >= 1)) / wl.sum()),
                  a1=dict(chi2=c, A=A, chi2_no2h=c0, d_vs_best=c - BEST[foot], d_vs_x1=c - X1[foot],
                          drop_one_bin_vs_x05=[float(min(drop)), float(max(drop))], chi2_inner9_free2h=inner_free, model=m.tolist()),
                  a2=dict(chi2=a2["chi2"], chi2_inner9=a2["chi2_inner9"], d_inner_vs_best5=a2["chi2_inner9"] - MIN5[foot],
                          best5=ARG5[foot], d_inner_vs_LAW_RTA=a2["chi2_inner9"] - RESC[foot]["LAW_RTA"]["chi2_inner9"],
                          d_full_vs_LCDM=a2["chi2"] - RESC[foot]["LCDM"]["chi2"], model=a2["model"]))
        r_["a1_pass"] = r_["a1"]["d_vs_best"] <= 4.0
        r_["a2_pass"] = r_["a2"]["d_inner_vs_best5"] <= 4.0
        OUTR[mode][foot] = r_
        P(f"  [{mode:6s}|{foot:9s}] f_ret median {r_['fret_median']:.3f} (10-90% {r_['fret_p10']:.3f}-{r_['fret_p90']:.3f}); x_edge (lens-wtd) "
          f"{r_['xedge_lensweighted']['p50']:.3f} ({r_['xedge_lensweighted']['p16']:.3f}-{r_['xedge_lensweighted']['p84']:.3f}); capped {r_['frac_capped_at_rta']:.3f}")
        P(f"      a1: chi2 {c:.3f} (A {A:.3f}; no-2h {c0:.1f}); - best {r_['a1']['d_vs_best']:+.3f}; - x1 {r_['a1']['d_vs_x1']:+.3f}; "
          f"drop-one-bin vs x0.5 {r_['a1']['drop_one_bin_vs_x05'][0]:+.2f}..{r_['a1']['drop_one_bin_vs_x05'][1]:+.2f} -> {'PASS' if r_['a1_pass'] else 'FAIL'}")
        P(f"      a2: chi2/15 {a2['chi2']:.2f} (LCDM {RESC[foot]['LCDM']['chi2']:.2f}); inner-9 {a2['chi2_inner9']:.2f} - best5 ({ARG5[foot]}) "
          f"{r_['a2']['d_inner_vs_best5']:+.2f}; - LAW_RTA {r_['a2']['d_inner_vs_LAW_RTA']:+.2f} -> {'PASS' if r_['a2_pass'] else 'FAIL'} "
          f"[label: CFG503 G1/G3 FAILED]")
    OUTR[mode]["a1_pass"] = all(OUTR[mode][f]["a1_pass"] for f in FOOTS)
    OUTR[mode]["a2_pass"] = all(OUTR[mode][f]["a2_pass"] for f in FOOTS)
    OUTR[mode]["a_pass"] = OUTR[mode]["a1_pass"] and OUTR[mode]["a2_pass"]
    P(f"  => {mode}: a1 {'PASS' if OUTR[mode]['a1_pass'] else 'FAIL'}, a2 {'PASS' if OUTR[mode]['a2_pass'] else 'FAIL'}, "
      f"(a) {'PASS' if OUTR[mode]['a_pass'] else 'FAIL'}")
RES["rows"] = OUTR
RES["cfg503_rescored"] = {f: {m: {k: v for k, v in RESC[f][m].items() if k != "model"} for m in FROZ5} for f in FOOTS}
RES["cfg413_best"] = BEST

if MUTATE:
    m1 = max(abs(OUTR["one"]["canonical"]["a1"]["d_vs_best"] - 60.5), abs(OUTR["one"]["alt"]["a1"]["d_vs_best"] - 70.6))
    check("M1 (KiDS) f_ret = 1 reproduces CFG487's edge_only_E1 d_vs_best +60.5 / +70.6 within 0.5", m1 <= 0.5, f"max |diff| {m1:.3f}")
    m1b = max(abs(OUTR["one"]["canonical"]["a2"]["chi2_inner9"] - J503["P"]["canonical"]["EDGE"]["chi2_inner9"]),
              abs(OUTR["one"]["alt"]["a2"]["chi2_inner9"] - J503["P"]["alt"]["EDGE"]["chi2_inner9"]))
    check("M1 (CFG503) f_ret = 1 reproduces CFG503's EDGE inner-9 (240.9 / 240.7) within 1", m1b <= 1.0, f"max |diff| {m1b:.3f}")

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; load-bearing failures {nlb}; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg515_kids_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg515_kids{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
