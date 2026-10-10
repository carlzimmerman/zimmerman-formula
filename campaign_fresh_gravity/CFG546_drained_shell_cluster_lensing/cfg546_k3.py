#!/usr/bin/env python3
"""CFG546 K3 (reported): does the 3D template, projected on the stacked S0 profile, reproduce the simulation's own ΔΣ ratio T2D?

Reads cfg546_predict_results.json only. The stacked S0 profile is known to 4 r_ta; beyond that the S0 overdensity is extended as
a power law fitted over 2-4 r_ta (the box projection includes it). Writes cfg546_k3.out / cfg546_k3_results.json.
Run: nice -n 10 python3 cfg546_k3.py
"""
import os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
trapz = getattr(np, "trapezoid", None) or np.trapz
R = json.load(open(os.path.join(HERE, "cfg546_predict_results.json")))
XC = np.array(R["xc"])
lines = []; out = {}


def P(s):
    print(s); lines.append(s)


P(__doc__.split("Run:")[0].strip())
rg = np.geomspace(0.01, 60, 1500); lg = np.concatenate([[0], np.geomspace(1e-3, 60, 600)])
X = np.geomspace(0.05, 4, 200)


def ds_of(d3):
    rr = np.sqrt(X[:, None] ** 2 + lg[None, :] ** 2)
    S = 2 * trapz(np.interp(rr, rg, d3), lg, axis=1)
    cum = np.concatenate([[S[0] * X[0] ** 2 / 2], S[0] * X[0] ** 2 / 2 + np.cumsum(0.5 * (S[1:] * X[1:] + S[:-1] * X[:-1]) * np.diff(X))])
    return 2 * cum / X ** 2 - S


for run, v in R["runs"].items():
    for b, bb in v["bins"].items():
        if bb.get("T2D") is None or not bb["resolved"]: continue
        d0 = np.array(bb["S0_profile"]) - 1.0; rel = np.array(bb["rel"])
        m = (XC >= 2) & (XC <= 4) & (d0 > 0)
        sl, ic = np.polyfit(np.log(XC[m]), np.log(d0[m]), 1)
        def ext(x, y): return np.where(rg <= XC[-1], np.interp(rg, XC, y), np.exp(ic) * rg ** sl)
        dS = ext(XC, d0); dF = ext(XC, d0 * (1 + rel))
        T = (ds_of(dF) - ds_of(dS)) / ds_of(dS)
        Tb = np.interp(XC, X, T)
        T2 = np.array(bb["T2D"]); s2 = np.array(bb["T2D_sig"])
        mm = (XC >= 0.3) & (XC <= 3.0)
        pull = (Tb[mm] - T2[mm]) / np.maximum(s2[mm], 1e-9)
        ok = bool(np.all(np.abs(pull) < 3))
        P(f"  {run} {b}: projected-3D vs T2D over 0.3-3 R/r_ta: max |pull| {np.max(np.abs(pull)):.2f}, chi2 {np.sum(pull ** 2):.1f}/{mm.sum()} -> "
          f"{'PASS' if ok else 'FAIL'} (reported); proj at X 0.45/1.05/1.95: {Tb[4]:+.3f}/{Tb[10]:+.3f}/{Tb[19]:+.3f} vs T2D {T2[4]:+.3f}/{T2[10]:+.3f}/{T2[19]:+.3f}")
        out[f"{run}|{b}"] = dict(max_pull=float(np.max(np.abs(pull))), chi2=float(np.sum(pull ** 2)), n=int(mm.sum()), ok=ok)
json.dump(out, open(os.path.join(HERE, "cfg546_k3_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg546_k3.out"), "w").write("\n".join(lines) + "\n")
