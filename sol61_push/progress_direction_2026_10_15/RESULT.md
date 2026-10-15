# Progress review and directed next steps

15 October 2026. Review of progress after mechanism checkpoint
`2968d72cfe6ca580dde906676c73207f95d63b73`, starting from
`7c1eae898ec964062a01f9a79f8d7b8af5d5d52b` and incorporating the DR4
readiness note at `0aec66b397c474309f6bf872bd370a9e9d6ac38d`.

**The most useful new progress is a conditional explanation of much of the
outer lensing signal through catchment supply and neighbouring matter. The
full physical theory remains open.** The next round should establish a
consistent finite-mass prediction and reliable controls for this explanation,
then test its remaining profile mismatch. The existing radial wall theorem
remains a separate mathematical control.

## What changed

| Recorded result | Progress supported by the raw record | Remaining condition |
|---|---|---|
| CFG803 infall-filled profile | Primary relative chi-square changes by about +0.1 from the no-edge reference; finite-cutoff supply scan needs N=3–4 in the primary range, N=16–24 over all radii | Its C template applies an enclosed-mass fill table to density and extends the nonzero fill to infinity. It is not a finite-supply dynamical mass theorem |
| CFG804 census catchment | Algebraic retention fixed point gives N about 5.6–10; primary relative differences are -0.229 canonical and about -1.505 alternative | Retention is externally calibrated; four galaxy masses are profiled. Canonical absolute chi-square is 83.63/28, p about 1.90e-7. Full-range relative difference is +148.69 |
| CFG805 two-halo template | Adding projected T1x clustering narrows the full-range relative difference from +148.69 to +11.06; its frozen classifier says NARROWED | Absolute chi-square remains 170.66/52, p about 1.50e-14; spectrum normalization control fails, exclusion mutation is only partly sensitive, and bias is fitted per bin |
| Joined critical two-fluid/wall body | The existing actual equilibrium and positive complete radial form remain audited | No new physical EOS, phase, angular-mode, metric, formation or abundance derivation landed in this review interval |
| Laboratory follow-up | CFG799 records a null for the stated converter-efficiency window; CFG802 classes the 541.700 GHz excess HINT FADES | Conversion limits depend on the specified density/geometry. The CFG802 polarization control has a disclosed mutation flaw; neither result proves every carrier impossible |
| DR4 outcome map | Makes the unresolved uncertainty/statistic convention explicit before unsealing | CFG800's R and the preregistration's pooled gamma are different statistics; their errors and hypothesis tests need an explicit mapping |

These are different candidate templates and registered tests, not consecutive
proofs of one completed theory. In particular, “supply suffices” in CFG804
means its relative criterion passes. It does not mean an acceptable absolute
fit, a microscopic production mechanism or a prediction with no fitted inputs.

## First priority: establish a reliable lensing comparison

Create a dated successor calculation with its criteria fixed before execution;
keep CFG801/803/804/805 outputs and classifications intact. Start with the
following dependencies, which can be resolved without another production
simulation:

1. **Reconcile spectrum estimators.** CFG650 measures sigma8 using the actual
   discrete Fourier modes; CFG805 integrates shell-mean power at shell-mean
   wave numbers. Both lack sub-fundamental box modes. Compare the same modes,
   window, mass assignment and normalization before attributing their 3.2%
   difference to missing large-scale power. A free bias can absorb a uniform
   amplitude change; it cannot generally absorb a change in template shape.
2. **Resolve the retention mass units and physical edge.** CFG416 calls its
   retention curve on a mass labelled solar masses/h; CFG804 uses physical
   solar masses. Trace the calibration's native convention and write the
   conversion explicitly. Recompute N and its physical cutoff in that same
   convention. Do not choose a conversion because it improves the fit.
3. **Use one declared exclusion rule during fitting.** CFG805 fixes exclusion
   radii from the old CFG804 best fit while refitting galaxy masses. Its
   nearest-N cutoff grid also changes the actual one-halo edge. Define the
   same exclusion prescription for both comparison models, consistent with
   the actual truncated profile, and update it for each trial mass. Demonstrate
   radial/projection and cutoff-grid convergence and optimizer convergence.
   First check the zero-exclusion projection against an independent
   Fourier/Bessel calculation with the same spectrum, smoothing and units.
4. **Diagnose the actual fitted models with the full covariance.** Save both
   models' predictions, residuals, nuisance parameters and joint chi-square.
   The recent heavy-bin diagnostic evaluates the earlier no-edge model without
   the two-halo term. It does not identify which bins cause the CFG805 residual.
   Separate-bin marginal chi-squares do not add to the joint chi-square when
   bins are correlated. Use conditional residuals or explicitly retained
   covariance cross terms before attributing a discrepancy to hot gas or
   early-type galaxies.

