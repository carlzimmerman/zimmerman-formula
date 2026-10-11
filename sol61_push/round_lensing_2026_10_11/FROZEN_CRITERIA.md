# Positive round-halo lensing relaxation: frozen contract

2026-10-11. Base 6fa743883. Commit this file ALONE before any solver run.
Source discovery acquired the author's small V1 README, gold catalogue,
parameter metadata and spectroscopic member catalogue. No lens fit was run.
Never import the author's fitted halo masses, profiles or mass maps.

Question: do arbitrary nonnegative CIRCULAR projected mass profiles at the
observed principal galaxy centres reproduce the gold image-position constraints?
This is a necessary-condition relaxation of a specified round-halo geometry,
NOT the fixed repaired-kernel prediction, an action, or a theory verdict.
Allowing arbitrary radial profiles is for bounds only, not a proposed new knob.
Positive spherical 3D profiles are a subset; projected positivity is weaker.

Use the prior verified 135 gold rows/49 features and Helmert operator. Cross-check
all gold IDs, sky positions (1e-6 degree tolerance), zsys against the newly fetched
author catalogue. Positions of BCG1/2/3 are member IDs 1/3/4; G5/9/10 are IDs
5/9/10. Fix TWO geometries before solving: three BCG centres; six centres including
G5/9/10. Verify relative west/north BCG2/3 offsets against Table 6 to .15 arcsec.
No centre optimization; no post-hoc galaxy selection. Other members and gas are
not represented independently in this relaxed-total-mass test; any miss is
limited to the chosen geometry and is not a complete framework exclusion.

For each centre sort all distinct observed image radii. The variables are
nonnegative increments of projected enclosed mass between these radii. At the
sample points this is an EXACT finite representation of arbitrary nonnegative
circular projected density, not a sampled radius grid. Prove the representation
by placing each increment in the intervening open annulus. Report mass in angular
deflection units; do not turn it into a cold-mass estimate without baryon and
distance accounting. Equality at a repeated radius shares one enclosed mass.

Use two FIXED background scenarios, never merge their results:
(1) the existing native PM flat-background values h=.6736,
Omega_m=(.02237+.1200)/h^2; (2) the author's reference h=.70, Omega_m=.30,
labelled external-context geometry only. In both integrate E(z)^-1 for flat
matter+constant-dark-energy backgrounds to get w=1-chi(.296)/chi(zsys).
No halo mass function, growth model, external lens mass, or MOND shortcut.
This is not a test of evolving dark energy or either a0 footing. A0/kernel
constraints have deliberately been relaxed for this necessary-condition test.

For A*x-b = H*(w*a_hat-theta), solve LP min t with x>=0,t>=0 and
|A*x-b|<=t. Then min sum(x) subject to residual<=t_min+1e-7 arcsec (numerical
tie-breaking tolerance, NOT observational acceptance). Report t_min, mass,
residual, dual bound and feasibility tolerances; no ALLOWED/EXCLUDED labels.
LP primal/dual checks require residual violation <=1e-6 arcsec, dual column
violation <=1e-7 and primal/dual gap <=1e-6*max(1,t). These are numerical checks,
not a rigorous interval certificate. Preserve failures. Require invariance of
optimal t under reversing image order after consistent operator rebuilding
(absolute 1e-6 arcsec). Run with fixed HiGHS tolerances 1e-9 and 1e-10 as refinement.

Controls: exact positive annulus realization at all sampled radii to 1e-10;
two-image point lens (unit source efficiency .7, true angular mass 1.2) has zero
minimum residual and minimum total mass 1.2 to 1e-7; positive point-lens images
at three source efficiencies also feasible; deliberate negative-deflection-sign
and omitted-efficiency MUTATE errors rejected by direct known-mass residual
>0.1 arcsec. Distances independently recomputed at tighter quadrature tolerance
must agree to 1e-10. Validate finite distinct radii/noncentral samples.

One numerical process/thread, dense arrays below 1000x1000, wall cap 90 seconds,
CPU cap 60 seconds; no PM simulation. Record source URLs/hashes, source selection,
software, code hashes, output, mathematical assumptions and the exact relaxation.
Use only this folder and read-only prior sources. Kappa remains fitted and
sealed predictions remain untouched. The original full goal remains open.
