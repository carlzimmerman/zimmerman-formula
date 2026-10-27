import json,argparse
from pathlib import Path
import numpy as np
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();p=Path(__file__).parent
load=lambda d:{r['label']:r for r in json.loads((p/d/'result.json').read_text())['rows']}
s=load('survey_run');l=load('long_run');f=load('refine_run');x=np.linspace(0,4,1001)
def cdf(r):
 rr=abs(np.array(r['final_r']));mi=np.array(r['shell_mass']);return np.array([sum(mi[rr<=xx])/sum(mi) for xx in x])
def mean(r):
 end=r['rows'][-1]['time'];return np.mean([q['masses'] for q in r['rows'] if q['time']>=2*end/3],axis=0)/r['mass']
def gap(a,b):return float(max(abs(cdf(a)-cdf(b))))
results=[]
def gate(name,ok,value):results.append(dict(name=name,passed=bool(ok),value=value));print(name,ok,value)
coarsefine=gap(s['baseline_1_0.02'],s['fine_grid']);finest=gap(s['fine_grid'],f['ultrafine']);meangap=float(max(abs(mean(s['fine_grid'])-mean(f['ultrafine']))))
gate('finest_profile_CDF',finest<.05,finest);gate('finest_time_average',meangap<.05,meangap)
for label,a1,b1 in [('unit_mass',s['baseline_1_0.02'],f['ultrafine']),('mass4_baseline',s['baseline_4_0.02'],f['mass4_fine']),('mass4_strong',l['long_4'],f['mass4_strong_fine'])]:
 dd=abs(a1['rows'][-1]['masses'][3]-b1['rows'][-1]['masses'][3])/a1['mass'];gate('bulk_'+label,dd<.05,dd)
ra=l['long_4']['rows'][-1]['flux6'][1];rb=f['mass4_strong_fine']['rows'][-1]['flux6'][1];rd=abs(ra/rb-1);gate('strong_phase_flux_repeat',ra>0 and rb>0 and rd<.30,rd)
mm=np.array([l['long_'+str(m)]['rows'][-1]['masses'][3] for m in [1,2,4]]);spread=float(np.ptp(mm)/np.mean(mm));gate('common_finite_time_mass',spread<.1,spread)
E=json.loads((p/'energy_run2/result.json').read_text());targets=E['targets'];energy_refine=[dict(mass_ratio=m,relative_difference=abs(next(q['energy'] for q in targets if q['mass_ratio']==m and q['n']==256)/next(q['energy'] for q in targets if q['mass_ratio']==m and q['n']==512)-1)) for m in [.5,1,2,4]]
out=dict(interpretation_gates=results,coarse_fine_CDF=coarsefine,finest_CDF=finest,finest_mean_difference=meangap,endpoint_energy_refinement=energy_refine,scope='Finite numerical interpretation; failed gates remain failed')
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
