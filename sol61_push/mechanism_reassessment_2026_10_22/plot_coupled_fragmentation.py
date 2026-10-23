"""Render measured early-stage observables; no inferred cold yield."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
fig,axes=plt.subplots(1,2,figsize=(11,4.2),constrained_layout=True)
for label,folder,name in [('64³','coupled_fragmentation_run','space'),('96³','coupled_fragmentation_96_run','fine96')]:
 t=np.genfromtxt(p/folder/(name+'.csv'),delimiter=',',names=True)
 variance=np.convolve(t['phi_variance'],np.ones(10),'valid')
 total=np.convolve(t['phi_variance']+t['phi_mean_squared'],np.ones(10),'valid')
 axes[0].plot(t['z'][9:],variance/total,label=label)
 rho=t['phi_kinetic_physical']+t['phi_gradient']+t['phi_potential']
 press=t['phi_kinetic_physical']-t['phi_gradient']/3-t['phi_potential']
 axes[1].plot(t['z'][9:],np.convolve(press,np.ones(10),'valid')/np.convolve(rho,np.ones(10),'valid'),label=label)
axes[0].set(ylabel='Inhomogeneous fraction of field variance',xlabel='Conformal time z',ylim=(0,1))
axes[1].set(ylabel='Averaged Phi pressure / energy',xlabel='Conformal time z',ylim=(-.1,.65))
axes[1].axhline(1/3,color='gray',linestyle='--',label='Radiation: 1/3')
axes[1].axhline(0,color='gray',linestyle=':',label='Cold matter: approximately 0')
for ax in axes: ax.legend(frameon=False);ax.grid(alpha=.2)
fig.suptitle('Coupled early field evolution: spatial structure, no established cold relic')
fig.savefig(p/'coupled_fragmentation.png',dpi=170)
