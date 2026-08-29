#!/usr/bin/env python3
r"""
ppn_khronon_routeB_candidate_2026.py -- THE DECISIVE RUN for ROUTE B.

Candidate locus: beta = lam = 0 (the candidate's gravity sector is EXACTLY
K_ij K^ij - K^2 + R3, i.e. GR, so the only Lorentz-violating operator is the
lapse-tied MOND term  chi (D phi)^2 = chi a_mu a^mu  ==>  khronometric alpha only).

CORRECTED PPN READOUT (calibrated on the published khronometric formulas -- see
ppn_khronon_routeB_num_2026.py, which reproduces BOTH of
   alpha_1^lit = 4(a-2b)/(b-1),
   alpha_2^lit = alpha_1^lit/2 + (a-2b)(a+b+3l)/((b+l)(2-a))
exactly, under the dictionary (a,b,l)_lit = (alpha, -beta, -lam) for OUR action
   S = (1/16 pi G) Int sqrt(-g)[R + alpha a.a + beta nab_m u_n nab^n u^m + lam (nab.u)^2] ):

   alpha_1 = -2 * d(Z_x/U)/d w_x  at w=0        (k along z, so Z_x carries NO gradient
                                                 piece and is gauge invariant)
   alpha_2 = coefficient of (k.w)^2/k^2 in Phi/U
   [the pure w^2 U coefficient in g_00 is degenerate with the w-dependence of the
    normalisation of G_N and is NOT used]

The published alpha_2 has a 1/(beta+lam) POLE, so it is SINGULAR on the candidate locus.
This script computes the candidate locus DIRECTLY, without taking that limit.
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

FRAME = {k1: 0, k2: 0, k3: kk, w1: wx, w2: 0, w3: wz,
         be: 0, lm: 0, kk: 1, G: 1, Rh: 1}
EQS = {key: sp.expand(sp.cancel(sp.together(e.subs(FRAME)))) for key, e in FEQ.items()}
UNK = [Ph, Ps, Z1h, Z2h, Z3h, Th]
SYS = [EQS['Phi'], EQS['Psi'], EQS['Z0'], EQS['Z1'], EQS['Z2'], EQS['tau']]
M6, R6 = sp.linear_eq_to_matrix(SYS, UNK)
M6 = M6.applyfunc(sp.cancel)
R6 = R6.applyfunc(sp.cancel)

print("=== candidate locus beta = lam = 0, alpha symbolic ===")
print("rank(M) =", M6.rank(), "  rank([M|b]) =", M6.row_join(R6).rank(), "  (6 unknowns)")
ns = M6.nullspace()
print("nullity =", len(ns))
for v in ns:
    print("   null direction:", sp.simplify(sp.cancel(v.T)))

sol = list(sp.linsolve((M6, R6), UNK))[0]
PhiS = sp.cancel(sp.together(sol[0]))
PsiS = sp.cancel(sp.together(sol[1]))
ZxS = sp.cancel(sp.together(sol[2]))
ZzS = sp.cancel(sp.together(sol[4]))
TauS = sp.cancel(sp.together(sol[5]))

gauge_syms = set(UNK)
for nm, ex in (('Phi', PhiS), ('Psi', PsiS), ('Z_x', ZxS)):
    bad = [f for f in ex.free_symbols if f in gauge_syms]
    print("   %-5s gauge-parameter dependence: %s" % (nm, bad if bad else "NONE (invariant)"))

print()
print("Phi(k,w) =", sp.simplify(PhiS))
print("Psi(k,w) =", sp.simplify(PsiS))
print("Z_x(k,w) =", sp.simplify(ZxS))

Phi0 = sp.simplify(sp.limit(sp.limit(PhiS, wx, 0), wz, 0))
GN = sp.simplify(Phi0/(4*sp.pi))
print()
print("G_N/G      =", GN, "   [expected 1/(1-alpha/2) =", sp.simplify(1/(1 - al/2)), "]")
print("gamma_PPN  =", sp.simplify(sp.limit(sp.limit(PsiS, wx, 0), wz, 0)/Phi0))

U0 = 4*sp.pi*GN
r = sp.cancel(PhiS/U0)
A = sp.simplify(sp.limit(sp.diff(r, wx, 2).subs(wz, 0), wx, 0)/2)
C = sp.simplify(sp.limit(sp.diff(r, wz, 2).subs(wx, 0), wz, 0)/2)
a2 = sp.simplify(sp.factor(C - A))
Azx = sp.simplify(sp.limit(sp.limit(sp.diff(ZxS/U0, wx), wz, 0), wx, 0))
a1 = sp.simplify(sp.factor(-2*Azx))

print()
print("*** alpha_1 =", a1)
print("*** alpha_2 =", a2)
print()
print("literature formula at beta=lam=0:  alpha_1^lit = 4*alpha/(0-1) =", -4*al)
print("literature formula at beta=lam=0:  alpha_2^lit = -2*alpha + alpha^2/(beta+lam)"
      "  -> POLE (singular limit)")
print()
print("series of alpha_2 in small alpha:", sp.series(a2, al, 0, 4))
print("series of alpha_1 in small alpha:", sp.series(a1, al, 0, 4))
