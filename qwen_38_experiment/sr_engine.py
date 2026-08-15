#!/usr/bin/env python3
"""sr_engine.py -- the AI-Feynman-style symbolic-regression engine (kit-local, no deps
beyond numpy).  Recovers FUNCTIONAL FORMS from data with verification built in:
train/holdout split + a shuffled-target null (the FDR analog for regression).

  python sr_engine.py --data data/rar_sparc_a0units.json --target y --features x \
      --gens 60 --pop 400 --seed 0 [--nulls 3] [--baseline a0line]

The LLM session's whole job: run this, read the 4-line summary, ledger the verdict.
A discovery claim requires BOTH: holdout RMSE competitive with (or better than) the
named baseline AND train R^2 far outside the shuffled-null distribution.  Deterministic
per --seed.  Results: sr_results/*.jsonl + auto REGISTRY_FDR row.
"""
import argparse, json, math, os, random, sys

import numpy as np

OPS2 = ["add", "sub", "mul", "div"]
OPS1 = ["sqrt", "sq"]
CONSTS = [0.5, 1.0, 2.0, 3.0, math.pi]


def ev(t, X):
    k = t[0]
    if k == "x":
        return X[t[1]]
    if k == "c":
        return np.full_like(X[0], t[1])
    if k in OPS1:
        a = ev(t[1], X)
        return np.sqrt(np.abs(a)) if k == "sqrt" else a * a
    a, b = ev(t[1], X), ev(t[2], X)
    if k == "add":
        return a + b
    if k == "sub":
        return a - b
    if k == "mul":
        return a * b
    d = np.where(np.abs(b) < 1e-9, np.sign(b) * 1e-9 + (b == 0) * 1e-9, b)
    return a / d


def size(t):
    return 1 if t[0] in ("x", "c") else (1 + size(t[1]) + (size(t[2]) if len(t) > 2 else 0))


def show(t):
    k = t[0]
    if k == "x":
        return f"x{t[1]}"
    if k == "c":
        return f"{t[1]:.6g}"
    if k in OPS1:
        return f"{k}({show(t[1])})"
    s = {"add": "+", "sub": "-", "mul": "*", "div": "/"}[k]
    return f"({show(t[1])}{s}{show(t[2])})"


def rand_tree(rng, nfeat, depth):
    if depth <= 0 or rng.random() < 0.3:
        return ("x", rng.randrange(nfeat)) if rng.random() < 0.6 else ("c", rng.choice(CONSTS))
    if rng.random() < 0.25:
        return (rng.choice(OPS1), rand_tree(rng, nfeat, depth - 1))
    return (rng.choice(OPS2), rand_tree(rng, nfeat, depth - 1), rand_tree(rng, nfeat, depth - 1))


def nodes(t, path=()):
    yield path, t
    if t[0] in OPS1:
        yield from nodes(t[1], path + (1,))
    elif t[0] in OPS2:
        yield from nodes(t[1], path + (1,))
        yield from nodes(t[2], path + (2,))


def replace(t, path, sub):
    if not path:
        return sub
    lst = list(t)
    lst[path[0]] = replace(t[path[0]], path[1:], sub)
    return tuple(lst)


def mutate(rng, t, nfeat):
    ns = list(nodes(t))
    path, node = ns[rng.randrange(len(ns))]
    if node[0] == "c" and rng.random() < 0.5:
        return replace(t, path, ("c", node[1] * rng.uniform(0.5, 2.0)))
    return replace(t, path, rand_tree(rng, nfeat, 2))


def crossover(rng, a, b):
    pa, _ = list(nodes(a))[rng.randrange(size(a))]
    _, nb = list(nodes(b))[rng.randrange(size(b))]
    return replace(a, pa, nb)


def rmse(t, X, y):
    with np.errstate(all="ignore"):
        p = ev(t, X)
    if not np.all(np.isfinite(p)):
        return np.inf
    return float(np.sqrt(np.mean((p - y) ** 2)))


