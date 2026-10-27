#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
import numpy as np

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
out=Path(args.output);out.mkdir(exist_ok=True);os.environ['MPLCONFIGDIR']=str(out/'mpl_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

r=Path(__file__).resolve().parent
disc=json.loads((r/'discovery_run001/results.json').read_text())
rep=json.loads((r/'replication_run001/results.json').read_text())
extra=json.loads((r/'additional_run001/results.json').read_text())
a=np.load(r/'discovery_run001/arrays.npz');s=np.load(r/'additional_run001/arrays.npz')
candidate=disc['frozen_candidate']
fig,ax=plt.subplots(2,2,figsize=(13.8,9.4),constrained_layout=True)
hr=a['HR_aligned40'];moment=(hr-hr[::-1,::-1,::-1]).sum(0)*4.12*np.pi/(4*np.log(2))*40**2
lim=np.percentile(abs(moment),97)
im=ax[0,0].imshow(moment,origin='lower',extent=[-300,300,-120,120],aspect='auto',cmap='RdBu_r',vmin=-lim,vmax=lim)
ax[0,0].add_patch(Rectangle((candidate['x_arcsec']-20,candidate['z_arcsec']-20),40,40,fill=False,lw=2,color='#00bd89'))
ax[0,0].add_patch(Rectangle((-candidate['x_arcsec']-20,-candidate['z_arcsec']-20),40,40,fill=False,lw=2,color='#00bd89'))
known=[(-72,80),(112,92),(120,-76)]
ax[0,0].scatter(*np.array(known).T,c='#f9ca24',marker='x',s=55,label='Published features')
ax[0,0].set(xlabel='Major-axis angle [arcsec], NE positive',ylabel='Minor-axis angle [arcsec], SE positive',title='Observed point-inversion residual, HALOGAS')
ax[0,0].legend(loc='lower left',fontsize=8)
fig.colorbar(im,ax=ax[0,0],label='Velocity-integrated difference [Jy beam⁻¹ km s⁻¹], 40″ beam',shrink=.8)
u=(np.arange(60)-29.5)*4.12
for name,color,ls in [('HR','#164e63','-'),('WHISP','#b45309','--')]:
 ax[0,1].plot(u,s[name+'_candidate_spectrum_sideA_Jy']*1000,color=color,ls=ls,label=name+' side A')
 ax[0,1].plot(u,s[name+'_candidate_spectrum_sideB_Jy']*1000,color=color,ls=ls,alpha=.5,label=name+' mirrored side B')
ax[0,1].axvspan(candidate['u_km_s']-12.36,candidate['u_km_s']+12.36,color='#00bd89',alpha=.13)
ax[0,1].axhline(0,color='.7',lw=.7)
ax[0,1].set(xlim=(-120,120),xlabel='Velocity relative to 404.8 km s⁻¹ [km s⁻¹]',ylabel='Flux density in frozen 40″ × 40″ patch [mJy]',title='Frozen patch: two independently observed cubes')
ax[0,1].legend(fontsize=8,ncol=2)
names=['HR','LR','WHISP'];labels=['HALOGAS HR','HALOGAS LR\nsame observations','1996 WHISP\nindependent observations']
for i,n in enumerate(names):
 d=(disc if n!='WHISP' else rep)['datasets'][n]['candidate']
 ax[1,0].errorbar(i,d['signed_difference_Jy_km_s'],yerr=d['blank_scatter'],fmt='o',capsize=5,color='#164e63' if n!='WHISP' else '#b45309')
 de=extra['datasets'][n]['matched_operator_controls']['dewarp']['candidate']
 ax[1,0].plot(i+.12,de['signed_difference_Jy_km_s'],'s',color='#7c3aed',markersize=5)
ax[1,0].axhline(0,color='.5',lw=.8)
ax[1,0].set(xticks=range(3),xticklabels=labels,ylabel='Frozen signed difference [Jy km s⁻¹]',title='Same sign in WHISP; much larger noise scatter')
ax[1,0].text(.02,.04,'Bars: one measured blank-aperture scatter; no discovery significance.\nPurple squares: empirical dewarp diagnostic.',transform=ax[1,0].transAxes,fontsize=8)
controls=disc['datasets']['HR']['controls']
cs=[c for c in controls if c['kind']=='center_vsys' and c['dx_arcsec']==0 and c['dv_km_s']==0]
cs=sorted(cs,key=lambda c:c['dz_arcsec'])
xx=[c['dz_arcsec'] for c in cs]
ax[1,1].plot(xx,[c['candidate']['signed_difference_Jy_km_s'] for c in cs],'o-',color='#164e63',label='Frozen patch difference')
ax[1,1].axhline(0,color='.6',lw=.8)
right=ax[1,1].twinx()
base=disc['datasets']['HR']['baseline']['all']['difference_power']
right.plot(xx,[c['all']['difference_power']/base for c in cs],'s--',color='#b45309',label='Whole-aperture mismatch / nominal')
right.set_ylabel('Whole-aperture difference power / nominal',color='#b45309')
ax[1,1].set(xlabel='Assumed minor-axis center shift [arcsec]',ylabel='Frozen patch difference [Jy km s⁻¹]',title='Center shifts also change the rest of the galaxy')
ax[1,1].text(.03,.94,'A local cancellation is not a globally acceptable center.',transform=ax[1,1].transAxes,va='top',fontsize=8)
for a0 in ax.ravel():a0.grid(alpha=.14)
fig.suptitle('NGC5023: raw HI symmetry test — no cosmology or acceleration law',fontsize=15)
fig.savefig(out/'summary.png',dpi=160)
plt.close(fig)
print('summary.png saved')
