#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A2 -- FRW LIMIT OF THE A1 ACTION: (a) a0(z) FLAT because the cap reads the HT constant; (b) the fluid is CDM-like dust with Omega_c FREE
(initial data) and a constant Lambda; (c) the tie survives across universes (Lambda_0 is a free integration constant, P_cap follows it).

The equations integrated are the ones DERIVED in A1 (sympy Euler-Lagrange of the minisuperspace action, lapse N = 1 after variation):
  HT (MUTATE=0/2):  E_T: Lambda' = 0;  E_theta: J0' = 0;  E_N: 3 Mp2 H^2 = Mp2 Lambda + rho(n; Lambda);  E_a: the second-order Raychaudhuri equation
  MUTATE=1 (scalar replaces the multiplier):  psi'' + 3 H psi' + U'(psi) + rho_Lambda U'/Mp2 = 0, Friedmann with (psi'^2/2 + U)
  MUTATE=2 (tie dropped): the cap reads an independent constant Lc (a0 does not follow Lambda_0).
Units: Mp2 = 1, m = 1, a = 1 today, Lambda = 1 for the reference universe (so Omega_c0 = n0/(Lambda + n0)-type ratios are dimensionless).

Checks:  A2-a a0(z)/a0(0), Lambda_eff(z) inferred from (H, rho) is constant;  A2-b E_N is preserved by the integrated E_a (Bianchi) and n a^3 = const;
         A2-c dust limit: rho a^3 constancy, w and c_s^2 sizes, H(z)/H_LCDM;  A2-d Omega_c free (two integration constants);  A2-e the tie across universes.
         C-XR20 (control): a thawing exponential field reproduces XR20's E4 rise of a0 toward high z (+0.07..+0.16 dex at z = 2.5).
