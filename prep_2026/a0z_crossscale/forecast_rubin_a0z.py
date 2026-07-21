#!/usr/bin/env python3
"""
FORECAST (not data): does Rubin/LSST SNe Ia SETTLE the a0(z) gate for the framework?
The framework's distinctive prediction a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE0) lives-or-dies on
whether dark energy evolves. Rubin gets light curves for ~400k SNe Ia (z<1); photometric
SN cosmology forecasts reach DETF FoM ~150 (LSST-alone) up to ~500 (LSST+CMB/BAO), vs
DES ~54 and Pantheon+/DESI-DR2 (~2.2 sigma on the a0 decline, our desi_posterior_a0z.py).
We propagate REPRESENTATIVE projected Rubin w0-wa covariances through the framework relation
and ask: at what significance does Rubin distinguish the framework's DECLINE from flat (w=-1)?
CPL: rho_DE(z)/rho_DE0=(1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z)); a0 ratio = sqrt of that (Z cancels
-> footing-independent). NOT A MEASUREMENT: Rubin has no calibrated SN Hubble diagram yet
(survey started 2026-06-30); the DESC cosmology sample is ~2027+. This is a forecast.
"""
import numpy as np
np.seterr(all='ignore')
from scipy.special import erfcinv
def a0ratio(z,w0,wa): return np.sqrt((1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z)))
def sig_decline(w0,sw0,wa,swa,rho,truth_w0,truth_wa,N=300000,z=3.0):
    g=np.random.default_rng(0)
    L=np.linalg.cholesky([[sw0**2,rho*sw0*swa],[rho*sw0*swa,swa**2]])
    pr=np.array([w0,wa])+g.standard_normal((N,2))@L.T
    r=a0ratio(z,pr[:,0],pr[:,1])
    truth=a0ratio(z,truth_w0,truth_wa)
    med,lo,hi=np.median(r),np.percentile(r,16),np.percentile(r,84)
    # significance that a0(3) differs from FLAT (=1.0), given this forecast error
    frac=max(np.mean(r>=1.0) if truth<1 else np.mean(r<=1.0),0.5/N)
    s=np.sqrt(2)*erfcinv(2*frac)
    return med,lo,hi,s,truth

# central "truth" = DESI-preferred evolving DE (the hypothesis Rubin will test)
TW0,TWA=-0.838,-0.62
print("a0(z=3)/a0(0) gate: framework DECLINE ~0.74 (DESI-central truth) vs FLAT=1.00 (w=-1)")
print("="*76)
cases=[
 ("DESI DR2 now (baseline)",          -0.838,0.055,-0.62,0.22,-0.86),
 ("Rubin SN moderate (FoM~150)",      -0.838,0.040,-0.62,0.15,-0.90),
 ("Rubin SN + CMB/BAO (FoM~500)",     -0.838,0.020,-0.62,0.08,-0.90),
]
for name,w0,sw0,wa,swa,rho in cases:
    med,lo,hi,s,truth=sig_decline(w0,sw0,wa,swa,rho,TW0,TWA)
    print(f"\n[{name}]  sigma(w0)={sw0}, sigma(wa)={swa}")
    print(f"    a0(3)/a0(0) = {med:.3f} [{lo:.3f},{hi:.3f}]  -> DECLINE detected at {s:.1f} sigma vs flat")
print("\n" + "="*76)
print("MIRROR TEST -- IF the universe is actually FLAT (w=-1, a0 truly constant):")
for name,w0,sw0,wa,swa,rho in cases[1:]:
    # truth flat; how tightly does Rubin pin a0(3) to 1.0, i.e. exclude the framework's 0.74?
    g=np.random.default_rng(1); L=np.linalg.cholesky([[sw0**2,rho*sw0*swa],[rho*sw0*swa,swa**2]])
    pr=np.array([-1.0,0.0])+g.standard_normal((300000,2))@L.T
    r=a0ratio(3.0,pr[:,0],pr[:,1]); sd=np.std(r)
    excl=abs(1.0-0.74)/sd
    print(f"  [{name}]: a0(3)/a0(0)=1.00 +/- {sd:.3f} -> the framework's 0.74 EXCLUDED at {excl:.1f} sigma")
print("\n" + "="*76)
print("VERDICT (forecast, both ways): Rubin SNe are the instrument that DECIDES the gate.")
print("  - If DE evolves at the DESI-central rate: Rubin sharpens the a0-decline detection from")
print("    DESI-now ~2.0 to ~3.3 sigma (SN-alone, FoM~150) / ~4.6 sigma (SN+CMB/BAO, FoM~500) --")
print("    crosses 3 sigma, approaches but does not alone reach 5 at the DESI-central 0.775-vs-1.0 (~0.22) gap.")
print("  - If DE is flat: Rubin pins a0(3)=1.00 and EXCLUDES the framework's 0.74 at ~3.3 sigma (FoM~150)")
print("    / ~6.0 sigma (FoM~500). The gate is likely settled at 3-6 sigma by ~2028-30 -- a real upgrade")
print("    on DESI-now, NOT a one-instrument 9-sigma slam dunk at the DESI-central rate.")
print("  CAVEATS: forecast, not data (no calibrated Rubin SN Hubble diagram until DESC ~2027+; the raw")
print("  alert stream is discoveries, not cosmology). This is the COSMOLOGY-SIDE gate -- it decides")
print("  whether a0(z) evolves at all; the DISTINCTIVE MI test still needs the GALAXY-side a0(z) measured")
print("  independently (cross-scale) to confront it. a0 ratio is footing-independent (Z cancels).")
print("EXIT 0")
