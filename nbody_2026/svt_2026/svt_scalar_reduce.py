#!/usr/bin/env python3
"""
Sections E/F: constraint elimination + kinetic matrix + no-ghost + dispersion,
from the checkpointed z-averaged quadratic Lagrangian L2s (svt_scalar_master.py).

Phi's p0^2 coefficient AP is velocity-free => exact completion of the square:
   L2s = AP (p0 - p0sol)^2 + Lred,  Lred = [4 AP L2s|_{p0=0} - (dL/dp0|_{p0=0})^2]/(4 AP).
The FRIEDMANN constraint  Lam = 3H^2 - 8 pi G (Qb K1 - K0)  is imposed on the reduced
action (background on-shell); the reduced kinetic matrix then degenerates EXACTLY
(the momentum constraint lost to complete gauge fixing) -- proven below.
"""
import sympy as sp
import time, sys, functools
print = functools.partial(print, flush=True)
t_start = time.time()
def banner(s): print("\n" + "="*100 + "\n" + s + "\n" + "="*100)
def tick(l): print("    [t=%6.1fs] %s" % (time.time()-t_start, l))
def check(cond, label):
    print(("  [PASS] " if cond else "  [FAIL] ") + label)
    if not cond: print("  *** HARD FAIL ***"); sys.exit(1)

k   = sp.Symbol('k', positive=True)
G   = sp.Symbol('G', positive=True)
Lam = sp.Symbol('Lam', real=True)
KB  = sp.Symbol('K_B', real=True)
Ab  = sp.Symbol('A_b', real=True)
ub  = sp.Symbol('u_b', real=True)
K0, K1, K2 = sp.symbols('K0 K1 K2', real=True)
A0cp = sp.Symbol('A0cp', positive=True)
p0, s0, x0, a0v = sp.symbols('p0 s0 x0 a0v', real=True)
s1, x1, a1v, p1 = sp.symbols('s1 x1 a1v p1', real=True)
Hh  = sp.Symbol('H', real=True)
av  = sp.Symbol('a_v', positive=True)
Qbs = sp.Symbol('Qb', real=True)

FRIEDMANN = [(Lam, 3*Hh**2 - 8*sp.pi*G*(Qbs*K1 - K0))]

def klead(e):
    """exact leading term of a rational function of k as k -> infinity"""
    e = sp.cancel(sp.together(e))
    num, den = sp.fraction(e)
    pn, pd = sp.Poly(num, k), sp.Poly(den, k)
    return sp.factor(pn.coeff_monomial(k**pn.degree())/pd.coeff_monomial(k**pd.degree())
                     * k**(pn.degree()-pd.degree()))

L2s = sp.sympify(open('L2s_checkpoint.txt').read())
print("L2s loaded:", len(sp.Add.make_args(sp.expand(L2s))), "terms")

banner("SECTION E -- eliminate Phi; impose Friedmann; kinetic degeneracy = the momentum constraint")
cP  = sp.expand(sp.diff(L2s, p0))
AP  = sp.expand(sp.diff(cP, p0)/2)
cP0 = sp.expand(cP.subs(p0, 0))
check(not any(AP.has(v) for v in (s1, x1, a1v, p1)), "AP (Phi^2 coefficient) is velocity-free")
p0sol = sp.cancel(-cP0/(2*AP))
Lred_num = sp.expand(4*AP*L2s.subs(p0, 0) - cP0**2)      # Lred = Lred_num/(4 AP)
AP_f = sp.factor(sp.expand(AP.subs(FRIEDMANN)))
print("  AP  (on Friedmann) =", AP_f, "   [> 0 at sub-horizon k for K_B > 0]")
tick("completed the square")