Run:  python3 A2_frw_flat_a0_and_dust_limit.py     (MUTATE=1 or 2 for the controls)
"""
import os
import sys
import math
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import A_common as C

R = C.Run("A2_frw_flat_a0_and_dust_limit")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)
P("MUTATE mode = %d" % M)

t = sp.Symbol('t')
Mp2, m, eps, nus, Lcs = sp.symbols('Mp2 m epsilon nu_s Lc', positive=True)


def rho_eos(n_, L_):
    x_ = m * n_ / (nus * Mp2 * L_)
    return m * n_ + eps * Mp2 * L_ * x_ * sp.atan(x_)


a = sp.Function('a')(t); N = sp.Function('N')(t); Lam = sp.Function('Lam')(t); T0 = sp.Function('T0')(t)
J0 = sp.Function('J0')(t); th = sp.Function('th')(t); psi = sp.Function('psi')(t)
n_of = J0 / a ** 3
lam_s = sp.Symbol('lambda_s', positive=True)
U_of = lambda p_: sp.exp(-lam_s * p_)                        # U(psi) = Lambda_0 e^{-lambda psi}, Lambda_0 carried by the initial psi

if M == 1:
    Lfl = U_of(psi)
    L_ = (-3 * Mp2 * a * a.diff(t) ** 2 / N + N * a ** 3 * Mp2 * (psi.diff(t) ** 2 / (2 * N ** 2) - U_of(psi)) - N * a ** 3 * rho_eos(n_of, Lfl) + J0 * th.diff(t))
    flds = [a, N, psi, J0, th]
else:
    Lfl = Lcs if M == 2 else Lam
    L_ = (-3 * Mp2 * a * a.diff(t) ** 2 / N - N * a ** 3 * Mp2 * Lam + Mp2 * Lam * T0.diff(t) - N * a ** 3 * rho_eos(n_of, Lfl) + J0 * th.diff(t))
    flds = [a, N, Lam, T0, J0, th]
EL = {str(f.func): e.lhs for f, e in zip(flds, euler_equations(L_, flds, t))}

# ---- lambdified right-hand sides (N = 1) ------------------------------------------------------------------------------
A_, Ad, Add = sp.symbols('A Ad Add')
J_, L_s = sp.symbols('J Lsym', positive=True)
psi_s, psid_s, psidd_s = sp.symbols('psi psid psidd')
sub_common = {N: 1}
Ea = EL['a']
if M == 1:
    Ea_s = Ea.subs(N, 1).subs({a.diff(t, 2): Add, a.diff(t): Ad, psi.diff(t): psid_s, psi: psi_s, J0: J_, a: A_})
    Add_sol = sp.solve(Ea_s, Add)[0]
    Epsi = EL['psi'].subs(N, 1).subs({a.diff(t): Ad, psi.diff(t, 2): psidd_s, psi.diff(t): psid_s, psi: psi_s, J0: J_, a: A_})
    psidd_sol = sp.solve(Epsi, psidd_s)[0]
    EN = sp.simplify(EL['N'].subs(N, 1).subs({a.diff(t): Ad, psi.diff(t): psid_s, psi: psi_s, J0: J_, a: A_}))
    f_add = sp.lambdify((A_, Ad, psi_s, psid_s, J_, lam_s, Mp2, m, eps, nus), Add_sol, 'numpy')
    f_psidd = sp.lambdify((A_, Ad, psi_s, psid_s, J_, lam_s, Mp2, m, eps, nus), psidd_sol, 'numpy')
    f_EN = sp.lambdify((A_, Ad, psi_s, psid_s, J_, lam_s, Mp2, m, eps, nus), EN, 'numpy')
else:
    Ea_s = Ea.subs(N, 1).subs({a.diff(t, 2): Add, a.diff(t): Ad, Lam: L_s, J0: J_, a: A_})
    Add_sol = sp.solve(Ea_s, Add)[0]
    EN = sp.simplify(EL['N'].subs(N, 1).subs({a.diff(t): Ad, Lam: L_s, J0: J_, a: A_}))
    f_add = sp.lambdify((A_, Ad, L_s, J_, Mp2, m, eps, nus, Lcs), Add_sol, 'numpy')
    f_EN = sp.lambdify((A_, Ad, L_s, J_, Mp2, m, eps, nus, Lcs), EN, 'numpy')
nn_ = sp.Symbol('nn_', positive=True); LL_ = sp.Symbol('LL_', positive=True)
rho_num = sp.lambdify((nn_, LL_, Mp2, m, eps, nus), rho_eos(nn_, LL_), 'numpy')
P_expr = sp.simplify(nn_ * sp.diff(rho_eos(nn_, LL_), nn_) - rho_eos(nn_, LL_))
P_num = sp.lambdify((nn_, LL_, Mp2, m, eps, nus), P_expr, 'numpy')
dP_num = sp.lambdify((nn_, LL_, Mp2, m, eps, nus), sp.diff(P_expr, nn_), 'numpy')
drho_num = sp.lambdify((nn_, LL_, Mp2, m, eps, nus), sp.diff(rho_eos(nn_, LL_), nn_), 'numpy')

NUS = 1.0e6
EPSV = float(C.EPS)
PAR = (1.0, 1.0, EPSV, NUS)                                   # Mp2, m, eps, nu_s


def run_HT(Lam0, n0, Lc_val=None, a_i=5e-4, nu_s=NUS):
    """integrate E_a (N=1) from a_i to a = 1 with E_N as initial data; returns dict of arrays.  Lambda' = 0 (E_T)."""
    Lc_val = (1.0 if M == 2 else Lam0) if Lc_val is None else Lc_val     # MUTATE=2: the cap reads a constant Lc held at the reference value
    par = (1.0, 1.0, EPSV, nu_s)
    Lfl_v = Lc_val if M == 2 else Lam0
    Ji = n0                                                     # J0 = n a^3 with a(today) = 1
    rho_i = float(rho_num(Ji / a_i ** 3, Lfl_v, *par))
    Hi = math.sqrt((Lam0 + rho_i) / 3.0)
    rhs = lambda tt, y: [y[1], float(f_add(y[0], y[1], Lam0, Ji, *par[0:1], par[1], par[2], par[3], Lc_val))]
    ev = lambda tt, y: y[0] - 1.0
    ev.terminal = True
    sol = solve_ivp(rhs, [0, 1e3], [a_i, a_i * Hi], events=ev, rtol=1e-13, atol=1e-16, dense_output=True, method='DOP853')
    tt = np.linspace(0, sol.t[-1], 4000)
    y = sol.sol(tt)
    return dict(t=tt, a=y[0], ad=y[1], Lam=np.full_like(tt, Lam0), J=Ji, Lfl=np.full_like(tt, Lfl_v), par=par, Lc=Lc_val)


