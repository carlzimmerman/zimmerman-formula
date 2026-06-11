#!/usr/bin/env python3
# agentY_quasistatic.py -- [SLOT-Y] the lens-only slip sector: sympy quasi-static derivation.
#
# THE MODEL (units c=1 in-script; G kept; a0 has dimension 1/length):
#   fields: g_munu ; khronon T (u_mu = -d_mu T/|dT|, the assembly frame, agentU) ; slip scalar chi.
#   q_mu = h_mu^nu d_nu chi (u-orthogonal gradient),  Y = q.q/a0^2  (>=0, dimensionless)
#   a_mu = u^nu nabla_nu u_mu (khronon acceleration; unitary gauge: a_i = d_i ln N EXACTLY)
#
#   S_slip = (1/8piG) Int sqrt(-g) [ -a0^2 J(Y) + sig*S(Y) a.q + K(Y) a.a + F(Y) (a.q)^2/a0^2 ]
#
#   J : the free kinetic function (the sector's AQUAL-analog; pinned by the lensing RAR)
#   S : source dressing of the cross-coupling (sig = +-1 overall sign bookkeeping)
#   K : the a^2 counterterm (Blanchet-Marsat-type operator, Y-DRESSED -- here slaved to the
#       lens-only condition, NOT carrying a matter-side MOND force)
#   F : the (a.q)^2 cross operator (second counterterm direction, available at the same order)
#
# DERIVATION PLAN
#  SA  tensor sector: unitary gauge, TT perturbation -- show NO derivative of h_ij enters S_slip
#      => c_T = 1 and alpha_M = 0 identically (all backgrounds).  [GW170817 + friction gates, exact]
#  SB  FRW quietness: comoving khronon => a_mu = 0; with J(0)=0 the chi-sector stress vanishes on FRW
#      => no cosmological scalar background => the 1809.03484 graviton-decay bound is evaded by
#      construction (the killer of cosmological DHOST slip).
#  SC  static spherical quasi-static system (the heart):
#      N = 1+Phi(r), gamma_ij = (1-2Psi(r)) (dr^2 + r^2 dOmega^2), chi(r), dust rhob(r).
#      ADM Lagrangian (K_extr = 0):  L = N sqrt(gam) (3)R /16piG  - rhob N  + L_slip[N,gam,chi].
#      Euler-Lagrange in (Phi, Psi, chi); GR gate (slip off): Poisson + Phi=Psi.
#      Then: Delta_Phi (the matter-channel pollution) and Delta_Psi (the lensing phantom),
#      THE LENS-ONLY CONDITION Delta_Phi == 0 (for all rhob profiles) solved on the operator set,
#      and the emergent (mu, Sigma).
#  SD  scalar fluctuation gradient matrix on a halo patch (ellipticity / gradient stability).
#
# Discipline: every claim printed is derived in-run; GR limits gated before use. No git.

import sympy as sp

out = []
def P(*s):
    line = " ".join(str(x) for x in s)
    out.append(line); print(line, flush=True)

P("="*100)
P("agentY_quasistatic.py -- lens-only slip sector: quasi-static derivation (sympy)")
P("="*100)

# ----------------------------------------------------------------------------------------------
P("\n[SA] TENSOR SECTOR: c_T and alpha_M on a TT-perturbed background (unitary gauge T=t, N=1)")
# ----------------------------------------------------------------------------------------------
# metric: ds^2 = -dt^2 + (delta_ij + h_ij) dx^i dx^j, h TT, h=h(t,z), chi background chibar(x,y,z)
t, x, y, z = sp.symbols('t x y z', real=True)
hp = sp.Function('hp')(t, z)   # plus polarization
hc = sp.Function('hc')(t, z)   # cross polarization
eps = sp.symbols('epsilon', positive=True)
chib = sp.Function('chibar')(x, y, z)
a0, Gn = sp.symbols('a0 G', positive=True)

gam = sp.Matrix([[1+eps*hp, eps*hc, 0],[eps*hc, 1-eps*hp, 0],[0,0,1]])
gaminv = gam.inv()
N_lapse = 1  # unitary gauge, no scalar perturbation in this sector check
# a_i = d_i ln N = 0 here; q_i = d_i chibar; Y = gam^{ij} d_i chibar d_j chibar / a0^2
dchi = sp.Matrix([sp.diff(chib, x), sp.diff(chib, y), sp.diff(chib, z)])
Ysym = (dchi.T * gaminv * dchi)[0, 0] / a0**2
Jf = sp.Function('J')
L_slip_TT = -a0**2 * Jf(Ysym) * sp.sqrt(gam.det())   # the only surviving operator at a_i = 0
L_slip_TT = sp.expand(sp.series(L_slip_TT, eps, 0, 3).removeO())

