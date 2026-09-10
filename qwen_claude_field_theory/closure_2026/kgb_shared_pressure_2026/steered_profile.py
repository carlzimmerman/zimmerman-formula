#!/usr/bin/env python3
"""Integrate P and P_X alongside the halo: no independent P_XX at every radius.

The midpoint of the action-derived causal interval supplies P_XX, and
dP/dr=P_X X', dP_X/dr=P_XX X' impose local functional integrability.
One completed profile would still not establish universality across masses.
"""
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad

spec=importlib.util.spec_from_file_location('steering',Path(__file__).with_name('jet_steering.py'))
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)


def integrate(eps=1e-6,bscale=.75,rtol=1e-6,max_trials=10000):
    hi,lo=20.,.02
    def du(y):
        a=gate.source.geometry(eps,y,0,.1,1.)
        return 2*a['g']*a['ry']/eps
    u0=quad(du,lo,hi,epsabs=1e-10)[0]
    a=gate.source.geometry(eps,hi,u0,.1,1.);W=a['r']*a['g']
    state=np.array([u0,bscale*W/(2*eps*(2+bscale*W)),0.,0.])
    t=np.log(hi);end=np.log(lo);h=-1e-4;accepted=[];rejections=0
    def rhs(t,state):
        u,z,P,logPX=state
        if not -80<logPX<80:raise ValueError('kinetic derivative outside numerical cap')
        PX=np.exp(logPX);y=np.exp(t)
        trial=gate.choose(eps,y,u,z,P,PX)
        if trial['selected'] is None:raise ValueError(trial['window']['reason'])
        a=gate.source.geometry(eps,y,u,z,PX,pressure=P)
        dX=a['Xr']*a['ry']*y
        return np.array([2*a['g']*a['ry']*y/eps,
            -(a['Xr']/a['invA']+2*a['g']*(.5-eps*z))*a['ry']*y/eps,
            PX*dX,trial['PXX']/PX*dX])
    def rk(t,state,h):
        k1=rhs(t,state);k2=rhs(t+h/2,state+h*k1/2)
        k3=rhs(t+h/2,state+h*k2/2);k4=rhs(t+h,state+h*k3)
        return state+h*(k1+2*k2+2*k3+k4)/6
    reason='trial cap';last_failure=None
    for count in range(max_trials):
        h=-min(abs(h),t-end,.1)
        if abs(h)<1e-12:reason='step floor; not a proof of nonexistence';break
        try:
            full=rk(t,state,h);half=rk(t+h/2,rk(t,state,h/2),h/2)
            scale=np.array([1e-9,1e-10,1e-12,1e-9])+rtol*np.maximum(abs(state),abs(half))
            error=np.max(abs(full-half)/(15*scale))
            if not np.isfinite(error):raise ValueError('nonfinite trial')
            if error>1:
                rejections+=1;h*=max(.1,.8*error**(-.2));continue
            next_t=t+h
            chosen=gate.choose(eps,np.exp(next_t),half[0],half[1],half[2],np.exp(half[3]))
            if chosen['selected'] is None:raise ValueError('accepted endpoint outside window')
            t=next_t;state=half
            row=chosen['selected'];row.update(PX=float(np.exp(state[3])),PXX=chosen['PXX'])
            accepted.append(row)
            if t-end<1e-12:reason='reached endpoint';break
            h*=min(2.,max(.5,.8*max(error,1e-15)**(-.2)))
        except (ValueError,FloatingPointError,OverflowError) as e:
            last_failure=str(e);rejections+=1;h*=.5
    return dict(epsilon=eps,bscale=bscale,rtol=rtol,reason=reason,last_trial_failure=last_failure,
                reached_end=reason=='reached endpoint',endpoint_y=float(np.exp(t)),
                trials=count+1,rejections=rejections,accepted_steps=len(accepted),
                all_accepted_healthy=bool(accepted and all(r['healthy'] for r in accepted)),
                max_sampled_speed=max((r['max_sampled_speed'] or float('inf') for r in accepted),default=None),
                max_pressure_ratio=max((abs(r['pr_over_rho']) for r in accepted),default=None),
                min_density=min((r['rho'] for r in accepted),default=None),
                rows=accepted)


def main():
    for eps,b in ((1e-6,.75),(2e-6,.75),(1e-6,1.25)):
        a=integrate(eps,b);rows=a.pop('rows');a.update(first=rows[0] if rows else None,last=rows[-1] if rows else None)
        print('STEERED='+json.dumps(a),flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