def run_scalar(psi_i, lam_v, n0, a_i=5e-4):
    """MUTATE=1: (a, a', psi, psi') with psi'(a_i) = 0 (thawing); J0 = n0 fixed."""
    par = (1.0, 1.0, EPSV, NUS)
    Ji = n0
    Ui = math.exp(-lam_v * psi_i)
    rho_i = float(rho_num(Ji / a_i ** 3, Ui, *par))
    Hi = math.sqrt((Ui + rho_i) / 3.0)

    def rhs(tt, y):
        A, Ad_, ps, psd = y
        args = (A, Ad_, ps, psd, Ji, lam_v) + par
        return [Ad_, float(f_add(*args)), psd, float(f_psidd(*args))]
    ev = lambda tt, y: y[0] - 1.0
    ev.terminal = True
    sol = solve_ivp(rhs, [0, 1e3], [a_i, a_i * Hi, psi_i, 0.0], events=ev, rtol=1e-12, atol=1e-15, dense_output=True, method='DOP853')
    tt = np.linspace(0, sol.t[-1], 6000)
    y = sol.sol(tt)
    return dict(t=tt, a=y[0], ad=y[1], psi=y[2], psid=y[3], J=Ji, lam=lam_v, par=par)


def at_z(res, z):
    a_t = 1.0 / (1.0 + z)
    i = np.searchsorted(res['a'], a_t)
    i = min(max(i, 1), len(res['a']) - 1)
    w = (a_t - res['a'][i - 1]) / (res['a'][i] - res['a'][i - 1])
    return i - 1, i, w


def interp(res, key, z):
    i0, i1, w = at_z(res, z)
    return (1 - w) * res[key][i0] + w * res[key][i1]


ZS = [0.5, 1.0, 2.5, 5.0, 1100.0]
N0 = 0.3 / 0.7                                                  # n0/Lambda: Omega_c0/Omega_Lambda0 = 0.3/0.7 (Mp2 = m = 1, Lambda = 1)

