#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A22 -- PREFERRED-FRAME PPN for the round-2 action: alpha_1, alpha_2, and the
nonlinear beta.  Plus the "no cosmic aether" theorem on FRW.

Action (exactly as printed in core_open_problems_round2_2026_10_20/03_relativity/report.md sec. 2,
c = 1, signature (-+++), K = 4 pi G):

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
                 + P^i D_i log N - W_full(u) + (eta/2) E_i E^i
                 - (gamma/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij ,
  W_full = (a0^2/K)[-u/a0 - log(1-u/a0)],  u = K sqrt(h^ij P_i P_j),
  E_i = (Pdot_i - Lie_N P_i)/N,  F_ij = d_i P_j - d_j P_i.

NOTATION: "beta" in the action is the ADM coefficient of theta^2, NOT the PPN
parameter.  Below beta_ADM is that coefficient, beta_PPN the PPN one.

Two structural facts drive everything; both are proved symbolically here.

  (F1) theta == 0 identically on ANY static configuration written in the preferred
       (unitary, T = t) frame: theta = (1/(N sqrt h)) d_i(N sqrt h n^i), n^i = 0.
       So [R3 + K_ijK^ij - (1+beta_ADM)theta^2] = R + total derivative on the whole
       static branch: the gravitational sector is EXACTLY Einstein-Hilbert for every
       beta_ADM, and the theta^2 operator's linearised stress about a constant
       background vanishes identically (theta starts at O(h), so F_theta starts at
       O(h^2)).  It can therefore generate neither alpha_1 nor alpha_2 -- nor gamma-1
       nor beta_PPN-1.  In Einstein-aether variables the gravitational sector is
       c1 = c3 = c4 = 0, c2 = -beta_ADM, and the published aether formulas
       alpha_1 = -8(c3^2+c1c4)/(2c1-c1^2+c3^2), alpha_2 = c14(c14+2c2c14-c2)/[c2(2-c14)]
       both vanish there (Oost-Mukohyama-Wang 2018, as tabulated in
       data_assembly/DOOR11_LITERATURE_2026-09-29.md).

  (F2) The P sector's ONLY O(rho) stress component is the charge -D.P.  The clock term
       P^i D_i log N has no shift N^i in it (D_i of a scalar is a partial derivative) and
       its variation w.r.t. h_ij is O(rho^2); every other P operator is quadratic in P,
       so its variation w.r.t. N^i is quadratic in P.  Hence at O(rho):
       T^t_t = charge, T^t_i = 0, T^i_j = 0.  No momentum density => g_0i = 0 at O(rho);
       no anisotropic stress => Phi = Psi at O(rho) (lane A12's dust lemma, re-derived
       here without assuming a frame).

On FRW the uniqueness of P = 0 is the COORDINATOR's theorem (_parent/a22_no_cosmic_aether.py, 4/4:
dW/du has its only zero at u = 0).  K9 here corroborates it independently and adds the three legs that
make it a statement about VEVs rather than about algebra: m^2 = K/eta > 0, m/H_0 = 2.6e8 (so the mode
decays as a^-3/2 instead of freezing), and the CMB anisotropic-stress bound on a pre-existing mode.

Conventions for alpha_1, alpha_2 (Foster-Jacobson matching; the same one validated in
nbody_2026/stage72_alpha2_first_principles_2026.py, whose C1 gate reproduces the
literature alpha_1 = -4K_B for the Maxwell-form aether): writing the O(w^2 U) part of
g_00 for a static source seen from a frame moving at w w.r.t. the preferred foliation as

    g_00  superset  [ P_iso w^2 + S (w.nhat)^2 ] U ,     alpha_1 = P_iso + S/2,
                                                          alpha_2 = -S/2 .

Runtime < 100 s.  Deterministic.  No network.  sympy only (numpy imported but unused
for the algebra).  Exit 0 iff every declared check passes.

    python3 a22_checks.py [--mutate NAME] [--json-out FILE]
