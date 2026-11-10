#!/usr/bin/env python3
"""KL1 AMENDMENT A1 (POST HOC, e01d1b9a35): MUTATE arm MA2b. KA2 (FROZEN_CRITERIA.md section 3) rerun with every effective density
n_i doubled must FAIL test (ii), on KiDS-1000 and DES Y3, both footings, at the A0 fiducial (the survey's best sigma8 from row A0).
The area is refitted on the mutated covariance exactly as KA2 fits it.

  OMP_NUM_THREADS=1 nice -n 10 python3 kl1_ma2b.py     -> parts/ma2b_MUTATE.json, parts/ma2b_MUTATE.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import kl1_lib as K1
HERE = K1.HERE; OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = dict(lane="KL1", arm="MA2b (MUTATE, AMENDMENT A1, post hoc): KA2 with every n_i doubled must fail (ii)", amendment="e01d1b9a35", note="kappa = 1/2 FITTED; not theory closed", rows={})
K1.setP(K1.PZ0)
for ft in K1.FOOTS:
    rows = json.load(open(os.path.join(HERE, "parts", f"rows_{ft}.json")))["rows"]; Rk = np.array(K1.HM["primary"][ft]["R_tot"])
    for sn, S in K1.SURV.items():
        fid = rows["A0"][sn]["best_sigma8"]; Pm = K1.Pmat(K1.run_of(Rk, (fid / K1.S8E) ** 2, "resp"), "F"); pub = np.where(S["pubkeep"])[0]
        out = {}
        for tag, sc in (("n_x1", 1.0), ("n_x2", 2.0)):
            G1, N1 = K1.gauss_cov(S, pub, K1.cell_full(S, Pm), ng_scale=sc); dg = np.diag(G1); nf = np.diag(N1) / dg; dp = np.diag(S["cov"][np.ix_(pub, pub)])
            nd = nf >= 0.8; sd = nf < 0.5; area = float(1.0 / np.median(dp[nd] / dg[nd])); r = dp / (dg / area)
            o = dict(n_noise=int(nd.sum()), n_signal=int(sd.sum()), area_deg2=area * (180 / math.pi) ** 2)
            if nd.sum() >= 5: q16, q84 = np.percentile(r[nd], [16, 84]); o.update(i_q16=float(q16), i_q84=float(q84), i_pass=bool(q16 >= 0.85 and q84 <= 1.15))
            else: o["i_pass"] = None
            if sd.sum() >= 5: o.update(ii_median=float(np.median(r[sd])), ii_min=float(np.min(r[sd])), ii_pass=bool(0.95 <= np.median(r[sd]) <= 1.6 and np.min(r[sd]) >= 0.80))
            else: o["ii_pass"] = None
            out[tag] = o
        out["bites"] = bool(out["n_x2"]["ii_pass"] is False); out["control_reproduces_KA2"] = bool(out["n_x1"]["i_pass"] is True and out["n_x1"]["ii_pass"] is True)
        RES["rows"].setdefault(ft, {})[sn] = out; m = out["n_x2"]
        P(f"[{ft}] {sn}: n x 2: area {m['area_deg2']:.0f} deg^2; (i) {m.get('i_q16', float('nan')):.3f}-{m.get('i_q84', float('nan')):.3f} -> {m['i_pass']}; (ii) {m['n_signal']} points, median "
          f"{m.get('ii_median', float('nan')):.3f}, min {m.get('ii_min', float('nan')):.3f} -> {m['ii_pass']} => {'FAILS, so the arm bites' if out['bites'] else 'DOES NOT BITE'}  "
          f"(control n x 1 reproduces KA2: {out['control_reproduces_KA2']})")
json.dump(RES, open(os.path.join(HERE, "parts", "ma2b_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "parts", "ma2b_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