R.banner("A2-a  a0(z) and the Lambda inferred from (H, rho): constant?  (a0 = sqrt(8 pi G P_cap) = sqrt(P_cap/Mp2))")
if M != 1:
    res = run_HT(1.0, N0)
    Lfl_z = lambda z: 1.0                                       # fluid's Lambda (HT constant, or Lc = Lambda_0 for MUTATE=2 at the reference universe)
    a0_ratio = {}
    for z in ZS:
        a0_ratio[z] = 1.0                                       # the cap is P_cap = eps Mp2 Lfl(z) with Lfl the HT field/constant from the solution:
    # a0(z) read from the SOLUTION: Lambda(t) is the integrated field (constant by E_T), Lambda_eff(z) from the geometry:
    Hs = res['ad'] / res['a']
    nz = res['J'] / res['a'] ** 3
    rho_z = rho_num(nz, res['Lfl'], *res['par'])
    Leff = 3 * Hs ** 2 - rho_z / res['par'][0]                 # Lambda_eff = 3H^2 - rho/Mp2 from the geometry and the fluid
    # a0 read from the field values along the solution
    a0_track = np.sqrt(EPSV * Leff)                             # a0(z) = alpha(Lambda) c^2 with Lambda READ FROM THE GEOMETRY (3H^2 - rho/Mp2), not assumed
    dlog = {z: math.log10(interp({'a': res['a'], 'x': a0_track}, 'x', z) / a0_track[-1]) for z in ZS}
    ZG = [z for z in ZS if z <= 10.0]                            # precision window: Lambda_eff = 3H^2 - rho is a difference of numbers ~ rho/Lambda times larger at high z
    mask = res['a'] >= 1.0 / 11.0
    spread = float(np.max(np.abs(Leff[mask] / Leff[-1] - 1)))
    spread_hi = float(np.max(np.abs(Leff / Leff[-1] - 1)))
    P("  a0(z)/a0(0) along the integrated HT solution (a0 = sqrt(eps Lambda_eff), Lambda_eff from the geometry): " + ", ".join("z=%g: %.15f" % (z, 10 ** dlog[z]) for z in ZS))
    P("  Lambda_eff(z) = 3H^2 - rho/Mp2, max |Lambda_eff/Lambda_eff(0) - 1| over z in [0, 10] = %.2e;  over z in [0, 1100] = %.2e "
      "(round-off amplified by rho/Lambda ~ 4e8 at z = 1100: 1e-13 x 4e8 ~ 4e-5; not physics)" % (spread, spread_hi))
    ok_flat = all(abs(10 ** dlog[z] - 1) < 1e-10 for z in ZG) and spread < 1e-10
    check("A2-a", "a0(z) = alpha(Lambda) c^2 is flat: with Lambda READ FROM THE GEOMETRY (3H^2 - rho/Mp2 along the integrated solution) a0(z)/a0(0) = 1 to 1e-10 at z = 0.5, 1, 2.5, 5, "
          "and Lambda_eff is constant to 1e-10 over z <= 10 (z = 1100 is beyond the round-off floor; there E_T's Lambda' = 0 is the statement)",
          "max |dlog a0| (z <= 10) = %.1e dex; Lambda_eff spread (z <= 10) %.2e" % (max(abs(dlog[z]) for z in ZG), spread), ok_flat,
          "DERIVED: E_T = -Mp2 Lambda' (A1); the numbers only confirm that the integrated E_a keeps the constraint")
    # MUTATE=2: a0 as the fluid's cap sees it vs the HT Lambda in a SECOND universe (done in A2-e); here the same-universe flatness holds
else:
    lam_v = 1.27                                                # XR20 E4 uses lambda = 1.27 / 1.03 / 1.46 for the DESY5 / Pantheon+ / Union3 w0

    def omega_c0(psi_i):
        r_ = run_scalar(psi_i, lam_v, 0.5)
        Uend = math.exp(-lam_v * r_['psi'][-1])
        H0sq = (r_['ad'][-1] / r_['a'][-1]) ** 2
        rho0 = float(rho_num(0.5, Uend, *r_['par']))
        return rho0 / (3 * H0sq) - 0.315
    psi_i = brentq(omega_c0, -2.0, 6.0, xtol=1e-12)
    res = run_scalar(psi_i, lam_v, 0.5)
    Uz = np.exp(-lam_v * res['psi'])
    H0sq = (res['ad'][-1] / res['a'][-1]) ** 2
    w0 = (res['psid'][-1] ** 2 / 2 - Uz[-1]) / (res['psid'][-1] ** 2 / 2 + Uz[-1])
    a0_track = np.sqrt(EPSV * Uz)                               # a0 = alpha(U(psi)) c^2: the cap reads the scalar
    dlog = {z: math.log10(interp({'a': res['a'], 'x': a0_track}, 'x', z) / a0_track[-1]) for z in ZS}
    Hs = res['ad'] / res['a']
    nz = res['J'] / res['a'] ** 3
    rho_z = rho_num(nz, Uz, *res['par'])
    Leff = 3 * Hs ** 2 - rho_z
    mask = res['a'] >= 1.0 / 11.0
    spread = float(np.max(np.abs(Leff[mask] / Leff[-1] - 1)))
    P("  thawing exponential U = U0 exp(-%.2f psi): tuned to Omega_c0 = 0.315 (flat); w0 = %.3f, Omega_de0 = %.3f" % (lam_v, w0, 1 - 0.315))
    P("  a0(z)/a0(0) = sqrt(U(z)/U(0)): " + ", ".join("z=%g: %.6f" % (z, 10 ** dlog[z]) for z in ZS))
    P("  Lambda_eff(z) = 3H^2 - rho/Mp2 spread over z in [0, 10]: %.2e (a constant Lambda gives < 1e-10)" % spread)
    ok_flat = all(abs(10 ** dlog[z] - 1) < 1e-10 for z in ZS if z <= 5.0) and spread < 1e-10
    check("A2-a", "a0(z) flat and Lambda_eff constant", "max |dlog a0| over z <= 5: %.3f dex (z=2.5: %+.3f dex); Lambda_eff spread %.2e"
          % (max(abs(dlog[z]) for z in ZS if z <= 5.0), dlog[2.5], spread), ok_flat, "MUTATE=1: the cap tracks the scalar; a0 rises toward high z (compare XR20 E4: +0.111 dex at z = 2.5 for the DESY5 w0)")
    xr20_E4 = 0.111
    check("C-XR20", "control: the thawing field's a0(2.5) rise is of XR20 E4's size (XR20: +0.111 dex for the DESY5-matched w0 = -0.752; this run has w0 = %.3f)" % w0,
          "this lane: %+.3f dex at z = 2.5 (w0 = %.3f); XR20 E4: +0.070 / +0.111 / +0.156 for w0 = -0.838 / -0.752 / -0.667" % (dlog[2.5], w0),
          0.03 < dlog[2.5] < 0.20, "same sign, same magnitude: the thawing-field realisation is the one XR20 T5 scored", load_bearing=False)

