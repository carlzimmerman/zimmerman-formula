#!/usr/bin/env python3
"""
CFG75 -- how the universal-debris-fraction verdict depends on the per-population acceptance level.

Declared AFTER a referee audit (not before any run): CFG59 and CFG71 answer 'is there a phi in [0,1] inside every population's 1 sigma
interval?' -- NO.  A referee recomputed that the same committed scan tables give a common phi at 2 sigma.  This lane reproduces that from
the committed tables only (CFG59_universal_debris_fraction_results.json, CFG71_universal_fraction_dynamical_sluggs_results.json; the 'scan'
entries give, for every population and footing, the offset o(phi) and its error e(phi) on the phi grid).  No new data, no new model.

QUESTION.  For k = 1, 2, 3 sigma: the intersection of {phi : |o(phi)| <= k e(phi)} over (a) CFG59's ten populations, (b) the nine
without the X-ray ellipticals, (c) CFG71's populations (dynamical SLUGGS), (d) CFG71's without SLUGGS.  PASS LINES: (C1 control) the k = 1
intersections reproduce the committed CFG59 / CFG71 answers (empty on both footings); (C2) the per-population 1 sigma intervals of SLUGGS
and the M31 LVD in CFG59 reproduce the committed segments (SLUGGS [0.808, 1], LVD [0, 0.301] canonical, tolerance 0.005).
MUTATE=1: every error e is multiplied by 0.5 -- the 2 sigma intersections must then become EMPTY (the control must fail the 2 sigma claim).
Reading rule: a common phi at k sigma is a statement about acceptance level, not a derivation of a fraction; nothing here says the data
favour the framework, and the sum's failures at 1 sigma stand.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUTATE", "") == "1"
EF = 0.5 if MUT else 1.0
ok = True
def load(n): return json.load(open(os.path.join(HERE, n)))["numbers"]["scan"]
def inter(scan, foot, k, drop=()):
    names = sorted({key.split("|")[0] for key in scan if key.endswith("|" + foot)})
    names = [n for n in names if not any(n.startswith(d) for d in drop)]
    phi = np.array(scan[names[0] + "|" + foot]["phi"]); good = np.ones(len(phi), bool)
    for n in names:
        s = scan[n + "|" + foot]; good &= np.abs(np.array(s["o"])) <= k * EF * np.array(s["e"])
    return (float(phi[good][0]), float(phi[good][-1])) if good.any() else None, len(names)
def seg(scan, name, foot, k=1):
    s = scan[name + "|" + foot]; phi = np.array(s["phi"]); g = np.abs(np.array(s["o"])) <= k * np.array(s["e"])
    return (float(phi[g][0]), float(phi[g][-1])) if g.any() else None
S59 = load("CFG59_universal_debris_fraction_results.json"); S71 = load("CFG71_universal_fraction_dynamical_sluggs_results.json")
print("CFG75 -- universal debris fraction against the acceptance level" + ("   [MUTATE: every error x 0.5]" if MUT else ""))
for label, S, drop in (("CFG59 ten populations", S59, ()), ("CFG59 nine (no X-ray ellipticals)", S59, ("U6",)), ("CFG71 populations (dynamical SLUGGS)", S71, ()),
                       ("CFG71 without SLUGGS", S71, ("U5",))):
    for foot in ("canonical", "alt"):
        row = []
        for k in (1, 2, 3):
            iv, n = inter(S, foot, k, drop); row.append(f"{k}s: " + ("empty" if iv is None else f"[{iv[0]:.2f}, {iv[1]:.2f}]"))
        print(f"  {label:38s} {foot:9s} ({n} pops)  " + "   ".join(row))
one59 = [inter(S59, f, 1)[0] for f in ("canonical", "alt")]; one71 = [inter(S71, f, 1)[0] for f in ("canonical", "alt")]
two59 = [inter(S59, f, 2)[0] for f in ("canonical", "alt")]
c1 = all(v is None for v in one59 + one71); c2 = True
for name, want in (("U5 SLUGGS", (0.808, 1.0)), ("U4 M31 LVD", (0.0, 0.301))):
    got = seg(S59, name, "canonical")
    c2 &= got is not None and abs(got[0] - want[0]) < 0.005 and abs(got[1] - want[1]) < 0.005
    print(f"  1 sigma segment {name} canonical: {got}  committed {want}")
h = all(v is not None for v in two59)
print(f"[{'PASS' if c1 else 'FAIL'}] C1 1-sigma intersections empty on both footings for CFG59 and CFG71 (the committed answer)")
print(f"[{'PASS' if c2 else 'FAIL'}] C2 the 1-sigma segments of SLUGGS and the M31 LVD reproduce the committed ones")
print(f"[{'PASS' if h else 'FAIL'}] H1 (reported acceptance-level statement; MUTATE must fail) CFG59's ten populations share a common phi at 2 sigma on both footings")
ok = c1 and c2 and h
print("checks: " + ("all pass" if ok else "load-bearing failure(s)"))
sys.exit(0 if ok else 1)
