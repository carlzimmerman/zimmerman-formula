#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf3_alpha2_closedform.py  (closed forms: base-AeST PPN alpha_1, alpha_2)
========================================================================
Certified pipeline (see wf3_will_dictionary_certificate / wf3_pure_ea_control
/ wf3_eta_K_final). Established so far (exact, multi-point):
  alpha_1 = -4 eta_K,   eta_K = (2 + K_B J_Y)/(1 + J_Y)          [PPN q->0]
  alpha_2(q) = c_-2/q^2 + c_0 + O(q^2),  c_-2 = -eta_K^2/((2-K_B)^2 J_Y)
  c_0 = A(K_B,J_Y) + B(K_B,J_Y) K2   (exactly linear in K2)
This script: (1) certify the hand-identified closed form
  B = (4 + 4 K_B J_Y - K_B^2 J_Y)/(J_Y^2 (2-K_B)^3)
on every grid point; (2) exact overdetermined 2D fit for A(K_B,J_Y); (3)
K_B->0 continuity check of alpha_1 (scalar-only preferred-frame effect);
(4) assemble alpha_2 closed form, lam2_eff, J_Y->oo limits, healthy-region
numbers vs Will bounds.
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
def ladder(kbv, k2v, jyv, want_a1=False):
    sub = {GT: 1, LAM: 0, kx: 1, KB: sp.nsimplify(kbv),
           K2: sp.nsimplify(k2v), JY: sp.nsimplify(jyv), Q0: q}
    eqf = {A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ = {B2k: 0, B3k: 0, s23k: 0, a2k: 0, a3k: 0}
    stat = ['Psi', 'Phi', 's22', 'a1', 'chi']
    eq0 = [sp.expand(eqf[S(n+'b')].coeff(wb, 0).subs(VZ)) for n in stat]
    s0s = lin(eq0, [S(n+'k') for n in stat])
    if s0s is None: return None
    s0 = {**s0s, B2k: sp.S(0), B3k: sp.S(0), s23k: sp.S(0),
          a2k: sp.S(0), a3k: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk)
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None: return 'SING1'
    a1v = None
    if want_a1:
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
    return sp.nsimplify(cm2), sp.nsimplify(c0), a1v

etaK = lambda kb, jy: (2 + sp.nsimplify(kb)*jy)/(1 + jy)
Bform = lambda kb, jy: (4 + 4*kb*jy - kb**2*jy)/(jy**2*(2-kb)**3)

P("="*74)
P("1. grid + certifications  (c_-2 form, B closed form, K2-linearity implicit)")
P("="*74)
pairs = [(sp.Rational(1,5),1), (sp.Rational(3,10),1), (sp.Rational(1,2),1),
         (sp.Rational(1,10),1), (sp.Rational(1,4),1), (sp.Rational(2,5),1),
         (sp.Rational(1,5),2), (sp.Rational(1,5),3), (sp.Rational(1,5),5),
         (sp.Rational(3,10),2), (sp.Rational(3,10),3), (sp.Rational(1,2),2),
         (sp.Rational(1,2),3), (sp.Rational(1,10),2), (sp.Rational(1,10),3),
         (sp.Rational(2,5),2), (sp.Rational(2,5),4), (sp.Rational(1,4),2)]
Adata = {}
allok_B = True; allok_cm2 = True
for kb, jy in pairs:
    cm2_a, c0_a, _ = ladder(kb, 10, jy)
    cm2_b, c0_b, _ = ladder(kb, 50, jy)
    Bv = sp.nsimplify((c0_b - c0_a)/40)
    Av = sp.nsimplify(c0_a - 10*Bv)
    okB = sp.simplify(Bv - Bform(sp.nsimplify(kb), sp.nsimplify(jy))) == 0
    okc = sp.simplify(cm2_a + etaK(kb, jy)**2/((2-sp.nsimplify(kb))**2*jy)) == 0
    allok_B &= okB; allok_cm2 &= okc
    Adata[(sp.nsimplify(kb), sp.nsimplify(jy))] = Av
    P(f"  (KB={kb},JY={jy}): A={Av}  B-closed-form={okB}  c_-2-form={okc}")
P(f"  ALL B == (4+4KB*JY-KB^2*JY)/(JY^2 (2-KB)^3): {allok_B}")
P(f"  ALL c_-2 == -etaK^2/((2-KB)^2 JY):           {allok_cm2}")
P(f"({time.time()-T0:.1f}s)")

P("")
P("="*74)
P("2. exact 2D fit of A(K_B,J_Y): numerator poly / [(2-KB)^s JY^p (1+JY)^r]")
P("="*74)
kbs, jys = sp.symbols('kbs jys')
found = None
for s_, p_, r_ in itertools.product((2, 3), (1, 2), (0, 1, 2)):
    den = (2-kbs)**s_ * jys**p_ * (1+jys)**r_
    coeffs = {}
    terms = []
    cc = []
    for i in range(4):
        for j in range(4):
            csym = sp.Symbol(f'c_{i}_{j}')
            cc.append(csym); terms.append(csym*kbs**i*jys**j)
    Pnum = sum(terms)
    eqs = [sp.expand((Pnum - Av*den).subs({kbs: kb, jys: jy}))
           for (kb, jy), Av in Adata.items()]
    Am, bb = sp.linear_eq_to_matrix(eqs, cc)
    sol = list(sp.linsolve((Am, bb), cc))
    if sol:
        sold = dict(zip(cc, sol[0]))
        free = [c for c in cc if sold[c] == c]
        sold2 = {k: v.subs({f: 0 for f in free}) for k, v in sold.items()}
        Afit = sp.cancel(Pnum.subs(sold2)/den)
        chk = all(sp.simplify(Afit.subs({kbs: kb, jys: jy}) - Av) == 0
                  for (kb, jy), Av in Adata.items())
        if chk:
            found = (s_, p_, r_, sp.simplify(Afit))
            P(f"  CONSISTENT fit with den (2-KB)^{s_} JY^{p_} (1+JY)^{r_}:")
            P("    A(K_B,J_Y) =", found[3])
            break
if found is None:
    P("  no consistent fit in the scanned family; raw A values stand as exact data")
P(f"({time.time()-T0:.1f}s)")

P("")
P("="*74)
P("3. K_B -> 0 continuity of alpha_1 (scalar-only preferred-frame residue)")
P("="*74)
for kbv in (sp.Rational(1, 100), 0):
    try:
        r = ladder(kbv, 10, 1, want_a1=True)
        if isinstance(r, str):
            P(f"  K_B={kbv}: {r}")
        else:
            P(f"  K_B={kbv}: alpha_1(q->0) = {r[2]}  [pred -4(2+KB)/2 = {sp.nsimplify(-2*(2+kbv))}]")
    except Exception as e:
        P(f"  K_B={kbv}: EXC {e!r}")
P(f"({time.time()-T0:.1f}s)")

P("")
P("="*74)
P("4. assembled result + healthy-region evaluation vs Will bounds")
P("="*74)
etaS = (2 + KB*JY)/(1 + JY)
alpha1S = -4*etaS
BS = (4 + 4*KB*JY - KB**2*JY)/(JY**2*(2-KB)**3)
P("  alpha_1 = -4(2+K_B J_Y)/(1+J_Y);  deep field J_Y=1: alpha_1 = -(4+2K_B)")
P("  alpha_2 = A(K_B,J_Y) + K2*(4+4K_B J_Y-K_B^2 J_Y)/(J_Y^2 (2-K_B)^3)  [+ contact c_-2/q^2]")
if found:
    AS = found[3].subs({kbs: KB, jys: JY})
    a2S = sp.simplify(AS + K2*BS)
    P("  closed alpha_2 =", a2S)
    a2_J1 = sp.simplify(a2S.subs(JY, 1))
    P("  alpha_2(J_Y=1) =", a2_J1)
    P("  J_Y->oo: alpha_1 ->", sp.limit(alpha1S, JY, sp.oo),
      " (pure-EA FJ -4K_B);  alpha_2 ->", sp.simplify(sp.limit(a2S, JY, sp.oo)))
    lam2 = sp.simplify(etaS**2/(2*a2S + etaS))
    P("  lam2_eff = etaK^2/(2 alpha2 + etaK) =", lam2)
    for kbv, k2v in [(sp.Rational(1,10), 1), (sp.Rational(1,10), 10),
                     (sp.Rational(1,4), 1), (sp.Rational(1,4), 10)]:
        a1n = float(alpha1S.subs({KB: kbv, JY: 1}))
        a2n = float(a2_J1.subs({KB: kbv, K2: k2v}))
        P(f"  K_B={kbv} K2={k2v}: alpha_1={a1n:+.4f} (bound 1e-4) "
          f"alpha_2={a2n:+.4f} (bound 1e-7..1e-4)  -> excluded by ~{abs(a1n)/1e-4:.0e}x / {abs(a2n)/1e-7:.0e}x")
P("  eta_K zero-locus: eta_K=(2+K_B J_Y)/(1+J_Y)=0 <=> K_B J_Y = -2: IMPOSSIBLE for K_B>0,J_Y>0")
P("  => eta_K NONZERO everywhere in the healthy region (0<K_B<0.25, K2>0, J_Y=1); min eta_K=1 (K_B->0)")
P(f"done ({time.time()-T0:.1f}s)")
