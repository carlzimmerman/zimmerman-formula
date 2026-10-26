from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
fig,ax=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for name,label in [('case_173_N24_dt0.002','Weak density'),('case_207_N24_dt0.002','Intermediate density'),('case_98_N24_dt0.001','Strong, 24³'),('case_98_N32_dt0.001','Strong, 32³')]:
 a=np.genfromtxt(p/f'lattice/{name}.csv',delimiter=',',names=True)
 ax[0].semilogy(a['time'],a['contrast'],label=label)
 ax[1].plot(a['time'],a['gradient_fraction'],label=label)
ax[0].set(ylabel='RMS energy-density contrast / mean',xlabel='Time × local mass m',ylim=(1e-5,2))
ax[1].set(ylabel='Gradient energy / total energy',xlabel='Time × local mass m',ylim=(0,.3))
ax[0].legend(fontsize=8);fig.suptitle('Seeded scalar instability in a periodic box — supplied energy, no abundance prediction',fontsize=11)
fig.savefig(p/'collective_dynamics.png',dpi=160)
