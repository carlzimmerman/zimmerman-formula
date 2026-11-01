# Reproduction

The common frozen API is `model.build_model(X,h,lam,g,f,vertices=True)`.
It returns scalar/vector eigenvectors as columns and a Takagi U satisfying
U.T MF U=diag(mF)>=0. `graph_weights(data)` returns ordered-index grouped
SSS,SS,FFS,barFFS weights with source symmetry factors already included.
The coordinator's gauge_diagrams/full.py consumes this API and combines
all ten graph classes; pressure.py uses the same full sum.

Three current successful contracts and their authored commands are:

| contract | command after runner separator | fresh result argument |
|---|---|---|
| builder_contract.json | python3 two_loop/check_builder.py | new-directory/result.json |
| basis_contract.json | python3 two_loop/check_basis.py | new-directory/result.json |
| gap_contract.json | python3 two_loop/check_gaps.py | new-directory/result.json, followed by original run_pressure/result.json |

Paths in that table are relative to reviews/finite_matching_2026_11_01/;
run from the repository root with the full project-relative paths. Use the
installed computation-audit runner, the indicated contract, and every
execution_artifacts entry repeated as --input. Declare a fresh --output
directory and the child program's new result file as --result. Preserve
--max-threads1, --timeout180, --max-cpu-seconds170 and a bounded log budget;
the gap control needs only60wall/50CPU seconds. Never overwrite an old
run or execute a command copied from an evidence record.

For provenance validation, for example:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/finite_matching_2026_11_01/two_loop/run_basis/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The installed runner/validator are local skill tools rather than bundled
dependencies. Software versions are recorded per manifest. No installs,
downloads or random seeds are needed. Repeating the same implementation
checks reproducibility, not independent mathematical correctness.

The initial failed run is intentionally retained with archived inputs;
see LAUNCH_HISTORY.md before interpreting a current-input validator failure
on that historical record. The later successful records pin the scientific
inputs actually used. Exact external code/source hashes reviewed here are
in GAUGE_REVIEW_INPUTS.json, separate from the independent vertex audit
in master_integrals/VERTEX_AUDIT.md.
