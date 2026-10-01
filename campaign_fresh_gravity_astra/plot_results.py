"""Render the pinned empirical diagnostic and the conditional spectral test."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
gal=list(csv.DictReader((HERE/'run_002/sparc_accelerations.csv').open()))
cl=list(csv.DictReader((HERE/'run_002/cluster_inverse_budget.csv').open()))
cl=[r for r in cl if r['kernel']=='R' and r['footing']=='canonical' and r['scaling']=='vacuum' and r['radius_kpc']=='300.0']
fig,axes=plt.subplots(1,2,figsize=(12,5.1),layout='constrained')
ax=axes[0]
ax.scatter([float(r['B']) for r in gal],[float(r['obs']) for r in gal],s=3,alpha=.14,c='#40566b',label='SPARC: 153 galaxies, 3166 points')
ax.scatter([float(r['B']) for r in cl],[float(r['obs']) for r in cl],s=45,marker='D',c='#c34732',label='7 X-COP clusters at 300 kpc')
b=np.logspace(-13,-8,500)
for a,label,color in [(9.3619e-11,'RAR: canonical scale','#007d83'),(1.1279e-10,'RAR: alternative scale','#697d2d')]:
    ax.plot(b,b/(-np.expm1(-np.sqrt(b/a))),color=color,lw=1.6,label=label)
ax.plot(b,b,ls=':',color='.5',lw=1)
ax.set(xscale='log',yscale='log',xlim=(1e-13,1e-8),ylim=(1e-13,1e-8),
       xlabel='Baryonic acceleration B [m/s²]',ylabel='Inferred radial acceleration [m/s²]',title='MOND included before assessing the residual')
ax.legend(fontsize=7.5,loc='upper left'); ax.grid(alpha=.12)
ax.text(.03,.03,'Fixed stellar M/L; central hydrostatic profiles.\nDifferent tracers and systematics; not a joint likelihood.',transform=ax.transAxes,fontsize=8)

ax=axes[1]; q=np.logspace(-4,0,400); E=np.sqrt(.315*4**3+.685)
ax.plot(q,(q+E)/(q+1),label='Q: distribution-independent lower bound',color='#007d83',lw=2)
ax.plot(q,np.maximum(1,E*(-np.expm1(-np.sqrt(q)))**2/q),label='RAR: distribution-independent lower bound',color='#bc5b31',lw=2)
rows=json.loads((HERE/'run_transition_001/results.json').read_text())['rows']
for kernel,color,marker in [('Q','#007d83','o'),('R','#bc5b31','s')]:
    sel=[r for r in rows if r['z']==3 and r['kernel']==kernel]
    ax.scatter([r['mean_B_over_a0_today'] for r in sel],[r['intrinsic_line_m4_over_m2_squared'] for r in sel],
               color=color,marker=marker,label=kernel+': exact lognormal examples',s=30)
ax.set(xscale='log',yscale='log',xlabel='Mean B / a₀(today)',ylabel='Intrinsic raw line-moment ratio U₄ / U₂²',
       title='Spectral price of hiding H(z) scaling at z = 3',ylim=(1,6000))
ax.legend(fontsize=7.5,loc='upper left'); ax.grid(alpha=.12)
ax.text(.03,.035,'Conditional: common radius / projection / weights.\nKnown Gaussian broadening; no real spectra fitted.',transform=ax.transAxes,fontsize=8)
fig.savefig(HERE/'campaign_results.png',dpi=170)
print(HERE/'campaign_results.png')
