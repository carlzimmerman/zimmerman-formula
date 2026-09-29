#!/usr/bin/env python3
"""
CFG156 -- independent re-derivation of CFG131's sound-speed headline (door 8: an interacting vacuum, Q(Lambda, rho_c)).

Frozen criteria: ../CFG156_FROZEN_CRITERIA.md (its sha256 is printed first; committed unchanged by the orchestrator as c3b321f99).
Built from CFG131's FROZEN_QUESTION.md and README.md, the ten-door gates, and CFG44's README and Bcommon.py docstrings only.
Nothing is imported from the repository. No CFG131 script or output was opened before these runs.

Headline under test (CFG131 README item 3, row R2): the cold fluid's sound speed that the interacting vacuum can provide is
c_s^2 <= 4.6e-12 (k = 30/Mpc, 5% growth to z = 0), against the V_f^2/2c^2 ~ 2e-8 (1e9 Msun) to 6e-7 (1e12 Msun) that the
target's hydrostatic support requires; the requirement is 4.3e3 above the bound.

  python3 cfg156_referee.py            -> cfg156_referee.out, cfg156_referee_results.json                (must exit 0)
  MUTATE=1 python3 cfg156_referee.py   -> cfg156_referee_MUTATE.out, cfg156_referee_MUTATE_results.json  (must exit 1)

MUTATE=1 multiplies the growth equation's pressure term by 1e-5 inside every bound search. The controls, R-req and R-dens
run unmutated.

Amended after the first run (its output is kept as cfg156_referee_firstrun.out / _firstrun_results.json); no pass line,
tolerance or physics input changed:
  (1) CB1's symbolic zero test. The first run used `simplify(e) == 0`, which left sin(2th)tan(th) + cos(2th) - 1 (identically
      zero) unreduced in the theta component of steps 1-2. The test is now is_zero(): simplify, then trigsimp(expand_trig(.)).
      A post-hoc self-check shows it still returns False on a nonzero expression.
  (2) Post-hoc row CM3' (reported only): the exact first-order solution INCLUDING the delta = a start at z = 1000,
      (2 f_c/7)(1 - 1.4 a_i + 0.4 a_i^3.5). CM3 keeps its declared 1e-3 line against the declared closed form and its FAIL.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
"""
import hashlib
import json
import math
import os
import sys
import time

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import jv, jvp

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.normpath(os.path.join(HERE, '..', 'CFG156_FROZEN_CRITERIA.md'))
MUTATE = os.environ.get('MUTATE', '0').strip() == '1'
TAG = 'cfg156_referee' + ('_MUTATE' if MUTATE else '')
PFAC_BOUND = 1e-5 if MUTATE else 1.0          # pressure-term factor used inside the bound searches only

# ------------------------------------------------------------------------------------------------ constants (SI unless stated)
C_LIGHT = 299792458.0              # m/s
GM_SUN = 1.32712440018e20          # m^3/s^2 (IAU 2015 nominal)
G_SI = 6.67430e-11                 # m^3/(kg s^2); only rho (kg/m^3) and masses in kg need it
MPC = 3.0856775814913673e22        # m
KPC = MPC/1e3
A0 = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
MASSES = (1e9, 1e10, 1e11, 1e12)   # Msun
X_LO, X_HI, NX = 0.1, 30.0, 2001

# growth conventions: CFG131's frozen question (two fluids, Omega_c = 0.265, Omega_b = 0.050, z = 1000, delta = a);
# H0 = 67.4 with k in Mpc^-1, flat, no radiation, Gamma = 0 are the spec's declared readings
H0_KMS = 67.4
H_LITTLE = H0_KMS/100.0
OM_C, OM_B = 0.265, 0.050
Z_START = 1000.0
N_START = -math.log(1.0 + Z_START)
KS = (0.5, 2.0, 10.0, 30.0)        # Mpc^-1
RATIO_LINE = 0.95
OMR_H2 = 4.18e-5                   # R-rad: photons + 3.046 massless neutrinos, T_CMB = 2.7255 K (declared in the spec)

# CFG131 README numbers (READ before any code; targets, not blind predictions)
CFG131 = {'bound_z0': {0.5: 1.7e-8, 2.0: 1.0e-9, 10.0: 4.2e-11, 30.0: 4.6e-12},
          'bound_z10': {0.5: 1.5e-7, 30.0: 4.3e-11},
          'req_1e9': 2e-8, 'req_1e12': 6e-7, 'factor': 4.3e3, 'S2_min': 32.0, 'S2_max': 272.0}

LINES, CHECKS = [], []
NUM = {}


def P(s=''):
    print(s, flush=True)
    LINES.append(s)


def check(name, ok, detail, load=True):
    ok = bool(ok)
    CHECKS.append({'name': name, 'ok': ok, 'load_bearing': load, 'detail': detail})
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load else ' (reported)'} {name}: {detail}")
    return ok


def within(v, target, tol=0.10):
    return abs(v/target - 1.0) <= tol


def e3(v):
    return f'{v:.3e}'


def is_zero(e):
    """Symbolic zero test (amended after the first run): simplify, then trigsimp(expand_trig(.)) if needed."""
    e = sp.simplify(e)
    if e == 0:
        return True
    return sp.simplify(sp.trigsimp(sp.expand_trig(e))) == 0


