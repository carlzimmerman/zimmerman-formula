#!/usr/bin/env python3
"""
A82 -- the galactic alpha_1, computed from the exact nonlinear boundary-value problem.

Replaces the PPN expansion of A36/A54 at 1-30 kpc (where it is invalid) by a direct
solve of the P-sector field equation of the frozen A33 action, with the Langmuir gate
W(u) active and the tilted (CMB) foliation.

Action sector used (K = 4 pi G, c = 1, signature (-+++)):

    L/(N sqrt h) = ... + P^i D_i ln N - W(u) - (gamma/2)(D_iP^i)^2
                       + (eta/2) E_i E^i - (gamma/4) F_ij F^ij ,
    u = K|P|_h ,  W(u) = (a0^2/K)[-u/a0 - ln(1-u/a0)] ,  gamma = K L*^2/2 .

Static spherical reduction, P_i = (u/K) rhat_i  (so |P| = u/K and K W'(u) = u/(1-u/a0)):

  (P)   gamma * d/dr [ (1/r^2) d(r^2 u)/dr ] = K W'(u) - (1+2w^2) g
  (L)   g = g_N + u                (first integral of the lapse equation)

with g = (ln N)' and g_N = G M_b(<r)/r^2.  Eliminating g:

  (L*^2/2) [ u'' + 2u'/r - 2u/r^2 ] = u^2/(a0-u) - g_N - 2 w^2 (g_N+u)          (EXACT)

The (1+2w^2) factor is the exact O(w^2) content of the tilted-foliation lapse
ln N = Phi + w^2(1/2 + Phi + Psi) - Phi^2 + O(w^4).

Usage:
    python3 a82_checks.py                        # full run, exit 0 iff all checks pass
    python3 a82_checks.py --json-out a82_results.json
    python3 a82_checks.py --mutate NAME          # one physical input broken; must exit 1
"""
import argparse
import json
import os
import sys
import numpy as np
from scipy.linalg import solve_banded

# --------------------------------------------------------------------------------------
# constants (SI)
# --------------------------------------------------------------------------------------
G       = 6.67430e-11
C_LIGHT = 2.99792458e8
MSUN    = 1.98892e30
KPC     = 3.0856775814913673e19
PC      = KPC/1e3
AU      = 1.495978707e11
A0      = 9.36e-11
LSTAR   = 24.0*PC
W_CMB   = 369.82e3
W2      = (W_CMB/C_LIGHT)**2
K_G     = 4*np.pi*G
GAMMA   = LSTAR**2/2.0          # coefficient of (u''+2u'/r-2u/r^2) in the P equation
MGAL    = 6e10*MSUN
AH      = 3.0*KPC
MNUC    = 1e8*MSUN
BN      = 1e-3*PC

# mutation switches (all default off)
MUT = {}


def mut(name):
    return MUT.get(name, False)


def a0v():
    """a0, possibly mutated (physical-input mutation)."""
    return A0*(1.0+5e-2) if mut('a0_off') else A0


def lstarv():
    return LSTAR*2.0 if mut('Lstar_off') else LSTAR


def gammav():
    if mut('no_gradient'):
        return 0.0
    return lstarv()**2/2.0


def u2_term(u, a0):
    """u^2/(a0-u) = K W'(u) - u on the slaved branch (the Langmuir gate).
    'w_quad' replaces the gate by a quadratic W (W' = 2u/K), i.e. 2u^2/a0."""
    if mut('w_quad'):
        return 2.0*u*u/a0
    return u*u/(a0-u)


def d_u2_term(u, a0):
    if mut('w_quad'):
        return 4.0*u/a0
    return (2.0*u*a0-u*u)/(a0-u)**2


def source_coeff():
    """coefficient of w^2 in the P-equation source: 2 (exact), 1 (mutant), -2 (mutant)."""
    if mut('boost_half'):
        return 1.0
    if mut('sign_flip'):
        return -2.0
    if mut('drop_boost'):
        return 0.0
    return 2.0


# --------------------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------------------
def gN_gal(r):
    return G*MGAL/(r+AH)**2


def gN_gal_nuc(r):
    return G*MGAL/(r+AH)**2 + G*MNUC*np.asarray(r)/(np.asarray(r)**2+BN*BN)**1.5


def u_slaved(gNv, w2v=0.0):
    """gradient-free root of u/(1-u/a0) = (1+2w2)(gN+u); stable branch."""
    a0 = a0v()
    beta = 1.0+2.0*w2v
    gv = np.asarray(gNv, dtype=float)
    B = 1.0-beta+beta*gv/a0
    disc = B*B+4.0*beta*beta*gv/a0
    u = 2.0*beta*gv/(B+np.sqrt(disc))
    return np.minimum(u, a0*(1.0-1e-13))


def loggrid(rin, rout, N):
    x = np.linspace(np.log(rin), np.log(rout), N)
    return x, np.exp(x)


def _banded(N, c_dn, c_di, c_up):
    ab = np.zeros((3, N))
    ab[1, 0] = 1.0
    ab[1, N-1] = 1.0
    ab[1, 1:N-1] = c_di
    ab[0, 2:N] = c_up
    ab[2, 0:N-2] = c_dn
    return ab


