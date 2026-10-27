# FSP-002/B reproduction

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. Python 3.9.6 and SymPy 1.14.0 were observed. The runner is the installed computation-audit helper; choose a **fresh** output directory for each run.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract /Users/carlzimmerman/new_physics/zimmerman-formula/fine_structure_puzzle/atomic_bridge/scalar_bridge/contract.json \
  --input fine_structure_puzzle/atomic_bridge/scalar_bridge/check_scalar_bridge.py \
  --output fine_structure_puzzle/atomic_bridge/scalar_bridge/run_003 \
  --result fine_structure_puzzle/atomic_bridge/scalar_bridge/run_003/results.json \
  --timeout 30 --max-output-bytes 1048576 --max-cpu-seconds 20 --max-threads 1 \
  -- python3 fine_structure_puzzle/atomic_bridge/scalar_bridge/check_scalar_bridge.py \
  --output fine_structure_puzzle/atomic_bridge/scalar_bridge/run_003
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/atomic_bridge/scalar_bridge/run_003/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Expected stdout: 23 checks, all passed; rank-3 minor `-1/(r + 1)`; augmented fixed-threshold determinant `a/(r + 1)`. No random sampling, alpha target, numerical formula search or external input retrieval occurs inside the computation. The contract records the scope of the symbolic families.

Historical command failures preserved: an initial invocation with `--max-cores 1` returned exit 2, `CPU affinity limits are unavailable on this platform`, before creating an output directory. Removing that option and retaining `--max-memory-bytes 1073741824` produced `run_001`, exit 127 / `launch-failed`, with `Exception occurred in preexec_fn.`. Removing only the unsupported memory setup produced completed `run_002`. The exact failed argv is in its manifest. CPU time, wall time, output size and conventional thread count remained bounded in the completed run; CPU affinity and virtual-memory limits were not enforced there.

Primary PDFs were read through the web tool and downloaded read-only to `/private/tmp/fsp002_scalar_sources/` for version/hash authentication. A default-sandbox curl initially failed DNS resolution; the authorized network-capable retry succeeded. No source text/PDF was copied into the repository. `source_records.json` records precise versions and hashes, including extracted text hashes. Temporary source availability is not promised; reacquire those exact URLs and compare hashes. The 1994 arXiv v1 PDF currently prints a 2024 typesetting date; the submission header/version remains hep-th/9401069v1, 14 January 1994. That generated PDF date is not used as a revision date.
