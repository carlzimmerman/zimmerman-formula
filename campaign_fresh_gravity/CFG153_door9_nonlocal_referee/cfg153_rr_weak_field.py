#!/usr/bin/env python3
"""
CFG153 -- referee of CFG123 (Door 9): the weak-field effective density of the
Maggiore-Mancarella RR model against CFG44's target.

Frozen criteria: ../CFG153_FROZEN_CRITERIA.md (its sha256 is printed first).
Own code throughout: nothing is imported from CFG123 or from CFG44.

Run (from anywhere; outputs are written beside this file):
    python3 cfg153_rr_weak_field.py             main run
    MUTATE=1 python3 cfg153_rr_weak_field.py    plant m_static = 1e3 * m in the static action

Outputs: cfg153_rr_weak_field[_MUTATE].out and cfg153_rr_weak_field[_MUTATE]_results.json.
Exit codes (frozen): main 0 iff H1 and C1-C6 pass, else 1.
                     MUTATE 1 iff H1 fails with the predicted 6.000 +- 0.01 dex shift at every
                     grid point; 0 (H1 still passes) or 2 (shift misses) = control failure.

Units: route A/B and the background are symbolic (c = 1).  The grid is in SI with mpmath.
"""
import os
import sys
import json
import time
import hashlib
import platform

import numpy as np
import sympy as sp
import mpmath as mpm
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.normpath(os.path.join(HERE, '..', 'CFG153_FROZEN_CRITERIA.md'))
MUTATE = os.environ.get('MUTATE', '0').strip() not in ('', '0')
if len(sys.argv) > 1 and sys.argv[1].strip().upper() in ('MUTATE', '--MUTATE', '1'):
    MUTATE = True
SLUG = 'cfg153_rr_weak_field' + ('_MUTATE' if MUTATE else '')
OUT_PATH = os.path.join(HERE, SLUG + '.out')
JSON_PATH = os.path.join(HERE, SLUG + '_results.json')
K_PLANT = 1000 if MUTATE else 1          # m_static = K_PLANT * m (frozen MUTATE factor 1e3)

_out = open(OUT_PATH, 'w')


def P(*args):
    s = ' '.join(str(a) for a in args)
    print(s)
    _out.write(s + '\n')
    _out.flush()


def banner(s):
    P('')
    P('=' * 100)
    P(s)
    P('=' * 100)


RES = {'lane': 'CFG153', 'mode': 'MUTATE' if MUTATE else 'main', 'K_plant': K_PLANT,
       'checks': {}, 'rows': {}}
CHECKS = []   # (name, ok, load_bearing, detail)


def check(name, ok, detail, load_bearing=True):
    ok = bool(ok)
    CHECKS.append((name, ok, load_bearing, detail))
    RES['checks'][name] = {'pass': ok, 'load_bearing': load_bearing, 'detail': detail}
    P('  [%s]%s %s: %s' % ('PASS' if ok else 'FAIL', '' if load_bearing else ' (reported)', name, detail))
    return ok


def f2s(v, n=6):
    try:
        return mpm.nstr(mpm.mpf(v), n)
    except Exception:
        return str(v)


