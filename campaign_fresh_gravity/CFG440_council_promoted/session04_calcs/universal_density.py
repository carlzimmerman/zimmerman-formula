#!/usr/bin/env python3
"""Session 4, Addendum U: one cold-fluid density for all dwarfs, fit on UFDs, predict classicals. Run: python3 universal_density.py [--mutate]"""
import os, sys, json, math
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
src = open(os.path.join(HERE, "classicals_supply.py")).read()
ns = {"__file__": os.path.join(HERE, "classicals_supply.py")}
sys_argv = sys.argv; sys.argv = [sys.argv[0]]
exec(src[:src.index("res = {}")], ns); sys.argv = sys_argv
j, rows, obj, pieces, Ru, ufd = ns["j"], ns["rows"], ns["obj"], ns["pieces"], ns["Ru"], ns["ufd"]
G, MSUN, PC, COSMIC = ns["G"], ns["MSUN"], ns["PC"], ns["COSMIC"]
OUT = []
def P(s=""): print(s); OUT.append(str(s))
cls, Rc = [], []
for nm, e in zip(j["NAMES"]["cls"], j["EST"]["-0.2|cls"]):
    d = obj(rows[nm]) if nm in rows else None
    if d and e and e.get("lR") is not None: cls.append(d); Rc.append(10 ** e["lR"])
Ruf = [Ru[d["name"]] for d in ufd]
def offs(objs, Rs, a0, rho):
    out = []
    for d, R in zip(objs, Rs):
        Mb, r, Ml = pieces(d, a0)
        Mc = 0.13 * COSMIC * R * Mb
        rc = (3 * Mc / (4 * math.pi * rho)) ** (1 / 3)              # pc, rho in Msun/pc^3
        q = min(1.0, (d["rh"] * 4 / 3 / rc) ** 3)
        out.append(math.log10(d["sig"] / (math.sqrt(G * (Ml + q * Mc) * MSUN / (3 * r)) / 1e3)))
    return np.array(out)
res = {}
for foot, a0 in (("canonical", 9.36e-11), ("alt", 1.13e-10)):
    fit = lambda lr, objs, Rs: float(np.median(offs(objs, Rs, a0, 10 ** lr)))
    try: rho_u = 10 ** brentq(lambda lr: fit(lr, ufd, Ruf), -6, 4)
    except ValueError: rho_u = float("nan")
    try: rho_c = 10 ** brentq(lambda lr: fit(lr, cls, Rc), -6, 4)
    except ValueError: rho_c = float("nan")
    use = rho_u * (100 if MUT else 1)
    x = offs(cls, Rc, a0, use); med = float(np.median(x))
    bs = [np.median(x[np.random.default_rng(21 + k).integers(0, len(x), len(x))]) for k in range(2000)]
    err = math.hypot(float(np.std(bs)), 0.077)
    v = "PASS" if abs(med) < 2 * err else "FAIL"
    res[foot] = dict(rho_ufd=rho_u, rho_cls=rho_c, ratio=rho_u / rho_c, cls_median=med, err=err, verdict=v)
    P(f"{foot:9s}: rho_c fit on UFDs {rho_u:.3g} Msun/pc^3; classicals predicted median {med:+.3f} +- {err:.3f} -> {v}; classicals alone need {rho_c:.3g} (UFD/cls ratio {rho_u/rho_c:.2g})")
json.dump(res, open(os.path.join(HERE, f"universal_density{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"universal_density{TAG}.out"), "w").write("\n".join(OUT) + "\n")
rc = 0
if MUT:
    c = json.load(open(os.path.join(HERE, "classicals_supply_results.json")))["-0.2|canonical|q1.0"]["median"]
    rc = 1 if abs(res["canonical"]["cls_median"] - c) < 0.005 else 0
    P(f"MUTATE: classical median {res['canonical']['cls_median']:+.3f} vs C q=1 {c:+.3f} -> {'detected' if rc else 'NOT detected'}")
sys.exit(rc)
