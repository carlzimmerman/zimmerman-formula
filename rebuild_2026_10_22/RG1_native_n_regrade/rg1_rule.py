#!/usr/bin/env python3
"""RG1: build the one native-N table from ND1's own RULE_NAT. S_cold (Msun/pc^2) against lg M200, backgrounds A, B. Criteria FROZEN_CRITERIA.md."""
import contextlib, io, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); P = os.path.join(REB, "ND1_native_dwarfs", "nd1_ab.py")
src = open(P).read(); src = src[:src.index("def gh(q, rule")]
g = {"__file__": P, "__name__": "nd1_ro"}; sys.argv = [P]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, P, "exec"), g)
import numpy as np
LG = [round(6.0 + 0.02 * i, 2) for i in range(501)]; R = g["RULE_NAT"]; U = g["MSUNE"] / g["PC2"]
T = dict(lg=LG, fc=g["FC"], A=[R(10 ** l, "A_c2b_refit") / U for l in LG], B=[R(10 ** l, "B_cfg886_bg") / U for l in LG])
json.dump(T, open(os.path.join(HERE, "rg1_rule_table.json"), "w"))
f = lambda mt, k="A": 10 ** float(np.interp(math.log10(mt * g["FC"]), LG, np.log10(T[k])))
ref = {1e10: 51.8, 1e11: 78.4, 1e12: 149, 1e13: 236, 1e14: 380}
dev = {str(k): f(k) / v - 1 for k, v in ref.items()}; s9 = 10 ** float(np.interp(9.0, LG, np.log10(T["A"])))
print("K0 rule S at M_t:", {k: round(f(float(k)), 1) for k in dev}, "dev", {k: round(v, 4) for k, v in dev.items()}, "S(lg M200 9)", round(s9, 1))
ok = max(abs(v) for v in dev.values()) < 0.01 and abs(s9 / 29.4 - 1) < 0.01; print("K0", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
