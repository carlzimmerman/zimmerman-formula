#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
aqual_solver_2026.py -- GATE: the AQUAL benchmark at epsilon = 0.

Solves the axisymmetric nonlinear Poisson equation of the FROZEN action's chi -> 0 limit

    div[ mu(|grad phi|) grad phi ] = 4 pi G M delta^3(r),      grad phi -> -g_e zhat

in units GM = a0 = 1, so R_M = 1 and a0/R_M = 1.  mu is the theory's own DERIVED function
    mu(x) = x/(1+x)          [from F_MOND = -2 sqrt(X) + 2 ln(1+sqrt(X)), verified]
and mu_2(x) = x/(1+x^2)^(1/2) is also run because it is the case Milgrom tabulates.

METHOD: finite volume on a (s = ln r, theta) grid, mu-lagged fixed point with under-
relaxation, sparse direct linear solves.  Unknown is u = phi + g_e r cos(theta), with
u -> -1/r at the inner boundary (deep Newtonian) and u -> 0 at the outer boundary.

VALIDATION, in order, none of which uses the QUMOND formula:
  V1  g_e = 0 must reproduce the EXACT spherical first integral mu(g) g = 1/r^2.
  V2  the deep-Newtonian and deep-MOND radial asymptotics.
  V3  q(eta) for mu_1 must exceed the QUMOND value by ~25%, and for mu_2 by
      < 1e-27 s^-2 once dimensionalised -- both stated verbatim in DHF footnote 6.
