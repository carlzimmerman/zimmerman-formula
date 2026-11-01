#!/usr/bin/env python3
"""DR6: direct Delta Sigma_2h amplitude without exclusion, M3's median z, M200, b from the grader's rows; J2 Hankel of RF5's P(k). Reported. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, glob
import numpy as np
from scipy.special import jv
H = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(H, "dr6_pk.json"))); z_ = np.load(os.path.join(H, "cache_pk", "pk.npz")); K, PK = z_["K"], z_["PK"]; lk = np.log(K)
rows = json.load(open(os.path.join(H, "cache_jobs", "C3_0.034_+1_rows.json"))); seen = {r["i"]: r for r in rows}; rows = list(seen.values()); out = {}
for t in range(3):
    r = [q for q in rows if q["t"] == t]; med = lambda k: float(np.median([q[k] for q in r])); z = med("z"); b = med("b"); Dz = float(np.interp(z, D["z"], D["D"])); e = dict(n=len(r), z=z, lgM200=med("lgM200"), R200=med("R200"), rta=med("rta"), b=b, nu=med("nu"), Mfair=med("Mfair"), add_share=float(np.median([q["add_in_rta"] / (q["Mfair"] + q["Mb"]) for q in r])), ratio={x: float(np.nanmedian([q["ratio"].get(x, np.nan) for q in r])) for x in ("1.5", "2.0", "3.0", "5.0", "0.9rta")}, n_ratio={x: int(sum(x in q["ratio"] for q in r)) for x in ("1.5", "2.0", "3.0", "5.0")}, dsig={})
    kk = np.geomspace(K[0], K[-1], 400000); P_ = np.exp(np.interp(np.log(kk), lk, np.log(PK))) * np.exp(-(kk * 0.05) ** 2)
    for R in (1.42, 2.0, 3.0):
        Rc = R * (1 + z); ds = b * Dz ** 2 * D["rhom"] * np.trapz(kk ** 2 * P_ * jv(2, kk * Rc), np.log(kk)) / (2 * np.pi) * (1 + z) ** 2 / 1e12; e["dsig"][str(R)] = float(ds)
    out[f"M{t + 1}"] = e; print(f"M{t + 1}", json.dumps(e))
json.dump(out, open(os.path.join(H, "dr6_amp.json"), "w"), indent=0)
