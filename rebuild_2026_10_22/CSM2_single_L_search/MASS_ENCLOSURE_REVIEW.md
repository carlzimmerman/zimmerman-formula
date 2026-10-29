# Endpoint mass-enclosure checkpoint

`mass_enclosure_001/` completes the declared 124 x 3601 = 446524 coordinate
coverage in39 seconds. All9 controls pass. Every old registered padded endpoint
box contains its directed enclosure; no padding was enlarged. The shifted1%
candidate fails containment. All arrays are finite, ordered and nonnegative.

For positive a<=r0<=b and t=min(r,R), positivity and B'(x)>0 imply

    a^2 B(t/b) <= r0^2 B(t/r0) <= b^2 B(t/a).

Multiplying by positive pi Sigma and adding the baryonic profile preserves
these inequalities. Directed50-digit evaluation covers endpoint-expression
rounding. Saved float64 endpoints are moved outward with nextafter; each is
then checked against its original interval endpoint. This is an endpoint mass
certificate for the fixed coefficients specified in MASS_ENCLOSURE_CRITERIA.
It includes radii outside R; the factor bound is conservative there as well.

The self/adversarial review refines all124 roots at80 digits and uses the
independent normalized compact mass M B(t/r0)/B(R/r0), with a different log
expression. Its496 selected radius checks all pass (127 review controls).
That selected-radius review complements the main computation's exhaustive
446524-coordinate coverage; it does not replace it.

Scope limits remain substantial: saved geometry/column coefficients and the
computed binary64 stellar/cold coefficients are interpreted exactly. Their
construction, continuum-L endpoint/branch enclosures, projection coefficients,
stacking/whitening and signed-dot rounding are not certified by this stage.
The local full-score result remains conditional. No passing witness, certified
L interval exclusion or continuous covering obstruction is established.

Metadata clarification: the contract's inherited conventions mention the
source2401-point projection quadrature and binary64 coefficient domain. No
projection quadrature runs in this subexperiment. Arithmetic actually performed
is the documented50-digit directed interval evaluation with fixed binary64
input coefficients. Runtime/backend are in the completed manifest/results.

Reproduce with the recorded scientific Python environment and
`launch_mass_enclosure.py NEW_RUN_DIRECTORY`. Do not overwrite completed data.