vels = [s1, x1, a1v]; flds = [s0, x0, a0v]
names = ["Psi", "chi", "alpha"]
Tnum_off = sp.Matrix(3,3, lambda i,j: sp.expand(sp.diff(Lred_num, vels[i], vels[j])/2))
detT_off = sp.factor(sp.expand(Tnum_off.det()))
print("\n  OFF-shell det Tnum =", detT_off)
print("  -> contains the factor (8 pi G K0 - 8 pi G K1 Qb + 3H^2 - Lam) == 0 on Friedmann:")
Tnum = Tnum_off.applyfunc(lambda e: sp.factor(sp.expand(e.subs(FRIEDMANN))))
detT = sp.expand(Tnum.det())
check(detT == 0, "ON the Friedmann background det T == 0 EXACTLY: rank drops -- the lost momentum "
                 "constraint reappears as a kinetic degeneracy (this is a DERIVED consistency, not input)")
print("\n  ON-shell kinetic numerator Tnum = 4*AP*T (basis Psi, chi, alpha):")
for i in range(3):
    for j in range(i, 3):
        print("   Tnum[%s,%s] = %s" % (names[i], names[j], Tnum[i,j]))
print("  rank(Tnum) =", Tnum.rank())
ns = Tnum.nullspace()
check(len(ns) == 1, "exactly ONE null direction")
nv = ns[0].applyfunc(lambda e: sp.factor(sp.cancel(e)))
print("  null direction (Psi, chi, alpha) =", list(nv.T))
tick("degeneracy established")

banner("SECTION E2 -- no-ghost: project onto the physical 2-plane; conditions")
# Physical modes: any basis of the quotient by the null direction. The null direction has
# nonzero Psi-component (generic k), so (chi, alpha) coordinates parametrise the quotient:
# write Psi-velocity in terms of the others along the null constraint. Projection matrix:
# columns = two independent vectors NOT in the null space; use e_chi, e_alpha completed
# against the null vector via a Psi-elimination: v_Psi = -(n_chi v_chi + n_al v_al)/n_Psi.
nPsi, nChi, nAl = nv[0], nv[1], nv[2]
# Basis vectors of the physical plane (Gram of T restricted to the plane transverse to null):
# choose w1 = (0,1,0), w2 = (0,0,1) -- valid iff null vector has nonzero Psi component:
check(sp.simplify(nPsi) != 0, "null vector has nonzero Psi-component (generic k): (chi, alpha) span the quotient")
W = sp.Matrix([[0, 0], [1, 0], [0, 1]])
T2num = (W.T*Tnum*W).applyfunc(lambda e: sp.factor(sp.expand(e)))
print("  2x2 physical kinetic numerator T2num (= 4*AP*T2), basis (chi, alpha):")
print("   T2num[chi,chi]     =", T2num[0,0])
print("   T2num[chi,alpha]   =", T2num[0,1])
print("   T2num[alpha,alpha] =", T2num[1,1])
det2 = sp.factor(sp.expand(T2num.det()))
print("   det T2num =", det2)
print("\n  leading terms as k -> infinity (sub-horizon: the ghost diagnostic):")
print("   AP   -> ", klead(AP_f))
print("   T2num[chi,chi]   -> ", klead(T2num[0,0]))
print("   T2num[alpha,alpha]-> ", klead(T2num[1,1]))
print("   det T2num        -> ", klead(det2))
lead_chichi = klead(T2num[0,0]); lead_det = klead(det2); lead_AP = klead(AP_f)
print("\n  => with 4AP > 0 (K_B > 0 at high k), Sylvester: T2[chi,chi] > 0 and det > 0:")
print("     T2[chi,chi] = K2 K_B a^4 k^2/(4AP*32 pi G)-type > 0  <=>  K2 > 0 (given K_B > 0)")
print("     det/(4AP)^2 > 0 fixes the K_B window jointly -- evaluated numerically below.")

import numpy as np
pars_base = dict(G=1.0, av=1.0, H=0.05, Qb=1.0, K0=-0.10, K1=0.02, K2=0.40, Ab=0.01, ub=1e-3, A0cp=1.0)
argsyms = (G, av, Hh, Qbs, K0, K1, K2, Ab, ub, A0cp, KB, k)
Tfull = (Tnum/(4*AP.subs(FRIEDMANN)))
Tfun = sp.lambdify(argsyms, Tfull, 'numpy')
def eig_T(p, KBv, kv):
    M = np.array(Tfun(p['G'], p['av'], p['H'], p['Qb'], p['K0'], p['K1'], p['K2'],
                      p['Ab'], p['ub'], p['A0cp'], KBv, kv), dtype=float)
    M = 0.5*(M+M.T)
    return np.sort(np.linalg.eigvalsh(M))
