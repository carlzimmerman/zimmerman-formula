# WLJ1 C4 footing-isolation verification — 2026-11-14

The requested shared-C4-flag correction was already present when this audit began. No production-code change was needed. The current grader computes C4 known answers separately for canonical and alt (`wlj1_grade.py`, lines 42–43), and C4, CO1 and HLF1 consume the corresponding footing's result (lines 121–122). The same implementation is present at the previously cited revision `38b52055e1` and the script's first tracked commit, `6cce4d7328` (2026-11-14 03:42:20 -0500). The initial inspection HEAD was `e278b5be2f07b1bc9e6f9e44c420367117d2631d`.

The remaining global `KA_ok: false` in `wlj1_c4.json` is an accurate summary that at least one as-frozen C4 check failed. It must not be applied to both footings when grading them separately. Canonical's KA-R has `r_eff = 1.0000000000000002`; alt has `r_eff = 1.0`. This audit preserves those numerical inputs and the existing frozen/A1 distinction.

## Work added

- `test_wlj1_grade.py`: seven tests that execute the complete grader in temporary copies of its fourteen saved stage inputs. They check actual C4/CO1/HLF1 labels and row-24 labels, both footings, failed non-reference known answers, A1 tolerance acceptance/rejection, and a stale global summary. They also compare all six generated output files with the historical files byte for byte.
- `codex_fix_2026_11_14/audit_grader.py`: reproducible audit entry point. It creates a test-only mutant that pools the two C4 flags, confirms the regression rejects the mutant, runs the seven tests against the current grader, and copies verified outputs into the separate run directory.
- `codex_fix_2026_11_14/run_01/`: verified outputs, observed source copy, test-only mutant, red/green test logs, `comparison.json`, and a v2 computation manifest.

The test-only mutant reconstructs the reported shared-flag failure mechanism. It is not represented as an authenticated historical source revision. The actual production grader, historical outputs, `RESULT.md`, criteria, amendments, and paper were not edited. No commit was made by this audit.

## Verification and finite result

The deliberately pooled mutant fails on the actual `C4|REF|alt` output: `NO VERDICT` instead of `ROW HOLDS WITH THE SPLIT`. The current grader passes all seven tests. The six files `wlj1_grade.json/.out`, `wlj1_grade_asfrozen.json/.out`, and `wlj1_grade_MUTATE.json/.out` are byte-identical to their historical counterparts. Thus all existing amended numerical values, labels, brackets, twins and report conclusions are preserved.

For each graded split case `S1.25`, `S2`, and `S3`:

| Reading | Row 24 canonical | Row 24 alt | Row 25 canonical / alt |
|---|---|---|---|
| As frozen | NO VERDICT | ROW HOLDS WITH THE SPLIT | NO VERDICT / NO VERDICT |
| A1 + A2 | ROW HOLDS WITH THE SPLIT | ROW HOLDS WITH THE SPLIT | NO VERDICT / NO VERDICT |

This agrees with the existing `RESULT.md`. No report correction or new physical conclusion follows from this verification. In particular, it does not turn the weak-lensing amplitude row into a hold, erase the alt BX1 known-answer failure, or create a hit needing a blind regrade. The reported `Sinf` exceptions remain unchanged.

## Commands and provenance

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.

Regression command:

```bash
/private/tmp/forj0332-fit-venv/bin/python -I -B \
  closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/test_wlj1_grade.py -v
```

The bounded runner's exact argv is stored in `codex_fix_2026_11_14/runner_command.json`; its declared contract is `codex_fix_2026_11_14/contract.json`. The runner executes:

```bash
/usr/bin/nice -n 10 /private/tmp/forj0332-fit-venv/bin/python -I -B \
  closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/codex_fix_2026_11_14/audit_grader.py \
  --output closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/codex_fix_2026_11_14/run_01
```

The runner creates the fresh output directory before invoking that command. Repeating a recorded run requires a new output directory and matching declared result paths. The helper always runs `wlj1_grade.py` and `wlj1_grade.py --as-frozen` in disposable copies; invoking the historical grader directly in its source folder would overwrite historical outputs.

Observed environment: computation Python 3.9.6, NumPy 1.26.4, SciPy 1.13.1; runner Python 3.12.11; macOS 26.5.2 arm64. `/usr/bin/python3` lacks NumPy and was not used for numerical grading. The recorded run started at `2026-11-14T18:48:14.776831+00:00`, completed in 18.260291 seconds, and exited 0. Bounds were 90 seconds wall time, 60 CPU seconds per process, 1 MiB combined logs, and conventional numerical-library thread variables set to 1. CPU affinity and an address-space cap were not enforced; the run only read approximately 4.8 MiB of saved lane files and performed grading, with no numerical-stage rerun.

The v2 manifest records repository revision `0aee9d1a75fb53af9f2a3b143cf7679fd47f5c36` and a dirty workspace. HEAD advanced concurrently; all 27 declared input artifacts were nevertheless unchanged before/after the run, including source, saved stage inputs, historical outputs, criteria and result note. The grader's observed SHA-256 before and after was `c77e6f2dd41084287ff102066d77ceb38e6f0c52c1bade62cb4251e3e2b5bb80`. The manifest contains every individual before/after input hash and result hash.

Manifest validation command:

```bash
/opt/homebrew/bin/python3.12 -B \
  /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/codex_fix_2026_11_14/run_01/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Observed result: `valid evidence record (run status: completed); mathematical interpretation requires review`.

Outcome: the C4 footing-isolation implementation and the stated finite grading assertions are verified for the saved WLJ1 fixtures and controlled regression variations. The upstream halo-model, C4, shear, KL1/BX1 and LWB computations were not independently validated or rerun. No repository-wide test command was identified; unrelated research scripts were not executed. This is a grader regression and reproduction audit, not an independent physical regrade or theory closure. Adopts nothing; kappa = 1/2 remains FITTED.
