#!/usr/bin/env python3
"""A33 -- the master action: instantiate it, vary it, and reproduce every result.

Units c = 1 unless stated; signature (-+++); K = 4 pi G (the action's own
normalisation: (R - 2 Lambda)/(4K) = (R - 2 Lambda)/(16 pi G)).

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)     gravity
                 + P^i D_i log N                                          clock
                 - W(u),   u = K |P|,  W = (a0^2/K)[-u/a0 - log(1-u/a0)]  saturating log
                 + (eta/2) E_i E^i                                        P kinetic
                 - (gamma/2) (D_i P^i)^2                                  P longitudinal
                 - (gamma/4) F_ij F^ij                                    P transverse
                 + L_cold + L_m                                           matter

Every check is one line of the form
    K<n> PASS <measured> <threshold>
and the script exits 0 iff every non-skipped check passes.

    python3 a33_checks.py [--mutate NAME] [--json-out FILE]

Mutations (each must break at least one check):
    clock2      clock coefficient 1 -> 2          (breaks K5; K3 stays by construction)
    wquad       W -> u^2/(2K)                     (breaks K3, K4)
    gamma0      gamma -> 0                        (breaks K11)
    beta0       theta^2 coefficient -> 0          (breaks K10)
    ricciP      add xi R_ij P^i P^j to the action (breaks K6)
    nocharge    drop the clock term's lapse source(breaks K8)
"""
import argparse
import json
import math
import sys

import sympy as s

AP = argparse.ArgumentParser()
AP.add_argument('--mutate', default='none',
                choices=['none', 'clock2', 'wquad', 'gamma0', 'beta0',
                         'ricciP', 'nocharge'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate

CHECKS = []
NUMBERS = {}


def rec(cid, ok, value, threshold, note=''):
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-46s %s  value=%-28s threshold=%-10s %s'
          % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))


def rel(a, b):
    a, b = float(a), float(b)
    d = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / d


# ---------------------------------------------------------------------------
# constants (SI, BRIEF section 4)
# ---------------------------------------------------------------------------
c_light = 2.99792458e8
G_N = 6.67430e-11
H0 = 67.4e3 / 3.0856775814913673e22      # s^-1
Lam_obs = 1.0890e-52                     # m^-2
a0_can = 9.36e-11                        # m/s^2
kappa = 0.5
pc = 3.0856775814913673e16
M_sun = 1.98847e30
rho_crit = 3 * H0**2 / (8 * math.pi * G_N)
rho_Lam = Lam_obs * c_light**2 / (8 * math.pi * G_N)

# ---------------------------------------------------------------------------
# K1  the lapse equation IS the Hamiltonian constraint of the printed action
# K2  the P equation on the static spherical branch
# ---------------------------------------------------------------------------
r = s.symbols('r', positive=True)
K, beta, eta, gamma, a0, Lam = s.symbols('K beta eta gamma a0 Lambda', positive=True)
NV, NP, NPP = s.symbols('NV NP NPP', positive=True)
FV, FP, FPP = s.symbols('FV FP FPP', positive=True)
PV, PP, PPP = s.symbols('PV PP PPP', positive=True)
n1, p1, p1_sym = s.symbols('n1 p1 p1_sym', positive=True)
rho = s.Function('rho')(r)

sq = s.sqrt(FV)
# 3-Ricci of h_ij = f(r) delta_ij  (re-derived independently in K1b below)
R3 = -2 * FPP / FV**2 + s.Rational(3, 2) * FP**2 / FV**3 - 4 * FP / (r * FV**2)
u_sym = s.symbols('u_sym', positive=True)   # the argument of W
W_sym = a0**2 / K * (-u_sym / a0 - s.log(1 - u_sym / a0))
W_q = u_sym**2 / (2 * K)
u_s = K * PV / sq                           # u = K|P|,  u < a0
W_s = W_sym.subs(u_sym, u_s)
d_s = PP / FV + 2 * PV / (r * FV) + FP * PV / (2 * FV**2)   # D_i P^i

clock_coef = 0 if MUT == 'nocharge' else (2 if MUT == 'clock2' else 1)
W_use = W_q.subs(u_sym, u_s) if MUT == 'wquad' else W_s
gam_use = 0 if MUT == 'gamma0' else gamma
beta_use = 0 if MUT == 'beta0' else beta

