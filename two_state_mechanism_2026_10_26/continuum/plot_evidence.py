"""Plot archived measurements; no model fitting or inferred reaction rates."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
b=Path(__file__).resolve().parent;a=json.loads((b/'run_audit/results.json').read_text())
fig,ax=plt.subplots(1,3,figsize=(13,4.3),layout='constrained')
labels=['Integral\n15 → 20','Radial basis\n20 → 25','Angular lmax\n2 → 4']
ax[0].bar(labels,[a['comparisons'][k]['absolute_S00_change'] for k in ['integral_order','radial_basis','angular_basis']],color='#307599')
ax[0].set_ylabel('Absolute change in S₀₀');ax[0].set_title('Corrected continuum checks\nR = 2, E = 0.001')
for run in ['scan_corrected','scan_physical']:
 d=json.loads((b/('run_'+run)/'results.json').read_text())
 for key,v in d.items():
  if not isinstance(v,dict):continue
  ax[1].plot(v['energies'],v['phase_derivative'],label={'multipole15':'M15, N20, L2','corrected20':'M20, N20, L2','physical_radial25':'M20, N25, L2','physical_angular4':'M20, N25, L4'}[key],lw=1.4)
ax[1].set_xlim(.12,.27);ax[1].set_xlabel('Electron energy (atomic units)');ax[1].set_ylabel('d(eigenphase sum)/dE');ax[1].set_title('Electronic resonance candidate\nNot a dissociation rate');ax[1].legend(fontsize=8)
ax[2].plot([r['R'] for r in a['nuclear']],[100*r['omitted_ground_fraction'] for r in a['nuclear']],marker='o',color='#a95730')
ax[2].set_ylim(0,100);ax[2].set_xlabel('Internuclear separation (atomic units)');ax[2].set_ylabel('Ground derivative norm omitted (%)');ax[2].set_title('Four-state nuclear projection\nNot a rate-error estimate')
fig.suptitle('Coulomb continuum progress — nuclear outgoing flux remains unresolved',fontsize=14)
fig.savefig(b/'evidence.png',dpi=170);fig.savefig(b/'evidence.pdf')
