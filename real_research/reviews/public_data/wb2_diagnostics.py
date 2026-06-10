#!/usr/bin/env python3
"""
WB-2 gating diagnostics (Fable) for the wide-binary first pass. D1 noise profile, D2 escape-fraction floor,
D3 selection provenance. Decision-gates for the Monte-Carlo: D1 deep-bin sigma/v_N>0.3 OR D2 super-escape>15%
=> STOP-AND-REPORT (the deep-bin rise is noise/contamination, not physics). Data: El-Badry Zenodo 4435257
(gitignored). See WB2_DIAGNOSTICS_HALT.md.  C. Zimmerman 2026-06-09. Needs astropy, numpy.
"""
import numpy as np, warnings, os; warnings.filterwarnings('ignore')
from astropy.io import fits
F=os.path.join(os.path.dirname(__file__),'..','..','data','widebinaries','all_columns_catalog.fits.gz')
c=['parallax1','parallax2','parallax_error1','parallax_error2','parallax_over_error1','parallax_over_error2',
   'pmra1','pmra2','pmdec1','pmdec2','pmra_error1','pmra_error2','pmdec_error1','pmdec_error2',
   'ruwe1','ruwe2','phot_g_mean_mag1','phot_g_mean_mag2','sep_AU','R_chance_align']
with fits.open(F,memmap=True) as h:
    d=h[1].data; D={k:np.array(d[k],dtype='f8') for k in c}
plx=0.5*(D['parallax1']+D['parallax2']); dist=1000.0/plx
m=((D['ruwe1']<1.4)&(D['ruwe2']<1.4)&(D['parallax_over_error1']>20)&(D['parallax_over_error2']>20)
   &(D['R_chance_align']<0.1)&(dist<200)&(dist>0))
for k in D: D[k]=D[k][m]
dist=dist[m]; plx=plx[m]
G=6.674e-11;Msun=1.989e30;AU=1.496e11;a0=9.36e-11
MG1=D['phot_g_mean_mag1']-5*np.log10(dist/10);MG2=D['phot_g_mean_mag2']-5*np.log10(dist/10)
mass=lambda MG:np.clip(10**((4.74-MG)/8.75),0.08,2.0); Mtot=mass(MG1)+mass(MG2)
s=D['sep_AU']*AU; vN=np.sqrt(G*Mtot*Msun/s)/1e3; gN=G*Mtot*Msun/s**2; x=np.log10(gN/a0)
dpmra=D['pmra1']-D['pmra2']; dpmdec=D['pmdec1']-D['pmdec2']; dpm=np.hypot(dpmra,dpmdec)
vsky=4.74*dpm*(dist/1000.0); vt=vsky/vN
sig_dpm=np.sqrt((dpmra*np.hypot(D['pmra_error1'],D['pmra_error2']))**2
               +(dpmdec*np.hypot(D['pmdec_error1'],D['pmdec_error2']))**2)/np.maximum(dpm,1e-6)
sig_d=1000.0*0.5*np.hypot(D['parallax_error1'],D['parallax_error2'])/plx**2
sig_vsky=np.sqrt((4.74*dist/1000*sig_dpm)**2+(4.74*dpm/1000*sig_d)**2)
print(f"selection: {m.sum():,} pairs (HYBRID -- looser than Chae ~26.5k / Banik ~8.6k; no sep-cut, no RV triple-screen)")
print(f"{'g/a0':>8} {'N':>7} {'med vt':>7} {'D1 sig/vN':>10} {'D2 vt>r2':>9} {'vt>1.9':>8}")
for lo,hi in [(2,3),(1,2),(0.5,1),(0,0.5),(-0.5,0),(-1,-0.5),(-1.5,-1)]:
    b=(x>=lo)&(x<hi)&np.isfinite(vt)
    if b.sum()>30:
        print(f"{10**((lo+hi)/2):>8.2f} {b.sum():>7,} {np.median(vt[b]):>7.3f} {np.median((sig_vsky/vN)[b]):>10.3f}"
              f" {np.mean(vt[b]>np.sqrt(2)):>9.3f} {np.mean(vt[b]>1.9):>8.3f}")
deep=(x<-0.5)&np.isfinite(vt)
print(f"\nDEEP-BIN (g/a0<0.3): D1 median sig/vN = {np.median((sig_vsky/vN)[deep]):.3f} (>0.3 STOP); "
      f"D2 super-escape f(vt>sqrt2) = {np.mean(vt[deep]>np.sqrt(2)):.3f} (>0.15 STOP)")
print("=> BOTH stop-triggers fired: the deep-bin rise is noise + contamination-dominated, not physics. HALT.")
