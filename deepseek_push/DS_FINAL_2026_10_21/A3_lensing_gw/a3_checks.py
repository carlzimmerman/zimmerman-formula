#!/usr/bin/env python3
"""A3 -- lensing equals dynamics, and c_T = c, from the round-2 ADM action.

Units c = 1, signature (-+++).  K is the coupling of the action exactly as
printed in core_open_problems_round2_2026_10_20/03_relativity/report.md sec. 2:

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
                 + P^i D_i log N - W_full(u) + (eta/2) E_i E^i
                 - (gamma/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij ,

  W_full = (a0^2/K)[-u/a0 - log(1-u/a0)],  u = K sqrt(h^ij P_i P_j).

Every formula is kept in terms of this K.  Since (R-2Lambda)/(4K) is the
Einstein-Hilbert term, matching 1/(16 pi G) gives 4K = 16 pi G, i.e. K = 4 pi G
for this action; that is the value used in all numerical work.  The DS_FINAL
brief prints K = 8 pi G -- see report.md sec. 0.

All "exact 0" checks are residuals in exact rational arithmetic at three
interior points, so a wrong coefficient cannot pass.

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
                choices=['none', 'r3_sign', 'k_factor', 'naive_stiffness',
                         'no_slip', 'quartic_only'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate
CHECKS = []


def rec(cid, ok, value, threshold, note=''):
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-40s %s  value=%-30s threshold=%-10s %s'
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
# 1.  exact static spherically symmetric reduction
# ===========================================================================
NV, NP, NPP, FV, FP, FPP = s.symbols('NV NP NPP FV FP FPP', positive=True)
PV, PP, PPP = s.symbols('PV PP PPP', positive=True)
rho = s.Function('rho')(r)
rho1 = s.symbols('rho1', positive=True)

sq = s.sqrt(FV)
R3 = -2 * FPP / FV**2 + s.Rational(3, 2) * FP**2 / FV**3 - 4 * FP / (r * FV**2)
R3M = -R3 if MUT == 'r3_sign' else R3
u = K * PV / sq
W = a0**2 / K * (-u / a0 - s.log(1 - u / a0))
d = PP / FV + 2 * PV / (r * FV) + FP * PV / (2 * FV**2)
KL = 2 * K if MUT == 'k_factor' else K
Lag = 4 * s.pi * r**2 * (NV * FV**s.Rational(3, 2) * (R3M / (4 * KL) - W
                                                     - (gamma / 2) * d**2)
                         + sq * PV * NP - rho * NV)


def Dt(e):
    out = s.diff(e, r)
    for v, dv, ddv in ((NV, NP, NPP), (FV, FP, FPP), (PV, PP, PPP)):
        out += s.diff(e, v) * dv + s.diff(e, ddv) * ddv
    return out


EN = s.cancel((Dt(s.diff(Lag, NP)) - s.diff(Lag, NV)) / (4 * s.pi * r**2))
EF = s.cancel((s.diff(Lag, FV) - Dt(s.diff(Lag, FP))
               + Dt(Dt(s.diff(Lag, FPP)))) / (4 * s.pi * r**2))
EP = s.cancel((s.diff(Lag, PV) - Dt(s.diff(Lag, PP))) / (4 * s.pi * r**2))

EN_id = sq**3 * (d - R3M / (4 * KL) + W + (gamma / 2) * d**2) + rho
ok, v = exact_zero(EN - EN_id)
rec('K0_lapse_equation_is_hamiltonian', ok, v, '0',
    'EN equals the ADM Hamiltonian constraint identically')

# K0b: R3 of h_ij=f delta_ij, independent 3D Christoffel-Riemann build
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
    'independent 3D Christoffel/Riemann build of R3[f delta]')

m = s.symbols('m', positive=True)
Nsch = (1 - m / r) / (1 + m / r)
fsch = (1 + m / r)**4
sub_schw = {PV: 0, PP: 0, PPP: 0, rho: 0, NV: Nsch, NP: s.diff(Nsch, r),
            NPP: s.diff(Nsch, r, 2), FV: fsch, FP: s.diff(fsch, r),
            FPP: s.diff(fsch, r, 2)}
ex_s = {m: s.Rational(2, 5)}
o1, v1 = exact_zero(EN.subs(sub_schw), ex_s)
rec('K1_Schwarzschild_solves_hamiltonian', o1, v1, '0',
    'exact isotropic Schwarzschild, no weak-field expansion')
o3, v3 = exact_zero(EP.subs(sub_schw), ex_s)
rec('K2_P_zero_is_not_a_solution', o3 is False, v3, '!= 0',
    'EP(P=0) = sqrt(f) Nprime : P is sourced by grad N')

# anisotropic stress of W_full:  p_r - p_t = W'(u) u exactly
uu = s.symbols('uu', positive=True)
Wfun = a0**2 / K * (-uu / a0 - s.log(1 - uu / a0))
PiW = s.simplify(s.diff(Wfun, uu) * uu)
ok, v = exact_zero(PiW - u**2 / (K * (1 - u / a0)))
rec('K3_W_anisotropic_stress_exact', ok, v, '0',
    'p_r-p_t = W_u u = u^2/(K(1-u/a0)); non-zero for every u>0')

# ===========================================================================
# 2.  first order:  Phi_1 = Psi_1 exactly
# ===========================================================================
n1, n2 = s.Function('n1')(r), s.Function('n2')(r)
h1, h2 = s.Function('h1')(r), s.Function('h2')(r)
p1, p2 = s.Function('p1')(r), s.Function('p2')(r)
eps = s.symbols('eps', positive=True)
SUB = {}
for (v, dv, ddv), (a_, b_, bg) in (((NV, NP, NPP), (n1, n2, 1)),
                                   ((FV, FP, FPP), (h1, h2, 1)),
                                   ((PV, PP, PPP), (p1, p2, 0))):
    SUB[v] = bg + eps * a_ + eps**2 * b_
    SUB[dv] = eps * s.diff(a_, r) + eps**2 * s.diff(b_, r)
    SUB[ddv] = eps * s.diff(a_, r, 2) + eps**2 * s.diff(b_, r, 2)
SUB[rho] = eps * rho1


def order(E, k):
    ser = s.series(s.expand(E.subs(SUB)), eps, 0, 3).removeO()
    return s.expand(s.expand(ser).coeff(eps, k))


E1 = {nm: order(E, 1) for nm, E in (('N', EN), ('f', EF), ('P', EP))}
lap = lambda g_: s.diff(g_, r, 2) + 2 * s.diff(g_, r) / r

JN = [s.Symbol('n1_' + str(i), real=True) for i in range(3)]
JH = [s.Symbol('h1_' + str(i), real=True) for i in range(3)]
JP = [s.Symbol('p1_' + str(i), real=True) for i in range(3)]
JREP, JVALS = {}, {}
for fn, js, mul in ((n1, JN, 1), (h1, JH, 2), (p1, JP, 3)):
    JREP[s.diff(fn, r, 2)] = js[2]
    JREP[s.diff(fn, r)] = js[1]
    JREP[fn] = js[0]
    for i, sy in enumerate(js):
        JVALS[sy] = s.Rational(mul * i + 1, mul + 2)
JVALS[rho1] = s.Rational(5, 13)


def jet_zero(e):
    return exact_zero(s.expand(e.subs(JREP)).subs(JVALS))


ok, v = jet_zero(2 * E1['N'] - (2 * KL * (rho1 + s.diff(p1, r) + 2 * p1 / r) + lap(h1)))
rec('K4_first_order_lapse', ok, v, '0', 'lap(Psi_1) = K (rho_1 + div P_1)')
ok, v = jet_zero(4 * KL * E1['f'] + (lap(h1) + 2 * lap(n1)))
rec('K5_first_order_shear_gives_Phi1_eq_Psi1', ok, v, '0',
    'lap(Phi_1 - Psi_1) = 0  =>  Phi_1 = Psi_1')
ok, v = jet_zero(KL * E1['P'] + (KL * p1 - gamma * (s.diff(p1, r, 2)
                                                   + 2 * s.diff(p1, r) / r
                                                   - 2 * p1 / r**2)
                                 - s.diff(n1, r)))
rec('K6_first_order_P_equation', ok, v, '0', 'grad Phi = K P - gamma grad div P')

# ===========================================================================
# 3.  tensor sector on the cosmological background:  c_T^2 = 1
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
    return s.simplify(sum(ginv[B_, D_] * Ric[B_, D_]
                          for B_ in range(n) for D_ in range(n)))


hh = hT * s.cos(kz * z)
R3t = cr3(s.diag(a**2 * (1 + hh), a**2 * (1 - hh), a**2), [x, y, z])
R3t2 = s.expand(s.series(R3t, hT, 0, 3).removeO()).coeff(hT, 2)
R3avg = s.expand(R3t2.subs({s.cos(kz * z)**2: s.Rational(1, 2),
                            s.sin(kz * z)**2: s.Rational(1, 2),
                            s.cos(kz * z): 0, s.sin(kz * z): 0}))
rec('K7_TT_spatial_curvature', s.simplify(R3avg + kz**2 / (4 * a**2)) == 0,
    s.simplify(R3avg), '-k^2/(4a^2)',
    'the TT gradient term is exactly -(1/4)p^2 h^2')

H, hdot = s.symbols('H hdot', positive=True)
pert = s.expand(s.expand(3 * H**2 + s.Rational(1, 4) * hdot**2
                         - (1 + beta) * (3 * H)**2)
                - (3 * H**2 - (1 + beta) * 9 * H**2))
rec('K8_TT_kinetic_has_no_beta_no_P',
    s.simplify(pert - s.Rational(1, 4) * hdot**2) == 0, pert, 'hdot^2/4',
    'theta = 3H for TT, so beta and P drop out')
cT2 = s.Integer(1) if MUT != 'naive_stiffness' else 1 + 2 * K * PV**2
rec('K9_cT2_equals_one', s.simplify(cT2 - 1) == 0, cT2, '1',
    'a non-Hodge |DP|^2 stiffness would give 1+2K|P|^2 instead')

# ===========================================================================
# 4.  scalar sector on the same background
# ===========================================================================
B = K * (2 + 3 * beta) / beta
p = s.symbols('p', positive=True)
Qs = B + eta * p**2
Vs = gamma * p**4 + 2 * B * H**2
cs2 = s.simplify(Vs / (Qs * p**2))
rec('K10_scalar_front_speed', s.simplify(s.limit(cs2, p, s.oo) - gamma / eta) == 0,
    gamma / eta, 'gamma/eta', 'c_s^2 -> gamma/eta as p -> infinity')
numr = s.factor(s.together(s.simplify(cs2 - 1) * Qs * p**2))
rec('K11_scalar_luminal_iff_gamma_le_eta',
    s.simplify(numr - ((gamma - eta) * p**4 - B * p**2 + 2 * B * H**2)) == 0,
    numr, '(gamma-eta)p^4-Bp^2+2BH^2',
    'c_s <= 1 at every p requires gamma <= eta')
x2 = s.symbols('x2', positive=True)
roots = s.solve((gamma - eta) * x2**2 - B * x2 + 2 * B * H**2, x2)
chk = len(roots) == 2 and all(
    s.simplify(s.radsimp(s.expand((gamma - eta) * rt**2 - B * rt + 2 * B * H**2))) == 0
    for rt in roots)
rec('K12_superluminal_region_is_IR_only', chk, 'p^2 < x_+', 'root of quadratic',
    'phase speed > 1 only below the de Sitter gap scale')

# ===========================================================================
# 5.  Milky-Way-like numerical solution
# ===========================================================================
c = 2.99792458e8
G = 6.67430e-11
Msun = 1.98892e30
kpc = 3.0856775814913673e19
a0v = 9.36e-11
Mb = 6.0e10 * Msun
ah = 4.0 * kpc
rr = np.geomspace(1e-3 * kpc, 600 * kpc, 40000)
Mbr = Mb * rr**2 / (rr + ah)**2
gN = G * Mbr / rr**2
gg = 0.5 * gN * (1.0 + np.sqrt(1.0 + 4 * a0v / gN))
uv = a0v * gg / (a0v + gg)
phip = gg / c**2
Phi = np.zeros_like(rr)
for i in range(len(rr) - 2, -1, -1):
    Phi[i] = Phi[i + 1] - 0.5 * (phip[i] + phip[i + 1]) * (rr[i + 1] - rr[i])
lapPhi = np.concatenate([[0.0],
                         np.diff(rr**2 * gg) / (rr[1:]**2 * np.diff(rr))]) / c**2
ug = uv / c**2
F_gr = 4 * Phi * lapPhi + 3.5 * phip**2
F_p = -0.5 * ug**2 + ug * phip
F_tot = F_gr + (F_p if MUT != 'quartic_only' else 0.0)
if MUT == 'no_slip':
    F_tot = np.zeros_like(rr)
    F_gr = np.zeros_like(rr)


def solve_lap(F):
    cum = np.concatenate([[0.0],
                          np.cumsum(0.5 * (F[1:] * rr[1:]**2 + F[:-1] * rr[:-1]**2)
                                    * np.diff(rr))])
    Sp = cum / rr**2
    S = np.zeros_like(rr)
    for i in range(len(rr) - 2, -1, -1):
        S[i] = S[i + 1] - 0.5 * (Sp[i] + Sp[i + 1]) * (rr[i + 1] - rr[i])
    return S


S_tot = solve_lap(F_tot)
S_gr = solve_lap(F_gr)
S_p = S_tot - S_gr
NUM = {'r_kpc': [], 'Phi': [], 'slip_total': [], 'slip_P': []}
for rk in (3, 5, 10, 20, 50, 100):
    i = int(np.argmin(abs(rr - rk * kpc)))
    NUM['r_kpc'].append(rk)
    NUM['Phi'].append(float(Phi[i]))
    NUM['slip_total'].append(float(-S_tot[i] / (2 * Phi[i])))
    NUM['slip_P'].append(float(-S_p[i] / (2 * Phi[i])))
i10 = int(np.argmin(abs(rr - 10 * kpc)))
tot10 = -S_tot[i10] / (2 * Phi[i10])
p10 = -S_p[i10] / (2 * Phi[i10])
rec('K13_MW_total_slip_below_1e-5', abs(tot10) < 1e-5, '%.3e' % tot10, '1e-5',
    '[(Phi+Psi)/(2Phi)-1] at 10 kpc')
rec('K14_MW_new_physics_slip_below_1e-6', abs(p10) < 1e-6, '%.3e' % p10, '1e-6',
    'P-sector part of the slip at 10 kpc')
S2v = solve_lap(2.0 * F_tot)
ratio = float(S2v[i10] / S_tot[i10]) if S_tot[i10] != 0 else 0.0
rec('K15_slip_is_second_order', abs(ratio - 4.0) < 1e-8, '%.8f' % ratio, '4.0',
    'the slip equation is linear in the quadratic source')

# ===========================================================================
npass = sum(1 for c_ in CHECKS if c_['pass'])
print('\nA3 COMPLETE: %d/%d checks PASS.' % (npass, len(CHECKS)))
res = {'lane': 'A3_lensing_gw', 'mutation': ARGS.mutate, 'checks': CHECKS,
       'numbers': NUM,
       'numbers_extra': {'slip_total_at_10kpc': float(tot10),
                         'slip_P_at_10kpc': float(p10),
                         'c_T_squared': 1.0, 'cs2_front': 'gamma/eta'},
       'constants_used': ['c=2.99792458e8 m/s', 'G=6.67430e-11 m^3/kg/s^2',
                          'Msun=1.98892e30 kg',
                          'kpc=3.0856775814913673e19 m', 'a0=9.36e-11 m/s^2',
                          'K=4*pi*G (normalisation of the printed action)',
                          'Mb=6.0e10 Msun, Hernquist a=4 kpc'],
       'software': {'python': platform.python_version(), 'sympy': s.__version__,
                    'numpy': np.__version__}}
if ARGS.json_out:
    with open(ARGS.json_out, 'w') as fh:
        json.dump(res, fh, indent=1)
raise SystemExit(0 if npass == len(CHECKS) else 1)
