#!/usr/bin/env python3
"""
The cleanest form: a0 as the surface gravity of the gravitational free-fall horizon.
===================================================================================
Earlier I split Z=2sqrt(8pi/3) into 'sqrt(8pi/3) (Friedmann, exact) + a loose factor 2'.
That is two posits. Here both collapse into ONE physical statement, which is cleaner and
is the right thing to put in a paper.

ONE PRINCIPLE:
   a0 is the surface gravity of the horizon at the gravitational free-fall radius R_*,
        R_* = c / sqrt(G rho)   (the distance light travels in one free-fall time t_ff=1/sqrt(Grho);
                                 equivalently the radius where t_freefall = t_lightcross --
                                 the causal scale of gravitational collapse),
   and the surface gravity of a horizon at radius R is the exact Schwarzschild value
        kappa = c^2 / (2 R).
Then
   a0 = c^2/(2 R_*) = c^2/(2 c/sqrt(Grho)) = (c/2) sqrt(G rho) = c H / [2 sqrt(8pi/3)].
Both factors of Z come from ONE object: the 1/2 is the horizon surface-gravity factor,
the sqrt(8pi/3) is R_* expressed through Friedmann. No separate loose '2'.
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0 = 67.4e3/Mpc
rho = 3*H0**2/(8*np.pi*G)

# the single principle, computed
R_star = c/np.sqrt(G*rho)               # free-fall horizon radius
a0     = c**2/(2*R_star)                # surface gravity there
Z      = c*H0/a0

print("="*82)
print("ONE-PRINCIPLE DERIVATION: a0 = surface gravity at the free-fall horizon")
print("="*82)
print(f"  free-fall rate     sqrt(G rho)      = {np.sqrt(G*rho):.3e} 1/s   (t_ff = {1/np.sqrt(G*rho):.2e} s)")
print(f"  free-fall horizon  R_* = c/sqrt(Grho)= {R_star:.3e} m = {R_star/Mpc/1e3:.1f} Gpc")
print(f"  Hubble radius      R_H = c/H0        = {c/H0:.3e} m = {c/H0/Mpc/1e3:.1f} Gpc")
print(f"     -> R_* / R_H = {R_star/(c/H0):.3f} = sqrt(8pi/3) = {np.sqrt(8*np.pi/3):.3f}  (Friedmann)")
print(f"  surface gravity    a0 = c^2/(2 R_*)  = {a0:.3e} m/s^2   (observed a0 ~ 1.2e-10)")
print(f"  => Z = c H0 / a0   = {Z:.3f}        target 2 sqrt(8pi/3) = {2*np.sqrt(8*np.pi/3):.3f}  MATCH")

print("\n"+"="*82)
print("WHY THIS IS CLEANER (and what is still a posit)")
print("="*82)
print(f"""  * It is ONE object, not two factors. The 1/2 is no longer a loose coefficient -- it is
    the SAME 1/2 that appears in every horizon's surface gravity kappa=c^2/2R (Schwarzschild
    R_s=2GM/c^2, Rindler, etc.). The sqrt(8pi/3) is just R_* written through Friedmann.
  * It connects to known MOND lore: R_* is where the dynamical (free-fall) time equals the
    light-crossing time, i.e. a0 is the acceleration at which a system's dynamical time
    reaches the cosmic causal time -- Milgrom's 'a0 ~ where t_dyn ~ t_cosmic' observation,
    made exact with the free-fall rate sqrt(G rho).
  * CONTRAST that fixes the value: the SAME construction at the HUBBLE horizon (R_H, the
    EXPANSION scale) gives a0 = c^2/(2 R_H) = cH/2, i.e. Z=2 -- ruled out 2.7x. The framework
    picks the GRAVITATIONAL free-fall horizon (R_*=sqrt(8pi/3) R_H, the COLLAPSE scale), not
    the expansion horizon, because a0 is a gravitational acceleration. That single choice --
    collapse horizon, not expansion horizon -- IS the physical content, and it is one clean
    statement instead of a scattered factor.

  THE REMAINING POSIT (stated honestly): 'a0 = the surface gravity of the gravitational
  free-fall horizon.' That is a physical principle, not a theorem -- exactly the level at
  which Milgrom posits a0~cH/2pi (Unruh) and Verlinde posits a0~cH/6 (entropy). It is now a
  SINGLE assumption from which BOTH factors of Z follow, which is the cleanest honest form.
  The data still cannot distinguish 5.79 from 6 or 2pi (Z in ~[5.5,6.5]); this derivation
  wins on PARSIMONY and physical transparency, not on a measurement.

  PAPER-READY STATEMENT:
     a0 = c^2/(2 R_*),   R_* = c/sqrt(G rho)   (free-fall horizon)
        = (c/2) sqrt(G rho) = c H(z) / [2 sqrt(8pi/3)],
     'the surface gravity of the cosmic gravitational free-fall horizon'.""")
print("="*82)
