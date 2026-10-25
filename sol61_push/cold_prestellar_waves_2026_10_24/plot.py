"""Scientific diagnostics; no inference bands or completion claim."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
HERE=Path(__file__).resolve().parent
fig,axs=plt.subplots(2,2,figsize=(10,6.5),constrained_layout=True)
for tag,color,label in [('sextans_hybrid','#4775b6','L=2'),('sextans_L4','#c05b2e','L=4')]:
    q=json.loads((HERE/'runs'/f'{tag}.json').read_text());h=q['history'];t=np.array([x['t'] for x in h]);J0=q['initial']['J']
    massout=np.array([x['removed']['M'] for x in h]);jout=np.array([x['removed']['J']/J0 for x in h])
    axs[0,0].plot(t,massout,color=color,label=label+' mass')
    axs[0,0].plot(t,jout,color=color,ls='--',label=label+' spin')
    axs[0,1].plot(t,[x['J']/x['M']/J0 for x in h],color=color,label=label)
    axs[1,0].plot(t,[x['M_inner']*q['physical']['Munit_Msun']/1e6 for x in h],color=color,label=label)
    axs[1,1].plot(t,[x['rhalf']*q['physical']['Runit_pc']/1000 for x in h],color=color,label=label)
for ax in axs.flat:
    ax.axvspan(0,24,color='grey',alpha=.09);ax.set_xlabel('Time / initial dynamical unit');ax.grid(alpha=.2)
axs[0,0].set_ylabel('Fraction removed at absorber');axs[0,0].legend(fontsize=8)
axs[0,1].set_ylabel('Retained specific spin / initial');axs[0,1].axhline(1,color='grey',ls=':');axs[0,1].legend()
axs[1,0].set_ylabel('Cold mass inside 486 pc (million Msun)')
axs[1,1].set_ylabel('Cold half-mass radius (kpc)')
fig.suptitle('Sextans finite angular-mode collapse: escape occurs, but the remnant remains variable',fontsize=12)
fig.savefig(HERE/'wave_diagnostics.png',dpi=160)
