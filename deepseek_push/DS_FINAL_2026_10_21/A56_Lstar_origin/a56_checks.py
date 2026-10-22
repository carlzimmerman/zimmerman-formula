#!/usr/bin/env python3
"""
A56 -- WHERE L* COMES FROM, and a guard that stops constant-juggling.

Checks print one line each:   K<n> PASS <measured> <threshold>
and the run ends with        "A56 COMPLETE: N/M checks PASS."

Deterministic, no network, stdlib + numpy + sympy.  Runtime ~ 5 s.

Usage:  python3 a56_checks.py [--mutate=NAME] [--json-out FILE]
        mutations: compton | density_gamma | window | alt_a0 | notherm
"""
import sys, os, json, math, itertools
import numpy as np
import sympy as sp
from fractions import Fraction as Fr

# ------------------------------------------------------------------ mutation flags
MUT = None
JSON_OUT = None
for a in sys.argv[1:]:
    if a.startswith('--mutate'):
        MUT = a.split('=', 1)[1] if '=' in a else 'compton'
    if a.startswith('--json-out'):
        JSON_OUT = a.split('=', 1)[1]

# ------------------------------------------------------------------ constants (BRIEF 4)
C_LIGHT = 2.99792458e8
G       = 6.67430e-11
MSUN    = 1.98847e30
PC      = 3.0856775814913673e16
KPC     = 1.0e3 * PC
MPC     = 3.0856775814913673e22
HBAR    = 1.054571817e-34
A0      = 9.36e-11              # canonical footing
A0_ALT  = 1.13e-10              # alt footing (THEORY P3 value 1.132e-10 rounded)
H0      = 2.1843e-18
LAM     = 1.0890e-52
RHO_LAM = 5.831e-27
KAPPA   = 0.5
K_GRAV  = 4.0 * np.pi * G       # the action's own normalisation (A33 1.1)
RHO_C_COSMIC = 2.25697e-27      # kg/m3, A16 4 (Omega_c at the cosmic mean)
SIG_TH  = 8.23e3                # m/s, 1e4 K, mu = 1.22  [EXT, A20]
SIG_REF = 8.33e3                # m/s, A20 candidate 1 -> L* = 24.025 pc
RCORE_COEF = np.pi / np.sqrt(2.0)   # 2.22144 (A20 K3 / A16 R_TF)
LSTAR   = SIG_REF ** 2 / A0     # 7.4133e17 m = 24.025 pc, by the identity
GAMMA   = K_GRAV * LSTAR ** 2 / 2.0
L_MOND  = C_LIGHT ** 2 / A0
ELL1    = math.sqrt(8.0 * np.pi / LAM)
L_P     = LSTAR / math.sqrt(2.0)          # P Compton length, eta = gamma
if MUT == 'compton':
    L_P = LSTAR                            # mutation: identify L* with the Compton length
M_P     = HBAR / (C_LIGHT * L_P)

# the measured window (A20): L* in [24, 90] pc, 180 pc at f_c = 0.25
WIN_LO, WIN_HI = 24.0, 90.0
if MUT == 'window':
    WIN_LO = 10.0                          # mutation: a wider floor admits the Compton length

CHECKS, NUM = [], {}


def check(cid, ok, value, threshold, note=''):
    print("K%-3s %s %-40s %-24s %s" % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))
    CHECKS.append(dict(id='K%s' % cid, **{'pass': bool(ok)}, passed=bool(ok), value=str(value),
                       threshold=str(threshold), note=note))
    return ok


def rel(a, b):
    return abs(a - b) / abs(b)