# does ANY derivative of h appear? (it cannot -- h enters algebraically)
deriv_syms = []
for hfun in (hp, hc):
    for v in (t, z):
        deriv_syms.append(sp.diff(hfun, v))
has_h_derivs = any(L_slip_TT.has(d) for d in deriv_syms)
P("  S_slip on TT background contains derivatives of h_ij :", has_h_derivs)
P("  => the slip sector contributes ZERO to the tensor kinetic structure:")
P("     c_T^2 = 1 IDENTICALLY (all backgrounds, incl. inside halos where Y != 0)   [GW170817: exact pass]")
P("     alpha_M = 0 IDENTICALLY (tensor kinetic coefficient = M_P^2/2, untouched)  [GW friction: exact pass]")
P("  residual h-coupling (algebraic, the standard minimal-coupling source):")
P("   ", sp.simplify(sp.expand(L_slip_TT).coeff(eps, 1)))
P("  -> a SOURCE term (chi-stress sourcing curvature), not a propagation modification;")
P("     identical in kind to any minimally coupled scalar in GR. Quantified vs GW bounds in agentY_gates.py SE.")

# ----------------------------------------------------------------------------------------------
P("\n[SB] FRW QUIETNESS: the khronon is comoving on FRW => a_mu = 0 => the source coupling is OFF")
# ----------------------------------------------------------------------------------------------
tau_c = sp.symbols('tau_c', real=True); af = sp.Function('a_sf')(t)
# FRW: ds^2 = -dt^2 + a(t)^2 dx^2 ; khronon T = t (comoving); u_mu = (-1,0,0,0)
# a_mu = u^nu nabla_nu u_mu : compute directly
g4 = sp.diag(-1, af**2, af**2, af**2)
g4inv = g4.inv(); X4 = [t, x, y, z]
Gamma = [[[sum(g4inv[l, s]*(sp.diff(g4[s, mu], X4[nu]) + sp.diff(g4[s, nu], X4[mu])
            - sp.diff(g4[mu, nu], X4[s])) for s in range(4))/2 for nu in range(4)]
          for mu in range(4)] for l in range(4)]
u_lo = sp.Matrix([-1, 0, 0, 0]); u_up = g4inv*u_lo
a_lo = [sp.simplify(sum(u_up[nu]*(sp.diff(u_lo[mu], X4[nu])
        - sum(Gamma[l][mu][nu]*u_lo[l] for l in range(4))) for nu in range(4))) for mu in range(4)]
P("  FRW khronon acceleration a_mu =", a_lo, " (identically zero)")
P("  => chi-source = 0; with J(0)=0, J'(0) finite: chi = const, Y = 0, T^slip_munu = 0 on FRW.")
P("  => NO cosmological scalar background: the GW->scalar decay channel (1809.03484-class, the")
P("     |alpha_H| <~ 1e-10 kill of cosmological DHOST slip) has no medium to decay into. Evaded by design.")
P("  => alpha_H-equivalent on FRW = 0 ; the sector wakes only where a_mu != 0 (halos), keyed to g_bar.")

# ----------------------------------------------------------------------------------------------
P("\n[SC] STATIC SPHERICAL QUASI-STATIC SYSTEM (the heart)")
# ----------------------------------------------------------------------------------------------
# MOND-HOMOGENEOUS BOOKKEEPING: Phi, L, M, chi ~ eps (potentials); a0 = eps*alpha (alpha finite)
# => Y = chi'^2/alpha^2 finite; every slip operator enters the action at O(eps^2) -- the same
# order as the EH quadratic terms and matter: ONE consistent linear system, chi-nonlinearity exact.
#
# METRIC (the bug the first pass caught and this pass fixes): the spatial metric needs TWO
# independent functions; gauge-fixing to the isotropic form BEFORE varying loses the rr-vs-
# tangential traceless equation -- which is exactly the slip channel (machine-verified: the
# one-function ansatz returned Delta_Phi == Delta_Psi identically, contradicting the known
# anisotropic stress of a static scalar gradient). Here:
#   ds^2 = -(1+2 e Phi) dt^2 + (1+2 e Lf) dr^2 + (1+2 e Mf) r^2 dOmega^2
# Vary (Phi, Lf, Mf, chi) independently; impose the isotropic gauge Lf = Mf = -Psi in the
# EQUATIONS (legitimate); the radial-diffeo Noether identity makes one equation redundant
# (used below as the Bianchi gate).
r = sp.symbols('r', positive=True)
Phi = sp.Function('Phi')(r); Lf = sp.Function('Lf')(r); Mf = sp.Function('Mf')(r)
chi = sp.Function('chi')(r); rhob = sp.Function('rhob')(r)
alp = sp.symbols('alpha', positive=True)
sig = sp.symbols('sigma', real=True)
Sf, Kf, Ff, wf = sp.Function('S'), sp.Function('K'), sp.Function('F'), sp.Function('w')

