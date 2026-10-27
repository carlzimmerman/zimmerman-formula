# Regeneration commands

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. The runner output directory must be new. These commands use fresh names and preserve authoritative historical runs. Only SymPy, NumPy and SciPy already present in the environment are used; no dependency installation is required.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/uv_selection/contract.json \
  --input fine_structure_puzzle/uv_selection/discriminator.py \
  --input fine_structure_puzzle/uv_selection/source_equations.json \
  --input fine_structure_puzzle/uv_selection/CONTRACT.md \
  --input fine_structure_puzzle/uv_selection/INPUT_PROVENANCE.json \
  --output fine_structure_puzzle/uv_selection/run-next \
  --result fine_structure_puzzle/uv_selection/run-next/result.json \
  --timeout 30 --max-output-bytes 200000 --max-cpu-seconds 25 --max-threads 1 \
  -- python3 fine_structure_puzzle/uv_selection/discriminator.py \
  --output fine_structure_puzzle/uv_selection/run-next/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/uv_selection/inverse_contract.json \
  --input fine_structure_puzzle/uv_selection/inverse_bvp.py \
  --input fine_structure_puzzle/uv_selection/inverse_inputs.json \
  --output fine_structure_puzzle/uv_selection/inverse-next \
  --result fine_structure_puzzle/uv_selection/inverse-next/result.json \
  --timeout 60 --max-output-bytes 200000 --max-cpu-seconds 50 --max-threads 1 \
  -- python3 fine_structure_puzzle/uv_selection/inverse_bvp.py \
  --output fine_structure_puzzle/uv_selection/inverse-next/result.json
```

Validate any resulting manifest with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/uv_selection/run-next/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The mutation control uses the exact-run command with a distinct fresh output directory and appends `--mutate` to the child command. Its expected run status is `failed` at the independent beta/charge-trace identity; it is not a successful physics run.

Authoritative supplied records: `run-003`, `inverse-002`, `mutation-001`. Earlier recorded attempts are retained and labelled in REPORT.md.
