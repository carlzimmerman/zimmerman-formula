# Self-review

Scope: REPORT.md and the two new numerical scripts. This is self-review, not
independent certification. Base research checkpoint is 2e20ebd591.

Exact claim: the stated reduced autonomous Hamiltonian conserves total energy
and bounds field excitation by H+B. Verdict: proved as written for the reduced
model. Dependencies are differentiation of H, the reciprocal d'(X)(A-1) force,
nonnegative orbital kinetic energy and Uorb>=-B. Removing the reciprocal force
invalidates the identity. The mutation explicitly tests its sign.

Conditional claim: the exterior continuum for a WKB excitation in a static
Einstein metric opens when N_in omega_in>=N_out omega_out. Verdict: conditional
on the stated static-metric, linear-excitation and WKB assumptions. The numerical
35-shell evaluation does not determine a trapped fraction or the actual lapse.
Angular barriers, interface bound states, nonlinear states and spatial gradients
are not excluded by this argument.

Finite claims: six autonomous controls, a 161-speed linear scan and the selected
100-period coupled run. Verdict: computationally verified only in these ranges.
The adaptive best-speed selection is disclosed and not interpreted as a physical
prediction. The original absolute convergence criterion is loose compared with
tiny seed energies; final small net orbital transfers are not claimed accurately
resolved. The selected resonant peak agrees to about 0.23% across tolerances.
A value sampled at the end of 100 periods is not an asymptotic retention result.

Source audit: all 35 retention rows use HJ=1.8e-18/s and shell averages, not
pointwise density. No new observed merger histories were imported. The reduced
profile and orbit are illustrative initial data. A rigid-profile encounter is
not equivalent to a live gas merger and no such equivalence is asserted.

Mathematical proofreading: the energy and mass dictionaries, q branch, orbital
period versus density period, and selective-CCT versus Palatini distinction
were reviewed. The force signs and potential derivative agree with the stated
Hamiltonian. No mathematical-token correction was required. The physical
mapping, nonlinear retention, galaxy law and microscopic selection remain open.

Validation: normal and adaptive-scan manifests validate with completed status;
mutation validates with expected failed status and the intended ledger assertion.
Raw numerical records retain the limitations of the tolerance checks.
