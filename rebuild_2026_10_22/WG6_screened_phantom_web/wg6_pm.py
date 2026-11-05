#!/usr/bin/env python3
"""WG6 engine (FROZEN_CRITERIA.md, 1a7c1cdde9): WG4's patched copy of WG2's engine (a0 tracking rho_DE, B2D; read only) with a NEW,
by-hand Yukawa screening of the phantom only: phi_k = phi_N,k + phi_ph,k k^2 / (k^2 + mu^2). Rule names R1Y<mu>, mu in 1/Mpc.
Usage: python3 wg6_pm.py run RULE A0RULE BG AS N NSTEP ZON FOOT   (writes runs/<tag>.json here)
       python3 wg6_pm.py checks                                  (WG2's K1, K2 and K10; runs/checks.json)
       WG2_MUTATE=1 halves the Poisson factor in the imported engine (K1 must FAIL).
kappa = 1/2 FITTED; the screening term is not from any action on record; not theory closed."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "WG4_a0_tracks_de_web")); import wg4_pm; B = wg4_pm.B   # read only
import numpy as np
B.RUNS = os.path.join(HERE, "runs")
_base_potential = B.potential_k

def potential_k(mesh, delta, a, rule, a0rule, foot, E, ocl, diag=None, mu=None):
    if not rule.startswith("R1Y"):
        return _base_potential(mesh, delta, a, rule, a0rule, foot, E, ocl, diag=diag)
    mu_h = (float(rule[3:]) if mu is None else mu) / B.H                  # 1/Mpc -> h/Mpc (mesh units)
    phN = _base_potential(mesh, delta, a, "R0", a0rule, foot, E, ocl)
    ph1 = _base_potential(mesh, delta, a, "R1", a0rule, foot, E, ocl, diag=diag)
    k2 = mesh.kk ** 2
    return phN + (ph1 - phN) * (k2 / (k2 + mu_h ** 2))

B.potential_k = potential_k

def checks():
    out = dict(B.checks())
    rng = np.random.default_rng(6); M = 32; mesh = B.Mesh(M); E, ocl = B.background("B2D")
    delta = (0.3 * rng.standard_normal((M,) * 3)).astype(np.float32); a = 0.5
    r1 = _base_potential(mesh, delta, a, "R1", "DE", "canonical", E, ocl); r0 = _base_potential(mesh, delta, a, "R0", "DE", "canonical", E, ocl)
    lo = potential_k(mesh, delta, a, "R1Y", "DE", "canonical", E, ocl, mu=1e-12); hi = potential_k(mesh, delta, a, "R1Y", "DE", "canonical", E, ocl, mu=1e6)
    ny = np.zeros(lo.shape, bool); ny[M // 2, :, :] = True; ny[:, M // 2, :] = True; ny[:, :, -1] = True
    ea = float(np.max(np.abs(lo - r1)[~ny]) / np.max(np.abs(r1))); eb = float(np.max(np.abs(hi - r0)[~ny]) / np.max(np.abs(r0)))
    out["K10"] = dict(mu0_vs_R1=ea, muinf_vs_R0=eb, pass_=bool(ea < 1e-6 and eb < 1e-6))
    print(f"K10 screening: mu 1e-12 vs R1 {ea:.2e}; mu 1e6 vs R0 {eb:.2e} -> {'PASS' if out['K10']['pass_'] else 'FAIL'}")
    os.makedirs(B.RUNS, exist_ok=True); json.dump(out, open(os.path.join(B.RUNS, f"checks{B.SUF}.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    if sys.argv[1] == "checks":
        checks()
    else:
        _, _, rule, a0r, bg, As, N, ns, zon, foot = sys.argv
        B.run(rule, a0r, bg, float(As), int(N), int(ns), float(zon), foot)
