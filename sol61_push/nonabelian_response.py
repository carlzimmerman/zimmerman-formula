#!/usr/bin/env python3
"""Local dipole response experiment, translated from arXiv:2502.14686v2.

Eq. (3.22), equivalently Eq. (9) of arXiv:2507.02563v1, to quadratic order.
eta_a=sqrt(3), sum eta_a^-2=1 is a declared tuned input.
z_a=omega_a^2 xi_a/(2g), forcing along x, alphabar=1 in dimensionless units.
No gravitational Poisson solve, spatial flow, capture, or full action stability.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    omegas=np.array([0.3,1.0,1.002])
    force=np.array([1.,0.,0.])
    ts=np.linspace(0,600,12001)
    rows=[]
    checks=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    for g in (0.0002,0.0004,0.0008):
        for kind,amp,phase in [('aligned',0.,0.),('coherent',0.5,0.),
                               ('reverse',-0.5,0.),('quadrature',0.5,math.pi/2),
                               ('double_amplitude',1.,0.)]:
            z0=np.tile(force,(3,1))
            zd0=np.zeros((3,3))
            # z_2 transverse oscillation along y; z_3 along z.
            z0[1,1]=0.5
            z0[2,2]=amp*math.cos(phase)
            zd0[2,2]=-omegas[2]*amp*math.sin(phase)
            if kind=='aligned':
                z0=np.tile(force,(3,1))
            coupling=math.sqrt(3)*g/2
            def rhs(t,y):
                z=y[:9].reshape(3,3); dz=y[9:].reshape(3,3)
                cross=np.array([np.cross(z[1],z[2]),np.cross(z[2],z[0]),np.cross(z[0],z[1])])
                dd=omegas[:,None]**2*(force-z-coupling*cross)
                return np.concatenate([dz.ravel(),dd.ravel()])
            sol=solve_ivp(rhs,(ts[0],ts[-1]),np.r_[z0.ravel(),zd0.ravel()],t_eval=ts,
                          rtol=2e-10,atol=1e-12,method='DOP853')
            z=sol.y[:9].reshape(3,3,-1)
            induction=1-z[:,0,:].sum(axis=0)/3
            use=ts>=100
            avg=float(np.trapz(induction[use],ts[use])/(ts[use][-1]-ts[use][0]))
            row=dict(g=g,kind=kind,mean_D_over_g=avg,mean_D_over_g_squared=avg/g,
                     maximum_z=float(np.max(np.abs(z))),completed=sol.success)
            rows.append(row)
            check(f'finite_response_g={g}_{kind}',sol.success and np.isfinite(avg) and row['maximum_z']<2,
                  f'D/g={avg:.8g}, D/g^2={avg/g:.8g}, max|z|={row["maximum_z"]:.6g}')
    aligned=[x for x in rows if x['kind']=='aligned']
    coherent=[x for x in rows if x['kind']=='coherent']
    reverse=[x for x in rows if x['kind']=='reverse']
    doubled=[x for x in rows if x['kind']=='double_amplitude']
    check('aligned_state_has_no_quadratic_response',max(abs(x['mean_D_over_g']) for x in aligned)<1e-12,
          'all dipoles parallel to g: all cross products zero; D=0 at tuned linear cancellation')
    check('response_chirality_flips_sign',all(x['mean_D_over_g']*y['mean_D_over_g']<0 for x,y in zip(coherent,reverse)),
          'transverse orientation is an initial-condition input')
    scale=[x['mean_D_over_g_squared'] for x in coherent]
    spread=(max(scale)-min(scale))/abs(np.mean(scale))
    check('quadratic_weak_forcing_scaling',spread<0.10,f'D/g^2 spread={spread:.6g} at fixed coherent initial amplitudes')
    ratios=[b['mean_D_over_g']/a['mean_D_over_g'] for a,b in zip(coherent,doubled)]
    check('coefficient_is_not_selected',all(abs(x-2)<0.1 for x in ratios),
          f'doubling one transverse amplitude multiplies response by {ratios}')
    data=dict(source='arXiv:2502.14686v2 Eq. (3.22); arXiv:2507.02563v1 Eq. (9)',
              assumptions=dict(eta='sqrt(3) for all three species',alphabar=1,
                               omega=omegas.tolist(),time_window=[100,600],
                               approximation='quadratic dipole expansion; constant local g; no spatial gradients'),
              rows=rows,checks=checks,
              verdict='A coherent transverse response can generate D proportional to g^2; sign and normalization remain initial data',
              open=['pump/transport selects chirality and amplitude','full Poisson/matter feedback','cosmology and UV completion',
                    'energy and stability of a driven through-flow','no universal a0 or exact P2 law established'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failures=sum(not x['passed'] for x in checks)
    print(f'{len(checks)-failures}/{len(checks)} checks pass; {failures} failures. Original theory goal OPEN.')
    return int(failures>0)


if __name__=='__main__':
    raise SystemExit(main())
