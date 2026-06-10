#!/usr/bin/env python3
"""
Project 1 first-pass: the deep-MOND velocity relation on the El-Badry+2021 Gaia eDR3 wide-binary catalog,
per PROJECT1_widebinaries_PREREG.md. Data: Zenodo 4435257 `all_columns_catalog.fits.gz` (1.42 GB, DOI-pinned,
gitignored). NO VERDICT -- this maps the disputed signal and probes fork F1 (contamination).

Pre-registered cuts (published-fidelity): RUWE<1.4 both, parallax_over_error>20 both, dist<200 pc.
Observable: sky-projected relative velocity v_sky = 4.74*|Delta_pm|*d  vs the Newtonian circular vN=sqrt(GM/s),
binned by g_N/a0 at the FRAMEWORK a0=9.36e-11. Masses from a rough M_G->mass MS relation (FLAGGED systematic).
CAVEAT (decisive, per prereg): v_sky is NOT deprojected for inclination/eccentricity/phase -- the TREND with
g/a0 is the signal; whether it exceeds Newton needs a matched Newtonian Monte-Carlo (forks F2/F3, next).
Needs astropy, numpy.  C. Zimmerman 2026-06-09.
"""
import numpy as np, warnings, os; warnings.filterwarnings('ignore')
from astropy.io import fits
F=os.path.join(os.path.dirname(__file__),'..','..','data','widebinaries','all_columns_catalog.fits.gz')
c=['parallax1','parallax2','parallax_over_error1','parallax_over_error2','pmra1','pmra2','pmdec1','pmdec2',
   'ruwe1','ruwe2','phot_g_mean_mag1','phot_g_mean_mag2','sep_AU','R_chance_align']
with fits.open(F,memmap=True) as h:
    d=h[1].data; D={k:np.array(d[k],dtype='f8') for k in c}
plx=0.5*(D['parallax1']+D['parallax2']); dist=1000.0/plx
base=((D['ruwe1']<1.4)&(D['ruwe2']<1.4)&(D['parallax_over_error1']>20)&(D['parallax_over_error2']>20)&(dist<200)&(dist>0))
G=6.674e-11;Msun=1.989e30;AU=1.496e11;a0=9.36e-11
MG1=D['phot_g_mean_mag1']-5*np.log10(dist/10);MG2=D['phot_g_mean_mag2']-5*np.log10(dist/10)
mass=lambda MG:np.clip(10**((4.74-MG)/8.75),0.08,2.0)
Mtot=mass(MG1)+mass(MG2); s=D['sep_AU']*AU
vN=np.sqrt(G*Mtot*Msun/s)/1e3; gN=G*Mtot*Msun/s**2
vrel=4.74*np.sqrt((D['pmra1']-D['pmra2'])**2+(D['pmdec1']-D['pmdec2'])**2)*(dist/1000.0)
ratio=vrel/vN; x=np.log10(gN/a0)
m=base&(D['R_chance_align']<0.1)
print(f"pairs {len(s):,} -> cuts {m.sum():,}")
print("\n(1) median(v_sky/v_N) vs g_N/a0:")
for lo,hi in [(2,3),(1,2),(0.5,1),(0,0.5),(-0.5,0),(-1,-0.5),(-1.5,-1)]:
    b=m&(x>=lo)&(x<hi)&np.isfinite(ratio)&(ratio<5)
    if b.sum()>30: print(f"   g/a0~{10**((lo+hi)/2):6.2f} | N={b.sum():>6,} | {np.median(ratio[b]):.3f}")
print("\n(2) fork F1 (contamination): deep-MOND median vs R_chance_align cut:")
for rc in (0.5,0.1,0.01,0.001):
    b=base&(D['R_chance_align']<rc)&(x<-0.5)&np.isfinite(ratio)&(ratio<5)
    print(f"   Rca<{rc:<6}: deep-MOND median = {np.median(ratio[b]):.3f}  (N={b.sum():,})")
print("""
RESULT (no verdict): the v_sky/v_N ratio RISES into deep-MOND (~0.68 -> ~0.88-0.96), and the rise SURVIVES a
500x tighter R_chance_align cut. CORRECTION (Fable, WB-1): this closes only F1 = LINE-OF-SIGHT chance
alignments. R_chance_align is BLIND to HIDDEN TRIPLES (a bound binary with an unresolved close companion) by
construction -- and hidden triples are Banik's PRIMARY contamination mechanism: they inflate v/v_N TWICE
(photocenter wobble in the numerator, missing companion mass making v_N too small in the denominator). So the
honest statement is 'NOT chance-alignment-driven' -- the broader 'contamination' claim is RETRACTED. Fork map: F1 chance-
alignment [CLOSED], F2 eccentricity [OPEN], F3 projection/phase [OPEN], F4 hidden triples [OPEN, PRIMARY].
The decisive test is the twin-resampling Newtonian/MOND Monte-Carlo (with F4 modeled). C1/C2, NOT C3.""")
