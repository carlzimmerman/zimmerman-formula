#!/usr/bin/env python3
"""Verify the modal ell=2 energy functionals (bulk INT(1/2)J^2 and deviatoric INT(e:e-J^2/3))
against DIRECT 2D integration of the exact spherical strain tensor for a known u_r=U(r)P2,
u_th=V(r)dP2/dth. If they agree, the modal Hessian is trustworthy and w can be believed.
Also: test the modal solver's w(mu) for a HOMOGENEOUS medium (K const) -- does it track the
P-wave suppression, i.e. is the shear coupling to J of the right magnitude?"""
import numpy as np, scipy.sparse as sp
AU=1.496e11
G_pp,G_pbp,G_pcb,G_bpbp,G_cbcb,G_bpcb,G_bb=0.4,-1.6,-0.8,8.4,3.6,1.2,2.4
def deriv1d(x):
    n=len(x);rows=[];cols=[];vals=[]
    for i in range(n):
        if i==0:h=x[1]-x[0];rows+=[0,0];cols+=[0,1];vals+=[-1/h,1/h]
        elif i==n-1:h=x[-1]-x[-2];rows+=[n-1,n-1];cols+=[n-2,n-1];vals+=[-1/h,1/h]
        else:
            hm=x[i]-x[i-1];hp=x[i+1]-x[i];rows+=[i,i,i];cols+=[i-1,i,i+1]
            vals+=[-hp/(hm*(hm+hp)),(hp-hm)/(hm*hp),hm/(hp*(hm+hp))]
    return sp.csr_matrix((vals,(rows,cols)),shape=(n,n))

# ---- radial grid + a smooth test (U,V) ----
NR=400
r=np.logspace(np.log10(50*AU),np.log10(3e4*AU),NR)
rc=5e3*AU
U=np.exp(-((np.log(r/rc))**2)/1.5)*1e6            # arbitrary smooth radial profiles (meters)
V=0.4*np.exp(-((np.log(r/(2*rc)))**2)/2.0)*1e6
Dr=deriv1d(r)
Up=Dr@U; Vp=Dr@V
# modal radial fields
A_rr=Up
a=U/r; b=V/r
g=U/r+Vp-V/r
Jr=Up+2*U/r-6*V/r
rw=2*np.pi*r**2*np.gradient(r)
# modal energies
E_bulk_modal=np.sum(rw*0.5*Jr**2*G_pp)
E_dev_modal=np.sum(rw*(A_rr**2*G_pp
                       + a**2*G_pp+2*a*b*G_pbp+b**2*G_bpbp
                       + a**2*G_pp+2*a*b*G_pcb+b**2*G_cbcb
                       + 0.5*g**2*G_bb
                       - (1.0/3.0)*Jr**2*G_pp))

# ---- DIRECT 2D integration with exact spherical strain ----
NT=4000
th=np.linspace(1e-5,np.pi-1e-5,NT); c=np.cos(th);s=np.sin(th)
P2=0.5*(3*c**2-1); B2=-3*c*s
dP2=B2                                   # dP2/dth
# build 2D fields
Rg,TH=np.meshgrid(r,th,indexing='ij'); ST=np.sin(TH)
ur=U[:,None]*P2[None,:]; ut=V[:,None]*B2[None,:]
# strains via 2D finite differences (independent of the modal algebra)
dur_dr=np.gradient(ur,r,axis=0); dut_dr=np.gradient(ut,r,axis=0)
dur_dth=np.gradient(ur,th,axis=1); dut_dth=np.gradient(ut,th,axis=1)
COT=np.cos(TH)/np.sin(TH)
e_rr=dur_dr
e_thth=dut_dth/Rg+ur/Rg
e_phph=ur/Rg+COT*ut/Rg
e_rth=0.5*(dur_dth/Rg+dut_dr-ut/Rg)
J=e_rr+e_thth+e_phph
ee=e_rr**2+e_thth**2+e_phph**2+2*e_rth**2
dV=2*np.pi*Rg**2*ST*np.gradient(r)[:,None]*np.gradient(th)[None,:]
E_bulk_2d=np.sum(0.5*J**2*dV)
E_dev_2d=np.sum((ee-J**2/3)*dV)
print("[A] energy cross-check: modal reduction vs direct 2D strain integration")
print(f"    bulk  INT (1/2)J^2 dV:   modal={E_bulk_modal:.6e}  2D={E_bulk_2d:.6e}  ratio={E_bulk_modal/E_bulk_2d:.4f}")
print(f"    dev   INT (e:e-J^2/3)dV: modal={E_dev_modal:.6e}  2D={E_dev_2d:.6e}  ratio={E_dev_modal/E_dev_2d:.4f}")
print(f"    (ratios ~1.00 => modal shear/bulk energy correctly assembled)")

# ---- [B] modal solver on a HOMOGENEOUS medium: w(mu) vs the irrotational P-wave bound K/(K+4/3mu) ----
print("\n[B] homogeneous K=1: modal w(mu) vs infinite-medium irrotational bound K/(K+4/3 mu)")
di=lambda v:sp.diags(v); Z0=sp.csr_matrix((NR,NR)); H2=lambda A,Bm:sp.hstack([A,Bm],format='csr')
OP_Up=H2(Dr,Z0); OP_a=H2(di(1/r),Z0); OP_b=H2(Z0,di(1/r))
OP_Jr=H2(Dr+di(2/r),di(-6/r)); OP_g=H2(di(1/r),Dr-di(1/r))
def addterm(H,w,P,Q): D=di(w); T=P.T@D@Q; return H+T+T.T
K=1.0
Hb=sp.csr_matrix((2*NR,2*NR)); Hb=addterm(Hb,rw*0.5*K*G_pp,OP_Jr,OP_Jr)
Hs=sp.csr_matrix((2*NR,2*NR))
Hs=addterm(Hs,rw*G_pp,OP_Up,OP_Up)
Hs=addterm(Hs,rw*G_pp,OP_a,OP_a); Hs=addterm(Hs,rw*G_pbp,OP_a,OP_b); Hs=addterm(Hs,rw*G_bpbp,OP_b,OP_b)
Hs=addterm(Hs,rw*G_pp,OP_a,OP_a); Hs=addterm(Hs,rw*G_pcb,OP_a,OP_b); Hs=addterm(Hs,rw*G_cbcb,OP_b,OP_b)
Hs=addterm(Hs,rw*0.5*G_bb,OP_g,OP_g)
Hs=addterm(Hs,-rw*(1/3)*G_pp,OP_Jr,OP_Jr)
# J-only drive with a smooth ell=2 source
src=np.exp(-((np.log(r/rc))**2)/1.5)
bvec=OP_Jr.T@(rw*K*src)
fixed=[NR-1,2*NR-1]; free=np.setdiff1d(np.arange(2*NR),fixed)
from scipy.sparse.linalg import spsolve
def q2(mu):
    H=(Hb+mu*Hs).tocsr()
    x=np.zeros(2*NR); x[free]=spsolve(H[free][:,free].tocsc(),bvec[free])
    Jr=OP_Jr@x
    return np.sum(rw*Jr/r)   # proportional to project(Jr P2)
q0=q2(1e-6)
print(f"    {'mu/K':>6} {'w_modal':>9} {'K/(K+4/3mu)':>12}")
for mu in (1e-6,0.33,1.0,3.0,6.0):
    print(f"    {mu:>6.2f} {q2(mu)/q0:>9.4f} {1.0/(1.0+4.0/3.0*mu):>12.4f}")
print("exit 0")
