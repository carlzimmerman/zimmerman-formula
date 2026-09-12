#!/usr/bin/env python3
"""Global search over coefficient histories for a self-critical dust sector. Resumable, checkpointing, no network.
Usage:  python3 hermes_push/search/run_search.py [--iters 400] [--seed 1] [--out hermes_push/search/best.json]
Read SEARCH.md first. Report the per-gate breakdown, never just the loss; a loss that stalls above zero is a RESULT, not a failure to
report. Do not edit thresholds in objective.py to make a candidate pass."""
import argparse, json, os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.optimize import differential_evolution
from objective import gates, describe, BOUNDS, PARAM_NAMES
ap = argparse.ArgumentParser(); ap.add_argument("--iters", type=int, default=400); ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--popsize", type=int, default=24); ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "best.json"))
A = ap.parse_args()
best = {"loss": float("inf")}
def f(th):
    global best
    L, g = gates(th)
    if L < best["loss"]:
        best = {"loss": float(L), "theta": [float(x) for x in th], "gates": {k: float(v) for k, v in g.items()}}
        json.dump(best, open(A.out, "w"), indent=1)
    return L
r = differential_evolution(f, BOUNDS, maxiter=A.iters, popsize=A.popsize, seed=A.seed, tol=1e-12, polish=True, init="sobol")
L, g = gates(r.x)
print(f"loss = {L:.6g}   (best seen {best['loss']:.6g})")
print("  per-gate violation: " + "  ".join(f"{k} {v:.4g}" for k, v in g.items()))
print("  theta: " + ", ".join(f"{n}={v:.4g}" for n, v in zip(PARAM_NAMES, r.x)))
print("  " + describe(r.x))
print("  VERDICT: " + ("a history meeting every gate exactly was found -- escalate it: recompute the gates from the full background ODE, "
                       "check the forest tracking precision, and write the H-entry" if L < 1e-9 else
                       f"no history met every gate; the residual sits at {L:.3g}, dominated by " + max(g, key=g.get) +
                       ". That is a result: report which gate resists and by how much, then morph the parameterisation (add a term to history(), do NOT move a threshold)."))
json.dump({"final_loss": float(L), "gates": {k: float(v) for k, v in g.items()}, "theta": [float(x) for x in r.x], "best_seen": best}, open(A.out, "w"), indent=1)
print(f"  written to {A.out}")
