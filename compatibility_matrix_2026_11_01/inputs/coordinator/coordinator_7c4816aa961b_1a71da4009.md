# CRISP FINDING: the corrected rule links switch position to core amplitude

The actual X43-A canonical equality at the old empirical midpoint logM=12.3 requires
**L=2.5090648745652686**. This is the single predeclared refit challenge. It is the same sole L applied everywhere,
not another independent T or a blind prediction. Compared with L=3.75/3.9/4, its collapse contribution is multiplied
by **0.6051329184 / 0.5761812275 / 0.5582321874** before the max floor is taken. A later switch therefore carries
a substantial, unavoidable reduction in the same collapse term. The actual corrected-definition challenge
passes lensing but fails canonical groups at Z=+2.6219198092. It does not rescue joint calibration.

The first scalar packet used displayed a0 rather than the extra FP0 digits imported by X43. Its derived
L=2.5090595510216196 was2.12ppm too low for the same frozen target. That packet and initial observational run
are retained. `precision_001` corrects this implementation precision error without a new target; the final
calibration `run_008_exact_challenge` and heldout `run_011_challenge_actual_floor` use the actual definition. None of the
lens-support, actual-floor heldout/LG or UFD conclusions changes. Frozen inputs of old runs were preserved.

There are also genuine necessary bounds for the fixed scorer, and an exhaustive alt obstruction:

| Footing | Necessary LG-on lower L from graded-A MW | Necessary lens-support upper L | Fixed UFD class |
|---|---:|---:|---|
| canonical | L > 2.4807124171 | L <= 5.0068312348 | halo Z=-1.90821 passes; law Z=+5.21661 fails |
| alt | L > 2.8865454081 | L <= 5.8258950322 | halo Z=-2.77500 and law Z=+4.87441 both fail |

The alt UFD conclusion is exhaustive over every positive L **for the unchanged X51 profile and fixed LG basin**:
all31 MW ultra-faints share one LG selector, and their halo/law profiles have no remaining L dependence.
The two states were independently reconstructed, including the original bootstrap, and reproduce both cached
scores exactly. A new L alone cannot pass this alt class. This conclusion does not extend to a revised dwarf
profile, error model, membership or new parameter. Canonical remains open inside the displayed necessary interval;
the interval is not sufficient and no all-L canonical calibration exclusion is proved here.

The upper lens cap is not the old empirical T window. It is a model identity: above that cap every positively
weighted interpolation node is halo, so ENV equals pureHalo and its frozen strict improvement condition fails.
Actual support has127 distinct stellar-grid nodes and181431 lenses in the four scoring bins. The lowest support
node has logMstar=8.52 and inferred logM200=10.6018893461. Calibration independently extracted and exactly matched
the four bin supports and native ranges. L3.75 still has a nonzero law tail, so this cap does not by itself explain
the measured L3.75 lens failure or rule out the interval below the cap.

## Scalar roots and pipeline conventions

Corrected X43-A roots, using the actual X43 rounded-PC floor conversion:

| L | canonical logM | alt logM |
|---|---:|---:|
|3.75|11.2232524490|11.5492201188|
|3.9|11.1394614344|11.4645010481|
|4|11.0854975034|11.4099455027|
|single challenge|12.3000000000|13.2958985022|

The same challenge gives X43-B roots12.4587243837/13.3480578211 and X53 cached-A roots12.3141466046/13.3005653999.
These differences are inherited representations: X43 freshly evaluates each background's CLASS/EPS column;
X53 interpolates the five-point cached background-A column and uses its own Gpc conversion. The actual switch
must compare the same column/floor used locally by its corresponding core. One diagnostic T is not a universal
replacement for those direct flags. Old CL3's precise-PC constant-L roots reproduce within1.31e-8 dex; old
independent consistent roots reproduce within2.07e-8 dex under the old diagnostic floor convention.

## Independent implementation review

`review_001` independently recomputes all2646 heldout selector columns and flags from original full-precision S9
and the saved native column table: zero violations and maximum relative column discrepancy1.11e-16.
All2112 MW logs use the original LG primary mass2.468826477849833e12, rather than the summed-baryon variant.
All S9 concentration knots match exactly. The heldout source restricts L to the halo column and selector;
its cache contains L-independent baryonic fields/observables. Author baseline controls reproduce the old BS1
primary, and unchanged-L4 replay matches the baseline. This is an independent selector/semantics review,
not a second raw MW/dwarf data reduction.

