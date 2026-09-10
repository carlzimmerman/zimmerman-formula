#!/usr/bin/env python3
"""Preserve one quadratic F and its reconstructed P/G through radial evolution."""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
import nonaffine_inverse as n


def rhs(t,v,eps,j0):
    y=np.exp(t);X=.5+eps*v[0];U=eps*v[1];z=v[2]
    a=n.coefficients(eps,y,X,U,z,j0=j0);dr=a['ry']*y
    return np.array([z*dr/eps,(-2*a['g']*(2*X+U)-2*z)*dr/eps,
                     a['zr']*dr,a['GX']*z*dr/np.sqrt(eps)])


def observe(t,v,eps,j0):
    return n.inspect(eps,np.exp(t),.5+eps*v[0],eps*v[1],v[2],j0=j0)


def admissibility(row):
    k,b,r,t=[row[key] for key in ('kinetic','cross','radial','angular')]
    scale=max(abs(k),abs(b),abs(r),abs(t))
    # Positive-f/positive-field-Jacobian branch continuously connected to seed.
    return min(k,-r,-t,k-abs(b),row['light_margin'])/scale


def integrate(j0=0.,eps=1e-6,y0=.1,b=.25,d=1.5,log_span=math.log(1000),max_step=.005):
    X,U,_=n.old.initial(eps,y0,.1,b,d);z=-d*n.old.metric(eps,y0)['g']
    v=np.array([0.,U/eps,z,0.]);t0=math.log(y0)
    seed=observe(t0,v,eps,j0)
    if not seed['strict_EF']:return dict(success=False,reason='seed fails EF health',seed=seed,j0=j0)
    def event(t,v):
        r=observe(t,v,eps,j0)
        return min(admissibility(r),r['f']/.05,r['Dfield'],r['X']/.5,r['F']/.525)
    event.terminal=True;event.direction=-1
    sol=solve_ivp(lambda t,v:rhs(t,v,eps,j0),(t0,t0+log_span),v,
        method='DOP853',rtol=2e-10,atol=2e-12,max_step=max_step,events=event)
    rows=[observe(t,v,eps,j0) for t,v in zip(sol.t,sol.y.T)]
    return dict(success=bool(sol.success),reason=sol.message,j0=j0,eps=eps,y0=y0,bscale=b,dscale=d,
        max_step=max_step,log_span=log_span,event=sol.status==1,reached_target=sol.status==0,
        nfev=sol.nfev,accepted_points=len(rows),final_state=sol.y[:,-1].tolist(),seed=seed,final=rows[-1],
        all_interior_healthy=all(r['strict_EF'] for r in rows[:-1]),
        max_metric_residual=max(r['residual']['metric'] for r in rows),
        max_current_residual=max(r['residual']['current'] for r in rows),
        G_increment=float(np.sqrt(eps)*sol.y[3,-1]),
        scope='One mass, one fixed quadratic F and preserved P/G; EF exterior diagnostic, not global physical theory')


def main():
    rows=[]
    for j in (-1e5,-75000.,-5e4,-25000.,-1e4,0.,1e4,25000.,5e4,75000.,1e5):
        try:rows.append(integrate(j0=j))
        except (ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
            rows.append(dict(j0=j,error=str(exc)))
    print('QUADRATIC_F_FLOW='+json.dumps(dict(rows=rows),allow_nan=False))
    return 0


if __name__=='__main__':raise SystemExit(main())
