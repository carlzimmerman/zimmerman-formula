#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_eta_K_final.py  (SOLVE A final: base-AeST eta_K + alpha_2 finite part)
==========================================================================
Corrected-extraction version (expand BEFORE coeff; the earlier
wf3_eta_K_q0limit.py had cancel() re-packing the expression so .coeff(w^2)
returned 0 - documented bug, its alpha_2/alpha_3 columns are void; its
alpha_1/U_amp/gamma columns are valid and reproduced here).

Pipeline: cached L2dc_v2.pkl (base AeST, J_Y inert), certified Will dictionary
(wf3_will_dictionary_certificate.py) validated end-to-end against pure-EA
Foster-Jacobson (wf3_pure_ea_control_build.py): alpha_1 = +2*coeff/U_amp
(w_Will = -wb*w), alpha_2 = (Cpar-Cperp)/2, alpha_3 = Cperp+alpha_1 == 0 gate.

PPN reading at kx=1: q := Q0/kx -> 0. alpha_1(q) is regular at q=0.
alpha_2(q) = c_-2/q^2 + c_0 + O(q^2): the c_-2/q^2 = c_-2 kx^2/Q0^2 piece
multiplies U_hat ~ rho_hat/k^2, i.e. it is a DENSITY-CONTACT term (vanishes
outside the source) NOT a 1/r PPN potential; the PPN alpha_2 is the finite
part c_0. Checks below verify the q=0-exact solve reproduces c_0 (regular
finite-part extraction) and alpha_3(q) == 0 identically.
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
Psik, Phik = S('Psik'), S('Phik')
B2k, B3k, s23k, a2k, a3k = S('B2k'), S('B3k'), S('s23k'), S('a2k'), S('a3k')
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    return dict(zip(unk, s[0])) if s else None

def ladder(subx):
    """Full wb ladder with CORRECTED extraction. subx: dict for KB,K2,JY,Q0."""
    sub = {GT: 1, LAM: 0, kx: 1}; sub.update(subx)
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    stat = ['Psi', 'Phi', 's22', 'a1', 'chi']
    eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
    s0s = lin(eq0, [S(n+'k') for n in stat])
    if s0s is None: return None
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0),
          a2k: sp.S(0), a3k: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk)
    gamma = sp.cancel(s0[Phik]/s0[Psik])
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None: return ('SING1', U_amp, gamma)
    c2t = sp.cancel(sp.expand(dk1[S('B2k')].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(2*c2t/U_amp)
    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS],
             list(dk2.values()))
    if s2 is None: return (alpha1, 'SING2', U_amp, gamma)
    h2 = sp.expand(-2*dk2[Psik].subs(s2))          # expand FIRST, then coeff
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp)
    Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    alpha2 = sp.cancel((Cpar - Cperp)/2)
    alpha3 = sp.cancel(Cperp + alpha1)
    return dict(U=U_amp, g=gamma, a1=alpha1, a2=alpha2, a3=alpha3)

P("="*74)
P("B. exact q-dependence at (K_B,K2,J_Y)=(1/5,10,1)")
P("="*74)
r = ladder({KB: sp.Rational(1, 5), K2: 10, JY: 1, Q0: q})
a1q, a2q, a3q = r['a1'], r['a2'], r['a3']
P("  alpha_1(q) =", a1q)
P("  alpha_3(q) identically 0? ->", sp.simplify(a3q) == 0, " (", sp.simplify(a3q), ")")
a2ser = sp.series(sp.expand(a2q), q, 0, 3)
P("  alpha_2(q) Laurent:", a2ser)
c_m2 = sp.limit(a2q*q**2, q, 0)
c_0 = sp.limit(sp.cancel(a2q - c_m2/q**2), q, 0)
P("  c_-2 =", sp.nsimplify(c_m2), "  c_0 (PPN alpha_2) =", sp.nsimplify(c_0),
  "=", float(c_0))
P("  consistency: pass-1 value at q=2/5:", float(a2q.subs(q, sp.Rational(2, 5))),
  " (expect -2.12546)")
P(f"  ({time.time()-T0:.1f}s)")

