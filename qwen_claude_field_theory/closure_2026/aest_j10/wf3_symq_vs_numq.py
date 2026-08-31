#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adversarial self-check: does the symbolic-q wb^2 solve, specialized to
q=2/5, agree with the direct numeric-q solve? Verifies residuals of BOTH
candidate solutions in BOTH equation sets."""
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
q = sp.Symbol('q', positive=True)
def S(t): return sp.Symbol(t)
names = ['Psi', 'Phi', 'B2', 'B3', 's22', 's23', 'a1', 'a2', 'a3', 'chi']
KETS = [S(n+'k') for n in names]; BRAS = [S(n+'b') for n in names]
Rk = S('rhok')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None
def ladder(Q0val):
    sub = {GT: 1, LAM: 0, kx: 1, KB: sp.Rational(1, 5), K2: 10, JY: 1, Q0: Q0val}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    stat = ['Psi', 'Phi', 's22', 'a1', 'chi']
    eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
    s0s = lin(eq0, [S(n+'k') for n in stat])
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0), a2k: sp.S(0), a3k: sp.S(0)}
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    E1 = [sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS]
    s1 = lin(E1, list(dk1.values()))
    E2 = [sp.expand(eqW[A].coeff(wb, 2)).subs(s1) for A in BRAS]
    s2 = lin(E2, list(dk2.values()))
    return E2, s1, s2, dk2
E2n, s1n, s2n, dk2 = ladder(sp.Rational(2, 5))
E2s, s1s, s2s, _ = ladder(q)
dPsi_num = s2n[sp.Symbol('d2_Psik')]
dPsi_sym = s2s[sp.Symbol('d2_Psik')]
dPsi_sym_at = sp.cancel(dPsi_sym.subs(q, sp.Rational(2, 5)))
P("d2_Psik  numeric-q      :", sp.simplify(dPsi_num))
P("d2_Psik  symbolic-q @2/5:", sp.simplify(dPsi_sym_at))
P("difference:", sp.simplify(dPsi_num - dPsi_sym_at))
# residuals: plug symbolic-q solution (specialized) into numeric E2
res_ok = all(sp.simplify(e.subs({k: sp.cancel(v.subs(q, sp.Rational(2, 5)))
             for k, v in s2s.items()})) == 0 for e in E2n)
P("symbolic-q solution satisfies numeric E2:", res_ok)
res_ok2 = all(sp.simplify(e.subs(s2n)) == 0 for e in E2n)
P("numeric-q solution satisfies numeric E2:", res_ok2)
# and does s1 agree?
d1B2_num = s1n[sp.Symbol('d1_B2k')]
d1B2_sym = sp.cancel(s1s[sp.Symbol('d1_B2k')].subs(q, sp.Rational(2, 5)))
P("d1_B2k diff:", sp.simplify(d1B2_num - d1B2_sym))
P(f"done ({time.time()-T0:.1f}s)")
