#!/usr/bin/env python3
"""CFG399: is the retention step keyed to virial temperature? Out-of-sample on super spirals (FROZEN_CRITERIA.md). Run: python3 cfg399_step_key.py [--mutate]"""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s); OUT.append(str(s))
d = json.load(open(os.path.join(LANES, "CFG390_council_promoted", "session02_calcs", "super_spirals_retention_results.json")))
lo_, hi_, Tm = 0.13, 0.60, math.sqrt(0.5e6 * 2.3e6)
w = (math.log10(2.3e6) - math.log10(0.5e6)) / (2 * math.log(9))     # 10-90% of a logistic spans 2 ln 9 scale units
def pred(T): return lo_ + (hi_ - lo_) / (1 + math.exp(-(math.log10(T) - math.log10(Tm)) / w))
k1 = abs(pred(3e5) - 0.13) < 0.01 and abs(pred(1e7) - 0.60) < 0.01
P(f"K1 logistic: f(3e5 K) = {pred(3e5):.3f}, f(1e7 K) = {pred(1e7):.3f} -> {'PASS' if k1 else 'FAIL'}")
res = {}
for foot in ("canonical", "alt"):
    rows = d[foot]["rows"]
    for lab, rs in (("T>2.3e6", [r for r in rows if r["T"] > 2.3e6]), ("nine fastest", sorted(rows, key=lambda r: -r["v"])[:9])):
        fm = np.array([pred(r["T"]) if MUT else r["f"] for r in rs]); fp = np.array([pred(r["T"]) for r in rs])
        diff = float(np.median(fp) - np.median(fm))
        rng = np.random.default_rng(51); bs = []
        for _ in range(2000):
            i = rng.integers(0, len(rs), len(rs)); bs.append(np.median(fp[i]) - np.median(fm[i]))
        sd = float(np.std(bs)) or 1e-9
        v = "FAILS" if diff / sd > 3 else "SURVIVES" if abs(diff) < 2 * sd else "INCONCLUSIVE"
        res[f"{foot}|{lab}"] = dict(n=len(rs), median_measured=float(np.median(fm)), median_predicted=float(np.median(fp)), diff=diff, sd=sd, verdict=v)
        P(f"{foot:9s} {lab:12s} N {len(rs):2d}: measured median f {np.median(fm):.3f}, predicted {np.median(fp):.3f}, diff {diff:+.3f} +- {sd:.3f} -> TEMPERATURE-KEYED STEP {v}")
json.dump(dict(res=res, K1=k1), open(os.path.join(HERE, f"cfg399_step_key{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg399_step_key{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    ok = res["canonical|T>2.3e6"]["verdict"] == "SURVIVES"; P(f"MUTATE -> {'detected (exit 1)' if ok else 'NOT detected'}"); sys.exit(1 if ok else 0)
sys.exit(0 if k1 else 1)
