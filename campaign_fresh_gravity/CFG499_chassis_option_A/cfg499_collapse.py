#!/usr/bin/env python3
"""CFG499 test (2): does gravitational collapse form the universal horizon (UH), and with which branch?

Criteria: FROZEN_CRITERIA.md section 3 (committed alone before any script, 3b820a1ec).

Model: marginally bound Oppenheimer-Snyder collapse (flat FRW dust ball, a(tau) = (-tau)^(2/3), comoving surface radius
chi_s = (9/2)^(1/3), M = 1) matched to Schwarzschild. At alpha_c = 0 the khronon equation is solved, for every lambda,
by any K = 0 slicing (the lambda K^2 stress vanishes with K), so the khronon is the maximal slicing that is
asymptotically the Schwarzschild time T. Leaves: interior tau = f(chi) with K = 0 and a regular centre, matched C^1 at
the surface to the exterior K = 0 leaf W = C/r^2 (ingoing EF), labelled by T at infinity.

2a  formation: the family of leaves, C(T), the surface radius R_s(T), the central lapse dtau_c/dT vs kappa_U = 2 sqrt6/9.
2b  the O(v) l = 1 perturbation of the late leaves: the Jacobi (maximal-slicing lapse) operator on the whole leaf,
    D^2 psi = (K_ij K^ij + Ric(n,n)) psi, regular centre, psi = Y F in the exterior (F the khronon perturbation of CFG319),
    and, separately, a family of arbitrary Robin data at the star surface. The exterior solution is decomposed, at the
    throat, into the two local branches of the alpha = 0 operator at the UH (x^(sqrt2 - 1) weak, x^(-1 - sqrt2) strong).
2c  alpha > 0 inside the O(M/c_S) boundary layer: argument only (exponent bookkeeping printed).
Imported by cfg499_option_a.py (run_collapse); also runnable alone.
"""
import math
import time
import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

mp.mp.dps = 40
NT = 28
TW = mp.mpf(2) / 3
CHIS = mp.cbrt(mp.mpf(9) / 2)
CLIM = 3 * mp.sqrt(3) / 4
KAPPA_U = 2 * mp.sqrt(6) / 9


# ------------------------------------------------------------------------------------------------ truncated series
def smul(a, b):
    return [mp.fsum(a[i] * b[k - i] for i in range(k + 1)) for k in range(NT)]


def spow(u, p):
    w = [u[0]**p]
    for k in range(1, NT):
        w.append(mp.fsum((p * j - (k - j)) * u[j] * w[k - j] for j in range(1, k + 1)) / (k * u[0]))
    return w


def sder(a):
    return [k * a[k] for k in range(1, NT)] + [mp.mpf(0)]


def sint(a, c0):
    return [c0] + [a[k - 1] / k for k in range(1, NT)]


def sadd(*xs):
    return [mp.fsum(x[k] for x in xs) for k in range(NT)]


def ssc(c, a):
    return [c * z for z in a]


def seval(a, t):
    return mp.fsum(a[k] * t**k for k in range(NT))


# ------------------------------------------------------------------------------------------------ interior K = 0 ODE
def derive_interior():
    """K of the level set tau - f(chi) in flat FRW, solved for f''. Also n.grad R (R = a chi) and K as a function of
    (f, f', f'', a, a') for the independent residual check."""
    tau, chi, th, ph = sp.symbols('tau chi theta phi')
    a = sp.Function('a')(tau)
    f = sp.Function('f')(chi)
    g = sp.diag(-1, a**2, a**2 * chi**2, a**2 * chi**2 * sp.sin(th)**2)
    X = [tau, chi, th, ph]
    gi = g.inv()
    Phi = tau - f
    dP = [sp.diff(Phi, x) for x in X]
    n2 = -sum(gi[i, j] * dP[i] * dP[j] for i in range(4) for j in range(4))
    N = 1 / sp.sqrt(n2)
    ud = [-N * d for d in dP]
    uu = [sum(gi[i, j] * ud[j] for j in range(4)) for i in range(4)]
    sg = a**3 * chi**2 * sp.sin(th)
    K = sp.simplify(sum(sp.diff(sg * uu[i], X[i]) for i in range(4)) / sg)
    nR = sp.simplify(sum(uu[i] * sp.diff(a * chi, X[i]) for i in range(4)))
    f0, f1, f2, A0, A1 = sp.symbols('f0 f1 f2 A0 A1')
    rep = lambda ex: ex.subs(f.diff(chi, 2), f2).subs(f.diff(chi), f1).subs(a.diff(tau), A1).subs(a, A0)
    Kx = rep(K)
    f2sol = sp.factor(sp.solve(sp.numer(sp.together(Kx)), f2)[0])
    return f2sol, rep(nR), Kx, (chi, f1, f2, A0, A1)


