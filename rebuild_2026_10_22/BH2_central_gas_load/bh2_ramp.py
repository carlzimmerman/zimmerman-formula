#!/usr/bin/env python3
"""BH2 post-result control, not frozen: reaching cells with CL5's 50 Myr ramp out (BH1's 5 Myr means about 20000 km/s at 1e14). Same-load STATIC is ramp independent.
    python3 bh2_ramp.py run NAME; python3 bh2_ramp.py list; python3 bh2_ramp.py grade"""
import json, os, sys
import numpy as np
import bh2
B = bh2.B; HERE = bh2.HERE; TOK = "up, dn = 5 / tu, 200 / tu"; src = open(B.__file__).read(); assert src.count(TOK) == 1
ns = dict(vars(B)); exec(compile(src.split("def integrate(")[1].join(["def integrate(", ""]).split("def run(name)")[0].replace(TOK, "up, dn = 50 / tu, 200 / tu"), "bh1_ramp50", "exec"), ns); integ = ns["integrate"]
CELLS = ["14_L02_N10", "14_L05_N3", "14_L05_N10", "14_L10_N3", "13_L02_N10", "13_L05_N3", "13_L05_N10", "13_L10_N10"]
if sys.argv[1] == "list": print("\n".join(CELLS))
elif sys.argv[1] == "run":
    name = sys.argv[2]; m, cell = name.split("_", 1); l, N, eps = bh2.GRID[cell]; L = bh2.LOADS[l]; d = bh2.idir(m, l); S = json.load(open(os.path.join(d, "setup.json"))); I = np.load(os.path.join(d, "cm1_ics.npz")); sch = bh2.sched(L, N, eps, S)
    integ(I["pos"].copy(), I["vel"].copy(), float(I["mp"]), S["xc500"], "G1", N, sch, bh2.MST + L, B.FG - L, B.AS, B.AG, B.TOT, os.path.join(HERE, f"bh2_ramp50_run_{name}.json"), dict(name=name))
else:
    res = {}; out = ["BH2 post-result control, not frozen: 50 Myr ramp out; R against same-load STATIC; kappa = 1/2 FITTED; not theory closed"]
    for name in CELLS:
        m, cell = name.split("_", 1); l = bh2.GRID[cell][0]; J = lambda s: json.load(open(os.path.join(HERE, s)))
        st = J(f"bh2_run_{m}_{l}_STATIC.json")["marks"][-1]["eta"]; q = J(f"bh2_ramp50_run_{name}.json"); R = q["marks"][-1]["eta"] / st; R5 = J(f"bh2_run_{name}.json")["marks"][-1]["eta"] / st
        res[name] = dict(R50=R, R5=R5, err=q["maxerr"], done=q["done"]); out.append(f"  {name}: R 50 Myr {R:.3f} vs 5 Myr {R5:.3f}; LIMIT {bh2.LIM[m]}; err {q['maxerr']:.1e}; {'at LIMIT' if R <= bh2.LIM[m] else 'misses'}")
    print("\n".join(out)); open(os.path.join(HERE, "bh2_ramp50.out"), "w").write("\n".join(out) + "\n"); json.dump(res, open(os.path.join(HERE, "bh2_ramp50_results.json"), "w"), indent=1)
