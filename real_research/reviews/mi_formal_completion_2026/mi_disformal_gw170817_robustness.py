#!/usr/bin/env python3
"""
IS THE GW170817 EXCLUSION OF THE DISFORMAL LENSING ROUTE ROBUST, OR WITHIN MEASUREMENT
VARIABILITY? Verify-the-deficit-as-hard-as-a-win: re-derive PROFILE-INDEPENDENTLY, test
every escape route, and compare against the actual measurement + its variability budget.
"""
import numpy as np
c=2.998e8; kpc=3.086e19; Mpc=1e3*kpc; G=6.674e-11; Msun=1.989e30; a0=9.36e-11

print("="*76)
print("(1) THE MEASUREMENT + ITS VARIABILITY BUDGET (what 'within variability' means)")
print("="*76)
print(""" GW170817/GRB170817A: gamma-rays observed +1.74 +/- 0.05 s AFTER the GW merger.
 The variability budget is the INTRINSIC emission delay of the GRB, generously
 0..+10 s (some analyses allow ~100 s). So ANY photon-vs-graviton propagation
 lag must satisfy  Delta_t  <~  seconds-to-minutes.  That's the bar.""")

print("="*76)
print("(2) PROFILE-INDEPENDENT DELAY: deflection and delay are TIED (cannot decouple)")
print("="*76)
# The disformal route needs photons to lens like nu*M_bar, i.e. light must feel the extra
# potential dPhi = Phi_MOND - Phi_bar ~ v_f^2 ln(r) in the halo. Deflection = transverse
# gradient of (2 dPhi/c^2) along the ray; delay = the SAME quantity integrated un-differentiated:
#   Delta_t = INT (2 dPhi/c^2) dl / c.   A potential with gradients ON the ray is nonzero ON the ray.
M=1e11*Msun
vf=(G*M*a0)**0.25                       # BTFR flat velocity of the host
twoPhi=2*vf**2/c**2                     # 2 dPhi/c^2 scale (log potential amplitude)
print(f" host (M_bar=1e11 Msun): v_flat={vf/1e3:.0f} km/s ->  2*dPhi/c^2 ~ {twoPhi:.2e}")
for L_kpc in (10,30,100,300):
    dt=twoPhi*(L_kpc*kpc)/c
    print(f"   MOND-region path L={L_kpc:>3d} kpc  ->  Delta_t ~ {dt:.2e} s  (~{dt/86400:.1f} days)")
print(""" Even the ABSOLUTE MINIMUM (10 kpc of MOND shell, one galaxy, ignore the Milky Way)
 gives ~ a week. Realistic (host+MW, 100-300 kpc of log potential) gives months-years.
 [Pre-registered in the literature: Kahya & Desai 2016 predicted ~800 days for this
 theory class; Boran, Desai, Kahya & Woodard PRD 97, 041501 (2018): 'GW170817
 falsifies dark matter emulators' -- the exact class: photons feel a deeper effective
 potential than the metric gravitons propagate in.]""")

print("="*76)
print("(3) EXCLUSION MARGIN vs THE VARIABILITY BUDGET")
print("="*76)
dt_min=twoPhi*(10*kpc)/c; dt_real=twoPhi*(150*kpc)/c
for name,dt in (("minimum (10 kpc, one halo)",dt_min),("realistic (host+MW ~150 kpc)",dt_real)):
    print(f"  {name}: Delta_t/{10}s-budget = {dt/10:.1e}x   {'EXCLUDED' if dt>100 else 'ok'}")
print("  -> 5 to 7 ORDERS over budget. Measurement variability is seconds; the signal is months.")

print("="*76)
print("(4) ESCAPE ROUTES, each tested and closed")
print("="*76)
print(""" (a) 'Put gravitons on g~ too' (both cones equal -> no relative delay): then the
     spin-2 kinetic term is S_EH[g~], i.e. g~ IS the metric; Einstein eqs for g~ are
     sourced by baryons only -> the g~ potential is BARYONIC -> photons on g~ get
     baryonic lensing -> the under-lensing returns. The enhancement existed only as a
     RELATIVE tilt between photon and Einstein metrics; equalizing the cones erases it.
 (b) 'Gradient disformal g~ = g + C dPhi dPhi (bend without slowing)': deflection needs
     the potential nonzero ON the ray (a gradient of zero is zero) -> the Shapiro-type
     photon-graviton difference INT(2 dPhi/c^2) dl/c returns at the same order. Tied.
 (c) 'Shrink B': B is FIXED by matching the observed galaxy-galaxy lensing = dynamics
     (Brouwer 2021 / Mistele-McGaugh); shrinking B un-solves lensing. Tied by data.
 (d) 'Geometry luck': GW170817's photons exit the host halo (source offset ~2 kpc) and
     enter ours (the Sun sits at g_bar ~ 2 a0, inside the MW's MOND-affected region).
     Both crossings are unavoidable; the IGM (B->0) doesn't matter.
 (e) 'Sign flip' (B<0, photons fast): superluminal photons vs g -- acausal, and a GRB
     ARRIVING BEFORE the GW is equally unobserved.
 THE ONLY genuine escape: put the enhancement IN the metric both photons and gravitons
 see = modified GRAVITY with c_GW=c (this is literally why Skordis-Zlosnik built AeST
 the way they did, post-GW170817) -- i.e. the MG limb, not photon-only disformal MI.""")

print("="*76)
print("VERDICT: the exclusion is REAL and ROBUST. Not within measurement variability")
print("(budget: seconds; signal: months; margin: 5-7 orders, profile-independent, all")
print("escape routes closed). The disformal photon-only lensing route is dead; the")
print("walk-back stands. We did NOT solve lensing.")
