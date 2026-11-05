# Implementation notes

The first BH run exited75 after its declared one-case checkpoint test. A
resume read the two existing checkpoints and computed the doubled-resolution
case, then failed while serializing a NumPy boolean in the aggregate checks.
This is a result-writing bug, not a numerical failure. The prior script and
three checkpoints are preserved in `bh_serialization_failure_cases/`; they
are excluded from the final production case set. The only fix adds scalar
conversion to JSON serialization. All production cases are rerun from scratch
under the new script hash; no thresholds, equations or parameters change.
`bh_resume.out` preserves the traceback with the local repository/home path
redacted. The final run is `bh_run.out`.
