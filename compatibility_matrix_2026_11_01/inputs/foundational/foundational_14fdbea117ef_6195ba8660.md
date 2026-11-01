# FR01: field response tested; a stable dense-core mechanism is not established

**Result, 1 November 2026.** The six inherited dense PN28 halos are energy
saddles within an explicitly tested canonical kinetic family. Independent
finite deformations preserve dark mass and phase-space occupancy and lower
the full energy in both directions. Three dilute controls have no negative
direction in the tested radial spaces, and three completed baryon-loaded
endpoints also pass that finite screen. The compact dilute example contracts
substantially. This work does not derive the desired suppression of spiral
contraction, the a0 relation, or cluster gravity.

This is new field-stress/energy work, not another fitted shell-contraction
rule. The parent, pressure coefficient, scalar stiffness and canonical
waterbag level are held fixed within each response experiment. The parent
itself remains a chosen conditional model, not a microscopic derivation.

## What was actually calculated

1. Reconstructed the six existing finite-gradient halo solutions from copied,
   hashed PN28 inputs: central depth psi_c=.8,.95,.99 and epsilon=.0001,.01.
2. Derived a positive-inertia *linear* fluid-plus-scalar completion and its
   full radial energy Hessian. Retained scalar gradient stress, reciprocal
   coupling, self-gravity, the exterior scalar, and fixed dark mass.
3. Found negative radial directions in all six reduced-fluid cases. Then
   restored the kinetic anisotropy created by an actual canonical radial
   deformation, instead of assuming instantaneous isotropization.
4. The original fluid directions become positive when that shear cost is
   included, but reoptimization finds different negative directions in all
   six kinetic cases. An independent full-energy calculation verifies those
   new directions without relying on the assembled Hessian alone.
5. Solved fixed-dark-mass equilibrium responses to two imposed Plummer baryon
   profiles, including smaller continuation steps after numerical failures.
6. Added three predeclared dilute controls and screened the three completed
   dilute baryon endpoints. No further parameter search was performed.

The kinetic result is **an accessible energy-saddle result, not a proof of an
exponentially growing Vlasov mode**. Positive finite-space values are not full
stability theorems. No nonlinear formation trajectory or general
vacuum-crossing completion was constructed.

## The dense-core result

The last two columns are normalized finite-space Rayleigh values. Only their
converged energy signs are used; they are not physical growth rates.

| Initial psi_c | epsilon | Reduced-fluid minimum | Canonical kinetic minimum |
|---:|---:|---:|---:|
| .80 | .0001 | -.050223 | -.015774 |
| .80 | .01 | -.047008 | -.014825 |
| .95 | .0001 | -.502896 | -.091619 |
| .95 | .01 | -.468320 | -.099148 |
| .99 | .0001 | -.625841 | -.087370 |
| .99 | .01 | -.779938 | -.109060 |

