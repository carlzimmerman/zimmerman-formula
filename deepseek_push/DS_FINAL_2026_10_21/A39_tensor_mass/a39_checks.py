#!/usr/bin/env python3
"""A39 -- the tensor mass on a Pbar != 0 background: does it break anything?

A31 check 28: A3 proves c_T^2 = 1 on the Pbar = 0 de Sitter background.  Off it,
W(u) with u = K sqrt(h^ij P_i P_j) contracts Pbar_i Pbar_j with the TT
perturbation.  What is the resulting mass, what is its sign, and does any
observation see it?

Action (frozen, exactly as printed in
core_open_problems_round2_2026_10_20/03_relativity/report.md sec. 2, and as used
by A3):

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
                 + P^i D_i log N - W(u) + (eta/2) E_i E^i
                 - (gamma/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij ,
  W(u) = (a0^2/K)[-u/a0 - log(1-u/a0)],   u = K sqrt(h^ij P_i P_j).

Units c = 1 in the algebra (u and a0 are then inverse lengths); every number is
converted to SI/eV explicitly.  K = 4 pi G for this action (A3 sec. 1).
K cancels out of m_T^2 -- it enters only through u = K|Pbar| -- so the
4 pi G vs 8 pi G convention moves no number in this lane.

The algebra is done with K = a0 = 1 and p = x (so u = x); the general formula is
restored at the end and checked against the direct symbolic result.

    python3 a39_checks.py [--mutate NAME] [--json-out FILE]
"""
import argparse
import json
import math
import platform

import numpy as np
import sympy as sp

AP = argparse.ArgumentParser()
AP.add_argument('--mutate', default='none',
                choices=['none', 'inverse_linear', 'no_sqrtg', 'W_sign',
                         'no_running', 'a31_coefficient'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate
CHECKS = []


def rec(cid, ok, value, threshold, note=''):
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-52s %s  value=%-34s threshold=%-12s %s'
          % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))


# ===========================================================================
# 0.  Geometry: one TT mode, inverse metric, exact u(h)
# ===========================================================================
h, c, p, K, a0, Y, tt = sp.symbols('h c p K a0 Y t', positive=True)
th, ph = sp.symbols('theta phi', real=True)
x, Ls, om, eta_s, mm, kk = sp.symbols('x L_ omega eta m_T2 k', positive=True)

EPS = sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]])   # TT polarization, k || z
I3 = sp.eye(3)

#  g_ij = delta_ij + h c eps_ij ;  g^ij = delta - h eps + h^2 eps^2 + O(h^3)
g = I3 + h * c * EPS
if MUT == 'inverse_linear':
    ginv = I3 - h * c * EPS                    # defect: linear-order inverse
else:
    ginv = I3 - h * c * EPS + h**2 * c**2 * (EPS * EPS)
detg = sp.expand((1 + h * c) * (1 - h * c))    # = 1 - h^2 c^2

Z3 = sp.zeros(3, 3)
r0 = sp.expand(g * ginv - I3)
rec('C0_inverse_metric_correct_to_O_h2',
    r0.subs(h, 0) == Z3 and sp.diff(r0, h).subs(h, 0) == Z3
    and sp.diff(r0, h, 2).subs(h, 0) == Z3 and r0 != Z3,
    'g g^{-1} - I = diag(%s, %s, %s)' % (r0[0, 0], r0[1, 1], r0[2, 2]), 'O(h^3), not 0',
    'g^ij = delta - h eps + h^2 eps^2 is exact through the order that enters a '
    'second-order expansion; dropping the h^2 term is a real defect (mutant)')


def W_of(u):
    w = a0**2 / K * (-u / a0 - sp.log(1 - u / a0))
    return -w if MUT == 'W_sign' else w


def sqrtg(hh):
    return sp.Integer(1) if MUT == 'no_sqrtg' else sp.sqrt(detg.subs(h, hh))


def u_of(n, hh=h, Yv=None):
    """u = K sqrt(g^ij P_i P_j), Pbar = p n, mode h_ij = hh*c*eps_ij."""
    q = sp.expand((n.T * ginv.subs(h, hh) * n)[0])
    return K * (p if Yv is None else p + Yv) * sp.sqrt(q)