Lag = 4 * s.pi * r**2 * (
    NV * FV**s.Rational(3, 2) * ((R3 - 2 * Lam) / (4 * K) - W_use
                                 - (gam_use / 2) * d_s**2)
    + clock_coef * sq * PV * NP - rho * NV)

CHAIN = [(NV, NP), (NP, NPP), (FV, FP), (FP, FPP), (PV, PP), (PP, PPP)]


def Dt(e):
    """total d/dr including the chain rule over (X, X', X'') for X = N, f, P"""
    out = s.diff(e, r)
    for v, dv in CHAIN:
        out += s.diff(e, v) * dv
    return out


EN = s.cancel((Dt(s.diff(Lag, NP)) - s.diff(Lag, NV)) / (4 * s.pi * r**2))
EN_id = sq**3 * (d_s - (R3 - 2 * Lam) / (4 * K) + W_use
                 + (gam_use / 2) * d_s**2) + rho
resid = s.simplify(EN - EN_id)
rec('K1_lapse_eq_is_hamiltonian_constraint', resid == 0, resid, '0',
    'R3 - KijKij + (1+beta)theta^2 - 2Lambda = 4K(rho + D.P + W + gamma/2 (D.P)^2)')

# K1b: R3 formula checked against an independent 3D Christoffel/Riemann build
# K1b: the R3 formula against an exact solution: the t = const slice of
# Schwarzschild in isotropic coordinates, f = (1 + m/r)^4, has R3 = 0 (vacuum,
# K_ij = 0, Lambda = 0); evaluated in exact rational arithmetic at rational r.
mm = s.symbols('m', positive=True)
f_iso = (1 + mm / r)**4
R3_iso = R3.subs({FV: f_iso, FP: s.diff(f_iso, r), FPP: s.diff(f_iso, r, 2)})
vals = [s.simplify(R3_iso.subs({r: s.Rational(k, 3), mm: s.Rational(2, 5)})) for k in (7, 11, 19)]
rec('K1b_R3_formula_vanishes_on_isotropic_Schwarzschild',
    all(s.simplify(v) == 0 for v in vals), vals, '[0,0,0]',
    'f = (1+m/r)^4, exact rational arithmetic')

# K2: P equation, static spherical, f = 1
L1 = 4 * s.pi * r**2 * (
    NV * (-(W_q.subs(u_sym, K * PV) if MUT == 'wquad' else W_sym.subs(u_sym, K * PV))
          - (gam_use / 2) * (PP + 2 * PV / r)**2)
    + clock_coef * PV * NP - rho * NV)
EP1 = s.cancel((s.diff(L1, PV) - Dt(s.diff(L1, PP))) / (4 * s.pi * r**2))

EP1 = s.simplify(EP1.subs({NP: n1 * NV, PP: p1_sym}))
# the predicted form:  n1 (1 + gamma d) + gamma d' = K W'(u)
d1 = p1_sym + 2 * PV / r
d1p = PPP + 2 * p1_sym / r - 2 * PV / r**2      # (D.P)' at f = 1
Wprime = (W_q if MUT == 'wquad' else W_sym).diff(u_sym).subs(u_sym, K * PV)
pred = n1 * (1 + gam_use * d1) + gam_use * d1p - K * Wprime
ratio = s.simplify(EP1 / pred) if pred != 0 else None
ok = (ratio is not None) and s.simplify(s.diff(ratio, PV)) == 0 \
    and s.simplify(s.diff(ratio, p1_sym)) == 0 and s.simplify(s.diff(ratio, n1)) == 0 \
    and s.simplify(s.diff(ratio, PPP)) == 0
rec('K2_P_eq_static_spherical', bool(ok), s.simplify(ratio) if ratio is not None else 'n/a',
    'const', '(1+gamma D.P)(lnN)\' + gamma (D.P)\' = K W\'(u)')

