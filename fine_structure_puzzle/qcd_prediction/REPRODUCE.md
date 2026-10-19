# Reproduce FSP-003 evidence

Run from the repository root. Python 3 with SymPy, NumPy, SciPy and mpmath is required in the combinations recorded by each contract. The current evidence is finite symbolic/numerical work and source auditing, not a full QCD simulation.

Authoritative contracts, implementations and run manifests:

| Route | Contract | Implementation | Current run |
| --- | --- | --- | --- |
| BPS/geometry | vacuum_geometry/COMPUTATION_CONTRACT_v4.json | vacuum_geometry/check_geometry_v4.py | vacuum_geometry/runs/geometry-004/ |
| QCD+QED chiral terms | electromagnetic/contract_v3.json | electromagnetic/chiral_response_v3.py | electromagnetic/run_003/ |
| Mixed-chiral relation | electromagnetic/mixed_chiral/contract.json | electromagnetic/mixed_chiral/mixed_response.py | electromagnetic/mixed_chiral/run_001/ |
| Compact Maxwell | controlled_model/contract.json | controlled_model/check_maxwell.py | controlled_model/run_002/ |
| Schwinger spectrum | coordinator/schwinger_contract_v2.json | coordinator/schwinger_check_v2.py | coordinator/schwinger_run_002/ |
| Radial ghost | vacuum_geometry/determinant_followup/COMPUTATION_CONTRACT.json | vacuum_geometry/determinant_followup/check_radial.py | vacuum_geometry/determinant_followup/runs/radial-001/ |
| Coupled radial vector | vacuum_geometry/determinant_followup/VECTOR_COMPUTATION_CONTRACT.json | vacuum_geometry/determinant_followup/check_vector.py | vacuum_geometry/determinant_followup/runs/vector-001/ |
| Complete static spherical comparison | vacuum_geometry/determinant_followup/phase_block/COMPUTATION_CONTRACT_v3.json | vacuum_geometry/determinant_followup/phase_block/check_phase_v3.py | vacuum_geometry/determinant_followup/phase_block/runs/phase-003/ |
| Four-dimensional pion determinant | coordinator/curved_pion/contract.json | coordinator/curved_pion/check_pion.py | coordinator/curved_pion/run_001/ |
| QCD chiral/topological zero modes | controlled_model/qcd_zero_modes/contract.json | controlled_model/qcd_zero_modes/check_qcd_zero_modes.py | controlled_model/qcd_zero_modes/run_001/ |
| Zero-mode electromagnetic response | controlled_model/qcd_zero_modes/qed_contract.json | controlled_model/qcd_zero_modes/check_qed_zero_modes.py | controlled_model/qcd_zero_modes/qed_run_002/ |

Paths in this table are relative to fine_structure_puzzle/qcd_prediction/. Exact command lines, versions, input/output hashes and limits are in each manifest. Do not overwrite a recorded run. Direct script usage is documented in its --help and contract; scripts accept an output path. To produce a new audited run, use a new output directory and the installed mathbox runner:

```text
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract CONTRACT_PATH --input INPUT_PATH [--input ADDITIONAL_INPUT_PATH ...] \
  --output NEW_RUN_DIRECTORY --result RESULT_PATH \
  --timeout 45 --max-output-bytes 1048576 --max-cpu-seconds 30 --max-threads 1 \
  -- python3 SCRIPT_PATH --output RESULT_PATH
```

Pass exactly the contract's execution artifacts as inputs, using the recorded syntax and resource limits. The placeholders above are not a ready-to-run command. In particular, the independently integrated QED zero-mode run took about 98 seconds and uses 270 seconds wall/240 seconds CPU caps; copy its recorded limits rather than the shorter illustrative ones above. Platform-specific affinity/memory caps are not required here. Validate an existing or new record with:

```text
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST_PATH --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

[MANIFEST_VALIDATION.json](reviews/MANIFEST_VALIDATION.json) records the coordinator's current validation. Older failed/superseded runs are retained with explanations; do not treat them as additional independent physics results. [Coordinator reproduction details](coordinator/REPRODUCE.md) and [Maxwell reproduction](controlled_model/REPRODUCE.md) give route-specific information.

Source-based hand reviews are not reproduced by rerunning symbolic code. Their exact versions, PDF hashes, selected inspected pages and independence limits are recorded in the route SOURCES/INPUTS files and the two fresh-review directories. Full source PDFs lived in /private/tmp and may need retrieval by exact version if that cache expires. Selected decisive page images are retained in the reviews. Reauthenticated downloads must match the recorded hashes before being treated as the same source evidence.

No script calculates physical four-dimensional R(alpha), performs a curved-QCD lattice run, or solves for alpha. The [assessment](REPORT.md) states the missing observables and domain restrictions.
