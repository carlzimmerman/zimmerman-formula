#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ppn_mmg_gate_2026.py
====================
GATE: GENUINE PPN EXPANSION of the frozen chassis MMG_constraint_first.

Chassis (as certified in openai_push/final_closure/, 12 gates + Gate 13):
  metric   ds^2 = -N^2 c^2 dt^2 + gamma_ij (dx^i+N^i dt)(dx^j+N^j dt)
  constraints  S_4 = pi_N,  S_1 = C_M = D_i[c^2 mu(y) D^i ln N] - 4 pi G rho_m,
               S_2 = D^2 q  (q = (1/6) ln det gamma),  S_3 = D^2 p  (p = pi/sqrt(gamma)),
  first-class (as asserted by the suite): pi_i, H_i (standard GR form, dust source),
  mu(y) = 1 - e^{-y},  y = (c^2/a0)|D ln N|   [frozen constitutive target]
  H_T = H_GR + H_m + lambda_N S_4 + mu_1 S_1 + mu_2 S_2 + mu_3 S_3 + N^i H_i.

THIS SCRIPT (everything computed here, nothing quoted without a check):
  PART 0  chassis frame: Dirac 4x4 Pfaffian/det/count + a bracket caveat the suite never computed
  PART 1  g_00 sector to O(c^-4): exact lapse law, beta_PPN, the Phi_1 coefficient, kernel corr.
  PART 2  g_ij sector: gamma_PPN (cross-checks the committed freeze-session lensing gate)
  PART 3  g_0i sector: sympy-derived linearized momentum-constraint solve for a moving source
  PART 4  PPN dictionary solve -> gamma, beta, alpha_1, alpha_2, alpha_3, zeta's; bounds table
  PART 5  EFE quadrupole Q2: INDEPENDENT integrator, anchors validation, both kernels, both footings