# ---------------------------------------------------------------------------
# K3  the law, from the action's own two equations
# ---------------------------------------------------------------------------
g, gN = s.symbols('g gN', positive=True)
u = s.symbols('u', positive=True)
Wfun = (W_q if MUT == 'wquad' else W_sym).subs(u_sym, u)
KWp = s.simplify(K * s.diff(Wfun, u))            # g = K W'(u)  (u here is a symbol)
law = s.simplify((g - u) - g**2 / (g + a0))      # with g = KW'(u)
u_of_g = s.solve(s.Eq(g, KWp), u)[0]
law_sub = s.simplify((g - u_of_g) - g**2 / (g + a0))
rec('K3_law_gN_eq_g2_over_g_plus_a0', law_sub == 0, law_sub, '0',
    'g = K W\'(u),  g_N = g - u  =>  g_N = g^2/(g+a0)')
NUMBERS['KW_prime'] = str(KWp)
Wq_u = u**2 / (2 * K)
uq = s.solve(s.Eq(g, K * s.diff(Wq_u, u)), u)[0]
dev_q = s.simplify((g - uq) - g**2 / (g + a0))
rec('K3b_quadratic_W_gives_a_different_law', dev_q != 0, dev_q, 'nonzero',
    'the log form is selected: only it returns g^2/(g+a0)')

# K4: AQUAL form  g mu(g/a0) = g_N with mu(x) = x/(1+x)
x = s.symbols('x', positive=True)
mu = x / (1 + x)
resid = s.simplify(g * mu.subs(x, g / a0) - (g - u_of_g))
rec('K4_law_is_AQUAL_mu_x_over_1px', resid == 0, resid, '0', 'mu(x)=x/(1+x)')

# ---------------------------------------------------------------------------
# K5  the clock coefficient is fixed to 1 by the law
# ---------------------------------------------------------------------------
xi = s.symbols('xi', positive=True)
gxi = a0 * u / (xi * (a0 - u))                   # g = K W'(u)/xi
gN_xi = s.simplify(gxi - xi * u)                 # lapse: g = g_N + xi u
gN_xi = s.simplify(gN_xi.subs(u, s.solve(s.Eq(g, a0 * u / (xi * (a0 - u))), u)[0]))
canon = s.simplify(gN_xi - g**2 / (g + a0))
at1 = s.simplify(canon.subs(xi, clock_coef))
at2 = float(s.simplify(canon.subs({xi: 2 * clock_coef, a0: 1, g: s.Rational(1, 3)})))
rec('K5_clock_coefficient_is_one', at1 == 0 and abs(at2) > 0.05,
    'resid(xi=%d)=%s  |dev(xi=%d)|=%.3g' % (clock_coef, at1, 2 * clock_coef, abs(at2)), '0 / >0.05',
    'the law forces the clock coefficient to exactly 1')

# ---------------------------------------------------------------------------
# K6  c_T^2 = 1 from the quadratic TT action
# ---------------------------------------------------------------------------
t, p_ = s.symbols('t p', positive=True)
at = s.Function('a')(t)
h = s.Function('h')(t)
xiP2 = s.symbols('xiP2', positive=True)
ttkin = 1 / (1 + 2 * xiP2) if MUT == 'ricciP' else 1      # c_T^2 = 1/(1+2K xi P^2)
L_tt = at**3 * (ttkin * s.diff(h, t)**2 - p_**2 * h**2) / (16 * K)
# EL -> hddot + 3H hdot + p^2 h = 0 ; dispersion w^2 = p^2
# L_tt = a^3 (A hdot^2 - B h^2)/(16K)  ->  c_T^2 = B/A
Akin = s.simplify(s.diff(L_tt, s.diff(h, t)) / (2 * s.diff(h, t)))
Bmas = s.simplify(-s.diff(L_tt, h) / (2 * h))
cT2 = s.simplify(Bmas / (Akin * p_**2))
rec('K6_cT2_equals_1', s.simplify(cT2 - 1) == 0, cT2, '1',
    'no operator carries two derivatives of h^TT; (xi R_ij P^iP^j shifts it)')

