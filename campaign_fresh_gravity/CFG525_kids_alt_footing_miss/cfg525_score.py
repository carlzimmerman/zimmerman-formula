#!/usr/bin/env python3
"""CFG525 stage 3 (FROZEN_CRITERIA.md 7f99a4371): scoring of every declared row in harnesses H1 (CFG413 free R^-0.8 two-halo, 15 bins),
H2 (H1 on the 9 trusted bins), H3 (CFG503 environment with the measured leaked fraction 0.2234, CFG520 part-B scaling; H3i = inner 9),
H4 (reported: H3's E stack as a free-amplitude shape), each as Delta = chi2 - chi2(best sharp-edge node x >= 0.2), both footings.
Inputs: stage-1 node tables (cfg525_tables.npz), stage-2 neighbours (cfg525_neighbours.npz), CFG503 / CFG515 / CFG520 / CFG522 / CFG413
committed files (read-only).  Edges between nodes: cubic spline in log x per group onto a 300-point fine grid, then linear per lens.
MUTATE (CFG525_MUTATE=1): T1 f_ret = 1 and T2 f_ret = 0.01 (direct rows) must FAIL H1 on both footings.
Run: nice -n 10 python3 cfg525_score.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import math, json, time, contextlib, io
import numpy as np
from scipy.interpolate import RegularGridInterpolator, CubicSpline

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
for p in (os.path.join(LANES, "CFG515_census_edge_resolution"), os.path.join(LANES, "CFG503_two_halo_nonlinear"),
          os.path.join(LANES, "CFG487_settled_fraction_switch"), os.path.join(LANES, "CFG100_kids_mass_rederivation"),
          os.path.join(LANES, "CFG495_drawdown_shell")):
    sys.path.insert(0, p)
import cfg515_lib as L                                                       # noqa: E402  (read-only)
import cfg100_lib as C                                                       # noqa: E402  (read-only)
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only)
with contextlib.redirect_stdout(io.StringIO()):
    import cfg503_own as OWN                                                 # noqa: E402  (read-only; direct rows below the node range)
try:
    os.nice(10)
except OSError:
    pass
MUTATE = os.environ.get("CFG525_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
LOG, CHK = [], {}
RES = {"lane": "CFG525", "script": "cfg525_score", "mutate": MUTATE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
# ------------------------------------------------------------------ data and stacks
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
lMg, llogM, lz = lens["Mgal"].astype(float), lens["logM"].astype(float), lens["z"].astype(float)
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
nL = len(lz); ALLM = np.ones(nL, bool)
F30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
OT = np.load(os.path.join(EXT, "cfg503_work", "cfg503_own_tables.npz"))
ET = np.load(os.path.join(EXT, "cfg503_work", "cfg503_env_table.npz"))
gi, GM, GZ, GS = OT["gi"], OT["GM"], OT["GZ"], OT["GS"]; NG = len(GM)
LMS, ZG, RG = ET["LMS"], ET["ZG"], ET["RG"]; LRG = np.log(RG)
TB = np.load(os.path.join(EXT, "cfg525_work", "cfg525_tables.npz"))
XN = TB["XN"]; LXN = np.log(XN)
RTA = {f: TB[f"{f}|rta"] for f in FOOTS}
NB = np.load(os.path.join(EXT, "cfg525_work", "cfg525_neighbours.npz"))
wl = WW.sum(1)


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


def gstack(tab, mask):
    """group table (NG, 15) -> stacked 15-vector over lenses in mask."""
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


def lstack(m, mask):
    """per-lens model (nL, 15) -> stacked 15-vector."""
    return (WW[mask] * m[mask]).sum(0) / WW[mask].sum(0)


J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
Rm = np.array(J377["primary"]["meanR"]); INN = Rm <= 0.445
DAT = {"P": esd_full_loo(ALLM), "f30": esd_full_loo(F30)}
MASK = {"P": ALLM, "f30": F30}
TT = np.array([C._finish(lambda R: R ** -0.8 * 1e12, GM[g]) for g in range(NG)])


def chi2_free(dv, Cv, h, m, t):
    Ci = np.linalg.inv(Cv); r = dv - m
    A = float((t @ Ci @ r) / (t @ Ci @ t)); rr = r - A * t
    return float(h * rr @ Ci @ rr), A


def chi2c(dv_, C_, h, m, delta=None):
    Ct = C_ / h + (np.outer(delta, delta) if delta is not None else 0.0)
    r = dv_ - m
    return float(r @ np.linalg.solve(Ct, r))


def grid_interp(tab):
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    return f(np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZG[0], ZG[-1])])


def evec(Etab):
    Eg = grid_interp(Etab); out = np.zeros((NG, 15))
    for g in range(NG):
        out[g] = LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), GM[g])
    return out


# ------------------------------------------------------------------ H3 environment: unscaled (K1) and scaled to 0.2234 (CFG520 part B)
F_OBS, X503M = 0.22342746446430256, 0.1805564701196465
XF = {}
for s in SHMRS:
    f = ET[f"{s}_W10_f"]; E = ET[f"E_{s}_nlz_W10"]; H = ET[f"{s}_HOLE"]; S2 = ET[f"{s}_S2H_nlz"]; bc = ET[f"{s}_W10_bc"]
    XF[s] = (E - H - bc[..., None] * S2) / f[..., None]


def E503(s, fg):
    return ET[f"{s}_HOLE"] + ET[f"{s}_W10_bc"][..., None] * ET[f"{s}_S2H_nlz"] + np.clip(fg, 0, 1)[..., None] * XF[s]


def f_stack(fg):
    return float(gstack(np.repeat(np.clip(grid_interp(fg), 0, 1)[:, None], 15, 1), ALLM)[0])


fm, fb = ET["moster_W10_f"], ET["behroozi_W10_f"]
sM, sB = F_OBS / X503M, F_OBS / f_stack(fb)
ENV = {"unscaled": {s: (np.clip(grid_interp(ET[f"{s}_W10_f"]), 0, 1), evec(ET[f"E_{s}_nlz_W10"])) for s in SHMRS},
       "scaled": {"moster": (np.clip(grid_interp(np.clip(sM * fm, 0, 1)), 0, 1), evec(E503("moster", np.clip(sM * fm, 0, 1)))),
                  "behroozi": (np.clip(grid_interp(np.clip(sB * fb, 0, 1)), 0, 1), evec(E503("behroozi", np.clip(sB * fb, 0, 1))))}}
P(f"H3 scaling to the measured leaked fraction {F_OBS:.4f}: s_M {sM:.4f}, s_B {sB:.4f} (CFG520 part B: 1.2374 / 1.2358)")


def h3_score(full_l, tr_l, env="scaled", mask=ALLM, lens_level=True):
    """CFG503 MAIN scoring: (1 - FW) full + FW tr + E, Moster primary, Behroozi difference as rank-one; returns 15-bin and inner-9 chi2."""
    dv, Cv = DAT["P"]
    m = {}
    for s in SHMRS:
        FW, EV = ENV[env][s]
        if lens_level:
            mm = (1 - FW[gi, None]) * full_l + FW[gi, None] * tr_l[s] + EV[gi]
            m[s] = lstack(mm, mask)
        else:
            m[s] = gstack((1 - FW[:, None]) * full_l + FW[:, None] * tr_l[s] + EV, mask)
    dl = m["behroozi"] - m["moster"]
    c15 = chi2c(dv, Cv, hart(15), m["moster"], dl)
    ci = chi2c(dv[INN], Cv[np.ix_(INN, INN)], hart(9), m["moster"][INN], dl[INN])
    return c15, ci


EST = {s: gstack(ENV["scaled"][s][1], ALLM) for s in SHMRS}


def harness_all(full_v, tr_v, sample="P", lens_level=True):
    """full_v: stacked-ready per-lens (nL,15) or group (NG,15) model; tr_v: dict shmr -> same.  Returns dict of chi2 per harness."""
    mask = MASK[sample]; dv, Cv = DAT[sample]
    st = (lambda m_: lstack(m_, mask)) if lens_level else (lambda m_: gstack(m_, mask))
    m = st(full_v); t = gstack(TT, mask)
    out = {}
    out["H1"], out["A_H1"] = chi2_free(dv, Cv, hart(15), m, t)
    if sample == "P":
        out["H2"], out["A_H2"] = chi2_free(dv[INN], Cv[np.ix_(INN, INN)], hart(9), m[INN], t[INN])
        out["H3"], out["H3i"] = h3_score(full_v, tr_v, "scaled", mask, lens_level)
        out["H3_unscaled"], out["H3i_unscaled"] = h3_score(full_v, tr_v, "unscaled", mask, lens_level)
        out["H4"], out["A_H4"] = chi2_free(dv, Cv, hart(15), m, EST["moster"])
    return out


# ------------------------------------------------------------------ best-x per harness from the exact nodes
NODE = {}
for foot in FOOTS:
    for sample in ("P", "f30"):
        rows = []
        for j, x in enumerate(XN):
            full = TB[f"{foot}|node|full"][:, j, :]
            tr = {s: TB[f"{foot}|node|tr_{s}"][:, j, :] for s in SHMRS}
            rows.append(harness_all(full, tr, sample, lens_level=False))
        NODE[(foot, sample)] = rows
BEST = {}
for foot in FOOTS:
    for sample in ("P", "f30"):
        rows = NODE[(foot, sample)]
        sel = [j for j, x in enumerate(XN) if x >= 0.2 - 1e-12]
        BEST[(foot, sample)] = {}
        for h in rows[0]:
            if h.startswith("A_"):
                continue
            j = min(sel, key=lambda j_: rows[j_][h])
            BEST[(foot, sample)][h] = dict(x=float(XN[j]), chi2=rows[j][h])
J413 = json.load(open(os.path.join(LANES, "CFG413_on_radius_kids_vs_growth", "cfg413_kids_results.json")))
k3 = 0.0
for foot in FOOTS:
    for x in (0.5, 1.0):
        j = int(np.argmin(np.abs(XN - x)))
        k3 = max(k3, abs(NODE[(foot, "P")][j]["H1"] - J413["primary"][foot][str(x)]["free"]["chi2"]))
    j = int(np.argmin(np.abs(XN - 0.3)))
    k3 = max(k3, abs(NODE[(foot, "f30")][j]["H1"] - J413["S1_f30"][foot]["0.3"]["free"]["chi2"]))
check("K3 nodes x = 0.5 / 1.0 reproduce CFG413's chi2 and f30 x = 0.3 reproduces CFG413 S1, within 0.01", k3 <= 0.01, f"max |diff| {k3:.5f}")
J520 = json.load(open(os.path.join(LANES, "CFG520_native_ruler_recalibrated", "cfg520_partB_results.json")))
lc = {s: (OT[f"P|canonical|LCDM|full_{s}"], OT[f"P|canonical|LCDM|tr_{s}_W10"]) for s in SHMRS}
# LCDM's own profile differs by SHMR -> scored explicitly (h3_score shares one 'full')
m_ = {s: gstack((1 - ENV["scaled"][s][0][:, None]) * lc[s][0] + ENV["scaled"][s][0][:, None] * lc[s][1] + ENV["scaled"][s][1], ALLM) for s in SHMRS}
dv, Cv = DAT["P"]
c4 = chi2c(dv, Cv, hart(15), m_["moster"], m_["behroozi"] - m_["moster"])
ref520 = J520["CFG503"]["scaled (primary: E and own mixing)"]["scores"]["canonical"]["LCDM"]["chi2"]
check("K4 H3 machinery with LCDM own tables reproduces CFG520 part B's scaled LCDM 15-bin chi2 within 0.01", abs(c4 - ref520) <= 0.01,
      f"{c4:.4f} vs {ref520:.4f}")
RES["H3_LCDM_chi2"] = c4
RES["best_x"] = {f"{foot}|{s}": BEST[(foot, s)] for foot in FOOTS for s in ("P", "f30")}
for foot in FOOTS:
    P(f"  [{foot}] best-x: " + ", ".join(f"{h} x={v['x']:.2f} chi2 {v['chi2']:.3f}" for h, v in BEST[(foot, 'P')].items())
      + f"; f30 H1 x={BEST[(foot, 'f30')]['H1']['x']:.2f} {BEST[(foot, 'f30')]['H1']['chi2']:.3f}")
H3RANGE = {}
for foot in FOOTS:
    v = [NODE[(foot, "P")][j]["H3"] for j, x in enumerate(XN) if x >= 0.2 - 1e-12]
    H3RANGE[foot] = float(max(v) - min(v))
    P(f"  [{foot}] H3 chi2 range over nodes x in [0.2, 1]: {H3RANGE[foot]:.2f}; node chi2 H1 / H3: "
      + ", ".join(f"{x:.2f}:{NODE[(foot, 'P')][j]['H1']:.1f}/{NODE[(foot, 'P')][j]['H3']:.1f}" for j, x in enumerate(XN) if x >= 0.2 - 1e-12))
RES["H3_range_x02_1"] = H3RANGE
RES["node_chi2"] = {foot: {f"{x:.2f}": NODE[(foot, "P")][j] for j, x in enumerate(XN)} for foot in FOOTS}

# ------------------------------------------------------------------ fine grid and per-lens evaluation
XF = np.geomspace(XN[0], 1.0, 300); LXF = np.log(XF); DLX = LXF[1] - LXF[0]
FINE = {}


def fine(foot, v):
    k = (foot, v)
    if k not in FINE:
        FINE[k] = CubicSpline(LXN, TB[f"{foot}|node|{v}"], axis=1)(LXF)
    return FINE[k]


def lens_models(foot, x_l):
    """x_l: per-lens edge in units of the group's r_ta.  Returns per-lens full (nL,15) and tr dict."""
    x = np.minimum(np.asarray(x_l, float), 1.0)
    lowm = x < XN[0] - 1e-12
    t = (np.log(np.maximum(x, XN[0])) - LXF[0]) / DLX
    i = np.clip(np.floor(t).astype(int), 0, len(XF) - 2); w = (t - i)[:, None]
    out = []
    for v in ("full", "tr_moster", "tr_behroozi"):
        F = fine(foot, v)
        out.append((1 - w) * F[gi, i] + w * F[gi, i + 1])
    if lowm.any():                                                           # frozen rule: below the node range -> computed directly
        LOWW[(foot, len(LOWW))] = float(np.sum(wl[lowm]) / wl.sum())
        for g in np.unique(gi[lowm]):
            sel = lowm & (gi == g)
            xg = float(np.average(x[sel], weights=wl[sel]))                  # group members share M_gal to 0.01 dex
            r, Md = OWN.kids_Md(GM[g], GZ[g], C.A0[foot], xg * RTA[foot][g])
            Wt = {s: OWN.rt_weights(f"{s}_W10", GS[g], GZ[g]) for s in SHMRS}
            out[0][sel] = OWN.kids_fin(GM[g], r, Md)
            out[1][sel] = OWN.kids_fin(GM[g], r, OWN.truncate(r, Md, Wt["moster"]))
            out[2][sel] = OWN.kids_fin(GM[g], r, OWN.truncate(r, Md, Wt["behroozi"]))
    return out[0], {"moster": out[1], "behroozi": out[2]}


