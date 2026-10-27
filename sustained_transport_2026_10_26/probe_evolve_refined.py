"""Paired live moving-boundary response; never used as formation seeds."""
import argparse,json
from pathlib import Path
import numpy as np
from evolve import run
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();dest=Path(args.output);cases={}
for d in [0.,-.01,.01]:
 label='case_'+str(d);sub=dest.parent/label;sub.mkdir();out=sub/'results.json'
 c={'case':'dilated','restart':'sustained_transport_2026_10_26/run_probe_initial/state_'+str(d)+'.npz','start_Myr':5.7,'duration_Myr':6.2,'dt_Myr':.00125,'wall_seconds':350,'step_energy_cap':2e-8,'global_energy_cap':3e-6,'material_h_kpc':.125,'sample_Myr':.025}
 run(c,str(out));cases[str(d)]=json.loads(out.read_text());assert abs(cases[str(d)]['initial_mass']-5.364)<1e-10
 if d:assert abs(cases[str(d)]['initial_charge']-cases['0.0']['initial_charge'])<1e-9
common=min(c['completed_time_Myr'] for c in cases.values());ts=np.linspace(5.7,common,21);rows=[]
def val(c,key,t):return float(np.interp(t,[x['time_Myr'] for x in c['trace']],[x[key] for x in c['trace']]))
for t in ts:
 r0=val(cases['0.0'],'boundary_kpc',t);rp=val(cases['0.01'],'boundary_kpc',t);rm=val(cases['-0.01'],'boundary_kpc',t)
 rows.append({'time_Myr':float(t),'unperturbed_R_kpc':r0,'outward_difference_kpc':rp-r0,'inward_difference_kpc':rm-r0,'odd_displacement_kpc':(rp-rm)/2,'even_nonlinear_bias_kpc':(rp+rm)/2-r0})
res={'common_endpoint_Myr':common,'response':rows,'odd_response_ratio_final':rows[-1]['odd_displacement_kpc']/rows[0]['odd_displacement_kpc'],'cases':{k:{j:v for j,v in x.items() if j not in ['trace','rejections']} for k,x in cases.items()},'non_claim':'One finite mass/charge-preserving perturbation family and short response interval; no global, asymptotic or continuum stability. Probe material perturbations are not population seeds in the autonomous baseline.'}
dest.write_text(json.dumps(res,indent=2)+'\n');print({'common_endpoint_Myr':common,'odd_response_ratio_final':res['odd_response_ratio_final']})
