#!/usr/bin/env python3
"""CSD1 S-cos tuning (FROZEN_CRITERIA.md section 2): from the law-off runs at log M_b 10.45 canonical, N 1200, A in
{4, 7, 10} (and any further points present), the A at which FLD1's charge_turned_around_over_Mb at z = 0 equals PD1's
z = 0 share (read from pd1.json), by linear interpolation of log(share) in log A. Prints A* to 3 significant digits.
  python3 -I -B csd1_tune.py -> csd1_tune.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, json, glob, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
pd1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust", "pd1.json")))
target = {f: float(np.median([r["share_over_Mb"] for r in pd1[f]["share_tables"]["z0.0"]])) for f in ("canonical", "alt")}
pts = []
for f in sorted(glob.glob(os.path.join(HERE, "runs", "csd1_canonical_M10.45_N1200_A*_lawoff.json"))):
    d = json.load(open(f)); pts.append((d["A"], d["charge_turned_around_over_Mb"]))
pts.sort()
out = [f"target (PD1 z 0 share): canonical {target['canonical']:.3f}, alt {target['alt']:.3f}"]
for A, s in pts: out.append(f"A {A:g}: turned around {s:.3f} M_b")
A_ = np.log([p[0] for p in pts]); S_ = np.log([p[1] for p in pts])
lt = math.log(target["canonical"])
if len(pts) >= 2 and S_.min() <= lt <= S_.max() and np.all(np.diff(S_) > 0):
    Astar = float(f"{math.exp(np.interp(lt, S_, A_)):.3g}"); out.append(f"A* = {Astar:g} (bracketed)")
else:
    Astar = None; out.append("target not bracketed by a monotone set: more points needed (criteria section 2)")
json.dump(dict(target=target, points=pts, A_star=Astar, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed."),
          open(os.path.join(HERE, "csd1_tune.json"), "w"), indent=1)
out.append("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "csd1_tune.out"), "w").write("\n".join(out) + "\n"); print("\n".join(out))
