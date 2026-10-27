"""Isolation-only candidate variational Gaussian-weighted expansion centre.

The centre is an explicit smooth function of all positions. Its complete
Jacobian is differentiated in the finite-basis selfexcluded Hamiltonian.
No production or free evolution is admitted by this diagnostic wrapper.
"""
import numpy as np
from scf_backend import G,diagonal,load_agama


def centre_and_chain(x,m,Rcent):
    if not np.isfinite(Rcent) or Rcent<=0:raise ValueError('fixed finite positive Rcent required')
    M=float(m.sum());X=np.average(x,axis=0,weights=m);y=x-X
    w=np.exp(-np.einsum('ij,ij->i',y,y)/(2*Rcent**2));Z=float(m@w)
    if not np.isfinite(Z) or Z<=0:raise FloatingPointError('weighted centre underflow/outside isolation domain')
    c=np.sum((m*w)[:,None]*y,axis=0)/Z

    def chain(F):
        # D_i^T F / m_i. A_i=(m_i/Z)[w_i I+(y_i-c) grad(w_i)^T].
        # Translation covariance gives sum D_i=I; all position dependence,
        # including X and the weight normalization, is retained.
        B=(w/Z)[:,None]*(F-y*((y-c)@F/Rcent**2)[:,None])
        return B+(F-np.sum(m[:,None]*B,axis=0))/M

    return X+c,chain


def gravity(x,m,nmax=32,lmax=6,r0=300.,eta=1.,Rcent=300.):
    x=np.ascontiguousarray(x,dtype=np.float64);m=np.ascontiguousarray(m,dtype=np.float64)
    if (m.ndim!=1 or x.shape!=(len(m),3) or len(m)<2 or not np.isfinite(x).all()
        or not np.isfinite(m).all() or np.any(m<=0) or not isinstance(nmax,int) or not 0<=nmax<=256
        or not isinstance(lmax,int) or not 0<=lmax<=64 or not np.isfinite(r0) or r0<=0
        or not np.isfinite(eta) or eta<.5):
        raise ValueError('finite positive-mass N>=2, fixed finite complete basis parameters required')
    centre,chain=centre_and_chain(x,m,Rcent);y=np.ascontiguousarray(x-centre);r=np.linalg.norm(y,axis=1)
    if np.any(r==0):raise ValueError('particle exactly at expansion centre outside analytic-gradient domain')
    agama=load_agama()
    if float(agama.G)!=1. or agama.getUnits()!={}:raise RuntimeError('candidate requires pristine native Agama G=1 units')
    pot=agama.Potential(type='BasisSet',particles=(y,G*m),symmetry='None',lmax=lmax,mmax=lmax,nmax=nmax,eta=eta,r0=r0)
    phi,afixed=pot.eval(y,pot=True,acc=True);phi=np.asarray(phi).copy();afixed=np.asarray(afixed).copy()
    k,dk=diagonal(r,nmax,lmax,eta,r0);phi-=G*m*k;afixed+=.5*(G*m*dk/r)[:,None]*y
    a=afixed-chain(np.sum(m[:,None]*afixed,axis=0))
    if not np.isfinite(a).all() or not np.isfinite(phi).all():raise FloatingPointError('nonfinite weighted SCF force')
    return a,.5*float(m@phi),phi
