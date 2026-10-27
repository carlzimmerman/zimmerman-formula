# Selective stress and reciprocal conversion radiation

**Original galaxy-formation objective remains open.** This continuation finds
a direct, reciprocal way for conversion potential to supply outgoing radiation
without changing the static energy. It also rejects the tested F-only stress
and initial virial-entropy repairs. It does not establish a universal galaxy
theory or a fully coupled formation history.

Base: [the previous physical-completion handoff](../physical_completion_2026_10_25/HANDOFF.md)
at Git32fca884da31642e5435be9b60a9b6ee5bca61d0. Every run pins its actual
revision; unrelated repository work continued during this research. The new
immutable [target](TARGET.md) retains the original criteria.

## The new mechanism

Add a shift-symmetric derivative interaction `g partial_mu(chi) jT^mu`.
For conserved T current it is a boundary term. During conversion,
`div(jT)=Gamma`, it becomes a direct source for massless waves. It therefore
does not need an initially supplied modulus oscillation. The scalar momentum
shift and reciprocal material force must both be included.

The full derivation is [DIRECT_RADIATION.md](DIRECT_RADIATION.md). Its Hamiltonian
is a positive wave/material kinetic energy plus the original static energy.
An exact square/Schur-complement argument preserves an existing static radial
minimum and its relaxed boundary stiffness. This inherits the previous
approximately 0.71% benchmark law residual and positive radial stiffness; it
does not repair the previous failures at other masses.

## Latest result: derive the internal inertia and use propagation at c

SS-23 derives conversion inertia from the stated canonical gapped internal
state, using the existing stiffness and alignment coefficient. The binding-
energy estimate gives a local inverse frequency of 0.493 Myr, compared with
R/c=0.184 Myr. SS-25 finds a9.68% fixed-background inertia correction and
negligible bare carrier inertia. This is an alignment-dominated internal-mode
calculation; it excludes the much larger inertia of moving matter.

With this inertia, the measured halo source and propagation at c, SS-24 exports
99.8077% of a **binding-only** potential. That energy is only about 46.5% of
the actual total collapse release. A separately labeled **whole-release cosine
potential hypothesis** exports 99.9141%; SS-29 doubles resolution and tests the
inertia correction, retaining more than 99.6% export by its shorter endpoint.
The latter potential is not derived from a mobile-density trajectory.

SS-26 propagates canonical outer material perturbations under that measured
pulse. The maximum perturbation-energy gain is 1.044071 over four local probes;
the smallest sampled phase gap remains14.1505. This is a frozen-density,
adiabatic-carrier test, not nonlinear reservoir evolution.

SS-27 then tests the dangerous missing inference. On one actual mass-conserving
endpoint interpolation, transport inertia is 3.89e8 times the internal inertia
and an energy barrier remains. SS-28 separates infall and front position; its
two finer grids find **zero sampled minimax barrier** with the original energy.
Neither result is a full physical trajectory. The explicit next reduction,
including the continuity-derived interface source and every reciprocal force,
is [FRONT_REDUCTION.md](FRONT_REDUCTION.md).

The canonical extraction and figure are
[run_report_checked/results.json](run_report_checked/results.json) and
[reciprocal_conversion.png](run_report_checked/reciprocal_conversion.png).

## Earlier radiation checks with a prescribed collective time

The autonomous spherical prototype starts with **zero field energy** and all
energy in a conversion potential. It includes the reciprocal backreaction,
outgoing-wave approximation, and both energy and shift-charge escape ledgers.

| Test | Result | Scope |
|---|---|---|
| SS-06, smooth compact source, g=1 |99.9920% export by t=2000 |Fixed source, reduced conversion potential |
| SS-07, three space/time meshes |97.7191% threshold times38.24,38.10,38.07 |Refined numerical transport |
| SS-10, measured halo T-mass source |99.904096% export by t=200 |Fixed density and boundary; reduced conversion potential |
| SS-10, doubled source resolution |Threshold38.60 ->38.59 |No initial wave energy |
| SS-10, finest ledgers |Energy6.75e-12; charge8.04e-11 |Maximum normalized ledger error |
| SS-15, joint outer phase response |Drive1.15885 below margin14.7024 |Frozen halo density, local phase stability |

