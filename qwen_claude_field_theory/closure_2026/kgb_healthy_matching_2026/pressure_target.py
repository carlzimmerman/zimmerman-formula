#!/usr/bin/env python3
"""One shared second-order metric freedom, not a change of MOND kernel.

B=B_log*(1+eta*(r*y)^2); fixed finite eta preserves leading weak no-slip,
not exact logarithmic no-slip at finite field. PPN and sources remain open.
"""
from functools import lru_cache
import importlib.util
from pathlib import Path
import json
import mpmath as mp
import numpy as np
import sympy as s

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'kgb_logslip_joint_2026'

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
    return model

base=load('healthy_target_base',OLD/'fast.py')

@lru_cache(None)
def geometry_kernel():
    eps,y,mu,e,eta=s.symbols('eps y mu e eta',real=True)
    Dy=lambda a:s.diff(a,y)+e*s.diff(a,mu)-e*s.diff(a,e)
    r=eps/s.sqrt(y*mu);ry=Dy(r);Dr=lambda a:Dy(a)/ry
    h=r*y;t=2/(1+s.sqrt(1-4*h));d=1+eta*h*h
    B=t*t*d;g=y*B;Br=Dr(B);gr=Dr(g)
    rho=y*(t+1+eta*h)/(d*r)+Br/(B*B*r)
    pr=y*y*(-t*t+eta*(2*h-1))/d
    pt=(gr+g*g-g*Br/(2*B)+(g-Br/(2*B))/r)/B
    names=['r','ry'];values=[r,ry]
    for key,q in [('g',g),('B',B),('rho',rho),('pr',pr),('pt',pt)]:
        names.extend([key,key+'r',key+'rr']);values.extend([q,Dr(q),Dr(Dr(q))])
    return s.lambdify((eps,y,mu,e,eta),values,'numpy',cse=True,docstring_limit=0),names

def single(eps,y,X,U,w,F,f,eta=0):
    geo,names=geometry_kernel();_,oldnames,jet=base.kernels()
    if names!=oldnames:raise ValueError('geometry ordering mismatch')
    vals=geo(eps,y,-np.expm1(-y),np.exp(-y),eta)
    g=dict(zip(names,vals));g.update(eps=eps,y=y,eta=eta)
    h=g['r']*y
    if h>=.25 or min(g['B'],U,X,F)<=0:raise ValueError('outside target chart')
    out=jet(X,U,w,F,f,*vals)
    return dict(P=out[0],H=out[1],K=out[2],Gamma=out[3],W=out[4],
        A=np.asarray(out[5:7]),B=np.asarray(out[7:9]),N=np.asarray(out[9:11]),
        geometry=g,X=X,U=U,w=w,F=F,f=f,Dfield=2*(F-X*f),Dcoord=1+g['r']*w/(2*F),
        second_order_to_first_order=abs(eta*h))

def reference(eta):
    """Private reference module with explicit geometry dependency substitution."""
    ref=load('healthy_private_reference',OLD/'reference/logslip_reference.py')
    oldgeo=ref.geometry
    def geometry(eps,y):
        eps,y=map(mp.mpf,(eps,y));ee=mp.mpf(str(eta))
        a=oldgeo(eps,y);r=a['r'];h=r*y;d=1+ee*h*h
        B=a['B']*d;Br=a['Br']*d+a['B']*2*ee*h*(y+r/a['ry'])
        g=y*B;gr=B/a['ry']+y*Br
        return dict(**ref.general.metric_invariants(r,B,Br,g,gr),eps=eps,y=y,ry=a['ry'],eta=ee)
    ref.geometry=geometry
    return ref

if __name__=='__main__':
    print(json.dumps(single(1e-6,.1,.5,.00475,-1533,.525,3.3,100),
        default=lambda v:v.tolist() if isinstance(v,np.ndarray) else str(v)))
