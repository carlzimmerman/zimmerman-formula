# P1D1 and X48 correction evidence

Executed under the parent closure plan's user-authorized disjoint scope. The
authoritative bounded run is `run_CORRECTED_002/manifest.json` (v2,
`run.status=completed`), validated against current inputs. Its stdout records
**8 tests passed**, and its results record peak RSS 59,736,064 bytes. The runner
records command, software, commit/dirty state, before/after input hashes and
output hashes. No full P1D likelihood fit or halo simulation was run.

**P1D1 result.** The actual historical shape/GLS kernels recover the independently
planted positive signal with mu=1.00000000393 and chi-square 4.32e-16. The same
injection fitted with negative SIGN gives mu=0 and chi-square 63.3333, failing
the regression. A sign-correlated negative injection reproduces the old false
recovery behavior. This uses controlled spectra and synthetic errors at fixed
nuisance; it does not calibrate physical flux response or survey power.
The completed historical data verdict remains NOT DIAGNOSTIC. Amendment A3 and
the lane's correction note supersede its upper-envelope interpretation and
independent-sign-test claim. Original frozen criteria, script and outputs remain
unchanged; corrected sign output is `run_CORRECTED_002/p1d1_sign_CORRECTED.json`.

**X48 result.** The actual historical random-draw block gives a shared-mode
mismatch 0.1760464 in dk/ng^3 between ng=8 and 16 and an rFFT round-trip boundary
error 43.89345 in dk. The helper's maximum shared-mode error across ng=8/12/16
is 1.55e-17. Hermitian/real-field round trips and Parseval pass on even and odd
grids. Four whitened-mode powers over 256 seeds are 1.0495, 0.9635, 0.9917 and
0.9906 against expectation 1; maximum off-diagonal covariance magnitude is
0.1016, below the predeclared 0.20 check. These finite statistics are not a proof
of arbitrary-seed independence or a continuum convergence result.

The new `x48_zoom_common.py` launcher is executable and tested in dry-run mode:
its transformed actual random-field prefix uses the helper, it starts no job
or cosmology load on dry-run, and it refuses an existing unmarked work directory.
It does not change the historical source or live jobs. See
`../../rebuild_2026_10_22/X48_native_cf_zoom/COMMON_MODES_CORRECTION_2026_10_27.md`
for invocation, cutoff conventions, resume restrictions and the remaining
post-constraint/force/softening/time-step/profile convergence obligations.

**Supersession of 001.** Independent review found that the first launcher masked
the draw but left P(k) unmasked in the HR correction and covariance. That can
reintroduce excluded modes and gives the wrong Gaussian conditional law.
`run_CORRECTED_001` is retained as historical evidence but does not validate
the launcher. `RED_HR_support_output.txt` reproduces the defect using the actual
transformed HR code: a normalized excluded coefficient of 0.0682337 exceeds
the declared 2e-14 tolerance. The current launcher applies one support mask
to P(k) for both draw and every covariance. The added regression checks output
support, unchanged retained P(k), constraint covariance and field-constraint
cross-covariance against an independent full complex-grid oracle; it also
checks achieved height/laplacian constraints. Cutoffs 1.5 and 10 at ng=8 test
both radial and Nyquist exclusions. Only the peak-target solve is replaced
by a fixed synthetic target (1,-2). No cosmological collapse is tested.

**Red/green evidence.** `RED_test_output.txt` records six failed assertions for
missing correction helpers before implementation; `RED_launcher_output.txt`
records the missing integration failure. The final bounded run passes all
eight behavioral tests, including independently planted sign mutation, actual
integration wiring, matching physical modes, real-field consistency, power,
covariance, band-limit and invalid-input checks. The harness also reproduces
the historical mathematical defects from the actual selected source code.

Ruling: execute the targeted suite only. The parent plan prohibits repository-
wide collection because research scripts have top-level output side effects.
Ruling: the helper and separate launcher are opt-in. Replacing the Gaussian
draw inside live or historical X48 jobs would invalidate their checkpoints.
Ruling: the new regression supersedes the retired P1D1 check; it does not
revive the inadequate forward model or reinterpret its fitted mu as physical.

**Verification:**

```bash
python3 closure_program_2026_10_27/technical_fixes/test_technical_fixes.py
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py closure_program_2026_10_27/technical_fixes/run_CORRECTED_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The manifest stores the full runner command; reruns require a **new** output
directory. Current outcome: implementation/finite assertions verified in the
stated range. Review provenance: independent reviewer `selector_audit` inspected the fix,
re-ran all eight tests and validated manifest 002; no remaining code blocker
within this declared finite scope. No commits were made.
