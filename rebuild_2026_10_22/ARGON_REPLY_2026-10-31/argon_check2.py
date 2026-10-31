#!/usr/bin/env python3
"""Recomputes the numbers in Argon's 10-31 re-send: mode cut-offs, the unresolved P(k) integrals, like-for-like concentrations, the soliton profile against the smooth core, and the baryon retention arithmetic. Reads no new data. kappa = 1/2 FITTED; not theory closed."""
import importlib.util, json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "X48_native_cf_zoom")); s = importlib.util.spec_from_file_location("x48_zoom", os.path.join(RB, "X48_native_cf_zoom", "x48_zoom.py")); X = importlib.util.module_from_spec(s); s.loader.exec_module(X); C = X.cosmology(); OUT = []
def P(t): print(t, flush=True); OUT.append(t)
K, PK = C["K"], C["PK"]; rho = C["rhom"]; h = C["h"]; zi = 40.0; G = 4.30091e-9
Di = float(np.interp(zi, C["ZG"], C["DG"])); ai = 1 / (1 + zi); Hi = X.Hz(C, zi); Om_i = C["Om"] * (1 + zi) ** 3 / (C["Om"] * (1 + zi) ** 3 + C["OL"]); fi = Om_i ** 0.55
def qM(M): return (3 * (M / 2) / (4 * math.pi * rho)) ** (1 / 3)
def kN(M, ng=64): return math.pi * ng / (4 * qM(M))
def I0(k1, k2):
    m = (K >= k1) & (K <= k2); return float(np.trapz(PK[m] / (2 * math.pi ** 2), K[m]))
def I2(k1, k2):
    m = (K >= k1) & (K <= k2); return float(np.trapz(PK[m] * K[m] ** 2 / (2 * math.pi ** 2), K[m]))
P("1. Mode cut-offs and unresolved integrals; Argon's text gives k_Nyq 65, 14, 6.5, 3.0 h/Mpc at 1e10, 1e12, 1e13, 1e14"); ktop = kN(1e10)
A_K = {1e10: 65, 1e12: 14, 1e13: 6.5, 1e14: 3.0}
for M in (1e10, 1e11, 1e12, 1e13, 1e14, 1e15):
    k = kN(M); Mg = 2 * 0 + rho * (4 * qM(M) / 64) ** 3; I = I0(k, ktop); sv_i = ai * Hi * fi * Di * math.sqrt(I); zf, Df = X.lacey_cole_zf(C, M); af = 1 / (1 + zf); Hf = X.Hz(C, zf); Om_f = C["Om"] * (1 + zf) ** 3 / (C["Om"] * (1 + zf) ** 3 + C["OL"]); ff = Om_f ** 0.55; sv_f = af * Hf * ff * Df * math.sqrt(I); rf = (3 * (M / 2) / (4 * math.pi * 18 * math.pi ** 2 * rho * (1 + zf) ** 3)) ** (1 / 3); Vv = math.sqrt(G * (M / 2) / rf); sd = Df * math.sqrt(I2(k, ktop)); P(f"  M {M:.0e}: q_M {qM(M):.3f} Mpc, k_Nyq(ng 64) {k:.2f}/Mpc = {k / h:.2f} h/Mpc (Argon {A_K.get(M, '-')}), particle mass {Mg:.2e}; missing band to {ktop:.0f}/Mpc: linear velocity rms at z_i {sv_i:.2f} km/s, at z_f {sv_f:.1f} km/s, V_vir(z_f) {Vv:.0f} km/s, ratio at z_f {sv_f / Vv:.3f}; density rms at z_f {sd:.3f}")
