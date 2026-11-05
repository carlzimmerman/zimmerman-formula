#!/usr/bin/env python3
"""Finite-time moving Fourier-source response on the declared charged PN background."""
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
t0=time.monotonic();checks={}
def check(k,v):checks[k]=bool(v)
k,K,rho0,M,gam,rm,rt=sp.symbols('k K rho0 M gamma rho_m rho_tau',real=True)
vdot=sp.I*K*rm/k-sp.I*(K*(M-1)/k+gam*k)*rt
rdd=sp.expand(-rho0*sp.I*k*vdot)
check('forced_equation',sp.simplify(rdd+rho0*(K*(M-1)+gam*k*k)*rt-K*rho0*rm)==0)
T,O,w,F=sp.symbols('t Omega omega F',positive=True)
solution=F*(sp.exp(-sp.I*w*T)-sp.cos(O*T)+sp.I*w*sp.sin(O*T)/O)/(O*O-w*w)
check('exact_forced_ODE',sp.simplify(sp.diff(solution,T,2)+O*O*solution-F*sp.exp(-sp.I*w*T))==0)
check('initial_data',solution.subs(T,0)==0 and sp.diff(solution,T).subs(T,0)==0)
check('zero_forcing',solution.subs(F,0)==0)
resonant=F*(sp.sin(O*T)/O-T*sp.exp(-sp.I*O*T))/(2*sp.I*O)
check('resonant_ODE',sp.simplify(sp.diff(resonant,T,2)+O*O*resonant-F*sp.exp(-sp.I*O*T))==0)
check('static_known',sp.simplify(solution.subs(w,0)-F*(1-sp.cos(O*T))/(O*O))==0)

def analytic(u,x,resonance):
    with mp.workdps(50):
        U=mp.mpf(str(u));X=U if resonance else mp.mpf(str(x))
        if resonance:answer=(mp.sin(U)/U-mp.exp(-mp.j*U))/(2*mp.j*U)
        else:answer=(mp.exp(-mp.j*X)-mp.cos(U)+mp.j*X*mp.sin(U)/U)/(U*U-X*X)
        convolution=mp.quad(lambda z:mp.sin(U*(1-z))/U*mp.exp(-mp.j*X*z),[0,1])
        err=float(abs(answer-convolution)/max(1,abs(answer)))
        return complex(answer),err
def numerical(u,x,tight):
    def rhs(T,y):return (y[1],np.exp(-1j*x*T)-u*u*y[0])
    sol=solve_ivp(rhs,(0,1),(0j,0j),method='DOP853',rtol=1e-11 if tight else 1e-9,atol=1e-13 if tight else 1e-11)
    return complex(sol.y[0,-1]),bool(sol.success)

PC=3.0856775814913673e16;AU=1.495978707e11;G=6.67430e-11;MSUN=1.98847e30
inputs={'canonical':dict(a0=9.3603e-11,rho=0.0447,xe=1.15,lengths=(21.68,24.,27.)),
        'alt':dict(a0=1.1312e-10,rho=0.0514,xe=2.6,lengths=(22.85,24.,24.60))}
rows={}
for foot,p in inputs.items():
    forcing=4*math.pi*G*p['rho']*MSUN/PC**3
    mt=(1+p['xe'])**2;data=[]
    for L in p['lengths']:
      for v in (220000.,369000.):
       for rAU in (1.,9.58):
        radius=rAU*AU;wave=1/radius
        omega=math.sqrt(forcing*(mt-1+(L*PC)**2*wave**2/2))
        pole=omega/(wave*v)
        check(f'{foot}_{L}_{v}_{rAU}_resonance_exists',0<pole<=1)
        for direction,cosine in (('transverse',0.),('resonant',pole),('parallel',1.)):
         for crossings in (1.,10.):
            tend=crossings*radius/v;u=omega*tend
            x=u if direction=='resonant' else wave*v*cosine*tend
            exact,err=analytic(u,x,direction=='resonant')
            coarse,ok0=numerical(u,x,False);fine,ok1=numerical(u,x,True)
            scale=max(1,abs(exact))
            e0=abs(coarse-exact)/scale;e1=abs(fine-exact)/scale;pair=abs(fine-coarse)/scale
            # rho_tau/rho_source = K rho0 t^2 h(1).
            transfer=forcing*tend*tend*exact
            data.append(dict(Lstar_pc=L,speed_m_s=v,r_AU=rAU,direction=direction,cosine=cosine,
                crossing_times=crossings,final_seconds=tend,Omega_per_s=omega,phase_speed_m_s=omega/wave,
                pole_cosine=pole,normalized_response=[exact.real,exact.imag],
                transfer=[transfer.real,transfer.imag],transfer_magnitude=abs(transfer),
                static_particular_transfer=forcing/omega**2,
                analytic_convolution_error=err,coarse_error=e0,fine_error=e1,pair_error=pair,integration_ok=ok0 and ok1))
    rows[foot]=dict(a0_m_s2=p['a0'],rho0_Msun_pc3=p['rho'],xe=p['xe'],cases=data)
    check(foot+'_convergence',max(max(v['coarse_error'],v['fine_error'],v['pair_error']) for v in data)<=1e-7)
    check(foot+'_analytic_convolution',max(v['analytic_convolution_error'] for v in data)<=1e-30)
    check(foot+'_integration',all(v['integration_ok'] for v in data))
sources=[Path(__file__),HERE/'FROZEN_CRITERIA.md',ROOT/'rebuild_2026_10_22/H4_v3_saddle_stability/README.md']
result=dict(label='PASS finite-time linear response; NO VERDICT full moving Sun',checks=checks,footings=rows,
    sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    scope='Frozen positive-divergence Galactic coefficients, zero initial response. Finite-time resonant response is regular; no uniform stationary static-to-moving transfer. No nonlinear halo, metric PPN inference or observational exclusion.',
    software=dict(scipy=scipy.__version__,numpy=np.__version__,sympy=sp.__version__,mpmath=mp.__version__),
    seconds=time.monotonic()-t0,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
    statement='kappa = 1/2 FITTED; not theory closed')
for mode in ('main','mutate'):
    result['mode']=mode;result['control_scope']='This invariant subtest is unchanged; the flat-congruence mutation bites in branch_and_flow.'
    out=HERE/mode;out.mkdir(exist_ok=True);tmp=out/'response.tmp';tmp.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');os.replace(tmp,out/'response.json')
print('checks',sum(checks.values()),'/',len(checks),'failed',[k for k,v in checks.items() if not v])
for f,d in rows.items():print(f,'cells',len(d['cases']),'max_pair',max(x['pair_error'] for x in d['cases']),'max_transfer',max(x['transfer_magnitude'] for x in d['cases']))
raise SystemExit(0 if all(checks.values()) else 1)