R.banner("A2-b  the constraint is preserved by the integrated Raychaudhuri equation (Bianchi) and n a^3 = const")
if M != 1:
    ENv = np.array([float(f_EN(res['a'][k], res['ad'][k], 1.0, res['J'], *res['par'][0:1], res['par'][1], res['par'][2], res['par'][3], res['Lc'])) for k in range(0, len(res['a']), 20)])
    scale = np.max(np.abs(3 * (res['ad'] / res['a']) ** 2 * res['a'] ** 3))
    bj = float(np.max(np.abs(ENv)) / scale)
    nconst = float(np.max(np.abs(res['J'] / res['a'] ** 3 * res['a'] ** 3 / res['J'] - 1)))
    check("A2-b", "E_N (Friedmann constraint) stays zero along the integration of E_a from data with E_N = 0, and n a^3 = J0 is constant",
          "max |E_N|/(3 H^2 a^3) = %.2e over a in [5e-4, 1]; n a^3/J0 - 1 = %.1e" % (bj, nconst), bj < 1e-9 and nconst < 1e-12,
          "the reparametrisation identity of A1 (H-BIANCHI) at work; the HT sector does not disturb it (Lambda' = 0)")
else:
    ENv = np.array([float(f_EN(res['a'][k], res['ad'][k], res['psi'][k], res['psid'][k], res['J'], res['lam'], *res['par'])) for k in range(0, len(res['a']), 60)])
    scale = np.max(np.abs(3 * (res['ad'] / res['a']) ** 2 * res['a'] ** 3))
    bj = float(np.max(np.abs(ENv)) / scale)
    check("A2-b", "E_N stays zero along the integration (the scalar action is also reparametrisation invariant) and n a^3 = const",
          "max |E_N|/(3 H^2 a^3) = %.2e; n a^3 const by E_theta (A1 H-NUM)" % bj, bj < 1e-8, "passes in every mode: the identity is a property of any invariant action; the physics is A2-a/c")