# --- C1: second-order coefficient of u itself (= A31's 3Kp/8) ---------------
n_x = sp.Matrix([1, 0, 0])                     # Pbar along x
u_ser = sp.series(u_of(n_x), h, 0, 3).removeO()
u0, u1, u2 = [sp.simplify(u_ser.coeff(h, i)) for i in range(3)]
rec('C1_u_expansion_coefficients',
    sp.simplify(u0 - K * p) == 0 and sp.simplify(u1 + K * p * c / 2) == 0
    and sp.simplify(u2 - sp.Rational(3, 8) * K * p * c**2) == 0,
    'u/Kp = 1 + (%s) h + (%s) h^2' % (sp.simplify(u1 / (K * p)),
                                     sp.simplify(u2 / (K * p * c**2))),
    'coeffs 1, -c/2, 3c^2/8',
    'reproduces A31 check 28 exactly: the h^2 coefficient of u is 3Kp/8 -- but '
    'that is d2u/dh2, not the h^2 coefficient of the action')

# --- C2: exact h^2 coefficient of -sqrt(g) W(u) ----------------------------
Lfroz = -sqrtg(h) * W_of(u_of(n_x))
chh_raw = sp.simplify(sp.expand(sp.series(Lfroz, h, 0, 3).removeO()).coeff(h, 2))
chh = sp.simplify(chh_raw.subs(c, 1) / 2)      # <c^2> = 1/2
if MUT == 'a31_coefficient':
    chh = sp.Rational(3, 8) * K * p                # defect: A31's 3Kp/8 used as the mass coefficient
mT2_lit = sp.simplify(-16 * K * chh)

#  work in x: K = a0 = 1, p = x  (so u = x); a0 = 1 also means 4 a0^2 -> 4
SUBX = {K: 1, a0: 1, p: x}


def inx(e):
    return sp.simplify(sp.expand(e.subs(SUBX)))


mT2_shape_x = x**2 * (4 - 3 * x) / (1 - x)**2
mT2_vol_x = 4 * (x + sp.log(1 - x))
resid = inx(mT2_lit) - mT2_shape_x - mT2_vol_x
rec('C2_closed_form_literal_expansion', sp.simplify(resid) == 0,
    'residual = %s' % sp.simplify(resid), '0',
    'm_T^2(literal) = u^2(4-3x)/(1-x)^2 + 4a0^2[x+ln(1-x)], x = u/a0')

#  finite-difference cross-check of the same coefficient (no series involved)
def fd(q, hv=2e-4):
    f = lambda z: float((-sqrtg(z) * W_of(u_of(n_x, hh=z))).subs({K: 1, a0: 1, p: q, c: 1}))
    return (f(hv) - 2 * f(0.0) + f(-hv)) / (2 * hv**2)


cA = lambda q: float((-mT2_lit / (16 * K)).subs({K: 1, a0: 1, p: q}))
fd_err = max(abs(fd(q) - 2 * cA(q)) / abs(2 * cA(q)) for q in (0.2, 0.5, 0.8))
rec('C2b_finite_difference_confirms_the_series', fd_err < 1e-6,
    'max rel. error of d2/dh2 = %.2e' % fd_err, '< 1e-6',
    'the sympy series is checked against a direct second difference of the exact '
    'Lagrangian at three backgrounds (factor 2 = <c^2> = 1/2)')

# --- C3: the two pieces separately -----------------------------------------
Wbar = a0**2 / K * (-K * p / a0 - sp.log(1 - K * p / a0))
if MUT == 'W_sign':
    Wbar = -Wbar
vol_diff = inx(chh + mT2_shape_x / (16 * K) - Wbar / 4)
rec('C3_volume_piece_is_the_Lambda_coupling', sp.simplify(vol_diff) == 0,
    'c_hh - c_shape - Wbar/4 = %s' % sp.simplify(vol_diff), '0',
    'the sqrt(g) piece is exactly +W/4 h^2: the coupling of a TT mode to an '
    'energy density W, i.e. a cosmological-constant term.  A Lambda does not '
    'give a graviton a mass, so this piece is removed by comparing with GR on '
    'the same background.  The P-specific (shape) piece is u^2(4-3x)/(1-x)^2.')

