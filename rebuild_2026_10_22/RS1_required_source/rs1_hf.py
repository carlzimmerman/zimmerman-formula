#!/usr/bin/env python3
"""RS1 Part 3: requirement map over HF1's cluster sigma and retention on X-COP. A private solve with sigma x s; fair share x r. HF1's label doesn't move. A map, not a rule. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); HF = os.path.join(os.path.dirname(HERE), "HF1_hybrid_fermion"); sys.path.insert(0, HF); sys.dont_write_bytecode = True
import hf1_g23 as H
import numpy as np
src = open(os.path.join(HF, "hf1_fermion.py")).read(); a = "s2 = 0.5 * np.max(np.where(insys, V2, 0.0), axis=-1, keepdims=True)"; assert src.count(a) == 1
src = src.replace(a, a + " * SFAC ** 2"); NS = {"SFAC": 1.0}; exec(compile(src, "hf1_fermion_private", "exec"), NS)
H.FM.solve = NS["solve"]; XC = H.C.xcop_load(); out = []; res = {}
def P(s): print(s, flush=True); out.append(s)
CELLS = {5.0: 0.17486 / 0.02797, 11.8: 0.13119 / 0.02363}
P("RS1 Part 3, X-COP on HF1's R4, sigma x s, fair share x r; numbers only. HSE. kappa = 1/2 FITTED; not theory closed.")
for ft in H.FEET:
    for m, Rf in CELLS.items():
        P(f"\n{ft} m {m:g}, omega_f/omega_b {Rf:.3f}: s, r, mean, rms, by x (0.1 0.2 0.3 0.5 0.7), median sigma km/s"); key = f"{ft}|{m:g}"; res[key] = []
        for s in (1.0, 0.85, 0.7, 0.6, 0.5, 0.4, 0.3):
            for r in (1.0, 0.8, 0.6, 0.4, 0.2):
                NS["SFAC"] = s; x = H.xcop_rows(XC, Rf * r, m, ft); a_ = x["all"]; sg = float(np.median([v["sigma_kms"] for v in x["info"].values()])) if "info" in x else float("nan"); bx = [x["by_x"][str(q)] for q in H.C.XS]; ok = bool(abs(a_["mean"]) <= 0.05 and a_["rms"] <= 0.10)
                res[key].append(dict(s=s, r=r, mean=a_["mean"], rms=a_["rms"], by_x=bx, sigma=sg, clears=ok))
                P(f"  {s:4.2f} {r:3.1f} {a_['mean']:+.3f} {a_['rms']:.3f} " + " ".join(f"{q:+.2f}" for q in bx) + f"  {sg:6.0f}" + ("  CLEARS" if ok else ""))
k = {f: next(c for c in res[f"canonical|{f}"] if c["s"] == 1.0 and c["r"] == 1.0)["mean"] for f in ("5", "11.8")}; res["K5"] = dict(m5=k["5"], m118=k["11.8"], passed=bool(abs(k["5"] - 0.159) <= 0.002 and abs(k["11.8"] - 0.178) <= 0.002)); P(f"\nK5 {res['K5']}"); P("Not theory closed.")
json.dump(res, open(os.path.join(HERE, "rs1_hf.json"), "w"), indent=1); open(os.path.join(HERE, "rs1_hf.out"), "w").write("\n".join(out) + "\n")