F2SOL, NR_EXPR, K_EXPR, ISYM = derive_interior()
_f2fun = sp.lambdify(ISYM[:2] + ISYM[3:], F2SOL, 'mpmath')
_Kfun = sp.lambdify(ISYM, K_EXPR, 'mpmath')


def rhs_series(x0, f):
    u = ssc(-1, f)
    A = spow(u, TW)
    Ad = ssc(-TW, spow(u, -mp.mpf(1) / 3))
    f1 = sder(f)
    chi = [x0, mp.mpf(1)] + [mp.mpf(0)] * (NT - 2)
    A2 = smul(A, A)
    num = sadd(ssc(-3, smul(smul(A2, A), smul(Ad, chi))), ssc(-2, smul(A2, f1)),
               ssc(4, smul(smul(A, Ad), smul(chi, smul(f1, f1)))), ssc(2, smul(f1, smul(f1, f1))))
    den = smul(A2, chi)
    return smul(num, spow(den, -1))


def taylor_step(x0, f0, f1):
    f = [f0, f1] + [mp.mpf(0)] * (NT - 2)
    for _ in range(NT + 1):
        g = rhs_series(x0, f)
        f = sint(sint(g, f1)[:NT], f0)[:NT]
    return f


def center_series(tau0):
    """(chi^2 f')' = chi^2[-3 a a' + 4 a' f'^2/a] + 2 chi f'^3/a^2 by Picard iteration in chi about the centre."""
    f = [tau0] + [mp.mpf(0)] * (NT - 1)
    chi = [mp.mpf(0), mp.mpf(1)] + [mp.mpf(0)] * (NT - 2)
    for _ in range(NT + 1):
        u = ssc(-1, f)
        A = spow(u, TW)
        Ad = ssc(-TW, spow(u, -mp.mpf(1) / 3))
        Ai = spow(u, -TW)
        fp = sder(f)
        chi2 = smul(chi, chi)
        rhs = sadd(smul(chi2, sadd(ssc(-3, smul(A, Ad)), ssc(4, smul(Ad, smul(smul(fp, fp), Ai))))),
                   ssc(2, smul(chi, smul(smul(fp, smul(fp, fp)), smul(Ai, Ai)))))
        Q = sint(rhs, mp.mpf(0))
        fp = Q[2:] + [mp.mpf(0)] * 2
        f = sint(fp, tau0)
    return f


def interior_leaf(tau0, x_start=mp.mpf('0.25'), hmax=mp.mpf('0.25'), keep=False):
    cs = center_series(tau0)
    f0 = seval(cs, x_start)
    f1 = seval(sder(cs), x_start)
    x = x_start
    pieces = [('c', mp.mpf(0), x_start, cs)]
    while x < CHIS:
        h = min(hmax, CHIS - x)
        s = taylor_step(x, f0, f1)
        pieces.append(('s', x, x + h, s))
        f0 = seval(s, h)
        f1 = seval(sder(s), h)
        x = x + h
    A0 = (-f0)**TW
    A1 = -TW * (-f0)**(-mp.mpf(1) / 3)
    Rs = A0 * CHIS
    nR = (A0 * A1 * CHIS + f1) / mp.sqrt(A0**2 - f1**2)
    C = -Rs**2 * nR
    out = dict(tau_s=f0, fp_s=f1, Rs=Rs, C=C, nR=nR, gamma=1 / mp.sqrt(1 - f1**2 / A0**2))
    if keep:
        out['pieces'] = pieces
    return out


