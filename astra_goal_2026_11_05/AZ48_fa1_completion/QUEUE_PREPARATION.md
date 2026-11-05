# NOT SUBMITTED — Bullet3D worker qualification

Kappa=1/2 FITTED; not theory closed. Retired sector, adopts nothing.
This is preparation, not a completed production or convergence calculation.

The frozen FROZEN_BULLET.md already required a signal-aware worker before
production. worker3d.py now stores the field and complete solver state in
one atomic NPZ checkpoint: same-directory temporary, flush/fsync, replace.
Every accepted Newton step is saved. Handlers only set a flag. The matrix
operator checks that flag before each application, so a request need not
wait for all400 applications. On interruption the worker saves the latest
accepted state and exits75. It resumes with the same source/criteria/code,
arguments and Python/NumPy/SciPy identities. A completed result is verified
against both field and report hashes before idempotent exit0.

The first live test recovered the exact field but exposed JSON key-order
changes after restart. Canonical result serialization fixes that, without
changing numerical operations or loosening the exact-equivalence rule.
Current direct and100/10/1 homotopy tests each pass12/12, repeated in fresh
folders: contract_d/e and homotopy_a/b under worker_verified. Each sends a
real SIGTERM after observing an accepted step, receives75, resumes, and
compares both scientific files byte-for-byte. The additional checks reject
changed footing, damaged field and unqueued N32; --resume without a
checkpoint starts normally. The homotopy boundary correction adds the new
spherical radial potential minus the old one at each epsilon transition.
Its final stage always uses physical epsilon. A bounded failure produces
UNDECIDED, not a successful physical grade, even though the worker exits0
because its bounded task has finished.

    python check_worker.py --tag NEW_DIRECT_TAG
    python check_worker.py --tag NEW_HOMOTOPY_TAG --homotopy
    python measure_worker.py --tag NEW_MEMORY_TAG

Run from this lane with the numerical dependencies and one-thread variables.
Fresh tags preserve older evidence. Binary arrays/checkpoints stay local;
compact reports and their array hashes are committed.

## Memory and disk estimate, not a measured production bound

measure_worker.py uses macOS proc_pid_rusage flavor4, including the lifetime
maximum physical footprint. The N16 Bullet canonical homotopy pilot exits0,
converges at the residual gate and yields90 samples. Lifetime physical peak
is54,412,080bytes (0.0545GB rounded up). This is not RSS. The result hash
matches the independently repeated homotopy run.

For queue requests reserve1GB for runtime/base overhead plus twice a
96-full-grid-float64-array allowance, rounded up to an integral decimal GB:

    est_gb = ceil(1 + 2*96*8*(N+1)^3/1e9)

This covers the21-vector restarted-GMRES basis, old/trial Hessians, residuals,
source, radial/boundary/field arrays, Jacobian temporaries and checkpoint
copies with additional headroom. It is deliberately conservative relative
to the small measured pilot; cubic extrapolation is an estimate and must be
checked against observed queue footprint at each larger rung.

| intervals | reserved GB | field bytes |
|---|---:|---:|
|32|2|287496|
|64|2|2197000|
|128|5|17173512|
|256|28|135796744|

At N256 an old/new checkpoint pair plus final field requires about0.408GB,
plus small metadata; reserve0.5GB per run for these artifacts. Checkpoints
are rolling, not one copy per Newton step. These estimates stay below the
queue52GB hard ceiling and do not waive its free-memory or disk gates.

No jobs have been submitted. Before submission complete the light-tier
labels, inspect live1024-cubed/other queue work, and add only through heavyq.
Still needed: postprocessing/known-answer/convergence grader, frozen physical
Plummer32/64/128 on both footings, Bullet64/128/256 and N256 expanded box,
plus separate selector-sign mutation output from each converged field.

## Saved-field analysis restart qualification

sample_field.py now has a separate atomic sampling_checkpoint.json. Its
identity binds the field/report hashes, sampling sources, mutation mode and
numerical environment. Completed disc quadratures are retained individually;
on resume the deterministic Hessian/physical residual is reconstructed from
the saved field, then completed disc work is reused. Signals only set a flag;
safe points save state and exit75. Completed sampling verifies its result
hash before idempotent exit0, and stale/damaged outputs are rejected.

Live tests wait until at least one disc result is actually checkpointed,
then send SIGTERM. Main and sign-reversed tests each pass9/9, repeated in
fresh folders with exact scientific output and exact compact test reports.
The independent saved-field integration suite remains11/11. Comparing
pre/post-checkpoint reports after removing the changed source hashes finds
identical scientific values; no numerical method or gate changed.

The N16 sampler measurement uses33 macOS samples and records lifetime
physical peak45,154,928bytes (0.0452GB rounded up). Its output hash matches
the independently checked baseline. Keep the existing conservative memory
reservation for queued analysis too; the smaller pilot does not justify
reducing the unmeasured large-grid allowance. The sampler keeps only compact
checkpoints in addition to the existing field artifact.

    python check_sample_resume.py --tag NEW_TAG
    python check_sample_resume.py --tag NEW_MUTATION_TAG --mutate
    python measure_worker.py --tag NEW_MEMORY_TAG --stage sample

No production jobs are submitted by these tools. Authenticated aggregation
of physical ladder evidence and all actual production runs remain pending.
