#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnose rank/uniqueness of the wb^0, wb^1, wb^2 linear systems of the
base-AeST boosted solve (L2dc_v2.pkl) at a numeric point, and whether the
alpha_2 extraction (d2_Psik) is unique. Also same diagnosis for nullspace
direction -> is the ambiguity a residual gauge mode, and does it touch Psi?"""
import sympy as sp, pickle, time, os
T0 = time.time(); P = lambda *a: print(*a, flush=True)
SC = None
root = '/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula'
for s in os.listdir(root):
    cand = os.path.join(root, s, 'scratchpad', 'L2dc_v2.pkl')
    if os.path.exists(cand):
        SC = os.path.join(root, s, 'scratchpad') + '/'
L2dc = pickle.load(open(SC+'L2dc_v2.pkl', 'rb'))
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
wb = sp.symbols('w_b', positive=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
GT, LAM, kx = sp.symbols('G_t Lambda k_x', real=True)
def S(t): return sp.Symbol(t)
names = ['Psi', 'Phi', 'B2', 'B3', 's22', 's23', 'a1', 'a2', 'a3', 'chi']
KETS = [S(n+'k') for n in names]; BRAS = [S(n+'b') for n in names]
Rk = S('rhok')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
sub = {GT: 1, LAM: 0, kx: 1, KB: sp.Rational(1, 5), K2: 10, JY: 1,
       Q0: sp.Rational(2, 5)}
eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
stat = ['Psi', 'Phi', 's22', 'a1', 'chi']
eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
unk0 = [S(n+'k') for n in stat]
A0, b0 = sp.linear_eq_to_matrix(eq0, unk0)
P("wb^0 5x5: rank(A) =", A0.rank(), "/", len(unk0))
s0s = dict(zip(unk0, list(sp.linsolve((A0, b0), unk0))[0]))
s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0), a2k: sp.S(0), a3k: sp.S(0)}
dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
E1 = [sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS]
A1m, b1 = sp.linear_eq_to_matrix(E1, list(dk1.values()))
P("wb^1 10x10: rank(A) =", A1m.rank(), "/ 10 ; rank([A|b]) =",
  A1m.row_join(b1).rank())
ns1 = A1m.nullspace()
P("  nullspace dim =", len(ns1))
for v in ns1:
    P("  null dir:", {k: sp.simplify(c) for k, c in zip(KETS, v) if c != 0})
s1 = dict(zip(list(dk1.values()), list(sp.linsolve((A1m, b1), list(dk1.values())))[0]))
fs1 = set().union(*[v.free_symbols for v in s1.values()])
P("  free syms in s1 solution:", [f for f in fs1 if str(f).startswith('d1_')])
E2 = [sp.expand(eqW[A].coeff(wb, 2)).subs(s1) for A in BRAS]
A2m, b2 = sp.linear_eq_to_matrix(E2, list(dk2.values()))
P("wb^2 10x10: rank(A) =", A2m.rank(), "/ 10 ; rank([A|b]) =",
  A2m.row_join(b2).rank())
ns2 = A2m.nullspace()
P("  nullspace dim =", len(ns2))
for v in ns2:
    P("  null dir:", {k: sp.simplify(c) for k, c in zip(KETS, v) if c != 0})
s2 = dict(zip(list(dk2.values()), list(sp.linsolve((A2m, b2), list(dk2.values())))[0]))
fs2 = set().union(*[v.free_symbols for v in s2.values()])
P("  free syms in s2 solution:", sorted([str(f) for f in fs2 if str(f).startswith('d2_')]))
P("  d2_Psik solution:", sp.simplify(s2[dk2[S('Psik')]]))
P(f"done ({time.time()-T0:.1f}s)")
