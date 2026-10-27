# Reproduce the finite connected-response control

Run from the repository root with Python3.9.6 and SymPy1.14.0. The exact code
and assertion are [check_connected.py](check_connected.py) and
[CONTRACT.json](CONTRACT.json); the actual output is
[run_001/RESULTS.json](run_001/RESULTS.json). Use a new output directory for any
execution, preserving the completed run and its inputs.

The command recorded in the manifest is:

```bash
python3 fine_structure_puzzle/qcd_nonborn_vacuum/coordinator/vacuum_let/check_connected.py fine_structure_puzzle/qcd_nonborn_vacuum/coordinator/vacuum_let/run_001/RESULTS.json
```

For a new execution use the installed mathbox bounded runner with the four
execution_artifacts in CONTRACT.json, fresh run/result paths, wall30s,
CPU20s, log65536bytes and one numerical thread. No RLIMIT_AS is used on macOS.
The direct command above is provenance, not permission to overwrite run001.

Validate the existing record with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_nonborn_vacuum/coordinator/vacuum_let/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The primary PDF is identified by its version/hash in SOURCES.json and retained
in the existing ignored literature cache. Its presence or cache verification
does not establish the mathematical application. Source acquisition and the
finite algebra are separate evidence.
