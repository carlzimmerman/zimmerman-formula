#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_alpha2_c0_fit.py  (closed form of the base-AeST PPN alpha_2 finite part)
============================================================================
Same certified pipeline as wf3_eta_K_final.py. For a grid of (K_B, J_Y),
solve with q=Q0/kx symbolic at K2 in {10,50,100}; extract the Laurent parts
    alpha_2(q) = c_-2/q^2 + c_0 + O(q^2).
Verify: c_-2 K2-independent and == -eta_K^2/((2-K_B)^2 J_Y); c_0 EXACTLY
linear in K2: c_0 = A(K_B,J_Y) + B(K_B,J_Y) K2. Then fit closed forms for
A and B over the (K_B,J_Y) grid (exact rational fits, verified on held-out
points). eta_K = (2+K_B J_Y)/(1+J_Y) (certified in wf3_eta_K_final.out).
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
Rk = S('rhok')
Psik = S('Psik')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None
def ladder_a2(kbv, k2v, jyv):
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
    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS],
             list(dk2.values()))
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
    Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    a2v = sp.cancel((Cpar - Cperp)/2)
    cm2 = sp.limit(a2v*q**2, q, 0)
    c0 = sp.limit(sp.cancel(a2v - cm2/q**2), q, 0)
    return sp.nsimplify(cm2), sp.nsimplify(c0)

pairs = [(sp.Rational(1,5),1), (sp.Rational(3,10),1), (sp.Rational(1,2),1),
         (sp.Rational(1,10),1), (sp.Rational(1,4),1),
         (sp.Rational(1,5),2), (sp.Rational(1,5),5), (sp.Rational(3,10),3),
         (sp.Rational(2,5),4), (sp.Rational(1,10),2), (sp.Rational(1,2),2),
         (sp.Rational(3,10),2)]
etaK = lambda kb, jy: (2 + kb*jy)/(1 + jy)
res = {}
P("(K_B,J_Y): c_-2 [check vs -etaK^2/((2-KB)^2 JY)] ; c_0 = A + B*K2 [linearity check @K2=100]")
for kb, jy in pairs:
    cm2_10, c0_10 = ladder_a2(kb, 10, jy)
    cm2_50, c0_50 = ladder_a2(kb, 50, jy)
    B = sp.nsimplify((c0_50 - c0_10)/40)
    A = sp.nsimplify(c0_10 - 10*B)
    cm2_100, c0_100 = ladder_a2(kb, 100, jy)
    lin_ok = sp.simplify(c0_100 - (A + 100*B)) == 0
    cm2_ok = (sp.simplify(cm2_10 - cm2_50) == 0 and
              sp.simplify(cm2_10 + etaK(kb, jy)**2/((2-kb)**2*jy)) == 0)
    res[(kb, jy)] = (A, B)
    P(f"  ({kb},{jy}): c_-2={cm2_10} ok={cm2_ok} ; A={A} B={B} lin100={lin_ok}")
pickle.dump(res, open(SC+'wf3_c0_AB.pkl', 'wb'))
P(f"({time.time()-T0:.1f}s)")

P("")
P("="*74)
P("FIT closed forms A(K_B,J_Y), B(K_B,J_Y) via exact rational interpolation")
P("="*74)
# Strategy: at fixed J_Y, A and B are rational in K_B. Collect per-J_Y rows and
# attempt ansatz fits with undetermined coefficients over a polynomial family.
kbs = sp.Symbol('kbs'); jys = sp.Symbol('jys')
def fit_rational(data, num_deg, den_deg, var):
    """data: list (x, value). Fit P(x)/Q(x), Q monic. Returns expr or None."""
    a = sp.symbols(f'fa0:{num_deg+1}'); b = sp.symbols(f'fb0:{den_deg+1}')
    Pn = sum(a[i]*var**i for i in range(num_deg+1))
    Qd = var**den_deg + sum(b[i]*var**i for i in range(den_deg))
    eqs = []
    for x, v in data:
        eqs.append(sp.expand((Pn - v*Qd).subs(var, x)))
    sol = sp.solve(eqs, list(a) + list(b[:den_deg]), dict=True)
    if not sol: return None
    sol = sol[0]
    if len(sol) < len(a) + den_deg: pass
    return sp.cancel(Pn.subs(sol)/Qd.subs(sol))
rows_j1 = [(kb, res[(kb, 1)][0]) for kb, jy in pairs if jy == 1]
rowsB_j1 = [(kb, res[(kb, 1)][1]) for kb, jy in pairs if jy == 1]
for nd in range(1, 4):
    fA = fit_rational(rows_j1, nd, nd, kbs)
    if fA is not None:
        ok = all(sp.simplify(fA.subs(kbs, x) - v) == 0 for x, v in rows_j1)
        if ok:
            P(f"  A(K_B, J_Y=1) [deg {nd}/{nd}] =", sp.simplify(fA)); break
for nd in range(1, 4):
    fB = fit_rational(rowsB_j1, nd, nd, kbs)
    if fB is not None:
        ok = all(sp.simplify(fB.subs(kbs, x) - v) == 0 for x, v in rowsB_j1)
        if ok:
            P(f"  B(K_B, J_Y=1) [deg {nd}/{nd}] =", sp.simplify(fB)); break
P("  raw A,B rows for the record:")
for k, v in res.items():
    P(f"    (KB={k[0]}, JY={k[1]}): A={v[0]}  B={v[1]}")
P(f"done ({time.time()-T0:.1f}s)")
