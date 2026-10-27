import json,argparse
from pathlib import Path
import numpy as np
from scipy.stats import ks_2samp
p=Path(__file__).resolve().parent;pa=argparse.ArgumentParser();pa.add_argument('--output');args=pa.parse_args();names=['mass1','mass2','mass4','frozen','particles','space','box','angular','long','seed'];runs={name:json.loads((p/(name+'_run')/'result.json').read_text()) for name in names};checks=[];gates=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=v))
def gate(n,b,v):gates.append(dict(name=n,passed=bool(b),value=v))
for name,r in runs.items():
 ck('energy_'+name,r['max_energy_error']<1e-3,r['max_energy_error']);ck('completed_interval_'+name,r['stop_reason']=='time_limit',r['stop_reason'])
base=runs['mass4'];z=base['rows'][-1];frozen=runs['frozen']['rows'][-1]['absorbed'];ck('frozen_export_control',frozen/z['absorbed']<.01,frozen/z['absorbed'])
repeat=[]
for name in ['particles','space','box']:
 r=runs[name];q=r['rows'][-1];cdf=float(ks_2samp(np.linalg.norm(base['final_x'],axis=1),np.linalg.norm(r['final_x'],axis=1)).statistic);loss=abs(q['absorbed']/z['absorbed']-1);flux=abs(q['flux'][1]/z['flux'][1]-1);repeat.append(dict(name=name,cdf=cdf,loss_difference=loss,chi_flux_difference=flux));gate('absorption_repeat_'+name,loss<.2,loss);gate('profile_repeat_'+name,cdf<.05,cdf);gate('chi_flux_repeat_'+name,flux<.2,flux)
ck('instrumentation_same_trajectory',np.max(abs(np.array(runs['angular']['final_x'])-np.array(base['final_x'])))<1e-12,float(np.max(abs(np.array(runs['angular']['final_x'])-np.array(base['final_x'])))))
gate('full_selected_mass_partition',False,'No persistent bound fragment mass spectrum established');gate('joint_observational_preservation',False,'No live baryons or cosmology')
summary=[]
for name in ['mass1','mass2','mass4','long','seed']:
 r=runs[name];x=np.array(r['final_x']);v=np.array(r['final_v']);x-=x.mean(0);v-=v.mean(0);A=np.linalg.lstsq(x,v,rcond=None)[0];vrem=v-x@A;z=r['rows'][-1];summary.append(dict(name=name,time=r['stop_time'],mass_over_canonical=r['parameters']['mass']/.08408132497418408,loss_fraction=z['absorbed']/abs(r['E0']),final_half_mass_radius=z['r50'],nonaffine_kinetic_fraction=float(np.sum(vrem*vrem)/np.sum(v*v)),mass_apertures=z['mass_apertures'],ejecta_candidate_fraction=r['partition']['candidate_newtonian_ejecta_fraction']))
long=runs['long'];a18=min(long['rows'],key=lambda z:abs(z['t']-18))['absorbed'];a42=min(long['rows'],key=lambda z:abs(z['t']-42))['absorbed'];cool=(long['rows'][-1]['absorbed']-a42)/a18
result=dict(checks=checks,interpretation_gates=gates,repeat=repeat,summary=summary,export_mass4_over_mass1=runs['mass4']['rows'][-1]['absorbed']/runs['mass1']['rows'][-1]['absorbed'],late_to_early_equal_interval_export=cool,max_total_J_error=max(z['total_L_relative_error'] for z in runs['angular']['rows']))
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
