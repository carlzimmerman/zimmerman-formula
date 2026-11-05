"""Fixed-length generalized QUMOND finite energy, with full weighted adjoints.

Coordinates are kpc; potentials are in a0*kpc, so gradients are in a0 and
covariant Hessian components are in a0/kpc. No Gaussian filter is used.
"""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/'KT34_reciprocal_epsilon_scan/mw'))
sys.path.insert(0,str(BASE/'KT37_generalized_action/analytic'))
import scan as E
import law as L
M,np=E.M,E.np
from scipy.sparse import csr_matrix,diags


def odd_theta_derivative(g):
    """(1/r)d/dtheta of an odd polar vector component at mirror boundaries."""
    nr,nt=g.Nr,g.Nt
    I=np.arange(g.n).reshape(nr,nt);j=np.arange(nt)
    jm=np.maximum(j-1,0);jp=np.minimum(j+1,nt-1)
    tm=np.where(j>0,g.tc[jm],-g.tc[0])
    outer=2*np.pi-g.tc[-1] if g.full else np.pi-g.tc[-1]
    tp=np.where(j<nt-1,g.tc[jp],outer)
    den=g.rc[:,None]*(tp-tm)[None,:]
    plus=np.where(j==nt-1,-1.,1.)[None,:]/den
    minus=-np.where(j==0,-1.,1.)[None,:]/den
    rows=np.concatenate([I.ravel(),I.ravel()])
    cols=np.concatenate([(np.arange(nr)[:,None]*nt+jp).ravel(),(np.arange(nr)[:,None]*nt+jm).ravel()])
    return csr_matrix((np.concatenate([plus.ravel(),minus.ravel()]),(rows,cols)),shape=(g.n,g.n))


class Generalized:
    """Derivative of Eph=-(8pi)^-1 sum W*x*(R(z)-1)."""
    multiplicity=np.array([1.,2.,1.,1.])

    def __init__(self,solver):
        self.sol=solver;self.g=solver.g;g=self.g
        dr,dt=g.Crr,g.Cth
        invr=diags(1/g.r2d)
        self.dt_odd=odd_theta_derivative(g)
        self.grad=(dr,dt)
        self.hess=(
            (dr@dr).tocsr(),
            (.5*(dt@dr-invr@dt+dr@dt)).tocsr(),
            (self.dt_odd@dt+invr@dr).tocsr(),
            (invr@dr+diags(np.cos(g.t2d)/(g.r2d*np.sin(g.t2d)))@dt).tocsr())

    def fields(self,psi):
        return np.array([d@psi for d in self.grad]),np.array([d@psi for d in self.hess])

    @staticmethod
    def coefficients(gg,hh,ell,newtonian=False):
        x=np.sum(gg*gg,axis=0)
        h2=np.sum(Generalized.multiplicity[:,None]*hh*hh,axis=0)
        z=x+ell*ell*h2
        A=np.zeros_like(gg);B=np.zeros_like(hh);energy=np.zeros_like(x)
        if newtonian:return A,B,energy,z
        active=z>0
        if np.any(active):
            zz=z[active];ratio=x[active]/zz
            excess=L.Rminus1(zz)
            dd=L.zRprime(zz)
            cc=excess+ratio*dd
            A[:,active]=cc*gg[:,active]
            B[:,active]=ell*ell*ratio*dd*hh[:,active]
            energy[active]=x[active]*excess
        return A,B,energy,z

    def source(self,psi,ell,newtonian=False,fields=None):
        gg,hh=self.fields(psi) if fields is None else fields
        A,B,e,z=self.coefficients(gg,hh,ell,newtonian)
        w=self.g.vol
        first=sum(op.T@(w*a) for op,a in zip(self.grad,A))
        second=sum(m*op.T@(w*b) for m,op,b in zip(self.multiplicity,self.hess,B))
        source=-(first+second)/w
        return source,dict(energy=-float(w@e)/(8*np.pi),
            gradient_source_norm=float(np.linalg.norm(first/w)),hessian_source_norm=float(np.linalg.norm(second/w)),
            z_min=float(z.min()),z_max=float(z.max()),finite=bool(np.all(np.isfinite(source))))

    def phantom(self,psi,ell,newtonian=False,fields=None):
        b,stats=self.source(psi,ell,newtonian,fields)
        if not stats['finite']:raise FloatingPointError('Nonfinite generalized source')
        return self.sol.LU.lu.solve(b),stats

    def energy(self,rho,ell):
        psi=self.sol.LU.newton(rho)
        gg,hh=self.fields(psi)
        return -float(self.g.vol@self.coefficients(gg,hh,ell)[2])/(8*np.pi)

    def response(self,rho,ell):
        psi=self.sol.LU.newton(rho)
        ph,stats=self.phantom(psi,ell)
        return psi+ph,stats
