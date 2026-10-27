# Regeneration and finite contract

The numerical claim is exactly the four TF and six GP/baryon stationary cases
in `contract.json`, not a global continuum stability certificate. Constants,
dimensionless conventions and bounds are in `parameters.json`. No random
numbers are used. All calculations use NumPy float64/SciPy ODE/BVP quadratures.

Use a new output-directory suffix for another run. The command actually used:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract sol61_push/shared_state_2026_10_19/equilibrium/contract.json \
  --input sol61_push/shared_state_2026_10_19/equilibrium/check_equilibrium.py \
  --input sol61_push/shared_state_2026_10_19/equilibrium/parameters.json \
  --output sol61_push/shared_state_2026_10_19/equilibrium/run_002 \
  --result sol61_push/shared_state_2026_10_19/equilibrium/run_002/results.json \
  --result sol61_push/shared_state_2026_10_19/equilibrium/run_002/profiles.json \
  --timeout 45 --max-output-bytes 65536 --max-cpu-seconds 30 --max-threads 1 \
  -- python3 sol61_push/shared_state_2026_10_19/equilibrium/check_equilibrium.py \
     sol61_push/shared_state_2026_10_19/equilibrium/run_002
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/shared_state_2026_10_19/equilibrium/run_002/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The manifest records the observed Git revision/dirty state, before/after
input hashes, versions, runtime, effective limits, successful exit, and hashed
results. It passed current-input hash validation. No hard memory or CPU affinity
limit was requested. The 30-second CPU cap is per process; conventional library
thread variables request one thread, not a kernel-level thread guarantee.

Independent implementation controls are the hand-solvable n=1 limit, Poisson
flux mass, separately integrated masses, the scalar/baryon virial balance,
and doubling the outer-box room with tighter tolerance. No full Hessian
spectrum is tested. Baryon cutoff interpolation is independently root-solved
from U(R_b)=mu_b. Finite-box scalar virial surface estimates are retained.
Passing these does not prove global optimality of the stationary solutions.

The earlier completed run_001 is preserved. Self-review then made the pure-n=1
error bounds executable assertions and clarified that non-unit TF eta controls
vary the dimensionless EOS parameter. Run_002 repeats the same numerical
values with that corrected contract and is the current input-pinned record.
