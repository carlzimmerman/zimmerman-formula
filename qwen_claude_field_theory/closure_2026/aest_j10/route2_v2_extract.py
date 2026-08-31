#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v2 anisotropic solve (s22,s23 included), fc's FIXED normalization U_hat=-4pi Rk.
Validate alpha_1=-4K_B, then alpha_2(J_Y) and C0=lim, C1. Compare to fc isotropic."""
import sympy as sp, pickle, time
T0=time.time(); P=lambda *a: print(*a,flush=True)
SC='/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/546626b7-08d0-4ddc-ac8f-d38babe5ed48/scratchpad/'
L2dc=pickle.load(open(SC+'L2dc_v2.pkl','rb'))
KB,Q0,K2,JY=sp.symbols('K_B Q_0 K_2 J_Y', real=True)
wb=sp.symbols('w_b', positive=True); w1,w2,w3=sp.symbols('w1 w2 w3', real=True)
GT,LAM,kx=sp.symbols('G_t Lambda k_x', real=True)
Uh=sp.Symbol('U_hat')
def S(t): return sp.Symbol(t)
names=['Psi','Phi','B2','B3','s22','s23','a1','a2','a3','chi']
KETS=[S(n+'k') for n in names]; BRAS=[S(n+'b') for n in names]
Rk=S('rhok')
Psik,Phik,s22k,a1k,chik=S('Psik'),S('Phik'),S('s22k'),S('a1k'),S('chik')
B2k,B3k,s23k,a2k,a3k=S('B2k'),S('B3k'),S('s23k'),S('a2k'),S('a3k')
eq={A: sp.expand(sp.diff(L2dc,A)) for A in BRAS}
def lin(eqs,unk):
    Am,bb=sp.linear_eq_to_matrix(eqs,unk); s=list(sp.linsolve((Am,bb),unk))
    return dict(zip(unk,s[0])) if s else None
subU={Rk:-Uh/(4*sp.pi)}   # fc fixed normalization

def solve(kbv,k2v,q0v,ISO=False):
    sub={KB:sp.nsimplify(kbv),K2:sp.nsimplify(k2v),Q0:sp.nsimplify(q0v),GT:1,LAM:0,kx:1}
    eqf={A: sp.expand(eq[A].subs(sub)) for A in BRAS}
    # ISO=True mimics fc by forcing s22=s23=0 (drop their eqs)
    active=[n for n in names if not (ISO and n in ('s22','s23'))]
    Aket={n:S(n+'k') for n in names}; Abra={n:S(n+'b') for n in names}
    VZ={B2k:0,B3k:0,s23k:0,a2k:0,a3k:0}
    if ISO: VZ[s22k]=0
    stat_fields=['Psi','Phi','s22','a1','chi'] if not ISO else ['Psi','Phi','a1','chi']
    eq0=[sp.expand(eqf[S(n+'b')].coeff(wb,0).subs(VZ)) for n in stat_fields]
    s0s=lin(eq0,[S(n+'k') for n in stat_fields])
    if s0s is None: return None
    s0={**s0s,B2k:sp.S(0),B3k:sp.S(0),s23k:sp.S(0),a2k:sp.S(0),a3k:sp.S(0)}
    if ISO: s0[s22k]=sp.S(0)
    KA=[S(n+'k') for n in active]; BA=[S(n+'b') for n in active]
    dk1={A:sp.Symbol(f'd1_{A}') for A in KA}; dk2={A:sp.Symbol(f'd2_{A}') for A in KA}
    subF={A: s0[A]+wb*dk1[A]+wb**2*dk2[A] for A in KA}
    if ISO: subF[s22k]=sp.S(0); subF[s23k]=sp.S(0)
    eqW={A: sp.expand(eqf[A].subs(subF)) for A in BA}
    s1=lin([sp.expand(eqW[A].coeff(wb,1)) for A in BA], list(dk1.values()))
    if s1 is None: return None
    # alpha_1 (fc): h02=B2 O(w). fc: alpha1 = -c2/(2pi), c2=coeff(w2 Rk) in B2^(1)
    c2=sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)
    alpha1=sp.cancel(-c2/(2*sp.pi))
    eq2=[sp.expand(eqW[A].coeff(wb,2)).subs(s1) for A in BA]
    s2=lin(eq2, list(dk2.values()))
    if s2 is None: return (alpha1,None)
    ps2=sp.expand(dk2[Psik].subs(s2)).subs(subU)   # Psi O(wb^2) in U_hat
    PA=sp.cancel(-2*ps2.coeff(w2**2*Uh))
    PApar=sp.cancel(-2*ps2.coeff(w1**2*Uh))
    PB=sp.cancel(PApar-PA)
    alpha2=sp.cancel(-PB/2)
    alpha2_A=sp.cancel((PA+alpha1)/2)
    return (alpha1,alpha2,alpha2_A)

P("VALIDATION alpha_1 == -4K_B (fixed U_hat, ANISOTROPIC s22/s23 on):")
for (kb,k2,q0) in [(sp.Rational(1,5),10,sp.Rational(2,5)),(sp.Rational(3,10),7,sp.Rational(3,5))]:
    r=solve(kb,k2,q0)
    P(f"  K_B={kb}: alpha_1={sp.simplify(r[0])}  ==-4K_B? {sp.simplify(r[0]+4*kb)==0}")

P("\nANISOTROPIC vs ISOTROPIC alpha_2 and C0=lim_{J_Y->oo}:")
for (kb,k2,q0) in [(sp.Rational(1,5),10,sp.Rational(2,5)),(sp.Rational(3,10),100,sp.Rational(1,5)),
                   (sp.Rational(1,10),50,sp.Rational(9,10)),(sp.Rational(1,2),5,sp.Rational(1,5))]:
    ra=solve(kb,k2,q0,ISO=False); ri=solve(kb,k2,q0,ISO=True)
    a2a=ra[1]; a2i=ri[1]
    # consistency: two extractions agree?
    agree=sp.simplify(ra[1]-ra[2])==0
    C0a=sp.limit(a2a,JY,sp.oo); C0i=sp.limit(a2i,JY,sp.oo)
    C1a=sp.simplify(sp.limit(JY*(a2a-C0a),JY,sp.oo))
    P(f"  K_B={kb},K2={k2},Q0={q0}:")
    P(f"     ANISO: C0={sp.nsimplify(C0a)}  C1={sp.nsimplify(C1a)} ({float(C1a):.4f})  two-extraction-agree={agree}")
    P(f"     ISO  : C0={sp.nsimplify(C0i)}   (fc-style)")
    P(f"     Route1 C1=2/(Q0^2(2-K_B))={float(2/(q0**2*(2-kb))):.4f}")
P(f"done ({time.time()-T0:.1f}s)")
