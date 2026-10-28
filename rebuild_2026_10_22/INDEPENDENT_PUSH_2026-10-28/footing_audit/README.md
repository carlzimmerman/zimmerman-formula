# CRISP FINDING: alt fails the combined grade; its SPARC scatter does not fail

The independently recounted stored evaluations are **14/72 canonical passes and
0/72 alt passes**: 4/48 in the CF1–CL3 census, plus 10/24 LEE1 draws. These are
related evaluations of selected configurations, not 72 independent experiments.
No raw-data astrophysical fit was rerun.

The SPARC gate is a conjunction: weighted RMS <= 0.110 dex **and** median stellar
mass-to-light ratio in [0.50, 0.80], as defined in EM1's `line`. For all three CL3
levels and BS1's primary point, on both backgrounds, both footings satisfy the
RMS cut. Alt fails the calibration cut. On background A:

| Configuration | canonical RMS / median U | alt RMS / median U |
|---|---|---|
| CL3 L=3.75 | 0.05555 / 0.53 | 0.05372 / 0.44 |
| CL3 L=3.9 | 0.05671 / 0.53 | 0.05372 / 0.44 |
| CL3 L=4 | 0.05787 / 0.53 | 0.05370 / 0.44 |
| BS1 primary | 0.05692 / 0.53 | 0.05649 / 0.46 |

Alt has slightly smaller residual scatter in these cells. That observation
neither licenses changing the frozen U prior nor erases its dwarf failure.
Every one of the 24 LEE1 draws fails both SPARC and MW ultra-faints on alt; other
individual lines often pass. The accurate status is **unsuccessful under the
current joint criteria**, rather than “fails everywhere” or universal exclusion
of that acceleration scale. Canonical remains the research baseline; preserve
alt as a separately reported diagnostic under the standing two-footing rule.
This report does not change repository-wide policy.

Verification: `run_normal_v2/results.json` reports 71/71 checks, 19.1 MB peak RSS.
The independently evaluated gate reproduces every inspected stored flag.
The mutation lowers the U cut to 0.40 diagnostically: `run_MUTATE_v2/results.json`
fails 8 gate checks (63/71), exits 1, and leaves the actual grade untouched.
Both v2 manifests pass the installed computation-audit manifest validator.
The two first launches failed before executing the audit because macOS rejected
RLIMIT_AS; they are preserved in `run_normal` and `run_MUTATE` with status
`launch-failed`. See `AMENDMENTS.md`.

Reproduce in a new output location with standard-library Python:

```sh
OMP_NUM_THREADS=1 nice -n 15 python3 -I rebuild_2026_10_22/INDEPENDENT_PUSH_2026-10-28/footing_audit/audit.py --output /tmp/ip28_footing_results.json
```

Add `--mutate` for the expected failing diagnostic. The runner's exact argv,
inputs before/after hashes, environment, and limits are in each manifest.
This is a stored-output audit, not independent validation of the upstream
selection, stellar calibration, or astronomical measurements. Criteria were
written before execution, hash pinned, and not committed (.git is read-only).
