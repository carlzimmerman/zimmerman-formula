#!/usr/bin/env python3
"""Controls: Lane-Emden known answers, isothermal limit, K x 16, fair share, grid doubling, TOV. DF3G_MUTATE=1: self-gravity x 4. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
os.environ["OMP_NUM_THREADS"] = "1"; os.nice(19); sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, df3g_solver as S
MUT = os.environ.get("DF3G_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; S.Cfg.gself = 4.0 if MUT else 1.0; ck = {}; KPC = 3.0857e19
S.Cfg.reading = "N"; S.Cfg.dln = 0.01; S.Cfg.r_start = 1e-3 * KPC
r = np.geomspace(1e-3 * KPC, 3e5 * KPC, 8000); Mt = 1e11 * S.MSUN; Z = np.zeros(r.size)
def run(gam, mult=1.0, M=Mt):
    S.Cfg.gamma = gam; S.Cfg.sigma = 3e4; S.Cfg.K = mult; S.Cfg.dln = 0.004; o = S.solve(r, Z, r[-1], KPC, M, a0=0.0); return o
K0 = lambda gam: S.Cfg.sigma ** 2 / gam * S.RHO_A ** (1 - gam)
o = run(5 / 3); rc = math.exp(o["lrc"]); K_ = K0(5 / 3); al = math.sqrt(2.5 * K_ * rc ** (-1 / 3) / (4 * math.pi * S.G)); lr = np.log(r); M = o["Mf"]; R = r[np.argmax(o["rho"] <= 1e-200)]; rbar = M[-1] / (4 * math.pi / 3 * R ** 3)
ck["K_LE_5_3"] = dict(rho_c=rc, rhoc_over_mean=rc / rbar, expect=5.99071, xi1=R / al, expect_xi=3.65375, M_over_fair=M[-1] / Mt, passed=bool(abs(rc / rbar / 5.99071 - 1) < 0.01 and abs(R / al / 3.65375 - 1) < 0.01 and abs(M[-1] / Mt - 1) < 0.01))
rc1 = rc; o16 = run(5 / 3, 16.0); ck["K_K16"] = dict(ratio=math.exp(o16["lrc"]) / rc1, expect=16.0 ** -3, passed=bool(abs(math.exp(o16["lrc"]) / rc1 / 16.0 ** -3 - 1) < 0.05))
# n = 1, Gamma 2: rho = rho_c sin(xi)/xi, xi_1 = pi
o = run(2.0); rc = math.exp(o["lrc"]); K_ = K0(2.0); al = math.sqrt(2 * K_ / (4 * math.pi * S.G)); xi = r[np.argmax(o["rho"] <= 1e-200)] / al; x = np.array([1.0, 2.0]); ana = np.sin(x) / x; num = np.exp(np.interp(np.log(x * al), lr, np.log(np.maximum(o["rho"], 1e-300)))) / rc
ck["K_LE_n1"] = dict(xi1=xi, expect=math.pi, rho_ratio=(num / ana).tolist(), passed=bool(abs(xi / math.pi - 1) < 0.01 and np.all(np.abs(num / ana - 1) < 0.01)))
# n = 5, Gamma 6/5: theta = (1 + xi^2/3)^(-1/2), rho = rho_c theta^5
S.Cfg.gamma = 1.2; S.Cfg.sigma = 3e4; S.Cfg.K = 1.0; K_ = K0(1.2); al = 1.0 * KPC; rc = (6 * K_ / (4 * math.pi * S.G * al ** 2)) ** (1 / 0.8); rr = np.geomspace(1e-3 * KPC, 1e3 * KPC, 1400); w = rr <= rr[-1]; _, _, _, pr = S.shoot(rr, np.zeros((1, rr.size)), w[None, :], np.array([[math.log(rc)]]), 0.0, keep=True); x = np.array([1.0, 3.0, 10.0]); ana = (1 + x * x / 3) ** -2.5; num = np.exp(np.interp(np.log(x * al), np.log(rr), np.log(pr[0, 0]))) / rc
ck["K_LE_n5"] = dict(rho_ratio=(num / ana).tolist(), passed=bool(np.all(np.abs(num / ana - 1) < 0.01)))
# isothermal maximum at fixed radius
S.Cfg.gamma = 1.0; S.Cfg.sigma = 1e5; S.Cfg.K = 1.0; Rv = 1e3 * KPC; rg = np.geomspace(1e-3 * Rv, Rv, 200); S.Cfg.r_start = 1e-4 * Rv; S.Cfg.dln = 0.02; o = S.solve(rg, np.zeros(rg.size), Rv, Rv, 1e60, a0=0.0); eta = o["Mf"][-1] * S.G / (S.Cfg.sigma ** 2 * Rv); ck["K_iso_max"] = dict(eta=eta, expect=2.52, noeq=o["noeq"], passed=bool(abs(eta / 2.52 - 1) < 0.02 and o["noeq"]))
# fair share and grid doubling in a law well
S.Cfg.gamma = 5 / 3; S.Cfg.sigma = 1e5; S.Cfg.r_start = S.PC; Mb0 = lambda x: 1e14 * S.MSUN * (x / (x + 300 * KPC)) ** 2; rta = 6e3 * KPC; x = np.geomspace(1 * KPC, rta * 1.0001, 400); vals = {}
for d in (0.06, 0.03):
    S.Cfg.dln = d; o = S.solve(x, Mb0(x), rta, 1500 * KPC, 5.3e14 * S.MSUN, a0=9.3603e-11); vals[d] = (float(np.interp(1500 * KPC, x, o["Mf"])), float(o["Mf"][-1]), o["rhalf"] / KPC)
ck["K_fair_grid"] = dict(fair=vals[0.03][1] / (5.3e14 * S.MSUN), ratio=vals[0.06][0] / vals[0.03][0], rhalf=vals[0.03][2], passed=bool(abs(vals[0.03][1] / (5.3e14 * S.MSUN) - 1) < 0.01 and abs(vals[0.06][0] / vals[0.03][0] - 1) < 0.01))
# isothermal in a flat-V well: analytic turn at V = sqrt(3) sigma, rho ~ r^(-V^2/sigma^2) in pure log potential
S.Cfg.gamma = 1.0; S.Cfg.dln = 0.06; S.Cfg.gself = 0.0; x = np.geomspace(0.1 * KPC, 1e3 * KPC, 200); tw = {}
for vr in (1.0, 2.0):
    V = vr * S.Cfg.sigma; Mw = V ** 2 * x / S.G; o = S.solve(x, Mw, x[-1], KPC, 1e11 * S.MSUN, a0=0.0); s = np.gradient(np.log(np.maximum(o["rho"], 1e-300)), np.log(x))[100]; tw[vr] = float(s)
ck["K_flat_V"] = dict(slope=tw, expect={1.0: -1.0, 2.0: -4.0}, passed=bool(abs(tw[1.0] + 1) < 0.05 and abs(tw[2.0] + 4) < 0.05)); S.Cfg.gself = 4.0 if MUT else 1.0
# TOV
mn = 1.67492750e-27; Mo = S.tov_max(mn); Kn = (3 * math.pi ** 2) ** (2 / 3) * S.HBAR ** 2 / (5 * mn ** (8 / 3)); M16 = S.tov_max(S.m_of_K(16 * Kn))
ck["K_tov"] = dict(M_OV=Mo, expect=0.71, m_back=S.m_of_K(Kn) / mn, ratio16=M16 / Mo, expect16=8.0, passed=bool(abs(Mo / 0.71 - 1) < 0.03 and abs(M16 / Mo / 8 - 1) < 0.03))
ck["all"] = all(v["passed"] for v in ck.values()); s = json.dumps(ck, indent=1, default=float, sort_keys=True); print(s); open(os.path.join(HERE, f"df3g_controls{TAG}.json"), "w").write(s + "\n")