def leaf_eval(pieces, chi):
    """f, f', f'' of the stored leaf at chi (clamped to the leaf's chi range against float rounding)."""
    chi = min(max(chi, mp.mpf(0)), pieces[-1][2])
    for kind, a, b, s in pieces:
        if a <= chi <= b:
            t = chi if kind == 'c' else chi - a
            d1 = sder(s)
            return seval(s, t), seval(d1, t), seval(sder(d1), t)
    raise ValueError(chi)


# ------------------------------------------------------------------------------------------------ exterior leaf
def Yext(r, C):
    return mp.sqrt(1 - 2 / r + C**2 / r**4)


def Hp(r, C):
    Y = Yext(r, C)
    return -1 / (Y * (Y + C / r**2))


def rstar(r):
    return r + 2 * mp.log(r / 2 - 1)


RREF = mp.mpf(4)


def Hval(R, C):
    Href = -rstar(RREF) - mp.quad(lambda q: Hp(q, C) + 1 / (1 - 2 / q), [RREF, 8, 40, mp.inf])
    pts = [R] + [p for p in (mp.mpf('1.5'), mp.mpf(2)) if R < p < RREF] + [RREF]
    return Href - mp.quad(lambda q: Hp(q, C), pts)


def Vs(tau):
    """EF advanced time of the surface (radial free fall from rest at infinity): dV/dtau = 1/(1 + sqrt(2/R))."""
    R = lambda t: CHIS * (-t)**TW
    return mp.quad(lambda t: 1 / (1 + mp.sqrt(2 / R(t))), [-20, tau])


def T_of_leaf(lf):
    return Vs(lf['tau_s']) + Hval(lf['Rs'], lf['C'])


# ------------------------------------------------------------------------------------------------ 2b Jacobi operator
def jacobi_identity():
    """Exterior: the l = 1 Jacobi operator with psi = Y F equals Y x CFG319's dK operator; the l = 0 lapse psi = Y solves it."""
    r, C = sp.symbols('r C', positive=True)
    e = 1 - 2 / r
    Y = sp.sqrt(e + C**2 / r**4)
    W = C / r**2
    Y1 = sp.diff(Y, r)
    F = sp.Function('F')(r)
    psi = Y * F
    jac = Y * sp.diff(r**2 * Y * sp.diff(psi, r), r) / r**2 - 2 * psi / r**2 - 6 * C**2 / r**6 * psi
    # CFG319 committed dK_ops (coefficients of F, F', F''): Y(W^2-Y^2+1)^2/2, -Y^2(W^2 Y - Y^3 + Y + 3 Y1), -Y^3
    dK = (Y * (W**2 - Y**2 + 1)**2 / 2 * F - Y**2 * (W**2 * Y - Y**3 + Y + 3 * Y1) * F.diff(r) - Y**3 * F.diff(r, 2))
    ratio = sp.simplify(jac / dK)
    lapse = sp.simplify(Y * sp.diff(r**2 * Y * sp.diff(Y, r), r) / r**2 - 6 * C**2 / r**6 * Y)
    return ratio, lapse


SW = math.sqrt(2) - 1
SS = -1 - math.sqrt(2)
CL = float(CLIM)


def ext_rhs(r, y, D):
    """exterior l = 1 Jacobi equation in F (psi = Y F), with Y^2 = [(r-3/2)^2 (r^2+r+3/4) + D]/r^4, D = C^2 - Clim^2."""
    C = math.sqrt(CL**2 + D)
    P = (r - 1.5)**2 * (r**2 + r + 0.75) + D
    dP = 2 * (r - 1.5) * (r**2 + r + 0.75) + (r - 1.5)**2 * (2 * r + 1)
    Y2 = P / r**4
    dY2 = dP / r**4 - 4 * P / r**5
    Y = math.sqrt(Y2)
    Y1 = dY2 / (2 * Y)
    W = C / r**2
    a2 = Y2
    a1 = Y * (W**2 * Y - Y**3 + Y + 3 * Y1)
    a0 = -(W**2 - Y2 + 1)**2 / 2
    return [y[1], -(a1 * y[1] + a0 * y[0]) / a2]


