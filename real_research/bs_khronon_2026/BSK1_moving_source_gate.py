#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BSK1 -- THE BLANCHET-SKORDIS KHRONON AGAINST THE MOVING-SOURCE GATE: the phantom moves (it is a conserved fluid
carried by the aether), but it is assembled, not generated, it follows velocity changes only inside
r ~ 2 G M_b / du^2, and a GR-recovering interpolating function makes the fluid linearly unstable beyond the
phantom peak at the local orbital rate.

THE THEORY TESTED
  Blanchet & Skordis, JCAP 11 (2024) 040, arXiv:2404.06584 ("BS24"):
      S = c^3/(16 pi G) Int sqrt(-g) [ R - 2 J(Y) + 2 K(Q) ] + S_m ,
      Q = c sqrt(-g^{mu nu} d_mu tau d_nu tau),  n_mu = -(c/Q) d_mu tau,  A_mu = c^2 n^nu nabla_nu n_mu,  Y = A.A/c^4,
  with J = Lambda - Y + (2c^2/3a0) Y^{3/2} + ... at low acceleration (their eq. 37), J -> Lambda_inf + O(a0/y) at
  high acceleration (eq. 40, GR recovery), and K = mu^2 (Q-1)^2 + ... (eq. 7; DBI form eq. 87).
  Their post-Newtonian system (eqs. 19, 25, 27, 29, 30), with tau = t + sigma/c^2:
      Xi = phi - sigma_dot + |grad sigma|^2/2                       (the unitary-gauge lapse perturbation)
      4 pi G rho_tau = -[ div(J_Y grad Xi) + mu^2 Xi ]              (the khronon "mass density" = the phantom)
      v_tau = -grad sigma                                          (the khronon "velocity" = the aether's flow)
      lap phi = 4 pi G (rho_m + rho_tau),   d_t rho_tau + div(rho_tau v_tau) = 0 .
  In the static case sigma = 0, Xi = phi and div[(1+J_Y) grad phi] + mu^2 phi = 4 pi G rho_m (eq. 35): AQUAL with
  f(y) = 1 + J_Y, y = |grad phi|/a0, plus a mass term.

WHY THIS LANE
  L330 showed that a MOND sector which is shift-free and free of time derivatives in unitary gauge (C-H) freezes
  its phantom at linear order around flat space.  BS24's extra sector has exactly that structure (M1 below), yet
  BS24 derive a phantom that moves.  The two are reconciled here (M2): the phantom is a conserved fluid carried
  by the aether's own flow; the transport term is second order around flat space and first order around a
  galaxy.  The gate is then run on BS24's own equations: does the phantom follow a moving source (M3), how fast
  does it respond (M4, M6), and is the static MOND halo a stable state of the fluid (M5)?  M7 records the
  structural fact behind BS24's k-dependent sound speed (their eq. 71) that the KiDS lane (BSX1) needs.

METHOD
  M1 symbolic, unitary gauge, general lapse/shift/conformal leaves (the machinery of L330 M1).
  M2-M4, M7 symbolic from BS24's PN equations; M4 is a WKB (frozen-coefficient, k >> 1/r) linearisation about a
  static halo, anisotropic through f_theta = f + y f'(y) cos^2(theta), theta the angle between k and grad phi.
  M5-M6 numbers on both a0 footings for the RAR kernel nu_RAR (the record's), the monotone kernel nu_mono (L340's)
  and power-law GR-recovering tails.

CONTROLS
  M3 control and MUTATE=1: pin the aether (sigma = 0 for all t, the setting of L330's linear analysis): the moving
  solution then fails the continuity equation and the WKB response has omega = 0 (no dynamics), so M3 and M4 must
  FAIL (rc = 1).  M4 is checked against the static linear response of AQUAL (it must reproduce the phantom ratio
  (1 - f_theta)/f_theta).  M5's kernels are cross-checked against L340's printed nu_RAR peak (y_p = 2.5396,
  h_p = 0.6476 a0) and nu_mono's maximum deviation (0.0104 dex).  MUTATE outputs go to separate files.

Run from the repository root:  python3 real_research/bs_khronon_2026/BSK1_moving_source_gate.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE = "BSK1"
SLUG = "BSK1_moving_source_gate"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("METHOD")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the aether is pinned (sigma = 0 for all t); M3 and M4 must FAIL ***")

# ---------------------------------------------------------------------------------------- constants
G = 6.674e-11; c = 2.998e8; MSUN = 1.989e30; KPC = 3.0857e19; PC = KPC / 1e3; AU = 1.496e11
YR = 3.156e7; MYR = 1e6 * YR; GYR = 1e9 * YR
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

# ============================================================================================ M1
banner("M1  BS24's EXTRA SECTOR IN UNITARY GAUGE: a function of the lapse and its spatial gradient only (L330's class)")
t, x, y, z = X = sp.symbols('t x y z', real=True)
N = sp.Function('N', positive=True)(*X)
b = [sp.Function(f'b{i}')(*X) for i in range(3)]          # shift N^i
w = sp.Function('w')(*X)                                   # conformal factor of the leaves
gam = sp.diag(*(3 * [sp.exp(2 * w)]))
gami = gam.inv()
bl = [sum(gam[i, j] * b[j] for j in range(3)) for i in range(3)]
g = sp.zeros(4)
g[0, 0] = -N**2 + sum(bl[i] * b[i] for i in range(3))
for i in range(3):
    g[0, i + 1] = g[i + 1, 0] = bl[i]
    for j in range(3):
        g[i + 1, j + 1] = gam[i, j]
gi = sp.zeros(4)
gi[0, 0] = -1 / N**2
for i in range(3):
    gi[0, i + 1] = gi[i + 1, 0] = b[i] / N**2
    for j in range(3):
        gi[i + 1, j + 1] = gami[i, j] - b[i] * b[j] / N**2
inv_ok = sp.simplify(g * gi - sp.eye(4)) == sp.zeros(4)
# tau = t (c = 1): Q = sqrt(-g^{mu nu} d tau d tau) = sqrt(-g^{00});  n_mu = -(1/Q) d_mu tau
Qexpr = sp.sqrt(-gi[0, 0])
Q_ok = sp.simplify(Qexpr - 1 / N) == 0
n_lo = [-1 / Qexpr, 0, 0, 0]
n_up = [sum(gi[m, k] * n_lo[k] for k in range(4)) for m in range(4)]
Gam = [[[sum(gi[l, s] * (sp.diff(g[s, m], X[nn]) + sp.diff(g[s, nn], X[m]) - sp.diff(g[m, nn], X[s]))
             for s in range(4)) / 2 for nn in range(4)] for m in range(4)] for l in range(4)]
A_lo = [sp.simplify(sum(n_up[nn] * (sp.diff(n_lo[m], X[nn]) - sum(Gam[l][nn][m] * n_lo[l] for l in range(4)))
                        for nn in range(4))) for m in range(4)]
Yexpr = sp.simplify(sum(gi[m, nn] * A_lo[m] * A_lo[nn] for m in range(4) for nn in range(4)))
Y_leaf = sum(gami[i, j] * sp.diff(sp.log(N), X[i + 1]) * sp.diff(sp.log(N), X[j + 1]) for i in range(3) for j in range(3))
Y_ok = sp.simplify(Yexpr - Y_leaf) == 0
no_shift = not any(e.has(bb) for e in (Qexpr, Yexpr) for bb in b)
no_tdot = not any(e.has(sp.Derivative(N, t)) or e.has(sp.Derivative(w, t)) for e in (Qexpr, Yexpr))
P(f"    ADM inverse verified: {inv_ok};  Q = 1/N: {Q_ok};  Y = gamma^ij d_i lnN d_j lnN: {Y_ok}")
P(f"    shift absent from Q and Y: {no_shift};  time derivatives absent: {no_tdot}")
OUT["numbers"]["M1"] = {"inverse": inv_ok, "Q_is_1_over_N": Q_ok, "Y_leaf": Y_ok, "shift_free": no_shift,
                        "time_derivative_free": no_tdot}
check("M1 in unitary gauge BS24's extra sector sqrt(-g)[-2J(Y) + 2K(Q)] depends on the lapse and its spatial "
      "gradient only (Q = 1/N, Y = gamma^ij d_i lnN d_j lnN): shift-free and time-derivative-free, L330's class",
      f"Q = 1/N {Q_ok}; Y leaf form {Y_ok}; shift-free {no_shift}; time-derivative-free {no_tdot}",
      inv_ok and Q_ok and Y_ok and no_shift and no_tdot,
      "by L330's linear identity its phantom would be frozen; M2 shows why it is not")

# ============================================================================================ M2
banner("M2  THE PHANTOM IS A CONSERVED FLUID CARRIED BY THE AETHER; its transport is 2nd order about flat space")
xs = (x, y, z)
lap = lambda f: sum(sp.diff(f, v, 2) for v in xs)
div = lambda F: sum(sp.diff(F[i], xs[i]) for i in range(3))
grad = lambda f: [sp.diff(f, v) for v in xs]
phi = sp.Function('phi')(*X); sig = sp.Function('sigma')(*X)
zeta = [sp.Function(f'zeta{i}')(*X) for i in range(3)]
Gs, fourpiG = sp.symbols('G', positive=True), None
fourpiG = 4 * sp.pi * Gs
rho_m = sp.Function('rho_m')(*X); vm = [sp.Function(f'vm{i}')(*X) for i in range(3)]
rho_tau = lap(phi) / fourpiG - rho_m                              # BS24 eq. 29a solved for rho_tau
v_tau = [-d for d in grad(sig)]                                   # eq. 27b
# divergence of the momentum equation (29b): div[lap zeta - grad div zeta - grad phi_dot] = - lap phi_dot identically
lhs29b = [lap(zeta[i]) - sp.diff(div(zeta), xs[i]) - sp.diff(phi, t, xs[i]) for i in range(3)]
div_lhs = sp.simplify(div(lhs29b) + lap(sp.diff(phi, t)))
# so div(29b) <=> -lap phi_dot = 4piG div(rho_m v_m + rho_tau v_tau); with d_t(29a) and matter continuity this IS eq. 30
cont_m = sp.diff(rho_m, t) + div([rho_m * vm[i] for i in range(3)])
cont_tau = sp.diff(rho_tau, t) + div([rho_tau * v_tau[i] for i in range(3)])
div29b_resid = -lap(sp.diff(phi, t)) - fourpiG * div([rho_m * vm[i] + rho_tau * v_tau[i] for i in range(3)])
identity = sp.simplify(sp.expand(div29b_resid + fourpiG * (cont_m + cont_tau)))
P(f"    div of eq. 29b's left side + lap(phi_dot) = {div_lhs};  div(29b) + 4piG[cont_m + cont_tau] = {identity}")
# linearise eq. 30 about (a) flat space rho0 = 0 and (b) a static halo rho0(x) != 0, with sigma = eps*s1
eps = sp.Symbol('epsilon')
r1 = sp.Function('r1')(*X); s1 = sp.Function('s1')(*X); rho0 = sp.Function('rho0')(x, y, z)
cont_lin = lambda rho_bg: sp.expand(sp.diff(rho_bg + eps * r1, t)
                                    + div([(rho_bg + eps * r1) * (-sp.diff(eps * s1, v)) for v in xs]))
flat_O1 = sp.simplify(cont_lin(0).coeff(eps, 1))
halo_O1 = sp.simplify(cont_lin(rho0).coeff(eps, 1))
P(f"    O(eps) continuity about flat space: {flat_O1} = 0   (frozen: L330's identity; BS24's omega = 0 on Minkowski)")
P(f"    O(eps) continuity about a halo rho0(x): {halo_O1} = 0   (transport by the aether flow is FIRST order)")
m2_ok = (div_lhs == 0) and (identity == 0) and (flat_O1 == sp.diff(r1, t)) and halo_O1.has(rho0) and halo_O1.has(s1)
OUT["numbers"]["M2"] = {"div29b_identity": str(identity), "flat_O1": str(flat_O1), "halo_O1": str(halo_O1)}
check("M2 BS24's PN equations make the phantom a conserved fluid, d_t rho_tau + div(rho_tau v_tau) = 0 with "
      "v_tau = -grad sigma (identity from div 29b + d_t 29a + matter continuity); about flat space the transport is "
      "second order (d_t rho_1 = 0: L330's frozen identity, BS24's omega = 0), about a galaxy it is first order",
      f"identity residual {identity}; flat O(eps): {flat_O1}; halo O(eps): {halo_O1}",
      m2_ok,
      "L330's frozen phantom is the flat-space linearisation of a transport law: the phantom is conserved (never "
      "generated by baryons) and moves with the aether")

# ============================================================================================ M3
banner("M3  A GALAXY AND ITS PHANTOM IN UNIFORM MOTION: an exact PN solution (Galilean boost of the static one)")
Vx, Vy, Vz = V = sp.symbols('V_x V_y V_z', real=True)
a0s, mus = sp.symbols('a_0 mu', positive=True)
fF = sp.Function('f')                                             # AQUAL interpolating function f(y) = 1 + J_Y
# work in comoving coordinates xi = x - V t: for any F(t,x) = Ft(xi), d_x F = d_xi Ft and d_t F = -V.grad_xi Ft
XIc = sp.symbols('xi1 xi2 xi3', real=True)
Dx = lambda e, i: sp.diff(e, XIc[i])
Dt = lambda e: -sum(V[i] * sp.diff(e, XIc[i]) for i in range(3))
PHI = sp.Function('phi0')(*XIc)                                   # the boosted static potential phi0(x - V t)
sig_mov = (0 * t) if MUTATE else (-(Vx * x + Vy * y + Vz * z) + (Vx**2 + Vy**2 + Vz**2) * t / 2)
gs = [sp.diff(sig_mov, v) for v in xs]                            # explicit: constants
sdot = sp.diff(sig_mov, t)
XI = PHI - sdot + sum(d**2 for d in gs) / 2                        # eq. 19
gXI = [Dx(XI, i) for i in range(3)]
modg = sp.sqrt(sum(d**2 for d in gXI))
JY = fF(modg / a0s) - 1
rho_tau_27a = -(sum(Dx(JY * gXI[i], i) for i in range(3)) + mus**2 * XI) / fourpiG     # eq. 27a
gP = [Dx(PHI, i) for i in range(3)]; modP = sp.sqrt(sum(d**2 for d in gP))
rho_m_static = (sum(Dx(fF(modP / a0s) * gP[i], i) for i in range(3)) + mus**2 * PHI) / fourpiG   # eq. 35, boosted
rho_tau_29a = sum(Dx(Dx(PHI, i), i) for i in range(3)) / fourpiG - rho_m_static          # eq. 29a
cons_resid = sp.simplify(sp.expand(rho_tau_27a - rho_tau_29a))
vT = [-d for d in gs]                                             # eq. 27b: the aether's velocity
cont_resid = sp.simplify(sp.expand(Dt(rho_tau_29a) + sum(Dx(rho_tau_29a * vT[i], i) for i in range(3))))
xi_is_phi = sp.simplify(XI - PHI) == 0
P(f"    sigma = {sig_mov};  Xi - phi = {sp.simplify(XI - PHI)};  (27a) - (29a) residual: {cons_resid}")
P(f"    aether velocity v_tau = {vT};  continuity residual d_t rho_tau + div(rho_tau v_tau): {cont_resid if cont_resid == 0 else 'nonzero: ' + str(cont_resid)[:160]}")
m3_ok = xi_is_phi and cons_resid == 0 and cont_resid == 0
OUT["numbers"]["M3"] = {"sigma": str(sig_mov), "Xi_minus_phi": str(sp.simplify(XI - PHI)),
                        "consistency_residual": str(cons_resid), "continuity_residual": str(cont_resid)}
check("M3 a galaxy moving uniformly at V with its phantom is an exact solution of BS24's PN system when the "
      "aether moves with it (sigma = -V.x + V^2 t/2): Xi = phi, eqs. 27a/29a/35 agree, continuity holds",
      f"Xi = phi {xi_is_phi}; 27a-29a residual {cons_resid}; continuity residual {'0' if cont_resid == 0 else 'nonzero'}",
      m3_ok,
      "the moving-source gate that C-H fails at linear order is passed: the phantom carries momentum rho_tau V "
      "(BS24 eq. 28b); with the aether pinned (control) the same moving phantom violates continuity")

# ============================================================================================ M4
banner("M4  HOW FAST THE PHANTOM FLUID RESPONDS: WKB linearisation about a static halo (anisotropic)")
k, om, th = sp.symbols('k omega theta', positive=True)
r0, fy, fp, yy = sp.symbols('rho_0 f fprime y', positive=True)
dphi, dXi, dsig, drho, drm = sp.symbols('dphi dXi dsigma drho drho_m')
C_th = (fy - 1) + yy * fp * sp.cos(th)**2                     # linearised J_Y tensor along k: C_T + (C_L - C_T) cos^2
f_th = fy + yy * fp * sp.cos(th)**2
eqs = [sp.Eq(-k**2 * dphi, fourpiG * (drm + drho)),                                    # Poisson (29a)
       sp.Eq(fourpiG * drho, (k**2 * C_th - mus**2) * dXi),                             # (27a) linearised
       sp.Eq(-sp.I * om * drho, (0 if MUTATE else -r0 * k**2 * dsig)),                  # continuity (30)
       sp.Eq(dXi, dphi + (0 if MUTATE else sp.I * om * dsig))]                          # Bernoulli (19)
# homogeneous dispersion: determinant of the linear system with drho_m = 0
Msys = sp.linear_eq_to_matrix([e.lhs - e.rhs for e in eqs], [dphi, dXi, dsig, drho])[0].subs(drm, 0)
det = sp.factor(sp.simplify(Msys.det()))
om2_sol = sp.solve(sp.Eq(det, 0), om**2) if not MUTATE else []
om2_expected = fourpiG * r0 * (k**2 * f_th - mus**2) / (k**2 * (1 - f_th) + mus**2)
om2_ok = (len(om2_sol) == 1) and sp.simplify(om2_sol[0] - om2_expected) == 0
# static response (omega -> 0) must reproduce AQUAL's linear phantom ratio
sol_static = sp.solve([e.subs(om, 0) for e in eqs[:2]] + [sp.Eq(dXi, dphi)], [dphi, dXi, drho], dict=True)
ratio = sp.simplify(sol_static[0][drho] / drm) if sol_static else None
ratio_expected = (1 - f_th + mus**2 / k**2) / (f_th - mus**2 / k**2)
ratio_ok = ratio is not None and sp.simplify(ratio - ratio_expected) == 0
P(f"    dispersion: omega^2 = {om2_sol[0] if om2_sol else 'none (omega = 0: no dynamics)'}")
P(f"    expected:   omega^2 = 4 pi G rho_0 (k^2 f_theta - mu^2)/(k^2 (1 - f_theta) + mu^2),  f_theta = f + y f' cos^2 theta")
P(f"    static response drho/drho_m = {ratio};  AQUAL linear phantom ratio (1 - f_th + mu^2/k^2)/(f_th - mu^2/k^2): {ratio_ok}")
P(f"    k >> mu: omega^2 -> 4 pi G rho_0 f_theta/(1 - f_theta)  (k-independent: no pressure, a local oscillator)")
OUT["numbers"]["M4"] = {"omega2": str(om2_sol[0]) if om2_sol else "none", "static_ratio": str(ratio)}
check("M4 about a static MOND halo the phantom fluid obeys omega^2 = 4 pi G rho_tau (k^2 f_th - mu^2)/(k^2(1-f_th) "
      "+ mu^2); its omega -> 0 limit is AQUAL's linear phantom response (1 - f_th)/f_th",
      f"dispersion matches: {om2_ok}; static limit matches AQUAL: {ratio_ok}",
      om2_ok and ratio_ok,
      "for k >> mu the frequency is k-independent: the phantom follows a source only on its local dynamical time; "
      "for k << mu/sqrt(f_th) omega^2 < 0 is ordinary Jeans clustering (the dust-like cosmological regime)")

# ============================================================================================ M5
banner("M5  STABILITY OF THE STATIC HALO: 0 < f_theta < 1 needs a MONOTONE phantom law; GR recovery breaks it")
P("    omega_L^2 = 4 pi G rho_tau f_L/(1 - f_L), f_L = f + y f' = d(g_N)/d(g): stable iff d g/d g_N > 1, i.e. the phantom")
P("    acceleration h = g - g_N must INCREASE with g_N -- L340's monotone-phantom condition, reached from the fluid side.")


def nu_rar(xN):
    return 1.0 / (1.0 - np.exp(-np.sqrt(xN)))


xg = np.logspace(-4, 6, 200001)
h_rar = (nu_rar(xg) - 1.0) * xg                                  # phantom acceleration / a0 vs x = g_N/a0
ip = int(np.argmax(h_rar)); x_p, h_p = xg[ip], h_rar[ip]
dgdgN_rar = 1.0 + np.gradient(h_rar, xg)
unstable_rar = xg[dgdgN_rar < 1.0]
# nu_mono (L340): nu_RAR below the peak, then h' = 0.05 h_p/(x + x_p)
h_mono = np.where(xg <= x_p, h_rar, h_p + 0.05 * h_p * np.log((xg + x_p) / (2 * x_p)))
dgdgN_mono = 1.0 + np.gradient(h_mono, xg)
dev_mono = np.max(np.abs(np.log10((xg + h_mono) / (xg + h_rar))))
P(f"    nu_RAR: phantom peak x_p = {x_p:.4f}, h_p = {h_p:.4f} a0 (L340: 2.5396, 0.6476);  d g/d g_N < 1 for x > {unstable_rar.min():.3f}")
P(f"    nu_mono: min d g/d g_N = {dgdgN_mono.min():.6f} (> 1: stable everywhere);  max |d log g| vs nu_RAR = {dev_mono:.4f} dex (L340: 0.0104)")
# any GR-recovering tail h = K g^-n: f_L - 1 = n h/g > 0 and 4piG rho = (2n+2) h/r  =>  growth rate^2 = (2 + 2/n) G M / r^3
nn_, KK, GM, rr, gg = sp.symbols('n K GM r g', positive=True)
h_r = KK * (GM / rr**2)**(-nn_)                                   # Newtonian regime, h << g
rho_term = sp.simplify(sp.diff(rr**2 * h_r, rr) / rr**2)          # 4 pi G rho_tau
fL_minus_1 = sp.simplify(nn_ * h_r / (GM / rr**2))
rate2 = sp.simplify(rho_term / fL_minus_1)
rate2_ok = sp.simplify(rate2 - (2 + 2 / nn_) * GM / rr**3) == 0
P(f"    GR-recovering tail h = K g^-n (h << g): 4piG rho_tau = {rho_term},  f_L - 1 = {fL_minus_1}")
P(f"      => growth rate^2 = 4piG rho_tau f_L/(f_L - 1) -> {rate2}  (independent of the tail's amplitude K)")
# numbers: e-folding time of the instability (a) at 1 AU (n = 2), (b) in the Milky Way inside nu_RAR's phantom peak
efold_AU = 1.0 / math.sqrt(3.0 * G * MSUN / AU**3)
P(f"    Solar System, 1 AU, n = 2: e-folding time {efold_AU / 86400:.0f} days  (any amplitude of the tail)")
MB = 6e10 * MSUN
m5_nums = {"x_p": round(float(x_p), 4), "h_p": round(float(h_p), 4), "unstable_from_x": round(float(unstable_rar.min()), 3),
           "mono_min_dg_dgN": float(dgdgN_mono.min()), "mono_dev_dex": round(float(dev_mono), 4),
           "efold_1AU_days": round(efold_AU / 86400, 1)}
for foot, a0 in A0.items():
    r = np.logspace(math.log10(0.2 * KPC), math.log10(300 * KPC), 4000)
    gN = G * MB / r**2
    xN = gN / a0
    h = (nu_rar(xN) - 1.0) * gN                                    # phantom acceleration (spherical, point mass)
    rho = np.gradient(r**2 * h, r) / (4 * np.pi * G * r**2)
    dg_dgN = 1.0 + np.gradient(h, gN)
    fL = 1.0 / dg_dgN
    with np.errstate(divide='ignore', invalid='ignore'):          # fL = 1 exactly at the peak (WKB singular there)
        rate2_num = 4 * np.pi * G * rho * fL / (fL - 1.0)        # > 0 = growth where fL > 1
    mask = (fL > 1.0) & (rho > 0)
    r_peak = math.sqrt(G * MB / (x_p * a0)) / KPC
    tmin = (1.0 / np.sqrt(rate2_num[mask])).min() / MYR if mask.any() else float('nan')
    t_at_r = {}
    for rk in (1, 2, 3):
        i = int(np.argmin(np.abs(r / KPC - rk)))
        t_at_r[rk] = round(float(1.0 / math.sqrt(rate2_num[i]) / MYR), 1) if mask[i] else None
    P(f"    {foot:9s} Milky Way (6e10 Msun, point mass, nu_RAR): unstable inside r = {r[mask].max()/KPC:.2f} kpc "
      f"(phantom peak at {r_peak:.2f} kpc); e-folding {t_at_r} Myr at r = 1/2/3 kpc")
    m5_nums[foot] = {"r_unstable_max_kpc": round(float(r[mask].max() / KPC), 2), "r_peak_kpc": round(r_peak, 2),
                     "efold_Myr_at_1_2_3kpc": t_at_r}
OUT["numbers"]["M5"] = m5_nums
check("M5a (derived) the static MOND halo is a stable state of BS24's phantom fluid iff 0 < f_theta < 1, i.e. iff the "
      "phantom acceleration increases with g_N (nu_mono passes everywhere; nu_RAR fails beyond x = 2.54)",
      f"nu_RAR unstable for x > {unstable_rar.min():.3f} (peak x_p = {x_p:.4f}, h_p = {h_p:.4f}); nu_mono min dg/dgN = "
      f"{dgdgN_mono.min():.4f}",
      abs(x_p - 2.5396) < 5e-3 and abs(h_p - 0.6476) < 5e-3 and dgdgN_mono.min() >= 1.0 - 1e-6 and abs(unstable_rar.min() - x_p) < 0.05
      and abs(dev_mono - 0.0104) < 5e-4,
      "the same condition L340 found for C-H/K's health, here as the stability of a fluid")
check("M5b (derived) any GR-recovering tail (BS24 eq. 40: h -> 0 as g grows) is unstable where the phantom falls, at "
      "growth rate^2 = (2 + 2/n) G M/r^3 -- the local orbital rate -- independent of how small the tail is",
      f"rate^2 = {rate2} (symbolic, matches {rate2_ok}); 1 AU e-folding {efold_AU/86400:.0f} d; Milky Way "
      f"inside the nu_RAR peak: {m5_nums['canonical']['efold_Myr_at_1_2_3kpc']} Myr at 1/2/3 kpc",
      rate2_ok,
      "the instability rearranges a conserved phantom, so its weight is set by how much phantom sits where the tail "
      "falls: for nu_RAR that is the inner Milky Way (e-folding 1-4 Myr at 1-3 kpc); pushing the fall to g >~ 1e3 a0 "
      "makes the rearranged mass negligible, but a monotone tail up to there is what the ephemerides bound (L340 S1: "
      "nu_mono's unfiltered tail is 1.9e4 x over) -- the record's Cassini-versus-ghost pincer returns as a "
      "stability condition, and BS24 has no heat filter (C-H/K's escape, L340 S1)")

# ============================================================================================ M6
banner("M6  HOW FAR THE PHANTOM FOLLOWS A CHANGE OF VELOCITY: r_follow where omega_L(r) r = du")
P("    deep MOND (f = y): omega_L^2 = 4 pi G rho_tau (2y)/(1 - 2y) -> 2 G M_b / r^3  => r_follow = 2 G M_b / du^2 (a0-free)")
masses = {"dwarf 1e8": 1e8, "dwarf 1e9": 1e9, "Milky Way 6e10": 6e10, "group 1e12": 1e12, "cluster 1e14": 1e14}
dus = [100, 300, 620, 1000, 3000]
m6 = {}
for lab, Mb in masses.items():
    row = {du: 2 * G * Mb * MSUN / (du * 1e3)**2 / KPC for du in dus}
    m6[lab] = {str(k_): round(v, 3) for k_, v in row.items()}
    P(f"    {lab:15s} r_follow [kpc] at du = " + ", ".join(f"{du}: {row[du]:9.3f}" for du in dus) + " km/s")
# the same with the full nu_RAR profile for the Milky Way (both footings), where omega_L is real (outside the peak)
for foot, a0 in A0.items():
    r = np.logspace(math.log10(6 * KPC), math.log10(3000 * KPC), 6000)
    gN = G * MB / r**2; h = (nu_rar(gN / a0) - 1.0) * gN
    rho = np.gradient(r**2 * h, r) / (4 * np.pi * G * r**2)
    fL = 1.0 / (1.0 + np.gradient(h, gN))
    omL = np.sqrt(np.clip(4 * np.pi * G * rho * fL / (1.0 - fL), 0, None))
    rf = {}
    for du in dus:
        ok_ = omL * r >= du * 1e3
        rf[du] = round(float(r[ok_].max() / KPC), 2) if ok_.any() else None
    P(f"    {foot:9s} Milky Way, full nu_RAR profile: r_follow [kpc] = {rf}")
    m6["MW_nuRAR_" + foot] = {str(k_): v for k_, v in rf.items()}
OUT["numbers"]["M6"] = m6
mw_deep = 2 * G * MB / (620e3)**2 / KPC
check("M6 (a prediction, not a test) a galaxy whose velocity relative to its own phantom changes by du keeps the "
      "phantom only inside r_follow ~ 2 G M_b/du^2: 1.4 kpc for the Milky Way at 620 km/s, 860 kpc for a 1e14 "
      "Msun cluster at 1000 km/s",
      f"MW at 620 km/s: {mw_deep:.2f} kpc (deep-MOND formula); cluster 1e14 at 1000 km/s: "
      f"{2*G*1e14*MSUN/(1e6)**2/KPC:.0f} kpc",
      True,
      "uniform motion costs nothing (M3); what costs is a CHANGE of velocity relative to the fluid, as in an "
      "encounter or a merger, and any flow that needs two velocities at one point: the fluid is single-valued and "
      "irrotational (v = -grad sigma), so interpenetrating halos (the Bullet Cluster) are outside its PN description",
      load_bearing=False)

# ============================================================================================ M7
banner("M7  IN THE LINEAR DEEP-MOND REGIME THE FLUID DOES NOT FEEL ITS OWN GRAVITY ON SCALES BELOW 1/mu")
kk, a_, rb, cad2, wq = sp.symbols('k a rhobar c_ad2 w', positive=True)
Xi_k = -fourpiG * sp.Symbol('drho') / (kk**2 + mus**2)             # eq. 27a with J_Y = -1 (Y second order)
phi_tau_k = -fourpiG * sp.Symbol('drho') / kk**2                   # the fluid's own Newtonian potential
ratio_self = sp.simplify(Xi_k / phi_tau_k)
lim_small = sp.limit(ratio_self, kk, sp.oo)
lim_large = sp.limit(ratio_self, kk, 0)
# BS24 eq. 71: c_s^2 = c_ad^2 / (1 + c_ad^2 k^2 / (4 pi G a^2 rhobar (1+w)));  c_s^2 k^2/a^2 -> 4 pi G rhobar (1+w)
cs2 = cad2 / (1 + cad2 * kk**2 / (fourpiG * a_**2 * rb * (1 + wq)))
lim_cs = sp.limit(cs2 * kk**2 / a_**2, kk, sp.oo)
P(f"    Xi / phi_tau = {ratio_self}:  -> {lim_small} for k >> mu (self-gravity cancelled), -> {lim_large} for k << mu")
P(f"    BS24 eq. 71: c_s^2 k^2/a^2 -> {lim_cs} as k -> inf  (their pressure term cancels the self-gravity term exactly)")
P(f"    late universe (quadratic regime): k_J^2 = 4piG a^2 rhobar/c_ad^2 = a^2 mu^2 -> the physical Jeans length is 1/mu,")
P(f"    independent of how small w is (BSX1 computes the consequence for the web's field and sigma_8)")
m7_ok = (lim_small == 1) and (lim_large == 0) and sp.simplify(lim_cs - fourpiG * rb * (1 + wq)) == 0
OUT["numbers"]["M7"] = {"Xi_over_phi_tau": str(ratio_self), "cs2k2_limit": str(lim_cs)}
check("M7 with J_Y = -1 (linear, deep MOND) the Euler force -grad phi + grad Xi on the fluid cancels its own gravity "
      "for k >> mu (Xi -> phi_tau) and keeps it for k << mu; BS24's eq. 71 is the same statement",
      f"Xi/phi_tau -> {lim_small} (k >> mu), {lim_large} (k << mu); c_s^2 k^2/a^2 -> {lim_cs}",
      m7_ok,
      "consequences (BSX1): the fluid clusters under baryons only below 1/mu at late times, and the aether's "
      "acceleration in the web -- the MOND function's external field -- is the fluid's own potential gradient there")

# ============================================================================================ VERDICT
banner("VERDICT")
n_ok = sum(1 for _, ok, _ in CH if ok); n_lb_fail = sum(1 for _, ok, lb in CH if (not ok) and lb)
P("""  BS24's extra sector is shift-free and time-derivative-free in unitary gauge (M1), the class in which L330 found
  a frozen phantom -- but only at linear order about flat space.  From BS24's own PN equations the phantom is a
  conserved fluid carried by the aether's flow (M2): about a galaxy the transport is first order, and a galaxy
  moving uniformly with its phantom is an exact solution (M3).  The moving-source gate is PASSED in L330's sense.
  What the passage costs:
   (1) the phantom is conserved, never generated by baryons: every galaxy must ASSEMBLE its phantom from the cosmic
       khronon dust (BS24's dark matter), as a CDM halo is assembled;
   (2) it responds to a change of velocity only on its local dynamical time (M4: omega^2 = 4 pi G rho_tau
       f_th/(1 - f_th), k-independent), so it keeps up only inside r_follow ~ 2 G M_b/du^2 (M6); interpenetrating
       flows (mergers) are outside the single-valued irrotational description;
   (3) the static MOND halo is a stable state of the fluid only for a monotone phantom law (M5a); BS24's own GR
       recovery (eq. 40) makes the phantom fall, and wherever it falls the fluid is unstable at the local
       orbital rate, whatever the tail's amplitude (M5b).  For nu_RAR the fall is inside galaxies (Milky Way
       e-folding 1-4 Myr at 1-3 kpc); moving it to g >~ 1e3 a0 hides the instability but meets the ephemeris
       bound on a monotone tail: the record's Cassini-versus-ghost pincer, as a stability condition, no filter.
  M7 hands BSX1 the web: below 1/mu the late fluid feels only the baryons' gravity, and the aether's acceleration
  there (the MOND function's external field) is the fluid's own potential gradient.""")
P(f"\n  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
sys.exit(1 if n_lb_fail else 0)
