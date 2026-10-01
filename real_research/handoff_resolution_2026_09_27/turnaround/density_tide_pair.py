#!/usr/bin/env python3
"""Spherical paired-environment P2 flux and ESD; environment radius 5 Mpc is a test input.
MUTATE removes the matched environment subtraction and fails the zero-lens control.
This is not an observational random-catalogue subtraction or a KiDS likelihood.
"""
from pathlib import Path
import os,math,json
for v in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS']:os.environ[v]='2'
import numpy as np
H=Path(__file__).resolve().parent; s=(H/'mirror/real_research/derivation_chain_2026/FP20_esd_projection_fix.py').read_text(); ns={'np':np,'math':math};exec(s[s.index('def shell_mats('):s.index('class M2Fix:')],ns)
G=6.6743e-11; MS=1.98892e30; MPC=3.0857e22; PC=MPC/1e6; c=2.99792458e8
h=.6736; H0=100*h*1e3/MPC; Om=(.02237+.1200)/h**2; z=.25; rho=3*H0**2*Om*(1+z)**3/(8*np.pi*G)
rr=np.geomspace(1e-4,400,16000)*MPC; R=np.array([.1,.3,.6,1.,2.,3.]); fix=ns['ESDFix'](rr,R*MPC,PC,MS); envR=5*MPC
Menv=4*np.pi*rho*np.minimum(rr,envR)**3/3; gt=G*Menv/rr**2; Mb=1e11*MS; gb=G*Mb/rr**2
MUT=os.environ.get('MUTATE')=='1'; out={'mutate':MUT,'checks':{},'numbers':{},'scope':'uniform peculiar delta=1 within 5 Mpc, fixed center, point baryons, both footings; density tide matched environment subtraction, no dynamical solution'}
for foot,a0 in {'canonical':9.3603e-11,'alt':1.1312e-10}.items():
 p=lambda g:g*(np.sqrt(1+a0/np.maximum(g,1e-80))-1)
 pair=lambda g,t:p(g+t)-(0 if MUT else p(t))
 null=float(np.max(abs(pair(np.zeros_like(gb),gt))/a0));out['checks'][f'zero_lens/{foot}']={'ok':null<1e-14,'value':null}
 mph_pair=rr**2/G*pair(gb,gt); mph_iso=rr**2/G*p(gb)
 paired=fix(Mb+mph_pair,0.); iso=fix(Mb+mph_iso,0.)
 samples=[]
 for r in R:
  radius=r*MPC; b=G*Mb/radius**2;t=4*np.pi*G*rho*radius/3;e=t/b
  samples.append({'R_Mpc':r,'e_tide_over_baryon':e,'exact_phantom_excess_ratio':float(pair(b,t)/p(b)),'deep_limit':float(np.sqrt(1+e)-np.sqrt(e))})
 out['numbers'][foot]={'force_samples':samples,'ESD_R_Mpc':R.tolist(),'isolated_ESD_Msun_pc2':iso.tolist(),'paired_ESD_Msun_pc2':paired.tolist(),'paired_over_isolated_ESD':(paired/iso).tolist()}
 # Independent projector linearity control in the unmutated reading, includes point-mass separately.
 split=fix(Mb+rr**2/G*p(gb+gt),0.)-fix(rr**2/G*p(gt),0.)
 err=float(np.max(abs(split-paired)/np.maximum(abs(paired),1e-12)));out['checks'][f'projection_linearity/{foot}']={'ok':err<1e-8,'value':err}
out['verdict']='pass' if all(v['ok'] for v in out['checks'].values()) else 'failed';(H/f"density_tide_pair_results{'_MUTATE' if MUT else ''}.json").write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));raise SystemExit(0 if out['verdict']=='pass' else 1)
