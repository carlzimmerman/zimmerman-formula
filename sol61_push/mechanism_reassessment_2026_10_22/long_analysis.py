import json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent
metrics={};curves={};checks={}
for ng in [256,512]:
 pair={}
 for s in ['control','kick']:
  data=json.loads((p/f'long_{s}_{ng}.json').read_text())
  if 'rows' not in data:data=json.loads((p/f'long_{s}_{ng}_partial.json').read_text())
  pair[s]=data
 for s,data in pair.items():
  old=json.loads((p/f'discrete_{s}_{ng}.json').read_text())
  prefix_error=max(abs(row[key]-prior[key]) for row,prior in zip(data['rows'],old['rows']) for key in prior)
  checks[f'prefix_{s}_{ng}']=prefix_error<1e-10
  data['prefix_max_absolute_error']=prefix_error
  checks[f'conservation_{s}_{ng}']=data['max_energy_drift']<1e-4 and data['max_L_error']<1e-10
 c,k=pair['control'],pair['kick']
 common=min(len(c['rows']),len(k['rows']))
 c=dict(c,rows=c['rows'][:common]);k=dict(k,rows=k['rows'][:common])
 t=np.array([r['t'] for r in c['rows']]);cr=np.array([r['rms_radius'] for r in c['rows']]);kr=np.array([r['rms_radius'] for r in k['rows']]);d=kr-cr
 de=k['rows'][0]['energy']-c['rows'][0]['energy'];checks[f'energy_match_{ng}']=abs(de-.0008)<1e-10
 windows={}
 for lo,hi in [(0,10),(30,40),(70,80),(110,120)]:
  x=d[(t>=lo)&(t<=hi)]
  if t[-1]<hi:windows[f'{lo}-{hi}']=None;continue
  windows[f'{lo}-{hi}']=dict(rms=float(np.sqrt(np.mean(x*x))),mean=float(np.mean(x)),std=float(np.std(x)),max_abs=float(max(abs(x))))
 metrics[str(ng)]=dict(windows=windows,common_end=float(t[-1]),failures={s:data.get('failure') for s,data in pair.items()},prefix_errors={s:data['prefix_max_absolute_error'] for s,data in pair.items()},control_drift=float(max(abs(cr-cr[0]))),injected_energy=de,energy_error_over_injection={s:max(abs(r['energy']-data['rows'][0]['energy']) for r in data['rows'])/de for s,data in pair.items()},max_energy_drift={s:data['max_energy_drift'] for s,data in pair.items()},max_L_error={s:data['max_L_error'] for s,data in pair.items()},max_q={s:max(r['max_q'] for r in data['rows']) for s,data in pair.items()})
 curves[ng]=(t,cr,kr)
t,c,k=curves[256];tf,cf,kf=curves[512];mask=t<=tf[-1];diff=(k-c)[mask]-np.interp(t[mask],tf,kf-cf)
metrics['comparison']=dict(rms=float(np.sqrt(np.mean(diff**2))),max_abs=float(max(abs(diff))))
out=dict(checks=checks,all_pass=all(checks.values()),metrics=metrics,scope='Conservation and prefix checks do not certify completion: inspect common_end and failures. Longer direct-run audit; warm spherical equilibrium only; no asymptotic damping or formation claim')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(2,1,figsize=(9,6),sharex=True,layout='constrained')
for ng,(t,c,k) in curves.items():
 ax[0].plot(t,c,ls='--',label=f'{ng}: control');ax[0].plot(t,k,label=f'{ng}: perturbed')
 ax[1].plot(t,k-c,label=f'{ng}: perturbed minus control')
ax[0].set_ylabel('RMS radius');ax[0].legend(ncol=2,fontsize=8)
ax[1].set_ylabel('Radius difference');ax[1].set_xlabel('Dimensionless time');ax[1].legend(fontsize=8);ax[1].axhline(0,color='gray',lw=.5)
fig.suptitle('Longer matched-energy response: warm spherical medium')
fig.savefig(p/'long_response.png',dpi=150)
sys.exit(0 if out['all_pass'] else 1)
