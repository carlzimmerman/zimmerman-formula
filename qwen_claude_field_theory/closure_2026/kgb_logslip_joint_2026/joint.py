#!/usr/bin/env python3
"""Four-variable common-action search on the corrected pressure target.

The eliminated pressure equation contains P1-2F*pr2; omitting that term
would silently restore the previous zero-pressure model.
"""
import json
import numpy as np
from scipy.optimize import least_squares
from fast import single


def pair(x,y1=.1,f=1.):
    dw,y2,u2,u1=np.exp(x);X,F=.5,.525
    first=single(1e-6,y1,X,1e-6*u1,-1,F,f)
    w1=-.05*dw*first['geometry']['g']
    a=single(1e-6,y1,X,1e-6*u1,w1,F,f)
    bb=single(2e-6,y2,X,2e-6*u2,-1,F,f);geo=bb['geometry']
    aa=geo['g']+2/geo['r'];target=a['P']-2*F*geo['pr']
    disc=aa*aa+1.5*geo['B']*target/F
    if disc<=0:raise ValueError('pressure root chart failed')
    w2=geo['B']*target/(aa+np.sqrt(disc))
    b=single(2e-6,y2,X,2e-6*u2,w2,F,f)
    for row in (a,b):
        if min(row['Dcoord'],row['geometry']['B'],row['U'])<=0 or row['w']==0:
            raise ValueError('outside regular chart')
        if not np.all(np.isfinite(np.r_[row['A'],row['B'],row['N'],row['P'],row['K'],row['Gamma']])):
            raise ValueError('nonfinite inverse')
    return a,b


def control(A,B,scale):
    aa,bb=A/scale,B/scale;den=np.dot(bb,bb)
    if den==0:raise ValueError('separate zero-control chart required')
    return -np.dot(aa,bb)/den


def angle(A,B,scale):
    a,b=A/scale,B/scale;den=np.linalg.norm(a)*np.linalg.norm(b)
    if den==0:raise ValueError('separate degenerate-vector chart required')
    return (a[0]*b[1]-a[1]*b[0])/den


def inspect(x,y1=.1):
    a,b=pair(x,y1);A=a['A']-b['A'];B=a['B']-b['B']
    scale=np.maximum(np.maximum(abs(a['A']),abs(b['A'])),1.)
    f=control(A,B,scale)
    a,b=pair(x,y1,f)
    if not f or not a['Dfield']:raise ValueError('singular field map')
    N=a['N']-b['N'];ns=np.maximum(np.maximum(abs(a['N']),abs(b['N'])),1.)
    j=control(N,B,ns)
    residual=np.r_[(a['H']-b['H'])/(1+abs(a['H'])+abs(b['H'])),
        (a['Gamma']-b['Gamma'])/(1+abs(a['Gamma'])+abs(b['Gamma'])),angle(A,B,scale),angle(N,B,ns)]
    def jets(r):return np.r_[r['P'],f*r['K'],f*r['Gamma'],j*np.array([r['K'],r['Gamma']])+f*(r['A']+f*r['B'])]
    aa,bb=jets(a),jets(b);raw=(aa-bb)/np.maximum(np.maximum(abs(aa),abs(bb)),1.)
    first=(A+f*B)/(1+abs(A)+abs(f*B));nxt=(N+j*B)/(1+abs(N)+abs(j*B))
    return dict(parameters=np.exp(x).tolist(),y1=y1,f=f,j=j,residual=residual.tolist(),
        five_jet_relative=raw.tolist(),first_relative=first.tolist(),next_relative=nxt.tolist(),
        accepted_numerical_joint=bool(max(abs(np.r_[residual,raw,first,nxt]))<1e-8),
        states=[{key:(r['geometry'][key] if key in ('eps','y') else r[key]) for key in ('eps','y','X','U','w','F')} for r in (a,b)])


def solve(start,y1=.1,max_nfev=300):
    lo=np.log([.01,1e-4,1e-6,.0001]);hi=np.log([1e7,10,5000,10000])
    out=least_squares(lambda x:inspect(x,y1)['residual'],np.log(start),bounds=(lo,hi),
        jac='3-point',x_scale='jac',ftol=3e-13,gtol=3e-13,xtol=3e-13,max_nfev=max_nfev)
    row=inspect(out.x,y1);row.update(nfev=out.nfev,optimizer_status=out.status,start=list(start),
        actual_jacobian_singular_values=np.linalg.svd(out.jac,compute_uv=False).tolist())
    return row


if __name__=='__main__':
    seed=[306704.14201367765,.18007338443212362,3057.78268757124,4754.976244115166]
    print('JOINT='+json.dumps(solve(seed),allow_nan=False))