R.banner("A2-c  DUST LIMIT: rho a^3, w, c_s^2 and H(z)/H_LCDM for the cold fluid (nu_s = %.0e; POSTULATED EOS)" % NUS)
zz = np.array([0.0, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 100.0, 300.0, 1100.0])
aa = 1.0 / (1.0 + zz)
Lam_z = 1.0 if M != 1 else None
if M != 1:
    Lref = 1.0
    nz_ = N0 / aa ** 3
    rho_ = rho_num(nz_, Lref, 1.0, 1.0, EPSV, NUS)
    P_ = P_num(nz_, Lref, 1.0, 1.0, EPSV, NUS)
    cs2 = dP_num(nz_, Lref, 1.0, 1.0, EPSV, NUS) / drho_num(nz_, Lref, 1.0, 1.0, EPSV, NUS)
    w_ = P_ / rho_
    rhoa3 = rho_ * aa ** 3 / (rho_[0])
    Hm = np.sqrt((Lref + rho_) / 3.0)
    # LCDM with the SAME dust (m n): Omega_m defined with the bare mass term; and with the best-fit dust density (Omega_c rescaled: free)
    Hd = np.sqrt((Lref + N0 / aa ** 3) / 3.0)
    dev_fixed = np.max(np.abs(Hm / Hd - 1))
    # best rescaling of the dust density (Omega_c free): minimise max |H/H_LCDM(k N0) - 1|
    from scipy.optimize import minimize_scalar
    fbest = minimize_scalar(lambda k: np.max(np.abs(Hm / np.sqrt((Lref + k * N0 / aa ** 3) / 3.0) - 1)), bounds=(0.9, 1.1), method='bounded', options={'xatol': 1e-14})
    P("  z         :" + " ".join("%10g" % z for z in zz))
    P("  rho a^3/(rho a^3)_0 - 1 :" + " ".join("%10.2e" % (v - 1) for v in rhoa3))
    P("  w = P/rho :" + " ".join("%10.2e" % v for v in w_))
    P("  c_s^2 = dP/drho :" + " ".join("%10.2e" % v for v in cs2))
    P("  H/H_LCDM - 1 (same bare dust) max = %.2e; after freeing the dust density (Omega_c rescale k = %.10f) max = %.2e" % (dev_fixed, fbest.x, fbest.fun))
    bump = float(np.max(np.abs(rhoa3 - 1)))
    ok_dust = bump < 5 * math.pi / 2 * EPSV / NUS and float(np.max(w_)) < 1e-6 and float(np.max(cs2)) < 1e-6 and fbest.fun < 1e-7
    check("A2-c", "cold-limit: rho a^3 constant to (pi/2) eps/nu_s ~ %.1e, w < 1e-6, c_s^2 < 1e-6 everywhere on z in [0, 1100], H(z) = LCDM with a rescaled (FREE) dust density "
          "to %.1e" % (math.pi / 2 * EPSV / NUS, fbest.fun),
          "max |rho a^3 - 1| = %.2e; max w = %.2e; max c_s^2 = %.2e (NB only a crude cold check: the Jeans/structure bound is applied in A3); H/H_LCDM residual %.2e"
          % (bump, float(np.max(w_)), float(np.max(cs2)), fbest.fun), ok_dust,
          "DERIVED in the limit x -> 0 or x -> oo (the EOS is dust + a constant mass renormalisation); the size of the bump is set by the POSTULATED nu_s")
else:
    Uz_ = np.interp(aa, res['a'], Uz)
    zsel = aa >= 1.0 / 11.0
    Lef = np.interp(aa[zsel], res['a'], Leff)
    check("A2-c", "cold-limit with a CONSTANT Lambda: Lambda_eff(z) spread over z <= 10 below 1e-7", "Lambda_eff varies by %.2e" % (float(np.max(Lef) / np.min(Lef) - 1)), float(np.max(Lef) / np.min(Lef) - 1) < 1e-7,
          "MUTATE=1: the scalar's energy density evolves; dust + constant Lambda no longer describes the background")

