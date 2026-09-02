#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Fast backstop for GATE 4: fix (K_B, J_Y=1, K2) numeric, keep c4 symbolic + Q0=q->0.
Solve alpha_1(c4)=0 at the physical deep field J_Y=1 and report c14*=K_B+c4* and the
spin-1 no-ghost condition c14>0. Reuses the cached L2dc_gen_c2c4.pkl from the main script.
"""
import sympy as sp, time, pickle, os, glob, sys
T0=time.time(); P=lambda *a: print(*a, flush=True)
# find the cache the main script built
cache=None
for root in ['/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula']:
    for c in glob.glob(root+'/*/scratchpad/L2dc_gen_c2c4.pkl'):
        cache=c
if not cache: P("no cache yet; run gen_aest_alpha1_c2c4.py first"); sys.exit(2)
L2dc=pickle.load(open(cache,'rb')); P(f"[cache] {cache}")
KB,Q0,K2,JY=sp.symbols('K_B Q_0 K_2 J_Y',real=True); C2,C4=sp.symbols('c2 c4',real=True)
w1,w2,w3=sp.symbols('w1 w2 w3',real=True); GT,LAM=sp.symbols('G_t Lambda',real=True)
kx=sp.symbols('k_x',real=True); wb=sp.Symbol('w_b',positive=True); q=sp.Symbol('q',positive=True)
def S(t): return sp.Symbol(t)
names=['Psi','Phi','B2','B3','s22','s23','a1','a2','a3','chi']
KETS=[S(n+'k') for n in names]; BRAS=[S(n+'b') for n in names]; Rk=S('rhok')
eq={A:sp.expand(sp.diff(L2dc,A)) for A in BRAS}
def lin(eqs,unk):
    Am,bb=sp.linear_eq_to_matrix(eqs,unk); s=list(sp.linsolve((Am,bb),unk))
    return dict(zip(unk,s[0])) if s else None
def alpha1(kbv,jyv,k2v,c4sym=True,c4val=0):
    sub={GT:1,LAM:0,kx:1,KB:sp.nsimplify(kbv),JY:sp.nsimplify(jyv),K2:sp.nsimplify(k2v),Q0:q,C2:0}
    sub[C4]=C4 if c4sym else sp.nsimplify(c4val)
    eqf={A:sp.expand(eq[A].subs(sub)) for A in BRAS}
    VZ={S('B2k'):0,S('B3k'):0,S('s23k'):0,S('a2k'):0,S('a3k'):0}
    stat=['Psi','Phi','s22','a1','chi']
    eq0=[sp.expand(eqf[S(n+'b')].coeff(wb,0).subs(VZ)) for n in stat]
    s0s=lin(eq0,[S(n+'k') for n in stat])
    if s0s is None: return None
    s0={**s0s,S('B2k'):sp.S(0),S('B3k'):sp.S(0),S('s23k'):sp.S(0),S('a2k'):sp.S(0),S('a3k'):sp.S(0)}
    U=sp.cancel(-s0[S('Psik')]/Rk)
    dk1={A:sp.Symbol(f'd1_{A}') for A in KETS}
    subF={A:s0[A]+wb*dk1[A] for A in KETS}
    eqW={A:sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1=lin([sp.expand(eqW[A].coeff(wb,1)) for A in BRAS],list(dk1.values()))
    if s1 is None: return 'SING1'
    c2t=sp.cancel(sp.expand(dk1[S('B2k')].subs(s1)).coeff(w2)/Rk)
    a1=sp.cancel(2*c2t/U)
    return sp.nsimplify(sp.limit(a1,q,0)) if a1.has(q) else sp.nsimplify(a1)
P("="*72); P("alpha_1(c4) at J_Y=1, solve alpha_1=0 for c4, report c14*=K_B+c4*"); P("="*72)
P(f"{'K_B':>6} {'alpha_1(c4)':>34} {'c4*':>12} {'c14*=K_B+c4*':>14} {'healthy?':>9}")
res=[]
for kbv in [sp.Rational(1,20),sp.Rational(1,10),sp.Rational(1,5),sp.Rational(1,4)]:
    a1c4=alpha1(kbv,1,10,c4sym=True)
    if not isinstance(a1c4,sp.Expr): P(f"{str(kbv):>6}  ladder returned {a1c4}"); continue
    sols=sp.solve(sp.Eq(a1c4,0),C4)
    for cs in sols:
        c14=sp.nsimplify(kbv+cs); healthy = c14>0
        P(f"{str(kbv):>6} {str(a1c4):>34} {str(sp.nsimplify(cs)):>12} {str(c14):>14} {'YES' if healthy else 'NO':>9}")
        res.append((kbv,sp.nsimplify(cs),c14,bool(healthy)))
    if not sols:
        P(f"{str(kbv):>6} {str(a1c4):>34}  (no real c4 zero)")
P(""); P("VERDICT:", "HEALTHY LOCUS EXISTS (extra crispy)" if any(h for *_,h in res) else
  "NO HEALTHY LOCUS -- alpha_1=0 forces c14=K_B+c4 <= 0 => spin-1 ghost (KILL stands, aether class dead in full)")
P(f"done ({time.time()-T0:.1f}s)")
