# Independent original-Euler sample audit

`REPORT.md` records the raw equations, proper-source/force dictionaries and center conditioning. `checks.py` reads the frozen parent core and results, extracts only three AST definitions, and assigns derivatives using mp50 and original binary64 RHS separately. It never imports the parent solver or runs top-level parent code. This is RHS/sample consistency, not a trajectory certificate.

`runs/main_a` must pass; `runs/zero_shift_matter_a` must fail EV checks by deleting the proper matter momentum source. Both standard manifests must validate. Contract/provenance pin actual input hashes. No global_matching files are inputs or outputs.

Use computation-audit run_experiment.py with this contract, all execution_artifacts as --input, a fresh output directory and /usr/bin/python3 checks.py --output <run>/results.json; caps wall60s CPU45s threads1. Control --control zero_shift_matter. Validate the generated manifests. No source download is required; equations are reconstructed from the already authenticated local action.
