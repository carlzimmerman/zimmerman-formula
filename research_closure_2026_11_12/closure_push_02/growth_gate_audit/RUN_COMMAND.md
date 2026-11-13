# Reproduction

Run from `<repo>`. The output directory must be new; change every occurrence of `run_001` when reproducing. The installed runner records input bytes, software, revision/dirty state, exit status, limits and result hashes. Python3.9.6, NumPy1.26.2 and SciPy1.11.4 were used.

```bash
python3 <home>/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root <repo> \
  --contract research_closure_2026_11_12/closure_push_02/growth_gate_audit/contract.json \
  --input research_closure_2026_11_12/closure_push_02/growth_gate_audit/growth.py \
  --input research_closure_2026_11_12/closure_push_02/growth_gate_audit/sources/03_kd1.json \
  --output research_closure_2026_11_12/closure_push_02/growth_gate_audit/run_001 \
  --result research_closure_2026_11_12/closure_push_02/growth_gate_audit/run_001/results.json \
  --result research_closure_2026_11_12/closure_push_02/growth_gate_audit/run_001/canonical_z3_curve.npz \
  --result research_closure_2026_11_12/closure_push_02/growth_gate_audit/run_001/alt_z3_curve.npz \
  --timeout 60 --max-cpu-seconds 55 --max-threads 1 --max-output-bytes 1048576 \
  -- python3 research_closure_2026_11_12/closure_push_02/growth_gate_audit/growth.py \
  --out research_closure_2026_11_12/closure_push_02/growth_gate_audit/run_001

python3 <home>/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  research_closure_2026_11_12/closure_push_02/growth_gate_audit/run_001/manifest.json \
  --root <repo>
```

The result is a completed finite computation in the stated approximation. A validated manifest is provenance, not proof of a full cosmological theory.
