# FSP-A commands and reproducibility

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Observed HEAD: `3c01aa2861bf576f4c2d942251eb9d2f89cae108`.
The surrounding repository was dirty before this work. No full campaign rerun, package installation, external publication, original-output rewrite, or Git mutation was performed.

Source inspection used `cat`, `sed -n` and `rg -n` on the files enumerated in `INPUTS.json`; `rg --files` located route files. Two initial guessed names did not exist: `B_asymptotic_safety/b1_asymptotic_safety.py` and `T1_self_sustained/t1_self_sustained.py`. They were located by `rg --files` as the B_rg_asymptotic_safety and T1_stationary_field paths. No missing artifact was silently treated as evidence.

The following exact commands produced the three new bounded execution records. The runner uses Python 3.12, while the child calculation uses the system Python 3.9.6 with SymPy 1.14.0; both interpreter records are represented in the manifests/contracts. The runner itself writes only the fresh output directory.

```bash
/opt/homebrew/bin/python3.12 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/archive_audit/contracts/scope.json --input fine_structure_puzzle/archive_audit/scope_checks.py --output fine_structure_puzzle/archive_audit/runs/scope --timeout 30 --max-output-bytes 262144 --max-cpu-seconds 25 --max-threads 1 -- /usr/bin/python3 fine_structure_puzzle/archive_audit/scope_checks.py

/opt/homebrew/bin/python3.12 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/archive_audit/contracts/ah5.json --input real_research/alpha_schwinger_2026/ah5_dimensional_obstruction.py --output fine_structure_puzzle/archive_audit/runs/ah5 --timeout 30 --max-output-bytes 262144 --max-cpu-seconds 25 --max-threads 1 -- /usr/bin/python3 real_research/alpha_schwinger_2026/ah5_dimensional_obstruction.py

/opt/homebrew/bin/python3.12 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/archive_audit/contracts/q3_flat.json --input real_research/alpha_principle_2026/Q3_salam_sezgin/q1_ss_vacuum_and_flat_direction.py --output fine_structure_puzzle/archive_audit/runs/q3_flat --timeout 30 --max-output-bytes 262144 --max-cpu-seconds 25 --max-threads 1 -- /usr/bin/python3 real_research/alpha_principle_2026/Q3_salam_sezgin/q1_ss_vacuum_and_flat_direction.py
```

All returned `status=completed`, exit 0. Their stdout was read in full; stderr was empty. There were 16, 4 and 14 passing checks respectively. No new mutation-control run was performed; this is exact algebra/reproduction, not a new sampled numerical algorithm. AH5 has no archived mutation control. No Lean compile was rerun in this audit.

Each manifest was then checked with:

```bash
/opt/homebrew/bin/python3.12 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/archive_audit/runs/scope/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
/opt/homebrew/bin/python3.12 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/archive_audit/runs/ah5/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
/opt/homebrew/bin/python3.12 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/archive_audit/runs/q3_flat/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Each returned `valid evidence record (run status: completed); mathematical interpretation requires review`. For reproduction choose a *new* output directory; the runner refuses to overwrite a prior one. Commands were selected by reading source/docstrings; none was blindly copied from an untrusted evidence file.

`INPUTS.json` contains SHA-256 and byte length for the 30 inspected physical/mathematical inputs at capture time. Run manifests separately authenticate declared input hashes before and after execution. Skills and tools are process dependencies; their identities are recorded by path here, without claiming they are physical premises.
