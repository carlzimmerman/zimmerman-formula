#!/usr/bin/env python3
"""Seek common P/PX/GX/PXX/GXX at distinct masses from ONE F-jet.

All five values come from the varied static inverse. F_XX is zero here because
its identical shared-jet slopes cannot repair matched-mass curvature gaps.
Any root is an INITIAL point only, not a universal or sourced MOND theory.
"""
from dataclasses import dataclass,asdict
from functools import lru_cache
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import least_squares

sys.path.append(str(Path(__file__).resolve().parents[1]/'kgb_nonaffine_clock_2026'))
import nonaffine_inverse as n


@dataclass(frozen=True)
class Spec:
    eps1:float=1e-6
    eps2:float=2e-6
    y1:float=.1
    X:float=.5
    F:float=.525
    f:float=.05


def raw_jet(eps,y,X,U,z,F=.525,f=.05,j=0.):
    a,pxx,gxx=n.action_curvatures(eps,y,X,U,z,j0=j,F0=F,f0=f,X0=X)
    return a,np.array([a['P'],a['PX'],a['GX'],pxx,gxx])


def regular_jet_map(F,X,f,rows):
    """Necessary regularity only; negative nonzero Dfield is allowed."""
    return bool(np.isfinite([F,X,f]).all() and F>0 and X>0 and f!=0 and
        F-X*f!=0 and all(np.isfinite([a['U'],a['B'],a['Dcoord']]).all() and
            min(a['U'],a['B'],a['Dcoord'])>0 for a in rows))


def pair(theta,spec=Spec(),j=0.):
    u1,d1,y2,u2,d2=np.exp(theta)
    result=[]
    for eps,y,u,d in ((spec.eps1,spec.y1,u1,d1),(spec.eps2,y2,u2,d2)):
        g=n.old.metric(eps,y)['g']
        result.append(raw_jet(eps,y,spec.X,u*eps,-d*g,spec.F,spec.f,j))
    return result


@lru_cache(None)
def scales(spec):
    g=n.old.metric(spec.eps1,spec.y1)['g']
    _,v=raw_jet(spec.eps1,spec.y1,spec.X,.128*spec.eps1,-1.5*g,spec.F,spec.f)
    return np.maximum(abs(v),1.)


def residual(theta,spec=Spec()):
    a,b=pair(theta,spec)
    return (a[1]-b[1])/scales(spec)


def inspect(theta,spec=Spec()):
    rows=pair(theta,spec);v1,v2=rows[0][1],rows[1][1]
    relative=abs(v1-v2)/np.maximum(np.maximum(abs(v1),abs(v2)),1e-100)
    scaled=(v1-v2)/scales(spec)
    halos=[]
    for eps,(a,v) in zip((spec.eps1,spec.eps2),rows):
        local=n.inspect(eps,a['y'],a['X'],a['U'],a['z'],F0=spec.F,f0=spec.f,X0=spec.X,j0=0.)
        local.update(eps=eps,r=a['r'],Dcoord=a['Dcoord'],jet=v.tolist())
        halos.append(local)
    return dict(spec=asdict(spec),theta=np.asarray(theta).tolist(),parameters=np.exp(theta).tolist(),
        signed_scaled_residual=scaled.tolist(),component_relative=relative.tolist(),
        max_scaled_residual=float(max(abs(scaled))),max_component_relative=float(max(relative)),halos=halos,
        scope='Common initial action jets only; mass labels not yet source-calibrated; no per-mass a0 or F/P/G retuning')


def solve(start=(.128,1.5,.15,.128,1.5),spec=Spec(),max_nfev=180):
    # Positive-U, negative-z regular branch around known healthy exterior.
    lower=np.log([.005,.05,.005,.005,.05]);upper=np.log([50.,20.,30.,50.,20.])
    out=least_squares(lambda theta:residual(theta,spec),np.log(start),
        bounds=(lower,upper),jac='3-point',xtol=2e-12,ftol=2e-12,gtol=2e-12,max_nfev=max_nfev)
    row=inspect(out.x,spec)
    row.update(initial_guess=list(start),optimizer_success=bool(out.success),message=out.message,
        nfev=out.nfev,actual_jacobian_singular_values=np.linalg.svd(out.jac,compute_uv=False).tolist(),
        distance_to_log_bounds=float(min(np.min(out.x-lower),np.min(upper-out.x))),
        accepted_initial_root=bool(max(abs(out.fun))<1e-7 and row['max_component_relative']<1e-7
            and regular_jet_map(spec.F,spec.X,spec.f,[a for a,_ in pair(out.x,spec)])))
    json.dumps(row,allow_nan=False)
    return row


def main():
    rows=[]
    for ratio in (1.2,2.,4.):
        spec=Spec(eps2=ratio*1e-6)
        for u in (.05,.128,.5,2.):
            for y2 in (.08,.2,.8):
                start=(u,1.5,y2,u,1.5)
                try:row=solve(start,spec)
                except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
                    row=dict(spec=asdict(spec),initial_guess=list(start),error=str(exc))
                rows.append(row);print('PAIR_SEED='+json.dumps(row,allow_nan=False),flush=True)
    print('SUMMARY='+json.dumps(dict(attempts=len(rows),
        initial_roots=sum(r.get('accepted_initial_root',False) for r in rows),
        scope='Finite bounded search for initial compatibility, not a universal no-go or theory closure')))
    return 0


if __name__=='__main__':raise SystemExit(main())
