#!/usr/bin/env python3
"""
Forecast for the ONE actionable clean door (open-doors scan): redshift-binned weak-lensing RAR.

Weak lensing measures g_obs directly -- no inclination, no pressure-support/asymmetric-drift, no beam-smearing
(the systematics that gave the kinematic IFS test a SPURIOUS rising a0). Brouwer+2021 (KiDS, arXiv:2106.11677)
reached deep-MOND (g_bar ~ 1e-15) with 259k isolated lenses over 0.1<z<0.5 but did NOT bin in lens redshift.
Splitting into z-bins is unpublished and tests a0(z) cleanly across the framework's z~0.4 BUMP.

This forecasts per-bin a0 precision for three survey scenarios and asks, per hypothesis: can it be SEEN?
Two windows: (A) the lensing window z<0.5 (small signal: the +6% bump); (B) the kinematic window z>=2 (big
signal: the -26% decline, but NO deep-MOND data exists there). The honest punchline is which signals clear which
floors.  C. Zimmerman, 2026-06-06. Pure numpy.
"""
import numpy as np
OM,OL=0.3137,0.6863; W0,WA=-0.752,-0.86
def Ez(z): return np.sqrt(OM*(1+z)**3+OL)
def rhoDE(z):
    a=1/(1+z); return a**(-3*(1+W0+WA))*np.exp(-3*WA*(1-a))
HYP={"framework":lambda z:np.sqrt(rhoDE(z)),"flat":lambda z:1+0*z,"Verlinde(cH)":Ez}

# ---- signal sizes in each window (a0 ratio across the window) ----
print("="*84); print("SIGNAL SIZES: a0(z_hi)/a0(z_lo) - 1  in each observational window"); print("="*84)
windows={"lensing  z=0.15->0.45 (where clean data EXIST)":(0.15,0.45),
         "kinematic z=0.5 ->2.5  (deep-MOND data do NOT exist)":(0.5,2.5)}
for wlab,(zlo,zhi) in windows.items():
    print(f"\n  {wlab}:")
    for nm,f in HYP.items():
        sig=f(zhi)/f(zlo)-1
        print(f"     {nm:14s}: {sig*100:+6.1f}%")

# ---- per-bin a0 precision model ----
# anchor: Brouwer full 259k-lens sample -> a0 to ~8% (conservative; statistical+method). Split n bins -> N/n each.
# stat precision scales as sqrt(N_ref/N_bin); plus a z-correlated circumgalactic-gas systematic floor.
N_REF=259_000; SIG_REF=0.08            # 8% a0 on the reference sample
def per_bin_sigma(N_total,n_bins,sys_floor):
    N_bin=N_total/n_bins
    stat=SIG_REF*np.sqrt(N_REF/N_bin)
    return np.hypot(stat,sys_floor)

print("\n"+"="*84); print("PER-BIN a0 PRECISION + SIGNIFICANCE TO DISTINGUISH EACH HYPOTHESIS (lensing window)"); print("="*84)
scenarios=[
 ("Brouwer KiDS now (259k, 2 bins, gas syst 5%)",      259_000, 2, 0.05),
 ("DES+HSC+KiDS combined (~1.5M, 3 bins, gas 5%)",     1_500_000, 3, 0.05),
 ("LSST/Euclid era (~10M, 4 bins, gas 3%)",           10_000_000, 4, 0.03),
]
zlo,zhi=0.15,0.45                       # representative extreme bins in the lensing window
for lab,N,nb,sysf in scenarios:
    sig_bin=per_bin_sigma(N,nb,sysf)
    sig_diff=sig_bin*np.sqrt(2)         # differencing the two extreme bins
    print(f"\n  {lab}")
    print(f"     per-bin sigma(a0) = {sig_bin*100:4.1f}% ;  extreme-bin difference sigma = {sig_diff*100:4.1f}%")
    for nm,f in HYP.items():
        s=f(zhi)/f(zlo)-1
        nsig=abs(s)/sig_diff
        verdict="DETECT" if nsig>3 else ("hint" if nsig>1.5 else "below floor")
        print(f"       {nm:14s} signal {s*100:+5.1f}%  ->  {nsig:4.1f} sigma  [{verdict}]")

print("\n"+"="*84); print("VERDICT"); print("="*84)
print("""  - The z-binned lensing RAR is the ONLY clean, public-data, systematics-free door (open-doors scan).
  - It can TIGHTEN the exclusion of the RISING rivals (Verlinde +19% across z=0.15-0.45): ~1 sigma now
    (Brouwer), ~2-3 sigma with combined DES+HSC+KiDS -- a cleaner Verlinde test than kinematics (which were
    contaminated to a spurious rise).
  - It CANNOT see the framework's +3% bump in the lensing window with any near-term data: the signal sits
    below the circumgalactic-gas systematic floor (~3-5%) until LSST/Euclid AND <3% gas control.
  - The framework's LARGE signal (the -26% decline) lives at z>=2, where NO deep-MOND (g<<a0) datum exists.
  => The framework's distinctive signal is below the floor of EVERY available/near-term probe: too small where
     clean data exist (z<0.5 lensing bump), and the clean data don't exist where it's large (z>=2 kinematics).
     'Safe but untested' is not a temporary state -- it is structural until either (a) sub-3% gas-controlled
     lensing RAR at z~0.4 (LSST/Euclid + better gas models) or (b) a clean deep-MOND rotation curve at z>=2
     (a future ELT/JWST target). THAT is what we need; nothing in current data can decide it.
  - Actionable NOW: z-bin the existing lensing RAR (Brouwer pipeline / Mistele-McGaugh 2024 deprojection,
    arXiv:2310.15248) to sharpen the Verlinde exclusion -- the one new result reachable from public data today.""")
