import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
fig,ax=plt.subplots(1,3,figsize=(13,4),layout='constrained')
for b in [1,2,4]:
 r=json.loads((p/f'mass{b}_run/result.json').read_text());ax[0].plot([z['t']*.01207427 for z in r['rows']],[z['mass_apertures'][2]*b for z in r['rows']],label=f'Initial mass {b} Mstar')
ax[0].set(xlabel='Time (Gyr)',ylabel='Mass inside 0.881 kpc / Mstar',title='Inventory is retained');ax[0].legend(fontsize=8)
for name,label in [('long','Quiet heavy seed'),('seed','Perturbed heavy seed')]:
 r=json.loads((p/(name+'_run')/'result.json').read_text());ax[1].plot([z['t']*.01207427 for z in r['rows']],[100*z['absorbed']/abs(r['E0']) for z in r['rows']],label=label)
ax[1].set(xlabel='Time (Gyr)',ylabel='Export / initial energy magnitude (%)',title='Cooling burst weakens');ax[1].legend(fontsize=8)
for name,label in [('mass4','Baseline'),('space','Finer grid + more particles'),('box','Larger box')]:
 r=json.loads((p/(name+'_run')/'result.json').read_text());rad=np.sort(np.linalg.norm(r['final_x'],axis=1))*.4404221297;ax[2].plot(rad,np.arange(1,len(rad)+1)/len(rad),label=label)
ax[2].set(xlabel='Radius (kpc)',ylabel='Enclosed material fraction',title='Profile precision remains limited');ax[2].legend(fontsize=8)
fig.suptitle('Spatial passive-sector tests: real energy export, no selected mass partition',fontsize=12)
fig.savefig(p/'summary.png',dpi=180)
