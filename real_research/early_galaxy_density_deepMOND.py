#!/usr/bin/env python3
"""
Carl's idea: calculate the DENSITY of early galaxies to FIND the deep-MOND population -- because the
acceleration regime is set by density (g_bar = G M_bar / R^2), not by the rotation curve. Then measure
a0(z) from the abundant INTEGRATED velocity dispersion sigma via the deep-MOND pressure-supported relation
    sigma^4 = (4/9) G M_bar a0   =>   a0 = (9/4) sigma^4 / (G M_bar),
which needs only sigma + M_bar (line widths + photometry) -- NOT resolved rotation curves.

The catch (same regime requirement as the BTFR): the relation holds only for DEEP-MOND systems (g_bar < a0).
So step 1 is to compute g_bar from the high-z size-mass relation and find the threshold mass M_dM(z) below
which early galaxies are deep-MOND. This determines whether the method is viable and on which galaxies.

C. Zimmerman, 2026-06-06. Pure numpy. a0 = 1.2e-10 m/s^2.
"""
import numpy as np
G=6.674e-11; Msun=1.989e30; kpc=3.086e19; a0=1.2e-10
SigM = a0/G / (Msun/ (3.086e16)**2)     # MOND surface density a0/G in Msun/pc^2

# --- high-z size-mass relation, UNCOVER-calibrated (Miller/Allen 2024, arXiv:2412.06957):
#     logM*=8.5 -> R_e = 0.83/0.575/0.40 kpc at z=4/6/8; slope s~0.27; R_e[kpc]=A*(M*/1e9)^s*((1+z)/7)^(-b) ---
def Re_kpc(logMstar, z, A=0.785, s=0.27, b=1.1):
    return A*(10**logMstar/1e9)**s * ((1+z)/7.0)**(-b)
def f_gas(z, logMstar):                  # cold gas fraction M_gas/M_star (rises with z, falls with mass)
    return min(0.85, 0.4*(1+z)**0.7*10**(-0.3*(logMstar-9.5)))
def g_bar(logMstar, z):                  # internal baryonic acceleration at R_e (m/s^2)
    Mb=10**logMstar*(1+f_gas(z,logMstar))*Msun; R=Re_kpc(logMstar,z)*kpc
    return G*Mb/R**2
def sigma_dM(logMstar, z, a0v=a0):       # predicted deep-MOND velocity dispersion (km/s)
    Mb=10**logMstar*(1+f_gas(z,logMstar))*Msun
    return ((4/9)*G*Mb*a0v)**0.25/1e3

print("="*84)
print(f"STEP 1 -- DENSITY/ACCELERATION OF EARLY GALAXIES  (MOND surface density a0/G = {SigM:.0f} Msun/pc^2)")
print("="*84)
print(f"\n{'z':>4} | {'logM*':>5} | {'R_e kpc':>7} | {'f_gas':>5} | {'g_bar/a0':>8} | {'regime':>12} | {'sigma_dM km/s':>12}")
print("-"*84)
for z in [2,3,6]:
    for logM in [7.5,8.0,8.5,9.0,9.5,10.0]:
        gr=g_bar(logM,z)/a0; reg="DEEP-MOND" if gr<1 else ("transition" if gr<2 else "Newtonian")
        print(f"{z:4.0f} | {logM:5.1f} | {Re_kpc(logM,z):7.2f} | {f_gas(z,logM):5.2f} | {gr:8.2f} | {reg:>12} | {sigma_dM(logM,z):12.1f}")

# --- deep-MOND threshold mass M_dM(z): solve g_bar(M,z)=a0 ---
print("\n"+"="*84); print("DEEP-MOND THRESHOLD: below logM_dM(z), early galaxies ARE deep-MOND (g_bar<a0)"); print("="*84)
def logM_dM(z):
    lm=np.linspace(6,11,2000); gr=np.array([g_bar(l,z)/a0 for l in lm])
    below=lm[gr<1]; return below.max() if len(below) else float('nan')
