# A pinned interface found; galaxy-law preservation fails

The original joint goal remains open. A new saturating binding interaction
does hold a finite phase interface with an almost free outer reservoir in
one large-disk template. Its actual matter force destroys static balance
of the granted galaxy-law profile. This separates successful phase pinning
from a successful galaxy mechanism.

Starting revision e64a9f9c447b57794350b1d9d7f7a4ae7000a1de. Snapshots preserve
the exact parent models. No earlier experiment or manuscript was edited.
Research used the two-state binding-gap obstruction, vorticity barrier,
local-capture handoff, and local-inside-out interface failures. The global
pump/inertia scans and the constant-gap common-bath selector were not repeated.

## What was tested

FI-1:24 minimizations across two disk templates, two rotation turnover
radii, three interaction settings and two starting states. The barrier-only
interaction loses T even with spatially varying rotation. The new binding
interaction holds nonuniform phases, but no FI-1 case meets both fraction
gates. Small-disk binding cases keep81–91% of the outer material converted.
They remain explicit failures of this common-parameter model.

FI-2: six targeted large-disk minima, at n128 and256, test whether the
kinematic transition can be placed outside the inherited interior without
converting the outer reservoir. All use the same epsilon=1e5 (km/s)².

| Rj/b, c (n256) | Inner T fraction | Outer T fraction | Maximum interior matter-force imbalance / gravity |
|---|---:|---:|---:|
|5, .03|.96282|.03909|32.67|
|8, .03|.99947|.53147|.169|
|8, .1|.98825|.14291|1.299|

Inner means mass weighted on .5b..min(5b,.4Rreservoir); outer means beyond
.8Rreservoir. These are the inherited gates, not radii selected after a run.
For the first candidate, the inner interval is1.5–15 kpc, and the outer
reservoir is measured beyond44.26 kpc. Its minimum pointwise inner q is
.9294, despite its mean exceeding .95. Moving the rotation transition out
reduces some interior distortion but fails the free-outer requirement.

The first candidate has one q=.5 crossing at28.4497 kpc. Its defined
front-shift stiffness is1.91976 in the specified dimensionless units,
independently checked by energy second differences. Its full phase Hessian
is positive. At n128 the same front lies at28.4494 kpc, with stiffness1.91683.
These are phase results at fixed mass, not continuum or live-system proofs.

FI-3: shifting that front by +/-.2 kpc and relaxing returns it to the same
phase state. The energy-plus-heat error is below1.08e-9. A separate variation
of T mass, keeping F fixed, confirms the actual T-force calculation. After
recovery the maximum interior force imbalance remains32.674 times gravity,
and its unweighted radial RMS is10.064 times gravity. The maximum occurs
near13.72 kpc. It is not a small numerical residual: the uniform pure-T
control's maximum discretization error is .00533 at n256 (.02255 at n128).
The phase-minimum force failure persists on refinement; the exact peak is
not claimed converged beyond the tested grids.

## What has actually been learned

Finite-radius pinning is possible in this effective energy family. It arises
from competing field/interface energy and a spatially varying binding benefit;
the restoring coefficient comes from their full Hessian. No phase radius or
total converted mass is externally constrained.

However, a binding interaction also acts on matter. The pinned candidate
passes the phase-fraction test while failing the force equation by orders of
magnitude. Reporting its preassigned gravitational profile as a preserved
RAR would be false: that profile would immediately accelerate under the
derived additional forces. We did not evolve that failing density and do not
claim its eventual outcome or exclude a different re-equilibrated solution.

The auxiliary-mode construction derives the effective gap from an explicitly
postulated interaction; it is not a microscopic derivation or a parameter
measurement. There is no observational data fit, formation demonstration,
live baryon calculation, noise lifetime or nonspherical stability result.

## Reproducibility and next obligation

DERIVATION.md gives the restoring force, exact species potentials and baryon
reciprocity terms. Each of run_pinning, run_forces and run_recovery contains
the v2 manifest, exact command, hashes and results. VALIDATION.json records
fresh manifest checks. Phase energy/Hessian checks are below2.4e-9; total
mass potential variation is below9.1e-11; T-only variation below2.4e-9.
Review is self-review, not independent certification.

Do not repeat this scan as evidence that pinning alone works. A next candidate
must solve the joint phase AND matter force equations, with an interaction
whose bulk derivative is acceptably small and whose interface still restores.
A re-equilibrated positive density, different independently justified
kinematics or a genuinely interface-local interaction remains open, but each
must retain all reciprocal derivatives. These are untested continuations;
the present failures do not establish a universal no-go theorem.