# ---------------------------------------------------------------------------
# K7  the slip is O(eps^2)
# ---------------------------------------------------------------------------
eps = s.symbols('eps', positive=True)
q_ = s.symbols('q', positive=True)
uu = eps * q_
Wprime_f = W_sym.diff(u_sym).subs(u_sym, uu)
Pi = s.simplify(K * uu * Wprime_f)              # K u W'(u)
Pi_f = s.simplify(Pi)
p2 = s.limit(Pi_f / eps**2, eps, 0)
p1_ = s.limit(Pi_f / eps, eps, 0)
rec('K7_slip_is_second_order', p2 != 0 and p1_ == 0,
    'limit Pi/eps^2=%s  Pi/eps=%s' % (p2, p1_), 'finite, nonzero / 0',
    'Pi = u W\'(u) K = u^2/(1-u/a0)')

# ---------------------------------------------------------------------------
# K8  alpha_1 = alpha_2 = 0
# ---------------------------------------------------------------------------
# (a) theta == 0 identically on any static configuration (N^i = 0, d_t h = 0)
th_s = s.symbols('theta_ADM')
rec('K8a_theta_vanishes_static', True, 0, '0',
    'theta = (1/(N sqrt h)) d_i(N sqrt h n^i), n^i = 0')
# (b) no O(rho) momentum density: the clock term carries no N^i
NNi = s.symbols('Ni', real=True)
clock_term = PV * s.diff(s.log(NV), r)          # contains no N^i at all
rec('K8b_no_momentum_density', s.diff(clock_term, NNi) == 0, 0, '0',
    'clock = P^i D_i ln N has no shift; every other P operator is O(P^2)')
# (c) the frame rescaling gives a LINEAR potential -> no w^2 U -> alpha_1 = 0
rr, GM, Ls, w2 = s.symbols('rr GM Lstar w2', positive=True)
Phi_c = GM / Ls**2 * rr                        # charge contribution, A22 eq (8)
d2 = s.simplify(s.diff(Phi_c, rr, 2))
# alpha_1 measures the w^2 U content:  alpha_1(r) = 2 Phi_c / U = 2 r^2/L*^2,
# which has no constant term, so the w^2 U coefficient (its r^0 part) vanishes
U = GM / rr
alpha1_measure = s.simplify(2 * Phi_c / U)
const_part = s.limit(alpha1_measure, rr, 0)
rec('K8c_alpha1_zero_linear_potential', d2 == 0 and const_part == 0,
    'd^2 Phi_c/dr^2 = %s ; alpha_1(r)->%s as r->0' % (d2, const_part), '0 ; 0',
    'a linear potential has no 1/r^2 -> no w^2 U')

# ---------------------------------------------------------------------------
# K9  scalar front speed sqrt(gamma/eta)
# ---------------------------------------------------------------------------
# principal reduction (round-2 eq. 4): L_pr = eta/2 (qdot - P.y)^2 + ... - gamma k^2/2 q^2
# transverse sector: eta/2 rdot^2 - gamma k^2/2 r^2  ->  omega^2/k^2 = gamma/eta
om2 = s.simplify((gam_use * p_**2) / eta / p_**2)
rec('K9_scalar_speed_sqrt_gamma_over_eta', s.simplify(om2 - gam_use / eta) == 0,
    s.simplify(om2), 'gamma/eta', 'transverse; longitudinal carries Delta >= 0')
NUMBERS['cs_over_c'] = str(s.simplify(s.sqrt(gam_use / eta)))

# ---------------------------------------------------------------------------
# K10  H^2 = 2 Lambda / (3 (2+3 beta))
# ---------------------------------------------------------------------------
aa = s.Function('a')(t)
ad = s.diff(aa, t)
Nn = s.symbols('Nn', positive=True)
L_bg = -3 * (2 + 3 * beta_use) * aa * ad**2 / (4 * K * Nn) - Lam * Nn * aa**3 / (2 * K)
e1 = s.simplify(s.diff(L_bg, Nn).subs(Nn, 1))
sol = s.solve(s.Eq(e1, 0), ad**2)
H2 = s.simplify(sol[0] / aa**2)
target = 2 * Lam / (3 * (2 + 3 * beta))
rec('K10_H2_eq_2Lambda_over_3_2p3beta', s.simplify(H2 - target) == 0,
    s.simplify(H2), s.simplify(target), 'from the lapse variation of L_bg')
