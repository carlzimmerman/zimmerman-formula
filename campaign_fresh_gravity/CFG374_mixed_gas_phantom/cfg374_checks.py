#!/usr/bin/env python3
"""CFG374 controls (frozen 396ed0c5a): C1 weights sum to 1, W(0) = 1, HOT1 equals CFG372's 1e6 K filter; MUTATE (CFG374_MUTATE=1):
f_coll = 1 gives W = 1 (the unfiltered T = 0 path) to 1e-6.  Algebraic, on the 256^3 k-grid magnitudes."""
import os, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUTATE = os.environ.get("CFG374_MUTATE", "0") == "1"
SLUG = "cfg374_checks" + ("_MUTATE" if MUTATE else ""); LOG, CH = [], []
def P(s=""): print(s); LOG.append(s)
def check(n, ok, v=""): CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")
Om = (0.02237 + 0.1200) / 0.6736**2
kJ = lambda T, a=1.0: math.sqrt(1.5 * Om * a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
MIXES = {"MIXA": (0.28, 0.54, 0.18), "MIXB": (0.57, 0.25, 0.18), "HOT1": (0.0, 1.0, 0.0), "COLL1": (0.0, 0.0, 1.0)}
k = np.linspace(0, 2 * math.pi / (200 / 256) * math.sqrt(3) / 2, 5000)
W = lambda m, a=1.0: MIXES[m][0] / (1 + (k / kJ(1e4, a))**2) + MIXES[m][1] / (1 + (k / kJ(1e6, a))**2) + MIXES[m][2]
if not MUTATE:
    check("C1a weights sum to 1", all(abs(sum(v) - 1) < 1e-12 for v in MIXES.values()))
    check("C1b W(0) = 1 for MIXA, MIXB", all(abs(W(m)[0] - 1) < 1e-12 for m in ("MIXA", "MIXB")))
    w372 = 1 / (1 + (k / kJ(1e6))**2)
    check("C1c HOT1 reproduces CFG372's 1e6 K filter (max diff)", float(np.max(np.abs(W("HOT1") - w372))) < 1e-12)
    for m in ("MIXA", "MIXB"):
        P(f"  {m}: W at k = 0.3 / 1 / 3 h/Mpc (z = 0) = " + " / ".join(f"{float(np.interp(x, k, W(m))):.3f}" for x in (0.3, 1.0, 3.0)))
else:
    check("MUTATE: f_coll = 1 gives W = 1 everywhere (to 1e-6)", float(np.max(np.abs(W("COLL1") - 1))) < 1e-6)
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
raise SystemExit(0 if all(CH) else 1)
