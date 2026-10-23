import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
p=Path(__file__).parent
ref=json.load(open(p/'cold_limit_run/results.json'))
continuum=ref['rows'][-1];cold=ref['cold_refined']['profile']
profiles={};metrics={};checks={};curves={}
for ng in [256,512,1024]:
 eq=json.load(open(p/f'cold_discrete_{ng}_10000_fine.json'));rg=np.array(eq['rg']);z=np.array(eq['z'])
 r=np.linspace(0,rg[-1],160001);psi=np.maximum(np.interp(r,rg,z)+1/np.sqrt(1+r*r),0);rho=10000*psi**2.5/(1+r*r)
 m=cumulative_trapezoid(r*r*rho,r,initial=0)
 profiles[str(ng)]=[]
 for warm,cr in zip(continuum['common_profile'],cold):
  rr=warm['r'];gn=rr/(1+rr*rr)**1.5;q=float(np.interp(rr,r,m)/rr**2)
  profiles[str(ng)].append(dict(r=rr,q=q,g_ratio_continuum=(gn+q)/(gn+warm['q']),g_ratio_cold_stiff=(gn+q)/(gn+cr['q'])))
 checks[f'equilibrium_{ng}']=eq['residual']<1e-10 and abs(eq['mass']-1)<1e-10
 if ng==1024:continue
 old=json.load(open(p/f'cold_discrete_{ng}_10000.json'));checks[f'quadrature_{ng}']=max(abs(np.array(old['z'])-z))<1e-8
 pair={s:json.load(open(p/f'cold_{s}_{ng}.json')) for s in ['control','kick']}
 checks[f'complete_{ng}']=all(d.get('failure') is None and d['rows'][-1]['t']==40 for d in pair.values())
 checks[f'conservation_{ng}']=all(d['max_energy_drift']<1e-4 and d['max_L_error']<1e-10 for d in pair.values())
 checks[f'force_{ng}']=all(max(d['force_relative_errors'])<1e-4 for d in pair.values())
 c,k=pair['control'],pair['kick'];t=np.array([x['t'] for x in c['rows']]);cc=np.array([x['rms_radius'] for x in c['rows']]);kk=np.array([x['rms_radius'] for x in k['rows']]);delta=kk-cc;de=k['rows'][0]['energy']-c['rows'][0]['energy']
 checks[f'equal_energy_{ng}']=abs(de-.0008)<1e-10
 windows={}
 for lo,hi in [(0,10),(30,40)]:
  a=delta[(t>=lo)&(t<=hi)];windows[f'{lo}-{hi}']=dict(mean=float(np.mean(a)),std=float(np.std(a)),rms=float(np.sqrt(np.mean(a*a))))
 metrics[str(ng)]=dict(windows=windows,control_drift=float(max(abs(cc-cc[0]))),injected_energy=de,dilation=k['dilation'],energy_error_over_injection={s:max(abs(x['energy']-d['rows'][0]['energy']) for x in d['rows'])/de for s,d in pair.items()},max_q={s:max(x['max_q'] for x in d['rows']) for s,d in pair.items()})
 curves[ng]=(t,cc,kk)
t,c,k=curves[256];tf,cf,kf=curves[512];dd=k-c-np.interp(t,tf,kf-cf);metrics['comparison']=dict(rms=float(np.sqrt(np.mean(dd*dd))),max_abs=float(max(abs(dd))))
checks={k:bool(v) for k,v in checks.items()}
out=dict(checks=checks,all_pass=all(checks.values()),metrics=metrics,profiles=profiles,scope='Cold A10000 equilibrium and finite-time spherical response; not formation or nonlinear 3D stability')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(2,1,figsize=(8,6),sharex=True,layout='constrained')
for ng,(t,c,k) in curves.items():
 ax[0].plot(t,c,ls='--',label=f'{ng}: control');ax[0].plot(t,k,label=f'{ng}: perturbed');ax[1].plot(t,k-c,label=f'{ng}: perturbed minus control')
ax[0].set_ylabel('RMS radius');ax[0].legend(fontsize=8,ncol=2);ax[1].set_ylabel('Radius difference');ax[1].set_xlabel('Dimensionless time');ax[1].legend(fontsize=8);ax[1].axhline(0,color='gray',lw=.5);fig.suptitle('Cold A=10000 branch: equal injected energy')
fig.savefig(p/'cold_discrete_response.png',dpi=160)
sys.exit(0 if out['all_pass'] else 1)
