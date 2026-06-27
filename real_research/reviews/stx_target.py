#!/usr/bin/env python3
"""The s^TX boost-dipole target of de Sitter-Unruh modified inertia (reproducible).
Preferred frame = the cosmic (CMB) rest frame -> a forced gravity-sector SME s^TX dipole at the CMB apex.
Magnitude inherits the banked a0->s_munu component ledger (Saturn channel); direction + CPT-even are robust."""
import math
c=299792.458                 # km/s
v=369.82                     # km/s, Solar-System velocity vs the CMB (Planck dipole)
beta=v/c
sTX_pred=8.68e-10            # framework prediction (banked SME component ledger, Saturn)
bound_now=1.3e-9            # tightest published gravity-sector bound (Hees+ 2015, ephemerides)
print(f"beta = v/c = {beta:.4e}   (v={v} km/s toward CMB apex l,b=264.0,48.3 deg)")
print(f"predicted s^TX = {sTX_pred:.2e} (CPT-even, fixed direction = CMB apex)")
print(f"current bound  = {bound_now:.1e}  ->  margin = {bound_now/sTX_pred:.2f}x under")
print(f"decisive: a dedicated s^TX fit reaching sigma~{sTX_pred/2:.1e} detects or excludes it")
print(f"footing: a0=9.36e-11 m/s^2, Z=sqrt(32pi/3)=5.789; analysis-limited, not data-limited")
