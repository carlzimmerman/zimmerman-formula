#!/usr/bin/env python3
r"""ROUTE 2 DECISIVE -- STEP 3: evaluate the MOND-sector khronon source with EXPLICIT F,
on a VACUUM potential, to decide OUTCOME A vs B.

Recompute K0,K1,X0,X1 (cheap), build S_T with F(X)=-2 sqrt(X)+2 ln(1+sqrt(X)) EXPLICIT,
then test whether S_T vanishes on a vacuum profile Phi=-M/r (lap Phi = 0).
c=1, Psi=0, a->1 locally (H kept).  Also keep leading order in the potential Phi (weak field).
"""
import sympy as sp
t, r, th = sp.symbols('t r theta', real=True)
H, Z, eps, M = sp.symbols('H Z epsilon M', positive=True)
Phi = sp.Function('Phi')(r); a = sp.Function('a')(t); psi = sp.Function('psi')(r, t)
XX = [t, r, th, sp.Symbol('ph')]
N2 = 1 + 2*Phi
g = sp.diag(-N2, a**2, a**2*r**2, a**2*r**2*sp.sin(th)**2); gi = g.inv()
def christoffel(g, gi, X):
    n=len(X); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                s=sum(gi[l,p]*(sp.diff(g[p,m],X[k])+sp.diff(g[p,k],X[m])-sp.diff(g[m,k],X[p])) for p in range(n))
                G[l][m][k]=sp.together(s/2)
    return G
Gam=christoffel(g,gi,XX); sqrtmg=sp.sqrt(-g.det())
T=t+eps*psi; wl=[sp.diff(T,XX[i]) for i in range(4)]
Ncal=sp.sqrt(-sum(gi[m,n]*wl[m]*wl[n] for m in range(4) for n in range(4)))
u_l=[-wl[m]/Ncal for m in range(4)]; u_u=[sum(gi[m,n]*u_l[n] for n in range(4)) for m in range(4)]
K=sum(sp.diff(sqrtmg*u_u[m],XX[m]) for m in range(4))/sqrtmg
nab=[[sp.diff(u_l[mu],XX[nu])-sum(Gam[l][nu][mu]*u_l[l] for l in range(4)) for mu in range(4)] for nu in range(4)]
a_l=[sum(u_u[nu]*nab[nu][mu] for nu in range(4)) for mu in range(4)]
a2=sum(gi[m,n]*a_l[m]*a_l[n] for m in range(4) for n in range(4))
adot=sp.Derivative(a,t); sub_H=lambda e:e.subs(adot,H*a)
K0=sub_H(K.subs(eps,0)); K1=sub_H(sp.diff(K,eps).subs(eps,0))
a2_0=sub_H(a2.subs(eps,0)); a2_1=sub_H(sp.diff(a2,eps).subs(eps,0))
X0=Z**2/K0**2*a2_0; X1=Z**2*(a2_1/K0**2-2*a2_0*K1/K0**3)
sX=sp.sqrt(X0); Fexpr=-2*sX+2*sp.log(1+sX)
Fp=sp.diff(Fexpr,Phi)  # not used directly
# L1 = -(2/Z^2)[2 K0 K1 F(X0) + K0^2 F'(X0) X1]; F'(X0)=dF/dX0
dF_dX0=sp.diff(Fexpr, X0) if False else None
# compute F'(X0) analytically: F'(X)=-1/(1+sqrt X)
Fprime = -1/(1+sX)
L1=-(2/Z**2)*(2*K0*K1*Fexpr + K0**2*Fprime*X1)
mu_meas=sp.sqrt(N2)*a**3*r**2
Ldens1=mu_meas*L1
pr=sp.Derivative(psi,r); prr=sp.Derivative(psi,r,2); pt=sp.Derivative(psi,t)
prt=sp.Derivative(psi,r,t); ptt=sp.Derivative(psi,t,2)
S_T=( sp.diff(Ldens1,psi)-sp.diff(sp.diff(Ldens1,pr),r)+sp.diff(sp.diff(Ldens1,prr),r,2)
      -sp.diff(sp.diff(Ldens1,pt),t)+sp.diff(sp.diff(Ldens1,ptt),t,2)
      +sp.diff(sp.diff(Ldens1,prt),r,t) )
S_T=sub_H(S_T)
zero={psi:0,pr:0,prr:0,pt:0,prt:0,ptt:0,sp.Derivative(psi,r,3):0,
      sp.Derivative(psi,r,2,t):0,sp.Derivative(psi,r,t,2):0,sp.Derivative(psi,t,3):0}
S_T=sub_H(S_T.subs(zero))
S_T_red=S_T/mu_meas
print("evaluating on vacuum Phi=-M/r ...", flush=True)
# VACUUM Newtonian profile, a=1
prof={Phi:-M/r}
def apply(e):
    e=e.subs(sp.Derivative(Phi,(r,3)), sp.diff(-M/r,r,3))
    e=e.subs(sp.Derivative(Phi,(r,2)), sp.diff(-M/r,r,2))
    e=e.subs(sp.Derivative(Phi,r), sp.diff(-M/r,r))
    e=e.subs(Phi,-M/r); e=e.subs(a,1)
    return e
S_vac=sp.simplify(apply(S_T_red))
print("\n===== S_T on vacuum Phi=-M/r (a=1) =====")
sp.pprint(S_vac)
print("\nIs it identically zero?", S_vac==0)
# Also test WEAK-FIELD leading (drop Phi in prefactors: keep only leading in potential)
# leading source: expand S_T_red to leading order in the potential amplitude
print("\n===== leading-in-potential form of S_T (general Phi) =====", flush=True)
# keep Phi-> small: substitute (2Phi+1)->1 in nonderivative slots by dropping Phi vs 1
S_lead=S_T_red
# expand and drop higher powers of Phi (bare, not derivatives) : series in a bookkeeping lam
lam=sp.symbols('lam',positive=True)
S_book=S_T_red.subs(Phi, lam*Phi)
S_book=sp.series(S_book, lam, 0, 2).removeO()  # keep O(lam^0)+O(lam^1)? source starts at some order
sp.pprint(sp.simplify(S_book))
with open('S_vac.txt','w') as f: f.write(str(S_vac))
print("\n[done]")
