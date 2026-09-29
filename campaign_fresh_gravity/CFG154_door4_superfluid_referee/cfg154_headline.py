"""CFG154 headline: independent re-derivation of CFG122's G1.1a "mass spread 31.6" (door 4, superfluid dark matter).

Frozen criteria: ../CFG154_FROZEN_CRITERIA.md (sha256 printed first).  Runs, in order:
  A  symbolic (sympy): S1-S7, H1a, and the symbolic parts of R1 and R3;
  C1 Lane-Emden controls (n = 0, 1, 5 closed forms; n = 1/2 against sympy series + mpmath; solver B in its LE limit);
  C2 the target's identities;
  H1b / H1c at the headline cell (m = 1e-3 eV, alpha = 10, Lambda from the tie, branch X < 0), with P1, C3, C5a;
  R1 (numeric), R4.
MUTATE=1: alpha(M_b) = 10 (M_b/1e12 Msun)^(1/2) at the headline cell; runs A (with the MUTATE substitution), H1b/H1c,
P1 and C3; H1b must then FAIL and the script exits 1.
Usage:  python3 cfg154_headline.py          (main)
        MUTATE=1 python3 cfg154_headline.py (MUTATE)
kappa = 1/2 is FITTED.  Nothing here says the data favour either model, or that the theory is closed.
"""
import math
import os
import sys

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg154_common import (A0, GEOMS, MASSES, MPL, MSUN_EV, M_SUN, G_SI, G_NAT, ACC_SI_TO_NAT, L_EV, X_EVAL,
                           Report, SolverB, eps_of, lam_tie, le_half_edge_rk4, le_rk4, P3, phi_b_minus, r_M_nat,
                           solver_C, target, xnodes)

MUTATE = os.environ.get('MUTATE', '0') not in ('0', '', 'false', 'False')
rep = Report('cfg154_headline', mutate=MUTATE)
M_HEAD, AL_HEAD = 1e-3, 10.0
SPREAD_EXACT = math.sqrt(1000.0)
XSPREAD_EXACT = math.sqrt(901.0 / 1.01)


def gname(g):
    return 'point' if g[0] == 'point' else f'exp h={g[1]:g} r_M'


def zero(expr):
    return sp.simplify(expr) == 0


# =====================================================================================================================
rep.banner('A. SYMBOLIC (sympy, my own derivation from the Lagrangian as frozen in CFG122)')
m, Lam, al, MPl, a0, M, x, J, kap = sp.symbols('m Lambda alpha M_Pl a_0 M x J kappa', positive=True)
Ysym = sp.symbols('Y', real=True)
Rr = sp.symbols('r', positive=True)
Gs = 1 / (8 * sp.pi * MPl ** 2)
cP = 2 * Lam * (2 * m) ** sp.Rational(3, 2) / 3
three_half = sp.Rational(3, 2)

# S1: Euler-Lagrange for phi of r^2 [P(X) - alpha (Lambda/M_Pl) phi rho_b], both signs of X
phi = sp.Function('phi')(Rr)
Yf = sp.Function('Y')(Rr)
rhob = sp.Function('rho_b')(Rr)
S1 = []
for sgn in (-1, 1):
    X = Yf - sp.diff(phi, Rr) ** 2 / (2 * m)
    P = sgn * cP * (sgn * X) ** three_half
    n_expr = Lam * (2 * m) ** three_half * sp.sqrt(sgn * X)
    L = Rr ** 2 * (P - al * Lam / MPl * phi * rhob)
    EL = sp.euler_equations(L, [phi], [Rr])[0].lhs
    tgt = sp.diff(Rr ** 2 * n_expr * sp.diff(phi, Rr) / m, Rr) - al * Lam * Rr ** 2 * rhob / MPl
    q = sp.symbols('q', positive=True)
    Pq = sgn * cP * (sgn * sgn * q) ** three_half if sgn > 0 else -cP * q ** three_half   # P at X = sgn q
    nq = Lam * (2 * m) ** three_half * sp.sqrt(q)
    dPdX = sp.diff(Pq, q) * sgn                                                          # dP/dX = sgn dP/dq
    S1.append((sgn, zero(EL - tgt), zero(dPdX - nq)))
    rep.p(f'S1 X {"<" if sgn < 0 else ">"} 0: Euler-Lagrange == d/dr[r^2 n phi\'/m] - alpha Lambda r^2 rho_b/M_Pl: '
          f'{S1[-1][1]};  P\'(X) == Lambda (2m)^(3/2) sqrt|X|: {S1[-1][2]}')
# Gauss first integral: r^2 n phi'/m = alpha Lambda Q(r)/M_Pl with Q' = r^2 rho_b  -> the EL equation holds identically
Qf = sp.Function('Q')(Rr)
gauss_ok = zero((sp.diff(al * Lam * Qf / MPl, Rr) - al * Lam * Rr ** 2 * rhob / MPl).subs(sp.diff(Qf, Rr), Rr ** 2 * rhob))
rep.p(f'S1 Gauss: 4 pi r^2 n phi\'/m = alpha Lambda M_b(<r)/M_Pl solves the EL equation: {gauss_ok}')

