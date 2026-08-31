#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_eta_K_q0limit.py  (PPN limit Q0/k -> 0 of the base-AeST boosted solve)
==========================================================================
Companion to wf3_base_aest_eta_K_solve.py (same cached L2dc_v2.pkl, same
CERTIFIED dictionary - see wf3_will_dictionary_certificate.py and the pure-EA
control wf3_pure_ea_control_build.py). kx=1, so Q0 means Q0/kx; PPN scales
(solar k >> cosmological aether mass) = Q0 -> 0.

Solves with Q0 SYMBOLIC at numeric (K_B, K2, J_Y), takes exact Q0->0 limits of
U_amp (G_N), alpha_1, alpha_2, alpha_3; scans K2 and J_Y dependence of the
limits; maps out eta_K = -alpha_1/4 as a function of (K_B, J_Y).
"""
import sympy as sp, pickle, time, os, itertools
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
q = sp.Symbol('q', positive=True)          # symbolic Q0
def S(t): return sp.Symbol(t)
names = ['Psi', 'Phi', 'B2', 'B3', 's22', 's23', 'a1', 'a2', 'a3', 'chi']
KETS = [S(n+'k') for n in names]; BRAS = [S(n+'b') for n in names]
Rk = S('rhok')
Psik, Phik, s22k, a1k, chik = S('Psik'), S('Phik'), S('s22k'), S('a1k'), S('chik')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None

def solve_symQ0(kbv, k2v, jyv):
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
    gamma = sp.cancel(s0[Phik]/s0[Psik])
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
    return U_amp, gamma, alpha1, alpha2, alpha3

P("="*74)
P("Q0->0 (PPN) LIMITS of the base-AeST boosted solve  [dictionary CERTIFIED]")
P("="*74)
rows = []
cases = [ (sp.Rational(1,5), 10, 1), (sp.Rational(1,5), 50, 1),
          (sp.Rational(1,5), 10, 2), (sp.Rational(1,5), 10, 5),
          (sp.Rational(3,10), 10, 1), (sp.Rational(1,10), 10, 1),
          (sp.Rational(1,2), 10, 1), (sp.Rational(1,4), 10, 1),
          (sp.Rational(3,10), 25, 3) ]
for kbv, k2v, jyv in cases:
    U_amp, gamma, a1v, a2v, a3v = solve_symQ0(kbv, k2v, jyv)
    U0 = sp.limit(U_amp, q, 0)
    a1_0 = sp.limit(a1v, q, 0)
    a3_0 = sp.limit(a3v, q, 0)
    # alpha_2 may diverge as q->0: get the Laurent structure
    a2ser = sp.series(sp.together(a2v), q, 0, 1)
    P(f"\nK_B={kbv} K2={k2v} J_Y={jyv}:")
    P(f"  gamma = {sp.simplify(gamma)}")
    P(f"  U_amp(q->0) = {sp.nsimplify(U0)}   [4pi/(1-KB/2) = {sp.nsimplify(4*sp.pi/(1-kbv/2))}]")
    P(f"  alpha_1(q->0) = {sp.nsimplify(a1_0)} = {float(a1_0):.6f}   (-4K_B = {float(-4*kbv):.4f})")
    P(f"  eta_K = -alpha_1/4 = {sp.nsimplify(-a1_0/4)} = {float(-a1_0/4):.6f}   (K_B = {float(kbv):.4f})")
    P(f"  alpha_3(q->0) = {sp.simplify(a3_0)}")
    P(f"  alpha_2 series in q: {a2ser}")
    rows.append((kbv, k2v, jyv, a1_0))
pickle.dump(rows, open(SC+'wf3_q0limit_rows.pkl', 'wb'))
P(f"\ndone ({time.time()-T0:.1f}s)")
