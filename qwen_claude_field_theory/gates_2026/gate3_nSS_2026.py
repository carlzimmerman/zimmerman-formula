#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate3_nSS_2026.py -- GATE 3: the Solar-System-required transition sharpness n_SS.

Carl's five-gate program, Gate 3. Independently of SPARC, determine the transition
sharpness the Solar-System quadrupole REQUIRES, using the corrected Milgrom
normalisation established in the closure phase.

CONVENTIONS, stated once and never re-derived silently
------------------------------------------------------
Milgrom 2009 (arXiv:0906.4817):   g_i = -q_ij x^j,  q_ij traceless axisymmetric,
    -2q_xx = -2q_yy = q_zz = q(eta) a_0/R_M,  R_M = sqrt(GM_sun/a_0).
    => delta Phi = (1/2) q_ij x^i x^j = (1/2) q_zz r^2 P_2   =>   c_2 = q_zz/2.
Desmond-Hees-Famaey 2024 Q_2 convention (as Carl states it):
    delta Phi = -(Q_2/2) x^i x^j (e_i e_j - delta_ij/3) = -(Q_2/3) r^2 P_2
    => c_2 = -Q_2/3.
THEREFORE   Q_2 = -(3/2) q_zz   and   |Q_2| = 3|c_2| = (3/2) q_Milgrom (a_0/R_M).
Both statements are consistent; the historical 1.45x discrepancy was exactly this 3/2.

The kernel family is Carl's Gate-1 microscope:
    mu_n(x) = x/(1+x^n)^(1/n)      -> x (x<<1),  -> 1 (x>>1),  n->inf sharp
whose EXACT QUMOND conjugate is
    nu_n(y) = [ (1 + sqrt(1+4 y^-n))/2 ]^(1/n)
