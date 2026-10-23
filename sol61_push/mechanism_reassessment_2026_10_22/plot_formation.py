"""Render already recorded results; no new dynamics or fitted parameters."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
production=json.loads((p/'physical_spectrum_wkb2_v2_run/results.json').read_text())['rows'][-1]
collapse=[json.loads((p/'collapse_core_run/results.json').read_text())['rows'][-1]]
collapse += json.loads((p/'collapse_core_compiled_run/results.json').read_text())['rows']
collapse += json.loads((p/'collapse_core_512_stream_run/results.json').read_text())['rows']
fig,ax=plt.subplots(1,2,figsize=(12,4.6),constrained_layout=True)
for s,label in zip(production['species'],['Daughter Φ','Parent X']):
    k=np.array(s['k']);n=np.array(s['occupation'])
    ax[0].loglog(k,k**3*n/np.pi**2,label=label,lw=2)
ax[0].set(xlabel='Comoving momentum k / m',ylabel='Comoving number per ln k / m³',
          title='Conditional vacuum production: H_inf = m',ylim=(1e-12,.02))
ax[0].text(.04,.06,'MeV benchmark: ≈10⁻²⁹ of target abundance',transform=ax[0].transAxes,fontsize=9)
ax[0].legend();ax[0].grid(alpha=.2,which='both')
for r in collapse:
    ax[1].plot([s['t'] for s in r['samples']],[s['mass_inside_3'] for s in r['samples']],label=f"{r['N']} shells",lw=1.7)
ax[1].set(xlabel='Dimensionless time',ylabel='Cold mass inside r = 3',
          title='Coarse inner mass: resolution comparison',ylim=(0,1))
ax[1].legend();ax[1].grid(alpha=.2)
fig.savefig(p/'formation_spectrum_and_core.png',dpi=180)