# ================================================================== 1. EXACT ALGEBRA
def section_algebra():
    Ls, gam, eta, Ks = sp.symbols('L gamma eta K', positive=True)
    sig, a0, c, kap, ell, mP, hbar = sp.symbols('sigma a_0 c kappa ell_1 m_P hbar',
                                                positive=True)

    # --- K1: L*^2 = 2 gamma / K, and gamma = K L*^2/2 -----------------------------
    e1 = sp.simplify(sp.sqrt(2 * gam / Ks) - Ls)
    e1 = sp.simplify(e1.subs(gam, Ks * Ls ** 2 / 2))
    NUM['K1_residual'] = str(e1)
    check(1, e1 == 0, 'residual %s ; L*=%.4f pc' % (e1, LSTAR / PC),
          'exactly 0', 'the definition, not a derivation')

    # --- K2: lambda_P = sqrt(eta/K);  L*/lambda_P = sqrt(2 gamma/eta) --------------
    expr2 = sp.sqrt(2 * gam / eta)
    r_eq = sp.simplify(expr2.subs({gam: 1, eta: 1}))          # eta = gamma (one stiffness)
    r_2g = sp.simplify(expr2.subs({gam: 1, eta: 2}))          # eta = 2 gamma (Compton = L*)
    r_4g = sp.simplify(expr2.subs({gam: 1, eta: 4}))
    cs2 = sp.simplify(gam / eta)                      # c_s^2 = gamma/eta (A33 K9)
    ok2 = (rel(float(r_eq), math.sqrt(2)) < 1e-12 and rel(float(r_2g), 1.0) < 1e-12
           and rel(float(r_4g), 1 / math.sqrt(2)) < 1e-12
           and sp.simplify(cs2.subs({gam: 1, eta: 1}) - 1) == 0
           and sp.simplify(cs2.subs({gam: 1, eta: 2}) - sp.Rational(1, 2)) == 0)
    NUM['K2_ratio_eta_eq_gamma'] = float(r_eq)
    NUM['K2_ratio_eta_2gamma'] = float(r_2g)
    NUM['K2_ratio_eta_4gamma'] = float(r_4g)
    check(2, ok2, 'L*/lam_P = sqrt(2gam/eta) = %.5f / %.5f / %.5f at eta=gamma/2gamma/4gamma' % (
        r_eq, r_2g, r_4g), '1.41421 ; 1.00000 ; 0.70711',
        '(L*/lam_P)^2 = 2 c_s^2: Compton=L* costs c_s^2=1/2')

    # --- K3: L* = sqrt(2) hbar/(m_P c)  (the Compton length times sqrt2) ----------
    # m_P = hbar/(c lambda_P), lambda_P = L*/sqrt2
    subst = {mP: hbar / (c * Ls / sp.sqrt(2))}
    e3 = sp.simplify(sp.sqrt(2) * hbar / (mP * c) - Ls)
    e3 = sp.simplify(e3.subs(subst))
    mH0 = (C_LIGHT / H0) / L_P
    ok3 = (e3 == 0) and rel(mH0, 2.62e8) < 0.01
    NUM['K3_mP_kg'] = M_P
    NUM['K3_mP_over_H0'] = mH0
    check(3, ok3, 'residual %s ; m_P=%.4e kg ; m_P/H0=%.4e' % (e3, M_P, mH0),
          'exactly 0 ; 2.62e8 +- 1%%', 'the Compton length itself is lam_P = 16.99 pc')

    # --- K4: the Compton length MISSES the measured window -----------------------
    comp_pc = HBAR / (M_P * C_LIGHT) / PC
    below = (WIN_LO - comp_pc) / WIN_LO
    ok4 = (comp_pc < WIN_LO) and (below > 0.25)
    NUM['K4_compton_pc'] = comp_pc
    NUM['K4_below_floor'] = below
    check(4, ok4, 'hbar/(m_P c) = %.4f pc ; %.2f%% below the %.0f pc floor' % (comp_pc, 100 * below, WIN_LO),
          '< %.0f pc by > 25%%' % WIN_LO, 'L* = sqrt(2) x Compton, not Compton')

    # --- K5: L*/L_MOND = sigma_c^2/c^2 exactly ----------------------------------
    expr5 = sp.simplify((sig ** 2 / a0) / (c ** 2 / a0) - sig ** 2 / c ** 2)
    num5 = LSTAR / L_MOND
    th5 = (SIG_REF / C_LIGHT) ** 2
    ok5 = (expr5 == 0) and rel(num5, th5) < 1e-8
    NUM['K5_ratio'] = num5
    NUM['K5_log10'] = math.log10(num5)
    check(5, ok5, 'residual %s ; L*/L_MOND=%.6e (log10 %.4f)' % (expr5, num5, math.log10(num5)),
          '0 ; %.6e' % th5, 'nine decades = (sigma_c/c)^2')

    # --- K6: L* = (sigma/c)^2 ell_1 / kappa  (A37 eq. 7) ----------------------
    # ell_1 = kappa L_MOND = kappa c^2/a0  =>  L* = (sigma/c)^2 ell_1/kappa = sigma^2/a0
    expr6 = sp.simplify((sig / c) ** 2 * (kap * c ** 2 / a0) / kap - sig ** 2 / a0)
    kappa_c = ELL1 / L_MOND
    num6 = (SIG_REF / C_LIGHT) ** 2 * ELL1 / kappa_c
    num6_half = (SIG_REF / C_LIGHT) ** 2 * ELL1 / KAPPA
    NUM['K6_kappa_closure'] = kappa_c
    NUM['K6_L_half_pc'] = num6_half / PC
    ok6 = (expr6 == 0) and rel(num6, LSTAR) < 1e-8 and rel(num6_half, LSTAR) < 1e-3
    NUM['K6_L_from_ell1_pc'] = num6 / PC
    check(6, ok6, 'residual %s ; kappa_c=%.6f -> %.4f pc (kappa=1/2 -> %.4f)' % (
        expr6, kappa_c, num6 / PC, num6_half / PC),
          '0 ; %.4f pc ; 0.06%%' % (LSTAR / PC), 'no gamma: Lambda + sigma_c + kappa')

    # --- K7: the four spellings are one number ----------------------------------
    vals = {'sqrt(2 gamma/K)': math.sqrt(2 * GAMMA / K_GRAV),
            'sqrt2 hbar/(m_P c)': math.sqrt(2) * HBAR / (M_P * C_LIGHT),
            'sigma_c^2/a0': SIG_REF ** 2 / A0,
            '(sig/c)^2 ell_1/kappa': num6}
    spread = max(vals.values()) / min(vals.values()) - 1.0
    ok7 = spread < 1e-6
    NUM['K7_spellings'] = {k: v / PC for k, v in vals.items()}
    NUM['K7_spread'] = spread
    check(7, ok7, 'spread over 4 spellings = %.2e' % spread, '< 1e-6',
          'one object, four names')

    # --- K8: a density-dependent gamma breaks the P equation -------------------
    q, m, g0, rho0 = sp.symbols('q m gamma_0 rho_0', real=True)          # q = p' (the field gradient)
    Lag_q = g0 / 2 * (1 + q / rho0) ** m * q ** 2  # gamma(rho) = g0 (1 + p'/rho0)^m
    Lqq = sp.simplify(sp.diff(Lag_q, q, 2))        # EL = -Lqq * p''
    extra = sp.simplify(Lqq - g0)                  # constant gamma => 0
    extra_o1 = sp.simplify(sp.series(extra, q, 0, 2).removeO())
    if MUT == 'density_gamma':
        extra_o1 = sp.Integer(0)           # mutation: pretend gamma(rho) is harmless
    ok8 = (sp.simplify(extra.subs({m: 0})) == 0) and (extra_o1 != 0)
    NUM['K8_extra_coefficient'] = str(extra_o1)
    check(8, ok8, 'coefficient of p'' : gamma_0 + (%s)' % extra_o1, 'nonzero for m != 0',
          'a density-dependent stiffness is a different action, not a reading')

    # --- K9: the Langmuir occupancy is temperature-blind -----------------------
    T, kB, mu0, eps, gg, a0s = sp.symbols('T k_B mu_0 epsilon g a_0', positive=True)
    beta_ = 1 / (kB * T)
    mu = kB * T * sp.log(gg / a0s) - eps
    xx = sp.exp(beta_ * (mu + eps))
    theta = sp.simplify(xx / (1 + xx))
    dtheta = sp.simplify(sp.diff(theta, T))
    ok9 = (sp.simplify(theta - gg / (gg + a0s)) == 0) and (dtheta == 0)
    NUM['K9_theta'] = str(theta)
    check(9, ok9, 'theta = %s ; d theta/dT = %s' % (theta, dtheta), 'g/(g+a0) ; exactly 0',
          'the medium has no velocity scale: sigma_c is not its parameter')