def jnum(v):
    if isinstance(v, (mpm.mpf,)):
        return float(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    return v


# ---------------------------------------------------------------------------------------------
banner('CFG153 referee of CFG123 (door 9) -- header')
with open(SPEC, 'rb') as fh:
    SPEC_SHA = hashlib.sha256(fh.read()).hexdigest()
P('frozen criteria: ../CFG153_FROZEN_CRITERIA.md  sha256 =', SPEC_SHA)
RES['spec_sha256'] = SPEC_SHA
P('mode:', RES['mode'], '  K_plant (m_static / m) =', K_PLANT)
P('python', platform.python_version(), ' sympy', sp.__version__, ' scipy', scipy.__version__,
  ' mpmath', mpm.__version__, ' numpy', np.__version__)
RES['versions'] = {'python': platform.python_version(), 'sympy': sp.__version__,
                   'scipy': scipy.__version__, 'mpmath': mpm.__version__, 'numpy': np.__version__}

# ---------------------------------------------------------------------------------------------
# Geometry helper (own): Christoffels, Ricci scalar for a diagonal metric.
# Convention: R_bd = d_a G^a_bd - d_d G^a_ba + G^a_ae G^e_bd - G^a_de G^e_ba ; R = g^bd R_bd.


def christoffel(g, coords):
    n = len(coords)
    assert g.is_diagonal()
    ginv = sp.diag(*[1 / g[i, i] for i in range(n)])
    Gam = [[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(b, n):
                s = sp.S.Zero
                for d in range(n):
                    if ginv[a, d] == 0:
                        continue
                    s += ginv[a, d] * (sp.diff(g[d, c], coords[b]) + sp.diff(g[d, b], coords[c])
                                       - sp.diff(g[b, c], coords[d]))
                Gam[a][b][c] = Gam[a][c][b] = s / 2
    return ginv, Gam


def ricci_scalar(g, coords):
    n = len(coords)
    ginv, Gam = christoffel(g, coords)
    R = sp.S.Zero
    for b in range(n):
        for d in range(n):
            if ginv[b, d] == 0:
                continue
            s = sp.S.Zero
            for a in range(n):
                s += sp.diff(Gam[a][b][d], coords[a]) - sp.diff(Gam[a][b][a], coords[d])
                for e in range(n):
                    s += Gam[a][a][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][a]
            R += ginv[b, d] * s
    return R


banner('Geometry helper self-tests (own code)')
_th, _ph = sp.symbols('theta_s phi_s')
_a0 = sp.Symbol('a_s', positive=True)
_R2 = sp.simplify(ricci_scalar(sp.diag(_a0 ** 2, _a0 ** 2 * sp.sin(_th) ** 2), (_th, _ph)))
_t = sp.Symbol('t_s')
_af = sp.Function('a_s')(_t)
_RF = ricci_scalar(sp.diag(-1, _af ** 2, _af ** 2, _af ** 2), (_t,) + sp.symbols('y1:4'))
_dF = sp.simplify(_RF - 6 * (_af.diff(_t, 2) / _af + _af.diff(_t) ** 2 / _af ** 2))
P('  2-sphere of radius a: R =', _R2, '   FRW: R - 6(a\'\'/a + a\'^2/a^2) =', _dF)
GEOM_OK = (sp.simplify(_R2 - 2 / _a0 ** 2) == 0) and (_dF == 0)
P('  geometry helper sane:', GEOM_OK)
RES['geometry_selftest'] = GEOM_OK

# ---------------------------------------------------------------------------------------------
Gs, msym, Msym = sp.symbols('G m M', positive=True)      # m = background-fixed mass (1/length)
rr = sp.Symbol('r', positive=True)
eps = sp.Symbol('epsilon')


def radial_lap(f, r=rr):
    return sp.diff(r ** 2 * sp.diff(f, r), r) / r ** 2


def route_A(K):
    """Route A: the nonlocal action at quadratic order, static, Newtonian gauge.
    Returns a dict of closed-form point-mass results with m_static = K*m."""
    ms = K * msym
    X, Y, Z, T = sp.symbols('x y z t', real=True)
    PhiF = sp.Function('Phi')(X, Y, Z)
    PsiF = sp.Function('Psi')(X, Y, Z)
    rhoF = sp.Function('rho')(X, Y, Z)
    gA = sp.diag(-(1 + 2 * eps * PhiF), 1 - 2 * eps * PsiF, 1 - 2 * eps * PsiF, 1 - 2 * eps * PsiF)
    RA = ricci_scalar(gA, (T, X, Y, Z))
    sqrtg = sp.sqrt((1 + 2 * eps * PhiF) * (1 - 2 * eps * PsiF) ** 3)
    R1 = sp.expand(sp.diff(RA, eps).subs(eps, 0))
    LEH2 = sp.expand(sp.diff(sqrtg * RA, eps, 2).subs(eps, 0) / 2)
    kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
    k2 = sp.Symbol('k2', positive=True)
    Pp, Qq, Rh = sp.symbols('Phat Psihat rhohat')
    Ew = sp.exp(sp.I * (kx * X + ky * Y + kz * Z))

    def to_fourier(expr):
        e = expr.subs({PhiF: Pp * Ew, PsiF: Qq * Ew, rhoF: Rh * Ew}).doit()
        e = sp.expand(sp.powsimp(sp.expand(e / Ew)))
        e = sp.expand(e.subs(kx ** 2, k2 - ky ** 2 - kz ** 2))
        return e

    # R^(1) = Lap F  with F = alpha Phi + beta Psi : found, not typed in
    R1h = to_fourier(R1)
    Fh = sp.expand(-R1h / k2)
    alpha = Fh.coeff(Pp)
    beta = Fh.coeff(Qq)
    F_ok = sp.simplify(Fh - alpha * Pp - beta * Qq) == 0 and not (alpha.has(k2) or beta.has(k2))
    Fexpr = alpha * PhiF + beta * PsiF
    # static box^-1 = Lap^-1 ; int R1 Lap^-4 R1 = int F^2 (decaying fields)
    L2 = (LEH2 - (ms ** 2 / 6) * Fexpr ** 2) / (16 * sp.pi * Gs) - rhoF * PhiF
    ELs = sp.euler_equations(L2, [PhiF, PsiF], [X, Y, Z])
    eqs = [to_fourier(e.lhs) for e in ELs]
    sol = sp.solve(eqs, [Pp, Qq], dict=True)[0]
    Phat = sp.factor(sp.simplify(sol[Pp] / Rh))
    Qhat = sp.factor(sp.simplify(sol[Qq] / Rh))

    def inv_ft_point(expr_k):
        """position space (r > 0) of expr_k * M for a point mass rho_hat = M.
        table: 1/k2 -> 1/(4 pi r);  1/(k2 - ms^2) -> cos(ms r)/(4 pi r) (standing wave, declared).
        Returns (function of r, list of terms, {'c0': coefficient of 1/k2, 'cm': coefficient of 1/(k2-ms^2)})."""
        out = sp.S.Zero
        terms = []
        coef = {'c0': sp.S.Zero, 'cm': sp.S.Zero, 'contact': sp.S.Zero}
        for term in sp.Add.make_args(sp.apart(sp.together(expr_k), k2)):
            num, den = sp.fraction(sp.together(term))
            if not den.has(k2):
                terms.append(('contact', str(term)))
                coef['contact'] += term
                continue
            pden = sp.Poly(den, k2)
            if pden.degree() != 1:
                raise RuntimeError('unexpected pole structure: %s' % term)
            d1, d0 = pden.all_coeffs()
            pole = sp.simplify(-d0 / d1)
            c = sp.simplify(num / d1)
            if pole == 0:
                out += c * Msym / (4 * sp.pi * rr)
                terms.append(('1/k2', str(c)))
                coef['c0'] += c
            elif sp.simplify(pole - ms ** 2) == 0:
                out += c * Msym * sp.cos(ms * rr) / (4 * sp.pi * rr)
                terms.append(('1/(k2-ms^2)', str(c)))
                coef['cm'] += c
            else:
                raise RuntimeError('unexpected pole at k2 = %s' % pole)
        return sp.simplify(out), terms, coef

    Phi_r, Phi_terms, Phi_coef = inv_ft_point(Phat)
    Psi_r, Psi_terms, Psi_coef = inv_ft_point(Qhat)
    # table checks: Green functions and their delta normalisation (flux through a small sphere)
    G0 = 1 / (4 * sp.pi * rr)
    Gm = sp.cos(ms * rr) / (4 * sp.pi * rr)
    tab_ok = (sp.simplify(radial_lap(G0)) == 0
              and sp.simplify(radial_lap(Gm) + ms ** 2 * Gm) == 0
              and sp.limit(-4 * sp.pi * rr ** 2 * sp.diff(G0, rr), rr, 0) == 1
              and sp.limit(-4 * sp.pi * rr ** 2 * sp.diff(Gm, rr), rr, 0) == 1)
    PhiN = -Gs * Msym / rr
    # CFG123's definition: rho_eff = (1/4 pi G r^2) d/dr [ r^2 (g_tot - g_N) ], g = dPhi/dr (inward +)
    rho_eff = sp.simplify(sp.diff(rr ** 2 * (sp.diff(Phi_r, rr) - sp.diff(PhiN, rr)), rr)
                          / (4 * sp.pi * Gs * rr ** 2))
    c1_exact_factor = sp.simplify(rho_eff / (ms ** 2 * Msym / (4 * sp.pi * rr)))
    c1 = sp.limit(c1_exact_factor, msym, 0)
    U_r = sp.simplify(-(alpha * Phi_r + beta * Psi_r))       # U = -Lap^-1 R1 = -F (decaying)
    rho_eff_LO = sp.simplify(sp.series(rho_eff, msym, 0, 3).removeO())
    dPhi_r = sp.simplify(sp.diff(Phi_r, rr))
    return dict(K=K, ms=ms, R1=R1, alpha=alpha, beta=beta, F_ok=F_ok, LEH2=LEH2,
                Phat=Phat, Qhat=Qhat, Phi_terms=Phi_terms, Psi_terms=Psi_terms,
                Phi_coef=Phi_coef, Psi_coef=Psi_coef, dPhi=dPhi_r,
                Phi=Phi_r, Psi=Psi_r, U=U_r, rho_eff=rho_eff, rho_eff_LO=rho_eff_LO,
                c1=c1, c1_exact_factor=c1_exact_factor, tab_ok=tab_ok)


banner('Route A: nonlocal RR action at quadratic order (static, Newtonian gauge), point mass')
tA = time.time()
A_res = route_A(K_PLANT)
ms_sym = A_res['ms']
P('  R^(1) =', A_res['R1'])
P('  found: R^(1) = Lap F with F = (%s) Phi + (%s) Psi ; F derivation consistent: %s'
  % (A_res['alpha'], A_res['beta'], A_res['F_ok']))
P('  Phi_hat/rho_hat =', A_res['Phat'])
P('  Psi_hat/rho_hat =', A_res['Qhat'])
P('  pole terms Phi:', A_res['Phi_terms'], '  Psi:', A_res['Psi_terms'])
P('  Green-function table checks (Lap, Lap+m^2, delta normalisation):', A_res['tab_ok'])
P('  Phi(r) =', A_res['Phi'])
P('  Psi(r) =', A_res['Psi'])
P('  U(r)   =', A_res['U'])
P('  rho_eff(r) (CFG123 definition) =', A_res['rho_eff'])
P('  rho_eff / (m_s^2 M / 4 pi r) =', A_res['c1_exact_factor'], '  ->  c1 =', A_res['c1'])
P('  leading order in m: rho_eff =', A_res['rho_eff_LO'])
P('  route A time %.1f s' % (time.time() - tA))
RES['routeA'] = {k: str(A_res[k]) for k in ('R1', 'alpha', 'beta', 'Phat', 'Qhat', 'Phi', 'Psi', 'U',
                                             'rho_eff', 'c1', 'c1_exact_factor', 'rho_eff_LO')}
RES['routeA']['F_ok'] = bool(A_res['F_ok'])
RES['routeA']['green_table_ok'] = bool(A_res['tab_ok'])

# ---------------------------------------------------------------------------------------------
banner('Route B: one-multiplier localised action, Weyl-reduced on -A dt^2 + B dr^2 + C r^2 dOmega^2')
tB = time.time()
th, vph, tt = sp.symbols('theta varphi t_B')
Af, Bf, Cf, Uf, lf, rhof = [sp.Function(nm)(rr) for nm in ('A', 'B', 'C', 'U', 'lam', 'rhoB')]
gB = sp.diag(-Af, Bf, Cf * rr ** 2, Cf * rr ** 2 * sp.sin(th) ** 2)
RB = sp.simplify(ricci_scalar(gB, (tt, rr, th, vph)))
RB_theta_free = sp.simplify(sp.diff(RB, th)) == 0
LB = (sp.sqrt(Af * Bf) * Cf * rr ** 2 * ((1 - lf) * RB - (ms_sym ** 2 / 6) * Uf ** 2
                                          + sp.diff(lf, rr) * sp.diff(Uf, rr) / Bf) / (16 * sp.pi * Gs)
      - rhof * rr ** 2 * sp.sqrt(Af))
ELB = sp.euler_equations(LB, [Af, Bf, Cf, Uf, lf], rr)
names = ['E_A', 'E_B', 'E_C', 'E_U', 'E_lam']
af_, bf_, uf_, lf_, rho1 = [sp.Function(nm)(rr) for nm in ('a', 'b', 'u', 'l', 'rho1')]


def linearise(e):
    e = e.subs(Cf, 1).doit()
    e = e.subs({Af: 1 + eps * af_, Bf: 1 + eps * bf_, Uf: eps * uf_, lf: eps * lf_,
                rhof: eps * rho1}).doit()
    e0 = sp.simplify(e.subs(eps, 0))
    e1 = sp.simplify(sp.expand(sp.diff(e, eps).subs(eps, 0)))
    return e0, e1


LIN = {}
zeroth_ok = True
for nm, e in zip(names, ELB):
    e0, e1 = linearise(e.lhs)
    zeroth_ok = zeroth_ok and (e0 == 0)
    LIN[nm] = e1
    P('  %-6s linear: %s' % (nm, e1))
P('  Ricci scalar theta-free:', RB_theta_free, '   zeroth order vanishes (flat, U = lam = 0):', zeroth_ok)
# a constant in lam must drop out of every linear equation
c0 = sp.Symbol('c_0')
lam_const_ok = all(sp.simplify(LIN[nm].subs(lf_, lf_ + c0).doit() - LIN[nm]) == 0 for nm in names)
P('  a constant added to lam drops out of all five linear equations:', lam_const_ok)
# R^(1) in the areal gauge and the first integral r^2 R1 = (r^2 X)'
RB1 = sp.simplify(sp.diff(RB.subs(Cf, 1).doit().subs({Af: 1 + eps * af_, Bf: 1 + eps * bf_}).doit(), eps)
                  .subs(eps, 0))
lap_u = radial_lap(uf_)
ratio_El = sp.simplify(LIN['E_lam'] / (rr ** 2 * (RB1 + lap_u)))
El_is_constraint = not ratio_El.has(rr) and not ratio_El.has(af_) and not ratio_El.has(uf_)
P('  R^(1) (areal) =', RB1)
P('  E_lam / [r^2 (R^(1) + Lap u)] =', ratio_El, ' (constant => E_lam is Box U = -R):', El_is_constraint)
pX = sp.symbols('p1:6')
Xans = (pX[0] * sp.diff(af_, rr) + pX[1] * bf_ / rr + pX[2] * af_ / rr + pX[3] * sp.diff(bf_, rr)
        + pX[4] * sp.diff(af_, rr, 2) * rr)
resX = sp.expand(sp.diff(rr ** 2 * Xans, rr) - rr ** 2 * RB1)
dsyms = sp.symbols('A0 A1 A2 A3 B0 B1 B2 B3')
rep = [(sp.diff(af_, rr, 3), dsyms[3]), (sp.diff(bf_, rr, 3), dsyms[7]), (sp.diff(af_, rr, 2), dsyms[2]),
       (sp.diff(bf_, rr, 2), dsyms[6]), (sp.diff(af_, rr), dsyms[1]), (sp.diff(bf_, rr), dsyms[5]),
       (af_, dsyms[0]), (bf_, dsyms[4])]
resX_s = sp.expand(resX.subs(rep))
eqX = [sp.expand(resX_s.coeff(ds)) for ds in dsyms]
eqX = [c for e_ in eqX for c in sp.Poly(sp.expand(e_ * rr ** 4), rr).coeffs()] if eqX else []
solX = sp.solve(eqX, pX, dict=True)
Xsol = sp.simplify(Xans.subs(solX[0]).subs({p: 0 for p in pX})) if solX else None
X_ok = bool(solX) and sp.simplify(sp.diff(rr ** 2 * Xsol, rr) - rr ** 2 * RB1) == 0
P('  first integral: X =', Xsol, '  (r^2 X)\' = r^2 R^(1):', X_ok)

# order-by-order point-mass solution in m_s^2 (vacuum r > 0; no new 1/r term beyond GR's mass)
rS = sp.Symbol('r_S', positive=True)
bm1, mum1 = sp.symbols('beta_m1 mu_m1')
al = sp.symbols('alpha0:3')
be = sp.symbols('beta0:3')
mu_ = sp.symbols('mu0:3')
la = sp.symbols('lam0:3')
unknowns = [bm1, mum1, *al, *be, *mu_, *la]
ms2 = ms_sym ** 2
a_ans = -rS / rr + ms2 * rS * (al[2] * rr ** 2 + al[1] * rr + al[0])
b_ans = bm1 / rr + ms2 * rS * (be[2] * rr ** 2 + be[1] * rr + be[0])
u_ans = mum1 / rr + ms2 * rS * (mu_[2] * rr ** 2 + mu_[1] * rr + mu_[0])
l_ans = ms2 * rS * (la[2] * rr ** 2 + la[1] * rr + la[0])
subsB = {af_: a_ans, bf_: b_ans, uf_: u_ans, lf_: l_ans, rho1: 0}
eq_list = []
for nm in names + ['flux']:
    ex = (sp.diff(uf_, rr) + Xsol) if nm == 'flux' else LIN[nm]
    ex = sp.expand(ex.subs(subsB).doit())
    for pw in (0, 1, 2):        # the ansatz is exact through O(m^2); O(m^4) terms are dropped
        cm = sp.expand(ex.coeff(msym, pw))
        if cm == 0:
            continue
        cm = sp.expand(sp.simplify(cm * rr ** 6))
        for cc in sp.Poly(cm, rr).coeffs():
            eq_list.append(sp.expand(cc))
solB = sp.solve(eq_list, unknowns, dict=True)
P('  order-by-order solve: %d equations, %d unknowns, %d solution(s)' % (len(eq_list), len(unknowns), len(solB)))
solB0 = solB[0] if solB else {}
for k_ in unknowns:
    P('     %-8s = %s' % (k_, solB0.get(k_, '(free)')))
alpha1_B = solB0.get(al[1], None)
c1_B = sp.simplify(2 * alpha1_B) if alpha1_B is not None else None
P('  route B: A = 1 + a, a_2 = alpha1 m_s^2 r_S r  =>  c1 = 2 alpha1 =', c1_B)
RES['routeB'] = {'linear_equations': {nm: str(LIN[nm]) for nm in names},
                 'zeroth_order_vanishes': bool(zeroth_ok), 'R_theta_free': bool(RB_theta_free),
                 'lam_constant_drops_out': bool(lam_const_ok), 'E_lam_is_constraint': bool(El_is_constraint),
                 'first_integral_X': str(Xsol), 'X_ok': bool(X_ok),
                 'order_by_order_solution': {str(k_): str(solB0.get(k_, 'free')) for k_ in unknowns},
                 'c1': str(c1_B)}

# substitute route A's exact solution (mapped to the areal radius at linear order) into route B
s_ = sp.Symbol('s', positive=True)
PhiA, PsiA, UA = A_res['Phi'], A_res['Psi'], A_res['U']
a_ex = 2 * PhiA
b_ex = sp.simplify(2 * rr * sp.diff(PsiA, rr))
u_ex = UA
flux_l = sp.simplify(sp.integrate((u_ex * rr ** 2).subs(rr, s_), (s_, 0, rr)))
lp_ex = sp.simplify(-(ms_sym ** 2 / 3) * flux_l / rr ** 2)                  # l' with zero flux at the origin
l_ex = sp.simplify(sp.integrate(lp_ex, rr))
subs_ex = {af_: a_ex, bf_: b_ex, uf_: u_ex, lf_: l_ex, rho1: 0}
resid_ex = {}
for nm in names + ['flux']:
    ex = (sp.diff(uf_, rr) + Xsol) if nm == 'flux' else LIN[nm]
    resid_ex[nm] = sp.simplify(sp.expand(ex.subs(subs_ex).doit()))
sub_ok = all(v == 0 for v in resid_ex.values())
P('  route-A exact solution in route-B equations (r > 0): residuals', {k: str(v) for k, v in resid_ex.items()})
P('  lam(r) of that solution =', l_ex)
P('  route B time %.1f s' % (time.time() - tB))
RES['routeB']['exact_solution_residuals'] = {k: str(v) for k, v in resid_ex.items()}
RES['routeB']['lam_exact'] = str(l_ex)

# ---------------------------------------------------------------------------------------------
banner('C1-C3: GR limit, the literature static limit, and the two routes')
Phi0 = sp.simplify(PhiA.subs(msym, 0))
Psi0 = sp.simplify(PsiA.subs(msym, 0))
rho0 = sp.simplify(A_res['rho_eff'].subs(msym, 0))
GRB = (solB0.get(bm1) == rS) if solB else False
check('C1 GR limit',
      sp.simplify(Phi0 + Gs * Msym / rr) == 0 and sp.simplify(Psi0 + Gs * Msym / rr) == 0 and rho0 == 0 and GRB,
      'm=0: Phi=%s, Psi=%s, rho_eff=%s; route B O(m^0): b = %s/r (GR areal: r_S/r)' % (Phi0, Psi0, rho0, solB0.get(bm1)))
# literature: Kehagias-Maggiore (4.31)-(4.33), areal gauge, r_S = 2GM; Maggiore-Mancarella small-mr statement
rS_GM = 2 * Gs * Msym
A_mine = 1 + 2 * PhiA
B_mine = 1 + b_ex
A_KM = 1 - (rS_GM / rr) * (1 + (1 - sp.cos(ms_sym * rr)) / 3)
B_KM = 1 + (rS_GM / rr) * (1 - (1 - sp.cos(ms_sym * rr)) / 3 + ms_sym * rr * sp.sin(ms_sym * rr) / 3)
U_KM = (rS_GM / rr) * sp.cos(ms_sym * rr)
dA = sp.simplify(A_mine - A_KM)
dB = sp.simplify(B_mine - B_KM)
dU = sp.simplify(UA - U_KM)
serA = sp.simplify(sp.series(A_mine, msym, 0, 3).removeO())
MM_A = 1 - (rS_GM / rr) * (1 + ms_sym ** 2 * rr ** 2 / 6)
dMM_A = sp.simplify(serA - MM_A)
dMM_B = sp.simplify(sp.series(A_mine + B_mine - 2, msym, 0, 3).removeO())
coef_rel = sp.simplify(sp.series((A_mine - 1) / (-(rS_GM / rr)) - 1, msym, 0, 3).removeO() / (ms_sym * rr) ** 2)
check('C2 literature static limit',
      dA == 0 and dB == 0 and dU == 0 and dMM_A == 0 and dMM_B == 0,
      'mine - KM(4.31-4.33): dA=%s dB=%s dU=%s; series vs MM A=1-(rS/r)(1+m^2r^2/6): %s; A+B-2 at O(m^2): %s; '
      'relative (mr)^2 coefficient of the potential = %s' % (dA, dB, dU, dMM_A, dMM_B, coef_rel))
# C3: routes A and B agree at linear order (g_tt and g_rr), exact form and order by order
A_ser = sp.expand(sp.series(A_mine, msym, 0, 3).removeO())
B_ser = sp.expand(sp.series(B_mine, msym, 0, 3).removeO())
aB = sp.expand(a_ans.subs(solB0).subs({al[0]: 0}).subs(rS, rS_GM))
bB = sp.expand(b_ans.subs(solB0).subs(rS, rS_GM))
dAB = sp.simplify(A_ser - 1 - aB)
dBB = sp.simplify(B_ser - 1 - bB)
check('C3 two routes',
      sub_ok and dAB == 0 and dBB == 0 and X_ok and El_is_constraint and lam_const_ok and zeroth_ok,
      'route-A exact solution solves all five route-B equations + flux: %s; O(m^2) g_tt diff %s, g_rr diff %s; '
      'c1 route A = %s, route B = %s' % (sub_ok, dAB, dBB, A_res['c1'], c1_B))
RES['c1_routeA'] = str(A_res['c1'])
RES['c1_routeB'] = str(c1_B)

# ---------------------------------------------------------------------------------------------
banner('Background: minisuperspace of the same one-multiplier action (units H0 = 1, 8 pi G/3 = 1)')
tC = time.time()
tb = sp.Symbol('t')
Nf, aF, UF, LF = [sp.Function(nm)(tb) for nm in ('N', 'a', 'Ub', 'lamb')]
gF = sp.diag(-Nf ** 2, aF ** 2, aF ** 2, aF ** 2)
RFm = ricci_scalar(gF, (tb,) + sp.symbols('z1:4'))
Om, Orad, OL, mu = sp.symbols('Omega_m Omega_r Omega_L mu', positive=True)
Lmini = (Nf * aF ** 3 * ((1 - LF) * RFm - (mu ** 2 / 6) * UF ** 2 - sp.diff(LF, tb) * sp.diff(UF, tb) / Nf ** 2) / 6
         - Nf * aF ** 3 * (Om * aF ** -3 + Orad * aF ** -4 + OL))
ELm = sp.euler_equations(Lmini, [Nf, aF, UF, LF], tb)
Hs, zeta, Asym = sp.symbols('H zeta A_sc', positive=True)
U0, U1, U2, L0, L1, L2 = sp.symbols('U0 U1 U2 L0 L1 L2')


def to_x(e):
    e = e.subs(Nf, 1).doit()
    e = e.subs({sp.diff(aF, tb, 2): Asym * Hs ** 2 * (1 + zeta), sp.diff(UF, tb, 2): Hs ** 2 * (U2 + zeta * U1),
                sp.diff(LF, tb, 2): Hs ** 2 * (L2 + zeta * L1)})
    e = e.subs({sp.diff(aF, tb): Asym * Hs, sp.diff(UF, tb): Hs * U1, sp.diff(LF, tb): Hs * L1})
    e = e.subs({aF: Asym, UF: U0, LF: L0})
    return sp.simplify(e)


EN, Ea, EU_, EL_ = [to_x(e.lhs) for e in ELm]
H2s_ = sp.Symbol('H2')
EN_H2 = sp.expand(EN).subs(Hs ** 2, H2s_)
assert not EN_H2.has(Hs), 'constraint is not a function of H^2 alone'
H2sol = sp.solve(EN_H2, H2s_)
H2expr = sp.simplify(H2sol[0])
P('  Friedmann constraint (from N):  H^2 =', H2expr)
# the three dynamical equations -> (zeta, U2, L2)
dyn = sp.solve([EU_, EL_, Ea], [zeta, U2, L2], dict=True)
P('  dynamical solve count:', len(dyn))
zeta_e = sp.simplify(dyn[0][zeta])
U2_e = sp.simplify(dyn[0][U2])
L2_e = sp.simplify(dyn[0][L2])
P('  U-equation (vary lam): ', sp.simplify(EL_), ' = 0')
P('  lam-equation (vary U): ', sp.simplify(EU_), ' = 0')
# C4: the published equations
W0, W1, h2s = sp.symbols('W0 W1 h2', positive=True)
gam = mu ** 2 / 9
Y_MM = sp.Rational(1, 2) * W1 * (6 - U1) + W0 * (3 - 6 * zeta + zeta * U1) + sp.Rational(1, 4) * U0 ** 2
mine_c = (Hs ** 2 * (1 - L0 - L1 + L1 * U1 / 6) - (Om * Asym ** -3 + Orad * Asym ** -4 + OL + mu ** 2 * U0 ** 2 / 36))
EN_over = sp.simplify(EN / mine_c)
mine_c_W = mine_c.subs({L0: (mu ** 2 / 3) * W0 / h2s, L1: (mu ** 2 / 3) * (W1 - 2 * zeta * W0) / h2s}).subs(Hs, sp.sqrt(h2s))
MM_c = h2s - (Om * Asym ** -3 + Orad * Asym ** -4 + OL) - gam * Y_MM
dC4a = sp.simplify(sp.expand(mine_c_W - MM_c))
# U equation and W equation vs Maggiore-Mancarella
xs_ = sp.Symbol('x')
Wf = sp.Function('W')(xs_)
hf = sp.Function('h')(xs_)
Uxf = sp.Function('Ux')(xs_)
lam_of_W = (mu ** 2 / 3) * Wf / hf ** 2
# my lam equation in x-form: take EU_ and replace L0..L2, U0, H, zeta by functions of x
EU_x = EU_.subs({L2: sp.diff(lam_of_W, xs_, 2), L1: sp.diff(lam_of_W, xs_), L0: lam_of_W, U0: Uxf,
                 Hs: hf, zeta: sp.diff(hf, xs_) / hf})
zet = sp.diff(hf, xs_) / hf
W_MM = sp.diff(Wf, xs_, 2) + 3 * (1 - zet) * sp.diff(Wf, xs_) - 2 * (sp.diff(zet, xs_) + 3 * zet - zet ** 2) * Wf - Uxf
ratioW = sp.simplify(EU_x / W_MM)
ratioU = sp.simplify(EL_ / (U2 + (3 + zeta) * U1 - 6 * (2 + zeta)))
C4_ok = (EN_over != 0 and EN_over.free_symbols <= {Asym} and dC4a == 0
         and ratioW != 0 and not ratioW.has(Wf) and not ratioW.has(Uxf) and not ratioW.has(hf)
         and ratioU != 0 and ratioU.free_symbols <= {Asym, Hs, mu})
check('C4 background equations = Maggiore-Mancarella',
      C4_ok,
      'my constraint / [H^2(1-l-l\'+l\'U\'/6) - (rho + mu^2 U^2/36)] = %s; mine - MM (h^2 = Om e^-3x + Or e^-4x + gamma Y) '
      '= %s; my lam-eqn / MM W-eqn = %s; my U-eqn / [U\'\'+(3+z)U\'-6(2+z)] = %s' % (EN_over, dC4a, ratioW, ratioU))
RES['background_equations'] = {'H2': str(H2expr), 'zeta': str(zeta_e), 'U2': str(U2_e), 'L2': str(L2_e),
                               'C4_ratios': [str(EN_over), str(dC4a), str(ratioW), str(ratioU)]}

# numerics
H0_SI = 67.36e3 / 3.0856775814913673e22
h_little = 0.6736
Om_v = 0.3153
Or_v = 4.15e-5 / h_little ** 2
fh2 = sp.lambdify((xs_, U0, U1, L0, L1, mu, Om, Orad, OL), H2expr.subs(Asym, sp.exp(xs_)), 'numpy')
fdyn = sp.lambdify((xs_, U0, U1, L0, L1, Hs, mu, Om, Orad, OL),
                   [zeta_e.subs(Asym, sp.exp(xs_)), U2_e.subs(Asym, sp.exp(xs_)), L2_e.subs(Asym, sp.exp(xs_))],
                   'numpy')
# constraint propagation: d(h^2)/dx along the flow vs 2 zeta h^2
h2_fun = H2expr.subs(Asym, sp.exp(xs_))
dh2 = (sp.diff(h2_fun, xs_) + U1 * sp.diff(h2_fun, U0) + U2 * sp.diff(h2_fun, U1)
       + L1 * sp.diff(h2_fun, L0) + L2 * sp.diff(h2_fun, L1))
fdh2 = sp.lambdify((xs_, U0, U1, L0, L1, U2, L2, mu, Om, Orad, OL), dh2, 'numpy')


def rhs(x, y, muv, OLv):
    U0v, U1v, L0v, L1v = y
    h2v = fh2(x, U0v, U1v, L0v, L1v, muv, Om_v, Or_v, OLv)
    z, u2, l2 = fdyn(x, U0v, U1v, L0v, L1v, np.sqrt(h2v), muv, Om_v, Or_v, OLv)
    return [U1v, u2, L1v, l2]


def integrate_bg(muv, OLv=0.0, xi=-18.0, dense=False):
    sol = solve_ivp(rhs, (xi, 0.0), [0.0, 0.0, 0.0, 0.0], method='DOP853', rtol=1e-11, atol=1e-14,
                    args=(muv, OLv), dense_output=dense)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def h2_today(muv, xi=-18.0):
    sol = integrate_bg(muv, 0.0, xi)
    y = sol.y[:, -1]
    return fh2(0.0, y[0], y[1], y[2], y[3], muv, Om_v, Or_v, 0.0)


def shoot(xi):
    return brentq(lambda mv: h2_today(mv, xi) - 1.0, 0.1, 0.5, xtol=1e-14, rtol=1e-13, maxiter=200)


mu_v = shoot(-18.0)
mu_15 = shoot(-15.0)
mu_21 = shoot(-21.0)
solbg = integrate_bg(mu_v, 0.0, -18.0, dense=True)
yend = solbg.y[:, -1]
Ubar0, U1bar0, lbar0, l1bar0 = yend
h2_0 = fh2(0.0, *yend, mu_v, Om_v, Or_v, 0.0)
z0, u20, l20 = fdyn(0.0, *yend, np.sqrt(h2_0), mu_v, Om_v, Or_v, 0.0)
OmDE0 = h2_0 - Om_v - Or_v
dOmDE0 = 2 * z0 * h2_0 + 3 * Om_v + 4 * Or_v
wDE0 = -1 - dOmDE0 / (3 * OmDE0)
S_bar0 = 3 * lbar0 / mu_v ** 2          # H0^2 S-bar (c = 1)
P('  inputs: H0 = 67.36 km/s/Mpc, Omega_m = %.4f, Omega_r = %.6e (Omega_r h^2 = 4.15e-5), no separate Lambda'
  % (Om_v, Or_v))
P('  shot: m/H0 = %.6f (x_i = -18);  x_i = -15: %.6f ; x_i = -21: %.6f' % (mu_v, mu_15, mu_21))
P('  today: h^2 = %.12f, U = %.5f, U\' = %.5f, lam = %.6f, lam\' = %.6f, H0^2 S = %.5f, zeta = %.6f, w_DE = %.5f'
  % (h2_0, Ubar0, U1bar0, lbar0, l1bar0, S_bar0, z0, wDE0))
# C5 (i) LCDM limit: nonlocal term off (mu = 0) with a constant Lambda
OL_v = 1 - Om_v - Or_v
sol_L = integrate_bg(0.0, OL_v, -18.0, dense=True)
maxdev_h = 0.0
maxdev_z = 0.0
for xv in np.linspace(-18.0, 0.0, 181):
    yv = sol_L.sol(xv)
    h2v = fh2(xv, *yv, 0.0, Om_v, Or_v, OL_v)
    zv = fdyn(xv, *yv, np.sqrt(h2v), 0.0, Om_v, Or_v, OL_v)[0]
    h2L = Om_v * np.exp(-3 * xv) + Or_v * np.exp(-4 * xv) + OL_v
    zL = (-3 * Om_v * np.exp(-3 * xv) - 4 * Or_v * np.exp(-4 * xv)) / (2 * h2L)
    maxdev_h = max(maxdev_h, abs(np.sqrt(h2v / h2L) - 1))
    maxdev_z = max(maxdev_z, abs(zv - zL) / max(abs(zL), 1e-300))
# C5 (ii) constraint propagation along the RR solution
maxprop = 0.0
for xv in np.linspace(-18.0, 0.0, 181):
    yv = solbg.sol(xv)
    h2v = fh2(xv, *yv, mu_v, Om_v, Or_v, 0.0)
    zv, u2v, l2v = fdyn(xv, *yv, np.sqrt(h2v), mu_v, Om_v, Or_v, 0.0)
    d1 = fdh2(xv, *yv, u2v, l2v, mu_v, Om_v, Or_v, 0.0)
    maxprop = max(maxprop, abs(d1 - 2 * zv * h2v) / abs(2 * zv * h2v))
dmu = max(abs(mu_15 / mu_v - 1), abs(mu_21 / mu_v - 1))
check('C5 integrator',
      maxdev_h < 1e-9 and maxdev_z < 1e-9 and maxprop < 1e-8 and dmu < 1e-4,
      'LCDM limit: max |h/h_LCDM - 1| = %.2e, max rel zeta dev = %.2e (line 1e-9); constraint propagation '
      'max rel = %.2e (line 1e-8); m/H0 change for x_i = -15/-21: %.2e (line 1e-4)' % (maxdev_h, maxdev_z, maxprop, dmu))
P('  background time %.1f s' % (time.time() - tC))
RES['background'] = {'m_over_H0': mu_v, 'm_over_H0_xi_m15': mu_15, 'm_over_H0_xi_m21': mu_21,
                     'U_bar_0': Ubar0, 'Uprime_0': U1bar0, 'lam_bar_0': lbar0, 'H0sq_S_bar_0': S_bar0,
                     'zeta_0': z0, 'w_DE_0': wDE0, 'h2_0': h2_0, 'Omega_r': Or_v,
                     'C5': {'lcdm_h': maxdev_h, 'lcdm_zeta': maxdev_z, 'propagation': maxprop, 'xi_sens': dmu}}

# ---------------------------------------------------------------------------------------------
banner('Target (own implementation of CFG44\'s point mass and exponential sphere) -- C6')
mpm.mp.dps = 50
G_SI = mpm.mpf('6.67430e-11')
GMSUN = mpm.mpf('1.32712440018e20')
C_SI = mpm.mpf('299792458')
KPC = mpm.mpf('3.0856775814913673e19')
MPC = KPC * 1000
H0m = mpm.mpf('67.36e3') / MPC
FOOT = {'canonical': mpm.mpf('9.3603e-11'), 'alt': mpm.mpf('1.1312e-10')}
XGRID = [mpm.mpf(s) for s in ('0.1', '0.2', '0.3', '0.5', '1', '2', '3', '5', '10', '20', '30')]
MGRID = [mpm.mpf(s) for s in ('1e9', '1e10', '1e11', '1e12')]


def r_M(GM, a0):
    return mpm.sqrt(GM / a0)


def rho_target_pm(r, GM, a0):
    x = r / r_M(GM, a0)
    return a0 / (4 * mpm.pi * G_SI * r * mpm.sqrt(1 + x ** 2))


def g_P2(r, GM, a0):
    gN = GM / r ** 2
    return mpm.sqrt(gN ** 2 + a0 * gN)


def Mc_closed(r, GM, a0):
    x = r / r_M(GM, a0)
    return (GM / G_SI) * (mpm.sqrt(1 + x ** 2) - 1)


def rho_from_cold_mass(r, GM, a0):
    # independent form: (d M_c/dr)/(4 pi r^2) with M_c = M(sqrt(1+x^2)-1)
    rM = r_M(GM, a0)
    x = r / rM
    return (GM / G_SI) * x / (mpm.sqrt(1 + x ** 2) * rM * 4 * mpm.pi * r ** 2)


def comparator(rho_eff, r, GM, a0):
    return rho_eff / rho_target_pm(r, GM, a0)


worst_id = 0
worst_quad = 0
worst_g = 0
worst_cmp = 0
for a0 in FOOT.values():
    for n in MGRID:
        GM = n * GMSUN
        for x in XGRID:
            r = x * r_M(GM, a0)
            C_t = rho_target_pm(r, GM, a0) * r ** 3 * g_P2(r, GM, a0)
            worst_id = max(worst_id, abs(C_t / (a0 / (4 * mpm.pi) * (GM / G_SI)) - 1))
            q = mpm.quad(lambda rp: 4 * mpm.pi * rp ** 2 * rho_target_pm(rp, GM, a0), [0, r])
            worst_quad = max(worst_quad, abs(q / Mc_closed(r, GM, a0) - 1))
            gm = G_SI * ((GM / G_SI) + Mc_closed(r, GM, a0)) / r ** 2
            worst_g = max(worst_g, abs(gm / g_P2(r, GM, a0) - 1))
            worst_cmp = max(worst_cmp, abs(comparator(rho_from_cold_mass(r, GM, a0), r, GM, a0) - 1))
# exponential sphere enclosed mass vs quadrature
h_sph = 2 * KPC
worst_sph = 0
for n in MGRID:
    Mkg = n * GMSUN / G_SI
    rho0 = Mkg / (8 * mpm.pi * h_sph ** 3)
    for rv in (mpm.mpf('0.1') * KPC, KPC, 5 * KPC, 50 * KPC):
        s = rv / h_sph
        Mcl = Mkg * (1 - (1 + s + s ** 2 / 2) * mpm.e ** (-s))
        Mq = mpm.quad(lambda rp: 4 * mpm.pi * rp ** 2 * rho0 * mpm.e ** (-rp / h_sph), [0, rv])
        worst_sph = max(worst_sph, abs(Mq / Mcl - 1))
check('C6 target identity',
      worst_id < 1e-12 and worst_quad < 1e-8 and worst_g < 1e-12 and worst_sph < 1e-10 and worst_cmp < 1e-12,
      'rho_c r^3 g_P2 vs (a0/4pi)M: %s; quadrature of M_c: %s; g_P2 = G(M+M_c)/r^2: %s; sphere M(<r): %s; '
      'comparator fed the cold-mass density: |R-1| = %s' % (f2s(worst_id, 3), f2s(worst_quad, 3), f2s(worst_g, 3),
                                                          f2s(worst_sph, 3), f2s(worst_cmp, 3)))

# ---------------------------------------------------------------------------------------------
banner('The ratio R_A = rho_eff / rho_target on the grid (point mass, exact linear rho_eff)')
m_bg = mpm.mpf(mu_v) * H0m / C_SI          # background-fixed m (1/m)
rho_eff_f = sp.lambdify((rr, Gs, Msym, msym), A_res['rho_eff'], 'mpmath')
Phi_f = sp.lambdify((rr, Gs, Msym, msym), A_res['Phi'], 'mpmath')
P('  m = (m/H0) H0/c = %s 1/m ; 1/m = %s Mpc ; m_static = %d m' % (f2s(m_bg, 8), f2s(1 / m_bg / MPC, 6), K_PLANT))


def RA_grid(rho_f, m_val):
    tab = {}
    for fn, a0 in FOOT.items():
        for n in MGRID:
            GM = n * GMSUN
            for x in XGRID:
                r = x * r_M(GM, a0)
                reff = rho_f(r, G_SI, GM / G_SI, m_val)
                tab[(fn, n, x)] = reff / rho_target_pm(r, GM, a0)
    return tab


RA = RA_grid(rho_eff_f, m_bg)
maxmr = max(K_PLANT * m_bg * x * r_M(n * GMSUN, a0) for a0 in FOOT.values() for n in MGRID for x in XGRID)
P('  max m_static r on the grid = %s' % f2s(maxmr, 6))
for fn in FOOT:
    P('  footing %s: log10|R_A| (rows M_b, columns x)' % fn)
    P('      M_b   ' + ' '.join('%8s' % f2s(x, 3) for x in XGRID))
    for n in MGRID:
        P('    %6s  ' % f2s(n, 2) + ' '.join('%8.3f' % float(mpm.log10(abs(RA[(fn, n, x)]))) for x in XGRID))
# definition check: rho_eff from g_tt by CFG123's formula, numerically at 50 digits:
# delta g = dPhi/dr - GM/r^2 is a difference at 50 digits (delta g/g_N <= 1e-9), then d/dr[r^2 delta g]
dPhi_f = sp.lambdify((rr, Gs, Msym, msym), A_res['dPhi'], 'mpmath')
worst_def = 0
for fn, a0 in FOOT.items():
    for n in (MGRID[0], MGRID[-1]):
        GM = n * GMSUN
        for x in (XGRID[0], XGRID[5], XGRID[-1]):
            r = x * r_M(GM, a0)
            Mkg = GM / G_SI
            dg = lambda rv: dPhi_f(rv, G_SI, Mkg, m_bg) - GM / rv ** 2
            num = mpm.diff(lambda rv: rv ** 2 * dg(rv), r) / (4 * mpm.pi * G_SI * r ** 2)
            worst_def = max(worst_def, abs(num / rho_eff_f(r, G_SI, Mkg, m_bg) - 1))
P('  numerical CFG123-definition rho_eff (mpmath 50 digits, from g_tt) vs closed form: max rel dev = %s'
  % f2s(worst_def, 3))
RES['definition_numeric_dev'] = float(worst_def)

# H1
CFG123 = {('canonical', 'min'): mpm.mpf('2.0e-15'), ('canonical', 'max'): mpm.mpf('6.1e-11'),
          ('alt', 'min'): mpm.mpf('1.7e-15'), ('alt', 'max'): mpm.mpf('5.0e-11')}
PIN = {'min': (MGRID[0], XGRID[0]), 'max': (MGRID[-1], XGRID[-1])}
h1_rows = []
h1_ok = True
corner_ok = True
for fn in FOOT:
    vals = {k: abs(v) for k, v in RA.items() if k[0] == fn}
    kmin = min(vals, key=vals.get)
    kmax = max(vals, key=vals.get)
    corner_ok = corner_ok and (kmin[1:] == PIN['min']) and (kmax[1:] == PIN['max'])
    for which in ('min', 'max'):
        n, x = PIN[which]
        mine = abs(RA[(fn, n, x)])
        ref = CFG123[(fn, which)]
        d = abs(mpm.log10(mine) - mpm.log10(ref))
        ok = d <= mpm.mpf('0.5')
        h1_ok = h1_ok and ok
        h1_rows.append({'footing': fn, 'point': which, 'M_b': float(n), 'x': float(x),
                        'r_kpc': float(x * r_M(n * GMSUN, FOOT[fn]) / KPC), 'mine': float(mine),
                        'CFG123': float(ref), 'dex': float(d), 'within_0p5': bool(ok)})
        P('  H1 %-9s %s (M_b=%s, x=%s, r=%s kpc): mine |R_A| = %s ; CFG123 %s ; |d log10| = %.4f dex'
          % (fn, which, f2s(n, 2), f2s(x, 3), f2s(x * r_M(n * GMSUN, FOOT[fn]) / KPC, 5), f2s(mine, 6),
             f2s(ref, 2), float(d)))
shortfall = 1 / abs(RA[('canonical', MGRID[-1], XGRID[-1])])
P('  canonical shortfall at (1e12, x = 30) = %s (log10 = %.3f); CFG123: 1.65e10' % (f2s(shortfall, 6),
                                                                                   float(mpm.log10(shortfall))))
H1 = check('H1 headline (four pinned points within 0.5 dex; extremes at the pinned corners)',
           h1_ok and corner_ok, 'within 0.5 dex at all four: %s; my grid extremes at (1e9, 0.1) and (1e12, 30): %s'
           % (h1_ok, corner_ok))
RES['H1'] = {'pass': bool(h1_ok and corner_ok), 'rows': h1_rows, 'corners_ok': bool(corner_ok),
             'shortfall_canonical': float(shortfall)}
RES['grid_log10_RA'] = {fn: {f2s(n, 2): [float(mpm.log10(abs(RA[(fn, n, x)]))) for x in XGRID] for n in MGRID}
                        for fn in FOOT}

# ---------------------------------------------------------------------------------------------
banner('Reported rows R1-R3 and E1 (not gates)')


def round2(v):
    return mpm.nstr(v, 2, min_fixed=0, max_fixed=0)


digits = []
for row in h1_rows:
    mine2 = round2(mpm.mpf(row['mine']))
    ref2 = round2(mpm.mpf(row['CFG123']))
    digits.append((row['footing'], row['point'], mine2, ref2, mine2 == ref2))
P('  R1 digits (my value to 2 figures vs CFG123 printed):', digits)
P('  R1 shortfall to 3 figures: %s vs 1.65e10' % mpm.nstr(shortfall, 3))
signs = set(mpm.sign(v) for v in RA.values())
P('  R1 c1 = %s (route A), %s (route B); sign of rho_eff on the grid: %s (CFG123: negative everywhere)'
  % (A_res['c1'], c1_B, 'all negative' if signs == {-1} else signs))
spreadS = {}
spreadM = {}
for fn in FOOT:
    for n in MGRID:
        vv = [abs(RA[(fn, n, x)]) for x in XGRID]
        spreadS[(fn, n)] = max(vv) / min(vv)
    for x in XGRID:
        vv = [abs(RA[(fn, n, x)]) for n in MGRID]
        spreadM[(fn, x)] = max(vv) / min(vv)
P('  R1 G1-S spread over x (point mass): %s .. %s (CFG123: 29.87)'
  % (f2s(min(spreadS.values()), 6), f2s(max(spreadS.values()), 6)))
P('  R1 G1-M spread over M_b: %s .. %s (CFG123: 1000)'
  % (f2s(min(spreadM.values()), 8), f2s(max(spreadM.values()), 8)))
# m_req at x = 0.1: exact linear and leading order
mreq = {}
rho_LO_f = sp.lambdify((rr, Gs, Msym, msym), A_res['rho_eff_LO'], 'mpmath')
for n in MGRID:
    GM = n * GMSUN
    a0 = FOOT['canonical']
    r = XGRID[0] * r_M(GM, a0)
    fLO = lambda mv: abs(rho_LO_f(r, G_SI, GM / G_SI, mv / K_PLANT) / rho_target_pm(r, GM, a0)) - 1
    fEX = lambda mv: abs(rho_eff_f(r, G_SI, GM / G_SI, mv / K_PLANT) / rho_target_pm(r, GM, a0)) - 1
    m_guess = mpm.sqrt(3 * a0 / (GM * mpm.sqrt(mpm.mpf('1.01'))))
    mLO = mpm.findroot(fLO, m_guess)
    mEX = mpm.findroot(fEX, m_guess)
    mreq[f2s(n, 2)] = {'LO_over_H0c': float(mLO * C_SI / H0m), 'exact_over_H0c': float(mEX * C_SI / H0m),
                       'LO_inv_rM': float(1 / (mLO * r_M(GM, a0))), 'exact_inv_rM': float(1 / (mEX * r_M(GM, a0)))}
_mr = list(mreq.values())
P('  R1 m_req at x = 0.1 (canonical), in units of H0/c (1e9 .. 1e12): leading order %s .. %s ; exact linear %s .. %s'
  % (f2s(_mr[0]['LO_over_H0c'], 4), f2s(_mr[-1]['LO_over_H0c'], 4), f2s(_mr[0]['exact_over_H0c'], 4),
     f2s(_mr[-1]['exact_over_H0c'], 4)))
P('     1/m_req = %s r_M (leading order) and %s r_M (exact linear); CFG123: 0.5788 r_M, 6.3e6 .. 2.0e5'
  % (f2s(list(mreq.values())[0]['LO_inv_rM'], 5), f2s(list(mreq.values())[0]['exact_inv_rM'], 5)))
RES['rows']['R1'] = {'digits': [list(d) for d in digits], 'shortfall_3fig': mpm.nstr(shortfall, 3),
                     'c1_A': str(A_res['c1']), 'c1_B': str(c1_B), 'all_negative': signs == {-1},
                     'G1S_spread': [float(min(spreadS.values())), float(max(spreadS.values()))],
                     'G1M_spread': [float(min(spreadM.values())), float(max(spreadM.values()))], 'm_req': mreq}
# R2 background
P('  R2 m/H0 = %.5f vs CFG123 0.2839 (rel %.2e; line 0.5%%) ; vs literature 0.283 (rel %.2e; sanity)'
  % (mu_v, mu_v / 0.2839 - 1, mu_v / 0.283 - 1))
P('  R2 U-bar(0) = %.4f vs 16.0 ; H0^2 S-bar(0) = %.4f vs 2.06 ; w_DE(0) = %.4f vs -1.146 (literature w0 -1.144)'
  % (Ubar0, S_bar0, wDE0))
RES['rows']['R2'] = {'m_over_H0': mu_v, 'rel_vs_0p2839': mu_v / 0.2839 - 1, 'within_0p5pct': abs(mu_v / 0.2839 - 1) < 0.005,
                     'rel_vs_lit_0p283': mu_v / 0.283 - 1, 'U_bar_0': Ubar0, 'H0sq_S_bar_0': S_bar0, 'w_DE_0': wDE0}
# R3 exponential sphere, h = 2 kpc, canonical.  Route A's Fourier solution for a general source:
#   Phi = c0 I_0 + cm I_m,  I_k(r) = int rho(x') cos(k|x-x'|)/(4 pi |x-x'|) d^3x'  (k = 0, m_static)
#   => Lap Phi = -(c0 + cm) rho - cm m_s^2 I_m,  rho_eff = -cm m_s^2 I_m/(4 pi G),  g_tot = dPhi/dr.
# For a spherical source: I_k(r) = (1/(2 k r)) int rho(r') r' [sin(k(r+r')) - sin(k|r-r'|)] dr'.
mpm.mp.dps = 30
a0c = FOOT['canonical']
m_st = K_PLANT * m_bg
c0_num = A_res['Phi_coef']['c0'].subs({Gs: 1})       # coefficients are G times numbers
cm_num = A_res['Phi_coef']['cm'].subs({Gs: 1})
c0_v = mpm.mpf(sp.N(c0_num, 40)) * G_SI
cm_v = mpm.mpf(sp.N(cm_num, 40)) * G_SI
norm_ok = abs(-(c0_v + cm_v) / (4 * mpm.pi * G_SI) - 1) < mpm.mpf('1e-25')
P('  R3 uses route A\'s coefficients: c0 = %s G, cm = %s G ; -(c0 + cm) = 4 pi G: %s' % (c0_num, cm_num, norm_ok))


def I_k_sphere(r, Mkg, h, kk):
    rho0 = Mkg / (8 * mpm.pi * h ** 3)
    f = lambda rp: rho0 * mpm.e ** (-rp / h) * rp * (mpm.sin(kk * (r + rp)) - mpm.sin(kk * abs(r - rp)))
    fp = lambda rp: rho0 * mpm.e ** (-rp / h) * rp * kk * (mpm.cos(kk * (r + rp))
                                                           - mpm.sign(r - rp) * mpm.cos(kk * abs(r - rp)))
    J = mpm.quad(f, [0, r, r + 40 * h, mpm.inf])
    Jp = mpm.quad(fp, [0, r, r + 40 * h, mpm.inf])
    return J / (2 * kk * r), -J / (2 * kk * r ** 2) + Jp / (2 * kk * r)


RX = {}
for n in MGRID:
    GM = n * GMSUN
    Mkg = GM / G_SI
    for x in XGRID:
        r = x * r_M(GM, a0c)
        s = r / h_sph
        Mb_in = Mkg * (1 - (1 + s + s ** 2 / 2) * mpm.e ** (-s))
        gN = G_SI * Mb_in / r ** 2
        Im, dIm = I_k_sphere(r, Mkg, h_sph, m_st)
        dI0 = -gN / (4 * mpm.pi * G_SI)                      # I_0 = -Phi_N/(4 pi G), Phi_N' = g_N
        rho_eff_s = -cm_v * m_st ** 2 * Im / (4 * mpm.pi * G_SI)
        g_tot = c0_v * dI0 + cm_v * dIm
        RX[(n, x)] = rho_eff_s * r ** 3 * g_tot / (a0c / (4 * mpm.pi) * Mb_in)
absRX = {k: abs(v) for k, v in RX.items()}
kmn = min(absRX, key=absRX.get)
kmx = max(absRX, key=absRX.get)
P('  R3 sphere (h = 2 kpc, canonical): |R_X| in [%s, %s] at (M_b, x) = (%s, %s) and (%s, %s); CFG123 [6e-17, 2.0e-12]'
  % (f2s(absRX[kmn], 4), f2s(absRX[kmx], 4), f2s(kmn[0], 2), f2s(kmn[1], 3), f2s(kmx[0], 2), f2s(kmx[1], 3)))
dR3 = [float(abs(mpm.log10(absRX[kmn]) - mpm.log10(mpm.mpf('6e-17')))),
       float(abs(mpm.log10(absRX[kmx]) - mpm.log10(mpm.mpf('2.0e-12'))))]
P('  R3 |d log10| at the two ends: %.4f, %.4f dex (line 0.5; reported); sign: %s'
  % (dR3[0], dR3[1], 'all negative' if set(mpm.sign(v) for v in RX.values()) == {-1} else 'mixed'))
RES['rows']['R3'] = {'min': float(absRX[kmn]), 'min_at': [float(kmn[0]), float(kmn[1])], 'max': float(absRX[kmx]),
                     'max_at': [float(kmx[0]), float(kmx[1])], 'dex': dR3, 'within_0p5': all(d <= 0.5 for d in dR3)}
# E1
P('  E1 U-bar(0)/2 = %.4f (hand expectation about 8): the size of the untested background coupling -U-bar dU g_mn '
  'relative to the flat-space -2 dU g_mn in the 00 equation' % (Ubar0 / 2))
RES['rows']['E1'] = {'U_bar_0_over_2': Ubar0 / 2}

# ---------------------------------------------------------------------------------------------
exit_code = None
if MUTATE:
    banner('MUTATE: m_static = 1e3 m planted in the static action; shift against an unmutated reference')
    A_ref = route_A(1)
    rho_ref_f = sp.lambdify((rr, Gs, Msym, msym), A_ref['rho_eff'], 'mpmath')
    mpm.mp.dps = 50
    RA_ref = RA_grid(rho_ref_f, m_bg)
    worst_shift = 0
    shifts = []
    for k, v in RA.items():
        fn, n, x = k
        r = x * r_M(n * GMSUN, FOOT[fn])
        pred = 6 + mpm.log10(mpm.cos(1000 * m_bg * r) / mpm.cos(m_bg * r))
        act = mpm.log10(abs(v)) - mpm.log10(abs(RA_ref[k]))
        shifts.append(float(act))
        worst_shift = max(worst_shift, abs(act - 6))
        if abs(act - pred) > mpm.mpf('1e-6'):
            P('   note: shift differs from the cos prediction at', k, float(act), float(pred))
    shift_ok = worst_shift <= 0.01
    P('  actual shift range: %.5f .. %.5f dex (predicted 5.998 .. 6.000; line 6.000 +- 0.01): %s'
      % (min(shifts), max(shifts), 'within' if shift_ok else 'MISSED'))
    RES['MUTATE'] = {'shift_min': min(shifts), 'shift_max': max(shifts), 'worst_abs_minus_6': float(worst_shift),
                     'shift_ok': bool(shift_ok), 'H1_pass_under_mutate': bool(H1)}
    if H1:
        exit_code = 0
    elif shift_ok:
        exit_code = 1
    else:
        exit_code = 2
else:
    lb_ok = all(ok for (nm, ok, lb, d) in CHECKS if lb)
    exit_code = 0 if lb_ok else 1

banner('Summary')
for (nm, ok, lb, d) in CHECKS:
    P('  %-4s %s%s' % ('PASS' if ok else 'FAIL', nm, '' if lb else ' (reported)'))
P('  exit code:', exit_code, '  runtime %.1f s' % (time.time() - T_START))
P('  kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory '
  'is closed.')
RES['exit_code'] = exit_code
RES['runtime_s'] = time.time() - T_START


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (mpm.mpf,)):
        return float(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, sp.Basic):
        return str(o)
    return o


with open(JSON_PATH, 'w') as fh:
    json.dump(_clean(RES), fh, indent=1)
_out.close()
sys.exit(exit_code)
