"""Plot retained bounded results; no claim-supporting experiment rerun."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
data=np.genfromtxt(root/'run_v2/calculation/modes.csv',delimiter=',',names=True)
profile=np.genfromtxt(root/'run_v2/calculation/plummer.csv',delimiter=',',names=True)
result=json.loads((root/'run_v2/calculation/results.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
fig.suptitle('A constructed tether medium: local wave test and density domain',fontsize=14)
mask=(data['R']==2)&(abs(data['sound_speed_squared']-.01)<1e-12)&(abs(data['angle']-np.pi/2)<1e-10)
d=data[mask]
axes[0].plot(d['x'],1/np.sqrt(1-d['x']),'o--',label='Earlier invariant-only gauge action')
axes[0].plot(d['x'],d['max_speed'],'o-',label='Varied-current medium: R=2, sound²=0.01')
axes[0].axhline(1,color='black',lw=1,label='Metric light speed')
axes[0].set(xlabel='Electric displacement / saturation scale',ylabel='Largest principal speed / c',yscale='log',ylim=(.05,12))
axes[0].legend(fontsize=8,loc='upper left'); axes[0].grid(alpha=.2)
axes[1].loglog(profile['radius_pc'],profile['rho_over_critical'],color='#167c80')
axes[1].axhline(1,color='black',lw=1,label='Local inertia threshold')
axes[1].set(xlabel='Radius (pc)',ylabel='Carrier density / critical density',ylim=(.5,1e15))
axes[1].set_title('Assigned extended baryon source: Plummer 6×10¹⁰ M☉, 3 kpc',fontsize=10)
axes[1].text(.04,.08,'401 sampled radii; no finite halo edge or formation derived',transform=axes[1].transAxes,fontsize=8)
axes[1].legend(fontsize=8); axes[1].grid(alpha=.2)
fig.savefig(root/'medium.png',dpi=180)
