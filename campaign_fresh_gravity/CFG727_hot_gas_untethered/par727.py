"""Parallel driver for CFG727's eRASS stage (implementation only: the lane's own functions, exec'd unchanged; same per-cluster
inputs, same order; output identical to the serial stage).  Verifies the first clusters against the serial partial file
before writing.  Usage: python3 par727.py <path/to/cfg727.py> [workers]"""
import os, sys, time
import numpy as np
from multiprocessing import Pool
SRC = os.path.abspath(sys.argv[1]); NW = int(sys.argv[2]) if len(sys.argv) > 2 else 10
os.environ["CFG727_MODE"] = "defs"
txt = open(SRC).read().split("# ============================================================================================ eRASS1 (CFG687)")[0]
G = {"__file__": SRC, "__name__": "cfg727_defs"}
exec(compile(txt, SRC, "exec"), G)
d = np.load(os.path.join(G["LANES"], "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
def one(i):
    np_ = G["np"]; R5, mgas = float(d["R500"][i]), float(d["mg"][i])
    r = G["RGRID"]; rc = 0.15 * R5; shape = (1 + (r / rc) ** 2) ** (-1.0); shape[r > 3.0] = 0
    dm = 4 * np_.pi * (r * G["MPC"]) ** 2 * shape; Mm = np_.r_[0, np_.cumsum(0.5 * (dm[1:] + dm[:-1]) * np_.diff(r * G["MPC"]))]
    Mg = Mm * (mgas / np_.interp(R5, r, Mm))
    return G["cluster_runs"](Mg, 0.20, float(d["z"][i]), R5 * 1000.0)
def flat(o):
    out = []
    for k in sorted(o):
        v = o[k]
        if isinstance(v, dict):
            out += flat(v)
        elif isinstance(v, (np.ndarray, list, float, int)):
            out.append(np.asarray(v, dtype=float).ravel())
    return out
if __name__ == "__main__":
    T0 = time.time(); n = len(d["mg"]); W = G["WORK"]
    with Pool(NW) as pool:
        res = pool.map(one, range(n), chunksize=1)
    part = list(np.load(os.path.join(W, "erass_partial.npy"), allow_pickle=True)) if os.path.exists(os.path.join(W, "erass_partial.npy")) else []
    nchk = min(len(part), n); bad = 0
    for i in range(nchk):
        a, b = flat(res[i]), flat(part[i])
        if len(a) != len(b) or any(not np.allclose(x, y, rtol=1e-10, atol=0) for x, y in zip(a, b)):
            bad += 1
    print(f"par727: {n} clusters, {NW} workers, {time.time() - T0:.0f} s; check vs serial partial: {nchk - bad}/{nchk} identical", flush=True)
    if bad:
        print("MISMATCH vs serial - not writing erass.npy", flush=True); sys.exit(2)
    tmp = os.path.join(W, "erass_tmp.npy"); np.save(tmp, np.array(res, dtype=object), allow_pickle=True)
    os.replace(tmp, os.path.join(W, "erass.npy")); print("wrote erass.npy", flush=True)
