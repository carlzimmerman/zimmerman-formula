# Reproduce the finite closed SU(3) calculation

Run from /Users/carlzimmerman/new_physics/zimmerman-formula. No third-party Python dependency, network access, measured input or RNG is required. Do not reuse an existing output directory.

Validate the retained evidence:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_hard_vacuum/global_qcd/runs/closed-001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_hard_vacuum/global_qcd/runs/closed-002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Execute the stronger finite calculation into a fresh directory:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/qcd_hard_vacuum/global_qcd/COMPUTATION_CONTRACT_v2.json --input fine_structure_puzzle/qcd_hard_vacuum/global_qcd/compute_closed_v2.py --input fine_structure_puzzle/qcd_hard_vacuum/global_qcd/PREEXEC_DERIVATION.md --input fine_structure_puzzle/qcd_hard_vacuum/global_qcd/SOURCE_RECEIPTS.json --input fine_structure_puzzle/qcd_hard_vacuum/global_qcd/PREEXEC_CONTINUATION.md --output fine_structure_puzzle/qcd_hard_vacuum/global_qcd/runs/closed-rerun --result fine_structure_puzzle/qcd_hard_vacuum/global_qcd/runs/closed-rerun/results.json --timeout 55 --max-output-bytes 65536 --max-cpu-seconds 45 --max-threads 1 -- python3 fine_structure_puzzle/qcd_hard_vacuum/global_qcd/compute_closed_v2.py --result fine_structure_puzzle/qcd_hard_vacuum/global_qcd/runs/closed-rerun/results.json
```

The immutable original beta6 command is recorded in closed-001/manifest.json and uses compute_closed.py with COMPUTATION_CONTRACT.json and the first three declared inputs. The complete beta9 command is recorded in closed-002/manifest.json.

Python 3.9.6 standard-library Fraction arithmetic gives exact rational series. Modular ranks are explicitly over two primes, not falsely reported as rational reconstruction. The topology supplies the characteristic-independent rank argument; those finite modular ranks are consistency checks. All source PDFs remain in the established ignored local cache, whose availability is not assumed on another clone. SOURCE_RECEIPTS.json pins their identities and exact locators; code does not read them at runtime.
