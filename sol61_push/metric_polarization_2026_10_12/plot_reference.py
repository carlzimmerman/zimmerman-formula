"""Render existing checked outputs; does not generate scientific data."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=Path(__file__).parent
a=json.loads((p/'adaptation_run/results.json').read_text())
s=json.loads((p/'reference_run/results.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(11,4.3),layout='constrained')
for frozen,label,color in [(False,'Adaptive reference','#167b8e'),(True,'Reference held fixed','#c25a38')]:
    row=next(r for r in a['runs'] if r['N']==128 and r['external_step']==3 and r['frozen_reference']==frozen)
    h=row['history']
    axes[0].plot([x['t'] for x in h],[100*x['relative_internal_error'] for x in h],'-o',label=label,color=color,markersize=4)
axes[0].set(xlabel='Time (uncalibrated model units)',ylabel='Internal-profile change (%)',title='Response to a uniform external-force step')
axes[0].legend(frameon=False)
for K in [10,100,1000]:
    row=next(r for r in s['profiles'] if r['outer']==600 and r['K']==K)
    axes[1].plot(row['radii'],row['polarization_over_zero_stiffness'],'-o',label=f'K = {K}',markersize=4)
axes[1].axhline(1,color='gray',linestyle='--',linewidth=1)
axes[1].set(xscale='log',yscale='log',xlabel='Radius / baryon scale radius',ylabel='Polarization / unregulated MOND value',title='The reference also changes the radial profile')
axes[1].legend(frameon=False)
for ax in axes: ax.grid(alpha=.15)
fig.suptitle('Reduced Newtonian toy model — no observational fit or relativistic test',fontsize=11)
fig.savefig(p/'reference_result.png',dpi=180)