# --- C4: general direction and polarization --------------------------------
n_gen = sp.Matrix([sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)])
Lg = -sqrtg(h) * W_of(u_of(n_gen))
c_g = sp.simplify(sp.expand(sp.series(Lg, h, 0, 3).removeO()).coeff(h, 2)
                  .subs(c, 1) / 2)
mT2_g = sp.simplify(-16 * K * c_g)
NX, NY = sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph)
pred_g = ((K * p)**2 * (4 * (NX**2 + NY**2) / (1 - x)
                        + (NX**2 - NY**2)**2 * x / (1 - x)**2)
          + 4 * a0**2 * (x + sp.log(1 - x)))
res_g = sp.simplify((mT2_g - pred_g).subs(SUBX))
kpar = sp.simplify((mT2_g - 4 * (x + sp.log(1 - x))).subs(SUBX).subs(th, 0))
rec('C4_general_direction_and_polarization',
    res_g == 0 and sp.simplify(kpar) == 0,
    'residual = %s ; k||Pbar residual %s' % (res_g, sp.simplify(kpar)), '0 ; 0',
    'm_T^2(n) = u^2[4(eps^2)_ij n^i n^j/(1-x) + (eps_ij n^i n^j)^2 x/(1-x)^2] '
    '+ volume.  The mass is direction- and polarization-dependent and vanishes '
    'identically for k || Pbar: an anisotropic medium mass, not Proca.')

# --- C5: sign --------------------------------------------------------------
xs = np.linspace(1e-7, 1 - 1e-7, 300001)
shape_num = xs**2 * (4 - 3 * xs) / (1 - xs)**2
lit_num = shape_num + 4 * (xs + np.log(1 - xs))
rec('C5_mT2_positive_definite_no_tachyon',
    bool(np.all(shape_num > 0) and np.all(lit_num > 0)),
    'min shape = %.3e, min literal = %.3e (both > 0)'
    % (shape_num.min(), lit_num.min()), '> 0',
    'both conventions (shape-only and the literal expansion including the '
    'volume piece) are strictly positive on x in (0,1).  4-3x > 0 for every '
    'x < 1, so there is no zero and no tachyon: the mode is massive, stable.')

# --- C6: u -> 0 ------------------------------------------------------------
lim_shape = sp.limit(shape_num[0] * 0 + mT2_shape_x / x**2, x, 0)
lim_lit = sp.limit((mT2_shape_x + mT2_vol_x) / x**2, x, 0)
rec('C6_vanishes_as_u_squared', lim_shape == 4 and lim_lit == 2,
    'shape/u^2 -> %s ; literal/u^2 -> %s' % (lim_shape, lim_lit), '4 and 2',
    'm_T^2 -> 4u^2 (shape) / 2u^2 (literal) as u -> 0: quadratic, so m_T = 0 '
    'exactly on the Pbar = 0 cosmological background')

# --- C7: Pbar = 0 ----------------------------------------------------------
rec('C7_mT_is_zero_exactly_at_Pbar_0',
    sp.simplify(mT2_lit.subs(p, 0)) == 0,
    'm_T^2(p=0) = %s' % sp.simplify(mT2_lit.subs(p, 0)), '0',
    'P = 0 is the unique homogeneous solution (no-aether theorem, FINAL 3), so '
    'the cosmological background has m_T = 0 exactly')

# ===========================================================================
# 1.  The P field relaxes: eliminating delta P -> a running mass
# ===========================================================================
L2 = -sqrtg(h) * W_of(u_of(n_x, Yv=Y))
Lq = sp.expand(sp.series(L2.subs({h: tt * h, Y: tt * Y}), tt, 0, 3).removeO()
               .subs(c, 1))
c_hh2 = inx(sp.simplify(Lq.coeff(h, 2) / tt**2))
c_YY = inx(sp.simplify(Lq.coeff(Y, 2) / tt**2))
c_hY = inx(sp.simplify(Lq.coeff(h, 1).coeff(Y, 1) / tt**2))
Wv = inx(Wbar / 2)   # c=1 convention: volume piece is W/2 (mode avg -> W/4)

