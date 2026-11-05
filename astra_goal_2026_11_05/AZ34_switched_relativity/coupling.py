#!/usr/bin/env python3
"""P3 vertex estimates on the declared positive-divergence backgrounds."""
import hashlib
import json
import math
import os
from pathlib import Path
import sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import mpmath as mp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
P3=ROOT/'rebuild_2026_10_22/P3_v3_strong_field'
source=(P3/'p3_v3_strong_field.py').read_text()
record=json.loads((P3/'p3_v3_strong_field_results.json').read_text())
c_SI=299792458.;GMSUN=1.32712440018e20;PC=3.0856775814913673e16
AU=1.495978707e11;MU_K=1/(100000*PC);SQK=math.sqrt(4*math.pi)*1.616255e-35
c_tt,c_zz,c_tilt=[float(record['E3'][k]) for k in ('c_tt','c_zz','c_tilt')]
exec(compile(source[source.index('def scales(zh, zPh, gh'):source.index('sysres = {}')],
             'P3[read-only scales definitions]','exec'))

def precise(zh,zp,gh,k,om,a0m,du,M,L,Q):
    """Independent 50-digit evaluation of the stated vertex coefficients."""
    with mp.workdps(50):
        zh,zp,gh,k,om,a0m,du,M,L,Q=map(lambda x:mp.mpf(str(x)),(zh,zp,gh,k,om,a0m,du,M,L,Q))
        sqk=mp.sqrt(4*mp.pi)*mp.mpf('1.616255e-35')
        mu=mp.mpf(str(MU_K));cp=mp.sqrt(gh/zh);energy=max(om/mp.mpf('299792458'),cp*k)
        vertices=[(zp*abs(c_zz)/2,2),(zp*abs(c_tt)/2,0),(zp*abs(c_tilt),0),
                  (mu**2/(2*Q**2),2),(a0m**2*k**3/(3*du**3*(M+L**2*k**2/2)**3),0)]
        eps=[]
        for lam,nx in vertices:
            cutoff2=zh**mp.mpf('1.5')*cp**(mp.mpf('1.5')+nx)/(lam*sqk)
            eps.append(energy**4/cutoff2**2)
        lam4=zp*(abs(c_zz)/2)**2/2
        cutoff4=zh**2*cp**7/(lam4*sqk**2)
        eps.append(energy**4/cutoff4)
        return dict(eps_max=float(max(eps)),mixing=float(mp.sqrt(zp)*cp/energy),all_eps=list(map(float,eps)))

footings={'canonical':9.3603e-11,'alt':1.1312e-10}
lengths={'canonical':(21.68,24.,27.,90.),'alt':(22.85,24.,24.60,90.)}
rows={};checks={};precision=[];known=[];mutants={}
for foot,a0 in footings.items():
    rows[foot]={};mutants[foot]={}
    for Lpc in lengths[foot]:
        L=Lpc*PC;ag=a0/c_SI**2
        phS=GMSUN/(AU*c_SI**2);phE=3.986e14/(6.371e6*c_SI**2)
        phB=2.59*GMSUN/(8.79e8*c_SI**2)
        systems={'Eot-Wash':(1/38.6e-6,1e-3,2*(phS+phE)/L**2),
                 'planets':(1/AU,2*math.pi/3.15576e7,2*phS/L**2),
                 'double pulsar':(1/8.79e8,2*math.pi/(2.45*3600),2*phB/L**2)}
        for name,(k,om,dP) in systems.items():
            for xe in (1.,2.,3.):
                for orientation,M in (('longitudinal',(1+xe)**2),('transverse',1+xe)):
                    u=ag*xe/(1+xe)+GMSUN/(c_SI**2*L**2)
                    du=ag-u
                    assert du>0, 'Do not silently omit an out-of-domain W cubic'
                    Q=1+1e-6;zp=zP_of(k,L,M,Q);zh=zp+MU_K**2
                    gh=dP*(1+dP*L**2/2)+MU_K**2*1e-6/Q
                    r=scales(zh,zp,gh,k,om,ag,du,M,L,Q)
                    high=precise(zh,zp,gh,k,om,ag,du,M,L,Q)
                    err=max(abs(r['eps_max']/high['eps_max']-1),abs(r['mixing_eps']/high['mixing']-1))
                    precision.append(err)
                    key=f'{name}|L{Lpc}|xe{xe}|{orientation}'
                    rows[foot][key]=dict(eps_max=r['eps_max'],mixing_eps=r['mixing_eps'],
                        energy_leakage_estimate=r['mixing_eps']**2,c_pi=r['c_pi'],
                        cap_margin=du/ag,divergence=dP,precision_relative=err,
                        W_cubic=r['vertices']['V6 pidot^3 [W cubic]']['eps'],
                        k_sc_min=min(v['k_sc_m-1'] for v in r['vertices'].values()))
                    # The inverted switch has F'=0 here whereas the main
                    # action has F'=gamma*dP. Their background equations differ.
                    mutants[foot][key]=dict(label='NOT EVALUABLE on shell',
                        main_branch_stiffness_factor=1,inverted_factor=0,
                        omitted_Fprime_over_gamma=dP,
                        reason='Positive-divergence screened background is not transferred to inverted switch.')
                    if Lpc==90 and name=='Eot-Wash':known.append(abs(r['eps_max']/1.312e-3-1))
    production=[v for k,v in rows[foot].items() if '|L90.0|' not in k]
    checks[foot+'_estimate']=max(v['eps_max'] for v in production)<=1e-2
checks['known_EotWash90']=max(known)<=.01
checks['float64_vs_50digits']=max(precision)<=1e-10
inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        (Path(__file__),HERE/'FROZEN_CRITERIA.md',P3/'p3_v3_strong_field.py',P3/'p3_v3_strong_field_results.json')}
for mode,data in (('main',rows),('mutate',mutants)):
    result=dict(label=('PASS scoped estimate' if all(checks.values()) else 'UNDECIDED') if mode=='main' else 'NOT EVALUABLE on shell',
                mode=mode,footings=data,checks=checks if mode=='main' else {},
                precision_max_relative=max(precision),known_max_relative=max(known),inputs=inputs,
                assumptions='P3 decoupling estimate, background-gradient truncation, Qbar-1=1e-6 illustrative, mu_K^-1=100kpc inherited, x_e bracket1..3; no nonlinear/interface EFT claim',
                statement='kappa = 1/2 FITTED; not theory closed')
    p=HERE/mode/'coupling.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');os.replace(tmp,p)
print('checks',checks,'precision',max(precision),'known',max(known))
for f,r in rows.items():
    production={k:v for k,v in r.items() if '|L90.0|' not in k}
    print(f,'max_eps',max(v['eps_max'] for v in production.values()),
          'max_pulsar_leakage',max(v['energy_leakage_estimate'] for k,v in production.items() if k.startswith('double pulsar')))
sys.exit(0 if all(checks.values()) else 1)