print("\n  numeric eigenvalues of full reduced T (one must be ~0 = the degeneracy), k = 1e3:")
for KBv in [-0.5, 0.1, 0.5, 1.0, 1.9, 2.0, 2.5, 3.0]:
    print("   K_B = %-5s K2 = +0.4 :" % KBv, np.array2string(eig_T(pars_base, KBv, 1e3), precision=6))
p_bad = dict(pars_base); p_bad['K2'] = -0.4
print("   K_B = 0.5   K2 = -0.4 :", np.array2string(eig_T(p_bad, 0.5, 1e3), precision=6))
tick("eigen scan done")

banner("SECTION F -- dispersion: the khronon gradient structure (k^2 sources; the k^4 question)")
# EL from Lred_num (overall 1/(4AP) is field-independent: root structure unchanged), ON Friedmann
Lred_num_f = sp.expand(Lred_num.subs(FRIEDMANN))
w = sp.Symbol('omega')
acc = sp.symbols('s2 x2 a2v', real=True)
def ddt_frozen(e):
    out = 0
    for f, v in zip(flds, vels): out += sp.diff(e, f)*v
    for v, aa in zip(vels, acc): out += sp.diff(e, v)*aa
    return out
EL = [sp.expand(ddt_frozen(sp.diff(Lred_num_f, vels[i])) - sp.diff(Lred_num_f, flds[i])) for i in range(3)]
hat = sp.symbols('hS hX hA', real=True)
subw = (list(zip(acc, [-w**2*h for h in hat]))
        + list(zip(vels, [sp.I*w*h for h in hat]))
        + list(zip(flds, hat)))
Msys = sp.Matrix(3,3, lambda i,j: sp.diff(sp.expand(EL[i].subs(subw, simultaneous=True)), hat[j]))
tick("WKB system built")
D = sp.expand(Msys.det())
Dpoly = sp.Poly(D, w)
deg = Dpoly.degree()
print("  det M(omega): degree", deg, "in omega   [degree 4, not 6, = the kinetic degeneracy again]")
coeffs = {n: sp.expand(Dpoly.coeff_monomial(w**n)) for n in range(deg+1)}
odd_zero = all(coeffs.get(n, 0) == 0 for n in range(1, deg+1, 2))
print("  odd-omega coefficients vanish:", odd_zero)
d0 = coeffs.get(0, 0); d2 = coeffs.get(2, 0); d4 = coeffs.get(4, 0)
tick("det computed")
print("\n  d0 (omega^0) =", sp.factor(d0))
print("\n  switch-off tests of d0 (what sources the khronon gradient/mass):")
print("   d0[K1=0, Ab=0] =", sp.factor(sp.expand(d0.subs([(K1, 0), (Ab, 0)]))))
print("   d0[Ab=0]       =", sp.factor(sp.expand(d0.subs(Ab, 0))))
print("   d0[K1=0]       =", sp.factor(sp.expand(d0.subs(K1, 0))))
soft = sp.cancel(-sp.factor(d0)/sp.factor(d2))
print("\n  soft-branch omega^2 = -d0/d2 =", soft)
print("  omega_soft^2 leading as k -> inf:", klead(soft))
try:
    ser_0 = sp.series(soft, k, 0, 5).removeO()
    print("  omega_soft^2 (k -> 0):", sp.factor(sp.expand(ser_0)))
except Exception as ex:
    print("  (k->0 series failed:", ex, ")")
# the hard branch for completeness
hard = sp.cancel(-sp.factor(d2)/sp.factor(d4))
print("\n  hard-branch omega^2 ~ -d2/d4 (leading, k -> inf):", klead(hard))
tick("dispersion done")
print("\nDONE  (%.1f s)" % (time.time()-t_start))
