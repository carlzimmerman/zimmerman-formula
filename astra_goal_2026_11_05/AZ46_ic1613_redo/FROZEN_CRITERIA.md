# AZ46 IC1613 cube redo — frozen after required diagnosis

Pre-freeze diagnosis: e282c8c2dc/a8f468e93c. It reproduces FN4a's two
stage0 mismatches; the full table-to-map mass discrepancy remains open.
Kappa=1/2 FITTED; not theory closed. This test is explicitly not blind
to FN4a's failures and does not change that record. These criteria are
committed alone before the new cube preparation or fits.

## Inputs and scope

Use the local natural and robust raw cubes, natural moment0/1/2 maps,
V image and published distance/mass assumptions already used by FN4a.
No new downloads. Each cube gets its OWN CLEAN beam from its header
HISTORY, including PA; the original hardcoded natural beam must not
propagate to the robust run. Natural primary-beam-corrected moment0
provides the COMMON gas-mass input for both cube fits, with helium1.33;
the robust cube is a kinematic/weighting cross-check, not an independent
high-resolution baryon map. Report that limitation.

Hold FN4a's stated primary Mstar2.88e7Msun and bracket1.9e8Msun, distance
0.73Mpc, constant-M/L V-profile assumption, and omitted Local Group EFE
as explicit assumptions. The missing UBV calibration is not invented.
Build the V profile in row chunks to avoid the original >1GB WCS grid.
No M/L, distance, inclination prior or mass calibration is fitted anew.

There are TWO distinct verdict layers. Exact reproduction of Oh2015's
published bulk-field/flux benchmark remains NOT EVALUABLE without the
missing products in NEEDS_OWNER. Do not treat Hunter's11% mean natural/
robust difference as an error bar. The second layer tests whether the
declared thin-disc forward model can describe the LOCAL cubes. It may
produce a conditional cube verdict after its own controls; it cannot
claim the external calibration discrepancy has been repaired.

## Independent preparations and numerical pairs

Read raw planes/header metadata in bounded memory. Use the same30arcmin
crop centred on Oh2015's centre and native spectral channels as FN4a.
Prepare separate natural/robust masks from their own noise using the
original physical smoothing: spatial Gaussian sigma10.2arcsec, spectral
3-channel box, threshold3 times smoothed emission-free noise, connected
components>=1% of the largest, dilation radius12arcsec and +/-2channels.
Noise comes from the first/last15 raw channels. Do not transplant the
natural mask or noise into the robust cube.

Rungs: native2x2 and4x4 binning (3arcsec and6arcsec pixels), with the fine
rung2x2. Keep physical smoothing/crop/rings fixed. Ring width is each
cube's own major-axis FWHM, and the outer edge is the last ring with at
least50% mask coverage, retaining holes. Sigma/noncircular terms use
six radial nodes. Sample residuals on a fixed physical lattice nearest
to sqrt(Gaussian beam area), rounded to an integer pixel stride, and
every second channel, anchored at the crop origin; report actual stride
and beam correlation caveat. This is the same approximate chi2 framework
as FN4a, not an exact likelihood for correlated interferometer pixels.

Known numerical comparisons: raw sums at32/64 row chunks<=1e-10
relative; header beams reproduce stated CLEAN records exactly; a point
source convolved by each beam has the correct second moments within2%
at supersampling5/9 (including box variance); constant field retains
unit DC response within1e-12. Natural map flux with original rounding
must reproduce262.8614460793164Jy km/s within1e-8 relative (a parser
anchor, NOT an observational acceptance gate). Independently regenerate
the natural coarse mask and ring kinematics and report differences from
FN4a; differences from physical beam-aware changes are not silently
called reproduction.

For graded fits require reduced-chi2 change<=5%, best inclination change
<=2.5deg, vc(2kpc) change<=2%, and unchanged physical/control flags
between rungs. Lattice/mask changes are included, not subtracted away.
Failed numerical checks mean UNDECIDED, not a retained best-rung result.
Natural/robust differences are reported separately and not averaged.

## Models and fitting, both footings

Preserve FN4a's four model families: free ring rotation, law, law plus
noncircular terms, and Newtonian baryons. Use its azimuthally averaged
in-plane FFT field and stated pressure-support form, with200pc thickness;
report100/300pc brackets. Do not replace this by the exploratory smoothed
Oh-profile fit from the diagnosis. Keep centre/PA/vsys/sigma/noncircular
bounds and the existing six-node noncircular representation documented
in FN4a's amendments. Report that representation rather than claiming a
more general harmonic model. Footings9.3603e-11 and1.1312e-10m/s2 never
pooled; Newtonian is a footing-independent control.

Law inclination grid15:5:60deg; noncircular15:7.5:60deg, followed by
bounded free-inclination refinement of each best grid result. This is
a frozen physical bracket, not a pass search. Free-model ring velocities
and geometry remain free as in FN4a. Use the original start plus a
second start with inclination35deg (other reference parameters unchanged).
Require status>0 for accepted fits; double max_nfev from initial100 to200
only as a predeclared optimizer-convergence check. Require accepted
best reduced-chi2 stable to1% and no gate flip; otherwise UNDECIDED.
Do not call a max-evaluation stop a converged optimum. Report all starts.

Conditional local-cube acceptance follows the old rules, without its
inapplicable external-benchmark substitution: M_free chi2_red<=1.5;
Delta chi2 to the law (with/without nc) <=chi2_0.95(k), k=extra free
ring-velocity parameters, and independent inclination24.5–45.8deg.
If the fit is acceptable only below24.5deg, retain that label. If every
tested inclination fails both law variants, report conditional GENUINE
OVER-PREDICTION on the tested grid/refinements only. If the free model
fails1.5, report NOT EVALUABLE even if the law is much worse. Do not
infer a universal exclusion between grid points or beyond this galaxy.

## Known answers and mutation

For EACH weighting, footing and numerical rung, use its own beam/noise
to generate a law mock at35deg, sigma9km/s, using reference geometry,
and a second mock with rotation0.505 times that law. Fixed noise seeds
SeedSequence([20261105,46,weight_index,foot_index,mock_index]), same
underlying physical noise convention across resolution pairs. Beam/
spectral-correlated noise must recover the measured voxel rms. KA1:
law mock accepted at35+/-5deg, free chi2_red<=1.5. KA2: slow mock
fails the law-vs-free line. These calibrate the conditional machinery;
they do not validate the real galaxy's thin-disc hypothesis.

KA3: Newtonian exceeds the same Delta-chi2 line on the real cube;
retain a failure of this expected outcome rather than forcing it.
MUTATE shuffles spectral channels with seed7 before fits, separately
for each prepared cube and rung. Free chi2_red must exceed1.5 and
the mutation verdict must reject local-cube evaluability (exit1 in the
grader). Keep all mutation files separate. No copied FN4a control numbers.

## Execution and deliverable

Each preparation, model, inclination/start and mock is a checkpoint
unit. Atomic writes, SIGTERM handler and resume identity checks are
required. Test byte-identical scientific output after interrupt/resume
on a small8x8-binned pilot before production. Reruns verify hashes of
raw inputs, source engines and criteria. Runtime/RSS are separate.

The full2x2/4x4 preparations and cube fits belong in heavyq, one thread,
after the light-tier work. Measure a pilot physical footprint and scale
the queue estimate conservatively; never start an unqueued >1GB fit.
Do not let a queued/pending state become a final lane label. The final
README must distinguish external benchmark NOT EVALUABLE, internal
controls, numerical/optimizer failures, each weighting/footing's local
conditional verdict, and all remaining work. Original FN4a stays intact.
