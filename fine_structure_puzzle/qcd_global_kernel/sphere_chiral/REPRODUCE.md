# Reproduce the global pion component

From the repository root, install nothing and use the existing Python, SymPy
and mpmath versions recorded in contract.json. The executed command was:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/qcd_global_kernel/sphere_chiral/contract.json --input fine_structure_puzzle/qcd_global_kernel/sphere_chiral/compute_sphere.py --input fine_structure_puzzle/qcd_global_kernel/sphere_chiral/DERIVATION.md --input fine_structure_puzzle/qcd_global_kernel/sphere_chiral/REPORT.md --input fine_structure_puzzle/qcd_global_kernel/sphere_chiral/INPUTS.json --input fine_structure_puzzle/qcd_global_kernel/sphere_chiral/SOURCES.json --output fine_structure_puzzle/qcd_global_kernel/sphere_chiral/run_001 --result fine_structure_puzzle/qcd_global_kernel/sphere_chiral/run_001/RESULTS.json --timeout 55 --max-output-bytes 65536 --max-cpu-seconds 45 --max-threads 1 -- python3 fine_structure_puzzle/qcd_global_kernel/sphere_chiral/compute_sphere.py fine_structure_puzzle/qcd_global_kernel/sphere_chiral/run_001/RESULTS.json
```

Use a NEW output/result directory for another run; preserve run_001. The
runner records observed input hashes before/after, software, limits and
outputs. No optional address-space limit is used on macOS. Validate:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_global_kernel/sphere_chiral/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Observed status: completed, validator exit 0. Interpretation is restricted
to DERIVATION.md. The quadrature/asymptotic tails are numerical checks,
not rigorous interval error certification. The positive-sum tail is an
analytic bound evaluated at high precision. Public source PDFs/text are
in temporary paths recorded in SOURCES.json and are not runtime inputs.
