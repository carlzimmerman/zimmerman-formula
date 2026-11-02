#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""ROUTE 2 v2: correct gauge. metric h_ij=-2Phi dij + s_ij (s traceless),
gauge-fix h01=0, h12=0, h13=0, s11=0  (retains spatial-trace Newtonian constraint).
Physical: Psi(h00=-2Psi), Phi, B2(h02),B3(h03), s22, s23, a1,a2,a3, chi.  k=(1,0,0)."""
import sympy as sp, time, pickle
T0=time.time(); P=lambda *a: print(*a,flush=True)
import sys; SC=sys.argv[1]
t,x1,x2,x3=sp.symbols('t x1 x2 x3', real=True)
eps,wb=sp.symbols('eps w_b', positive=True)
KB,Q0,K2,JY=sp.symbols('K_B Q_0 K_2 J_Y', real=True)
w1,w2,w3=sp.symbols('w1 w2 w3', real=True)
GT,LAM=sp.symbols('G_t Lambda', real=True)
eta=sp.diag(-1,1,1,1); I=sp.I
def tr(e,p,n):
    e=sp.expand(e); return sum(e.coeff(p,k)*p**k for k in range(n+1))
ww=w1**2+w2**2+w3**2; S0=1+wb**2*ww/2
Aup_bg=sp.Matrix([S0,wb*w1,wb*w2,wb*w3]); Adn_bg=eta*Aup_bg
dphi_bg=-Q0*Adn_bg
Es,Eis=sp.symbols('E_s E_is'); kx=sp.symbols('k_x', real=True); kv=[0,kx,0,0]
def nf(tag): ket=sp.Symbol(tag+'k'); bra=sp.Symbol(tag+'b'); return ket*Es+bra*Eis,ket,bra
def d(f,mu): return sp.diff(f,Es)*(I*kv[mu]*Es)+sp.diff(f,Eis)*(-I*kv[mu]*Eis)
Psi,Psik,Psib=nf('Psi'); Phi,Phik,Phib=nf('Phi')
B2f,B2k,B2b=nf('B2'); B3f,B3k,B3b=nf('B3')
s22,s22k,s22b=nf('s22'); s23,s23k,s23b=nf('s23')
a1f,a1k,a1b=nf('a1'); a2f,a2k,a2b=nf('a2'); a3f,a3k,a3b=nf('a3')
chi,chik,chib=nf('chi'); rho,Rk,Rb=nf('rho'); a0f,a0k,a0b=nf('a0p')
H=sp.zeros(4,4)
H[0,0]=-2*Psi
H[0,2]=B2f; H[2,0]=B2f; H[0,3]=B3f; H[3,0]=B3f
H[1,1]=-2*Phi
H[2,2]=-2*Phi+s22; H[3,3]=-2*Phi-s22
H[2,3]=s23; H[3,2]=s23
gd=sp.Matrix(4,4,lambda m,n: eta[m,n]+eps*H[m,n])
Hup=eta*H*eta
gu=sp.Matrix(4,4,lambda i,j:(eta-eps*Hup+eps**2*(Hup*H*eta))[i,j])
trH=sum(eta[m,n]*H[m,n] for m in range(4) for n in range(4))
HH=sum(Hup[m,n]*H[m,n] for m in range(4) for n in range(4))
sqg=1+eps*trH/2+eps**2*(trH**2/8-HH/4)
Adn=sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
Aup=sp.Matrix(4,1,lambda i,j: sum(gu[i,k]*Adn[k] for k in range(4)))
C1=sp.expand(sum(Aup[i]*Adn[i] for i in range(4))+1).coeff(eps,1)
solA=sp.solve([sp.expand(C1).coeff(Es,1),sp.expand(C1).coeff(Eis,1)],[a0k,a0b],dict=True)[0]
solA={k:sp.expand(sp.series(v,wb,0,3).removeO()) for k,v in solA.items()}
a0f=a0f.subs(solA)
Adn=sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
Aup=sp.Matrix(4,1,lambda i,j: sum(gu[i,k]*Adn[k] for k in range(4)))
# AS3 repair, unit constraint at O(eps^2): solve b0 in A_0 -> A_0 - eps^2 b0
b0s=sp.Symbol('b0s')
Adn2=sp.Matrix([Adn[0]-eps**2*b0s,Adn[1],Adn[2],Adn[3]])
Aup2=sp.Matrix(4,1,lambda i,j: sum(gu[i,k]*Adn2[k] for k in range(4)))
C2=sp.expand(sum(Aup2[i]*Adn2[i] for i in range(4))+1).coeff(eps,2)
b0v=sp.solve(C2,b0s)[0]
b0v=sp.expand(sp.series(b0v,wb,0,3).removeO())
Adn=sp.Matrix([Adn[0]-eps**2*b0v,Adn[1],Adn[2],Adn[3]])
Aup=sp.Matrix(4,1,lambda i,j: sum(gu[i,k]*Adn[k] for k in range(4)))
P(f"[S1] constraint solved ({time.time()-T0:.1f}s)")
dphi=sp.Matrix([dphi_bg[m]+eps*d(chi,m) for m in range(4)])
def te(e):
    e=sp.expand(e); out=0
    for i in range(3):
        ci=e.coeff(eps,i)
        for j in range(3): out+=ci.coeff(wb,j)*eps**i*wb**j
    return out
def wtrunc(e):
    e=sp.expand(e); return sum(e.coeff(wb,n)*wb**n for n in range(3))
guT=sp.Matrix(4,4,lambda m,n: te(gu[m,n])); AupT=sp.Matrix(4,1,lambda i,j: te(Aup[i]))
Gam=[[[sp.Rational(1,2)*sum(gu[r,s]*(d(gd[s,n],m)+d(gd[s,m],n)-d(gd[m,n],s)) for s in range(4))
       for n in range(4)] for m in range(4)] for r in range(4)]
GamT=[[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
dphiT=sp.Matrix(4,1,lambda i,j: te(dphi[i]))
Fmn=sp.Matrix(4,4,lambda m,n: sp.expand(d(Adn[n],m)-d(Adn[m],n)))
F1=sp.Matrix(4,4,lambda m,n: Fmn[m,n].coeff(eps,1))
F2=eps**2*sum(F1[m,n]*F1[a,b]*eta[m,a]*eta[n,b] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
Jup=[te(sum(AupT[nu]*(d(AupT[al],nu)+sum(GamT[al][nu][r]*AupT[r] for r in range(4))) for nu in range(4))) for al in range(4)]
Jdphi=te(sum(Jup[m]*dphiT[m] for m in range(4)))
Qc=te(sum(AupT[m]*dphiT[m] for m in range(4)))
Yc=te(sum((guT[m,n]+AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
dQ=Qc-Q0; Kq=-2*LAM+K2*te(dQ**2)
P(f"    dark scalars ({time.time()-T0:.1f}s)")
def ric(a,b):
    o=0
    for m in range(4):
        o+=d(Gam[m][b][a],m)-d(Gam[m][m][a],b)
        for l in range(4): o+=Gam[m][m][l]*Gam[l][b][a]-Gam[m][b][l]*Gam[l][m][a]
    return o
Rsc=te(sum(guT[m,n]*ric(m,n) for m in range(4) for n in range(4)))
P(f"    Ricci ({time.time()-T0:.1f}s)")
def grade(e):
    e=sp.expand(e); return [wtrunc(e.coeff(eps,n)) for n in range(3)]
gF2=grade(F2); gJ=grade(Jdphi); gY=grade(Yc); gK=grade(Kq); gsq=grade(sqg); gR=grade(Rsc)
gS=[gR[n]-(2*LAM if n==0 else 0)-(KB/2)*gF2[n]+2*(2-KB)*gJ[n]-(2-KB)*gY[n]-gK[n] for n in range(3)]
L2_grav=wtrunc(sum(gsq[a]*gS[2-a] for a in range(3)))-(2-KB)*JY*gY[2]
L2_matt=-16*sp.pi*GT*wtrunc(rho*(-H[0,0]/2))
L2=sp.expand(L2_grav+L2_matt)
def DC(e):
    e=sp.expand(e); pol=sp.Poly(e,Es,Eis); out=0
    for mon,c in zip(pol.monoms(),pol.coeffs()):
        if mon[0]==mon[1]: out+=c*(Es*Eis)**mon[0]
    return out.subs(Es*Eis,1) if out!=0 else out
L2dc=DC(L2)
pickle.dump(L2dc, open(SC+'L2dc_v2.pkl','wb'))
P(f"    L2dc built+cached: {len(sp.Add.make_args(L2dc))} terms ({time.time()-T0:.1f}s)")

