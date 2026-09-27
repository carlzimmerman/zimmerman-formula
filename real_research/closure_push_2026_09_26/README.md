# Continuing the gravity construction — CD26-2

**We have a more concrete route to closure, not a completed theory.** The
strongest new construction is a cosmological Hamiltonian whose physical
linear metric and ordinary-fluid system is local, whose nonzero-mode kinetic
matrix is positive under stated conditions, and whose nonlinear lapse admits
explicit expanding, inhomogeneous, positive-density constraint data. The
homogeneous lapse mode is retained as a global constraint.

This continues [CD26-1](../closure_doors_2026_09_26/README.md) and the earlier
[source audit](../closure_resume_2026_09_26/README.md). It does not restart those
calculations or treat failed parameter families as a universal no-go.

## The target changed during this calculation

External commit `9092fc0fd` amended the operative recipe to **filtered
nu_mono** and **preferred-foliation causality criterion B**. The initial
contract had pinned exact exponential AQUAL and the former metric-cone test.
Both versions and their hashes are retained in [target_versions.json](target_versions.json)
and [snapshots](snapshots/). No specification was edited by this campaign.

The new zero-field filter calculation follows the amended target. The
exponential action calculations remain explicitly separate branch results.
Instantaneous physical responses are not, by themselves, failures under
criterion B. Their boundary conditions, stability, clock and well-posedness
remain obligations. No change of target turns a partial calculation into a
full-action certificate.

## The strongest constructive chain

1. **Retain the independent IC28 auxiliary and constant tensor normalization.**
   This derives equal physical metric potentials on the tested active-pin
   branch. Tying the auxiliary by hand loses the coefficient that supports
   the scalar response.
2. **Make the active potential genuinely constant.** Set P0=P_Lambda<0 and
   L(S)=ell exp(S), with positive D(S) fixed before variation. This repairs
   the ordinary-matter pole of the earlier exceptional vacuum candidate.
   The independently transformed physical equations give local clock/fluid
   principal speeds; an explicit parameter choice has clock speed squared
   1/6 and ordinary-fluid speed squared w_f. The coupled nonzero-mode kinetic
   matrix is positive for the displayed a,B>0 and positive-enthalpy,
   positive-sound-speed fluid. The pressureless limit still needs treatment.
3. **Repair the nonlinear lapse-gradient coefficient explicitly.** Replacing
   B_old(S) by b exp(S) requires a displayed gradient counterterm. It changes
   the action; it is not a reinterpretation of old equations. The lapse
   constraint becomes (-4b Delta-A)y=0 with y=exp(S/2)>0.
4. **Construct actual nonlinear constraint data.** On a flat periodic leaf,
   y=exp(epsilon cos x), a constant expanding trace momentum, and an explicitly
   positive inhomogeneous ordinary density solve the lapse and momentum
   constraints. A ground-state factorization proves uniqueness of the lapse
   shape and an explicit positive gap on its normalized complement. A separate
   numerical source control adjusts an initial trace momentum, not the action
   constants, to satisfy the global constraint.
5. **Preserve the global condition under a stated reduction.** With an
   isolated positive lapse ground state, a regular second-class shape block,
   and all remaining canonical dependencies retained, the reduced Hamiltonian
   is H_red=-c(t)lambda0. It preserves lambda0=0. The independent
   [spectral reduction audit](lapse_kinetic/SPECTRAL_REDUCTION_AUDIT.md) derives
   the changing-volume correction and checks an exact two-mode analogue.
   This is a conditional local symplectic result; proving the full proposed
   action satisfies every assumption and has a well-posed continuum evolution
   remains necessary.

These are connected constructions in a specified **new cosmological sector**.
They are not yet connected to the operative static filtered-MOND action by a
fully varied transition. The detailed equations, controls and limitations are
in the [IC bridge](ic27_bridge/REPORT.md) and
[nonlinear lapse construction](spectral_lapse/RESULT.md).

## What each additional door earned

| Route | New result | Remaining limitation |
|---|---|---|
| [Filtered zero field](filtered_zero_field/RESULT.md) | The outer heat operator makes the fixed-leaf physical force spatially Lipschitz, including inner acceleration zeros. | Source dependence still has square-root behavior; the coupled Cauchy theorem does not follow. |
| [Auxiliary and lapse velocities](lapse_kinetic/REPORT.md) | A globally C2 symmetric penalty realizes the required anisotropic Hessian without the old zero-field cusp. An exact ADM kinetic Hessian gives two primary momentum relations. | Fixed-background static convexity and primary degeneracy do not complete the nonlinear Dirac chain. This construction uses the exponential branch. |
| [Measured Newton normalization](newton_normalization/RESULT.md) | G_N=G_bare/C opens an all-positive-acceleration principal window for exact exponential AQUAL. | Its same-action preferred-frame response is unacceptable in the tested family. The numerical obstruction does not transfer automatically to nu_mono. |
| [Covariant amplitude and phase](covariant_clock/RESULT.md) | Explicit two-scalar action; healthy local circular modes; a global homogeneous timelike-clock branch with conserved nonzero charge. | The [common-action test](covariant_clock/MOND_INTERFACE.md) derives a nonzero extra density/pressure response. It cannot silently retain a baryon-only MOND source. |

## Dark energy: what is and is not explained

The new active potential supplies a constant vacuum stress and an expanding
branch. The polar-clock construction independently shows why conserved charge
and cosmological dilution must be followed together. Neither result derives
the vacuum energy's magnitude or selects the a0–Lambda coefficient from first
principles. Flattening a potential is a declared action choice. Constant vacuum
subtraction cannot erase the charged clock's inhomogeneous susceptibility.
No dark-matter particle species or fitted particle abundance was inserted.

## Evidence and what the certificates mean

The accepted package has **45 compiled Lean declarations in six files**, with
only `propext`, `Classical.choice` and `Quot.sound` in their axiom reports.
They certify the stated exponential inequalities, real-algebra identities,
derivative implications, finite-mode bounds and constraint substitutions.
They do not certify the entire covariant action, the complete nonlinear PDE,
or empirical viability. [lean_manifest.json](lean_manifest.json) records the
source and compiler-output hashes and exact commands.

Twelve accepted run manifests cover eleven science calculations plus one bounded
compiler run. They include exact symbolic identities, high-precision witness
comparison, radial-response checks and spatial refinement. Failed/limited
development runs are retained separately; no timeout is treated as evidence
that an identity is false. [computation_validation.json](computation_validation.json)
records independent freshness checks. Recheck saved evidence with:

```sh
python3 real_research/closure_push_2026_09_26/verify_evidence.py
```

Independent reviews are recorded in [the Newton review](newton_normalization/REVIEW.md),
[the clock/filter/lapse review](covariant_clock/PEER_REVIEW.md) and
[the IC bridge review](ic27_bridge/review.md). Execution success is not the
same thing as a physical acceptance test.

## The next decisive calculation

Follow the new constant-potential, homogeneous-gradient cosmological sector
through its complete functional constraint chain, verifying the assumptions
of the conditional global-preservation result and deriving the independent
scalar/clock count. Then specify
one transition action to the operative filtered nu_mono sector and vary that
same action with respect to both metric potentials, the lapse, clock,
auxiliaries and ordinary matter. Carry the measured-G and moving-source PPN
tests through that transition. These are concrete construction obligations;
the gains above do not remove them.

No new empirical cosmology or galaxy fit was produced in this checkpoint.
The full thirteen-requirement theory remains **OPEN**.