# S2: the roots of s|Y - s| = J^2 and BK eq. 57
dp = sp.sqrt(Ysym ** 2 + 4 * J ** 2)
dm = sp.sqrt(Ysym ** 2 - 4 * J ** 2)
s_m, s_a, s_b = (Ysym + dp) / 2, (Ysym - dm) / 2, (Ysym + dm) / 2
S2 = {'B-': zero(sp.expand(s_m * (s_m - Ysym) - J ** 2)),
      'B+a': zero(sp.expand(s_a * (Ysym - s_a) - J ** 2)),
      'B+b': zero(sp.expand(s_b * (Ysym - s_b) - J ** 2)),
      'BK eq57': zero((Ysym - sp.sqrt(Ysym ** 2 + (2 * m * J) ** 2 / m ** 2)) / 2 - (Ysym - s_m))}
qq, ss = sp.symbols('q s', positive=True)
S2['flux: n phi\' = 4 m^2 Lambda sqrt(s|Y-s|)'] = zero(Lam * (2 * m) ** three_half * sp.sqrt(qq) * sp.sqrt(2 * m * ss)
                                                      - 4 * m ** 2 * Lam * sp.sqrt(qq * ss))
J_def = al * M / (16 * sp.pi * m * Rr ** 2 * MPl)
S2['flux: 4 m^2 Lambda J = m alpha Lambda M/(4 pi r^2 M_Pl)'] = zero(4 * m ** 2 * Lam * J_def
                                                                     - m * al * Lam * M / (4 * sp.pi * Rr ** 2 * MPl))
for k, v in S2.items():
    rep.p(f'S2 {k}: {v}')

# S3: the gradient limit, the force and N_a
absX_grad = sp.limit(s_m - Ysym, Ysym, 0)
kap_def = al * M / (8 * sp.pi * MPl * Rr ** 2)
rho_grad = m * Lam * (2 * m) ** three_half * sp.sqrt(absX_grad)
S3a = zero(absX_grad - J)
S3b = zero(rho_grad.subs(J, kap / (2 * m)) - 2 * m ** 2 * Lam * sp.sqrt(kap))
S3c = zero(kap_def - 2 * m * J_def)
a_phi = al * Lam / MPl * sp.sqrt(2 * m * J_def)          # s = J in the gradient limit, phi' = sqrt(2 m s)
N_a = sp.simplify(a_phi ** 2 / (Gs * M / Rr ** 2 * al ** 3 * Lam ** 2 / MPl))
rep.p(f'S3 |X| -> J as Y -> 0: {S3a}; rho_DM = 2 m^2 Lambda sqrt(kappa): {S3b}; kappa = 2 m J: {S3c}; '
      f'a_phi^2/(g_N alpha^3 Lambda^2/M_Pl) = N_a = {N_a}')
N_A = float(N_a)

# S4: the ratio, exponent, spreads (H1a)
rM = sp.sqrt(Gs * M / a0)
r_x = x * rM
kap_x = kap_def.subs(Rr, r_x)
rho_DM_x = 2 * m ** 2 * Lam * sp.sqrt(kap_x)
rho_c_x = a0 / (4 * sp.pi * Gs * r_x * sp.sqrt(1 + x ** 2))
R_free = sp.simplify(rho_DM_x / rho_c_x)
Lam_tie = sp.sqrt(a0 * MPl / (N_a * al ** 3))
R_tie = sp.simplify(R_free.subs(Lam, Lam_tie))
eps_def = m ** 2 * rM / (al * MPl)
S4 = {}
S4['R = eps sqrt(1+x^2) (tie)'] = sp.simplify(R_tie / (eps_def * sp.sqrt(1 + x ** 2))) == 1
S4['kappa at fixed x = alpha a0 M_Pl/x^2'] = zero(kap_x - al * a0 * MPl / x ** 2)
exp_rhoDM = sp.simplify(M * sp.diff(sp.log(rho_DM_x), M))
exp_rhoc = sp.simplify(M * sp.diff(sp.log(rho_c_x), M))
exp_free = sp.simplify(M * sp.diff(sp.log(R_free), M))
exp_tie = sp.simplify(M * sp.diff(sp.log(R_tie), M))
spread = sp.simplify(R_tie.subs(M, 10 ** 12) / R_tie.subs(M, 10 ** 9))
xspread = sp.sqrt(1 + 30 ** 2) / sp.sqrt(1 + sp.Rational(1, 10) ** 2)
a_mm, b_mm = sp.sqrt(sp.Rational(101, 100)), sp.sqrt(901)
estar = (b_mm - a_mm) / (b_mm + a_mm)
rep.p(f'S4 R (no tie) = {R_free}')
rep.p(f'S4 R (tie)    = {R_tie}')
for k, v in S4.items():
    rep.p(f'S4 {k}: {v}')
rep.p(f'S4 d ln rho_DM/d ln M at fixed x = {exp_rhoDM};  d ln rho_target/d ln M = {exp_rhoc}')
rep.p(f'S4 d ln R/d ln M at fixed x: no tie {exp_free}, tie {exp_tie};  spread R(1e12)/R(1e9) = {spread} = {float(spread):.6f}')
rep.p(f'S4 x-spread sqrt(1+30^2)/sqrt(1+0.1^2) = {sp.nsimplify(xspread)} = {float(xspread):.6f};  '
      f'single-mass minimax error (b-a)/(b+a) = {float(estar):.6f}')