# ================================================================================================ (b) B1: the covariant chain
def cb1_derivation():
    P('CB1 / B1 -- the covariant chain (sympy) on ds^2 = -N(t,r)^2 dt^2 + A(t,r)^2 dr^2 + B(t,r)^2 dOmega^2,')
    P('            the cold fluid comoving, u = N^-1 d_t (a hypersurface-orthogonal congruence in comoving coordinates)')
    t, r, th, ph = sp.symbols('t r theta phi', real=True)
    Nf, Af, Bf = (sp.Function(s)(t, r) for s in ('N', 'A', 'B'))
    X = (t, r, th, ph)
    g = sp.diag(-Nf**2, Af**2, Bf**2, Bf**2*sp.sin(th)**2)
    gi = g.inv()
    Gam = [[[sp.simplify(sum(gi[l, s]*(sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s]))
                             for s in range(4))/2) for n in range(4)] for m in range(4)] for l in range(4)]

    def div2(T):   # nabla_mu T^{mu nu}
        out = []
        for n in range(4):
            e = sum(sp.diff(T[m, n], X[m]) for m in range(4))
            e += sum(Gam[m][m][l]*T[l, n] for m in range(4) for l in range(4))
            e += sum(Gam[n][m][l]*T[m, l] for m in range(4) for l in range(4))
            out.append(e)
        return out

    steps = {}
    # (1) Lorentz-invariant vacuum: nabla_mu(-rho_L g^{mu nu}) = -d^nu rho_L for any rho_L(t, r)
    rL = sp.Function('rho_L')(t, r)
    dv = div2(-rL*gi)
    r1 = [dv[n] + sum(gi[n, l]*sp.diff(rL, X[l]) for l in range(4)) for n in range(4)]
    steps['1  nabla_mu(-rho_L g^{mu nu}) = -d^nu rho_L'] = all(is_zero(e) for e in r1)
    # (2) the exchange nabla_mu T_vac^{mu nu} = -Q u^nu  ->  d_r rho_L = 0 and d_t rho_L = -N Q
    Q = sp.Symbol('Q')
    u = (1/Nf, 0, 0, 0)
    dtL, drL = sp.symbols('dtL drL')
    sub = {sp.Derivative(rL, t): dtL, sp.Derivative(rL, r): drL}
    eqs = [sp.simplify((dv[n] + Q*u[n]).subs(sub)) for n in range(4)]
    sol = sp.solve(eqs[:2], [dtL, drL], dict=True)
    steps['2  exchange -> d_r rho_L = 0, N = -d_t rho_L / Q'] = (
        len(sol) == 1 and is_zero(sol[0][dtL] + Nf*Q) and is_zero(sol[0][drL])
        and is_zero(eqs[2]) and is_zero(eqs[3]))
    # (3) the fluid's acceleration a_mu = u^nu nabla_nu u_mu
    ul = [sum(g[m, n]*u[n] for n in range(4)) for m in range(4)]
    acc = [sp.simplify(sum(u[n]*sp.diff(ul[m], X[n]) for n in range(4))
                       - sum(Gam[l][n][m]*u[n]*ul[l] for l in range(4) for n in range(4))) for m in range(4)]
    steps['3  a_mu = (0, d_r ln N, 0, 0)'] = (is_zero(acc[0]) and is_zero(acc[1] - sp.diff(Nf, r)/Nf)
                                             and is_zero(acc[2]) and is_zero(acc[3]))
    # (4) the cold perfect fluid with the exchange: nabla_mu T_c^{mu nu} = +Q u^nu
    rho, p, Qf = (sp.Function(s)(t, r) for s in ('rho', 'p', 'Q'))
    Tc = sp.Matrix(4, 4, lambda m, n: (rho + p)*u[m]*u[n] + p*gi[m, n])
    dc = div2(Tc)
    E = [sp.simplify(dc[n] - Qf*u[n]) for n in range(4)]
    euler = E[1]*Af**2 - (sp.diff(p, r) + (rho + p)*sp.diff(Nf, r)/Nf)
    energy = E[0]*Nf - ((sp.diff(rho, t) + (rho + p)*sp.diff(sp.log(Af*Bf**2), t))/Nf - Qf)
    steps['4  Euler: A^2 E^r = d_r p + (rho+p) d_r ln N, no Q term'] = (
        is_zero(euler) and not E[1].has(Qf) and is_zero(E[2]) and is_zero(E[3]))
    steps['4b energy: N E^t = [d_t rho + (rho+p) d_t ln(A B^2)]/N - Q'] = is_zero(energy)
    # (5) rho_L uniform on the slice, N = -rho_L'(t)/Q(rho_L, rho)  ->  d_r p = (rho+p)(Q_rho/Q) d_r rho
    rLt = sp.Function('rho_L')(t)
    Ls, Rs = sp.symbols('L R', positive=True)
    xi, nn, mm, al, rs = sp.symbols('xi n m alpha rho_s', positive=True)
    forms = [('general Q(L,R)', sp.Function('Q')(Ls, Rs)),
             ('power law xi R^n L^m', xi*Rs**nn*Ls**mm),
             ('non-power xi L^m exp(alpha R)(1+R/rho_s)^n', xi*Ls**mm*sp.exp(al*Rs)*(1 + Rs/rs)**nn)]
    for name, QLR in forms:
        Nsub = -sp.diff(rLt, t)/QLR.subs({Ls: rLt, Rs: rho})
        pr_euler = -(rho + p)*sp.diff(sp.log(Nsub), r)
        cs2 = ((rho + p)*sp.diff(QLR, Rs)/QLR).subs({Ls: rLt, Rs: rho})
        res = (pr_euler - cs2*sp.diff(rho, r)).doit()
        steps[f'5  d_r p = (rho+p)(Q_rho/Q) d_r rho  [{name}]'] = is_zero(res)
    # (6) the power law: the forced equation of state and c_s^2 = n(1+w)
    rr = sp.Symbol('rho', positive=True)
    Cc = sp.Symbol('C')
    pf = sp.Function('p')
    ode = sp.Eq(pf(rr).diff(rr), nn*(rr + pf(rr))/rr)
    claim = nn*rr/(1 - nn) + Cc*rr**nn
    r6a = sp.simplify(claim.diff(rr) - nn*(rr + claim)/rr)          # the claim solves the ODE for symbolic n
    r6b = sp.simplify(claim.diff(rr) - nn*(1 + claim/rr))           # c_s^2 = n(1+w)
    r6h = sp.simplify(sp.diff(rr**nn, rr) - nn*rr**nn/rr)           # rho^n spans the homogeneous solutions (1st-order linear)
    n_c = sp.Rational(3, 10)                                        # dsolve itself at a generic concrete n (avoids n = 1 branch)
    ode_c = ode.subs(nn, n_c)
    ds = sp.dsolve(ode_c)
    chk = sp.checkodesol(ode_c, ds)
    r6c = sp.simplify(sp.diff((ds.rhs - n_c*rr/(1 - n_c))/rr**n_c, rr))
    steps['6  power law: p = n rho/(1-n) + C rho^n, c_s^2 = n(1+w)'] = (chk[0] is True and is_zero(r6a) and is_zero(r6b)
                                                                       and is_zero(r6h) and is_zero(r6c))
    P(f'     sympy dsolve of dp/drho = n(rho+p)/rho at n = 3/10: {ds}')
    # (7, reported) the static limit: nothing depends on t -> the energy equation forces Q = 0 (CFG131's A5)
    Ns_, As_, Bs_, rhos_, ps_ = (sp.Function(s)(r) for s in ('N', 'A', 'B', 'rho', 'p'))
    E0s = sp.simplify(E[0].subs({Nf: Ns_, Af: As_, Bf: Bs_, rho: rhos_, p: ps_}).doit())
    qsol = sp.solve(sp.Eq(E0s, 0), Qf)
    for k_, v_ in steps.items():
        check(f'CB1 step {k_}', v_, 'zero residual' if v_ else 'NONZERO residual')
    check('B1 step 7 (static limit forces Q = 0; CFG131 A5)', qsol == [0], f'static N E^t = {sp.simplify(E0s*Ns_)}; '
          f'solve -> Q = {qsol}', load=False)
    # post hoc (added after the first run): the amended zero test must not return True on a nonzero expression
    th_res = dv[2] + sum(gi[2, l]*sp.diff(rL, X[l]) for l in range(4))
    selfcheck = is_zero(th_res) and not is_zero(th_res + rL*sp.cos(th)/Bf**2)
    check("CB1' (post hoc) zero-test self-check", selfcheck, 'is_zero(theta residual of step 1) = True and '
          'is_zero(same + rho_L cos(theta)/B^2) = False', load=False)
    return all(steps.values())


