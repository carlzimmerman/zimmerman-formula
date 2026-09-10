#!/usr/bin/env python3
"""Bounded continuation of a JOINT root; unchanged global a0 and action class."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'kgb_joint_tangency_2026'))
import search
from candidate_health import screen
from refine_joint import SEED


def solve(start,y1,max_nfev=400):
    def unpack(x):return np.r_[x[:3],np.log(y1)],np.exp(x[3])
    def residual(x):
        theta,u1=unpack(x)
        return search.evaluate(theta,u1)[4]
    lower=np.log([.01,1e-4,1e-6,.0001]);upper=np.log([1e7,10,5000.,10000.])
    opt=least_squares(residual,np.log(start),bounds=(lower,upper),jac='3-point',x_scale='jac',
                      xtol=3e-13,ftol=3e-13,gtol=3e-13,max_nfev=max_nfev)
    theta,u1=unpack(opt.x);row=search.inspect(theta,u1)
    row.update(nfev=opt.nfev,optimizer_status=opt.status,start=list(start),
               bound_distance=float(min(np.min(opt.x-lower),np.min(upper-opt.x))),
               actual_jacobian_singular_values=np.linalg.svd(opt.jac,compute_uv=False).tolist())
    if row['accepted_numerical_joint']:row['health']=screen(row)
    return row


def run(ys,max_nfev=400):
    successful={.1:SEED['parameters'][:3]+[SEED['u1']]}
    rows=[]
    for yy in ys:
        nearest=min(successful,key=lambda y:abs(np.log(y/yy)))
        start=successful[nearest].copy();start[1]*=yy/nearest
        try:
            row=solve(start,yy,max_nfev)
            if row['accepted_numerical_joint']:
                successful[yy]=row['parameters'][:3]+[row['u1']]
        except (ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
            row=dict(error=str(exc),start=start)
        row.update(y1=yy,max_nfev=max_nfev);rows.append(row)
        print('FAMILY='+json.dumps(row,allow_nan=False),flush=True)
    print('SUMMARY='+json.dumps(dict(attempts=len(rows),
        numerical_joint=sum(r.get('accepted_numerical_joint',False) for r in rows),
        health_survivors=sum(r.get('health',{}).get('needs_high_precision',False) for r in rows),
        scope='One continued seed family, bounded numerical evidence, no all-family exclusion')))
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--max-nfev',type=int,default=400)
    parser.add_argument('--ys',nargs='+',type=float,default=[.1,.08,.05,.03,.01,.003,.001,.15,.2,.3,.5,1,2,3])
    args=parser.parse_args();run(args.ys,args.max_nfev)
