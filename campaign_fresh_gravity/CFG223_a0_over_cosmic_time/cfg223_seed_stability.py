#!/usr/bin/env python3
"""CFG223 POST HOC robustness check (written after an independent brentq recomputation showed the 68% bootstrap edges move between seeds; reported only, not frozen).
The bootstrap distribution of a median at n = 6 to 27 is discrete, so the 16th / 84th percentile edges can jump by one atom when the seed changes.  Here: the same estimator and B = 10,000
with ten other seeds; the spread of each edge across seeds next to the committed (seed 223) value.  LambdaCDM has no a0; author decompositions; not a detection; kappa = 1/2 FITTED."""
import os, sys, io, contextlib
sys.dont_write_bytecode = True
import numpy as np
LANE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(LANE, "cfg223_a0_over_time.py")).read()
stop = src.index('P("\\nCONTROLS")')
ns = {"__file__": os.path.join(LANE, "cfg223_a0_over_time.py"), "__name__": "cfg223_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:stop], "cfg223_a0_over_time.py", "exec"), ns)
build_points, implied, NU, A0L = ns["build_points"], ns["implied"], ns["NU"], ns["A0L"]
import json
J = json.load(open(os.path.join(LANE, "cfg223_results.json")))["points"]
PTS, _, _ = build_points(mut=False)
OUT = []


def P(s=""):
    print(s); OUT.append(s)


P(__doc__.strip())
LAWS = ["FLAT", "PROXY", "H(z)", "M-DEC"]
P("\n  point            n   68% lower edge: committed | range over 10 seeds        68% upper edge: committed | range          95% lower: committed | range        95% upper: committed | range")
inside = {}
for p, r in zip(PTS[:8], J[:8]):
    n = p["z"].size; q = []
    for seed in range(1, 11):
        I = np.random.default_rng(seed * 7919 + n).integers(0, n, size=(10000, n))
        lb, _ = implied(p["D"][I], p["gb"][I], NU, A0L)
        q.append(np.percentile(10 ** lb, [2.5, 16, 84, 97.5]))
    q = np.array(q)
    P(f"  {p['short']:13s} {n:3d}   {r['lo68']:.3f} | {q[:, 1].min():.3f} to {q[:, 1].max():.3f}            {r['hi68']:.3f} | {q[:, 2].min():.3f} to {q[:, 2].max():.3f}            {r['lo95']:.3f} | {q[:, 0].min():.3f} to {q[:, 0].max():.3f}          {r['hi95']:.3f} | {q[:, 3].min():.3f} to {q[:, 3].max():.3f}")
    for L in LAWS:
        e = r["expected"][L]["s"]
        k = int(r["lo95"] <= e <= r["hi95"]) + sum(int(a <= e <= b) for a, b in zip(q[:, 0], q[:, 3]))
        inside[(p["short"], L)] = k
P("\n  Is the caption rule's 95% flag (the law's expected ratio inside the 95% interval) the same in all 11 draws (committed seed + ten others)?  count inside / 11; a count other than 0 or 11 is seed-sensitive:")
P("  " + f"{'point':14s} " + " ".join(f"{L:>7s}" for L in LAWS))
unstable = []
for p in PTS[:8]:
    row = [inside[(p["short"], L)] for L in LAWS]
    P("  " + f"{p['short']:14s} " + " ".join(f"{k:7d}" for k in row))
    unstable += [(p["short"], L, k) for L, k in zip(LAWS, row) if k not in (0, 11)]
P("\n  Seed-sensitive flags: " + ("; ".join(f"{a} / {b}: inside in {k} of 11 draws" for a, b, k in unstable) if unstable else "none"))
open(os.path.join(LANE, "cfg223_seed_stability.out"), "w").write("\n".join(OUT) + "\n")
