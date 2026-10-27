# Reproduce the matched compact-mode continuation

No installations or Git mutations are needed. The existing computation
interpreter is Python 3.9.6 with mpmath 1.3.0 and SymPy 1.14.0; the runner
uses Python 3.11.16. Inputs and code were frozen before this first run.
The raw Haar/Dashen integral is an inherited FSP003 result; this command
tests only the new replacement/interacting-pion response and new points.

From `/Users/carlzimmerman/new_physics/zimmerman-formula`:

```bash
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/contract.json --input fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/compute_matched.py --input fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/INPUTS.json --input fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/DERIVATION.md --input fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/SOURCES.json --input fine_structure_puzzle/qcd_prediction/controlled_model/qcd_zero_modes/REPORT.md --input fine_structure_puzzle/qcd_prediction/coordinator/ZERO_MODE_QED_RAW.md --input fine_structure_puzzle/qcd_global_kernel/sphere_chiral/DERIVATION.md --output fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/run_001 --result fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/run_001/RESULTS.json --timeout 55 --max-output-bytes 65536 --max-cpu-seconds 50 --max-threads 1 -- python3 fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/compute_matched.py fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/run_001/RESULTS.json
```

Use a NEW output/result directory for subsequent runs; preserve run_001.
No RLIMIT_AS/address-space or CPU-affinity cap is requested on macOS.
Wall time, CPU time, logs and conventional numerical threads are bounded.

```bash
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_global_kernel/chiral_zero_mode/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Observed status: `completed`; validator exit 0. The result reports 143
controls. Interpretation: implementation and finite assertion verified in
the stated range, conditional on arbitrary-precision quadrature/special
functions, with independent precision and algorithm checks. Exact
polynomial identities and the analytic source/measure derivations support
the identities; the numerical grid alone does not prove them universally.

SOURCES.json records exact public PDF/text hashes. Those temporary sources
are not mathematical runtime inputs and are not assumed present on another
machine. REPORT.md and CURRENT_MANIFEST.json are post-run interpretation
and artifact receipts, not retroactively listed as frozen runtime inputs.
