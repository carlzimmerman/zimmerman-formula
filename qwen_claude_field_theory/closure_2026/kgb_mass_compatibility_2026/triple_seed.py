#!/usr/bin/env python3
"""Solve shared three-mass derivative compatibility, then inspect actual health.

Only initial jets here. A root is NOT an invariant compatible trajectory.
No dark-matter particles, no PXX steering after the common-action solve.
"""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import least_squares

PREVIOUS=Path(__file__).resolve().parent.parent/'kgb_joint_action_2026'
sys.path.insert(0,str(PREVIOUS))
import joint_static as j
import third_mass as third


def jet(y1,y2,y3,bscale,P=0.,eps3=1.5e-6,health=False):
    eps=(1e-6,2e-6);X=.5
    state=j.initial(*eps,y1,y2,bscale,P=P)
    px,pxx=j.action_jet(X,state,eps)
    _,v1,v2=j.shared(X,state,eps)
    v3=third.match(eps3,y3,X,P,v1['H'])
    f1=v1['a']+px*v1['b'];f3=v3['a']+px*v3['b']
    d1=third.derivatives(v1,px);d3=third.derivatives(v3,px)
    f1x=d1[0]+px*d1[1]+pxx*v1['b']
    f3x=d3[0]+px*d3[1]+pxx*v3['b']
    residual=np.array([(f3-f1)*eps[0],(f3x-f1x)*eps[0]**2])
    row=dict(y1=y1,y2=y2,y3=y3,bscale=bscale,P=P,eps3=eps3,
             residual=residual.tolist(),PX=px,PXX=pxx,
             state=state.tolist(),U3=v3['U'],H=v1['H'])
    if health:
        row['halos']=[j.local(v,px,pxx) for v in (v1,v2,v3)]
        row['all_bounded']=all(h['bounded_static_hamiltonian'] for h in row['halos'])
        row['all_causal']=all(h['strict_cone'] for h in row['halos'])
    return row


def solve(bscale,start=(.3,.16),y1=.1,P=0.,eps3=1.5e-6):
    def fun(logys):return jet(y1,*np.exp(logys),bscale,P,eps3)['residual']
    try:
        out=least_squares(fun,np.log(start),bounds=(np.log(.02),np.log(20.)),
                          xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=150,jac='3-point')
        row=jet(y1,*np.exp(out.x),bscale,P,eps3,health=True)
        row.update(optimizer_success=bool(out.success),nfev=out.nfev,
                   max_scaled_residual=float(max(abs(out.fun))),initial_guess=list(start),
                   singular_values=np.linalg.svd(out.jac,compute_uv=False).tolist())
        # Optimizer status alone cannot establish equations or regularity.
        json.dumps(row,allow_nan=False)
        return row
    except (ValueError,FloatingPointError,ZeroDivisionError) as exc:
        return dict(bscale=bscale,P=P,y1=y1,eps3=eps3,initial_guess=list(start),error=str(exc))


def main():
    rows=[]
    for b in (.05,.1,.2,.25,.4,.6,.8,1.2,2.,4.):
        for initial in ((.3,.16),(.7,.3),(2.,1.),(6.,4.)):
            row=solve(b,initial);rows.append(row)
            print('SOLVE='+json.dumps(row),flush=True)
    good=[a for a in rows if a.get('max_scaled_residual',1)<1e-7]
    print('SUMMARY='+json.dumps(dict(attempts=len(rows),equation_roots=len(good),
                                     healthy_roots=sum(r.get('all_causal',False) for r in good),
                                     scope='Finite initial jets, not global compatibility or full theory')))
    return 0


if __name__=='__main__':raise SystemExit(main())