def ext_integ(r0, r1, D, F0, F1):
    s = solve_ivp(ext_rhs, [r0, r1], [F0, F1], args=(D,), method='DOP853', rtol=1e-13, atol=1e-300)
    return s.y[:, -1]


def interior_psi(lf, tau0):
    """l = 1 Jacobi equation on the interior part of the leaf (variable chi), regular centre psi ~ chi.
    (1/(R^2 L)) d/dchi (R^2 psi_chi / L) - 2 psi/R^2 - [6 (n.gradR)^2/R^2 + 4 pi rho (2 gamma^2 - 1)] psi = 0,
    L = dl/dchi = sqrt(a^2 - f'^2), R = a chi, rho = 3 a'^2/(8 pi a^2). Returns (psi, dpsi/dl) at the surface."""
    pcs = lf['pieces']

    def geo(chi):
        f, fp, fpp = leaf_eval(pcs, mp.mpf(chi))
        a = (-f)**TW
        ad = -TW * (-f)**(-mp.mpf(1) / 3)
        add = -mp.mpf(2) / 9 * (-f)**(-mp.mpf(4) / 3)
        L = mp.sqrt(a**2 - fp**2)
        R = a * chi
        dR = ad * fp * chi + a                      # dR/dchi along the leaf
        dL = (a * ad * fp - fp * fpp) / L           # dL/dchi
        nR = (a * ad * chi + fp) / L
        gam2 = 1 / (1 - fp**2 / a**2)
        rho = 3 * ad**2 / (8 * mp.pi * a**2)
        Vpot = 6 * nR**2 / R**2 + 4 * mp.pi * rho * (2 * gam2 - 1)
        return float(R), float(dR), float(L), float(dL), float(Vpot)

    def rhs(chi, y):
        R, dR, L, dL, Vp = geo(chi)
        psi, q = y                                   # q = R^2 psi_chi / L
        dpsi = q * L / R**2
        dq = R**2 * L * (2 * psi / R**2 + Vp * psi)
        return [dpsi, dq]
    c0 = 1e-3
    R, dR, L, dL, Vp = geo(c0)
    y0 = [c0, R**2 * 1.0 / L]
    s = solve_ivp(rhs, [c0, float(CHIS)], y0, method='DOP853', rtol=1e-11, atol=1e-300)
    psi, q = s.y[:, -1]
    R, dR, L, dL, Vp = geo(float(CHIS))
    return psi, q / R**2                             # psi and dpsi/dl


def branch_basis(xm, x0=1e-5):
    pw = ext_integ(1.5 + x0, 1.5 + xm, 0.0, x0**SW, SW * x0**(SW - 1))
    ps = ext_integ(1.5 + x0, 1.5 + xm, 0.0, x0**SS, SS * x0**(SS - 1))
    return pw, ps


def decompose(F, pw, ps):
    Wsw = ps[0] * pw[1] - ps[1] * pw[0]
    cs = (F[0] * pw[1] - F[1] * pw[0]) / Wsw
    cw = -(F[0] * ps[1] - F[1] * ps[0]) / Wsw
    return cs, cw


