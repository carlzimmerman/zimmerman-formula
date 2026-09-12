#!/usr/bin/env python3
"""Independent potential/DF invariants and persisted-run convergence checks."""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('orbit_audit',BASE/'audit_orbits.py')
oa=importlib.util.module_from_spec(spec)
spec.loader.exec_module(oa)


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True); args=p.parse_args()
    eq=oa.Equilibrium()
    checks=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:
            raise AssertionError(name+': '+str(detail))
    # Force-potential consistency tested independently by finite differences.
    x=np.geomspace(1e-3,1e3,100)
    h=1e-5*x
    numeric=(oa.psi(x+h)-oa.psi(x-h))/(2*h)
    expected=-oa.m(x)/x**2
    err=float(np.max(np.abs(numeric/expected-1)))
    check('NFW force is minus gradient of implemented potential',err<2e-7,err)
    sigma=[]
    for name,_,ve,xx in oa.HOSTS:
        den=quad(lambda v:4*np.pi*v*v*float(eq.df(oa.psi(xx)-.5*v*v)),
                 0,np.sqrt(2*oa.psi(xx)),epsabs=1e-7,limit=200)[0]
        num=quad(lambda v:4*np.pi*v**4/3*float(eq.df(oa.psi(xx)-.5*v*v)),
                 0,np.sqrt(2*oa.psi(xx)),epsabs=1e-7,limit=200)[0]
        jeans=xx*(1+xx)**2*quad(lambda y:float(oa.m(y))/(y**3*(1+y)**2),
                              xx,np.inf,epsabs=1e-13)[0]
        rel=float(num/den/jeans-1)
        check(name+' Eddington velocity moment recovers independent Jeans integral',abs(rel)<.001,rel)
        sigma.append(dict(host=name,relative_variance_error=rel))
    con=json.loads((BASE/'convergence_001/results.json').read_text())
    rep=json.loads((BASE/'replication_001/results.json').read_text())
    coarse,fine=con['runs']; independent=rep['runs'][0]
    differences=[]
    for i,(old,new,other) in enumerate(zip(coarse['rows'],fine['rows'],independent['rows'])):
        delta=abs(old['retention']-new['retention'])
        noise=np.hypot(new['particle_se'],other['particle_se'])
        check(new['host']+' retention timestep convergence',delta<.002,delta)
        check(new['host']+' independent-seed agreement',
              abs(new['retention']-other['retention'])<4*noise,
              dict(difference=new['retention']-other['retention'],combined_se=float(noise)))
        check(new['host']+' no-kick controls passed in every run',
              all(z['numerical_control_pass'] for z in [old,new,other]),
              [z['control_early_to_late_fractional_drift'] for z in [old,new,other]])
        differences.append(dict(host=new['host'],dt_retention_difference=delta))
    for run in [coarse,fine,independent]:
        sigma_n=np.sqrt(oa.MEAN/run['n_per_host'])
        check('Poisson sample mean within six sampling errors',
              abs(run['mean_kicks_realized']-oa.MEAN)<6*sigma_n,
              dict(seed=run['seed'],mean=run['mean_kicks_realized'],target=oa.MEAN))
    rc=3*(67.36/1000)**2/(8*np.pi*oa.G)
    masses=[]
    for host in oa.host_params():
        a,rs=host['A'],host['rs_kpc']
        c=brentq(lambda c:a*rs/oa.G*float(oa.m(c))/(4*np.pi/3*(c*rs)**3)-200*rc,.01,100)
        masses.append(dict(host=host['name'],c200=c,M200_Msun=float(a*rs/oa.G*oa.m(c))))
    science=dict(spiral_ceiling=.15,cluster_window=[.45,.70],
                 spiral_all_point_estimates_pass=all(r['rows'][0]['retention']<=.15
                                                    for r in [coarse,fine,independent]),
                 cluster_all_CI95_lower_above_upper_gate=all(r['rows'][3]['CI95_normal'][0]>.70
                                                           for r in [coarse,fine,independent]),
                 scope='Prescribed fixed NFW potential and stationary energy-cut tracer DF only; not a universal C003 exclusion.')
    out=dict(checks=checks,passed=len(checks),failed=0,timestep_differences=differences,
             source_halo_mass_normalizations=masses,scientific_outcome=science)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