The exact additional kinetic Hessian is

    Q_kinetic - Q_fluid = (8/9) integral E_rel (xi' - xi/r)^2 d^3x.

It follows from the cotangent lift of a radial spatial map, which conserves
canonical phase-space volume and each trajectory's angular momentum. Thus the
extra cost is not a tunable response factor. The independent finite-energy
test confirms lower energy for both signs in all six cases; its quadratic
comparison and doubled-quadrature comparison agree within 6.64e-10, and its
finest finite-difference curvature error is at most 8.53e-6 relatively. Exact
rational bounds confirm positive map stretches and an enclosed matter edge
for all 24 recorded perturbation steps; the conservative radial-stretch lower
bound is at least .86217 throughout the occupied region.
See [the independent energy report](CANONICAL_ENERGY_REPORT.md),
[the derivation](THEORY_REVIEW.md), and [the reviewer report](INDEPENDENT_REVIEW.md).

## What happens when ordinary matter is added

The two dimensionless forcing choices are diagnostic assumptions, not measured
dwarf/spiral galaxies: diffuse baryons have Mb/Mdark=.05 and scale a/Rhalo=.5;
compact baryons have Mb/Mdark=.20 and a/Rhalo=.1. Dark mass and the field
coefficients stay fixed. Central potential and density are outputs. The
baryonic potential is imposed; its assembly and reciprocal dynamics are not
modeled as an autonomous baryon population. Fixed mass and waterbag level do
not impose the full orbital-invariant distribution along the static sequence.

On the original dense branches, three complete diffuse paths lower the core
column by 16–20%. Those endpoints must not be promoted as a stable suppression
mechanism: their starting states have the adverse energy result above.
Moreover a finer-step concentrated weak-gradient example increases the column,
so the static response has no universal sign. Unfinished paths are numerical
nonconvergences, not established physical endpoints or nonexistence results.

The dilute controls psi_c=.2,.4,.6 at epsilon=.01 have positive tested fluid
and kinetic minima. Three complete forcing paths were obtained:

| Initial psi_c | Forcing | Final core column / initial | Radius enclosing original core mass / initial | Endpoint radial screen |
|---:|---|---:|---:|---|
| .2 | diffuse | 1.08159 | .96444 | no negative tested direction |
| .2 | compact | 3.03708 | .68562 | no negative tested direction |
| .4 | diffuse | 1.10892 | .95647 | no negative tested direction |

The compact example shrinks the radius enclosing the **same original dark
core mass by 31.4%**, while the central density increases by a factor 7.05.
It therefore demonstrates a self-consistent conditional field response with
substantial contraction, not the desired nearly absent spiral response.
There is no observational mass mapping or comparison to a calibrated
Blumenthal suppression fraction here. Endpoint positive tests do not establish
that a time-dependent evolution reaches these equilibria.

Details and retained failures are in [dense static results](STATIC_RESULTS.md),
[continuation refinement](STATIC_REFINEMENT_RESULTS.md), and
[dilute response](STATIC_DILUTE_RESULTS.md).

## What this advances, and what remains

The work separates two questions that static halo shapes could not answer:
whether a dense core is an energy minimum, and whether the same field actually
responds weakly to baryons. The six inherited dense states fail the energy
minimum test even after the kinetic correction. Dilute states remain open,
but the resolved compact response contracts strongly. Neither outcome supplies
the missing universal mechanism.

The next missing physical calculation is the **full anisotropic kinetic
evolution/spectrum with scalar backreaction and an explicit vacuum boundary**,
including how a halo selects its state. Repeating the same static dense cores
or inserting a fitted contraction switch would not address that dependency.
The pressure/vacuum ratio B/V and phase-space level remain unselected; kappa=1/2
is not derived. No old galaxy or cluster observational pass transfers to this
changed field model automatically.

## Evidence and reproducibility

All experiments were short, conventionally single-threaded and locally bounded
at 300 seconds wall / 240 seconds CPU. Reported peak memory stayed below 1 GB;
unsupported macOS address-space or affinity enforcement is not claimed.
The zero-baryon algebra, exact kinetic correction and finite-deformation energy
were independently reviewed. Numerical refinement is not interval certification.

| Evidence | Recorded run status | Meaning |
|---|---|---|
| radial_run_003 | completed | six reduced-fluid adverse directions; controls pass |
| kinetic_run_002 | completed | six corrected kinetic energy saddles; controls pass |
| canonical_energy_run_001 | completed | independent full-energy verification |
| dilute_stability_run_001 | completed | three dilute finite radial screens |
| endpoint_stability_run_001 | completed | three completed baryon endpoint screens |
| static_run_002 | failed | 24 passing states, 9 failed solves, 27 skipped; partial grid |
| static_refinement_run_001 | failed | 163 passing states, 9 failed solves, 320 skipped |
| static_dilute_run_001 | failed | 173 passing states, 3 failed solves, 70 skipped |

Earlier execution/serialization/control failures are retained with their original
sources and manifests. A valid manifest is provenance, not a successful physical
result. [Diagnostic labels](DIAGNOSTIC_DICTIONARY.md) and
[kinetic metadata clarification](KINETIC_METADATA_CLARIFICATION.md) resolve
inherited wording without rewriting records. [Verification](VERIFICATION.json)
lists current manifest checks and source hashes; [reproduction instructions](REPRODUCE.md)
give the bounded commands. The publication branch is
`codex/fr01-field-response-2026-11-01`; no earlier lane or shared staging state
was changed by the publication procedure.
