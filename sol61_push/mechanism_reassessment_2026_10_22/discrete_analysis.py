import json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent
runs={}
metrics={}
curves={}
for ng in [256,512]:
 eq=json.load(open(p/f'discrete_eq_{ng}.json'));fine=json.load(open(p/f'discrete_eq_{ng}_fine.json'))
 control=json.load(open(p/f'discrete_control_{ng}.json'));kick=json.load(open(p/f'discrete_kick_{ng}.json'))
 t=np.array([r['t'] for r in control['rows']]);c=np.array([r['rms_radius'] for r in control['rows']]);k=np.array([r['rms_radius'] for r in kick['rows']]);delta=k-c
 old=json.load(open(p/('live_control.json' if ng==256 else 'live_space_control.json')));oldr=np.array([r['rms_radius'] for r in old['rows']])
 dE=kick['rows'][0]['energy']-control['rows'][0]['energy']
 metrics[str(ng)]=dict(equilibrium_residual=eq['residual'],mass_error=abs(eq['mass']-1),quadrature_z_change=float(max(abs(np.array(eq['z'])-fine['z']))),control_drift=float(max(abs(c-c[0]))),old_control_drift=float(max(abs(oldr-oldr[0]))),injected_energy=dE,dilation=kick['dilation'],early_rms=float(np.sqrt(np.mean(delta[t<=10]**2))),late_rms=float(np.sqrt(np.mean(delta[t>=30]**2))),late_early_ratio=float(np.sqrt(np.mean(delta[t>=30]**2)/np.mean(delta[t<=10]**2))),energy_drift_over_injection=max(abs(r['energy']-kick['rows'][0]['energy']) for r in kick['rows'])/dE)
 runs[str(ng)]=dict(control={k:v for k,v in control.items() if k!='rows'},kick={k:v for k,v in kick.items() if k!='rows'})
 curves[ng]=(t,c,k)
t,c,k=curves[256];tf,cf,kf=curves[512];diff=(k-c)-np.interp(t,tf,kf-cf)
metrics['comparison']=dict(max_curve_difference=float(max(abs(diff))),rms_curve_difference=float(np.sqrt(np.mean(diff*diff))))
allruns=[v for pair in runs.values() for v in pair.values()]
checks=dict(equilibrium=all(metrics[str(g)]['equilibrium_residual']<1e-10 and metrics[str(g)]['mass_error']<1e-10 for g in [256,512]),quadrature=all(metrics[str(g)]['quadrature_z_change']<1e-9 for g in [256,512]),equal_energy=all(abs(metrics[str(g)]['injected_energy']-.0008)<1e-10 for g in [256,512]),force=all(max(r['force_relative_errors'])<1e-4 for r in allruns),energy=all(r['max_energy_drift']<1e-4 for r in allruns),angular_momentum=all(r['max_L_error']<1e-10 for r in allruns))
out=dict(checks=checks,all_pass=all(checks.values()),metrics=metrics,runs=runs,scope='audit of direct live runs and exact CIC mean-field initialization; no damping-rate fit')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(dict(checks=checks,metrics=metrics),indent=2))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(2,1,figsize=(8,6),sharex=True,layout='constrained')
for ng,(tt,cc,kk) in curves.items():
 ax[0].plot(tt,cc,label=f'{ng} nodes: control',ls='--');ax[0].plot(tt,kk,label=f'{ng} nodes: perturbed')
 ax[1].plot(tt,kk-cc,label=f'{ng} nodes: perturbed minus control')
ax[0].set_ylabel('RMS radius');ax[0].legend(fontsize=8)
ax[1].set_ylabel('Radius difference');ax[1].set_xlabel('Dimensionless time');ax[1].axhline(0,color='gray',lw=.5);ax[1].legend(fontsize=8)
fig.suptitle('Matched-energy response from discrete equilibria\nFinite-time spherical test, not primordial formation',fontsize=11)
fig.savefig(p/'discrete_response.png',dpi=160)
sys.exit(0 if out['all_pass'] else 1)