rep.num('N_a', N_A)
rep.num('S4_exponent_tie', str(exp_tie))
rep.num('S4_exponent_free', str(exp_free))
rep.num('S4_spread_exact', float(spread))
rep.num('S4_xspread_exact', float(xspread))
rep.num('single_mass_minimax_pure_gradient', float(estar))
H1a_ok = (exp_tie == sp.Rational(1, 2) and exp_free == sp.Rational(1, 2) and zero(spread - sp.sqrt(1000))
          and zero(xspread - sp.sqrt(sp.Rational(901) / sp.Rational(101, 100))) and all(S4.values())
          and exp_rhoDM == 0 and exp_rhoc == -sp.Rational(1, 2))
if MUTATE:
    al0, M12 = sp.symbols('alpha_0 M_12', positive=True)
    R_mut = R_tie.subs(al, al0 * sp.sqrt(M / M12))
    exp_mut = sp.simplify(M * sp.diff(sp.log(R_mut), M))
    rep.p(f'S4 MUTATE alpha -> alpha_0 (M/M_12)^(1/2): d ln R/d ln M = {exp_mut}')
    rep.num('S4_exponent_MUTATE', str(exp_mut))
    rep.check('MUTATE symbolic: the exponent becomes 0', exp_mut == 0, f'exponent {exp_mut}', kind='mutate')

# S5: self-similar extended profile
f_, ut = sp.symbols('f u_t', positive=True)
kap_f = al * M * f_ / (8 * sp.pi * MPl * r_x ** 2)
rho_c_f = a0 * f_ / (4 * sp.pi * Gs * r_x * ut)
R_f = sp.simplify((2 * m ** 2 * Lam * sp.sqrt(kap_f) / rho_c_f).subs(Lam, Lam_tie))
S5a = sp.simplify(R_f / (eps_def * ut / sp.sqrt(f_))) == 1
exp_f = sp.simplify(M * sp.diff(sp.log(R_f), M))
rep.p(f'S5 extended self-similar profile: R = eps u_t/sqrt(f): {S5a}; d ln R/d ln M at fixed x = {exp_f}')

# S6: the reduction
J_M = al * M / (16 * sp.pi * m * rM ** 2 * MPl)
C_y = m * Gs * M / (J_M * rM)
C_mu = 4 * sp.pi * rM ** 3 * m * Lam * (2 * m) ** three_half * sp.sqrt(J_M) / M
xh = sp.symbols('xhat_abs', positive=True)
den_target = sp.simplify(4 * sp.pi * x ** 2 * rM ** 3 * rho_c_x / M)
S6 = {'dyhat/dx coefficient = 2 eps': sp.simplify(C_y / (2 * eps_def)) == 1,
      'dmu/dx coefficient = eps (tie)': sp.simplify((C_mu / eps_def).subs(Lam, Lam_tie)) == 1,
      '4 pi x^2 r_M^3 rho_target/M = x/sqrt(1+x^2)': zero(den_target - x / sp.sqrt(1 + x ** 2)),
      'R = eps x sqrt(1+x^2) sqrt|xhat|': sp.simplify((C_mu * x ** 2 * sp.sqrt(xh) / den_target).subs(Lam, Lam_tie)
                                                     / (eps_def * x * sp.sqrt(1 + x ** 2) * sp.sqrt(xh))) == 1}
for k, v in S6.items():
    rep.p(f'S6 {k}: {v}')

# S7: K and the Lane-Emden scale of the X > 0, gradient-free branch
Xp, rho_s, Yc = sp.symbols('X_p rho Y_c', positive=True)
P_pos = cP * Xp ** three_half
rho_pos = m * Lam * (2 * m) ** three_half * sp.sqrt(Xp)
X_of_rho = sp.solve(sp.Eq(rho_pos, rho_s), Xp)[0]
K = sp.simplify(P_pos.subs(Xp, X_of_rho) / rho_s ** 3)
S7a = zero(K - 1 / (12 * Lam ** 2 * m ** 6))
S7b = zero(m * sp.diff(P_pos, Xp) - rho_pos)
a2_expr = sp.sqrt(Yc) / (4 * sp.pi * Gs * m ** 2 * Lam * (2 * m) ** three_half)
S7c = zero(Yc / a2_expr - 4 * sp.pi * Gs * m ** 2 * Lam * (2 * m) ** three_half * sp.sqrt(Yc))
rep.p(f'S7 K = P/rho^3 = {K}  (== 1/(12 Lambda^2 m^6): {S7a});  rho = m P\'(X): {S7b};  '
      f'LE scale a^2 = sqrt(Y_c)/(4 pi G m^2 Lambda (2m)^(3/2)) consistent: {S7c}')

sym_ok = (all(a and b for _, a, b in S1) and gauss_ok and all(S2.values()) and S3a and S3b and S3c and N_A == 1.0
          and S5a and exp_f == sp.Rational(1, 2) and all(S6.values()) and S7a and S7b and S7c)
rep.check('S1-S7 symbolic steps', sym_ok, f'N_a = {N_a}; all identities hold = {sym_ok}', kind='control')
rep.check('H1a symbolic headline', H1a_ok,
          f'd ln R/d ln M_b at fixed x = {exp_tie} (tie), {exp_free} (no tie); spread = sqrt(1000) = {float(spread):.4f}; '
          f'x-spread = {float(xspread):.4f}', kind='headline')

