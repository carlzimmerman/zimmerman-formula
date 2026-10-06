# Execution handoff

Current `runs/main_a`: 21 symbolic checks pass. Each of `control_mond_exceptional_a`, `control_sqrt_mass_a`, `control_offset_selected_a` fails exactly its intended false assertion; all four standard manifests validate against current pinned inputs. Actual starting HEAD is recorded in provenance.json and the manifests; no commit was made.

For a quick algebra rerun from repository root, choose a NEW output path:

```sh
/usr/bin/python3 sol61_push/puzzle_32pi/exceptional_scalar_selector_2026_10_06/checks.py --output /private/tmp/exceptional_new_results.json
```

For audited execution, use computation-audit `scripts/run_experiment.py` with --root the absolute repository root, --contract this folder's contract.json, --input each path in contract.execution_artifacts, --output a new owned runs/<name> directory, --result its results.json, --timeout 60 --max-cpu-seconds 45 --max-output-bytes 200000 --max-threads 1; append -- then the same Python/script command with --output matching --result. Controls are `--control mond_exceptional`, `sqrt_mass`, `offset_selected`. Use the installed mathbox runner Python3.13, then validate_manifest.py --root PROJECT MANIFEST. Inputs include report, source review, registry and provenance. Changing any requires a fresh run; do not overwrite prior manifests.

The PDF itself is not retained. Source review reruns reopen exactly arXiv:1605.06418v2; sources.json honestly records only the local source-note content hash. No downloaded paper redistribution or global ledger edits were performed.

Preflight caught and corrected the sign of the nonzero MOND ODE residual before evidence runs. The static inverse check uses a squared-flux polynomial identity plus the report's explicit positive-branch/radicand hypotheses; this avoids treating SymPy's unconstrained square-root simplification as a branch proof.
