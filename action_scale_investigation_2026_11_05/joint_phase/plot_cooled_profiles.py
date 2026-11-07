"""Render already-recorded profiles and eigenvalue convergence, without fitting."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
b=Path(__file__).resolve().parent
main=json.loads((b/'evidence/cooled_profiles/result.json').read_text())
extra=json.loads((b/'evidence/cooled_profiles_followup/result.json').read_text())
cases=[next(c for c in main['cases'] if c['gamma']==g and c['source_scale']==1) for g in [1,2]]
cases.append(next(c for c in extra['cases'] if c['label']=='strong_gravity'))
fig,axs=plt.subplots(2,2,figsize=(10,7),layout='constrained')
for c,color in zip(cases,['#1565c0','#d97706','#7c3aed']):
 p=c['runs'][-1]['profile'];r=np.array(p['r']);label=f"gravity parameter {c['gamma']:g}"
 axs[0,0].semilogy(r,p['n'],color=color,label=label)
 axs[0,1].plot(r,p['T'],color=color,label=label)
 axs[1,0].plot(r,np.sqrt(p['v2']),color=color,label=label)
 axs[1,1].plot([x['N'] for x in c['runs']], [x['max_eigen_real']*1e4 for x in c['runs']],'-o',color=color,label=label)
for ax,title,y in [(axs[0,0],'Solved density profiles','number density'),(axs[0,1],'Solved temperature profiles','temperature'),(axs[1,0],'Circular-speed curves','circular speed')]:
 ax.set(title=title,xlabel='radius (dimensionless)',ylabel=y);ax.grid(alpha=.2)
axs[0,0].legend(fontsize=8)
axs[1,1].set(title='Slowest radial mode: refinement',xlabel='radial cells',ylabel='largest Re(eigenvalue) × 10⁴');axs[1,1].grid(alpha=.2)
fig.suptitle('Radiatively cooled fluid: prescribed reflecting boundary at R = 3\nDimensionless conditional model; negative eigenvalues mean radial damping',fontsize=12)
fig.savefig(b/'cooled_profiles.png',dpi=180)
fig.savefig(b/'cooled_profiles.pdf')