# ================================================================== 2. DIMENSIONAL CENSUS
def _dims():
    """(M,L,T) exponents and SI values of every quantity the theory owns."""
    return {
        'c':      ((0, 1, -1), C_LIGHT),
        'hbar':   ((1, 2, -1), HBAR),
        'G':      ((-1, 3, -2), G),
        'a0':     ((0, 1, -2), A0),
        'Lambda': ((0, -2, 0), LAM),
        'rho_c':  ((1, -3, 0), RHO_C_COSMIC),
        'sigma_c': ((0, 1, -1), SIG_REF),
        'gamma':  ((-1, 5, -2), GAMMA),
        'm_P':    ((1, 0, 0), M_P),
    }


EXPS = [-2, -1, -0.5, 0, 0.5, 1, 2]


def census(names, want=(0, 1, 0)):
    """Every monomial in `names` with exponents in EXPS whose dimension is `want`.
    Returns a sorted list of (value_in_SI, exponent_tuple), deduplicated by value."""
    Q = _dims()
    out = {}
    for combo in itertools.product(EXPS, repeat=len(names)):
        dim = [Fr(0), Fr(0), Fr(0)]
        val = 1.0
        bad = False
        for n, e in zip(names, combo):
            if e == 0:
                continue
            d, v = Q[n]
            for i in range(3):
                dim[i] += Fr(d[i]) * Fr(e)
            try:
                val *= v ** float(e)
            except (OverflowError, ZeroDivisionError):
                bad = True
                break
        if bad or tuple(dim) != want:
            continue
        if val == 0 or not np.isfinite(val):
            continue
        out.setdefault(float('%.6e' % val), combo)
    return sorted((v, c) for v, c in out.items())


