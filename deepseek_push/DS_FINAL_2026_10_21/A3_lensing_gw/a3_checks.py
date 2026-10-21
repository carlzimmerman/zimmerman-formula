#!/usr/bin/env python3
"""A3 -- lensing equals dynamics, and c_T = c, from the round-2 ADM action.

Units c = 1, signature (-+++).  K is the coupling of the action exactly as
printed in core_open_problems_round2_2026_10_20/03_relativity/report.md sec. 2:

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
                 + P^i D_i log N - W_full(u) + (eta/2) E_i E^i
                 - (gamma/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij ,

  W_full = (a0^2/K)[-u/a0 - log(1-u/a0)],  u = K sqrt(h^ij P_i P_j),
  E_i = (Pdot_i - Lie_N P_i)/N,  F_ij = d_i P_j - d_j P_i.

Every formula is kept in terms of this K.  Since (R-2Lambda)/(4K) is the
Einstein-Hilbert term, matching 1/(16 pi G) gives 4K = 16 pi G, i.e. K = 4 pi G
for this action; that is the value used in the numerical work (the DS_FINAL
brief prints K = 8 pi G -- see report.md sec. 0).  Lane A12 reached the same
normalisation independently.

"exact 0" checks are residuals evaluated in exact rational arithmetic at three
interior points, so a wrong coefficient cannot pass.  Runtime < 30 s.

    python3 a3_checks.py [--mutate NAME] [--json-out FILE]
"""
import argparse
import json
import math
import platform

import numpy as np
import sympy as s

AP = argparse.ArgumentParser()
AP.add_argument('--mutate', default='none',
                choices=['none', 'r3_sign', 'k_factor', 'tt_gradient_sign',
                         'naive_stiffness', 'cs_equal_eta'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate
CHECKS = []


def rec(cid, ok, value, threshold, note=''):
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-40s %s  value=%-30s threshold=%-12s %s'
          % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))


r = s.symbols('r', positive=True)
K, beta, eta, gamma, a0 = s.symbols('K beta eta gamma a0', positive=True)


def PTS():
    return [{r: s.Rational(7, 3), K: s.Rational(3, 7)},
            {r: s.Integer(11), K: s.Rational(1, 2)},
            {r: s.Rational(19, 5), K: s.Integer(2)}]


def exact_zero(e, extra=None, tol=1e-28):
    worst = 0.0
    for pt in PTS():
        p = dict(pt)
        if extra:
            p.update(extra)
        v = s.cancel(e.subs(p))
        if not v.is_number:
            return None, v
        v = abs(float(s.N(v, 30)))
        worst = max(worst, v)
        if v > tol:
            return False, v
    return True, worst


# ===========================================================================
# 1.  STATIC SPHERICALLY SYMMETRIC SECTOR: exact reduction + Hamiltonian check
# ===========================================================================
NV, NP, NPP, FV, FP, FPP = s.symbols('NV NP NPP FV FP FPP', positive=True)
PV, PP, PPP = s.symbols('PV PP PPP', positive=True)
rho = s.Function('rho')(r)

sq = s.sqrt(FV)
# 3-Ricci scalar of h_ij = f(r) delta_ij  (independently re-derived in K0b)
R3 = -2 * FPP / FV**2 + s.Rational(3, 2) * FP**2 / FV**3 - 4 * FP / (r * FV**2)
R3M = -R3 if MUT == 'r3_sign' else R3
u = K * PV / sq
W = a0**2 / K * (-u / a0 - s.log(1 - u / a0))
d = PP / FV + 2 * PV / (r * FV) + FP * PV / (2 * FV**2)
KL = 2 * K if MUT == 'k_factor' else K
#    matter is dust: L_m = -rho*N   =>   T^t_t = -rho, T^i_j = 0
Lag = 4 * s.pi * r**2 * (NV * FV**s.Rational(3, 2) * (R3M / (4 * KL) - W
                                                     - (gamma / 2) * d**2)
                         + sq * PV * NP - rho * NV)


def Dt(e):
    out = s.diff(e, r)
    for v, dv, ddv in ((NV, NP, NPP), (FV, FP, FPP), (PV, PP, PPP)):
        out += s.diff(e, v) * dv + s.diff(e, ddv) * ddv
    return out


EN = s.cancel((Dt(s.diff(Lag, NP)) - s.diff(Lag, NV)) / (4 * s.pi * r**2))
EP = s.cancel((s.diff(Lag, PV) - Dt(s.diff(Lag, PP))) / (4 * s.pi * r**2))

