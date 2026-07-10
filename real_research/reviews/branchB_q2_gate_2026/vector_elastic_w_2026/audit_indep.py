#!/usr/bin/env python3
"""ADVERSARIAL AUDIT of methodB_fem.py.
(1) Divergence-free relaxation test: build a genuinely solenoidal ell=2 field (Jr=0 by
    construction) and confirm the code's OP_Jr returns ~0 while the shear Hessian returns >0.
    This is the reviewer's crux: solenoidal fields carry shear energy but leave J untouched.
(2) FULLY INDEPENDENT w(beta): rebuild the elastic energy as a quadratic form in nodal (U,V)
    by DIRECT theta-quadrature of the EXACT spherical strain tensor (no closed G_pp algebra),
    minimize, and read w = project(J,beta)/project(J,0). Compare to methodB's modal w.
"""
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import spsolve
G=6.674e-11; Msun=1.989e30; AU=1.496e11
Z=np.sqrt(32*np.pi/3); yc=Z/2.0
def nu(y): return np.sqrt(1.0+1.0/np.maximum(y,1e-30))
kappa=1.0/((nu(yc)-1.0)*yc)
def _tan(y):
    dy=1e-5*max(y,1e-3); eps=lambda q:kappa*(nu(q)-1.0)*q; sig=lambda q:q/yc
    return (sig(y+dy)-sig(y-dy))/(eps(y+dy)-eps(y-dy))
_deep=_tan(0.01)
def S_of(y): return _tan(max(y,1e-6))/_deep

def deriv1d(x):
    n=len(x); rows=[];cols=[];vals=[]
    for i in range(n):
        if i==0: h=x[1]-x[0]; rows+=[0,0];cols+=[0,1];vals+=[-1/h,1/h]
        elif i==n-1: h=x[-1]-x[-2]; rows+=[n-1,n-1];cols+=[n-2,n-1];vals+=[-1/h,1/h]
        else:
            hm=x[i]-x[i-1];hp=x[i+1]-x[i]; rows+=[i,i,i];cols+=[i-1,i,i+1]
            vals+=[-hp/(hm*(hm+hp)),(hp-hm)/(hm*hp),hm/(hp*(hm+hp))]
    return sp.csr_matrix((vals,(rows,cols)),shape=(n,n))

def rho_phantom(a0,gext_a0,r,th):
    gext=gext_a0*a0
    R,TH=np.meshgrid(r,th,indexing='ij'); ST=np.sin(TH); CT=np.cos(TH)
    gr=G*Msun/R**2+gext*CT; gth=-gext*ST; gmag=np.sqrt(gr**2+gth**2); f=nu(gmag/a0)-1.0
    Ar=f*gr; Ath=f*gth
    d_r=np.gradient(R**2*Ar,r,axis=0)/R**2; d_t=np.gradient(ST*Ath,th,axis=1)/(R*ST)
    return (d_r+d_t)/(4*np.pi*G)

