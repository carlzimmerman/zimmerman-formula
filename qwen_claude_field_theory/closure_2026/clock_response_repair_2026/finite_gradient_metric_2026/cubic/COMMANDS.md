# Cubic run commands and provenance

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Write scope: this `finite_gradient_metric_2026/cubic/` directory only.

Commands actually executed with exit 0:

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/cubic -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/cubic/run_bounded.py
```

The final six-test suite passed in .445 seconds. An earlier five-test run
passed before the nonzero-Hessian fixture was added; the final suite was
then rerun. The bounded execution passed all fourteen symbolic checks and
completed in 3.844426 seconds. Its 120-second wall-clock cap, 1 MiB combined
log cap and cooperative one-thread numerical setting are recorded. No hard
memory or CPU-affinity cap is claimed.

The wrapper prints its exact argv, runs the installed computation-audit
bounded runner, and then validates the v2 manifest against the repository.
Experiment exit 0, validation exit 0. The actual source checkout was
`706cd625f648079d318aa968b59fbd45850720f2`, dirty.

The archive contains:

- `run_001/result.json`: covariant tensor contractions, exact discriminant
  identities, old-root evaluations with both q conventions, finite-gamma
  coefficient values, newly solved finite-gamma proxy zeros, and specified
  physical FLRW Hessian fixtures.
- `run_001/manifest.json`: actual argv, source hashes before/after, software
  versions, dirty-state provenance, runtime, exit, bounds and result hash.
- `run_001/stdout.txt` and `stderr.txt`: actual process logs.

Selected SHA-256 hashes:

| File | SHA-256 |
|---|---|
| cubic_debraiding.py | 98f607334f3415937a1137f43b8b598c97443957eb6eabcf6a767d01480b10cb |
| test_cubic_debraiding.py | 79c5b6cd4aa9dc94136bb7ecf0145ce177724297f02249b6926b5169b72dfc90 |
| run_001/result.json | 4c80afb67925ecfc2c26359757e04c97cfe1eb5839488434c7f08d10f52652c3 |

In `corrected()` output, `quarter_gamma0` means the discriminant before the
explicit cubic metric/Hessian corrections while holding that call's P/W
jets fixed. Under the `frozen_finite_gamma_action` column those jets already
contain the original coefficient functions' gamma dependence; that field is
not the discriminant of the entire theory with gamma reset to zero.
`quarter_shift_from_exact_polynomial` and its roundoff diagnostic refer only
to the affine metric-feedback polynomial. Nonzero-Hessian corrections are
recorded separately and included in `quarter_finite_gamma` for those fixtures.

The scalar commutator and the integrated-by-parts metric variation identity
are analytical inputs, written out in the report; the script does not claim
to mechanize all covariant variation rules. No original files were edited,
no new action coefficients fitted, and no Git mutation performed.
