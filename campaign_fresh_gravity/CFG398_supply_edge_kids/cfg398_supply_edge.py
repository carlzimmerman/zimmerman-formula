#!/usr/bin/env python3
"""CFG398: supply-limited phantom edge vs KiDS's required reach (FROZEN_CRITERIA.md). Run: python3 cfg398_supply_edge.py [--mutate]"""
import os, sys, json, math, io, contextlib
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s); OUT.append(str(s))
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; COSMIC = 0.1200 / 0.02237
def nu(y): return float(C.nu_mono(np.array([y]))[0])
def r_ta(lmb): return 10 ** (math.log10(0.95) + (lmb - 10) / 1.5 * (math.log10(2.25) - math.log10(0.95)))   # Mpc
def r_edge(Mb, a0, f):
    sup = COSMIC / f * (100 if MUT else 1)
    g = lambda lr: (nu(G * Mb * MSUN / ((10 ** lr) * KPC) ** 2 / a0) - 1) - sup
    return 10 ** brentq(g, -1, 6)   # kpc
res = {}; checks = {}
for foot, a0 in A0.items():
    Mb = 1e11; rM = math.sqrt(G * Mb * MSUN / a0) / KPC
    est = rM * (1 + COSMIC / 0.10 * (100 if MUT else 1)); ex = r_edge(Mb, a0, 0.10)
    checks[f"K1_{foot}"] = abs(ex / est - 1) < 0.05
    checks[f"K2_{foot}"] = r_edge(Mb, a0, 1.0) < r_edge(Mb, a0, 0.18)
    P(f"{foot}: K1 exact {ex:.1f} vs deep {est:.1f} kpc -> {checks[f'K1_{foot}']}; K2 monotone {checks[f'K2_{foot}']}")
    for f in (0.07, 0.10, 0.18):
        xs = []
        for lmb in (10.0, 10.5, 11.0, 11.5):
            re = r_edge(10 ** lmb, a0, f); x = re / 1e3 / r_ta(lmb); xs.append(x)
            P(f"   f_ret {f:.2f} log M_b {lmb}: r_edge {re:7.1f} kpc, r_ta {r_ta(lmb):.2f} Mpc, x = {x:.2f}")
        v = "CONSISTENT-STRICT" if min(xs) >= 0.47 else "CONSISTENT" if min(xs) >= 0.30 else "TENSION"
        res[f"{foot}|{f}"] = dict(x=xs, verdict=v); P(f"   -> f_ret {f:.2f}: {v}")
    for lmb in (10.0, 10.5, 11.0, 11.5):
        need = {}
        for xt in (0.30, 0.47):
            target = xt * r_ta(lmb) * 1e3
            sup_need = nu(G * 10 ** lmb * MSUN / (target * KPC) ** 2 / a0) - 1
            need[xt] = COSMIC / sup_need * (100 if MUT else 1)
        res[f"{foot}|need|{lmb}"] = need
        P(f"   log M_b {lmb}: largest f_ret for x >= 0.30: {need[0.30]:.3f}; for x >= 0.47: {need[0.47]:.3f}")
json.dump(dict(res=res, checks=checks), open(os.path.join(HERE, f"cfg398_supply_edge{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg398_supply_edge{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    ok = all(v["verdict"] == "CONSISTENT-STRICT" for k, v in res.items() if "need" not in k)
    P(f"MUTATE: all CONSISTENT-STRICT -> {'detected (exit 1)' if ok else 'NOT detected'}"); sys.exit(1 if ok else 0)
sys.exit(0 if all(checks.values()) else 1)
