import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
s=json.loads((p/'static_v2_run/result.json').read_text());w=json.loads((p/'wells_run/result.json').read_text());b=json.loads((p/'affine_refine_run/result.json').read_text())['cases'][0];c=json.loads((p/'affine_convergence_run/result.json').read_text())['cases'][1]
fig,ax=plt.subplots(1,3,figsize=(13,4),layout='constrained')
for R in [.4,.6,.9]:
 rows=[r for r in s['rows'] if r['R']==R];ax[0].plot([r['mass']/.08408132497418408 for r in rows],[r['mass_scaled_force_difference'] for r in rows],'o-',label=f'Width R/ell0 = {R}')
ax[0].set(xlabel='Source mass / reference mass',ylabel='Relative defect in force scaling',title='Nonlinearity breaks scaling');ax[0].legend(fontsize=8)
rows=[r for r in w['rows'] if r['n']==64 and r['box']==6];ax[1].plot([r['b'] for r in rows],[r['energy_per_mass'] for r in rows],'o-',color='purple');ax[1].set(xlabel='Mass / reference mass',ylabel='E/M in units a0 ell0',title='Binding still favors larger masses')
colors=['#3b6fb6','#d57c29','#359567']
for i in range(3):
 ax[2].plot([r['t']*.0120742729 for r in b['rows']],[r['axes'][i]*.4404221297 for r in b['rows']],color=colors[i],label=f'Axis {i+1}, grid40')
 ax[2].plot([r['t']*.0120742729 for r in c['rows']],[r['axes'][i]*.4404221297 for r in c['rows']],color=colors[i],ls='--',alpha=.8)
ax[2].set(xlabel='Time (Gyr)',ylabel='Gaussian width (kpc)',title='Affine rebound; dashed = grid48');ax[2].legend(fontsize=8)
fig.suptitle('Exact nonlinear fields in restricted matter models — no derived fragment masses',fontsize=12)
fig.savefig(p/'summary.png',dpi=180)
