"""Milgrom2305.01589v2 Eq16 with Q'=simple nu(sqrt(z)), Q(0)=0.

P=xQ(z)/z; x=|g|²/a0²,z=x+ell²(H:H)/a0². tensor_terms returns the
dimensional energy a0²P and half-partials A=.5 E_g-g, B=.5 E_H.
No physical regularization floor, file writes, imports of empirical solvers,
or global-state mutation. Full Frobenius contraction includes both offdiagonals.
"""
import math
import numpy as np


# Q=.5*u^4+sum c_k*u^(2k+3), u=z^1/4. Eight correction terms suffice
# below u=.25, where the neglected term is below float64 rounding.
_SERIES=[]
_binomial=1.
for _k in range(9):
    if _k:_binomial*=((.5-(_k-1))/_k)
    _SERIES.append((2*_k-1,4*_binomial/(4.**_k*(2*_k+3))))
_SERIES=tuple(_SERIES)


def _input(z):
    z=np.asarray(z,dtype=float)
    if np.any(z<0) or np.any(~np.isfinite(z)):
        raise ValueError('z must be nonnegative and finite')
    return z


def _coefficients(z):
    """Return R-1 and D=zR', retaining small high-field differences."""
    z=_input(z);u=z**.25
    rm=np.empty_like(z);d=np.empty_like(z)
    zero=z==0;small=(u<.25)&~zero;large=~(zero|small)
    rm[zero]=np.inf;d[zero]=-np.inf
    if np.any(small):
        us=u[small];rms=np.full_like(us,-.5);ds=np.zeros_like(us)
        for power,coefficient in _SERIES:
            term=coefficient*us**power
            rms+=term;ds+=(power/4)*term
        rm[small]=rms;d[small]=ds
    if np.any(large):
        ul=u[large];y=ul*ul;root=np.sqrt(1+4/y)
        delta=4/(y*(root+1))
        rm[large]=.5*delta+1/y+delta/y-4*np.arcsinh(ul/2)/z[large]
        d[large]=.5*delta-rm[large]
    return rm,d


def Rminus1(z):return _coefficients(z)[0]
def R(z):return 1+Rminus1(z)
def zRprime(z):return _coefficients(z)[1]


def Rprime(z):
    z=_input(z)
    with np.errstate(divide='ignore',over='ignore'):
        return zRprime(z)/z


def Q(z):
    z=_input(z);out=np.zeros_like(z);mask=z>0
    out[mask]=z[mask]*R(z[mask])
    return out


def Qprime(z):
    z=_input(z)
    with np.errstate(divide='ignore'):
        return .5+np.sqrt(.25+1/np.sqrt(z))


def Qsecond(z):
    z=_input(z)
    with np.errstate(divide='ignore',over='ignore'):
        u=z**.25
        return -np.exp(-math.log(2)-5*np.log(u)-.5*np.log(u*u+4))


def Rsecond(z):
    z=_input(z)
    with np.errstate(divide='ignore',invalid='ignore',over='ignore'):
        out=(Qsecond(z)-2*Rprime(z))/z
    return np.where(z==0,np.inf,out)


def evaluate(x,z,newtonian=False):
    """Invariant partials treating x,z as independent: P=xR,Px=R,Pz=xR'.

    At x=z=0, P=0, Pz=0 is the fixed-x partial; Px=+inf. The partials
    in invariant coordinates are singular, but tensor_terms is continuous.
    """
    x,z=np.broadcast_arrays(np.asarray(x,dtype=float),_input(z))
    if np.any(x<0):raise ValueError('x must be nonnegative')
    if newtonian:return dict(P=x.copy(),Px=np.ones_like(x),Pz=np.zeros_like(x))
    if np.any((z==0)&(x!=0)):raise ValueError('x must vanish when z is zero')
    r=R(z);d=zRprime(z);f=np.zeros_like(z);np.divide(x,z,out=f,where=z>0)
    value=np.zeros_like(z);pz=np.zeros_like(z);mask=z>0
    value[mask]=x[mask]*r[mask];pz[mask]=f[mask]*d[mask]
    return dict(P=value,Px=r,Pz=pz)


def tensor_terms(g,H,ell,a0=1.,newtonian=False):
    """Physical energy and response tensors; g(...,d), H(...,d,d).

    Acceleration units for g and a0 must match. H is acceleration/length,
    and ell has that same length unit. A has acceleration units; B has
    acceleration*length units. Phantom source is div A-double_div B.
    """
    g=np.asarray(g,dtype=float);H=np.asarray(H,dtype=float)
    if g.ndim<1 or H.shape[-2:]!=(g.shape[-1],g.shape[-1]):
        raise ValueError('g/H vector and square-tensor axes mismatch')
    if ell<0 or a0<=0:raise ValueError('ell>=0 and a0>0 required')
    g2=np.sum(g*g,axis=-1);h2=np.sum(H*H,axis=(-2,-1))
    x=g2/(a0*a0);z=x+(ell*ell/(a0*a0))*h2
    if newtonian:
        return dict(energy=g2,P=x,A=np.zeros_like(g),B=np.zeros_like(H),x=x,z=z,
                    C=np.zeros_like(x),D=np.zeros_like(x))
    rm,d=_coefficients(z);mask=z>0;f=np.zeros_like(z)
    np.divide(x,z,out=f,where=mask)
    c=np.zeros_like(z);bc=np.zeros_like(z);energy=np.zeros_like(z)
    c[mask]=rm[mask]+f[mask]*d[mask]
    bc[mask]=ell*ell*f[mask]*d[mask]
    energy[mask]=g2[mask]*(1+rm[mask])
    A=c[...,None]*g;B=bc[...,None,None]*H
    return dict(energy=energy,P=energy/(a0*a0),A=A,B=B,x=x,z=z,C=c,D=d)