if not MUTATE:
    # R1 symbolic: the P ~ rho^3 branch (X = Y, gradient dropped), mu = 0 or an edge at fixed x_e
    rho_poly = m * Lam * (2 * m) ** three_half * sp.sqrt(m * Gs * M / r_x)
    R_poly = sp.simplify((rho_poly / rho_c_x).subs(Lam, Lam_tie))
    exp_poly = sp.simplify(M * sp.diff(sp.log(R_poly), M))
    xe = sp.symbols('x_e', positive=True)
    rho_edge = m * Lam * (2 * m) ** three_half * sp.sqrt(m * Gs * M * (1 / r_x - 1 / (xe * rM)))
    exp_edge = sp.simplify(M * sp.diff(sp.log((rho_edge / rho_c_x).subs(Lam, Lam_tie)), M))
    rep.p(f'R1 symbolic (P ~ rho^3 branch, mu = 0): d ln R/d ln M = {exp_poly}; with an edge at fixed x_e: {exp_edge}; '
          f'spread 1000^(3/4) = {1000 ** 0.75:.3f}')
    rep.num('R1_exponent_symbolic', str(exp_poly))
    rep.num('R1_exponent_edge_symbolic', str(exp_edge))

    # R3 symbolic: BK's finite-temperature Lagrangian (BFK 2018 eq. 13 as read), static Y = mu - m Phi, beta > 1
    beta, muh, s3, phip_s = sp.symbols('beta mu_hat s phi_p', positive=True)
    P_T = cP * (muh - s3) * sp.sqrt((beta - 1) * muh + s3)
    rho_T = m * sp.diff(P_T, muh)
    rho_33 = 2 * sp.sqrt(2) * m ** sp.Rational(5, 2) * Lam * (3 * (beta - 1) * muh + (3 - beta) * s3) / (
        3 * sp.sqrt((beta - 1) * muh + s3))
    R3a = zero(rho_T - rho_33)
    Xs_, Ys_ = sp.symbols('X Y_s', real=True)
    P_XY = cP * Xs_ * sp.sqrt(beta * Ys_ - Xs_)
    cur = (sp.diff(P_XY, Xs_) * phip_s / m).subs({Xs_: muh - phip_s ** 2 / (2 * m), Ys_: muh})
    bfk35 = 2 * Lam * (phip_s ** 2 + 2 * m * (2 * beta / 3 - 1) * muh) / sp.sqrt(
        phip_s ** 2 + 2 * m * (beta - 1) * muh) * phip_s
    R3b = zero(cur - bfk35)
    grad_phip = sp.solve(sp.Eq((bfk35 / (2 * Lam)).subs(muh, 0), kap), phip_s)
    factor = sp.simplify(rho_T.subs(muh, 0).subs(s3, kap / (2 * m)) / (2 * m ** 2 * Lam * sp.sqrt(kap)))
    rep.p(f'R3 m dP/dmu reproduces BFK eq. 33 (as read): {R3a}; the phonon current reproduces BFK eq. 35 (as read): {R3b}')
    rep.p(f'R3 gradient limit: phi\' = {grad_phip} (phi\'^2 = kappa); density factor vs zero temperature = {factor}; '
          f'at beta = 2: {factor.subs(beta, 2)}; the M_b exponent is unchanged (rho ~ sqrt(kappa))')
    rep.num('R3_eq33_reproduced', R3a)
    rep.num('R3_eq35_reproduced', R3b)
    rep.num('R3_factor', str(factor))

