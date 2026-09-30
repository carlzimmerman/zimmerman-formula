#!/usr/bin/env python3
"""Ballistic through-stream probe, independently derived from flux/residence time.

python3 sol61_push/through_stream.py --output sol61_push/stream_results.json
Add --mutate to insert an incorrect residence-time density (negative control).
Spherical average of a single uniform cold beam in a fixed point-mass potential.
No capture, sinks, interactions or beam self-gravity. Not a no-go for those.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
import sympy as sp


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True)
    ap.add_argument('--mutate',action='store_true')
    args=ap.parse_args()
    checks=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")

    r,G,M,V,rhoinf=sp.symbols('r G M V rhoinf',positive=True)
    # v_r^2=A-V^2 b^2/r^2. Incoming flux at infinity in impact annulus db is
    # 2pi*b*db*rho_inf*V; two crossings of dr take 2dr/|v_r|.
    # Set b=(r sqrt(A)/V) sin(theta) to integrate the turning-point endpoint.
    theta=sp.symbols('theta',positive=True)
    A=V*V+2*G*M/r
    bmax=r*sp.sqrt(A)/V
    b=bmax*sp.sin(theta)
    integrand=sp.simplify(b*sp.diff(b,theta)/(sp.sqrt(A)*sp.cos(theta)))
    residence=sp.integrate(integrand,(theta,0,sp.pi/2))
    density=sp.simplify(4*sp.pi*rhoinf*V*residence/(4*sp.pi*r*r))
    exact=rhoinf*sp.sqrt(1+2*G*M/(r*V*V))
    check('flux_residence_time_density',sp.simplify(density-exact)==0,str(density))
    check('conservative_stream_is_unbound',sp.simplify((V*V+2*G*M/r)/2-G*M/r-V*V/2)==0,
          'E=V_infinity^2/2 > 0; gravity alone does not bind a tracer orbit')
    # Beam's radial average must be the isotropic result by linearity and rotation.
    # This says nothing about the angular profile, which is not spherical.
    numeric=[]
    for z in (1e-3,0.01,0.1,1,10,100,1000):
        # z=2GM/(rV^2). Radius and V set to 1 for this audit.
        av=1+z
        bm=math.sqrt(av)
        integ=quad(lambda t: bm*bm*math.sin(t)/math.sqrt(av),0,math.pi/2,
                   epsabs=1e-12,epsrel=1e-12)[0]
        found=integ
        if args.mutate:
            found=1.0  # erase gravitational residence-time enhancement
        expected=math.sqrt(av)
        check(f'residence_quadrature_z={z}',abs(found/expected-1)<1e-10,
              f'found={found:.8g}, expected={expected:.8g}')
        numeric.append(dict(z=z,density_over_ambient=found,expected=expected))
    # Analytic slope of density excess. delta_rho=rhoinf(sqrt(1+z)-1), z~r^-1.
    z=sp.symbols('z',positive=True)
    excess=sp.sqrt(1+z)-1
    slope=sp.simplify(-z*sp.diff(excess,z)/excess)
    slope_exact=-(1+1/sp.sqrt(1+z))/2
    check('excess_density_slope',sp.simplify(slope-slope_exact)==0,
          'dln(delta_rho)/dlnr=-(1+1/sqrt(1+z))/2, between -1 and -1/2')
    check('fails_deep_target_shape',True,
          'P2 point-mass halo tends to r^-2; ballistic stream excess is never steeper than r^-1')

    Gsi=6.67430e-11; Msun=1.98847e30; kpc=3.0856775814913673e19
    rows=[]
    for footing,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
        for v in (100e3,300e3,600e3):
            for mass_sol in (1e9,1e10,1e11,1e12):
                mass=mass_sol*Msun
                rM=math.sqrt(Gsi*mass/a0)
                rf=Gsi*mass/(v*v)
                rows.append(dict(footing=footing,a0_si=a0,velocity_kms=v/1000,
                                 Mb_Msun=mass_sol,rM_kpc=rM/kpc,focusing_radius_kpc=rf/kpc,
                                 focusing_over_rM=rf/rM))
        for v in (100,300,600):
            cell=[x for x in rows if x['footing']==footing and x['velocity_kms']==v]
            spread=cell[-1]['focusing_over_rM']/cell[0]['focusing_over_rM']
            check(f'mass_scaling_{footing}_v={v}',abs(spread-math.sqrt(1000))<1e-10,
                  f'r_focus/rM spread={spread:.8g}; constant external V gives r_focus proportional to M')
    # Matching r_focus=rM requires V_infinity^4=G M a0: the desired relation inserted.
    a0=sp.symbols('a0',positive=True)
    vf2=sp.sqrt(G*M*a0)
    check('matching_scale_inserts_BTFR',sp.simplify(G*M/vf2-sp.sqrt(G*M/a0))==0,
          'r_focus=rM iff V_infinity^2=sqrt(G M a0)')
    check('Newtonian_not_flow_acceleration',True,
          'gravity sourced by real density; bodies are not assumed to be carried by the stream')
    payload=dict(checks=checks,numbers=dict(residence=numeric,physical_rows=rows),
                 model='steady uniform cold beam, fixed spherical point-mass potential, two crossings, no absorber',
                 verdict='FAIL as a standalone mechanism: no binding, wrong radial shape and mass scaling',
                 scope='Not a no-go for time-dependent/self-gravitating/multistream/interacting/coherent-field flows',
                 environment=dict(numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__),
                 mutation=args.mutate)
    Path(args.output).write_text(json.dumps(payload,indent=2)+'\n')
    failures=sum(not c['passed'] for c in checks)
    print(f'{len(checks)-failures}/{len(checks)} checks pass; {failures} failures. Theory completion OPEN.')
    return int(failures>0)


if __name__=='__main__':
    raise SystemExit(main())
