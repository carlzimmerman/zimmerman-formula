#!/usr/bin/env python3
"""CFG967 POST HOC diagnostics (not frozen, no verdict weight; written after the frozen score was seen).
Is the NO EFFECT reading a property of the term or of the exclusion choice, and can the pipeline see a slope change at all?
  (a) per gas tercile: W-weighted two-halo OUTER/MID stack under E0 (no exclusion), X2, X1 (primary), vs the law, and the
      additive OUTER term each tercile would need for A_OUTER = 1;
  (b) amplitude scan s(lambda) for the E0 and X2 terms, and the lambda that would reach s_obs - 1 sigma;
  (c) a planted term that grows with mass, T = 0.5 law (Mgas/median)^0.43, must move the slope by about +0.14.
Inputs: cfg967_tables.npz (stage A), CFG687 per-cluster file, CFG687 law() exec'd with nu_s (as cfg967_score.py).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg967_posthoc.py   -> cfg967_posthoc.out, cfg967_posthoc.json
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import contextlib, io, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES); os.environ.pop("MUTATE", None)
import CFG4_common as C4                                                      # noqa: E402
A0 = {"canonical": float(C4.A0["canonical"]), "alt": float(C4.A0["alt"])}
SRC686 = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py"); TXT686 = open(SRC686).read()
NS6 = {"__file__": SRC686, "__name__": "cfg686"}; _argv = sys.argv; sys.argv = [SRC686, "UNUSED"]
with contextlib.redirect_stdout(io.StringIO()):
    exec(TXT686.split("# ---- sources ----")[0], NS6)
    NS6["EDGES"] = np.logspace(np.log10(0.15), np.log10(3.0), 9); NS6["RC"] = np.sqrt(NS6["EDGES"][1:] * NS6["EDGES"][:-1]); NS6["M_BIAS"] = -0.01
    exec(TXT686.split("# ---- the law's prediction from ACCEPT gas ----")[1].split("# ---- measure ----")[0], NS6)
sys.argv = _argv
def nu_s(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 0.5 + np.sqrt(0.25 + 1.0 / y)
TXT687 = open(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_stack.py")).read()
ns = dict(RGRID=NS6["RGRID"], MPC=NS6["MPC"], MSUN=NS6["MSUN"], G=NS6["G"], nu_mono=nu_s, sigma_proj=NS6["sigma_proj"], RC=NS6["RC"], KG=NS6["KG_PER_MSUN_PC2"], np=np)
exec("def law(" + TXT687.split("def law(")[1].split("BR = [")[0], ns); law = ns["law"]
PC = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
D, E, mg, R500 = (np.asarray(PC[k], float) for k in ("D", "E", "mg", "R500")); N = len(mg)
W = np.where(E > 0, 1 / E ** 2, 0)
q = np.quantile(mg, [0, 1 / 3, 2 / 3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2); ALL = np.ones(N, bool)
J = {"MID": [3, 4, 5], "OUTER": [6, 7]}
def wm(sel, arr, b): j = J[b]; return float((W[sel][:, j] * arr[sel][:, j]).sum() / W[sel][:, j].sum())
def A(sel, Pm, b): j = J[b]; return float((W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum())
def slope(arr):                                                               # CFG687 T2, verbatim
    xs, ys = [], []
    for k in range(3):
        s = tid == k; v = wm(s, arr, "OUTER")
        if v <= 0: return np.nan
        xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10(v))
    return float(np.polyfit(xs, ys, 1)[0])
TB = np.load(os.path.join(HERE, "cfg967_tables.npz"))
S_OBS, S_ERR = 0.8958077850439714, 0.20930889609694792                         # CFG687 T2 (reproduced by cfg967_score K1)
OUT, RES = [], {}
def P(s=""): print(s, flush=True); OUT.append(s)
P("CFG967 POST HOC diagnostics (no verdict weight)")
for foot in ("canonical", "alt"):
    Pl = np.array([law(dict(Mgas500=mg[i], R500=R500[i]), A0[foot]) for i in range(N)]); s0 = slope(Pl)
    T = {x: TB[f"L_{foot}|V0P1{x}"] - TB[f"R_{foot}|V0P1{x}"] for x in ("X1", "X2", "E0")}
    P(f"\n{foot}: law alone s = {s0:.4f}")
    r = {"terciles": {}, "scan": {}, "planted": {}}
    for k in range(3):
        s = tid == k; lo = wm(s, Pl, "OUTER"); need = (A(s, Pl, "OUTER") - 1) * lo
        row = dict(law_outer=lo, need_outer_for_A1=need, **{f"T_{x}_{b}": wm(s, T[x], b) for x in T for b in ("MID", "OUTER")})
        r["terciles"][k] = row
        P(f"  tercile {k}: law OUTER {lo:6.2f}; needed additive OUTER for A_OUTER = 1: {need:+6.2f} Msun/pc^2; two-halo OUTER E0 {row['T_E0_OUTER']:+.2f}, "
          f"X2 {row['T_X2_OUTER']:+.2f}, X1 {row['T_X1_OUTER']:+.2f}; MID E0 {row['T_E0_MID']:+.2f}")
    for x in ("E0", "X2"):
        sc = {lam: slope(Pl + lam * T[x]) for lam in (1, 2, 5, 10, 20, 50)}
        lo_, hi_ = 0.0, 1000.0; tgt = S_OBS - S_ERR; lam_need = None
        if slope(Pl + hi_ * T[x]) >= tgt > s0:
            for _ in range(60):
                mid = 0.5 * (lo_ + hi_); lo_, hi_ = (mid, hi_) if slope(Pl + mid * T[x]) < tgt else (lo_, mid)
            lam_need = 0.5 * (lo_ + hi_)
        r["scan"][x] = dict(s=sc, lambda_for_s_obs_minus_1sigma=lam_need)
        P(f"  amplitude scan {x}: " + ", ".join(f"x{l}: {v:.3f}" for l, v in sc.items()) + f"; lambda for s_obs - 1 sigma ({tgt:.3f}): {lam_need}")
    Tp = 0.5 * Pl * (mg / np.median(mg))[:, None] ** 0.43
    sp = slope(Pl + Tp); r["planted"] = dict(s=sp, ds=sp - s0)
    P(f"  planted T = 0.5 law (Mgas/median)^0.43: s {s0:.4f} -> {sp:.4f} (ds {sp - s0:+.4f}; expected about +0.14): pipeline sees a mass-growing term")
    RES[foot] = r
json.dump(RES, open(os.path.join(HERE, "cfg967_posthoc.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg967_posthoc.out"), "w").write("\n".join(OUT) + "\n")
