#!/usr/bin/env python3
"""Diagnostics: (1) verify the spherical strain operators on analytic displacement fields;
(2) with radial-only K_t(r), check the beta=0 FEM reproduces J=rho_ph (validation);
(3) see how much J actually changes with beta (is w=1 real or artifact?)."""
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import spsolve, lsmr
G=6.674e-11; Msun=1.989e30; AU=1.496e11
Z=np.sqrt(32*np.pi/3); yc=Z/2.0
def nu(y): return np.sqrt(1.0+1.0/np.maximum(y,1e-30))
kappa=1.0/((nu(yc)-1.0)*yc)
def _tan(y):
    dy=1e-5*max(y,1e-3)
    eps=lambda yy: kappa*(nu(yy)-1.0)*yy; sig=lambda yy: yy/yc
    return (sig(y+dy)-sig(y-dy))/(eps(y+dy)-eps(y-dy))
_deep=_tan(0.01)
def S_of(y): return _tan(max(y,1e-6))/_deep

def deriv1d(x):
    n=len(x); rows=[];cols=[];vals=[]
    for i in range(n):
        if i==0: h=x[1]-x[0]; rows+=[0,0];cols+=[0,1];vals+=[-1/h,1/h]
        elif i==n-1: h=x[-1]-x[-2]; rows+=[n-1,n-1];cols+=[n-2,n-1];vals+=[-1/h,1/h]
        else:
            hm=x[i]-x[i-1];hp=x[i+1]-x[i]
            rows+=[i,i,i];cols+=[i-1,i,i+1]
            vals+=[-hp/(hm*(hm+hp)),(hp-hm)/(hm*hp),hm/(hp*(hm+hp))]
    return sp.csr_matrix((vals,(rows,cols)),shape=(n,n))

def build_ops(r,th):
    NRr=len(r);NTt=len(th);N=NRr*NTt
    R,TH=np.meshgrid(r,th,indexing='ij');ST=np.sin(TH);CT=np.cos(TH);COT=CT/ST
    Dr1=deriv1d(r);Dt1=deriv1d(th)
    Ir=sp.identity(NRr);It=sp.identity(NTt)
    Dr=sp.kron(Dr1,It,format='csr');Dt=sp.kron(Ir,Dt1,format='csr')
    rinv=sp.diags((1.0/R).ravel());cotr=sp.diags((COT/R).ravel())
    RiDt=rinv@Dt
    Zc=sp.csr_matrix((N,N))
    H2=lambda a,b: sp.hstack([a,b],format='csr')
    Err=H2(Dr,Zc); Ethth=H2(rinv,RiDt); Ephph=H2(rinv,cotr)
    Erth=H2(0.5*RiDt,0.5*(Dr-rinv)); Jop=Err+Ethth+Ephph
    return dict(N=N,NRr=NRr,NTt=NTt,R=R,TH=TH,ST=ST,CT=CT,Dr=Dr,Dt=Dt,rinv=rinv,RiDt=RiDt,
                Err=Err,Ethth=Ethth,Ephph=Ephph,Erth=Erth,Jop=Jop)

# ---------- (1) operator self-tests ----------
print("[1] operator self-tests (spherical strain on analytic u):")
r=np.linspace(1.0,2.0,40); th=np.linspace(0.05,np.pi-0.05,40)
O=build_ops(r,th); R=O['R'];TH=O['TH'];CT=O['CT'];ST=O['ST']
# (a) uniform z-translation: u_r=cos th, u_th=-sin th  -> strain=0
ur=CT.ravel(); ut=-ST.ravel(); x=np.concatenate([ur,ut])
J=O['Jop']@x; erth=O['Erth']@x
print(f"    uniform-z translation: max|J|={np.abs(J).max():.2e} max|e_rth|={np.abs(erth).max():.2e} (expect ~0)")
# (b) radial homothety u_r=r, u_th=0 -> J=div=3, deviatoric=0
ur=R.ravel(); ut=0*ur; x=np.concatenate([ur,ut])
J=O['Jop']@x
dev=(O['Err']@x)**2+(O['Ethth']@x)**2+(O['Ephph']@x)**2+2*(O['Erth']@x)**2-J**2/3
# interior only (avoid one-sided edges)
NRr,NTt=O['NRr'],O['NTt']; Jm=J.reshape(NRr,NTt)[2:-2,2:-2]; dm=dev.reshape(NRr,NTt)[2:-2,2:-2]
print(f"    homothety u_r=r: mean J={Jm.mean():.4f} (expect 3.0), max|dev|={np.abs(dm).max():.2e} (expect ~0)")
# (c) u_r=r*P2? check J for u_r=f(r): J=f'+2f/r ; take u_r=r^2 -> J=2r+2r=4r
ur=(R**2).ravel(); ut=0*ur; x=np.concatenate([ur,ut]); J=O['Jop']@x
Jm=J.reshape(NRr,NTt)[2:-2,2:-2]; expect=4*R[2:-2,2:-2]
print(f"    u_r=r^2: J vs 4r rel-err max={np.abs(Jm-expect).max()/np.abs(expect).max():.2e}")

