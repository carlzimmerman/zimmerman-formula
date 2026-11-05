# IN PROGRESS — diagnosis complete; beam-aware cube redo frozen

Kappa=1/2 FITTED; not theory closed. DIAGNOSIS.md records the preliminary
investigation committed in a8f468e93c. It reproduces both old discrepancies
and identifies beam/weighting and derivative/velocity-field comparison
issues without changing FN4a's verdict. The full table-to-map mass origin
remains unidentified; missing reference products are in NEEDS_OWNER.

Criteria e3d557204a now freeze the independent cube redo: each weighting's
own beam/mask/noise, both a0 footings,2x2/4x4 numerical pairs, original
model families and mass/thickness brackets, mock controls, shuffled-
channel mutation, optimizer checks and preemptible heavy-queue execution.

No new preparation or production cube fit has yet run. The implementation,
small pilot/footprint/resume contract, queue submission and final physical
labels remain required. External benchmark NOT EVALUABLE is distinct
from any future conditional local-cube verdict. This is not a completed
lane12 result.

## New beam and raw-reader checks: partial numerical failure retained

The new io_beam.py reads each cube's own CLEAN header and integrates its
Gaussian over pixel boxes once. It does not carry FN4a's natural beam into
the robust cube, nor add another Gaussian box variance before subpixel
integration. check_beam.py applies the already-frozen2% second-moment line
at3/6arcsec pixels and5/9 subpixel quadrature. It passes16/18 checks.
Natural weighting and the3arcsec robust grid pass; the6arcsec robust grid
fails the minor-axis moment at both quadratures: relative errors6.3024%
and5.3341%, versus the2% line. Increasing quadrature from5 to9 changes
that moment1.0229%; the continuous Gaussian-plus-box moment is still not
recovered on this coarse sampled grid. No tolerance was changed, and no
moment-matching adjustment was made to obtain a pass. This is an open
numerical obstruction to the robust coarse/fine cube verdict, not a
physical rejection of the galaxy or action.

MUTATE substitutes the natural beam for the robust beam. The correct
robust CLEAN-header anchor passes in main and fails in the separate
mutate/beam_checks.json. This specific changed check establishes that the
control bites, independently of the main run's existing moment failures.
Both a0 footings share these geometric checks; no field fit is graded.

check_io.py passes4/4: independent Astropy-section agreement at32/64 row
chunks, row-sum convergence1e-10, and exact recovery of the rounded
262.8614460793164Jy km/s parser anchor. This remains a parser test, not an
observational flux acceptance. All three scientific JSONs are byte-identical
on fresh repeats, including the beam failures. Commands in the installed
conda environment:

    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_io.py
    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_beam.py

The first exits0; the second deliberately exits1 for the two failed main
checks. Full cube preparation, interrupted/resumed pilot, physical footprint,
queued fits and local-cube grading remain pending. The external published
benchmark remains NOT EVALUABLE for the separately documented missing data.

## Bounded stellar-profile preparation

stars.py computes the V-image WCS and radial samples in row chunks, using
fixed Oh geometry, the original background region beyond1500arcsec and
first-nonpositive-annulus truncation. check_stars.py passes7/7 checks:
32/64-row scientific outputs are byte-identical at the original13.2arcsec
spacing and the two beam-major-axis spacings; the original background,
half-light radius301.047383arcsec and cut976.8arcsec are recovered exactly;
a cooperative stop is observed. A fresh complete checker run is also
byte-identical. The natural/robust spacings give half-light radii301.060780
and304.027831arcsec; both profiles are saved, with no pooling or new mass
calibration. Constant M/L and the two frozen mass normalizations remain
assumptions. This does not resolve the failed coarse robust beam check.

Runtime is about1.4seconds; peak RSS442MB. FITSFixedWarning header repairs
(deprecated RADECSYS and legacy DATE-OBS spelling) initially stopped the
warnings-as-errors test. The final code preserves Astropy's original WCS
interpretation and explicitly records those repairs, while leaving other
warnings as errors. Raw headers/files are never edited. Full cube/mask
preparation and interrupted/resumed8x8 pilot remain the next required work.

    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_stars.py

## Restartable raw-cube stage and spectral correction

Amendment2ab4024308 was committed alone after the first raw prototype,
before any new cube fit. FELO-HEL is not a linear optical-velocity axis:
the old expression differs from the header's spectral WCS by up to
0.06207714km/s for both cubes. The corrected worker uses spectral WCS;
an independent optical Doppler calculation agrees within5.12e-11km/s.
This is a coordinate correction, not a changed physical acceptance line.