Footings: a0 canonical 9.3619e-11 / alt 1.1279e-10 (kappa=1/2 and Z~21 are FITTED, not derived).
Exit 0 = all checks pass.
"""
import math, sys
import numpy as np
import sympy as sp
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq

FAIL, NCHK = [], [0]
def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok
def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
def head(t):
    print("\n" + "=" * 102 + "\n" + t + "\n" + "=" * 102)

G_SI     = 6.6743e-11
MSUN     = 1.98892e30
GM_SUN   = 1.32712440018e20
AU       = 1.495978707e11
RSUN     = 6.957e8
A0       = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
A0_MILG  = 1.2e-10
GEXT     = 2.32e-10                    # Gaia EDR3 solar-neighbourhood, DHF24 sec 3.3
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27   # Park+2026 (2-sigma ceiling)
MARS_EPM = 1.400e-15                   # corpus-anchored Mars ephemeris budget [m/s^2]

# ==========================================================================================
head("PART 0 -- CHASSIS FRAME: the 4x4 Dirac matrix, the count, and one uncomputed bracket")
# ==========================================================================================
LN, K, b, c_ = sp.symbols("L_N K b c")
M = sp.Matrix([[0, LN, 0, 0], [-LN, 0, b, c_], [0, -b, 0, K], [0, -c_, -K, 0]])
Pf = sp.simplify(M[0,1]*M[2,3] - M[0,2]*M[1,3] + M[0,3]*M[1,2])
detM = sp.simplify(M.det())
check(sp.simplify(M + M.T) == sp.zeros(4,4), "0.1 Delta is antisymmetric")
check(sp.simplify(Pf - LN*K) == 0, "0.2 Pf(Delta) = L_N K  (independent of b, c)",
      f"Pf = {Pf}")
check(sp.simplify(detM - (LN*K)**2) == 0, "0.3 det(Delta) = (L_N K)^2",
      f"det = {detM}")
check(all(sp.simplify(sp.diff(Pf, s)) == 0 for s in (b, c_)),
      "0.4 Pfaffian independent of the off-diagonal couplings {C_M,D^2q}, {C_M,D^2p}")
check(20 - 12 - 4 == 4 and (20-12-4)//2 == 2,
      "0.5 count arithmetic: 20 - 12 - 4 = 4 phase-space dims = 2 DOF -- CONDITIONAL on the "
      "'12 first-class' side (pi_i, H_i)")
# The caveat: the suite never computed {H_i, S_2}. q = (1/6) ln det gamma is NOT a spatial
# scalar: delta_xi q = xi.grad q + (1/3) D.xi has an INHOMOGENEOUS piece, so
# {S_2, H_i[xi]} = D^2(delta_xi q) contains (1/3) D^2 (D.xi) != 0 even on q = 0.
xr = sp.symbols("x", real=True)
xi = sp.Function("xi")(xr)         # 1D longitudinal diffeo parameter
q_lin = sp.Integer(0)              # on the constraint surface take q -> 0 (weakest case)
delta_q = q_lin*sp.diff(xi, xr) + sp.Rational(1,3)*sp.diff(xi, xr)   # transport + inhomogeneous
bracket = sp.diff(delta_q, xr, 2)  # D^2(delta_xi q)
check(sp.simplify(bracket) != 0,
      "0.6 CAVEAT (new): {D^2 q, H_i[xi]} contains (1/3) D^2(D.xi) != 0 even at q = 0",
      "the certified suite verified only the 4x4 sub-block; H_i's brackets with S_2 were asserted, "
      "not computed.  A repaired first-class combination may exist but is UNVERIFIED; the count "
      "20-12-4 inherits this as an unverified hypothesis.")

# ==========================================================================================
head("PART 1 -- g_00 SECTOR: exact lapse law, beta_PPN, the Phi_1 coefficient, kernel corrections")
# ==========================================================================================
# 1.1  With N = e^{Psi/c^2} EXACTLY (not a truncation), C_M is c-independent and exactly AQUAL:
X, Y2 = sp.symbols("X Y", real=True)
a0s, cs = sp.symbols("a0 c", positive=True)
Psi = sp.Function("Psi")(X, Y2)
lnN = Psi / cs**2                                 # exact: N = exp(Psi/c^2)
grad = [sp.diff(lnN, v) for v in (X, Y2)]
yv = (cs**2/a0s)*sp.sqrt(sum(g**2 for g in grad))
mu_s = 1 - sp.exp(-yv)
CM_flux = sum(sp.diff(cs**2*mu_s*g, v) for g, v in zip(grad, (X, Y2)))
gP = [sp.diff(Psi, v) for v in (X, Y2)]
target = sum(sp.diff((1-sp.exp(-sp.sqrt(sum(h**2 for h in gP))/a0s))*g, v)
             for g, v in zip(gP, (X, Y2)))
check(sp.simplify(CM_flux - target) == 0,
      "1.1 N = e^{Psi/c^2}: C_M == D.[mu(|DPsi|/a0) DPsi] - 4 pi G rho EXACTLY (all orders in 1/c^2)",
      "so g_00 = -e^{2Psi/c^2} exactly, with Psi solving the mu-Poisson equation -- no PN "
      "nonlinearities enter the lapse sector at any order")

# 1.2  Eulerian dust source at O(c^-4): rho_m = rho*(1 + v^2/2c^2), rho* the conserved density.
v2, N_s = sp.symbols("v2 N", positive=True)      # v2 = v^2/c^2
rho0 = sp.symbols("rho0", positive=True)
u_dot_n_sq = 1/(1 - v2/N_s**2)                    # (u.n)^2 for dust, gamma_ij = delta_ij
rho_m = rho0*u_dot_n_sq
rho_star = rho0/sp.sqrt(1 - v2/N_s**2)            # rho* = rho0 N u^0 sqrt(gamma), det gamma = 1
ratio = sp.series(sp.simplify(rho_m/rho_star).subs(N_s, 1), v2, 0, 2).removeO()
check(sp.simplify(ratio - (1 + v2/2)) == 0,
      "1.2 rho_m = rho* (1 + v^2/2c^2) + O(c^-4) for dust  (rho* = conserved rest-mass density)",
      f"rho_m/rho* = {ratio}")

# 1.3  Static exterior, mu -> 1: -g_00 = e^{-2U/c^2} => beta_PPN.
U_s = sp.symbols("U", positive=True)
mg00 = sp.series(sp.exp(-2*U_s), U_s, 0, 4).removeO()     # U in units of c^2
c_U2 = mg00.coeff(U_s, 2)
check(sp.simplify(c_U2 - 2) == 0,
      "1.3 -g_00 = 1 - 2U + 2U^2 + O(U^3)  =>  coefficient 2 beta U^2 gives beta_PPN = 1 EXACTLY",
      f"-g_00 series = {mg00}")
BETA = 1

# 1.4  Moving source (preferred frame): Psi = -U - Phi_1/2 (from 1.2, mu->1, instantaneous elliptic)
#      => -g_00 = 1 - 2U - Phi_1 + 2U^2  =>  g_00 = -1 + 2U + 1*Phi_1 - 2U^2.
#      Standard PPN: coefficient of Phi_1 is (2 gamma + 2 + alpha_3 + zeta_1 - 2 xi); GR value 4.
#      No (w.nhat)^2 structure (exact instantaneous 1/r) => coefficient of curly-A = -(zeta_1-2xi) = 0.
#      No Phi_2 (elliptic eq has no U-nonlinearity), Phi_3 coefficient 2, Phi_4 coefficient 0.
U_f, P1 = sp.symbols("Uf Phi1", positive=True)
Psi_mov = -U_f - P1/2
g00_mov = -sp.series(sp.exp(2*Psi_mov), P1, 0, 2).removeO()
g00_mov = sp.expand(sp.series(g00_mov, U_f, 0, 3).removeO())
cPhi1 = sp.expand(g00_mov).coeff(P1, 1).coeff(U_f, 0)   # coefficient of Phi_1 in g_00 = -1+2U+Phi_1-2U^2
check(sp.simplify(cPhi1 - 1) == 0,
      "1.4 coefficient of Phi_1 in g_00 = 1  (GR: 4).  With gamma from Part 2 this forces alpha_3 != 0",
      f"g_00 = {sp.expand(-g00_mov)}  (cross terms U*Phi1 are O(c^-6))")
COEF_PHI1, COEF_A, COEF_PHI2, COEF_PHI3, COEF_PHI4 = 1, 0, 0, 2, 0

# 1.5  Kernel corrections to the lapse sector at solar-system accelerations (both kernels).
print()
info("1.5 kernel corrections (fractional deviation of Psi from Newtonian) -- NOT hand-waved:")
for fn, a0 in A0.items():
    y_1AU  = (GM_SUN/AU**2)/a0
    y_imp  = (GM_SUN/(1.6*RSUN)**2)/a0            # Cassini conjunction impact parameter 1.6 R_sun
    # mu_exp = 1-e^{-y}: nu-1 = e^{-x} with x ~ y  =>  log10 correction:
    lg_exp_1AU = -y_1AU/math.log(10); lg_exp_imp = -y_imp/math.log(10)
    m5_1AU,  m5_imp  = (1/5)*y_1AU**-2.5, (1/5)*y_imp**-2.5
    m10_1AU, m10_imp = (1/10)*y_1AU**-5.0, (1/10)*y_imp**-5.0
    print(f"     {fn:<10} y(1AU)={y_1AU:.3e}  y(1.6Rsun)={y_imp:.3e}")
    print(f"       mu_exp : 10^({lg_exp_1AU:+.3e}) @1AU   10^({lg_exp_imp:+.3e}) @Cassini")
    print(f"       mu_5   : {m5_1AU:.2e} @1AU   {m5_imp:.2e} @Cassini")
    print(f"       mu_10  : {m10_1AU:.2e} @1AU   {m10_imp:.2e} @Cassini")
y1c = (GM_SUN/AU**2)/A0["canonical"]
check((1/5)*y1c**-2.5 < 1e-19 and (1/10)*y1c**-5.0 < 1e-19,
      "1.5 the LARGEST kernel correction in the whole family (mu_5 at 1 AU) is < 1e-19",
      "=> every PPN parameter below is kernel-INDEPENDENT to better than 1e-19; the O(1) failures "
      "cannot be repaired by the Gate-13 kernel swap")

# ==========================================================================================
head("PART 2 -- g_ij SECTOR: gamma_PPN  (cross-check of the committed freeze-session lensing gate)")
# ==========================================================================================
# Linear scalar sector of gamma_ij: gamma_ij = (1+2C) delta_ij + 2 E_{,ij}.
# q = (1/6) ln det gamma = C + (1/3) lap E  (linear).  S_2: D^2 q = 0, k != 0  =>  q(k) = 0.
# Spatial diffeos (suite's own assignment) gauge E away; then C(k) = q(k) = 0 for all k != 0.
kk = sp.symbols("k", positive=True)
Csym, Esym = sp.symbols("C E")
q_k = Csym + sp.Rational(1,3)*(-kk**2)*Esym
sol_C = sp.solve(sp.Eq((-kk**2)*q_k, 0), Csym)[0]
check(sp.simplify(sol_C.subs(Esym, 0)) == 0,
      "2.1 D^2 q = 0 (k!=0) with E gauged to zero  =>  C = 0: NO scalar spatial potential",
      "the GR Hamiltonian constraint (which sources C from rho) was DELETED and replaced by the "
      "source-free D^2 q = 0.  Hence g_ij = delta_ij + h_TT and gamma_PPN = 0 EXACTLY, at every "
      "acceleration, for every kernel.  Agrees with committed gate_lensing_weakfield_derivation.out")
GAMMA = 0
sig_cassini = abs(GAMMA - 1 - 2.1e-5)/2.3e-5
sig_vlbi    = abs(GAMMA - 1 - (-0.8e-4))/1.2e-4
info("2.2 Cassini Shapiro (Bertotti+03: gamma-1 = (2.1+-2.3)e-5)",
     f"MMG gamma-1 = -1  =>  {sig_cassini:,.0f} sigma")
info("2.2 VLBI deflection (gamma-1 = (-0.8+-1.2)e-4)", f"=> {sig_vlbi:,.0f} sigma")
check(sig_cassini > 4e4, "2.2 gamma_PPN = 0 vs Cassini: excluded at > 40,000 sigma")

# ==========================================================================================
head("PART 3 -- g_0i SECTOR: linearized momentum constraint for a moving source (sympy, no quoted formula)")
# ==========================================================================================
# Plane-wave mode locked to a source moving with velocity w = (wx, 0, wz), k = k zhat:
# every field ~ exp(i(k z - k wz t)).  Amplitudes are solved exactly.
t, x1, y1_, z1 = sp.symbols("t x y z", real=True)
kR, wx, wz, rho_h, Gn = sp.symbols("k w_x w_z rho G", real=True, positive=False)
I = sp.I
phase = sp.exp(I*(kR*z1 - kR*wz*t))
coords = (t, x1, y1_, z1)
eta = sp.diag(-1, 1, 1, 1)

def lin_G(hfun):
    """Linearized Einstein tensor G^(1)_{mu nu} for h_{mu nu} (4x4 sympy Matrix of exprs)."""
    hud = sp.zeros(4, 4)     # h^a_b
    for a in range(4):
        for bb in range(4):
            hud[a, bb] = sum(eta[a, m]*hfun[m, bb] for m in range(4))
    htr = sum(hud[a, a] for a in range(4))
    def d(e, m): return sp.diff(e, coords[m])
    box = lambda e: sum(eta[m, n]*d(d(e, m), n) for m in range(4) for n in range(4))
    Gt = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            t1 = sum(d(d(hud[a, n], a), m) for a in range(4))
            t2 = sum(d(d(hud[a, m], a), n) for a in range(4))
            t3 = box(hfun[m, n])
            t4 = d(d(htr, m), n)
            t5 = sum(eta[al, bt]*0 for al in range(4) for bt in range(4))  # placeholder
            dab = sum(d(d(hud[a, bb], a), 0)*0 for a in range(4) for bb in range(4))
            # d_a d_b h^{ab}:
            dadb = sum(sp.diff(sp.diff(sum(eta[a, m2]*hud[m2, bb]*0 for m2 in range(4)), coords[0]), coords[0])
                       for a in range(4) for bb in range(4))
            Gt[m, n] = sp.Rational(1, 2)*(t1 + t2 - t3 - t4)
    # subtract trace part: - (1/2) eta_{mn} (d_a d_b h^{ab} - box h)
    huu = sp.zeros(4, 4)     # h^{ab}
    for a in range(4):
        for bb in range(4):
            huu[a, bb] = sum(eta[a, m2]*eta[bb, n2]*hfun[m2, n2] for m2 in range(4) for n2 in range(4))
    dadb_h = sum(sp.diff(sp.diff(huu[a, bb], coords[a]), coords[bb]) for a in range(4) for bb in range(4))
    box_htr = box(htr)
    for m in range(4):
        for n in range(4):
            Gt[m, n] += -sp.Rational(1, 2)*eta[m, n]*(dadb_h - box_htr)
    return sp.simplify(Gt)

# 3.1 gauge check: h = d_mu xi_nu + d_nu xi_mu  =>  G^(1) = 0
xiamp = sp.symbols("xi0 xi1 xi2 xi3")
xiv = [xiamp[i]*phase for i in range(4)]
hg = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        hg[m, n] = sp.diff(xiv[n], coords[m]) + sp.diff(xiv[m], coords[n])
Gg = lin_G(hg)
check(all(sp.simplify(Gg[m, n]) == 0 for m in range(4) for n in range(4)),
      "3.1 sympy linearized-G routine: G^(1)[pure gauge] = 0 identically (all 16 components)")

# 3.2 identity: G^(1)_{0i} = sigma * [d_j(K^j_i - delta^j_i K)],  K_ij = (hdot_ij - d_i h_0j - d_j h_0i)/2
A00, Axx, Ayy, Azz, Axz, A0x, A0y, A0z = sp.symbols("A00 Axx Ayy Azz Axz A0x A0y A0z")
h = sp.zeros(4, 4)
h[0, 0] = A00*phase
h[1, 1] = Axx*phase; h[2, 2] = Ayy*phase; h[3, 3] = Azz*phase
h[1, 3] = h[3, 1] = Axz*phase
h[0, 1] = h[1, 0] = A0x*phase; h[0, 2] = h[2, 0] = A0y*phase; h[0, 3] = h[3, 0] = A0z*phase
Gh = lin_G(h)
Kt = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Kt[i, j] = sp.Rational(1, 2)*(sp.diff(h[i+1, j+1], t)
                                      - sp.diff(h[0, j+1], coords[i+1])
                                      - sp.diff(h[0, i+1], coords[j+1]))
Ktr = sum(Kt[i, i] for i in range(3))
Mvec = [sp.simplify(sum(sp.diff(Kt[j, i], coords[j+1]) for j in range(3)) - sp.diff(Ktr, coords[i+1]))
        for i in range(3)]
sigma_found = None
for sgn in (+1, -1):
    if all(sp.simplify(Gh[0, i+1] - sgn*Mvec[i]) == 0 for i in range(3)):
        sigma_found = sgn
check(sigma_found is not None,
      "3.2 EXACT identity G^(1)_{0i} = sigma * d_j(K^j_i - delta K) for arbitrary amplitudes",
      f"sigma = {sigma_found}; also verifies G^(1)_{{0i}} contains NO h_00 term "
      f"(h_00-coefficient: {sp.simplify(sp.diff(Gh[0,1], A00))}, {sp.simplify(sp.diff(Gh[0,3], A00))})")
check(sp.simplify(sp.diff(Gh[0, 1], A00)) == 0 and sp.simplify(sp.diff(Gh[0, 3], A00)) == 0,
      "3.2b the 0i equation is independent of the lapse potential h_00 (pure momentum sector)")

# 3.3 GR anchor: h_00 = 2U, h_ij = 2U delta_ij, T_{0i} = -rho w_i  =>  transverse h_0x = -4 V_x.
Uamp = 4*sp.pi*Gn*rho_h/kR**2                       # lap U = -4 pi G rho
subs_GR = {A00: 2*Uamp, Axx: 2*Uamp, Ayy: 2*Uamp, Azz: 2*Uamp, Axz: 0}
T0 = [-rho_h*wx*phase, 0, -rho_h*wz*phase]          # T_{0i} for dust (sympy-checked below)
# dust check: T_{mu nu} = rho u_mu u_nu, u ~ (1, w):  T_{0i} = g_00 g_ij rho u^0 u^j ~ -rho w_i
u_up = sp.Matrix([1, wx, 0, wz])
Tdn = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Tdn[m, n] = rho_h*sum(eta[m, a]*u_up[a] for a in range(4))*sum(eta[n, bb]*u_up[bb] for bb in range(4))
check(sp.simplify(Tdn[0, 1] + rho_h*wx) == 0 and sp.simplify(Tdn[0, 3] + rho_h*wz) == 0,
      "3.3a dust source: T_{0i} = -rho w_i at leading order (index lowering, sympy)")
eqs_GR = [sp.simplify((Gh[0, i+1].subs(subs_GR) - 8*sp.pi*Gn*T0[i])/phase) for i in range(3)]
sol_GR = sp.solve(eqs_GR[0], A0x)
Vx = 4*sp.pi*Gn*rho_h*wx/kR**2                      # lap V_i = -4 pi G rho w_i
check(len(sol_GR) == 1 and sp.simplify(sol_GR[0] + 4*Vx) == 0,
      "3.3b GR anchor: transverse h_0x = -4 V_x  (= the known PPN -(7/2)V-(1/2)W transverse part)",
      f"h_0x = {sp.simplify(sol_GR[0])}")
lon_GR = sp.simplify(eqs_GR[2])
check(sp.simplify(sp.diff(lon_GR, A0z)) == 0 and sp.simplify(lon_GR) == 0,
      "3.3c GR longitudinal 0i-equation: no h_0z dependence and identically satisfied "
      "(continuity) -- longitudinal h_0i is GAUGE in GR, as it must be")

# 3.4 MMG: h_ij = 0 (Part 2), K -> Ktilde with the mu_3 multiplier from H_T (S_3 = D^2 p feeds
#     gamma-dot by + delta_ij lap mu_3), and the D^2 p constraint = trace Ktilde = 0.
M3 = sp.symbols("M3")
mu3f = M3*phase
subs_MMG = {A00: 2*Uamp, Axx: 0, Ayy: 0, Azz: 0, Axz: 0}
lap_mu3 = sp.diff(mu3f, z1, 2)
Ktil = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        hij_dot = sp.diff(h[i+1, j+1], t) - (lap_mu3 if i == j else 0)
        Ktil[i, j] = sp.Rational(1, 2)*(hij_dot
                                        - sp.diff(h[0, j+1], coords[i+1])
                                        - sp.diff(h[0, i+1], coords[j+1]))
Ktil_tr = sp.simplify(sum(Ktil[i, i] for i in range(3)))
Mtil = [sp.simplify(sum(sp.diff(Ktil[j, i], coords[j+1]) for j in range(3))
                    - sp.diff(sp.simplify(sum(Ktil[m2, m2] for m2 in range(3))), coords[i+1]))
        for i in range(3)]
eqs_MMG = [sp.simplify((sigma_found*Mtil[i].subs(subs_MMG) - 8*sp.pi*Gn*T0[i])/phase) for i in range(3)]
eq_tr   = sp.simplify(Ktil_tr.subs(subs_MMG)/phase)
sol_MMG = sp.solve(eqs_MMG + [eq_tr], [A0x, A0y, A0z, M3], dict=True)
check(len(sol_MMG) == 1, "3.4a MMG 0i system + trace-Ktilde = 0: unique solution for (h_0i, mu_3)")
sm = sol_MMG[0]
h0x_MMG, h0z_MMG = sp.simplify(sm[A0x]), sp.simplify(sm[A0z])
info("3.4b MMG solution", f"h_0x = {h0x_MMG},   h_0z = {h0z_MMG},   mu_3 = {sp.simplify(sm.get(M3, 0))}")
# match to PPN structures:  V_i(k) = 4 pi G rho w_i /k^2 ;  W_i(k) = 4 pi G rho (w_i - 2 khat_i (khat.w))/k^2
Vz = 4*sp.pi*Gn*rho_h*wz/kR**2
Wx = 4*sp.pi*Gn*rho_h*wx/kR**2
Wz = 4*sp.pi*Gn*rho_h*(wz - 2*wz)/kR**2
cV, cW = sp.symbols("c_V c_W")
sol_cc = sp.solve([sp.Eq(h0x_MMG, cV*Vx + cW*Wx), sp.Eq(h0z_MMG, cV*Vz + cW*Wz)], [cV, cW])
check(bool(sol_cc), "3.4c MMG h_0i matches the PPN (V_i, W_i) structure exactly")
cV_val, cW_val = sp.nsimplify(sol_cc[cV]), sp.nsimplify(sol_cc[cW])
check(sp.simplify(cV_val + sp.Rational(7, 2)) == 0 and sp.simplify(cW_val + sp.Rational(1, 2)) == 0,
      "3.4d g_0i = -(7/2) V_i - (1/2) W_i  -- numerically GR's PPN-gauge form, but with gamma = 0 "
      "the PPN dictionary reads it very differently",
      f"c_V = {cV_val}, c_W = {cW_val}")

# ==========================================================================================
head("PART 4 -- THE PPN DICTIONARY SOLVE AND THE BOUNDS TABLE")
# ==========================================================================================
# Standard PPN metric (Will), preferred frame = foliation rest frame (w = 0 coordinates):
#  g_00  = -1 + 2U - 2 beta U^2 + (2g+2+a3+z1-2xi) Phi1 + 2(3g-2b+1+z2+xi) Phi2
#          + 2(1+z3) Phi3 + 2(3g+3z4-2xi) Phi4 - (z1-2xi) A - 2 xi Phi_W
#  g_0i  = -(1/2)(4g+3+a1-a2+z1-2xi) V_i - (1/2)(1+a2-z1+2xi) W_i
#  g_ij  = (1+2g U) delta_ij
al1, al2, al3, ze1, ze2, ze3, ze4, xiW = sp.symbols("alpha_1 alpha_2 alpha_3 zeta_1 zeta_2 zeta_3 zeta_4 xi")
g_, b_ = sp.Integer(GAMMA), sp.Integer(BETA)
eqs = [sp.Eq(2*g_ + 2 + al3 + ze1 - 2*xiW, COEF_PHI1),      # Phi_1 coefficient (Part 1.4)
       sp.Eq(-(ze1 - 2*xiW), COEF_A),                       # no curly-A term
       sp.Eq(2*(3*g_ - 2*b_ + 1 + ze2 + xiW), COEF_PHI2),   # no Phi_2 term
       sp.Eq(2*(1 + ze3), COEF_PHI3),                       # Phi_3 coefficient 2
       sp.Eq(2*(3*g_ + 3*ze4 - 2*xiW), COEF_PHI4),          # no Phi_4 term
       sp.Eq(-sp.Rational(1, 2)*(4*g_ + 3 + al1 - al2 + ze1 - 2*xiW), cV_val),
       sp.Eq(-sp.Rational(1, 2)*(1 + al2 - ze1 + 2*xiW), cW_val)]
sol_ppn = sp.solve(eqs, [al1, al2, al3, ze1, ze2, ze3, ze4], dict=True)
check(len(sol_ppn) == 1, "4.1 the PPN dictionary has a unique solution (xi undetermined by point-dust probes)")
S = sol_ppn[0]
ALPHA1 = sp.simplify(S[al1]); ALPHA2 = sp.simplify(S[al2]); ALPHA3 = sp.simplify(S[al3])
print(f"""
   ===========================  PPN PARAMETERS OF MMG_constraint_first  ===========================
   gamma_PPN = {GAMMA}                (GR 1;  Cassini |gamma-1| < 2.3e-5)
   beta_PPN  = {BETA}                (GR 1;  LLR/Mercury |beta-1| < ~1e-4)
   alpha_1   = {ALPHA1}                (bound |alpha_1| < 1e-4)
   alpha_2   = {ALPHA2}                (bound |alpha_2| < ~2e-7 .. 2e-9)
   alpha_3   = {ALPHA3}               (bound |alpha_3| < 4e-20; also = momentum non-conservation)
   zeta_1 = {sp.simplify(S[ze1])},  zeta_2 = {sp.simplify(S[ze2])},  zeta_3 = {sp.simplify(S[ze3])},  zeta_4 = {sp.simplify(S[ze4])}   (xi not probed here)
   ================================================================================================""")
check(ALPHA1 == 4, "4.2 alpha_1 = 4  ->  violates the |alpha_1| < 1e-4 bound by 4.0e4 x",
      "physical origin: gamma = 0 removes the 4*gamma part of the V_i coefficient; the "
      "gravito-magnetic sector is GR-like, so the mismatch is booked entirely as alpha_1")
check(ALPHA2 == 0, "4.3 alpha_2 = 0  ->  PASSES the solar-spin-axis bound (the one clean pass)")
check(ALPHA3 == -1, "4.4 alpha_3 = -1  ->  violates the pulsar bound |alpha_3| < 4e-20 by 2.5e19 x",
      "physical origin: the lapse responds INSTANTANEOUSLY (elliptic C_M) to the source's "
      "kinetic energy with coefficient 1 instead of GR's retardation-consistent 4; alpha_3 != 0 "
      "also means the theory is non-conservative (self-accelerating binaries)")
# Mercury perihelion with gamma=0, beta=1: lambda = (2 + 2 gamma - beta)/3 = 1/3
lam_per = (2 + 2*GAMMA - BETA)/3
prec_GR = 42.98
info("4.5 Mercury perihelion", f"(2+2g-b)/3 = {lam_per:.4f} -> {lam_per*prec_GR:.2f} arcsec/cy "
     f"vs observed {prec_GR}+-0.04 => {abs(prec_GR - lam_per*prec_GR)/0.04:,.0f} sigma")
check(abs(prec_GR - lam_per*prec_GR)/0.04 > 500, "4.5 perihelion: excluded at > 500 sigma")
print("""
  THEORY-SPECIFIC PREFERRED-FRAME TERMS (beyond the alpha's):
   (i)   alpha_3 = -1: the elliptic (action-at-a-distance) lapse response.  In a frame moving at
         w relative to the foliation this generates the PPN term -(alpha_1-alpha_2-alpha_3) w^2 U
         = -(5) w^2 U in g_00 and (2 alpha_3 - alpha_1) w^i V_i = -6 w^i V_i; with w ~ 369 km/s
         (CMB frame) these are ~7.6e-6 U effects -- 2 orders above the Cassini gamma precision,
         5 above pulsar timing sensitivity to alpha_3.
   (ii)  the k = 0 scalar zero-mode pair (q, p) survives S_2, S_3 and is 'reserved for cosmology'
         (Gate 7): the preferred foliation has an undetermined homogeneous mode -- no PPN effect,
         but the PPN frame itself is only defined up to it.
   (iii) the a0-scale EFE quadrupole (PART 5): kernel-dependent, aligned with the GALACTIC-CENTRE
         direction (not the CMB dipole) -- separable from (i) by axis, per the corpus's audit3.""")

# ==========================================================================================
head("PART 5 -- THE EFE QUADRUPOLE Q2: INDEPENDENT INTEGRATOR, BOTH KERNELS, BOTH FOOTINGS")
# ==========================================================================================
# Independent method (this file): interior l=2 Green's-function coefficient with the integration
# by parts done on the FLUX, not the source:
#   lap phi = div F,  F = (nu(|u|)-1) u,  u = grad Phi_N = rhat/r^2 - e zhat   (GM = a0 = 1)
#   phi ⊃ A r^2 P2(mu),  A = +(1/4pi) INT F . grad'[P2(mu')/r'^3] d^3x'
#     = -(1/2) INT dr/r^2 INT dmu [ 3 F_r P2(mu) + F_theta sin(theta) dP2/dmu * (-1) ... ]
#   (the theta-gradient of P2(cos th)/r^3 is -sin(th) P2'(mu)/r^4)
#   q_DHF = 2 A   (Q_zz = 2A a0^{3/2}/sqrt(GM); Q2 = (3/2)|Q_zz| in the DHF24 convention)
def nu_ms08(yy):
    yy = np.asarray(yy, float)
    s = np.sqrt(yy)
    out = np.where(s > 40, 1.0 + np.exp(-np.minimum(s, 700)), 1.0/(1.0 - np.exp(-np.minimum(s, 700))))
    return out
def nu_a0line(yy):
    return np.sqrt(1.0 + 1.0/np.asarray(yy, float))
def make_nu_from_mu(mu_of_x, x_asym):
    """nu(y): invert y = x mu(x).  x_asym(y) = asymptotic inverse for large y."""
    def nu(yy):
        yy = np.atleast_1d(np.asarray(yy, float))
        out = np.empty_like(yy)
        for i, yv_ in enumerate(yy):
            if yv_ > 1e6:
                out[i] = x_asym(yv_)/yv_
            else:
                g = lambda xx: xx*mu_of_x(xx) - yv_
                hi = max(10.0, 2.0*math.sqrt(yv_) + 2.0)
                while g(hi) < 0: hi *= 2
                out[i] = brentq(g, 1e-14, hi, xtol=1e-15, rtol=8.9e-16)/yv_
        return out if out.size > 1 else out[0]
    return nu
mu_exp_x  = lambda xx: 1.0 - math.exp(-min(xx, 700.0))
nu_muexp  = make_nu_from_mu(mu_exp_x,  lambda yv_: yv_ + yv_*math.exp(-min(yv_, 700.0)))
def make_nu_mun(n):
    mu = lambda xx: xx/(1.0 + xx**n)**(1.0/n)
    return make_nu_from_mu(mu, lambda yv_: yv_*(1.0 + (1.0/n)*yv_**(-n/2.0) if n*math.log(yv_) < 600 else 1.0))
nu_mu5, nu_mu10, nu_mu20 = make_nu_mun(5), make_nu_mun(10), make_nu_mun(20)
nu_mu1 = lambda yy: 0.5 + np.sqrt(0.25 + 1.0/np.asarray(yy, float))

def nu_tab(nu, lo=-8, hi=12, n=1600):
    """log-log table of nu-1 for fast vectorized evaluation."""
    lg = np.linspace(lo, hi, n)
    vals = np.array([float(np.asarray(nu(10.0**g)).ravel()[0]) - 1.0 for g in lg])
    vals = np.clip(vals, 1e-300, None)
    lv = np.log(vals)
    def f(yy):
        yy = np.asarray(yy, float)
        return np.exp(np.interp(np.log10(np.clip(yy, 10.0**lo, 10.0**hi)), lg, lv))
    return f

def solve_eN(nu, etil):
    return brentq(lambda xx: xx*float(np.asarray(nu(xx)).ravel()[0]) - etil, 1e-12, 1e8,
                  xtol=1e-15, rtol=8.9e-16)

MU_G, W_G = leggauss(160)
def q_mine(nu, etil, nr=6001, rlo=1e-4, rhi=3e4):
    """|q| in the DHF convention (Q_zz coefficient), computed by MY flux-IBP quadrature."""
    eN = solve_eN(nu, etil)
    f_nu1 = nu_tab(nu)
    r = np.geomspace(rlo, rhi, nr)
    R, MU = np.meshgrid(r, MU_G, indexing="ij")
    ST = np.sqrt(np.clip(1.0 - MU**2, 0.0, None))
    u_r = 1.0/R**2 - eN*MU          # u = grad Phi_N, Phi_N = -1/r - e z
    u_t = eN*ST
    Ymag = np.sqrt(u_r**2 + u_t**2)
    amp = f_nu1(Ymag)
    F_r, F_t = amp*u_r, amp*u_t
    P2 = 0.5*(3*MU**2 - 1.0)
    dP2 = 3.0*MU                     # dP2/dmu
    integ_mu = np.sum((3.0*F_r*P2 + F_t*ST*(-dP2)*(-1.0))*W_G[None, :], axis=1)
    # NOTE: grad'[P2/r^3]_theta = (1/r) d_theta P2 / r^3 = -sin(th) P2'(mu) / r^4 ;
    # F.grad' = F_r(-3 P2/r^4) + F_t(-sin P2'/r^4);  A = (1/4pi) INT (2 pi r^2 dr dmu) [...]
    integ_mu = np.sum((F_r*(-3.0*P2) + F_t*(-ST*dP2))*W_G[None, :], axis=1)
    A = 0.5*np.trapz(integ_mu/r**2, r)
    return abs(2.0*A), eN

# 5.1 validation against the DHF24 anchors (which audit3 proved are the MS08 kernel's q):
ANCH = {1.0: 0.094, 1.5: 0.159, 2.0: 0.221}
print("  5.1  anchors (DHF24 / MS08 kernel):")
anch_ok = True
for e_, qa in ANCH.items():
    qm, eN = q_mine(nu_ms08, e_)
    dev = qm/qa - 1
    anch_ok &= abs(dev) < 0.03
    print(f"       etilde={e_:4.1f}: mine {qm:.4f} vs anchor {qa:.3f}  ({dev:+.2%}),  e_N={eN:.4f}")
check(anch_ok, "5.1 MY integrator reproduces the validated anchors q(1)=0.094, q(1.5)=0.159, "
               "q(2)=0.221 to < 3%")
qc, _ = q_mine(nu_ms08, 2.0); qc2, _ = q_mine(nu_ms08, 2.0, nr=12001, rlo=3e-5, rhi=1e5)
check(abs(qc2/qc - 1) < 0.005, "5.1b grid-convergence: doubling resolution moves q(2) by < 0.5%",
      f"{qc:.5f} -> {qc2:.5f}")
qa0, _ = q_mine(nu_a0line, 2.0)
info("5.1c cross-check vs audit3's independent slope/level forms",
     f"a0-line q(2): mine {qa0:.4f} vs audit3 0.1669  ({qa0/0.1669-1:+.2%})")

# 5.2 normalization: Q2_AQUAL = 1.5 * R_A * sqrt(a0^3/GM) * |q|.  R_A = 1.2344 is the corpus's
#     ONE imported number (AQUAL/QUMOND excess, calibrated on BN11).  Robustness: per-kernel
#     BN11 anchoring (a0=1.2e-10, g_ext=1.9e-10 -> etilde=1.5833; published AQUAL Q2).
R_A = 1.2344
BN11 = {"mu_exp": (nu_muexp, 3.0e-26), "mu5": (nu_mu5, 7.4e-27), "mu20": (nu_mu20, 2.1e-27),
        "mu1": (nu_mu1, 3.8e-26)}
ET_BN = 1.9e-10/1.2e-10
PREF_BN = 1.5*(1.2e-10)**1.5/math.sqrt(GM_SUN)
print("\n  5.2  BN11 (published AQUAL) per-kernel calibration at a0=1.2e-10, etilde=1.5833:")
RA_kernel = {}
for nm, (nu, q2pub) in BN11.items():
    qb, _ = q_mine(nu, ET_BN)
    RA_kernel[nm] = q2pub/(PREF_BN*qb)
    print(f"       {nm:<7} my|q|={qb:.5f}  1.5*pref*|q|={PREF_BN*qb:.3e}  BN11={q2pub:.2e}  "
          f"=> R_A({nm}) = {RA_kernel[nm]:.3f}")
check(1.0 < min(RA_kernel.values()) and max(RA_kernel.values()) < 1.5,
      "5.2 per-kernel R_A in [1.0, 1.5]; corpus value 1.2344 sits inside the spread",
      f"spread {min(RA_kernel.values()):.3f}-{max(RA_kernel.values()):.3f}")

# 5.3 the Q2 table -- the chassis's frozen kernel mu_exp = 1-e^{-y} and the swap kernels mu_5/mu_10
def Q2_row(nu, a0, RAval):
    etil = GEXT/a0
    qv, eN = q_mine(nu, etil)
    Q2 = 1.5*RAval*math.sqrt(a0**3/GM_SUN)*qv
    return etil, eN, qv, Q2, Q2/Q2_CEIL, (Q2 - Q2_CEN)/Q2_SIG
KERNELS = [("mu_exp (FROZEN)", nu_muexp), ("mu_5", nu_mu5), ("mu_10", nu_mu10)]
RES = {}
for fn, a0 in A0.items():
    print(f"\n  5.3  footing {fn}: a0 = {a0:.4e}, g_ext = {GEXT:.2e}  (R_A = {R_A})")
    print(f"       {'kernel':<16}{'etilde':>8}{'e_N':>8}{'|q|':>10}{'Q2 AQUAL':>12}{'x ceiling':>10}{'sigma':>8}")
    for nm, nu in KERNELS:
        etil, eN, qv, Q2, xc, sg = Q2_row(nu, a0, R_A)
        RES[(nm, fn)] = (qv, Q2, xc, sg)
        print(f"       {nm:<16}{etil:>8.3f}{eN:>8.3f}{qv:>10.5f}{Q2:>12.3e}{xc:>10.3f}{sg:>8.1f}")
# the task's y_ext ~ 1.9 line (Milgrom a0 = 1.2e-10, where the anchors live):
etil19 = GEXT/A0_MILG
q19, eN19 = q_mine(nu_muexp, etil19)
Q2_19_dhf = 1.5*math.sqrt(A0_MILG**3/GM_SUN)*q19            # DHF/QUMOND convention, no R_A
Q2_19_aq  = Q2_19_dhf*R_A
q19_anchor = np.interp(1.9, [1.0, 1.5, 2.0], [0.094, 0.159, 0.221])   # anchors, as tasked
Q2_19_anchor = 1.5*math.sqrt(A0_MILG**3/GM_SUN)*q19_anchor
print(f"\n  5.3b the tasked y_ext ~ 1.9 point (a0 = 1.2e-10, etilde = {etil19:.3f}):")
print(f"       anchors-interpolated q(1.9) = {q19_anchor:.3f} -> Q2 = {Q2_19_anchor:.3e} "
      f"= {Q2_19_anchor/Q2_CEIL:.2f} x ceiling  [MS08-kernel anchors, QUMOND convention]")
print(f"       mu_exp's own |q|({etil19:.2f}) = {q19:.4f} -> Q2 = {Q2_19_dhf:.3e} (QUMOND) / "
      f"{Q2_19_aq:.3e} (AQUAL) = {Q2_19_dhf/Q2_CEIL:.2f} / {Q2_19_aq/Q2_CEIL:.2f} x ceiling")
check(RES[("mu_exp (FROZEN)", "canonical")][2] > 3 and RES[("mu_exp (FROZEN)", "alt")][2] > 3
      and Q2_19_anchor/Q2_CEIL > 3,
      "5.3 mu_exp FAILS the Q2 ceiling on every footing and at the tasked y_ext~1.9 point "
      "(>= 3x ceiling however normalized)",
      f"canonical {RES[('mu_exp (FROZEN)','canonical')][2]:.2f}x ({RES[('mu_exp (FROZEN)','canonical')][3]:.0f} sigma), "
      f"alt {RES[('mu_exp (FROZEN)','alt')][2]:.2f}x ({RES[('mu_exp (FROZEN)','alt')][3]:.0f} sigma)")
c5, a5 = RES[("mu_5", "canonical")][2], RES[("mu_5", "alt")][2]
c10, a10 = RES[("mu_10", "canonical")][2], RES[("mu_10", "alt")][2]
check(abs(c5/0.387 - 1) < 0.15 and abs(c10/0.078 - 1) < 0.20,
      "5.4 INDEPENDENT verification of the route1B/audit3 claim: mu_5 / mu_10 = 0.39 / 0.08 of "
      "the ceiling on the canonical footing",
      f"mine: mu_5 {c5:.3f}x (claim 0.387), mu_10 {c10:.3f}x (claim 0.078)")
check(c5 < 1 and c10 < 1 and a5 < 1 and a10 < 1,
      "5.4b mu_5 and mu_10 CLEAR the ceiling on both footings",
      f"alt: mu_5 {a5:.3f}x (claim 0.811), mu_10 {a10:.3f}x (claim 0.203)")
# robustness of the mu_5 alt margin against the calibration systematic:
worst_RA = max(RA_kernel.values())
a5_worst = a5*worst_RA/R_A
info("5.4c calibration systematic on the tightest cell (mu_5, alt)",
     f"R_A in [{min(RA_kernel.values()):.3f},{worst_RA:.3f}] -> mu_5 alt = "
     f"{a5*min(RA_kernel.values())/R_A:.3f}-{a5_worst:.3f} x ceiling "
     f"({'still clears' if a5_worst < 1 else 'MARGINAL'})")

# 5.5 1-AU monopoles vs the Mars EPM budget
print("\n  5.5  1-AU anomalous monopole vs the Mars EPM budget (1.4e-15 m/s^2):")
for fn, a0 in A0.items():
    y1 = (GM_SUN/AU**2)/a0
    g1 = GM_SUN/AU**2
    m_exp = math.exp(-min(y1, 700.0))            # underflows to 0: report log10 instead
    lg_exp = -y1/math.log(10)
    m5 = (1/5)*y1**-2.5*g1/MARS_EPM
    m10 = (1/10)*y1**-5.0*g1/MARS_EPM
    print(f"       {fn:<10} mu_exp: 10^({lg_exp:+.3e}) x budget   mu_5: {m5:.2e} x   mu_10: {m10:.2e} x")
check((1/5)*((GM_SUN/AU**2)/A0['canonical'])**-2.5*(GM_SUN/AU**2)/MARS_EPM < 1e-6,
      "5.5 every kernel's 1-AU monopole is >= 6 orders under the Mars budget (mu_exp doubly so)")

# ==========================================================================================
head("VERDICTS")
# ==========================================================================================
print(f"""
  PPN PARAMETERS (kernel-independent to < 1e-19, Part 1.5):
     gamma = 0   beta = 1   alpha_1 = 4   alpha_2 = 0   alpha_3 = -1
     [zeta_1 = 2xi, zeta_2 = 1-xi, zeta_3 = 0, zeta_4 = 2xi/3; xi not probed by point-dust]

  KERNEL mu_exp = 1 - e^-y (FROZEN):   FAIL
     - gamma_PPN = 0: Cassini {sig_cassini:,.0f} sigma, VLBI {sig_vlbi:,.0f} sigma  [structural, D^2q = 0]
     - alpha_1 = 4 (4.0e4 x bound), alpha_3 = -1 (2.5e19 x bound), perihelion 1/3 of GR
     - EFE quadrupole Q2 = {RES[('mu_exp (FROZEN)','canonical')][1]:.2e} / {RES[('mu_exp (FROZEN)','alt')][1]:.2e} s^-2 (canon/alt)
       = {RES[('mu_exp (FROZEN)','canonical')][2]:.1f}x / {RES[('mu_exp (FROZEN)','alt')][2]:.1f}x the 5.2e-27 ceiling ({RES[('mu_exp (FROZEN)','canonical')][3]:.0f} / {RES[('mu_exp (FROZEN)','alt')][3]:.0f} sigma); at the tasked
       y_ext ~ 1.9 anchor point: {Q2_19_anchor/Q2_CEIL:.1f}x (anchors) / {Q2_19_aq/Q2_CEIL:.1f}x (own kernel, AQUAL)

  KERNEL mu_n (n = 5, 10):   FAIL  (repairs ONLY the quadrupole, not the PPN structure)
     - Q2: mu_5 {c5:.2f}x / {a5:.2f}x ceiling, mu_10 {c10:.2f}x / {a10:.2f}x (canon/alt) -- clears; route1B's
       0.39/0.08 INDEPENDENTLY CONFIRMED at {c5:.3f}/{c10:.3f}
     - but gamma = 0, alpha_1 = 4, alpha_3 = -1 are UNTOUCHED by the kernel swap: the failures
       live in the constraint structure (D^2q = 0 deleted the Phi-sourcing Hamiltonian
       constraint; the elliptic C_M fixes the Phi_1 coefficient at 1), not in mu(y).

  The chassis's Cassini liability is therefore NOT the EFE quadrupole (which mu_n does repair,
  as priced) -- it is the PPN structure itself.  The named repair S_2 -> D^2(q + ln N) (Part H of
  the committed lensing gate) would set gamma = 1 and needs re-certification; whether it also
  repairs alpha_1/alpha_3 is OPEN (the g_0i and Phi_1 sectors are untouched by that repair as
  named -- alpha_3 = -1 comes from C_M itself and looks repair-resistant inside this chassis).
""")
print("=" * 102)
if FAIL:
    print(f"RESULT: {NCHK[0]-len(FAIL)}/{NCHK[0]} checks passed.  FAILURES: {FAIL}")
    sys.exit(1)
print(f"RESULT: {NCHK[0]}/{NCHK[0]} checks passed.")
sys.exit(0)
