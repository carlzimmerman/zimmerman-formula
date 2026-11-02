#!/usr/bin/env python3
"""UX5 checks Q1-Q5 + nu = 1 MUTATE. python3 ux5_checks.py [--mutate]; writes ux5_checks[_MUTATE].out/.json. kappa = 1/2 FITTED; not theory closed."""
import json, sys, time, math
from ux5_core import *
MUT = "--mutate" in sys.argv; OUT = []; RES = {}
def P(s): print(s, flush=True); OUT.append(s)
a0 = A0["canonical"]; g, Mu = grid(a0); LU = Lapl(g); fail = 0
conv = a0 / (2 * math.pi * PS.G_SI) / ns["SIGU"]
def field(Phi, R, Z):
    dr, dt = g.grad_cells(Phi); dz = np.cos(g.t2d) * dr - np.sin(g.t2d) * dt; dR = np.sin(g.t2d) * dr + np.cos(g.t2d) * dt; return g.interp_cells(dR, R, Z), g.interp_cells(dz, R, Z)
M = 6e10 / Mu
# Q1 Plummer, off-plane point at each radius
a = 3.0; rho1 = g.rho_axisym(lambda R, z: (3 * M / (4 * math.pi * a ** 3)) * (1 + (R * R + z * z) / a ** 2) ** -2.5, nq=4); PN = LU.newton(rho1); PQ = LU.qumond(PN, MUT); PA, _, _ = PS.Problem(g, rho1, 2 * float(np.sum(rho1 * g.vol)), 0.0, Lam=0.0).solve_aqual()
r = np.geomspace(a, 30 * a, 12); th = math.radians(60); R_, Z_ = r * math.sin(th), r * math.cos(th); gN = M * r / (r * r + a * a) ** 1.5; ex = nu(gN) * gN
for nm, Ph in (("Q", PQ), ("A", PA)):
    fR, fz = field(Ph, R_, Z_); e = float(np.max(np.abs(np.hypot(fR, fz) / ex - 1))); RES["Q1_" + nm] = e; ok = e <= 0.01; fail += not ok; P(f"Q1 Plummer form {nm}: max |g/g_exact - 1| {e:.4f} over 1-30 a: {'PASS' if ok else 'FAIL'}")
# Q2 Kuzmin, thin sheet of exp thickness eps, exact off plane
A = 3.0; eps = 0.02
rho2 = g.rho_axisym(lambda R, z: (M * A / (2 * math.pi * (R * R + A * A) ** 1.5)) * np.exp(-np.abs(z) / eps) / (2 * eps), nq=4); PN = LU.newton(rho2); PQ = LU.qumond(PN, MUT); PA, _, _ = PS.Problem(g, rho2, 2 * float(np.sum(rho2 * g.vol)), 0.0, Lam=0.0).solve_aqual()
Rq = np.array([4., 6., 8., 10., 12.]); Zq = np.full(5, 1.1); dd = Rq * Rq + (Zq + A) ** 2; gNk = M / dd; ezfrac = (Zq + A) / np.sqrt(dd); ez = nu(gNk) * gNk * ezfrac
fRN, fzN = field(PN, Rq, Zq); eN = float(np.max(np.abs(fzN / (gNk * ezfrac) - 1))); RES["Q2_N"] = eN; P(f"Q2 Kuzmin Newton K(1.1) max rel err {eN:.4f} (context)")
for nm, Ph in (("Q", PQ), ("A", PA)):
    fR, fz = field(Ph, Rq, Zq); e = float(np.max(np.abs(fz / ez - 1))); RES["Q2_" + nm] = e; ok = e <= 0.02; fail += not ok; P(f"Q2 Kuzmin form {nm}: K(1.1), R 4-12: max rel err {e:.4f}; ratios {np.round(fz / ez, 4).tolist()}: {'PASS' if ok else 'FAIL'}")
# Q3, Q4 against LW1
if not MUT:
    rows = [json.loads(l) for l in open(os.path.join(RB, "LW1_law_scorecard", "cache_mw", "canonical_1.0.jsonl"))]; m = [d for d in rows if d.get("mcm")][0]
    o = solve(ns["rho_mcm"], a0, g, Mu, LU, "QRA"); P(f"Q4 Newton McMillan {o['N']['vc']:.3f} {o['N']['K0']:.3f} (177.092, 61.889): {'PASS' if abs(o['N']['vc'] - 177.092) < 1e-3 and abs(o['N']['K0'] - 61.889) < 1e-3 else 'FAIL'}")
    for f_ in ("A", "R"): e = max(abs(o[f_][a] / m[f_][b] - 1) for a, b in (("vc", "vc_R0"), ("K0", "K_R0"), ("cK", "chi2_Kz"))); RES["Q3_" + f_] = e; P(f"Q3 McMillan form {f_} vs LW1 max rel {e:.1e}: {'PASS' if e <= 1e-6 else 'FAIL'}"); fail += e > 1e-6
    P(f"McMillan: A vc {o['A']['vc']:.2f} K {o['A']['K0']:.2f} h {o['A']['h']:.2f}; Q vc {o['Q']['vc']:.2f} K {o['Q']['K0']:.2f} h {o['Q']['h']:.2f}; R vc {o['R']['vc']:.2f} K {o['R']['K0']:.2f}"); RES["mcm"] = o
    t = time.time(); solve(ns["rho_mcm"], a0, g, Mu, LU, "QR"); t1 = time.time() - t; t = time.time(); solve(ns["rho_mcm"], a0, g, Mu, LU, "A"); P(f"timing QR {t1:.2f}s A {time.time() - t:.2f}s")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(f"ux5_checks{sfx}.out", "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(f"ux5_checks{sfx}.json", "w"), indent=1)