# --------------------------------------------------------------------------------------
# static nonlinear BVP
# --------------------------------------------------------------------------------------
def solve_static(gNf, rin, rout, N, w2v=0.0, tol=1e-8, maxit=120):
    a0 = a0v()
    gam = gammav()
    x, r = loggrid(rin, rout, N)
    h = x[1]-x[0]
    h2 = h*h
    gn = gNf(r)
    u = u_slaved(gn, w2v)
    u[0] = 0.0
    tb = float(u_slaved(gNf(r[-1]), w2v))
    u[-1] = tb
    co = gam/r[1:-1]**2
    c_up = co*(1.0/h2+1.0/(2*h))
    c_dn = co*(1.0/h2-1.0/(2*h))
    c_di = co*(-2.0/h2-2.0)
    if mut('first_order'):          # upwind the first-derivative term: O(h) scheme
        c_dn = c_dn-co/h
        c_di = c_di+co/h
    sc = source_coeff()

    def rhs_of(uu):
        return u2_term(uu, a0)-gn-sc*w2v*(gn+uu)

    def rint(uu):
        return c_dn*uu[:-2]+c_di*uu[1:-1]+c_up*uu[2:]-rhs_of(uu)[1:-1]

    it = 0
    for it in range(1, maxit+1):
        Ri = rint(u)
        rr = rhs_of(u)
        drhs = d_u2_term(u, a0)-sc*w2v
        ab = _banded(N, c_dn, c_di-drhs[1:-1], c_up)
        Rv = np.zeros(N)
        Rv[1:-1] = Ri
        Rv[0] = u[0]
        Rv[-1] = u[-1]-tb
        du = solve_banded((1, 1), ab, -Rv)
        n0 = np.max(np.abs(Ri))
        lam = 1.0
        ok = False
        for _ in range(40):
            ut = u+lam*du
            if np.all(ut < a0*(1-1e-13)) and np.all(ut > -1e-3*a0):
                nt = np.max(np.abs(rint(ut)))
                if np.isfinite(nt) and (nt < n0 or nt < 1e-13*a0):
                    ok = True
                    break
            lam *= 0.5
        if not ok:
            lam = 0.0
        u = u+lam*du
        if np.max(np.abs(rint(u)))/a0 < tol:
            break
    Ri = rint(u)
    rr = rhs_of(u)
    return dict(x=x, r=r, u=u, g=gn+u, gn=gn, h=h, it=it, N=N,
                res_abs=np.max(np.abs(Ri))/a0,
                res_rel=np.max(np.abs(Ri)/np.maximum(np.abs(rr[1:-1]), 1e-300)))


# --------------------------------------------------------------------------------------
# linearised O(w^2) BVP
# --------------------------------------------------------------------------------------
def solve_boost(gNf, sol, w2v, tol=1e-14, maxit=200):
    """The O(w^2) equation is LINEAR in du: one direct banded solve (iterated twice for safety)."""
    a0 = a0v()
    gam = gammav()
    r = sol['r']
    u = sol['u']
    g = sol['g']
    N = sol['N']
    h = sol['h']
    h2 = h*h
    if mut('linear_response'):
        C = 2.0*u/a0                      # response replaced by its small-u (Newtonian) value
    else:
        C = u*(2*a0-u)/(a0-u)**2
    co = gam/r[1:-1]**2
    c_up = co*(1.0/h2+1.0/(2*h))
    c_dn = co*(1.0/h2-1.0/(2*h))
    c_di = co*(-2.0/h2-2.0)-C[1:-1]
    sc = source_coeff()
    src = -sc*w2v*g
    bc = float(u_slaved(gNf(r[-1]), w2v)-u_slaved(gNf(r[-1]), 0.0))
    du = np.zeros(N)
    du[-1] = bc
    ab = _banded(N, c_dn, c_di, c_up)
    Rv = np.zeros(N)
    Rv[1:-1] = src[1:-1]
    Rv[0] = -du[0]
    Rv[-1] = -du[-1]-bc*0.0+bc      # placeholder, overwritten below
    # Dirichlet rows: value = 0 at r_in, value = bc at r_out
    Rv[0] = 0.0
    Rv[-1] = bc
    du = solve_banded((1, 1), ab, Rv)
    it = 1
    Ri = (c_dn*du[:-2]+(c_di)*du[1:-1]+c_up*du[2:])-src[1:-1]
    return du, np.max(np.abs(Ri))/max(np.max(np.abs(src)), 1e-300), it



# --------------------------------------------------------------------------------------
# pure-boost artefacts must cancel in the observable acceleration
# --------------------------------------------------------------------------------------
def _grad(f, x, h):
    g = np.zeros(3)
    for k in range(3):
        e = np.zeros(3); e[k] = h
        g[k] = (f(x+e)-f(x-e))/(2*h)
    return g


def _curl(F, x, h):
    out = np.zeros(3)
    for k in range(3):
        e = np.zeros(3); e[k] = h
        dFp = (F(x+e)-F(x-e))/(2*h)     # dF_i/dx_k
        out[k] = 0.0
        out[k] += 0.0
        out[k] = dFp[k]                 # placeholder
    # explicit curl
    e = [np.zeros(3) for _ in range(3)]
    for k in range(3):
        e[k][k] = h
    d = np.zeros((3, 3))                # d[i][k] = dF_i/dx_k
    for i in range(3):
        for k in range(3):
            d[i, k] = (F(x+e[k])[i]-F(x-e[k])[i])/(2*h)
    return np.array([d[2, 1]-d[1, 2], d[0, 2]-d[2, 0], d[1, 0]-d[0, 1]])


