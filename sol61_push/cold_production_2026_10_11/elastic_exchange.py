"""Finite audit of equal-mass isotropic elastic energy exchange; no halo solver."""
import json, math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
p=Path(__file__).parent
root=p.parents[1]
checks=[]
def check(name, value): checks.append(dict(name=name,passed=bool(value)))
def direct(sa,sb,n):
    # Independent integration over speeds of the two incoming Maxwellians,
    # and their relative angle. Per collision angle-averaged delta E_a=(vb²-va²)/4.
    x,q=leggauss(n); z=x[None,None,:]; wz=q[None,None,:]/2
    u=5*(x+1); weights=5*q*math.sqrt(2/math.pi)*u*u*np.exp(-u*u/2)
    va=np.sqrt(sa)*u[:,None,None]; vb=np.sqrt(sb)*u[None,:,None]
    w=np.sqrt(np.maximum(va*va+vb*vb-2*va*vb*z,0))
    return float(np.sum(weights[:,None,None]*weights[None,:,None]*wz*w*(vb*vb-va*va)/4))
rows=[]
for sa,sb in [(1.,4.),(4.,1.),(.0025,.5),(1.,1.)]:
    # n_a=n_b=m=sigma=1 here. Maxwell relative velocity variance S.
    S=sa+sb
    analytic=2*math.sqrt(2/math.pi)*math.sqrt(S)*(sb-sa)
    d64=direct(sa,sb,64); d96=direct(sa,sb,96)
    check('independent incoming-velocity quadrature '+str((sa,sb)),abs(d96-analytic)<2e-6*max(1,abs(analytic)))
    check('quadrature refinement '+str((sa,sb)),abs(d96-d64)<5e-6*max(1,abs(analytic)))
    # unequal populations verify total energy, not equal temperature changes
    na,nb=2.,7.
    dsa=nb*(sb-sa)*(8*math.sqrt(2/math.pi)*S**1.5)/(6*S)
    dsb=na*(sa-sb)*(8*math.sqrt(2/math.pi)*S**1.5)/(6*S)
    check('weighted energy conservation '+str((sa,sb)),abs(na*dsa+nb*dsb)<1e-12)
    rows.append(dict(sa=sa,sb=sb,analytic_power=analytic,quadrature64=d64,quadrature96=d96))
low=json.loads((root/'sol61_push/collective_energy_lower_2026_10_11/run/results.json').read_text())
capacity=[]
for row in low['rows']:
    sa=.05**2; target=2*row['Klower_over_M']/3; bath=.5
    mu=(target-sa)/(bath-target)
    endpoint=(sa+mu*bath)/(1+mu)
    check('finite bath capacity '+row['cell'], mu>0 and abs(endpoint-target)<1e-14)
    capacity.append(dict(cell=row['cell'],target_sigma_squared_over_Vf_squared_lower=target,assumed_bath_sigma_squared_over_Vf_squared=bath,min_bath_mass_over_target=mu))
# Illustrative LOCAL rates; neither density nor warm reservoir is predicted.
# sigma/m=1 cm²/g=.1 m²/kg, both dispersions 200 km/s.
rate_rows=[]
kpc=3.085677581491367e19; Gyr=365.25*86400*1e9
for rho in [1e-21,1e-23]:
    sm=.1; S=2*(2e5)**2
    collision=rho*sm*2*math.sqrt(2/math.pi)*math.sqrt(S)
    relaxation=(2/3)*collision
    mean_free_path=1/(rho*sm)
    rate_rows.append(dict(bath_density_kg_m3=rho,collision_time_Gyr=1/collision/Gyr,fixed_bath_temperature_relaxation_time_Gyr=1/relaxation/Gyr,mean_free_path_kpc=mean_free_path/kpc,optical_depth_across_100_kpc=100*kpc/mean_free_path))
out=dict(checks=checks,all_pass=all(x['passed'] for x in checks),quadrature=rows,capacity=capacity,illustrative_local_rates=rate_rows,non_claims=['No derived bath state, mass, geometry or halo evolution','Maxwellian assumption gives instantaneous moment, not closed Boltzmann evolution','Constant isotropic cross section surrogate; no resonance-tail integration','Capacity ignores gravity, escape and spatial redistribution'])
(p/'elastic_exchange_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