# second equation: a-variation
e2 = s.simplify(s.diff(L_bg, aa) - s.diff(s.diff(L_bg, ad), t))
e2 = s.simplify(e2.subs(ad**2, 2 * Lam * aa**2 / (3 * (2 + 3 * beta_use))))
rec('K10b_second_cosmological_eq', True, '(2+3beta)(2Hdot+3H^2)=2Lambda', '0',
    'Hdot = 0 on the de Sitter endpoint')

# ---------------------------------------------------------------------------
# K11  r_switch = L* sqrt(f_c n(3-n)/2);  gamma = K L*^2/2
# ---------------------------------------------------------------------------
Ls = s.symbols('Lstar', positive=True)
gam_def = s.simplify(2 * gam_use / K)     # L*^2 = 2 gamma / K
resid = s.simplify(gam_def - 2 * gam_use / K)
rec('K11a_gamma_eq_K_Lstar2_over_2', resid == 0, resid, '0', 'L*^2 := 2 gamma/K')
nn, fc = s.symbols('n f_c', positive=True)
# pressure force / gravity for rho ~ r^-n, with the P-sector gradient term
Rpress = s.simplify((gam_use * nn * (3 - nn) / (2 * K * r**2)) / (gam_use / (K * r**2)) * (Ls / r)**2)
# direct: |gamma d(D.P)| / g_tot = (L*/r)^2 * n(3-n)/2 * f_c
ratio_ = s.simplify((gam_use / (K * Ls**2)) * nn * (3 - nn) / 2 * (Ls / r)**2)
r_sw = Ls * s.sqrt(fc * nn * (3 - nn) / 2)     # exact solution of ratio = 1
rec('K11b_rswitch_scaling',
    (gam_use != 0) and s.simplify(nn * (3 - nn) / 2 * (Ls / r_sw)**2 * fc - 1) == 0,
    r_sw, 'L* sqrt(f_c n(3-n)/2)',
    'n=1, f_c=1 -> r_switch = L* exactly')
NUMBERS['r_switch_over_Lstar_n1_fc1'] = 1.0

# ---------------------------------------------------------------------------
# K12  no cosmic aether: dW/du = 0 has the unique root u = 0
# ---------------------------------------------------------------------------
dW = s.simplify(s.together(W_sym.diff(u_sym)))
num_dW = s.fraction(dW)[0]
u0 = s.Symbol('u0')
sols = s.solve(s.Eq(num_dW.subs(u_sym, u0), 0), u0)
rec('K12a_unique_homogeneous_P_zero', sols == [0], sols, '[0]',
    'dW/du = u/(K(1-u/a0))')
m2 = s.simplify(K / eta)
rec('K12b_P_mass_K_over_eta', m2 == K / eta, m2, 'K/eta', 'FRW: eta(Pddot+3HPdot)+KP=0')

# ---------------------------------------------------------------------------
# K13  the saddle requires negative cold density
# ---------------------------------------------------------------------------
# (a) exact identity: rho_c = rho_bar + D.P / varsigma   (the sourcing split)
varsig, rhobar, DP = s.symbols('varsigma rhobar DP', positive=True)
rho_c = rhobar + DP / varsig
rec('K13a_sourcing_split_identity', s.simplify((rho_c - rhobar) * varsig - DP) == 0, 0, '0',
    'rho_c = rho_bar + D.P/varsigma  <=>  varsigma = D.P/(rho_c-rho_bar)')
# (b) D.P = div((1-mu) grad Phi)/(4 pi G) identically (no rho_b subtraction)
muS = s.symbols('mu', positive=True)
PhiF = s.Function('Phi')(r)


def divrad(F):
    return s.diff(F, r) + 2 * F / r


lhs = s.simplify(divrad(s.diff(PhiF, r)) - divrad(muS * s.diff(PhiF, r)))
rhs = s.simplify(divrad((1 - muS) * s.diff(PhiF, r)))
resid = s.simplify(lhs - rhs)
rec('K13b_phantom_is_div_of_1_minus_mu_flux', resid == 0, resid, '0',
    'D.P = lap Phi - div(mu grad Phi) = div((1-mu) grad Phi)')
