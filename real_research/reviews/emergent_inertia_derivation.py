#!/usr/bin/env python3
"""
Emergent inertia from the cosmic horizon -- how far does it actually close?
==========================================================================
Goal: derive a0=(c/2)sqrt(G rho) (the free-fall-horizon surface gravity) from a
foundation -- inertia/MOND emerging from the cosmic gravitational horizon -- so that
the form, and ideally the coefficient, become CONSEQUENCES rather than posits.
We work the two real routes exactly and report honestly what each forces.
  Route A: Machian / Sciama inertia (inertia = gravitational coupling to all matter).
  Route B: Unruh / horizon thermodynamics (MOND onset = Unruh ~ horizon temperature).
Labels: [EXACT] proven; [GROUNDS] makes a choice physically natural; [POSIT] still free;
        [OPEN] unsolved even for the experts.
"""
import numpy as np

c, G, hbar, kB, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 3.0857e22
H0 = 67.4e3/Mpc
rho = 3*H0**2/(8*np.pi*G)            # critical density
RH  = c/H0                           # Hubble radius
Rff = c/np.sqrt(G*rho)               # free-fall horizon
A0F = 0.5*c*np.sqrt(G*rho)           # framework a0

print("="*84)
print("ROUTE A -- Machian / Sciama inertia (Sciama 1953; Brans-Dicke)")
print("="*84)
# Sciama: the inertial reaction on an accelerated body is the gravitational pull of the
# rest of the universe; consistency requires the universe's potential Phi ~ c^2.
M_H  = (4/3)*np.pi*RH**3*rho
Phi_over_c2 = G*M_H/(RH*c**2)
print(f"  Hubble sphere:  M_H=(4/3)pi R_H^3 rho_c = {M_H/2e30:.2e} Msun")
print(f"  Machian potential of the Hubble sphere:")
print(f"     G M_H/(R_H c^2) = {Phi_over_c2:.4f}   ->  EXACTLY 1/2 for rho=rho_crit  [EXACT]")
print(f"     (=> Phi_universe = c^2/2: the observable universe is 'half-Machian-closed';")
print(f"      this is the well-known GM/Rc^2 ~ 1 flatness/Mach coincidence, here exact.)")
# The radius where the gravitational potential of the medium reaches ~c^2:
# uniform sphere center potential |Phi|=2 pi G rho R^2; set =c^2/2 (the Machian value):
R_mach = np.sqrt(c**2/(4*np.pi*G*rho))
print(f"\n  Machian radius (where |Phi(center)|=2pi G rho R^2 equals c^2/2):")
print(f"     R_mach = c/sqrt(4 pi G rho) = {R_mach:.3e} m;  R_ff = c/sqrt(Grho) = {Rff:.3e} m")
print(f"     R_mach/R_ff = {R_mach/Rff:.3f} = 1/sqrt(4pi) = {1/np.sqrt(4*np.pi):.3f}")
print(f"""  [GROUNDS] Machian inertia makes the GRAVITATIONAL rate sqrt(G rho) -- not the
  expansion rate H -- the natural clock: inertia is the back-reaction of the matter that
  GRAVITATES, which acts at sqrt(G rho). So a0 ~ c sqrt(G rho) is grounded, and a0 ~ cH
  follows only because H ~ sqrt(G rho) at criticality. [GROUNDS the form + the sqrt(Grho) choice]
  [POSIT] but the O(1) is convention-dependent (R_mach has 1/sqrt(4pi), the free-fall horizon
  has 1, surface gravity inserts a further 1/2): Mach fixes the SCALE, not the coefficient.""")

print("\n"+"="*84)
print("ROUTE B -- Unruh / horizon thermodynamics (Milgrom 1999; Verlinde 2011)")
print("="*84)
# Unruh temperature of an accelerated particle vs the cosmic-horizon temperature.
def T_unruh(a): return hbar*a/(2*np.pi*c*kB)
def T_hor(rate): return hbar*rate/(2*np.pi*kB)     # horizon temperature for a 'rate' [1/s]
# MOND onset where the particle's Unruh temperature ~ the horizon temperature:
#   T_unruh(a0) = T_hor(rate)  ->  a0/c = rate  ->  a0 = c*rate.
for name, rate in [("expansion rate H (de Sitter horizon)", H0),
                   ("free-fall rate sqrt(G rho) (Machian)", np.sqrt(G*rho))]:
    a0 = c*rate
    Z = c*H0/a0
    print(f"  T_unruh(a0)=T_hor({name.split()[0]}):  a0 = c*rate = {a0:.2e} m/s^2  -> Z={Z:.2f}")
print(f"""  [GROUNDS the evolution] Whatever the rate, a0 ~ c*rate ∝ sqrt(G rho_cosmic) ∝ E(z):
  the REDSHIFT LAW a0(z)=a0(0)E(z) drops out of horizon thermodynamics independent of the
  O(1). That is the robust, falsifiable content -- and it is derived here, not posited.
  [POSIT] the coefficient: simple matching gives Z=1; Milgrom's careful deep-MOND/Unruh
  matching gives Z=2pi; Verlinde's entropy gives Z~6; the framework's surface-gravity
  reading gives Z=2sqrt(8pi/3)=5.79. All O(1), all data-allowed, none forced.""")

print("\n"+"="*84)
print("HONEST LEDGER -- what the foundation closes, and what it does not")
print("="*84)
print(f"""  [EXACT]   the Machian coincidence G M_H/(R_H c^2) = 1/2 for rho=rho_crit -- the
            observable universe's gravitational potential is c^2/2. Real, and the only
            place a clean, non-convention '1/2' actually appears.
  [GROUNDS] inertia-from-matter (Mach) makes sqrt(G rho) the natural rate (vs H); horizon
            thermodynamics makes a0 ~ c*rate. Together they GROUND the FORM a0~c sqrt(Grho)
            and, robustly, the EVOLUTION a0(z)=a0(0)E(z) -- the falsifiable claim is derived.
  [POSIT]   the exact coefficient Z. The Machian '1/2' (potential) and the surface-gravity
            '1/2' (c^2/2R) are NOT shown to be the same 1/2; bridging them is the open step.
  [OPEN]    a COMPLETE modified-inertia theory. Milgrom himself (1994,2011) showed modified
            inertia is only defined for trajectories with a fixed frequency (closed orbits);
            no consistent equation of motion for general acceleration exists yet. So 'inertia
            from the horizon' is an unfinished program for the experts, not just for us.

  BOTTOM LINE: the foundation genuinely DEEPENS the theory -- the FORM and the EVOLUTION are
  grounded (Mach + Unruh), and the GM/Rc^2=1/2 coincidence is exact -- but it does NOT close
  the coefficient, and a full emergent-inertia dynamics remains open even in the literature.
  The honest gain: a0=(c/2)sqrt(Grho) is now 'the surface gravity of the Machian free-fall
  horizon', with the sqrt(Grho) GROUNDED and only the 1/2 left as the (shared, universal) posit.""")
print("="*84)