# ------------------------------------------------------------------------------------------------ driver
def run_collapse(P=print, check=None):
    res = {}
    t0 = time.time()
    P('  2a  Oppenheimer-Snyder collapse, khronon = maximal slicing (alpha -> 0; lambda drops out because K = 0)')
    P(f'      interior K = 0 ODE (sympy): f\'\' = {F2SOL}')
    # early leaves
    early = []
    for t in ['-10', '-3', '-2.5', '-2.2', '-2.0', '-1.9', '-1.8', '-1.7']:
        lf = interior_leaf(mp.mpf(t))
        T = T_of_leaf(lf)
        early.append((float(t), float(T), float(lf['Rs']), float(lf['C'] - CLIM)))
        P(f'      tau_c {t:>5}: T = {float(T):9.4f}   R_s = {float(lf["Rs"]):.6f}   C - Clim = {float(lf["C"] - CLIM):+.6e}')
    # tau0* where C = Clim
    lo, hi = mp.mpf('-1.75'), mp.mpf('-1.6')
    for _ in range(110):
        mid = (lo + hi) / 2
        if interior_leaf(mid)['C'] > CLIM:
            lo = mid
        else:
            hi = mid
    ts = (lo + hi) / 2
    lfs = interior_leaf(ts)
    P(f'      limiting leaf: tau_c* = {mp.nstr(ts, 25)}, R_s* = {mp.nstr(lfs["Rs"], 15)}, C - Clim = {mp.nstr(lfs["C"] - CLIM, 3)}')
    late = []
    for k in range(2, 26, 2):
        tc = ts - mp.mpf(10)**(-k)
        lf = interior_leaf(tc, keep=(k <= 12))
        T = T_of_leaf(lf)
        late.append(dict(k=k, tau0=tc, T=T, Rs=lf['Rs'], dC=lf['C'] - CLIM, lf=lf))
        P(f'      tau_c* - 10^-{k:<2d}: T = {mp.nstr(T, 12):>14}   R_s = {mp.nstr(lf["Rs"], 12)}   C - Clim = {mp.nstr(lf["C"] - CLIM, 5)}')
    kap = []
    for i in range(1, len(late)):
        a_, b_ = late[i - 1], late[i]
        kap.append((b_['k'] - a_['k']) * mp.log(10) / (b_['T'] - a_['T']))
    P('      kappa from the central lapse dtau_c/dT ~ exp(-kappa T): ' + ', '.join(mp.nstr(k_, 10) for k_ in kap))
    P(f'      kappa_U = y1 W0 = 2 sqrt6/9 = {mp.nstr(KAPPA_U, 10)}')
    kap_late = kap[-1]
    Tmax = late[-1]['T']
    Cs = [float(e_[3]) for e_ in early] + [float(l_['dC']) for l_ in late]
    mono_dec = all(Cs[i + 1] < Cs[i] for i in range(len(Cs) - 1))
    mono_inc = all(Cs[i + 1] > Cs[i] for i in range(len(Cs) - 1))
    Rs_min = min([e_[2] for e_ in early] + [float(l_['Rs']) for l_ in late])
    # K6 controls
    lf = late[3]['lf']
    pcs = lf['pieces']
    resid = 0
    for chi in [0.1, 0.4, 0.8, 1.2, 1.6]:
        f, fp, fpp = leaf_eval(pcs, mp.mpf(chi))
        a = (-f)**TW
        ad = -TW * (-f)**(-mp.mpf(1) / 3)
        resid = max(resid, abs(_Kfun(mp.mpf(chi), fp, fpp, a, ad)))
    # normal continuity: n.U_s from both sides (C was fixed by n.grad R only)
    Rs, C = lf['Rs'], lf['C']
    UV, Ur = 1 / (1 + mp.sqrt(2 / Rs)), -mp.sqrt(2 / Rs)
    Y = Yext(Rs, C)
    nU_ext = -Y * (UV + Hp(Rs, C) * Ur)
    nU_int = -lf['gamma']
    mdev = abs(nU_ext / nU_int - 1)
    P(f'      K6: interior K residual (independent sympy K at 5 chi) = {mp.nstr(resid, 3)};  normal continuity n.U_s '
      f'exterior {mp.nstr(nU_ext, 15)} vs interior {mp.nstr(nU_int, 15)} (rel {mp.nstr(mdev, 3)})')
    if check:
        check('K6 collapse controls: interior leaf solves K = 0 (independent expression) <= 1e-9 and the leaf is C^1 at '
              'the surface (n.U_s equal from both sides) <= 1e-9', f'K resid {mp.nstr(resid, 3)}; n.U rel {mp.nstr(mdev, 3)}',
              resid < 1e-9 and mdev < 1e-9)
    a_i = Tmax >= 40
    a_ii_frozen = mono_inc and abs(float(late[-1]['dC'])) < 1e-6
    a_ii_corr = abs(float(late[-1]['dC'])) < 1e-6
    a_iii_frozen = Rs_min > 1.5
    a_iv = abs(kap_late / KAPPA_U - 1) < 0.01
    res['2a'] = dict(tau0_star=mp.nstr(ts, 25), Rs_star=float(lfs['Rs']), T_max=float(Tmax), kappa_fit=float(kap_late),
                     kappa_U=float(KAPPA_U), kappa_rel_dev=float(abs(kap_late / KAPPA_U - 1)),
                     C_minus_Clim_early=[e_[3] for e_ in early], C_minus_Clim_late=[float(l_['dC']) for l_ in late],
                     T_late=[float(l_['T']) for l_ in late], Rs_late=[float(l_['Rs']) for l_ in late],
                     C_monotone_decreasing=mono_dec, C_monotone_increasing=mono_inc, Rs_min=Rs_min,
                     i_exist_T40=a_i, ii_frozen_C_increases_to_Clim=a_ii_frozen, ii_corrected_C_to_Clim=a_ii_corr,
                     iii_frozen_Rs_gt_1p5=a_iii_frozen, iv_kappa=a_iv, K6_resid=float(resid), K6_normal=float(mdev))
    P(f'      2a(i) leaves exist to T = {float(Tmax):.1f} >= 40: {a_i}')
    P(f'      2a(ii) AS FROZEN "C(T) increases monotonically to 3 sqrt3/4": {a_ii_frozen}  (C - Clim is monotone '
      f'DECREASING from above: {mono_dec}; it reaches {float(late[-1]["dC"]):.2e})')
    P(f'      2a(iii) AS FROZEN "R_s(T) > 3/2 for every T": {a_iii_frozen}  (R_s falls to R_s* = {float(lfs["Rs"]):.6f} < 3/2)')
    P(f'      2a(iv) central lapse rate = kappa_U within 1%: {a_iv}  (rel dev {float(abs(kap_late / KAPPA_U - 1)):.1e})')
    P(f'      [2a time {time.time() - t0:.0f}s]')

    # ---------------------------------------------------------------- 2b
    t1 = time.time()
    P('  2b  O(v) l = 1 perturbation of the late leaves (alpha -> 0): Jacobi operator on the whole leaf')
    ratio, lapse = jacobi_identity()
    P(f'      identity: Jacobi(psi = Y F) / CFG319 dK(F) = {ratio};  l = 0 lapse psi = Y residual = {lapse}')
    ok_id = ratio.is_number and ratio != 0 and lapse == 0
    if check:
        check('K6b the exterior l = 1 Jacobi operator with psi = Y F is a constant multiple of CFG319\'s committed (Y-weighted) dK operator, and the l = 0 '
              'lapse psi = Y solves the l = 0 operator (sympy, exact)', f'ratio {ratio}; lapse residual {lapse}', ok_id)
    P(f'      local exponents of the alpha = 0 operator at the UH: s^2 + 2 s - 1 = 0 -> weak {SW:.6f}, strong {SS:.6f}')
    rows = []
    for xm in (0.05, 0.2):
        pw, ps = branch_basis(xm)
        for L_ in late[:6]:
            lf = L_['lf']
            D = float(L_['dC'] * (2 * CLIM + L_['dC']))
            Rs = float(lf['Rs'])
            psi_s, dpsi_s = interior_psi(lf, L_['tau0'])
            Y = float(Yext(lf['Rs'], lf['C']))
            # psi = Y F; d/dl = Y d/dr  ->  F = psi/Y, F' = (dpsi/dl / Y - F Y')/Y
            Cf = float(lf['C'])
            Y1 = float(mp.diff(lambda q: Yext(q, lf['C']), lf['Rs']))
            Fs = psi_s / Y
            Fps = (dpsi_s / Y - Fs * Y1) / Y
            Fm = ext_integ(Rs, 1.5 + xm, D, Fs, Fps)
            cs_, cw_ = decompose(Fm, pw, ps)
            robin = []
            for rho in [-100.0, -1.0, 0.0, 1.0, 100.0, 'inf']:
                F0, F1 = (0.0, 1.0) if rho == 'inf' else (1.0, rho)
                cs2, cw2 = decompose(ext_integ(Rs, 1.5 + xm, D, F0, F1), pw, ps)
                robin.append(abs(cs2 / cw2))
            # fine-tuned inner datum that would give the pure strong branch at xm
            phA = ext_integ(Rs, 1.5 + xm, D, 1.0, 0.0)
            phB = ext_integ(Rs, 1.5 + xm, D, 0.0, 1.0)
            _, cwA = decompose(phA, pw, ps)
            _, cwB = decompose(phB, pw, ps)
            rho_star = -cwA / cwB
            rows.append(dict(xm=xm, k=L_['k'], sqrtD=math.sqrt(D), Rs=Rs, ratio_true=abs(cs_ / cw_),
                             robin_max=max(robin), robin_min=min(robin), rho_star=rho_star, inner_rho_true=Fps / Fs))
            P(f'      x_m {xm:4.2f}  k {L_["k"]:2d}  throat sqrt(D) {math.sqrt(D):.2e}: |c_strong/c_weak| true interior '
              f'{abs(cs_ / cw_):.3e}; Robin family max {max(robin):.3e}; inner F\'/F true {Fps / Fs:+.4f}, '
              f'fine-tuned {rho_star:+.4f}')
    # scaling with D at the smallest throats
    sel = [r_ for r_ in rows if r_['xm'] == 0.05]
    fin = [r_ for r_ in sel if r_['k'] >= 8]
    slope = (math.log(fin[-1]['ratio_true']) - math.log(fin[0]['ratio_true'])) / (math.log(fin[-1]['sqrtD']) - math.log(fin[0]['sqrtD']))
    P(f'      d ln|c_s/c_w| / d ln sqrt(D) (k 8 -> 12, x_m 0.05) = {slope:.3f}')
    b_pass = all(r_['ratio_true'] < 1e-6 for r_ in rows if r_['k'] >= 8) and sel[-1]['ratio_true'] < sel[3]['ratio_true'] \
        and all(r_['robin_max'] < 1e-6 for r_ in rows if r_['k'] >= 8)
    res['2b'] = dict(rows=rows, slope_vs_sqrtD=slope, passes=b_pass)
    P(f'      2b weak branch selected for the true interior and for every Robin datum tested, the strong admixture '
      f'falling with the throat width: {b_pass}   [2b time {time.time() - t1:.0f}s]')
    # ---------------------------------------------------------------- 2c bookkeeping
    P('  2c  alpha > 0 inside the O(M/c_S) layer (C vs C\'): ARGUMENT. Leaf displacement kappa x v F ~ x^(1+s):')
    book = {}
    for nm, s_ in (('alpha=0 weak sqrt2-1', SW), ('alpha=0 strong -1-sqrt2', SS), ('alpha>0 s+', 0.618034),
                   ('alpha>0 s-', -1.618034), ('displacement -1', -1.0), ('constant 0', 0.0)):
        book[nm] = 1 + s_
        P(f'      {nm:26s}: 1 + s = {1 + s_:+.4f}  -> {"bounded" if 1 + s_ >= 0 else "DIVERGES"} as x -> 0')
    P('      at alpha = 0 the computed selection (2b) removes exactly the branch whose displacement diverges; the same rule')
    P('      at alpha > 0 removes s- (option C\') and keeps s+ (option C). Not computed for alpha > 0: 2c is an argument.')
    res['2c'] = dict(displacement_powers=book, status='ARG')
    res['time_s'] = time.time() - t0
    return res


if __name__ == '__main__':
    import json
    out = run_collapse()
    print(json.dumps({k: (v if k != '2b' else {kk: vv for kk, vv in v.items() if kk != 'rows'}) for k, v in out.items()},
                     indent=1, default=str)[:3000])
