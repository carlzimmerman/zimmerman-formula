#!/usr/bin/env python3
"""CB1 Part A: replay the public code's seeded split on the authors' parameter file. No simulation data; no GNN.

Frozen criteria: FROZEN_CRITERIA.md (53735de87f). Authors' code at commit 6d01c315d1 of ilemleisher/merger_tree_gnn.

    python3 cb1_part_a.py            -> cb1_part_a.out, cb1_part_a_results.json
    python3 cb1_part_a.py --mutate   -> permuted and wrong-unit targets; separate outputs; exit 1 if the wrong-unit test does not bite
"""
import json, os, random, sys
import numpy as np

MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); TAG = "_MUTATE" if MUTATE else ""; OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

def split_dataset(dataset, train_size, valid_size, test_size):      # verbatim logic, gnn_script.py lines 34-45
    random.seed(5)
    random.shuffle(dataset)
    ndata = len(dataset)
    split_valid = int(np.floor(valid_size * ndata))
    split_test = split_valid + int(np.floor(test_size * ndata))
    valid_dataset = dataset[:split_valid]
    test_dataset = dataset[split_valid:split_test]
    train_dataset = dataset[split_test:]
    return train_dataset, valid_dataset, test_dataset

S = np.loadtxt(os.path.join(HERE, "authors_code", "WDM_TNG_MW_SB4_parameters.txt"))
Y = S[:, 0].copy(); M = 1 / Y; N = len(Y)
P(f"CB1 Part A  {'MUTATE' if MUTATE else 'normal run'}  frozen 53735de87f; authors' commit 6d01c315d1. Not a framework test.")
P(f"K1 rows {N}; 1/M [{Y.min():.5f}, {Y.max():.5f}] keV^-1; M [{M.min():.2f}, {M.max():.2f}] keV; authors' norm bounds [{1/30:.5f}, {1/1.8:.5f}]")
K1 = N == 1007 and Y.min() >= 1 / 30 - 2e-3 and Y.max() <= 1 / 1.8 + 2e-3

def calls(y, n_calls=51, inplace=True):
    ds = list(range(len(y))); out = []
    for _ in range(n_calls):
        tr, va, te = split_dataset(ds if inplace else list(range(len(y))), 0.8, 0.1, 0.1)
        out.append(dict(train=list(tr), valid=list(va), test=list(te)))
    return out
def overlap(a, b): return len(set(a) & set(b))
def status(c): return "SPLIT CHANGES" if any(set(x["test"]) != set(c[0]["test"]) for x in c[1:]) else "SPLIT FIXED"

