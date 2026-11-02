#!/usr/bin/env python3
"""GM1 grader job (FROZEN_CRITERIA.md): LM1's driver, read only, with GS4's per-cluster pointed gas on matched lensing clusters. Own cache; resumes. kappa = 1/2 FITTED; not theory closed."""
import csv, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); names = [str(x).strip() for x in X["name"]]
R = {}
for r in csv.DictReader(open(os.path.join(RB, "GS4_pointed_gas_offset", "gs4_matched.csv"))):
    if r["erass"] in names: R.setdefault(r["erass"], []).append(r)
D = {k: dict(d=float(np.median([float(q["d"]) for q in v])), dlgR=float(np.median([float(q["dlgR"]) for q in v])), n=len(v), cats=[q["cat"] for q in v]) for k, v in R.items()}
json.dump(D, open(os.path.join(HERE, "gm1_pointed.json"), "w"), indent=0)
fac = {n: (10 ** (D[n]["d"] - 0.005) if n in D else 1.0) for n in names}; FP = os.path.join(HERE, "gm1_factor_gs4.json"); json.dump(fac, open(FP, "w"), indent=0); print("pointed clusters in lens", len(D), flush=True)
src = open(os.path.join(RB, "LM1_law_missing_mass_map", "lm1_grade.py")).read()
for a, b in (('HERE = os.path.dirname(os.path.abspath(__file__)); RB', f'HERE = {HERE!r}; RB'), ('RUNS = {"BASE_f034"', f'RUNS = {{"GS4_f034": ("0.034", 1.0, {FP!r})}}; _o = {{"BASE_f034"'), ('    capfile()\n', '')):
    assert src.count(a) >= 1, a; src = src.replace(a, b, 1)
exec(compile(src, "lm1_grade_driven", "exec"), dict(__name__="__main__", __file__=os.path.join(HERE, "x.py")))