LOWW = {}


def edge_x(foot, Mb, f, per_lens=True):
    """x = r_edge(Mb, f) / r_ta(group); Mb, f per lens (arrays) or per group."""
    a0 = C.A0[foot]
    re = np.sqrt(C.G_MPC * Mb / a0) / np.log1p(f * L.FB / (1 - L.FB))
    return re / (RTA[foot][gi] if per_lens else RTA[foot])


_LFC = np.linspace(8.0, 13.5, 22001)
_FC = np.array([L.fret_census(10 ** v)[0] for v in _LFC])


def fcensus_vec(M):
    """fret_census on a 2.5e-4-dex table (linear interpolation; checked against direct calls in K2b)."""
    return np.interp(np.log10(np.asarray(M, float)), _LFC, _FC)


ROWS = {}


def score_row(name, xfun, sample="P", note=""):
    ROWS[name] = {}
    for foot in FOOTS:
        x_l = xfun(foot)
        full, tr = lens_models(foot, x_l)
        r_ = harness_all(full, tr, sample, lens_level=True)
        o = srt = np.argsort(x_l); cw = np.cumsum(wl[o]) / wl.sum()
        rec = dict(x_med=float(x_l[o][np.searchsorted(cw, 0.5)]), x_p16=float(x_l[o][np.searchsorted(cw, 0.16)]),
                   x_p84=float(x_l[o][np.searchsorted(cw, 0.84)]))
        for h, v in r_.items():
            rec[h] = v
            if not h.startswith("A_") and h in BEST[(foot, sample)]:
                rec[f"D_{h}"] = v - BEST[(foot, sample)][h]["chi2"]
        rec["pass_H1"] = rec["D_H1"] <= 4.0
        ROWS[name][foot] = rec
    ROWS[name]["pass_H1_both"] = all(ROWS[name][f]["pass_H1"] for f in FOOTS)
    ROWS[name]["note"] = note
    c_, a_ = ROWS[name]["canonical"], ROWS[name]["alt"]
    extra = "" if sample != "P" else (f" | H2 {c_['D_H2']:+.2f}/{a_['D_H2']:+.2f} | H3 {c_['D_H3']:+.2f}/{a_['D_H3']:+.2f} | "
                                      f"H3i {c_['D_H3i']:+.2f}/{a_['D_H3i']:+.2f} | H4 {c_['D_H4']:+.2f}/{a_['D_H4']:+.2f}")
    P(f"  {name:34s} x_med {c_['x_med']:.3f}/{a_['x_med']:.3f} | H1 {c_['D_H1']:+.2f}/{a_['D_H1']:+.2f} "
      f"[{'PASS' if ROWS[name]['pass_H1_both'] else 'FAIL'}]{extra}")
    return ROWS[name]


