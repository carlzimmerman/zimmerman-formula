#!/usr/bin/env python3
"""RK01 numerical audit: scalar active-set fit, independent of BLAS/NNLS.

The v2 run emitted matrix-operation warnings despite finite results. Recompute
the two-variable convex fit by enumerating all stationary faces, with Python
scalar sums, then run the same frozen physical experiment. No new physics
parameters, data cuts, profile choices, or screening lines are introduced.
"""
import argparse
import math
from pathlib import Path
import kernel_test_v2 as experiment


def scalar_fit(p, d, bmax=None):
    p,d=[float(v) for v in p],[float(v) for v in d]
    dot=lambda x,y:math.fsum(a*b for a,b in zip(x,y))
    pp,dd,pd=dot(p,p),dot(d,d),dot(p,d)
    py,dy=math.fsum(p),math.fsum(d)
    candidates=[(0.,0.),(max(0.,py/pp),0.)]
    bz=max(0.,dy/dd)
    if bmax is not None:bz=min(bz,bmax)
    candidates.append((0.,bz))
    det=pp*dd-pd*pd
    assert det>1e-12*pp*dd,'degenerate fitting columns'
    a=(py*dd-dy*pd)/det;b=(dy*pp-py*pd)/det
    if a>=0 and b>=0 and (bmax is None or b<=bmax):candidates.append((a,b))
    if bmax is not None:candidates.append((max(0.,(py-bmax*pd)/pp),bmax))
    loss=lambda ab:math.fsum((ab[0]*x+ab[1]*y-1)**2 for x,y in zip(p,d))
    a,b=min(candidates,key=loss)
    support=[a*x+b*y for x,y in zip(p,d)]
    positive=all(s>0 for s in support)
    # KKT checks at all selected faces, to a relative arithmetic tolerance.
    ga=math.fsum(x*(s-1) for x,s in zip(p,support))
    gb=math.fsum(x*(s-1) for x,s in zip(d,support))
    tol=1e-9*max(1.,abs(py),abs(dy),pp,dd)
    assert (abs(ga)<=tol if a>0 else ga>=-tol)
    if b==0:assert gb>=-tol
    elif bmax is not None and b==bmax:assert gb<=tol
    else:assert abs(gb)<=tol
    return {'A_over_Aref':a,'zeta_over_Zref':b,'mu_K_Mpc_inverse':None if a==0 else 4/math.sqrt(a),
            'ell_kpc':50*b**.25,'fractional_support_rms':math.sqrt(loss((a,b))/len(p)),
            'log10_support_rms':math.sqrt(math.fsum(math.log10(s)**2 for s in support)/len(support)) if positive else None,
            'all_support_positive':positive,'KKT_checked':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--omit-redshift',action='store_true');args=parser.parse_args()
    experiment.base.fit_support=scalar_fit
    experiment.main(args.output,args.omit_redshift)