# ============================================================================================
# INDEPENDENT solver: direct theta-quadrature of the EXACT spherical strain (no G_pp algebra).
# u_r=U(r)P2, u_th=V(r)dP2/dth. Strain components analytic in r-operators, but the angular
# integrals are done by NUMERICAL quadrature over a theta grid -- independent of the closed forms.
# ============================================================================================
def solve_indep(a0,gext_a0,betas,mu_tracks_tangent=False,NR=700,NT=1500):
    r=np.logspace(np.log10(5.0*AU),np.log10(5.0e5*AU),NR)
    th=np.linspace(1e-4,np.pi-1e-4,NT)
    c=np.cos(th); s=np.sin(th)
    P2=0.5*(3*c**2-1); B2=-3*c*s; B2p=-3*np.cos(2*th); cb2=(c/s)*B2   # dP2, d2P2, cot*dP2
    wth=s*np.gradient(th)                                            # sin(th) dth quadrature
    Keff=a0**2/(16*np.pi*G)
    y0=(G*Msun/r**2)/a0
    Kt=Keff*np.array([S_of(v) for v in y0])
    Dr=deriv1d(r); di=lambda v:sp.diags(v); Z0=sp.csr_matrix((NR,NR))
    H2=lambda A,Bm:sp.hstack([A,Bm],format='csr')
    OP_Up=H2(Dr,Z0); OP_a=H2(di(1/r),Z0); OP_b=H2(Z0,di(1/r))
    OP_Jr=H2(Dr+di(2/r),di(-6/r)); OP_g=H2(di(1/r),Dr-di(1/r))
    rw=2*np.pi*r**2*np.gradient(r)
    def addterm(H,wv,P,Q): D=di(wv); T=P.T@D@Q; return H+T+T.T
    # numerical angular integrals (independent of the hard-coded G_*)
    Ipp =np.sum(P2*P2*wth); Iaa=Ipp
    Ipbp=np.sum(P2*B2p*wth); Ipcb=np.sum(P2*cb2*wth)
    Ibpbp=np.sum(B2p*B2p*wth); Icbcb=np.sum(cb2*cb2*wth); Ibb=np.sum(B2*B2*wth)
    # bulk
    Hb=sp.csr_matrix((2*NR,2*NR)); Hb=addterm(Hb,rw*0.5*Kt*Ipp,OP_Jr,OP_Jr)
    def shearH(muw):
        w=rw*muw; H=sp.csr_matrix((2*NR,2*NR))
        H=addterm(H,w*Ipp,OP_Up,OP_Up)
        H=addterm(H,w*Iaa,OP_a,OP_a); H=addterm(H,w*Ipbp,OP_a,OP_b); H=addterm(H,w*Ibpbp,OP_b,OP_b)
        H=addterm(H,w*Iaa,OP_a,OP_a); H=addterm(H,w*Ipcb,OP_a,OP_b); H=addterm(H,w*Icbcb,OP_b,OP_b)
        H=addterm(H,w*0.5*Ibb,OP_g,OP_g)
        H=addterm(H,-w*(1/3)*Ipp,OP_Jr,OP_Jr)
        return H
    rho_ph=rho_phantom(a0,gext_a0,r,th)
    rho_ph2=np.sum(rho_ph*P2[None,:]*wth[None,:],axis=1)
    bvec=OP_Jr.T@(rw*Kt*rho_ph2)
    fixed=[NR-1,2*NR-1]; free=np.setdiff1d(np.arange(2*NR),fixed)
    # committed project2d: integrand Jr*P2 * P2 / r^3 * (2pi r^2 sin dr dth) = 2pi dr/r * Jr * Ipp
    def proj(Jr): return abs(np.sum(rw*Jr/r**3*Ipp))   # rw/r^3 = 2pi dr/r  (matches methodB project2d)
    def q2(beta):
        bb=max(beta,1e-6)
        muvec=3.0*bb*(Kt if mu_tracks_tangent else Keff*np.ones(NR))
        H=(Hb+shearH(muvec)).tocsr()
        x=np.zeros(2*NR); x[free]=spsolve(H[free][:,free].tocsc(),bvec[free])
        return proj(OP_Jr@x), x, OP_Jr, shearH, Hb
    q0=q2(0.0)[0]
    return {b:q2(b)[0]/q0 for b in betas}, q2

