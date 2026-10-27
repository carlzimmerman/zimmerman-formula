from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=Path(__file__).resolve().parent
data=json.loads((p/'run_source/stdout.txt').read_text())
fig,axes=plt.subplots(1,2,figsize=(11,4.2),constrained_layout=True)
for c in data['cases'][:9]:
    if c['outer_radius']==200:
        x=np.array(c['graph_radius']);y=np.array(c['graph_force_over_leading'])
        mask=(x>=.1)&(x<=80)
        axes[0].semilogx(x[mask],y[mask],label=f"source radius d = {c['source_radius']:g}")
axes[0].axhline(1,color='black',ls='--',lw=1,label='leading 1/r force')
axes[0].set(xlabel='Radius / regulator length',ylabel='Scalar force / leading 1/r force',ylim=(0,1.05),title='Regular finite-source solutions')
axes[0].legend(fontsize=8,loc='lower right')
for idx in [3,4,5,11]:
    c=data['cases'][idx];x=np.array(c['graph_radius']);y=np.array(c['graph_force_over_leading'])
    mask=(x>=10)&(x<=45)
    label=f"L={c['outer_radius']:g}, {c['boundary']}"
    axes[1].plot(x[mask],y[mask],label=label)
axes[1].set(xlabel='Radius / regulator length',ylabel='Scalar force / leading 1/r force',title='Outer-boundary control, d = 1')
axes[1].legend(fontsize=8)
for ax in axes:ax.grid(alpha=.2)
fig.suptitle('Fixed-frame classical model — not a galaxy fit',fontsize=12)
fig.savefig(p/'source_profiles.png',dpi=180)
