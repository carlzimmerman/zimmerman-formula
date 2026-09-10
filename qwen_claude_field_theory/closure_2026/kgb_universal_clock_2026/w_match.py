#!/usr/bin/env python3
"""Two exterior jets with one shared, freely solved F_X (not two fitted actions)."""
from dataclasses import asdict
import json
import numpy as np
from scipy.optimize import least_squares
import universal_seed as s


def pair(theta,spec=s.Spec(),u1=.128):
    f,dw1,y2,u2,dw2=np.exp(theta)
    rows=[]
    for eps,y,u,dw in ((spec.eps1,spec.y1,u1,dw1),(spec.eps2,y2,u2,dw2)):
        g=s.n.old.metric(eps,y)['g']
        a,v=s.raw_jet(eps,y,spec.X,eps*u,-dw*.05*g/f,spec.F,f)
        v[1:]/=f
        rows.append((a,v))
    return rows


def scales(spec):
    result=s.scales(spec).copy();result[1:]/=spec.f
    return result


def residual(theta,spec=s.Spec(),u1=.128):
    a,b=pair(theta,spec,u1)
    return (a[1]-b[1])/scales(spec)


def solve(start=(.05,1.5,.15,.128,1.5),spec=s.Spec(),u1=.128,max_nfev=250):
    lower=np.log([1e-6,.05,.005,.005,.05]);upper=np.log([100.,100.,30.,50.,100.])
    out=least_squares(lambda t:residual(t,spec,u1),np.log(start),bounds=(lower,upper),
        jac='3-point',xtol=2e-12,ftol=2e-12,gtol=2e-12,max_nfev=max_nfev)
    rows=pair(out.x,spec,u1);a,b=rows[0][1],rows[1][1]
    rel=abs(a-b)/np.maximum(np.maximum(abs(a),abs(b)),1e-100)
    f=float(np.exp(out.x[0]))
    result=dict(spec=asdict(spec),u1=u1,initial_guess=list(start),parameters=np.exp(out.x).tolist(),
        optimizer_success=bool(out.success),message=out.message,nfev=out.nfev,
        normalized_jets=[v.tolist() for _,v in rows],
        signed_scaled_residual=out.fun.tolist(),component_relative=rel.tolist(),
        max_scaled_residual=float(max(abs(out.fun))),max_component_relative=float(max(rel)),
        actual_jacobian_singular_values=np.linalg.svd(out.jac,compute_uv=False).tolist(),
        distance_to_log_bounds=float(min(np.min(out.x-lower),np.min(upper-out.x))),
        regular_map=s.regular_jet_map(spec.F,spec.X,f,[a for a,_ in rows]),
        accepted_initial_root=bool(max(abs(out.fun))<1e-7 and max(rel)<1e-7
            and s.regular_jet_map(spec.F,spec.X,f,[a for a,_ in rows])),
        Dfield=2*(spec.F-spec.X*f),
        scope='Common initial jets only; fixed global a0; no interior mass calibration or global/CMB certification')
    json.dumps(result,allow_nan=False)
    return result


def main():
    rows=[]
    for ratio in (1.2,2.,4.):
        for u1 in (.03,.128,.5):
            for y2 in (.08,.2,.8):
                spec=s.Spec(eps2=ratio*1e-6);start=(.05,1.5,y2,u1,1.5)
                try:row=solve(start,spec,u1)
                except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
                    row=dict(spec=asdict(spec),u1=u1,initial_guess=list(start),error=str(exc))
                rows.append(row);print('W_PAIR='+json.dumps(row,allow_nan=False),flush=True)
    print('SUMMARY='+json.dumps(dict(attempts=len(rows),
        initial_roots=sum(r.get('accepted_initial_root',False) for r in rows),
        scope='Bounded numerical search, not a no-go or theory certificate')))
    return 0


if __name__=='__main__':raise SystemExit(main())
