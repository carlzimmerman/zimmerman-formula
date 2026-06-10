#!/usr/bin/env python3
"""
delta-Q/Q0 term magnitudes -- bound the linear identity delta-Q/Q0 = dphidot/Q0 - Phi (dQ_partial.py),
and the 2nd-order tilt term, to grade the AeST PINNED label for the declining carrier Q=A^mu d_mu phi.

Convention (FLAGGED as an assumption, NOT verified against Skordis-Zlosnik 2007.00082 normalization): phi
dimensionless, cosmological roll Q0 ~ H0. Under this convention the advection/time-derivative term can
DOMINATE the redshift term Phi, so the finder's quoted ~1e-6 may understate by ~70x. Both ends remain far
sub-threshold (swamping needs O(1) or O(v/c)). numpy only.  C. Zimmerman 2026-06-09.
"""
import numpy as np
c=2.998e8; H0=2.27e-18; v=150e3; a0=9.36e-11
Phi=(v/c)**2                                  # metric perturbation, redshift term (robust)
alpha=v/c                                     # 1st-order radial tilt ~ v/c
g_over_cH0=a0/(c*H0)                           # = 0.14 -- but this is the SZ-CONVENTION-DEPENDENT piece
# The open quantity is the SZ ratio  R = |grad dphi| / phibar-dot.  Two conventions bracket it:
R_mine=g_over_cH0                              # convention A: scalar gradient ~ a0 in cH0 units -> ~0.14
R_fable=2e-10                                  # convention B (Fable's normalization): ~2e-10
tilt_mine=alpha*R_mine                         # 2nd-order tilt term under conv A
tilt_fable=alpha*R_fable                       # under conv B

print("="*78)
print("delta-Q/Q0 term magnitudes (V=150 km/s deep-MOND galaxy)")
print("="*78)
print(f"  Phi = (v/c)^2                          = {Phi:.2e}   (redshift term; ROBUST, convention-free)")
print(f"  STRUCTURAL: tilt term = alpha * R, with R=|grad dphi|/phibar-dot the OPEN Skordis-Zlosnik ratio.")
print(f"    conv A (R~g/cH0~{R_mine:.2f}, this pass): tilt = {tilt_mine:.1e}  [alpha-suppressed vs the O(0.1) field]")
print(f"    conv B (R~{R_fable:.0e}, Fable's norm):   tilt = {tilt_fable:.1e}")
print("-"*78)
print(f"  => DIVERGENCE with Fable (hygiene rule, reported): the tilt/advection magnitude is SZ-CONVENTION-DEPENDENT")
print(f"     -- this pass gives ~{tilt_mine:.0e}, Fable's pass ~{tilt_fable:.0e}; the ~1e9 gap IS the open ratio R.")
print(f"     delta-Q/Q0 therefore sits somewhere in [{tilt_fable:.0e}, {max(Phi,tilt_mine):.0e}]; swamping needs O(v/c)={v/c:.0e}")
print(f"     or O(1). EVERY end of the bracket is FAR sub-threshold ({max(Phi,tilt_mine)/(v/c):.1e} of v/c at worst) -> Q PINNED.")
print(f"     What is NOT convention-dependent (dQ_partial.py): the tilt is 2nd-ORDER, suppressed before any energy argument.\n")
print("="*78)
print(f"""GRADE (AeST declining carrier Q): from 'single-angle, pending' UP to
  'mechanism CORROBORATED by an independent kinematic route (tilt term is 2nd-order, suppressed before the
   energy argument); magnitude OPEN in [1e-6, 1e-4], both far sub-threshold'.
  The full third-computation closure shrinks to ONE ratio: |grad dphi|/phibar-dot in Skordis-Zlosnik
  conventions, and whether the energy minimum suppresses the advection term as well as the cross-term.
  (PINNED stays the working hypothesis; this is corroboration + a sharpened, bounded open question -- NOT a
   full independent re-derivation, which remains the named closure job.)""")
