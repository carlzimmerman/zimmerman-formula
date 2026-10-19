# Commands and immutable-run notes

Project root: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Computation skill directory: `/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit`.

The recorded commands, limits, Python/library versions, hardware, commit/dirty state, before/after input hashes, results and logs are in each v2 manifest. Existing run directories and their inputs are immutable. To reproduce, copy the corresponding script and contract to a new numbered pair, update only the script's fresh result path and the contract's script input path, then run against a new directory. Do not overwrite a completed or failed run.

Successful first experiment:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_completion/closed_dual_qcd/contract_002.json \
  --input fine_structure_puzzle/qcd_completion/closed_dual_qcd/verify_closed_002.py \
  --input fine_structure_puzzle/qcd_completion/closed_dual_qcd/DERIVATION.md \
  --input fine_structure_puzzle/qcd_completion/closed_dual_qcd/INPUTS_001.json \
  --input fine_structure_puzzle/qcd_completion/closed_dual_qcd/SOURCES.json \
  --output fine_structure_puzzle/qcd_completion/closed_dual_qcd/runs/closed-002 \
  --result fine_structure_puzzle/qcd_completion/closed_dual_qcd/runs/closed-002/result.json \
  --timeout 120 --max-output-bytes 1048576 --max-cpu-seconds 110 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_completion/closed_dual_qcd/verify_closed_002.py
```

The kernel experiment uses `contract_003.json`, inputs `verify_green_003.py`, `CLOSED_GREEN.md`, `INPUTS_001.json`, output `runs/green-003`, result `runs/green-003/result.json`, and CPU/wall bounds 45/50 seconds. All other flags match the first experiment. This command is fully recorded in that manifest.

Read-only validation of each record:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_completion/closed_dual_qcd/runs/closed-002/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Use the analogous manifest path for `closed-001` and `green-003`. The first is valid provenance for **launch-failed**, not a passing scientific computation. Its stderr is the observed preexec exception. CPU affinity is unavailable on this macOS platform and the memory-capped child failed before mathematical execution; the successful fresh run does not claim either cap.
