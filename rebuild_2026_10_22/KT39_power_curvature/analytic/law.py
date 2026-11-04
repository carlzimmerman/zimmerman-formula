"""KT39 phenomenological power curvature: z=x+s**p, P=xR(z).

Two shared searched parameters p and physical ell. Scalar Q/R functions
are imported read-only from KT37, with unchanged simple nu and Q(0)=0.
"""
import importlib.util
from pathlib import Path
import numpy as np

_PRIMITIVE_PATH=Path(__file__).resolve().parents[2]/'KT37_generalized_action/analytic/law.py'
_spec=importlib.util.spec_from_file_location('kt39_readonly_kt37_primitive',_PRIMITIVE_PATH)
_primitive=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_primitive)
Q=_primitive.Q
Qprime=_primitive.Qprime
Qsecond=_primitive.Qsecond
R=_primitive.R
Rminus1=_primitive.Rminus1
Rprime=_primitive.Rprime
Rsecond=_primitive.Rsecond
zRprime=_primitive.zRprime
evaluate=_primitive.evaluate  # P=xR(z): these invariant partials are unchanged.


def tensor_terms(g,H,ell,a0=1.,newtonian=False,p=1.5):
    """Return E=a0^2 P, A=.5E_g-g, B=.5E_H and invariants.

    g is acceleration, H acceleration/length, ell a physical length. Full
    Frobenius contraction counts both off-diagonal entries. No floor is used.
    The anomalous source is div(A)-partial_i partial_j(B_ij).
    """
    g=np.asarray(g,dtype=float);H=np.asarray(H,dtype=float)
    if g.ndim<1 or H.shape[-2:]!=(g.shape[-1],g.shape[-1]):
        raise ValueError('g/H vector and square-tensor axes mismatch')
    if ell<0 or a0<=0 or not np.isfinite(p) or p<1:raise ValueError('ell>=0,a0>0 and finite p>=1 required')
    g2=np.sum(g*g,axis=-1);h2=np.sum(H*H,axis=(-2,-1))
    x=g2/(a0*a0);s=(ell*ell/(a0*a0))*h2;z=x+s**p
    if newtonian:
        return dict(energy=g2,P=x,A=np.zeros_like(g),B=np.zeros_like(H),x=x,s=s,z=z,
                    C=np.zeros_like(x),D=np.zeros_like(x),B_coefficient=np.zeros_like(x))
    rm=Rminus1(z);d=zRprime(z);mask=z>0;f=np.zeros_like(z)
    np.divide(x,z,out=f,where=mask)
    c=np.zeros_like(z);bc=np.zeros_like(z);energy=np.zeros_like(z)
    c[mask]=rm[mask]+f[mask]*d[mask]
    bc[mask]=p*ell*ell*s[mask]**(p-1)*f[mask]*d[mask]
    energy[mask]=g2[mask]*(1+rm[mask])
    return dict(energy=energy,P=energy/(a0*a0),A=c[...,None]*g,B=bc[...,None,None]*H,
                x=x,s=s,z=z,C=c,D=d,B_coefficient=bc)
