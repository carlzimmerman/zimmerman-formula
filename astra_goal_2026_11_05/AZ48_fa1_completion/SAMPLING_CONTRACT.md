# AZ48 sampling details — before field-selector results

This implements FROZEN_BULLET.md, without changing any physical or numerical
gate. No Bullet selector has yet been sampled from the new3D field.
Kappa=1/2 FITTED; not theory closed. Retired sector, adopts nothing.

Compute the six physical-coordinate Hessian components on interior nodes.
Trilinearly interpolate those components to requested locations, then form
the invariant s. Do not extrapolate beyond interior nodes, interpolate
potential values as if they were Hessians, clip s, or assume axisymmetry.
Record Hessian norm and a roundoff diagnostic at each sampled point: flag
norm<=64*machine_epsilon*maximum interior Hessian norm. This flags tiny
ratios relative to the field scale; it does not bound discretization error.
A zero maximum norm flags all samples. Flagged/nonfinite samples are
numerically ineligible, without silently replacing them by valid zeroes.

The100kpc z=0 discs use equal-area radial midpoints
r=100*sqrt((j+1/2)/nr), angular midpoints theta=2*pi*(k+1/2)/ntheta,
and equal weights1/(nr*ntheta). Use32x64 and64x128 exactly as frozen.
Report mean s, on-fraction(s>=s_c), mean-s>=s_c, minimum norm and number
of roundoff flags. The existing0.01 quadrature line applies to mean s and
on-fraction; mean-s threshold flags must agree. Across field resolutions,
use the already frozen0.02 point and0.03 disc lines and unchanged flags.

Read the two inherited thresholds from I6's i6_results.json xcop/footings:
these are data-calibrated values, not new native measurements or parameters
derived from the action. Record that file's hash. The point diagnostic is
WRONG SIGN if either gas point is on while its associated BCG is off;
otherwise WEIGHT ALLOWED AT GALAXIES if both BCGs are on, else NO SIGN.
These conditional readings never override incomplete numerical eligibility.
Report s_c<=min(s_BCG1,s_BCG3) and any nonempty wrong-sign intervals
(s_BCG1,s_GASM] and(s_BCG3,s_GASB] without adjusting a threshold.

For the centred-Plummer oracle, sample r/a=0.3,0.5,1,2,5 along six signed
coordinate axes and eight signed cube diagonals normalized to unit length:
70 samples per footing/grid. Compute the oracle directly from radial and
tangential Hessian eigenvalues, independently of Cartesian interpolation.
Compare exact values and inherited-threshold flags at the frozen0.02 line.
The N32/N64/N128 field ladder remains mandatory before production grading.

Known answers: constant rotated quadratic fields preserve Hessian and
selector under sampling; constant isotropic fields have s=1 and full disc
on-fraction at inherited thresholds; equal-area quadrature reproduces the
constant and r^2 disc averages to1e-12 relative. Mixed/planar and outside-
domain controls must be handled explicitly. The separate sign mutation
must fail the isotropic selector known answer. These are implementation
checks, not substitutes for physical field convergence.
