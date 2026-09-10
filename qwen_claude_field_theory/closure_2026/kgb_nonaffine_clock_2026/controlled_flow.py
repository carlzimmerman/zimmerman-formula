#!/usr/bin/env python3
"""Construct one monotonic-X exterior action using the exact curvature window.

The control is a specified inverse-construction policy, NOT a fundamental law
or a different a0 per galaxy. It must subsequently pass shared-mass and FLRW
tests. w=F_X X' avoids an artificial F_XX term in w'.
"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
import curvature_window as w


def state(v,eps):
    return .5+eps*v[0],eps*v[1],.525+eps*v[2],v[3],v[4]


def local(t,v,eps):
    X,U,F,f,wr=state(v,eps)
    return w.inspect_window(eps,np.exp(t),X,U,wr/f,F=F,f=f,verify_correlation=False)


def rhs(t,v,eps):
    row=local(t,v,eps);X,U,F,f,wr=state(v,eps)
    j=row['j'] if row['j'] is not None else 0.
    # PX/GX are j-independent; w' equals f*z'_at_j0 exactly. This avoids
    # subtracting the two large opposite j*z^2 terms in floating point.
    a=w.n.coefficients(eps,np.exp(t),X,U,wr/f,j0=0.,F0=F,f0=f,X0=X)
    dr=a['ry']*np.exp(t);z=wr/f
    return np.array([z/eps,(-2*a['g']*(2*X+U)-2*z)/eps,wr/eps,
                     j*z,f*a['zr'],a['GX']*z/np.sqrt(eps)])*dr


def integrate(eps=1e-6,y0=.1,b=.25,d=1.5,log_span=math.log(1000),max_step=.005,window_guard=1e-8):
    X,U,_=w.n.old.initial(eps,y0,.1,b,d);z=-d*w.n.old.metric(eps,y0)['g']
    v=np.array([0.,U/eps,0.,.05,.05*z,0.]);t0=math.log(y0)
    def event(t,v):
        row=local(t,v,eps);a=row['base'];scale=max(abs(a[k]) for k in ('kinetic','cross','radial','angular'))
        # Stop before cancellation dominates at the exact zero-width window.
        # This is a disclosed numerical guard, not an exact no-go boundary.
        return min(row['gap']/scale-window_guard,-a['radial']/scale,
                   a['f']/.05,a['Dfield'],a['F']/.525)
    event.terminal=True;event.direction=-1
    sol=solve_ivp(lambda t,v:rhs(t,v,eps),(t0,t0+log_span),v,method='DOP853',
        rtol=2e-10,atol=2e-12,max_step=max_step,events=event,dense_output=True)
    rows=[local(t,v,eps) for t,v in zip(sol.t,sol.y.T)]
    selected=[r.get('selected',r['base']) for r in rows]
    midtimes=(sol.t[1:]+sol.t[:-1])/2
    midrows=[local(t,sol.sol(t),eps) for t in midtimes]
    midselected=[r.get('selected',r['base']) for r in midrows]
    checks=selected+midselected
    samples=[]
    for i in np.unique(np.linspace(0,len(rows)-1,min(33,len(rows)),dtype=int)):
        a=selected[i]
        sample={key:a[key] for key in ('y','X','F','f','j','P','PX','PXX','GX','GXX','strict_EF')}
        sample['G']=float(np.sqrt(eps)*sol.y[5,i]);samples.append(sample)
    return dict(eps=eps,y0=y0,bscale=b,dscale=d,log_span=log_span,max_step=max_step,window_guard=window_guard,
        success=bool(sol.success),reached_target=sol.status==0,event=sol.status==1,
        reason=sol.message,nfev=sol.nfev,accepted_points=len(rows),final_y=float(np.exp(sol.t[-1])),
        final_state=sol.y[:,-1].tolist(),first=rows[0],final=rows[-1],
        all_healthy=all(r['strict_EF'] for r in checks),midpoint_checks=len(midselected),
        max_metric_residual=max(r['residual']['metric'] for r in checks),
        max_current_residual=max(r['residual']['current'] for r in checks),
        min_X=float(min(.5+eps*sol.y[0])),max_X=float(max(.5+eps*sol.y[0])),
        monotonic_X=bool(np.all(np.diff(sol.y[0])>0) or np.all(np.diff(sol.y[0])<0)),
        sampled_action=samples,
        scope='One mass, inverse-constructed monotonic-X F/P/G with fixed curvature policy and fixed global a0 units; NOT universal or CMB-certified')


def main():
    rows=[]
    for span,step,guard in ((.02,.005,1e-8),(.5,.005,1e-8),(.5,.0025,1e-8),
                            (math.log(1000),.005,1e-8),(math.log(1000),.0025,1e-8),
                            (math.log(1000),.005,1e-7)):
        try:rows.append(integrate(log_span=span,max_step=step,window_guard=guard))
        except (ValueError,ArithmeticError,np.linalg.LinAlgError) as exc:
            rows.append(dict(log_span=span,max_step=step,window_guard=guard,error=type(exc).__name__+': '+str(exc)))
    print('CONTROLLED_FLOW='+json.dumps(dict(rows=rows),allow_nan=False))
    return 0


if __name__=='__main__':raise SystemExit(main())
