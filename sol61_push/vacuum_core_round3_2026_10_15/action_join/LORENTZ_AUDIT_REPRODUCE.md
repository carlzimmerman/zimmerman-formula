# Independent Lorentz audit: authoritative run and preserved attempt

The successful orthogonal check uses `check_lorentz_full_matrix_v2.py`,
`lorentz_audit_contract_v2.json`, and `lorentz_audit_run_v2/manifest.json`.
It passes 10 checks, including the complete 6x6 constitutive Hessian, every
linearized Maxwell constraint/equation for the selected mode, the response slope
identity and the exact audited proof hash. The narrative audit is
`../lorentz/AUDIT.md`. Its reference to the unversioned reconstruction points
to the initial implementation; use the v2 script and run for successful
execution evidence.

The initial `lorentz_audit_run_v1` is retained unchanged. Its mathematical
matrix/constraint checks completed, then its explicit proof-hash check failed
with FileNotFoundError because the inferred repository parent was one directory
too high. The v2 change is only `parents[4]` to `parents[3]` in locating that
proof; all symbolic assertions are unchanged. This was a path bug, not a
mathematical counterexample.

Reproduce with the installed computation-audit bounded runner, a fresh output
directory, and each `execution_artifacts` path in the v2 contract as `--input`.
Use `--timeout 45 --max-output-bytes 65536 --max-cpu-seconds 35 --max-threads 1`.
The child command is:

    python3 sol61_push/vacuum_core_round3_2026_10_15/action_join/check_lorentz_full_matrix_v2.py NEW_OUTPUT_DIRECTORY/results.json

The runner's `--result` must name that same result, and `--output` must name its
fresh parent. Validate with the skill's `validate_manifest.py` and repository
root. Both preserved and successful records validate, with their respective
failed/completed statuses; an execution record never upgrades a mathematical
claim without its derivation and scope.
