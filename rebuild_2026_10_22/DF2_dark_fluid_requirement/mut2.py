#!/usr/bin/env python3
"""DF2 replacement MUTATE (AMENDMENT_A1). kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, signal
os.environ["DF2_RUNMUT"] = "1"; sys.argv = ["df2.py", "none"]
P_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "df2.py"); src = open(P_).read()
g = {"__name__": "df2ro", "__file__": P_}; exec(compile(src, "df2.py", "exec"), g)
L = g["R"]["Lik"](); SK = g["fixed_cut"]()
a = g["evalp"](L, g["cell"]("m2_base", "K", DF2_CS0=4, DF2_N=1), g["PF"], g["RF1"]["A"], S_K=SK, tag="a")
signal.alarm(1800)
try: b = g["evalp"](L, g["cell"]("m2_mut", "K", DF2_CS0=4, DF2_N=1, DF2_MUT=1), g["PF"], g["RF1"]["A"], S_K=SK, tag="b")
except g["TO"]: b = dict(status="TIMEOUT")
signal.alarm(0)
r = dict(base=a.get("plik"), mut=b.get("plik"), status=b["status"], msg=b.get("msg"), passed=bool(b["status"] != "OK" or abs(b["plik"] - a["plik"]) > 1)); print(json.dumps(r, default=float))
json.dump(r, open(os.path.join(g["HERE"], "cells_MUTATE", "m2_checks.json"), "w"), indent=1, default=float)