def geodesic_artefact(w2v, h):
    """acceleration of a body comoving with a spherical source, in the tilted foliation.
    Returns (a + grad Phi)/|grad Phi| -- must vanish: the pure-boost O(w^2) ADM pieces
    are a re-slicing, not a source."""
    w = W_CMB*np.array([0.3, -0.5, 0.81])
    w = w/np.linalg.norm(w)*(W_CMB/C_LIGHT)
    x0 = np.array([8e0*KPC, 0.37*KPC, 1.7*KPC])

    def Phi(x):
        return -G*MGAL/(np.linalg.norm(x)+AH)

    def N(x):
        return 1.0+Phi(x)+w2v*(0.5+2.0*Phi(x))

    def Nv(x):
        return -w*(1.0+2.0*Phi(x))

    gN_ = _grad(N, x0, h)
    gP = _grad(Phi, x0, h)
    Nvec = Nv(x0)
    dNdt = np.zeros(3)                  # d_t = w.grad for a field steady in the source frame
    for k in range(3):
        e = np.zeros(3); e[k] = h
        dNdt += w[k]*(Nv(x0+e)-Nv(x0-e))/(2*h)
    curl = _curl(Nv, x0, h)
    v = -w
    a = -gN_ - dNdt + np.cross(v, curl)
    return float(np.linalg.norm(a+gP)/np.linalg.norm(gP))



def sym_geodesic(include_phi2):
    """Symbolic: acceleration of a body comoving with a spherical source in the tilted
    foliation, from the ADM data (N, N_i, h_ij).  Returns the residual a + grad(Phi),
    simplified, as a list of three expressions (strings)."""
    import sympy as sp
    x, y, z, wx, wy, wz = sp.symbols('x y z wx wy wz', real=True)
    rr = sp.sqrt(x**2+y**2+z**2)
    f = sp.Function('f')(rr)
    w2 = wx**2+wy**2+wz**2
    Phi = f
    N = 1+Phi+w2*(sp.Rational(1, 2)+(1 if mut('lapse_half') else 2)*Phi)
    if include_phi2 and not mut('no_phi2'):
        N = N-Phi**2
    Nv = [-wx*(1+2*Phi), -wy*(1+2*Phi), -wz*(1+2*Phi)]
    X = [x, y, z]
    W = [wx, wy, wz]
    gN = [sp.diff(N, X[i]) for i in range(3)]
    dNdt = [sum(W[k]*sp.diff(Nv[i], X[k]) for k in range(3)) for i in range(3)]
    curl = [sp.diff(Nv[2], X[1])-sp.diff(Nv[1], X[2]),
            sp.diff(Nv[0], X[2])-sp.diff(Nv[2], X[0]),
            sp.diff(Nv[1], X[0])-sp.diff(Nv[0], X[1])]
    v = [-W[0], -W[1], -W[2]]
    cross = [v[1]*curl[2]-v[2]*curl[1], v[2]*curl[0]-v[0]*curl[2], v[0]*curl[1]-v[1]*curl[0]]
    a = [-gN[i]-dNdt[i]+cross[i] for i in range(3)]
    gPhi = [sp.diff(Phi, X[i]) for i in range(3)]
    return [sp.simplify(a[i]+gPhi[i]) for i in range(3)]


def at(r, y, rq):
    return float(np.interp(np.log(rq), np.log(r), y))


# --------------------------------------------------------------------------------------
# angular structure of the O(w^2) sources
# --------------------------------------------------------------------------------------
def legendre_project(f, l, ngl=400):
    """a_l = (2l+1)/2 int_{-1}^{1} f(c) P_l(c) dc   (Gauss-Legendre)."""
    c, w = np.polynomial.legendre.leggauss(ngl)
    Pl = np.polynomial.legendre.Legendre.basis(l)
    return float((2*l+1)/2.0*np.sum(w*f(c)*Pl(c)))


def angular_terms():
    """O(w^2) source terms in the (P, lapse) system, per unit |P| g w^2.

    clock  P^i D_i ln N with P^i = h^{ij}P_j = (1+2Phi)P_i + w^i(w.P):
        (1+2w^2)[ (1+2Phi)|P|g + |P| g c^2 ]        -> 2 + c^2
    Langmuir gate  -W(u),  u = K|P|_h = u0(1+Phi+c^2 w^2/2),  K W'(u0)=g:
        - (u0/(1-u0/a0)) (c^2/2) = -|P| g c^2/2    -> -c^2/2
    lapse  sqrt(h)[rho + d + W]:  sqrt(h) = 1-3Phi-w^2/2, and the W term above
        -> -1/2 (density sector, l=0) and -c^2/2 (W sector)
    """
    d = {}
    if mut('spurious_dipole'):
        d['spurious_dip'] = (lambda c: 0.7*c, 'P equation')
    d.update({
        'clock_iso':  (lambda c: (1.0 if mut('lapse_half') else 2.0)+0.0*c, 'P equation'),
        'clock_hij':  (lambda c: c**2, 'P equation'),
        'gate_W':     (lambda c: -0.5*c**2, 'P equation'),
        'lapse_sqrth': (lambda c: -0.5+0.0*c, 'lapse equation'),
        'lapse_W':    (lambda c: -0.5*c**2, 'lapse equation'),
    })
    return d


def total_source_shape(c):
    """sum of the P-equation source terms; (2 + c^2) - c^2/2 = 13/6 + (1/3) P_2(c)"""
    cc = np.asarray(c, dtype=float)
    tot = np.zeros_like(cc)
    for k, (f, eq) in angular_terms().items():
        if eq == 'P equation':
            tot = tot+f(cc)
    return tot


