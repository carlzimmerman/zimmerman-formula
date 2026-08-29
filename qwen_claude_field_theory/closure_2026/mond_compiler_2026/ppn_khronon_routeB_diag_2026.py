#!/usr/bin/env python3
r"""
ppn_khronon_routeB_diag_2026.py -- diagnostics for ROUTE B.

(i)  determinant of the 5x5 quasi-static response matrix as a function of (alpha,beta,lam):
     does the CANDIDATE point beta = lam = 0 sit on a DEGENERATE (non-invertible) locus?
(ii) correct O(w) extraction of the gauge-invariant combination alpha_1 - alpha_2 from g_0x
(iii) sign-convention match of our (alpha,beta,lam) against the published khronometric
     alpha_1 = 4(alpha-2beta)/(beta-1),
     alpha_2 = alpha_1/2 + (alpha-2beta)(alpha+beta+3lam)/((beta+lam)(2-alpha))
     [Blas-Sibiryakov; = Foster-Jacobson Einstein-aether alpha_2 in the
      hypersurface-orthogonal dictionary alpha=c14, beta=c13, lam=c2, c1->infty]
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

FRAME = {k1: 0, k2: 0, k3: kk, w1: wx, w2: 0, w3: wz, Th: 0}
EQS = {key: sp.expand(e.subs(FRAME)) for key, e in FEQ.items()}
UNK = [Ph, Ps, Z1h, Z2h, Z3h]
SYS = [EQS['Phi'], EQS['Psi'], EQS['Z0'], EQS['Z1'], EQS['Z2']]

M, RHS = sp.linear_eq_to_matrix(SYS, UNK)

print("### (i) determinant of the response matrix ###")
det = sp.factor(sp.simplify(M.det()))
print("det(M) =", det)
print()
print("det at w = 0 :", sp.factor(sp.simplify(det.subs({wx: 0, wz: 0}))))
print("det at beta=lam=0 :", sp.factor(sp.simplify(det.subs({be: 0, lm: 0}))))
print("det at beta=lam=0, alpha=0 (GR) :",
      sp.factor(sp.simplify(det.subs({be: 0, lm: 0, al: 0}))))
print()
print("### rank at the candidate point beta=lam=0 (symbolic alpha) ###")
M0 = M.subs({be: 0, lm: 0}).applyfunc(sp.simplify)
print("rank(M0) =", M0.rank())
print("rank of augmented [M0|RHS] =",
      M0.row_join(RHS.subs({be: 0, lm: 0})).applyfunc(sp.simplify).rank())
ns = M0.nullspace()
print("nullspace dim =", len(ns))
for v in ns:
    print("   null vector:", sp.simplify(v.T))
