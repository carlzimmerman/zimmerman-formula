"""Plot existing finite source-capacity and conditional mass records."""
import json,csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parent
g=json.loads((B/'geometry_audit/run_01/result.json').read_text())
d=json.loads((B/'dynamics/run_01/central.json').read_text())
rows=list(csv.DictReader((B/'dynamics/run_01/mass_scan.csv').open()))
x=np.array([float(r['log10_total_mass']) for r in rows])
prior=np.array([float(r['SED_prior_density_per_dex']) for r in rows])
post=np.array([float(r['v21_posterior_beta0.0_seeing1.2']) for r in rows])
fig,ax=plt.subplots(2,1,figsize=(10,7),sharex=True,layout='constrained',height_ratios=[1.3,1])
for cap,label,color in [('flat_matter_Lambda_horizon','Any source distance in the fiducial cosmology','#7a0177'),('conservative_beta_le_one','Larger, conservative domain: 0 ≤ Dls/Ds ≤ 1','#0570b0')]:
 r=[a for a in g['capacity_rows'] if a['inclination']==90 and a['gamma_max']==.3 and a['geometry_cap_name']==cap]
 ax[0].plot([a['logmass'] for a in r],[a['minimum_diameter_primal_arcsec'] for a in r],label=label,color=color,lw=2)
ax[0].axhline(.3,color='black',ls='--',label='Released association threshold: 0.3″')
ax[0].set_ylabel('Smallest source-marker diameter (arcsec)')
ax[0].set_ylim(0,2.6);ax[0].legend(fontsize=9)
ax[1].plot(x,prior,label='Aperture-corrected stellar-mass constraint',color='#238b45',lw=2)
ax[1].plot(x,post,label='Plus spherical DESI dynamics fixture',color='#636363',lw=2)
for a in ax:a.axvline(d['logM_infinite_SED_median'],color='#238b45',ls=':',lw=1.5)
ax[1].set_ylabel('Conditional mass density per dex')
ax[1].set_xlabel('log₁₀(infinite Sérsic stellar-mass normalization / M☉)')
ax[1].set_xlim(11.7,12.4);ax[1].set_ylim(bottom=0);ax[1].legend(fontsize=9,loc='upper right')
fig.suptitle('L015780: conditional source-position and mass constraints\nFixed edge-on light profile; zero convergence; shear magnitude ≤ 0.3',fontsize=13)
fig.savefig(B/'constraints.png',dpi=170)
