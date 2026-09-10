#!/usr/bin/env python3
"""Cached analytic shared-action derivatives; no matching or health decisions.

single(eps,y,X,U,w,F,f) evaluates normalized K=P_X/f and Gamma=G_X/f,
A=L0(K,Gamma), B=L1(K,Gamma), N=(L0+fL1)(A+fB) at fixed f.
The last derivative includes the changing vector field; L0,L1 do not commute.
Regular physical chart: positive eps,y,X,U,F and metric B, nonzero f,w.
The analytic kernels deliberately impose no numerical rank or health cutoff.
Complex inputs are supported locally on the same square-root branch.
"""
from functools import lru_cache
import argparse
import json
import time
import numpy as np
import sympy as s


@lru_cache(None)
def _kernels():
    started=time.perf_counter()
    eps,y,mu,e=s.symbols('eps y mu e',nonzero=True)
    # Keep mu=-expm1(-y) as an input to avoid small-y subtraction loss.
    Dy=lambda expression:s.diff(expression,y)+e*s.diff(expression,mu)-e*s.diff(expression,e)
    r=eps/s.sqrt(y*mu);ry=Dy(r)
    metricB=1/(1-2*r*y);g=y*metricB
    rho=4*y*y*e/(r*(mu+y*e))
    Dr=lambda expression:Dy(expression)/ry
    gr=Dr(g);rhor=Dr(rho)
    names=('r','ry','g','gr','grr','rho','rhor','rhorr','B','Br')
    geometry=s.lambdify((eps,y,mu,e),(r,ry,g,gr,Dr(gr),rho,rhor,Dr(rhor),metricB,Dr(metricB)),
                        modules='numpy',cse=True,docstring_limit=0)

    X,F,r,g,gr,grr,rho,rhor,rhorr,U,w,f=s.symbols(
        'X F r g gr grr rho rhor rhorr U w f',nonzero=True)
    metricB=1+2*r*g;b=(g+r*gr)/metricB;p=s.sqrt(metricB*U)
    Q=2*X+U;a=g+2/r
    P=(2*w*a+s.Rational(3,2)*w*w/F)/metricB
    L=2*F*rho+2*w*(g+b)/metricB+3*w*w/(F*metricB)
    S=2*F*a*rho+4*w*(r*g-1)/(r*r*metricB)
    Gamma=p*r*S/(2*Q*w)
    W=metricB*(L-X*r*S/Q)/2
    H=((2/r+w/F)*U-(2*g+w/F)*X)/p
    K=2*P/F+H*Gamma
    L0=lambda expression:s.diff(expression,X)-2*s.diff(expression,U)
    def L1(expression):
        radial=(s.diff(expression,r)+gr*s.diff(expression,g)+grr*s.diff(expression,gr)
                +rhor*s.diff(expression,rho)+rhorr*s.diff(expression,rhor))
        return s.diff(expression,F)+(radial+W*s.diff(expression,w)-2*g*Q*s.diff(expression,U))/w
    A=(-2*Gamma*(a+3*w/(2*F))/p,-Gamma/U)
    B=tuple(L1(q) for q in (K,Gamma))
    # Differentiating A+fB with f held fixed retains both mixed orders.
    N=tuple(L0(aa)+f*(L1(aa)+L0(bb))+f*f*L1(bb) for aa,bb in zip(A,B))
    output=(P,H,K,Gamma,*A,*B,*N,W,p,Q)
    args=(X,F,r,g,gr,grr,rho,rhor,rhorr,U,w,f)
    jets=s.lambdify(args,output,modules='numpy',cse=True,docstring_limit=0)
    return geometry,names,jets,time.perf_counter()-started


def single(eps,y,X,U,w,F,f):
    """Return P,H,K,Gamma,A(2),B(2),N(2), W, geometry and regularity data.

    B is the two-component derivative coefficient, not metric B. Access the
    latter as result['geometry']['B']. No field-map admissibility is implied.
    """
    geo,names,jets,_=_kernels()
    values=geo(eps,y,-np.expm1(-y),np.exp(-y))
    geometry=dict(zip(names,values));geometry.update(eps=eps,y=y)
    out=jets(X,F,*(geometry[key] for key in ('r','g','gr','grr','rho','rhor','rhorr')),U,w,f)
    P,H,K,Gamma=out[:4]
    return dict(P=P,H=H,K=K,Gamma=Gamma,kappa=K,gamma=Gamma,
                A=np.asarray(out[4:6]),B=np.asarray(out[6:8]),N=np.asarray(out[8:10]),
                W=out[10],p=out[11],Q=out[12],geometry=geometry,
                X=X,U=U,w=w,F=F,f=f,Dfield=2*(F-X*f),Dcoord=1+geometry['r']*w/(2*F))


def benchmark(repeats=1000):
    """Bounded warm-evaluation timing, no optimization or physical verdict."""
    if repeats<1:raise ValueError('repeats must be positive')
    point=(1e-6,.1,.5,3e-8,-20.8245196960960745,.525,259.6853685595673)
    row=single(*point)
    started=time.perf_counter()
    for _ in range(repeats):single(*point)
    elapsed=time.perf_counter()-started
    return dict(compile_seconds=_kernels()[3],repeats=repeats,warm_seconds=elapsed,
                seconds_per_single=elapsed/repeats,N=row['N'].tolist(),
                scope='Timing and one evaluator output only; no joint root or health conclusion')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repeats',type=int,default=1000)
    args=parser.parse_args();print(json.dumps(benchmark(args.repeats),indent=2))
