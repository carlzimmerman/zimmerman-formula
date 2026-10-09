#!/usr/bin/env python3
"""CFG525 stage 1 (FROZEN_CRITERIA.md 7f99a4371, section 0): per stack-P group, per footing, the 15-bin own-profile ESD of CFG413's sharp
edge at x r_ta on the frozen node grid, in three variants (full; CFG503 W10 stripping with Moster / Behroozi tidal weights), plus DIRECT
rows for the census edge (CFG515), f_ret = 1 and f_ret = 0.01 (MUTATE teeth).  Model code: CFG503 cfg503_own (read-only).
Output: ../../../_external_data/cfg525_work/cfg525_tables.npz ; cfg525_tables.out
Run: nice -n 10 python3 cfg525_tables.py   (4 worker processes, 1 thread each)
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
for p in (os.path.join(LANES, "CFG515_census_edge_resolution"), os.path.join(LANES, "CFG503_two_halo_nonlinear"),
          os.path.join(LANES, "CFG487_settled_fraction_switch"), os.path.join(LANES, "CFG100_kids_mass_rederivation"),
          os.path.join(LANES, "CFG495_drawdown_shell")):
    sys.path.insert(0, p)
import cfg515_lib as L                                                       # noqa: E402  (read-only)
import cfg100_lib as C                                                       # noqa: E402  (read-only)
with contextlib.redirect_stdout(io.StringIO()):
    import cfg503_own as OWN                                                 # noqa: E402  (read-only)
try:
    os.nice(10)
except OSError:
    pass
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg525_work"))
os.makedirs(WORK, exist_ok=True)
W503 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
OT = np.load(os.path.join(W503, "cfg503_own_tables.npz"))
GM, GZ, GS = OT["GM"], OT["GZ"], OT["GS"]
NG = len(GM)
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
XN = np.array([0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60,
               0.70, 0.80, 0.90, 1.00])
DIRECT = {"census": None, "one": 1.0, "dep01": 0.01}
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def work(args):
    Mg, zl, lms = args
    W = {s: OWN.rt_weights(f"{s}_W10", lms, zl) for s in SHMRS}
    out = {}
    for foot in FOOTS:
        a0 = C.A0[foot]
        rta = C.r_ta_law(Mg, a0, zl)
        out[f"{foot}|rta"] = rta
        nodes = {v: [] for v in ("full",) + tuple(f"tr_{s}" for s in SHMRS)}
        for x in XN:
            r, Md = OWN.kids_Md(Mg, zl, a0, x * rta)
            nodes["full"].append(OWN.kids_fin(Mg, r, Md))
            for s in SHMRS:
                nodes[f"tr_{s}"].append(OWN.kids_fin(Mg, r, OWN.truncate(r, Md, W[s])))
        for v, arr in nodes.items():
            out[f"{foot}|node|{v}"] = np.array(arr)
        for nm, fc in DIRECT.items():
            f = L.fret("census", Mg) if fc is None else fc
            re = L.r_edge_pm(Mg, C.G_MPC, a0, f)
            r, Md = OWN.kids_Md(Mg, zl, a0, min(re, rta))
            out[f"{foot}|dir|{nm}|fret"] = f
            out[f"{foot}|dir|{nm}|x"] = re / rta
            out[f"{foot}|dir|{nm}|full"] = OWN.kids_fin(Mg, r, Md)
            for s in SHMRS:
                out[f"{foot}|dir|{nm}|tr_{s}"] = OWN.kids_fin(Mg, r, OWN.truncate(r, Md, W[s]))
    return out


if __name__ == "__main__":
    P(__doc__.split("Run:")[0].strip())
    P(f"groups {NG}; nodes {len(XN)}: {XN.tolist()}")
    t = time.time()
    with MP.get_context("fork").Pool(4) as pool:
        res = pool.map(work, list(zip(GM, GZ, GS)), chunksize=4)
    TAB = {k: np.array([r_[k] for r_ in res]) for k in res[0]}
    TAB["XN"] = XN
    np.savez(os.path.join(WORK, "cfg525_tables.npz"), **TAB)
    P(f"built {len(TAB)} arrays in {time.time() - t:.0f} s -> {os.path.relpath(os.path.join(WORK, 'cfg525_tables.npz'), REPO)}")
    for foot in FOOTS:
        P(f"  [{foot}] median r_ta {np.median(TAB[f'{foot}|rta']):.3f} Mpc; census x_edge median {np.median(TAB[f'{foot}|dir|census|x']):.3f} "
          f"(min {TAB[f'{foot}|dir|census|x'].min():.3f}, max {TAB[f'{foot}|dir|census|x'].max():.3f})")
    open(os.path.join(HERE, "cfg525_tables.out"), "w").write("\n".join(LOG) + "\n")