Time and speed in these earlier tests are stated dimensionless choices. In this
regime the scalar crossing time of the source is comparable to the bare
conversion inverse frequency. Mapping R=56.36 kpc and R/c_s=100 Myr would
require c_s approximately 550 km/s and put the sampled heat threshold near
3.86 Gyr. Neither that medium sound speed nor the kinetic inertia is derived.
The source follows the actual computed halo T profile in SS-10, but the
conversion potential remains a reduced cosine, **not the actual collapse
energy as a function of redistribution**.

The frozen-reservoir check includes simultaneous carrier and matter phase
variations. It does not simply compare the pulse to the alignment constant J.
It does not establish nonlinear nucleation suppression, absence of F heating,
or a mobile-reservoir trajectory. For a conserved current the spatial canonical
momentum shift cancels the apparent pure-gauge Euler force; a chemical-potential
gradient alone must not be misreported as an extra material body force.

## Restrictions that matter

**Fast relativistic escape is not a free improvement.** The direct interaction
adds positive inertia `Delta I=g^2 A0/c_s^2`. At low frequency a normalized
compact spherical source obeys `A0>=1/(4pi R)` and its linear harmonic energy
decay rate is at most `omega^2 R/c_s`. A uniform sphere with inverse angular
frequency 100 Myr and c_s=c has an approximate minimum energy e-folding time
65.28 Gyr. This is a restricted low-frequency bound, not a nonlinear no-go.
SS-05 checks the exact sphere kernel and finite-frequency imaginary part;
SS-08 retains reciprocal inertia and moves absorption into the true wave zone.
Its c=500 case exports 84.54% by t=2000, below the required 97.7191% threshold.

**The previous supplied-pump result did not supply its own energy.** SS-03
removes that assumption in an autonomous adiabatic-modulus model. The tested
six single-mode cases export very little; the fast-escape k=500 case mostly
exports its tiny initial angular seed. The successful direct-source interaction
is a changed mechanism, not a relabeling of that old oscillator calculation.

**F-only gradient stress does not supply the demonstrated filled branch.**
SS-01 stalls in angular variables. SS-02 reformulates the same energy in
species amplitudes and checks exact energy agreement and directional gradients.
SS-04 uses a different globalizer. It still produces a severe depleted layer;
its density rebound exceeds1e23 and sampled law error is about 7.77%.
It is not fully force-converged, so this rejects the attempted repair, not all
possible cold two-fluid theories. The canonical spinor identity remains intact:
the alternative explicitly changes the material constitutive hypothesis.

**A derived initial F entropy does not automatically repair the law.** SS-12
solves a gamma5/3 hydrostatic F reference with total mass and a stated
200-critical virial density, without fitting the law or setting temperature
from its desired velocity. The derived K values are3.8574,3.0585,2.4241 for
scales0.5,1,2. SS-14 continues the high-mass branch toward that state; SS-16
changes the globalizer and reaches force stationarity with 43.27% law error,
density rebound6.52, and three phase crossings. Thus this tested adiabatic
virial-entropy continuation is not a solution.

See [DERIVATION.md](DERIVATION.md) for selective material forces, the autonomous
pump, and the distinction between an energy ledger and a physical radiation
channel. No target-law density or force residual is used in any energy.

## Evidence and route outcomes

Each `run_*` directory contains its frozen contract reference, argv, input
hashes, raw logs, result and v2 provenance manifest. Completed process status
does not mean a physical success. SS-13 is a reporting-inheritance error before
iteration; SS-14 corrects it without changing the canonical energy. SS-17
fails its independent mass-quadrature tolerance; the BVP itself converges.
SS-18 increases quadrature resolution and confirms the same entropy.

