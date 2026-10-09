#!/usr/bin/env python3
"""CFG529 stage 1 (FROZEN_CRITERIA.md, criteria commit 33969d1a7, section 3): per f30 group (every CFG503 stack-P group holding >= 1 f30
lens), per footing, the 15-bin own-profile ESD of (a) the census edge (direct, as CFG525), (b) CFG413's sharp edge at x r_ta on the CFG525
nodes x >= 0.20, (c) f_ret = 1 (MUTATE T1), in the variants
    A (CFG503 sharp):  full, tr_{s}_W10, tr_{s}_W30
    B (CFG504 smooth): prim_full_{s}, prim_tr_{s}_W30     (edge model-intrinsic, continued flat, windowed f_t(r / r_ta,LCDM(s)), x_t prim)
plus K6 test rows: CFG504's 5.85 r_M EDGE through this lane's windowing path for 20 groups.
Model code: CFG504 cfg504_own (copied paths of CFG503 kids_Md / kids_fin / truncate and CFG504 kids_Md_ext / window; read-only import).
Output: ../../../_external_data/cfg529_work/cfg529_tables.npz ; cfg529_tables.out
Run: nice -n 10 python3 cfg529_tables.py   (4 worker processes, 1 thread each)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import time, contextlib, io
import numpy as np
import multiprocessing as MP

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
for p in (os.path.join(LANES, "CFG515_census_edge_resolution"), os.path.join(LANES, "CFG504_smooth_halo_transition"),
          os.path.join(LANES, "CFG487_settled_fraction_switch"), os.path.join(LANES, "CFG100_kids_mass_rederivation"),
          os.path.join(LANES, "CFG495_drawdown_shell")):
    sys.path.insert(0, p)
import cfg515_lib as L                                                       # noqa: E402  (read-only)
import cfg100_lib as C                                                       # noqa: E402  (read-only)
import cfg487_lib as LB                                                      # noqa: E402  (read-only)
with contextlib.redirect_stdout(io.StringIO()):
    import cfg504_own as O                                                   # noqa: E402  (read-only; __main__ guarded)
EL = O.EL
try:
    os.nice(10)
except OSError:
    pass
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg529_work")
os.makedirs(WORK, exist_ok=True)
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
OT = np.load(os.path.join(EXT, "cfg503_work", "cfg503_own_tables.npz"))
GM, GZ, GS, gi = OT["GM"], OT["GZ"], OT["GS"], OT["gi"]
NG = len(GM)
F30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
GSEL = np.unique(gi[F30])
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
XN = np.array([0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80, 0.90, 1.00])
DIRECT = {"census": None, "one": 1.0}
XTP = O.XTP
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def setup(Mg, zl, lms):
    W = {f"{s}_{k}": O.rt_weights(f"{s}_{k}", lms, zl) for s in SHMRS for k in ("W10", "W30")}
    RTL = {s: EL.r_ta_lcdm(lms, zl, s)[0] for s in SHMRS}
    XTW = {s: {w: O.xt_of(w, O.lMta_h(RTL[s], zl)) for w in O.WINS} for s in SHMRS}
    return W, RTL, XTW


def variants(Mg, zl, a0, rout, rext, W, RTL, XTW):
    """all variants for one intrinsic edge at rout (phantom settled inside, frozen beyond)."""
    r0, Md0, r, Md = O.kids_Md_ext(Mg, zl, a0, rout, max(rext, 6 * rout), intrinsic=True)
    out = {"full": O.kids_fin(Mg, r0, Md0)}
    for s in SHMRS:
        for k in ("W10", "W30"):
            out[f"tr_{s}_{k}"] = O.kids_fin(Mg, r0, O.truncate(r0, Md0, W[f"{s}_{k}"]))
        xt = XTW[s]["prim"]
        out[f"prim_full_{s}"] = O.kids_fin(Mg, r, O.window(r, Md, RTL[s], xt))
        out[f"prim_tr_{s}_W30"] = O.kids_fin(Mg, r, O.window(r, O.truncate(r, Md, W[f"{s}_W30"]), RTL[s], xt))
    return out


def work(g):
    Mg, zl, lms = GM[g], GZ[g], GS[g]
    W, RTL, XTW = setup(Mg, zl, lms)
    out = {}
    for foot in FOOTS:
        a0 = C.A0[foot]
        rta = C.r_ta_law(Mg, a0, zl)
        rext = max(max(8 * XTW[s][w] * RTL[s] for s in SHMRS for w in O.WINS), 6 * rta)      # CFG504 work_P's r_ext rule
        out[f"{foot}|rta"] = rta
        rows = [variants(Mg, zl, a0, x * rta, rext, W, RTL, XTW) for x in XN]
        for v in rows[0]:
            out[f"{foot}|node|{v}"] = np.array([rw[v] for rw in rows])
        for nm, fc in DIRECT.items():
            f = L.fret("census", Mg) if fc is None else fc
            re = L.r_edge_pm(Mg, C.G_MPC, a0, f)
            out[f"{foot}|dir|{nm}|fret"] = f
            out[f"{foot}|dir|{nm}|x"] = re / rta
            for v, arr in variants(Mg, zl, a0, min(re, rta), rext, W, RTL, XTW).items():
                out[f"{foot}|dir|{nm}|{v}"] = arr
    return g, out


def work_k6(g):
    """CFG504's 5.85 r_M EDGE through this lane's path (K6): must equal cfg504_own_tables 'EDGE|prim|full_s' / 'tr_s_W30'."""
    Mg, zl, lms = GM[g], GZ[g], GS[g]
    W, RTL, XTW = setup(Mg, zl, lms)
    out = {}
    for foot in FOOTS:
        a0 = C.A0[foot]
        rta = C.r_ta_law(Mg, a0, zl)
        rext = max(max(8 * XTW[s][w] * RTL[s] for s in SHMRS for w in O.WINS), 6 * rta)
        re1 = float(LB.r_edge(Mg, C.G_MPC, a0))
        v = variants(Mg, zl, a0, re1, rext, W, RTL, XTW)
        for s in SHMRS:
            out[f"{foot}|full_{s}"] = v[f"prim_full_{s}"]
            out[f"{foot}|tr_{s}_W30"] = v[f"prim_tr_{s}_W30"]
    return g, out


if __name__ == "__main__":
    P(__doc__.split("Run:")[0].strip())
    P(f"stack-P groups {NG}; f30 groups {len(GSEL)}; f30 lenses {int(F30.sum())}; nodes {XN.tolist()}; x_t prim {XTP:.4f}")
    rng = np.random.default_rng(529)
    K6G = np.sort(rng.choice(GSEL, 20, replace=False))
    with MP.get_context("fork").Pool(4) as pool:
        res = pool.map(work, list(GSEL), chunksize=4)
        P(f"  f30 group tables done ({time.time() - T0:.0f} s)")
        rk6 = pool.map(work_k6, list(K6G))
    keys = res[0][1].keys()
    TAB = {}
    for k in keys:
        a0_ = np.asarray(res[0][1][k])
        arr = np.full((NG,) + a0_.shape, np.nan)
        for g, o in res:
            arr[g] = o[k]
        TAB[k] = arr
    for k in rk6[0][1]:
        TAB[f"K6|{k}"] = np.array([o[k] for _, o in rk6])
    TAB["K6G"] = K6G; TAB["XN"] = XN; TAB["GSEL"] = GSEL
    np.savez(os.path.join(WORK, "cfg529_tables.npz"), **TAB)
    P(f"built {len(TAB)} arrays in {time.time() - T0:.0f} s -> _external_data/cfg529_work/cfg529_tables.npz")
    for foot in FOOTS:
        x = TAB[f"{foot}|dir|census|x"][GSEL]
        P(f"  [{foot}] f30 groups: census x_edge median {np.median(x):.3f} (min {x.min():.3f}, max {x.max():.3f})")
    open(os.path.join(HERE, "cfg529_tables.out"), "w").write("\n".join(LOG) + "\n")
