"""Enlarge the recorded pair-gas comparison by the pole-free mixed crossing.

The definitions-only parent extraction and exact one-line reaction replacement
are saved for review. No source-pole-containing or raw six-point rate is added.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator

out=Path(sys.argv[1]);assert out.is_dir()
base=Path(__file__).parent
table=json.loads((base/'source_assisted_rate_table_run_002/results.json').read_text())
K=table['NR_event_coefficient_GeVminus5']
parent=base/'pair_conversion_closure.py'
source=parent.read_text();marker='\nruns=[]'
assert source.count(marker)==1
prefix=source.split(marker)[0]
old='P=B*B*rr.pair_reverse(T)*y*y*(math.exp(-min(2*m/T,750))-y*y)'
new='P=(B*B*rr.pair_reverse(T)+2*source_assisted_K3zero*B*(n/y)**2*assisted_correction(T))*y*y*(math.exp(-min(2*m/T,750))-y*y)'
assert prefix.count(old)==1
prefix=prefix.replace(old,new)
(out/'executed_parent_definitions.py').write_text(prefix)
ns={'__file__':str(parent),'__name__':'assisted_gas_definitions',
    'source_assisted_K3zero':K,'assisted_correction':lambda T:0.}
exec(compile(prefix,str(parent),'exec'),ns)
m=ns['m'];check=ns['check'];runs=[]

def correction(coarse=False,flat_tail=False):
    rows=[r for r in table['rows'] if not coarse or r['on_coarse_grid']]
    xs=np.array([r['Tdark_over_m'] for r in rows])
    hs=np.array([r['gamma3_over_NR'] for r in rows])
    interpolation=PchipInterpolator(np.log(xs),np.log(hs),extrapolate=False)
    def rate(T):
        x=T/m
        assert 0<x<=3*(1+1e-10),('rate domain',x)
        if x<xs[0]:return 1. if flat_tail else math.exp(math.log(hs[0])*x/xs[0])
        return math.exp(float(interpolation(math.log(min(x,3.)))))
    return rate

def run(ratio,label,callback,refined=False):
    ns['assisted_correction']=callback
    r=ns['evolve'](ratio,True,ns['rate128'] if refined else ns['rate64'],2e-9 if refined else 2e-7)
    r['reaction_set']=label
    r['scope_gates']={
        'MB_occupation_below_0p02':r['max_MB_occupation']<.02,
        'source_decay_over_evolution_above_1e5':r['min_decay_over_evolution_rate']>1e5,
        'elastic_lower_over_evolution_above_10':r['min_elastic_over_evolution_rate']>10}
    check('energy ceiling '+label+str(ratio),r['peak_yield_ratio']<=r['initial_energy_ceiling_on_yield_ratio']*(1+1e-7))
    runs.append(r)
    print(json.dumps({k:v for k,v in r.items() if k!='samples'}),flush=True)
    return r

oldruns=json.loads((base/'pair_conversion_run_004/results.json').read_text())['runs']
for ratio in (.3,1.,3.):
    baseline=run(ratio,'pair_only_control',lambda T:0.)
    oldrun=next(r for r in oldruns if r['pair_enabled'] and r['initial_Tdark_over_m']==ratio)
    check('parent baseline reproduction '+str(ratio),abs(baseline['final_yield_ratio']/oldrun['final_yield_ratio']-1)<1e-7)
    fine=run(ratio,'pair_and_pole_free_assisted',correction())
    coarse=run(ratio,'coarse_temperature_grid_control',correction(True))
    for key in ('final_yield_ratio','final_T_dark_GeV'):
        check('temperature interpolation '+key+str(ratio),abs(coarse[key]/fine[key]-1)<.003)
    if ratio==.3:
        refined=run(ratio,'joint_ODE_pair_rate_refinement',correction(),True)
        tail=run(ratio,'flat_NR_tail_control',correction(flat_tail=True))
        for key in ('final_yield_ratio','final_T_dark_GeV'):
            check('ODE refinement '+key,abs(refined[key]/fine[key]-1)<2e-5)
            check('NR tail control '+key,abs(tail[key]/fine[key]-1)<2e-5)

result=dict(parameters=table['parameters'],NR_event_coefficient_GeVminus5=K,
    model='specified initial states; fast source partial equilibrium; common MB gas; pair plus two conjugate pole-free mixed source-assisted channels',
    initial_total_weighted_yield=ns['yield_total'],runs=runs,checks=ns['checks'],
    failed_scope_gates=[dict(ratio=r['initial_Tdark_over_m'],reaction_set=r['reaction_set'],gate=k) for r in runs for k,v in r['scope_gates'].items() if not v],
    non_claims=['No Higgs-era initial-state derivation','No source-pole-containing assisted crossing, full six-point remainder, Bose/medium corrections or full momentum solution','No relic-density, galaxy-response, metric or universal novelty closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('All %d bounded numerical controls passed.'%len(ns['checks']))