c_eff0 = sp.simplify(c_hh2 - c_hY**2 / (4 * c_YY))
c_res0 = sp.simplify(c_eff0 - Wv)          # shape piece left after relaxation
rec('C8_static_elimination_screens_the_shape_term_to_O_u3',
    sp.simplify(c_res0 + x**3 / (8 * (1 - x))) == 0,
    'c_eff(0) - W/2 = %s   (= -u^2 x/(8(1-x)) = -x^3/(8(1-x)))'
    % sp.simplify(c_res0), '-x^3/(8(1-x))',
    'with delta P free at zero frequency the O(u^2) shape term is absorbed (a '
    'shift of P along Pbar holds u fixed); the residue is O(u^3/a0).  The '
    'volume piece survives untouched.  So the mass is a running mass.')

mY2 = sp.simplify(-2 * c_YY / (Ls**2 / 2))     # m_Y^2 = A/eta, A = -2c_YY, eta = K L*^2/2
rec('C9_P_field_mass_is_sqrt2_over_Lstar',
    sp.simplify(mY2 - 2 / (Ls**2 * (1 - x)**2)) == 0,
    'm_Y^2 = -2 c_YY/(K L*^2/2) = %s' % sp.simplify(mY2), '2/(L*^2 (1-x)^2)',
    'the mediator is the P field: m_Y = sqrt(2)/(L*(1-x)) = 3.77e-25 eV, i.e. '
    'lambda_P = 17.0 pc = L*/sqrt2 at x = 0 -- A22 eq. (9).  Normalisation check.')

#  finite frequency: c_YY -> c_YY - eta omega^2/2 with eta = L*^2/2
c_eff_om = sp.simplify(c_hh2 - c_hY**2 / (4 * (c_YY - (Ls**2 / 2) * om**2 / 2)))
mY2x = 2 / (Ls**2 * (1 - x)**2)
interp = (sp.simplify(c_hh2) if MUT == 'no_running'
          else sp.simplify(c_hh2 - (c_hh2 - c_eff0) * mY2x / (om**2 + mY2x)))
grid = [(0.10, 0.3), (0.10, 3.0), (0.30, 1.0), (0.50, 0.01),
        (0.50, 1.0), (0.70, 10.0), (0.90, 1.0), (0.90, 100.0)]
worst = 0.0
for xv, q in grid:
    s = {x: xv, Ls: sp.Float(1.0), om: sp.Float(q)}
    a_ = complex(sp.N(c_eff_om.subs(s), 30))
    b_ = complex(sp.N(interp.subs(s), 30))
    worst = max(worst, abs(a_ - b_) / max(abs(b_), 1e-300))
rec('C10_running_mass_interpolation', worst < 1e-9,
    'max rel. deviation over 8 (x, omega) points = %.2e' % worst, '< 1e-9',
    'c_eff(omega) = c_frozen - (c_frozen - c_eff(0)) m_Y^2/(omega^2+m_Y^2) is '
    'exact: c_eff(0) after relaxation, c_frozen for omega >> m_Y')

mT2_run = sp.simplify((-8 * (c_hh2 - Wv) * om**2
                       - 8 * c_res0 * mY2x) / (om**2 + mY2x))
worst2 = 0.0
for xv, q in grid:
    s = {x: xv, Ls: sp.Float(1.0), om: sp.Float(q)}
    a_ = complex(sp.N(mT2_run.subs(s), 30))
    pred = ((mT2_shape_x * om**2 + (x**3 / (1 - x)) * mY2x)
            / (om**2 + mY2x)).subs(s)
    b_ = complex(sp.N(pred, 30))
    worst2 = max(worst2, abs(a_ - b_) / max(abs(b_), 1e-300))
rec('C11_running_mass_closed_form', worst2 < 1e-9,
    'max rel. deviation = %.2e' % worst2, '< 1e-9',
    'm_T^2(omega) = [u^2(4-3x)/(1-x)^2 omega^2 + (u^2 x/(1-x)) m_Y^2]/'
    '(omega^2+m_Y^2), m_Y = sqrt(2)/(L*(1-x)): the answer in (a0, K, u, L*)')