The calibration source leaves corrected X43/X53 direct comparisons intact by omitting the `_T` override,
changes SPARC basin flags through the same sig_core callable at parent mass, and retains own-mass profile
amplitudes. A precision issue in the first script's `{L:g}` challenge tag was reported; `calibrate_audited.py`
uses17 significant digits. `calibration_review_002` independently recomputes57920 positive primitive columns
with maximum relative discrepancy3.55e-15, exactly matches floors and finds no direct-predicate disagreement.
Its14000 own/basin amplitude/flag checks have zero violations and maximum relative discrepancy1.89e-15.
Normal wrapper violations are zero; the actual input-flag mutant has8806 violations. Twelve old baseline
comparisons and164 applicable harness controls pass. The final target column/floor ratio is0.9999999999999999.
Legacy X43 old-budget/floor controls and point-mass X53 checks on law witnesses are explicitly classified
from their source assumptions; caught exits are preserved, not recast as successful original-scorer exits.
Full calibration and challenge grades are owned by calibration/; this lane does not substitute scalar identities
for those grades.

## Provenance and regeneration

- `run_001` and `run_002`: independent CLASS/EPS scalar audit,9/9 checks, byte-identical results SHA256
  `1b642b7d99946497c87d18175cd855d27fff59e6d1cdb41b3a081a04a28e3580`.
- `run_003_MUTATE`: q divided by two only in the direct formulation; algebra, branch, prior-root and challenge
  checks fail, exit1 as intended.
- `support_001` and `support_002`: exact interpolation-support reduction,8/8 checks, byte-identical results SHA256
  `536373b737f46a809ace38d1ea8801f8802a9ce2fab67f3516cb90e45b9e10e0`.
- `support_003_MUTATE`: one support coefficient corrupted; interpolation identity and conservation fail, exit1.
- `review_001`:7/7 independent heldout selector/support checks.
- `lg_001`:6/6 necessary LG threshold and cached law-state checks.
- `ufd_001`:6/6 exhaustive UFD state reduction and independent bootstrap checks.
- `precision_001`:3/3 actual-FP0 correction and logged-floor checks; the original packet remains unchanged.
- `calibration_review_002`:10/10 independent final primitive and challenge checks. `calibration_review_001`
  is a retained pre-science path-normalization failure; v2 uses resolved source paths.

The extra `review_heldout_challenge.py` helper and its criteria were prepared but not executed; they are not
evidence. The completed primary heldout selector review and coordinator's final four-level reconciliation
are the applicable records. No further investigation was undertaken after checkpoint closeout was requested.

Each run has a v2 bounded-runner manifest, exact child argv, before/after input hashes and hashed outputs.
Use its matching contract and complete `execution_artifacts` list as repeated `--input` arguments under the
installed computation-audit runner, with a fresh output path. The scripts' `--output` argument writes that
same path. No existing output directory should be reused. Interpreter is isolated Python3.13.9; NumPy1.26.4,
SciPy1.14.1 and classy v3.3.4 where used. Wall limit60s, CPU50s, one-thread environment, nice15 requested
(any platform denial remains in stderr). The scalar run
took7.758495s at0.132GB observed peak RSS; support run took0.388667s at0.169GB. macOS RLIMIT_AS is not requested.

`FROZEN_CRITERIA.md` and its pre-result amendments govern the first scalar packet; each later mathematical
discriminator has its own pre-arithmetic criteria. No earlier frozen file was changed after serving as a run
input. Base checkout is2c6b17d683c1a69a1c95754c255de1cc6f79800a with dirty files preserved. No commits, historical
lane writes, simulations, downloads or live-job changes were made by this subagent.

The record check covered shared rebuild/doors briefs, CL2/CL3/LEE1, the prior native_l_t audit, X43/X53/F2,
X51/HO2/BS1 and bounded searches in campaign ledgers, candidate-law register, DS final, argon, why-4, time and
core-open-problem trees. No closed expensive route was rerun. Kappa=1/2 remains fitted; both footings stay separate.
CLASS/EPS reproduction validates finite formulas under recorded inputs, not EPS physics or a condensation law.
