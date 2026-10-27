import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;r=json.loads((p/'run/result.json').read_text());fr=json.loads((p/'formation_run/result.json').read_text());d=np.load('campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_percluster.npz');W=np.where(np.isfinite(d['E'])&(d['E']>0),1/d['E']**2,0);R=np.sqrt(np.geomspace(.15,3,9)[:-1]*np.geomspace(.15,3,9)[1:]);stack=lambda x:np.sum(W*x,axis=0)/W.sum(axis=0)
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(11,4.6),layout='constrained')
ax[0].loglog(R,stack(np.nan_to_num(d['D'])),'o-',color='black',label='Cached cluster stack')
for i,col,label in [(0,'#197c80','Baryons + core population'),(2,'#c45434','Full law + extra population')]:
 row=r['clusters'][i];extra=row['mass_median']*R**2/(np.pi*(R**2+row['b_median_Mpc']**2)**2)/1e12;ax[0].loglog(R,stack(d[row['baseline']])+extra,'o-',color=col,label=label)
ax[0].axvspan(.15*20**(3/8),.15*20**(6/8),alpha=.1,color='grey');ax[0].set(xlabel='Projected radius [Mpc]',ylabel='DeltaSigma [solar masses / pc²]',title='Extended population: MID fitted, rest held out');ax[0].legend(fontsize=8)
for k,col in [(.1,'#197c80'),(1,'#c45434')]:
 for beta,style in [(1,'-'),(.997,'--')]:
  rr=[v for v in fr['rows'] if v['k']==k and v['beta']==beta and v['matching']=='velocity'];ax[1].plot([v['z_form'] for v in rr],[v['amplitude'] for v in rr],'o'+style,color=col,label=f'k={k}/Mpc, beta={beta}')
ax[1].axhline(1,color='grey',lw=1);ax[1].axvspan(27.497,105,color='grey',alpha=.1);ax[1].set(xlabel='Assumed conversion redshift',ylabel='Final amplitude / reference dust',title='Late conversion retains earlier growth losses',ylim=(.94,1.005),xlim=(5,105));ax[1].legend(fontsize=8,loc='lower left');ax[1].text(.43,.60,'Shading: >1% core filling',transform=ax[1].transAxes,fontsize=8)
fig.suptitle('Conditional population tests — abundance, formation and distribution remain inputs',fontsize=12)
fig.savefig(p/'population_tests.png',dpi=180);fig.savefig(p/'population_tests.pdf')
