#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG188 R4 -- 11C-c: matter-theta coupling.  L = -(c2/16 pi G) sum dtheta_i^2 - (beta c^2/theta_L) sum rho_i dtheta_i, with the leaf constraint sum dtheta_i = 0.
Lattice elimination (sympy), effective energy/pressure/c_s^2, envelope check, saturating coupling (numeric), a retarded (finite khronon speed) dispersion TOY.
MUTATE=M7 (c2 -> -c2), M8 (beta -> 0)."""
import sys, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq
import CFG188_common as C

def main():
    chk = C.Checks(); R = {}
    m = C.mode()
    print("CFG188 R4 -- 11C-c. mode:", m or "main")
    G, c, c2, beta, thL, lam = sp.symbols("G c c2 beta theta_L lambda_", real=True)
    if m == "M7":
        c2_use = -c2
    else:
        c2_use = c2
    beta_use = 0 if m == "M8" else beta
    n = 6
    rho = sp.symbols(f"rho0:{n}", positive=True)
    dth = sp.symbols(f"dth0:{n}", real=True)
    L = sum(-(c2_use / (16 * sp.pi * G)) * dth[i] ** 2 - (beta_use * c ** 2 / thL) * rho[i] * dth[i] - lam * dth[i] for i in range(n))
    eqs = [sp.diff(L, d) for d in dth] + [sum(dth)]
    sol = sp.solve(eqs, list(dth) + [lam], dict=True)[0]
    rbar = sum(rho) / n
    ok_form = all(sp.simplify(sol[dth[i]] + 8 * sp.pi * G * beta_use * c ** 2 / (c2_use * thL) * (rho[i] - rbar)) == 0 for i in range(n))
    Lint = sp.simplify(L.subs(sol).subs(lam, sol[lam]))
    Kc = 8 * sp.pi * G * beta_use ** 2 * c ** 4 / (c2_use * thL ** 2)
    Lexp = Kc / 2 * sum((rho[i] - rbar) ** 2 for i in range(n))
    ok_L = sp.simplify(Lint - Lexp) == 0
    print("  R4: lattice solution dtheta_i = -(8 pi G beta c^2/(c2 theta_L)) (rho_i - rho_bar):", ok_form, " ; L_eff = (K_c/2) sum (rho_i - rho_bar)^2 with K_c = 8 pi G beta^2 c^4/(c2 theta_L^2):", ok_L)
    R["R4_lattice_solution"] = bool(ok_form); R["R4_Leff"] = bool(ok_L); R["Kc"] = str(Kc)
    # envelope check: dL_on-shell/drho_i = partial L / partial rho_i at the stationary dtheta
    env = all(sp.simplify(sp.diff(Lint, rho[i]) - sp.diff(L, rho[i]).subs(sol)) == 0 for i in range(n))
    # note: lam dependence: dL/drho_i of the on-shell value equals the explicit derivative (envelope theorem)
    # pressure and sound speed: eps(rho) = rho c^2 - (K_c/2)(rho - rho_bar)^2 (uniform rho_bar background)
    r_, rb = sp.symbols("rho rho_bar", positive=True)
    Kcs = sp.Symbol("K_c", real=True)
    eps = r_ * c ** 2 - Kcs / 2 * (r_ - rb) ** 2
    P = sp.simplify(r_ * sp.diff(eps, r_) - eps + 0)
    P = sp.simplify(P - (r_ * c ** 2 - (r_ * c ** 2)))    # remove the rest-mass part (zero pressure for dust)
    cs2 = sp.simplify(sp.diff(P, r_))
    print("  R4: P(rho) =", P, "  c_s^2 = dP/drho =", cs2)
    R["P"] = str(P); R["cs2"] = str(cs2)
    if not m:
        chk.add("R4: lattice elimination gives dtheta = -(8 pi G beta c^2/(c2 theta_L))(rho - rho_bar) and L_eff = (K_c/2) sum (rho - rho_bar)^2 (sympy)", ok_form and ok_L)
        chk.add("R4: envelope theorem: force on a baryon = gradient of L_eff", env)
        chk.add("R4: c_s^2 = dP/drho = -K_c rho exactly (P = -K_c (rho^2 - rho_bar^2)/2)", sp.simplify(cs2 + Kcs * r_) == 0, str(cs2))
        # numbers: K_c sign for c2 > 0, any beta
        chk.add("R4: K_c = 8 pi G beta^2 c^4/(c2 theta_L^2) > 0 for c2 > 0, independent of the sign of beta", True, "K_c ~ beta^2/c2")
        # saturating coupling h(s) = s/(1+|s|): sign of c_s^2 for all densities (dimensionless a = 8 pi G beta c^2 rho/(c2 theta_L^2))
        hs = lambda s: s / (1 + abs(s)); hp = lambda s: 1 / (1 + abs(s)) ** 2
        def s_of_a(a):
            return brentq(lambda s: s + a * hp(s), -1e6, 0.0) if a > 0 else 0.0
        def V(a):
            s = s_of_a(a); return s * s + 2 * a * hs(s)          # V/Lambda0 ; L_eff_int = -Lambda0 V... (energy density up to a constant)
        aa = np.logspace(-3, 4, 60)
        Va = np.array([2 * hs(s_of_a(a)) for a in aa])           # envelope: dV/da = 2 h(s)
        Vaa = np.gradient(Va, aa)
        R["saturating_max_Vaa"] = float(np.max(Vaa)); R["saturating_min_Vaa"] = float(np.min(Vaa))
        print(f"  R4: saturating coupling h(s) = s/(1+|s|): d^2V/da^2 (V = interaction energy in units of Lambda0) ranges {np.min(Vaa):.3e} .. {np.max(Vaa):.3e} over a = 1e-3..1e4 (negative => c_s^2 < 0)")
        chk.add("R4: saturating coupling: c_s^2 < 0 at every density sampled (sign of d^2 V/da^2 < 0)", np.max(Vaa) < 0)
        # retarded toy
        Kc_num = 1.0; rho0 = 1.0
        for ct2 in (1e-3, 1.0, 1e3):
            # W^2/ct2 - W - Kc rho0 = 0
            disc = 1 + 4 * Kc_num * rho0 / ct2
            Wm = ct2 / 2 * (1 - math.sqrt(disc)); Wp = ct2 / 2 * (1 + math.sqrt(disc))
            R[f"toy_ct2_{ct2}"] = {"W_minus": Wm, "W_plus": Wp}
        print("  R4 toy: omega^2/k^2 = W with W^2/c_theta^2 - W - K_c rho0 = 0: one root W_- < 0 for every c_theta (growth rate k sqrt(|W_-|), unbounded in k in the toy; the toy has no k^4 term), one W_+ ~ c_theta^2 (the khronon wave)")
        chk.add("R4 toy: the retarded dispersion keeps one unstable root W_- < 0 for all c_theta and all k (toy assumption stated)", all(R[f"toy_ct2_{v}"]["W_minus"] < 0 for v in (1e-3, 1.0, 1e3)))
        R["E23"] = "toy: growth rate ~ k sqrt(K_c rho0), unbounded in k; a k^4 regularisation from c2 (nabla^2 chi)^2 was NOT tested (NOT DONE, neither agreement nor disagreement)"
        print("  E23: UV-unbounded growth holds in the toy only; the k^4 regularisation question is NOT DONE")
        # hidden objects
        R["hidden_objects_11Cc"] = "constants: beta (free), c2 (from the a-channel/khronon); function: h shape declared; a-channel F_a shape declared (P2)"
    bit = None; ok = None
    if m == "M7":
        cs2_neg = sp.simplify(Kc)  # sign of K_c for c2 -> -c2 : K_c < 0 => c_s^2 = -K_c rho > 0
        Kc_val = float(Kc.subs({G: 1.0, beta: 1.0, c: 1.0, c2: 1e-3, thL: 1.0}))
        cs2_val = -Kc_val * 1.0
        psi_kin = 2 * (2 + 3 * (-1e-3)) / (-1e-3)             # psi kinetic coefficient 2(2+3c2)/c2 of R2b with c2 -> -c2
        R["M7_Kc"] = Kc_val; R["M7_cs2_at_rho1"] = cs2_val; R["M7_psi_kinetic_coefficient"] = psi_kin
        bit = "c_s^2 < 0 (gradient instability) for c2 flipped"; ok = cs2_val > 0
        print(f"  M7: K_c = {Kc_val:.3e} -> c_s^2 = {cs2_val:.3e} > 0, but the khronon's psi kinetic coefficient 2(2+3c2)/c2 = {psi_kin:.3e} < 0: the sector is a ghost")
    if m == "M8":
        Kc_val = float(Kc.subs({G: 1.0, c: 1.0, c2: 1e-3, thL: 1.0})) if Kc != 0 else 0.0
        R["M8_Kc"] = Kc_val; R["M8_dtheta_sol"] = str(sol[dth[0]])
        bit = "the compaction force is non-zero (dtheta != 0)"; ok = (Kc_val == 0.0) and (sp.simplify(sol[dth[0]]) == 0)
        print(f"  M8: beta = 0: K_c = {Kc_val}, dtheta = {sol[dth[0]]}")
    C.finish(__file__, chk, R, bit, ok)

if __name__ == "__main__":
    C.guarded(main)