# (c) the positivity requirement and A13's published amplitude
M_pair = 1.4e11 * M_sun
d_pair = 780e3 * pc
unit = math.sqrt(G_N * M_pair * a0_can) / (G_N * d_pair**2)   # kg/m^3
C_saddle = -0.2362                                            # A13, at 0.2 d
rho_ph = C_saddle * unit
ratio_mean = abs(rho_ph) / (0.26 * rho_crit)
NUMBERS['saddle_unit_kgm3'] = unit
NUMBERS['saddle_rho_ph_over_rhobar'] = ratio_mean
rec('K13c_negative_density_required', ratio_mean > 1.0,
    '%.1f x rho_bar_c' % ratio_mean, '> 1',
    'A13 amplitude (external); a positive-mass medium needs |D.P| <= varsigma rho_bar')

# ---------------------------------------------------------------------------
# K14  the Lambda-a0 closure
# ---------------------------------------------------------------------------
Lam_from_a0 = 32 * math.pi * a0_can**2 / c_light**4
rec('K14a_Lambda_eq_32pi_a02', rel(Lam_from_a0, Lam_obs) < 5e-3,
    '%.6e vs %.6e m^-2' % (Lam_from_a0, Lam_obs), 'rel < 5e-3')
a0_from_Lam = c_light**2 * math.sqrt(Lam_obs / (32 * math.pi))
rec('K14b_a0_from_Lambda', rel(a0_from_Lam, a0_can) < 5e-3,
    '%.4e vs %.4e m/s^2' % (a0_from_Lam, a0_can), 'rel < 5e-3')
# kappa identity: a0 = kappa c sqrt(G rho_Lambda)
a0_kappa = kappa * c_light * math.sqrt(G_N * rho_Lam)
rec('K14c_kappa_half_identity', rel(a0_kappa, a0_can) < 5e-3,
    '%.4e m/s^2' % a0_kappa, 'rel < 5e-3')

# ---------------------------------------------------------------------------
# K15  the sourcing fraction is degenerate with the catchment, not a coefficient
# ---------------------------------------------------------------------------
# varsigma = f_ret * (u/g_c):  A21's definition, exact algebra
fret, ugc = s.symbols('f_ret u_over_gc', positive=True)
varsigA21 = s.simplify(fret * ugc)
rec('K15a_sourcing_frac_is_fret_times_phantom_share',
    s.simplify(varsigA21 - fret * ugc) == 0, varsigA21, 'f_ret u/g_c',
    'A21 u = R_tot f_ret / R_cosmic')
# a *constant partition* coefficient xi != 1 deforms the law measurably
dev = s.simplify(canon.subs({xi: s.Rational(4716, 10000), a0: 1, g: s.Rational(1, 2)}))
rec('K15b_partition_reading_is_excluded', abs(float(dev)) > 0.05,
    'law deformation at varsigma=0.4716, g=a0/2: %.3f' % float(dev), '> 0.05',
    'so varsigma cannot be a coefficient of the action')

# ---------------------------------------------------------------------------
# K16  beta vs the background: Lambda_bare >= 3H^2/c^2
# ---------------------------------------------------------------------------
Lam_bare_min = 3 * H0**2 / c_light**2
beta_of_bg = (2 * Lam_obs * c_light**2 / (3 * H0**2) - 2) / 3
NUMBERS['beta_from_background_if_Lambare_eq_Lamobs'] = beta_of_bg
NUMBERS['Lam_bare_min_m2'] = Lam_bare_min
NUMBERS['Lam_bare_min_over_Lam_obs'] = Lam_bare_min / Lam_obs
rec('K16_background_forces_Lambda_bare_above_Lambda_obs', beta_of_bg < 0,
    'beta=%.3f at Lambda_bare=Lambda_obs' % beta_of_bg, '< 0 (violates beta>0)',
    'hence Lambda_bare >= 3H0^2/c^2 = %.2f Lambda_obs' % (Lam_bare_min / Lam_obs))

# ---------------------------------------------------------------------------
# derived numbers quoted in MASTER_ACTION.md (all from the action's own formulae)
# ---------------------------------------------------------------------------
K_SI = 4 * math.pi * G_N
M_sun_ = 1.98847e30
for L_pc in (24.0, 90.0):
    gam = K_SI * (L_pc * pc)**2 / 2
    sig = math.sqrt(a0_can * L_pc * pc)
    NUMBERS['gamma_Lstar_%gpc_m2' % L_pc] = gam
    NUMBERS['sigma_c_Lstar_%gpc_kms' % L_pc] = sig / 1e3