# =====================================================================================================================
if not MUTATE:
    rep.banner('C1. LANE-EMDEN CONTROLS (n = 1/2 has no elementary closed form)')
    c1 = []
    for n, xmax, fcl in [(0, math.sqrt(6.0), lambda z: 1 - z ** 2 / 6), (1, math.pi, lambda z: np.sin(z) / z),
                         (5, 10.0, lambda z: (1 + z ** 2 / 3) ** -0.5)]:
        xis, TH, _ = le_rk4(n, xmax, hstep=1e-3)
        err = float(np.max(np.abs(TH - fcl(xis))))
        c1.append(rep.check(f'C1a LE n = {n} against its closed form', err <= 1e-8, f'max |theta - closed| = {err:.2e} '
                            f'on [0, {xis[-1]:.4f}] (line 1e-8)'))
        rep.num(f'C1a_err_n{n}', err)
    # (b) n = 1/2 reference: exact series (sympy) to xi^16, then mpmath's Taylor integrator (30 digits)
    xi_s = sp.symbols('xi', positive=True)
    coef = [sp.Integer(1)]
    for k in range(1, 9):
        th_k = sum(coef[j] * xi_s ** (2 * j) for j in range(k))
        sq = sp.series(sp.sqrt(th_k), xi_s, 0, 2 * k).removeO()
        ck = -sp.Poly(sq, xi_s).coeff_monomial(xi_s ** (2 * k - 2)) / (2 * k * (2 * k + 1))
        coef.append(sp.nsimplify(ck))
    rep.p('C1b n = 1/2 central series coefficients (xi^0..xi^16): ' + ', '.join(str(c) for c in coef))
    mp.mp.dps = 30
    ser = lambda z: sum(mp.mpf(sp.Rational(c).p) / mp.mpf(sp.Rational(c).q) * z ** (2 * j) for j, c in enumerate(coef))
    dser = lambda z: sum(mp.mpf(sp.Rational(c).p) / mp.mpf(sp.Rational(c).q) * 2 * j * z ** (2 * j - 1)
                         for j, c in enumerate(coef) if j > 0)
    z05 = mp.mpf('0.5')
    ode = mp.odefun(lambda z, y: [y[1], -mp.sqrt(y[0]) - 2 * y[1] / z], z05, [ser(z05), dser(z05)])
    th27, p27 = ode(mp.mpf('2.7'))
    us = mp.sqrt(th27)
    ode2 = mp.odefun(lambda v, y: [-2 * (us - v) / y[1], ((us - v) + 2 * y[1] / y[0]) * (2 * (us - v) / y[1])],
                     mp.mpf(0), [mp.mpf('2.7'), p27])
    xi1_ref, p1_ref = ode2(us)
    xi1_ref, p1_ref = float(xi1_ref), float(p1_ref)
    omega_ref = -xi1_ref ** 2 * p1_ref

    def theta_ref(z):
        z = float(z)
        return float(ser(mp.mpf(z))) if z <= 0.5 else float(ode(mp.mpf(z))[0])

    xis, TH, DTH = le_rk4(0.5, 2.7, hstep=1e-3)
    sel = np.where(xis >= 0.5 - 1e-12)[0][::50]
    errb = max(abs(TH[i] - theta_ref(xis[i])) for i in sel)
    xi1_rk, p1_rk = le_half_edge_rk4(xis[-1], TH[-1], DTH[-1])
    c1.append(rep.check('C1b LE n = 1/2: my RK4 against series + mpmath (theta on [0.5, 2.7])', errb <= 1e-8,
                        f'max |theta_RK4 - theta_ref| = {errb:.2e} at {len(sel)} points (line 1e-8)'))
    c1.append(rep.check('C1b LE n = 1/2: xi_1', abs(xi1_rk - xi1_ref) <= 1e-6,
                        f'xi_1 RK4 {xi1_rk:.10f} vs reference {xi1_ref:.10f} (|d| = {abs(xi1_rk - xi1_ref):.1e}, line 1e-6)'))
    rep.p(f'C1 reported: n = 1/2  xi_1 = {xi1_ref:.8f}, -xi_1^2 theta\'(xi_1) = {omega_ref:.8f}  '
          f'(recalled table values about 2.7527 and 3.787; from memory, unverified; no pass line)')
    rep.num('LE_half_xi1_ref', xi1_ref)
    rep.num('LE_half_omega_ref', omega_ref)
    rep.num('LE_half_xi1_rk4', xi1_rk)
    # (c) solver B in its X > 0 branch, flux off, no baryons: must reproduce theta(r/a) and the homology slope 1/5
    m_c, lam_c = 1.0, 1e-3
    edges = []
    errc_all = 0.0
    for Yc_v in (1e-7, 1.6e-6):
        a_le = math.sqrt(math.sqrt(Yc_v) / (4 * math.pi * G_NAT * m_c ** 2 * lam_c * (2 * m_c) ** 1.5))
        rho_c0 = m_c * lam_c * (2 * m_c) ** 1.5 * math.sqrt(Yc_v)
        Bl = SolverB(m_c, 0.0, lam_c, 0, ('none', None), None, 'B+a', flux=False, selfgrav=True)
        xi_ev = np.concatenate([[1e-4], np.linspace(0.01, 0.99 * xi1_ref, 100)])
        o = Bl.solve(1e-4 * a_le, Yc_v, 0.0, xi_ev * a_le, 3.0 * a_le, rtol=1e-12, Ys=Yc_v,
                     Ms=4 * math.pi * a_le ** 3 * rho_c0)
        th_B = o['Y'] / Yc_v
        errc = max(abs(th_B[i] - theta_ref(xi_ev[i])) for i in range(len(xi_ev)))
        errc_all = max(errc_all, errc)
        edges.append((o['r_edge'], o['Mdm_edge'], a_le))
        rep.p(f'C1c Y_c = {Yc_v:g} eV: a = {a_le * L_EV / 3.0856775814913673e19:.4f} kpc; max |Y/Y_c - theta_ref| = '
              f'{errc:.2e}; edge at xi = {o["r_edge"] / a_le:.8f}; M_edge = {o["Mdm_edge"] / MSUN_EV:.6e} Msun')
    slope = math.log(edges[1][0] / edges[0][0]) / math.log(edges[1][1] / edges[0][1])
    c1.append(rep.check('C1c solver B (X > 0, flux off, no baryons) reproduces Lane-Emden n = 1/2', errc_all <= 1e-6,
                        f'max |Y/Y_c - theta(r/a)| = {errc_all:.2e} on [0, 0.99 xi_1] (line 1e-6)'))
    c1.append(rep.check('C1c homology slope d ln R/d ln M = 1/5', abs(slope - 0.2) <= 1e-4,
                        f'slope {slope:.8f} (line |slope - 0.2| <= 1e-4)'))
    c1.append(rep.check('C1d K = 1/(12 Lambda^2 m^6) (BK eq. 30 as read)', S7a, f'K = {K}'))
    rep.num('C1c_err', errc_all)
    rep.num('C1c_slope', slope)

    # =================================================================================================================
    rep.banner('C2. THE TARGET REPRODUCES ITS OWN IDENTITIES (CFG44 closure, integrated in SI)')
    x_dense = np.logspace(math.log10(0.05), math.log10(40.0), 4001)
    worst = {'pm_Mc': 0.0, 'pm_rho': 0.0, 'pm_g': 0.0, 'C': 0.0, 'Mb_sph': 0.0}
    TGT = {}
    for foot, a0v in A0.items():
        for Mv in MASSES:
            for g in GEOMS:
                T = target(Mv, g, a0v, X_EVAL, x_dense=x_dense)
                TGT[(foot, Mv, g)] = T
                d = T['dense']
                cs = CubicSpline(np.log(d['r']), np.log(d['Mc']))
                rho_sp = T['Mc'] / T['r'] * cs(np.log(T['r']), 1) / (4 * math.pi * T['r'] ** 2)
                C = rho_sp * T['r'] ** 3 * T['g_tot']
                worst['C'] = max(worst['C'], float(np.max(np.abs(C / (a0v / (4 * math.pi) * T['Mb']) - 1))))
                Mkg = Mv * M_SUN
                if g[0] == 'point':
                    xx = X_EVAL
                    worst['pm_Mc'] = max(worst['pm_Mc'], float(np.max(np.abs(T['Mc'] / (Mkg * (np.sqrt(1 + xx ** 2) - 1)) - 1))))
                    rho_cl = a0v / (4 * math.pi * G_SI * T['r'] * np.sqrt(1 + xx ** 2))
                    worst['pm_rho'] = max(worst['pm_rho'], float(np.max(np.abs(T['rho_c'] / rho_cl - 1))))
                    g_cl = np.sqrt(T['g_N'] ** 2 + a0v * T['g_N'])
                    worst['pm_g'] = max(worst['pm_g'], float(np.max(np.abs(T['g_tot'] / g_cl - 1))))
                else:
                    Mb_cl = Mkg * np.array([P3(rr / (g[1] * T['rM'])) for rr in T['r']])
                    worst['Mb_sph'] = max(worst['Mb_sph'], float(np.max(np.abs(T['Mb'] / Mb_cl - 1))))
    c2 = [rep.check('C2 point mass: M_c = M_b(sqrt(1+x^2) - 1)', worst['pm_Mc'] <= 1e-8, f'max rel err {worst["pm_Mc"]:.2e} (line 1e-8)'),
          rep.check('C2 point mass: rho_c = a0/(4 pi G r sqrt(1+x^2))', worst['pm_rho'] <= 1e-8, f'max rel err {worst["pm_rho"]:.2e} (line 1e-8)'),
          rep.check('C2 point mass: g_tot = sqrt(g_N^2 + a0 g_N)', worst['pm_g'] <= 1e-8, f'max rel err {worst["pm_g"]:.2e} (line 1e-8)'),
          rep.check('C2 all geometries: C(r) = rho_c r^3 g_tot = (a0/4pi) M_b(<r), rho_c from a spline derivative',
                    worst['C'] <= 1e-5, f'max rel err {worst["C"]:.2e} (line 1e-5)'),
          rep.check('C2 spheres: integrated M_b(<r) = M_b[1 - (1 + s + s^2/2)e^-s] for x >= 0.1', worst['Mb_sph'] <= 1e-9,
                    f'max rel err {worst["Mb_sph"]:.2e} (line 1e-9)')]
    rep.num('C2_worst', worst)
