# FGF-011 worker report — awaiting orchestrator acceptance

Actual worker: Astra agent `/root/dynamics_precision`, run `fgf011_audit_001`.
This is not a DeepSeek execution. Outcome: **supports_scoped_claim**.

All seven pinned MS1 intake hashes matched. Independent reconstruction confirms
the constant-coefficient dispersion, directional threshold, unique growth
maximum, positive kinetic form and high-frequency classification. These are
statements about the explicitly supported, mean-subtracted model. Unsupplemented
uniform positive density plus an affine field fails both background equations.
The exact hydrostatic slab identity kJ² Lrho Lg=1 is also confirmed; it prevents
an unstable local mode from fitting a slowly varying patch of those slabs.

The new discriminating audit result is a positive factorization of the proposed
inhomogeneous energy. With C=4 pi G, exact isothermal hydrostatic balance,
rho,A>0 and xi=psi=0 at both fixed endpoints,

    2V = integral [cs² rho (xi')² + (A/C)(psi'+C rho xi/A)²] dx > 0

for every nonzero admissible pair. The unreduced boundary term is
[cs²rho' xi²-2rho xi psi] at the two endpoints. Its sign and normalization
were independently derived and numerically checked. The full finite slab
therefore has positive longitudinal linear squared frequencies for K>0,
under these precise boundary conditions. This is not nonlinear/global physical
stability, not a three-dimensional result, and not an isolated-object result.

The bounded independent run passed **34 controls**: 672 operator/root cases,
96 growth maxima, eight dimensional backgrounds carrying both normalizations
and the separate frozen H comparison, and four independently reconstructed
slabs. Each source root was normalized by its own magnitude, rather than by
the larger root. Largest lower-root relative-or-absolute error was 5.44e-14;
maximum peak-location relative difference was 1.18e-7; slab-profile difference
was 2.23e-15. Sixteen energy trials included four deliberately inadmissible
boundary controls. Full factorization residuals were below 3.56e-15, while
omitting their nonzero boundary terms leaves errors from 4.71e-4 to 0.190.
These are finite binary64 implementation checks, not interval-certified bounds.

The numerical runner enforced a 120 s child wall limit, 100 s CPU cap and
1 MiB log limit; one numerical-library thread was requested cooperatively.
Runtime was 0.346 s, exit 0. No memory cap was claimed. Manifest validation
against the repository root passed. No failed numerical run occurred.
Expected negative controls remain explicitly recorded in audit_results.json.

The original candidate's eight time integrations were inspected but not rerun;
no finite-slab eigen-spectrum was computed. The continuum factorization has an
exact proof independent of the finite checks. Cosmology, photon coupling,
observations, empirical K and more general boundaries remain outside coverage.

Recommended next action after independent acceptance: revise **FGF-015** to
verify positive-spectrum convergence with a conforming variational scheme and
correct boundary support, then consider separately specified changes of the
boundary problem. A negative numerical mode under the exact current walls
should trigger an implementation/boundary audit. This worker has not edited
the shared task, queue, claims or any earlier evidence.
