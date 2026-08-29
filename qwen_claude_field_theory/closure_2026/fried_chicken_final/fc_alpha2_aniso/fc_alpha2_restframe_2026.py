#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_alpha2_restframe_2026.py  --  FC-AeST preferred-frame PPN alpha_1, alpha_2 (METHOD B, corrected).
================================================================================
STANDARD preferred-frame setup: AETHER AT REST (defines the preferred frame),
DUST SOURCE MOVING at velocity w.  This makes the dark+EH field operator
w-INDEPENDENT and the moving matter the SOLE w-source, so the standard PPN
extraction (with the GR gravitomagnetic baseline correctly present in the source)
applies -- fixing the two defects of the aether-boosted/source-rest version:
  * that version's H0-perp extraction returned the raw -4wU GR baseline (alpha_1=-8
    in the heavy limit) instead of the preferred-frame deviation;
  * the k-along-x gauge H01=0 discarded the a+b combination alpha_1 needs.

Full anisotropic spatial metric h_ij; unit constraint solved to O(eps^2)
(lambda eliminated via the proven -lam_bg*C2a term, lam_bg=(2-K_B)(1+J_Y)Q0^2);
kernel-blind (Y-coefficient (2-K_B)(1+J_Y), J_Y inert).

Moving dust: T^{mn}=rho u^m u^n, u^m=(1+w^2/2, w^i) (w = source velocity / preferred
frame).  Linear coupling (1/2)*16 pi G_t * rho * u^m u^n H_{mn}, which sources
H00 at O(w^0,w^2), H0i at O(w^1), H_ij at O(w^2) -- the standard PPN source.

Solve order by order in w (w-independent dark+EH operator, w-dependent source):
  w^0 static (gamma), w^1 (H0i -> alpha_1), w^2 (H00,Hij -> alpha_2).
