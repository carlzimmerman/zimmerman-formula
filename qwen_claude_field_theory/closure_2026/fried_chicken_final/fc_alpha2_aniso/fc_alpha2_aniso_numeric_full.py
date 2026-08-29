#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_alpha2_aniso_numeric_full.py  --  anisotropic FC-AeST alpha_1, alpha_2 with NUMERIC
(K_B,K_2,Q_0,J_Y) baked in from the start (so the quadratic-action build and the 10-field
order-by-order-in-wb solve are fast).  Full symmetric spatial metric h_ij retained through
variation; correct residual-diffeo gauge; two-channel [D2] perp==par consistency check.

This delivers the VERDICT the fully-symbolic solver is too heavy to reach in one sitting:
alpha_1 (validate = -4 K_B), alpha_2(perp), alpha_2(par), and their agreement, over a grid
INCLUDING a sweep of the scalar-mass combination m^2 ~ K_2 Q_0^2 (which regularises the
c_123=0 EA pole).  k=1 units; length scale carried by K_2 Q_0^2 = (m_Psi/k)^2 * (2-K_B).
"""
import sympy as sp, time, itertools, sys

T0 = time.time(); P = lambda *a: print(*a, flush=True)
eps, wb = sp.symbols('eps w_b', positive=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True); kv=[0,kx,ky,kz]
eta = sp.diag(-1,1,1,1); I = sp.I
Es, Eis = sp.symbols('E_s E_is')
Uh = sp.Symbol('U_hat')

def nf(tag):
    ket=sp.Symbol(tag+'k'); bra=sp.Symbol(tag+'b'); return ket*Es+bra*Eis, ket, bra
def d(f,mu):
    return sp.diff(f,Es)*(I*kv[mu]*Es)+sp.diff(f,Eis)*(-I*kv[mu]*Eis)

# amplitudes (module-level so they're shared)
Psi,Psik,Psib = nf('Psi')
Bf=[];Bk=[];Bb=[]
for i in range(3):
    f,kk,bb=nf(f'B{i+1}');Bf.append(f);Bk.append(kk);Bb.append(bb)
hh={};hk={};hb={}
for (i,j) in [(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]:
    f,kk,bb=nf(f'h{i}{j}');hh[(i,j)]=f;hh[(j,i)]=f;hk[(i,j)]=kk;hb[(i,j)]=bb
af=[];ak=[];ab=[]
for i in range(3):
    f,kk,bb=nf(f'a{i+1}');af.append(f);ak.append(kk);ab.append(bb)
chi,chik,chib = nf('chi'); rho,Rk,Rb = nf('rho'); a0f0,a0k,a0b = nf('a0p')

def te_maker(eps,wb):
    def te(e):
        e=sp.expand(e); out=0
        for i in range(3):
            ci=e.coeff(eps,i)
            for j in range(3):
                out+=ci.coeff(wb,j)*eps**i*wb**j
        return out
    return te
te = te_maker(eps,wb)
def wtr(e):
    e=sp.expand(e); return sum(e.coeff(wb,n)*wb**n for n in range(3))

def build_and_solve(KBv,K2v,Q0v,JYv):
    KB=sp.nsimplify(KBv);K2=sp.nsimplify(K2v);Q0=sp.nsimplify(Q0v);JY=sp.nsimplify(JYv);LAM=sp.S(0)
    ww=w1**2+w2**2+w3**2; S0=1+wb**2*ww/2
    Aup_bg=sp.Matrix([S0,wb*w1,wb*w2,wb*w3]); Adn_bg=eta*Aup_bg
    dphi_bg=-Q0*Adn_bg
    # metric
    H=sp.zeros(4,4);H[0,0]=-2*Psi
    for i in range(3): H[0,i+1]=Bf[i];H[i+1,0]=Bf[i]
    for i in range(1,4):
        for j in range(1,4): H[i,j]=hh[(i,j)]
    gd=sp.Matrix(4,4,lambda m,n: eta[m,n]+eps*H[m,n])
    Hup=eta*H*eta
    gu=sp.Matrix(4,4,lambda a,b:(eta-eps*Hup+eps**2*(Hup*H*eta))[a,b])
    trH=sum(eta[m,n]*H[m,n] for m in range(4) for n in range(4))
    HH=sum(Hup[m,n]*H[m,n] for m in range(4) for n in range(4))
    sqg=1+eps*trH/2+eps**2*(trH**2/8-HH/4)
    a0f=a0f0
    Adn=sp.Matrix([Adn_bg[0]-eps*a0f,Adn_bg[1]+eps*af[0],Adn_bg[2]+eps*af[1],Adn_bg[3]+eps*af[2]])
    Aup=sp.Matrix(4,1,lambda i,j:sum(gu[i,k]*Adn[k] for k in range(4)))
    C1=sp.expand(sum(Aup[i]*Adn[i] for i in range(4))+1).coeff(eps,1)
    solA=sp.solve([sp.expand(C1).coeff(Es,1),sp.expand(C1).coeff(Eis,1)],[a0k,a0b],dict=True)[0]
    solA={k:sp.expand(sp.series(v,wb,0,3).removeO()) for k,v in solA.items()}
    a0f=a0f.subs(solA)
    Adn=sp.Matrix([Adn_bg[0]-eps*a0f,Adn_bg[1]+eps*af[0],Adn_bg[2]+eps*af[1],Adn_bg[3]+eps*af[2]])
    Aup=sp.Matrix(4,1,lambda i,j:sum(gu[i,k]*Adn[k] for k in range(4)))
    dphi=sp.Matrix([dphi_bg[m]+eps*d(chi,m) for m in range(4)])
    gdT=sp.Matrix(4,4,lambda m,n:te(gd[m,n])); guT=sp.Matrix(4,4,lambda m,n:te(gu[m,n]))
    AupT=sp.Matrix(4,1,lambda i,j:te(Aup[i])); dphiT=sp.Matrix(4,1,lambda i,j:te(dphi[i]))
    GamT=[[[ te(sp.Rational(1,2)*sum(guT[r,s]*(d(gdT[s,n],m)+d(gdT[s,m],n)-d(gdT[m,n],s))
            for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]
    Fmn=sp.Matrix(4,4,lambda m,n:sp.expand(d(Adn[n],m)-d(Adn[m],n)))
    F1=sp.Matrix(4,4,lambda m,n:Fmn[m,n].coeff(eps,1))
    F2=eps**2*sum(F1[m,n]*F1[a,b]*eta[m,a]*eta[n,b] for m in range(4) for n in range(4)
                  for a in range(4) for b in range(4))
    Jup=[te(sum(AupT[nu]*(d(AupT[al],nu)+sum(GamT[al][nu][r]*AupT[r] for r in range(4)))
             for nu in range(4))) for al in range(4)]
    Jdphi=te(sum(Jup[m]*dphiT[m] for m in range(4)))
    Qc=te(sum(AupT[m]*dphiT[m] for m in range(4)))
    Yc=te(sum((guT[m,n]+AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
    dQ=Qc-Q0; Kq=-2*LAM+K2*te(dQ**2)
    def grade(e):
        e=sp.expand(e); return [wtr(e.coeff(eps,n)) for n in range(3)]
    def ric(a,b):
        o=0
        for m in range(4):
            o+=d(GamT[m][b][a],m)-d(GamT[m][m][a],b)
            for l in range(4):
                o+=te(GamT[m][m][l]*GamT[l][b][a]-GamT[m][b][l]*GamT[l][m][a])
        return te(o)
    Rsc=te(sum(guT[m,n]*ric(m,n) for m in range(4) for n in range(4)))
    gF2=grade(F2);gJ=grade(Jdphi);gY=grade(Yc);gK=grade(Kq);gsq=grade(sqg);gR=grade(Rsc)
    gS=[gR[n]-(2*LAM if n==0 else 0)-(KB/2)*gF2[n]+2*(2-KB)*gJ[n]-(2-KB)*gY[n]-gK[n] for n in range(3)]
    L2=wtr(sum(gsq[a]*gS[2-a] for a in range(3)))-(2-KB)*JY*gY[2]-16*sp.pi*wtr(rho*(-H[0,0]/2))
    L2=sp.expand(L2)
    pol=sp.Poly(L2,Es,Eis); L2dc=0
    for mon,cc in zip(pol.monoms(),pol.coeffs()):
        if mon[0]==mon[1]: L2dc+=cc*(Es*Eis)**mon[0]
    L2dc=L2dc.subs(Es*Eis,1)
    GAUGE={Bk[0]:0,Bb[0]:0,hk[(1,1)]:0,hb[(1,1)]:0,hk[(1,2)]:0,hb[(1,2)]:0,hk[(1,3)]:0,hb[(1,3)]:0}
    L2dc=sp.expand(L2dc.subs(GAUGE))
    NUM={ky:0,kz:0,kx:1}
    L2dc=sp.expand(L2dc.subs(NUM))
    BRAS=[Psib,Bb[1],Bb[2],hb[(2,2)],hb[(3,3)],hb[(2,3)],ab[0],ab[1],ab[2],chib]
    KETS=[Psik,Bk[1],Bk[2],hk[(2,2)],hk[(3,3)],hk[(2,3)],ak[0],ak[1],ak[2],chik]
    eqf={A:sp.expand(sp.diff(L2dc,A)) for A in BRAS}
    def lin(eqs,unk):
        M,b=sp.linear_eq_to_matrix(eqs,unk); s=list(sp.linsolve((M,b),unk))
        return dict(zip(unk,s[0])) if s else None
    VZ={Bk[1]:0,Bk[2]:0,ak[1]:0,ak[2]:0,hk[(2,3)]:0}
    su=[Psik,hk[(2,2)],hk[(3,3)],ak[0],chik]
    e0=[sp.expand(eqf[A].coeff(wb,0).subs(VZ)) for A in [Psib,hb[(2,2)],hb[(3,3)],ab[0],chib]]
    s0s=lin(e0,su)
    if s0s is None: return ('static-fail',)
    s0={**s0s,Bk[1]:sp.S(0),Bk[2]:sp.S(0),ak[1]:sp.S(0),ak[2]:sp.S(0),hk[(2,3)]:sp.S(0)}
    d1={A:sp.Symbol(f'd1_{A}') for A in KETS};d2={A:sp.Symbol(f'd2_{A}') for A in KETS}
    sub={A:s0[A]+wb*d1[A]+wb**2*d2[A] for A in KETS}
    eqW={A:sp.expand(eqf[A].subs(sub)) for A in BRAS}
    s1=lin([sp.expand(eqW[A].coeff(wb,1)) for A in BRAS],list(d1.values()))
    if s1 is None: return ('w1-fail',)
    e2=[sp.expand(eqW[A].coeff(wb,2)).subs(s1) for A in BRAS]
    s2=lin(e2,list(d2.values()))
    if s2 is None: return ('w2-fail',)
    kvl=lambda A: sp.expand(s0[A]+wb*d1[A].subs(s1)+wb**2*d2[A].subs(s2))
    subU={Rk:-Uh/(4*sp.pi)}
    b2=sp.expand(kvl(Bk[1]).coeff(wb,1).subs(subU)); a1=sp.cancel(2*b2.coeff(w2*Uh))
    ps2=sp.expand(kvl(Psik).coeff(wb,2).subs(subU))
    PA=sp.cancel(-2*ps2.coeff(w2**2*Uh)); PApar=sp.cancel(-2*ps2.coeff(w1**2*Uh))
    a2p=sp.cancel((PA+a1)/2); a2l=sp.cancel(-(PApar-PA)/2)
    return ('ok',complex(a1),complex(a2p),complex(a2l),sp.simplify(s0[Psik]))

if __name__=='__main__':
    P(f"{'K_B':>5} {'K2':>6} {'Q0':>4} {'JY':>4} | {'alpha_1':>10} (-4K_B={'':>0}) | {'a2_perp':>12} {'a2_par':>12}  [D2]")
    P("-"*88)
    grid=list(itertools.product([0.05,0.3],[10.0,300.0],[0.2,0.9],[1.0,2.0]))
    for kbv,k2v,q0v,jyv in grid:
        r=build_and_solve(kbv,k2v,q0v,jyv)
        if r[0]!='ok':
            P(f"{kbv:5} {k2v:6} {q0v:4} {jyv:4} | {r[0]}"); continue
        _,a1,a2p,a2l,psist=r
        dd=abs(a2p-a2l)
        P(f"{kbv:5} {k2v:6} {q0v:4} {jyv:4} | {a1.real:10.5f} (t={-4*kbv:.3f}) | {a2p.real:12.6g} {a2l.real:12.6g}  {'OK' if dd<1e-6 else f'D={dd:.1e}'}")
    P(f"\n[runtime {time.time()-T0:.1f}s]")
