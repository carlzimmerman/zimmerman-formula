#!/usr/bin/env python3
"""Bounded signed common-F_X search with no artificial negative-w cap.

F,X and a0 are common. Both negative w charts obey Dcoord>0 by construction.
Actual five-jet residuals, not optimizer success, decide initial matching.
"""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import least_squares
from scipy.special import expit

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(HERE.parent/'structure'))
import universal_seed as s
import closed_inverse as c


def normalized_jet(eps,y,X,U,w,F,f):
    a=c.normalized(eps,y,X,U,w,F)
    point=np.array([y,X,U,w,F],dtype=float)
    tangent=np.array([f/(a['ry']*w),1.,-2-2*f*a['g']*a['Q']/w,f*a['W']/w,f])
    step=1e-25
    varied=c.normalized(eps,*(point+1j*step*tangent))
    derivatives=np.imag([varied['kappa'],varied['gamma']])/step
    return np.array([a['P'],a['kappa'],a['gamma'],*derivatives])


def pair(theta,sign,spec=s.Spec(),u1=.128):
    if sign not in (-1,1):raise ValueError('f sign must be -1 or +1')
    f=sign*np.exp(theta[0]);eta1,eta2=expit(theta[[1,4]])
    y2,u2=np.exp(theta[[2,3]])
    rows=[]
    for eps,y,u,eta in ((spec.eps1,spec.y1,u1,eta1),(spec.eps2,y2,u2,eta2)):
        r=c.geometry(eps,y)['r'];w=-2*spec.F*eta/r;U=eps*u
        a=c.coefficients(eps,y,spec.X,U,w,spec.F,f)
        rows.append((a,normalized_jet(eps,y,spec.X,U,w,spec.F,f)))
    return rows


def residual(theta,sign,spec=s.Spec(),u1=.128):
    a,b=pair(theta,sign,spec,u1)
    # Symmetric componentwise scale prevents a common tiny f from faking PX/GX matching.
    scale=np.sqrt(a[1]*a[1]+b[1]*b[1]+1e-40)
    return (a[1]-b[1])/scale


def inspect(theta,sign,spec=s.Spec(),u1=.128):
    rows=pair(theta,sign,spec,u1);values=[v for _,v in rows]
    relative=abs(values[0]-values[1])/np.maximum(np.maximum(abs(values[0]),abs(values[1])),1e-100)
    f=rows[0][0]['f'];original=[];consistency=[]
    for a,v in rows:
        _,raw=s.raw_jet(a['eps'],a['y'],spec.X,a['U'],a['z'],spec.F,f)
        normalized=raw.copy();normalized[1:]/=f;original.append(raw)
        consistency.append(float(max(abs(v-normalized)/np.maximum(np.maximum(abs(v),abs(normalized)),1.))))
    original_relative=abs(original[0]-original[1])/np.maximum(np.maximum(abs(original[0]),abs(original[1])),1e-100)
    regular=all(a['Dcoord']>0 and a['B']>0 and a['U']>0 and abs(a['Dfield'])>1e-8 for a,_ in rows)
    matched=bool(max(relative)<1e-7 and max(original_relative)<1e-7 and max(consistency)<2e-7 and regular)
    return dict(spec=asdict(spec),u1=u1,sign=sign,theta=np.asarray(theta).tolist(),f=float(f),
        states=[dict(eps=a['eps'],y=a['y'],U=a['U'],w=a['w'],z=a['z'],Dcoord=a['Dcoord'],Dfield=a['Dfield']) for a,_ in rows],
        normalized_jets=[v.tolist() for v in values],physical_jets=[v.tolist() for v in original],
        component_relative=relative.tolist(),original_component_relative=original_relative.tolist(),
        max_component_relative=float(max(relative)),original_consistency=consistency,
        regular=regular,accepted_initial_root=matched,
        scope='Five initial action jets at one X, shared F and signed f; no health/global/CMB or source-calibrated universal theory certificate')


def solve(start,sign,spec=s.Spec(),u1=.128,max_nfev=500):
    lower=np.array([np.log(1e-6),-24,np.log(1e-4),np.log(1e-5),-24])
    upper=np.array([np.log(1e5),13,np.log(30.),np.log(1e4),13])
    out=least_squares(lambda t:residual(t,sign,spec,u1),start,bounds=(lower,upper),
        jac='3-point',xtol=2e-12,ftol=2e-12,gtol=2e-12,max_nfev=max_nfev)
    row=inspect(out.x,sign,spec,u1)
    row.update(start=np.asarray(start).tolist(),optimizer_success=bool(out.success),message=out.message,nfev=out.nfev,
        max_scaled_residual=float(max(abs(out.fun))),singular_values=np.linalg.svd(out.jac,compute_uv=False).tolist(),
        distance_to_bounds=float(min(np.min(out.x-lower),np.min(upper-out.x))))
    return row


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);parser.add_argument('--max-nfev',type=int,default=500);args=parser.parse_args()
    rows=[]
    for sign in (-1,1):
        for u1 in (.03,.128,.5):
            for eta_logit in (-17,-7,0):
                start=np.array([np.log(.05),eta_logit,np.log(.2),np.log(u1),eta_logit])
                try:row=solve(start,sign,u1=u1,max_nfev=args.max_nfev)
                except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
                    row=dict(sign=sign,u1=u1,start=start.tolist(),error=str(exc))
                rows.append(row);print('SIGNED_SEARCH='+json.dumps(row,allow_nan=False),flush=True)
    result=dict(attempts=len(rows),accepted=sum(r.get('accepted_initial_root',False) for r in rows),rows=rows,
        scope='Bounded signed-f, broad negative-w search; neither optimizer status nor failed multistart is a theorem')
    if args.result_file:args.result_file.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print('SUMMARY='+json.dumps({k:v for k,v in result.items() if k!='rows'}))


if __name__=='__main__':main()
