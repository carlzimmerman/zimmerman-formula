#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_alpha2_fp_solve.py  --  FAST anisotropic FC-AeST alpha_1, alpha_2.
The metric background is FLAT (only the aether/scalar are boosted), so the O(eps^2) EH action
is the standard Fierz-Pauli / linearized-Einstein form  L_EH = (1/2) h^{mn} G^(1)_{mn}[h],
computed from SECOND DERIVATIVES of h (NO Christoffel products) => no symbolic blow-up.
The dark sector (F^2, J.dphi via Christoffels-only, Y, Q, K, unit constraint) is unchanged and
already cheap.  Numeric (K_B,K_2,Q_0,J_Y).  Full symmetric spatial metric h_ij.

SELF-VALIDATION (must pass, else the anisotropic number is not trusted):
  ISO gate:   with h_ij = -2 Phi delta_ij (isotropic ansatz) reproduce the committed
              alpha_1 = -4 K_B  (fc_ctensor_map)  in the Q0->0 decouple limit.
  [D2]:       anisotropic two channels agree  alpha_2(perp) == alpha_2(par).
Reports alpha_1, alpha_2(perp,par) over a grid + a scalar-mass (K2 Q0^2) sweep.

MODE: pass 'iso' or 'aniso' as argv[1] (default aniso).  'validate' runs iso+aniso compare.
"""
import sympy as sp, time, itertools, sys

T0=time.time(); P=lambda *a: print(*a, flush=True)
eps,wb=sp.symbols('eps w_b',positive=True)
w1,w2,w3=sp.symbols('w1 w2 w3',real=True)
kx,ky,kz=sp.symbols('k_x k_y k_z',real=True); kv=[0,kx,ky,kz]
eta=sp.diag(-1,1,1,1); I=sp.I
Es,Eis=sp.symbols('E_s E_is'); Uh=sp.Symbol('U_hat')

def nf(tag):
    ket=sp.Symbol(tag+'k');bra=sp.Symbol(tag+'b');return ket*Es+bra*Eis,ket,bra
def d(f,mu):
    return sp.diff(f,Es)*(I*kv[mu]*Es)+sp.diff(f,Eis)*(-I*kv[mu]*Eis)

# amplitudes
Psi,Psik,Psib=nf('Psi')
Bf=[];Bk=[];Bb=[]
for i in range(3):
    f,kk,bb=nf(f'B{i+1}');Bf.append(f);Bk.append(kk);Bb.append(bb)
hh={};hk={};hb={}
for (i,j) in [(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]:
    f,kk,bb=nf(f'h{i}{j}');hh[(i,j)]=f;hh[(j,i)]=f;hk[(i,j)]=kk;hb[(i,j)]=bb
Phi,Phik,Phib=nf('Phi')   # isotropic-mode amplitude (used only in iso mode)
af=[];ak=[];ab=[]
for i in range(3):
    f,kk,bb=nf(f'a{i+1}');af.append(f);ak.append(kk);ab.append(bb)
chi,chik,chib=nf('chi'); rho,Rk,Rb=nf('rho'); a0f0,a0k,a0b=nf('a0p')
KB,K2,Q0,JY=sp.symbols('K_B K_2 Q_0 J_Y',real=True); LAM=sp.S(0)   # module symbolic params
_GEOM={}   # cache: mode -> param-symbolic L2dc (built once, the expensive step)

def te(e):
    e=sp.expand(e);out=0
    for i in range(3):
        ci=e.coeff(eps,i)
        for j in range(3): out+=ci.coeff(wb,j)*eps**i*wb**j
    return out
def wtr(e):
    e=sp.expand(e);return sum(e.coeff(wb,n)*wb**n for n in range(3))

def build(mode):
    if mode in _GEOM: return _GEOM[mode]
    ww=w1**2+w2**2+w3**2;S0=1+wb**2*ww/2
    Aup_bg=sp.Matrix([S0,wb*w1,wb*w2,wb*w3]);Adn_bg=eta*Aup_bg;dphi_bg=-Q0*Adn_bg
    # metric perturbation
    H=sp.zeros(4,4);H[0,0]=-2*Psi
    for i in range(3): H[0,i+1]=Bf[i];H[i+1,0]=Bf[i]
    if mode=='iso':
        for i in range(1,4): H[i,i]=-2*Phi
    else:
        for i in range(1,4):
            for j in range(1,4): H[i,j]=hh[(i,j)]
    gd=sp.Matrix(4,4,lambda m,n:eta[m,n]+eps*H[m,n])
    Hup=eta*H*eta
    gu=sp.Matrix(4,4,lambda a,b:(eta-eps*Hup+eps**2*(Hup*H*eta))[a,b])
    trH=sum(eta[m,n]*H[m,n] for m in range(4) for n in range(4))
    HH=sum(Hup[m,n]*H[m,n] for m in range(4) for n in range(4))
    sqg=1+eps*trH/2+eps**2*(trH**2/8-HH/4)
    # ---- Fierz-Pauli EH: L_EH = (1/2) h^{mn} G^(1)_{mn}, G^(1)=R^(1)-1/2 eta R^(1) ----
    def R1(m,n):
        t1=sum(eta[a,b]*d(d(H[a,n],b),m) for a in range(4) for b in range(4))
        t2=sum(eta[a,b]*d(d(H[a,m],b),n) for a in range(4) for b in range(4))
        t3=d(d(trH,m),n)
        t4=sum(eta[a,b]*d(d(H[m,n],a),b) for a in range(4) for b in range(4))
        return sp.Rational(1,2)*(t1+t2-t3-t4)
    R1m=sp.Matrix(4,4,lambda m,n:R1(m,n))
    R1sc=sum(eta[m,n]*R1m[m,n] for m in range(4) for n in range(4))
    G1=sp.Matrix(4,4,lambda m,n:R1m[m,n]-sp.Rational(1,2)*eta[m,n]*R1sc)
    # sign fixed: full-Ricci sqrt(-g)R|_eps^2 == -(1/2) h.G^(1) (verified: Ricci/FP EOM ratio = -1)
    L_EH=-sp.Rational(1,2)*sum(Hup[m,n]*G1[m,n] for m in range(4) for n in range(4))
    # ---- aether unit constraint ----
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
    # Christoffels (for J only) -- truncated, cheap
    gdT=sp.Matrix(4,4,lambda m,n:te(gd[m,n]));guT=sp.Matrix(4,4,lambda m,n:te(gu[m,n]))
    AupT=sp.Matrix(4,1,lambda i,j:te(Aup[i]));dphiT=sp.Matrix(4,1,lambda i,j:te(dphi[i]))
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
    dQ=Qc-Q0;Kq=-2*LAM+K2*te(dQ**2)
    def grade(e):
        e=sp.expand(e);return [wtr(e.coeff(eps,n)) for n in range(3)]
    gF2=grade(F2);gJ=grade(Jdphi);gY=grade(Yc);gK=grade(Kq);gsq=grade(sqg)
    # dark Lagrangian at O(eps^2) (with sqrt(-g)); EH added separately via L_EH
    darkS=[-(2*LAM if n==0 else 0)-(KB/2)*gF2[n]+2*(2-KB)*gJ[n]-(2-KB)*gY[n]-gK[n] for n in range(3)]
    L2_dark=wtr(sum(gsq[a]*darkS[2-a] for a in range(3)))-(2-KB)*JY*gY[2]
    L2=sp.expand(wtr(te(L_EH))+L2_dark-16*sp.pi*wtr(rho*(-H[0,0]/2)))
    # diagonal ket-bra
    pol=sp.Poly(L2,Es,Eis);L2dc=0
    for mon,cc in zip(pol.monoms(),pol.coeffs()):
        if mon[0]==mon[1]: L2dc+=cc*(Es*Eis)**mon[0]
    L2dc=L2dc.subs(Es*Eis,1)
    _GEOM[mode]=sp.expand(L2dc.subs({ky:0,kz:0,kx:1}))
    return _GEOM[mode]

def solve(mode,KBv,K2v,Q0v,JYv):
    L2dc=sp.expand(build(mode).subs({KB:sp.nsimplify(KBv),K2:sp.nsimplify(K2v),
                                     Q0:sp.nsimplify(Q0v),JY:sp.nsimplify(JYv)}))
    if mode=='iso':
        GAUGE={Bk[0]:0,Bb[0]:0}
        BRAS=[Psib,Phib,Bb[1],Bb[2],ab[0],ab[1],ab[2],chib]
        KETS=[Psik,Phik,Bk[1],Bk[2],ak[0],ak[1],ak[2],chik]
        VZ={Bk[1]:0,Bk[2]:0,ak[1]:0,ak[2]:0}
        su=[Psik,Phik,ak[0],chik]; sb=[Psib,Phib,ab[0],chib]
    else:
        GAUGE={Bk[0]:0,Bb[0]:0,hk[(1,1)]:0,hb[(1,1)]:0,hk[(1,2)]:0,hb[(1,2)]:0,hk[(1,3)]:0,hb[(1,3)]:0}
        BRAS=[Psib,Bb[1],Bb[2],hb[(2,2)],hb[(3,3)],hb[(2,3)],ab[0],ab[1],ab[2],chib]
        KETS=[Psik,Bk[1],Bk[2],hk[(2,2)],hk[(3,3)],hk[(2,3)],ak[0],ak[1],ak[2],chik]
        VZ={Bk[1]:0,Bk[2]:0,ak[1]:0,ak[2]:0,hk[(2,3)]:0}
        su=[Psik,hk[(2,2)],hk[(3,3)],ak[0],chik]; sb=[Psib,hb[(2,2)],hb[(3,3)],ab[0],chib]
    L2dc=sp.expand(L2dc.subs(GAUGE))
    eqf={A:sp.expand(sp.diff(L2dc,A)) for A in BRAS}
    def lin(eqs,unk):
        M,b=sp.linear_eq_to_matrix(eqs,unk);s=list(sp.linsolve((M,b),unk))
        return dict(zip(unk,s[0])) if s else None
    e0=[sp.expand(eqf[A].coeff(wb,0).subs(VZ)) for A in sb]
    s0s=lin(e0,su)
    if s0s is None: return ('static-fail',)
    zero_extra={k:sp.S(0) for k in ([Bk[1],Bk[2],ak[1],ak[2]]+([] if mode=='iso' else [hk[(2,3)]]))}
    s0={**s0s,**zero_extra}
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
    return ('ok',complex(a1),complex(a2p),complex(a2l))

if __name__=='__main__':
    P("="*70+"\nISO validation (must give alpha_1 = -4 K_B):");
    for kbv in [0.05,0.3]:
        r=solve('iso',kbv,10.0,0.2,1.0)
        if r[0]=='ok':
            P(f"  K_B={kbv}: alpha_1={r[1].real:+.5f}  (target {-4*kbv:+.3f})  a2p={r[2].real:.4g} a2l={r[3].real:.4g}")
        else: P(f"  K_B={kbv}: {r[0]}")
    P(f"  [iso time {time.time()-T0:.1f}s]")
    P("="*70+"\nANISO grid  (alpha_1, alpha_2 perp/par, [D2] agreement):")
    P(f"{'K_B':>5}{'K2':>7}{'Q0':>5}{'JY':>4} | {'a1':>9} | {'a2_perp':>12}{'a2_par':>12}  D2")
    for kbv,k2v,q0v,jyv in itertools.product([0.05,0.3],[10.0,300.0],[0.2,0.9],[1.0,2.0]):
        r=solve('aniso',kbv,k2v,q0v,jyv)
        if r[0]!='ok': P(f"{kbv:5}{k2v:7}{q0v:5}{jyv:4} | {r[0]}"); continue
        _,a1,a2p,a2l=r; dd=abs(a2p-a2l)
        P(f"{kbv:5}{k2v:7}{q0v:5}{jyv:4} | {a1.real:+9.5f} | {a2p.real:12.6g}{a2l.real:12.6g}  {'OK' if dd<1e-6 else f'{dd:.0e}'}")
    P(f"[total {time.time()-T0:.1f}s]")
