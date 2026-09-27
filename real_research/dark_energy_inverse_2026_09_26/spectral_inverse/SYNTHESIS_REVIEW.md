# Independent CD26-3 synthesis review

Date: 2026-09-26. Scope: the campaign README and only the CD26-3 amendment
near the recipe top, compared with the spectral inverse report and the
pressure/expansion reconstruction. Science sources and recipe were read only.

**Verdict:** no substantive mathematical contradiction found. The one small
domain omission identified below has been corrected and verified in both files.

## Finding

The initially reviewed README pressure-null display and recipe's “Add the
inverse pressure test” bullet omitted `a0(0) != 0` and `Q(z)>0`, which the
reconstruction report states explicitly at line 118. The author added those
conditions locally; direct inspection confirms them at README line 34 and
recipe line 81. The finding is **resolved**. This was a presentation omission,
not a failure of the conditional identity. No observational fit has been claimed.

## Scope retained correctly

- The pressure law is proposed, its common-action origin is open, and an
  allowed constitutive input is distinguished from a derived origin.
  `epsilon=Pi+D/a^3` retains independent density/charge data without turning
  that mathematical constant into a particle requirement.
- Effective Einstein-form pressure is distinguished from an identified
  material or vacuum stress. “Cosmic tension” is explicitly provisional;
  the evidence does not establish that this is nature's selected microscopic
  interpretation.
- Lapse inversion identifies `A/b` for positive lapse. Its spatial-constancy
  test needs source, geometry, proper-expansion and coupling calibration.
  The positive/zero/negative vacuum counterfamily really does preserve the
  stated lapse, source and expansion by changing the trace coupling. It is
  a result of the declared CD26-2 cosmological sector, not a proof that this
  sector is already embedded in the operative filtered `nu_mono` theory.
- The unequal Newton/cosmological couplings, unfiltered-kernel control scope,
  observational covariance and remaining full-action obligations are retained.
  Neither the README nor amendment turns the scoped Lean certificates into a
  complete field-theory or observational certification.

The reconstruction compiler's pending issue is now resolved by the actual
successful attempt3 record and log, as recorded in
[RECONSTRUCTION_REVIEW.md](RECONSTRUCTION_REVIEW.md). Six declarations have
only the standard printed axioms; three lint warnings are harmless.

## Reviewed versions

- `../README.md`: SHA256
  `ff62611a69949363b7d6df6c71bf970fcbfd48dd06417ef1bd5c8b7a02f3c42b`.
- `../../../qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md`:
  whole-file SHA256
  `9644fa82f6ca98eaa895f1da44d87a365d6bb8bdce3c9796d9b87bbcbef87339`;
  reviewed scope is the CD26-3 amendment at lines 64–118.
- `../reconstruction/RESULT.md`: SHA256
  `0289761bf2a9924306dd7ef9d7060deeb61e795f12232d18b0cb2141ee37a766`.
- `../reconstruction/check.py`: SHA256
  `9c10d252e6e73470aa023880d12c453f34cfae9b9f3218b2c261c3ab3f09157d`.

The shared tree may advance concurrently; these hashes delimit this review.
Before the domain clarification, the README hash was
`a898e5b0e58434b0b859da9febec52b971ac9aed0d1f6639f451f41016b95472`
and the recipe hash was
`85666d8e57f7184a0c2dee1a7afbaa55eb0a4d85f4019b491505a44fef7f51f3`.
External-source authentication and the other agents' gate/clock derivations
were not independently repeated in this bounded synthesis review.