_tst = np.geomspace(1e9, 3e11, 997)
_k2b = float(np.max(np.abs(fcensus_vec(_tst) - np.array([L.fret_census(m)[0] for m in _tst]))))
check("K2b tabulated fret_census equals direct calls within 1e-4", _k2b <= 1e-4, f"max |d| {_k2b:.1e}")
GML = GM[gi]                                                                 # group M_gal per lens (the model's baryons)
FCEN_G = np.array([L.fret_census(m)[0] for m in GM])
XCEN = {f: TB[f"{f}|dir|census|x"] for f in FOOTS}

# ------------------------------------------------------------------ K1 / K2 and the direct census, MUTATE teeth
P("\n== direct rows (stage-1 direct tables) ==")
J515 = json.load(open(os.path.join(LANES, "CFG515_census_edge_resolution", "cfg515_kids_results.json")))
DIRR = {}
for nm in ("census", "one", "dep01"):
    DIRR[nm] = {}
    for foot in FOOTS:
        full = TB[f"{foot}|dir|{nm}|full"]; tr = {s: TB[f"{foot}|dir|{nm}|tr_{s}"] for s in SHMRS}
        r_ = harness_all(full, tr, "P", lens_level=False)
        r_["D_H1_vs_CFG413best"] = r_["H1"] - J515["cfg413_best"][foot]
        for h in ("H1", "H2", "H3", "H3i", "H4"):
            r_[f"D_{h}"] = r_[h] - BEST[(foot, "P")][h]["chi2"]
        DIRR[nm][foot] = r_
    P(f"  direct {nm:7s}: H1 chi2 {DIRR[nm]['canonical']['H1']:.3f}/{DIRR[nm]['alt']['H1']:.3f}; vs CFG413 best "
      f"{DIRR[nm]['canonical']['D_H1_vs_CFG413best']:+.3f}/{DIRR[nm]['alt']['D_H1_vs_CFG413best']:+.3f}; vs fine-node best "
      f"{DIRR[nm]['canonical']['D_H1']:+.3f}/{DIRR[nm]['alt']['D_H1']:+.3f}; H3 {DIRR[nm]['canonical']['D_H3']:+.2f}/{DIRR[nm]['alt']['D_H3']:+.2f}")
