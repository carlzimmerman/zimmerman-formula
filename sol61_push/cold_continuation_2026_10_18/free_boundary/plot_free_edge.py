"""Plot stored finite-boundary profiles; no new physical inference."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

b=Path(__file__).parent
data=json.loads((b/'run_004/results.json').read_text())
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,2,figsize=(11,4.3),layout='constrained')
for H,color in zip([.005,.05,.5],['#2463a1','#139875','#b85e22']):
    row=next(x for x in data['profiles'] if x['A']==1 and x['S']==1 and x['H']==H)
    r=np.asarray(row['sample_x'])*row['edge']
    axes[0].plot(np.r_[r,3.],np.r_[row['sample_mass'],1.],label=f'H = {H:g}',color=color,lw=2)
    axes[1].plot(np.r_[r,3.],np.r_[row['sample_rho'],0.],color=color,lw=2)
    for ax in axes:
        ax.axvline(row['edge'],color=color,alpha=.22,lw=1)
axes[0].set(xlabel=r'Radius $r/r_M$',ylabel=r'Enclosed cold mass $m/M_b$',xlim=(0,3),ylim=(0,1.06))
axes[1].set(xlabel=r'Radius $r/r_M$',ylabel=r'Cold density $\rho\,r_M^3/M_b$',xlim=(0,3),ylim=(0,None))
axes[0].legend(frameon=False)
for ax in axes:ax.grid(alpha=.15)
fig.suptitle('A finite cold-fluid edge with fixed Plummer stars and fixed cold stock',fontsize=13)
fig.supxlabel('Conditional Newtonian action; A = 1, S = 1. Vertical lines mark zero-pressure edges.',fontsize=10)
fig.savefig(b/'FINITE_STOCK_PROFILES.png',dpi=180,facecolor='white')
print(b/'FINITE_STOCK_PROFILES.png')