else:
    c1, c2 = [], []
    TGT = {}
    for foot, a0v in A0.items():
        for Mv in MASSES:
            for g in GEOMS:
                TGT[(foot, Mv, g)] = target(Mv, g, a0v, X_EVAL)

# =====================================================================================================================
rep.banner('H1b / H1c. MY RADIAL SOLVER (solver B) AT THE HEADLINE CELL'
           + ('  --  MUTATE: alpha(M_b) = 10 (M_b/1e12 Msun)^(1/2)' if MUTATE else ''))


def alpha_at(Mv):
    return 10.0 * math.sqrt(Mv / 1e12) if MUTATE else AL_HEAD


def run_head(rtol):
    res = {}
    for foot, a0v in A0.items():
        for g in GEOMS:
            Rm, P1m, C3m, Mbm = [], 0.0, 0.0, 0.0
            for Mv in MASSES:
                alv = alpha_at(Mv)
                lam = lam_tie(alv, a0v, N_A)
                B = SolverB(M_HEAD, alv, lam, Mv, g, a0v, 'B-')
                rM_n = r_M_nat(Mv, a0v)
                r_in = 1e-3 * rM_n
                Y_in = M_HEAD * phi_b_minus(Mv * MSUN_EV, g, r_in, rM_n)
                o = B.solve(r_in, Y_in, 0.0, X_EVAL * rM_n, 40.0 * rM_n, rtol=rtol)
                T = TGT[(foot, Mv, g)]
                R = o['rho_SI'] / T['rho_c']
                Rm.append(R)
                P1m = max(P1m, float(np.max(np.abs(o['Y']) / o['J'])))
                if g[1] is not None:
                    Mb_cl = np.array([P3(xx / g[1]) for xx in X_EVAL]) * Mv * MSUN_EV
                    Mbm = max(Mbm, float(np.max(np.abs(o['Mb'] / Mb_cl - 1))))
                if g[0] == 'point':
                    phip = np.sqrt(2 * M_HEAD * o['s'])
                    a_phi_SI = alv * lam / MPL * phip / ACC_SI_TO_NAT
                    gN = G_SI * Mv * M_SUN / (X_EVAL * math.sqrt(G_SI * Mv * M_SUN / a0v)) ** 2
                    C3m = max(C3m, float(np.max(np.abs(a_phi_SI / np.sqrt(a0v * gN) - 1))))
            Rm = np.array(Rm)
            res[(foot, g)] = {'R': Rm, 'P1': P1m, 'C3': C3m, 'Mb_err': Mbm}
    return res