Acceptance evidence: matching spectrum-estimator control in its declared
tolerance, deterministic unit and edge identities, a sensitive exclusion
control for its stated range, numerical convergence, and reproducible joint
scores with identical nuisance freedom for both models. Report the absolute
fit as well as the relative difference. Reuse the old CLOSED thresholds only
with an explicit successor registration; a narrowed relative gap alone
cannot satisfy the absolute p>=.01 requirement.

The [control review](LENSING_CONTROL_REVIEW.md) gives the estimator evidence,
source hashes and exact implementation limits. None of the old scores is
silently corrected by that review.

A bounded [independent shell/window replay](lensing_control_check/run_001/result.json)
recovers `sigma8=.775159` from saved shell means with integer-lattice mode
counts, compared with the stored actual-mode `.779143` and CFG805's
trapezoidal `.754300`. Its largest calculation retains 1,072,218 modes through
`k<3.99 h/Mpc`, with no simulation or fit. The remaining difference is about
0.51%. This supports estimator compression/quadrature as a major contributor;
unknown individual mode powers prevent exact reconstruction. The
[manifest](lensing_control_check/run_001/manifest.json) pins the copied inputs
and bounded execution. This diagnostic does not change the original failed K2
or validate the lensing transform. Recover the original per-mode/window sums
or export an equivalent measurement before claiming an exact estimator match.

## Second priority: close the finite inventory and dynamics bridge

Carry the retention-derived N as a conditional, externally calibrated input.
Define non-overlapping ownership or normalized weights for host, satellite,
diffuse and neighbouring populations. Integrate their actual mass function and
volumes against one baryon/cold inventory; a stack of overlapping lens-centred
profiles is not an inventory. Track matter crossing a catchment boundary and
the corresponding gravity, gauge charge and energy.

Then name the action/evolution equations and applicable O2 health checks and
derive the **actual finite N~5.6–10 profile** used in the lensing calculation.
A reduced mechanical evolution must retain that conditional label. Check its enclosed-mass and density relation,
finite outer boundary, escape/retention, energy drift and convergence for
independent initial states. CFG748's much larger initial supply and CFG803's
infinite continuation do not supply that implication. Project this finite
profile and the separately owned neighbouring population to DeltaSigma with
the same covariance and sample selection as the repaired comparison.

Acceptance evidence: every mass element counted once, a finite charge/energy
budget, an actual supported or evolving density profile at the stated supply,
and a candidate-matched lensing prediction. Keep the source/ownership rule and
irreversible settling open until their dynamics are derived.

The [catchment review](CATCHMENT_REVIEW.md) also limits ARGON09: its provisional
global cell estimate and surface-density budget do not establish a unique
cosmic inventory or a covariance-scored two-halo subtraction. Its
pi R-squared times DeltaSigma proxy is not an exact enclosed mass. These
estimates motivate the test; they do not revoke CFG801's recorded result or
establish physical rescue on their own.

## Parallel physics and observation work

**Keep one physical candidate explicit.** Relate the finite-stiffness current,
its physical density and outer population to a common varied action with
actual baryons, gauge field, phase and metric. If the high-pressure wall body
is retained, derive its EOS, reflecting interaction and wall carrier and show
how it reaches the intended galactic regime. Until then, use its positive
radial theorem as a control. The next mathematical falsifier is the coupled
nonspherical interface/relative-current sector, including constraint
elimination and all surface work; pure-electric bulk cones are insufficient.
Preserve the old taper, minimal Lorentz-vacuum and weak-neutral-core
obstructions unless a changed premise addresses their proofs.

**Specify the sealed-test scorer before unsealing.** Define CFG800's R,
uncertainty budget, systematic floor, null hypothesis and meaning of the 2/3
sigma statements. Map it to the preregistered gamma statistic if they are to
share errors or labels. Distinguish exclusion of CFG740 from exclusion of an
entire framework arm. The dated DR4 note identifies owner decisions; this
review changes no sealed file, criterion or preregistration. A sensitivity
calculation using sigma=.028 remains conditional on adopting that error model
for the correct statistic. No future outcome can be scored now.

Formation/export, microscopic parameter origins, abundance and native
cosmology remain O1–O8 obligations. T1x still carries inherited initial
conditions/background. A clearer manuscript and an upload-ready file are
communication progress, not additional physical evidence. The
[physics priority review](PHYSICS_PRIORITY_REVIEW.md) identifies the unchanged
proof dependencies and the laboratory routes that should remain closed under
their existing assumptions.

## Evidence and next handoff

[CONTRACT.md](CONTRACT.md) fixes this review's scope;
[source_manifest.json](source_manifest.json) pins its read inputs and review
artifacts. Existing scores are quoted from raw repository records, not rerun
or statistically re-certified. The small independently recorded estimator
diagnostic, where used, is distinguished from a corrected production score.

The next handoff should identify the exact successor candidate, unit and
exclusion conventions, control outcomes, full-covariance residuals and first
remaining physical implication. Declare closure only for an obligation that
those artifacts actually settle. The complete physical theory remains open.