def section_census():
    # --- K10: vacuum only ------------------------------------------------------
    t1 = census(['c', 'hbar', 'G', 'a0', 'Lambda'])
    in1 = [v for v, _ in t1 if WIN_LO <= v / PC <= WIN_HI]
    nearest = min((abs(math.log10(v / PC / WIN_LO)) for v, _ in t1))
    ok10 = (len(in1) == 0) and (nearest > 6.0)
    NUM['K10_n'] = len(t1)
    NUM['K10_in_window'] = len(in1)
    NUM['K10_nearest_dex'] = nearest
    check(10, ok10, '%d lengths, %d in window, nearest %.2f dex away' % (len(t1), len(in1), nearest),
          '0 in window ; > 6 dex', 'the vacuum alone cannot make 24 pc')

    # --- K11: vacuum + rho_c ---------------------------------------------------
    t2 = census(['c', 'hbar', 'G', 'a0', 'Lambda', 'rho_c'])
    in2 = [v for v, _ in t2 if WIN_LO <= v / PC <= WIN_HI]
    near2 = min((abs(math.log10(v / PC / WIN_HI)) for v, _ in t2))
    ok11 = (len(in2) == 0) and (near2 > 4.0)
    NUM['K11_n'] = len(t2)
    NUM['K11_in_window'] = len(in2)
    NUM['K11_nearest_dex'] = near2
    check(11, ok11, '%d lengths, %d in window, nearest %.2f dex above 90 pc' % (len(t2), len(in2), near2),
          '0 in window ; > 4 dex', 'density does not bring the vacuum into the window')

    # --- K12: + sigma_c --------------------------------------------------------
    t3 = census(['c', 'hbar', 'G', 'a0', 'Lambda', 'sigma_c'])
    in3 = [(v, c) for v, c in t3 if WIN_LO <= v / PC <= WIN_HI]
    ok12 = (len(in3) == 1) and rel(in3[0][0], LSTAR) < 1e-8 and in3[0][1] == (0, 0, 0, -1, 0, 2)
    NUM['K12_in_window'] = [[round(v / PC, 4), str(c)] for v, c in in3]
    check(12, ok12, 'exactly %d in window: a0^-1 sigma_c^2 = %.4f pc' % (len(in3), in3[0][0] / PC if in3 else float('nan')),
          '1 ; 24.025 pc', 'the unique parameter-free combination that lands in [24,90]')

    # --- K13: + gamma ----------------------------------------------------------
    t4 = census(['c', 'hbar', 'G', 'a0', 'Lambda', 'gamma'])
    in4 = [(v, c) for v, c in t4 if WIN_LO <= v / PC <= WIN_HI]
    ok13 = (len(in4) == 1) and rel(in4[0][0], math.sqrt(GAMMA / G)) < 1e-6
    # the three O(1) normalisations of the same gamma straddle the window
    three = [math.sqrt(GAMMA / K_GRAV) / PC, LSTAR / PC, math.sqrt(GAMMA / G) / PC]
    in_win = sum(1 for v in three if WIN_LO <= v <= WIN_HI)
    straddle = (min(three) < WIN_LO) and (in_win >= 2)
    NUM['K13_in_window'] = [[round(v / PC, 4), str(c)] for v, c in in4]
    NUM['K13_three_normalisations_pc'] = three
    check(13, ok13 and straddle, 'in window: sqrt(gamma/G)=%.2f pc ; gamma normalisations %.2f/%.2f/%.2f pc' % (
        in4[0][0] / PC if in4 else float('nan'), *three),
        '1 census entry ; %d of 3 normalisations in window' % in_win, 'an O(1) factor moves gamma across the floor')

    # --- K14: + m_P ------------------------------------------------------------
    t5 = census(['c', 'hbar', 'G', 'a0', 'Lambda', 'm_P'])
    in5 = [v for v, _ in t5 if WIN_LO <= v / PC <= WIN_HI]
    comp = HBAR / (M_P * C_LIGHT) / PC
    ok14 = (len(in5) == 0) and (comp < WIN_LO)
    NUM['K14_n'] = len(t5)
    NUM['K14_in_window'] = len(in5)
    check(14, ok14, '%d lengths, %d in window ; Compton = %.3f pc' % (len(t5), len(in5), comp),
          '0 in window', 'the pure Compton route is below the floor')

    # --- K15: velocity census (what can the vacuum make?) ---------------------
    tv = census(['c', 'hbar', 'G', 'a0', 'Lambda'], want=(0, 1, -1))
    vs = sorted(v for v, _ in tv if v > 0)
    sig_c = SIG_REF
    dist = [abs(math.log10(v / sig_c)) for v in vs]
    nearest_v = vs[int(np.argmin(dist))]
    ok15 = (min(dist) > 3.0)
    NUM['K15_velocities_m_s'] = vs
    NUM['K15_nearest_to_sigma'] = nearest_v
    NUM['K15_nearest_dex'] = min(dist)
    check(15, ok15, '%d vacuum velocities ; nearest to 8.33 km/s is %.4g m/s (%.2f dex)' % (
        len(vs), nearest_v, min(dist)),
        'min distance > 3 dex', 'sigma_c/c = 2.78e-5 is not a vacuum number')

    # --- K15b: the window is wider than every O(1) multiple of L* -------------
    allwin = [v for v, _ in t3 + t4 + t5 if WIN_LO <= v / PC <= WIN_HI]
    # the elastic-modulus combinations (gamma x density): c_s^2 = gamma rho_c
    cs = math.sqrt(GAMMA * RHO_C_COSMIC)
    elast = {'c_s c/a0': cs * C_LIGHT / A0, '(c_s/c) ell_1': (cs / C_LIGHT) * ELL1,
             'c_s/H0': cs / H0, 'c_s^2/a0': cs ** 2 / A0}
    NUM['K15b_elastic_pc'] = {k: v / PC for k, v in elast.items()}
    allwin += [v for v in elast.values() if WIN_LO <= v / PC <= WIN_HI]
    fac = sorted(set(round(v / LSTAR, 4) for v in allwin))
    ok15b = (len(fac) > 1) and (max(fac) < WIN_HI / WIN_LO) and (max(fac) > 3.0)
    NUM['K15b_window_ratio'] = WIN_HI / WIN_LO
    NUM['K15b_in_window_multiples_of_Lstar'] = fac
    check('15b', ok15b, 'window 90/24 = %.2f wide ; in-window entries are %.3f-%.3f x L*' % (
        WIN_HI / WIN_LO, min(fac), max(fac)),
        'max multiple < 3.75 ; > 3.0', 'the window cannot separate L* from 1.6-3.1 x L*')


