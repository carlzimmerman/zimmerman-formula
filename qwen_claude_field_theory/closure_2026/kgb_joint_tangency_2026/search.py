#!/usr/bin/env python3
"""Search all four necessary joint equations, not optimizer success flags.

Four logarithmic parameters: |w1|/(.05*g1), y2, U2/eps2, y1.
Fixed global a0=1, eps1=1e-6, eps2=2e-6, X=.5, F=.525.
Only the negative-w, GR-connected pressure root is searched here. Other
branches are not excluded. A numerical joint point still needs mp refinement,
actual action checks, health, and higher preservation.
"""
import argparse
import json
import numpy as np
from scipy.optimize import least_squares
from derivatives.fast import single


def pair(theta,u1,f=1.):
    dw,y2,u2,y1=np.exp(theta)
    X,F=.5,.525
    base=single(1e-6,y1,X,1e-6*u1,-1,F,f)
    w1=-.05*dw*base['geometry']['g']
    a=single(1e-6,y1,X,1e-6*u1,w1,F,f)
    bb=single(2e-6,y2,X,2e-6*u2,-1,F,f)
    geo=bb['geometry'];aa=geo['g']+2/geo['r']
    disc=aa*aa+1.5*geo['B']*a['P']/F
    if disc<=0:raise ValueError('nonreal pressure root')
    w2=geo['B']*a['P']/(aa+np.sqrt(disc))
    b=single(2e-6,y2,X,2e-6*u2,w2,F,f)
    for row in (a,b):
        if min(row['Dcoord'],row['geometry']['B'],row['U'])<=0 or not row['w']:
            raise ValueError('invalid coordinate chart')
        if not np.all(np.isfinite(np.r_[row['A'],row['B'],row['N'],row['P'],row['H'],row['Gamma']])):
            raise ValueError('nonfinite coefficients')
    return a,b


def angle(a,b,scale):
    aa,bb=a/scale,b/scale
    den=np.linalg.norm(aa)*np.linalg.norm(bb)
    if den==0:raise ValueError('zero preservation vector: separate chart required')
    return (aa[0]*bb[1]-aa[1]*bb[0])/den


def control(a,b,scale):
    aa,bb=a/scale,b/scale
    den=np.dot(bb,bb)
    if den==0:raise ValueError('zero control vector')
    return -np.dot(aa,bb)/den


def evaluate(theta,u1):
    a,b=pair(theta,u1)
    A,B=a['A']-b['A'],a['B']-b['B']
    scale=np.maximum(np.maximum(abs(a['A']),abs(b['A'])),1.)
    f=control(A,B,scale)
    a,b=pair(theta,u1,f)
    if f==0 or a['Dfield']==0:raise ValueError('singular field map')
    N=a['N']-b['N'];next_scale=np.maximum(np.maximum(abs(a['N']),abs(b['N'])),1.)
    j=control(N,B,next_scale)
    residual=np.array([(a['H']-b['H'])/(1+abs(a['H'])+abs(b['H'])),
                       (a['Gamma']-b['Gamma'])/(1+abs(a['Gamma'])+abs(b['Gamma'])),
                       angle(A,B,scale),angle(N,B,next_scale)])
    return a,b,f,j,residual


def inspect(theta,u1):
    a,b,f,j,residual=evaluate(theta,u1)
    def jets(row):
        return np.r_[row['P'],f*row['K'],f*row['Gamma'],
                     j*np.array([row['K'],row['Gamma']])+f*(row['A']+f*row['B'])]
    ja,jb=jets(a),jets(b)
    rel=(ja-jb)/np.maximum(np.maximum(abs(ja),abs(jb)),1.)
    N=a['N']-b['N'];B=a['B']-b['B'];A=a['A']-b['A']
    first_rel=(A+f*B)/(1+abs(A)+abs(f*B))
    next_rel=(N+j*B)/(1+abs(N)+abs(j*B))
    return dict(parameters=np.exp(theta).tolist(),u1=u1,f=float(f),j=float(j),
                residual=residual.tolist(),five_jet_relative=rel.tolist(),first_relative=first_rel.tolist(),next_relative=next_rel.tolist(),
                Dfield=float(a['Dfield']),Dcoord=[float(r['Dcoord']) for r in (a,b)],
                accepted_numerical_joint=bool(max(abs(residual))<1e-8 and max(abs(rel))<1e-8
                    and max(abs(first_rel))<1e-8 and max(abs(next_rel))<1e-8))


def solve(start,u1,max_nfev=1000):
    lower=np.log([.01,1e-4,1e-6,1e-4]);upper=np.log([1e7,10,1e6,10])
    def residual(theta):
        return evaluate(theta,u1)[4]
    opt=least_squares(residual,np.log(start),bounds=(lower,upper),jac='3-point',x_scale='jac',
                      xtol=3e-13,ftol=3e-13,gtol=3e-13,max_nfev=max_nfev)
    row=inspect(opt.x,u1)
    row.update(nfev=opt.nfev,optimizer_status=opt.status,
               bound_distance=float(min(np.min(opt.x-lower),np.min(upper-opt.x))),
               actual_jacobian_singular_values=np.linalg.svd(opt.jac,compute_uv=False).tolist())
    return row


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-nfev',type=int,default=1000)
    parser.add_argument('--u1',type=float,nargs='+',default=[.03,.128,.5,2,10,100,1000])
    args=parser.parse_args();rows=[]
    for u1 in args.u1:
        for y1 in (.03,.1,.3):
            start=[4164.89540032022,1.537936934617971*y1,.86686081999816*u1,y1]
            try:row=solve(start,u1,args.max_nfev)
            except (ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:row=dict(error=str(exc))
            row.update(start=start,u1=u1,max_nfev=args.max_nfev)
            rows.append(row);print('JOINT='+json.dumps(row,allow_nan=False),flush=True)
    print('SUMMARY='+json.dumps(dict(attempts=len(rows),numerical_joint=sum(r.get('accepted_numerical_joint',False) for r in rows),
          scope='Finite deterministic joint-root search; not interval certification or full-theory proof')))


if __name__=='__main__':main()