R.banner("A2-d  Omega_c is FREE (initial data J0) and independent of Lambda_0: two integration constants, P_cap depends on Lambda_0 only")
if M != 1:
    outs = {}
    for (Lam0, n0) in ((1.0, 0.3 / 0.7), (1.0, 0.1 / 0.9), (1.0, 0.6 / 0.4), (2.0, 0.3 / 0.7)):
        r_ = run_HT(Lam0, n0)
        H0sq = (r_['ad'][-1] / r_['a'][-1]) ** 2
        rho0 = float(rho_num(n0, r_['Lfl'][-1], *r_['par']))
        Om_c = rho0 / (3 * H0sq)
        Pcap0 = EPSV * r_['Lfl'][-1]
        outs[(Lam0, n0)] = (Om_c, Lam0 / (3 * H0sq), Pcap0)
        P("   Lambda_0 = %g, n0 = %.4f  ->  Omega_c0 = %.6f, Omega_Lambda0 = %.6f, P_cap = eps Mp2 Lambda_fluid = %.6e" % (Lam0, n0, Om_c, Lam0 / (3 * H0sq), Pcap0))
    keys = list(outs)
    # independence: Omega_c varies with J0 at fixed Lambda_0 while P_cap does not (mode 0)
    dP_dn = abs(outs[keys[1]][2] - outs[keys[0]][2]) + abs(outs[keys[2]][2] - outs[keys[0]][2])
    dOm_dn = abs(outs[keys[1]][0] - outs[keys[0]][0])
    ok_free = dOm_dn > 0.1 and dP_dn < 1e-14 and abs(outs[keys[0]][0] + outs[keys[0]][1] - 1) < 1e-6
    check("A2-d", "Omega_c0 varies freely with the initial data J0 (0.1 ... 0.6) at fixed Lambda_0, while P_cap does not move; Omega_c + Omega_Lambda = 1 in every run (GR + Lambda + dust)",
          "Delta Omega_c = %.3f at fixed Lambda_0; Delta P_cap = %.1e; flatness residual %.1e" % (dOm_dn, dP_dn, abs(outs[keys[0]][0] + outs[keys[0]][1] - 1)), ok_free,
          "Omega_c is initial data (like LCDM); the cap depends on Lambda_0 only")

    R.banner("A2-e  the tie holds across universes: a0 (from the fluid's cap) / kappa sqrt(Lambda_0/8pi) is the same in every solution")
    ratios = []
    for Lam0 in (0.5, 1.0, 2.0, 7.0):
        r_ = run_HT(Lam0, 0.3 / 0.7 * Lam0 if False else 0.4 * Lam0)
        a0_cap_sol = math.sqrt(EPSV * r_['Lfl'][-1])            # sqrt(P_cap/Mp2) with the cap read from what the fluid Lagrangian depends on
        a0_tie = math.sqrt(EPSV * Lam0)                          # kappa sqrt(Lambda_0/8 pi)
        ratios.append(a0_cap_sol / a0_tie)
        P("   Lambda_0 = %-4g  a0_cap = %.6f   kappa sqrt(Lambda_0/8pi) = %.6f   ratio %.12f" % (Lam0, a0_cap_sol, a0_tie, ratios[-1]))
    check("A2-e", "a0_cap(universe) / [kappa sqrt(Lambda_0/8 pi)] = 1 for Lambda_0 = 0.5, 1, 2, 7: the cap follows the HT integration constant (one constant, kappa the coupling)",
          "ratios %s" % ["%.12f" % r for r in ratios], all(abs(r - 1) < 1e-12 for r in ratios),
          "MUTATE=2: the fluid's cap reads Lc (held at the reference value), so the ratio drifts as sqrt(Lc/Lambda_0)")
else:
    P("  [n/a ] A2-d/e: with a dynamical scalar the 'universes' are labelled by (psi_i, lambda): Lambda_0 is not an integration constant; the tie check A2-e reduces to A2-a")
    check("A2-e", "a0_cap tracks the scalar: a0_cap(z)/a0_cap(0) equals sqrt(U(z)/U(0)) but is not constant",
          "z=2.5: %.4f" % (10 ** dlog[2.5]), abs(10 ** dlog[2.5] - 1) < 1e-12, "MUTATE=1: not a constant")

import json
tag = "" if M == 0 else "_MUTATE%d" % M
with open(os.path.join(C.HERE, "A2_frw_flat_a0_and_dust_limit_results" + tag + ".json"), "w") as fjs:
    json.dump({"mode": M, "dlog_a0_dex": {str(z): float(dlog[z]) for z in ZS}}, fjs, indent=1)
R.finish()
