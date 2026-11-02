#!/usr/bin/env python3
"""BK1 target budget (FROZEN_CRITERIA.md), before any search. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "UX3_cluster_gas_term"))
from ux3_common import *
from scipy.optimize import minimize_scalar
X, nm = xcop(); XT = X[X[:, 4].astype(int) % 2 == 0]
def kf(A, a0): return minimize_scalar(lambda k: (resid(A, a0, lambda y, f, _: 1 + k * y * f) ** 2).sum(), bounds=(0, 60), method="bounded", options=dict(xatol=1e-6)).x
STAT = dict(canonical=2.098, alt=2.281); VAL = dict(canonical=13.287, alt=14.251); DQ = dict(canonical=(7.56, 5.37), alt=(7.18, 4.93))
R = {"T": {}}
for f, a0 in A0S.items():
    XL = XT.copy(); XL[:, 1] = XL[:, 1] * 10 ** -.12; k0, k1 = kf(XT, a0), kf(XL, a0); sy = (k0 - k1) / 2; hsc = (1.7 - 1) * k0 / 2
    R[f] = dict(K=dict(value=k0, k_hse_low=k1, stat=STAT[f], sys_hse=sy, sigma=math.hypot(STAT[f], sy), sigma_hsc=math.sqrt(STAT[f] ** 2 + sy ** 2 + hsc ** 2)))
    for t, v, st_, s2 in (("D8", DQ[f][0], 1.03, 1.4), ("D5", DQ[f][1], .79, 1.05)):
        h = .7 * v / 2; R[f][t] = dict(value=v, stat=st_, sys_hse=s2, sigma=math.hypot(st_, s2), sigma_hsc=math.sqrt(st_ ** 2 + s2 ** 2 + h ** 2))
    print(f, json.dumps(R[f]))
oc, ob = 0.1197242714576543, 0.02237712457035148; rel = math.hypot(.027, .002); rel2 = math.hypot(rel, .01)
R["XR"] = dict(value=oc / ob, sigma=oc / ob * rel, sigma_2=oc / ob * rel2, f_b=ob / (ob + oc)); R["RHO"] = dict(value=2.249e-27, sigma=2.249e-27 * rel, sigma_2=2.249e-27 * rel2)
R["FQ"] = dict(value=.946, sigma=math.hypot(.15, .037)); R["T"] = dict(value=12.29, sigma_dex=.05)
print({k: R[k] for k in ("XR", "RHO", "FQ", "T")}); json.dump(R, open("bk1_budget.json", "w"), indent=1, sort_keys=True)
