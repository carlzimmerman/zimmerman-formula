# Execution index

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
All scripts and output directories below are under
`qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026`.

The six wrapper invocations were actually executed. Each wrapper prints its
complete argv, invokes the installed computation-audit bounded runner, and
validates the resulting v2 manifest against the repository. A seventh bounded
runner invocation archives clock-specific endpoint sensitivity. All seven
experiments and validations exited 0. Each output directory contains the
unchanged input hashes before/after, actual argv, versions, dirty base commit,
runtime, exit status, stdout/stderr and result checksum. A successful process
does not turn a scientific gradient failure into a viable theory.

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/run_bounded.py --name scan_001 --grid 1601
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/run_bounded.py --name scan_002 --grid 3201
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/run_bounded.py --name refinement_001 --refine-input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/scan_001/result.json
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/run_early.py --name early_001 --step .025
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/run_early.py --name early_002 --step .0125
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/run_diagnostics.py
```

The seventh run used the same installed runner and shared `INPUTS` list,
plus `endpoint_sensitivity.py`, `endpoint_contract.json`, and
`early_002/result.json`, with output `endpoint_001`, a 120-second timeout,
1 MiB log cap and cooperative one-thread limit. Its exact child argv was:

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/endpoint_sensitivity.py --source qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/early_002/result.json --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026/endpoint_001/result.json
```

The runner and subsequent `validate_manifest.py --root` each exited 0;
the manifest records complete runner bounds and scientific argv.

The first five runs took approximately 46.5, 59.1, 57.1, 7.45 and 10.9 seconds.
Each has a 420-second wall-clock cap, 1 MiB combined log cap, and cooperative
one-thread numerical-library setting; the diagnostic run has a 180-second cap.
No hard memory/CPU-affinity cap is claimed. These caps apply per execution.
The wrapper names identify fresh output directories; do not rerun against
an existing output directory expecting an overwrite.

Focused checks were actually executed with exit 0: four tests passed in
20.083 seconds. They verify the joined coefficient IVP, agreement with the
old baseline and two root grids, original constraints and Ward identity for
new initial data, and conserved charges during a short new-data continuation.
They do not assert an expected physical kinetic rank or sound speed.

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fixed_action_initial_data_2026 -p 'test_*.py' -v
```

An initial wrapper attempt exited 2 before any run started because the
handwritten contract used an invalid JSON `.2` literal. It was corrected to
`0.2`; the successful archived commands use the corrected hashed contract.
An exploratory 801-grid execution exited 0 and generated the transient, untracked `exploratory.json`
before the higher-k extension. It is not substituted for an archived manifest.

No original coefficient, action, derivative, background, transfer, or L186
source was edited, and no commit or external write was performed. Changes
were confined to this new output directory. The computation-audit and
research-program skills were used; no complete theory or new Lean theorem
is claimed.

Selected SHA-256 checksums (the manifests retain the complete lists):

| Artifact | SHA-256 |
|---|---|
| initial_data.py | 2d5db41bb7f52fd96ff85a18bd2484abb220ab51ef5e1132e53d62b80e1b41ba |
| early_extension.py | 737c753dfaca8f1ebd17c28a6a243da9a6e6a7c1f5c406e8f7e269ecbbdc9fc3 |
| early_002/result.json | 0f122dfb0fc68ecd6cfaf0bd2600d482e9abf4051198dccb9d20e901f656bf4f |
| diagnostics_001/result.json | c4ebbf7a63c82df902a2ffaae87c4a3bd295c64f70ae84662033e7fd85ed9d25 |