def cm2_symbolic():
    Nn, bb = sp.symbols('N beta', positive=True)
    dl = sp.exp(-Nn/4)*sp.besselj(sp.Rational(5, 2), 2*sp.sqrt(bb*sp.exp(Nn)))
    res = sp.diff(dl, Nn, 2) + sp.diff(dl, Nn)/2 - sp.Rational(3, 2)*dl + bb*sp.exp(Nn)*dl
    sym = sp.simplify(sp.expand_func(res))
    if sym == 0:
        return True, "sympy: delta'' + delta'/2 - (3/2) delta + beta a delta simplifies to 0"
    worst = 0.0
    for (Nv, bv) in [(-3.0, 0.2), (-1.0, 1.0), (0.0, 5.0), (-5.0, 3.0), (0.0, 0.7)]:
        val = abs(complex(res.subs({Nn: Nv, bb: bv}).evalf(30)))
        scl = abs(complex(dl.subs({Nn: Nv, bb: bv}).evalf(30)))
        worst = max(worst, val/scl)
    return worst < 1e-20, f'sympy numeric fallback (no symbolic zero): max |residual/delta| = {worst:.1e} at 5 points'


# ================================================================================================ (a) the target side
def point_target(M, a0, x):
    """CFG44 point mass under the P2 law (README formulas)."""
    GM = M*GM_SUN
    rM = math.sqrt(GM/a0)
    r = x*rM
    gN = GM/r**2
    gtot = np.sqrt(gN**2 + gN*a0)
    rho = a0/(4.0*math.pi*G_SI*r*np.sqrt(1.0 + x**2))
    return r, rho, gtot, gN, rM, GM


def point_callables(M, a0):
    GM = M*GM_SUN
    rM = math.sqrt(GM/a0)

    def rho_f(r):
        x = r/rM
        return a0/(4.0*math.pi*G_SI*r*math.sqrt(1.0 + x*x))

    def g_f(r):
        gN = GM/(r*r)
        return math.sqrt(gN*gN + gN*a0)
    return rho_f, g_f


def hydro_P(rho_f, g_f, r_arr):
    """Hydrostatic pressure with P(inf) = 0: P(r) = int_r^inf rho g dr', by quadrature in s = ln(r'/r) on [0, 80]."""
    out = np.empty(len(r_arr))
    for i, ri in enumerate(r_arr):
        def f(s, ri=ri):
            rr = ri*math.exp(s)
            return rho_f(rr)*g_f(rr)*rr
        out[i] = quad(f, 0.0, 80.0, epsabs=0.0, epsrel=1e-12, limit=400)[0]
    return out


def centred_dPdrho(P_ext, rho_ext):
    """dP/drho at the interior points of a uniform ln-x grid carrying one ghost point at each end (centred differences)."""
    return (P_ext[2:] - P_ext[:-2])/(rho_ext[2:] - rho_ext[:-2])


def ln_grid():
    lnx = np.linspace(math.log(X_LO), math.log(X_HI), NX)
    d = lnx[1] - lnx[0]
    return np.exp(np.concatenate(([lnx[0] - d], lnx, [lnx[-1] + d])))


def target_side():
    x_ext = ln_grid()
    x = x_ext[1:-1]
    TGT = {}
    for fname, a0 in A0.items():
        TGT[fname] = {}
        for M in MASSES:
            r_ext, rho_ext, gt_ext, gN_ext, rM, GM = point_target(M, a0, x_ext)
            rho_f, g_f = point_callables(M, a0)
            P_ext = hydro_P(rho_f, g_f, r_ext)
            dPdrho = centred_dPdrho(P_ext, rho_ext)
            Pi, rhoi, ri, gti, gNi = P_ext[1:-1], rho_ext[1:-1], r_ext[1:-1], gt_ext[1:-1], gN_ext[1:-1]
            # CT1: the target's own identity
            C_num = rhoi*ri**3*gti
            C_cf = a0*GM/(4.0*math.pi*G_SI)
            Mc = np.empty(NX)
            integrand = (lambda rr: 4.0*math.pi*rr*rr*rho_f(rr))
            acc = quad(integrand, 0.0, ri[0], epsabs=0.0, epsrel=1e-13, limit=200)[0]
            Mc[0] = acc
            for i in range(1, NX):
                acc += quad(integrand, ri[i - 1], ri[i], epsabs=0.0, epsrel=1e-13, limit=200)[0]
                Mc[i] = acc
            Mc_cf = (GM/G_SI)*(np.sqrt(1.0 + x**2) - 1.0)
            g_from_M = G_SI*(GM/G_SI + Mc)/ri**2
            # CT3: closed forms (mine, from CFG44's formulas)
            P_cf = a0*GM/(8.0*math.pi*G_SI*ri**2)
            Vc2 = (GM/ri)*np.sqrt(1.0 + x**2)
            dPdrho_cf = Vc2*(1.0 + x**2)/(1.0 + 2.0*x**2)
            Vf2 = math.sqrt(GM*a0)
            c2 = dPdrho/C_LIGHT**2
            c2P = (Pi/rhoi)/C_LIGHT**2
            TGT[fname][M] = {
                'x': x, 'rho': rhoi, 'P': Pi, 'c2_dPdrho': c2, 'c2_Prho': c2P, 'rM_kpc': rM/KPC,
                'Vf_kms': math.sqrt(Vf2)/1e3, 'c2_flat': Vf2/(2.0*C_LIGHT**2),
                'CT1_C': float(np.max(np.abs(C_num/C_cf - 1.0))),
                'CT1_Mc': float(np.max(np.abs(Mc/Mc_cf - 1.0))),
                'CT1_g': float(np.max(np.abs(g_from_M/gti - 1.0))),
                'CT3_P': float(np.max(np.abs(Pi/P_cf - 1.0))),
                'CT3_dPdrho': float(np.max(np.abs(dPdrho/dPdrho_cf - 1.0))),
                'CT3_Prho_vs_Vc2half': float(np.max(np.abs((Pi/rhoi)/(Vc2/2.0) - 1.0))),
                'c2_dPdrho_min': float(c2.min()), 'x_at_min': float(x[int(np.argmin(c2))]),
                'c2_dPdrho_max': float(c2.max()), 'x_at_max': float(x[int(np.argmax(c2))]),
                'c2_Prho_min': float(c2P.min()), 'c2_Prho_max': float(c2P.max()),
            }
    return TGT