RES = dict(frozen="53735de87f", authors_commit="6d01c315d1", n=N)
def run(y, label):
    C = calls(y); Ctrl = calls(y, inplace=False)
    sz = (len(C[0]["train"]), len(C[0]["valid"]), len(C[0]["test"]))
    ov = [overlap(C[0]["test"], x["test"]) for x in C[1:]]
    ovt = [overlap(C[0]["test"], x["train"]) for x in C[1:]]
    st, stc = status(C), status(Ctrl)
    P(f"\n[{label}] A1: sizes train/valid/test {sz}. In place (public code): {st}. Copy each call (paper's stated behaviour): {stc}")
    P(f"  Overlap of call 0's test set with later test sets: median {np.median(ov):.0f} of {sz[2]}, range {min(ov)}-{max(ov)}; with later TRAIN sets: median {np.median(ovt):.0f}, range {min(ovt)}-{max(ovt)}")
    V = np.array([np.var(y[x["test"]]) for x in C])
    hi6 = np.array([(1 / y[x["test"]] > 6.0).sum() for x in C]); hi97 = np.array([(1 / y[x["test"]] > 9.7).sum() for x in C])
    R2fix = 1 - 0.031 ** 2 / V
    P(f"  A2: var(y_test) min {V.min():.5f} median {np.median(V):.5f} max {V.max():.5f}; full sample {np.var(y):.5f}; call 0 {V[0]:.5f}")
    P(f"  A2: R2 implied by fixed RMSE 0.031: min {R2fix.min():.4f} median {np.median(R2fix):.4f} max {R2fix.max():.4f}; call 0 {R2fix[0]:.4f}. Test sims > 6 keV: {hi6.min()}-{hi6.max()} (call 0 {hi6[0]}); > 9.7 keV: {hi97.min()}-{hi97.max()} (call 0 {hi97[0]})")
    PAIRS = [("snapshot only", 0.708, 0.082), ("no features", 0.509, 0.107), ("best", 0.957, 0.031), ("main branch", 0.073, 0.147), ("flattened", 0.873, 0.054), ("pruned", 0.454, 0.117)]
    A3 = {}; inrange = []
    for name, r2, rm in PAIRS:
        lo = (rm - 5e-4) ** 2 / (1 - (r2 - 5e-4)); hi = (rm + 5e-4) ** 2 / (1 - (r2 + 5e-4))
        admit = [i for i, v in enumerate(V) if lo <= v <= hi]
        A3[name] = dict(var_lo=lo, var_hi=hi, n_calls_admit=len(admit), call0=bool(lo <= V[0] <= hi), full=bool(lo <= np.var(y) <= hi), calls=admit)
        inrange.append(lo <= V.max() and hi >= V.min())
        P(f"  A3: {name:14s} R2 {r2:.3f} RMSE {rm:.3f}: implied var [{lo:.5f}, {hi:.5f}]; admitted by {len(admit)}/51 calls; call 0 {A3[name]['call0']}; full-sample var {A3[name]['full']}")
    both = set(range(51))
    for v in A3.values(): both &= set(v["calls"])
    # AMENDMENT 1 (README, after the first run): the published ApJ text's pairs, which the frozen arXiv list missed; and a chance level.
    PUB = [("snapshot only", 0.708, 0.082), ("no features", 0.509, 0.107), ("best", 0.957, 0.031), ("main branch", 0.073, 0.147), ("flattened ApJ", 0.683, 0.086), ("pruned caption", 0.477, 0.110), ("pruned text", 0.454, 0.117)]
    rv = np.random.default_rng(20261030); vs = np.array([np.var(y[rv.choice(len(y), 100, replace=False)]) for _ in range(200000)])
    iv = {n: ((rm - 5e-4) ** 2 / (1 - (r2 - 5e-4)), (rm + 5e-4) ** 2 / (1 - (r2 + 5e-4))) for n, r2, rm in PUB}
    pc = {n: float(np.mean((vs >= l) & (vs <= h))) for n, (l, h) in iv.items()}
    for n, (l, h) in iv.items():
        P(f"  A3-ApJ: {n:15s} implied var [{l:.5f}, {h:.5f}]; calls {[i for i, v in enumerate(V) if l <= v <= h]}; call 0 {bool(l <= V[0] <= h)}; chance for a random 100-set {pc[n]:.3f}")
    core = [n for n in iv if n != "pruned text"]
    lo = max(iv[n][0] for n in core); hi = min(iv[n][1] for n in core); ind = float(np.prod([pc[n] for n in core]))
    P(f"  A3-ApJ: six pairs (all but 'pruned text') share var [{lo:.5f}, {hi:.5f}]; calls inside {[i for i, v in enumerate(V) if lo <= v <= hi]}; P(six independent splits each fit their own pair) {ind:.1e}")
    uc = all(inrange)
    P(f"  A3: {'UNITS CONFIRMED' if uc else 'UNITS NOT CONFIRMED'}. Calls admitting every pair at once: {sorted(both)}")
    fr = {t: float((1 / y > t).mean()) for t in (6.0, 9.7)}
    P(f"  A4: share of sims above 6.0 keV {fr[6.0]:.3f}, above 9.7 keV {fr[9.7]:.3f}")
    cond = {}
    for t in (6.0, 9.7):
        tst = y[C[0]["test"]]; sel = tst[1 / tst > t]; vs = np.var(sel); va = np.var(y[1 / y > t])
        cond[str(t)] = dict(n_test=int(len(sel)), R2_test=float(1 - 0.031 ** 2 / vs), R2_sample=float(1 - 0.031 ** 2 / va))
        P(f"  A4 ASSUMPTION (constant RMSE 0.031): above {t} keV: test-set n {len(sel)}, R2 {cond[str(t)]['R2_test']:+.2f}; sample R2 {cond[str(t)]['R2_sample']:+.2f}")
    return dict(sizes=sz, status=st, control=stc, overlap_test=ov, overlap_train=ovt, var=V.tolist(), R2fix=R2fix.tolist(), hi6=hi6.tolist(), hi97=hi97.tolist(), A3=A3, units=uc, all_pairs_calls=sorted(both), frac=fr, cond=cond, test0=C[0]["test"], train0=C[0]["train"], valid0=C[0]["valid"])

if not MUTATE:
    r = run(Y, "1/M, keV^-1"); RES.update(r)
    K2 = r["sizes"] == (807, 100, 100)
    P(f"\nChecks: K1 {'PASS' if K1 else 'FAIL'}; K2 sizes {r['sizes']} {'PASS' if K2 else 'FAIL (see sizes; K2 reads what the code gives)'}; control {r['control']}")
    P("\nA5 code facts (commit 6d01c315d1):")
    P("  graph_script.py:131 u = np.log10(ngal), built for every graph in create_dataset")
    P("  gnn_script.py:122 NodeModel: torch.cat([x, out1, out2, out3, u[batch]]) in every message-passing layer")
    P("  gnn_script.py:188 forward: torch.cat([addpool,meanpool,maxpool,u]) immediately before outlayer")
    P("  gnn_script.py:365 objective returns test_loss, which Optuna minimizes; gnn_script.py:429 best_idx is the lowest of those")
    P("  gnn_script.py:34-35 + 347 + 377 split_dataset reseeds and shuffles the same list in place on each call")
    P("  Paper: 'we do not input any global features' (2.2.2); 'minimize the validation loss', 'identical dataset division' (2.2.5)")
    code = 0 if K1 else 1
else:
    rng = np.random.default_rng(20261030)
    a = run(rng.permutation(Y), "MUTATE permuted 1/M"); b = run(M, "MUTATE wrong unit, M in keV")
    bite = not b["units"]
    P(f"\nPermuted target UNITS {a['units']} (a variance statistic is blind to row order, so this frozen mutation cannot bite; disclosed). Wrong-unit target UNITS {b['units']}: bite {bite}")
    RES["bite"] = bite; code = 0 if bite else 1
json.dump(RES, open(os.path.join(HERE, f"cb1_part_a_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cb1_part_a{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(code)
