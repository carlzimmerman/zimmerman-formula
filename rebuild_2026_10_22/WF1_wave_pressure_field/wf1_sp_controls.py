#!/usr/bin/env python3
"""WF1 SP controls: Newtonian ground state (known answer), virial as referee, m x 16 at fixed mass (MUTATE). kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "HF1_hybrid_fermion")); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import numpy as np, wf1_solver as S
def sp(M, m_ev, n=1200):
    mk = m_ev * S.EV / S.C_L ** 2; a = (S.HBAR / mk) ** 2 / (S.G * M); kap = (S.HBAR / mk) ** 2 / 2; r = np.geomspace(1e-3 * a, 300 * a, n); dl = math.log(r[1] / r[0]); Mf = M * (1 - np.exp(-(r / (3 * a)) ** 3))
    for _ in range(400):
        g = S.G * Mf / r ** 2; C = S._cum(g * r, dl); Phi = C - C[-1] - S.G * M / r[-1]; E, y = S.ground(r, Phi, kap, dl); Mn = M * (np.cumsum(y * y) - 0.5 * y * y); d = float(np.max(np.abs(Mn - Mf))) / M; Mf = 0.5 * Mf + 0.5 * Mn
        if d < 1e-9: break
    W = -float((y * y * S.G * Mn / r * 1).sum()); Wself = 0.5 * float((y * y * Phi).sum()); T = E - float((y * y * Phi).sum()); rh = float(np.interp(0.5, Mn / M, r))
    return dict(E_dimless=E / (S.G * M / a), r_half_dimless=rh / a, virial=(2 * T + Wself) / abs(Wself), rh=rh, iters=_ + 1)
ck = {}; a = sp(1e10 * 1.989e30, 1e-22); ck["K_SP"] = dict(a, E_expect=-0.163, rh_expect=3.93, passed=bool(abs(a["virial"]) <= 0.005 and abs(a["E_dimless"] / -0.163 - 1) <= 0.01 and abs(a["r_half_dimless"] / 3.93 - 1) <= 0.01))
b = sp(1e10 * 1.989e30, 16e-22); ck["M_m16"] = dict(ratio=b["rh"] / a["rh"], expect=16.0 ** -2, passed=bool(abs(b["rh"] / a["rh"] * 256 - 1) <= 0.01))
c = sp(1e10 * 1.989e30, 1e-22, n=2400); ck["K_grid"] = dict(d=c["rh"] / a["rh"] - 1, passed=bool(abs(c["rh"] / a["rh"] - 1) <= 0.01))
json.dump(ck, open(os.path.join(HERE, "wf1_sp_controls.json"), "w"), indent=1, default=float); print(json.dumps(ck, indent=1, default=float)); sys.exit(0 if all(v["passed"] for v in ck.values()) else 1)
