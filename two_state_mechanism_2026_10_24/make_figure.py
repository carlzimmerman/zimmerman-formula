"""Display recorded numerical results; no additional physical fit."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=Path(__file__).resolve().parent
static=json.loads((p/'run_static_v1/results.json').read_text())
refine=json.loads((p/'run_refinement/results.json').read_text())
dwarf=refine['runs'][-1]
t=[s['time']/8*dwarf['physical_duration_gyr'] for s in dwarf['snapshots']]
fig,axes=plt.subplots(1,3,figsize=(14,4.8),layout='constrained')
fig.suptitle('Two-state prototype: retention works conditionally; the tested selector fails',fontsize=14)
axes[0].plot(t,[s['bound_fraction'] for s in dwarf['snapshots']],color='#126782',lw=2.5)
axes[0].set(title='Dwarf toy: bound cold fraction',xlabel='Time after imposed conversion (Gyr)',ylabel='Instantaneous negative-energy fraction',ylim=(.7,1.02))
axes[0].text(.32,.89,'88% at final snapshot',ha='right',fontsize=10,color='#126782')
axes[1].plot(t,[s['acceleration_over_postloss_baryonic_law'] for s in dwarf['snapshots']],color='#126782',lw=2.5)
axes[1].axhline(1,color='gray',ls='--')
axes[1].set(title='Dwarf toy: excess at 0.3 kpc',xlabel='Time after imposed conversion (Gyr)',ylabel='Acceleration / post-loss baryonic law',ylim=(.8,2.2))
qs=[row['phase_epsilon0_theta100']['tethered_fraction'] for row in static['profiles']]
axes[2].bar(['Dwarf','Dwarf\ndisk','Large\ndisk','Cluster'],qs,color=['#126782','#c5543c','#c5543c','#126782'])
axes[2].set(title='Frozen-profile reversible selector',ylabel='Stationary tethered fraction',yscale='log',ylim=(1e-4,1.5))
axes[2].axhline(.95,color='#c5543c',ls='--',label='Illustrative disk target: ≥0.95')
axes[2].legend(loc='lower left',fontsize=8)
for ax in axes:
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y',alpha=.18)
fig.supxlabel('Left and middle: all T→F, 90% baryon loss, fixed softening, N=512.  Right: ε=0, θ=100 (km/s)²; common bath.',fontsize=9)
fig.savefig(p/'summary.png',dpi=160)
fig.savefig(p/'summary.pdf')
print(p/'summary.png')