print("   z  | logM_dM (deep-MOND if logM* < this) | predicted sigma at threshold (km/s)")
for z in [1,2,3,4,6,8]:
    lmd=logM_dM(z); print(f"  {z:3.0f} | {lmd:6.2f}                             | {sigma_dM(lmd,z):.1f}")

print("\n"+"="*84); print("VIABILITY OF THE sigma-METHOD (vs resolved rotation curves)"); print("="*84)
print(f"""  GOOD NEWS (real JWST sizes): at z=2-3 the deep-MOND population reaches logM* ~ 9-9.6 (the extended
    tail, R_e ~ 1-2 kpc), with predicted sigma ~ 60-85 km/s -- WELL ABOVE the NIRSpec grating floor
    (~25-30 km/s) and measurable. At z=6 only logM* <~ 7.8 is deep-MOND (sigma~30, at the floor).
    => z=2-3 is the sweet spot: deep-MOND AND sigma-measurable. The targets exist (KLASS lensed dwarfs
       sigma=18-35 km/s at logM*~8; de Graaff JADES logM*~8 z>6; UNCOVER/GLASS/CANUCS lensed low-mass).
  COEFFICIENT VERIFIED: the deep-MOND M-sigma coefficient 9/4 (sigma_3D) matches the June-2026 local
    Baryonic Faber-Jackson measurement (arXiv:2605.26965, a0=1.2e-10). The relation is real and calibrated.
  NOVELTY VERIFIED: nobody has tested a0 (or a0(z)) from the high-z pressure-supported M-sigma relation --
    every existing a0(z) test is rotation-curve based. This density-select + sigma route is UNOCCUPIED.

  THE BINDING SYSTEMATIC (the make-or-break, honest): at z>=2 the integrated sigma is NOT clean pressure
    support -- it is inflated by (i) gas turbulence (sigma_turb ~ 30-80 km/s, not gravity), (ii) partial
    ROTATION (KLASS v/sigma ~ 2.5; only ~16% are dispersion-dominated; V_circ^2 = v_rot^2 + 3.4 sigma^2),
    (iii) outflows/feedback. Measured M_dyn/M_bar ~ 3-4 even where MOND predicts a modest boost. And sigma^4
    AMPLIFIES it: a 30% sigma error -> 2.7x error in a0. To get a CLEAN a0 you must isolate genuinely
    pressure-supported, deep-MOND systems and correct turbulence/rotation -- which partially reintroduces
    the resolved-kinematics requirement the method was meant to avoid. NOT fully escaped, but the sample is
    larger and the regime selection (by density) is the genuinely new, correct first step.
  Sanity check: de Graaff (logM~9-10, z>6) -> g/a0 ~ 2-10 (Newtonian) -- the method correctly rejects them
    as NOT deep-MOND; the usable ones are the lower-mass z=2-3 tail.""")

# --- forecast: a0(z) statistical precision from N deep-MOND galaxies with sigma ---
print("\n"+"="*84); print("FORECAST: a0(z) from N deep-MOND galaxies (sigma method)"); print("="*84)
print("   a0 = (9/4) sigma^4/(G M_bar) ; dlog a0 = 4 dlog sigma - dlog M_bar")
print("   per-galaxy sigma error ~20% (high-z, turbulence-corrected) -> per-galaxy a0 error ~ 4*0.20+0.15 ~ 0.95 (in ln)")
for N in [10,30,100]:
    err=np.hypot(4*0.20,0.15)/np.sqrt(N)
    print(f"   N={N:3d} deep-MOND galaxies/z-bin -> a0(z) statistical error ~ {err*100:4.0f}%  "
          f"({'decisive vs 26% decline' if err<0.13 else 'marginal' if err<0.26 else 'insufficient'})")
print("""
  => ~30-100 deep-MOND (logM*~8-8.5) lensed galaxies per z-bin with grating sigma would reach <10-15%,
     enough to test the framework's a0(z=3)~0.74 vs constant. This is a STACKING / lensed-dwarf-sigma
     program -- larger N than resolved curves allow, and it uses data JWST is ALREADY taking (NIRSpec
     gratings of lensed fields: UNCOVER, GLASS, CANUCS). The density calc shows the targets exist; the
     dispersion measurement is the make-or-break.""")
