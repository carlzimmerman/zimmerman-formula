# Mechanism investigation,26 October2026

Start with [STATUS.md](STATUS.md). The audited checkpoint is
[RESULTS.md](RESULTS.md); the fixed target is [TARGET.md](TARGET.md).

All scripts, contracts and run directories are local. Keep manifested source
and outputs unchanged. Reproduction requires a fresh run directory. For the
main checked experiment, from the repository root:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract mechanism_parent_2026_10_26/checked_contract.json \
  --input mechanism_parent_2026_10_26/check_parent_checked.py \
  --input mechanism_parent_2026_10_26/DERIVATION.md \
  --input mechanism_parent_2026_10_26/TARGET.md \
  --output mechanism_parent_2026_10_26/NEW_RUN \
  --result mechanism_parent_2026_10_26/NEW_RUN/result.json \
  --timeout 60 --max-output-bytes 1048576 --max-cpu-seconds 45 --max-threads 1 \
  -- python3 mechanism_parent_2026_10_26/check_parent_checked.py \
  --output mechanism_parent_2026_10_26/NEW_RUN/result.json
```

The other exact argv and inputs are recorded in their manifests. Create new
contracts/scripts before changing model assumptions; do not refresh hashes to
make altered evidence appear current. No inherited checkpoint was resumed or
reset in this phase, and no commit or remote push was performed.