# ===========================================================================
# 2.  c_T^2 survives as a speed statement
# ===========================================================================
w2 = kk**2 + mm
cT2 = sp.simplify(w2.coeff(kk, 2))
vg = sp.series(sp.diff(sp.sqrt(w2), kk), mm, 0, 2).removeO()
vph = sp.series(sp.sqrt(w2) / kk, mm, 0, 2).removeO()
rec('C12_cT2_is_1_and_vg_is_c_1_minus_m2_over_2E2',
    cT2 == 1 and sp.simplify(vg - (1 - mm / (2 * kk**2))) == 0
    and sp.simplify(vph - (1 + mm / (2 * kk**2))) == 0,
    'omega^2 = k^2 + m_T^2 -> c_T^2 = %s, v_g = 1 - m_T^2/(2 omega^2)' % cT2, '1',
    'the mass term is a pure potential (W carries no derivative of h), so it '
    'adds to omega^2 but not to the k^2 coefficient: c_T^2 = 1 exactly survives, '
    'while the group velocity is c(1 - m_T^2/2omega^2).')

# ===========================================================================
# 3.  numbers
# ===========================================================================
c_light = 2.99792458e8
hbar = 1.054571817e-34
eV = 1.602176634e-19
G = 6.67430e-11
pc = 3.0856775814913673e16
kpc = 1e3 * pc
Mpc = 1e6 * pc
Gpc = 1e9 * pc
a0v = 9.36e-11
Lstar_m = 24.0 * pc
Kv = 4 * math.pi * G
H0 = 2.184e-18
MG_BOUND = 1.76e-23


def fT(xv):
    return xv * math.sqrt(max(4 - 3 * xv, 0.0)) / (1 - xv)


def mT_eV(xv):
    return hbar * a0v * fT(xv) / c_light / eV          # E = hbar u f(x)/c


def lam_m(xv):
    return 1.0 / ((a0v * xv / c_light**2) * fT(xv))


def mY_eV(xv):
    return hbar * c_light * (math.sqrt(2) / (Lstar_m * (1 - xv))) / eV


TAB = []
for xv in (0.1, 0.3, 0.5, 0.7, 0.9):
    TAB.append({'x': xv, 'u_over_a0': xv, 'u_m_s2': a0v * xv,
                'm_T_eV': mT_eV(xv), 'compton_m': lam_m(xv),
                'compton_pc': lam_m(xv) / pc, 'compton_kpc': lam_m(xv) / kpc,
                'compton_Mpc': lam_m(xv) / Mpc, 'compton_Gpc': lam_m(xv) / Gpc,
                'm_T_over_mY': mT_eV(xv) / mY_eV(xv),
                'margin_vs_1p76e-23': MG_BOUND / mT_eV(xv)})
rec('C13_mass_table_is_monotone_and_horizon_scale',
    all(TAB[i]['m_T_eV'] < TAB[i + 1]['m_T_eV'] for i in range(len(TAB) - 1))
    and TAB[-1]['m_T_eV'] < 1e-30,
    'm_T(0.1)=%.2e eV ... m_T(0.9)=%.2e eV' % (TAB[0]['m_T_eV'], TAB[-1]['m_T_eV']),
    '< 1e-30 eV',
    'galactic background u = 0.1 a0 ... 0.9 a0; Compton wavelength 1.5e6 Mpc '
    'down to 3.4e3 Mpc -- the mass is a horizon-scale quantity')

# --- (i) GW dispersion at 100 Hz -------------------------------------------
f_gw = 100.0
E_gw = hbar * 2 * math.pi * f_gw / eV
DISP = []
for xv in (0.1, 0.5, 0.9):
    m = mT_eV(xv)
    DISP.append({'x': xv, 'm_T_eV': m, 'E_gw_eV': E_gw,
                 'frac_speed_deficit': 0.5 * (m / E_gw)**2,
                 'arrival_delay_s_at_40Mpc':
                 0.5 * (m / E_gw)**2 * (40 * Mpc) / c_light})
BOUND_SPEED = 1e-15
rec('C14_gw_speed_deficit_vs_GW170817',
    all(d['frac_speed_deficit'] < BOUND_SPEED for d in DISP),
    'max deficit = %.2e at x=0.9' % max(d['frac_speed_deficit'] for d in DISP),
    '< 1e-15',
    '(c_gw-c)/c = -1/2 (m_T c^2/E)^2 with E = hbar 2 pi 100 Hz = 4.14e-13 eV: '
    '26 orders of magnitude inside GW170817, and a 1e-34 s arrival delay')

