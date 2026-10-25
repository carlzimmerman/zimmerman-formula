"""Saved-data scientific figure; no new fit."""
import pathlib,json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];rows=json.loads((P/'diagnostic_history.json').read_text())['results'];hist={r['tag']:r for r in rows};models={m['name']:m for m in json.loads((ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json').read_text())['models']}
fig,axs=plt.subplots(2,2,figsize=(10,7.6));colors={'bound':'#566f9c','marginal':'#c28737','escape':'#237c70'}
for col,name in enumerate(['Draco','Sextans']):
 tags=[('bound','draco_L12_long' if name=='Draco' else 'sextans_L24_long'),('marginal','draco_marginal' if name=='Draco' else 'sextans_marginal'),('escape','draco_escape_long' if name=='Draco' else 'sextans_escape_long')]
 ax=axs[0,col]
 for kind,tag in tags:
  r=hist[tag];h=r['history'];x=[v['T_Myr'] for v in h];key='sigma_equilibrium_kms' if name=='Draco' else 'twice_NLL_above_reference';ax.plot(x,[v[key] for v in h],color=colors[kind],lw=1.8,label=kind)
 if name=='Draco':
  ax.axhspan(9.29,9.8,color='black',alpha=.13,label='observed interval');ax.axhline(9.55,color='black',lw=.7);ax.set_ylabel('Instantaneous equilibrium σ (km/s)');ax.set_ylim(3,40)
 else:
  ax.axhline(0,color='black',lw=.8);ax.set_ylabel('Survey 2ΔNLL above reference');ax.set_ylim(bottom=0)
 ax.set_title(name+' — fixed-origin diagnostics');ax.set_xlabel('Time (Myr)');ax.legend(fontsize=8,loc='best');ax.grid(alpha=.2)
 ax=axs[1,col];m=models[name];rr=np.geomspace(30 if name=='Draco' else 100,6000 if name=='Draco' else 14000,240)
 target=m['cold_mass']*rr**3/(rr*rr+m['cold_scale_pc']**2)**1.5;ax.loglog(rr,target/1e6,'k--',label='CCT-008 target',lw=1.5)
 for kind,tag in tags:
  q=json.loads((P/'runs'/f'{tag}.json').read_text());r=np.array(q['radial_grid']);edges=np.r_[0,(r+np.r_[r[1:],q['parameters']['rmax']])/2];u=q['physical'];h=q['history'][-1];cdf=np.array(h['cdf']);got=u['Munit_Msun']*np.interp(rr/u['Runit_pc'],edges,np.r_[0,cdf],left=0,right=cdf[-1]);ax.loglog(rr,got/1e6,color=colors[kind],label=kind+' final')
  if kind=='escape':
   tail=[v['cdf'] for v in q['history'] if v['t']>=.75*h['t']];avg=np.mean(tail,axis=0);got=u['Munit_Msun']*np.interp(rr/u['Runit_pc'],edges,np.r_[0,avg],left=0,right=avg[-1]);ax.loglog(rr,got/1e6,color=colors[kind],ls=':',lw=2,label='escape late mean')
 ax.set_xlabel('Radius (pc)');ax.set_ylabel('Enclosed cold mass (million M☉)');ax.set_title(name+' — original-origin profiles');ax.grid(alpha=.2,which='both');ax.legend(fontsize=8,loc='best')
fig.suptitle('Coherent mode transfer does not yet select a stable four-dwarf envelope',fontsize=13)
fig.text(.5,.01,'Conditional CCT wave model, η = 1500 pc km/s. Monopole diagnostics; stars were not evolved.\nLate means are posthoc. Draco develops off-centre wells; see centering.json.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.055,1,.96]);fig.savefig(P/'formation_diagnostics.png',dpi=160)
