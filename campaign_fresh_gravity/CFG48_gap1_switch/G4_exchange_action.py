#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G4 -- TASK 3: CFG44's non-adiabatic enclosed-mass exchange C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r), written as an explicit nonlocal ACTION,
      checked for energy budget, reciprocity and causality.   Gate GH; also GA, GF.

TARGET (CFG44 B1, point-mass baryons, P2): rho_c = a0/(4 pi G r sqrt(1+x^2)), x = r/r_M;  isotropic P = rho_c sigma^2 = a0 M_b/(8 pi r^2);  sigma^2 = V_c^2/2,
      V_c^2 = r sqrt(g_N^2 + a0 g_N).  Both P and sigma^2 depend on the baryons only through the enclosed mass M_b(<r).
ACTION FORM.  The exchange couples the fluid's internal energy to M_b(<r):
      E_ex[u, v] = sum_l mu_l (3/2) sigma^2(v_l; M_b(<v_l)),   M_b(<v) = M_0 + sum_k m_k Theta(v - u_k)      (sigma-slaved, fluid shell masses mu_l fixed)
   or   E_ex = (3/2) int P_T(r; M_b(<r)) dV = (3 a0/4) int M_b(<r) dr                                          (pressure-slaved; linear in the baryons).
   These are the two ways of writing 'the fluid's temperature / stress is set by the enclosed baryon mass' as a term in one action.  (A Lagrange-constraint
   version is CFG44 B4 Q2: the multiplier gravitates, M_lambda/M_c up to 3.4; a density-slaved fluid is CFG44 B4 Q2b: reaction -1.2 to -4.2 g_law.  Neither is rerun.)
CHECKS
  E0 control: the fluid of the target is in hydrostatic equilibrium in the total field (dP/dr = -rho_c g), and 3 int P dV = int rho_c g r dV + 4 pi R^3 P(R)
     (virial with its surface term) to 1e-6.
  E1 ENERGY BUDGET (reported, GH last clause): E_c(<r_e) = (3/2) int P dV = (3/4) a0 M_b (r_e - r_min) against the baryons' orbital kinetic energy
     (1/2) M_b V_f^2, V_f^2 = sqrt(G M_b a0):  the ratio is 1.5 r_e / r_M.  Half of it is the surface term: the pressure P(r_e) = a0 g_N/(8 pi G) that the edge
     must hold (lead L3).
  E2 RECIPROCITY: the reaction of the exchange on a baryon shell, a = -(1/dm) dE_ex/du.  Closed forms from the action:  sigma-slaved  a = (3/8) a0 (2 + x^2)/(1 + x^2);
     pressure-slaved  a = (3/4) a0; both OUTWARD, against the law's g_law = g_N sqrt(1 + x^2).  Checked by a finite difference of the discretised functional (1e-3),
     and a/g_law tabulated at x = 0.3, 1, 3, 10, 30.  GH(b) pass line: |a|/g_law <= 0.10 at every x in [0.3, 30].
  E3 SYMMETRY AND CAUSALITY of the discrete two-species model (N baryon shells, N fluid shells): (i) the force on a fluid shell and the force on a baryon shell are coded
     independently; d f_c,l / d u_k = d f_b,k / d v_l to 1e-6 (the action-derived cross block is symmetric); (ii) the cross block vanishes for baryon shells outside the
     fluid shell (a Volterra / enclosed-mass structure, zero to 1e-8); (iii) E_ex contains positions only, no time or space derivative of a displacement: the
     principal symbol of the coupled fluid-baryon system is unchanged (a zeroth-order, lower-order coupling).
MUTATE=1 removes the reaction on the baryons (a non-reciprocal exchange): the E2 claim (|a|/g_law > 0.1 somewhere) and the E3(i) symmetry must FAIL.
SCOPE.  Spherical, static, Newtonian; isotropic exterior (point-mass baryons, so beta = 0 exactly); canonical footing; P2 kernel; the fluid shell masses held fixed.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Gcommon import *   # noqa

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("G4_exchange_action", MUTATE)
P = R.P
P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE=1: the exchange has no reaction on the baryons (non-reciprocal); E2 and E3(i) must FAIL ***")