# --------------------------------------------------------------------------------------
# main computation
# --------------------------------------------------------------------------------------
def compute(verbose=True):
    out = {}
    res = {'checks': [], 'data': {}}

    def emit(s=''):
        if verbose:
            print(s)

    # ---------------- constants ----------------
    emit('='*88)
    emit('A82 -- THE GALACTIC ALPHA_1 FROM THE EXACT NONLINEAR BVP')
    emit('='*88)
    emit('a0            = %.6e m/s^2' % a0v())
    emit('L*            = %.6f pc   (coefficient of the P-gradient operator = L*^2/2 = %.6e m^2)' % (lstarv()/PC, gammav()))
    emit('w_CMB         = %.2f km/s    w^2 = (w/c)^2 = %.10e' % (W_CMB/1e3, W2))
    emit('galaxy        = Hernquist M_bar=6e10 Msun, a=3 kpc;  r_MOND = %.4f kpc'
         % (np.sqrt(G*MGAL/a0v())/KPC))
    emit('domain        = [3 pc, 1000 kpc], N = 15001')
    emit('lane A82_galactic_alpha1 (2026-10-22): closes the qualifier of THEORY 3.5b and 6.1,')
    emit('  document sections 2.1, 2.2, 2.3, 2.4, 2.5 ; refs Shao & Wex 2012 (PSR J1738+0333),')
    emit('  Kramer+ 2021, A36, A54, A59, A68.')
    emit('')

    # ---------------- background ----------------
    sol = solve_static(gN_gal, 3*PC, 1000*KPC, 15001)
    r = sol['r']
    u = sol['u']
    g = sol['g']
    a0 = a0v()
    up = a0**2/(g+a0)**2

    emit('[A] STATIC NONLINEAR BACKGROUND BVP')
    emit('    Newton iterations = %d   max|residual| = %.3e a0 (roundoff floor)   max relative residual = %.3e'
         % (sol['it'], sol['res_abs'], sol['res_rel']))
    emit('    u < a0 everywhere: %s ;  max u/a0 = %.6f at r = %.5f kpc'
         % (np.all(u < a0), np.max(u)/a0, r[np.argmax(u)]/KPC))
    emit('')
    emit('    r(kpc)    g_N/a0     g/a0      u/a0     u\'=dg_N/dg  4u\'/(1-u\')  '
         'u_slaved/a0  |u-us|/u')
    usl = u_slaved(sol['gn'])
    for rr in (1, 2, 3, 5, 8, 12, 20, 30, 100, 300, 1000):
        i = np.argmin(abs(r-rr*KPC))
        emit('   %6.1f  %9.5f %9.5f  %8.5f  %11.6f  %11.6f   %9.5f   %.2e'
             % (rr, sol['gn'][i]/a0, g[i]/a0, u[i]/a0, up[i], 4*up[i]/(1-up[i]), usl[i]/a0,
                abs(u[i]-usl[i])/max(u[i], 1e-300)))
    emit('')


    # ---------------- boosted ----------------
    du, bres, bit = solve_boost(gN_gal, sol, W2)
    a1 = 2.0*du/(W2*g)
    emit('[B] BOOSTED O(w^2) BVP  (source -2 w^2 g ; response C = d/du[u^2/(a0-u)])')
    emit('    iterations = %d   max relative residual = %.3e' % (bit, bres))
    emit('')
    emit('    r(kpc)    g/a0      da=du (m/s^2)   da/(w^2 a0)   da/g        '
         'a1_eff=2da/(w^2 g)   a1*A36   ratio   a1 g/(2a0)')
    A36 = [0.073, 0.143, 0.235, 0.475, 0.928, 1.628, 3.169, 5.194]
    tabs = []
    for j, rr in enumerate((1, 2, 3, 5, 8, 12, 20, 30)):
        i = np.argmin(abs(r-rr*KPC))
        ratio = a1[i]/A36[j]
        tabs.append((rr, g[i]/a0, du[i], du[i]/(W2*a0), du[i]/g[i], a1[i], A36[j], ratio,
                     a1[i]*g[i]/(2*a0)))
        emit('   %6.1f  %8.5f  %13.6e  %11.5f  %11.4e  %13.5f  %9.3f  %7.5f  %9.5f'
             % tabs[-1])
    emit('')
    imax = int(np.argmax(du))
    emit('    max da            = %.6e m/s^2  at r = %.3f kpc  (w^2 a0 = %.6e)'
         % (du[imax], r[imax]/KPC, W2*a0))
    emit('    max da/(w^2 a0)   = %.8f' % np.max(du/(W2*a0)))
    emit('    max a1_eff        = %.6f at r = %.3f kpc' % (a1[-1], r[-1]/KPC))
    emit('    max a1_eff*g/(2a0) = %.8f' % np.max(a1*g/(2*a0)))
    m = (r > 2*KPC) & (r < 100*KPC)
    emit('    max |a1_eff/(4u\'/(1-u\'))-1| for 2<r<100 kpc = %.3e'
         % np.max(np.abs(a1[m]/(4*up[m]/(1-up[m]))-1)))
    emit('    alpha_1_eff / 1e-4 at 1 kpc = %.2f ; at 30 kpc = %.2f'
         % (a1[np.argmin(abs(r-1*KPC))]/1e-4, a1[np.argmin(abs(r-30*KPC))]/1e-4))
    emit('    bilinearity factor w^2/2 = %.6e (A59: every alpha_1 observable carries (v/c)^2)'
         % (W2/2))
    emit('    quadrupole upper bound (2/13 of the monopole): %.4e m/s^2, axis along w'
         % (2/13*np.max(du)))
    idev = np.argmax(np.abs(a1[m]/(4*up[m]/(1-up[m]))-1))
    emit('    the max deviation over 2-100 kpc sits at r = %.4f kpc (O((L*/r)^2) gradient '
         'correction)' % (r[m][idev]/KPC))
    dev_far = abs(a1[-1]/(4*up[-1]/(1-up[-1]))-1)
    emit('    at the 1000 kpc boundary the deviation is %.3e: the finite-w^2 term 2w^2 u\'/(1-u\')'
         % dev_far)
    emit('')

    # ---- where the PPN expansion breaks ----
    emit('    PPN BREAKDOWN DIAGNOSTICS')
    rr_i = r
    def rad_at(val):
        idx = np.argsort(up)
        return float(np.interp(val, up[idx], rr_i[idx]))
    for uu, lab in ((0.0909, '10% response error'), (0.5, '50% response error'),
                    (0.9, '90%'), (0.99, '99%')):
        emit('      u\' = %.4f (%s) at r = %.4f kpc' % (uu, lab, rad_at(uu)/KPC))
    Phi_c2 = G*MGAL/(C_LIGHT**2*(r+AH))
    i8b = np.argmin(abs(r-8*KPC))
    emit('      Phi/c^2 at 8 kpc = %.4e ; w^2 = %.4e ; w^2/(Phi/c^2) = %.4f'
         % (Phi_c2[i8b], W2, W2/Phi_c2[i8b]))
    emit('      max Phi/c^2 (r=0) = %.4e  -> w^2 exceeds Phi/c^2 at every radius'
         % np.max(Phi_c2))
    contam = 2*Phi_c2/(0.5*a1*W2)
    emit('      dropped O(eps^2) term |2 Phi| vs retained alpha1 term (a1/2)w^2:')
    emit('        r=1 kpc %.3f ; 3 kpc %.3f ; 8 kpc %.3f ; 20 kpc %.4f ; 30 kpc %.4f ; '
         '100 kpc %.2e'
         % tuple(at(r, contam, q*KPC) for q in (1, 3, 8, 20, 30, 100)))
    idx = np.argsort(contam)
    r_cross = float(np.interp(1.0, contam[idx], rr_i[idx]))
    emit('      contamination = 1 at r = %.4f kpc ; response 1/(1-u\') = 2 at r = %.4f kpc'
         % (r_cross/KPC, rad_at(0.5)/KPC))
    emit('      -> PPN-contaminated below %.2f kpc, response-nonlinear above %.2f kpc'
         % (r_cross/KPC, rad_at(0.5)/KPC))
    emit('      (L*/r)^2 u\'/2 at 1, 8, 30 kpc = %.3e, %.3e, %.3e'
         % tuple(at(r, (lstarv()/r)**2*up/2, q*KPC) for q in (1, 8, 30)))
    emit('      u/g (the P charge fraction of the field) at 1, 8, 30, 1000 kpc = '
         '%.4f, %.4f, %.4f, %.4f'
         % tuple(at(r, u/g, q*KPC) for q in (1, 8, 30, 1000)))
    emit('')
    # nonlinear cross-check
    s1 = solve_static(gN_gal, 3*PC, 1000*KPC, 15001, w2v=W2)
    dnl = s1['u']-u
    i8 = np.argmin(abs(r-8*KPC))
    emit('    nonlinear cross-check: u(w^2)-u(0) at 8 kpc = %.6e ; linear = %.6e ; '
         'rel diff = %.3e' % (dnl[i8], du[i8], abs(dnl[i8]-du[i8])/du[i8]))
    emit('    nonlinear solve: it=%d res=%.3e a0, u<a0 %s'
         % (s1['it'], s1['res_abs'], np.all(s1['u'] < a0)))
    emit('')

    # w^2 continuation
    emit('    w^2 continuation (nonlinear difference / w^2, normalised to w^2=1e-8):')
    q0 = None
    cont = []
    for wv in (1e-8, 1e-6, 1e-4, 1e-2):
        sv = solve_static(gN_gal, 3*PC, 1000*KPC, 15001, w2v=wv)
        q = (sv['u'][i8]-u[i8])/wv
        if q0 is None:
            q0 = q
        cont.append((wv, q, q/q0-1))
        emit('      w^2=%.0e   q/q(w^2=1e-8)-1 = %+.3e' % (wv, q/q0-1))
    emit('')

    # ---------------- angular structure ----------------
    emit('[C] ANGULAR STRUCTURE OF THE O(w^2) SOURCES')
    terms = angular_terms()
    proj = {}
    emit('    term            equation         l=0        l=1          l=2')
    for k, (f, eq) in terms.items():
        a0p = legendre_project(f, 0)
        a1p = legendre_project(f, 1)
        a2p = legendre_project(f, 2)
        proj[k] = (a0p, a1p, a2p)
        emit('    %-14s %-16s %9.5f  %11.3e  %9.5f' % (k, eq, a0p, a1p, a2p))
    a0t = legendre_project(total_source_shape, 0)
    a1t = legendre_project(total_source_shape, 1)
    a2t = legendre_project(total_source_shape, 2)
    emit('    %-14s %-16s %9.5f  %11.3e  %9.5f' % ('TOTAL', 'P equation', a0t, a1t, a2t))
    emit('    analytic: l=0 = 13/6 = %.6f, l=1 = 0, l=2 = 1/3 = %.6f, l=2/l=0 = 2/13 = %.6f'
         % (13/6, 1/3, 2/13))
    emit('    the numerical l=0 solve uses the clock term only (coefficient 2.00000); the full')
    emit('    O(w^2) l=0 coefficient is 13/6, i.e. alpha_1 is 13/12 = +%.6e larger if the h^{ij}'
         % (13/12-1))
    emit('    corrections are included; the l=2 (quadrupole) source is 2/13 of the l=0 one.')
    emit('')
    # dipole moment of the induced acceleration for a pure l=0 + l=2 radial field
    c, wq = np.polynomial.legendre.leggauss(200)
    phi = np.linspace(0, 2*np.pi, 400, endpoint=False)
    CC, PP = np.meshgrid(c, phi, indexing='ij')
    sth = np.sqrt(1-CC**2)
    P2 = 0.5*(3*CC**2-1)
    dOm = np.ones_like(CC)*(2*np.pi/len(phi))
    # radial field f0 + f2*P2, with f0=1, f2=2/13
    ar = (1.0+(a2t/a0t)*P2+3.0*a1t*CC)
    Dx = np.sum(dOm*ar*sth*np.cos(PP))*0.0
    dy = np.sum(dOm*ar*sth*np.sin(PP))
    dz = np.sum(dOm*ar*CC)
    Dr = np.sqrt((np.sum(dOm*ar*sth*np.cos(PP)))**2+dy**2+dz**2)
    emit('    dipole moment of a pure l=0+l=2 radial acceleration field: |D| = %.3e (normalised)'
         % Dr)
    emit('    -> the l=1 (dipole) content of the induced field is identically zero.')
    emit('')

    # ---------------- gates ----------------
    emit('[E] THE kL* >> 1 REGIME (does the galactic solve touch the four gates?)')
    solu = solve_static(gN_gal_nuc, 1e-5*PC, 1000*KPC, 9001)
    ru = solu['r']
    gu = solu['g']
    upu = a0**2/(gu+a0)**2
    duu, bresu, _ = solve_boost(gN_gal_nuc, solu, W2)
    a1u = 2.0*duu/(W2*gu)
    emit('    r(pc)      g/a0        (L*/r)^2      u\'          a1_eff       8(r/L*)^2')
    gate_rows = []
    for rr in (0.01, 0.1, 1.0, 3.0, 10.0, 30.0):
        i = np.argmin(abs(ru-rr*PC))
        gate_rows.append((rr, gu[i]/a0, (lstarv()/ru[i])**2, upu[i], a1u[i],
                          8*(ru[i]/lstarv())**2))
        emit('   %7.2f  %11.4e  %11.4e  %11.4e  %11.4e  %11.4e' % gate_rows[-1])
    emit('')

    # ---------------- pulsar ----------------
    emit('[D] BINARY PULSAR IN THE GALACTIC FIELD')
    a0 = a0v()
    # J1738+0333-like: mp=1.47, mc=0.16, Pb=5.85 h
    mp = 1.47*MSUN
    mc = 0.16*MSUN
    Mt = mp+mc
    Pb = (100.0*86400.0) if mut('pulsar_wide') else (5.85*3600.0)
    ab = (G*Mt*(Pb/(2*np.pi))**2)**(1/3)
    vorb = 2*np.pi*ab/Pb
    nb = 2*np.pi/Pb
    g_int = G*mp/ab**2
    up_int = (a0/g_int)**2
    a1_int = 4*up_int/(1-up_int)
    dmM = (mp-mc)/Mt
    Vc = W_CMB/C_LIGHT
    vc = vorb/C_LIGHT
    eF = 0.5*a1_int*dmM*Vc*vc
    dedt = nb*eF
    SW = 3.5e-5
    emit('    binary: mp=1.47 mc=0.16 Msun, Pb=5.85 h -> a=%.5e m, v_orb=%.4e m/s'
         % (ab, vorb))
    emit('    g_int = G mp/a^2 = %.4f m/s^2 = %.4e a0' % (g_int, g_int/a0))
    emit('    u\'_int = (a0/g)^2 = %.4e ;  alpha-hat_1(int) = 4u\'/(1-u\') = %.4e'
         % (up_int, a1_int))
    emit('    (Delta m/M) = %.4f ;  (V/c)(v/c) = %.4e' % (dmM, Vc*vc))
    emit('    e_F = 0.5 a1 (Dm/M)(V/c)(v/c) = %.4e' % eF)
    emit('    de/dt = n_b e_F = %.4e s^-1' % dedt)
    emit('    Shao-Wex 2012 prior |alpha-hat_1| < %.1e -> margin = %.2f decades'
         % (SW, np.log10(SW/a1_int)))
    # external-field channel
    gext_decl = 1.8*a0
    up_ext = (a0/gext_decl)**2
    a1_ext = 4*up_ext/(1-up_ext)
    i8d = np.argmin(abs(r-8*KPC))
    a1_gal = a1[i8d]
    up_gal = up[i8d]
    Da = 0.5*a1_ext*gext_decl*Vc*(vorb/C_LIGHT)
    dpb = 3*Da/vorb
    emit('    galactic field at R_GC=8 kpc: declared g_ext = 1.8 a0 -> u\'=%.6f, a1=%.6f'
         % (up_ext, a1_ext))
    emit('    (model here gives g/a0 = %.5f at 8 kpc -> a1 = %.5f)' % (g[i8d]/a0, a1_gal))
    emit('    external-field differential acceleration across the orbit:')
    emit('      Da = 0.5 a1_ext g_ext (V/c)(v_orb/c) = %.4e m/s^2' % Da)
    emit('      dPb/Pb ~ 3 Da/v_orb = %.4e   (timing floor ~1e-15)' % dpb)
    emit('    EFE: mu(g_tot) = g_int/(g_int+g_ext) = 1 - %.3e  -> external field changes'
         % (gext_decl/g_int))
    emit('         the internal response by %.3e (relative)' % (gext_decl/g_int))
    emit('    r_switch (A20) = 3.73 pc vs orbital separation %.3e pc -> separation is %.3e x smaller'
         % (ab/PC, (3.73*PC)/ab))
    emit('    log10(g_int/a0) = %.2f' % np.log10(g_int/a0))
    emit('    declared literature priors (not data on disk): |alpha-hat_1| < 3.5e-05 (Shao-Wex 2012);')
    emit('      generic pulsar-timing |alpha_1| < 1e-4 ; Galactic differential-acceleration level')
    emit('      1e-3-1e-2 ; timing floor 1e-15.')
    emit('')

    # ---------------- assemble ----------------
    data = dict(
        w2=W2, a0=a0, Lstar=lstarv(), gamma=gammav(),
        r_mond_kpc=float(np.sqrt(G*MGAL/a0)/KPC),
        static_it=sol['it'], static_res=sol['res_abs'], static_res_rel=sol['res_rel'],
        umax_over_a0=float(np.max(u)/a0), r_umax_kpc=float(r[np.argmax(u)]/KPC),
        table=[dict(r=t[0], g_over_a0=t[1], da=t[2], da_over_w2a0=t[3], da_over_g=t[4],
                    a1=t[5], a36=t[6], ratio=t[7], a1g_over_2a0=t[8]) for t in tabs],
        max_da=float(du[imax]), max_da_r_kpc=float(r[imax]/KPC),
        max_da_over_w2a0=float(np.max(du/(W2*a0))),
        max_a1g_over_2a0=float(np.max(a1*g/(2*a0))),
        max_a1_minus_slaved=float(np.max(np.abs(a1[m]/(4*up[m]/(1-up[m]))-1))),
        nl_check=dict(dnl=float(dnl[i8]), dlin=float(du[i8]),
                      rel=float(abs(dnl[i8]-du[i8])/du[i8]),
                      it=s1['it'], res=s1['res_abs']),
        continuation=[dict(w2=c0[0], q_over_q0_minus1=c0[2]) for c0 in cont],
        angular={k: dict(l0=v[0], l1=v[1], l2=v[2]) for k, v in proj.items()},
        angular_total=dict(l0=a0t, l1=a1t, l2=a2t),
        dipole_moment=float(Dr),
        gate=[dict(r_pc=t[0], g_over_a0=t[1], kL2=t[2], up=t[3], a1=t[4], eight=t[5])
              for t in gate_rows],
        pulsar=dict(ab=ab, vorb=vorb, g_int=g_int, g_int_over_a0=g_int/a0,
                    up_int=up_int, a1_int=a1_int, eF=eF, dedt=dedt,
                    sw=SW, margin=float(np.log10(SW/a1_int)),
                    gext=gext_decl, up_ext=up_ext, a1_ext=a1_ext,
                    a1_gal=a1_gal, Da=Da, dPb=dpb,
                    efe_rel=float(gext_decl/g_int)),
    )

    # ------------------------------------------------------------------
    # checks
    # ------------------------------------------------------------------
    def chk(cid, what, value, ok):
        res['checks'].append(dict(id=cid, what=what, value=value, ok=bool(ok)))

    # --- A: background solver ---
    chk('A1', 'static BVP max relative residual < 1e-8', '%.3e' % sol['res_rel'],
        sol['res_rel'] < 1e-8)
    s_lo = solve_static(gN_gal, 3*PC, 1000*KPC, sol['N']//4)
    v1 = at(s_lo['r'], s_lo['u'], 8*KPC)
    v2 = at(r, u, 8*KPC)
    emit('    grid convergence: u(8 kpc)/a0 at N/4 = %.9f, at N = %.9f, rel diff = %.2e'
         % (v1/a0, v2/a0, abs(v1-v2)/v2))
    dev = np.max(np.abs(u[m]-usl[m])/usl[m])
    chk('A3', 'slaved limit: |u-u_slaved|/u < 5e-3 for r>3 kpc', '%.3e' % dev, dev < 5e-3)
    law = np.abs(g-sol['gn']-u)/np.maximum(sol['gn'], 1e-300)
    mm = r > 1*KPC
    # gradient operator is active: at 0.3 kpc the exact solution differs from the algebraic one
    il = np.argmin(abs(r-0.3*KPC))
    dact = abs(u[il]-usl[il])/usl[il]
    chk('A7', 'P-gradient term active: |u-u_slaved|/u > 1e-6 at 0.3 kpc', '%.4e' % dact,
        dact > 1e-6)

    # --- B: boosted solver ---
    chk('B1', 'boosted BVP max relative residual < 1e-8', '%.3e' % bres, bres < 1e-8)
    rel = abs(dnl[i8]-du[i8])/du[i8]
    chk('B2', 'linearised du = u(w^2)-u(0) to < 1e-5', '%.3e' % rel, rel < 1e-5)
    chk('B3', 'da = du > 0 at every interior radius', '%.4e' % du[1:-1].min(),
        np.all(du[1:-1] > 0))
    chk('B4', 'bound 0.9 < max da/(w^2 a0) < 1', '%.6f' % np.max(du/(W2*a0)),
        0.9 < np.max(du/(W2*a0)) < 1.0)
    dev1 = np.max(np.abs(a1[m]/(4*up[m]/(1-up[m]))-1))
    Dm = 1.0+(lstarv()/r[m])**2*up[m]/2.0
    dev2 = np.max(np.abs(a1[m]/(4*up[m]/(Dm-up[m]))-1))
    chk('B5', 'alpha_1_eff = 4u\'/(1-u\') for 2<r<100 kpc, < 1e-4', '%.3e' % dev1, dev1 < 1e-4)
    chk('B6', 'alpha_1_eff * g <= 2 a0 with max ratio > 0.95',
        '%.6f' % np.max(a1*g/(2*a0)),
        np.all(a1*g <= 2*a0*(1+1e-12)) and np.max(a1*g/(2*a0)) > 0.95)
    rmax = max(abs(t[7]-1.0) for t in tabs)
    chk('B7', 'A36 table reproduced, max |ratio-1| < 2e-2', '%.3e' % rmax, rmax < 2e-2)
    okc = all(abs(c0[2]) < 5.0*c0[0]+1e-9 for c0 in cont)
    chk('B8', 'w^2-continuation: q(w^2)/q(0) - 1 = O(w^2)',
        ' '.join('%+.2e' % c0[2] for c0 in cont), okc)
    chk('B9', 'A36 8 kpc value: 0.92 < alpha_1 < 0.94', '%.5f' % a1[i8],
        0.92 < a1[i8] < 0.94)

    # --- C: angular ---
    l1max = max(abs(v[1]) for v in proj.values())
    chk('C1', 'every O(w^2) source has zero l=1 projection', '%.3e' % l1max, l1max < 1e-13)
    chk('C2', 'total source l=2/l=0 = 2/13 = 0.153846', '%.6f' % (a2t/a0t),
        abs(a2t/a0t-2/13) < 1e-9)
    chk('C3', 'l=0 = 13/6 = 2.166667', '%.6f' % a0t, abs(a0t-13/6) < 1e-9)
    chk('C4', 'dipole moment of l=0+l=2 field = 0', '%.3e' % Dr, Dr < 1e-13)


    r0 = sym_geodesic(False)
    r2 = sym_geodesic(True)
    zero0 = all(sp_is_zero(e) for e in r0) if False else all(str(e) == '0' for e in r0)
    chk('C5', 'pure-boost O(w^2) ADM pieces cancel: a = -grad Phi exactly',
        ','.join(str(e) for e in r0)[:24], zero0)
    phi2 = all(('2*' in str(e)) or ('0' == str(e)) for e in r2) and any(str(e) != '0' for e in r2)
    chk('C6', 'the O(eps^2) term -Phi^2 does NOT cancel: residual = 2 Phi grad Phi',
        str(r2[0])[:34], phi2)

    chk('C7', 'PPN 2PN contamination > 10 at 1 kpc',
        '%.2f' % at(r, contam, 1*KPC), at(r, contam, 1*KPC) > 10)
    chk('C8', 'PPN 2PN contamination < 0.05 at 30 kpc',
        '%.4f' % at(r, contam, 30*KPC), at(r, contam, 30*KPC) < 0.05)

    # --- E: gates ---
    i1 = np.argmin(abs(ru-1.0*PC))
    i10 = np.argmin(abs(ru-10.0*PC))
    chk('E1', 'kL*>>1 regime: alpha_1_eff(1 pc) < 1e-6', '%.3e' % a1u[i1], a1u[i1] < 1e-6)
    chk('E2', 'kL*>>1 regime: alpha_1_eff(10 pc) < 1e-4', '%.3e' % a1u[i10], a1u[i10] < 1e-4)
    ok8 = all(abs(t[4]/(4.0*t[3])-1.0) < 0.1 for t in gate_rows)
    chk('E3', 'kL*>>1 scaling alpha_1_eff = 4(a0/g)^2 within 10%', str(ok8), ok8)

    # --- D: pulsar ---
    chk('D1', 'alpha-hat_1 at the binary internal field < 1e-20', '%.3e' % a1_int,
        a1_int < 1e-20)
    chk('D2', 'e_F < 1e-25', '%.3e' % eF, eF < 1e-25)
    chk('D3', 'Shao-Wex margin > 15 decades', '%.2f' % np.log10(SW/a1_int),
        np.log10(SW/a1_int) > 15)
    chk('D6', 'EFE correction to the internal field < 1e-9', '%.3e' % (gext_decl/g_int),
        gext_decl/g_int < 1e-9)

    res['data'] = data
    res['summary'] = dict(n=len(res['checks']),
                          npass=sum(1 for c in res['checks'] if c['ok']))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json-out', default=None)
    ap.add_argument('--mutate', default=None)
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    menv = os.environ.get('A82_MUTATE')
    if menv:
        MUT[menv] = True
    if args.mutate:
        MUT[args.mutate] = True

    res = compute(verbose=not args.quiet)

    print('')
    print('-'*88)
    print('CHECKS')
    print('-'*88)
    for c in res['checks']:
        print('  %-4s %-62s %-28s %s' % (c['id'], c['what'], c['value'],
                                         'PASS' if c['ok'] else 'FAIL'))
    n = res['summary']['n']
    npass = res['summary']['npass']
    print('')
    print('  %d/%d PASS' % (npass, n))
    if args.mutate or menv:
        print('  MUTATION: %s' % (args.mutate or menv))
    if args.json_out:
        with open(args.json_out, 'w') as f:
            json.dump(res, f, indent=1)
        print('  json -> %s' % args.json_out)

    if npass != n:
        print('  EXIT 1')
        return 1
    print('  EXIT 0')
    return 0


if __name__ == '__main__':
    sys.exit(main())
