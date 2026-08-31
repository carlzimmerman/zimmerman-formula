#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_heldout_and_JYinf.py
========================
(1) HELD-OUT certification of the J_Y=1 closed form
    alpha_2(J_Y=1) = [K2(KB^2-4KB-4) - KB^4+8KB^3-4KB^2-32KB+32]/(KB-2)^3
  at K_B in {1/3, 3/5, 3/20} x K2 in {7, 33}  (none used in the fit), plus
  alpha_1 = -(4+2K_B) there.
(2) J_Y -> infinity trend of alpha_2 (K_B=1/5, K2=10) at J_Y = 10, 20, 50:
  does it approach Route 3's SUGGESTIVE regulated-pole C0 = -K_B/2 = -0.1?
Same certified pipeline as wf3_eta_K_final.py.
"""
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
Rk = S('rhok'); Psik = S('Psik')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None
def ladder(kbv, k2v, jyv):
    sub = {GT: 1, LAM: 0, kx: 1, KB: sp.nsimplify(kbv),
           K2: sp.nsimplify(k2v), JY: sp.nsimplify(jyv), Q0: q}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    stat = ['Psi', 'Phi', 's22', 'a1', 'chi']
    eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
    s0s = lin(eq0, [S(n+'k') for n in stat])
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0),
          a2k: sp.S(0), a3k: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk)
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    c2t = sp.cancel(sp.expand(dk1[S('B2k')].subs(s1)).coeff(w2)/Rk)
    a1v = sp.limit(sp.cancel(2*c2t/U_amp), q, 0)
    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS],
             list(dk2.values()))
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
    Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    a2v = sp.cancel((Cpar - Cperp)/2)
    cm2 = sp.limit(a2v*q**2, q, 0)
    c0 = sp.limit(sp.cancel(a2v - cm2/q**2), q, 0)
    return a1v, sp.nsimplify(c0)

a2form = ((K2*(KB**2 - 4*KB - 4) - KB**4 + 8*KB**3 - 4*KB**2 - 32*KB + 32)
          / (KB - 2)**3)
P("="*74)
P("1. HELD-OUT points (not in any fit):  J_Y = 1")
P("="*74)
for kbv, k2v in [(sp.Rational(1, 3), 7), (sp.Rational(3, 5), 33),
                 (sp.Rational(3, 20), 7)]:
    a1v, c0 = ladder(kbv, k2v, 1)
    pred1 = -(4 + 2*sp.nsimplify(kbv))
    pred2 = sp.nsimplify(a2form.subs({KB: kbv, K2: k2v}))
    P(f"  K_B={kbv} K2={k2v}: alpha_1={a1v} pred={pred1} ok={sp.simplify(a1v-pred1)==0} ;"
      f" alpha_2={c0} pred={pred2} ok={sp.simplify(c0-pred2)==0}")
P(f"({time.time()-T0:.1f}s)")
P("")
P("="*74)
P("2. J_Y -> oo trend (K_B=1/5, K2=10): Route-3 suggestive C0 = -K_B/2 = -0.1?")
P("="*74)
for jyv in [10, 20, 50]:
    a1v, c0 = ladder(sp.Rational(1, 5), 10, jyv)
    P(f"  J_Y={jyv}: alpha_1={a1v}={float(a1v):+.5f} (->-4K_B=-0.8)  "
      f"alpha_2={c0}={float(c0):+.6f}")
P(f"done ({time.time()-T0:.1f}s)")
