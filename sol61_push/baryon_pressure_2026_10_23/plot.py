import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/baryon-pressure-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json,numpy as np
from pathlib import Path
from hydro_v2 import Hydro
base=Path(__file__).parent;fig,axes=plt.subplots(1,3,figsize=(13,4.3))
for name,label,style in [('gas_base','Gas, 256','--'),('gas_fine','Gas, 512','-'),('cooling_fine','H2 sensitivity, 512',':'),('gas_smooth','Initially smooth baryons','-.'),('gas_small','Half seed radius','-')]:
 r=json.loads((base/name/'result.json').read_text());pa=r['parameters'];m=Hydro(pa['n'],pa['amp'],ratio=pa['ratio'],size=pa.get('size',1));f=r['final'];U=np.array(f['U']);A=(f['time']/m.ti)**(2/3);rc=m.dep(np.array(f['xc']),m.mc)[0];rg=m.r*A*m.ell;edge=(np.arange(m.n)+1)*m.dx*A*m.ell;rho,v,p,cs=m.primitive(U);T=p/rho/m.kT
 axes[0].loglog(rg,rc/(sum(m.mc)/sum(m.vol)),style,label=label);axes[1].loglog(rg,T,style);axes[2].loglog(edge,np.cumsum(rc*m.vol)*m.M0,style)
for ax in axes:
 ax.axvline(.3214846543,lw=.7,color='black',alpha=.4);ax.set_xlim(.01,3);ax.set_xlabel('Physical radius (kpc)');ax.grid(alpha=.15)
axes[0].set_ylabel('Cold density / mean');axes[1].set_ylabel('Gas temperature (K)');axes[2].set_ylabel('Enclosed cold mass (solar masses)');axes[0].legend(fontsize=7);axes[2].set_ylim(1e2,2e7)
fig.suptitle('Pressure and thermal evolution at z=10: collapse survives, core selection is unproven',fontsize=11);fig.tight_layout();fig.savefig(base/'profiles.png',dpi=160)
