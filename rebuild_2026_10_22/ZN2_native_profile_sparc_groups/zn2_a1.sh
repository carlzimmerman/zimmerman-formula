#!/bin/bash
# ZN2 A1 read: measure the low-mass z = 0 runs with ZN1's measure(), then the frozen grade with tags 1e10 to 1e14. Run from this directory.
python3 - <<'PY'
import glob, importlib.util, json, math, os, sys
import numpy as np
RB = os.path.dirname(os.getcwd()); ZD = os.path.join(RB, "ZN1_zooms_to_z0"); s = importlib.util.spec_from_file_location("zm", os.path.join(ZD, "zn1_measure.py")); Z = importlib.util.module_from_spec(s); sys.argv = ["x"]; s.loader.exec_module(Z); J = json.load(open(os.path.join(ZD, "zn1_shapes.json")))
for M in ("1e10", "1e11"):
    J[M] = {}; rows = []
    for d in sorted(glob.glob(f"runs/M{M}_s?_ng64")):
        f = os.path.join(d, "snap_z0.00.npz")
        if not os.path.exists(f): continue
        A = np.load(f, allow_pickle=False); me = json.loads(str(A["meta"])); o = Z.measure(A["x"], float(A["m"]), 0.0, me["eps"]); rows.append(dict(lgM=math.log10(o["M200"]), x_edge=o["x_edge"], lnm=o["lnm"], M_over_nom=o["M200"] / me["M"], x_conv=o["x_conv"], R200=o["R200"]))
    assert len(rows) >= 6, M
    J[M]["0.00"] = dict(n=len(rows), lgM=float(np.median([q["lgM"] for q in rows])), x_edge=min(q["x_edge"] for q in rows), lnm=np.median([q["lnm"] for q in rows], axis=0).tolist(), seeds=rows); X = np.array(J["x"]); mu = lambda y: np.log1p(y) - y / (1 + y); from scipy.optimize import minimize_scalar as ms; l = np.array(J[M]["0.00"]["lnm"]); xc = np.median([q["x_conv"] for q in rows]); k = (X >= max(0.05, xc)) & (X <= 1); print(M, "n", len(rows), "lgM", round(J[M]["0.00"]["lgM"], 3), "M200/nom", round(np.median([q["M_over_nom"] for q in rows]), 3), "x_conv", round(xc, 3), "c200", round(ms(lambda c: float(np.sum((np.log(mu(c * X[k]) / mu(c)) - l[k]) ** 2)), bounds=(1, 40), method="bounded").x, 2))
json.dump(J, open("zn2_low_shapes.json", "w"))
PY
export ZN2_SHAPEFILE=$PWD/zn2_low_shapes.json ZN2_TAGS=1e10,1e11,1e12,1e13,1e14 ZN2_OUTTAG=zn2_a1
python3 zn2_grade.py; python3 zn2_grade.py --mutate | tail -1