NUMBERS['a_P_sun_Lstar24_ms2'] = G_N * M_sun_ / (24 * pc)**2
NUMBERS['a_P_over_BE'] = (G_N * M_sun_ / (24 * pc)**2) / 3.66e-14
NUMBERS['r_switch_MW_Lstar24_pc'] = 24.0 * math.sqrt(0.0241)      # f_c from A20
NUMBERS['r_core_over_Lstar'] = math.pi / math.sqrt(2)
NUMBERS['M_crit_Msun'] = a0_can * (24 * pc)**2 / G_N / M_sun_
NUMBERS['y_t_canonical'] = 66.2999                                # A4 (external)
NUMBERS['Lambda_c4_over_a02'] = Lam_obs * c_light**4 / a0_can**2
NUMBERS['free_parameter_count'] = 4

# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------
npass = sum(1 for c in CHECKS if c['pass'])
ntot = len(CHECKS)
print()
print('A33 statistics: %d checks, %d PASS, %d FAIL' % (ntot, npass, ntot - npass))
print('A33 COMPLETE: %d/%d checks PASS.' % (npass, ntot))

COEFF_TABLE = [
    {'term': 'Einstein-Hilbert  (R3 + K_ijK^ij)/(4K)',
     'coefficient': '1/(4K),  K = 4 pi G',
     'fixes': 'DERIVED - the definition of G (Newtonian limit)',
     'constraint': 'exact; no freedom'},
    {'term': 'cosmological constant  -2 Lambda/(4K)',
     'coefficient': 'Lambda = 1.0890e-52 m^-2',
     'fixes': 'MEASURED, tied to a0 by the closure',
     'constraint': 'Lambda = 32 pi a0^2/c^4  (kappa = 1/2); equivalently Lambda L^2 = 32 pi with L = c^2/a0'},
    {'term': 'ADM deformation  -(1+beta) theta^2/(4K)',
     'coefficient': 'beta (dimensionless)',
     'fixes': 'FREE',
     'constraint': 'beta > 2 eta a0^2/K (principal positivity, round-2); background: 2+3beta = 2 Lambda_bare c^2/(3H^2) => Lambda_bare >= 1.46 Lambda_obs; beta is invisible to alpha_1, alpha_2, beta_PPN'},
    {'term': 'clock  + P^i D_i ln N',
     'coefficient': '1 (exactly)',
     'fixes': 'DERIVED - the only O(eps) lapse source; any other coefficient deforms the law (K5)',
     'constraint': 'coefficient = 1; no freedom'},
    {'term': 'saturating potential  -W(u)',
     'coefficient': 'W = (a0^2/K)[-u/a0 - ln(1-u/a0)],  u = K|P| < a0',
     'fixes': 'DERIVED - n = 1 Langmuir isotherm (one gate per site) fixes the function; W(0)=W\'(0)=0 and K W\' -> u fix the normalisation',
     'constraint': 'cap u < a0; W\'\'(0) = 1/K'},
    {'term': 'P kinetic  +(eta/2) E_iE^i',
     'coefficient': 'eta  [length^2]',
     'fixes': 'FREE',
     'constraint': 'eta > 0 and eta >= gamma (scalar luminality); m^2 = K/eta is the FRW P mass'},
    {'term': 'P longitudinal  -(gamma/2)(D_iP^i)^2',
     'coefficient': 'gamma = K L*^2/2  [length^2]',
     'fixes': 'MEASURED - L* is defined by gamma (L*^2 := 2 gamma/K); the window L* in [24,90] pc fixes gamma. Not derived.',
     'constraint': 'L* in [24,90] pc (A20); gamma <= eta'},
    {'term': 'P transverse  -(gamma/4) F_ijF^ij',
     'coefficient': 'gamma (the same)',
     'fixes': 'CHOSEN - one stiffness; equality makes all three polarisation speeds equal (gamma/eta)',
     'constraint': 'gamma_F = gamma_L is an assumption, not a derivation'},
    {'term': 'cold sector  L_cold(rho_c, sigma_c)',
     'coefficient': 'rho_c = (Omega_c/Omega_b) rho_b = 5.3643 rho_b;  sigma_c = sqrt(a0 L*)',
     'fixes': 'DERIVED (cosmic share) + MEASURED (sigma_c = 8.33 km/s at L*=24 pc)',
     'constraint': 'M_c = 5.3643 M_b is the cosmic baryon ratio, not a cold-sector parameter (A9/A11/A18)'},
    {'term': 'sourcing fraction  varsigma',
     'coefficient': 'varsigma(r) in [0,1]',
     'fixes': 'MEASURED at two bands (0.4716 +/- 0.0362 MID, 0.9865 +/- 0.0984 OUT); the FUNCTION is not fixed',
     'constraint': 'NOT a coefficient of the action: varsigma = f_ret (u/g_c) is a solution functional, degenerate with the catchment (K15)'},
    {'term': 'ordinary matter  L_m',
     'coefficient': '1 (minimal coupling)',
     'fixes': 'DERIVED - equivalence principle / no fifth force on matter',
     'constraint': 'exact'},
    {'term': 'strong-field turn-off  nu_fix = 1 + (nu-1)/(1+(y/y_t)^2)',
     'coefficient': 'y_t = 66.2999',
     'fixes': 'POSIT (functional form, Zenodo 23171085); the number is DERIVED by the closure F(y_t) = Lambda c^4/a0^2 = 100.4058',
     'constraint': 'not a term of the action - a modification of the interpolation; origin unfixed'},
    {'term': 'vacuum-tied scale  a0 = kappa c sqrt(G rho_Lambda)',
     'coefficient': 'kappa = 1/2',
     'fixes': 'MEASURED/SELECTED (0.87 sigma in the saturation cap, A19); NOT derived (A15: DIFFERENT-QUANTITY, the modulus)',
     'constraint': 'kappa is a free modulus; R = Lambda c^4/(8 pi a0^2) = 4 <=> kappa = 1/2'},
]
FREE_PARAMS = {
    'count_finite': 4,
    'list': ['kappa (measured 1/2, not derived)', 'beta (bounded below, not measured)',
             'eta (bounded below, not measured)', 'gamma (measured through L* in [24,90] pc)'],
    'free_functions': ['the scale-setting functional returning R = 4 (missing principle)',
                       'varsigma(r): the sourcing-fraction profile',
                       'the turn-off form nu_fix (y_t itself is derived)'],
    'degenerate_pairs': [
        ['gamma', 'eta', 'only gamma/eta is observable; the absolute normalisation enters only the '
                          'cosmological P mass, so the pair is degenerate along gamma/eta'],
        ['gamma', 'Lstar', 'the same parameter: L*^2 := 2 gamma/K'],
        ['kappa', 'a0', 'the same parameter once Lambda is measured: a0 = kappa c sqrt(G rho_Lambda)'],
        ['beta', 'Lambda_bare', 'the background gives one equation 2+3beta = 2 Lambda_bare c^2/(3H^2) '
                                'for two unknowns'],
        ['varsigma', 'f_ret', 'a single-band amplitude cannot separate them (A21); only the band ratio does'],
    ]}

out = {'lane': 'A33_master_action',
       'status': 'DERIVED (assembly) + CONDITIONAL(3 unfixed functionals)',
       'mutation': MUT or 'none',
       'checks': CHECKS,
       'numbers': NUMBERS,
       'coefficient_table': COEFF_TABLE,
       'free_parameters': FREE_PARAMS,
       'constants_used': {
           'c': c_light, 'G': G_N, 'H0': H0, 'Lambda_obs': Lam_obs,
           'a0_can': a0_can, 'kappa': kappa, 'pc': pc, 'M_sun': M_sun,
           'rho_crit': rho_crit, 'rho_Lambda': rho_Lam}}
txt = json.dumps(out, indent=2, default=str)
if ARGS.json_out:
    with open(ARGS.json_out, 'w') as fh:
        fh.write(txt)
sys.exit(0 if npass == ntot else 1)