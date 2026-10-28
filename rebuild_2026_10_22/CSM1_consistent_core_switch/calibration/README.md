# Corrected same-function calibration: previous passes do not survive

The three previously used levels fail the actual KiDS lensing criterion on both footings. At these levels SPARC (both backgrounds, own and BS1 basin flags), 63 groups and all 15 cluster keys at both h values still pass. No independent T or fitted number was added. The canonical one-L challenge restores lensing but loses groups.

| L | canonical lens Δχ² versus law | alt lens Δχ² versus law | canonical groups Z | result |
|---|---:|---:|---:|---|
|3.75|+415.281018|+422.597116|+1.931923|lensing fails|
|3.9|+420.306421|+425.782862|+1.892021|lensing fails|
|4|+423.234303|+430.293059|+1.866611|lensing fails|
|2.5090648745652686, same-target challenge|0|0|+2.621920|canonical groups fail; altSPARC fails|

The lens limit is Δχ²≤9 versus the law, and improvement over the pure-halo comparator. The three normal levels improve over pure halos but remain strongly worse than the law. The challenge uses the sole L giving **actual X43 canonical background-A** crossover logM12.3. It changes the existing one free normalization; it adds no independent threshold. These finite cells do not prove that every possible L fails.

## Model and assumptions

For each L the original S9 concentration shape is retained:

    eta(M)=4/(3B(1)) [L*S9(M)/S9(1e14)]^(5/4)
    core(M)=max(floor,eta(M)*Sigma_coll(M))
    flag(Mselector) = eta(Mselector)*Sigma_coll(Mselector)>floor.

SPARC keeps its own core amplitude and uses the **same actual sig_core** at the selected BS1 basin mass (own-mass fallback). Background B uses its own exact EPS function. Groups/clusters keep their original own mass assignment and GS1 measured gas budget. KiDS lenses use their original own mass and X53 coarse collapse table, with the direct inequality from their actual core calculation. The model retains its original units and slightly different precise/rounded footing constants in these scorers. Kappa=1/2 remains fitted; S9 convergence/transfer, backgrounds, EPS and basin physics remain assumptions.

## Baseline, independent checks and mutation

Before corrected interpretation, the full old raw CL3 L=3.75 R43 footings reproduce all 315 leaves exactly, including all 15 keys at both h values. R53 reproduces all 1,964 leaves exactly. Original X53cf4 halo scores also reproduce. See `baseline_full_comparison.json` and the baseline in run003.

The bounded audited program independently repeats L=3.75; pinned-reference replays repeat3.9/4. All three full grade dictionaries are **bit-identical** to the uncached pilot. Cached T2 is the actual first computed fixed-spectrum/radius/exclusion template and a repeated old baseline agrees in all four primary/all model scores to1e-6 before use. Only three explicitly reported ungraded variant stacks were omitted.

`columns_final` independently implements CLASS/EPS for both backgrounds and separate coarse-table arithmetic. It checks71,772 actual callback records (including repeated calls and2,268 inherited eta=0 control records),8,400 selected-mass records and the strict inequalities: maximum positive-column relative error3.553e-15, floor error0, flag disagreements0 and selected-mass disagreements0. This shares CLASS with the source and does not validate its physics.

`run_005_MUTATE` actually inverts every physical input branch flag before the scorer combines forces:8,806 of 8,806decisions are detected; its numerical profiles and grades change, and it exits1 as expected. The unmodified pure-halo comparator has2,010 non-inverted flags. Source n_active counters in the mutant describe the pre-inversion predicate; actual FLAGS records determine the control counts.

The inherited source self-checks are retained with caught source SystemExit statuses. X43 K0 compares pre-GS1 budget references and K0x38 assumes an unconditional floor halo; X53 K_T assumes a truncated halo even when the actual branch is the law. These inapplicable checks are not silently called passing. Independent baseline, column, floor and actual-branch controls supply the relevant gates.

## Why the lens result changes

There are181,431 positive-weight lenses and362,862 nonzero interpolation-node contributions. AtL=3.75, halo flags affect321705contributions(88.66%) on canonical and266328(73.40%) on alt. After actual source weights and interpolation coefficients, the halo contribution fractions are96.29% and86.28%. At the exact challenge all positive-weight support is on the law:0of127unique support grid nodes are halo on either footing. These are actual estimator support counts, not repeated kernel-call counts. `support_final/results.json` includes per-bin counts and fractions.

AtL=3.75 actual X43A crossover logs are11.2232524490/11.5492201188(canonical/alt), versus retained X53table11.2262903897/11.5535814869. At the exact challenge these are12.3000000000/13.2958985022 versus12.3141466046/13.3005653999. Exact background-B roots and grid diagnostics remain in full JSON. No exact-EPS replacement of the primary X53 representation was made.

## Authoritative evidence and reproduction

- `run_003_audited`: baseline/replay and correctedL=3.75, completed.
- `run_004_replay`: pinned-baseline correctedL=3.9/4, completed.
- `run_005_MUTATE`: expected failed mutation control.
- `run_008_exact_challenge`: actual-FP0 same-target challenge, completed.
- `columns_final`: bounded independent primitive audit, completed.
- `support_final`: bounded positive-weight support audit, completed.
- `calibration_summary.json`: complete grade tables, exact roots, controls and source hashes.

Their schema-v2 manifests validate against the repository root. Scientific results, manifests, exact argv, software, before/after hashes and executed transformed sources are preserved. All scientific scorers request one numerical thread; normal/challenge peakRSS is below0.70GB per process. Audited runs enforce wall900s/CPU600s perprocess; scalar audits use wall60s/CPU50s. No macOS RLIMIT_AS or enforced global memory cap is claimed. Nice15 was denied by sandbox on the first startup.

To regenerate without overwriting evidence, run the recorded interpreter/program argv with a fresh output directory, under the computation-audit bounded runner and the saved contract/input list. For replay runs preserve the pinned run003 reference and its SHA. `launch_exact.py` is the immutable corrected-challenge launcher; `launch_column_audit.py` and `launch_support_audit.py` show the scalar audit commands, with their fixed output names changed to fresh directories.

## Preserved history and limits

`run_001` failed before a scientific scorer because the initial hash-hook recursively opened itself. `run_002` is the complete uncached pilot; its main-script startup hash was unobserved and it had no enforced wall/CPU cap, so these limits are explicit in its manual manifest (validated against the broader new_physics root to include external inputs). Every normal grade is independently corroborated by pinned bounded runs003/004.

`run_006` used displayed a0 for the same frozen challenge,2.12ppm low inL; `DEFINITION_CORRECTION.md` documents the required actual-FP0 correction. `run_007` computed the corrected value but its launcher metadata input changed; its inputs-changed manifest is excluded from authoritative evidence. Run008 pins the corrected launcher and supplies the valid result. No old lane, NL1 follower, zoom process or existing output was modified; no commit was made.

Dwarfs/MW belong to the separate heldout package. These calibration computations do not establish native convergence, a condensation mechanism or a covariant parent, and are not a global-L impossibility proof.