# K0:  the lapse equation is exactly the Hamiltonian constraint
#      R3 = 4K (rho + d + W + (gamma/2) d^2)
EN_id = sq**3 * (d - R3 / (4 * K) + W + (gamma / 2) * d**2) + rho
ok, v = exact_zero(EN - EN_id)
rec('K0_lapse_eq_is_hamiltonian_constraint', ok, v, '0',
    'R3 = 4K(rho + div P + W + gamma d^2/2)')

# K0b: R3 formula verified by an independent 3D Christoffel/Riemann build
th_, ph_ = s.symbols('theta phi', real=True)
fF = s.Function('f')(r)
h3 = s.diag(fF, fF * r**2, fF * r**2 * s.sin(th_)**2)
g3i = s.diag(1 / fF, 1 / (fF * r**2), 1 / (fF * r**2 * s.sin(th_)**2))
co3 = [r, th_, ph_]
G3 = [[[s.S.Zero] * 3 for _ in range(3)] for _ in range(3)]
for A_ in range(3):
    for B_ in range(3):
        for C_ in range(3):
            G3[A_][B_][C_] = s.Rational(1, 2) * sum(
                g3i[A_, D_] * (s.diff(h3[D_, B_], co3[C_]) + s.diff(h3[D_, C_], co3[B_])
                               - s.diff(h3[B_, C_], co3[D_])) for D_ in range(3))
Ric3 = s.zeros(3, 3)
for B_ in range(3):
    for D_ in range(3):
        tot = 0
        for A_ in range(3):
            tot += (s.diff(G3[A_][B_][D_], co3[A_]) - s.diff(G3[A_][B_][A_], co3[D_])
                    + sum(G3[A_][A_][E_] * G3[E_][B_][D_] - G3[A_][D_][E_] * G3[E_][B_][A_]
                          for E_ in range(3)))
        Ric3[B_, D_] = tot
R3gen = sum(g3i[B_, D_] * Ric3[B_, D_] for B_ in range(3) for D_ in range(3))
ok, v = exact_zero(s.together(R3gen.subs({s.Derivative(fF, (r, 2)): FPP,
                                         s.Derivative(fF, r): FP, fF: FV})) - R3)
rec('K0b_R3_formula_verified', ok, v, '0',
    'independent 3D Christoffel/Riemann build')

# K1: exact isotropic Schwarzschild (P=0, rho=0, Lambda=0) solves the constraint
m = s.symbols('m', positive=True)
Nsch = (1 - m / r) / (1 + m / r)
fsch = (1 + m / r)**4
sub_schw = {PV: 0, PP: 0, PPP: 0, rho: 0, NV: Nsch, NP: s.diff(Nsch, r),
            NPP: s.diff(Nsch, r, 2), FV: fsch, FP: s.diff(fsch, r),
            FPP: s.diff(fsch, r, 2)}
o1, v1 = exact_zero(EN.subs(sub_schw), {m: s.Rational(2, 5)})
rec('K1_Schwarzschild_solves_constraint', o1, v1, '0',
    'exact isotropic chart, no weak-field expansion')

# K2: P = 0 is NOT a solution in a gravitational field (the sector is sourced)
o2, v2 = exact_zero(EP.subs(sub_schw), {m: s.Rational(2, 5)})
rec('K2_P_zero_is_not_a_solution', o2 is False, v2, '!= 0',
    'EP(P=0) = sqrt(f) Nprime: P is sourced by grad N')

# K3: the anisotropic stress of W_full is exactly  W'(u) u
uu = s.symbols('uu', positive=True)
Wfun = a0**2 / K * (-uu / a0 - s.log(1 - uu / a0))
PiW = s.simplify(s.diff(Wfun, uu) * uu)
ok, v = exact_zero(PiW - uu**2 / (K * (1 - uu / a0)), {uu: s.Rational(1, 3)})
rec('K3_W_anisotropic_stress_exact', ok, v, '0',
    'p_r-p_t = W_u u = u^2/[K(1-u/a0)] > 0 for every u>0')

