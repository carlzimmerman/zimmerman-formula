#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_unitary_gauge_solve.py  (ANCHOR iv, corrected static split: B1 is ACTIVE)
=============================================================================
Solve of the UNITARY-gauge (chi=0, h01=B1 retained) base-AeST boosted system
from the cache L2dc_unitary.pkl (built by wf3_unitary_gauge_build.py).
wf3_unitary_diag.py showed the static (wb^0) sector is full-rank with
{Psi,Phi,B1,s22,a1} active (B1 static is an i*k U-phase piece, a unitary-gauge
artifact carrying what chi carried in the route2_v2 gauge); odd sector
{B2,B3,s23,a2,a3} vanishes at wb^0. Gauge-invariant statics already agree with
route2_v2 (U_amp=2000pi/769 at the test point, gamma=1).
Extractions (certified dictionary, w_Will=-wb*w):
  alpha_1: transverse g02 at O(wb) (gauge-invariant channel)
  alpha_2 [g00]: (Cpar-Cperp)/2 at O(wb^2)
  alpha_2 [g0i]: parallel h01 at O(wb): coeff(w1)/Rk/U_amp = -(-alpha_1/2+2alpha_2)
Anchor-iv = agreement of both alpha_2 structures across BOTH gauges with the
closed forms from the route2_v2-gauge solve.
"""
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
q = sp.Symbol('q', positive=True)
def S(t): return sp.Symbol(t)
names = ['Psi', 'Phi', 'B1', 'B2', 'B3', 's22', 's23', 'a1', 'a2', 'a3']
KETS = [S(n+'k') for n in names]; BRAS = [S(n+'b') for n in names]
Rk = S('rhok'); Psik = S('Psik')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None
def solve(kbv, k2v, jyv):
    sub = {KB: sp.nsimplify(kbv), K2: sp.nsimplify(k2v), JY: sp.nsimplify(jyv),
           Q0: q, GT: 1, LAM: 0, kx: 1}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {S('B2k'): 0, S('B3k'): 0, S('s23k'): 0, S('a2k'): 0, S('a3k'): 0}
    stat = ['Psi', 'Phi', 'B1', 's22', 'a1']
    eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
    s0s = lin(eq0, [S(n+'k') for n in stat])
    if s0s is None: return 'SING0'
    s0 = {**s0s, **VZ}
    U_amp = sp.cancel(-s0[Psik]/Rk)
    gamma = sp.cancel(s0[S('Phik')]/s0[Psik])
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None: return ('SING1', U_amp, gamma)
    c2t = sp.cancel(sp.expand(dk1[S('B2k')].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(2*c2t/U_amp)
    C01 = sp.cancel(sp.expand(dk1[S('B1k')].subs(s1)).coeff(w1)/Rk/U_amp)
    alpha2_g0i = sp.cancel((alpha1/2 - C01)/2)
    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS],
             list(dk2.values()))
    if s2 is None: return (alpha1, alpha2_g0i, 'SING2', U_amp, gamma)
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
    Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    alpha2_g00 = sp.cancel((Cpar - Cperp)/2)
    alpha3 = sp.cancel(Cperp + alpha1)
    return dict(U=U_amp, g=gamma, a1=alpha1, a2_g0i=alpha2_g0i,
                a2_g00=alpha2_g00, a3=alpha3)

a2form = ((K2*(KB**2 - 4*KB - 4) - KB**4 + 8*KB**3 - 4*KB**2 - 32*KB + 32)
          / (KB - 2)**3)
for kbv, k2v, jyv in [(sp.Rational(1, 5), 10, 1), (sp.Rational(3, 10), 7, 1),
                      (sp.Rational(1, 5), 10, 2)]:
    r = solve(kbv, k2v, jyv)
    if not isinstance(r, dict):
        P(f"KB={kbv} K2={k2v} JY={jyv}: {r if isinstance(r,str) else r[0]}")
        continue
    a1_0 = sp.limit(r['a1'], q, 0)
    pred_a1 = sp.nsimplify(-4*(2 + sp.nsimplify(kbv)*jyv)/(1 + jyv))
    cm2_i = sp.limit(r['a2_g0i']*q**2, q, 0)
    c0_i = sp.limit(sp.cancel(r['a2_g0i'] - cm2_i/q**2), q, 0)
    cm2_0 = sp.limit(r['a2_g00']*q**2, q, 0)
    c0_0 = sp.limit(sp.cancel(r['a2_g00'] - cm2_0/q**2), q, 0)
    same_fn = sp.simplify(sp.together(r['a2_g0i'] - r['a2_g00'])) == 0
    P(f"KB={kbv} K2={k2v} JY={jyv}:")
    P(f"  U_amp(q->0)={sp.nsimplify(sp.limit(r['U'],q,0))} gamma={sp.simplify(r['g'])} alpha_3=={sp.simplify(r['a3'])}")
    P(f"  alpha_1(q->0)={a1_0}  pred={pred_a1}  ok={sp.simplify(a1_0-pred_a1)==0}")
    P(f"  alpha_2[g00] c_-2={sp.nsimplify(cm2_0)} c_0={sp.nsimplify(c0_0)}")
    P(f"  alpha_2[g0i] c_-2={sp.nsimplify(cm2_i)} c_0={sp.nsimplify(c0_i)}")
    P(f"  identical alpha_2(q) functions g00 vs g0i: {same_fn}")
    if jyv == 1:
        pred = sp.nsimplify(a2form.subs({KB: sp.nsimplify(kbv), K2: sp.nsimplify(k2v)}))
        P(f"  route2_v2-gauge closed form={pred}: g00-match={sp.simplify(c0_0-pred)==0}"
          f" g0i-match={sp.simplify(c0_i-pred)==0}")
P(f"done ({time.time()-T0:.1f}s)")
