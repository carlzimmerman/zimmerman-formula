#!/usr/bin/env python3
"""CB1 Part B: count-only baselines for Leisher+ 2026. Frozen criteria: FROZEN_CRITERIA.md (53735de87f). One thread.

    python3 cb1_part_b.py synthetic                  -> K3 and K4 only, cb1_part_b_synthetic.out (no simulation data)
    python3 cb1_part_b.py extract <tree_dir> <out.npz>  -> reads <tree_dir>/box_<n>/tree_extended.hdf5, selected fields only
    python3 cb1_part_b.py grade <counts.npz>         -> the frozen grades, cb1_part_b_results.json
"""
import json, os, sys
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
REMOVED = [1, 2, 4, 5, 6, 9, 10, 11, 14, 17, 18, 19, 20, 21, 30, 42, 88]         # merger_tree_script.py
ALPHAS = np.logspace(-4, 4, 33); H = 0.6909; NSNAP = 91

def walk(fp, np_, root_id, root_index):
    """Indices of the authors' walk: root, root's next progenitors, then every first and next progenitor below them. Iterative, same set of nodes."""
    def ix(i): return root_index + (i - root_id)
    seen = [root_index]; starts = [root_index]; n = np_[root_index]
    while n != -1:
        seen.append(ix(n)); starts.append(ix(n)); n = np_[ix(n)]
    stack = list(starts)
    while stack:
        i = stack.pop(); f = fp[i]
        while f != -1:
            k = ix(f); seen.append(k); m = np_[k]
            while m != -1:
                q = ix(m); seen.append(q); stack.append(q); m = np_[q]
            f = fp[k]
    return np.array(seen, dtype=np.int64)
def walk_recursive(fp, np_, root_id, root_index):        # the authors' recursion, as reference for K4
    def ix(i): return root_index + (i - root_id)
    seen = [root_index]; starts = [root_index]; n = np_[root_index]
    while n != -1:
        seen.append(ix(n)); starts.append(ix(n)); n = np_[ix(n)]
    def go(i):
        f = fp[i]
        while f != -1:
            k = ix(f); seen.append(k); m = np_[k]
            while m != -1:
                q = ix(m); seen.append(q); go(q); m = np_[q]
            f = fp[k]
    for s in starts: go(s)
    return np.array(seen, dtype=np.int64)

def extract_box(path):
    import h5py
    with h5py.File(path, "r") as t:
        keys = ["SnapNum", "SubhaloID", "FirstProgenitorID", "NextProgenitorID", "FirstSubhaloInFOFGroupID"]
        d = {k: np.array(t[k]) for k in keys}; gmt = np.array(t["GroupMassType"]); smt = np.array(t["SubhaloMassType"])
    masses = gmt * 1e10 / H; tot = masses.sum(1); con = masses[:, 2] / tot
    cut = (tot > 7e11) & (tot < 2.5e12) & (d["SnapNum"] == 90)
    mw = np.arange(len(tot))[cut][np.argmin(con[cut])]; target = d["FirstSubhaloInFOFGroupID"][mw]
    at90 = np.where(d["SnapNum"] == 90)[0]; root = at90[np.argmin(np.abs(d["FirstSubhaloInFOFGroupID"][at90] - target))]
    idx = walk(d["FirstProgenitorID"], d["NextProgenitorID"], d["SubhaloID"][root], root)
    sn = d["SnapNum"][idx]; cnt = np.bincount(sn, minlength=NSNAP)[:NSNAP]
    mdm = np.bincount(sn, weights=smt[idx, 1] * 1e10 / H, minlength=NSNAP)[:NSNAP]
    n, f = 1, d["FirstProgenitorID"][root]
    while f != -1:
        k = root + (f - d["SubhaloID"][root]); n += 1; f = d["FirstProgenitorID"][k]
    return dict(N=int(len(idx)), counts=cnt, mdm=mdm, main=n)

