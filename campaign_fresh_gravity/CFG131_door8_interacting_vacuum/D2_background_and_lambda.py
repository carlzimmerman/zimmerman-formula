#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D2 -- Door 8, deliverable 2: the background evolution, whether Lambda stays a global constant, and a0(z).

  A (sympy, minisuperspace of CFG43's action): S = int { -3 Mp2 a a'^2/N - N a^3 Mp2 Lambda + Mp2 Lambda T0' - N a^3 rho(n; Lambda) + J theta' + l(T0) }.
      Euler-Lagrange in T0:  Mp2 Lambda' = dl/dT0.   With l = 0 (CFG43: the matter Lagrangian has no T0 dependence) Lambda' = 0 whatever rho(n; Lambda) is
      (CFG43's 'global integration constant', re-derived).  The shift T0 -> T0 + c is a symmetry iff dl/dT0 = 0 (Noether: Lambda' = 0 IS the shift charge).
      => an exchange with Lambda' = -Q != 0 (covariant D1: d_mu rho_L = Q u_mu, i.e. rho_L' = -a Q) REQUIRES explicit T0 dependence (breaks the HT 4-form gauge symmetry),
      so it is not the HT sector any more; Q does NOT keep Lambda a global constant.  No action is constructed here (untested: whether one exists).
  B Q a function of Lambda only (the only cold-safe entry, D1/D3):  Q = xi H_L rho_L, H_L = sqrt(rho_L/3 Mp2).  Closed form (sympy): rho_L^(-1/2) rises linearly in t:
        a0(t)/a0(0) = 1/(1 + xi sqrt(Omega_L) H0 (t - t0)/2)   (a0 = kappa c sqrt(G rho_L), so a0 is proportional to sqrt(rho_L)).
      Numerical background (flat FRW, LCDM early data, a0(0) anchored) for a scan of xi: a0(z)/a0(0), H0 shift, comoving distance out to z = 999 (a theta_* proxy: reported, NOT a gate).
  C The record's flat-a0(z) standing (< 1% for z <= 5): the largest |xi| that keeps it, and what Q buys at that size.