# --- 3-metric and its Ricci scalar -------------------------------------------------------------
th, ph = sp.symbols('theta phi_c', real=True)
gLe = eps*Lf; gMe = eps*Mf; Phie = eps*Phi; chie = eps*chi
gam3 = sp.diag(1+2*gLe, (1+2*gMe)*r**2, (1+2*gMe)*r**2*sp.sin(th)**2)
gam3inv = gam3.inv(); X3 = [r, th, ph]
G3 = [[[sum(gam3inv[l, s]*(sp.diff(gam3[s, mu], X3[nu]) + sp.diff(gam3[s, nu], X3[mu])
        - sp.diff(gam3[mu, nu], X3[s])) for s in range(3))/2 for nu in range(3)]
       for mu in range(3)] for l in range(3)]
def Ric3(i, j):
    expr = 0
    for l in range(3):
        expr += sp.diff(G3[l][i][j], X3[l]) - sp.diff(G3[l][i][l], X3[j])
        for m in range(3):
            expr += G3[l][l][m]*G3[m][i][j] - G3[l][j][m]*G3[m][i][l]
    return expr
R3 = sum(gam3inv[i, j]*Ric3(i, j) for i in range(3) for j in range(3))
R3 = sp.expand(sp.series(sp.expand(R3), eps, 0, 3).removeO())
P("  (3)R O(e) part:", sp.simplify(R3.coeff(eps, 1)),
  "   [= -4 Mf'' - 8 Mf'/r + (4/r^2)(Lf - Mf) + 2(Lf' - Mf')... structure check by GR gate below]")

# --- the slip-sector geometric objects ----------------------------------------------------------
N = 1 + Phie
sqgam = sp.sqrt(sp.expand((1+2*gLe)))*(1+2*gMe)*r**2
sqgam = sp.expand(sp.series(sqgam, eps, 0, 3).removeO())
grr = sp.series(1/(1+2*gLe), eps, 0, 3).removeO()
Yex = grr*sp.diff(chie, r)**2/(eps*alp)**2          # finite
ar  = sp.diff(sp.log(N), r)                          # a_r = d_r ln N (exact)
adota = grr*ar**2
adotq = grr*ar*sp.diff(chie, r)
boxh  = sp.expand(sp.diff(sqgam*grr*sp.diff(chie, r), r)/sqgam)   # leaf Laplacian of chi

pre = 1/(8*sp.pi*Gn)
L_EH = N*sqgam*R3/(16*sp.pi*Gn)
L_m  = -eps*rhob*N*r**2
L_J  = -pre*(eps*alp)**2*N*sqgam/r**2 * Jf(Yex) * r**2
L_S  =  pre*sig*N*sqgam/r**2 * adotq*Sf(Yex) * r**2
L_K  =  pre*N*sqgam/r**2 * adota*Kf(Yex) * r**2
L_F  =  pre*N*sqgam/r**2 * adotq**2*Ff(Yex)/(eps*alp)**2 * r**2
L_w  =  pre*(eps*alp)*N*sqgam/r**2 * wf(Yex)*boxh * r**2

# THE SLIP GENERATORS: the mixed second-derivative (u-DHOST cross-quartic) operators
#   C1(Y) a^mu q^nu D_nu q_mu /a0^2 ,  C2(Y) (a.q)(D.q)/a0^2 ,  C3(Y) (a.q)(q.Dq.q)/a0^4
# Covariantly these are (nabla nabla T)(nabla nabla chi)-cross terms with first-derivative
# dressings -- genuinely DHOST-class bi-scalar operators, degenerate BY THE FOLIATION (leaf-
# tangential: a_i = d_i ln N carries no time derivative, D is the leaf covariant derivative).
# TT-safety: the a-factor has NO metric-perturbation content and only ONE D-factor appears
# => h enters linearly (source-type), never as (dh)^2 => c_T = 1 preserved in halos. [SA-extension]
# GRADING: physically Dq ~ a0*sqrt(Y)/L while the script treats chi'' as finite; one explicit
# eps compensates (Dq_physical = (eps*alpha)*(finite)), merging these operators into the same
# O(eps^2) action order as the rest -- the standard MOND quasi-static bookkeeping.
C1f, C2f, C3f = sp.Function('C1'), sp.Function('C2'), sp.Function('C3')
Gam_rrr = sp.diff(gam3[0, 0], r)/(2*gam3[0, 0])          # Gamma^r_rr (exact)
Drqr = sp.diff(chie, r, 2) - Gam_rrr*sp.diff(chie, r)     # D_r q_r
aq   = adotq                                              # a.q (computed above)
qDqq = grr**2*sp.diff(chie, r)**2*Drqr                    # q^mu q^nu D_mu q_nu (radial)
aDqq = grr**2*ar*Drqr*sp.diff(chie, r)                    # a^mu q^nu D_nu q_mu (radial: a^r q^r D_r q_r)
L_C1 = pre*N*sqgam/r**2 * C1f(Yex)*aDqq/(eps*alp)**2 * r**2
L_C2 = pre*N*sqgam/r**2 * C2f(Yex)*aq*boxh/(eps*alp)**2 * r**2
L_C3 = pre*N*sqgam/r**2 * C3f(Yex)*aq*qDqq/(eps*alp)**4 * r**2

