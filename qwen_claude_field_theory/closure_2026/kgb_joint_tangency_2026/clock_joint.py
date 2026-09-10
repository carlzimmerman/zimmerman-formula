#!/usr/bin/env python3
"""Solve next tangency using the clock-gradient magnitude as fourth control.

The two initial seeds are prior matched points, not claimed solutions of the
four equations. Fixed y1=.1, global a0=1. Deterministic bounded search.
"""
import argparse
import json
import numpy as np
from scipy.optimize import least_squares
import search

SEEDS = [[16213.665635575568,.16684741777676196,74.17372946915628,100.],
         [70548.72439127016,.16934512212623238,721.9304286130189,1000.]]


def solve(start,y1=.1,max_nfev=1000):
    def unpack(x):return np.r_[x[:3],np.log(y1)],np.exp(x[3])
    def residual(x):
        theta,u1=unpack(x)
        return search.evaluate(theta,u1)[4]
    lower=np.log([.01,1e-4,1e-6,.0001]);upper=np.log([1e7,10,1e6,5000.])
    opt=least_squares(residual,np.log(start),bounds=(lower,upper),jac='3-point',x_scale='jac',
                      xtol=3e-13,ftol=3e-13,gtol=3e-13,max_nfev=max_nfev)
    theta,u1=unpack(opt.x)
    row=search.inspect(theta,u1)
    row.update(nfev=opt.nfev,optimizer_status=opt.status,start=start,
               bound_distance=float(min(np.min(opt.x-lower),np.min(upper-opt.x))),
               actual_jacobian_singular_values=np.linalg.svd(opt.jac,compute_uv=False).tolist())
    return row


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--max-nfev',type=int,default=1000)
    args=parser.parse_args()
    for seed in SEEDS:
        try:result=solve(seed,max_nfev=args.max_nfev)
        except (ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:result=dict(start=seed,error=str(exc))
        print('CLOCK_JOINT='+json.dumps(result,allow_nan=False),flush=True)
