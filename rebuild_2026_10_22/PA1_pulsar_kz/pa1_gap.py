#!/usr/bin/env python3
"""PA1 part 1: form gaps at K(R0, 1.1 kpc) from UX5's cache, in-prior cells, same baryons. No new solve. Footings never pooled. kappa = 1/2 FITTED; not theory closed."""
import json, numpy as np, os
C = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "UX5_mw_stellar_mass", "cache")
CONV = 2*np.pi*4.30091e-6*1e6 *1e6/3.0856775814913673e19 /(1e-3/(365.25*86400))  # K in Msun/pc^2 to mm/s/yr
O = {"mm_s_yr_per_K": CONV}
for f in ("canonical", "alt"):
    rows = [json.loads(l) for l in open(f"{C}/{f}_1.0.jsonl")]
    for box in ("B175", "BV", "BV2"):
        r = [x for x in rows if x["box"] == box and x["inp"]]
        for tag, s in (("all in-prior", r), ("A v_c in line", [x for x in r if x["A"]["L1"]])):
            if not s: O[f"{f} {box} {tag}"] = dict(n=0); continue
            d = np.array([x["A"]["K0"]-x["R"]["K0"] for x in s]); dq = np.array([x["Q"]["K0"]-x["R"]["K0"] for x in s]); ka = np.array([x["A"]["K0"] for x in s]); kr = np.array([x["R"]["K0"] for x in s])
            O[f"{f} {box} {tag}"] = dict(n=len(s), gapA_min=d.min(), gapA_med=float(np.median(d)), gapA_max=d.max(), gapQ_min=dq.min(), KA_min=ka.min(), KA_med=float(np.median(ka)), KR_min=kr.min(), KR_med=float(np.median(kr)), KR_max=kr.max(), frac_med=float(np.median(d/ka)))
    allr = [x for x in rows if x["inp"] and x["A"]["L1"]]
    O[f"{f} counts"] = dict(in_prior_A_L1=len(allr), in_prior_Q_L1=sum(x["Q"]["L1"] for x in rows if x["inp"]), R_inprior_L1=sum(x["R"]["L1"] for x in rows if x["inp"]))
json.dump(O, open("pa1_gap.json","w"), indent=1, sort_keys=True, default=float)
for k in sorted(O):
    print(k, O[k] if not isinstance(O[k],dict) else {a:(round(b,3) if isinstance(b,float) else b) for a,b in O[k].items()})