def models():
    def ridge(): return make_pipeline(StandardScaler(), RidgeCV(alphas=ALPHAS, cv=5))
    return {"B0 cubic": ("N", lambda: make_pipeline(StandardScaler(), PolynomialFeatures(3), RidgeCV(alphas=[1e-6], cv=None))),
            "B0 isotonic": ("N1", lambda: IsotonicRegression(increasing="auto", out_of_bounds="clip")),
            "B1 ridge": ("C", ridge), "B1 gboost": ("C", lambda: GradientBoostingRegressor(random_state=0)),
            "B2 ridge": ("CM", ridge), "B3 main": ("B", lambda: make_pipeline(StandardScaler(), PolynomialFeatures(3), RidgeCV(alphas=[1e-6], cv=None)))}
def feats(D):
    lN = np.log10(D["N"])[:, None]; C = np.log1p(D["counts"]); M = np.log10(1 + D["mdm"])
    return {"N": lN, "N1": lN[:, 0], "C": C, "CM": np.hstack([C, M]), "B": D["main"][:, None].astype(float)}
def r2_rmse(t, p):
    t, p = np.asarray(t), np.asarray(p)
    return 1 - np.sum((t - p) ** 2) / np.sum((t - t.mean()) ** 2), float(np.sqrt(np.mean((t - p) ** 2)))
