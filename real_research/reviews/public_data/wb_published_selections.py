#!/usr/bin/env python3
"""
WB-2b: D1 (noise) + D2 (super-escape) diagnostics under RECONSTRUCTIONS of Chae's and Banik's published wide-
binary cuts, vs the loose hybrid. Same catalog (El-Badry Zenodo 4435257, gitignored), same scripts as wb2.
RECONSTRUCTIONS target the published pair counts (Chae ~26.5k, Banik ~8.6k) -- NOT exact cut replications;
the Banik-grade comes back ~12.8k (looser than his actual RV/triple screen). See WB2B_PUBLISHED_SELECTIONS.md.
C. Zimmerman 2026-06-09. Needs astropy, numpy.
"""
import numpy as np, warnings, os; warnings.filterwarnings('ignore')
from astropy.io import fits
F=os.path.join(os.path.dirname(__file__),'..','..','data','widebinaries','all_columns_catalog.fits.gz')
cols=['parallax1','parallax2','parallax_error1','parallax_error2','parallax_over_error1','parallax_over_error2',
   'pmra1','pmra2','pmdec1','pmdec2','pmra_error1','pmra_error2','pmdec_error1','pmdec_error2','ruwe1','ruwe2',
   'phot_g_mean_mag1','phot_g_mean_mag2','sep_AU','R_chance_align',
   'dr2_radial_velocity1','dr2_radial_velocity2','dr2_radial_velocity_error1','dr2_radial_velocity_error2']
with fits.open(F,memmap=True) as h:
    d=h[1].data; D={k:np.array(d[k],dtype='f8') for k in cols}
plx=0.5*(D['parallax1']+D['parallax2']); dist=1000.0/plx
G=6.674e-11;Msun=1.989e30;AU=1.496e11;a0=9.36e-11
def diag(sel):
    s=D['sep_AU'][sel]*AU; di=dist[sel]; px=plx[sel]
    MG1=D['phot_g_mean_mag1'][sel]-5*np.log10(di/10);MG2=D['phot_g_mean_mag2'][sel]-5*np.log10(di/10)
    M=np.clip(10**((4.74-MG1)/8.75),0.08,2)+np.clip(10**((4.74-MG2)/8.75),0.08,2)
    vN=np.sqrt(G*M*Msun/s)/1e3; x=np.log10(G*M*Msun/s**2/a0)
    dra=D['pmra1'][sel]-D['pmra2'][sel];dde=D['pmdec1'][sel]-D['pmdec2'][sel];dpm=np.hypot(dra,dde)
    vt=4.74*dpm*(di/1000)/vN
    sdpm=np.sqrt((dra*np.hypot(D['pmra_error1'][sel],D['pmra_error2'][sel]))**2
                +(dde*np.hypot(D['pmdec_error1'][sel],D['pmdec_error2'][sel]))**2)/np.maximum(dpm,1e-6)
    sd=1000*0.5*np.hypot(D['parallax_error1'][sel],D['parallax_error2'][sel])/px**2
    svt=np.sqrt((4.74*di/1000*sdpm)**2+(4.74*dpm/1000*sd)**2)/vN
    deep=(x<-0.5)&np.isfinite(vt)
    return sel.sum(),deep.sum(),np.median(svt[deep]),np.mean(vt[deep]>np.sqrt(2))
base=(D['ruwe1']<1.4)&(D['ruwe2']<1.4)&(dist>0); skAU=D['sep_AU']/1e3
chae=base&(dist<200)&(D['parallax_over_error1']>30)&(D['parallax_over_error2']>30)&(D['R_chance_align']<0.1)&(skAU>2)&(skAU<30)&(D['phot_g_mean_mag1']<18)&(D['phot_g_mean_mag2']<18)
rvok=np.isfinite(D['dr2_radial_velocity1'])&np.isfinite(D['dr2_radial_velocity2'])
drv=np.abs(D['dr2_radial_velocity1']-D['dr2_radial_velocity2']); rverr=np.hypot(D['dr2_radial_velocity_error1'],D['dr2_radial_velocity_error2'])
banik=chae&(D['parallax_over_error1']>50)&(D['parallax_over_error2']>50)&rvok&(drv<np.maximum(4.0,3*rverr))
hyb=base&(D['parallax_over_error1']>20)&(D['parallax_over_error2']>20)&(D['R_chance_align']<0.1)&(dist<200)
print(f"{'selection':>20}{'N':>9}{'N_deep':>8}{'D1 sig/vN':>11}{'D2 super-esc':>13}")
for sel,lab in [(hyb,'hybrid'),(chae,'Chae-grade recon'),(banik,'Banik-grade recon')]:
    N,nd,d1,d2=diag(sel); print(f"{lab:>20}{N:>9,}{nd:>8,}{d1:>11.3f}{d2:>13.3f}")
print("reconstructions, NOT exact cuts (Banik-grade ~12.8k vs his ~8.6k); trend cut-insensitive, threshold-crossing not.")
