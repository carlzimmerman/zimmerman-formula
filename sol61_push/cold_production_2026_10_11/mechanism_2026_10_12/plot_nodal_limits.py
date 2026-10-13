"""Plot separately valid asymptotes; deliberately leave crossover uncomputed."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
fig,ax=plt.subplots(figsize=(8,4.7),layout='constrained')
x=np.geomspace(1e-4,1e3,500)
ax.loglog(x,x,'--',color='#666666',label='Target scaling: y = x')
lo=np.geomspace(1e-4,.03,200);hi=np.geomspace(10,1e3,200)
ax.loglog(lo,(32/np.pi**3)**2*lo**2,color='#1765ad',lw=2.6,label='Weak-source calculation')
ax.loglog(hi,hi-2/9,color='#b04d10',lw=2.6,label='Large-gap gradient expansion')
ax.axvspan(.03,10,color='#aaaaaa',alpha=.12)
ax.text(.7,1e-6,'Crossover not computed',ha='center',color='#666666',fontsize=10)
ax.set(xlabel=r'Baryonic mass $M/M_s$ (free model scale)',ylabel=r'$V^4/(K M_s)$',title='The generated interaction predicts a change in mass scaling',xlim=(1e-4,1e3),ylim=(1e-9,2e3))
ax.grid(alpha=.15);ax.legend(loc='upper left',frameon=False)
fig.text(.5,-.035,'Conditional zero-temperature model; curves are asymptotes, not galaxy data or a full solution.',ha='center',fontsize=9)
fig.savefig(p/'nodal_force_limits.png',dpi=180,bbox_inches='tight')
