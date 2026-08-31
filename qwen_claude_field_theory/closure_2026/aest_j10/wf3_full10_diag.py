#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnose the O(wb) inconsistency of the full ungauged 10-field system:
ranks, the left-null obstruction vector (which combination of equations is
violated and by how much), and its q- and parameter-dependence. Also check
whether the obstruction vanishes if the wb^0 free gauge modes are chosen
suitably (i.e. whether it is a gauge-orbit artifact rather than absolute)."""
import sympy as sp, pickle, os, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)
SC = None
root = '/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula'
for s in os.listdir(root):
    cand = os.path.join(root, s, 'scratchpad', 'L2dc_full10.pkl')
    if os.path.exists(cand):
        SC = os.path.join(root, s, 'scratchpad') + '/'
L2dc = pickle.load(open(SC+'L2dc_full10.pkl', 'rb'))
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
wb = sp.symbols('w_b', positive=True)
w1, w2 = sp.symbols('w1 w2', real=True)
GT, LAM, kx = sp.symbols('G_t Lambda k_x', real=True)
q = sp.Symbol('q', positive=True)
def S(t): return sp.Symbol(t)
names = ['Psi', 'B1', 'B2', 'H11', 'H22', 'H33', 'H12', 'chi', 'a1', 'a2']
KETS = [S(n+'k') for n in names]; BRAS = [S(n+'b') for n in names]
Rk = S('rhok')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
sub = {KB: sp.Rational(1, 5), K2: 10, JY: 1, Q0: q, GT: 1, LAM: 0, kx: 1}
eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
# wb^0
eq0 = [sp.expand(eqf[b].coeff(wb, 0)) for b in BRAS]
A0, b0 = sp.linear_eq_to_matrix(eq0, KETS)
P("wb^0: rank(A)=", A0.rank(), " rank([A|b])=", A0.row_join(b0).rank(), "/10")
sols = list(sp.linsolve((A0, b0), KETS))
s0full = dict(zip(KETS, sols[0]))
free0 = [u for u in KETS if s0full[u] == u]
P("  free wb^0 modes:", free0)
# keep the free modes SYMBOLIC through the wb^1 stage
dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
subF = {A: s0full[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
E1 = [sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS]
A1m, b1 = sp.linear_eq_to_matrix(E1, list(dk1.values()))
r1 = A1m.rank(); r1b = A1m.row_join(b1).rank()
P("wb^1 (free0 symbolic): rank(A)=", r1, " rank([A|b])=", r1b, "/10")
# left null space of A1m
NT = A1m.T.nullspace()
P("  left-null dim:", len(NT))
for v in NT:
    ob = sp.simplify(sp.expand((v.T*b1)[0, 0]))
    vv = {BRAS[i]: sp.simplify(v[i]) for i in range(10) if sp.simplify(v[i]) != 0}
    P("  obstruction combo (eq weights):", vv)
    P("  v.b =", ob)
    P("   -> vanishes for which free-mode choice?",
      sp.solve(ob, free0, dict=True) if ob != 0 else "identically 0")
P(f"done ({time.time()-T0:.1f}s)")