def sis_control():
    sigma = 1.0e5
    rho_f = (lambda r: sigma**2/(2.0*math.pi*G_SI*r*r))
    g_f = (lambda r: 2.0*sigma**2/r)
    r_ext = ln_grid()*KPC*10.0          # 1 .. 300 kpc
    P_ext = hydro_P(rho_f, g_f, r_ext)
    rho_ext = np.array([rho_f(rr) for rr in r_ext])
    Prho = P_ext[1:-1]/rho_ext[1:-1]
    dPdrho = centred_dPdrho(P_ext, rho_ext)
    return float(np.max(np.abs(Prho/sigma**2 - 1.0))), float(np.max(np.abs(dPdrho/sigma**2 - 1.0)))


# ================================================================================================ (b) B2-B3: growth and the bound
def cosmology(H0=H0_KMS, om_r=0.0):
    return {'H0': H0, 'h0c': H0/(C_LIGHT/1e3), 'om_c': OM_C, 'om_b': OM_B, 'om_r': om_r,
            'om_l': 1.0 - OM_C - OM_B - om_r}


COS = cosmology()


def grow(k, cs2, cos, N_end=0.0, w=0.0, pfac=1.0, cs2_func=None, y0=None, rtol=1e-10, atol=1e-14, breaks=()):
    """Sub-horizon two-fluid growth in N = ln a; y = (delta_c, delta_c', delta_b, delta_b'). k in Mpc^-1, c_s^2 in c^2.
    w = 0 is B2; w = c_s^2 is R-w (background rho_c ~ a^-3(1+w) and the (1+w), (1-3w) factors)."""
    om_c, om_b, om_r, om_l, h0c = cos['om_c'], cos['om_b'], cos['om_r'], cos['om_l'], cos['h0c']
    kk = k*k

    def rhs(N, y):
        a = math.exp(N)
        rc = om_c*a**(-3.0*(1.0 + w))
        rb = om_b*a**-3
        rr = om_r*a**-4
        e2 = rc + rb + rr + om_l
        dlnH = -(3.0*(1.0 + w)*rc + 3.0*rb + 4.0*rr)/(2.0*e2)
        src = 1.5*(rc*y[0] + rb*y[2])/e2
        c2 = cs2 if cs2_func is None else cs2_func(a)
        press = pfac*c2*kk/((h0c*a)**2*e2)
        return [y[1], -(2.0 + dlnH - 3.0*w)*y[1] + (1.0 + w)*src - press*y[0],
                y[3], -(2.0 + dlnH)*y[3] + src]

    a_i = math.exp(N_START)
    y = np.array([a_i, a_i, a_i, a_i] if y0 is None else y0, dtype=float)
    nodes = [N_START] + sorted(b for b in breaks if N_START < b < N_end) + [N_end]
    for Na, Nb in zip(nodes[:-1], nodes[1:]):
        sol = solve_ivp(rhs, (Na, Nb), y, method='DOP853', rtol=rtol, atol=atol)
        if not sol.success:
            raise RuntimeError(sol.message)
        y = sol.y[:, -1]
    return y


def delta_m(y, cos, N, w=0.0):
    a = math.exp(N)
    rc = cos['om_c']*a**(-3.0*(1.0 + w))
    rb = cos['om_b']*a**-3
    return (rc*y[0] + rb*y[2])/(rc + rb)


_REF = {}


def ref_dm(cos, N_end, rtol=1e-10, atol=1e-14):
    key = (cos['H0'], cos['om_r'], cos['om_c'], cos['om_b'], cos['om_l'], N_end, rtol, atol)
    if key not in _REF:
        _REF[key] = delta_m(grow(1.0, 0.0, cos, N_end, rtol=rtol, atol=atol), cos, N_end)
    return _REF[key]


def ratio(k, cs2, cos, N_end=0.0, w=0.0, pfac=1.0, cs2_func=None, rtol=1e-10, atol=1e-14, breaks=()):
    y = grow(k, cs2, cos, N_end, w=w, pfac=pfac, cs2_func=cs2_func, rtol=rtol, atol=atol, breaks=breaks)
    return delta_m(y, cos, N_end, w)/ref_dm(cos, N_end, rtol, atol)


def bound(k, cos, z_eval=0.0, w_eq_cs2=False, pfac=None, rtol=1e-10, atol=1e-14):
    """Smallest constant c_s^2 at which the total-matter growth ratio at z_eval falls to 0.95:
    a 0.1-dex scan upward from 1e-16 to the first crossing, then brentq in log10 c_s^2."""
    pfac = PFAC_BOUND if pfac is None else pfac
    N_end = -math.log(1.0 + z_eval)

    def R(lc):
        c2 = 10.0**lc
        return ratio(k, c2, cos, N_end, w=(c2 if w_eq_cs2 else 0.0), pfac=pfac, rtol=rtol, atol=atol)
    prev = None
    for j in range(0, 161):
        lc = -16.0 + 0.1*j
        if R(lc) < RATIO_LINE:
            if prev is None:
                raise RuntimeError('ratio already below the line at c_s^2 = 1e-16')
            return 10.0**brentq(lambda l: R(l) - RATIO_LINE, prev, lc, xtol=1e-12, rtol=1e-14, maxiter=200)
        prev = lc
    raise RuntimeError('no crossing up to c_s^2 = 1')


