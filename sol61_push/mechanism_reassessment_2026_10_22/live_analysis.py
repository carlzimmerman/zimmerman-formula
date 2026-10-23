import json,sys
from pathlib import Path
import numpy as np
base=Path(__file__).parent
names=['control','kick','time_refined','space_refined','space_control']
runs={n:json.load(open(base/('live_'+n+'.json'))) for n in names}
def series(n,key):
 d=runs[n]['rows'];return np.array([r['t'] for r in d]),np.array([r[key] for r in d])
metrics={}
for label,con,kick in [('coarse','control','kick'),('refined','space_control','space_refined')]:
 t,c=series(con,'rms_radius');tt,k=series(kick,'rms_radius');d=k-np.interp(tt,t,c)
 metrics[label]=dict(initial_difference=float(d[0]),early_rms=float(np.sqrt(np.mean(d[tt<=10]**2))),late_rms=float(np.sqrt(np.mean(d[tt>=30]**2))),late_to_early=float(np.sqrt(np.mean(d[tt>=30]**2)/np.mean(d[tt<=10]**2))),control_max_drift=float(np.max(np.abs(c-c[0]))))
t,c=series('control','rms_radius');_,k=series('kick','rms_radius');tf,cf=series('space_control','rms_radius');_,kf=series('space_refined','rms_radius')
d=k-c;df=np.interp(t,tf,kf-cf)
tt,kt=series('time_refined','rms_radius')
metrics['comparison']=dict(max_response_curve_difference=float(max(abs(d-df))),rms_response_curve_difference=float(np.sqrt(np.mean((d-df)**2))),max_timestep_curve_difference=float(max(abs(k-np.interp(t,tt,kt)))))
checks=dict(force_derivative=all(max(x['force_relative_errors'])<1e-4 for x in runs.values()),energy=all(x['max_energy_drift']<1e-4 for x in runs.values()),angular_momentum=all(x['max_L_error']<1e-10 for x in runs.values()),completed=all(x['rows'][-1]['t']==40 for x in runs.values()),cap_and_grid=all(max(r['max_q'] for r in x['rows'])<.98 and max(r['max_radius'] for r in x['rows'])<10 for x in runs.values()))
out=dict(checks=checks,all_pass=all(checks.values()),metrics=metrics,runs={n:{k:v for k,v in x.items() if k!='rows'} for n,x in runs.items()},scope='audits existing live-run artifacts; exploratory damping indicators, no physical discovery gate')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2))
print(json.dumps(dict(checks=checks,metrics=metrics),indent=2))
# Scientific plot of the same recorded data, no resimulation.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(3,1,figsize=(8,8),sharex=True,layout='constrained')
for n,col,style in [('control','gray','--'),('kick','tab:blue','-'),('space_control','black','--'),('space_refined','tab:orange','-')]:
 tx,y=series(n,'rms_radius');ax[0].plot(tx,y,color=col,ls=style,lw=1,label=n.replace('_',' '))
ax[0].set_ylabel('RMS radius');ax[0].legend(fontsize=8,ncol=2)
ax[1].plot(t,d,label='Coarse: perturbed minus control');ax[1].plot(tf,kf-cf,label='Refined: perturbed minus control');ax[1].axhline(0,c='gray',lw=.5);ax[1].set_ylabel('Radius difference');ax[1].legend(fontsize=8)
for n in ['kick','time_refined','space_refined']:
 tx,y=series(n,'relative_energy_drift');ax[2].plot(tx,y*1e6,label=n.replace('_',' '),lw=.8)
ax[2].set_ylabel('Energy drift (ppm)');ax[2].set_xlabel('Dimensionless time');ax[2].legend(fontsize=8)
fig.suptitle('Live spherical response: conserved energy, declining bulk oscillation\nExploratory near-equilibrium test; not a formation or selector result',fontsize=11)
fig.savefig(base/'live_relaxation.png',dpi=160)
sys.exit(0 if out['all_pass'] else 1)