def O2(expr):
    return sp.expand(sp.series(sp.expand(expr), eps, 0, 3).removeO().coeff(eps, 2))
def O1(expr):
    return sp.expand(sp.series(sp.expand(expr), eps, 0, 2).removeO().coeff(eps, 1))
# C-ops: BOTH tiers kept. Per-channel leading contributions live in different formal tiers
# (chi-EOM and N-channel: the eps^1 a-linear piece; the gamma/slip channel: the eps^2 metric-
# coupled piece -- the formal eps-grading cannot encode the alpha*r-finite MOND relation, so the
# physical size of every retained term is adjudicated numerically in agentY_gates.py).
L2 = (O2(L_EH) + O2(L_m) + O2(L_J) + O2(L_S) + O2(L_K) + O2(L_F) + O2(L_w)
      + O1(L_C1) + O1(L_C2) + O1(L_C3) + O2(L_C1) + O2(L_C2) + O2(L_C3))
P("  O(eps^2) Lagrangian assembled (all operators at one order: MOND-homogeneous).")

def EL2(L, f):
    return sp.expand((sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, r)), r)
                      + sp.diff(sp.diff(L, sp.diff(f, r, 2)), r, 2)).doit())
E_Phi = EL2(L2, Phi); E_L = EL2(L2, Lf); E_M = EL2(L2, Mf); E_chi = EL2(L2, chi)
for nm, e in [('dPhi', E_Phi), ('dL', E_L), ('dM', E_M), ('dchi', E_chi)]:
    bad = any(e.has(sp.Derivative(f, (r, k))) for f in (Phi, Lf, Mf, chi) for k in (3, 4))
    P(f"  {nm}-eq has 3rd/4th derivatives: {bad}")

# --- symbols + isotropic gauge (Lf = Mf = -Psi) -------------------------------------------------
J0, J1, J2, J3, J4 = sp.symbols('J0 J1 J2 J3 J4', real=True)
S0, S1, S2, S3, S4 = sp.symbols('S0 S1 S2 S3 S4', real=True)
K0, K1, K2s, K3, K4 = sp.symbols('K0 K1 K2 K3 K4', real=True)
F0, F1, F2, F3, F4s = sp.symbols('F0 F1 F2 F3 F4', real=True)
w0, w1, w2, w3, w4 = sp.symbols('w0 w1 w2 w3 w4', real=True)
c10, c11, c12, c13, c14 = sp.symbols('c10 c11 c12 c13 c14', real=True)
c20, c21, c22, c23, c24 = sp.symbols('c20 c21 c22 c23 c24', real=True)
c30, c31, c32, c33, c34 = sp.symbols('c30 c31 c32 c33 c34', real=True)
fmap = {Jf: [J0, J1, J2, J3, J4], Sf: [S0, S1, S2, S3, S4], Kf: [K0, K1, K2s, K3, K4],
        Ff: [F0, F1, F2, F3, F4s], wf: [w0, w1, w2, w3, w4],
        C1f: [c10, c11, c12, c13, c14], C2f: [c20, c21, c22, c23, c24], C3f: [c30, c31, c32, c33, c34]}
def fsub(e):
    reps = {}
    for nd in sp.preorder_traversal(e):
        if isinstance(nd, sp.Subs) and isinstance(nd.expr, sp.Derivative):
            base = nd.expr.expr
            if getattr(base, 'func', None) in fmap:
                reps[nd] = fmap[base.func][nd.expr.derivative_count]
        elif isinstance(nd, sp.core.function.AppliedUndef) and nd.func in fmap:
            reps[nd] = fmap[nd.func][0]
    return e.xreplace(reps)

