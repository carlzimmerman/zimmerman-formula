#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
linear_response_2026.py -- dq_zz/dchi by the STABLE route.

The parameter-differentiation run (dq2_dchi_2026.py) diverged because it LAGGED the tidal
flux, which contains the solution's own fourth derivatives: chi k^4 grid-scale noise is
amplified without bound.  Carl's linear-response equation avoids that entirely:

    L_AQUAL phi_1 = -div[ A'(X0) Sb0^2 grad phi0 ] + d_i d_j [ A(X0) Sb0_ij ]

with every fourth derivative acting on the KNOWN smooth AQUAL background phi0.

IMPLEMENTATION: solve the ORIGINAL validated nonlinear AQUAL problem twice with the fixed
extra source +-delta * RHS1[phi0] added, and central-difference:
    phi_1 = (phi[+delta] - phi[-delta]) / (2 delta).
This is exactly the first-order response (central differencing kills even-order error) and
reuses 100% validated machinery: V1 spherical 6e-4, V2 Blanchet-Novak 1.9%, H0 Hessian
identity 4e-3.  The fixed source cannot feed back, so the iteration is as stable as AQUAL.
"""
import sys, time, json
import numpy as np
import scipy.sparse as sps, scipy.sparse.linalg as spl
sys.path.insert(0,'.')
from aqual_solver_2026 import Grid, MU, grads, multipoles
from dq2_dchi_2026 import sph_derivs, tensor_div, Afun, Apfun, hessian_check
def head(t): print("\n"+"="*100+f"\n{t}\n"+"="*100,flush=True)
def ok(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else ""),flush=True); return c
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)

def rhs1_cells(G,phi0):
    """FV cell integrals of  div J,  J_i = -A'(X0) Sb0^2 d_i phi0 + [div(A Sb0)]_i ."""
    g=grads(G,phi0); X=g*g
    phi_r,pt,H_rr,H_rt,H_tt,H_ff,lap=sph_derivs(G,phi0)
    S_rr=H_rr-lap/3.0; S_tt=H_tt-lap/3.0; S_ff=H_ff-lap/3.0; S_rt=H_rt
    Sb2=S_rr**2+S_tt**2+S_ff**2+2*S_rt**2
    A_=Afun(X); Ap=Apfun(X)
    Vr,Vt=tensor_div(G,A_*S_rr,A_*S_rt,A_*S_tt,A_*S_ff)
    r=G.r[:,None]
    gr=np.gradient(phi0,G.s,axis=0)/r; gt=np.gradient(phi0,G.th,axis=1)/r
    Jr=-Ap*Sb2*gr+Vr; Jt=-Ap*Sb2*gt+Vt
    ns,nt=G.ns,G.nt
    out=np.zeros((ns,nt))
    Jr_f=0.5*(Jr[1:,:]+Jr[:-1,:]); Jt_f=0.5*(Jt[:,1:]+Jt[:,:-1])
    for i in range(1,ns-1):
        for j in range(nt):
            acc=(Jr_f[i,j]*G.sf[i]**2*G.sin[j]*G.dt-Jr_f[i-1,j]*G.sf[i-1]**2*G.sin[j]*G.dt)
            if j<nt-1: acc+=Jt_f[i,j]*G.r[i]*G.sintf[j]*G.ds
            if j>0:    acc-=Jt_f[i,j-1]*G.r[i]*G.sintf[j-1]*G.ds
            out[i,j]=acc
    # trim innermost/outermost rings: the source is analytically negligible there
    # (A Sb ~ r^5 inward, ~ r^-3 outward) but one-sided stencils are noisy
    out[:7,:]=0.0; out[-7:,:]=0.0
    return out

def solve_with_source(G,eta,S,itmax=400,relax=0.5,tol=1e-10):
    """The validated AQUAL mu-lagged solver plus a FIXED extra FV source S."""
    ns,nt=G.ns,G.nt; r=G.r[:,None]; ct=G.mu_c[None,:]
    u=-1.0/r*np.ones((ns,nt)); ue=-eta*r*ct
    idx=lambda i,j: i*nt+j
    for it in range(itmax):
        phi=u+ue
        g=grads(G,phi); m=MU["mu1"](np.maximum(g,1e-30))
        mfs=0.5*(m[1:,:]+m[:-1,:]); mft=0.5*(m[:,1:]+m[:,:-1])
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
        rhs=-(Amat.dot(ue.ravel()))-S.ravel()
        rhs[:nt]=(-1.0/G.r[0]+eta*G.r[0]*G.mu_c); rhs[-nt:]=0.0
        unew=spl.spsolve(Amat,rhs).reshape(ns,nt)
        du=np.max(np.abs(unew-u))/max(1.0,np.max(np.abs(unew)))
        u=(1-relax)*u+relax*unew
        if du<tol: break
    return u,it,du

if __name__=="__main__":
    t0=time.time()
    head("L0 -- machinery re-checks")
    G=Grid(1e-4,1e4,384,96)
    ok(hessian_check(G)<2e-2,"L0  Hessian/tensor-divergence identity holds on this grid")
    RES={}
    for eta,lab in ((1.9/1.2,"Blanchet-Novak eta=1.583"),(2.0/1.08,"DHF fiducial eta=1.852")):
        head(f"L1 -- background + response at {lab}")
        u0,it0,du0=solve_with_source(G,eta,np.zeros((G.ns,G.nt)))
        _,_,c2_0=multipoles(G,u0,eta); q0=2*c2_0
        info("L1  background",f"q_zz(0) = {q0:+.4f}  (iters {it0}, resid {du0:.0e})")
        phi0=u0+(-eta*G.r[:,None]*G.mu_c[None,:])
        S=rhs1_cells(G,phi0)
        info("L1  tidal source built",f"max |cell integral| = {np.abs(S).max():.3e}")
        ders=[]
        for d in (0.01,0.02,0.04):
            up,_,_=solve_with_source(G,eta,+d*S)
            um,_,_=solve_with_source(G,eta,-d*S)
            _,_,c2p=multipoles(G,up,eta); _,_,c2m=multipoles(G,um,eta)
            der=(2*c2p-2*c2m)/(2*d); ders.append(der)
            info(f"L2  delta={d}",f"q(+d)={2*c2p:+.5f}  q(-d)={2*c2m:+.5f}  dq/dchi = {der:+.5f}")
        spread=max(ders)-min(ders)
        ok(spread<0.1*max(1e-9,abs(np.mean(ders))) or spread<5e-3,
           "L2  derivative is delta-independent (linear regime confirmed)",
           f"spread {spread:.2e} across a 4x range of delta")
        der=ders[0]
        RES[lab]=dict(eta=eta,q0=float(q0),dqdchi=float(der))
        head(f"L3 -- meaning at {lab}")
        print(f"  q_zz(chi) = {q0:+.4f} + ({der:+.4f}) chi + O(chi^2)")
        for chi in (0.5,1.0,1.73):
            print(f"    chi = {chi:>5}:  q_zz = {q0+chi*der:+.4f}   "
                  f"({(q0+chi*der)/q0*100:6.1f}% of AQUAL)")
        if der!=0:
            print(f"  linear extrapolation to q_zz = 0 would need chi = {abs(q0/der):.2f}"
                  f"   (ellipticity cap: 1.73)")
    json.dump(RES,open("linear_response_result.json","w"),indent=1)
    print(f"\n  runtime {time.time()-t0:.0f} s")