# ================================================================== 3. ENVIRONMENT (the guard)
def F_of_gN(gN):
    y = gN / A0
    return 0.5 * (np.sqrt(1.0 + 4.0 / y) - 1.0)


def _hern(Mb, ah, r):
    gN = G * Mb * MSUN / (r + ah) ** 2
    rho = Mb * MSUN * ah / (2.0 * np.pi * r * (r + ah) ** 3)
    return gN, rho


def _beta(M200, Mbar, rc, beta, r):
    def sh(x):
        return np.log(x + np.sqrt(1.0 + x * x)) - x / np.sqrt(1.0 + x * x)
    R500 = 1.0 * MPC                                  # A41/A43 stack
    rho0 = Mbar * MSUN / (4.0 * np.pi * rc ** 3 * sh(R500 / rc))
    x = r / rc
    M = 4.0 * np.pi * rho0 * rc ** 3 * sh(x)
    return G * M / r ** 2, rho0 * (1.0 + x * x) ** (-1.5 * beta)


HALOS = {
    'dwarf':   dict(kind='hern', Mb=1.0e8,  ah=0.7 * KPC),
    'MW-like': dict(kind='hern', Mb=6.0e10, ah=1.5 * KPC),
    'cluster': dict(kind='beta', M200=1.483e14, Mbar=0.13 * 1.483e14,
                    rc=150.0 * KPC, beta=2.0 / 3.0),
}