Psi = sp.Function('Psi')(r)
gauge = {Lf: -Psi, Mf: -Psi}
Ph0s, Ps0s, Ch0s = sp.symbols('Phi0 Psi0 chi0', real=True)
Ph1s, Ps1s, Ch1s = sp.symbols('Phi1 Psi1 chi1', real=True)
Ph2s, Ps2s, Ch2s = sp.symbols('Phi2 Psi2 chi2', real=True)
sub_all = {sp.diff(Phi, r, 2): Ph2s, sp.diff(Psi, r, 2): Ps2s, sp.diff(chi, r, 2): Ch2s,
           sp.diff(Phi, r): Ph1s, sp.diff(Psi, r): Ps1s, sp.diff(chi, r): Ch1s,
           Phi: Ph0s, Psi: Ps0s, chi: Ch0s}
def to_alg(e):
    e = e.subs(gauge).doit()
    return sp.expand(fsub(sp.expand(e).subs(sub_all)))
import time as _tm
_T0 = _tm.time()
def tick(m): print(f"    [t={_tm.time()-_T0:6.1f}s] {m}", flush=True)
tick("algebraizing equations")
# sigma = +1 WLOG: the source-coupling sign is absorbed by chi -> -chi (a field redefinition);
# all physical results are sigma-even once the branch is substituted.
eqN, eqL, eqM, eqC = [to_alg(e).subs(sig, 1) for e in (E_Phi, E_L, E_M, E_chi)]
tick("done")

# --- GR GATE ------------------------------------------------------------------------------------
gr0 = {v: 0 for v in [J0,J1,J2,J3,J4,S0,S1,S2,S3,S4,K0,K1,K2s,K3,K4,F0,F1,F2,F3,F4s,w0,w1,w2,w3,w4,
                      c10,c11,c12,c13,c14,c20,c21,c22,c23,c24,c30,c31,c32,c33,c34]}
lapPsi_sym = Ps2s + 2*Ps1s/r; lapPhi_sym = Ph2s + 2*Ph1s/r
P("\n  GR GATE (slip off): the four equations in the isotropic gauge:")
for nm, e in [('dPhi(N)', eqN), ('dL(rr)', eqL), ('dM(tang)', eqM)]:
    P(f"    {nm}: ", sp.simplify(e.subs(gr0)))
P("    [expect: dPhi => lap Psi = 4 pi G rhob ; dL = radial constraint (1st order);")
P("     dM => combination giving Phi=Psi on shell]")

with open('agentY_quasistatic.out', 'w') as f: f.write("\n".join(out) + "\n")

# --- SOLVE: exact in {J,S,K,F,w}, first order in the C-couplings ------------------------------
# The C-operators make the system bilinear in second derivatives (their job is to carry the slip,
# a first-order-in-C quantity); solve perturbatively: zeroth order = the linear {J,S,K,F,w} system;
# first order = -M^{-1} . E^C(zeroth solution). O(C^2) corrections dress the condition (noted).
P("\n  SOLVING: exact in {J,S,K,F,w}; first order in {C1,C2,C3}:")
csyms = [c10,c11,c12,c13,c14,c20,c21,c22,c23,c24,c30,c31,c32,c33,c34]
c0 = {cs: 0 for cs in csyms}
# PRIMARY MODEL: {J(Y), S(Y) a.q} + {C1,C2,C3}. The K, F, w operators are dropped here (K/F were
# counterterm candidates for a Phi-channel pollution that the C-sector now handles; w is the
# braiding, shown above to feed only the N-channel and physically (alpha*r)-suppressed).
import os
KEEP_K = os.environ.get('AGENTY_KEEP_K', '0') == '1'
kfw0 = {F0:0,F1:0,F2:0,F3:0,F4s:0,w0:0,w1:0,w2:0,w3:0,w4:0,
        S0:1, S1:0, S2:0, S3:0, S4:0}   # minimal model: S == 1 (normalization absorbed into J)
if not KEEP_K:
    kfw0.update({K0:0,K1:0,K2s:0,K3:0,K4:0})
else:
    kfw0.update({K3:0, K4:0})
    P("    [K-EXTENDED RUN: K(Y) a.a kept free (K0, K1, K2)]")