RES["direct"] = DIRR
k1 = max(abs(DIRR["census"][f]["H1"] - J515["rows"]["census"][f]["a1"]["chi2"]) for f in FOOTS)
k1b = max(abs(DIRR["census"][f]["H3i_unscaled"] - J515["rows"]["census"][f]["a2"]["chi2_inner9"]) for f in FOOTS)
check("K1 direct census reproduces CFG515 (a1) chi2 and (a2) inner-9 within 0.01", max(k1, k1b) <= 0.01, f"a1 max |d| {k1:.5f}; a2 inner-9 {k1b:.5f}")
P("\n== rows (Delta vs best node in the same harness; canonical/alt) ==")
r_int = score_row("census (interpolated)", lambda f: XCEN[f][gi])
k2 = max(abs(r_int[f]["H1"] - DIRR["census"][f]["H1"]) for f in FOOTS)
check("K2 interpolated census reproduces the direct census H1 chi2 within 0.05", k2 <= 0.05, f"max |d| {k2:.4f}")
D6 = {f: float(np.sum(wl * (XCEN[f][gi] >= 1)) / wl.sum()) for f in FOOTS}
P(f"  D6 lens weight with census r_edge >= r_ta: {D6['canonical']:.4f} / {D6['alt']:.4f} -> the census model does not depend on z_l")
RES["D6_frac_capped"] = D6

