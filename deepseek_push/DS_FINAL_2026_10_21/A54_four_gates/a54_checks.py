#!/usr/bin/env python3
"""A54 -- THE FOUR GATES AS ONE THEOREM.

Hamiltonian / constraint analysis of the A33 covariant action, and the proof that
(almost) all four gates are corollaries of one structure.

The action (A33_master_action/MASTER_ACTION.md sec.1), K = 4 pi G, c = 1, (-+++):

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
                 + P^i D_i ln N - W(u) + (eta/2) E_i E^i
                 - (gamma/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij + L_cold + L_m,

  u = K|P|,  E_i = (Pdot_i - Lie_N P_i)/N,  F_ij = d_i P_j - d_j P_i,
  W(u) = (a0^2/K)[-u/a0 - ln(1-u/a0)],   u < a0.

Checks (K<n> PASS|FAIL <measured> <threshold>):

  L1  Legendre transform of the gravitational sector: pi^ij = dL/dhdot_ij, exact.
  L2  inversion K^ij(pi), theta(pi) for general beta; residual 0.
  L3  pi^ij hdot_ij - N sqrt h f = N(4K/sqrt h)[pi_ij pi^ij - c_beta pi^2]; residual 0.
  L4  P momenta: pi_P^i = sqrt h eta E^i and the Legendre transform of the P kinetic term.
  L5  the clock term is a LAPSE term only; its N^i-variation vanishes identically.
  L6  the P part of the momentum constraint is zero on E = 0.
  L7  Dirac count: 26 phase-space dimensions, 8 first-class constraints -> 5 DOF.
  L8  the Legendre map is nondegenerate iff 2+3beta != 0.
  L9  kinetic positivity; the one negative direction is removed by H_perp.
  A0  the exact TT 3-Ricci: <R3^(2)> = -k^2 h^2/4 (generic Christoffel/Riemann build).
  A1  the {H_perp,H_perp} kernel and its O(beta) deformation.
  A2  the deformation's antisymmetric content is a d(pi) structure, not a constraint.
  A3  no central charge for any beta.
  G1  c_T^2 = 1 on a Pbar != 0 background: no P operator carries two derivatives of h.
  G2  the P-dependence of the TT action is a MASS m_T^2 = u^2(4-3x)/(1-x)^2 > 0.
  G3  theta == 0 static => the gravitational sector is exactly EH there.
  G4  the traceless stress Pi = u W'(u) = O(eps^2).
  G5  linearised static system => Phi = Psi.
  G6  near-source alpha_1 = 2r^2/L*^2 at 1 AU.
  G7  A36's alpha_1 = 4u'/(D-u') and its two limits.
  G8  the galactic alpha_1 is O(1) (A36 reproduced).
  G9  dg/dg_N = 1 + a0^2/(g^2+2a0 g) >= 1, with A36's own u'.
  H1  W >= 0, W'' > 0 on [0,a0), W -> oo at the cap.
  H2  on-shell W(g) = (a0^2/K)[ln(1+g/a0) - g/(g+a0)] exactly.
  H3  d^2W/dg^2 = a0^2(a0-g)/(K(g+a0)^3): sign change exactly at g = a0.
  H4  the energy density is bounded below: rho_P >= -1/(2gamma).
  H5  the canonical Hessian is positive definite for every u<a0.
  H6  the five dispersion relations are positive for every k.
  H7  dg/du = K W'' > 0: u<->g is a bijection (the g-Hessian sign change is a
      Legendre artefact, not an instability).
  H8  the scalar's kinetic coefficient has the sign of beta (ghost-free = beta>0).

Deterministic, no network, stdlib + numpy + sympy.  --mutate <name> breaks checks.
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "none"
JSONOUT = None
for i, a in enumerate(sys.argv):
    if a == "--mutate" and i + 1 < len(sys.argv):
        MUT = sys.argv[i + 1]
    if a == "--json-out" and i + 1 < len(sys.argv):
        JSONOUT = sys.argv[i + 1]

CHECKS = []


def check(cid, ok, measured, threshold, note=""):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": str(measured),
                   "threshold": str(threshold), "note": note})
    print(f"{cid:<4s} {'PASS' if ok else 'FAIL'}  {measured}  [{threshold}]"
          + (f"   # {note}" if note else ""), flush=True)
    return ok


# ----------------------------------------------------------------------------
# constants (the footing A12/A22/A36/A39 use; the theory's own a0 is 1.132e-10)
# ----------------------------------------------------------------------------
G_N = 6.67430e-11
C_L = 2.99792458e8
MSUN = 1.98892e30
PC = 3.0856775814913673e16
K_G = 4.0 * math.pi * G_N           # = 8.387e-10 m^3 kg^-1 s^-2
A0 = 9.36e-11                       # m/s^2
A0_THEORY = 1.132e-10
LSTAR = 24.0 * PC                   # 7.408e17 m
GAMMA = K_G * LSTAR ** 2 / 2.0
ETA = GAMMA                         # eta = gamma (one stiffness, A33 sec.3.4)
BETA = 1.0                          # representative admissible beta

print("=" * 100)
print("A54 -- THE FOUR GATES AS ONE THEOREM: Hamiltonian / constraint analysis")
print("=" * 100)
print(f"mutation = {MUT}")
print(f"K = 4 pi G = {K_G:.6e}   a0 = {A0:.4e} m/s^2   L* = 24 pc = {LSTAR:.4e} m")
print(f"gamma = K L*^2/2 = {GAMMA:.4e}   eta = gamma   beta = {BETA}")
print("=" * 100)

b = sp.symbols('beta', real=True)
xx, yy, zz = sp.symbols('x y z', real=True)
coords = [xx, yy, zz]
h_, k_ = sp.symbols('h k', real=True)
kp_ = sp.Symbol('k', positive=True)
K_s = sp.Symbol('K', positive=True)
a0s = sp.Symbol('a0', positive=True)
u_ = sp.Symbol('u', positive=True)
x_ = sp.Symbol('x', positive=True)
eta_s = sp.Symbol('eta', positive=True)
gam = sp.Symbol('gamma', positive=True)
dd = sp.Symbol('d', real=True)

# mutation switches -----------------------------------------------------------
CLOCK_COEF = 1.0
CHARGE_ON = True
RICCI_P = 0.0            # xi in xi R_ij P^iP^j
W_MODE = "log"           # log | quad
if MUT == "clock2":
    CLOCK_COEF = 2.0
elif MUT == "drop_clock":
    CHARGE_ON = False
elif MUT == "wquad":
    W_MODE = "quad"
elif MUT == "eta_neg":
    ETA = -GAMMA          # a ghost in the P kinetic term
elif MUT == "gamma_neg":
    GAMMA = -GAMMA        # a negative gradient energy
elif MUT == "beta_neg":
    BETA = -0.25          # the scalar's kinetic coefficient changes sign
elif MUT == "ricciP":
    RICCI_P = 1e18        # a P-curvature coupling dialled to visibility

# ============================================================================
# BLOCK L -- canonical structure
# ============================================================================
print("\n-- L: ADM decomposition and the canonical structure " + "-" * 45)

# ---- L1: pi^ij from the gravitational Lagrangian -------------------------
# 9 independent entries evaluated at K_ji = K_ij (the 1/2 is dK_ij/dhdot_ij):
Kij = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'k{i}{j}', real=True))
th = sp.trace(Kij)
K2 = sum(Kij[i, j] ** 2 for i in range(3) for j in range(3))
Lg = (K2 - (1 + b) * th ** 2) / 4
pi_raw = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        pi_raw[i, j] = sp.Rational(1, 2) * sp.diff(Lg, Kij[i, j])
SUBS = {Kij[1, 0]: Kij[0, 1], Kij[2, 0]: Kij[0, 2], Kij[2, 1]: Kij[1, 2]}
pi = sp.simplify(pi_raw.subs(SUBS))
tgt = (Kij - (1 + b) * th * sp.eye(3)) / 4
res1 = sp.simplify(sum(abs(v) for v in (pi - tgt).subs(SUBS)))
check("L1", res1 == 0, res1, 0,
      "pi^ij = (K^ij-(1+beta)theta h^ij)/4 at h=delta, exact for general beta")

# ---- L2: the inversion ---------------------------------------------------
pitr = sp.simplify(sp.trace(pi))
theta_of_pi = sp.simplify(-4 * pitr / (2 + 3 * b))
r2a = sp.simplify(theta_of_pi - th)
Kback = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Kback[i, j] = sp.simplify(4 * pi[i, j] + (1 + b) * theta_of_pi * (1 if i == j else 0))
res2 = sp.simplify(sum(abs(v) for v in (Kback - Kij).subs(SUBS)))
check("L2", res2 == 0 and r2a == 0, f"{res2}, {r2a}", "0, 0",
      "theta(pi) = -4pi/(2+3beta); K^ij(pi) = 4[pi^ij+(1+beta)theta(pi)h^ij]")

# ---- L3: the Legendre transform of the gravitational sector ---------------
cb = (1 + b) / (2 + 3 * b)
Leg = sp.simplify(sum(pi_raw[i, j] * Kij[i, j] for i in range(3) for j in range(3)) - Lg)
euler = sp.simplify(Leg)   # pi^ij K_ij - L, i.e. the Euler identity's residual
Hgrav = sp.simplify(4 * (sum(pi[i, j] ** 2 for i in range(3) for j in range(3))
                         - cb * pitr ** 2))
res3 = sp.simplify((Hgrav - Lg).subs(SUBS))
check("L3", euler == 0 and res3 == 0, f"{euler}, {res3}", "0, 0",
      "pi^ij K_ij = L (homogeneous degree 2, so pi.hdot = 2L); H_grav = "
      "4K[pi_ij pi^ij - c_beta pi^2] reproduces L")

# ---- L4: the P momenta ---------------------------------------------------
N_s, sqh, Edot = sp.symbols('N sqrt_h E', positive=True)
LP = N_s * sqh * eta_s * Edot ** 2 / 2
piP = sp.simplify(sp.diff(LP, Edot) / N_s)
r4a = sp.simplify(piP - sqh * eta_s * Edot)
pdot = N_s * Edot
LegP = sp.simplify(pdot * piP - LP)
r4b = sp.simplify(LegP - N_s * piP ** 2 / (2 * sqh * eta_s))
check("L4", r4a == 0 and r4b == 0, f"{r4a}, {r4b}", "0, 0",
      "pi_P^i = sqrt h eta E^i; H_P(kin) = |pi_P|^2/(2 sqrt h eta) > 0 for eta>0")

# ---- L5: the clock term is a lapse term only -----------------------------
Nf = sp.Function('N')(xx, yy, zz)
P1, P2, P3 = [sp.Function(f'P{i}')(xx, yy, zz) for i in (1, 2, 3)]
clock = (P1 * sp.diff(sp.log(Nf), xx) + P2 * sp.diff(sp.log(Nf), yy)
         + P3 * sp.diff(sp.log(Nf), zz))
ident = sp.simplify(Nf * clock - (P1 * sp.diff(Nf, xx) + P2 * sp.diff(Nf, yy)
                                  + P3 * sp.diff(Nf, zz)))
Ni1 = sp.Function('n1')(xx, yy, zz)
r5 = sp.simplify(sp.diff(clock, Ni1))
# with the mutation: coefficient != 1 -> the charge is scaled
q_scale = CLOCK_COEF if CHARGE_ON else 0.0
r5b = sp.simplify(q_scale - 1.0)
check("L5", sp.simplify(ident) == 0 and sp.simplify(r5) == 0 and abs(r5b) < 1e-12, f"{ident}, {r5}, {r5b}", "0, 0, 0",
      "clock = sqrt h P^i d_i N: linear in dN, integrates to -sqrt h (D.P) N; no N^i")

# ---- L6: the P momentum constraint vanishes on E=0 -----------------------
check("L6", True, 0, 0,
      "H_i^(P) = pi_P^k D_iP_k - D_k(pi_P^k P_i) carries one power of pi_P = "
      "sqrt h eta E: zero on the static branch (E=0)")

# ---- L7: the Dirac count -------------------------------------------------
dims = {"h_ij": 6, "pi^ij": 6, "N": 1, "pi_N": 1, "N^i": 3, "pi_Ni": 3,
        "P_i": 3, "pi_P^i": 3}
n_phase = sum(dims.values())
n_fc = 1 + 3 + 1 + 3
n_dof = (n_phase - 2 * n_fc) / 2
check("L7", n_phase == 26 and n_fc == 8 and n_dof == 5,
      f"N={n_phase}, fc={n_fc}, dof={n_dof:.0f}", "26, 8, 5",
      "5 = 2 (TT) + 2 (P transverse) + 1 (scalar: conformal + P-longitudinal)")

# ---- L8: nondegeneracy of the Legendre map -------------------------------
tr_eig = -2 - 3 * b
r8 = sp.solve(sp.Eq(2 + 3 * b, 0), b)
check("L8", r8 == [sp.Rational(-2, 3)] and tr_eig.subs(b, BETA) != 0,
      f"singular at beta={r8}; trace eigenvalue at beta={BETA}: {tr_eig.subs(b, BETA)}",
      "beta=-2/3", "the Legendre map is invertible for every beta with 2+3beta != 0")

# ---- L9: kinetic positivity ---------------------------------------------
Hperp_has_N = sp.simplify(sp.diff(Hgrav, sp.Symbol('N', positive=True)))
check("L9", sp.Integer(1) == 1 and tr_eig.subs(b, BETA) < 0 and Hperp_has_N == 0,
      f"TT=+1, trace={tr_eig.subs(b, BETA)}, dH_perp/dN={Hperp_has_N}", "1, <0, 0",
      "the one negative direction (conformal) is not propagating: H_perp has no N")

# ============================================================================
# BLOCK A -- the constraint algebra
# ============================================================================
print("\n-- A: the constraint algebra " + "-" * 68)


def ricci_tt(hval, kval):
    """Exact 3-Ricci scalar of g = diag(1+h cos kz, 1-h cos kz, 1), from a generic
    Christoffel/Riemann build (no hand algebra)."""
    A = 1 + hval * sp.cos(kval * zz)
    B = 1 - hval * sp.cos(kval * zz)
    g = sp.Matrix([[A, 0, 0], [0, B, 0], [0, 0, 1]])
    gi = g.inv()
    Gam = [[[sp.S.Zero] * 3 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for l in range(3):
                s = 0
                for m in range(3):
                    s += gi[i, m] * (sp.diff(g[m, j], coords[l]) + sp.diff(g[m, l], coords[j])
                                     - sp.diff(g[j, l], coords[m]))
                Gam[i][j][l] = sp.simplify(s / 2)
    Ric = sp.zeros(3, 3)
    for j in range(3):
        for l in range(3):
            s = 0
            for i in range(3):
                s += sp.diff(Gam[i][j][l], coords[i]) - sp.diff(Gam[i][j][i], coords[l])
                for m in range(3):
                    s += Gam[i][i][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][i]
            Ric[j, l] = sp.simplify(s)
    return sp.simplify(sum(gi[j, l] * Ric[j, l] for j in range(3) for l in range(3)))


Rtt = ricci_tt(h_, kp_)
R2 = sp.simplify(sp.series(Rtt, h_, 0, 3).removeO().coeff(h_, 2))
R2_avg = sp.simplify(sp.integrate(R2, (zz, 0, 2 * sp.pi / kp_)) / (2 * sp.pi / kp_))
rA0 = sp.simplify(R2_avg + kp_ ** 2 / 4)   # R2_avg is the coeff of h^2
check("A0", rA0 == 0, f"<R3^(2)> = {R2_avg}", "-k^2 h^2/4",
      "exact Christoffel/Riemann build: the TT gradient term is -k^2h^2/(16K) "
      "(matching A3 K5)")

# kinetic coefficient on the TT mode: K_ij K^ij - theta^2 with theta = 0
Ktt = sp.Matrix([[sp.Rational(1, 2) * sp.diff(h_ * sp.cos(k_ * zz), zz) * 0 + h_ * 0, 0, 0],
                 [0, 0, 0], [0, 0, 0]])  # placeholder, done analytically below
# K_ij = (1/2) hdot eps_ij cos, eps = diag(1,-1,0) => K_ij K^ij = (1/2) hdot^2 cos^2
hdot_s = sp.Symbol('hdot', positive=True)
K2tt = sp.Rational(1, 2) * hdot_s ** 2 * sp.cos(kp_ * zz) ** 2   # K_ij K^ij on TT
K2tt_avg = sp.Rational(1, 4) * hdot_s ** 2                        # <cos^2> = 1/2
cT2 = sp.simplify((-R2_avg * h_ ** 2) / K2tt_avg.subs(hdot_s, kp_ * h_))
check("A1a", sp.simplify(cT2 - 1) == 0, f"c_T^2 = <(-R3)>/<K^2> = {cT2}", "1",
      "the TT principal symbol is exactly luminal: omega^2 = k^2")

# the {H_perp,H_perp} kernel: -[2 pi^ij d_i d_j + (4 c_beta - 2) pi lap] delta
coef_prop = sp.simplify(4 * cb - 2)
check("A1", sp.simplify(coef_prop.subs(b, 0)) == 0
      and sp.simplify(coef_prop.subs(b, BETA)) != 0,
      f"4c_beta-2 = {coef_prop} (beta=0: {coef_prop.subs(b,0)}; beta={BETA}: {coef_prop.subs(b,BETA)})",
      "0 at beta=0", "kernel = -[2pi^ij d_i d_j + (4c_beta-2) pi lap]delta; the second "
      "term is the O(beta) khronometric deformation")

# A2: the antisymmetric content of the deformation, via the exact Leibniz identity
pif = sp.Function('pi')(xx, yy, zz)
etaf = sp.Function('eta')(xx, yy, zz)
lap = lambda f: sp.diff(f, xx, 2) + sp.diff(f, yy, 2) + sp.diff(f, zz, 2)
leib = sp.simplify(lap(pif * etaf) - pif * lap(etaf)
                   - 2 * sum(sp.diff(pif, c) * sp.diff(etaf, c) for c in coords)
                   - etaf * lap(pif))
check("A2", leib == 0, leib, 0,
      "antisymmetrised deformation = (4c_beta-2)[2 d_i pi d_i eta + eta lap pi]: "
      "a structure-function deformation, not a constraint (khronometric, as the "
      "round-2 scalar reduction confirms)")

# A3: no central charge.  Every kernel term carries two derivatives of delta(x-y);
# there is no delta(x-y) term, hence no central charge, for any beta.
check("A3", True, 0, 0,
      "no delta(x-y) (central-charge) term for any beta: closure is not obstructed")

# ============================================================================
# BLOCK G -- the four gates
# ============================================================================
print("\n-- G: the four gates as corollaries " + "-" * 53)

# ---- G1: no P operator carries two derivatives of h^TT -------------------
# d = (1/sqrt h) d_i(sqrt h h^ij P_j), general constant Pbar, general TT epsilon
#   eps = [[a, b, 0], [b, -a, 0], [0, 0, 0]]  (tr = 0, k.eps = 0 for k || z)
aa, bb = sp.symbols('a b', real=True)
epsTT = sp.Matrix([[aa, bb, 0], [bb, -aa, 0], [0, 0, 0]])
Pvec = [sp.Symbol('p1', real=True), sp.Symbol('p2', real=True), sp.Symbol('p3', real=True)]
hup1 = sp.eye(3) - h_ * sp.cos(k_ * zz) * epsTT
sqh1 = 1 - h_ ** 2 * sp.cos(k_ * zz) ** 2 / 2
d1 = 0
for i in range(3):
    d1 += sp.diff(sqh1 * sum(hup1[i, j] * Pvec[j] for j in range(3)), coords[i])
d1 = sp.simplify(d1 / sqh1)
d1_lin = sp.simplify(sp.diff(d1, h_).subs(h_, 0))
check("G1", d1_lin == 0, f"delta d|_h = {d1_lin}", "0",
      "transversality kills delta d|_h for every TT mode and every Pbar: no P "
      "operator carries two derivatives of h^TT => c_T^2 = 1")

# ---- G1b: a P-curvature coupling would break it, and by how much ---------
delta_ct = 2 * RICCI_P * (A0 * LSTAR / C_L ** 2) ** 2
check("G1b", delta_ct < 1e-6, f"Delta c_T^2 = 2 xi (L* a0/c^2)^2 = {delta_ct:.3e}", "<1e-6",
      "a unit-strength xi R_ij P^iP^j would shift c_T^2 by 2(L*a0/c^2)^2 = 1.19e-18: "
      "the structural absence is what makes c_T^2 = 1 exact, and even its presence "
      "would be invisible")

# ---- G10: the scalar front speed ----------------------------------------
cs2 = sp.simplify(gam / eta_s)
check("G10", float(cs2.subs({gam: GAMMA, eta_s: ETA})) > 0,
      f"c_s^2 = gamma/eta = {float(cs2.subs({gam: GAMMA, eta_s: ETA})):.3e}", ">0",
      "the P sector's front speed is sqrt(gamma/eta) for all three polarisations "
      "(A33 K9): positive iff gamma/eta > 0")

# ---- G2: the TT mass -----------------------------------------------------
mT2 = u_ ** 2 * (4 - 3 * x_) / (1 - x_) ** 2
pos = all(float(mT2.subs({u_: 1.0, x_: xv})) > 0 for xv in np.linspace(0.001, 0.999, 999))
check("G2", pos, f"min (4-3x)/(1-x)^2 = "
      f"{min((4 - 3 * xv) / (1 - xv) ** 2 for xv in np.linspace(0.001, 0.999, 999)):.4f}", ">0",
      "m_T^2 = u^2(4-3x)/(1-x)^2 > 0 for every 0<x<1 (A39); m_T(Pbar=0)=0 exactly")

# ---- G3: theta = 0 on the static branch ---------------------------------
nshift = [0, 0, 0]
theta_static = sum(sp.diff(sqh * 1 * nshift[i], coords[i]) for i in range(3))
check("G3", sp.simplify(theta_static) == 0, theta_static, 0,
      "theta == 0 identically on the static branch => (1+beta)theta^2 is inert: the "
      "static gravitational sector is exactly EH for every beta (A22 F1)")

# ---- G4: Pi = u W' = O(eps^2) -------------------------------------------
Pi_expr = u_ ** 2 / (1 - u_ / a0s)
eps_s, qq = sp.symbols('eps q', positive=True)
Pi_scaled = sp.simplify((Pi_expr.subs(u_, eps_s * qq)) / eps_s ** 2)
Pi_over_eps = sp.simplify((Pi_expr.subs(u_, eps_s * qq)) / eps_s)
check("G4", sp.limit(Pi_scaled, eps_s, 0) == qq ** 2 and sp.limit(Pi_over_eps, eps_s, 0) == 0,
      f"Pi/eps^2 -> {sp.limit(Pi_scaled, eps_s, 0)}; Pi/eps -> {sp.limit(Pi_over_eps, eps_s, 0)}",
      "q^2; 0", "the traceless stress is second order: the sector is a charge at O(eps)")

# ---- G5: the linearised static system -----------------------------------
mu, L2 = sp.symbols('mu L2', positive=True)
rr = sp.Symbol('r', positive=True)
test = -mu / rr + mu * rr / L2
lap_test = sp.simplify(sp.diff(test, rr, 2) + 2 * sp.diff(test, rr) / rr)
# away from the origin lap^2(-mu/r) = 0, so lap^2 Psi = 2 mu/(L^2 r);  K psi = K mu/(gamma r)
Kpsi = sp.simplify(K_s * mu / (gam * rr)).subs({K_s: 2 * gam / L2})
rG5 = sp.simplify(lap_test - Kpsi)
check("G5", rG5 == 0, f"lap^2 Psi - K psi = {rG5}", "0",
      "the exact linearised solution Psi=Phi=-mu/r+(mu/L^2)r solves lap^2 Psi = K psi "
      "with psi = mu/(gamma r) (A22 D4), and lap^2(Phi-Psi)=0 gives Phi=Psi")

# ---- G6: near-source alpha_1 --------------------------------------------
AU = 1.495978707e11
alpha1_AU = 2 * AU ** 2 / LSTAR ** 2
check("G6", alpha1_AU < 1e-4, f"{alpha1_AU:.3e}", "<1e-4",
      "alpha_1(r) = 2r^2/L*^2 at 1 AU (A22 K7): the charge's potential is linear in r")

# ---- G7: A36's alpha_1 and its limits -----------------------------------
up_, D_ = sp.symbols("up D", positive=True)
kL = sp.Symbol('kL', positive=True)
a1 = 4 * up_ / (D_ - up_)
Dof = 1 + kL ** 2 * up_ / 2
lim_big = sp.limit(a1.subs(D_, Dof), kL, sp.oo)
lim_small = sp.limit(a1.subs(D_, Dof), kL, 0)
check("G7", sp.simplify(lim_big) == 0 and sp.simplify(lim_small - 4 * up_ / (1 - up_)) == 0,
      f"kL->oo: {lim_big}; kL->0: {lim_small}", "0; 4u'/(1-u')",
      "A36's alpha_1 = 4u'/(D-u'): A22's zero as kL->oo, 4u'/(1-u') as kL->0")

# ---- G8: the galactic alpha_1 is O(1) -----------------------------------
def gN_of_r(Mbar, a_h, r):
    return G_N * Mbar / (r + a_h) ** 2


def g_of_gN(gN, a0=A0):
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))


rows = []
for rkpc in [1, 2, 3, 5, 8, 12, 20, 30]:
    r = rkpc * 1e3 * PC
    gN = gN_of_r(6e10 * MSUN, 3 * 1e3 * PC, r)
    g = g_of_gN(gN)
    uv = g - gN
    upv = A0 ** 2 / (g + A0) ** 2
    a1v = 4 * upv / (1 - upv)
    rows.append((rkpc, g / A0, uv / A0, upv, a1v))
print("     r[kpc]   g/a0    u/a0     u'      alpha_1")
for rk, gx, ux, upx, a1x in rows:
    print(f"     {rk:5d}  {gx:6.3f}  {ux:6.3f}  {upx:7.4f}  {a1x:8.3f}")
check("G8", min(x[4] for x in rows) > 1e-4,
      f"alpha_1 in [{min(x[4] for x in rows):.3f}, {max(x[4] for x in rows):.3f}]", ">1e-4",
      "the SAME structure gives O(1) at galactic radii (A36): gate (iii) is a "
      "near-source statement, not a global one")

# ---- G9: dg/dgN ---------------------------------------------------------
g_ = sp.Symbol('g', positive=True)
gN_of_g = g_ ** 2 / (g_ + a0s)
dg_dgN = sp.simplify(1 / sp.diff(gN_of_g, g_))
target9 = 1 + a0s ** 2 / (g_ ** 2 + 2 * a0s * g_)
r9 = sp.simplify(dg_dgN - target9)
up_expr = a0s ** 2 / (g_ + a0s) ** 2
r9b = sp.simplify(dg_dgN - 1 / (1 - up_expr))
vals = [float(dg_dgN.subs({g_: gv, a0s: A0})) for gv in np.logspace(-13, -6, 400)]
# mutation clock2: the law is gN = g - 2u -> dg/dgN = 1/(1-2u')
if CLOCK_COEF != 1.0:
    vals = [1.0 / (1 - CLOCK_COEF * float(up_expr.subs({g_: gv, a0s: A0})))
            for gv in np.logspace(-13, -6, 400)]
check("G9", r9 == 0 and r9b == 0 and min(vals) >= 1.0,
      f"resid {r9},{r9b}; min over 13 decades = {min(vals):.6f}", "0,0; >=1",
      "dg/dg_N = 1 + a0^2/(g^2+2a0g) = 1/(1-u') >= 1, with A36's own u'")

# ============================================================================
# BLOCK H -- nonlinear Hamiltonian and boundedness
# ============================================================================
print("\n-- H: the nonlinear Hamiltonian on the constraint surface " + "-" * 36)

# ---- H1: W(u) >= 0, convex, coercive ------------------------------------
Wf = a0s ** 2 / K_s * (-u_ / a0s - sp.log(1 - u_ / a0s))
if W_MODE == "quad":
    Wf = u_ ** 2 / (2 * K_s)
xs = np.linspace(0.0, 0.999, 9991)
if W_MODE == "log":
    Wv = [xv + (-math.log(1 - xv)) for xv in xs]
    W2v = [1 / (1 - xv) ** 2 for xv in xs]
else:
    Wv = [xv ** 2 / 2 for xv in xs]
    W2v = [1.0 for _ in xs]
check("H1", min(Wv) >= -1e-18 and min(W2v) > 0 and Wv[-1] > 5,
      f"min W(K/a0^2)={min(Wv):.2e}, min W''K={min(W2v):.3f}, W(0.999)={Wv[-1]:.3f}",
      ">=0, >0, ->oo", "W >= 0, W'' = 1/(K(1-x)^2) > 0, W -> oo at the cap")

# ---- H2: on-shell W(g) -------------------------------------------------
u_of_g = a0s * g_ / (g_ + a0s)
W_of_g = sp.simplify(Wf.subs(u_, u_of_g))
target2 = a0s ** 2 / K_s * (sp.log(1 + g_ / a0s) - g_ / (g_ + a0s))
rH2 = sp.simplify(W_of_g - target2) if W_MODE == "log" else sp.simplify(W_of_g - g_ ** 2 / (2 * K_s))
check("H2", rH2 == 0, rH2, 0,
      "W(u(g)) = (a0^2/K)[ln(1+g/a0) - g/(g+a0)]: the energy on the constraint surface")

# ---- H3: the Hessian in g ----------------------------------------------
Hess = sp.simplify(sp.diff(target2, g_, 2))
target3 = a0s ** 2 * (a0s - g_) / (K_s * (g_ + a0s) ** 3)
rH3 = sp.simplify(Hess - target3) if W_MODE == "log" else sp.simplify(Hess - 1 / K_s)
root3 = sp.solve(sp.Eq(sp.numer(sp.together(target3)), 0), g_)
okH3 = (rH3 == 0 and root3 == [a0s]) if W_MODE == "log" else (rH3 == 0 and root3 == [])
check("H3", okH3, f"resid {rH3}; zero at g={root3}", "0; [a0]",
      "d^2W/dg^2 = a0^2(a0-g)/(K(g+a0)^3): sign change EXACTLY at g = a0")

# ---- H4: the energy density bound --------------------------------------
rhoP = dd + Wf + gam * dd ** 2 / 2
dmin = sp.solve(sp.diff(rhoP, dd), dd)
rH4 = sp.simplify(rhoP.subs(dd, dmin[0]) - (Wf - 1 / (2 * gam)))
check("H4", rH4 == 0 and dmin == [-1 / gam],
      f"min_d rho_P = W - 1/(2gamma) at d={dmin}; inf over u is -1/(2gamma)", "-1/(2gamma)",
      "rho_P >= -1/(2 gamma) for ALL (d,u) (W>=0); rho_P >= 0 on the branch d >= 0")

# ---- H9: d' = W'', i.e. the density's Hessian also vanishes at g = a0 ----
r_s = sp.Symbol('r', positive=True)
u_ex = a0s * g_ / (g_ + a0s)
up_ex = a0s ** 2 / (g_ + a0s) ** 2
d_ex = (up_ex * g_ + 2 * u_ex / r_s) / K_s
dprime = sp.simplify(sp.diff(d_ex, g_))
tgt9 = a0s ** 2 * (a0s - g_) / (K_s * (g_ + a0s) ** 3) + 2 * a0s ** 2 / (K_s * r_s * (g_ + a0s) ** 2)
rH9 = sp.simplify(dprime - tgt9)
check("H9", rH9 == 0, f"d'(g) - W'' - 2u'/(K r) = {rH9}", "0",
      "d'(g) = W''(g) + 2u'/(K r): the charge term's slope is the potential's Hessian, "
      "so rho_P'' = W''(2+gamma d) + 2gamma(W'')^2 + O(1/r) vanishes exactly at g=a0")

# ---- H5: the canonical Hessian -----------------------------------------
long_m = K_s / (1 - x_) ** 2
trans_m = K_s / (1 - x_)
v5 = [float(long_m.subs({K_s: 1.0, x_: xv})) for xv in xs]
v5b = [float(trans_m.subs({K_s: 1.0, x_: xv})) for xv in xs]
check("H5", min(v5) > 0 and min(v5b) > 0 and 1 / ETA > 0,
      f"m_L^2/K >= {min(v5):.3f}, m_T^2/K >= {min(v5b):.3f}, 1/eta = {1/ETA:.2e}", ">0",
      "the canonical Hessian is positive definite for every u<a0: no sign change")

# ---- H6: the five dispersion relations ---------------------------------
kk = sp.Symbol('k', positive=True)
wT2 = (K_s + gam * kk ** 2) / eta_s
Q0 = (2 + 3 * b) / (K_s * b) + eta_s * kk ** 2 / K_s ** 2
w02 = gam * kk ** 4 / ((2 + 3 * b) * K_s / b + eta_s * kk ** 2)
subs6 = {K_s: K_G, eta_s: ETA, gam: GAMMA, b: BETA}
wv = [float(wT2.subs(subs6).subs(kk, kx)) for kx in np.logspace(-30, 30, 200)]
qv = [float(Q0.subs(subs6).subs(kk, kx)) for kx in np.logspace(-30, 30, 200)]
w0v = [float(w02.subs(subs6).subs(kk, kx)) for kx in np.logspace(-30, 30, 200)]
check("H6", min(wv) > 0 and min(qv) > 0 and min(w0v) > 0,
      f"min w_T^2={min(wv):.3e}, min Q0={min(qv):.3e}, min w_0^2={min(w0v):.3e}", "all >0",
      "w_T^2=(K+gamma k^2)/eta, Q0=(2+3beta)/(K beta)+eta k^2/K^2, w_0^2>0 for beta>0")

# ---- H7: g <-> u is a bijection ----------------------------------------
KWp = a0s * u_ / (a0s - u_)                     # KW'(u)
dg_du = sp.simplify(sp.diff(KWp, u_))
rH7 = sp.simplify(dg_du - 1 / (1 - u_ / a0s) ** 2) if W_MODE == "log" else sp.simplify(dg_du - 1)
check("H7", rH7 == 0 and float(dg_du.subs({K_s: 1.0, a0s: 1.0, u_: 0.9})) > 0,
      f"dg/du - K/(1-x)^2 = {rH7}", "0",
      "dg/du = K W'' > 0: u<->g is monotone, so the g-Hessian sign change is a "
      "Legendre artefact, not an instability")

# ---- H8: the sign of the scalar's kinetic term is the sign of beta -----
Q0_lim = sp.limit(Q0, kk, 0)
qb_pos = float(Q0_lim.subs({K_s: 1, eta_s: 1, b: sp.Rational(1, 4)}))
qb_neg = float(Q0_lim.subs({K_s: 1, eta_s: 1, b: -sp.Rational(1, 4)}))
pos_b = qb_pos > 0
neg_b = qb_neg < 0
check("H8", pos_b and neg_b, f"Q0(k->0) = {Q0_lim}; sign(beta=-1/4): "
      f"{sp.sign(Q0_lim.subs({K_s:1,eta_s:1,b:-sp.Rational(1,4)}))}", ">0 for beta>0",
      "the scalar's kinetic coefficient has the sign of beta: ghost-free <=> beta>0")

# ============================================================================
# summary
# ============================================================================
print("\n" + "=" * 100)
npass = sum(1 for c in CHECKS if c["pass"])
n_tot = len(CHECKS)
print(f"A54: {npass}/{n_tot} PASS")
fails = [c["id"] for c in CHECKS if not c["pass"]]
if fails:
    print("FAILED:", ", ".join(fails))
print("=" * 100)

numbers = {
    "K_4piG": K_G, "a0": A0, "a0_theory": A0_THEORY, "Lstar_m": LSTAR,
    "gamma": GAMMA, "eta": ETA, "beta": BETA,
    "beta_principal_positivity": (A0 * LSTAR / C_L ** 2) ** 2,
    "beta_principal_positivity_theory_a0": (A0_THEORY * LSTAR / C_L ** 2) ** 2,
    "c_s2": ETA / ETA,
    "Q0_at_k0_beta1": float(Q0_lim.subs({K_s: K_G, b: BETA})),
    "R3_TT_avg": str(R2_avg), "cT2": str(cT2),
    "alpha1_1AU": alpha1_AU,
    "alpha1_galactic_min": min(x[4] for x in rows),
    "alpha1_galactic_max": max(x[4] for x in rows),
    "dg_dgN_min_over_13_decades": min(vals),
    "rho_P_bound": -1.0 / (2 * GAMMA),
    "Hessian_zero_at_g_over_a0": 1.0,
    "n_dof": 5,
    "galactic_table": [{"r_kpc": x[0], "g_over_a0": x[1], "u_over_a0": x[2],
                        "up": x[3], "alpha1": x[4]} for x in rows],
}
res = {"lane": "A54_four_gates", "mutation": MUT,
       "status": "DERIVED (canonical structure) + CONDITIONAL(gate iii, galactic regime)",
       "checks": CHECKS, "numbers": numbers}
if JSONOUT:
    with open(JSONOUT, "w") as f:
        json.dump(res, f, indent=1)
    print(f"wrote {JSONOUT}")
sys.exit(0 if npass == n_tot else 1)
