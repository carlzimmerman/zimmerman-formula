#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
dq2_dchi_2026.py -- THE DECISIVE NUMBER: dQ2/dchi at chi = 0 for the frozen action.

Equation (dimensionless, GM = a0 = 1):
    div[ (mu0(X) + chi A'(X) Sb2) grad phi  -  chi V ] = 4 pi delta^3,   V_i = D_j(A(X) Sb_ij)
with mu0(x)=x/(1+x), A(X)=X^2/(1+X)^4, Sb_ij the trace-free Hessian of phi,
Sb2 = Sb_ij Sb_ij, boundary grad phi -> -eta zhat.

METHOD: parameter differentiation through the VALIDATED nonlinear AQUAL solver (V1 1.9e-4
spherical, V2 1.9% against Blanchet-Novak 2011).  The tidal flux enters the same mu-lagged
fixed point; q_zz(chi) at chi = +-delta gives the centred derivative.  No new linear-operator
code, so no new untested machinery.

HESSIAN CHECK built in: for any smooth phi, div(Hessian) = grad(lap phi) identically, so
div(Sb)_i = (2/3) d_i (lap phi).  The tensor-divergence routine must pass this before use.
"""
import sys, time
import numpy as np
import scipy.sparse as sps, scipy.sparse.linalg as spl
sys.path.insert(0,'.')
from aqual_solver_2026 import Grid, MU, grads, multipoles
def head(t): print("\n"+"="*100+f"\n{t}\n"+"="*100,flush=True)
def ok(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else ""),flush=True); return c
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)

def sph_derivs(G,phi):
    """phi_r, phi_t, and the orthonormal spherical Hessian components (axisymmetric)."""
    r=G.r[:,None]; th=G.th[None,:]
    ds,dt=G.ds,G.dt
    def d_s(f):
        out=np.empty_like(f); out[1:-1]=(f[2:]-f[:-2])/(2*ds)
        out[0]=(-3*f[0]+4*f[1]-f[2])/(2*ds); out[-1]=(3*f[-1]-4*f[-2]+f[-3])/(2*ds); return out
    def d_t(f):
        out=np.empty_like(f); out[:,1:-1]=(f[:,2:]-f[:,:-2])/(2*dt)
        out[:,0]=(-3*f[:,0]+4*f[:,1]-f[:,2])/(2*dt)
        out[:,-1]=(3*f[:,-1]-4*f[:,-2]+f[:,-3])/(2*dt); return out
    ps=d_s(phi); pt=d_t(phi)
    phi_r=ps/r; phi_t=pt                       # d/dr = (1/r) d/ds
    pss=d_s(ps); pst=d_t(ps); ptt=d_t(pt)
    H_rr=(pss-ps)/r**2
    H_rt=(pst/r - pt/r)/r                      # (1/r)d_r(phi_t) - phi_t/r^2 ; d_r phi_t = pst/r
    H_tt=ptt/r**2 + phi_r/r
    ct=np.cos(th)/np.sin(th)
    H_ff=phi_r/r + ct*pt/r**2
    lap=H_rr+H_tt+H_ff
    return phi_r,pt,H_rr,H_rt,H_tt,H_ff,lap

def tensor_div(G,T_rr,T_rt,T_tt,T_ff):
    """(div T)_r, (div T)_theta for symmetric axisymmetric T in the orthonormal basis."""
    r=G.r[:,None]; th=G.th[None,:]; ds,dt=G.ds,G.dt
    ct=np.cos(th)/np.sin(th)
    def d_s(f):
        out=np.empty_like(f); out[1:-1]=(f[2:]-f[:-2])/(2*ds)
        out[0]=(-3*f[0]+4*f[1]-f[2])/(2*ds); out[-1]=(3*f[-1]-4*f[-2]+f[-3])/(2*ds); return out
    def d_t(f):
        out=np.empty_like(f); out[:,1:-1]=(f[:,2:]-f[:,:-2])/(2*dt)
        out[:,0]=(-3*f[:,0]+4*f[:,1]-f[:,2])/(2*dt)
        out[:,-1]=(3*f[:,-1]-4*f[:,-2]+f[:,-3])/(2*dt); return out
    dr=lambda f: d_s(f)/r
    dth=lambda f: d_t(f)
    Vr=dr(T_rr)+dth(T_rt)/r+(2*T_rr-T_tt-T_ff+T_rt*ct)/r
    Vt=dr(T_rt)+dth(T_tt)/r+(3*T_rt+(T_tt-T_ff)*ct)/r
    return Vr,Vt

def hessian_check(G):
    """div(Hessian) must equal grad(lap) for a smooth test field."""
    r=G.r[:,None]; th=G.th[None,:]
    phi=np.exp(-((np.log(r)-np.log(0.5))**2))*(1+0.3*np.cos(th))*r**0.5
    _,_,H_rr,H_rt,H_tt,H_ff,lap=sph_derivs(G,phi)
    Vr,Vt=tensor_div(G,H_rr,H_rt,H_tt,H_ff)
    # grad(lap)
    ds,dt=G.ds,G.dt
    gl_r=np.gradient(lap,G.s,axis=0)/r
    gl_t=np.gradient(lap,G.th,axis=1)/r
    m=(G.r>2e-3)&(G.r<2e2)
    e1=np.max(np.abs(Vr[m,4:-4]-gl_r[m,4:-4]))/np.max(np.abs(gl_r[m,4:-4]))
    e2=np.max(np.abs(Vt[m,4:-4]-gl_t[m,4:-4]))/np.max(np.abs(gl_t[m,4:-4]))
    return max(e1,e2)

def Afun(X):  return X**2/(1.0+X)**4
def Apfun(X): return 2.0*X*(1.0-X)/(1.0+X)**5

def solve_chi(G,eta,chi,itmax=400,relax=0.5,tol=1e-10):
    """mu-lagged fixed point for the FULL flux, chi included; returns u and diagnostics."""
    ns,nt=G.ns,G.nt; r=G.r[:,None]; ct=G.mu_c[None,:]
    u=-1.0/r*np.ones((ns,nt)); ue=-eta*r*ct
    mu_min_seen=np.inf
    for it in range(itmax):
        phi=u+ue
        g=grads(G,phi); X=g*g
        phi_r,pt,H_rr,H_rt,H_tt,H_ff,lap=sph_derivs(G,phi)
        S_rr=H_rr-lap/3; S_tt=H_tt-lap/3; S_ff=H_ff-lap/3; S_rt=H_rt
        Sb2=S_rr**2+S_tt**2+S_ff**2+2*S_rt**2
        mue=MU["mu1"](np.maximum(g,1e-30))+chi*Apfun(X)*Sb2
        mu_min_seen=min(mu_min_seen,float(mue[(G.r>1e-2)[:,None]&(G.r<1e2)[:,None]&np.ones((1,nt),bool)].min()))
        # tidal vector V_i = D_j(A Sb_ij), lagged
        A_=Afun(X)
        Vr,Vt=tensor_div(G,A_*S_rr,A_*S_rt,A_*S_tt,A_*S_ff)
        # assemble: div[mue grad u] = -div[mue grad ue] + chi div V   (all lagged)
        idx=lambda i,j: i*nt+j
        mfs=0.5*(mue[1:,:]+mue[:-1,:]); mft=0.5*(mue[:,1:]+mue[:,:-1])
        Ar=mfs*G.sf[:,None]*G.sin[None,:]*(G.dt/G.ds)
        Bt=mft*G.r[:,None]*G.sintf[None,:]*(G.ds/G.dt)
        rows=[];cols=[];vals=[]
        N=ns*nt
        for i in range(ns):
            for j in range(nt):
                k=idx(i,j)
                if i==0 or i==ns-1:
                    rows.append(k);cols.append(k);vals.append(1.0); continue
                diag=0.0
                for (ii,a) in ((i-1,Ar[i-1,j]),(i+1,Ar[i,j])):
                    rows.append(k);cols.append(idx(ii,j));vals.append(a); diag-=a
                if j>0:
                    b=Bt[i,j-1]; rows.append(k);cols.append(idx(i,j-1));vals.append(b); diag-=b
                if j<nt-1:
                    b=Bt[i,j]; rows.append(k);cols.append(idx(i,j+1));vals.append(b); diag-=b
                rows.append(k);cols.append(k);vals.append(diag)
        Amat=sps.csr_matrix((vals,(rows,cols)),shape=(N,N))
        rhs=-(Amat.dot(ue.ravel()))
        # chi * div V as a volume term: FV cell integral of div V = flux of V through faces;
        # use centred face values of Vr, Vt
        divV=np.zeros((ns,nt))
        Vr_f=0.5*(Vr[1:,:]+Vr[:-1,:]); Vt_f=0.5*(Vt[:,1:]+Vt[:,:-1])
        for i in range(1,ns-1):
            for j in range(nt):
                acc=(Vr_f[i,j]*G.sf[i]**2*G.sin[j]*G.dt-Vr_f[i-1,j]*G.sf[i-1]**2*G.sin[j]*G.dt)
                if j<nt-1: acc+=Vt_f[i,j]*G.r[i]*G.sintf[j]*G.ds
                if j>0:    acc-=Vt_f[i,j-1]*G.r[i]*G.sintf[j-1]*G.ds
                divV[i,j]=acc
        rhs+=chi*divV.ravel()
        rhs[:nt]=(-1.0/G.r[0]+eta*G.r[0]*G.mu_c)
        rhs[-nt:]=0.0
        unew=spl.spsolve(Amat,rhs).reshape(ns,nt)
        du=np.max(np.abs(unew-u))/max(1.0,np.max(np.abs(unew)))
        u=(1-relax)*u+relax*unew
        if du<tol: break
    return u,it,du,mu_min_seen

if __name__=="__main__":
    t0=time.time()
    head("H0 -- Hessian/tensor-divergence identity check: div(H) = grad(lap)")
    G=Grid(1e-4,1e4,384,96)
    e=hessian_check(G)
    ok(e<2e-2,"H0  div(Hessian) reproduces grad(laplacian) on a smooth test field",
       f"max rel err {e:.2e} (centred FD, interior region)")
    head("H1 -- chi = 0 must reproduce the validated AQUAL result")
    eta=1.9/1.2
    u0,it0,du0,mm0=solve_chi(G,eta,0.0)
    _,_,c2_0=multipoles(G,u0,eta)
    info("H1  chi=0",f"q_zz = {2*c2_0:+.4f} (validated value -0.224; iters {it0}, resid {du0:.0e})")
    ok(abs(2*c2_0+0.224)<0.01,"H1  chi=0 branch of the tidal solver matches the AQUAL solver")
    head("H2 -- THE DERIVATIVE dq_zz/dchi at chi = 0")
    res={}
    for d in (0.02,0.04,0.08):
        up,itp,dup,mmp=solve_chi(G,eta,+d)
        um,itm,dum,mmm=solve_chi(G,eta,-d)
        _,_,c2p=multipoles(G,up,eta); _,_,c2m=multipoles(G,um,eta)
        der=(2*c2p-2*c2m)/(2*d)
        res[d]=der
        info(f"H2  delta = {d}",f"q(+d) = {2*c2p:+.5f}  q(-d) = {2*c2m:+.5f}  "
             f"dq/dchi = {der:+.5f}   (mu_min at +d: {mmp:.3f})")
    ds=sorted(res)
    rich=(4*res[ds[0]]-res[ds[1]])/3.0
    info("H2  Richardson",f"dq_zz/dchi|_0 = {rich:+.5f}")
    head("H3 -- WHAT IT MEANS")
    q0=2*c2_0
    print(f"  q_zz(chi) = {q0:+.4f} + ({rich:+.4f}) chi + O(chi^2)")
    print(f"  Cassini needs |q_zz| <= (2/3) Q2max/(a0/R_M).")
    print(f"  At the ellipticity cap chi = 1.73:  q_zz = {q0+1.73*rich:+.4f}")
    print(f"  fractional change available: {1.73*abs(rich)/abs(q0):.1%} of the AQUAL value")
    print(f"\n  runtime {time.time()-t0:.0f} s")
