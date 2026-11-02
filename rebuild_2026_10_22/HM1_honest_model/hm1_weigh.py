#!/usr/bin/env python3
"""HM1 direct weighing: SP3's weigh path, UR3's method, read only: native EM1 rows only, outputs here. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); F = os.path.join(RB, "SP3_starting_point", "sp3_weigh.py"); T = open(F).read(); T = T[:T.index('R = {}; P("SP3 weighing')]; ns = {"__file__": F, "__name__": "x"}; exec(compile(T, "sp3w", "exec"), ns); ns["U"].T = ns["NR2T"]; R = {}; J = json.load(open(os.path.join(RB, "SP3_starting_point", "sp3_weigh.json")))
for mp in ("tot", "fc1"):
    for mo in ("off", "fq"):
        a = ns["weigh"](line="EM1", shape="native", map=mp, mode=mo); k = f"native-{mp}|EM1|{mo}"; R[k] = a; print(k, a["r"], a["n"], a["cls"], a["n_all"], "SP3 |d r|", abs(a["r"] - J[k]["r"]), flush=True)
json.dump(R, open(os.path.join(HERE, "hm1_weigh.json"), "w"), indent=1, default=float)
