import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/physical-refinement-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json,numpy as np
from pathlib import Path
from radial_v2 import Radial
p=Path(__file__).parent
fig,ax=plt.subplots(1,2,figsize=(10,4.2))
for name,label,style in [('newton','3%, 256','--'),('fine','3%, 512','-'),('strong','5%, 256','--'),('strong_fine','5%, 512','-'),('strong_late','5%, 512, z=8',':')]:
 r=json.loads((p/name/'result.json').read_text());pa=r['parameters'];m=Radial(pa['n'],pa['amp'],pa['zi'],pa['size']);f=r['final'];A=(f['time']/m.ti)**(2/3);rho,_,_=m.dep(np.array(f['xc']),m.mc);radius=m.r*A*m.ell;contrast=rho/(m.mc.sum()/m.vol.sum());mass=np.cumsum(rho*m.vol)*m.M0
 ax[0].loglog(radius,contrast,style,label=label);ax[1].loglog((np.arange(m.n)+1)*m.dx*A*m.ell,mass,style,label=label)
for a in ax:
 a.axvline(.3214846543,color='black',lw=.8,alpha=.5);a.set_xlim(.008,3);a.grid(alpha=.15);a.set_xlabel('Physical radius (kpc)')
ax[0].set_ylabel('Cold density / mean');ax[1].set_ylabel('Enclosed cold mass (solar masses)');ax[1].set_ylim(1,2e7);ax[0].legend(fontsize=8)
fig.suptitle('Radial collapse: aperture convergence does not resolve the central peak',fontsize=11)
fig.tight_layout();fig.savefig(p/'profiles.png',dpi=160)