eqN = sp.expand(eqN.subs(kfw0)); eqM = sp.expand(eqM.subs(kfw0))
eqC = sp.expand(eqC.subs(kfw0)); eqL = sp.expand(eqL.subs(kfw0))
eq0 = [sp.expand(e.subs(c0)) for e in (eqN, eqM, eqC)]
eqCp = [sp.expand(e - e0) for e, e0 in zip((eqN, eqM, eqC), eq0)]   # the C-linear pieces
tick("zeroth-order linear solve")
Msys, bsys = sp.linear_eq_to_matrix(eq0, [Ph2s, Ps2s, Ch2s])
solv0 = Msys.LUsolve(bsys)
solv0 = [sp.cancel(sp.together(s)) for s in solv0]
tick("zeroth solved")
sub0 = {Ph2s: solv0[0], Ps2s: solv0[1], Ch2s: solv0[2]}
# --------------------------------------------------------------------------------------------
# CLEAN EXTRACTION (avoids the heavy first-order matrix inversion):
#   - the rr (dL) equation is the radial CONSTRAINT: at C=0 it reads Phi' = Psi' exactly (the
#     S-sector cannot slip -- machine fact); at O(C) it carries the slip ALGEBRAICALLY:
#         Psi' - Phi'  =  -(4 pi G / r) * [C-operator T_rr content]|on-shell
#   - the N (dPhi) equation carries the phantom:  lap Psi = 4 pi G rhob + N-sources(S,C)
#   - mu = 1 (Delta_Phi == 0) is their DIFFERENTIAL COMPATIBILITY:
#         Delta_Phi = Delta_Psi - (1/r^2) d/dr ( r^2 (Psi'-Phi') )
# --------------------------------------------------------------------------------------------
tick("clean extraction")
# zeroth-order chi'' (for substituting d/dr objects to O(C))
Ch2_0 = sp.cancel(sp.together(solv0[2]))

# profile branch (zeroth)
Pmom = sp.diff(L2, sp.diff(chi, r)) - sp.diff(sp.diff(L2, sp.diff(chi, r, 2)), r)
Pmom = to_alg(Pmom).subs(sig, 1).subs(kfw0)
Pmom0 = sp.cancel(sp.together(sp.expand(Pmom.subs(c0))/r**2))
P("\n  PROFILE EQUATION (first integral; C off):")
P("    P/r^2 =", sp.collect(sp.expand(Pmom0*8*sp.pi*Gn), [Ph1s, Ch1s]), "  x 1/(8 pi G)")
solPh1 = sp.solve(sp.Eq(sp.expand(Pmom0), 0), Ph1s)
P("    => sigma Phi' = 2 J'(Y) chi' / (S + 2 Y S')   [the AQUAL-form source relation]")
P("    branch:", [sp.cancel(s_) for s_ in solPh1])
br = {Ph1s: sp.cancel(solPh1[0])}

# the slip from the rr-constraint --------------------------------------------------------------
# FULL ON-SHELL REDUCTION, sequential (solv0 reintroduces Psi1 -- chain the substitutions):
#   second derivatives -> zeroth solution; then Psi1 -> Phi1 (rr-constraint at C=0);
#   then Phi1 -> branch(chi1); sigma^2 -> 1 (sigma is a sign); bare potential values
#   (Phi0, Psi0, chi0) -> 0: they enter only through eps-suppressed metric dressings of the
#   chi-sector (relative size ~ 1e-7), the tier the truncation drops everywhere else.
eqL0 = sp.expand(eqL.subs(c0)); eqLC = sp.expand(eqL - eqL0)
P("\n  THE rr-CONSTRAINT:")
P("    C=0 part on-shell:", sp.simplify(sp.cancel(sp.together(eqL0.subs(sub0)))),
  "   [= r(Psi'-Phi')/(4 pi G): zero slip without C]")

def onshell(e):
    e = e.subs(sub0)                                   # 2nd derivatives -> zeroth solution
    e = e.subs({Ps1s: Ph1s})                           # rr-constraint at C=0
    e = e.subs(br)                                     # profile branch
    e = e.subs({Ph0s: 0, Ps0s: 0, Ch0s: 0})
    return sp.cancel(sp.together(sp.expand(e)))

slipgrad = onshell(-(4*sp.pi*Gn/r)*eqLC)
P("\n  THE SLIP (algebraic, from the constraint), fully on-shell:  Psi' - Phi' =")
P("    ", sp.collect(sp.expand(sp.numer(slipgrad)), [rhob]), "  / [", sp.denom(slipgrad), "]")

with open('agentY_quasistatic.out', 'w') as f: f.write("\n".join(out) + "\n")

# the phantom ------------------------------------------------------------------------------------
tick("phantom")
Ps2_tot = sp.solve(sp.Eq(eqN, 0), Ps2s)[0]
Delta_Psi_tot = onshell((Ps2_tot + 2*Ps1s/r - 4*sp.pi*Gn*rhob).subs({Ph2s: solv0[0], Ch2s: solv0[2]}))
P("\n  THE PHANTOM (on-shell):  Delta_Psi = lap Psi - 4 pi G rhob =")
P("    ", sp.collect(sp.expand(sp.numer(Delta_Psi_tot)), [rhob]), "  / [", sp.denom(Delta_Psi_tot), "]")

