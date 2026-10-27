# LD-18: redo the decisive joint restoration test after numerical correction

LD-17 fixes gravity/W quadrature and restores the parent's stable W tail.
The bulk control now recovers the law without density comb, but the joint
front still has about.24dex error to30kpc and.34dex to50kpc. Redo n128
refinement and joint species-conserving perturbations ±1kpc with this corrected
energy. Save checkpoints every50 iterations and compare interpolated q=.5
radii, not crossing-cell indices. This supersedes LD-13's restoration numbers
for the current implementation; it does not erase their historical provenance.
Original stationarity, free-outer and full radial law diagnostics remain.
