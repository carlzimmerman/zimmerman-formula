#!/usr/bin/env python3
"""
LANE B -- QUASAR NUMBER-COUNT DIPOLE (Secrest+2021, ApJL 908:L51).

CatWISE 1.36M QSO kinematic dipole:  D_obs ~ 1.5e-2, DIRECTION CMB-consistent,
AMPLITUDE ~2x the Ellis-Baldwin prediction  D_EB = [2 + x(1+alpha)] beta.

Framework datum: the apex-locked signature is a DYNAMICAL RAR/lensing anisotropy of
fractional size ~(1/2) beta_cmb -- a DIFFERENT observable from a count-aberration
dipole. Question: is (1/2)beta_cmb anywhere near the ~0.7e-2 QSO EXCESS?
Both footings: (1/2)beta_cmb is a0-INDEPENDENT, so both footings give the SAME number.
"""
import numpy as np

c        = 299792.458            # km/s
v_cmb    = 369.82                # km/s (Planck solar dipole)
beta_cmb = v_cmb/c               # 1.233e-3

# Ellis-Baldwin expectation for CatWISE QSO (Secrest values)
x, alpha = 1.7, 1.0              # count slope & spectral index
D_EB   = (2.0 + x*(1.0+alpha))*beta_cmb
D_obs  = 1.54e-2                 # Secrest 2021 measured
D_exc  = D_obs - D_EB            # the excess to be explained

# Framework apex dipole (a0-INDEPENDENT -> identical both footings)
D_frame = 0.5*beta_cmb

print("="*68)
print("LANE B -- FRAMEWORK APEX DIPOLE vs SECREST QUASAR EXCESS")
print("="*68)
print(f"beta_cmb = v_cmb/c            = {beta_cmb:.3e}")
print(f"D_EB  = [2+x(1+a)]beta (x={x},a={alpha}) = {D_EB:.3e}")
print(f"D_obs (Secrest 2021)         = {D_obs:.3e}")
print(f"D_excess = D_obs - D_EB      = {D_exc:.3e}")
print("-"*68)
print(f"Framework apex dipole (1/2)beta_cmb = {D_frame:.3e}   (a0-independent)")
print(f"  canonical a0 footing: {D_frame:.3e}")
print(f"  alt      a0 footing: {D_frame:.3e}   (IDENTICAL -- kinematic, not a0-set)")
print("-"*68)
print(f"D_frame / D_excess = {D_frame/D_exc:.3f}   "
      f"(framework is ~{D_exc/D_frame:.0f}x too small)")
print(f"D_frame / D_obs    = {D_frame/D_obs:.4f}")
print()
print("Even if the framework RAR/lensing anisotropy fed directly into a count")
print("dipole (it does NOT -- different observable), it would supply only")
print(f"~{100*D_frame/D_exc:.1f}% of the excess. VERDICT: framework-NEGLIGIBLE.")
print("The real shared datum is DIRECTION: framework apex == CMB apex == QSO dipole")
print("direction. Amplitude of the Secrest excess is NOT a framework prediction.")
print("\nDONE (exit 0).")
