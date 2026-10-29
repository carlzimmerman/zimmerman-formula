# Frozen completed-main snapshot and audit

Capture only the completed amended NL1 main JSON, final .out, source, original
frozen criteria, A1 amendment/failure record and read-only grading harness.
Require final out's results-SHA to match exact JSON bytes, all4main controls,
all9seed coverage and stable before/after byte-identical copies. Read original
paths only; do not alter/restart the active scorer, rerun or mutation jobs.

Independently reconcile each seed's primary measurements with published
measurement_007_nine, compute the exact declared median/normalization and the
2000-resample seeded bootstrap using the frozen recipe, and reconstruct the
reported frozen-primary verdict from saved fail lists and convergence-band
rule. Synthetic/source checks are the completed main's reported controls;
this audit is not a new full physical regrade or an independent convergence test.

A missing byte-identical rerun or mutation record remains PENDING, never a
passed check. Package status is MAIN_COMPLETE_VALIDATION_PARTIAL until those
controls are separately verified. Keep the old fixed-T and extrapolated CL3
results distinct from corrected CSM1 same-column linked-T results. Retain
first-crossing/binning instability, non-paired-resolution and mass-extrapolation
assumptions. One numerical thread, wall120/CPU90; immutable-copy/input hashes,
finite checks and source-scope review. No physical fit, cut or input change.
