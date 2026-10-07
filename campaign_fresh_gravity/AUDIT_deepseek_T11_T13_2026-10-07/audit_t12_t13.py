#!/usr/bin/env python3
"""Orchestrator review of DeepSeek T12 (three-clock lambda) and T13 (phantom sound speed).  Read-only on deepseek_push.
(1) T12's lambda consistency re-run with the CFG382 target audit's ONE-definition levels (def A, same hydrostatic bias b) instead of the mixed 0.60/0.43.
(2) T13's algebra re-derived: c^2 = v^2/2 and lambda_J = sqrt(2) pi r for rho = v^2/(4 pi G r^2)."""
import math, sympy as sp
G = 6.674e-11; GYR = 3.15576e16; RHO_CRIT0 = 3 * (70e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
def lam(f, t, z):
    if f >= 1: return None
    rho = 500 * RHO_CRIT0 * (0.3 * (1 + z) ** 3 + 0.7); return -math.log(1 - f) / (t * GYR * math.sqrt(4 * math.pi * G * rho))
print("(1) T12 clocks (t_c 6.7 Gyr z 0.75, t_g 11.9 Gyr z 0.15 -- these epochs are T11's, which T11 derived FROM the same 0.43/0.60 levels)")
print(f"    T12 inputs (mixed definitions): groups 0.60 -> lam {lam(0.60, 11.9, 0.15):.4f}; clusters 0.43 -> lam {lam(0.43, 6.7, 0.75):.4f}")
for b, fg, fc in ((0.0, 0.79, 0.41), (0.1, 1.04, 0.54), (0.2, 1.35, 0.70), (0.3, 1.76, 0.91)):
    lg, lc = lam(fg, 11.9, 0.15), lam(fc, 6.7, 0.75)
    print(f"    one-definition levels at b = {b}: groups {fg} -> {('%.4f' % lg) if lg else 'UNDEFINED (f >= 1)'}; clusters {fc} -> {lc:.4f}")
r, v, Gs = sp.symbols("r v G", positive=True); rho = v ** 2 / (4 * sp.pi * Gs * r ** 2); c2 = sp.symbols("c2", positive=True)
sol = sp.solve(sp.Eq(c2 * sp.diff(rho, r), -rho * v ** 2 / r), c2)[0]
lamJ = sp.sqrt(sol) * sp.sqrt(sp.pi / (Gs * rho))
print(f"(2) T13: hydrostatic c^2 = {sol}; lambda_J/r = {sp.simplify(lamJ / r)} = {float(sp.simplify(lamJ / r)):.4f}  (singular isothermal sphere; textbook)")
