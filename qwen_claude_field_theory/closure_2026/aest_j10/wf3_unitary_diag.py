#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnose the unitary-gauge static (wb^0) sector: which fields are active,
system ranks, and the correct field split. Uses cached L2dc_unitary.pkl."""
import sympy as sp, pickle, os, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)
SC = None
root = '/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula'
for s in os.listdir(root):
    cand = os.path.join(root, s, 'scratchpad', 'L2dc_unitary.pkl')
    if os.path.exists(cand):
        SC = os.path.join(root, s, 'scratchpad') + '/'
L2dc = pickle.load(open(SC+'L2dc_unitary.pkl', 'rb'))
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
wb = sp.symbols('w_b', positive=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
GT, LAM, kx = sp.symbols('G_t Lambda k_x', real=True)
def S(t): return sp.Symbol(t)
names = ['Psi', 'Phi', 'B1', 'B2', 'B3', 's22', 's23', 'a1', 'a2', 'a3']
KETS = [S(n+'k') for n in names]; BRAS = [S(n+'b') for n in names]
Rk = S('rhok')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
sub = {GT: 1, LAM: 0, kx: 1, KB: sp.Rational(1, 5), K2: 10, JY: 1,
       Q0: sp.Rational(2, 5)}
eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
# full 10-field static system
eq0 = [sp.expand(eqf[b].coeff(wb, 0)) for b in BRAS]
A0, b0 = sp.linear_eq_to_matrix(eq0, KETS)
P("static 10x10: rank(A) =", A0.rank(), " rank([A|b]) =", A0.row_join(b0).rank())
sol = list(sp.linsolve((A0, b0), KETS))
if sol:
    s0 = dict(zip(KETS, sol[0]))
    for k in KETS:
        v = sp.simplify(s0[k])
        P(f"  {k} = {v}")
else:
    P("  static system INCONSISTENT")
P(f"done ({time.time()-T0:.1f}s)")
