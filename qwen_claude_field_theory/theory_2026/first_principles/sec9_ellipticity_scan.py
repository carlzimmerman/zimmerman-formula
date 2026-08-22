#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec9_ellipticity_scan.py -- program section 9, part (d) numerics
================================================================
Numeric scan of the necessary-and-sufficient local conditions derived in
sec9_second_variation_symbol.py, along the SAME Newtonian point-mass profile
used by the repo's pointwise estimate mu_positivity_2026.py, and the honest
comparison with that script's chi_c ~ 1.73.

Profile and conventions (IDENTICAL to mu_positivity_2026.py):
  Phi0 = Psi0 = -1/x  (x in MOND radii R_M = sqrt(GM/a0); background slip is
  O(eps)),  g/a0 = x^-2,  X = x^-4,  Sbar_ij = (3 rhat rhat - delta)/x^3,
  Sbar^2 = 6/x^6 = 6 X^{3/2},  Sbar:khat khat = (3 tau^2 - 1) X^{3/4},
  tau = rhat.khat;  Y0 = Lambda Sbar^2,  chi = eps Lambda,
  Lambda = c^4/(G M a0) (dimensionless).  Every condition below is
  Lambda-free once written in chi (checked): units a0 = R_M = 1, eps c^4 = chi.

The invariants (loaded from sec9_symbol_invariants.json, derived in [B4]-[B5]):
  mu_dir(X, tau; chi) = mu + chi A' Sbar^2 + 2 (f_XX + chi A'' Sbar^2) X tau^2
  D(X, tau; chi)      = (2 chi A/3)(mu_dir - 1) - 4 chi^2 A'^2 X^{5/2}
                                                     tau^2 (3 tau^2 - 1)^2
  det M(k) = k^4 [ -mu_dir + D k^2 ]   (form-density normalisation)

Conditions scanned over the whole profile (X in [1e-3, 1e3]) and sphere
(tau^2 in [0,1]):
  (repo)  mu + chi A' Sbar^2 > 0 at tau = 0 only  -> reproduces chi_c = 1.7328
  (i)     mu_dir > 0 everywhere   (no real finite-k characteristic, healthy)
  (ii)    D < 0 everywhere        (DN-ellipticity with the healthy sign)
  honest  (i) AND (ii)
Also: the eps < 0 exclusion (any |chi|), with the explicit characteristic.

