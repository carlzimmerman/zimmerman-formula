#!/usr/bin/env python3
"""Small discriminating family: dilute exclusion, solved sources and controls."""
import json
from scipy.optimize import brentq
from solve import solve,coefficients,eos


if __name__=='__main__':
    specifications=[dict(hc=h,lam=50.) for h in (1e-6,1e-5,1e-4,.001,.01)]
    specifications += [dict(hc=.01,lam=lam) for lam in (20.,100.)]
    specifications += [dict(hc=.01,lam=50.,points=800,tolerance=1e-8),
                       dict(hc=.01,lam=50.,outer=6.,points=900,tolerance=1e-8)]
    results=[]
    for spec in specifications:
        try:out=solve(**spec)
        except ValueError as exc:out=dict(status='solver_domain_failure',message=str(exc),inputs=spec)
        results.append(out);print(json.dumps(out),flush=True)
    print(json.dumps({'scope':'bounded initial pressure-balance family; solver failures are not exclusions',
                      'solved':sum(x['status']=='initial_bvp_solved' for x in results),
                      'analytic_exclusions':sum(x['status']=='excluded_by_necessary_binding_bound' for x in results),
                      'unresolved_solver_cases':sum(x['status'] not in ('initial_bvp_solved','excluded_by_necessary_binding_bound') for x in results)}))
    c=coefficients();thresholds=[]
    for lam in (20.,50.,100.):
        def criterion(h):
            rho,p=eos(h,lam)
            return c['lambdab']*(rho+3*p)-c['lambda0']*h
        root=brentq(criterion,1e-12,1.,xtol=1e-15)
        thresholds.append(dict(lam=lam,necessary_h_min=root,density_at_threshold=eos(root,lam)[0]))
    print(json.dumps({'necessary_thresholds_code_units':thresholds,
                      'scope':'necessary, not sufficient; center is global enthalpy maximum'}))
