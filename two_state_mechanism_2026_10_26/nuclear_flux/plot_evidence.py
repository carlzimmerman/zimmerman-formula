from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
b=Path(__file__).resolve().parent;d=json.loads((b/'run_audit_v2/results.json').read_text())
fig,ax=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
ax[0].plot([0,1,2],[r['first_dipole_allowed_energy'] for r in d['atomic']],'o-',color='#236d91',label='Computed first p level')
ax[0].axhline(-.125,ls='--',color='#555555',label='Exact Coulomb2p')
ax[0].set_xticks([0,1,2],['Original basis','Diffuse2','Diffuse3']);ax[0].set_ylabel('Atomic energy (atomic units)');ax[0].set_title('A previously missing product channel');ax[0].legend(fontsize=9)
for basis,label in [('rydberg2','130 electronic states'),('rydberg3','192 electronic states'),('rydberg4','266 electronic states')]:
 rows=sorted([r for r in d['nuclear'] if r['basis']==basis and r['end']==30],key=lambda r:r['h'])
 ax[1].plot([r['h'] for r in rows],[r['ground_dominated_mode_to_other_modes_probability'] for r in rows],'o-',label=label)
ax[1].set_yscale('log');ax[1].set_xlabel('Radial grid spacing (atomic units)');ax[1].set_ylabel('Neutral-mode transition probability');ax[1].set_title('Nuclear convergence remains unresolved\nE = −0.60; these are NOT DR probabilities');ax[1].legend(fontsize=9)
fig.suptitle('Microscopic progress does not yet provide a physical recombination rate',fontsize=13)
fig.savefig(b/'evidence.png',dpi=170);fig.savefig(b/'evidence.pdf')
