#!/usr/bin/env python3
"""WG6 run matrix (FROZEN_CRITERIA.md 1a7c1cdde9): 8 single-thread runs, at most 5 at a time, each writing runs/<tag>.json.
Runs already on disk are skipped. kappa = 1/2 FITTED; not theory closed."""
import os, sys, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, "runs")
M = []
for mu in ("0.01", "0.03", "0.1"):
    for As in ("1e-09", "4e-09"):
        M.append(("R1Y" + mu, "DE", "B2D", As, "128", "200", "50", "canonical"))
M += [("R1Y0.03", "DE", "B2D", "2.1e-09", "128", "200", "50", "canonical"),
      ("R1Y0.03", "DE", "B2D", "2.1e-09", "192", "200", "50", "canonical")]
def tag(m):
    rule, a0r, bg, As, N, ns, zon, foot = m
    return f"{rule}_{a0r}_{bg}_As{float(As):g}_N{N}_s{ns}_zon{float(zon):g}_{foot}"
os.makedirs(RUNS, exist_ok=True)
todo = [m for m in M if not os.path.exists(os.path.join(RUNS, tag(m) + ".json"))]
todo.sort(key=lambda m: -int(m[4]))
live = []
while todo or live:
    while todo and len(live) < 5:
        m = todo.pop(0); lg = open(os.path.join(RUNS, tag(m) + ".log"), "w")
        live.append((m, subprocess.Popen([sys.executable, os.path.join(HERE, "wg6_pm.py"), "run", *m], stdout=lg, stderr=subprocess.STDOUT, cwd=HERE)))
        print(f"start {tag(m)}", flush=True)
    for x in list(live):
        if x[1].poll() is not None:
            print(f"done  {tag(x[0])} exit {x[1].returncode}", flush=True); live.remove(x)
    time.sleep(5)
print("ALL RUNS FINISHED", flush=True)
