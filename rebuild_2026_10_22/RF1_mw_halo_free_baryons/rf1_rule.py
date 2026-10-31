#!/usr/bin/env python3
"""RF1: build the native-N table once from ND1's own RULE_NAT (ND1 commit 73805754b6). Criteria FROZEN_CRITERIA.md.
S_cold in Msun/pc^2 against lg M200, backgrounds A, B. By-products of ND1's loader land here and are removed.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf1_rule.py
kappa = 1/2 FITTED; cold dark energy, never a particle; not theory closed."""
import contextlib, io, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); P = os.path.join(REB, "ND1_native_dwarfs", "nd1_ab.py")
src = open(P).read(); src = src[:src.index("def gh(q, rule")]
LOADER = os.path.join(HERE, "nd1_loader_ro.py")
g = {"__file__": LOADER, "__name__": "nd1_ro"}; sys.argv = [LOADER]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, P, "exec"), g)
g["cleanup"]()
LG = [round(6.0 + 0.02 * i, 2) for i in range(501)]; R = g["RULE_NAT"]; U = g["MSUNE"] / g["PC2"]
T = dict(lg=LG, fc=g["FC"], A=[R(10 ** l, "A_c2b_refit") / U for l in LG], B=[R(10 ** l, "B_cfg886_bg") / U for l in LG])
json.dump(T, open(os.path.join(HERE, "rf1_rule_table.json"), "w"), indent=0)
print("rf1_rule_table.json written; f_c", T["fc"])