MUTATE=1: Q dropped (xi = 0) in the claim 'Q != 0 makes a0(z) depart from flat by more than 1% at |xi| = 0.3': must FAIL (exit 1).
MUTATE=2: the claim of A2 is replaced by 'Lambda is dynamical even with l = 0 (no explicit T0 dependence)': sympy shows Lambda' = 0 there, so the mutated claim must FAIL (exit 1).
Run: python3 D2_background_and_lambda.py
"""
import os, sys, math
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.integrate import solve_ivp, quad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import Dcommon as C

R = C.Run("D2_background_and_lambda")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)

# ============================================================================================ A: HT minisuperspace
R.banner("A  HT sector: Euler-Lagrange in T0 and the shift symmetry (sympy)")
tt = sp.Symbol('t')
Mp2, m = sp.symbols('Mp2 m', positive=True)
a = sp.Function('a')(tt); N = sp.Function('N')(tt); Lam = sp.Function('Lam')(tt); T0 = sp.Function('T0')(tt)
J0 = sp.Function('J0')(tt); th = sp.Function('th')(tt)
rho_fn = sp.Function('rho_fluid')                       # rho(n; Lambda), arbitrary
n_of = J0 / a ** 3
ell = sp.Function('ell')                                 # extra matter term l(T0)  (explicit T0 dependence)
Lg_base = -3 * Mp2 * a * a.diff(tt) ** 2 / N - N * a ** 3 * Mp2 * Lam + Mp2 * Lam * T0.diff(tt) - N * a ** 3 * rho_fn(n_of, Lam) + J0 * th.diff(tt)
fields = [a, N, Lam, T0, J0, th]
EL0 = {str(f.func): e.lhs for f, e in zip(fields, euler_equations(Lg_base, fields, tt))}
E_T0 = sp.simplify(EL0['T0'])
P("  CFG43 action: E_T =", E_T0, " (= -Mp2 Lambda')")
okA1 = sp.simplify(E_T0 + Mp2 * Lam.diff(tt)) == 0
check("A1", "with a matter Lagrangian that has no T0 dependence (CFG43), E_T reads Mp2 Lambda' = 0 for ANY rho(n; Lambda)", "sympy: E_T = %s -> %s" % (E_T0, okA1), okA1, "re-derives CFG43's 'Lambda is a global integration constant'")
L_int = Lg_base + ell(T0)
EL1 = {str(f.func): e.lhs for f, e in zip(fields, euler_equations(L_int, fields, tt))}
E_T1 = sp.simplify(EL1['T0'])
P("  with an explicit T0 term l(T0): E_T =", E_T1, "  => Mp2 Lambda' = dl/dT0")
if M == 2:
    okA2 = sp.simplify(sp.solve(sp.Eq(E_T0, 0), Lam.diff(tt))[0]) != 0                      # mutated claim: Lambda' != 0 even with l = 0
    check("A2", "MUTATED claim: Lambda' is nonzero even without explicit T0 dependence", "E_T0 solved for Lambda' gives %s" % sp.solve(sp.Eq(E_T0, 0), Lam.diff(tt)), okA2, "the control")
else:
    Lp = sp.solve(sp.Eq(E_T1, 0), Lam.diff(tt))[0]
    okA2 = sp.simplify(Lp - sp.diff(ell(T0), T0) / Mp2) == 0
    check("A2", "Lambda' = (1/Mp2) dl/dT0: a nonzero exchange needs explicit T0 dependence, which breaks the shift T0 -> T0 + c (the HT 4-form gauge symmetry)", "Lambda' = %s -> %s" % (Lp, okA2), okA2,
          "so Q != 0 makes Lambda a dynamical field on the fluid-orthogonal slicing (D1), NOT a global constant; the HT identification is lost.  Existence of an action realising it is untested")

# ============================================================================================ B: closed form
R.banner("B  Q a function of Lambda only: closed form for rho_L(t) and a0(z) (sympy)")
tS = sp.Symbol('t'); xi = sp.Symbol('xi', real=True); rl = sp.Function('rL')
Hl = sp.sqrt(rl(tS) / 3)                                  # Mp2 = 1
ode = sp.Eq(rl(tS).diff(tS), -xi * Hl * rl(tS))
u = sp.Function('u')                                      # u = rL^(-1/2)
u_ode = sp.simplify(sp.Derivative(rl(tS) ** sp.Rational(-1, 2), tS).doit().subs(rl(tS).diff(tS), -xi * Hl * rl(tS)))
P("  d(rho_L^(-1/2))/dt =", u_ode, "  (constant: xi/(2 sqrt 3) in units Mp2 = 1)")
okB1 = sp.simplify(u_ode - xi / (2 * sp.sqrt(3))) == 0
check("B1", "for Q = xi H_L rho_L: d(rho_L^(-1/2))/dt = xi/(2 sqrt 3 Mp): a0 ~ sqrt(rho_L) = 1/(1 + xi sqrt(Omega_L) H0 (t - t0)/2)", "sympy: %s" % okB1, okB1, "a0 is no longer flat: a0(z) departs at first order in xi")

xis = [-0.30, -0.10, -0.03, -0.01, 0.0, 0.01, 0.03, 0.10, 0.30]
ZS = [0.5, 1.0, 2.5, 5.0, 10.0]
P("")
P("  numerical backgrounds (rho_L(a = 1) anchored to the LCDM value; rho_c a^3 at z = 999 equal to LCDM; Q = xi H_L rho_L):")
P("   xi     a0(z)/a0(0) at z = %s    H0/H0ref   rho_c0/ref   D_m(z<=999)/ref-1 [theta* proxy]" % ", ".join("%g" % z for z in ZS))
tab = {}
E0 = None
for x_ in xis:
    bg = C.background(x_)
    a0r = [math.sqrt(C.bg_state(bg, 1 / (1 + z))[1] / C.bg_state(bg, 1.0)[1]) for z in ZS]
    H0 = C.bg_state(bg, 1.0)[2]
    rc0 = C.bg_state(bg, 1.0)[0] / (3 * C.OC)
    # comoving distance from z = 999 (the background's start) to 0 in units c/H0ref: dchi = c dlna/(a H); the z > 999 piece is common to all xi and omitted
    Dm = quad(lambda la: 1.0 / (math.exp(la) * C.bg_state(bg, math.exp(la))[2]), math.log(1e-3), 0.0, epsabs=1e-12, epsrel=1e-12)[0]
    tab[x_] = (a0r, H0, rc0, Dm)
Dm0 = tab[0.0][3]
for x_ in xis:
    a0r, H0, rc0, Dm = tab[x_]
    P("  %+5.2f   %s    %.5f    %.5f     %+.2e" % (x_, "  ".join("%.5f" % v for v in a0r), H0 / tab[0.0][1], rc0, Dm / Dm0 - 1))
# cross-check closed form vs numeric integration
xchk = 0.1
bg = C.background(xchk)
# cosmic time via t(a) = int dlna / H  (units H0ref = 1)
def t_of(a):
    return quad(lambda la: 1.0 / C.bg_state(bg, math.exp(la))[2], math.log(1e-3), math.log(a), epsabs=1e-12, epsrel=1e-12)[0]
z_c = 2.5
tz, t0 = t_of(1 / (1 + z_c)), t_of(1.0)
rl0 = C.bg_state(bg, 1.0)[1]
# closed form: rho_L^(-1/2)(t) = rho_L0^(-1/2) + xi (t - t0)/(2 sqrt 3)  =>  a0(z)/a0(0) = sqrt(rL(z)/rL0) = 1/(1 + xi sqrt(rL0/3) (t_z - t0)/2)
pred = 1.0 / (1.0 + xchk * math.sqrt(rl0 / 3.0) * (tz - t0) / 2.0)
num = math.sqrt(C.bg_state(bg, 1 / (1 + z_c))[1] / rl0)
check("B2", "the integrated background reproduces the closed form a0(z)/a0(0) = 1/(1 + xi sqrt(rho_L0/3)(t_z - t0)/2) (xi = 0.1, z = 2.5)", "numeric %.7f vs closed form %.7f (rel. diff %.1e)" % (num, pred, abs(num / pred - 1)), abs(num / pred - 1) < 1e-6, "")

# ============================================================================================ C: how much xi the flat-a0(z) law tolerates
R.banner("C  the flat-a0(z) standing (|a0(z)/a0(0) - 1| < 1% for z <= 5) against |xi|")
def dev5(x_):
    bg = C.background(x_)
    return max(abs(math.sqrt(C.bg_state(bg, 1 / (1 + z))[1] / C.bg_state(bg, 1.0)[1]) - 1) for z in (0.5, 1.0, 2.5, 5.0))
from scipy.optimize import brentq
xi1 = brentq(lambda x_: dev5(x_) - 0.01, 1e-4, 0.5)
P("  |xi| for which max_z<=5 |a0(z)/a0(0) - 1| = 1%%: %.4f (both signs are within 10%% of each other by symmetry at this order)" % xi1)
# what a modest xi buys: energy per Hubble time transferred
rho_ratio = lambda x_: (lambda bg: (C.bg_state(bg, 1.0)[1] / C.bg_state(bg, 1 / 3.5)[1]))(C.background(x_))
if M == 1:
    dev_claim = dev5(0.0)     # MUTATE=1: Q dropped
    check("C1", "CLAIM: with Q != 0 (|xi| = 0.3) a0(z) departs from flat by more than 1% within z <= 5", "MUTATED (xi = 0): max deviation %.2e" % dev_claim, dev_claim > 0.01, "the control")
else:
    dev_claim = dev5(0.3)
    check("C1", "CLAIM: with Q != 0 at |xi| = 0.3 a0(z) departs from flat by more than 1% within z <= 5, so the tie 'a0 flat' is lost", "max deviation at xi = 0.3: %.3f; threshold |xi| = %.4f" % (dev_claim, xi1), dev_claim > 0.01,
          "the flat-a0 law survives only for |xi| < %.4f, where the total energy moved over a Hubble time is xi H_L rho_L/rho_L ~ %.1f%% per Hubble time" % (xi1, 100 * xi1 * math.sqrt(0.685)))
check("C2", "with xi = 0 (no exchange) the background reproduces the flat a0(z) of CFG43 to 1e-6 and H0 to 1e-4 (the 9e-5 radiation term)", "max dev %.2e, H0/1 - 1 = %.2e" % (dev5(0.0), tab[0.0][1] - 1),
      dev5(0.0) < 1e-6 and abs(tab[0.0][1] - 1) < 1e-4, "control agreeing with CFG43 A2")
R.finish()