P("")
P("="*74)
P("C. q=0-EXACT solve vs Laurent finite part (regularity of the PPN limit)")
P("="*74)
r0 = ladder({KB: sp.Rational(1, 5), K2: 10, JY: 1, Q0: 0})
if isinstance(r0, dict):
    P("  q=0 solve: alpha_1 =", sp.nsimplify(r0['a1']),
      " alpha_2 =", sp.nsimplify(r0['a2']), " alpha_3 =", sp.simplify(r0['a3']))
    P("  alpha_1(q=0) == lim alpha_1:", sp.simplify(r0['a1'] - sp.limit(a1q, q, 0)) == 0)
    P("  alpha_2(q=0) == c_0:", sp.simplify(r0['a2'] - c_0) == 0)
else:
    P("  q=0 solve singular:", r0[0] if isinstance(r0, tuple) else r0)
P(f"  ({time.time()-T0:.1f}s)")

P("")
P("="*74)
P("D. grid: PPN limits over (K_B, K2, J_Y)  [q symbolic, Laurent parts]")
P("="*74)
grid = [(sp.Rational(1,5),10,1), (sp.Rational(1,5),50,1), (sp.Rational(1,5),10,2),
        (sp.Rational(1,5),10,5), (sp.Rational(3,10),10,1), (sp.Rational(1,10),10,1),
        (sp.Rational(1,2),10,1), (sp.Rational(1,4),10,1), (sp.Rational(3,10),25,3),
        (sp.Rational(1,10),50,2), (sp.Rational(2,5),20,4)]
rows = []
for kbv, k2v, jyv in grid:
    rr = ladder({KB: kbv, K2: sp.nsimplify(k2v), JY: sp.nsimplify(jyv), Q0: q})
    a1_0 = sp.nsimplify(sp.limit(rr['a1'], q, 0))
    cm2 = sp.nsimplify(sp.limit(rr['a2']*q**2, q, 0))
    c0v = sp.nsimplify(sp.limit(sp.cancel(rr['a2'] - cm2/q**2), q, 0))
    a3id = sp.simplify(rr['a3'])
    rows.append((kbv, k2v, jyv, a1_0, cm2, c0v))
    P(f"  KB={kbv} K2={k2v} JY={jyv}: alpha1(0)={a1_0}  "
      f"pred(-4(2+KB*JY)/(1+JY))={sp.nsimplify(-4*(2+kbv*jyv)/(1+jyv))}  "
      f"c_-2={cm2}  c_0={c0v}={float(c0v):.6f}  alpha3=={a3id}")
pickle.dump(rows, open(SC+'wf3_final_rows.pkl', 'wb'))
P(f"  ({time.time()-T0:.1f}s)")

P("")
P("="*74)
P("E. SYMBOLIC certificate: q=0, K_B & J_Y symbolic (K2 numeric x2)")
P("="*74)
for k2v in (10, 50):
    try:
        rs = ladder({K2: sp.nsimplify(k2v), Q0: 0})
        a1s = sp.simplify(rs['a1']); a2s = sp.simplify(rs['a2'])
        a3s = sp.simplify(rs['a3'])
        P(f"  K2={k2v}:")
        P("    alpha_1(K_B,J_Y) =", a1s)
        P("    check == -4(2+K_B J_Y)/(1+J_Y):",
          sp.simplify(a1s + 4*(2 + KB*JY)/(1 + JY)) == 0)
        P("    eta_K = -alpha_1/4 =", sp.simplify(-a1s/4))
        P("    alpha_2(K_B,J_Y) =", a2s)
        P("    alpha_3 ==", a3s)
        etaK = sp.simplify(-a1s/4)
        lam2 = sp.simplify(etaK**2/(2*a2s + etaK))
        P("    lam2_eff = etaK^2/(2 a2 + etaK) =", lam2)
        P("    alpha_2 at J_Y=1 :", sp.simplify(a2s.subs(JY, 1)))
        P("    alpha_2 J_Y->oo  :", sp.simplify(sp.limit(a2s, JY, sp.oo)),
          "  [Route-3 suggestive C0=-K_B/2 cross-check]")
        P("    alpha_1 J_Y->oo  :", sp.simplify(sp.limit(a1s, JY, sp.oo)),
          "  [pure-EA FJ = -4K_B]")
    except Exception as e:
        P(f"  K2={k2v}: FAILED {e!r}")
P(f"done ({time.time()-T0:.1f}s)")
