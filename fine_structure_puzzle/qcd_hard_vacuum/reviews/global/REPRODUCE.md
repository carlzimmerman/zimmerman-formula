# Reproduce this independent audit

From /Users/carlzimmerman/new_physics/zimmerman-formula. Keep run_001 immutable;
the second command uses a new run_REPRODUCE directory and requires no install,
network, RNG or external numerical input.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_hard_vacuum/reviews/global/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/qcd_hard_vacuum/reviews/global/CONTRACT.json --input fine_structure_puzzle/qcd_hard_vacuum/reviews/global/independent_check.py --input fine_structure_puzzle/qcd_hard_vacuum/reviews/global/INPUTS.json --input fine_structure_puzzle/qcd_hard_vacuum/reviews/global/PRETARGET.md --input fine_structure_puzzle/qcd_hard_vacuum/global_qcd/runs/closed-002/results.json --output fine_structure_puzzle/qcd_hard_vacuum/reviews/global/run_REPRODUCE --result fine_structure_puzzle/qcd_hard_vacuum/reviews/global/run_REPRODUCE/result.json --timeout 55 --max-cpu-seconds 45 --max-output-bytes 65536 --max-threads 1 -- python3 fine_structure_puzzle/qcd_hard_vacuum/reviews/global/independent_check.py fine_structure_puzzle/qcd_hard_vacuum/reviews/global/run_REPRODUCE/result.json
```

The actual run_001 argv and observed limits are authoritative in its manifest.

The retained author manifest validation commands are in global_qcd/REPRODUCE.md
and coordinator/sea_hodge/REPRODUCE.md. This reviewer executed those three
validation commands, not their author rerun commands. The qualified support
population and exact original run bounds are summarized in REPORT.md.
