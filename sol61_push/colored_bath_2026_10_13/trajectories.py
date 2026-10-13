#!/usr/bin/env python3
"""Bounded nonlinear Duffing trajectories under the prescribed delayed OU force.
Coupled coarse/fine noise; no inferred astrophysical or universal crossing rate.
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.special import ellipk, ellipj

SEED=20261013; N=512; STEPS=1024; PERIODS=10
rng=np.random.default_rng(SEED)
phase=rng.uniform(0,1,N)
a2R=4/(1+np.sqrt(5)); TR=4*ellipk(a2R/(2*(1+a2R)))/np.sqrt(1+a2R)
dt=TR/STEPS
# Exact OU samples at grid endpoints, including one period of stationary history.
eta=np.empty(((PERIODS+1)*STEPS+1,N));eta[0]=rng.normal(size=N)
rho=np.exp(-dt); innov=np.sqrt(-np.expm1(-2*dt))
for i in range(1,len(eta)):eta[i]=rho*eta[i-1]+innov*rng.normal(size=N)
sigmas=np.array([.001,.003,.01]); E0=1-sigmas
x0=[];p0=[]
for E in E0:
 a2=4*E/(1+np.sqrt(1+4*E));w=np.sqrt(1+a2);m=a2/(2*(1+a2))
 sn,cn,dn,_=ellipj(4*ellipk(m)*phase,m)
 x0.append(np.sqrt(a2)*cn);p0.append(-np.sqrt(a2)*w*sn*dn)
x0=np.array(x0);p0=np.array(p0)
def energy(x,p):return p*p/2+x*x/2+x**4/4

def simulate(stride):
 h=dt*stride;x=x0.copy();p=p0.copy();xb=x0.copy();pb=p0.copy()
 crossed=np.zeros_like(x,dtype=bool);baseline_error=np.zeros(3)
 for j in range(STEPS, (PERIODS+1)*STEPS,stride):
  xi0=eta[j]-eta[j-STEPS];xi1=eta[j+stride]-eta[j+stride-STEPS]
  ph=p+h/2*(-x-x**3+sigmas[:,None]*xi0)
  x=x+h*ph
  p=ph+h/2*(-x-x**3+sigmas[:,None]*xi1)
  pbh=pb+h/2*(-xb-xb**3);xb=xb+h*pbh;pb=pbh+h/2*(-xb-xb**3)
  crossed|=energy(x,p)>1
  baseline_error=np.maximum(baseline_error,np.max(abs(energy(xb,pb)-E0[:,None]),axis=1))
 return dict(final_energy=energy(x,p),crossed=crossed,baseline_error=baseline_error)
coarse=simulate(2);fine=simulate(1)
checks=[];rows=[]
for i,sigma in enumerate(sigmas):
 rms=float(np.sqrt(np.mean((fine['final_energy'][i]-coarse['final_energy'][i])**2)))
 fraction=float(np.mean(fine['crossed'][i]));frac_coarse=float(np.mean(coarse['crossed'][i]))
 # Wilson interval for sampled path fraction, not time-discretization bias.
 z=1.959963984540054;den=1+z*z/N
 center=(fraction+z*z/(2*N))/den
 half=z*np.sqrt(fraction*(1-fraction)/N+z*z/(4*N*N))/den
 passed=(rms<.03*sigma and abs(fraction-frac_coarse)<.03 and fine['baseline_error'][i]<.05*sigma)
 checks.append(dict(sigma=float(sigma),passed=bool(passed),
                    energy_grid_difference_limit=float(.03*sigma),cross_fraction_grid_limit=.03,
                    unforced_energy_error_limit=float(.05*sigma)))
 rows.append(dict(sigma=float(sigma),initial_gap=float(sigma),paths=N,elapsed_periods=PERIODS,
                  sampled_paths_crossing_ER=int(sum(fine['crossed'][i])),crossing_fraction=fraction,
                  wilson95=[float(center-half),float(center+half)],coarse_crossing_fraction=frac_coarse,
                  fine_unforced_max_energy_error=float(fine['baseline_error'][i]),
                  coarse_fine_final_energy_RMS_difference=rms,
                  final_energy_increment_variance_over_sigma2=float(np.var(fine['final_energy'][i]-E0[i],ddof=1)/sigma**2)))
result=dict(seed=SEED,generator='NumPy PCG64 via default_rng',paths=N,finest_steps_per_period=STEPS,
            coarse_steps_per_period=STEPS//2,elapsed_periods=PERIODS,delay=TR,rows=rows,
            checks=checks,all_passed=all(c['passed'] for c in checks),
            scope='Finite stochastic trajectory sample in prescribed external colored force, fixed initial gaps equal to sigma. Crossings are diagnostic, not absorbing. No cold-carrier drift, feedback, or empirical calibration.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(0 if result['all_passed'] else 1)