if MUTATE:
    t1 = all(DIRR["one"][f]["D_H1_vs_CFG413best"] > 4 for f in FOOTS)
    rep = max(abs(DIRR["one"]["canonical"]["D_H1_vs_CFG413best"] - 60.48), abs(DIRR["one"]["alt"]["D_H1_vs_CFG413best"] - 70.57))
    check("T1 f_ret = 1 FAILS H1 on both footings and reproduces CFG515 M1 (+60.48 / +70.57) within 0.1", t1 and rep <= 0.1,
          f"{DIRR['one']['canonical']['D_H1_vs_CFG413best']:+.2f} / {DIRR['one']['alt']['D_H1_vs_CFG413best']:+.2f}")
    t2 = all(DIRR["dep01"][f]["D_H1_vs_CFG413best"] > 4 for f in FOOTS)
    check("T2 f_ret = 0.01 FAILS H1 on both footings", t2,
          f"{DIRR['dep01']['canonical']['D_H1_vs_CFG413best']:+.2f} / {DIRR['dep01']['alt']['D_H1_vs_CFG413best']:+.2f}")
    RES["mutate_detected"] = bool(t1 and rep <= 0.1 and t2)
else:
    # ---------------------------------------------------------------- D1 mass scale (edge only)
    P("\n-- D1 stellar-mass scale (edge only; plausible |delta| <= 0.10) --")
    D1 = {}
    for dl in (-0.15, -0.10, -0.05, 0.05, 0.10, 0.15):
        Mg2 = GM * 10 ** dl; fg = np.array([L.fret_census(m)[0] for m in Mg2])
        D1[dl] = score_row(f"D1 delta {dl:+.2f} dex", lambda f, Mg2=Mg2, fg=fg: edge_x(f, Mg2, fg, per_lens=False)[gi])
    # ---------------------------------------------------------------- D2 cold gas
    P("\n-- D2 cold gas (edge only) --")
    Ms = 10 ** llogM; fcold = 10 ** (-0.69 * llogM + 6.63)
    ratio = lMg / GML                                                        # per-lens M_gal relative to its group's (~1)
    D2 = {}
    for nm, Mb in (("stars only", Ms), ("f_cold x 2", Ms * (1 + 2 * fcold))):
        Mb_g = Mb / ratio                                                    # scaled so the group M_gal maps consistently
        D2[nm] = score_row(f"D2 {nm}", lambda f, Mb_g=Mb_g: edge_x(f, Mb_g, fcensus_vec(Mb_g)))
    # ---------------------------------------------------------------- f scan (D3 rows + post hoc)
    P("\n-- f_ret scan, constant per lens (D3 rows 0.05 / 0.07 / 0.09; the rest post hoc) --")
    FS = (0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.14, 0.16, 0.18, 0.20)
    for fc in FS:
        score_row(f"f_ret {fc:.2f}", lambda f, fc=fc: edge_x(f, GML, np.full(nL, fc)))
    need = {}
    for foot in FOOTS:
        dd = [(fc, ROWS[f"f_ret {fc:.2f}"][foot]["D_H1"]) for fc in FS]
        fneed = None
        for (f1, d1), (f2, d2) in zip(dd[:-1], dd[1:]):
            if d1 <= 4 < d2:
                fneed = f1 + (4 - d1) * (f2 - f1) / (d2 - d1)
        need[foot] = fneed
    P(f"  POST HOC (no verdict weight): largest constant f_ret with Delta_H1 <= 4: canonical {need['canonical']}, alt {need['alt']}")
    RES["posthoc_f_needed"] = need
    # LG conflict test (CFG522 committed scan, canonical)
    J522 = json.load(open(os.path.join(LANES, "CFG522_local_group_timing", "cfg522_results.json")))
    sc = {row["f"]: row for row in J522["post_hoc_scan_canonical"]}
    z08, z10 = sc[0.08]["z_full_LMC"], sc[0.10]["z_full_LMC"]
    zLG07 = z08 + (0.07 - 0.08) * (z10 - z08) / (0.10 - 0.08)
    d3_pass = ROWS["f_ret 0.07"]["pass_H1_both"]
    d3_conf = abs(zLG07) > 3
    P(f"  D3(c) LG full statistic (CFG522 scan, canonical) at common f_ret: 0.08 z_full,LMC {z08:+.2f}; 0.10 {z10:+.2f}; 0.07 (linear extrapolation) "
      f"{zLG07:+.2f} -> {'CONFLICTED' if d3_conf else 'no conflict'}; f_ret 0.07 H1 {'PASS' if d3_pass else 'FAIL'} both footings")
    RES["D3"] = dict(f07_pass_both=d3_pass, LG_zfullLMC_f07_extrap=zLG07, LG_zfullLMC_f08=z08, LG_zfullLMC_f10=z10, conflicted=d3_conf,
                     status=("DATA-ISSUE candidate" if d3_pass and not d3_conf else ("CONFLICTED" if d3_pass else "no effect")))
    # ---------------------------------------------------------------- D7 f30
    P("\n-- D7 isolation: f30 sample (H1 only) --")
    D7 = score_row("D7 census, f30 sample", lambda f: XCEN[f][gi], sample="f30")
    # ---------------------------------------------------------------- M-i shared catchments
    P("\n-- M-i shared catchments (census once per catchment; supply by own baryons) --")
    MI = {}
    for foot in FOOTS:
        raw = NB[f"raw_{foot}"]; bg = NB[f"bg_{foot}"]; exc = raw - bg
        exc_g = np.bincount(gi, weights=exc, minlength=NG) / np.bincount(gi, minlength=NG)
        MI[foot] = dict(exc_g=exc_g, raw=raw)
        P(f"  [{foot}] group-mean neighbour excess / M_gal: lens-weighted mean {np.average(exc_g[gi] / GML, weights=wl):+.4f}; "
          f"raw per lens mean {np.average(raw / lMg, weights=wl):.4f}")

    def x_shared(foot, kind):
        if kind == "a":
            Msum = np.maximum(GML + MI[foot]["exc_g"][gi], GML)              # a negative mean excess cannot remove the lens's own baryons
        elif kind == "a_upper":
            Msum = GML + MI[foot]["raw"] * GML / lMg
        return edge_x(foot, GML, fcensus_vec(Msum)), Msum

    score_row("M-i(a) photometric neighbours", lambda f: x_shared(f, "a")[0])
    score_row("M-i(a) upper (raw, per lens)", lambda f: x_shared(f, "a_upper")[0])
    FSAT = F_OBS

    def mix_row(name, xc_fun, xs_fun):
        ROWS[name] = {}
        for foot in FOOTS:
            fc_, trc = lens_models(foot, xc_fun(foot)); fs_, trs = lens_models(foot, xs_fun(foot))
            full = (1 - FSAT) * fc_ + FSAT * fs_; tr = {s: (1 - FSAT) * trc[s] + FSAT * trs[s] for s in SHMRS}
            r_ = harness_all(full, tr, "P", lens_level=True)
            rec = {h: v for h, v in r_.items()}
            for h in ("H1", "H2", "H3", "H3i", "H4"):
                rec[f"D_{h}"] = rec[h] - BEST[(foot, "P")][h]["chi2"]
            rec["pass_H1"] = rec["D_H1"] <= 4
            ROWS[name][foot] = rec
        ROWS[name]["pass_H1_both"] = all(ROWS[name][f]["pass_H1"] for f in FOOTS)
        c_, a_ = ROWS[name]["canonical"], ROWS[name]["alt"]
        P(f"  {name:34s} H1 {c_['D_H1']:+.2f}/{a_['D_H1']:+.2f} [{'PASS' if ROWS[name]['pass_H1_both'] else 'FAIL'}] | H2 {c_['D_H2']:+.2f}/"
          f"{a_['D_H2']:+.2f} | H3 {c_['D_H3']:+.2f}/{a_['D_H3']:+.2f} | H3i {c_['D_H3i']:+.2f}/{a_['D_H3i']:+.2f}")

    mix_row("M-i(b) leaked satellites only", lambda f: XCEN[f][gi], lambda f: edge_x(f, GML, fcensus_vec(2 * GML)))
    mix_row("M-i (a)+(b) [the M-i row]", lambda f: x_shared(f, "a")[0],
            lambda f: edge_x(f, GML, fcensus_vec(x_shared(f, "a")[1] + GML)))

    def x_double(foot):
        x0, Msum = x_shared(foot, "a")
        fsh = fcensus_vec(Msum); feff = fsh * GML / Msum
        return edge_x(foot, GML, feff)

    def x_double_sat(foot):
        _, Msum = x_shared(foot, "a"); Ms2 = Msum + GML
        fsh = fcensus_vec(Ms2); return edge_x(foot, GML, fsh * GML / Ms2)

    mix_row("FORBIDDEN double-counted supply", x_double, x_double_sat)
    # ---------------------------------------------------------------- M-ii level vs shape
    P("\n-- M-ii uniform multiplier s on the census edge (H1) --")
    SS = (0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.4)
    for s_ in SS:
        score_row(f"s x census edge {s_:.1f}", lambda f, s_=s_: s_ * XCEN[f][gi])
    MII = {}
    for foot in FOOTS:
        ch = np.array([ROWS[f"s x census edge {s_:.1f}"][foot]["H1"] for s_ in SS])
        jb = int(np.argmin(ch)); best = BEST[(foot, "P")]["H1"]["chi2"]
        ok = [s_ for s_, c in zip(SS, ch) if c - best <= 4]
        jj = min(max(jb, 1), len(SS) - 2)
        a, b_, c3 = np.polyfit(SS[jj - 1:jj + 2], ch[jj - 1:jj + 2], 2)
        s_ref = float(-b_ / (2 * a)) if a > 0 else float(SS[jb])
        excess = float(ch[jb] - best)
        lvl = (excess <= 1.0) and (ROWS["s x census edge 1.0"][foot]["D_H1"] > 4)
        shp = excess > 4.0
        o = np.argsort(XCEN[foot][gi]); cw = np.cumsum(wl[o]) / wl.sum(); xm = float(XCEN[foot][gi][o][np.searchsorted(cw, 0.5)])
        MII[foot] = dict(s_best_grid=SS[jb], s_best_parabola=s_ref, min_chi2_minus_bestx=excess, s_range_D4=[min(ok), max(ok)] if ok else None,
                         LEVEL=bool(lvl), SHAPE=bool(shp), x_census_median=xm, x_at_s_best=xm * s_ref)
        P(f"  [{foot}] s_best {SS[jb]} (parabola {s_ref:.3f}); min_s chi2 - best-x {excess:+.2f}; s range Delta<=4 {MII[foot]['s_range_D4']}; "
          f"x_census {xm:.3f} -> x at s_best {xm * s_ref:.3f}; LEVEL {lvl}; SHAPE {shp}")
    rta_ratio = float(np.average(RTA["canonical"][gi] / RTA["alt"][gi], weights=wl))
    der = math.sqrt(C.A0["canonical"] / C.A0["alt"]) * rta_ratio
    obs = float(np.average(XCEN["alt"][gi] / XCEN["canonical"][gi], weights=wl))
    P(f"  derived footing ratio x_alt/x_can = (a0_can/a0_alt)^1/2 * r_ta,can/r_ta,alt = {math.sqrt(C.A0['canonical'] / C.A0['alt']):.4f} x "
      f"{rta_ratio:.4f} = {der:.4f} (lens-weighted; measured from the tables {obs:.4f}); ratio of placed edges x(s_best) alt/can "
      f"{MII['alt']['x_at_s_best'] / MII['canonical']['x_at_s_best']:.4f}")
    MII["footing_ratio_derived"] = der; MII["footing_ratio_tables"] = obs
    MII["placed_ratio"] = MII["alt"]["x_at_s_best"] / MII["canonical"]["x_at_s_best"]
    RES["M_ii"] = MII
    # ---------------------------------------------------------------- verdict
    P("\n== verdict (frozen order) ==")
    mech = ROWS["M-i (a)+(b) [the M-i row]"]["pass_H1_both"]
    di = []
    for dl in (-0.10, -0.05, 0.05, 0.10):
        if ROWS[f"D1 delta {dl:+.2f} dex"]["pass_H1_both"]:
            di.append(f"D1 {dl:+.2f}")
    for nm in ("stars only", "f_cold x 2"):
        if ROWS[f"D2 {nm}"]["pass_H1_both"]:
            di.append(f"D2 {nm}")
    if RES["D3"]["status"] == "DATA-ISSUE candidate":
        di.append("D3 phase-matched f_ret 0.07")
    if ROWS["D7 census, f30 sample"]["pass_H1_both"]:
        di.append("D7 f30")
    cen = ROWS["census (interpolated)"]
    if all(cen[f]["D_H3"] <= 4 for f in FOOTS):
        di.append("D4 H3 (measured 0.2234)")
    nd = cen["alt"]["D_H2"] <= 4 and H3RANGE["alt"] <= 4
    if mech:
        V = "MECHANISM FOUND"
    elif di:
        V = "DATA-ISSUE"
    elif nd:
        V = "NOT DIAGNOSTIC"
    else:
        V = "GENUINE TENSION"
    sig = {h: math.sqrt(max(DIRR["census"]["alt"][f"D_{h}"], 0)) for h in ("H1", "H3")}
    RES["verdict"] = dict(label=V, data_issue_items=di, mechanism_row_pass=mech, not_diagnostic_test=dict(alt_D_H2=cen["alt"]["D_H2"],
                          alt_H3_range=H3RANGE["alt"], met=nd),
                          sigma_alt=dict(H1_vs_fine_best=sig["H1"], H1_vs_CFG413best=math.sqrt(DIRR["census"]["alt"]["D_H1_vs_CFG413best"]),
                                         H3=sig["H3"]))
    P(f"  M-i row passes H1 both: {mech}; DATA-ISSUE items: {di if di else 'none'}; NOT-DIAGNOSTIC test: alt D_H2 {cen['alt']['D_H2']:+.2f}, "
      f"alt H3 range {H3RANGE['alt']:.2f} -> {nd}")
    P(f"  VERDICT: {V}" + (f"  (alt census: H1 {sig['H1']:.2f} sigma vs fine best, "
                           f"{math.sqrt(DIRR['census']['alt']['D_H1_vs_CFG413best']):.2f} sigma vs CFG413 best; H3 {sig['H3']:.2f} sigma)"))
