# Reproduction

Run from the repository root with Python3.13.9, NumPy1.26.4, SciPy1.14.1,
PyTorch2.6.0 and SymPy1.13.1. One BLAS/Torch thread. Matplotlib3.10.8 is used only
for the optional plot. No downloads, parameter fitting or randomized evolution.
The finite-difference direction uses NumPy default_rng seed713.

Set TASK to astra_goal_2026_11_05/AZ40_canonical_coupling/inhomogeneous_cap.
Use a fresh output directory for every command. Standalone commands:

    python3 "$TASK/algebra.py" --out "$TASK/evidence/fresh_algebra"
    python3 "$TASK/planar.py" --mode check --out "$TASK/evidence/fresh_check"
    python3 "$TASK/planar.py" --mode check --uncapped --out "$TASK/evidence/fresh_uncapped_check"
    python3 "$TASK/bracketed.py" --mode check --out "$TASK/evidence/fresh_bracket_check"
    python3 "$TASK/planar.py" --mode evolve --n 65 --rtol 1e-7 --wall 280 --out "$TASK/evidence/fresh_cap65"
    python3 "$TASK/planar.py" --mode evolve --n 65 --rtol 1e-9 --wall 280 --out "$TASK/evidence/fresh_cap65tight"
    python3 "$TASK/bracketed.py" --mode evolve --n 257 --rtol 1e-7 --wall 280 --out "$TASK/evidence/fresh_cap257"

Evolution defaults to target t=3. Nonzero exit and a saved partial trajectory
are EXPECTED for the recorded tests; do not convert those statuses to success.
The current analysis reads the explicitly named archived runs:

    python3 "$TASK/analyze.py" --root "$TASK" --out "$TASK/evidence/fresh_analysis"
    python3 "$TASK/plot.py"

For provenance, use the mathbox computation-audit run_experiment.py with
--timeout300 --max-threads1 (120 for checks/analysis), --root ., the appropriate
*_contract.json, one --input per execution_artifacts entry, a fresh --output,
and --result for results.json plus trajectory.npz when evolving. Place the
standalone command after --. The archived manifests give actual argv, versions,
limits, input and output hashes, run status and elapsed time. Their absolute
interpreter location is host-specific; choose the installed compatible Python.

computation_contract.json covers the original17/33/65 runs. refinement_contract
adds129/257; bracket_contract adds the safeguarded solver and its root-failure
record. analysis_v2_contract pins all trajectories and scripts used in the final
analysis. The129 run was authorized by prose REFINEMENT.md, but its original
machine contract was not expanded; see RESULT.md for that metadata limitation.

## Historical provenance and portable logs

Historical manifests are never rewritten to claim current source hashes.
planar_first_attempt.py.txt is the exact source for check17 and the original
cap17 failure. analyze_first_attempt.py.txt is the source of the failed first
off-grid analysis; analyze_selected_times.py.txt is the successful selected-time
analysis before the final79-sample interval audit. Current inputs validate for
the final analysis and retained evolutions using planar.py/bracketed.py.

Raw stderr from some runs contains local filesystem paths and is kept locally,
not committed when it contains those paths. A separately named stderr.redacted.txt
preserves its diagnostic content with path labels. The original manifest retains
the raw log hash; no redacted log is passed off as the original. Thus full raw-log
hash validation of those historical records requires the local raw files or a
new run. Mathematical inputs, result JSON, trajectories, source snapshots and
portable log copies are committed. verification.json records the local validator
outcome and explicitly identified archived-source matches.
