#!/usr/bin/env python3
"""Radial continuation of ONE reconstructed conformal action, not fresh jets.

ln(y) is the independent variable. Evolve X, U, P and the primitive G; compute
all P/G derivatives from that trajectory. Stop on loss of a local EF health
condition rather than counting off-shell trial states as solutions.
"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
import conformal_inverse as c
import gradient_inverse as gradient


def unpack(eps,sigma,v):
    return .5+eps*v[0],eps*v[1],sigma*v[2]/eps


def rhs(t,v,eps,sigma,chart='pressure'):
    y=np.exp(t);X,U,P=unpack(eps,sigma,v)
    a=(c.coefficients(eps,y,X,U,P,sigma) if chart=='pressure' else
       gradient.coefficients(eps,y,X,U,v[2],sigma))
    dr=a['ry']*y;z=a['z'];ur=-2*a['g']*(2*X+U)-2*z
    third=a['PX']*z*dr*eps/sigma if chart=='pressure' else a['zr']*dr
    return np.array([z*dr/eps,ur*dr/eps,third,
                     a['GX']*z*dr/np.sqrt(eps)])


def observe(t,v,eps,sigma,chart='pressure'):
    if chart=='pressure':return c.inspect(eps,np.exp(t),*unpack(eps,sigma,v),sigma)
    X,U,_=unpack(eps,sigma,v)
    return gradient.inspect(eps,np.exp(t),X,U,v[2],sigma)


def health_value(row):
    scale=max(abs(row[k]) for k in ('kinetic','radial','angular','cross'))
    return min(row['kinetic'],-row['radial'],-row['angular'],
               row['kinetic']-abs(row['cross']),row['light_margin'])/scale


def integrate(eps=1e-6,y0=.1,sigma=.1,b=.25,d=1.5,log_span=1.,max_step=.01,chart='pressure'):
    if chart not in ('pressure','gradient'):raise ValueError('unknown chart')
    X,U,P=c.initial(eps,y0,sigma,b,d)
    state=np.array([(X-.5)/eps,U/eps,P*eps/sigma,0.])
    if chart=='gradient':state[2]=-d*c.metric(eps,y0)['g']
    first=observe(math.log(y0),state,eps,sigma,chart)
    if not first['EF_strict_cone']:
        return dict(solver_success=False,reason='seed fails EF health diagnostic',seed=first)
    def health_event(t,v):return health_value(observe(t,v,eps,sigma,chart))
    health_event.terminal=True;health_event.direction=-1
    sol=solve_ivp(lambda t,v:rhs(t,v,eps,sigma,chart),
        (math.log(y0),math.log(y0)+log_span),state,method='DOP853',
        events=health_event,rtol=2e-10,atol=2e-12,max_step=max_step)
    # Retained accepted solver states, including the interpolated event state.
    rows=[observe(t,v,eps,sigma,chart) for t,v in zip(sol.t,sol.y.T)]
    final=rows[-1]
    return dict(solver_success=bool(sol.success),reason=sol.message,
        eps=eps,y0=y0,sigma=sigma,bscale=b,dscale=d,log_span=log_span,chart=chart,
        max_step=max_step,accepted_points=len(rows),nfev=sol.nfev,
        reached_target=sol.status==0,health_event=sol.status==1,
        final_y=final['y'],final_state=sol.y[:,-1].tolist(),seed=first,final=final,
        max_metric_error=max(r['relative_metric_error'] for r in rows),
        max_current_error=max(r['relative_total_current_error'] for r in rows),
        min_interior_health=min(health_value(r) for r in rows[:-1]),
        interior_strict_cone=all(r['EF_strict_cone'] for r in rows[:-1]),
        G_increment=float(np.sqrt(eps)*sol.y[3,-1]),
        scope='One mass, retained exterior radial states; boundary is not a global no-go. No PPN/interior/FLRW certification.')


def main():
    rows=[]
    for y0 in (.1,1.,10.):
        for sigma in (1e-6,.1,1.):
            for direction in (-1.,1.):
                try:rows.append(integrate(y0=y0,sigma=sigma,log_span=direction*math.log(10)))
                except (ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
                    rows.append(dict(y0=y0,sigma=sigma,direction=direction,error=str(exc)))
    for chart in ('pressure','gradient'):
        for step in (.01,.005):
            for direction in (-1.,1.):
                rows.append(integrate(sigma=.1,log_span=direction*math.log(10),
                                      chart=chart,max_step=step))
    for sigma in (.1,1.):
        for step in (.02,.01):
            rows.append(integrate(sigma=sigma,chart='gradient',
                log_span=-math.log(1e4),max_step=step))
    print('CONFORMAL_FLOW='+json.dumps(dict(runs=rows),allow_nan=False))
    return 0


if __name__=='__main__':raise SystemExit(main())