Extraction: gauge-invariant, calibrated so GR/heavy limit gives alpha=0 and V1=-4K_B.
"""
import sympy as sp, time, os, pickle, sys

T0 = time.time(); P = lambda *a: print(*a, flush=True)
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, GT, JY = sp.symbols('K_B Q_0 K_2 G_t J_Y', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True); kv = [0, kx, ky, kz]
eta = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is'); Uh = sp.Symbol('U_hat')
ww = w1**2 + w2**2 + w3**2

def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b'); return ket*Es+bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)
def te(e):                       # truncate eps<=2 (dark operator is w-free; w only via matter)
    e = sp.expand(e); return sum(e.coeff(eps, n)*eps**n for n in range(3))

# amplitudes
Psi, Psik, Psib = nf('Psi')
Bf=[];Bk=[];Bb=[]
for i in range(3):
    f,kk,bb=nf(f'B{i+1}'); Bf.append(f);Bk.append(kk);Bb.append(bb)
hh={};hk={};hb={}
for (i,j) in [(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]:
    f,kk,bb=nf(f'h{i}{j}'); hh[(i,j)]=f;hh[(j,i)]=f;hk[(i,j)]=kk;hb[(i,j)]=bb
af=[];ak=[];ab=[]
for i in range(3):
    f,kk,bb=nf(f'a{i+1}'); af.append(f);ak.append(kk);ab.append(bb)
chi,chik,chib=nf('chi'); rho,Rk,Rb=nf('rho'); a0f0,a0k,a0b=nf('a0p')

ALL_KETS=[Psik,Bk[0],Bk[1],Bk[2],hk[(1,1)],hk[(2,2)],hk[(3,3)],hk[(1,2)],hk[(1,3)],hk[(2,3)],ak[0],ak[1],ak[2],chik]
ALL_BRAS=[Psib,Bb[0],Bb[1],Bb[2],hb[(1,1)],hb[(2,2)],hb[(3,3)],hb[(1,2)],hb[(1,3)],hb[(2,3)],ab[0],ab[1],ab[2],chib]

# ---- rest-aether background ----
Aup_bg = sp.Matrix([1,0,0,0]); Adn_bg = eta*Aup_bg; dphi_bg = -Q0*Adn_bg   # dphi_bg=(Q0,0,0,0)
assert sp.expand((Adn_bg.T*Aup_bg)[0]+1)==0
P(f"[A] rest-aether background A.A=-1, Q=Q0, Y=0  ({time.time()-T0:.1f}s)")

# ---- metric ----
H=sp.zeros(4,4); H[0,0]=-2*Psi
for i in range(3): H[0,i+1]=Bf[i];H[i+1,0]=Bf[i]
for i in range(1,4):
    for j in range(1,4): H[i,j]=hh[(i,j)]
gd=sp.Matrix(4,4,lambda m,n:eta[m,n]+eps*H[m,n])
Hup=eta*H*eta
gu=sp.Matrix(4,4,lambda a,b:(eta-eps*Hup+eps**2*(Hup*H*eta))[a,b])
trH=sum(eta[m,n]*H[m,n] for m in range(4) for n in range(4))
HH=sum(Hup[m,n]*H[m,n] for m in range(4) for n in range(4))
sqg=1+eps*trH/2+eps**2*(trH**2/8-HH/4)

# ---- unit constraint to O(eps^2) ----
Adn=sp.Matrix([Adn_bg[0]-eps*a0f0, Adn_bg[1]+eps*af[0], Adn_bg[2]+eps*af[1], Adn_bg[3]+eps*af[2]])
Aup=sp.Matrix(4,1,lambda i,j:sum(gu[i,k]*Adn[k] for k in range(4)))
C1=sp.expand(sum(Aup[i]*Adn[i] for i in range(4))+1).coeff(eps,1)
solA=sp.solve([sp.expand(C1).coeff(Es,1),sp.expand(C1).coeff(Eis,1)],[a0k,a0b],dict=True)[0]
a0_1=a0f0.subs(solA)
Adn=sp.Matrix([Adn_bg[0]-eps*a0_1, Adn_bg[1]+eps*af[0], Adn_bg[2]+eps*af[1], Adn_bg[3]+eps*af[2]])
Aup=sp.Matrix(4,1,lambda i,j:sum(gu[i,k]*Adn[k] for k in range(4)))
Cfull=sp.expand(sum(Aup[i]*Adn[i] for i in range(4))+1)
C2a=sp.expand(Cfull.coeff(eps,2))
lam_bg=(2-KB)*(1+JY)*Q0**2
assert sp.expand(sp.expand(sum(Aup[i]*Adn[i] for i in range(4))+1).coeff(eps,1))==0
P(f"[B] constraint O(eps) solved; lam_bg term ready  ({time.time()-T0:.1f}s)")

# ---- build dark+EH operator (w-free) + moving-source matter (w-dependent) ----
dphi=sp.Matrix([dphi_bg[m]+eps*d(chi,m) for m in range(4)])
_CACHE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'L2dc_restframe_cache.pkl')
if os.path.exists(_CACHE):
    L2dc=pickle.load(open(_CACHE,'rb')); P(f"[C] L2dc loaded from cache ({time.time()-T0:.1f}s)")
else:
    gdT=sp.Matrix(4,4,lambda m,n:te(gd[m,n])); guT=sp.Matrix(4,4,lambda m,n:te(gu[m,n]))
    AupT=sp.Matrix(4,1,lambda i,j:te(Aup[i])); dphiT=sp.Matrix(4,1,lambda i,j:te(dphi[i]))
    GamT=[[[ te(sp.Rational(1,2)*sum(guT[r,s]*(d(gdT[s,n],m)+d(gdT[s,m],n)-d(gdT[m,n],s)) for s in range(4)))
            for n in range(4)] for m in range(4)] for r in range(4)]
    P(f"    Christoffels ({time.time()-T0:.1f}s)")
    def ric(a,b):
        o=0
        for m in range(4):
            o+=d(GamT[m][b][a],m)-d(GamT[m][m][a],b)
            for l in range(4): o+=te(GamT[m][m][l]*GamT[l][b][a]-GamT[m][b][l]*GamT[l][m][a])
        return te(o)
    Rsc=te(sum(te(guT[m,n]*ric(m,n)) for m in range(4) for n in range(4)))
    P(f"    Ricci ({time.time()-T0:.1f}s)")
    Fmn=sp.Matrix(4,4,lambda m,n:sp.expand(d(Adn[n],m)-d(Adn[m],n)))
    F1=sp.Matrix(4,4,lambda m,n:Fmn[m,n].coeff(eps,1))
    F2=eps**2*sum(F1[m,n]*F1[a,b]*eta[m,a]*eta[n,b] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    mt=lambda a,b: te(sp.expand(a)*sp.expand(b))
    covA=[[ te(d(AupT[al],nu)+sum(mt(GamT[al][nu][r],AupT[r]) for r in range(4))) for nu in range(4)] for al in range(4)]
    Jup=[te(sum(mt(AupT[nu],covA[al][nu]) for nu in range(4))) for al in range(4)]
    Jdphi=te(sum(mt(Jup[m],dphiT[m]) for m in range(4)))
    Qc=te(sum(mt(AupT[m],dphiT[m]) for m in range(4)))
    dphi2=[[ mt(dphiT[m],dphiT[n]) for n in range(4)] for m in range(4)]
    Yc=te(sum(mt(guT[m,n]+mt(AupT[m],AupT[n]),dphi2[m][n]) for m in range(4) for n in range(4)))
    dQ=Qc-Q0; Kq=K2*te(dQ**2)
    P(f"    dark scalars ({time.time()-T0:.1f}s)")
    def grade(e): e=sp.expand(e); return [e.coeff(eps,n) for n in range(3)]
    gF2=grade(F2);gJ=grade(Jdphi);gY=grade(Yc);gK=grade(Kq);gsq=grade(sqg);gR=grade(Rsc)
    gS=[gR[n]-(KB/2)*gF2[n]+2*(2-KB)*gJ[n]-(2-KB)*gY[n]-gK[n] for n in range(3)]
    L2_darkEH=sum(gsq[a]*gS[2-a] for a in range(3)) - (2-KB)*JY*gY[2] - lam_bg*C2a
    # moving-source matter: (1/2)*16 pi Gt * rho * u^m u^n H_mn ; u^m=(1+wb^2 ww/2, wb w^i)
    u=sp.Matrix([1+wb**2*ww/2, wb*w1, wb*w2, wb*w3])
    uHu=sum(u[m]*u[n]*H[m,n] for m in range(4) for n in range(4))
    uHu=sum(sp.expand(uHu).coeff(wb,n)*wb**n for n in range(3))   # truncate wb<=2
    L2_matt=8*sp.pi*GT*rho*uHu
    L2=sp.expand(te(L2_darkEH)+L2_matt)
    P(f"    L2 built: {len(sp.Add.make_args(L2))} terms ({time.time()-T0:.1f}s)")
    pol=sp.Poly(L2,Es,Eis); out=0
    for mon,cc in zip(pol.monoms(),pol.coeffs()):
        if mon[0]==mon[1]: out+=cc*(Es*Eis)**mon[0]
    L2dc=out.subs(Es*Eis,1) if out!=0 else out
    pickle.dump(L2dc,open(_CACHE,'wb'))
    P(f"[C] L2dc cached: {len(sp.Add.make_args(sp.expand(L2dc)))} terms ({time.time()-T0:.1f}s)")

# ---- solver ----
def lin_solve(eqs,unk):
    M,b=sp.linear_eq_to_matrix(eqs,unk); s=list(sp.linsolve((M,b),unk)); return dict(zip(unk,s[0])) if s else None