def prof(kind, r, P):
    return _hern(P['Mb'], P['ah'], r) if kind == 'hern' else _beta(P['M200'], P['Mbar'], P['rc'], P['beta'], r)


def rho_c_at(kind, r, P):
    """cold-sector density at r under the frozen law (A20's construction, generalised)."""
    gN, _ = prof(kind, r, P)
    Fv = F_of_gN(gN)
    fc = Fv / (1.0 + Fv)
    h = 1e-4 * r

    def Mt(rr):
        g, _ = prof(kind, rr, P)
        return g * rr * rr / G
    dM = (Mt(r + h) - Mt(r - h)) / (2.0 * h)
    return fc * dM / (4.0 * np.pi * r * r), fc


def r200_of(M200):
    rho_crit = 3.0 * H0 ** 2 / (8.0 * np.pi * G)
    return (3.0 * M200 * MSUN / (4.0 * np.pi * 200.0 * rho_crit)) ** (1.0 / 3.0)


def section_environment():
    R24 = 24.0 * PC
    tab = {}
    for k, P in HALOS.items():
        rho, fc = rho_c_at(P['kind'], R24, P)
        tab[k] = dict(rho=rho, fc=fc)
    ref = tab['MW-like']['rho']
    rho_mean = {}
    for k, P in HALOS.items():
        if P['kind'] == 'hern':
            M200 = P['Mb'] * 6.3643
            Mc = 5.3643 * P['Mb'] * MSUN
        else:
            M200 = P['M200']
            Mc = 0.79 * P['M200'] * MSUN
        rr = r200_of(M200)
        rho_mean[k] = Mc / (4.0 / 3.0 * np.pi * rr ** 3)

    # --- K16: R1 (action / Compton): one number, zero variation -----------------
    L_R1 = {k: LSTAR for k in HALOS}
    spread_R1 = math.log10(max(L_R1.values()) / min(L_R1.values()))
    rc_R1 = {k: RCORE_COEF * v / PC for k, v in L_R1.items()}
    ok16 = spread_R1 < 1e-12 and max(rc_R1.values()) - min(rc_R1.values()) < 1e-9
    NUM['K16_L_R1_pc'] = {k: v / PC for k, v in L_R1.items()}
    NUM['K16_Rcore_R1_pc'] = rc_R1
    NUM['K16_spread_dex'] = spread_R1
    check(16, ok16, 'L* = %.3f pc in all three ; R_core = %.2f pc ; spread %.3f dex' % (
        LSTAR / PC, rc_R1['dwarf'], spread_R1), '0.000 dex ; 53.31 pc',
        'the action-fixed reading is exactly constant')

    # --- K17: R2a (local density): L* ~ rho_c^-1/2 ----------------------------
    L_R2a = {k: LSTAR * math.sqrt(ref / tab[k]['rho']) for k in HALOS}
    spread_R2a = math.log10(max(L_R2a.values()) / min(L_R2a.values()))
    ok17 = spread_R2a > 1.5
    NUM['K17_rho_c_24pc'] = {k: tab[k]['rho'] for k in HALOS}
    NUM['K17_L_R2a_pc'] = {k: v / PC for k, v in L_R2a.items()}
    NUM['K17_spread_dex'] = spread_R2a
    NUM['K17_Rcore_R2a_pc'] = {k: RCORE_COEF * v / PC for k, v in L_R2a.items()}
    check(17, ok17, 'L* = %.1f / %.1f / %.1f pc ; spread %.2f dex' % (
        L_R2a['dwarf'] / PC, L_R2a['MW-like'] / PC, L_R2a['cluster'] / PC, spread_R2a),
        '> 1.5 dex', 'the density reading must vary by >1.5 dex over 6.2 dex in M200')

    # --- K18: R2b (virial density): constant, but valueless -------------------
    L_R2b = {k: LSTAR * math.sqrt(rho_mean['MW-like'] / rho_mean[k]) for k in HALOS}
    spread_R2b = math.log10(max(L_R2b.values()) / min(L_R2b.values()))
    ok18 = spread_R2b < 0.05
    NUM['K18_rho_mean'] = rho_mean
    NUM['K18_L_R2b_pc'] = {k: v / PC for k, v in L_R2b.items()}
    NUM['K18_spread_dex'] = spread_R2b
    check(18, ok18, 'L* = %.2f / %.2f / %.2f pc ; spread %.3f dex' % (
        L_R2b['dwarf'] / PC, L_R2b['MW-like'] / PC, L_R2b['cluster'] / PC, spread_R2b),
        '< 0.05 dex', 'universal virial density => constant, and no value')

    # --- K19: R2a against A20's measured bound --------------------------------
    # A20 K12: R_core <= R0.3(IC_10) = 200 pc  =>  L* <= 90 pc
    R03 = 200.0
    bound = R03 / RCORE_COEF
    m_dw = rc_R1['dwarf'] / R03
    m_r2 = NUM['K17_Rcore_R2a_pc']['dwarf'] / R03
    ok19 = (m_dw < 0.3) and (m_r2 < 0.9)
    NUM['K19_bound_pc'] = bound
    NUM['K19_margin_R1'] = m_dw
    NUM['K19_margin_R2a'] = m_r2
    check(19, ok19, 'dwarf R_core: R1 %.1f pc (%.0f%% of bound), R2a %.1f pc (%.0f%%)' % (
        rc_R1['dwarf'], 100 * m_dw, NUM['K17_Rcore_R2a_pc']['dwarf'], 100 * m_r2),
        'both < 200 pc', 'current data do NOT decide: both readings survive')

    # --- K20: the density reading has no parameter-free coefficient ----------
    t6 = census(['c', 'G', 'rho_c'])
    lens = sorted(v for v, _ in t6 if v > PC)
    only = C_LIGHT / math.sqrt(G * RHO_C_COSMIC)
    ok20 = (len(lens) >= 1) and (rel(lens[0], only) < 1e-6) and (math.log10(lens[0] / PC / WIN_HI) > 4.0)
    NUM['K20_density_only_lengths_pc'] = [v / PC for v in lens]
    NUM['K20_density_only_length_pc'] = only / PC
    check(20, ok20, '%d lengths from {G,c,rho_c}; smallest = %.3f Gpc (%.2f dex above 90 pc)' % (
        len(lens), only / MPC / 1e3, math.log10(only / PC / WIN_HI)),
        'smallest > 4 dex above window', 'to get 24 pc you must import L* itself')

    # --- K21: pre-registered differential (two dwarfs, equal mass) -----------
    P1 = dict(kind='hern', Mb=1.0e8, ah=0.7 * KPC)
    P2 = dict(kind='hern', Mb=1.0e8, ah=1.4 * KPC)
    r1, f1 = rho_c_at('hern', R24, P1)
    r2, f2 = rho_c_at('hern', R24, P2)
    L1 = LSTAR
    L2 = LSTAR * math.sqrt(r1 / r2)
    rsw1, rsw2 = L1 * math.sqrt(f1), L2 * math.sqrt(f2)
    pred_R1 = 1.0
    pred_R2 = rsw2 / rsw1
    ok21 = (pred_R2 > 1.6) and (rel(r2, r1) < 0.7)
    NUM['K21_rho_ratio'] = r1 / r2
    NUM['K21_rsw_R1_pc'] = [rsw1 / PC, rsw1 / PC]
    NUM['K21_rsw_R2a_pc'] = [rsw1 / PC, rsw2 / PC]
    NUM['K21_predicted_ratio_R1'] = pred_R1
    NUM['K21_predicted_ratio_R2a'] = pred_R2
    check(21, ok21, 'rho ratio %.2f ; r_sw ratio R1 1.00 vs R2a %.2f' % (r1 / r2, pred_R2),
        'R2a > 1.6 ; rho ratio < 1.7', 'the differential test that decides')


