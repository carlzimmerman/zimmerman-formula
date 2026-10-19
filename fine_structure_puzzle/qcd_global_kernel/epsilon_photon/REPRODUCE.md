# Reproduction

Current evidence: run_002/manifest.json, status completed, validator exit 0.
The first run failed only the order-8 small-time heat check; preserve its
manifest, stderr and exact historical code snapshot. See RUN_TRANSITION.md.

The command and all five frozen input paths are recorded in the current
manifest and contract. To reproduce, choose a NEW output directory and run:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/qcd_global_kernel/epsilon_photon/contract.json --input fine_structure_puzzle/qcd_global_kernel/epsilon_photon/compute_photon.py --input fine_structure_puzzle/qcd_global_kernel/epsilon_photon/DERIVATION.md --input fine_structure_puzzle/qcd_global_kernel/epsilon_photon/REPORT.md --input fine_structure_puzzle/qcd_global_kernel/epsilon_photon/INPUTS.json --input fine_structure_puzzle/qcd_global_kernel/epsilon_photon/SOURCES.json --output fine_structure_puzzle/qcd_global_kernel/epsilon_photon/run_NEW --result fine_structure_puzzle/qcd_global_kernel/epsilon_photon/run_NEW/RESULTS.json --timeout 55 --max-output-bytes 65536 --max-cpu-seconds 45 --max-threads 1 -- python3 fine_structure_puzzle/qcd_global_kernel/epsilon_photon/compute_photon.py fine_structure_puzzle/qcd_global_kernel/epsilon_photon/run_NEW/RESULTS.json
```

Validate the saved current evidence:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_global_kernel/epsilon_photon/run_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

No address-space limit, installation, external job, fitted constant or inherited
Haar numerical grid was used. Numerical quadrature is not interval certified.