if not MUTATE:
    # ---------------------------------------------------------------- POST HOC (written after the verdict was seen; no verdict weight)
    P("\n== POST HOC (no verdict weight): how solid is the D7 f30 pass? ==")
    PH = {}
    for foot in FOOTS:
        v = [NODE[(foot, "f30")][j]["H1"] for j, x in enumerate(XN) if x >= 0.2 - 1e-12]
        PH[f"f30_node_range_{foot}"] = float(max(v) - min(v))
        P(f"  [{foot}] f30 H1 node chi2 (x >= 0.2): " + ", ".join(f"{x:.2f}:{NODE[(foot, 'f30')][j]['H1']:.1f}" for j, x in enumerate(XN)
                                                            if x >= 0.2 - 1e-12) + f"; range {PH[f'f30_node_range_{foot}']:.2f}")
        one = gstack(TB[f"{foot}|dir|one|full"], F30); dv, Cv = DAT["f30"]
        c1, _ = chi2_free(dv, Cv, hart(15), one, gstack(TT, F30))
        PH[f"f30_fret1_D_{foot}"] = c1 - BEST[(foot, "f30")]["H1"]["chi2"]
        P(f"  [{foot}] f30 f_ret = 1 (direct): Delta_H1 {PH[f'f30_fret1_D_{foot}']:+.2f}")
    for fc in (0.05, 0.07, 0.10, 0.12, 0.14, 0.18):
        score_row(f"PH f30 f_ret {fc:.2f}", lambda f, fc=fc: edge_x(f, GML, np.full(nL, fc)), sample="f30")

    def drop_one(sample, xfun):
        out = {}
        mask = MASK[sample]; dv, Cv = DAT[sample]; t = gstack(TT, mask)
        for foot in FOOTS:
            full, _ = lens_models(foot, xfun(foot)); m = lstack(full, mask)
            nodes = [gstack(TB[f"{foot}|node|full"][:, j, :], mask) for j, x in enumerate(XN) if x >= 0.2 - 1e-12]
            ds = []
            for kb in range(15):
                sel = np.array([i for i in range(15) if i != kb])
                cm, _ = chi2_free(dv[sel], Cv[np.ix_(sel, sel)], hart(14), m[sel], t[sel])
                cb = min(chi2_free(dv[sel], Cv[np.ix_(sel, sel)], hart(14), n_[sel], t[sel])[0] for n_ in nodes)
                ds.append(cm - cb)
            out[foot] = [float(min(ds)), float(max(ds))]
        return out

    PH["drop_one_census_P"] = drop_one("P", lambda f: XCEN[f][gi])
    PH["drop_one_census_f30"] = drop_one("f30", lambda f: XCEN[f][gi])
    for k in ("drop_one_census_P", "drop_one_census_f30"):
        P(f"  {k}: Delta vs best node per dropped bin: canonical {PH[k]['canonical'][0]:+.2f}..{PH[k]['canonical'][1]:+.2f}; "
          f"alt {PH[k]['alt'][0]:+.2f}..{PH[k]['alt'][1]:+.2f}")
    # the stack-P lenses that are NOT f30 (environment-richer complement)
    NF = ~F30
    DAT["nf30"] = esd_full_loo(NF); MASK["nf30"] = NF
    BEST[("canonical", "nf30")] = {}; BEST[("alt", "nf30")] = {}
    for foot in FOOTS:
        t = gstack(TT, NF); dv, Cv = DAT["nf30"]
        cs = [(float(XN[j]), chi2_free(dv, Cv, hart(15), gstack(TB[f"{foot}|node|full"][:, j, :], NF), t)[0]) for j, x in enumerate(XN) if x >= 0.2 - 1e-12]
        xb, cb = min(cs, key=lambda q: q[1]); BEST[(foot, "nf30")]["H1"] = dict(x=xb, chi2=cb)
        P(f"  [{foot}] complement (stack P minus f30, {int(NF.sum())} lenses) best node x {xb:.2f} chi2 {cb:.2f}")
    score_row("PH census, complement of f30", lambda f: XCEN[f][gi], sample="nf30")
    RES["posthoc"] = PH
RES["rows"] = ROWS
RES["lens_weight_computed_directly_below_nodes"] = {f"{k[0]}#{k[1]}": v for k, v in LOWW.items()}
if LOWW:
    P(f"  rows with lens weight below the node range (computed directly): {len(LOWW)}; max weight {max(LOWW.values()):.4f}")
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; load-bearing failures {nlb}; elapsed {RES['elapsed_s']} s")


def _js(o):
    if isinstance(o, dict):
        return {str(k): _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_js(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


json.dump(_js(RES), open(os.path.join(HERE, f"cfg525_score_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg525_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