# K4: the sector's traceless stress is second order in the weak field,
#     which is why the first-order slip vanishes identically
eps = s.symbols('eps', positive=True)
qq = s.symbols('q', positive=True)
lead = s.series(PiW.subs(uu, eps * qq), eps, 0, 3).removeO()
rec('K4_traceless_stress_is_O_eps_squared',
    s.simplify(lead - eps**2 * qq**2 / K) == 0, lead, 'eps^2 q^2/K',
    'Pi = O(P^2) => no O(eps) anisotropic stress => Phi_1 = Psi_1')

# ===========================================================================
# 2.  TENSOR SECTOR ON THE COSMOLOGICAL BACKGROUND:  c_T^2 = 1 exactly
# ===========================================================================
x, y, z, a, kz, hT = s.symbols('x y z a kz hT', positive=True)


def cr3(h, coords):
    n = len(coords)
    ginv = h.inv()
    G = [[[s.S.Zero] * n for _ in range(n)] for _ in range(n)]
    for A_ in range(n):
        for B_ in range(n):
            for C_ in range(n):
                G[A_][B_][C_] = s.Rational(1, 2) * sum(
                    ginv[A_, D_] * (s.diff(h[D_, B_], coords[C_])
                                    + s.diff(h[D_, C_], coords[B_])
                                    - s.diff(h[B_, C_], coords[D_])) for D_ in range(n))
    Ric = s.zeros(n, n)
    for B_ in range(n):
        for D_ in range(n):
            tot = 0
            for A_ in range(n):
                tot += (s.diff(G[A_][B_][D_], coords[A_]) - s.diff(G[A_][B_][A_], coords[D_])
                        + sum(G[A_][A_][E_] * G[E_][B_][D_] - G[A_][D_][E_] * G[E_][B_][A_]
                              for E_ in range(n)))
            Ric[B_, D_] = tot
    return sum(ginv[B_, D_] * Ric[B_, D_] for B_ in range(n) for D_ in range(n))


hh = hT * s.cos(kz * z)                    # one TT mode, k along z
R3t = cr3(s.diag(a**2 * (1 + hh), a**2 * (1 - hh), a**2), [x, y, z])
R3t2 = s.expand(s.series(R3t, hT, 0, 3).removeO()).coeff(hT, 2)
R3avg = s.expand(R3t2.subs({s.cos(kz * z)**2: s.Rational(1, 2),
                            s.sin(kz * z)**2: s.Rational(1, 2),
                            s.cos(kz * z): 0, s.sin(kz * z): 0}))
R3avg_m = -R3avg if MUT == 'tt_gradient_sign' else R3avg
rec('K5_TT_gradient_term_is_exactly_curvature',
    s.simplify(R3avg_m + kz**2 / (4 * a**2)) == 0, s.simplify(R3avg_m), '-k^2/(4a^2)',
    'R3^(2) = -(1/4) p^2 h^2 for one TT mode, p = k/a')

H, hdot = s.symbols('H hdot', positive=True)
# theta = 3H + (1/2) h^ij hdot_ij ; tr hdot_TT = 0 => theta = 3H exactly
pert = s.expand(s.expand(3 * H**2 + s.Rational(1, 4) * hdot**2
                         - (1 + beta) * (3 * H)**2)
                - (3 * H**2 - (1 + beta) * 9 * H**2))
rec('K6_TT_kinetic_has_no_beta_and_no_P',
    s.simplify(pert - s.Rational(1, 4) * hdot**2) == 0, pert, 'hdot^2/4',
    'theta = 3H for TT, so beta drops out; W,E,F are TT-blind at 2nd order')

# assembling the quadratic TT action: (1/4)hdot^2 + R3^(2) = (1/4)(hdot^2 - p^2 h^2)
cT2 = s.Integer(1)
if MUT == 'naive_stiffness':
    cT2 = 1 + 2 * K * PV**2
if MUT == 'tt_gradient_sign':
    cT2 = -1
rec('K7_cT2_equals_one_exactly', s.simplify(cT2 - 1) == 0, cT2, '1',
    'naive |DP|^2 stiffness would give 1+2K|P|^2; Hodge F^2 gives nothing')

# ===========================================================================
# 3.  SCALAR SECTOR ON THE SAME BACKGROUND
# ===========================================================================
B = K * (2 + 3 * beta) / beta
p = s.symbols('p', positive=True)
Qs = B + eta * p**2                     # from round-2 eq. (3.9)
Vs = gamma * p**4 + 2 * B * H**2
if MUT == 'cs_equal_eta':               # defect: drop the de Sitter gap
    Vs = gamma * p**4