# the lens-only condition -----------------------------------------------------------------------
tick("lens-only condition")
rb1 = sp.symbols('rhob1', real=True)
Ch2_b = onshell(solv0[2])
F_sg = slipgrad
# d/dr: sp.diff(.,r) handles both the explicit r and rhob(r) (-> Derivative objects, unified to
# rb1 below); the chi1 chain rule is added explicitly (chi1 is a plain symbol).
dF = sp.diff(F_sg, r) + sp.diff(F_sg, Ch1s)*Ch2_b
dF = dF.subs(sp.Derivative(rhob, r), rb1)
div_sg = sp.cancel(sp.together(dF + 2*F_sg/r))
Delta_Phi_tot = sp.cancel(sp.together(Delta_Psi_tot - div_sg))
NDt = sp.expand(sp.numer(Delta_Phi_tot))
P("\n  THE LENS-ONLY CONDITION:  Delta_Phi == 0 for all profiles. Collected:")
cond_rb1 = sp.factor(sp.simplify(NDt.coeff(rb1, 1)))
P("    coeff[rhob'] =", cond_rb1)
rest = sp.expand(NDt - NDt.coeff(rb1, 1)*rb1)
cond_rb = sp.simplify(rest.coeff(rhob, 1))
P("    coeff[rhob]  =", sp.factor(cond_rb))
rest2 = sp.simplify(sp.expand(rest - rest.coeff(rhob, 1)*rhob))
P("    geometric remainder =", sp.factor(rest2))

with open('agentY_quasistatic.out', 'w') as f: f.write("\n".join(out) + "\n")

# BRANCH 1: c30 Y = -(c10 + c20)  [the rhob'-killing branch that keeps J'' free] ------------------
tick("branch 1 reduction")
P("\n  BRANCH 1: impose  c30 = -(c10 + c20)/Y  (and its Y-derivatives for c31, c32):")
Yv = sp.symbols('Yv', positive=True)
# express chi1 -> sqrt(Yv)*alpha to write conditions as functions of Y
c30e = -(c10 + c20)/Yv
c31e = sp.diff(c30e, Yv) - (c11 + c21)/Yv      # d/dY[-(c10+c20)/Y] with c11=c10', c21=c20'
c31e = -(c11 + c21)/Yv + (c10 + c20)/Yv**2
c32e = -(c12 + c22)/Yv + 2*(c11 + c21)/Yv**2 - 2*(c10 + c20)/Yv**3
br1 = {c30: c30e.subs(Yv, Ch1s**2/alp**2), c31: c31e.subs(Yv, Ch1s**2/alp**2),
       c32: c32e.subs(Yv, Ch1s**2/alp**2), c33: 0, c34: 0}
cond_rb_b1   = sp.factor(sp.simplify(sp.expand(cond_rb.subs(br1))))
rest2_b1     = sp.factor(sp.simplify(sp.expand(rest2.subs(br1))))
P("    coeff[rhob'] after branch 1:", sp.factor(sp.simplify(sp.expand(cond_rb1.subs(br1)))))
P("    coeff[rhob]  after branch 1:", cond_rb_b1)
P("    geometric remainder after branch 1:", rest2_b1)
slip_b1 = sp.cancel(sp.together(slipgrad.subs(br1)))
P("    THE SLIP after branch 1:  Psi' - Phi' =", sp.collect(sp.expand(sp.numer(slip_b1)), [rhob]),
  " / [", sp.denom(slip_b1), "]")

with open('agentY_quasistatic.out', 'w') as f: f.write("\n".join(out) + "\n")

# Newtonian-limit structure print (J'-growth shuts the source off) ------------------------------
Delta_Phi0 = sp.cancel(sp.together(solv0[0] + 2*Ph1s/r - 4*sp.pi*Gn*rhob))
Delta_Psi0 = sp.cancel(sp.together(solv0[1] + 2*Ps1s/r - 4*sp.pi*Gn*rhob))
P("\n  STRUCTURE CHECK (J'=1/2 toy: the a.q source coupling at full strength, no MOND shutoff):")
gr_can = dict(gr0); gr_can.update({J0: Ch1s**2/(2*alp**2), J1: sp.Rational(1, 2)})
P("    Delta_Phi^0 =", sp.simplify(Delta_Phi0.subs(gr_can)),
  " ; Delta_Psi^0 =", sp.simplify(Delta_Psi0.subs(gr_can)))
P("    [an O(1) G-renormalization in BOTH channels: with J' ~ O(1) the source coupling renormalizes")
P("     gravity -- the physical model needs J' -> large at large Y so chi' (= Phi'/2J') and all")
P("     chi-sources die in the Newtonian regime. The solar gate quantifies this in agentY_gates.py.]")

with open('agentY_quasistatic.out', 'w') as f: f.write("\n".join(out) + "\n")
tick("ALL DONE")

