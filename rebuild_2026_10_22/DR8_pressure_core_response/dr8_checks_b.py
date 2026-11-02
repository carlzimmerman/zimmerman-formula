#!/usr/bin/env python3
"""DR8 part B checks K8, K9, K10, K12, K5 (FROZEN_CRITERIA.md). kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, shutil, sys, tempfile
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dr8_ic as IC, dr8_action as AC, dr8_live as DL, dr8_rule as RU
L = DL.L; G = IC.G; OUT = []; ok = True; T = os.path.join(HERE, "runs", "_checks"); os.makedirs(T, exist_ok=True)
def P(s): print(s, flush=True); OUT.append(s)
# K5 Hernquist
a, M = 1.0, 1.0; Mo = IC.Model(lambda r: M / (2 * np.pi) * a / (r * (r + a) ** 3), lambda r, m: 1.0, 1e-4, 1e4)
def fH(E):
    q = np.sqrt(E * a / (G * M)); return M / (8 * np.sqrt(2) * np.pi ** 3 * a ** 3 * (G * M / a) ** 1.5) / (1 - q * q) ** 2.5 * (3 * np.arcsin(q) + q * np.sqrt(1 - q * q) * (1 - 2 * q * q) * (8 * q ** 4 - 8 * q * q - 3))
e = Mo.E + G * M / 1e4; s = (e / (G * M / a) > 1e-3) & (e / (G * M / a) < 0.99); k5 = float(np.abs(Mo.f[s] / fH(e[s]) - 1).max()); g = k5 <= 0.01; ok &= g; P(f"K5 Eddington vs Hernquist closed form, E/Psi0 1e-3 to 0.99: {k5:.1e}: {'PASS' if g else 'FAIL'}")
J = json.load(open(os.path.join(HERE, "dr8_precheck.json")))
for k in ("core_0.1", "nfw_0.1"): g = J[k]["N_neg"] == 0 and J[k]["rho_err_max"] <= 0.01 and abs(J[k]["virial"] - 1) <= 0.03; ok &= g; P(f"K5/K6 {k}: f < 0 at {J[k]['N_neg']} energies, rho recovered {J[k]['rho_err_max']:.1e}, analytic-grid 2T/W from f consistent {J[k]['virial']:.4f}; N(<r) sampled {J[k]['N_meas']} vs {J[k]['N_an']}: {'PASS' if g else 'FAIL'}")
# K8 zero-mass disc path vs plain kernel
c = ["--kind", "core", "--seed", "11", "--N", "3000", "--T", "1", "--md-mult", "0", "--centre", "com", "--max-steps", "25"]; d1, d2 = os.path.join(T, "k8a"), os.path.join(T, "k8b"); [shutil.rmtree(d, ignore_errors=True) for d in (d1, d2)]; DL.main(c + ["--work", d1]); DL.main(c + ["--work", d2, "--zero-through"]); A, B = np.load(d1 + "/end.npz"), np.load(d2 + "/end.npz"); k8 = max(float(np.abs(A["x"] - B["x"]).max() / np.abs(A["x"]).max()), float(np.abs(A["v"] - B["v"]).max() / np.abs(A["v"]).max())); g = k8 <= 1e-12; ok &= g; P(f"K8 zero-mass disc path vs kernel, 25 steps: {k8:.1e}: {'PASS' if g else 'FAIL'}")
# K9 disc force
rng = np.random.default_rng(1); dx = rng.normal(size=(1000, 3)) * 0.01; u = np.array([0, 0, 1.0]); h = 1e-6; Md, A_, B_ = 6e10, 3e-3, 6e-4; num = np.stack([-(L.disc_pot(dx + h * np.eye(3)[k], Md, A_, B_, u) - L.disc_pot(dx - h * np.eye(3)[k], Md, A_, B_, u)) / (2 * h) for k in range(3)], axis=1); an = L.disc_acc(dx, Md, A_, B_, u); k9 = float(np.max(np.linalg.norm(an - num, axis=1) / np.linalg.norm(an, axis=1))); g = k9 <= 1e-6; ok &= g; P(f"K9 disc force vs potential: {k9:.1e}: {'PASS' if g else 'FAIL'}")
# K10 preemption
c = ["--kind", "core", "--seed", "12", "--N", "3000", "--T", "1", "--md-mult", "1", "--centre", "com", "--max-steps", "40"]; d1, d2 = os.path.join(T, "k10a"), os.path.join(T, "k10b"); [shutil.rmtree(d, ignore_errors=True) for d in (d1, d2)]; DL.main(c + ["--work", d1]); r = DL.main(c + ["--work", d2, "--term-at", "20"]); r2 = DL.main(c + ["--work", d2, "--resume"]); A, B = np.load(d1 + "/end.npz"), np.load(d2 + "/end.npz"); k10 = max(float(np.abs(A["x"] - B["x"]).max() / np.abs(A["x"]).max()), float(np.abs(A["v"] - B["v"]).max() / np.abs(A["v"]).max())); g = k10 <= 1e-12 and r == 75; ok &= g; P(f"K10 SIGTERM + resume vs uninterrupted, exit {r}: {k10:.1e}: {'PASS' if g else 'FAIL'}")
# K12 action solver: null, then Young's slope
S = IC.setup(); x, v, m, Ms, Mod = IC.build("core", S, 30000, 5); rg = np.geomspace(1e-4 * S["r0"], Mod.r[-1] * 3, 2500); Mi = np.interp(np.log(rg), np.log(Mod.r), Mod.M); Mf, ch, J_, L_ = AC.respond(x, v, rg, Mi, 0 * rg, 1.0, m, passes=4); rr = np.array([0.25, 0.5, 1, 2, 4]) * S["r0"]; q = np.interp(rr, rg, Mf) / np.interp(rr, rg, Mi); e0 = float(np.abs(q - 1).max()); g = e0 <= 0.03; ok &= g; P(f"K12a action null, M_b 0, Q at r/r0 0.25-4: {np.round(q,3).tolist()}, max |Q-1| {e0:.3f} (N 30000, Poisson at 0.25 r0 about 0.09 of orbit-averaged sampling): {'PASS' if g else 'FAIL'}")
# Young: point mass in a harmonic core. The cusp lives inside G M_p / sigma^2, not inside r_h: at 0.1 M(<r0) that is well above the fit range, and f is f(Psi0) there, so slope and coefficient are both known
r0 = S["r0"]; Mcore = float(np.interp(math.log(r0), np.log(Mod.r), Mod.M)); u3 = float(np.interp(math.log(0.5 * r0), np.log(Mod.r), Mod.M)) / Mod.Mtot; xx, vv = Mod.sample(60000, 7, ulim=u3); rs = np.linalg.norm(xx, axis=1); Ms2 = u3 * Mod.Mtot / 60000; Pi = AC.Pot(rg, Mi); LL = np.linalg.norm(np.cross(xx, vv), axis=1); EE = Pi.phi(rs) + 0.5 * (vv * vv).sum(1); JJ = Pi.Jr(EE, LL); f0 = float(Mod.f_at(np.array([Mod.pa[-1] * 0.9999]))[0]); C = Mcore / float(RU.BS(np.asarray(1.0))); ra = np.geomspace(1e-4 * r0, r0, 3000); Mi_ = np.interp(np.log(ra), np.log(Mod.r), Mod.M)
for fr, a1, a2, gate in ((0.1, 0.003, 0.03, True), (1e-3, 0.002, 0.012, False)):
    Mp = fr * Mcore; Pf = AC.Pot(rg, Mi + Mp); Ef = AC.solve_E(Pf, JJ, LL); occ = AC.occupancy(Pf, Ef, LL, rg) * Ms2; s = (rg > a1 * r0) & (rg < a2 * r0); sl = np.polyfit(np.log(rg[s]), np.log(occ[s]), 1)[0] - 3; rp = 0.008 * r0; an = (4 * np.pi) ** 2 * f0 * (2 * 2 ** 0.5 / 3) * (G * Mp) ** 1.5 * (2 / 3) * rp ** 1.5; co = float(np.interp(rp, rg, occ) / an); rinf = G * Mp / (float(Mod.Psi[0]) / 3)
    Rr = RU.rule(ra, Mp + 0 * ra, Mi_, 0.0, "RULE", r0=r0, C=C); Rb = RU.rule(ra, Mp + 0 * ra, Mi_, 0.0, "BLUM0", r0=r0, C=C); s_ = (ra > a1 * r0) & (ra < a2 * r0); sR = np.polyfit(np.log(ra[s_]), np.log(Rr[0][s_]), 1)[0] - 3; sB = np.polyfit(np.log(ra[s_]), np.log(Rb[0][s_]), 1)[0] - 3; rt = float(np.interp(rp, ra, Rr[0]) / np.interp(rp, rg, occ)); bt = float(np.interp(rp, ra, Rb[0]) / np.interp(rp, rg, occ))
    P(f"M_p {fr:g} M(<r0), G M_p/sigma^2 about {rinf/r0:.3f} r0: rho slope at r/r0 {a1}-{a2}: exact solver {sl:.3f}, RULE {sR:.3f}, Blumenthal F = 0 {sB:.3f}; M(<0.008 r0) over the exact: RULE {rt:.3f}, Blumenthal {bt:.2f}; solver over Young's analytic coefficient {co:.3f}")
    if gate: g = abs(sl + 1.5) <= 0.15; ok &= g; P(f"K12b Young's slope -1.5 +- 0.15: {'PASS' if g else 'FAIL'}")
open(os.path.join(HERE, "dr8_checks_b.out"), "w").write("\n".join(OUT) + f"\nALL {'PASS' if ok else 'FAIL'}\n"); P(f"ALL {'PASS' if ok else 'FAIL'}"); shutil.rmtree(T, ignore_errors=True)
