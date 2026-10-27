import json,argparse
from pathlib import Path
import numpy as np
from isolated import Isolated
p=Path(__file__).resolve().parent;pa=argparse.ArgumentParser();pa.add_argument('--output');args=pa.parse_args();checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=v))
base=json.loads((p/'affine_refine_run/result.json').read_text())['cases'][0];repeat=json.loads((p/'affine_convergence_run/result.json').read_text())['cases'];a=np.array([r['axes'] for r in base['rows'] if r['t']<=12.00001]);t=np.array([r['axes'] for r in repeat[0]['rows'][::2]]);g=np.array([r['axes'] for r in repeat[1]['rows']]);dt=float(np.max(abs(a-t)));dg=float(np.max(abs(a-g)))
ck('bounce_timestep_axes',dt<.001,dt);ck('bounce_grid_axes',dg<.01,dg)
for c in [base]+repeat:
 mins=np.min([r['axes'] for r in c['rows']],axis=0);last=np.array(c['rows'][-1]['axes']);ck('three_axis_rebound_%s_%s'%(c['n'],c['dt']),c['stop_reason']=='time_limit' and bool(np.all(last>mins+.05)),dict(minimum=mins.tolist(),final=last.tolist(),energy_error=c['max_energy_error']))
f=Isolated(48,6);w=json.loads((p/'wells_run/result.json').read_text());curv=[]
for r in [r for r in w['rows'] if r['n']==48]:
 R=r['Rmin'];M=r['mass'];ep=.01;minus=f.evaluate(M,[R*np.exp(-ep)]*3);plus=f.evaluate(M,[R*np.exp(ep)]*3);value=(plus['energy']+minus['energy']-2*r['energy'])/ep**2;curv.append(dict(b=r['b'],curvature=value));ck('positive_gaussian_radius_curvature_'+str(r['b']),value>0,value)
Path(args.output).write_text(json.dumps(dict(checks=checks,curvature=curv),indent=2)+'\n')