def gp_run(X, y, gens, pop, seed, parsimony=0.002):
    rng = random.Random(seed)
    nfeat = len(X)
    P = [rand_tree(rng, nfeat, 3) for _ in range(pop)]
    best = None
    for g in range(gens):
        scored = sorted((rmse(t, X, y) + parsimony * size(t), i) for i, t in enumerate(P))
        if best is None or scored[0][0] < best[0]:
            best = (scored[0][0], P[scored[0][1]])
        elite = [P[i] for _, i in scored[: max(4, pop // 20)]]
        nxt = list(elite)
        while len(nxt) < pop:
            a = P[min(rng.sample(range(pop), 3), key=lambda i: rmse(P[i], X, y))]
            if rng.random() < 0.6:
                b = P[min(rng.sample(range(pop), 3), key=lambda i: rmse(P[i], X, y))]
                c = crossover(rng, a, b)
            else:
                c = mutate(rng, a, nfeat)
            if size(c) <= 25:
                nxt.append(c)
        P = nxt
    return best[1]


BASELINES = {
    "a0line": lambda X: np.sqrt(X[0] ** 2 + X[0]),
    "ms08": lambda X: X[0] / (1.0 - np.exp(-np.sqrt(np.maximum(
        _y_of_x_arr(X[0]), 1e-12)))),
    "newton": lambda X: X[0],
    "btfr": lambda X: X[0] ** 0.25,
}


def _y_of_x_arr(x):
    y = np.array(x, dtype=float)
    for _ in range(80):
        y = x * (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-12))))
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--features", required=True, help="comma-separated column names")
    ap.add_argument("--gens", type=int, default=60)
    ap.add_argument("--pop", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--nulls", type=int, default=3)
    ap.add_argument("--baseline", default=None, choices=[None, *BASELINES])
    ap.add_argument("--holdout", type=float, default=0.3)
    a = ap.parse_args()

    d = json.load(open(a.data))
    cols = d["columns"]
    arr = np.array(d["rows"], dtype=float)
    feats = a.features.split(",")
    X_all = [arr[:, cols.index(f)] for f in feats]
    y_all = arr[:, cols.index(a.target)]
    rng = np.random.RandomState(a.seed)
    idx = rng.permutation(len(y_all))
    ntr = int(len(idx) * (1 - a.holdout))
    tr, ho = idx[:ntr], idx[ntr:]
    Xtr = [x[tr] for x in X_all]
    Xho = [x[ho] for x in X_all]

    best = gp_run(Xtr, y_all[tr], a.gens, a.pop, a.seed)
    r_tr = rmse(best, Xtr, y_all[tr])
    r_ho = rmse(best, Xho, y_all[ho])
    var = float(np.var(y_all[ho]))
    r2_ho = 1.0 - r_ho**2 / var if var > 0 else float("nan")

    null_r2 = []
    for k in range(a.nulls):
        ys = y_all[tr].copy()
        np.random.RandomState(1000 + k).shuffle(ys)
        bn = gp_run(Xtr, ys, a.gens, a.pop, a.seed + 100 + k)
        rn = rmse(bn, Xho, y_all[ho])
        null_r2.append(1.0 - rn**2 / var if var > 0 else float("nan"))

    base = None
    if a.baseline:
        with np.errstate(all="ignore"):
            bp = BASELINES[a.baseline](Xho)
        base = float(np.sqrt(np.mean((bp - y_all[ho]) ** 2)))

    row = dict(data=os.path.basename(a.data), target=a.target, features=feats,
               gens=a.gens, pop=a.pop, seed=a.seed, expression=show(best),
               complexity=size(best), rmse_train=round(r_tr, 6), rmse_holdout=round(r_ho, 6),
               r2_holdout=round(r2_ho, 6), null_r2_holdout=[round(v, 4) for v in null_r2],
               baseline=a.baseline, baseline_rmse_holdout=(round(base, 6) if base else None),
               verdict_suggestion=("CANDIDATE-ESCALATE" if base and r_ho < 0.98 * base
                                   else ("STRUCTURE-FOUND" if null_r2 and
                                         r2_ho > max(null_r2) + 0.2 else "NULL")))
    os.makedirs("sr_results", exist_ok=True)
    out = f"sr_results/{os.path.basename(a.data).split('.')[0]}_{a.target}_s{a.seed}.jsonl"
    with open(out, "a") as f:
        f.write(json.dumps(row) + "\n")
    with open("REGISTRY_FDR.md", "a") as f:
        f.write(f"| sr:{row['data']}/{a.target}/s{a.seed} | auto | GP pop{a.pop}xgen{a.gens}"
                f" | 1 run | {a.nulls} shuffled-target nulls | yes (engine) |\n")
    print(f"[sr] best: {row['expression']}  (complexity {row['complexity']})")
    print(f"[sr] holdout RMSE {r_ho:.5f}  R^2 {r2_ho:.4f}   shuffled-null R^2 {null_r2}")
    print(f"[sr] baseline {a.baseline}: RMSE {base}" if base else "[sr] no baseline")
    print(f"[sr] suggestion: {row['verdict_suggestion']}  ({out})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