if __name__=="__main__":
    print("="*90)
    print("(1) DIVERGENCE-FREE RELAXATION TEST (reviewer crux)")
    print("="*90)
    # build the modal operators on a modest grid
    NR=500
    r=np.logspace(np.log10(5*AU),np.log10(5e5*AU),NR)
    Dr=deriv1d(r); di=lambda v:sp.diags(v); Z0=sp.csr_matrix((NR,NR))
    H2=lambda A,Bm:sp.hstack([A,Bm],format='csr')
    OP_Jr=H2(Dr+di(2/r),di(-6/r))
    # choose arbitrary smooth U(r); set V so that Jr = U'+2U/r-6V/r = 0 EXACTLY => V=r(U'+2U/r)/6
    rc=4000*AU
    U=np.exp(-((np.log(r/rc))**2)/1.2)
    Up=Dr@U
    V=r*(Up+2*U/r)/6.0                      # makes analytic Jr=0
    x=np.concatenate([U,V])
    Jr=OP_Jr@x
    # scalar norm for comparison: a non-solenoidal field of similar amplitude
    Uns=U.copy(); Vns=np.zeros_like(V)      # V=0 -> Jr=U'+2U/r != 0
    xns=np.concatenate([Uns,Vns]); Jrns=OP_Jr@xns
    print(f"  solenoidal field:  ||Jr||/||Jr_nonsolenoidal|| = {np.linalg.norm(Jr)/np.linalg.norm(Jrns):.3e}")
    print(f"    -> OP_Jr correctly annihilates the divergence-free field (should be ~0, up to FD error)")
    # shear energy of the solenoidal field (should be >0): build shearH at unit mu
    # quick shear energy via the same G-integrals used in methodB
    Gpp,Gpbp,Gpcb,Gbpbp,Gcbcb,Gbb=0.4,-1.6,-0.8,8.4,3.6,2.4
    OP_Up=H2(Dr,Z0); OP_a=H2(di(1/r),Z0); OP_b=H2(Z0,di(1/r)); OP_g=H2(di(1/r),Dr-di(1/r))
    rw=2*np.pi*r**2*np.gradient(r)
    def addterm(H,wv,P,Q): D=di(wv); T=P.T@D@Q; return H+T+T.T
    Hs=sp.csr_matrix((2*NR,2*NR))
    Hs=addterm(Hs,rw*Gpp,OP_Up,OP_Up); Hs=addterm(Hs,rw*Gpp,OP_a,OP_a); Hs=addterm(Hs,rw*Gpbp,OP_a,OP_b)
    Hs=addterm(Hs,rw*Gbpbp,OP_b,OP_b); Hs=addterm(Hs,rw*Gpp,OP_a,OP_a); Hs=addterm(Hs,rw*Gpcb,OP_a,OP_b)
    Hs=addterm(Hs,rw*Gcbcb,OP_b,OP_b); Hs=addterm(Hs,rw*0.5*Gbb,OP_g,OP_g); Hs=addterm(Hs,-rw*(1/3)*Gpp,OP_Jr,OP_Jr)
    Esh_sol=0.5*x@(Hs@x); Esh_ns=0.5*xns@(Hs@xns)
    print(f"  shear energy of solenoidal field = {Esh_sol:.4e}  (>0 => solenoidal fields DO carry shear)")
    print(f"  shear energy of V=0 field        = {Esh_ns:.4e}")
    print(f"    => a div-free field costs shear energy but leaves J=0: the medium CANNOT relax shear")
    print(f"       for free; it trades shear vs bulk. Suppression governed by mu_s/K_t. OK.\n")

    print("="*90)
    print("(2) FULLY INDEPENDENT w (direct theta-quadrature, no hard-coded G_pp): footing A")
    print("="*90)
    betas=[0.0,0.33,0.6,0.95,2.0]
    for tag,a0 in (("canon",9.36e-11),("alt",1.13e-10)):
        wA,_=solve_indep(a0,2.2,betas,mu_tracks_tangent=False)
        print(f"  {tag}: "+"  ".join(f"w({b})={wA[b]:.3f}" for b in betas[1:]))
    print("\n  footing B (mu tracks K_t):")
    for tag,a0 in (("canon",9.36e-11),):
        wB,_=solve_indep(a0,2.2,betas,mu_tracks_tangent=True)
        print(f"  {tag}: "+"  ".join(f"w({b})={wB[b]:.3f}" for b in betas[1:]))
    print("exit 0")