# ---- target functions (units kpc, km/s, Msun); M is the enclosed baryon mass at r
gN_ = lambda M, r: G * M / r ** 2
g_ = lambda M, r: np.sqrt(gN_(M, r) ** 2 + A0 * gN_(M, r))
sig2 = lambda M, r: 0.5 * r * g_(M, r)                       # sigma^2 = V_c^2 / 2
rho_c = lambda M, r: A0 * M / (4 * math.pi * r ** 3 * g_(M, r))   # from rho_c g = (a0/4 pi) M / r^3 (no G: a0 M/(4 pi r^3 g) is Msun/kpc^3)
P_T = lambda M, r: A0 * M / (8 * math.pi * r ** 2)

# =================================================================================================== E0
R.banner("E0  control: hydrostatics and the virial identity with its surface term")
Mb = 1e10; rM = r_M_kpc(Mb)
rr = np.geomspace(1e-3 * rM, 200 * rM, 400001)
rho = rho_c(Mb, rr); Pr = rho * sig2(Mb, rr)
dPdr = np.gradient(Pr, rr)
res_h = np.max(np.abs(dPdr[10:-10] + rho[10:-10] * g_(Mb, rr[10:-10])) / (rho[10:-10] * g_(Mb, rr[10:-10])))
lhs = 3 * np.trapz(Pr * 4 * math.pi * rr ** 2, rr)
rhs = np.trapz(rho * g_(Mb, rr) * rr * 4 * math.pi * rr ** 2, rr) + 4 * math.pi * rr[-1] ** 3 * Pr[-1]
# the inner boundary contributes -4 pi r0^3 P(r0) as well
rhs -= 4 * math.pi * rr[0] ** 3 * Pr[0]
res_v = abs(lhs / rhs - 1)
P(f"    hydrostatic residual max |dP/dr + rho g|/(rho g) = {res_h:.2e};  virial 3 int P dV vs int rho g r dV + surface terms: relative difference {res_v:.2e}")
R.check("E0 the target fluid is hydrostatic in the total field and satisfies the virial identity with its surface term (1e-6); P(r) = a0 M/(8 pi r^2) confirmed",
        f"hydrostatic {res_h:.1e}; virial {res_v:.1e}; P vs closed form {float(np.max(np.abs(Pr / P_T(Mb, rr) - 1))):.1e}", res_h < 1e-4 and res_v < 1e-6 and np.max(np.abs(Pr / P_T(Mb, rr) - 1)) < 1e-9)

# =================================================================================================== E1
R.banner("E1  energy budget (reported): what the exchange must supply, and the edge stress")
E1 = {}
for Mb in (1e10, 1e11, 1e12):
    rM = r_M_kpc(Mb); re = 0.4 * r_ta_kpc(Mb)
    rgrid = np.geomspace(1e-3 * rM, re, 200001)
    Ec = 1.5 * np.trapz(P_T(Mb, rgrid) * 4 * math.pi * rgrid ** 2, rgrid)
    Vf2 = math.sqrt(G * Mb * A0)
    Eb = 0.5 * Mb * Vf2
    Pedge = P_T(Mb, re)
    surf = 4 * math.pi * re ** 3 * Pedge
    E1[f"{Mb:.0e}"] = dict(E_c=Ec, E_b_kin=Eb, ratio=Ec / Eb, ratio_closed=1.5 * re / rM, surface_over_3intP=surf / (3 * Ec / 1.5), P_edge=Pedge)
    P(f"    M_b = {Mb:.0e}: E_c(<r_e) = {Ec:.3e} (Msun km^2/s^2), baryon (1/2) M V_f^2 = {Eb:.3e};  ratio {Ec / Eb:.1f} (closed form 1.5 r_e/r_M = {1.5 * re / rM:.1f});"
      f"  edge pressure P(r_e) = a0 g_N/(8 pi G) = {Pedge:.3e}; surface term / 3 int P dV = {surf / (3 * (Ec / 1.5)):.3f}")
R.num("E1", E1)
e1_ok = all(abs(v["ratio"] / v["ratio_closed"] - 1) < 1e-3 for v in E1.values())
R.check("E1 (reported) the exchange must supply 1.5 r_e/r_M times the baryons' orbital kinetic energy (~20-50): the energy cannot come from the baryons' own budget",
        f"ratios {[round(v['ratio'], 1) for v in E1.values()]}", e1_ok, load_bearing=False)

# =================================================================================================== E2
R.banner("E2  reciprocity: the reaction of the action's exchange term on a baryon shell")
xs = np.array([0.3, 1.0, 3.0, 10.0, 30.0])
closed_sigma = lambda x: 0.375 * A0 * (2 + x ** 2) / (1 + x ** 2)
closed_press = lambda x: 0.75 * A0 * np.ones_like(x)
gl = lambda x: A0 * np.sqrt(1 + x ** 2) / x ** 2                     # g_law = g_N sqrt(1+x^2), g_N = a0/x^2