raw_cube.py reads/crops/bins planes with rolling, hashed, atomic checkpoints.
Full2x2/4x4 work is refused outside heavyq; the8x8 pilot is allowed. All16
known-answer checks pass, including exact synthetic binning and independent
Astropy real-plane access. All13 raw-stage contract checks pass: both cubes
complete at32/64 row chunks with identical scientific fields/array hashes;
a live SIGTERM after the first committed plane exits75; resume reproduces
the uninterrupted manifest byte-for-byte; complete resume exits0; stale
identity is rejected. Each pilot uses107x150x150 voxels and 144–187MB
peak RSS across the two row sizes. Full physical footprint will be measured after mask/model pilot
preparation, not inferred from RSS.

    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_raw.py
    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_raw_resume.py --tag fresh_raw_contract

The second command requires a fresh tag and regenerates the pilot artifacts.
Compact manifests and verification output are committed; cube/coordinate
NumPy arrays and per-plane rolling checkpoints remain local reproducible
runtime artifacts, identified by hashes in those manifests. raw_contract/
is the superseded pre-A1 prototype and must not be used as production input.
raw_verified/ holds the current tested raw pilots. Neither is a finished
mask preparation or a cube fit; the existing robust beam failure remains.

## Complete8x8 preparation pilot

masking.py implements own-cube noise, physical smoothing, component
selection, dilation and the beam-based sampling lattice. Its10 synthetic
checks pass, including source recovery, a negative-source mutation and
rejection of an empty emission mask. prepare.py adds the shared natural
PB gas map, own-width stellar profile and mask-based ring extent, with
atomic stage checkpoints and strict raw-input/source/output hash checks.
The grid is anchored at crop pixel0 and native channel0. Physical dilation
uses the actual header pixel scale; boundary pixels are selected by the
stated12arcsec distance, not a transplanted nominal-pixel stencil.

All19 check_prepare.py checks pass. Natural/robust masks and beams differ;
noise at this pilot binning is0.221714/0.188885mJy per beam. Their common
gas-map files match byte-for-byte. Both complete; live SIGTERM exits75;
resume reproduces every stage manifest and final manifest exactly; an
independent fresh repeat matches. Known map block means and disc geometry
pass, and a mismatched map/cube grid is rejected. Peak RSS283/335MB in the
baseline pair; macOS physical footprint of a separate robust pilot peaks
at140,772,384bytes over17 samples. That measurement covers preparation,
not the still-unimplemented new fit worker or full-resolution memory.

    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_mask.py
    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_prepare.py --tag fresh_preparation_contract

The second command uses raw_verified/baseline/ raw inputs and requires a
fresh output tag. Masks and prepared arrays remain local runtime artifacts;
compact stage/final manifests, hashes and verification outputs are committed.
No8x8 pilot is a numerical convergence pair or a local-cube verdict. Full
2x2/4x4 preparation remains queue-only. New forward model, mocks, fits,
physical-footprint scaling, full-resolution comparison and final grader
are still required. The coarse robust beam failure is unchanged.

## Forward-model implementation checkpoint (not fit-qualified)

model.py loads only hash-verified preparations and uses each cube's own
beam, pixel scale, noise and mask. Before any new fits, the inherited
four-pixel border is expressed as 24 arcsec and the force grid's radial
extent as 960 arcsec (the old 160 bins at 6 arcsec). This preserves physical
scales across the future resolution pair. The original empirical Gaussian
line amplitude and data-dependent local intensity normalization remain;
these are conditional cube-model assumptions, not a generative action.
The new fitter must not inherit the old fixed-ring Jacobian sparsity:
changing geometry and beam convolution invalidate those exact zeros.

The initial check_model.py checkpoint passed 14 of 16 checks and exited 1. The independent
softened point-mass FFT comparison differs by 3.40e-16 relative. The old
force calculation is reproduced exactly on an identical explicit radial
grid, for Newtonian/modified gravity on both footings. Both prepared pilot
cubes load their own beams and produce finite forward predictions. A wrong
velocity control fails, and a compact Gaussian source is recovered within
6.67e-16 absolute error.