(derived below symbolically, not asserted).  n is the ONLY shape parameter and the
asymptotics are n-INDEPENDENT, which is precisely Gate 1's requirement.
"""
import sys
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq

FAIL, NCHK = [], [0]
def check(cond, label, detail=""):
    NCHK[0] += 1; ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok
def info(l, d=""): print(f"  [info] {l}" + (f"   {d}" if d else ""))
def head(t): print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)

print(__doc__)
G_, MSUN = 6.6743e-11, 1.98892e30
GM_SUN = G_ * MSUN
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

# ---------------------------------------------------------------- Part A: the conjugate
head("PART A -- the exact QUMOND conjugate of mu_n, DERIVED not asserted")
import sympy as sp
x, y, nn = sp.symbols('x y n', positive=True)
mu = x/(1+x**nn)**(sp.Rational(1,1)/nn)
yy = sp.simplify(x*mu)                     # y = x mu(x)
u = sp.symbols('u', positive=True)         # u = x^n
# y^n = x^{2n}/(1+x^n) = u^2/(1+u)  ->  u^2 - y^n u - y^n = 0
quad = sp.Eq(u**2 - y**nn*u - y**nn, 0)
uroot = sp.solve(quad, u)
uplus = [r for r in uroot if float(r.subs({nn: 2, y: 1.7})) > 0][0]
info("A1  y^n = u^2/(1+u) with u = x^n", f"positive root u = {sp.simplify(uplus)}")
# nu = 1/mu = (1+u)^{1/n}/x = ((1+u)/u)^{1/n} = (u/y^n)^{1/n}
nu_sym = sp.simplify((uplus/y**nn)**(1/nn))
info("A2  nu_n(y) = 1/mu(x(y))", f"= {sp.simplify(nu_sym)}")
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from munu import nu_n_fn as nu_n          # log-space, stable to n~200 over 20 decades in y
# numeric verification of conjugacy: nu(x mu(x)) * x mu(x) == x
for n_ in (1.0, 2.0, 3.5, 8.0):
    xs = np.geomspace(1e-3, 1e3, 40)
    mus = xs/(1+xs**n_)**(1/n_); ys = xs*mus
    back = nu_n(n_)(ys)*ys
    check(np.allclose(back, xs, rtol=1e-10),
          f"A3  nu_{n_:g} is the EXACT conjugate of mu_{n_:g} (nu(y)y = x for y = x mu(x))",
          f"max rel err {np.max(np.abs(back/xs-1)):.2e}")
for n_ in (1.0, 3.0, 10.0):
    f = nu_n(n_)
    check(abs(f(1e8)-1) < 1e-6 and abs(f(1e-8)*np.sqrt(1e-8)-1) < 1e-4,
          f"A4  n={n_:g} asymptotics are n-INDEPENDENT: nu->1 deep-Newtonian, nu->y^(-1/2) deep-MOND",
          f"nu(1e8)-1={f(1e8)-1:.2e}   nu(1e-8)*sqrt(y)={f(1e-8)*np.sqrt(1e-8):.6f}")

# ---------------------------------------------------------------- Part B: q(eta)
head("PART B -- the anomalous quadrupole, validated against Milgrom's published anchors")
def eta_N_of(nu, eta):
    f = lambda t: t*float(nu(np.array([t]))[0]) - eta
    hi = max(10.0*eta, 10.0)
    while f(hi) < 0: hi *= 2
    return brentq(f, 1e-8, hi, xtol=1e-14, rtol=1e-15)

def c2_raw(nu, etaN, nr=2600, nth=96, rmin=3e-4, rmax=400.0):
    """l=2 coefficient of delta Phi in units GM = a_0 = 1 (so R_M = 1, a_0/R_M = 1)."""
    mu_g, w_g = leggauss(nth)
    r = np.geomspace(rmin, rmax, nr)
    R, MU = np.meshgrid(r, mu_g, indexing="ij")
    ST = np.sqrt(np.clip(1 - MU**2, 0, None))
    gs = 1.0/R**2
    gz, gp = etaN - gs*MU, -gs*ST
    gN = np.sqrt(gz**2 + gp**2)
    A = nu(gN) - 1.0
    Ar = A*(gz*MU + gp*ST); At = A*(-gz*ST + gp*MU)
    dAr = np.gradient(R**2*Ar, r, axis=0)/R**2
    dAt = np.gradient(At*ST, np.arccos(mu_g), axis=1)/(R*np.maximum(ST, 1e-12))
    S2 = 2.5*np.sum((dAr+dAt)*(0.5*(3*MU**2-1))*w_g[None, :], axis=1)
    ok = np.isfinite(S2)
    return -0.2*np.trapz((S2/r)[ok], r[ok])

def q_milgrom(nu, eta):  return 2.0*abs(c2_raw(nu, eta_N_of(nu, eta)))
def Q2_over_pref(nu, eta): return 3.0*abs(c2_raw(nu, eta_N_of(nu, eta)))   # |Q_2|/(a_0/R_M)

nu_simple = nu_n(1.0)
ANCH = {1.0: 0.094, 1.5: 0.159, 2.0: 0.221}
qs = {e: q_milgrom(nu_simple, e) for e in ANCH}
for e in ANCH:
    info(f"B1  eta={e}", f"published q={ANCH[e]:.4f}   computed q={qs[e]:.4f}   "
                         f"frac diff {qs[e]/ANCH[e]-1:+.3%}")
worst = max(abs(qs[e]/ANCH[e]-1) for e in ANCH)
check(worst < 0.05, f"B2  Milgrom's q(eta) reproduced to {worst:.1%} with NO fitted factor "
      "(convention q_zz = 2 c_2, the 3/2 removed)", "machinery validated")
sl_c = np.polyfit(np.log(list(ANCH)), np.log([qs[e] for e in ANCH]), 1)[0]
sl_p = np.polyfit(np.log(list(ANCH)), np.log(list(ANCH.values())), 1)[0]
check(abs(sl_c-sl_p) < 0.05, f"B3  log-slope {sl_c:.3f} vs published {sl_p:.3f}", "shape reproduced too")

# ---------------------------------------------------------------- Part C: n_SS
head("PART C -- GATE 3: the sharpness the Solar System REQUIRES")
V0, R0 = 233.0e3, 8.20*3.0857e19
g_ext = V0**2/R0
info("C0  Galactic external field at the Sun", f"V0=233 km/s, R0=8.20 kpc -> g_ext={g_ext:.4e} m/s^2")
CEILS = {"Cassini 1sigma |Q2|<3e-27": 3.0e-27,
         "Cassini 2sigma |Q2|<9e-27": 9.0e-27,
         "legacy ceiling 5.2e-27":    5.2e-27}
nSS = {}
for fname, a0 in A0.items():
    eta = g_ext/a0
    pref = np.sqrt(a0**3/GM_SUN)              # = a_0/R_M
    info(f"C1  {fname}", f"a0={a0:.4e}  eta={eta:.3f}  a0/R_M={pref:.4e} s^-2")
    for cname, ceil in CEILS.items():
        Qtarget = ceil/pref                   # required |Q2|/(a0/R_M)
        f = lambda n: Q2_over_pref(nu_n(n), eta) - Qtarget
        lo, hi = 0.6, 60.0
        if f(lo) < 0:
            nSS[(fname, cname)] = None
            info(f"C2  {cname:28s}", "even n->0.6 passes: no constraint"); continue
        while f(hi) > 0 and hi < 400: hi *= 1.6
        if f(hi) > 0:
            nSS[(fname, cname)] = np.inf
            info(f"C2  {cname:28s}", "NO n passes up to n=400"); continue
        n_star = brentq(f, lo, hi, xtol=1e-4)
        nSS[(fname, cname)] = n_star
        info(f"C2  {cname:28s}", f"|Q2| <= ceiling requires  n >= {n_star:.3f}")
check(all(v is not None and np.isfinite(v) for v in nSS.values()),
      "C3  a finite n_SS exists for every ceiling/footing combination",
      "the family can always be made sharp enough -- the question is whether galaxies allow it")
n_lo = min(v for v in nSS.values()); n_hi = max(v for v in nSS.values())
info("C4  *** GATE 3 RESULT ***", f"n_SS = {n_lo:.2f} to {n_hi:.2f} across footing x ceiling")

head("PART D -- reference q and |Q2| for a grid of n, both footings")
print(f"  {'n':>6} | " + " | ".join(f"{f[:4]}: q(eta)   |Q2| [s^-2]" for f in A0))
for n_ in (1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0):
    cells = []
    for fname, a0 in A0.items():
        eta = g_ext/a0; pref = np.sqrt(a0**3/GM_SUN)
        cells.append(f"{q_milgrom(nu_n(n_), eta):.4f}    {Q2_over_pref(nu_n(n_), eta)*pref:.3e}")
    print(f"  {n_:6.1f} | " + " | ".join(cells))

head("PART E -- what is established here, and what is NOT")
for s in [
 "ESTABLISHED: mu_n and nu_n are exact conjugates with n-independent asymptotics, so n moves "
 "the transition SHAPE ONLY and cannot touch the deep-MOND normalisation. Gate 1 is satisfied "
 "by construction, not by assumption.",
 f"ESTABLISHED: the q(eta) machinery reproduces Milgrom 2009's published anchors to {worst:.1%} "
 f"and his log-slope to {abs(sl_c-sl_p):.3f}, with no fitted factor. The conventions are "
 "c_2 = q_zz/2 (Milgrom) and c_2 = -Q_2/3 (DHF), hence |Q_2| = (3/2) q (a_0/R_M).",
 f"ESTABLISHED: the Solar System requires n >= {n_lo:.2f}-{n_hi:.2f}.",
 "NOT ESTABLISHED HERE: what n the galaxies prefer. That is Gate 2 and it is measured, not "
 "assumed. Until Gate 2 returns, NO claim is made about whether a window exists.",
 "ASSUMED: QUMOND form for the Solar-System field equation, a point-mass Sun, a uniform "
 "external field, and the quasi-static limit. All four are DHF's assumptions too, deliberately: "
 "Gate 3 must use the SAME instrument as the published constraint or the comparison is void.",
 "FAILURE TEST: if the true theory's Solar-System limit is not QUMOND, n_SS is not the right "
 "target at all and Gate 3 must be recomputed from the new field equation. That is Part VII "
 "and it is downstream of Gates 2-3, not upstream.",
]:
    info("S", s)
np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate3_nSS.npy"), np.array([n_lo, n_hi]))
import json; json.dump({f"{a}|{b}": v for (a,b),v in nSS.items()}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"gate3_nSS.json"),"w"), indent=1)
print("\n" + "="*100 + f"\nGATE 3 CHECKS: {NCHK[0]-len(FAIL)}/{NCHK[0]} passed\n" + "="*100)
sys.exit(1 if FAIL else 0)
