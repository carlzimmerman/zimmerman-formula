"""Display saved data; dashed segments are outside the validated interval."""
import os,tempfile,json
os.environ['MPLCONFIGDIR']=tempfile.mkdtemp(prefix='cap-plot-')
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=Path(__file__).parent
fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
for name,label,color in [('cap65','65 nodes','#4778a8'),('cap129','129 nodes','#c47d24'),('cap257bracket','257 nodes','#34845d')]:
 r=json.loads((p/'evidence'/name/'results.json').read_text());d=r['diagnostics'];t=np.array([x['t'] for x in d])
 for ax,key in zip(axes.ravel(),['max_polarization_ratio','min_N','cap_gap','M_res']):
  y=np.array([x[key] for x in d]);a=t<=.78;b=t>=.78
  ax.plot(t[a],y[a],color=color,label=label,lw=1.7);ax.plot(t[b],y[b],color=color,ls='--',lw=1.4)
for ax,title in zip(axes.ravel(),['Polarization fraction (nodal maximum)','Minimum lapse','Expansion-cap gap','Discrete momentum residual']):
 ax.set_title(title);ax.set_xlim(.5,.85);ax.axvspan(.78,.85,color='gray',alpha=.12);ax.axvline(.78,color='gray',ls=':',lw=1);ax.set_xlabel('Clock coordinate time');ax.grid(alpha=.2)
axes[0,0].axhline(1,color='black',lw=.7);axes[0,0].set_ylim(.4,1.02);axes[0,1].set_ylim(0,1.05);axes[1,0].set_ylim(0,.3);axes[1,1].set_yscale('log');axes[1,1].set_ylim(1e-12,.01);axes[0,0].legend(loc='lower right',fontsize=9)
fig.suptitle('Coupled cap collapse: steepening is resolved; the late endpoint is not\nSolid: audited through t=0.78. Dashed/shaded: no continuum-validity claim.',fontsize=12)
fig.savefig(p/'collapse_audit.png',dpi=160)
