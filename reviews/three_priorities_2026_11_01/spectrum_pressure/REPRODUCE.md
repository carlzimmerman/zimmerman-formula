# Reproduction and evidence

The five successful v2 records are `run_diagnostic_supported/`,
`run_blocks/`, `run_pressure/`, `run_exact_gap/` and `run_density/`.
All manifest/result hashes validate with the repository root. The first
`run_diagnostic/` record has status `launch-failed`, not a mathematical
failure: the requested 1 GB address-space restriction failed in macOS's
preexec function. A preceding affinity request failed before a run folder
was created because CPU affinity is unavailable on this platform. Successful
runs use one numerical thread, explicit CPU/wall/log caps, and measured RSS.

Contracts and executed inputs are immutable. Each completed run records
the actual shared Git revision and dirty state; HEAD advanced during this
work, so its hash alone does not identify scientific inputs. The original
microscopic model files were not edited by this route.

`reproduce.py` launches an authored command using its frozen contract and
listed inputs into a *new* direct child folder. It does not execute commands
read from evidence manifests. Example from the repository root:

```bash
python3 reviews/three_priorities_2026_11_01/spectrum_pressure/reproduce.py pressure run_pressure_independent --runner /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py
```

Stages: `diagnostic`, `blocks`, `pressure`, `exact_gap`, `density`.
The last two intentionally compare against the frozen original pressure
and derivative results. Choose a fresh output name. Repeating the same
implementation checks reproducibility, not independent mathematical
correctness. No rerun of unchanged successful inputs is needed merely
because the repository HEAD advances.

Validate a record with the installed computation-audit validator:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/three_priorities_2026_11_01/spectrum_pressure/run_pressure/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The paths above identify tools installed on this author's machine; they
are not bundled project dependencies. Python 3.9.6, NumPy 1.26.2, SciPy
1.11.4, SymPy 1.14.0 and mpmath 1.3.0 were used as specified per manifest.
No random sampling or new packages were used.
