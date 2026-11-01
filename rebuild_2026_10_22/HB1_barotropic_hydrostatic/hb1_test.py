#!/usr/bin/env python3
"""HB1 solver checks K2-K6 on test profiles, standalone, no grader. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hb1_core as H
OUT = []; R = {}
def P(s): print(s, flush=True); OUT.append(s)
ok = True
def chk(k, v, line): 
    global ok
    p = v <= line; ok &= p; R[k] = v; P(f"{k}: {v:.2e} (line {line:g}) {'PASS' if p else 'FAIL'}")
BS = H.BS; X = np.geomspace(1e-4, 1e4, 1500)
for a in (3.0, 30.0, 300.0, 3000.0):
    x = X[X <= a]; x = np.r_[x, a]; m0 = BS(x); E = H.eos("E1"); o, Hc, st, ns, Ho = H.solve_scaled(x, 0 * x, a, float(BS(np.asarray(a))), E); i = m0 > 1e-8
    chk(f"K2 Form B null, x_e {a:g}, grid", float(np.max(np.abs(o[i] / m0[i] - 1))), 1e-4); P(f"   H_c {Hc:.9f}, H(edge) {Ho[-1]:.6f} vs asinh(a)/a {math.asinh(a) / a:.6f}")
# truncated edge through the wrapper
r = np.geomspace(1e-3, 50.0, 600); r0 = 0.4; re = 20.0; M0 = 7.0 * BS(np.minimum(r, re) / r0); Mf = H.contract_hb(r, 0 * r, M0, "E1")[0]; i = M0 > 1e-6 * M0[-1]; chk("K2 null through wrapper, truncated edge", float(np.max(np.abs(Mf[i] / M0[i] - 1))), 1e-4)
rr, C, n = H.infer_r0(r, M0); chk("K7 r0 inferred", abs(rr / r0 - 1), 1e-5)
# a test disc-like Mb
Mb = 0.3 * M0[-1] * (1 - 0.1 / np.sqrt(r * r + 0.01)); Mb = np.maximum(Mb, 0)
for f in ("E1", "A"):
    a_ = H.contract_hb(r, Mb, M0, f)[0]; H.SUB[0] = 4; b_ = H.contract_hb(r, Mb, M0, f)[0]; H.SUB[0] = 2; chk(f"K3 substeps x 2, {f}, test", float(np.max(np.abs(b_ / a_ - 1))), 1e-5)
# Mb -> 0
e_ = []
for eps in (1e-2, 1e-4, 1e-6):
    m = H.contract_hb(r, Mb * eps, M0, "E1")[0]; e_.append(float(np.max(np.abs(m[i] / M0[i] - 1))))
P(f"K4 M_b x 1e-2, 1e-4, 1e-6: max |dM/M| {e_}"); R["K4_series"] = e_; chk("K4 linear scaling 1e-4 to 1e-6, off 1 (A2: the 1e-2 leg is past a fold, reported)", abs(e_[1] / e_[2] / 100 - 1), 2.0)
# residuals of a finished solution
x = r / rr; xe = float(np.max(x[M0 < M0[-1]])); mb = Mb / C; a = re / r0; g = np.r_[x[x < a], a]; mbg = np.interp(np.log(g), np.log(x), mb); E = H.eos("E1"); o, Hc, st, ns, Ho = H.solve_scaled(g, mbg, a, float(BS(np.asarray(a))), E, nsub=8); lg = np.log(g)
dH = np.gradient(Ho, lg); res = dH + (o + mbg) / (4 * g); ii = (g > 2e-2) & (g < a * 0.9); rhon = np.interp(Ho, np.arange(H.NT) * H.DH, H.TAB_B) * (Ho < 1) + (1 + 9 * (Ho - 1)) * (Ho >= 1); P4 = np.gradient(o, lg) - 4 * g ** 3 * rhon
chk("K5 hydrostatic residual, |r| / force", float(np.median(np.abs(res[ii]) / ((o[ii] + mbg[ii]) / (4 * g[ii])))), 1e-4); chk("K5 Poisson residual, median", float(np.median(np.abs(P4[ii]) / np.maximum(4 * g[ii] ** 3 * rhon[ii], 1e-30))), 1e-3); chk("K5 mass held", abs(o[-1] / float(BS(np.asarray(a))) - 1), 1e-7)
# K6 Form A closed form: rho^ = H/q, k^2 = 1/q, sinc radius pi sqrt(q)
q = 0.7; E = H.eos("A", q); g = np.geomspace(1e-3, 10.0, 2000); rs = math.pi * math.sqrt(q); Hc0 = 0.5; m_ = H.mass_at(g, 0 * g, 9.0, Hc0, E, 4); an = 4 * (Hc0 / q) * q ** 1.5 * math.pi; chk("K6 sinc total mass vs closed form 4 pi q^0.5 H_c", abs(m_ / an - 1), 1e-4)
Ek = H.eos("A", q); o, Hc, st, ns, Ho = H.solve_scaled(g, 0 * g, 9.0, m_, Ek, 4); j = (g < rs * 0.9) & (g > 0.01); s = Hc0 * np.sin(g[j] / math.sqrt(q)) / (g[j] / math.sqrt(q)); chk("K6 sinc profile H(x)", float(np.max(np.abs(Ho[j] / s - 1))), 1e-4)
# separate solver: point mass-like Mb in gamma = 2, solve_ivp
b0 = 0.8; mbf = lambda x_: b0 * x_ ** 3 / (x_ ** 3 + 0.1); gg = np.geomspace(1e-3, 3.0, 800); mbg = mbf(gg); mC = H.mass_at(gg, mbg, 3.0, 1.0, E, 8)
def rhs(t, y): return [-(y[1] + mbf(t)) / (4 * t ** 2), 4 * t ** 2 * max(y[0], 0) / q]
s_ = solve_ivp(rhs, (1e-5, 3.0), [1.0, 4 / 3 * 1e-15 / q], rtol=1e-10, atol=1e-13, method="LSODA"); chk("K6 solve_ivp cross-check, gamma = 2 with a compact M_b", abs(mC / s_.y[1, -1] - 1), 1e-3)
# E tables
chk("K6 E2 table agrees with E1 at H <= 1", float(np.max(np.abs(np.interp(np.linspace(0.05, 1, 500), np.arange(H.N2) * H.D2, H.TAB_E2) / np.interp(np.linspace(0.05, 1, 500), np.arange(H.NT) * H.DH, H.TAB_B) - 1))), 1e-3)
# branch: wide scan for root count on the Phi_b = 0 null and with Mb, and continuation
for lab, mbx in (("null", 0 * g), ("test Mb", 0.3 * BS(np.asarray(30.0)) * (1 - 0.3 / np.sqrt(g * g + 0.09)))):
    g2 = np.geomspace(1e-3, 30.0, 800); mbz = np.interp(np.log(g2), np.log(g), mbx) if lab == "null" else 0.3 * float(BS(np.asarray(30.0))) * (1 - 0.3 / np.sqrt(g2 * g2 + 0.09)); mt = float(BS(np.asarray(30.0))); E = H.eos("E1"); Hs = np.geomspace(1e-3, 300.0, 200); f = np.array([H.mass_at(g2, mbz, 30.0, h, E) / mt - 1 for h in Hs]); nr = int(np.sum(f[1:] * f[:-1] < 0)); roots = Hs[:-1][f[1:] * f[:-1] < 0]; R[f"roots_{lab}"] = roots.tolist(); P(f"wide scan, {lab}, a 30: {nr} roots near H_c {np.round(roots, 3).tolist()}; f at low H_c end {f[0]:+.3f}")
    d = (H.mass_at(g2, mbz, 30.0, 1.002, E) - H.mass_at(g2, mbz, 30.0, 0.998, E)) / 0.004 / mt; R[f"dmdHc_{lab}"] = d; P(f"   dm(x_e)/dH_c at H_c 1, over m_t: {d:+.3f}")
g2 = np.geomspace(1e-3, 30.0, 800); mbt = 0.3 * float(BS(np.asarray(30.0))) * (1 - 0.3 / np.sqrt(g2 * g2 + 0.09)); mt = float(BS(np.asarray(30.0))); last = 1.0; Hcs = []
for lam in np.linspace(0, 1, 21):
    E = H.eos("E1"); Hc = H.solve_scaled(g2, lam * mbt, 30.0, mt, E)[1]; Hcs.append(Hc)
jump = float(np.max(np.abs(np.diff(np.log(Hcs))))); R["continuation_max_step"] = jump; P(f"continuation in Phi_b, 21 steps: H_c {Hcs[0]:.4f} to {Hcs[-1]:.4f}, largest step in ln H_c {jump:.3f} (branch rule root at lambda 1 {H.solve_scaled(g2, mbt, 30.0, mt, H.eos('E1'))[1]:.4f})")
# a over the range: multiple equilibria at fixed mass and edge, null only
R["roots_by_a"] = {}
g_ = H.eos("E1")
for a in (3, 10, 30, 50, 100, 300, 1000):
    gg = np.geomspace(1e-3, a, 1200); mt = float(BS(np.asarray(float(a)))); Hs = np.geomspace(.02, 50, 400); f = np.array([H.mass_at(gg, 0 * gg, float(a), h, g_) / mt - 1 for h in Hs]); rt = Hs[:-1][f[1:] * f[:-1] < 0]; d = (H.mass_at(gg, 0 * gg, float(a), 1.002, g_) - H.mass_at(gg, 0 * gg, float(a), .998, g_)) / .004 / mt; R["roots_by_a"][a] = dict(roots=rt.tolist(), dmdHc=d); P(f"null a {a}: roots near {np.round(rt, 3).tolist()}, dm(x_e)/dH_c at the core {d:+.3f}")
P("ALL PASS" if ok else "SOME FAIL"); R["ok"] = bool(ok); json.dump(R, open(os.path.join(H.HERE, "hb1_test.json"), "w"), indent=1, default=float); open(os.path.join(H.HERE, "hb1_test.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
