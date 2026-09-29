#!/usr/bin/env python3
"""CFG122 G3.3 -- structure control: the reaction derived by virtual work from the action equals the force a_phi on the baryons to <= 1% (hostile check that reciprocity is built in).
1-D planar analogue with the gradient-regime cubic energy and two thin source plates (unit-free numbers; the check is structural):
   E[phi; z1, z2] = int_{-L}^{L} [ (2 Lam/3)|phi'|^3 + (alpha Lam/M_Pl) phi (s1 delta(z-z1) + s2 delta(z-z2)) ] dz,   phi(+-L) = 0, minimised over phi.
   EL: 2 Lam d(|phi'| phi')/dz = (alpha Lam/M_Pl) sum s_i delta(z - z_i)  => u = |phi'| phi' is piecewise constant, jumps j_i = alpha s_i/(2 M_Pl).
   Force on plate 1 from the field: F1 = -(alpha Lam/M_Pl) s1 <phi'(z1)>  (mean of the one-sided derivatives);  from the action: F1 = -dE_min/dz1 (finite difference).
Run: python3 cfg122_g3_virtualwork.py"""
import os, sys, math
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import Report

R = Report("cfg122_g3_virtualwork")
P, check = R.P, R.check
Lam, ratio_a, L = 0.7, 1.3, 10.0            # alpha/M_Pl = ratio_a (unit-free)
s1, s2 = 1.0, 2.0


def solve(z1, z2):
    j1, j2 = ratio_a * s1 / 2, ratio_a * s2 / 2
    seg = [(-L, z1), (z1, z2), (z2, L)]

    def pvals(u0):
        us = [u0, u0 + j1, u0 + j1 + j2]
        return [math.copysign(math.sqrt(abs(u)), u) for u in us]

    def phiend(u0):
        p = pvals(u0)
        return sum(pi * (b - a) for pi, (a, b) in zip(p, seg))          # phi(L) - phi(-L)

    u0 = brentq(phiend, -(j1 + j2) * 3, (j1 + j2) * 3, xtol=1e-14)
    p = pvals(u0)
    phi_left = 0.0
    phi_z1 = phi_left + p[0] * (z1 + L)
    phi_z2 = phi_z1 + p[1] * (z2 - z1)
    grad = sum((2 * Lam / 3) * abs(pi) ** 3 * (b - a) for pi, (a, b) in zip(p, seg))
    E = grad + Lam * ratio_a * (s1 * phi_z1 + s2 * phi_z2)
    return E, p


z1, z2 = -1.0, 2.0
h = 1e-5
Ep, _ = solve(z1 + h, z2)
Em, _ = solve(z1 - h, z2)
F_action = -(Ep - Em) / (2 * h)                                           # -dE_min/dz1 (virtual work)
_, p = solve(z1, z2)
F_field = -Lam * ratio_a * s1 * 0.5 * (p[0] + p[1])                        # force from the field on plate 1 (mean one-sided derivative)
rel = abs(F_action / F_field - 1)
P(f"  one-sided derivatives at plate 1: {p[0]:.6f}, {p[1]:.6f};  F_field = {F_field:.8f}, F_action (virtual work) = {F_action:.8f};  relative difference {rel:.2e}")
check("G3.3-plates (reported, first draft; kept as it fell)  virtual work vs the MEAN of the one-sided derivatives for two THIN plates (delta sources) with the nonlinear |phi'|^3 term", f"relative difference {rel:.2e} (limit 1e-2): for a delta source sitting on a kink of the minimiser the action's force is a nonlinear weighted mean of the one-sided derivatives, not their average (the singular self-force of a point source; the smooth-source check below is the one that matches how a_phi is used)", rel < 1e-2, load_bearing=False)
# Newton's third law between the plates: F1 + F2 = -d E_min / d(rigid shift) = 0 in the interior of a symmetric box? (translation invariance only if the box walls do not matter): report
E1, _ = solve(z1 + h, z2 + h); E0, _ = solve(z1 - h, z2 - h)
P(f"  rigid-shift derivative of E_min (vanishes by translation invariance away from the walls): {(E1 - E0) / (2 * h):.3e}  (box +-{L}); F1 + F2 from the field: "
  f"{-Lam * ratio_a * (s1 * 0.5 * (p[0] + p[1]) + s2 * 0.5 * (p[1] + p[2])):.3e}")
R.num("G3.3_plates", dict(F_action=F_action, F_field=F_field, rel=rel))

R.banner("G3.3 (gate)  the same check for SMOOTH sources (Gaussian slabs, width 0.4): F_action = -dE_min/dz1 vs F_field = -(alpha Lam/M_Pl) int rho_1 phi' dz")
w, zc1, zc2 = 0.4, -1.0, 2.0
NZ = 40001
zz = np.linspace(-L, L, NZ)
dz = zz[1] - zz[0]


def smooth(z1, z2):
    g = lambda z0, sgm: sgm * np.exp(-0.5 * ((zz - z0) / w) ** 2) / (w * math.sqrt(2 * math.pi))
    rho1, rho2 = g(z1, s1), g(z2, s2)
    rho = rho1 + rho2
    J = np.concatenate([[0.0], np.cumsum(0.5 * (rho[1:] + rho[:-1]) * dz)])
    def pv(u0):
        u = u0 + ratio_a * J / 2
        return np.sign(u) * np.sqrt(np.abs(u))
    def phiend(u0):
        p = pv(u0)
        return float(np.sum(0.5 * (p[1:] + p[:-1]) * dz))
    u0 = brentq(phiend, -3 * ratio_a * (s1 + s2) / 2, 3 * ratio_a * (s1 + s2) / 2, xtol=1e-14)
    p = pv(u0)
    phi = np.concatenate([[0.0], np.cumsum(0.5 * (p[1:] + p[:-1]) * dz)])
    E = float(np.sum(0.5 * ((2 * Lam / 3) * np.abs(p[1:]) ** 3 + (2 * Lam / 3) * np.abs(p[:-1]) ** 3) * dz)) + Lam * ratio_a * float(np.sum(0.5 * (rho * phi)[1:] * dz + 0.5 * (rho * phi)[:-1] * dz))
    F1_field = -Lam * ratio_a * float(np.sum(0.5 * ((rho1 * p)[1:] + (rho1 * p)[:-1]) * dz))
    return E, F1_field, p


hh = 1e-3
Ep_, _, _ = smooth(zc1 + hh, zc2)
Em_, _, _ = smooth(zc1 - hh, zc2)
_, F1f, _ = smooth(zc1, zc2)
F1a = -(Ep_ - Em_) / (2 * hh)
rel2 = abs(F1a / F1f - 1)
P(f"  smooth sources: F_field = {F1f:.8f}, F_action = {F1a:.8f}, relative difference {rel2:.2e}")
check("G3.3  reaction on a smooth baryon distribution from virtual work on the action = the field force (nonlinear |phi'|^3 kinetic term, two Gaussian slabs)", f"relative difference {rel2:.2e} (limit 1e-2)", rel2 < 1e-2)
R.num("G3.3", dict(F_action=F1a, F_field=F1f, rel=rel2))
R.verdict("G3.3", "PASS" if rel2 < 1e-2 else "FAIL", f"virtual-work force equals the field force on smooth sources to {rel2:.1e}; the thin-plate variant differs by {rel:.1e} (reported)")
nf, gf = R.write()
sys.exit(1 if (nf or gf) else 0)
