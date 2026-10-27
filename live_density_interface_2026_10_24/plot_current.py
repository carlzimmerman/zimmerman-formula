import json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).parent/'inputs'))
from model import G,A0

p=Path(__file__).parent
bulk=json.loads((p/'run_stable/results.json').read_text())['bulk'][1]
coarse=json.loads((p/'run_stable/results.json').read_text())['joint'][0]
fine=json.loads((p/'run_stable_recovery/results.json').read_text())['refinement'][0]
fig,axes=plt.subplots(1,2,figsize=(12,4.6),layout='constrained')
ax=axes[0]
for r,label,color in [(bulk,'All-T bulk control (no free exterior)','#687b8e'),(coarse,'Free exterior, 96 cells','#b7b7b7'),(fine,'Free exterior, 128 cells','#b84735')]:
    rad=np.array(r['r']);mask=(rad>=1.5)&(rad<=100)
    ax.plot(rad[mask],(np.array(r['g_total'])/r['g_law'])[mask],label=label,color=color,lw=2)
ax.axhline(1,color='#222',ls='--',lw=1);ax.axvspan(1.5,15,color='#c8dfcd',alpha=.4,label='Original inner test interval')
ax.set(xscale='log',xlim=(1.5,100),ylim=(.25,1.35),xlabel='Radius (kpc)',ylabel='Computed gravity / galaxy-law gravity',title='The bulk law survives; the transition does not')
ax.legend(fontsize=8,loc='lower left');ax.grid(alpha=.2)
ax=axes[1];rad=np.array(fine['r']);rm=np.sqrt(G*6e10/A0);R=fine['R_kpc']/rm;edges=R*np.linspace(0,1,fine['n']+1)**2;vol=np.diff(edges**3)/3
mass=np.array(fine['mass']);q=np.array(fine['q'])
for density,label,color in [(mass*q/vol,'Converted T','#245b7b'),(mass*(1-q)/vol,'Free F','#db8b35'),(mass/vol,'Total','#333333')]:
    mask=(rad>=1.5)&(rad<=150);ax.plot(rad[mask],np.maximum(density[mask],1e-9),label=label,color=color,lw=1.7)
ax.axvline(fine['crossings_kpc'][-1],ls=':',color='#777',label='Phase crossing')
ax.set(xscale='log',yscale='log',xlim=(1.5,150),ylim=(3e-10,100),xlabel='Radius (kpc)',ylabel='Density (dimensionless; display floor $10^{-9}$)',title='Density relaxation creates a depleted transition')
ax.legend(fontsize=9);ax.grid(alpha=.2)
fig.savefig(p/'current_result.png',dpi=180)