SS-19/20 test the previously untried combination of a stronger carrier barrier,
independent carrier/matter fields, larger existing census supply and derived
virial entropy, starting in an inside-out prepared basin. This explicitly
changes the mass budget to53.643 Mb. It is neither the fixed 5.364 test nor a
formation simulation. Its changed globalizer leaves a seven-crossing depleted
state with 58.50% window error; it misses the phase-force tolerance. This does
not establish a universal exclusion of other basins. The exact assessment and
resumption conditions are recorded in the handoff.

The designated short live view is [STATUS.md](STATUS.md). Use
[HANDOFF.md](HANDOFF.md) for the next discriminating physical calculation and
[SELF_REVIEW.md](SELF_REVIEW.md) for the claim boundaries and audit provenance.

## Bounded-run ledger

31 valid manifests:29 completed processes and2 failed processes. Process completion is not physical success.

| Claim | Run | Process status |
|---|---|---|
| SS-01 | [run_high](run_high/manifest.json) | completed |
| SS-02 | [run_species_high](run_species_high/manifest.json) | completed |
| SS-03 | [run_conversion_pump](run_conversion_pump/manifest.json) | completed |
| SS-04 | [run_globalize](run_globalize/manifest.json) | completed |
| SS-05 | [run_direct_radiation](run_direct_radiation/manifest.json) | completed |
| SS-06 | [run_reciprocal_wave](run_reciprocal_wave/manifest.json) | completed |
| SS-07 | [run_reciprocal_refine](run_reciprocal_refine/manifest.json) | completed |
| SS-08 | [run_retarded_wave](run_retarded_wave/manifest.json) | completed |
| SS-09 | [run_reservoir_margin](run_reservoir_margin/manifest.json) | completed |
| SS-10 | [run_halo_source_wave](run_halo_source_wave/manifest.json) | completed |
| SS-11 | [run_static_extension](run_static_extension/manifest.json) | completed |
| SS-12 | [run_virial_entropy](run_virial_entropy/manifest.json) | completed |
| SS-13 | [run_thermal_branch](run_thermal_branch/manifest.json) | failed |
| SS-14 | [run_thermal_branch_checked](run_thermal_branch_checked/manifest.json) | completed |
| SS-15 | [run_reservoir_halo_margin](run_reservoir_halo_margin/manifest.json) | completed |
| SS-16 | [run_thermal_globalize](run_thermal_globalize/manifest.json) | completed |
| SS-17 | [run_census_entropy](run_census_entropy/manifest.json) | failed |
| SS-18 | [run_census_entropy_checked](run_census_entropy_checked/manifest.json) | completed |
| SS-19 | [run_census_joint](run_census_joint/manifest.json) | completed |
| SS-20 | [run_census_globalize](run_census_globalize/manifest.json) | completed |
| SS-21 | [run_halo_pulse_record](run_halo_pulse_record/manifest.json) | completed |
| SS-22 | [run_outer_dynamics](run_outer_dynamics/manifest.json) | completed |
| SS-23 | [run_spinor_inertia](run_spinor_inertia/manifest.json) | completed |
| SS-24 | [run_derived_inertia_wave](run_derived_inertia_wave/manifest.json) | completed |
| SS-25 | [run_inertia_audit](run_inertia_audit/manifest.json) | completed |
| SS-26 | [run_outer_derived_dynamics](run_outer_derived_dynamics/manifest.json) | completed |
| SS-27 | [run_transport_audit](run_transport_audit/manifest.json) | completed |
| SS-28 | [run_front_landscape](run_front_landscape/manifest.json) | completed |
| SS-29 | [run_derived_wave_refine](run_derived_wave_refine/manifest.json) | completed |
| SS-30 | [run_report](run_report/manifest.json) | completed |
| SS-31 | [run_report_checked](run_report_checked/manifest.json) | completed |