def fitpred(make, Xtr, ytr, Xte): return make().fit(Xtr, ytr).predict(Xte)
def evaluate(D, y, test, n_rep=200, n_boot=10000, seed=20261030):
    F = feats(D); res = {}; all_i = np.arange(len(y)); tr = np.setdiff1d(all_i, test); rng = np.random.default_rng(seed)
    for name, (k, make) in models().items():
        X = F[k]; p = fitpred(make, X[tr], y[tr], X[test]); r2, rm = r2_rmse(y[test], p)
        b = rng.integers(0, len(test), (n_boot, len(test))); bs = [r2_rmse(y[test][i], p[i])[0] for i in b[:: max(1, n_boot // 2000)]]
        rep = []
        for s in range(n_rep):
            pr = np.random.default_rng(seed + s).permutation(all_i); cut = int(0.8 * len(y))
            rep.append(r2_rmse(y[pr[cut:]], fitpred(make, X[pr[:cut]], y[pr[:cut]], X[pr[cut:]]))[0])
        cond = {}
        for t in (6.0, 9.7):
            s = 1 / y[test] > t; cond[str(t)] = r2_rmse(y[test][s], p[s])[0] if s.sum() > 2 else None
        res[name] = dict(r2=r2, rmse=rm, boot=np.percentile(bs, [2.5, 97.5]).tolist(), rep=np.percentile(rep, [2.5, 50, 97.5]).tolist(), cond=cond)
        P(f"  {name:12s} test R2 {r2:+.3f} RMSE {rm:.3f}; bootstrap 95% [{res[name]['boot'][0]:+.3f}, {res[name]['boot'][1]:+.3f}]; repeated-split 95% [{res[name]['rep'][0]:+.3f}, {res[name]['rep'][2]:+.3f}]; R2 >6 keV {cond['6.0']}, >9.7 keV {cond['9.7']}")
    return res

def synthetic():
    P("CB1 Part B synthetic checks (no simulation data)")
    rng = np.random.default_rng(1)
    # K4: walk vs the authors' recursion on random trees, with IDs in depth-first order
    ok = True
    for tr in range(20):
        fp, np_ = [], []
        def build():
            i = len(fp); fp.append(-1); np_.append(-1)
            if rng.random() < 0.75 and i < 3000:
                c = build(); fp[i] = c
                while rng.random() < 0.3 and i < 3000:
                    s = build(); e = c
                    while np_[e] != -1: e = np_[e]
                    np_[e] = s
            return i
        import sys as _s; _s.setrecursionlimit(20000)
        build(); fa = np.array(fp); na = np.array(np_)
        ok &= sorted(walk(fa, na, 0, 0).tolist()) == sorted(walk_recursive(fa, na, 0, 0).tolist())
    P(f"K4 iterative walk = authors' recursion on 20 random trees: {'PASS' if ok else 'FAIL'}")
    # K3: planted count law
    S = np.loadtxt(os.path.join(HERE, "authors_code", "WDM_TNG_MW_SB4_parameters.txt")); y = S[:, 0]; n = len(y)
    def make(sig):
        z = rng.normal(0, sig, n); lN = 4.3 - 0.9 * np.sqrt(y) + z
        shape = np.exp(-0.5 * ((np.arange(NSNAP)[None] - 50) / 18) ** 2); shape = shape / shape.sum(1, keepdims=True)
        lam = 10 ** lN[:, None] * shape; c = rng.poisson(lam)
        return dict(N=np.maximum(c.sum(1), 1), counts=c, mdm=c * 1e9, main=rng.integers(85, 92, n))
    test = np.array(json.load(open(os.path.join(HERE, "cb1_part_a_results.json")))["test0"])
    tr = np.setdiff1d(np.arange(n), test)
    D = make(0.03)
    # truth: invert the planted law exactly, the highest R2 attainable from the count
    inv = ((4.3 - np.log10(D["N"])) / 0.9) ** 2; truth = r2_rmse(y[test], inv[test])[0]
    P(f"K3 planted law: R2 of exact inversion on the test set {truth:.3f}")
    R = evaluate(D, y, test, n_rep=20)
    k3a = abs(R["B0 cubic"]["r2"] - truth) < 0.03
    P("K3 null target (permuted y):")
    R0 = evaluate(D, rng.permutation(y), test, n_rep=20)
    k3b = abs(R0["B0 cubic"]["r2"]) < 0.15 and abs(R0["B1 ridge"]["r2"]) < 0.25
    P(f"K3 recovers planted law within 0.03: {'PASS' if k3a else 'FAIL'}; null near zero: {'PASS' if k3b else 'FAIL'}")
    json.dump(dict(K3_truth=truth, K3=R, K3_null=R0, K4=bool(ok)), open(os.path.join(HERE, "cb1_part_b_synthetic.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cb1_part_b_synthetic.out"), "w").write("\n".join(OUT) + "\n")
    return 0 if ok and k3a and k3b else 1

def grade(path):
    Z = np.load(path); D = {k: Z[k] for k in ("N", "counts", "mdm", "main")}; y = Z["y"]
    if len(y) != 1007: P(f"WARNING: {len(y)} rows, not 1007; split replay differs from the paper's")
    test = np.array(json.load(open(os.path.join(HERE, "cb1_part_a_results.json")))["test0"])
    P("CB1 Part B grades; not a framework test"); R = evaluate(D, y, test)
    PAPER = [("no features 0.509", "B0 cubic", 0.509), ("snapshot only 0.708", "B1 ridge", 0.708), ("flattened ApJ 0.683", "B1 ridge", 0.683), ("best 0.957", "B2 ridge", 0.957)]
    G = {}
    for label, b, v in PAPER:
        lo, _, hi = R[b]["rep"]; G[label] = "COUNT SUFFICES" if hi >= v else "GRAPH ADDS"; P(f"  {label:22s} vs {b}: upper {hi:+.3f}: {G[label]}")
    json.dump(dict(R=R, grades=G), open(os.path.join(HERE, "cb1_part_b_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cb1_part_b.out"), "w").write("\n".join(OUT) + "\n")
    return 0

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "synthetic": sys.exit(synthetic())
    if mode == "grade": sys.exit(grade(sys.argv[2]))
    if mode == "extract":
        S = np.loadtxt(os.path.join(HERE, "authors_code", "WDM_TNG_MW_SB4_parameters.txt")); boxes = [b for b in range(1024) if b not in REMOVED]
        rows = [extract_box(os.path.join(sys.argv[2], f"box_{b}", "tree_extended.hdf5")) for b in boxes]
        np.savez(sys.argv[3], y=S[:, 0], N=np.array([r["N"] for r in rows]), counts=np.array([r["counts"] for r in rows]), mdm=np.array([r["mdm"] for r in rows]), main=np.array([r["main"] for r in rows]))