P(f"  P(k) table ends at {K[-1]:.0f}/Mpc, so the top of the band for 1e10 runs out at the table's end")
P("2. Like for like, ng 48 then ng 64 (from X48's and CE1's committed outputs)")
A = [l for l in open(os.path.join(RB, "X48_native_cf_zoom", "x48_grade_A4.out")) if l.startswith("M 1e")]
for l in A: P("  r_-2 and NFW-fit: " + l.strip()[:110])
J = json.load(open(os.path.join(RB, "CE1_converged_eta_grade", "ce1_a4_results.json"))); E = json.load(open(os.path.join(RB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]
P("  eta_conv: ng 64 " + ", ".join(f"{J['eta'][str(e)]['med']:.2f}" for e in (12, 13, 14)) + "; ng 48 cluster masses " + ", ".join(f"{E[str(e)]['med']:.2f}" for e in (13, 14)) + " (1e12 25.94 is ng 64 in both)")
Z = json.load(open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_shapes.json"))); XG = np.array(Z["x"]); mu = lambda y: np.log1p(y) - y / (1 + y)
from scipy.optimize import minimize_scalar
k_ = (XG >= 0.05) & (XG <= 1)
for M in ("1e12", "1e13", "1e14"):
    ln = np.array(Z[M]["0.00"]["lnm"]); c = minimize_scalar(lambda c_: float(np.sum((np.log(mu(c_ * XG[k_]) / mu(c_)) - ln[k_]) ** 2)), bounds=(1, 40), method="bounded").x; a_ = (XG >= 1.0) & (XG <= 1.8); sl = 3 - float(np.polyfit(np.log(XG[a_]), ln[a_], 1)[0]); P(f"  ZN1 z = 0, M {M}: c200 {c:.2f}, density slope over 1-1.8 R200 {sl:.2f}, x_edge {Z[M]['0.00']['x_edge']:.2f}, M200/M nominal {np.median([q['M_over_nom'] for q in Z[M]['0.00']['seeds']]):.3f}")
P("3. Soliton (Schroedinger-Poisson ground state) against the smooth core (1 + x^2)^(-3/2)")
def shoot(E0):
    def f(r, y): psi, dpsi, V, dV = y; return [dpsi, 2 * (V - E0) * psi - (2 / r) * dpsi, dV, psi ** 2 - (2 / r) * dV]
    ev = lambda r, y: y[0]; ev.terminal = True; ev.direction = -1; ev2 = lambda r, y: y[1]; ev2.terminal = True; ev2.direction = 1; r0 = 1e-4
    return solve_ivp(f, (r0, 40.0), [1.0, -(2 * E0 / 3) * r0, r0 ** 2 / 6, r0 / 3], events=[ev, ev2], rtol=1e-11, atol=1e-13, max_step=0.02)
lo, hi = 0.1, 2.0
for _ in range(80):
    mid = 0.5 * (lo + hi); s_ = shoot(mid)
    if len(s_.t_events[0]) > 0: hi = mid
    else: lo = mid
s_ = shoot(lo); r = s_.t; psi = s_.y[0]; d = psi ** 2; rmin = r[np.argmin(d)]; m_ = r <= rmin * 0.98; r = r[m_]; d = d[m_]; rh = float(np.interp(0.5, d[::-1], r[::-1])); x = r / rh; P(f"  ground state eigenvalue {lo:.5f}; half-density radius {rh:.4f}; check against the known fit (1 + 0.091 (r/r_c)^2)^-8: max |ln d - ln form| over d above 1e-3: {np.max(np.abs(np.log(d[d > 1e-3]) - np.log((1 + 0.091 * x[d > 1e-3] ** 2) ** -8))):.3f}")
sm = lambda a: (1 + (x * a) ** 2) ** -1.5; a_h = math.sqrt(2 ** (2 / 3) - 1); P(f"  smooth core with the same half-density radius: ln(soliton/core) at x = 1, 2, 3, 4: " + ", ".join(f"{float(np.interp(v, x, np.log(np.maximum(d, 1e-300)) - np.log(sm(a_h)))):+.2f}" for v in (1, 2, 3, 4)) + f"; soliton log slope at x = 2, 3: {float(np.interp(2, x, np.gradient(np.log(np.maximum(d, 1e-300)), np.log(x)))):.2f}, {float(np.interp(3, x, np.gradient(np.log(np.maximum(d, 1e-300)), np.log(x)))):.2f}; smooth core's limit -3")
P("  so the gradient-plus-gravity minimum at fixed mass is the soliton, not (1 + x^2)^(-3/2). With a fixed oscillation frequency M_c r_c is constant, so S = rho_0 r_c goes as r_c^-3 and rises as the core shrinks")
P("4. Baryon retention at L*: M_b/M200 at lg M_b 10.78 with EM1's relation")
lm2 = 11.18 + 0.90 * 0.78; fc = 0.84055; rr = 10 ** (10.78 - lm2); P(f"  lg M200 {lm2:.3f} (Argon 11.94); M_b/M200 {rr:.4f}. EM1's M200 is the cold mass under FC1, so retention = (M_b/M200) / (Omega_b/Omega_c) = {rr * 5.27:.3f}; Argon's 0.498 divides by 0.1595 against the cold mass")
open(os.path.join(HERE, "argon_check2.out"), "w").write("\n".join(OUT) + "\n")
