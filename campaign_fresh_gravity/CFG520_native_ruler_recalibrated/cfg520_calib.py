#!/usr/bin/env python3
"""CFG520 calibration (FROZEN_CRITERIA.md sections 1-2; criteria commit 6d184c37d).

1. Target: CFG519's parent (ALL candidates) satellite fraction S_IC per (log M*, z) cell, from CFG519's own state and cell code (C_T check);
   T_a = W-weighted over z 0.1-0.4 for a = [10.50, 10.75), [10.75, 11.00).
2. Fit the occupation constant B (primary; alpha = 1) on the two S0 512^3 catalogues ONLY; CAL-OK; declared (B, alpha) fallback.
3. C_A: drawn catalogue vs expectation. Blindness: list of files opened.
MUTATE (CFG520_MUTATE=1): the same procedure with every target doubled (M2X); writes cfg520_calib_results_MUTATE.json.
Run: nice -n 10 python3 -u cfg520_calib.py ; CFG520_MUTATE=1 nice -n 10 python3 -u cfg520_calib.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import json, math, time
import numpy as np
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg520_lib as LB  # noqa: E402

MUT = os.environ.get("CFG520_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
OPENED = []
LOG, CHK, RES = [], {}, {"lane": "CFG520", "script": "cfg520_calib", "mutate": MUT}
T0 = time.time()


def say(s=""):
    print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


def load(path):
    OPENED.append(os.path.relpath(path, EXT)); return np.load(path)


say(__doc__.split("Run:")[0].strip())
say(f"mode: {'MUTATE M2X (targets doubled)' if MUT else 'MAIN'}")

# ================================================================= 1. target (CFG519's state + cell code)
X = load(os.path.join(EXT, "cfg519_work", "cfg519_state.npz"))
S = load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
llm, lz, ltyp = S["logM"], S["z"], S["typ"]
iso10 = S["iso10"]; wl = S["WW"].sum(1); NA = len(lz)
inside, L_m, REG, S_IC, cell = X["inside"], X["L_m"], X["REG"], X["S_IC"], X["cell"]
ME = np.array([8.5, 9.5, 10.0, 10.25, 10.5, 10.75, 11.0]); ZE = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
NCM, NCZ = len(ME) - 1, len(ZE) - 1; NC = NCM * NCZ * 2
cm = np.clip(np.digitize(llm, ME) - 1, 0, NCM - 1); cz = np.clip(np.digitize(lz, ZE) - 1, 0, NCZ - 1)
assert np.array_equal(cell, (cm * NCZ + cz) * 2 + ltyp)


def cell_frac(val, src, w=wl):                       # CFG519's cell_frac, copied
    num = np.bincount(cell[src], weights=(w * val)[src], minlength=NC)
    den = np.bincount(cell[src], weights=w[src], minlength=NC)
    n = np.bincount(cell[src], minlength=NC)
    f = np.full(NC, np.nan); direct = n >= 20
    f[direct] = num[direct] / den[direct]
    n3 = n.reshape(NCM, NCZ, 2); num3 = num.reshape(NCM, NCZ, 2); den3 = den.reshape(NCM, NCZ, 2)
    f3 = f.reshape(NCM, NCZ, 2)
    for a in range(NCM):
        for t in range(2):
            for zc in range(NCZ):
                if np.isnan(f3[a, zc, t]):
                    if n3[a, :, t].sum() >= 20:
                        f3[a, zc, t] = num3[a, :, t].sum() / den3[a, :, t].sum()
                    elif n3[a].sum() >= 20:
                        f3[a, zc, t] = num3[a].sum() / den3[a].sum()
    return f3.reshape(NC), n


def reweight(val, src, tgt, w=wl):                   # CFG519's reweight, copied
    f, n = cell_frac(val, src, w)
    W = np.bincount(cell[tgt], weights=w[tgt], minlength=NC)
    good = np.isfinite(f)
    return float((W[good] * f[good]).sum() / W[good].sum())


ALLC = np.ones(NA, bool)
fpar0 = reweight(S_IC.astype(float), inside & L_m, ALLC)
fic0 = reweight(S_IC.astype(float), iso10 & inside & L_m, iso10)
check("C_T target code reproduces CFG519's f_ALL_parent and ISO f_IC (1e-9)",
      abs(fpar0 - 0.3133864614828175) < 1e-9 and abs(fic0 - 0.22342746446430256) < 1e-9, f"parent {fpar0:.10f}, ISO {fic0:.10f}")
WALL = np.bincount(cell, weights=wl, minlength=NC).reshape(NCM, NCZ, 2)


def cell_table(excl=-1):
    use = REG != excl
    f, n = cell_frac(S_IC.astype(float), inside & L_m & use)
    f3 = f.reshape(NCM, NCZ, 2)
    tab = np.full((NCM, NCZ), np.nan)
    for a in range(NCM):
        for zc in range(NCZ):
            w_ = WALL[a, zc]; g = np.isfinite(f3[a, zc]) & (w_ > 0)
            if g.any():
                tab[a, zc] = (w_[g] * f3[a, zc][g]).sum() / w_[g].sum()
    # calibration targets: a = 4 ([10.50, 10.75)), 5 ([10.75, 11.00)); z cells 0..2
    T = np.array([(WALL[a, :3].sum(1) * tab[a, :3]).sum() / WALL[a, :3].sum() for a in (4, 5)])
    return tab, T


TAB, T = cell_table()
jk = [cell_table(k) for k in range(12)]
sT = np.sqrt(11 / 12 * ((np.array([j[1] for j in jk]) - np.mean([j[1] for j in jk], 0)) ** 2).sum(0))
sTAB = np.sqrt(11 / 12 * ((np.array([j[0] for j in jk]) - np.mean([j[0] for j in jk], 0)) ** 2).sum(0))
say("\nCFG519 parent (ALL) satellite fraction S_IC per (log M*, z_phot) cell, colour pooled with the ALL weight (12-region jackknife):")
say("  log M*       | " + " | ".join(f"z {ZE[i]:.1f}-{ZE[i + 1]:.1f}" for i in range(NCZ)))
for a in range(NCM):
    say(f"  {ME[a]:5.2f}-{ME[a + 1]:5.2f} | " + " | ".join(f"{TAB[a, i]:.3f}+-{sTAB[a, i]:.3f}" for i in range(NCZ)))
EDGES = np.array([10.5, 10.75, 11.0])
wa = np.array([wl[iso10 & (llm >= EDGES[i]) & (llm < EDGES[i + 1])].sum() for i in range(2)])
say(f"targets T_a (z 0.1-0.4): [10.50, 10.75) {T[0]:.4f} +- {sT[0]:.4f}; [10.75, 11.00) {T[1]:.4f} +- {sT[1]:.4f}; "
    f"stack-P ISO weight shares {np.round(wa / wa.sum(), 3).tolist()}")
RES["target"] = dict(cells={f"{ME[a]:.2f}-{ME[a + 1]:.2f}|{ZE[i]:.1f}-{ZE[i + 1]:.1f}": dict(f=float(TAB[a, i]), sig=float(sTAB[a, i]))
                            for a in range(NCM) for i in range(NCZ)},
                     T=T.tolist(), sig_T=sT.tolist(), edges=EDGES.tolist(), w_a=(wa / wa.sum()).tolist(), f_ALL_parent=fpar0, f_IC=fic0)
TT = 2 * T if MUT else T.copy()
if MUT:
    say(f"MUTATE M2X: targets doubled -> {np.round(TT, 4).tolist()}")

# ================================================================= 2. S0 catalogues only
S0KEYS = ("S0512_359", "S0512_360")
CAT = {}
for k in S0KEYS:
    Z = load(os.path.join(EXT, "cfg506_work", f"cfg506_box_{k}.npz"))
    CAT[k] = dict(Mta=Z["Mta"], MP=float(Z["MP"]), rta=Z["rta"], r200m=Z["r200m"], cen=Z["cen"].astype(np.float64))


def fbox(B, alpha):
    return np.mean([LB.Sham(CAT[k]["Mta"], CAT[k]["MP"], B, alpha).parent_fraction_expect(EDGES) for k in S0KEYS], axis=0)


def obj(lB, alpha):
    fb = fbox(10 ** lB, alpha)
    return float((wa * (fb - TT) ** 2).sum())


def fit_B(alpha, coarse_step=0.05):
    """grid over log10 B in [0.5, 3.5] then bounded refinement to 1e-4 dex. Primary: the full 0.005-dex grid (frozen). Fallback scan
    (disclosed implementation detail, for run time): 0.05-dex coarse grid, then 0.005 dex around its best, then the refinement."""
    g1 = np.arange(0.5, 3.5 + 1e-9, coarse_step); v1 = np.array([obj(x, alpha) for x in g1])
    i = int(np.argmin(v1)); lo, hi = g1[max(i - 1, 0)], g1[min(i + 1, len(g1) - 1)]
    g2 = np.arange(lo, hi + 1e-9, 0.005); v2 = np.array([obj(x, alpha) for x in g2])
    j = int(np.argmin(v2)); a_, b_ = g2[max(j - 1, 0)], g2[min(j + 1, len(g2) - 1)]
    r = minimize_scalar(lambda x: obj(x, alpha), bounds=(a_, b_), method="bounded", options=dict(xatol=1e-4))
    return float(r.x), float(r.fun)


def cal_ok(fb):
    mb = float((wa * fb).sum() / wa.sum()); mt = float((wa * TT).sum() / wa.sum())
    return bool(np.all(np.abs(fb - TT) <= 0.05) and abs(mb - mt) <= 0.02), mb, mt


say("\nB = 17 (CFG506) on the S0 catalogues: f_box " + str(np.round(fbox(17.0, 1.0), 4).tolist()))
lB, J_ = fit_B(1.0, coarse_step=0.005)          # primary: the full 0.005-dex grid as frozen
fb = fbox(10 ** lB, 1.0)
ok, mb, mt = cal_ok(fb)
say(f"primary (alpha = 1): B* = {10 ** lB:.3f} (log {lB:.4f}); f_box {np.round(fb, 4).tolist()} vs T {np.round(TT, 4).tolist()}; "
    f"weighted mean {mb:.4f} vs {mt:.4f} -> CAL-OK {ok}")
RES["primary"] = dict(B=10 ** lB, alpha=1.0, f_box=fb.tolist(), mean_box=mb, mean_T=mt, cal_ok=ok)
FORM = "primary"; Bc, Ac = 10 ** lB, 1.0
if not ok:
    say("primary fails CAL-OK -> declared fallback (B, alpha)")
    best = None; scan = []
    for al in np.round(np.arange(0.30, 1.5001, 0.01), 2):
        lb_, j_ = fit_B(float(al))
        scan.append((float(al), lb_, j_))
        if best is None or j_ < best[2]:
            best = (float(al), lb_, j_)
    al, lb_, _ = best
    fb = fbox(10 ** lb_, al); ok, mb, mt = cal_ok(fb)
    say(f"fallback: alpha* = {al:.2f}, B* = {10 ** lb_:.3f}; f_box {np.round(fb, 4).tolist()} vs T {np.round(TT, 4).tolist()}; "
        f"weighted mean {mb:.4f} vs {mt:.4f} -> CAL-OK {ok}")
    RES["fallback"] = dict(B=10 ** lb_, alpha=al, f_box=fb.tolist(), mean_box=mb, mean_T=mt, cal_ok=ok, scan=scan)
    FORM = "fallback"; Bc, Ac = 10 ** lb_, al
RES["rule"] = dict(form=FORM, B=Bc, alpha=Ac, cal_ok=ok)
if not ok:
    say("CALIBRATION FAILED (frozen): no validation, no re-score.")

# ================================================================= 3. C_A and diagnostics at the calibrated rule
from scipy.spatial import cKDTree
fine = np.arange(10.0, 11.11, 0.1)
for k in S0KEYS:
    c = CAT[k]; sh = LB.Sham(c["Mta"], c["MP"], Bc, Ac)
    tree = cKDTree(c["cen"] % LB.L, boxsize=LB.L)
    _, GLMS, GSAT, _, _, _, _, _ = LB.draw_galaxies(sh, c["cen"], c["Mta"], c["rta"], c["r200m"], None, tree)
    drawn = np.array([GSAT[(GLMS >= EDGES[i]) & (GLMS < EDGES[i + 1])].mean() for i in range(2)])
    ex = sh.parent_fraction_expect(EDGES)
    check(f"C_A [{k}] drawn vs expected parent fraction within 0.01 per calibration bin", bool(np.all(np.abs(drawn - ex) <= 0.01)),
          f"drawn {np.round(drawn, 4).tolist()}, expected {np.round(ex, 4).tolist()}")
    say(f"  [{k}] m_lim,box {sh.mlim_box:.2f}; log M_min(10.5) {float(sh.lMmin_of_m(10.5)):.2f}, (11.0) {float(sh.lMmin_of_m(11.0)):.2f}; "
        f"parent fraction per 0.1 dex (expected) " + ", ".join(f"{a:.1f}: {v:.3f}" for a, v in zip(fine[:-1], sh.parent_fraction_expect(fine))))
    RES[f"diag_{k}"] = dict(m_lim_box=sh.mlim_box, lMmin_10p5=float(sh.lMmin_of_m(10.5)), lMmin_11=float(sh.lMmin_of_m(11.0)),
                            fpar_fine=sh.parent_fraction_expect(fine).tolist(), drawn=drawn.tolist(), expected=ex.tolist())

blind = all(("TA" not in p) and ("esd" not in p.lower()) and ("cfg110" not in p) for p in OPENED)
check("blindness: only S0 catalogues, CFG519 state, CFG502 staging opened (no TA box, no shear/ESD file)", blind, "; ".join(OPENED))
RES["opened"] = OPENED
RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, f"cfg520_calib_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg520_calib{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if any(c["load_bearing"] and not c["ok"] for c in CHK.values()) else 0)