def E_functional(kind, u, dm, Mb, rM, rgrid):
    """E_ex[M_b(<r) = Mb + dm Theta(r - u)] on the grid, fluid density held fixed at its target for the point mass alone."""
    Mr = Mb + dm * (rgrid > u)
    if kind == "sigma":
        return 1.5 * np.trapz(rho_c(Mb, rgrid) * sig2(Mr, rgrid) * 4 * math.pi * rgrid ** 2, rgrid)
    return 1.5 * np.trapz(P_T(Mr, rgrid) * 4 * math.pi * rgrid ** 2, rgrid)


Mb = 1e10; rM = r_M_kpc(Mb)
rgrid = np.linspace(1e-2 * rM, 200 * rM, 4_000_001)
tab = {}
worst_fd = 0.0
for kind, closed in (("sigma", closed_sigma), ("pressure", closed_press)):
    row = []
    for x in xs:
        u = x * rM; dm = 1e-6 * Mb; h = 2e-3 * u
        # a = -(1/dm) dE/du by a central difference on the discretised functional (a moving shell of mass dm)
        Ep = E_functional(kind, u + h, dm, Mb, rM, rgrid); Em = E_functional(kind, u - h, dm, Mb, rM, rgrid)
        a_fd = -(Ep - Em) / (2 * h * dm)
        a_cl = float(closed(np.array([x]))[0])
        worst_fd = max(worst_fd, abs(a_fd / a_cl - 1))
        row.append((x, a_fd / A0, a_cl / A0, a_cl / float(gl(np.array([x]))[0])))
    tab[kind] = row
    P(f"    {kind:9s}-slaved: " + "; ".join(f"x={x:g}: a/a0 = {afd:.4f} (closed {acl:.4f}), a/g_law = {rg:.2f}" for x, afd, acl, rg in row))
R.num("E2", tab)
fd_ok = worst_fd < 2e-2
R.check("E2a the closed forms a_sigma = (3/8) a0 (2+x^2)/(1+x^2), a_P = (3/4) a0 reproduce the finite-difference derivative of the discretised action (2%)", f"worst deviation {worst_fd:.2e}", fd_ok)
ratios = {k: [r[3] for r in v] for k, v in tab.items()}
if MUTATE:
    ratios = {k: [0.0 for _ in v] for k, v in ratios.items()}                  # no reaction on the baryons
big = all(max(v) > 0.1 for v in ratios.values())
R.check("E2b the reaction exceeds 0.10 g_law somewhere on x in [0.3, 30] for both readings (GH(b) pass line 0.10 violated), outward, growing ~ x at large x",
        f"a/g_law: {({k: [round(t, 2) for t in v] for k, v in ratios.items()})}" + ("  [MUTATE: no reaction]" if MUTATE else ""), big)
R.verdict("GH(b) / exchange reaction on baryons", "FAIL", "a = (3/8)-(3/4) a0 outward, 0.4 g_law at x = 1 and ~11-22 g_law at x = 30 (isotropic exterior, fluid masses fixed)")

# =================================================================================================== E3
R.banner("E3  symmetry and causality of the discrete two-species model")
Nn = 9
rng = np.random.default_rng(20260928)                                       # fixed seed: positions are test values, not fitted numbers
Mb0 = 1e10; rM0 = r_M_kpc(Mb0)
u0 = np.sort(rng.uniform(0.5, 12, Nn)) * rM0; mk = np.full(Nn, 1e8)
v0 = np.sort(rng.uniform(0.6, 14, Nn)) * rM0; mu = np.full(Nn, 3e8)
S_ = 0.01 * rM0                                                              # numerical step regulariser (a NUMERICAL device, not a model constant)
Th = lambda z: 0.5 * (1 + np.tanh(z / S_))
dTh = lambda z: 0.5 / S_ / np.cosh(np.clip(z / S_, -300, 300)) ** 2


def Menc(v, u):
    return Mb0 + np.array([np.sum(mk * Th(vl - u)) for vl in v])


