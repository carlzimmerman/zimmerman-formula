"""Exploratory source comparison on local raw SPARC; no discovery verdict."""
import ast
import builtins
import json
import math
import os
import sys
from pathlib import Path
import numpy as np

checks=[]
def check(name,condition):
    ok=bool(condition)
    checks.append(dict(name=name,passed=ok))
    if not ok:
        raise AssertionError(name)

# Execute only the existing read-only loader; do not initialize CFG4 or its Run.
source=Path('campaign_fresh_gravity/CFG4_common.py')
tree=ast.parse(source.read_text())
func=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='load_sparc']
check('unique existing raw SPARC loader',len(func)==1)
env=dict(np=np,os=os,builtins=builtins,DATA='real_research/data')
exec(compile(ast.Module(body=func,type_ignores=[]),str(source),'exec'),env)
gals=env['load_sparc']()
check('175 local rotation curves loaded',len(gals)==175)
fp0=json.loads(Path('real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
footings={'canonical':float(fp0['a0_canonical']),'alt':float(fp0['a0_rho_total'])}
KPC=3.0856775814913673e19
UPS=np.round(np.arange(.1,2.0001,.01),2)
UPS5=np.round(np.arange(.1,5.0001,.01),2)

def u_of(bs,a0):
    bs=np.asarray(bs)
    root=np.sqrt(bs*bs+4*a0*bs)
    return np.divide(2*a0*bs,root+bs,out=np.zeros_like(bs),where=(bs>0))

for a0 in footings.values():
    bs=np.array([0.,a0*1e-4,a0,a0*1e3])
    u=u_of(bs,a0)
    check('positive saturation root stable on fixed source grid',np.all((u>=0)&(u<a0)))
    check('root reproduces exact simple law',np.allclose(u[1:]**2/(a0-u[1:]),bs[1:],rtol=1e-9,atol=1e-25))
    check('all baryons eligible reproduces simple-kernel total acceleration',
          np.allclose(bs[1:]+u[1:],(bs[1:]+np.sqrt(bs[1:]**2+4*a0*bs[1:]))/2,rtol=1e-14))

sample=[]
for g in gals:
    m=g['meta']
    if m is None or m['Q'] not in (1,2) or m['Inc']<30 or len(g['R'])<5:
        continue
    gas=np.sign(g['Vgas'])*g['Vgas']**2
    stars=.5*g['Vdisk']**2+.7*g['Vbul']**2
    total=gas+stars
    if total[-1]<=0 or gas[-1]<=0 or gas[-1]/total[-1]<.8:
        continue
    ok=(g['R']>0)&(g['eV']>0)&(g['Vobs']>0)&(total>0)
    if np.count_nonzero(ok)<5:
        continue
    sample.append((g,ok,float(gas[-1]/total[-1])))
check('gas-dominated sample nonempty',len(sample)>0)

def fit(g,ok,a0,eta,grid,mutate=False):
    radius=g['R'][ok]*KPC
    gas=(np.sign(g['Vgas'][ok])*g['Vgas'][ok]**2)*1e6/radius
    stars=(g['Vdisk'][ok]**2+1.4*g['Vbul'][ok]**2)*1e6/radius
    btotal=gas[:,None]+stars[:,None]*grid[None,:]
    bsource=eta*gas[:,None]+stars[:,None]*grid[None,:]
    valid=np.all((btotal>0)&(bsource>=0),axis=0)
    predictions=np.sqrt(np.maximum((btotal+u_of(np.maximum(bsource,0),a0))*radius[:,None],0))/1e3
    observed=g['Vobs'][ok]
    if mutate:
        bref=gas+.5*stars
        observed=np.sqrt((bref+u_of(bref,a0))*radius)/1e3
    c=np.sum(((predictions-observed[:,None])/g['eV'][ok,None])**2,axis=0)
    c[~valid]=math.inf
    best=int(np.argmin(c))
    return dict(chi2=float(c[best]),stellar_mass_to_light=float(grid[best]),
                residual_acceleration_rms_dex=float(np.sqrt(np.mean((2*np.log10(observed/predictions[:,best]))**2))))

summaries={}
for foot,a0 in footings.items():
    rows=[]
    for g,ok,fg in sample:
        only_star=fit(g,ok,a0,0.,UPS)
        star_gas=fit(g,ok,a0,1.,UPS)
        only_star5=fit(g,ok,a0,0.,UPS5)
        check('finite compared source scores '+foot+' '+g['name'],
              all(math.isfinite(x['chi2']) for x in [only_star,star_gas,only_star5]))
        control=fit(g,ok,a0,1.,UPS,mutate=True)
        check('synthetic all-eligible curve recovered '+foot+' '+g['name'],control['chi2']<1e-16)
        rows.append(dict(name=g['name'],points=int(np.count_nonzero(ok)),
                         outer_gas_force_fraction_at_reference_ups05=fg,
                         stars_only_eligible=only_star,stars_and_gas_eligible=star_gas,
                         stars_only_eligible_ups5=only_star5,
                         delta_chi2_stars_only_minus_stars_gas=only_star['chi2']-star_gas['chi2'],
                         delta_chi2_stars_only_ups5_minus_stars_gas=only_star5['chi2']-star_gas['chi2']))
    rows.sort(key=lambda x:-x['delta_chi2_stars_only_minus_stars_gas'])
    summaries[foot]=dict(galaxies=len(rows),
        count_delta_chi2_ge25=sum(r['delta_chi2_stars_only_minus_stars_gas']>=25 for r in rows),
        count_delta_chi2_ge25_allow_stars_ups5=sum(r['delta_chi2_stars_only_ups5_minus_stars_gas']>=25 for r in rows),
        median_delta_chi2=float(np.median([r['delta_chi2_stars_only_minus_stars_gas'] for r in rows])),
        rows=rows)
out=dict(checks=checks,selection='Q 1/2, inclination>=30deg, >=5 valid points, gas contributes >=80% of outer Newtonian radial force at reference Upsilon=.5; bulge=1.4*disc',
         footings=summaries,
         model='g_pred=gN_stars+gN_gas+u(gN_stars+eta_gas*gN_gas); eta_gas 0 vs1; u exact saturating positive root; all gas gravity always retained',
         status='exploratory comparison, no pre-existing frozen test or discovery claim',
         limitations=['fixed catalog distances and inclinations; velocity errors only; no covariance/systematics likelihood',
                      'independent per-galaxy stellar M/L grid .1..2 with stars-only bracket .1..5',
                      'gas template is supplied SPARC Vgas, not phase-resolved HI/H2/ionized thermometry',
                      'radial algebraic extension is phenomenological, not solved nonspherical carrier dynamics',
                      'Delta chi2 thresholds describe score differences, not independent sigma significances',
                      'no explanation of attachment, hot-gas behavior, medium production or finite supply'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),all_passed=all(x['passed'] for x in checks),
                      summaries={foot:{k:v for k,v in result.items() if k!='rows'} for foot,result in summaries.items()}),indent=2))
