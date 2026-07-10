#!/usr/bin/env python3
"""Decisive machinery test: does J respond to the shear modulus at all?
Homogeneous medium (K const, mu const), gradient body force f=-grad(chi) with an ell=2 chi,
spherical shell, Dirichlet outer + free inner + axis u_th=0. Compare:
 (i)  project(J) vs mu       -> must DECREASE with mu if the P-wave modulus K+4/3 mu governs J
 (ii) the solenoidal fraction of u (curl) vs mu -> how much relief the geometry allows.
Also print the FULL-field change ||J(mu2)-J(mu1)|| to catch a stuck solver."""
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import spsolve
AU=1.496e11
def deriv1d(x):
    n=len(x);rows=[];cols=[];vals=[]
    for i in range(n):
        if i==0:h=x[1]-x[0];rows+=[0,0];cols+=[0,1];vals+=[-1/h,1/h]
        elif i==n-1:h=x[-1]-x[-2];rows+=[n-1,n-1];cols+=[n-2,n-1];vals+=[-1/h,1/h]
        else:
            hm=x[i]-x[i-1];hp=x[i+1]-x[i];rows+=[i,i,i];cols+=[i-1,i,i+1]
            vals+=[-hp/(hm*(hm+hp)),(hp-hm)/(hm*hp),hm/(hp*(hm+hp))]
    return sp.csr_matrix((vals,(rows,cols)),shape=(n,n))
NR,NT=140,64
r=np.logspace(np.log10(5*AU),np.log10(5e5*AU),NR); th=np.linspace(0.03,np.pi-0.03,NT)
NRr,NTt=len(r),len(th); N=NRr*NTt
R,TH=np.meshgrid(r,th,indexing='ij');ST=np.sin(TH);CT=np.cos(TH);COT=CT/ST
Dr1=deriv1d(r);Dt1=deriv1d(th);Ir=sp.identity(NRr);It=sp.identity(NTt)
Dr=sp.kron(Dr1,It,format='csr');Dt=sp.kron(Ir,Dt1,format='csr')
rinv=sp.diags((1.0/R).ravel());cotr=sp.diags((COT/R).ravel());RiDt=rinv@Dt
Zc=sp.csr_matrix((N,N));H2=lambda a,b:sp.hstack([a,b],format='csr')
Err=H2(Dr,Zc);Ethth=H2(rinv,RiDt);Ephph=H2(rinv,cotr)
Erth=H2(0.5*RiDt,0.5*(Dr-rinv));Jop=Err+Ethth+Ephph
# curl (phi-component of curl u) for axisymmetric u=(u_r,u_th):
# (curl u)_phi = (1/r) d_r(r u_th) - (1/r) d_th u_r = d_r u_th + u_th/r - (1/r) d_th u_r
Curl=H2(-RiDt, Dr+rinv)
dr=np.gradient(r);dth=np.gradient(th);dV=2*np.pi*R**2*ST*dr[:,None]*dth[None,:]
Wd=sp.diags(dV.ravel())
def project(F):
    P2=0.5*(3*CT**2-1);W=2*np.pi*R**2*ST*dr[:,None]*dth[None,:]
    return abs(np.sum(F*P2/R**3*W))
# ell=2 driving potential chi (constant modulus scenario): chi = A * P2(cos th) * shape(r)
shape=np.exp(-((np.log(r/(3e3*AU)))**2)/2.0)   # bump around 3000 AU (the sourcing shell)
chi=(0.5*(3*CT**2-1)*shape[:,None])
K=1.0   # constant bulk modulus (units arbitrary)
Kt=K*np.ones_like(R)
KtWd=sp.diags((Kt*dV).ravel())
f_r=-(Dr@chi.ravel());f_th=-(RiDt@chi.ravel())
b=np.concatenate([f_r*dV.ravel(),f_th*dV.ravel()])
H_bulk=Jop.T@KtWd@Jop
H_sh=(Err.T@Wd@Err+Ethth.T@Wd@Ethth+Ephph.T@Wd@Ephph+2*(Erth.T@Wd@Erth)-(1/3)*(Jop.T@Wd@Jop))
def gidx(i,j,c):return c*N+i*NTt+j
fixed=set()
for j in range(NTt):fixed.add(gidx(NRr-1,j,0));fixed.add(gidx(NRr-1,j,1))
for i in range(NRr):fixed.add(gidx(i,0,1));fixed.add(gidx(i,NTt-1,1))
fixed=np.array(sorted(fixed));free=np.setdiff1d(np.arange(2*N),fixed)
def solve(mu):
    H=(H_bulk+2*mu*H_sh).tocsr()+1e-12*sp.diags(np.concatenate([dV.ravel(),dV.ravel()]))
    uf=spsolve(H[free][:,free].tocsc(),b[free]);u=np.zeros(2*N);u[free]=uf
    J=(Jop@u).reshape(NRr,NTt);curl=(Curl@u).reshape(NRr,NTt)
    return J,curl,u
print("constant-K test (K=1): P-wave theory J ~ chi/(K+4/3 mu) if response irrotational")
print(f"{'mu/K':>7} {'project(J)':>12} {'w=J/J(0)':>10} {'||curl||/||J||':>14} {'K/(K+4/3mu)':>12}")
J0,c0,u0=solve(1e-6)
p0=project(J0)
for mu in (1e-6,0.33,1.0,1.8,3.0,6.0):
    J,curl,u=solve(mu)
    solr=np.linalg.norm(curl*R.ravel().reshape(NRr,NTt))/max(np.linalg.norm(J),1e-30) if False else np.linalg.norm(curl)/max(np.linalg.norm(J),1e-30)
    pw=1.0/(1.0+ (4.0/3.0)*mu)
    print(f"{mu:>7.2f} {project(J):>12.4e} {project(J)/p0:>10.4f} {np.linalg.norm(curl)/np.linalg.norm(J):>14.3e} {pw:>12.4f}")
# also field-level change to catch a stuck solver:
Ja,_,_=solve(0.33);Jb,_,_=solve(6.0)
print(f"\nfield change J(mu=0.33)->J(mu=6): ||dJ||/||J|| = {np.linalg.norm(Jb-Ja)/np.linalg.norm(Ja):.3e}")
print("exit 0")
