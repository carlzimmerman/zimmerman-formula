# Reproduce the QCD and Dashen zero-mode calculations

Working directory:
`/Users/carlzimmerman/new_physics/zimmerman-formula`.
Observed software: Python 3.9.6, mpmath 1.3.0; no installation or random sampling.

All original run directories are immutable. The commands below intentionally
use fresh directory names; change all three output/result occurrences together
if those names already exist.

## Pure two-flavor QCD group function

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/contract.json \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/check_qcd_zero_modes.py \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/inputs.json \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/source_records.json \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/RAW_DERIVATION.md \
  --output fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/run_002 \
  --result fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/run_002/results.json \
  --timeout 90 --max-output-bytes 1048576 --max-cpu-seconds 80 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/check_qcd_zero_modes.py \
  --inputs fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/inputs.json \
  --output fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/run_002/results.json
```

The observed original run is `run_001`, status `completed`; it passed 325
controls at each of 100 and 130 decimal digits. This is finite evidence for
the specified assertions, with analytic identities and physical limits in
`REPORT.md`.

## Leading electromagnetic operator

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/qed_contract.json \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/check_qed_zero_modes.py \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/check_qcd_zero_modes.py \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/qed_inputs.json \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/qed_source_record.json \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/QED_RAW_DERIVATION.md \
  --output fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/qed_run_003 \
  --result fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/qed_run_003/results.json \
  --timeout 270 --max-output-bytes 1048576 --max-cpu-seconds 240 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/check_qed_zero_modes.py \
  --inputs fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/qed_inputs.json \
  --output fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/qed_run_003/results.json
```

`qed_run_001` used the same frozen code/inputs but reached its 80-second CPU
cap. Its runner status is `resource-limit`; this is resource inconclusiveness,
not a mathematical failure. `qed_run_002` repeats the full contracted
calculation under the enlarged bounded cap above. Read its manifest's status
before interpreting any outputs.

The observed `qed_run_002` completed in 98.29 seconds: 105 controls at
each precision passed, maximum repeated-precision discrepancy 1.280e-80.
Its manifest validation with current input hashes passed.

## Manifest validation

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/run_001/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/qed_run_002/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

## Source reacquisition

The exact public versions can be reacquired into temporary storage:

```bash
curl -L --fail --silent --show-error https://arxiv.org/pdf/hep-th/0108166v2 \
  -o /private/tmp/fsp003_hep-th_0108166v2.pdf
curl -L --fail --silent --show-error https://arxiv.org/pdf/hep-ph/9405341v2 \
  -o /private/tmp/fsp003_hep-ph_9405341v2.pdf
shasum -a 256 /private/tmp/fsp003_hep-th_0108166v2.pdf
shasum -a 256 /private/tmp/fsp003_hep-ph_9405341v2.pdf
```

The observed hashes and version authentication are in `source_records.json`
and `qed_source_record.json`. A byte mismatch requires explicit source
reconciliation rather than silent substitution. No full source PDF/text is
included in the tracked packet.