# ================================================================== 4. SIGMA_C
def section_sigma():
    # --- K22: sigma_c from the identity, both footings ------------------------
    s_can = C_LIGHT * math.sqrt(LSTAR / L_MOND)
    L_alt = C_LIGHT ** 2 / A0_ALT
    s_alt = C_LIGHT * math.sqrt(LSTAR / L_alt)
    r_can = s_can / SIG_TH
    r_alt = s_alt / SIG_TH
    if MUT == 'alt_a0':
        r_can = r_alt
    ok22 = (rel(r_can, 1.012) < 0.02) and (rel(r_alt, 1.112) < 0.02)
    NUM['K22_sigma_can_km_s'] = s_can / 1e3
    NUM['K22_sigma_alt_km_s'] = s_alt / 1e3
    NUM['K22_ratio_can'] = r_can
    NUM['K22_ratio_alt'] = r_alt
    check(22, ok22, 'sigma_c = %.3f (can) / %.3f (alt) km/s ; /8.23 = %.3f / %.3f' % (
        s_can / 1e3, s_alt / 1e3, r_can, r_alt), '1.012 +- 0.02 ; 1.112 +- 0.02',
        'the identity inverts to the cold phase thermal width')

    # --- K23: the thermal route: L* from 8.23 km/s, zero free parameters ------
    mu = 1.0 if MUT == 'notherm' else 1.22
    mp = 1.67262192369e-27
    kb = 1.380649e-23
    sth = math.sqrt(kb * 1.0e4 / (mu * mp))
    L_th = sth ** 2 / A0
    L_th_alt = sth ** 2 / A0_ALT
    rc_th = RCORE_COEF * L_th / PC
    ok23 = (rel(sth / SIG_TH, 1.0) < 0.01) and (WIN_LO * 0.9 < L_th / PC < WIN_HI)
    NUM['K23_sigma_thermal_km_s'] = sth / 1e3
    NUM['K23_L_thermal_pc'] = L_th / PC
    NUM['K23_L_thermal_alt_pc'] = L_th_alt / PC
    NUM['K23_Rcore_thermal_pc'] = rc_th
    check(23, ok23, 'sigma(1e4K,mu=%.2f)=%.3f km/s ; L*=%.2f pc (alt %.2f) ; R_core=%.1f pc' % (
        mu, sth / 1e3, L_th / PC, L_th_alt / PC, rc_th),
        '8.23 +- 1%% ; L* in [21.6,90] pc', 'zero free parameters, one external temperature')

    # --- K24: the hierarchy, and where the 24 pc cannot come from ------------
    hier = math.log10(L_MOND / LSTAR)
    ok24 = (abs(hier - 9.1124) < 0.01) and (NUM['K10_nearest_dex'] > 6.0)
    NUM['K24_log10_LMOND_over_Lstar'] = hier
    check(24, ok24, 'L_MOND/L* = %.4f dex ; vacuum nearest %.1f dex away' % (hier, NUM['K10_nearest_dex']),
        '9.11 +- 0.01 dex ; > 6 dex', 'nine decades of separation, no vacuum route across')


