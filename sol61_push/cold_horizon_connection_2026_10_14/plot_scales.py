import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
j=json.loads((p/'run_v1/results.json').read_text())
c=j['constants']; G=c['G']; cc=c['c']; a=c['a0']; ms=c['Msun_kg']; H=c['H_per_s']; pc=3.0856775814913673e16
m=np.geomspace(1e3,1e14,400); rM=np.sqrt(G*m*ms/a)/(1000*pc); rta=(G*m*ms/H**2)**(1/3)/(1000*pc)
fig,ax=plt.subplots(figsize=(9.5,5.8),layout='constrained')
ax.loglog(m,rM,color='#2374ab',lw=2.5,label='Model transition: mass exponent 1/2')
ax.loglog(m,rta,color='#c36b22',lw=2.2,label='Newtonian attraction = vacuum repulsion: exponent 1/3')
ax.loglog(m,2**(1/6)*rta,color='#76659c',lw=1.5,ls='--',label='Mass curvature = vacuum curvature: exponent 1/3')
ax.scatter([4e6,6e10],[j['mass_examples'][1]['rM_kpc'],j['mass_examples'][3]['rM_kpc']],s=55,zorder=5,color='#2374ab')
ax.annotate('Assigned central BH\n77 pc',xy=(4e6,.0771785),xytext=(9e6,.009),arrowprops={'arrowstyle':'-','color':'#666'},fontsize=10)
ax.annotate('Assigned galaxy mass\n9.45 kpc',xy=(6e10,9.4524),xytext=(2e8,.8),arrowprops={'arrowstyle':'-','color':'#666'},fontsize=10)
ax.set(xlabel='Spherical source mass (solar masses)',ylabel='Radius (kpc)',title='The geometric-mean transition is distinct from vacuum-force balance')
ax.text(.02,.97,r'$r_M=1.701\sqrt{r_gL}$,  $r_g=2GM/c^2$,  $L=5.375$ Gpc'+'\nConditional on the project’s fitted acceleration scale',transform=ax.transAxes,va='top',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
ax.grid(True,which='major',alpha=.2); ax.legend(loc='lower right',fontsize=9)
ax.set_ylim(.0008,2e4)
fig.savefig(sys.argv[1],dpi=170)