At that checkpoint the two original extended-source tests FAILED at their unchanged
tolerances. Maximum line-profile error was 3.6402e-10 at channel/pixel
(15,0,40), where the data value is 7.8492e-6. Interior error is 7.78e-16.
The fixed border removes intrinsic light at those corners; normalizing
tiny beam leakage there amplifies floating-point error. The compact-source
check is a separate diagnostic, not a replacement or waiver. The model has
not been shown numerically safe for fitting all selected real-data pixels;
that limitation must be resolved or propagated before any fit verdict.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_model.py

Use the recorded NumPy/SciPy/Astropy environment. The saved runtime is about
2 seconds with peak RSS about 255 MB; it does not establish fit memory use.
Mocks, optimization, fit restart tests and production convergence remain
pending. kappa = 1/2 FITTED; not theory closed.

## Dense fitting implementation and arithmetic fallback

MODEL_NUMERICS.md was committed before these implementations. model.py
now recomputes weak positive-intensity pixels by direct summation of the
same full periodic beam kernel. No physical mask, beam or tolerance is
changed. The extended-source maximum error falls to 1.638e-12, but both
original tests still FAIL: check_model.py remains 14/16, exit 1. This is
an improvement in arithmetic, not a successful numerical qualification.
The original 3.6402e-10 failure remains in commit 8a18286e8e. Selected
pixels at one reference evaluation of the real 8x8 pilots contain neither
border pixels nor fallback pixels; other geometries are not certified.

fitting.py provides free-ring, law, noncircular and Newtonian model
parameterizations with dense finite-difference Jacobians, original bounds,
six radial dispersion/noncircular nodes, and signal checks at each residual
boundary. Pressure smoothing preserves the original 30-arcsec physical
width with explicit cell-overlap weights and reflected boundaries. Frozen
production budgets are 100/200; the separate two-evaluation implementation
pilot is explicitly ineligible for production acceptance even if stationary.
The fit summary records status, evaluations, parameter count, residual calls
and fallback use; it does not issue a local-cube verdict.

check_fitting.py passes 14/14 bounded synthetic implementation checks:
original 6-arcsec filter reproduction, 3-arcsec half-weight endpoints,
independent top-hat cell integration and DC response, exact free-model
truth recovery, stationary optimizer, explicit pilot ineligibility,
wrong-systemic-velocity control, interruption, constant-density pressure
support, independent projected velocity and noncircular harmonics. These
are not the frozen noisy KA1/KA2 mocks. Restartable fit workers, matched
physical noise, real-data fits, footprint measurements and full convergence
comparisons remain pending. The beam and extended-source failures remain.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_fitting.py

## Restartable individual fit units

fit_unit.py implements one model/inclination/start unit with atomic outputs,
source/preparation/version identities and flag-only signal handlers. An
interrupted optimizer unit restarts from its identical input; completed
units verify their result hash and return without refitting. Fixed-inclination
law-family results can seed a free-inclination refinement after identity
checks. Real and seed7 channel-shuffle datasets are supported, with shuffle
outputs required in a separate mutate tree. The noisy KA1/KA2 datasets and
full grid orchestration remain to be implemented. Every production fit is
heavyq-only; the sole unqueued allowance is bin8 with budget2.

check_fit_resume.py passes 12/12 checks in each of two independent fresh
runs. Each sees a live fitting checkpoint, sends SIGTERM, observes exit75,
and resumes to a byte-identical result. Independent repeat and completed
resume also match exactly. Changed start identities, unqueued production
budgets and mutation outputs outside their own tree are rejected. Both
complete check reports and all six fit results match across the two runs.
The free-model pilot stops at its two-evaluation budget (status0), and the
acceptance flag stays false. Its reduced chi-square is an ungraded early
iterate, not evidence for a physical or local-cube conclusion.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_fit_resume.py --tag fit_verified/fresh_contract

Use a fresh tag. Compact reports, scientific results and runtimes are
committed; temporary execution checkpoints and logs remain runtime artifacts.
A separate identical pilot completed in4.19seconds. macOS footprint sampled
46 live-process records, with peak physical footprint284,607,952bytes
(0.285GB); RSS high-water was904,806,400bytes. These are distinct memory
measurements. The physical measurement is saved in
fit_footprint_measurement.json and its scientific output matches the baseline.
It does not yet establish the full-resolution, robust-ring or production
optimizer memory bound. Full mocks, fit grid, refinement/bracket execution,
numerical comparisons and final grading remain pending. No queue submission
or fit verdict follows from this checkpoint.
