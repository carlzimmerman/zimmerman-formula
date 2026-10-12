import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=Path(__file__).parent;x=json.loads((p/'halo_formation_probe_v2_run/results.json').read_text())
r=np.array(x['score_radii']);M=x['cell']['Mcat'];fig,ax=plt.subplots(1,2,figsize=(11,4.3))
ax[0].plot(r,np.array(x['target_enclosed_mass'])/M,'k--',lw=2,label='Repo target')
labels={'refined':'Extended cloud','smaller_cells':'Extended, smaller cells','compact_refined':'Denser cloud','collisionless':'Extended, no scattering'}
for row in x['rows']:
 if row['name'] not in labels:continue
 s=row['snapshots'][-1];label=labels[row['name']]
 ax[0].plot(r,np.array(s['cumulative_mass'])/M,label=label)
 ax[1].plot([z['elapsed_Gyr'] for z in row['snapshots']],[z['mass_within_target_radius']/M for z in row['snapshots']],'.-',label=label)
ax[0].set(xscale='log',xlabel='Radius / target radius',ylabel='Enclosed mass / total supplied cold mass',title='Final profiles: 24.35 Gyr of isolated evolution')
ax[1].axhline(1,color='k',ls='--');ax[1].set(xlabel='Elapsed model time (Gyr)',ylabel='Mass inside target radius / supplied mass',title='No target force or temperature imposed')
for a in ax:a.grid(alpha=.2)
ax[0].legend(fontsize=8);fig.suptitle('Exploratory MW canonical test — spherical gravity; not a cosmological simulation',fontsize=11)
fig.tight_layout();fig.savefig(p/'halo_formation.png',dpi=180)