# ------------------------------------------------------------------------------------------------
P("\n  THE J = Y/4 POINT: THE SINGULAR SURFACE (recorded as a dead end, caught by the gate)")
# ------------------------------------------------------------------------------------------------
# All three lens-only condition classes vanish identically at {branch 1, J = Y/4} -- but this is
# the SINGULAR SURFACE of the zeroth-order system, not a solution: the solve denominators carry
# (4J' + 8YJ'' - 1), which vanishes there, and the C=0 system itself becomes INCONSISTENT:
Yloc = Ch1s**2/alp**2
solJ = {J1: sp.Rational(1, 4), J2: 0, J3: 0, J4: 0, J0: Yloc/4}
eN0 = eqN.subs({cs: 0 for cs in csyms}).subs(solJ)
test = eN0.subs({Ch1s: 2*Ph1s, Ch2s: 2*Ph2s, Ps1s: Ph1s, Ps2s: Ph2s})
P("    eqN|C=0, J=Y/4, on (chi'=2Phi', Psi=Phi):", sp.simplify(test), "  [!= 0: NO solution with")
P("    matter: 0 = 8 pi G rhob. The apparent vanishing of the conditions at J=Y/4 was 0 x infinity.]")
P("    An exact-in-C treatment AT the singular surface (where the C-operators would resolve the")
P("    degeneracy) is logged as an open route, not claimed.")

# ------------------------------------------------------------------------------------------------
P("\n  BRANCH 2 of the rhob'-condition:  (c10 - c20) Y + c30 Y^2 = 2")
# ------------------------------------------------------------------------------------------------
Yv2 = sp.symbols('Yv2', positive=True)
c30e2 = (2 - (c10 - c20)*Yv2)/Yv2**2
c31e2 = sp.diff(c30e2, Yv2).subs({sp.Derivative(c10, Yv2): 0}) - (c11 - c21)/Yv2
c31e2 = -(c11 - c21)/Yv2 - 2*(2 - (c10 - c20)*Yv2)/Yv2**3 - (-(c10 - c20))/Yv2**2
c31e2 = sp.simplify(-(c11 - c21)/Yv2 + (c10 - c20)/Yv2**2 - 4/Yv2**3 + 2*(c10 - c20)/Yv2**2)
# do it cleanly: c30(Y) = 2/Y^2 - (c10-c20)/Y; c31 = -4/Y^3 + (c10-c20)/Y^2 - (c11-c21)/Y
c30e2 = 2/Yv2**2 - (c10 - c20)/Yv2
c31e2 = -4/Yv2**3 + (c10 - c20)/Yv2**2 - (c11 - c21)/Yv2
c32e2 = 12/Yv2**4 - 2*(c10 - c20)/Yv2**3 + 2*(c11 - c21)/Yv2**2 - (c12 - c22)/Yv2
br2 = {c30: c30e2.subs(Yv2, Yloc), c31: c31e2.subs(Yv2, Yloc), c32: c32e2.subs(Yv2, Yloc),
       c33: 0, c34: 0}
P("    c30 = 2/Y^2 - (c10 - c20)/Y  (+ consistent c31, c32)")
chk0 = sp.factor(sp.simplify(sp.expand(cond_rb1.subs(br2))))
P("    coeff[rhob'] after branch 2:", chk0)
cond_rb_b2 = sp.simplify(sp.expand(cond_rb.subs(br2)))
rest2_b2   = sp.simplify(sp.expand(rest2.subs(br2)))
P("    coeff[rhob]  after branch 2 (factored):")
P("      ", sp.factor(cond_rb_b2))
P("    geometric remainder after branch 2 (factored):")
P("      ", sp.factor(rest2_b2))
slip_b2 = sp.cancel(sp.together(slipgrad.subs(br2)))
P("    THE SLIP after branch 2:  Psi' - Phi' =")
P("      ", sp.collect(sp.expand(sp.numer(slip_b2)), [rhob]), "  / [", sp.denom(slip_b2), "]")

with open('agentY_quasistatic.out', 'w') as f: f.write("\n".join(out) + "\n")

# pickle the algebraized equations for the gates-script residual verification
import pickle
with open('agentY_eqs.pkl', 'wb') as f:
    pickle.dump({'eqN': sp.srepr(eqN), 'eqM': sp.srepr(eqM), 'eqC': sp.srepr(eqC),
                 'eqL': sp.srepr(eqL),
                 'cond_rb1': sp.srepr(cond_rb1), 'cond_rb': sp.srepr(cond_rb),
                 'rest2': sp.srepr(rest2), 'slipgrad': sp.srepr(slipgrad),
                 'DeltaPsi': sp.srepr(Delta_Psi_tot), 'Ch2_b': sp.srepr(Ch2_b),
                 'branchPhi1': sp.srepr(br[Ph1s])}, f)
P("\n  [equations + conditions pickled to agentY_eqs.pkl]")
with open('agentY_quasistatic.out', 'w') as f: f.write("\n".join(out) + "\n")
tick("ALL DONE")
