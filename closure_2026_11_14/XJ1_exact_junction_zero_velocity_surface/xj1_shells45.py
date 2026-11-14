#!/usr/bin/env python3
"""XJ1 (AMENDMENT_A6; reported, post hoc; no label): a copy of xj1_shells.py with the passage count carried to 5 (two more
series columns, R_4 and R_5); known answer: the first eight series columns equal this lane's stored run in shells/ to 1e-9
relative. Output shells45/xj1_shells45_<footing>_M<logMb>.json. The first script's docstring follows.
XJ1 (reported, post hoc, hypothesis-generating; no label): inner caustic radii of the clock's shells.
FLD1's fld1_shells.py (fable52_push/FLD1_fold_reach) is executed with three stated text insertions and nothing else changed:
a per-shell count of passages through the centre (reflections), and three extra series columns, the largest current
radius among shells that have passed the centre at least 1, 2 and 3 times (R_1, R_2, R_3). Known answer: the first five
series columns equal FLD1's stored run (same footing, mass, N) to 1e-9 relative.
  python3 -I -B xj1_shells.py <footing> <logMb> -> shells/xj1_shells_<footing>_M<logMb>.json
Limits: behind the fold FLD1's independent-shell equation is not exact and the action gives no answer (COL1); the
reflection at the centre is FLD1's device. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "fable52_push", "FLD1_fold_reach", "fld1_shells.py"); code = open(SRC).read()
def ins(a, b):
    global code
    assert code.count(a) == 1, a
    code = code.replace(a, b)
ins("    crossed = np.zeros(N, bool)\n", "    crossed = np.zeros(N, bool)\n    nhit = np.zeros(N, int)\n")
ins("            rn[hit] = 2 * rw[hit] - rn[hit]; vh[hit] = np.abs(vh[hit])\n", "            rn[hit] = 2 * rw[hit] - rn[hit]; vh[hit] = np.abs(vh[hit]); nhit[hit] += 1\n")
ins("                       float(crossed.mean())])\n", "                       float(crossed.mean())] + [float(r[nhit >= k].max()) if (nhit >= k).any() else 0.0 for k in (1, 2, 3, 4, 5)])\n")
NS = {"__file__": SRC, "__name__": "fld1_shells_xj1"}
exec(compile(code, SRC, "exec"), NS)
ft, lM = sys.argv[1], float(sys.argv[2])
res = NS["run"](ft, lM)
S = np.array(res["series"]); old = np.array(json.load(open(os.path.join(HERE, "shells", f"xj1_shells_{ft}_M{lM:g}.json")))["series"])
dev = float(np.max(np.abs(S[:, :8] - old) / np.maximum(np.abs(old), 1e-30))) if S[:, :8].shape == old.shape else float("inf")
def at(z, c):
    o = np.argsort(S[:, 1]); return float(np.interp(z, S[o, 1], S[o, c]))
rows = {str(z): dict(R_fold=at(z, 2), R_ta=at(z, 3), R_1=at(z, 5), R_2=at(z, 6), R_3=at(z, 7), R_4=at(z, 8), R_5=at(z, 9)) for z in (0.0, 0.3, 1.0, 2.2, 2.6, 3.0, 3.4, 3.8, 4.4)}
out = dict(lane="XJ1", part="inner caustic radii to the fifth (AMENDMENT_A6; reported)", footing=ft, logMb=lM, known_answer_max_rel=dev, known_answer_ok=bool(dev <= 1e-9),
           series_cols=res["series_cols"] + ["R_1_kpc", "R_2_kpc", "R_3_kpc", "R_4_kpc", "R_5_kpc"], at_z=rows, series=res["series"], note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
os.makedirs(os.path.join(HERE, "shells45"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "shells45", f"xj1_shells45_{ft}_M{lM:g}.json"), "w"))
print(f"[{ft}] log M_b {lM:g}: known answer (this lane's stored shell run, eight columns) max rel {dev:.1e} -> {'PASS' if dev <= 1e-9 else 'FAIL'}")
for z, r_ in rows.items():
    f = r_["R_fold"]
    print(f"[{ft}] log M_b {lM:g} z {z}: R_fold {f:.1f} kpc; R_1 to R_5 over R_fold: " + " / ".join(f"{(r_[k] / f if f > 0 else float('nan')):.3f}" for k in ("R_1", "R_2", "R_3", "R_4", "R_5")) + f"; R_ta / R_fold {r_['R_ta'] / f if f > 0 else float('nan'):.3f}")