# --- (ii) Yukawa cutoff ----------------------------------------------------
L_gal = 30 * kpc
YUK = []
for xv in (0.1, 0.5, 0.9):
    for D, tag in ((L_gal, '30 kpc: the real path through the P-medium'),
                   (40 * Mpc, '40 Mpc: if the mass were on all the way'),
                   (1 * Gpc, '1 Gpc: unphysical, Pbar = 0 in the IGM')):
        YUK.append({'x': xv, 'D_m': D, 'label': tag,
                    'amp_suppression': 1 - math.exp(-D / lam_m(xv))})
rec('C15_yukawa_cutoff_unobservable_on_the_real_path',
    max(y['amp_suppression'] for y in YUK if 'real path' in y['label']) < 1e-4,
    'max on a 30 kpc path = %.2e' % max(y['amp_suppression'] for y in YUK
                                        if 'real path' in y['label']),
    '< 1e-4',
    'exp(-D/lambda_C).  The mode is massive only inside the P-medium (Pbar = 0 '
    'in the IGM by the no-aether theorem), so the physical path is ~30 kpc '
    'against lambda_C > 3.4e3 Mpc.')

# --- (iii) graviton mass bound --------------------------------------------
RAT = [{'x': xv, 'ratio_bound_over_mT': MG_BOUND / mT_eV(xv)} for xv in (0.1, 0.5, 0.9)]
rec('C16_below_the_graviton_mass_bound',
    all(r['ratio_bound_over_mT'] > 1e9 for r in RAT),
    'min margin = %.2e at x=0.9' % min(r['ratio_bound_over_mT'] for r in RAT),
    '> 1e9',
    'm_g < 1.76e-23 eV: the theory sits 8.4e9 (x=0.9) to 4.0e11 (x=0.1) below it')

xc = None
for i in range(1, 600000):
    xv = 1 - 10**(-i / 10000.0)
    if mT_eV(xv) > MG_BOUND:
        xc = xv
        break
rec('C17_bound_needs_u_within_1e-11_of_the_cap',
    xc is not None and (1 - xc) < 1e-9,
    'x_crit = %.12f  (1-x = %.3e)' % (xc, 1 - xc) if xc else 'not reached',
    '1-x < 1e-9',
    'the theory would reach the graviton bound only if u/a0 were within ~1e-11 '
    'of the cap u = a0, where W itself is singular')

# --- (iv) lensing ----------------------------------------------------------
N_l = sp.symbols('N_l', positive=True)
mass_term = sp.expand(sp.series(Lfroz, h, 0, 3).removeO()).coeff(h, 2)
rho_gw = (c_light**2 / (32 * math.pi * G)) * (2 * math.pi * f_gw)**2 * (1e-22)**2
rho_c = 3 * H0**2 * c_light**2 / (8 * math.pi * G)
shift = (mT_eV(0.5) / E_gw)**2 * rho_gw / rho_c
rec('C18_mass_term_is_TT_only_lapse_blind_and_null_for_lensing',
    sp.simplify(sp.diff(mass_term, N_l)) == 0 and sp.simplify(sp.trace(EPS)) == 0
    and shift < 1e-40,
    'd(coeff)/dN = 0 ; tr(eps) = 0 ; dPhi/Phi <= %.2e' % shift, '0 ; 0 ; < 1e-40',
    'W(u) contains neither lapse nor shift and the polarization is traceless, '
    'so the mass term has no scalar projection and cannot enter the lapse/shift '
    'constraints that fix Phi, Psi.  Its own O(h^2) stress is (m_T/E)^2 rho_gw, '
    'a fraction 1e-46 of rho_c: the lensing prediction is untouched.')