HEAD = run_head(1e-10)
lnM = np.log(np.array(MASSES))
h1b, h1c, p1ok, c3ok = True, True, True, True
worstS, worstp, worstC3, worstP1 = 0.0, 0.0, 0.0, 0.0
collapse = 0.0
pmax = 0.0
Mb_solverB = 0.0
for (foot, g), d in HEAD.items():
    R = d['R']
    S = R.max(axis=0) / R.min(axis=0)
    p = np.polyfit(lnM, np.log(R), 1)[0]
    devS = float(np.max(np.abs(S / SPREAD_EXACT - 1)))
    devp = float(np.max(np.abs(p - 0.5)))
    worstS, worstp = max(worstS, devS), max(worstp, devp)
    collapse = max(collapse, float(np.max(np.abs(S - 1))))
    pmax = max(pmax, float(np.max(np.abs(p))))
    worstP1 = max(worstP1, d['P1'])
    Mb_solverB = max(Mb_solverB, d['Mb_err'])
    h1b &= (devS <= 0.02) and (devp <= 0.01)
    eps_row = [eps_of(M_HEAD, alpha_at(Mv), Mv, A0[foot]) for Mv in MASSES]
    R0 = R[:, 0] / math.sqrt(1 + X_EVAL[0] ** 2) if g[0] == 'point' else R[:, 0]
    rep.p(f'{foot:9s} {gname(g):16s} eps = ' + ', '.join(f'{e:.4e}' for e in eps_row)
          + f' | S(x): min {S.min():.6f} max {S.max():.6f} | p(x): min {p.min():.6f} max {p.max():.6f} | '
          f'max|Y|/J = {d["P1"]:.2e}' + (f' | R(x=0.1)/sqrt(1.01) = ' + ', '.join(f'{v:.4e}' for v in R0)
                                         if g[0] == 'point' else ''))
    rep.num(f'H1b_{foot}_{gname(g)}', {'S_min': S.min(), 'S_max': S.max(), 'p_min': p.min(), 'p_max': p.max(),
                                       'P1': d['P1'], 'eps': eps_row, 'R_at_x0.1': R[:, 0], 'R_at_x30': R[:, -1]})
    if g[0] == 'point':
        worstC3 = max(worstC3, d['C3'])
        for iM, Mv in enumerate(MASSES):
            xs_ = R[iM].max() / R[iM].min()
            ok = abs(xs_ / XSPREAD_EXACT - 1) <= 0.02
            h1c &= ok
            rep.p(f'    H1c {foot} M_b = {Mv:.0e}: max/min of R over x = {xs_:.6f} (exact {XSPREAD_EXACT:.6f})')
            rep.num(f'H1c_{foot}_{Mv:.0e}', xs_)
p1ok = worstP1 <= 1e-2
rep.check('P1 precondition: max |Y|/J <= 1e-2 over the range (every mass, geometry, footing)', p1ok,
          f'max |Y|/J = {worstP1:.2e}', kind='precondition')
rep.check('C3 the tie: a_phi = alpha (Lambda/M_Pl) phi\' equals sqrt(a0 g_N) (point mass)', worstC3 <= 1e-4,
          f'max |a_phi/sqrt(a0 g_N) - 1| = {worstC3:.2e} (line 1e-4)')
if not MUTATE:
    rep.check('C2 (solver B) spheres: integrated M_b(<r) matches the closed form for x >= 0.1', Mb_solverB <= 1e-9,
              f'max rel err {Mb_solverB:.2e} (line 1e-9)')
h1b = h1b and p1ok
rep.check('H1b numeric: |S(x)/31.623 - 1| <= 0.02 and |p(x) - 1/2| <= 0.01 at all 200 x (3 geometries x 2 footings)', h1b,
          f'max |S/sqrt(1000) - 1| = {worstS:.3e}; max |p - 1/2| = {worstp:.3e}', kind='headline')
rep.check('H1c numeric: point-mass x-spread within 2% of 29.868 at each mass (both footings)', h1c,
          f'exact sqrt(901/1.01) = {XSPREAD_EXACT:.6f}', kind='headline')
