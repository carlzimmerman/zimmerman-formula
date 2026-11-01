#!/usr/bin/env python3
"""DR7 K2, K3, K4 on a test case, with an independent Q. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); from dr7_cap import cap
S = open(os.path.join(H, "..", "X39_baryonic_contraction", "x39_contraction.py")).read(); SGN = 1; exec(S[S.index("def contract(r, Mb, M0, F, gnedin=None):"):S.index('P("\\n=== checks")')])
def B(x): return np.log(1 + x * x) + 2 * np.log(1 + x) - 2 * np.arctan(x)
def case(n, a=0.3, Mbt=0.15):
    r = np.geomspace(1e-3, 30.0, n); M0 = B(r) / B(np.array(30.0)); Mb = Mbt * r ** 2 / (r + a) ** 2 / (30 / 30.3) ** 2; return r, Mb, M0, float(Mb[-1])
def indep(r, M, Mo):
    """Independent: np.gradient density, direct Jeans quadrature, Q = rho/sigma^3."""
    rho = np.gradient(M, r) / (4 * np.pi * r ** 2); f = rho * (M + Mo) / r ** 2; P = np.array([np.trapz(f[i:], r[i:]) for i in range(len(r))]); o = (rho > 0) & (P > 0); Q = np.full(len(r), np.nan); Q[o] = rho[o] / (P[o] / rho[o]) ** 1.5; return Q
Q = {}; res = {}
r, Mb, M0, F = case(1600); Mc = contract(r, Mb, M0, F)[0]; M, inf = cap(r, Mb, M0, Mc, F); i = inf["i_s"]; Qi = indep(r, M0, F * M0); Q0 = np.nanmax(Qi[2:i + 1]); Qm = indep(r, M, Mb); Qu = indep(r, Mc, Mb)
w = np.arange(4, i - 3); a = float(np.nanmax(Qm[w]) / Q0); u = float(np.nanmax(Qu[w]) / Q0)
res["K2"] = dict(capped_over_Q0=a, uncapped_over_Q0=u, PASS=bool(a <= 1.05 and u > 1.05), r_s=float(r[i]), conv=inf["conv"])
Mz = contract(r, F * M0, M0, F)[0]; Mi, inz = cap(r, F * M0, M0, Mz, F); j = np.arange(5, len(r) - 5); res["K3"] = dict(dev=float(np.max(np.abs(Mi[j] / M0[j] - 1))), blum_dev=float(np.max(np.abs(Mz[j] / M0[j] - 1)))); res["K3"]["PASS"] = res["K3"]["dev"] <= 1e-3
rh = float(np.interp(0.5 * Mb[-1], Mb, r)); m1 = float(np.interp(math.log(rh), np.log(r), M)); r2, Mb2, M02, F2 = case(3200); M2 = cap(r2, Mb2, M02, contract(r2, Mb2, M02, F2)[0], F2)[0]; m2 = float(np.interp(math.log(rh), np.log(r2), M2)); res["K4"] = dict(move=abs(m2 / m1 - 1), M_over_Mc_rh=m1 / float(np.interp(math.log(rh), np.log(r), Mc)), PASS=bool(abs(m2 / m1 - 1) <= 0.01))
print(json.dumps(res, indent=1)); json.dump(res, open(os.path.join(H, "dr7_checks.json"), "w"), indent=1); sys.exit(0 if all(v["PASS"] for v in res.values()) else 1)