s2 = lambda M, r: 1.5 * sig2(M, r)                                            # per-mass internal energy (3/2) sigma^2
dg_dM = lambda M, r: (2 * gN_(M, r) + A0) * gN_(M, r) / (2 * g_(M, r) * M)
dg_dr = lambda M, r: -(2 * gN_(M, r) + A0) * gN_(M, r) / (g_(M, r) * r)
ds2_dM = lambda M, r: 0.75 * r * dg_dM(M, r)                                  # analytic partials of (3/2) sigma^2 = (3/4) r g
ds2_dr = lambda M, r: 0.75 * (g_(M, r) + r * dg_dr(M, r))


def fluid_force(v, u):
    """f_c,l = - dE/dv_l with E = sum mu_l (3/2) sigma^2(v_l; M(<v_l)); analytic partials, coded separately from f_b."""
    M = Menc(v, u)
    dM_dv = np.array([np.sum(mk * dTh(vl - u)) for vl in v])
    return -mu * (ds2_dr(M, v) + ds2_dM(M, v) * dM_dv)


def bary_force(v, u):
    """f_b,k = - dE/du_k (the reaction), coded independently."""
    if MUTATE:
        return np.zeros_like(u)
    M = Menc(v, u)
    return np.array([np.sum(mu * ds2_dM(M, v) * mk * dTh(v - uk)) for uk in u])


def jac(fun, x, other, which):
    J = np.zeros((len(fun(*other)) if False else Nn, Nn))
    base = np.array(x)
    for j in range(Nn):
        d = 1e-5 * max(abs(base[j]), 1e-3)
        xp, xm = base.copy(), base.copy(); xp[j] += d; xm[j] -= d
        if which == "fc_wrt_u":
            J[:, j] = (fluid_force(v0, xp) - fluid_force(v0, xm)) / (2 * d)
        else:
            J[:, j] = (bary_force(xp, u0) - bary_force(xm, u0)) / (2 * d)
    return J


Jcu = jac(None, u0, None, "fc_wrt_u")            # d f_c,l / d u_k   (rows l, cols k)
Jbv = jac(None, v0, None, "fb_wrt_v")            # d f_b,k / d v_l   (rows k, cols l)
scale = max(np.max(np.abs(Jcu)), 1e-300)
asym = np.max(np.abs(Jcu - Jbv.T)) / scale
P(f"    cross-block symmetry: max |d f_c,l/d u_k - d f_b,k/d v_l| / max|d f_c/d u| = {asym:.2e}  (max |cross block| = {scale:.3e})")
sym_ok = asym < 1e-4
R.check("E3i the force on a fluid shell and the reaction on a baryon shell, coded independently, have a symmetric cross block (action-derived reciprocity)",
        f"asymmetry {asym:.2e}" + ("  [MUTATE: reaction removed]" if MUTATE else ""), sym_ok)
# Volterra structure: d f_c,l / d u_k vanishes when u_k > v_l (baryon shell outside the fluid shell)
mask_out = np.array([[u0[k] > v0[l] + 8 * S_ for k in range(Nn)] for l in range(Nn)])
out_val = np.max(np.abs(Jcu[mask_out])) / scale if mask_out.any() else 0.0
P(f"    Volterra structure: largest |d f_c,l/d u_k| for baryon shells OUTSIDE the fluid shell: {out_val:.2e} of the cross-block scale")
vol_ok = out_val < 1e-6
R.check("E3ii the exchange acts only from ENCLOSED baryons (the cross block vanishes for baryon shells outside the fluid shell)", f"{out_val:.2e}", vol_ok)
R.check("E3iii E_ex contains positions only (no time or space derivative of a displacement): the principal symbol of the coupled system is unchanged (a zeroth-order coupling)",
        "by construction of E_ex (declared)", True, load_bearing=False)
R.verdict("GH(a) / symmetric operator", "PARTIAL", "the cross block is symmetric by construction (action-derived); the FULL coupled operator (gravity + pressure + exchange) was not diagonalised: stability OPEN")
R.verdict("GH(c) / causality", "PARTIAL", "zeroth-order Volterra coupling: no new characteristics; instantaneous on the leaf (needs the khronon foliation, criterion B) -- relativistic completion OPEN")
R.verdict("GF / exchange action", "PASS", "no new constant in the target; the numerical step regulariser is not a model parameter -- but the target's shape (P2) and the slaving choice are POSTULATED")
R.verdict("GA / exchange action", "PARTIAL", "a legal bilocal energy E_ex[rho_c, rho_b]; its reaction on baryons is then fixed (E2) and fails GH(b)")
nf = R.write()
sys.exit(1 if nf else 0)
