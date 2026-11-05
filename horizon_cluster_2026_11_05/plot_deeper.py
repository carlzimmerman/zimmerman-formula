"""Plot saved results only; no new inference."""
import json,os
from pathlib import Path
B=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR',str(B/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
old=json.loads((B/'deeper002/results.json').read_text());clean=json.loads((B/'clean001/results.json').read_text())
fig,ax=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
labels=['Original catalog\n85 objects','Remove traced limits\n& inferred T: 65','Modern BH masses\nmatched subset: 54']
vals=[old['hotgas']['original85']['held_out_RMSE'],clean['hotgas']['without_upper_limits_or_inferred_T']['held_out_RMSE'],clean['hotgas']['same_sample_modern_BH']['held_out_RMSE']]
x=np.arange(3)
for j,(label,color) in enumerate([('Optical + distance + environment','#7c8996'),('Those controls + gas temperature','#087f8c')]):
 h=[v[j] for v in vals];ax[0].bar(x+(j-.5)*.32,h,.32,color=color,label=label)
 for xx,yy in zip(x+(j-.5)*.32,h):ax[0].text(xx,yy+.008,f'{yy:.3f}',ha='center',fontsize=9)
ax[0].set(xticks=x,xticklabels=labels,ylabel='Held-out BH prediction error (dex)',ylim=(0,.54),title='Temperature association survives source exclusions')
ax[0].legend(fontsize=8,loc='upper right');ax[0].spines[['top','right']].set_visible(False)
a=np.loadtxt(B.parent/'real_research/data/sparc_data/NGC7331_rotmod.dat');r,v,ev,vg,vd,vb=a[:,:6].T
G=6.674e-11;MS=1.98892e30;KPC=3.0857e19;take=r>=r.max()/2
for ud in [.3,.5,.7]:
 for ub in [.5,.7,.9]:
  extra=v*v-vg*np.abs(vg)-ud*vd**2-ub*vb**2
  mass=extra*1e6*r*KPC/G/MS
  ax[1].plot(r[take],mass[take],color='#087f8c',alpha=.4,lw=1)
upper=1.6e8*14.7/12.23
ax[1].axhline(upper,color='#ba4c35',ls='--',label='33° nuclear-disc BH upper limit')
ax[1].plot([],[],color='#087f8c',label='Required central mass: 9 stellar M/L choices')
ax[1].set(yscale='log',xlabel='Radius (kpc)',ylabel='Equivalent central mass (solar masses)',title='NGC 7331: central mass is too small')
ax[1].legend(fontsize=8,loc='center right');ax[1].spines[['top','right']].set_visible(False)
fig.suptitle('Source checks and a radius-matched gravity test',fontsize=15)
fig.savefig(B/'records/HC010_overview.png',dpi=160)
print(B/'records/HC010_overview.png')