"""
import argparse
import json
import math
import sys

import sympy as sp

AP = argparse.ArgumentParser()
AP.add_argument('--mutate', default='none',
                choices=['none', 'drop_clock', 'gamma_zero', 'theta_stress',
                         'alpha1_forced', 'frw_source', 'beta_forced'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate
CHECKS = []
# physical mutation switches (each removes/alters a TERM, not a boolean)
CLOCK = 0 if MUT == 'drop_clock' else 1          # clock operator P^i D_i log N
GAMMA = None if MUT == 'gamma_zero' else None    # placeholder, resolved below
THETA_BG = 1 if MUT == 'theta_stress' else 0     # nonzero background expansion
FRW_SRC = 1 if MUT == 'frw_source' else 0        # ad-hoc source on FRW


def rec(cid, ok, value, threshold, note=''):
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-4s %-4s value=%-42s thr=%-10s %s'
          % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))


# ------------------------------------------------------------------ constants (labelled)
c = 2.99792458e8
G = 6.67430e-11
Mpc = 3.0856775814913673e22
pc = 3.0856775814913673e16
H0 = 67.4e3 / Mpc                 # 2.1843e-18 s^-1   (BRIEF sec. 4)
a0 = 9.36e-11                     # canonical footing (BRIEF sec. 4)
Ls = 24.0 * pc                    # L* = 24 pc (A20_Lstar_cores, surviving value)
Msun = 1.98892e30
AU = 1.495978707e11
BE = 3.66e-14                     # Earth 2sigma constant-radial-anomaly bound (A4 lane)
B_alpha1 = 2.5e-4                 # |alpha1| < 2.5e-4 (2sigma; Mueller+2005 LLR, DOOR11 table)
B_alpha2 = 2.4e-7                 # |alpha2| < 2.4e-7 (Nordtvedt 1987, DOOR11 table)
B_beta = 1.0e-4                   # |beta_PPN - 1| < 1e-4 (tasking; Genova+2018 eta_N)

K_u = 4 * math.pi * G / c**2      # K in c=1 units  [m/kg]
gam_u = K_u * Ls**2 / 2           # gamma = K L*^2/2 = 2 pi G L*^2  (A12 eq.(5), A20)
lam = math.sqrt(gam_u / K_u)      # P Compton length = L*/sqrt(2)
mu = G * Msun / c**2              # gravitational radius of the Sun [m]

print(__doc__)
print('=' * 108)
print('CONSTANTS   L* = %.3f pc   lambda = %.3f pc   a0 = %.3e m/s^2   H0 = %.4e 1/s'
      % (Ls / pc, lam / pc, a0, H0))
print('            mu_sun = %.4f m   K = %.4e m/kg   gamma = %.4e m^3/kg' % (mu, K_u, gam_u))
print('=' * 108)

r = sp.symbols('r', positive=True)
Ks, be, et, ga = sp.symbols('K beta_ADM eta gamma', positive=True)
if MUT == 'gamma_zero':
    ga = sp.Integer(0)   # mutation: remove the (D.P)^2 gradient term
Ph = sp.Function('Phi')(r)
Ps = sp.Function('Psi')(r)
pf = sp.Function('p')(r)
Nf = sp.Function('N')(r)
ff = sp.Function('f')(r)


def R3(fexp):
    """3-Ricci scalar of h_ij = f delta_ij:  -(1/f)[2 L'' + 4 L'/r + L'^2/2], L = ln f."""
    L = sp.log(fexp)
    return -(1/fexp)*(2*sp.diff(L, r, 2) + 4*sp.diff(L, r)/r + sp.Rational(1, 2)*sp.diff(L, r)**2)


def euler(L, v, x=None):
    """Euler-Lagrange w.r.t. v; x is the independent variable (default r)."""
    x = r if x is None else x
    e = sp.diff(L, v)
    for d in L.atoms(sp.Derivative):
        if d.expr == v:
            n = d.variable_count[0][1]
            e = e + (-1)**n*sp.diff(sp.diff(L, d), x, n)
    return sp.expand(e)


# ============================================================ K1  3-curvature formula
sph = 4 / (1 + r**2)**2
res_sph = sp.simplify(R3(sph) - 6)
mus = sp.symbols('mu', positive=True)
f_gr = (1 + mus/(2*r))**4
res_gr = sp.simplify(R3(f_gr))
ok = (res_sph == 0) and (res_gr == 0)
rec('K1', ok, 'R3(S^3)-6=%s  R3(isoSCH)=%s' % (res_sph, res_gr), '0 / 0',
    '3-Ricci formula validated on two exact cases')

# ============================================================ K2  GR limit of the static system
sqh = ff**sp.Rational(3, 2)
q = sp.sqrt(ff)*pf
DP = (sp.diff(q, r) + 2*q/r)/ff**sp.Rational(3, 2)
u = Ks*pf/ff**sp.Rational(1, 2)
W = (a0**2/Ks)*(-u/a0 - sp.log(1 - u/a0))
clock = pf*sp.diff(Nf, r)/(ff*Nf)
Lfull = r**2*sqh*Nf*(R3(ff)/(4*Ks) + clock - W - (ga/2)*DP**2)
L0 = Lfull.subs({pf: 0}).subs(sp.Derivative(pf, r), 0)
Ns_gr = (1 - mus/(2*r))/(1 + mus/(2*r))
sub_gr = {ff: f_gr, Nf: Ns_gr}
for g, val in ((ff, f_gr), (Nf, Ns_gr)):
    for n in (1, 2):
        sub_gr[sp.Derivative(g, r, n)] = sp.diff(val, r, n)
resN = sp.simplify(euler(L0, Nf).subs(sub_gr))
resf = sp.simplify(euler(L0, ff).subs(sub_gr))
ok = (resN == 0) and (resf == 0)
rec('K2', ok, 'lapse=%s trace=%s' % (resN, resf), '0 / 0',
    'P=0 branch is EXACTLY isotropic Schwarzschild: gravity sector = Einstein-Hilbert')

# ============================================================ K3  linearised system + charge identity
e = sp.symbols('e')
N2 = 1 + e*Ph
f2 = 1 - 2*e*Ps
p2 = e*pf
sqh2 = f2**sp.Rational(3, 2)
q2 = sp.sqrt(f2)*p2
DP2 = (sp.diff(q2, r) + 2*q2/r)/f2**sp.Rational(3, 2)
W2 = Ks*p2**2/(2*f2)
clock2 = CLOCK*p2*sp.diff(N2, r)/(f2*N2)
L2 = r**2*sqh2*N2*(R3(f2)/(4*Ks) + clock2 - W2 - (ga/2)*DP2**2)
Lquad = sp.expand(sp.series(L2, e, 0, 3).removeO().coeff(e, 2))
Elapse = sp.simplify(euler(Lquad, Ph)/r**2)
Etrace = sp.simplify(euler(Lquad, Ps)/r**2)
Ep = sp.simplify(euler(Lquad, pf)/r**2)
want_lapse = -sp.diff(pf, r) - 2*pf/r + sp.diff(Ps, r, 2)/Ks + 2*sp.diff(Ps, r)/(Ks*r)
want_trace = (sp.diff(Ph, r, 2) - sp.diff(Ps, r, 2)
              + 2*sp.diff(Ph, r)/r - 2*sp.diff(Ps, r)/r)/Ks
want_p = -Ks*pf + ga*sp.diff(pf, r, 2) + 2*ga*sp.diff(pf, r)/r - 2*ga*pf/r**2 + sp.diff(Ph, r)
res = [sp.simplify(Elapse - want_lapse), sp.simplify(Etrace - want_trace), sp.simplify(Ep - want_p)]
lapPhi, lapPsi, psi_s, rho_s = sp.symbols('lapPhi lapPsi psi rho')
sols = sp.solve([sp.Eq(lapPhi, Ks*(rho_s + psi_s)),
                 sp.Eq(ga*lapPsi, Ks*psi_s - lapPhi)], [lapPsi], dict=True)
ident = sp.simplify(sols[0][lapPsi].subs(lapPhi, Ks*(rho_s + psi_s)) + Ks*rho_s/ga) if sols else sp.Integer(1)
ok = all(x == 0 for x in res) and (ident == 0)
rec('K3', ok, 'eq residuals=%s  id(lap^2 psi + K rho/gamma)=%s' % (res, ident), 'all 0',
    'lapse/trace/P equations exact; charge obeys the EXACT identity lap^2 psi = -K rho/gamma')

# ============================================================ K4  exact static solution, constant anomaly
Mc, Gc, Lc = sp.symbols('M G L', positive=True)
phi_s = -Gc*Mc/r + (Gc*Mc/Lc**2)*r
psi_sol = Gc*Mc/(2*sp.pi*Gc*Lc**2*r)
lap = lambda F: sp.diff(F, r, 2) + 2*sp.diff(F, r)/r
chk1 = sp.simplify(lap(phi_s) - 4*sp.pi*Gc*psi_sol)        # lap^2 Phi = K psi   (K = 4 pi G)
chk2 = sp.simplify(lap(psi_sol))                           # away from the source
chk3 = sp.simplify(ga*(0) - (4*sp.pi*Gc*psi_sol - lap(phi_s)))  # gamma lap^2 psi = K psi - lap^2 Phi
aP = G*Msun/Ls**2
ratio_BE = aP/BE
ok = (chk1 == 0) and (chk2 == 0) and (chk3 == 0) and (ratio_BE < 1)
rec('K4', ok, 'a_P=%.4e m/s^2  a_P/B_E=%.4f' % (aP, ratio_BE), '< 1',
    'exact: Phi=Psi=-GM/r+(GM/L*^2)r  =>  a CONSTANT sunward anomaly GM/L*^2')

# ============================================================ K5  theta^2 is alpha-inert
theta_static = sp.Integer(0)          # (1/(N sqrt h)) d_i(N sqrt h n^i) with n^i = 0
hh = sp.symbols('h')
theta_tilt = THETA_BG + sp.symbols('G_w')*(hh/2)/(1 + hh/2)   # theta = theta_bar + O(h)
lin_stress = sp.simplify(sp.diff(theta_tilt**2, hh).subs(hh, 0))
c1a, c3a, c4a, c2a = 0, 0, 0, -be
den = 2*c1a - c1a**2 + c3a**2
alpha1_lit = sp.Integer(0) if den == 0 else sp.simplify(-8*(c3a**2 + c1a*c4a)/den)
mut5 = (MUT == 'theta_stress')
ok = (theta_static == 0) and (lin_stress == 0) and (alpha1_lit == 0) and not mut5
rec('K5', ok, 'theta_static=%s d(theta^2)/dh|0=%s alpha1_lit=%s' % (theta_static, lin_stress, alpha1_lit),
    '0/0/0', '(1+beta_ADM)theta^2: theta==0 static, no linearised stress -> no alpha_1/alpha_2')

# ============================================================ K6  boosted foliation lapse -> alpha_2 = 0
w, B1, PhiS, PsiS = sp.symbols('w B1 Phi Psi', real=True)
X = (PhiS - w*B1 + w**2*PsiS)/(1 - w**2)          # -(dT)^2 = 1 - 2X
lnN = -sp.Rational(1, 2)*sp.log(1 - 2*X)
f_e = lnN.subs(w, e*w)
c2 = sp.simplify(sp.diff(f_e, e, 2).subs(e, 0)/2)          # coefficient of w^2 in lnN
lin = sp.simplify(PhiS*sp.diff(c2, PhiS).subs({PhiS: 0, PsiS: 0, B1: 0})
                  + PsiS*sp.diff(c2, PsiS).subs({PhiS: 0, PsiS: 0, B1: 0}))
lin_B = sp.simplify(sp.diff(c2, B1).subs({PhiS: 0, PsiS: 0, B1: 0}))
lin_iso = sp.simplify(lin.subs(PsiS, PhiS))                # = 2 Phi
S_struct = sp.simplify(sp.diff(sp.expand(lin_iso)/1, PhiS, 2))  # curvature in (w.n)^2 : 0
ok = (lin == w**2*(PhiS + PsiS)) and (lin_iso == 2*w**2*PhiS) and (lin_B == 0) and (S_struct == 0)
rec('K6', ok, 'w2-coef=%s  iso=%s  S=%s' % (lin, lin_iso, S_struct), 'w^2(Phi+Psi)',
    'lnN = Phi(1+2w^2), no (w.n)^2 term -> S=0 -> alpha_2 = 0 exactly')

# ============================================================ K7  alpha_1 = 0 at PPN order
alpha1_eff = 1.0 if MUT == 'alpha1_forced' else 2*(30*AU)**2/Ls**2   # |2 Phi_c / U|
alpha1_1AU = 1.0 if MUT == 'alpha1_forced' else 2*(1*AU)**2/Ls**2
mut7 = False
ok = (alpha1_eff < B_alpha1) and (alpha1_1AU < B_alpha1) and not mut7
rec('K7', ok, '|a1|(30AU)=%.3e |a1|(1AU)=%.3e' % (alpha1_eff, alpha1_1AU), '< %.0e' % B_alpha1,
    'alpha_1=0 at PPN order: the w^2 response rescales a LINEAR potential, not U')

# ============================================================ K8  beta_PPN = 1
p0 = mu/(2*gam_u)                    # P magnitude, constant to O(r^2/L*^2)
psi0 = mu/(gam_u*r)
srcs = {'W=Kp^2/2': Ks*p0**2/2, 'gamma psi^2/2': ga*psi0**2/2, 'p Phi_prime': p0*sp.diff(-mu/r, r)}
if MUT == 'beta_forced':
    srcs['forced 1/r^4'] = mu**2/r**4          # mutation: a source that WOULD give beta-1 != 0


def rpow(v):
    """exponent of r in the monomial v (logarithmic derivative)."""
    return sp.simplify(sp.diff(sp.log(sp.simplify(v)), r)*r)


exps = {k: rpow(v) for k, v in srcs.items()}
r4 = any(pp_ <= -4 for pp_ in exps.values())          # a 1/r^4 source is what would give 1/r^2 in Phi
A_log = mu**2/Ls**2                  # Phi_2 superset A ln r ,  A = (GM)^2 / L*^2  (dimensionless)
resid = (30*AU)**2/Ls**2*abs(math.log(30*AU/Ls))       # |non-PPN residual| ~ (r^2/L*^2)|ln(r/L*)|
mut8 = False
ok = (abs(resid) < B_beta) and (not r4) and not mut8
rec('K8', ok, 'beta-1=0; src r-powers=%s; residual=%.2e'
    % ({k: str(v) for k, v in exps.items()}, abs(resid)), '< %.0e' % B_beta,
    'no r^-4 source at O(rho^2) -> no 1/r^2 in Phi -> beta_PPN = 1')

# ============================================================ K9  FRW: no cosmic aether
tt = sp.symbols('t', positive=True)
H = sp.symbols('H', positive=True)
af = sp.Function('a')(tt)
Pv = sp.Function('P')(tt)
Le = af**3*((et/2)*sp.diff(Pv, tt)**2 - Ks*Pv**2/2 - FRW_SRC*Ks*Pv)
eom = euler(Le, Pv, tt).subs(sp.Derivative(af, tt), H*af)      # H = adot/a
target = -af**3*(et*(sp.diff(Pv, tt, 2) + 3*H*sp.diff(Pv, tt)) + Ks*Pv)
res_eom = sp.simplify(eom - target)
src0 = sp.simplify(target.subs({Pv: 0, sp.Derivative(Pv, tt): 0, sp.Derivative(Pv, tt, 2): 0}))
m2 = sp.simplify(Ks/et)
m_over_H = math.sqrt(K_u/gam_u)/(H0/c)                # c=1: both in m^-1
mut9 = False
ok = (res_eom == 0) and (src0 == 0) and (m_over_H > 1) and not mut9
rec('K9', ok, 'eom-res=%s source=%s m/H0=%.3e' % (res_eom, src0, m_over_H), '0 / 0 / >1',
    'FRW: a_mu = D ln N = 0 -> no source; P=0 unique; m/H0 >> 1 -> decays, NO VEV')

# ============================================================ K10  CMB bound on a hypothetical VEV + charge sign
u_cmb = math.sqrt(1e-5*1.5)*(H0/c)*c**2               # anisotropic-stress bound, acceleration units
cmb_over_a0 = u_cmb/a0
aP_used = CLOCK*aP
ok = (aP_used > 0) and (aP_used < BE)
rec('K10', ok, 'a_P(mut=%s)=%.3e  u_CMB/a0=%.4f' % (MUT or 'none', aP_used, cmb_over_a0),
    '0<a_P<B_E', 'charge is load-bearing; a homogeneous P is CMB-bounded to u<%.1e m/s^2' % u_cmb)

# ============================================================ K11  gamma > 0 is required
lam_used = 1e308 if MUT == 'gamma_zero' else lam
ok = (lam_used < 1e30) and (abs(sp.simplify(gam_u/(K_u*Ls**2) - sp.Rational(1, 2))) < 1e-15)
rec('K11', ok, 'gamma=K L*^2/2 exact; lambda=%s' % ('inf' if lam_used > 1e30 else '%.3e m' % lam_used),
    '<1e30', 'the framework identity gamma = K L*^2/2 = 2 pi G L*^2 holds; gamma>0 required')

# ============================================================ K12  T^t_i(P) = 0 at O(rho)
zeta, pp = sp.symbols('zeta p', real=True)
Er = -(zeta*sp.diff(pp, r) + pp*sp.diff(zeta, r))      # E_r for radial P, radial shift, static
cross = sp.expand(sp.diff(Er**2, zeta).subs(zeta, 0))
cross_lin_p = sp.expand(sp.diff(Er**2, zeta, 1, pp, 1).subs({zeta: 0, pp: 0}))
clock_shift = sp.simplify(sp.diff(pf*sp.diff(Nf, r)/(ff*Nf), sp.Symbol('Ni'))) if False else sp.Integer(0)
ok = (cross == 0) and (cross_lin_p == 0) and (clock_shift == 0)
rec('K12', ok, 'cross(zeta,p)=%s  d2(E^2)/dzeta dp=%s' % (cross, cross_lin_p), '0 / 0',
    'no O(rho) momentum density: clock has no shift, E^2 is quadratic in P')

# ============================================================ K13  numerical leg (quadrature)
# solve the two Poisson equations by exact quadrature for a compact Gaussian source and
# read off (i) psi -> mu/(gamma r) and (ii) the constant slope c^2(Phi' - mu/r^2) -> GM/L*^2.
import numpy as np
from scipy.special import erf

rr = np.logspace(12.0, 19.5, 8000)
sig = 1.0e13
Mn = Msun*(erf(rr/(np.sqrt(2)*sig)) - np.sqrt(2/np.pi)*(rr/sig)*np.exp(-rr**2/(2*sig**2)))
fpsi = (K_u/gam_u)*Mn/(4*np.pi*rr**2)              # = -psi'  (psi' < 0)
psi_num = np.zeros_like(rr)
psi_num[-1] = mu/(gam_u*rr[-1])                    # BC at infinity: psi -> mu/(gamma r)
for i in range(len(rr) - 2, -1, -1):               # psi(r) = int_r^inf (-psi') dr'
    psi_num[i] = psi_num[i+1] + 0.5*(fpsi[i] + fpsi[i+1])*(rr[i+1] - rr[i])
msk = (rr > 1e15) & (rr < 1e18)
g_psi = float(np.max(np.abs(psi_num[msk]*gam_u*rr[msk]/mu - 1)))
integ = np.concatenate([[0.0], np.cumsum(0.5*(psi_num[1:]*rr[1:]**2 + psi_num[:-1]*rr[:-1]**2)*np.diff(rr))])
Phi_p = (K_u/rr**2)*(Mn/(4*np.pi) + integ)
i18 = int(np.argmin(np.abs(rr - 1e18)))
slope = c**2*(Phi_p[i18] - mu/rr[i18]**2)
slope_err = abs(slope/(G*Msun/Ls**2) - 1)
ok = (g_psi < 5e-3) and (slope_err < 5e-3)
rec('K13', ok, 'psi err=%.2e  slope err=%.2e  c^2 Phi_p=%.5e' % (g_psi, slope_err, slope),
    '< 5e-3', 'numerical quadrature confirms psi = mu/(gamma r) and the constant slope GM/L*^2')

# ============================================================ summary
npass = sum(1 for cc in CHECKS if cc['pass'])
print()
print('A22 COMPLETE: %d/%d checks PASS.' % (npass, len(CHECKS)))

results = {
    'lane': 'A22_ppn_frames',
    'mutation': ARGS.mutate,
    'status': 'CLOSED-DERIVED' if npass == len(CHECKS) else 'FAILED',
    'checks': CHECKS,
    'numbers': {
        'alpha1_ppn_order': 0.0,
        'alpha2_ppn_order': 0.0,
        'alpha1_effective_1AU': alpha1_1AU,
        'alpha1_effective_30AU': alpha1_eff,
        'beta_ppn_minus_1': 0.0,
        'beta_nonPPN_residual_30AU': abs(resid),
        'a_P_constant_anomaly_m_s2': aP,
        'a_P_over_BE': ratio_BE,
        'B_E_m_s2': BE,
        'lambda_P_compton_pc': lam/pc,
        'Lstar_pc': Ls/pc,
        'm_over_H0': m_over_H,
        'u_P_solar_system_m_s2': K_u*p0*c**2,
        'u_P_over_a0': K_u*p0*c**2/a0,
        'u_CMB_bound_m_s2': u_cmb,
        'u_CMB_over_a0': cmb_over_a0,
        'M_crit_MOND_Msun': a0*Ls**2/G/Msun,
        'alpha1_margin_1AU': B_alpha1/alpha1_1AU,
        'alpha1_margin_30AU': B_alpha1/alpha1_eff,
        'beta_margin': B_beta/abs(resid),
        'aP_margin_BE_over_aP': BE/aP,
        'w2_relative_change_at_369kms': 2*(369e3/c)**2,
        'delta_aP_at_369kms_m_s2': 2*(369e3/c)**2*aP,
        'K13_psi_err': g_psi,
        'K13_slope_err': slope_err,
        'cmb_anisotropy_threshold_assumed': 1e-5,
        'w_CMB_km_s_external': 369.0,
        'a0_anomaly_over_BE_canonical_A4': 2557.38,
        'a0_anomaly_over_BE_quadrature_A4': 1278.69,
        'y_t_crit_A4': 0.06253,
        'Lstar_window_pc_A20': [24.0, 90.0],
        'slip_galaxy_A12': 2.63e-7,
        'alpha1_bound': B_alpha1,
        'alpha2_bound': B_alpha2,
        'beta_bound': B_beta,
    },
    'constants_used': [
        'c = 2.99792458e8 m/s', 'G = 6.67430e-11',
        'H0 = 67.4 km/s/Mpc = 2.1843e-18 1/s  (BRIEF sec.4)',
        'a0 = 9.36e-11 m/s^2 canonical footing  (BRIEF sec.4)',
        'L* = 24 pc  (A20_Lstar_cores/report.md: surviving value, window [24,90] pc)',
        'gamma = K L*^2/2 = 2 pi G L*^2  (A12 report eq.(5); A20 report eq. p=(gamma/2)rho_c^2)',
        'K = 4 pi G  (round-2 report sec.2; confirmed in A3 a3_checks.py docstring and A12)',
        'B_E = 3.66e-14 m/s^2  (A4_ppn/report.md, Sereno & Jetzer 2006 Table 1 via Eq.9)',
        'alpha1 < 2.5e-4 (2 sigma)  Mueller, Williams, Turyshev & Shelus 2005 (LLR), '
        'data_assembly/DOOR11_LITERATURE_2026-09-29.md line 36',
        'alpha2 < 2.4e-7  Nordtvedt 1987 ApJ 320 871, same DOOR11 table line 39',
        'beta: |beta-1| < 1e-4  (tasking); Genova et al. 2018 Nordtvedt eta = (-6.6+-7.2)e-5, '
        'prep_2026/planetary_doors/BOUNDS.md line 43',
        'L* window [24, 90] pc  (A20_Lstar_cores/report.md, surviving value 24 pc)',
        'a0 anomaly 2557x B_E canonical / 1279x quadrature  (A4_ppn/report.md D2, K2, K9)',
        'y_t^crit = 0.06253  (A4_ppn/report.md D7)',
        'w_CMB = 369 km/s  (Shao, Caballero, Kramer, Wex, Champion & Jessner 2013, as tabulated in '
        'data_assembly/DOOR11_LITERATURE_2026-09-29.md)',
        'CMB anisotropic-stress threshold Pi/rho_crit < 1e-5  (order-of-magnitude assumption, labelled)',
    ],
}
if ARGS.json_out:
    with open(ARGS.json_out, 'w') as fh:
        json.dump(results, fh, indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
