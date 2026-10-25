"""Continuation: diagnostic acceleration excess in the declared toy profiles.

No observational fit. Uses the same all-F impulse, zero radial velocity,
softening and finite-time energy diagnostic as model.py. Sampled accelerations
are instantaneous, not an equilibrium prediction for a stellar tracer.
"""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from model import G, A0, RESERVOIR, PROFILES, outer, mt, shell_fields, law


def run(profile,n,dt):
    name,mass,b_kpc,test_r=profile
    rm=(G*mass/A0)**.5
    beta=b_kpc/rm
    R=outer(beta)
    r=np.array([brentq(lambda x: mt(x,beta)-target,1e-12,R)
                for target in (np.arange(n)+.5)/n*RESERVOIR])/R
    b=beta/R
    v=np.zeros(n)
    a,p,phi=shell_fields(r,b,.1/RESERVOIR,.02)
    e0=p
    a0_unit=R*R/RESERVOIR
    rtest=test_r/(R*rm)
    gb=(.1/RESERVOIR)*rtest/(rtest*rtest+b*b)**1.5
    glaw=a0_unit*law(gb/a0_unit)
    samples=[]
    maxerr=0.
    steps=round(8/dt)
    for i in range(steps):
        v+=dt*a/2
        r+=dt*v
        neg=r<0
        r[neg]*=-1
        v[neg]*=-1
        a,p,phi=shell_fields(r,b,.1/RESERVOIR,.02)
        v+=dt*a/2
        err=abs((.5*np.mean(v*v)+p-e0)/e0)
        maxerr=max(maxerr,err)
        if (i+1) % (steps//16)==0:
            frac=float(np.mean(r<rtest))
            gf=frac*rtest/(rtest*rtest+.02**2)**1.5
            samples.append(dict(time=(i+1)*dt,bound_fraction=float(np.mean(.5*v*v+phi<0)),
                                enclosed_free_fraction=frac,
                                acceleration_over_postloss_baryonic_law=float((gb+gf)/glaw)))
    late=[x['acceleration_over_postloss_baryonic_law'] for x in samples if x['time']>=4]
    # Interpret time from the same initial radius/mass normalization.
    time_gyr=8*((R*rm)**3/(G*RESERVOIR*mass))**.5*.9777922217
    return dict(name=name,n=n,dt=dt,initial_baryon_mass_msun=mass,
                final_baryon_mass_msun=.1*mass,test_radius_kpc=test_r,
                physical_duration_gyr=time_gyr,softening_kpc=.02*R*rm,
                max_energy_relative_error=maxerr,
                final_bound_fraction=samples[-1]['bound_fraction'],
                late_acceleration_ratio_min=min(late),late_acceleration_ratio_max=max(late),
                snapshots=samples)


if __name__=='__main__':
    results=[run(p,n,dt) for p in (PROFILES[0],PROFILES[3])
             for n,dt in ((128,.0001),(256,.00005))]
    payload=dict(runs=results,energy_criterion_pass=all(x['max_energy_relative_error']<.005 for x in results),
                 bound_resolution_pass=all(abs(results[i]['final_bound_fraction']-results[i+1]['final_bound_fraction'])<.05 for i in (0,2)),
                 classification='post-hoc acceleration diagnostic, no observational fit')
    Path(sys.argv[1]).write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
    print(json.dumps(payload,indent=2,allow_nan=False))
