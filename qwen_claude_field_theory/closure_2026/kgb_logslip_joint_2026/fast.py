#!/usr/bin/env python3
"""Analytic general-pressure jets on the selected logarithmic-slip target.

Geometry and action kernels are separate. No health or matching verdicts.
The simplification uses the geometric Bianchi identity, checked independently
against the original general-pressure 3x3 inverse.
"""
from functools import lru_cache
import json
import numpy as np
import sympy as s


@lru_cache(None)
def kernels():
    eps,y,mu,e=s.symbols('eps y mu e',nonzero=True)
    Dy=lambda q:s.diff(q,y)+e*s.diff(q,mu)-e*s.diff(q,e)
    r=eps/s.sqrt(y*mu);ry=Dy(r)
    Dr=lambda q:Dy(q)/ry
    btarget=2/(1+s.sqrt(1-4*r*y));B=btarget*btarget;g=y*B
    Br=Dr(B);gr=Dr(g)
    # B-1 = (r*y)*B*(sqrt(B)+1), and pt=-pr on this target.
    # These exact geometric identities avoid weak-field subtraction loss.
    rho=y*(btarget+1)/r+Br/(B**2*r)
    pr=-g*g/B
    pt=g*g/B
    names=['r','ry'];values=[r,ry]
    for key,q in [('g',g),('B',B),('rho',rho),('pr',pr),('pt',pt)]:
        names.extend([key,key+'r',key+'rr']);values.extend([q,Dr(q),Dr(Dr(q))])
    geo=s.lambdify((eps,y,mu,e),values,modules='numpy',cse=True,docstring_limit=0)

    X,U,w,F,f=s.symbols('X U w F f',nonzero=True)
    symbols=s.symbols(' '.join(names),nonzero=True)
    v=dict(zip(names,symbols));r=v['r'];g=v['g'];B=v['B'];b=v['Br']/(2*B)
    rho,pr,pt=v['rho'],v['pr'],v['pt'];p=s.sqrt(B*U);Q=2*X+U;a=g+2/r
    P=2*F*pr+(2*w*a+s.Rational(3,2)*w*w/F)/B
    S=4*F*(rho+pt)/r+4*w*(r*g-1)/(B*r*r)
    Gamma=p*r*S/(2*Q*w)
    L=2*F*(rho+pr)+2*w*(g+b)/B+3*w*w/(F*B)
    W=B*(L-2*X*w*Gamma/p)/2
    H=((2/r+w/F)*U-(2*g+w/F)*X)/p
    K=2*P/F+H*Gamma
    def L1(expression):
        radial=s.diff(expression,r)
        for key in ('g','B','rho','pr','pt'):
            radial+=v[key+'r']*s.diff(expression,v[key])+v[key+'rr']*s.diff(expression,v[key+'r'])
        return s.diff(expression,F)+(radial+W*s.diff(expression,w)-2*g*Q*s.diff(expression,U))/w
    L0=lambda q:s.diff(q,X)-2*s.diff(q,U)
    A=(-2*Gamma*(a+3*w/(2*F))/p,-Gamma/U)
    BB=tuple(L1(q) for q in (K,Gamma))
    N=tuple(L0(aa)+f*(L1(aa)+L0(bb))+f*f*L1(bb) for aa,bb in zip(A,BB))
    jet=s.lambdify((X,U,w,F,f,*symbols),(P,H,K,Gamma,W,*A,*BB,*N),modules='numpy',cse=True,docstring_limit=0)
    return geo,names,jet


def single(eps,y,X,U,w,F,f):
    geo,names,jet=kernels();values=geo(eps,y,-np.expm1(-y),np.exp(-y))
    geometry=dict(zip(names,values));geometry.update(eps=eps,y=y)
    out=jet(X,U,w,F,f,*values)
    return dict(P=out[0],H=out[1],K=out[2],Gamma=out[3],W=out[4],
                A=np.asarray(out[5:7]),B=np.asarray(out[7:9]),N=np.asarray(out[9:11]),
                geometry=geometry,X=X,U=U,w=w,F=F,f=f,
                Dfield=2*(F-X*f),Dcoord=1+geometry['r']*w/(2*F))


if __name__=='__main__':
    row=single(1e-6,.1,.5,.004754976244,-1533.523854,.525,3.29992587867)
    print(json.dumps({k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in row.items()},allow_nan=False))