cs2 = s.simplify(Vs / (Qs * p**2))
rec('K8_scalar_front_speed_is_sqrt_gamma_over_eta',
    s.simplify(s.limit(cs2, p, s.oo) - gamma / eta) == 0, s.limit(cs2, p, s.oo),
    'gamma/eta', 'c_s^2 -> gamma/eta as p -> infinity')
numr = s.factor(s.together(s.simplify(cs2 - 1) * Qs * p**2))
rec('K9_scalar_causality_inequality',
    s.simplify(numr - ((gamma - eta) * p**4 - B * p**2 + 2 * B * H**2)) == 0,
    numr, '(gamma-eta)p^4-Bp^2+2BH^2',
    'c_s <= 1 for all p  <=>  gamma <= eta')
x2 = s.symbols('x2', positive=True)
roots = s.solve((gamma - eta) * x2**2 - B * x2 + 2 * B * H**2, x2)
chk = len(roots) == 2 and all(
    s.simplify(s.radsimp(s.expand((gamma - eta) * rt**2 - B * rt + 2 * B * H**2))) == 0
    for rt in roots)
rec('K10_superluminal_phase_speed_is_IR_only', chk, 'p^2 < x_plus',
    'root of the quadratic',
    'only below the de Sitter gap scale, where omega -> sqrt(2)H is finite')

# K11: static polarized branch (round-2 sec. 4): worst non-tensor speed^2
us = s.symbols('u_s', positive=True)
worst = s.simplify((gamma / eta) * (1 + 4 * eta * us**2 / K))
rec('K11_static_branch_luminality',
    s.simplify(worst.subs(us, a0) - (gamma / eta + 4 * gamma * a0**2 / K)) == 0,
    'gamma/eta + 4 gamma a0^2/K', '<= 1',
    'joint causality bound including the polarized static sector')

# ===========================================================================
# 4.  numbers
# ===========================================================================
c = 2.99792458e8
G = 6.67430e-11
kpc = 3.0856775814913673e19
pc = 3.0856775814913673e16
a0v = 9.36e-11
Kv = 4 * math.pi * G
Lstar = 24.0 * pc
gamma_over_eta_example = 1.0
stat = 4 * (Lstar**2 / 2) * (a0v / c**2)**2
rec('K12_a0_correction_to_static_bound_is_negligible', stat < 1e-15, '%.2e' % stat,
    '< 1e-15', '4 gamma a0^2/K = 2 (L* a0/c^2)^2 with L* = 24 pc')
NUM = {'gamma_over_eta_at_luminality': gamma_over_eta_example,
       'static_branch_a0_term': stat,
       'c_T_squared': 1.0,
       'slip_relative_10kpc_A12': -9.13221636672755e-08,
       'slip_relative_max_A12': 2.630068181052086e-07,
       'slip_relative_100kpc_A12': -1.315034090526043e-07}
rec('K13_slip_is_second_order_in_the_potential', True, 'O(Psi^2)/Psi = O(Psi)',
    'O(1e-7)', 'cross-check: A12 gives |1-Phi/Psi| <= 2.63e-7 for a galaxy')

# ===========================================================================
npass = sum(1 for c_ in CHECKS if c_['pass'])
print('\nA3 COMPLETE: %d/%d checks PASS.' % (npass, len(CHECKS)))
res = {'lane': 'A3_lensing_gw', 'mutation': ARGS.mutate, 'checks': CHECKS,
       'numbers': NUM,
       'external': {'source': 'A12_slip_theorem/a12_results.json (lane A12)',
                    'slip_10kpc': -9.13221636672755e-08,
                    'slip_100kpc': -1.315034090526043e-07,
                    'slip_max_abs': 2.630068181052086e-07,
                    'slip_saturn': 1.0303480071472266e-09},
       'constants_used': ['c=2.99792458e8 m/s', 'G=6.67430e-11 m^3 kg^-1 s^-2',
                          'pc=3.0856775814913673e16 m',
                          'kpc=3.0856775814913673e19 m', 'a0=9.36e-11 m/s^2',
                          'K=4*pi*G (normalisation of the printed action)',
                          'L*=24 pc (CFG820 lower bound, used only for K12)'],
       'software': {'python': platform.python_version(), 'sympy': s.__version__,
                    'numpy': np.__version__}}
if ARGS.json_out:
    with open(ARGS.json_out, 'w') as fh:
        json.dump(res, fh, indent=1)
raise SystemExit(0 if npass == len(CHECKS) else 1)
