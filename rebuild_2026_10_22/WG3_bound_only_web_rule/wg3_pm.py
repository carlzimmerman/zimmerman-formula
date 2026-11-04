#!/usr/bin/env python3
"""WG3 engine (FROZEN_CRITERIA.md, bb3410083d): WG2's engine (imported read only) with the record's bound-only switch.
T1 (CFG354 rule as CFG359 ran it): QUMOND's phantom density times f = clip(1/2 + (l2 - tau)/(2 eps), 0, 1), eps = 0.077,
tau = (Delta_ta - 1)/3 with the EdS Delta_ta = 9 pi^2 / 16; l1 >= l2 >= l3 the eigenvalues of t_ij = FFT^-1[k_i k_j delta_k / k^2].
T1V: T1 with f = 0 where l3 < 0. T1T0: tau = 0. Everything else is WG2's.
Usage: python3 wg3_pm.py run RULE A0RULE BG AS N NSTEP ZON FOOT   (writes runs/<tag>.json here)
       python3 wg3_pm.py checks                                  (WG2's K1, K2 on the imported engine, and K8; runs/checks.json)
       WG2_MUTATE=1 halves the Poisson factor in the imported engine (K1 must FAIL).
kappa = 1/2 FITTED; the cold sector stays retired (T1 is borrowed from it as a test, adopting nothing); not theory closed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "WG2_bare_law_web_lensing")); import wg2_pm as B   # read only
import numpy as np

B.RUNS = os.path.join(HERE, "runs")
EPS = 0.077; DTA_EDS = 9 * math.pi ** 2 / 16; TAU = {"T1": (DTA_EDS - 1) / 3, "T1V": (DTA_EDS - 1) / 3, "T1T0": 0.0}
_base_potential = B.potential_k

def eig3(t):
    """closed-form eigenvalues of symmetric 3x3 fields (t = [xx, yy, zz, xy, xz, yz]); l1 >= l2 >= l3 (copied from cfg359_pm.eig3)."""
    a11, a22, a33, a12, a13, a23 = [x.astype(np.float64) for x in t]
    p1 = a12 ** 2 + a13 ** 2 + a23 ** 2; q = (a11 + a22 + a33) / 3
    p2 = (a11 - q) ** 2 + (a22 - q) ** 2 + (a33 - q) ** 2 + 2 * p1; p = np.sqrt(p2 / 6); ps = np.where(p > 0, p, 1.0)
    b11, b22, b33 = (a11 - q) / ps, (a22 - q) / ps, (a33 - q) / ps; b12, b13, b23 = a12 / ps, a13 / ps, a23 / ps
    r = 0.5 * (b11 * (b22 * b33 - b23 ** 2) - b12 * (b12 * b33 - b23 * b13) + b13 * (b12 * b23 - b22 * b13))
    ph = np.arccos(np.clip(r, -1, 1)) / 3
    l1 = q + 2 * p * np.cos(ph); l3 = q + 2 * p * np.cos(ph + 2 * np.pi / 3); l2 = 3 * q - l1 - l3
    return l1, l2, l3

def switch(mesh, delta, rule, tau=None):
    dk = mesh.fwd(delta) * mesh.DEC
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = [mesh.inv(mesh.kvec[i] * mesh.kvec[j] * dk * mesh.ik2) for i, j in tk]
    l1, l2, l3 = eig3(t)
    tau = TAU[rule] if tau is None else tau
    f = np.clip(0.5 + (l2 - tau) / (2 * EPS), 0.0, 1.0).astype(np.float32)
    if rule == "T1V":
        f[l3 < 0] = 0.0
    return f

def potential_k(mesh, delta, a, rule, a0rule, foot, E, ocl, diag=None, tau=None):
    if rule not in TAU:
        return _base_potential(mesh, delta, a, rule, a0rule, foot, E, ocl, diag=diag)
    phN = _base_potential(mesh, delta, a, "R0", a0rule, foot, E, ocl)
    ph1 = _base_potential(mesh, delta, a, "R1", a0rule, foot, E, ocl, diag=diag)
    f = switch(mesh, delta, rule, tau)
    if diag is not None:
        rho = 1.0 + delta; diag.update(f_vol=float(f.mean()), f_mass=float((f * rho).mean() / rho.mean()))
    phant = mesh.inv((ph1 - phN) * (-mesh.kk ** 2))                   # real-space phantom density (lap phi_ph)
    return phN + mesh.fwd(phant * f) * (-mesh.ik2)                     # lap^-1 of f x phantom density

B.potential_k = potential_k                                            # WG2's run() now calls the switched potential

def checks():
    out = {}
    k12 = B.checks()                                                   # WG2's K1, K2 on the imported engine (writes runs/checks.json)
    out.update(k12)
    rng = np.random.default_rng(3); M = 32; mesh = B.Mesh(M); E, ocl = B.background("B2"); a = 0.5
    delta = (0.3 * rng.standard_normal((M,) * 3)).astype(np.float32)
    r1 = _base_potential(mesh, delta, a, "R1", "TIE", "canonical", E, ocl); r0 = _base_potential(mesh, delta, a, "R0", "TIE", "canonical", E, ocl)
    on = potential_k(mesh, delta, a, "T1", "TIE", "canonical", E, ocl, tau=-1e9); off = potential_k(mesh, delta, a, "T1", "TIE", "canonical", E, ocl, tau=1e9)
    ny = np.zeros(on.shape, bool); ny[M // 2, :, :] = True; ny[:, M // 2, :] = True; ny[:, :, -1] = True   # A1: Nyquist planes excluded
    ea_all = float(np.max(np.abs(on - r1)) / np.max(np.abs(r1)))
    ea = float(np.max(np.abs(on - r1)[~ny]) / np.max(np.abs(r1))); eb = float(np.max(np.abs(off - r0)) / np.max(np.abs(r0)))
    A = rng.standard_normal((1000, 3, 3)); A = A + A.transpose(0, 2, 1)
    l1, l2, l3 = eig3([A[:, 0, 0], A[:, 1, 1], A[:, 2, 2], A[:, 0, 1], A[:, 0, 2], A[:, 1, 2]])
    ref = np.linalg.eigvalsh(A)[:, ::-1]; ec = float(np.max(np.abs(np.stack([l1, l2, l3], 1) - ref)) / np.max(np.abs(ref)))
    out["K8"] = dict(on_vs_R1_all_modes_as_frozen=ea_all, on_vs_R1=ea, off_vs_R0=eb, eig_vs_numpy=ec, tol=[1e-6, 1e-6, 1e-5], pass_=bool(ea < 1e-6 and eb < 1e-6 and ec < 1e-5))
    print(f"K8 switch: tau -1e9 vs R1 {ea:.2e} off the Nyquist planes (all modes {ea_all:.2e}), tau +1e9 vs R0 {eb:.2e}, eig3 vs numpy {ec:.2e} -> {'PASS' if out['K8']['pass_'] else 'FAIL'}")
    os.makedirs(B.RUNS, exist_ok=True); json.dump(out, open(os.path.join(B.RUNS, f"checks{B.SUF}.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    if sys.argv[1] == "checks":
        checks()
    else:
        _, _, rule, a0r, bg, As, N, ns, zon, foot = sys.argv
        B.run(rule, a0r, bg, float(As), int(N), int(ns), float(zon), foot)
