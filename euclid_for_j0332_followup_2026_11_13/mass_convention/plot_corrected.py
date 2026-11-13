"""Display recorded fit and aperture-correct mass comparison; no new inference."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm

B=Path(__file__).resolve().parent
r=json.loads((B/'reweighted_geometry_01/result.json').read_text())
s=r['scenarios']['catalogue_redshift']
f=np.load(B/'reweighted_geometry_01/representative_fit.npz')
model=np.full_like(f['data'],np.nan);model[f['mask']]=f['model_valid']
res=(f['data']-model)/f['noise']
fig=plt.figure(figsize=(12,7.5),layout='constrained')
gs=fig.add_gridspec(2,3,height_ratios=[1.35,1])
norm=SymLogNorm(linthresh=.001,vmin=-.003,vmax=.045)
for j,(arr,title) in enumerate([(f['data'],'Euclid VIS data'),(model,'Model at fixed theory acceleration'),(res,'Residual / released RMS')]):
 ax=fig.add_subplot(gs[0,j]);im=ax.imshow(arr,origin='lower',extent=[-5,5,-5,5],cmap='RdBu_r' if j==2 else 'magma',**({'vmin':-3,'vmax':3} if j==2 else {'norm':norm}));ax.set_xlim(-3,3);ax.set_ylim(-3,3);ax.set_title(title);ax.set_xlabel('West offset (arcsec)')
 if j==0:ax.set_ylabel('North offset (arcsec)')
 if j==2:fig.colorbar(im,ax=ax,shrink=.8)
ax=fig.add_subplot(gs[1,:]);m=np.linspace(11.4,12.2,1000);mu,lo,hi=r['prior_MED_LO_HI_dex'];sig=np.where(m<mu,lo,hi);density=np.exp(-.5*((m-mu)/sig)**2)/(sig*np.sqrt(2*np.pi));ax.plot(m,density,color='#225ea8',lw=2,label='Stellar-population mass constraint');ax.fill_between(m,0,density,where=(m>=mu-lo)&(m<=mu+hi),color='#9ecae1',alpha=.7,label='Approximate central 68% stellar-mass interval');q=s['log10_aperture_mass_quantiles'];ax.axvspan(q[1],q[3],color='#238b45',alpha=.5);ax.axvline(q[2],color='#006d2c',lw=2,label='Image-required mass (fixed light shape)');ax.set_xlim(11.45,12.13);ax.set_ylim(0,5.3);ax.set_xlabel(r'$\log_{10}(M_\star/M_\odot)$ within the same modelling aperture');ax.set_ylabel('Prior density per dex');ax.legend(loc='upper left',fontsize=9);ax.text(.98,.94,'Required: 8.80 × 10¹¹ M☉\nSED median: 6.78 × 10¹¹ M☉\nOffset: 1.31 upper-side error units',transform=ax.transAxes,ha='right',va='top',fontsize=11)
fig.suptitle('FOR J0332: corrected aperture mass comparison\nFixed light shape and constant M/L; no calibrated theory pass probability',fontsize=14)
fig.savefig(B/'for_j0332_corrected_fit.png',dpi=170)