# ---------- (2)+(3) FEM with radial-only K_t, validation + beta sensitivity ----------
print("\n[2] radial-only K_t(r): beta=0 reproduces J=rho_ph?  [3] does J change with beta?")
a0=9.36e-11; gx=2.2; gext=gx*a0
NR,NT=150,64
r=np.logspace(np.log10(5*AU),np.log10(5e5*AU),NR); th=np.linspace(0.03,np.pi-0.03,NT)
O=build_ops(r,th); N=O['N']; NRr,NTt=O['NRr'],O['NTt']
R=O['R'];TH=O['TH'];ST=O['ST'];CT=O['CT']
# rho_ph (committed def)
gr=G*Msun/R**2+gext*CT; gth=-gext*ST; gmag=np.sqrt(gr**2+gth**2); f=nu(gmag/a0)-1.0
Ar=f*gr; Ath=f*gth
d_r=np.gradient(R**2*Ar,r,axis=0)/R**2; d_t=np.gradient(ST*Ath,th,axis=1)/(R*ST)
rho_ph=(d_r+d_t)/(4*np.pi*G)
# radial-only K_t(r) from Sun's monopole background y0(r)=(GM/r^2)/a0
y0=(G*Msun/r**2)/a0; Kt_r=(a0**2/(16*np.pi*G))*np.array([S_of(v) for v in y0])
Keff=a0**2/(16*np.pi*G)
Kt=np.repeat(Kt_r[:,None],NTt,axis=1)   # radial, broadcast in theta
def project(field2d):
    P2=0.5*(3*CT**2-1.0); dr=np.gradient(r);dth=np.gradient(th)
    W=2*np.pi*R**2*ST*dr[:,None]*dth[None,:]
    return abs(np.sum(field2d*P2/R**3*W))
I2_scalar=project(rho_ph)
# weights, driving chi=K_t(r)*rho_ph
dr=np.gradient(r);dth=np.gradient(th); dV=2*np.pi*R**2*ST*dr[:,None]*dth[None,:]
Wd=sp.diags(dV.ravel()); KtWd=sp.diags((Kt*dV).ravel())
chi=(Kt*rho_ph).ravel()
f_r=-(O['Dr']@chi); f_th=-(O['RiDt']@chi)
b=np.concatenate([f_r*dV.ravel(), f_th*dV.ravel()])
Jop=O['Jop']
H_bulk=Jop.T@KtWd@Jop
H_sh=(O['Err'].T@Wd@O['Err']+O['Ethth'].T@Wd@O['Ethth']+O['Ephph'].T@Wd@O['Ephph']
      +2*(O['Erth'].T@Wd@O['Erth'])-(1/3)*(Jop.T@Wd@Jop))
# constraints
def gidx(i,j,c): return c*N+i*NTt+j
fixed=set()
for j in range(NTt): fixed.add(gidx(NRr-1,j,0)); fixed.add(gidx(NRr-1,j,1))
for i in range(NRr): fixed.add(gidx(i,0,1)); fixed.add(gidx(i,NTt-1,1))
fixed=np.array(sorted(fixed)); free=np.setdiff1d(np.arange(2*N),fixed)
def solve(beta,use_lsmr=False):
    mu=3*beta*Keff
    H=(H_bulk+2*mu*H_sh).tocsr()
    H=H+ (1e-10*Keff)*sp.diags(np.concatenate([dV.ravel(),dV.ravel()]))
    Hff=H[free][:,free]; bf=b[free]
    if use_lsmr:
        uf=lsmr(Hff.tocsr(),bf,atol=1e-10,btol=1e-10,maxiter=20000)[0]
    else:
        uf=spsolve(Hff.tocsc(),bf)
    u=np.zeros(2*N);u[free]=uf
    return (Jop@u).reshape(NRr,NTt), u
J0,u0=solve(0.0,use_lsmr=True)
print(f"    I2_scalar(rho_ph) on grid = {I2_scalar:.4e}")
print(f"    beta=0: project(J)={project(J0):.4e}  ratio to scalar={project(J0)/I2_scalar:.3f}")
for beta in (0.33,0.6,0.95,2.0):
    Jb,ub=solve(beta)
    dJrel=np.linalg.norm((Jb-J0))/np.linalg.norm(J0)
    print(f"    beta={beta:4.2f}: project(J)={project(Jb):.4e}  w={project(Jb)/project(J0):.4f}  ||dJ||/||J0||={dJrel:.3e}")
print("exit 0")