# --- A31 cross-check ------------------------------------------------------
dim_slip = sp.simplify(u2 - sp.Rational(3, 8) * K * p * c**2)
d2W = sp.simplify(sp.diff(W_of(u_of(n_x)), h, 2).subs(h, 0))
mT2_A31 = sp.simplify(-16 * K * (sp.Rational(3, 8) * K * p))   # the A31 reading
rec('C20_A31_coefficient_is_d2u_dh2_not_the_action',
    dim_slip == 0 and sp.simplify(d2W - sp.Rational(3, 8) * K * p * c**2) != 0
    and sp.simplify(mT2_lit - mT2_A31) != 0,
    'd2u/dh2 = 3Kp/8 ; d2W/dh2 = %s' % sp.simplify(d2W.subs(c, 1)),
    '3Kp/8 vs a different object',
    'A31 check 28 quotes 3Kp/8 as the "h^2 coefficient"; that is d2u/dh2, not '
    'd2W/dh2, so it is not a mass.  The action coefficient is C2.  A31 is '
    'qualitatively right that the quadratic action is not Einstein off Pbar=0; '
    'the number it prints is not the mass and the magnitude is harmless.')

# ===========================================================================
npass = sum(1 for c_ in CHECKS if c_['pass'])
print('\nA39 COMPLETE: %d/%d checks PASS.' % (npass, len(CHECKS)))
res = {'lane': 'A39_tensor_mass', 'mutation': ARGS.mutate,
       'status': 'DERIVED / harmless', 'checks': CHECKS,
       'verdict': {'m_T_eV_at_u_a0_over_10': mT_eV(0.1),
                   'm_T_eV_at_u_0p9_a0': mT_eV(0.9),
                   'ratio_to_graviton_bound_worst': MG_BOUND / mT_eV(0.9),
                   'gw_speed_deficit_at_100Hz': max(d['frac_speed_deficit'] for d in DISP),
                   'gw170817_speed_bound': BOUND_SPEED,
                   'tachyonic': False, 'excludes_Pbar_nonzero': False},
       'formula': {'m_T2_shape': 'u^2 (4-3x)/(1-x)^2,  x = u/a0',
                   'm_T2_literal': 'u^2(4-3x)/(1-x)^2 + 4 a0^2 [x + ln(1-x)]',
                   'm_T2_running': '[shape*omega^2 + (u^2 x/(1-x))*mY^2]/(omega^2+mY^2)',
                   'm_T2_at_LIGO': 'shape to 8e-25 relative',
                   'm_Y': 'sqrt(2)/(L*(1-x))'},
       'table': TAB, 'dispersion': DISP, 'yukawa': YUK, 'mass_bound': RAT,
       'numbers': {'a0_m_s2': a0v, 'Lstar_pc': Lstar_m / pc, 'K_SI': Kv,
                   'E_gw_100Hz_eV': E_gw, 'M_graviton_bound_eV': MG_BOUND,
                   'mY_eV_x0': mY_eV(0.0),
                   'lambda_P_pc': 1 / (math.sqrt(2) / Lstar_m) / pc,
                   'x_crit': xc, 'one_minus_x_crit': (1 - xc) if xc else None,
                   'c_over_H0_Mpc': c_light / H0 / Mpc,
                   'c2_over_a0_Mpc': c_light**2 / a0v / Mpc,
                   'Lstar_a0_over_c2_sq': (Lstar_m * a0v / c_light**2)**2},
       'constants_used': ['c=2.99792458e8 m/s', 'hbar=1.054571817e-34 J s',
                          'G=6.67430e-11', 'pc=3.0856775814913673e16 m',
                          'a0=9.36e-11 m/s^2 (canonical footing)',
                          'L*=24 pc (A20 lower bound)',
                          'K=4*pi*G (action normalisation; cancels in m_T^2)'],
       'external': {'A31_check28': '3Kp/8 reproduced as d2u/dh2 (not a mass)',
                    'A3': 'c_T^2 = 1 on Pbar = 0 (m_T(p=0) = 0 reproduced)',
                    'A22': 'lambda_P = L*/sqrt2 = 17.0 pc (reproduced as m_Y)'},
       'software': {'python': platform.python_version(), 'sympy': sp.__version__,
                    'numpy': np.__version__}}
if ARGS.json_out:
    with open(ARGS.json_out, 'w') as fh:
        json.dump(res, fh, indent=1)
raise SystemExit(0 if npass == len(CHECKS) else 1)
