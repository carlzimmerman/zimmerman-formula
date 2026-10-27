"""Independent finite diagnostic reference functions, never an evolution solver."""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scf_backend import G


def direct_sample(x,m,ids,eps):
    out=np.empty((len(ids),3));phi=np.empty(len(ids))
    for k,i in enumerate(ids):
        delta=x-x[i];r2=np.einsum('ij,ij->i',delta,delta)+eps*eps
        r2[i]=np.inf
        inv=1/np.sqrt(r2)
        out[k]=G*np.sum((m*inv**3)[:,None]*delta,axis=0)
        phi[k]=-G*float(m@inv)
    return out,phi


def ellipsoid_field(x,mass,axes):
    """Uniform ellipsoid, principal coordinates; exact integral, numerical quadrature.

    Dimensionless integration variable u=physical_u/max(axes)^2. The lower
    confocal coordinate is zero inside. Quad tolerances are reference accuracy
    settings, not a rigorous interval certificate.
    """
    scale=float(np.max(axes));b2=(np.asarray(axes)/scale)**2
    acc=np.empty_like(np.asarray(x));phi=np.empty(len(x))
    for k,p in enumerate(np.asarray(x)/scale):
        fun=lambda u: np.sum(p*p/(b2+u))-1
        if fun(0)<=0:lam=0.
        else:lam=brentq(fun,0.,max(1.,float(p@p)))
        D=lambda u: np.sqrt(np.prod(b2+u))
        potint=quad(lambda u:(1.-np.sum(p*p/(b2+u)))/D(u),lam,np.inf,
                    epsabs=2e-12,epsrel=2e-12,limit=150)[0]
        phi[k]=-3*G*mass/(4*scale)*potint
        for j in range(3):
            integ=quad(lambda u:1./((b2[j]+u)*D(u)),lam,np.inf,
                       epsabs=2e-12,epsrel=2e-12,limit=150)[0]
            acc[k,j]=-3*G*mass/(2*scale**2)*p[j]*integ
    return acc,phi


def force_metrics(a,b):
    delta=np.linalg.norm(a-b,axis=1);scale=np.linalg.norm(b,axis=1)
    denom=float(np.linalg.norm(b));positive=scale>0
    return dict(L2_relative=float(np.linalg.norm(a-b)/denom) if denom else None,
                absolute_max=float(delta.max()),absolute_median=float(np.median(delta)),
                relative_median=float(np.median(delta[positive]/scale[positive])) if np.any(positive) else None,
                relative_max=float(np.max(delta[positive]/scale[positive])) if np.any(positive) else None)


def unit_check(agama):
    state=dict(G=float(agama.G),units=agama.getUnits())
    if state['G']!=1. or state['units']!={}:raise RuntimeError('candidate requires pristine native Agama G=1 units')
    # An independent point-mass normalization check authenticates the source
    # mass G*m conversion, beyond the internally homogeneous gradient tests.
    p=agama.Potential(type='Plummer',mass=G*7.,scaleRadius=2.)
    actual=p.force(np.array([[3.,0.,0.]]))[0]
    expected=np.array([-G*7.*3./13.**1.5,0.,0.])
    if not np.allclose(actual,expected,rtol=3e-15,atol=1e-18):raise AssertionError('physical G normalization mismatch')
    state['physical_G']=G;state['independent_Plummer_force']=actual.tolist()
    return state
