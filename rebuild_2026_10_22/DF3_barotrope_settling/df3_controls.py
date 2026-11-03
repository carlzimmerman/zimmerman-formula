#!/usr/bin/env python3
"""DF3 controls. DF3_MUTATE=1 runs K x 16. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import numpy as np, df3_solver as S
MUT = os.environ.get("DF3_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; ck = {}
KPC = 3.0857e19; r = np.geomspace(1e-3 * KPC, 3e5 * KPC, 4000)
Mt = 1e11 * S.MSUN
# Lane-Emden, Newtonian: M finite, surface where rho = 0. rta beyond it
S.Cfg.gamma = 5 / 3; S.Cfg.sigma = 3e4; S.Cfg.K_mult = 1.0; S.Cfg.nmax = 4000
def le(mult):
    S.Cfg.K_mult = mult; o = S.solve(r, np.zeros(r.size), r[-1], KPC, Mt, a0=0.0); M = o["Mf"]; rho = o["rho"]; i = np.argmax(M >= 0.99999 * M[-1]); R = r[np.argmax(rho <= 0)] if (rho <= 0).any() else r[-1]; rc = math.exp(o["lrc"]); return rc, M[-1], R
rc, M, R = le(1.0); rb = M / (4 * math.pi / 3 * R ** 3); P = None; K_true = S.Cfg.sigma ** 2 / (5 / 3) * S.RHO_A ** (-2 / 3); alpha = math.sqrt(2.5 * K_true * rc ** (-1 / 3) / (4 * math.pi * S.G)); ck["K_lane_emden"] = dict(rhoc_over_mean=rc / rb, expect=5.99071, xi1=R / alpha, expect_xi=3.65375, M_over_fair=M / Mt, passed=bool(abs(rc / rb / 5.99071 - 1) < 0.05 and abs(R / alpha / 3.65375 - 1) < 0.02 and abs(M / Mt - 1) < 0.01))
rc16, _, _ = le(16.0); ck["K_K16"] = dict(ratio=rc16 / rc, expect=16 ** -3.0, passed=bool(abs(rc16 / rc / 16 ** -3.0 - 1) < 0.05)); S.Cfg.K_mult = 1.0
# isothermal, Newtonian: largest M inside fixed r, regular branch
S.Cfg.gamma = 1.0; S.Cfg.sigma = 1e5; Rv = 1e3 * KPC; rg = np.geomspace(1e-3 * Rv, Rv, 1600); o = S.solve(rg, np.zeros(rg.size), Rv, Rv, 1e60, a0=0.0); eta = o["Mf"][-1] * S.G / (S.Cfg.sigma ** 2 * Rv); ck["K_isothermal_max"] = dict(eta=eta, expect=2.52, noeq=bool(o["noeq"]), passed=bool(abs(eta / 2.52 - 1) < 0.02 and o["noeq"]))
S.Cfg.nmax = 200
# fair share reached, law on, baryon well; grid doubling
S.Cfg.gamma = 5 / 3; S.Cfg.sigma = 1e5; Mb0 = lambda x: 1e14 * S.MSUN * (x / (x + 300 * KPC)) ** 2; rta = 6e3 * KPC; A0 = 9.3603e-11; vals = {}
for n in (420, 840):
    x = np.geomspace(1 * KPC, rta * 1.0001, n); o = S.solve(x, Mb0(x), rta, 1500 * KPC, 5.3e14 * S.MSUN, a0=A0); vals[n] = (float(np.interp(1500 * KPC, x, o["Mf"])), float(o["Mf"][-1]))
ck["K_fair_grid"] = dict(M1500=vals, fair=vals[840][1] / (5.3e14 * S.MSUN), ratio=vals[420][0] / vals[840][0], passed=bool(abs(vals[840][1] / (5.3e14 * S.MSUN) - 1) < 0.01 and abs(vals[420][0] / vals[840][0] - 1) < 0.01))
ck["all"] = all(v["passed"] for v in ck.values()); print(json.dumps(ck, indent=1, default=float)); json.dump(ck, open(os.path.join(HERE, f"df3_controls{TAG}.json"), "w"), indent=1, default=float)
