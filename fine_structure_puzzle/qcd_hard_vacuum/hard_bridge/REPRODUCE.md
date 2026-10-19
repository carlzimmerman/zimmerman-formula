# Bounded reproduction

The following exact v2 command was established before execution. The output
directory must be new. No RLIMIT_AS is requested on macOS. Replace every
`run_001` consistently with a fresh run name for reproduction.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula \
 --contract fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/COMPUTATION_CONTRACT.json \
 --input fine_structure_puzzle/qcd_hard_vacuum/BASELINE.json \
 --input fine_structure_puzzle/qcd_hard_vacuum/CONTRACT.md \
 --input fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/DERIVATION.md \
 --input fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/INPUTS.json \
 --input fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/SOURCE_ADMISSION.json \
 --input fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/check_reconstruction.py \
 --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/DERIVATION.md \
 --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/DIRAC_MSBAR_MATCHING.md \
 --input fine_structure_puzzle/qcd_nonborn_vacuum/photon_mass/DERIVATION.md \
 --output fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/run_001 \
 --result fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/run_001/result.json \
 --timeout 240 --max-output-bytes 1048576 --max-cpu-seconds 220 --max-threads 1 \
 -- python3 fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/check_reconstruction.py \
 fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/run_001/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
 fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/run_001/manifest.json \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Primary-source retention is ignored local cache state. The source receipt
pins its PDF hash and exact formula locators; no cached full text is copied
into this deliverable. The executable control depends only on the frozen
mathematics and declared elementary theory, not a numerical source table.
