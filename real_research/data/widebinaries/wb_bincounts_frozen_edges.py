#!/usr/bin/env python3
"""PROVENANCE SCRIPT for real_research/reviews/wb_a0_amplitude_degeneracy.py.

Extracts the REAL bin populations of log10(g_N/a0) and the bin-median PHYSICAL
g_N on the Banik-exact wide-binary selection (identical cut list to
wb_mond_orbit_mc.py) for the FROZEN DR4 bin edges of
prep_2026/gaia_dr4_prep/wide_binary_pipeline.py.

Output (N_sel = 9508; counts and medians for BOTH a0 footings) is transcribed as
literals into wb_a0_amplitude_degeneracy.py (CNT_CAN/GNMED_CAN/CNT_ALT/GNMED_ALT)
so that the degeneracy analysis is self-contained and runs without the 1.4 GB
El-Badry+2021 eDR3 catalog (gitignored: external catalog, DOI-pinned).
Run this to regenerate/verify those literals.  Requires astropy.
"""
import numpy as np, os, json, warnings
warnings.filterwarnings('ignore')
from astropy.io import fits
G = 6.674e-11; Msun = 1.989e30; AU = 1.496e11
A0C, A0A = 9.36e-11, 1.130e-10
F = '/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/widebinaries/all_columns_catalog.fits.gz'
C = ['ra1', 'dec1', 'parallax1', 'parallax2', 'parallax_error1', 'parallax_error2',
     'pmra1', 'pmra2', 'pmdec1', 'pmdec2', 'pmra_error1', 'pmra_error2',
     'pmdec_error1', 'pmdec_error2', 'ruwe1', 'ruwe2', 'ipd_frac_multi_peak1',
     'ipd_frac_multi_peak2', 'phot_g_mean_mag1', 'phot_g_mean_mag2', 'sep_AU']
with fits.open(F, memmap=True) as h:
    d = h[1].data
    D = {k: np.array(d[k], dtype='f8') for k in C}
aN, dN = np.radians(192.85948), np.radians(27.12825)
ra, dec = np.radians(D['ra1']), np.radians(D['dec1'])
bgal = np.degrees(np.arcsin(np.sin(dec)*np.sin(dN)+np.cos(dec)*np.cos(dN)*np.cos(ra-aN)))
d1 = 1000/D['parallax1']; d2 = 1000/D['parallax2']; dist = 0.5*(d1+d2)
skAU = D['sep_AU']/1e3
sd1 = 1000*D['parallax_error1']/D['parallax1']**2
sd2 = 1000*D['parallax_error2']/D['parallax2']**2
sdd = np.hypot(sd1, sd2)
MG1 = D['phot_g_mean_mag1']-5*np.log10(dist/10)
MG2 = D['phot_g_mean_mag2']-5*np.log10(dist/10)
xg = np.linspace(-1.46, 0.99, 4000)
MGg = 4.887-5.693*xg+0.4164*xg**2+0.9611*xg**3
o = np.argsort(MGg)
mfn = lambda MG: np.exp(np.interp(np.clip(MG, 0.6, 11.1), MGg[o], xg[o]))
Mtot = mfn(MG1)+mfn(MG2)
s = D['sep_AU']*AU
dpm = np.hypot(D['pmra1']-D['pmra2'], D['pmdec1']-D['pmdec2'])
vN = np.sqrt(G*Mtot*Msun/s)/1e3
vsky = 4.74*dpm*(dist/1000); vt = vsky/vN
sel = ((np.abs(bgal) > 15) & (D['phot_g_mean_mag1'] < 17) & (D['phot_g_mean_mag2'] < 17)
       & (dist < 250) & (D['ruwe1'] < 1.2) & (D['ruwe2'] < 1.2)
       & (skAU > 2) & (skAU < 30) & (D['ipd_frac_multi_peak1'] <= 2)
       & (D['ipd_frac_multi_peak2'] <= 2) & (Mtot > 0.464) & (Mtot < 4.31)
       & (vt <= 5) & (np.abs(d1-d2) < np.minimum(4*sdd, 8)))
gN = (G*Mtot*Msun/s**2)[sel]
EDGES = np.array([-1.5, -1.1, -0.8, -0.5, -0.2, 0.1, 0.5, 1.0, 2.2])
out = {'N_sel': int(sel.sum())}
for lab, a0 in (('can', A0C), ('alt', A0A)):
    ly = np.log10(gN/a0)
    cnt = [int(((ly >= EDGES[b]) & (ly < EDGES[b+1])).sum()) for b in range(len(EDGES)-1)]
    # median physical g_N in each bin (m/s^2) -- the model's evaluation point
    med = []
    for b in range(len(EDGES)-1):
        m = (ly >= EDGES[b]) & (ly < EDGES[b+1])
        med.append(float(np.median(gN[m])) if m.sum() > 0 else float('nan'))
    out['cnt_'+lab] = cnt
    out['gNmed_'+lab] = med
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'bincounts.json'), 'w'), indent=1)