Exit code 1 on any FAIL.
"""
import sys, os, json, time
import numpy as np
import sympy as sp

T0 = time.time()
results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name, '   [t=%.1fs]' % (time.time() - T0))

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'sec9_symbol_invariants.json')) as f:
    inv = json.load(f)
mu_dir_e = sp.sympify(inv['mu_dir'])
D_e = sp.sympify(inv['D'])

def subs_by_name(expr, mapping):
    """substitute by symbol NAME (assumption-proof against the exporting script)"""
    tab = {str(a): a for a in expr.free_symbols}
    return expr.subs({tab[n]: v for n, v in mapping.items() if n in tab})

chi = sp.symbols('chi', real=True)
Xp = sp.symbols('X_prof', positive=True)
tau = sp.symbols('tau_prof', real=True)
Sbar2 = 6 * Xp**sp.Rational(3, 2)
sig_prof = (3 * tau**2 - 1) * Xp**sp.Rational(3, 4)
# profile substitution: a0 = R_M = 1, eps c^4 = chi (Lambda-free; checked below).
# eps and c appear only via eps*c^4 (= chi) and eps^2 c^8 (= chi^2) once
# Y0 = Lambda Sbar^2; in units Lambda = 1: eps -> chi, c -> 1, Y0 -> Sbar^2.
common = {'X_0': Xp, 'tau': tau, 'eta_K': sp.S(0), 'a_0': sp.S(1)}
mu_dir_p = subs_by_name(mu_dir_e, {**common, 'Y_0': Sbar2, 'c': sp.S(1),
                                   'epsilon': chi})
D_p = subs_by_name(D_e, {**common, 'Y_0': Sbar2, 'c': sp.S(1),
                         'epsilon': chi, 'sigma': sig_prof})
# Lambda-independence check: redo with Lambda = 137 (c = 137^(1/4),
# eps = chi/137, Y0 = 137 Sbar^2) and compare numerically
Lam = sp.S(137)
mu_dir_L = subs_by_name(mu_dir_e, {**common, 'Y_0': Lam * Sbar2,
                                   'c': Lam**sp.Rational(1, 4), 'epsilon': chi / Lam})
D_L = subs_by_name(D_e, {**common, 'Y_0': Lam * Sbar2,
                         'c': Lam**sp.Rational(1, 4), 'epsilon': chi / Lam,
                         'sigma': sig_prof})
for nm, ex in (('mu_dir_p', mu_dir_p), ('D_p', D_p), ('mu_dir_L', mu_dir_L), ('D_L', D_L)):
    extra = ex.free_symbols - {Xp, tau, chi}
    assert not extra, '%s has unresolved symbols: %s' % (nm, extra)
f_md = sp.lambdify((Xp, tau, chi), mu_dir_p, 'numpy')
f_D = sp.lambdify((Xp, tau, chi), D_p, 'numpy')
f_mdL = sp.lambdify((Xp, tau, chi), mu_dir_L, 'numpy')
f_DL = sp.lambdify((Xp, tau, chi), D_L, 'numpy')
Xt_, tt_, ct_ = 2.7, 0.61, 1.3
check('[C0] Lambda-independence: the conditions depend on eps, c, Y0 only through'
      ' chi = eps Lambda (Lambda = c^4/(GM a0)); verified at Lambda = 137',
      abs(f_md(Xt_, tt_, ct_) - f_mdL(Xt_, tt_, ct_)) < 1e-12 and
      abs(f_D(Xt_, tt_, ct_) - f_DL(Xt_, tt_, ct_)) < 1e-12)

Xg = np.geomspace(1e-3, 1e3, 4000)
t2g = np.linspace(0.0, 1.0, 241)
TAU = np.sqrt(t2g)[None, :]
XG = Xg[:, None]

def worst(chi_v):
    md = f_md(XG, TAU, chi_v)
    Dv = f_D(XG, TAU, chi_v)
    return md, Dv

def min_mu_dir(chi_v):
    return worst(chi_v)[0].min()

def max_D(chi_v):
    return worst(chi_v)[1].max()

def bisect(fail, lo=1e-4, hi=1e3, n=80):
    """smallest chi>0 at which `fail` first True (monotone assumed; verified by scan)"""
    if fail(lo): return lo
    if not fail(hi): return np.inf
    for _ in range(n):
        mid = np.sqrt(lo * hi)
        if fail(mid): hi = mid
        else: lo = mid
    return np.sqrt(lo * hi)

print('=' * 100)
print('[C1] reproduce the repo pointwise estimate (tau = 0 slice)')
print('=' * 100)
mu0 = lambda X: np.sqrt(np.sqrt(X)**2)**0.5 * 0 + np.sqrt(X)**0.5  # placeholder
def mu_of_X(X):
    xx = X**0.5
    return xx / (1 + xx)
def Ap_of_X(X): return 2 * X * (1 - X) / (1 + X)**5
chi_repo = bisect(lambda cv: (mu_of_X(Xg) + cv * Ap_of_X(Xg) * 6 * Xg**1.5).min() < 0)
print('  repo criterion  min_X [mu + chi A\' Sbar^2] > 0  fails first at chi = %.4f' % chi_repo)
check('[C1] reproduces mu_positivity_2026.py: chi_c(repo) = %.4f ~ 1.7328' % chi_repo,
      abs(chi_repo - 1.7328) < 0.01)
# consistency: our mu_dir at tau=0 equals the repo mu_eff
md0 = f_md(Xg, 0.0 * Xg, 0.9)
check('[C1.1] mu_dir(tau=0) == repo mu_eff = mu + chi A\' Sbar^2 (numeric identity)',
      float(np.abs(md0 - (mu_of_X(Xg) + 0.9 * Ap_of_X(Xg) * 6 * Xg**1.5)).max()) < 1e-10)

print('=' * 100)
print('[C2] the honest thresholds (chi > 0)')
print('=' * 100)
chi_i = bisect(lambda cv: min_mu_dir(cv) < 0)
chi_ii = bisect(lambda cv: max_D(cv) > 0)
chi_honest = min(chi_i, chi_ii)
md, Dv = worst(chi_i * 1.0001)
iX, it = np.unravel_index(np.argmin(md), md.shape)
print('  (i)  mu_dir > 0 everywhere fails first at  chi = %.4f' % chi_i)
print('       location: X = %.4g (x = %.3g R_M), tau^2 = %.3f' % (Xg[iX], Xg[iX]**-0.25, t2g[it]))
md2, Dv2 = worst(chi_ii * 1.0001)
jX, jt = np.unravel_index(np.argmax(Dv2), Dv2.shape)
print('  (ii) D < 0 everywhere (DN)   fails first at  chi = %.4f' % chi_ii)
print('       location: X = %.4g (x = %.3g R_M), tau^2 = %.3f' % (Xg[jX], Xg[jX]**-0.25, t2g[jt]))
print('  honest all-scale ellipticity threshold: chi_c(honest) = %.4f' % chi_honest)
print('  repo pointwise estimate:                chi_c(repo)   = %.4f' % chi_repo)
check('[C2.1] the honest threshold is STRICTER than the repo estimate:'
      ' chi_c(honest) = %.3f < chi_c(repo) = %.3f' % (chi_honest, chi_repo),
      chi_honest < chi_repo - 0.05)
# where does the honest condition fail while the repo criterion still passes?
chi_between = 0.5 * (chi_honest + min(chi_repo, chi_i if chi_i > chi_honest else chi_repo))
chi_demo = min(chi_honest * 1.2, chi_repo * 0.95)
md3, Dv3 = worst(chi_demo)
repo_ok = (mu_of_X(Xg) + chi_demo * Ap_of_X(Xg) * 6 * Xg**1.5).min() > 0
hon_bad = (md3.min() < 0) or (Dv3.max() > 0)
print('  DEMO at chi = %.3f: repo criterion PASSES (min mu_eff = %.4f > 0) but the' %
      (chi_demo, (mu_of_X(Xg) + chi_demo * Ap_of_X(Xg) * 6 * Xg**1.5).min()))
if Dv3.max() > 0:
    kX, kt = np.unravel_index(np.argmax(Dv3), Dv3.shape)
    print('       honest condition FAILS via (ii): D = %+.3g > 0 at X = %.3g'
          ' (x = %.3g R_M), tau^2 = %.3f' % (Dv3.max(), Xg[kX], Xg[kX]**-0.25, t2g[kt]))
    mdk = f_md(Xg[kX], np.sqrt(t2g[kt]), chi_demo)
    if mdk > 0:
        print('       and mu_dir = %.4f > 0 there => REAL characteristic at'
              ' k = %.3g / R_M in that direction' % (mdk, np.sqrt(mdk / Dv3.max())))
if md3.min() < 0:
    kX, kt = np.unravel_index(np.argmin(md3), md3.shape)
    print('       honest condition also FAILS via (i): min mu_dir = %.4f at X = %.3g,'
          ' tau^2 = %.2f' % (md3.min(), Xg[kX], t2g[kt]))
check('[C2.2] explicit regime where the repo criterion passes but the honest'
      ' condition fails (chi = %.3f)' % chi_demo, repo_ok and hon_bad)
print('  DRIVER: the tau^2-anisotropy 2(f_XX + chi A\'\' Sbar^2) X tau^2.  At X = 1')
print('  A\'(1) = 0 -- the repo mu_eff correction VANISHES there -- but')
print('  A\'\'(1) = -1/16 != 0: mu_dir(X=1, tau=1) = 3/4 - (3/4) chi, zero at chi = 1.')
md_x1 = f_md(1.0, 1.0, 1.0)
check('[C2.3] closed form at the failure point: mu_dir(X=1, tau=1, chi) = (3/4)(1-chi):'
      ' the honest chi_c <= 1 exactly where the repo correction is blind',
      abs(md_x1) < 1e-12 and abs(f_md(1.0, 1.0, 0.5) - 0.375) < 1e-12)

print('=' * 100)
print('[C3] chi < 0 (eps < 0): excluded at ANY magnitude')
print('=' * 100)
ok_neg = True
for chim in (-1e-3, -1e-2, -0.1, -1.0):
    md, Dv = worst(chim)
    md0 = f_md(Xg, 0.0 * Xg, chim)
    D0 = f_D(Xg, 0.0 * Xg, chim)
    # healthy transverse points with same-sign D => real characteristic
    sick = (md0 > 0) & (D0 > 0)
    frac = float(np.mean(sick))
    if np.any(sick):
        ii = int(np.argmax(sick))
        kchar = float(np.sqrt(md0[ii] / D0[ii]))
        print('  chi = %8.3g : real characteristic at e.g. X = %.3g, tau = 0,'
              ' k_char = %.3g / R_M  (%.0f%% of profile points affected)'
              % (chim, Xg[ii], kchar, 100 * frac))
    ok_neg = ok_neg and bool(np.any(sick))
check('[C3] every chi < 0 tested produces a real finite-k characteristic on the'
      ' profile (the [B6.2] theorem, instantiated)', ok_neg)

print('=' * 100)
print('[C4] context: the solar-system mechanism needed chi ~ 12; ellipticity dies at'
      ' chi ~ %.2f' % chi_honest)
print('=' * 100)
for cv in (0.5, 1.0, 1.7328, 2.0, 12.0):
    md, Dv = worst(cv)
    repo_min = (mu_of_X(Xg) + cv * Ap_of_X(Xg) * 6 * Xg**1.5).min()
    print('  chi = %7.3f : min mu_dir = %+8.4f   max D = %+9.3g   repo min mu_eff = %+8.4f'
          % (cv, md.min(), Dv.max(), repo_min))
print('  => the repo verdict (mechanism needs chi ~ 12 >> chi_c) SURVIVES and gets')
print('     STRONGER: the honest all-scale threshold is chi_c = %.3f, not 1.73;' % chi_honest)
print('     ratio required/allowed = %.1f (repo said 6.9).' % (12.0 / chi_honest))

print('=' * 100)
nfail = sum(1 for _, okc in results if not okc)
print('SUMMARY: %d checks, %d FAIL   [total %.1fs]' % (len(results), nfail, time.time() - T0))
sys.exit(1 if nfail else 0)
