#!/usr/bin/env python3
"""HM1 Local Group (FROZEN_CRITERIA.md): OP1's P1, EM1's M200, the 1e10 tag, with the response. Plummer baryons on M*. OP1, SN1 read only. kappa = 1/2 FITTED, unused; not theory closed."""
import contextlib, io, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); T = open(os.path.join(RB, "OP1_one_profile_dwarfs", "op1.py")).read(); T = T[:T.index("RES = {}\n")]
ns = {"__file__": os.path.join(RB, "OP1_one_profile_dwarfs", "op1.py"), "__name__": "x"}; a_ = sys.argv; sys.argv = ["op1.py"]; exec(compile(T, "op1", "exec"), ns); sys.argv = a_
Mh, g, G, MSUN, CLS = ns["Mh"], ns["g"], ns["G"], ns["MSUN"], ns["CLS"]; SGN = 1
_x = open(os.path.join(RB, "X39_baryonic_contraction", "x39_contraction.py")).read(); exec(_x[_x.index("def contract(r, Mb, M0, F, gnedin=None):"):_x.index('P("\\n=== checks")')])
def E_(Q, lM, mp, f):
    o = []
    for q, l in zip(Q, lM):
        R2 = Mh(q["r12"], 10 ** l, mp, "tag10")[1]; r12 = q["r12"]
        if f == 0: Mc = Mh(r12, 10 ** l, mp, "tag10")[0]
        else:
            rg = np.geomspace(min(r12, R2) * 1e-3, max(R2, r12 * 2), 400); M0 = np.array([Mh(r, 10 ** l, mp, "tag10")[0] for r in rg]); Mb = 2 * q["gN"] * r12 ** 2 / G; a = r12 / 1.305; Mbg = Mb * rg ** 3 / (rg ** 2 + a ** 2) ** 1.5; Mf = contract(rg, Mbg, M0, float(Mbg[-1] / M0[-1]))[0]; Mc = float(np.interp(math.log(r12), np.log(rg), M0 + f * (Mf - M0)))
        o.append(math.log10(q["gobs"] / (q["gN"] + G * Mc / r12 ** 2)))
    return np.array(o)
RES = {}; OP = json.load(open(os.path.join(RB, "OP1_one_profile_dwarfs", "op1_results.json"))); kk = 0.0
for ft in g["FEET"]:
    Q = g["systems"](ft); idx = g["boot_setup"](Q); lE = np.log10([q["M200"] / MSUN for q in Q]); RES[ft] = {}
    for mp in ("frozen", "FC1"):
        for lab, f in (("off", 0.0), ("fq", 0.872), ("blum", 1.0), ("MUTATE05", 0.436)):
            z = g["clsZ"](E_(Q, lE, mp, f), Q, idx); RES[ft][f"{mp}|{lab}"] = {c: dict(E=v[0], Z=v[2]) for c, v in z.items()}; print(ft, mp, lab, {c[:8]: (round(v[0], 3), round(v[2], 2)) for c, v in z.items()}, flush=True)
            if lab == "off": kk = max(kk, max(abs(RES[ft][f"{mp}|off"][c]["E"] - OP[ft][mp]["P1_tag10"][c]["E"]) for c in CLS))
RES["K6_op1"] = kk; print("K6 off vs OP1 P1 |d|", kk); json.dump(RES, open(os.path.join(HERE, "hm1_op1.json"), "w"), indent=1, default=float)