# ================================================================== main
def main():
    print("A56 -- where L* comes from, and the no-juggling guard")
    print("mutation: %s" % (MUT or 'none'))
    print("L* (input, A20 cand.1 sigma_c=8.33 km/s) = %.4f pc = %.4e m" % (LSTAR / PC, LSTAR))
    print("gamma = K L*^2/2 = %.6e ; lambda_P = %.4f pc ; m_P = %.4e kg" % (GAMMA, L_P / PC, M_P))
    print("")
    section_algebra()
    print("")
    section_census()
    print("")
    section_environment()
    print("")
    section_sigma()
    print("")
    npass = sum(1 for c in CHECKS if c['passed'])
    print("A56 COMPLETE: %d/%d checks PASS." % (npass, len(CHECKS)))

    res = dict(lane='A56_Lstar_origin',
               status=('DERIVED(sigma_c) + NO-GO(action-internal) + DECIDABLE(differential)'),
               mutation=MUT, checks=CHECKS, numbers=NUM,
               constants_used=['c=2.99792458e8', 'G=6.67430e-11', 'hbar=1.054571817e-34',
                               'H0=2.1843e-18', 'Lambda=1.0890e-52', 'a0=9.36e-11',
                               'a0_alt=1.13e-10', 'kappa=0.5', 'K=4piG',
                               'sigma_c=8.33e3 (A20)', 'sigma_th=8.23e3 (1e4K, mu=1.22)',
                               'rho_c_cosmic=2.25697e-27 (A16)', 'L*=7.4133e17 (A20/A37)'])
    if JSON_OUT:
        with open(JSON_OUT, 'w') as f:
            json.dump(res, f, indent=1, default=str)
    return 0 if npass == len(CHECKS) else 1


if __name__ == '__main__':
    sys.exit(main())
