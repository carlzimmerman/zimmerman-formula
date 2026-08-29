#!/usr/bin/env python3
r"""
ppn_khronon_routeB_limit_2026.py -- CONTINUITY TEST of the candidate locus.

The published khronometric formulas
    alpha_1 = 4(a-2b)/(b-1)                                        (regular at b=l=0)
    alpha_2 = alpha_1/2 + (a-2b)(a+b+3l)/((b+l)(2-a))              (POLE at b+l=0)
are derived assuming a propagating khronon (c_123 = b+l != 0).  The candidate sits at
b = l = 0 EXACTLY (its gravity sector is K_ijK^ij - K^2 + R3, i.e. GR).

This script walks beta = lam = delta -> 0 with alpha fixed and compares with the value
computed AT delta = 0, to show whether the limit is uniform.
Convention: our (alpha,beta,lam) = literature (alpha, -beta, -lam), calibrated in
ppn_khronon_routeB_num_2026.py (alpha_1 and alpha_2 both reproduced exactly at 4 points).
"""
import sympy as sp
import pickle
import os

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, '_routeB_feq.pkl'), 'rb') as fh:
    D = pickle.load(fh)
FEQ = {k: sp.sympify(v) for k, v in D['FEQ'].items()}

k1, k2, k3 = sp.symbols('k1 k2 k3', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
G = sp.symbols('G', positive=True)
al, be, lm = sp.symbols('alpha beta lambda_', real=True)
Ph, Ps, Z1h, Z2h, Z3h, Th, Rh = sp.symbols('Phih Psih Z1h Z2h Z3h tauh rhoh')
kk, wx, wz = sp.symbols('kk wx wz', real=True)

FRAME = {k1: 0, k2: 0, k3: kk, w1: wx, w2: 0, w3: wz}
EQS = {key: sp.expand(e.subs(FRAME)) for key, e in FEQ.items()}
UNK = [Ph, Ps, Z1h, Z2h, Z3h, Th]
SYS = [EQS['Phi'], EQS['Psi'], EQS['Z0'], EQS['Z1'], EQS['Z2'], EQS['tau']]
M6, R6 = sp.linear_eq_to_matrix(SYS, UNK)

ALPHA = sp.Rational(1, 5)


def readout(a, b, l):
    sub = {al: a, be: b, lm: l, kk: 1, G: 1, Rh: 1}
    Mn = M6.subs(sub).applyfunc(sp.cancel)
    Rn = R6.subs(sub).applyfunc(sp.cancel)
    sol = list(sp.linsolve((Mn, Rn), UNK))[0]
    PhiS = sp.cancel(sp.together(sol[0]))
    ZxS = sp.cancel(sp.together(sol[2]))
    Phi0 = sp.limit(sp.limit(PhiS, wx, 0), wz, 0)
    GN = sp.simplify(Phi0/(4*sp.pi))
    U0 = 4*sp.pi*GN
    r = sp.cancel(PhiS/U0)
    A = sp.limit(sp.diff(r, wx, 2).subs(wz, 0), wx, 0)/2
    C = sp.limit(sp.diff(r, wz, 2).subs(wx, 0), wz, 0)/2
    a2 = sp.nsimplify(sp.simplify(C - A))
    a1 = sp.nsimplify(sp.simplify(-2*sp.limit(sp.limit(sp.diff(ZxS/U0, wx), wz, 0), wx, 0)))
    return sp.simplify(GN), a1, a2


A_, B_, L_ = sp.symbols('A_ B_ L_')
a1_pub = 4*(A_ - 2*B_)/(B_ - 1)
a2_pub = a1_pub/2 + (A_ - 2*B_)*(A_ + B_ + 3*L_)/((B_ + L_)*(2 - A_))

print("alpha = %s fixed;  our beta = lam = delta  ->  literature b = l = -delta" % ALPHA)
print("%-10s %-14s %-22s %-22s %-14s %-14s"
      % ("delta", "G_N/G", "alpha_1(computed)", "alpha_2(computed)",
         "alpha_1(pub)", "alpha_2(pub)"))
for dl in [sp.Rational(1, 2), sp.Rational(1, 10), sp.Rational(1, 100),
           sp.Rational(1, 1000), 0]:
    try:
        GN, a1, a2 = readout(ALPHA, dl, dl)
    except Exception as e:                                  # noqa
        print("%-10s  FAILED: %s" % (dl, e))
        continue
    if dl != 0:
        m = {A_: ALPHA, B_: -dl, L_: -dl}
        p1 = sp.nsimplify(a1_pub.subs(m))
        p2 = sp.nsimplify(a2_pub.subs(m))
    else:
        p1 = -4*ALPHA          # regular limit of the published alpha_1
        p2 = sp.oo             # published alpha_2 has a 1/(b+l) pole
    print("%-10s %-14s %-22s %-22s %-14s %-14s"
          % (dl, GN, a1, a2, p1, p2))

print()
print("expected from the published (limit) formulas at delta -> 0 :"
      "  alpha_1 -> %s ,  alpha_2 -> divergent" % (-4*ALPHA))
print("computed AT delta = 0 (the candidate's own locus)            :"
      "  see last row")
