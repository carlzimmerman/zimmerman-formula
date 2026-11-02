#!/usr/bin/env python3
"""AR1 solver checks K2, K3, K4, K7 on the solver alone (FROZEN_CRITERIA.md). K2's reference is dr8_action.py, 8 seeds of 100,000 particles on DR8's own start. Each seed caches. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, pickle, sys
sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); DR8 = os.path.join(RB, "DR8_pressure_core_response"); sys.path[:0] = [HERE, DR8]; import ar1_solver as A, dr8_ic as IC, dr8_action as AC
OUT = []; ok = True; CD = os.path.join(HERE, "cache_k2"); os.makedirs(CD, exist_ok=True)
def P(s): print(s, flush=True); OUT.append(str(s))
S = IC.setup(); Rd, r0, R2, Md = S["Rd"], S["r0"], S["R2"], S["Md"]; x, v, m, Msim, Mod = IC.build("core", S, 100, 1, 0.1); RR = np.array([1, 2, 2.2, 3, 4, 6, 8, 10.0]) * Rd; RX = np.array([0.135, 0.25, 0.5, 1, 2, 4, 8]) * r0; frac = 1 - Md / Msim; FF = Md / (Msim - Md)
rg3 = np.geomspace(2e-5, R2, 1500); M3 = np.interp(np.log(rg3), np.log(Mod.r), Mod.M) * frac; Mb3 = Md * (1 - Rd / np.sqrt(rg3 ** 2 + Rd ** 2)); Qof = lambda M, g, m0, rr: np.interp(np.log(rr), np.log(g), M) / np.interp(np.log(rr), np.log(g), m0)
st = A.Start(rg3, M3); Mn = A.act_contract(rg3, Mb3, M3, FF, st=st); Qn, Qnx = Qof(Mn[0], rg3, M3, RR), Qof(Mn[0], rg3, M3, RX); P(f"new solver, DR8's start: Fm {st.Fm:.4f}, mass on f<0 {st.mneg:.1e}, last-pass change {Mn[1]:.1e}; Q(R_d) " + " ".join(f"{q:.3f}" for q in Qn))
Qs = []
for sd in range(1, 9):
    f = os.path.join(CD, f"s{sd}.pkl")
    if not os.path.exists(f):
        xx, vv, mm, Ms, Mo = IC.build("core", S, 100000, 100 + sd, 0.1); rg = np.geomspace(max(Mo.r[0], 2e-5), Mo.r[-1] * 3, 2500); Mi = np.where(rg < Mo.r[0], Mo.M[0], np.interp(np.log(rg), np.log(Mo.r), Mo.M)); Mbb = Md * (1 - Rd / np.sqrt(rg ** 2 + Rd ** 2)); Mf, ch, _, _ = AC.respond(xx, vv, rg, Mi, Mbb, frac, mm, passes=12); Mc = Mi * frac; pickle.dump((Qof(Mf, rg, Mc, RR), Qof(Mf, rg, Mc, RX), ch), open(f, "wb")); print("seed", sd, ch, flush=True)
    Qs.append(pickle.load(open(f, "rb")))
Q8 = np.median([q[0] for q in Qs], axis=0); Sc = np.std([q[0] for q in Qs], axis=0, ddof=1) / math.sqrt(len(Qs)); Q8x = np.median([q[1] for q in Qs], axis=0); P("dr8_action, 8 seeds of 1e5: Q " + " ".join(f"{q:.3f}" for q in Q8) + "; standard error " + " ".join(f"{q:.3f}" for q in Sc)); d = Qn / Q8 - 1; a = np.max(np.abs(d[[1, 3, 4]])); b = np.max(np.abs(d[[0, 5, 6, 7]])); g = a <= 0.01 and b <= 0.03; ok &= g; P(f"K2 Q_new/Q_dr8 - 1 at r/R_d {RR / Rd}: " + " ".join(f"{q:+.3f}" for q in d) + f"; 2,3,4 R_d max {a:.3f} (line 0.01), 1,6,8,10 max {b:.3f} (line 0.03): {'PASS' if g else 'FAIL'}"); P("  by r/r0: " + " ".join(f"{q:+.3f}" for q in (Qnx / Q8x - 1)))
J = json.load(open(os.path.join(DR8, "dr8_live_results.json")))["core"]["table"]; P("  live Q (DR8) " + " ".join(f"{q:.3f}" for q in J["Q"][:8]) + "; new action f (Q-1)/(Q_new-1) at 2,3,4 R_d " + " ".join(f"{(J['Q'][i] - 1) / (Qn[i] - 1):.3f}" for i in (1, 3, 4)))
# K3 identity
Bs = lambda z: 4 * (np.arcsinh(z) - z / np.sqrt(1 + z * z)); e = []; rg = np.geomspace(R2 * 1e-4, R2, 300)
for nm, M0, th in (("core", 8e11 * Bs(rg / r0), None), ("core a=4", 8e11 * Bs(rg / (R2 / 4)), None), ("core a=40", 8e11 * Bs(rg / (R2 / 40)), None), ("nfw", 8e11 * (np.log1p(rg / (R2 / 8)) - (rg / (R2 / 8)) / (1 + rg / (R2 / 8))), None), ("cluster truncated", 8e11 * Bs(np.minimum(rg, 0.3 * R2) / r0), None)):
    o = A.act_contract(rg, 0 * rg, M0, 0.0, st=A.Start(rg, M0, thin=th))[0]; e.append(float(np.max(np.abs(o / M0 - 1))))
g = max(e) <= 1e-6; ok &= g; P(f"K3 zero baryons, M_out = M0, max |d| core, a=4, a=40, NFW, truncated: {e}: {'PASS' if g else 'FAIL'}")
# K4 Kepler J_r and the point mass
Xg = np.arange(math.log(1e-4), math.log(100.0), 0.01); Gk = A.Grid(Xg, np.ones_like(Xg)); N = A.Nodes(48); Ee = np.array([-0.5, -1.0, -2.0]); LL = np.array([0.3, 0.5, 0.2]); Ja = 1 / np.sqrt(-2 * Ee) - LL; Jn = A.orbit(Gk, Ee + Gk.phi[-1] + 1 / math.exp(Xg[-1]), LL, N)[0]; k = float(np.max(np.abs(Jn / Ja - 1))); g = k <= 1e-3; ok &= g; P(f"K4a Kepler J_r: {k:.1e}: {'PASS' if g else 'FAIL'}")
Mc = 8e11 * float(Bs(1.0)); rg2 = np.geomspace(1e-4 * r0, R2, 1200); M2c = 8e11 * Bs(rg2 / r0); s = (rg2 > 0.003 * r0) & (rg2 < 0.03 * r0)
Msl = A.act_contract(rg2, 0 * rg2 + 0.1 * Mc, M2c, 0.0)[0]; sl = np.polyfit(np.log(rg2[s]), np.log(Msl[s]), 1)[0] - 3; g = abs(sl + 1.41) <= 0.05; ok &= g; P(f"K4b point mass 0.1 M(<r0), inner slope at the graded grid {sl:.3f}, DR8's exact -1.41, line 0.05: {'PASS' if g else 'FAIL'}"); Msf = A.act_contract(rg2, 0 * rg2 + 0.1 * Mc, M2c, 0.0, nE=384, nY=64, nT=128)[0]; P(f"     same, finer grid (384, 64, 128), not on the line: {np.polyfit(np.log(rg2[s]), np.log(Msf[s]), 1)[0] - 3:.3f}; Young's theoretical -1.5")
P("ALL " + ("PASS" if ok else "FAIL")); open(os.path.join(HERE, "ar1_checks.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