S_all_max = max(float((d['R'].max(axis=0) / d['R'].min(axis=0)).max()) for d in HEAD.values())
door = 'PASS' if S_all_max <= 1.10 else 'FAIL'
rep.p(f'The door\'s own line (CFG122 G1.1a: spread <= 1.10): {door} (largest numeric spread {S_all_max:.6f})')
rep.num('door_G1_1a', door)
rep.num('H1b_worst_dev_S', worstS)
rep.num('H1b_worst_dev_p', worstp)
rep.num('P1_max', worstP1)
rep.num('C3_max', worstC3)
if MUTATE:
    rep.check('MUTATE: the spread collapses to 1 (to 1e-6)', collapse <= 1e-6, f'max |S - 1| = {collapse:.2e}', kind='mutate')
    rep.check('MUTATE: the exponent p collapses to 0 (to 1e-6)', pmax <= 1e-6, f'max |p| = {pmax:.2e}', kind='mutate')
    rep.check('MUTATE: H1c (the x-shape) does not move', h1c, 'see the H1c lines above', kind='mutate')
    rep.num('MUTATE_collapse_maxdev', collapse)
    rep.num('MUTATE_pmax', pmax)

c5 = []
if not MUTATE:
    HEAD8 = run_head(1e-8)
    dR = max(float(np.max(np.abs(HEAD8[k]['R'] / HEAD[k]['R'] - 1))) for k in HEAD)
    c5.append(rep.check('C5a resolution: rtol 1e-8 instead of 1e-10 changes R by <= 1e-6', dR <= 1e-6,
                        f'max |dR/R| = {dR:.2e}'))
    rep.num('C5a_dR', dR)

# =====================================================================================================================
if not MUTATE:
    rep.banner('R1 (reported). THE P ~ rho^3 BRANCH: X = Y (gradient dropped), baryonic point-mass potential, mu = 0, '
               'self-gravity off')
    for foot, a0v in A0.items():
        Rm = []
        for Mv in MASSES:
            lam = lam_tie(AL_HEAD, a0v, N_A)
            B = SolverB(M_HEAD, AL_HEAD, lam, Mv, ('point', None), a0v, 'B+a', flux=False, selfgrav=False)
            rM_n = r_M_nat(Mv, a0v)
            r_in = 1e-3 * rM_n
            o = B.solve(r_in, M_HEAD * G_NAT * Mv * MSUN_EV / r_in, 0.0, X_EVAL * rM_n, 40.0 * rM_n, rtol=1e-10)
            Rm.append(o['rho_SI'] / TGT[(foot, Mv, ('point', None))]['rho_c'])
        Rm = np.array(Rm)
        S = Rm.max(axis=0) / Rm.min(axis=0)
        p = np.polyfit(lnM, np.log(Rm), 1)[0]
        rep.p(f'R1 {foot}: spread S(x) {S.min():.4f} .. {S.max():.4f} (1000^(3/4) = {1000 ** 0.75:.4f}); '
              f'exponent p(x) {p.min():.6f} .. {p.max():.6f}; R at x = 1 per mass: '
              + ', '.join(f'{np.interp(0.0, np.log(X_EVAL), np.log(r_)):.3f}' for r_ in Rm) + ' (ln R)')
        rep.num(f'R1_{foot}', {'S_min': S.min(), 'S_max': S.max(), 'p_min': p.min(), 'p_max': p.max()})

    rep.banner('R4 (reported). HOW FAR 31.6 HOLDS: B-, point mass, mu = 0 (yhat(0.1) = 20 eps), self-gravity on (solver C)')
    xs = xnodes()
    rep.p('eps0        S(x=0.1)     S(x=1)       S(x=10)      S(x=30)      [p(x=0.1), p(x=30)]')
    R4 = {}
    for e0 in (1e-8, 1e-6, 1e-4, 1e-2, 1.0, 1e2):
        ee = e0 * np.sqrt(np.array(MASSES) / 1e9)
        c = solver_C(ee, 20.0 * ee, 'B-', keep_full=True)
        Rf = c['Rfull']
        vals = []
        for xq in (0.1, 1.0, 10.0, 30.0):
            Rq = np.array([math.exp(CubicSpline(np.log(xs), np.log(Rf[i]))(math.log(xq))) for i in range(4)])
            vals.append(Rq)
        S_q = [v.max() / v.min() for v in vals]
        p_q = [np.polyfit(lnM, np.log(v), 1)[0] for v in (vals[0], vals[-1])]
        rep.p(f'{e0:<10.0e}  ' + '  '.join(f'{s:11.4f}' for s in S_q) + f'   [{p_q[0]:.4f}, {p_q[1]:.4f}]')
        R4[f'{e0:.0e}'] = {'S': S_q, 'p_x0.1': p_q[0], 'p_x30': p_q[1]}
    rep.num('R4', R4)
    rep.p('R4 depends on solver C, whose reduction is tested by C4 in cfg154_plane.py.')

# =====================================================================================================================
rep.banner('SUMMARY')
must = [c for c in rep.checks if c['kind'] in ('headline', 'control', 'precondition')]
exit_code = 0 if all(c['pass'] for c in must) else 1
for c in rep.checks:
    rep.p(f'  {"PASS" if c["pass"] else "FAIL"}  [{c["kind"]}] {c["name"]}')
if MUTATE:
    rep.p('MUTATE mode: H1b is expected to FAIL (exit 1); an exit 0 would mean the MUTATE did not change the headline.')
rep.p('kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.')
rep.write(exit_code)
sys.exit(exit_code)