def D_integral(a, cos):
    om_m = cos['om_c'] + cos['om_b']

    def E(aa):
        return math.sqrt(om_m/aa**3 + cos['om_l'])
    I = quad(lambda aa: 1.0/(aa*E(aa))**3, 0.0, a, epsabs=0.0, epsrel=1e-13, limit=400)[0]
    return 2.5*om_m*E(a)*I


# ================================================================================================ main
def main():
    spec_hash = hashlib.sha256(open(SPEC, 'rb').read()).hexdigest()
    P(f'CFG156 frozen criteria sha256 = {spec_hash}  (../CFG156_FROZEN_CRITERIA.md)')
    P(f"CFG156 -- independent re-derivation of CFG131's sound-speed headline (door 8, interacting vacuum). MODE = "
      f"{'MUTATE=1 (pressure term x 1e-5 inside every bound search)' if MUTATE else 'main'}")
    P(f'python {sys.version.split()[0]}, numpy {np.__version__}, scipy {scipy.__version__}, sympy {sp.__version__}')
    P(f'a0 canonical {A0["canonical"]:.4e}, alt {A0["alt"]:.4e} m/s^2; GM_sun {GM_SUN:.11e}; G {G_SI:.5e}; c {C_LIGHT:.0f}')
    P(f'growth: flat, Omega_c {OM_C}, Omega_b {OM_B}, Omega_L {COS["om_l"]:.3f}, no radiation, H0 {H0_KMS} (H0/c = '
      f'{COS["h0c"]:.6e} /Mpc), start z = {Z_START:.0f} with delta = a, k in Mpc^-1, ratio line {RATIO_LINE}')
    P('amended after the first run (cfg156_referee_firstrun.out kept): CB1 zero test strengthened (trig identity), post-hoc '
      "rows CB1' and CM3' added; no pass line, tolerance or physics input changed")
    NUM['spec_sha256'] = spec_hash
    NUM['mode'] = 'MUTATE' if MUTATE else 'main'
    NUM['pressure_factor_in_bound_search'] = PFAC_BOUND

    # ---------------------------------------------------------------- B1 / CB1
    P()
    cb1_ok = cb1_derivation()
    NUM['CB1_all_steps_zero'] = cb1_ok

    # ---------------------------------------------------------------- (a) target side
    P()
    P('(a) TARGET SIDE -- CFG44 point mass, P2 law; hydrostatics dP/dr = -rho_c g_tot; P(inf) = 0 by quadrature;')
    P('    dP/drho by centred differences on a 2001-point ln-x grid in [0.1, 30] (one ghost point at each end)')
    s_Prho, s_dPdrho = sis_control()
    check('CT2 SIS solver: P/rho = sigma^2', s_Prho <= 1e-8, f'max rel dev {s_Prho:.2e} (line 1e-8)')
    check('CT2 SIS solver: dP/drho = sigma^2', s_dPdrho <= 1e-5, f'max rel dev {s_dPdrho:.2e} (line 1e-5)')
    NUM['CT2'] = {'Prho': s_Prho, 'dPdrho': s_dPdrho}
    TGT = target_side()
    ct1 = max(max(d['CT1_C'], d['CT1_Mc'], d['CT1_g']) for f in TGT.values() for d in f.values())
    worst = {kk: max(d[kk] for f in TGT.values() for d in f.values()) for kk in ('CT1_C', 'CT1_Mc', 'CT1_g', 'CT3_P',
                                                                                 'CT3_dPdrho', 'CT3_Prho_vs_Vc2half')}
    check('CT1 target identity C(r) = rho_c r^3 g_tot = a0 M_b/4pi', worst['CT1_C'] <= 1e-12,
          f'max rel dev {worst["CT1_C"]:.2e} over 4 masses x 2 footings x 2001 points (line 1e-12)')
    check('CT1 M_c(<r) by quadrature = M_b(sqrt(1+x^2) - 1)', worst['CT1_Mc'] <= 1e-8,
          f'max rel dev {worst["CT1_Mc"]:.2e} (line 1e-8)')
    check('CT1 G(M_b + M_c)/r^2 = sqrt(g_N^2 + g_N a0)', worst['CT1_g'] <= 1e-8,
          f'max rel dev {worst["CT1_g"]:.2e} (line 1e-8)')
    check('CT3 numeric P = a0 M_b/(8 pi r^2)', worst['CT3_P'] <= 1e-8, f'max rel dev {worst["CT3_P"]:.2e} (line 1e-8)')
    check('CT3 numeric dP/drho = V_c^2 (1+x^2)/(1+2x^2)', worst['CT3_dPdrho'] <= 1e-5,
          f'max rel dev {worst["CT3_dPdrho"]:.2e} (line 1e-5)')
    check('CT3b numeric P/rho = V_c^2/2', worst['CT3_Prho_vs_Vc2half'] <= 1e-8,
          f'max rel dev {worst["CT3_Prho_vs_Vc2half"]:.2e}', load=False)
    NUM['CT1_CT3_worst'] = worst
    _ = ct1

    P()
    P('    required c_s^2 (units of c^2) per mass: dP/drho [min over x (at x), max over x (at x)], P/rho [min, max], '
      'and the x -> inf value V_f^2/2c^2')
    NUM['target'] = {}
    for fname in A0:
        P(f'    footing {fname} (a0 = {A0[fname]:.4e}):')
        NUM['target'][fname] = {}
        for M in MASSES:
            d = TGT[fname][M]
            P(f'      M_b = {M:.0e}: r_M = {d["rM_kpc"]:7.3f} kpc, V_f = {d["Vf_kms"]:6.2f} km/s | dP/drho min '
              f'{e3(d["c2_dPdrho_min"])} (x = {d["x_at_min"]:.2f}), max {e3(d["c2_dPdrho_max"])} (x = {d["x_at_max"]:.2f})'
              f' | P/rho min {e3(d["c2_Prho_min"])}, max {e3(d["c2_Prho_max"])} | V_f^2/2c^2 = {e3(d["c2_flat"])}'
              f' | min/flat = {d["c2_dPdrho_min"]/d["c2_flat"]:.5f}')
            NUM['target'][fname][f'{M:.0e}'] = {kk: v for kk, v in d.items() if not isinstance(v, np.ndarray)}

    # ---------------------------------------------------------------- (b) model side: growth controls
    P()
    P('(b) MODEL SIDE -- sub-horizon two-fluid growth, Gamma = 0, constant c_s^2 in the cold fluid, baryons pressureless')
    a_i = math.exp(N_START)
    dm_lcdm = delta_m(grow(1.0, 0.0, COS, 0.0), COS, 0.0)
    D_pred = a_i*D_integral(1.0, COS)/D_integral(a_i, COS)
    cm1 = abs(dm_lcdm/D_pred - 1.0)
    check('CM1 LCDM: delta_m(z=0) = growth integral D(a), normalised to delta = a at z = 1000', cm1 <= 1e-6,
          f'solver {dm_lcdm:.10f}, integral {D_pred:.10f}, rel dev {cm1:.2e} (line 1e-6)')
    NUM['CM1'] = {'solver': dm_lcdm, 'integral': D_pred, 'rel_dev': cm1}

    ok_sym, msg_sym = cm2_symbolic()
    check('CM2a J_(5/2) growing mode solves the EdS Jeans equation', ok_sym, msg_sym)
    eds1 = {'H0': H0_KMS, 'h0c': COS['h0c'], 'om_c': 1.0, 'om_b': 0.0, 'om_r': 0.0, 'om_l': 0.0}
    cm2 = {}
    for beta in (0.2, 1.0, 5.0):
        zi = 2.0*math.sqrt(beta*a_i)
        dB = a_i**-0.25*jv(2.5, zi)
        dBp = a_i**-0.25*(-0.25*jv(2.5, zi) + 0.5*zi*jvp(2.5, zi))
        s = a_i/dB
        y = grow(1.0, beta*eds1['h0c']**2, eds1, 0.0, y0=[s*dB, s*dBp, s*dB, s*dBp])
        exact = s*jv(2.5, 2.0*math.sqrt(beta))
        cm2[beta] = {'solver': float(y[0]), 'exact': float(exact), 'rel_dev': float(abs(y[0]/exact - 1.0)),
                     'ratio_to_pressureless': float(exact/1.0)}
    cm2w = max(v['rel_dev'] for v in cm2.values())
    check('CM2b solver = exact EdS Jeans solution at a = 1 for beta = 0.2, 1, 5', cm2w <= 1e-6,
          '; '.join(f'beta {b}: delta(1)/[pressureless] = {v["exact"]:.6f}, rel dev {v["rel_dev"]:.1e}'
                    for b, v in cm2.items()) + ' (line 1e-6)')
    NUM['CM2'] = {str(b): v for b, v in cm2.items()}

    fc = OM_C/(OM_C + OM_B)
    eds2 = {'H0': H0_KMS, 'h0c': COS['h0c'], 'om_c': fc, 'om_b': 1.0 - fc, 'om_r': 0.0, 'om_l': 0.0}
    beta3 = 1e-4
    d0 = delta_m(grow(1.0, 0.0, eds2, 0.0), eds2, 0.0)
    d1 = delta_m(grow(1.0, beta3*eds2['h0c']**2, eds2, 0.0), eds2, 0.0)
    coef = (1.0 - d1/d0)/beta3
    cm3 = abs(coef/(2.0*fc/7.0) - 1.0)
    check('CM3 two-fluid EdS first order: (1 - ratio)/beta = 2 f_c/7', cm3 <= 1e-3,
          f'solver {coef:.6f}, 2f_c/7 = {2.0*fc/7.0:.6f}, rel dev {cm3:.2e} (line 1e-3)')
    # post hoc (added after the first run; reported only): the first-order solution with the delta = a start at a_i.
    # delta_m'' + delta_m'/2 - (3/2) delta_m = -f_c beta a^2 (d/dN) has particular S a^2, S = -2 f_c beta/7; the start
    # u(a_i) = u'(a_i) = 0 adds c1 a + c2 a^-3/2 with c1 = -1.4 S a_i, c2 = 0.4 S a_i^3.5, so at a = 1:
    # (1 - ratio)/beta = (2 f_c/7)(1 - 1.4 a_i + 0.4 a_i^3.5) + O(beta).
    cf_start = (2.0*fc/7.0)*(1.0 - 1.4*a_i + 0.4*a_i**3.5)
    cm3p = abs(coef/cf_start - 1.0)
    check("CM3' (post hoc) the same with the delta = a start: (2f_c/7)(1 - 1.4 a_i + 0.4 a_i^3.5)", cm3p <= 1e-3,
          f'solver {coef:.6f}, start-corrected closed form {cf_start:.6f}, rel dev {cm3p:.2e} (the O(beta) term is '
          f'~1e-4 x O(0.1))', load=False)
    NUM['CM3'] = {'solver': coef, 'closed_form': 2.0*fc/7.0, 'rel_dev': cm3,
                  'posthoc_start_corrected_closed_form': cf_start, 'posthoc_rel_dev': cm3p}

    # ---------------------------------------------------------------- B3: the bounds
    P()
    P(f'    B3 bound search (pressure factor {PFAC_BOUND:g}): smallest constant c_s^2 with growth ratio = 0.95')
    b0 = {k: bound(k, COS, 0.0) for k in KS}
    b10 = {k: bound(k, COS, 10.0) for k in KS}
    for k in KS:
        P(f'      k = {k:5.1f}/Mpc: z = 0 bound {e3(b0[k])} (x k^2 = {b0[k]*k*k:.4e}); z = 10 bound {e3(b10[k])} '
          f'(x k^2 = {b10[k]*k*k:.4e})')
    NUM['bounds_z0'] = {f'{k:g}': b0[k] for k in KS}
    NUM['bounds_z10'] = {f'{k:g}': b10[k] for k in KS}

    b30_unmut = b0[30.0] if not MUTATE else bound(30.0, COS, 0.0, pfac=1.0)
    b30_fine = bound(30.0, COS, 0.0, pfac=1.0, rtol=1e-12, atol=1e-16)
    cm4 = abs(b30_fine/b30_unmut - 1.0)
    check('CM4 convergence: bound(k = 30) at rtol 1e-12 vs 1e-10 (unmutated)', cm4 <= 1e-5,
          f'{e3(b30_unmut)} vs {e3(b30_fine)}, rel change {cm4:.1e} (line 1e-5)')
    NUM['CM4'] = {'rtol_1e-10': b30_unmut, 'rtol_1e-12': b30_fine, 'rel_change': cm4}

    # ---------------------------------------------------------------- headline
    P()
    P('HEADLINE (canonical footing)')
    tc = TGT['canonical']
    h1 = within(b0[30.0], CFG131['bound_z0'][30.0])
    check('H1 model side: c_s,max^2(k = 30, z = 0) within 10% of 4.6e-12', h1,
          f'{e3(b0[30.0])} vs 4.6e-12 (ratio {b0[30.0]/4.6e-12:.4f})')
    r9, r12 = tc[1e9]['c2_dPdrho_min'], tc[1e12]['c2_dPdrho_min']
    h2 = within(r9, CFG131['req_1e9']) and within(r12, CFG131['req_1e12'])
    check('H2 target side: smallest required dP/drho within 10% of 2e-8 (1e9) and 6e-7 (1e12)', h2,
          f'1e9: {e3(r9)} (ratio {r9/2e-8:.4f}); 1e12: {e3(r12)} (ratio {r12/6e-7:.4f})')
    req_min = min(tc[M]['c2_dPdrho_min'] for M in MASSES)
    fac = req_min/b0[30.0]
    h3 = (req_min > b0[30.0]) and within(fac, CFG131['factor'])
    check('H3 ordering: smallest requirement > c_s,max^2(30), factor within 10% of 4.3e3', h3,
          f'smallest requirement {e3(req_min)} (1e9 Msun, x = {tc[1e9]["x_at_min"]:.2f}) / bound {e3(b0[30.0])} = '
          f'{fac:.4e} (ratio to 4.3e3: {fac/4.3e3:.4f})')
    NUM['headline'] = {'H1_bound_k30_z0': b0[30.0], 'H2_req_1e9': r9, 'H2_req_1e12': r12, 'H3_req_min': req_min,
                       'H3_factor': fac, 'H3_factor_with_flat_value': tc[1e9]['c2_flat']/b0[30.0],
                       'H1': h1, 'H2': h2, 'H3': h3}
    P(f'    (the same factor with the x -> inf value V_f^2/2c^2 = {e3(tc[1e9]["c2_flat"])}: '
      f'{tc[1e9]["c2_flat"]/b0[30.0]:.4e})')

    # ---------------------------------------------------------------- secondary rows
    P()
    P('SECONDARY ROWS (same 10% line; not in the exit code)')
    for k in (0.5, 2.0, 10.0):
        check(f'S1 bound k = {k:g}, z = 0 vs {CFG131["bound_z0"][k]:.1e}', within(b0[k], CFG131['bound_z0'][k]),
              f'{e3(b0[k])} (ratio {b0[k]/CFG131["bound_z0"][k]:.4f})', load=False)
    for k in (0.5, 30.0):
        check(f'S1 bound k = {k:g}, z = 10 vs {CFG131["bound_z10"][k]:.1e}', within(b10[k], CFG131['bound_z10'][k]),
              f'{e3(b10[k])} (ratio {b10[k]/CFG131["bound_z10"][k]:.4f})', load=False)
    NUM['S1_ordering'] = {}
    for k in KS:
        P(f'    S1 ordering at k = {k:4.1f}: smallest requirement / z = 0 bound = {req_min/b0[k]:.4e}; '
          f'/ z = 10 bound = {req_min/b10[k]:.4e}')
        NUM['S1_ordering'][f'{k:g}'] = {'z0': req_min/b0[k], 'z10': req_min/b10[k]}

    d9, d12 = tc[1e9], tc[1e12]
    lr9, lr12 = np.log(d9['rho'])[::-1], np.log(d12['rho'])[::-1]
    lo, hi = max(lr9[0], lr12[0]), min(lr9[-1], lr12[-1])
    gl = np.linspace(lo, hi, 2001)
    Pr = np.exp(np.interp(gl, lr12, np.log(d12['P'])[::-1]) - np.interp(gl, lr9, np.log(d9['P'])[::-1]))
    Cr = np.exp(np.interp(gl, lr12, np.log(d12['c2_dPdrho'])[::-1]) - np.interp(gl, lr9, np.log(d9['c2_dPdrho'])[::-1]))
    s2 = within(Pr.min(), CFG131['S2_min']) and within(Pr.max(), CFG131['S2_max'])
    check('S2 P_req(1e12)/P_req(1e9) at matched rho_c: min, max vs 32, 272', s2,
          f'min {Pr.min():.2f}, max {Pr.max():.2f} over rho_c in [{math.exp(lo):.3e}, {math.exp(hi):.3e}] kg/m^3; '
          f'the same ratio for dP/drho: {Cr.min():.2f} to {Cr.max():.2f}', load=False)
    NUM['S2'] = {'P_ratio_min': float(Pr.min()), 'P_ratio_max': float(Pr.max()), 'dPdrho_ratio_min': float(Cr.min()),
                 'dPdrho_ratio_max': float(Cr.max()), 'rho_lo': math.exp(lo), 'rho_hi': math.exp(hi)}

    # ---------------------------------------------------------------- reported-only rows
    P()
    P('REPORTED-ONLY ROWS (declared in the spec; no pass line)')
    ta = TGT['alt']
    req_min_alt = min(ta[M]['c2_dPdrho_min'] for M in MASSES)
    P(f'    R-alt: smallest dP/drho 1e9 {e3(ta[1e9]["c2_dPdrho_min"])} (ratio to 2e-8 {ta[1e9]["c2_dPdrho_min"]/2e-8:.4f}),'
      f' 1e12 {e3(ta[1e12]["c2_dPdrho_min"])} (ratio to 6e-7 {ta[1e12]["c2_dPdrho_min"]/6e-7:.4f}); '
      f'H3 factor {req_min_alt/b0[30.0]:.4e}')
    NUM['R_alt'] = {'req_1e9': ta[1e9]['c2_dPdrho_min'], 'req_1e12': ta[1e12]['c2_dPdrho_min'],
                    'factor': req_min_alt/b0[30.0]}
    P(f'    R-z10: ' + ', '.join(f'k = {k:g}: {e3(b10[k])}' for k in KS))
    b_units = bound(30.0*H_LITTLE, COS, 0.0)
    P(f'    R-units (k = 30 read in h/Mpc, physical k = {30.0*H_LITTLE:.3f}/Mpc): bound {e3(b_units)} '
      f'(x{b_units/b0[30.0]:.4f} of the main reading)')
    b_h70 = bound(30.0, cosmology(H0=70.0), 0.0)
    P(f'    R-h (H0 = 70, k in Mpc^-1): bound {e3(b_h70)} (x{b_h70/b0[30.0]:.4f})')
    cos_rad = cosmology(om_r=OMR_H2/H_LITTLE**2)
    b_rad = bound(30.0, cos_rad, 0.0)
    P(f'    R-rad (Omega_r = {cos_rad["om_r"]:.4e}, Omega_L = {cos_rad["om_l"]:.6f}): bound {e3(b_rad)} '
      f'(x{b_rad/b0[30.0]:.4f})')
    b_w = bound(30.0, COS, 0.0, w_eq_cs2=True)
    P(f'    R-w (full constant-w fluid, w = c_s^2): bound {e3(b_w)} (rel change {b_w/b0[30.0] - 1.0:.2e})')
    NUM['R_sens'] = {'units_h_per_Mpc': b_units, 'H0_70': b_h70, 'radiation': b_rad, 'full_w': b_w}

    rreq = {k: ratio(k, req_min, COS, 0.0) for k in KS}
    P(f'    R-req (c_s^2 = smallest requirement {e3(req_min)}, unmutated): growth ratio at z = 0: '
      + ', '.join(f'k = {k:g}: {rreq[k]:.4f}' for k in KS))
    NUM['R_req'] = {f'{k:g}': rreq[k] for k in KS}

    rho_crit0 = 3.0*(H0_KMS*1e3/MPC)**2/(8.0*math.pi*G_SI)
    lnrc0 = math.log(OM_C*rho_crit0)
    curves = []
    for M in MASSES:
        d = tc[M]
        curves.append((np.log(d['rho'])[::-1], d['c2_dPdrho'][::-1]))

    def c2_of_lnrho(lr):
        vals = [np.interp(lr, cl, cc) for (cl, cc) in curves if cl[0] <= lr <= cl[-1]]
        return min(vals) if vals else 0.0

    def c2_dens(a):
        return c2_of_lnrho(lnrc0 - 3.0*math.log(a))
    edges_lnrho = sorted({float(cl[0]) for cl, _ in curves} | {float(cl[-1]) for cl, _ in curves})
    breaks = [(lnrc0 - e)/3.0 for e in edges_lnrho]
    z_on = [math.exp(-b) - 1.0 for b in breaks]
    rdens = {k: ratio(k, 0.0, COS, 0.0, cs2_func=c2_dens, breaks=breaks) for k in KS}
    aa = np.exp(np.linspace(N_START, 0.0, 4001))
    c2h = np.array([c2_dens(a) for a in aa])
    on = c2h > 0
    P(f'    R-dens (beyond CFG131; unmutated): rho_bar_c(z=0) = {OM_C*rho_crit0:.4e} kg/m^3; c_s^2(rho_bar_c(z)) > 0 for z in '
      f'[{min(z_on):.2f}, {max(z_on):.2f}], applied c_s^2 from {e3(c2h[on].min())} to {e3(c2h[on].max())}')
    P(f'           growth ratio at z = 0: ' + ', '.join(f'k = {k:g}: {rdens[k]:.4f}' for k in KS))
    NUM['R_dens'] = {'ratio_z0': {f'{k:g}': rdens[k] for k in KS}, 'z_window': [min(z_on), max(z_on)],
                     'c2_applied_min': float(c2h[on].min()), 'c2_applied_max': float(c2h[on].max()),
                     'rho_bar_c0': OM_C*rho_crit0}

    Ng = np.linspace(N_START, 0.0, 4001)
    aHc = COS['h0c']*np.exp(Ng)*np.sqrt((OM_C + OM_B)*np.exp(-3.0*Ng) + COS['om_l'])
    ksub = float((0.5/aHc).min())
    P(f'    R-sub: smallest k/(aH/c) over the integration at k = 0.5/Mpc = {ksub:.1f} (at z = {math.exp(-Ng[int(np.argmin(0.5/aHc))]) - 1:.0f})')
    NUM['R_sub'] = ksub
    P('    R-prof: the requirement falls monotonically from x = 0.1 to x = 30 for every mass (see the table above): '
      + ', '.join(f'{M:.0e}: max/min = {tc[M]["c2_dPdrho_max"]/tc[M]["c2_dPdrho_min"]:.3f}' for M in MASSES))
    mono = all(bool(np.all(np.diff(tc[M]['c2_dPdrho']) < 0)) for M in MASSES)
    P(f'           dP/drho strictly decreasing in x on the grid for all four masses: {mono}')
    NUM['R_prof_monotone'] = mono

    # ---------------------------------------------------------------- exit
    P()
    fails_lb = [c['name'] for c in CHECKS if c['load_bearing'] and not c['ok']]
    fails_rep = [c['name'] for c in CHECKS if not c['load_bearing'] and not c['ok']]
    n_lb = sum(1 for c in CHECKS if c['load_bearing'])
    P(f'SUMMARY: {n_lb - len(fails_lb)}/{n_lb} load-bearing checks pass; reported rows failing their line: '
      f'{len(fails_rep)}')
    for f in fails_lb:
        P(f'  load-bearing FAIL: {f}')
    for f in fails_rep:
        P(f'  reported-row miss: {f}')
    code = 0 if not fails_lb else 1
    P(f'exit code {code} (main must exit 0; MUTATE must exit 1).  Runtime {time.time() - T_START:.1f} s')
    P('kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.')
    NUM['checks'] = CHECKS
    NUM['exit_code'] = code
    NUM['runtime_s'] = time.time() - T_START
    with open(os.path.join(HERE, TAG + '.out'), 'w') as fh:
        fh.write('\n'.join(LINES) + '\n')

    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o
    with open(os.path.join(HERE, TAG + '_results.json'), 'w') as fh:
        json.dump(clean(NUM), fh, indent=1)
    return code


if __name__ == '__main__':
    sys.exit(main())
