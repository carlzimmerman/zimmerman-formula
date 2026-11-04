"""Show the physical force and virial failures of the fixed KT39 witness."""
import json,os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/kt34_matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
force=json.loads((HERE/'mw/force_001/results.json').read_text())
efe=[]
for name in ['run_001','low_001']:
    efe+=json.loads((HERE/'efe'/name/'results.json').read_text())['cases']['fine']
fig,axs=plt.subplots(1,2,figsize=(12,4.8))
ax=axs[0]
c=next(c for c in force['cases'] if c['footing']=='canonical' and c['refine']==6)
p=next(p for p in c['profiles'] if p['R_kpc']==12)
z=np.array(p['z_kpc']);colors={'Newton':'#75828f','A':'#b8860b','B':'#bc4858','total':'#087e8b'}
for name in ['Newton','A','B','total']:
    ax.plot(z,p['force'][name],label=name if name!='total' else 'Full response',color=colors[name],lw=2 if name=='total' else 1.4)
full=np.array(p['force']['total'])
ax.fill_between(z,full,0,where=full<0,color='#bc4858',alpha=.16)
ax.axhline(0,color='#333333',lw=.8)
ax.scatter([.3],[-843.7699442474329],color='#087e8b',zorder=4)
ax.set(xlabel='Height above plane z [kpc]',ylabel='Potential gradient ∂Φ/∂z [(km/s)²/kpc]',title='Canonical MW fit at R = 12 kpc')
ax.text(.98,.05,'Below zero: acceleration points away from the plane',transform=ax.transAxes,ha='right',fontsize=8.2,color='#88313e')
ax.legend(frameon=False,fontsize=8)
ax=axs[1]
for foot,color,label in [('canonical','#087e8b','Canonical a₀'),('alt','#b25128','Alternate a₀')]:
    rows=sorted((r for r in efe if r['name']=='Draco' and r['footing']==foot),key=lambda r:r['eta'])
    ax.plot([r['eta'] for r in rows],[r['variance'][-1] for r in rows],marker='o',ms=4,color=color,label=label,lw=1.7)
ax.axhline(0,color='#333333',lw=.8)
ax.set_xscale('symlog',linthresh=.001)
ax.set_xticks([0,.001,.01,.1,1,3],['0','.001','.01','.1','1','3'])
ax.set_xlim(0,3)
ax.set(xlabel='Auxiliary external field η = e/a₀',ylabel='Binding virial W/(3M) [(km/s)²]',title='Fixed Draco Plummer profile, Υ = 3')
ax.axhspan(ax.get_ylim()[0],0,color='#bc4858',alpha=.08)
ax.text(.03,.05,'Negative W cannot balance positive kinetic energy',transform=ax.transAxes,fontsize=8.2,color='#88313e')
ax.legend(frameon=False,fontsize=8)
for ax in axs:
    ax.spines[['top','right']].set_visible(False);ax.grid(alpha=.16)
fig.suptitle('The p = 9/8, ℓ = 3 kpc response: curvature stress can overwhelm attraction',fontsize=13)
fig.text(.5,.02,'Fixed baryons and law. MW: refinement 6. Dwarf: imposed uniform fields; no actual satellite orbit or Galactic tides assumed.',ha='center',fontsize=8.5)
fig.tight_layout(rect=(0,.055,1,.94))
fig.savefig(HERE/'mechanism_failures.png',dpi=180)
fig.savefig(HERE/'mechanism_failures.pdf')
