#!/usr/bin/env python3
"""Solar-interior input inventory and analytic validation; fixtures are not a solar model."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
mode='mutate' if args.mutate else 'main';out=HERE/mode;out.mkdir(exist_ok=True)
t0=time.monotonic();checks={}
def check(k,v):checks[k]=bool(v)
pattern=r'cptrho|fgong|helio_b16|bs05|bs16|agss09|gs98|solar[_ -]?(?:model|interior|profile|density)'
regex=re.compile(pattern,re.I)
command=['rg','--files','--hidden','--no-ignore','-g','!**/.git/**','-g','!.git/**','.']
proc=subprocess.Popen(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
count=0;matches=[]
for line in proc.stdout:
    name=line.strip().removeprefix('./');count+=1
    if name.startswith(str(HERE.relative_to(ROOT))+'/'):continue
    if regex.search(name):matches.append(name)
stderr=proc.stderr.read();rc=proc.wait()
check('inventory_completed',rc==0 and not stderr)
inventory=dict(command=command,pattern=pattern,file_count=count,candidate_paths=sorted(matches),
    scope='Filename discovery only; candidates require provenance inspection. No authenticated solar profile is selected automatically.')
x,q=sp.symbols('x q',nonnegative=True)
C=sp.simplify(1/sp.integrate(q*q*(1-q*q)**3,(q,0,1)))
profiles={'uniform':sp.Integer(3),'manufactured':C*(1-x*x)**3*(-1 if args.mutate else 1)}
exact={}
for name,density in profiles.items():
    mass=sp.integrate(density.subs(x,q)*q*q,(q,0,x))
    potential=sp.simplify(mass/x+sp.integrate(density.subs(x,q)*q,(q,x,1)))
    exact[name]=dict(density=density,mass=mass,potential=potential)
check('uniform_exact_known',sp.simplify(exact['uniform']['potential']-(3-x*x)/2)==0)
check('normalization_exact',sp.integrate(C*(1-q*q)**3*q*q,(q,0,1))==1)
for name,e in exact.items():
    check(name+'_Poisson_identity',sp.simplify(sp.diff(x*x*sp.diff(e['potential'],x),x)+x*x*e['density'])==0)

GM=1.32712440018e20;RSUN=6.957e8;PC=3.0856775814913673e16
footings={'canonical':(9.3603e-11,(21.68,24.,27.)), 'alt':(1.1312e-10,(22.85,24.,24.60))}
rows={}
for foot,(a0,lengths) in footings.items():
    rows[foot]=dict(a0_m_s2=a0,profiles={})
    for name,e in exact.items():
        results=[];arrays=[]
        for intervals in (256,512):
            xx=np.linspace(0,1,intervals+1)
            ww=np.broadcast_to(sp.lambdify(x,e['density'],'numpy')(xx),xx.shape)
            mass=cumulative_trapezoid(ww*xx*xx,xx,initial=0)
            shell=cumulative_trapezoid(ww*xx,xx,initial=0)
            U=np.divide(mass,xx,out=np.zeros_like(xx),where=xx>0)+shell[-1]-shell
            known=np.broadcast_to(sp.lambdify(x,e['potential'],'numpy')(xx),xx.shape)
            error=float(np.max(np.abs(U-known)))
            mass_error=float(abs(mass[-1]-float(e['mass'].subs(x,1))))
            arrays.append(U)
            estimates={}
            for L in lengths:
                minusPhi=GM/RSUN*U
                # K*s=2(-Phi)/L². Report s/(a0/(K L)), retaining each footing.
                s_normalized=2*minusPhi/(a0*L*PC)
                cs2=np.where(s_normalized>0,minusPhi,0.)
                estimates[str(L)]=dict(center_s_normalized=float(s_normalized[0]),
                    min_s_normalized=float(s_normalized.min()),
                    center_cs2_m2_s2=float(cs2[0]),min_cs2_m2_s2=float(cs2.min()),
                    center_cs_m_s=float(np.sqrt(cs2[0])))
            results.append(dict(intervals=intervals,mass_integral=float(mass[-1]),mass_error=mass_error,
                potential_max_error=error,center_U=float(U[0]),nonnegative_density=bool(np.all(ww>=0)),estimates=estimates))
        pair=float(np.max(np.abs(arrays[0]-arrays[1][::2])))
        rows[foot]['profiles'][name]=dict(levels=results,pair_absolute_change=pair,
            classification='analytic engine fixture; not a realistic solar model')
        check(foot+'_'+name+'_convergence',pair<=1e-4 and max(r['potential_max_error'] for r in results)<=1e-4 and max(r['mass_error'] for r in results)<=1e-4)
        check(foot+'_'+name+'_positive_density',all(r['nonnegative_density'] for r in results))
        check(foot+'_'+name+'_positive_mass',all(r['mass_integral']>0 for r in results))
        check(foot+'_'+name+'_positive_switched_speed',all(z['min_cs2_m2_s2']>0 for r in results for z in r['estimates'].values()))
sources=[Path(__file__),HERE/'FROZEN_CRITERIA.md',ROOT/'rebuild_2026_10_22/V3X_v3s_close_undecided/v3x_w4c_health.py']
result=dict(mode=mode,label='NOT EVALUABLE realistic solar interior: authenticated profile not located',
    checks=checks,inventory=inventory,footings=rows,
    exact={n:{k:str(v) for k,v in e.items()} for n,e in exact.items()},
    sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    scope='Radial Green integral and leading screened estimate only; no realistic-data or full-interior health verdict.',
    software=dict(numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__),
    seconds=time.monotonic()-t0,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
    statement='kappa = 1/2 FITTED; not theory closed')
tmp=out/'results.tmp';tmp.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');os.replace(tmp,out/'results.json')
print(mode,sum(checks.values()),'/',len(checks),'candidates',len(matches),'failed',[k for k,v in checks.items() if not v])
for name in matches:print('candidate',name)
raise SystemExit(0 if all(checks.values()) else 1)
