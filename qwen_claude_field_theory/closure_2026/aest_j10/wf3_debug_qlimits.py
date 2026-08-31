#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug: exact q-dependence of alpha_1, alpha_2, alpha_3, Cperp at
(K_B,K2,J_Y)=(1/5,10,1). Checks the symbolic-q solve against the numeric-q
pass and pins down the q->0 Laurent structure of each quantity."""
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
Psik, Phik = S('Psik'), S('Phik')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None
sub = {GT: 1, LAM: 0, kx: 1, KB: sp.Rational(1, 5), K2: 10, JY: 1, Q0: q}
eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
stat = ['Psi', 'Phi', 's22', 'a1', 'chi']
eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
s0s = lin(eq0, [S(n+'k') for n in stat])
s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0), a2k: sp.S(0), a3k: sp.S(0)}
U_amp = sp.cancel(-s0[Psik]/Rk)
dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
c2t = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)
alpha1 = sp.cancel(2*c2t/U_amp)
eq2 = [sp.expand(eqW[A].coeff(wb, 2)).subs(s1) for A in BRAS]
s2 = lin(eq2, list(dk2.values()))
h2 = sp.cancel(-2*sp.expand(dk2[Psik].subs(s2)))
Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
alpha2 = sp.cancel((Cpar - Cperp)/2)
alpha3 = sp.cancel(Cperp + alpha1)
P(f"built ({time.time()-T0:.1f}s)")
P("alpha1(q) =", alpha1)
P("Cperp(q)  =", Cperp)
P("Cpar(q)   =", Cpar)
P("alpha2(q) =", alpha2)
P("alpha3(q) =", sp.simplify(alpha3))
for qv in [sp.Rational(2, 5), sp.Rational(1, 25), sp.Rational(1, 100), sp.Rational(1, 1000)]:
    P(f"\n q={qv}: alpha1={float(alpha1.subs(q,qv)):.6f}  alpha2={float(alpha2.subs(q,qv)):.6f}"
      f"  alpha3={float(alpha3.subs(q,qv)):.6g}  Cperp={float(Cperp.subs(q,qv)):.6f}")
P("\nq->0 limits: alpha1:", sp.limit(alpha1, q, 0), " Cperp:", sp.limit(Cperp, q, 0),
  " Cpar:", sp.limit(Cpar, q, 0), " alpha2:", sp.limit(alpha2, q, 0),
  " alpha3:", sp.limit(alpha3, q, 0))
P("\nalpha2 Laurent: ", sp.series(alpha2, q, 0, 3))
P(f"done ({time.time()-T0:.1f}s)")
