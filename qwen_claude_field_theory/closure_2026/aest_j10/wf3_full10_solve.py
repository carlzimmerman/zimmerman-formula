#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_full10_solve.py  (ADJUDICATION of the alpha_2 gauge discrepancy, w3=0)
==========================================================================
Solves the FULL ungauged 10-field (w3=0 WLOG) boosted base-AeST system from
L2dc_full10.pkl - i.e. {E_00,E_0i,E_ij,E_A,E_phi}+A^2=-1 with NO gauge fixing:
h01 and chi both live, gauge zero modes (xi^0, xi^1, xi^2) kept as free
parameters at each wb order and set two different ways (extraction must be
identical: h00 is static-gauge-invariant). Residual-checked on ALL equations.
Arbitrates (J_Y=1):
  (1/5,10):  alpha_2 c_0 = 13811/3645  (route2_v2, lost E_01)
             vs         19076/3645  (unitary chi=0, lost E_phi)
  (3/10,7):  alpha_2 c_0 = 135221/49130 (v2) vs 219031/49130 (unitary)
and re-certifies alpha_1(q->0) = -4(2+K_B J_Y)/(1+J_Y) on the full system.
"""
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
Rk = S('rhok'); Psik = S('Psik')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}

def solve_param(eqs, unk, fixval):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    sols = list(sp.linsolve((Am, bb), unk))
    if not sols: return None
    sol = dict(zip(unk, sols[0]))
    free = [u for u in unk if sol[u] == u]
    subsf = {u: fixval*Rk*(i + 1) for i, u in enumerate(free)}
    sol = {k: sp.expand(v.subs(subsf)) for k, v in sol.items()}
    return sol, free

def run(kbv, k2v, jyv, qval, fixval):
    sub = {KB: sp.nsimplify(kbv), K2: sp.nsimplify(k2v), JY: sp.nsimplify(jyv),
           Q0: qval, GT: 1, LAM: 0, kx: 1}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    eq0 = [sp.expand(eqf[b].coeff(wb, 0)) for b in BRAS]
    r0 = solve_param(eq0, KETS, fixval)
    if r0 is None: return 'INC0'
    s0, free0 = r0
    ok0 = all(sp.simplify(e.subs(s0)) == 0 for e in eq0)
    U_amp = sp.cancel(-s0[Psik]/Rk)
    Phi0 = sp.cancel(-(s0[S('H22k')] + s0[S('H33k')])/4)
    gamma = sp.cancel(Phi0/(-s0[Psik]))
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    E1 = [sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS]
    r1 = solve_param(E1, list(dk1.values()), fixval)
    if r1 is None: return 'INC1'
    s1, free1 = r1
    ok1 = all(sp.simplify(e.subs(s1)) == 0 for e in E1)
    c2t = sp.cancel(sp.expand(dk1[S('B2k')].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(2*c2t/U_amp)
    E2 = [sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS]
    r2 = solve_param(E2, list(dk2.values()), fixval)
    if r2 is None: return 'INC2'
    s2, free2 = r2
    ok2 = all(sp.simplify(e.subs(s2)) == 0 for e in E2)
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
    Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    alpha2 = sp.cancel((Cpar - Cperp)/2)
    alpha3 = sp.cancel(Cperp + alpha1)
    return dict(U=U_amp, g=gamma, a1=alpha1, a2=alpha2, a3=alpha3,
                nfree=(len(free0), len(free1), len(free2)),
                res=(ok0, ok1, ok2))

targets = [((sp.Rational(1, 5), 10, 1),
            sp.Rational(13811, 3645), sp.Rational(19076, 3645)),
           ((sp.Rational(3, 10), 7, 1),
            sp.Rational(135221, 49130), sp.Rational(219031, 49130)),
           ((sp.Rational(1, 5), 10, 2),
            -sp.Rational(959, 1215), sp.Rational(107, 2430))]
for (kbv, k2v, jyv), v2pred, unipred in targets:
    P("="*74)
    P(f"FULL UNGAUGED SOLVE (w3=0)  K_B={kbv} K2={k2v} J_Y={jyv}  (q symbolic)")
    P("="*74)
    outs = []
    for fixval, lab in [(sp.S(0), 'gauge A (free=0)'),
                        (sp.S(3), 'gauge B (free=3Rk,6Rk,..)')]:
        r = run(kbv, k2v, jyv, q, fixval)
        if not isinstance(r, dict):
            P(f"  {lab}: {r}"); continue
        a1_0 = sp.limit(r['a1'], q, 0)
        cm2 = sp.limit(r['a2']*q**2, q, 0)
        c0 = sp.limit(sp.cancel(r['a2'] - cm2/q**2), q, 0)
        P(f"  {lab}: free/order={r['nfree']} residuals-zero={r['res']}")
        P(f"    U(q->0)={sp.nsimplify(sp.limit(r['U'],q,0))} gamma={sp.simplify(r['g'])} "
          f"alpha_3=={sp.simplify(r['a3'])}")
        P(f"    alpha_1(q->0)={a1_0} [pred {sp.nsimplify(-4*(2+sp.nsimplify(kbv)*jyv)/(1+jyv))}]"
          f"  alpha_2: c_-2={sp.nsimplify(cm2)} c_0={sp.nsimplify(c0)}")
        outs.append((a1_0, cm2, c0))
    if len(outs) == 2:
        P(f"  gauge-choice-independent: "
          f"{all(sp.simplify(a-b)==0 for a,b in zip(outs[0],outs[1]))}")
    if outs:
        c0 = outs[0][2]
        P(f"  VERDICT alpha_2 c_0={sp.nsimplify(c0)} : v2({v2pred})="
          f"{sp.simplify(c0-v2pred)==0}  unitary({unipred})="
          f"{sp.simplify(c0-unipred)==0}")
P(f"done ({time.time()-T0:.1f}s)")