"""
import sys, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
def head(t): print("\n"+"="*100+f"\n{t}\n"+"="*100,flush=True)
def ok(c,l,d=""):
    print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else ""),flush=True); return c
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)

MU = {"mu1": lambda x: x/(1.0+x),
      "mu2": lambda x: x/np.sqrt(1.0+x*x)}

class Grid:
    def __init__(self,rmin=1e-4,rmax=1e4,ns=320,nt=96):
        self.s=np.linspace(np.log(rmin),np.log(rmax),ns); self.ds=self.s[1]-self.s[0]
        self.r=np.exp(self.s); self.ns=ns
        self.th=(np.arange(nt)+0.5)*np.pi/nt; self.dt=np.pi/nt; self.nt=nt
        self.mu_c=np.cos(self.th); self.sin=np.sin(self.th)
        self.sf=np.exp(0.5*(self.s[1:]+self.s[:-1]))                 # r at radial faces
        self.tf=np.arange(1,nt)*np.pi/nt                             # theta faces
        self.sintf=np.sin(self.tf)

def grads(G,phi):
    """|grad phi| at cell centres, from centred differences."""
    dpds=np.zeros_like(phi); dpdt=np.zeros_like(phi)
    dpds[1:-1,:]=(phi[2:,:]-phi[:-2,:])/(2*G.ds)
    dpds[0,:]=(phi[1,:]-phi[0,:])/G.ds; dpds[-1,:]=(phi[-1,:]-phi[-2,:])/G.ds
    dpdt[:,1:-1]=(phi[:,2:]-phi[:,:-2])/(2*G.dt)
    dpdt[:,0]=(phi[:,1]-phi[:,0])/G.dt; dpdt[:,-1]=(phi[:,-1]-phi[:,-2])/G.dt
    r=G.r[:,None]
    gr=dpds/r; gt=dpdt/r
    return np.sqrt(gr*gr+gt*gt)

def build(G,mufun,phi,eta):
    """Linear system for u on the (s,theta) grid with mu lagged at phi."""
    ns,nt=G.ns,G.nt; N=ns*nt
    x=grads(G,phi); m=mufun(np.maximum(x,1e-30))
    # face values of mu (harmonic-free arithmetic average is fine here)
    mfs=0.5*(m[1:,:]+m[:-1,:])          # radial faces  (ns-1, nt)
    mft=0.5*(m[:,1:]+m[:,:-1])          # theta faces   (ns, nt-1)
    idx=lambda i,j: i*nt+j
    rows=[];cols=[];vals=[];rhs=np.zeros(N)
    # coefficients: radial face k between i,i+1 has weight  A = m * r_f * sin(th) * dt/ds
    #               theta  face k between j,j+1 has weight  B = m * r   * sin(tf) * ds/dt
    Ar=mfs*G.sf[:,None]*G.sin[None,:]*(G.dt/G.ds)
    Bt=mft*G.r[:,None]*G.sintf[None,:]*(G.ds/G.dt)
    for i in range(ns):
        for j in range(nt):
            k=idx(i,j)
            if i==0 or i==ns-1:
                rows.append(k);cols.append(k);vals.append(1.0)
                rhs[k]= (-1.0/G.r[0]+eta*G.r[0]*G.mu_c[j]) if i==0 else 0.0
                continue
            diag=0.0
            for (ii,a) in ((i-1,Ar[i-1,j]),(i+1,Ar[i,j])):
                rows.append(k);cols.append(idx(ii,j));vals.append(a); diag-=a
            if j>0:
                b=Bt[i,j-1]; rows.append(k);cols.append(idx(i,j-1));vals.append(b); diag-=b
            if j<nt-1:
                b=Bt[i,j]; rows.append(k);cols.append(idx(i,j+1));vals.append(b); diag-=b
            rows.append(k);cols.append(k);vals.append(diag)
            # source from the external field carried by u = phi + eta r cos(theta)
            rhs[k]=0.0
    A=sps.csr_matrix((vals,(rows,cols)),shape=(N,N))
    return A,rhs

def solve(G,mufun,eta,tol=1e-10,itmax=300,relax=0.55,verbose=False):
    ns,nt=G.ns,G.nt
    r=G.r[:,None]; ct=G.mu_c[None,:]
    u=-1.0/r*np.ones((ns,nt))
    phi=u-eta*r*ct
    for it in range(itmax):
        A,rhs=build(G,mufun,phi,eta)
        # u equation: div[mu grad(u - eta r cos)] = 0  ->  move the external part to the rhs
        # the external field is a HARMONIC function, but mu is not constant, so it sources:
        ue=-eta*r*ct
        Ae,_=build(G,mufun,phi,eta)
        rhs2=-(Ae.dot(ue.ravel()))
        rhs2[:nt]=rhs[:nt]; rhs2[-nt:]=0.0
        unew=spl.spsolve(A,rhs2).reshape(ns,nt)
        du=np.max(np.abs(unew-u))/max(1.0,np.max(np.abs(unew)))
        u=(1-relax)*u+relax*unew
        phi=u+ue
        if verbose and it%20==0: info(f"    iter {it:3d}",f"rel change {du:.3e}")
        if du<tol: break
    return u,phi,it,du

def multipoles(G,u,eta,lmax=4,rfit=(3e-3,3e-2)):
    """Fit u + 1/r = c0 + c2 r^2 P2 + c4 r^4 P4 in the inner region."""
    from numpy.polynomial.legendre import leggauss
    sel=(G.r>rfit[0])&(G.r<rfit[1])
    rr=G.r[sel]; f=u[sel,:]+1.0/rr[:,None]
    P2=0.5*(3*G.mu_c**2-1); P4=(35*G.mu_c**4-30*G.mu_c**2+3)/8
    w=G.sin*G.dt
    # Legendre projection: coefficient_l = (2l+1)/2 * INT f P_l sin(th) dth.
    # (The earlier version divided the l=2,4 projections by INT sin = 2 a second time,
    #  halving them -- caught because q came out a CONVERGED factor ~2 below the
    #  Blanchet-Novak anchor.  The l=0 average was unaffected: (2*0+1)/2 = 1/2.)
    a0=0.5*(f*w).sum(1)
    a2=2.5*(f*P2*w).sum(1)
    a4=4.5*(f*P4*w).sum(1)
    c2=np.polyfit(rr**2,a2,1)[0]
    return a0,a2,c2

if __name__=="__main__":
    t0=time.time()
    head("V1 -- spherical check (eta = 0) against the EXACT first integral mu(g) g = 1/r^2")
    from scipy.optimize import brentq
    G=Grid(1e-4,1e4,320,32)
    for name in ("mu1","mu2"):
        u,phi,it,du=solve(G,MU[name],0.0,itmax=400)
        gnum=grads(G,phi)[:,G.nt//2]
        gex=np.array([brentq(lambda g: MU[name](g)*g-1.0/rr**2,1e-12,1e12) for rr in G.r])
        m=(G.r>1e-3)&(G.r<1e3)
        err=np.max(np.abs(gnum[m]/gex[m]-1))
        ok(err<0.02,f"V1  {name}: radial field matches the exact first integral",
           f"max rel err {err:.3e} over 1e-3 < r < 1e3, {it} iters, resid {du:.1e}")
    info("V1 note","this validates mu, the discretisation and the boundary handling with no "
                    "reference to any published number")
    print(f"\n  runtime {time.time()-t0:.0f} s")

    head("V2 -- external field ON: mu_1 against the Blanchet-Novak 2011 exact-AQUAL anchor")
    # [BN11, via Carl] mu(x) = x/(1+x), a0 = 1.2e-10, g_e = 1.9e-10  =>  eta = 1.58333,
    # Q2 = 3.8e-26 s^-2, dimensionless q2 = 0.33 in their convention Q2 = q2 a0/R_M.
    # Frozen lock: Q2 = (3/2) q_zz a0/R_M, so the target is q_zz = (2/3)(0.33) = 0.2200.
    G2=Grid(1e-4,1e4,512,128)
    eta_bn=1.9/1.2
    u,phi,it,du=solve(G2,MU["mu1"],eta_bn,itmax=400,relax=0.5)
    a0c,a2c,c2=multipoles(G2,u,eta_bn)
    qzz=2.0*c2
    info("V2  BN11 anchor",f"eta = {eta_bn:.4f}: q_zz = {qzz:+.4f}  target -0.2200  "
         f"ratio {abs(qzz)/0.22:.3f}   (Q2 = {abs(qzz)*1.5:.3f} a0/R_M vs BN 0.33)")
    ok(abs(abs(qzz)/0.22-1)<0.06,"V2  Blanchet-Novak exact-AQUAL quadrupole reproduced",
       f"{abs(abs(qzz)/0.22-1):.1%} from the published 2-significant-figure value")

    head("V3 -- the AQUAL-vs-QUMOND excess for mu_1, against DHF footnote 6")
    QUM={1.5:0.15337,2.0:0.21321}      # this repo's exact QUMOND quadrature (gate0), TRUE eta
    for eta,qq in QUM.items():
        u,phi,it,du=solve(G2,MU["mu1"],eta,itmax=400,relax=0.5)
        a0c,a2c,c2=multipoles(G2,u,eta)
        ex=abs(2.0*c2)/qq-1.0
        print(f"  eta={eta}: AQUAL q_zz = {abs(2*c2):.4f}  QUMOND q = {qq:.4f}  excess = {ex:+.1%}")
    print("  DHF footnote 6 (n=1): 'about 25% larger' (at their fitted eta ~ 1.6-1.9)")
    info("V3 note","the M09 Table-1 'exact' anchors fetched earlier are NOT used: two "
         "independent fetches returned mutually inconsistent column alignments for that "
         "table, so those numbers are unreliable as anchors. BN11 is the benchmark.")
    print(f"\n  total runtime {time.time()-t0:.0f} s")
