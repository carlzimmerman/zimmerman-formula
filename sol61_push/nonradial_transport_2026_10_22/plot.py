from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=Path(__file__).resolve().parent;s=json.loads((p/'sheet_run/result.json').read_text());d=json.loads((p/'transport_run/result.json').read_text())
fig,axs=plt.subplots(1,3,figsize=(13,3.9),layout='constrained')
k=np.geomspace(.02,20,500)
def T(a):return (2+a)/(2*(1+a)**2)
for H in [0,1,3]:
 q=np.sqrt(1+k*k);axs[0].semilogx(k,k*T(k*H)-k*k/q*T(q*H),label=f'H/ell0 = {H}')
axs[0].set(xlabel='k ell0',ylabel='Sheet response F',title='A preferred length');axs[0].legend(fontsize=8)
for h in [0,1,3]:
 row=next(x for x in s['thickness'] if x['H']==h);x=np.array([.25,.5,1,2,4]);axs[1].loglog(x,x*row['patch_mass_over_canonical_at_sigma_star'],marker='o',label=f'H/ell0 = {h}')
axs[1].set(xlabel='Surface density / reference density',ylabel='Footprint mass / canonical mass',title='Mass still depends on supply');axs[1].legend(fontsize=8)
for idx,label in [(0,'N96'),(3,'N192'),(4,'N96, half softening')]:
 c=d['cases'][idx];axs[2].plot([r['time']*.0120742729 for r in c['rows']],[r['inner_L_fraction'] for r in c['rows']],label=label)
axs[2].set(xlabel='Time (Gyr)',ylabel='Share of total angular momentum',title='Initially inner-quarter labels');axs[2].legend(fontsize=8)
fig.suptitle('Reduced-model tests: length selection and transport, no selected core mass',fontsize=13)
fig.savefig(p/'summary.png',dpi=180)
