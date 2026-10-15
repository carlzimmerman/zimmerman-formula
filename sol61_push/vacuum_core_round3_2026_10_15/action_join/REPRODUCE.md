# Action-join reproduction and self-review

Authoritative successful computation: `run_v2/manifest.json` and
`run_v2/results.json`, using `check_join_v2.py` and `contract_v2.json`.
All 28 symbolic/direct-record assertions pass. Both the successful record and
the preserved failed record validate against the pinned inputs and outputs.

`run_v1` is retained as a failed symbolic check. SymPy did not infer the declared
physical branch 0<D<D0 when simplifying two logarithms in the Legendre identity.
The initial script remains unchanged at `check_join.py`. The corrected version
uses the explicit chart D=D0*t/(1+t), t>0, so every positive-branch D is covered
without a forced complex-log simplification. No mathematical constitutive law
or result was changed to force a pass.

To reproduce in a fresh output directory, run the computation-audit bounded
runner with `contract_v2.json`, passing each path in its `execution_artifacts`
array as one `--input`, and these limits:

    --timeout 45 --max-output-bytes 65536 --max-cpu-seconds 35 --max-threads 1

The child command is:

    python3 sol61_push/vacuum_core_round3_2026_10_15/action_join/check_join_v2.py NEW_OUTPUT_DIRECTORY/results.json

Declare that exact result with `--result`, and use NEW_OUTPUT_DIRECTORY as
`--output`; it must not already exist. The installed runner is
`/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py`.
The corresponding `validate_manifest.py` accepts the generated manifest and
`--root /Users/carlzimmerman/new_physics/zimmerman-formula`.

Self-review checked:

- Constitutive dimensions: kappa_G=zeta^2, D0=a0/zeta, so both W and H have
  energy-density units; W=H-D^2/2 has the correct coefficient.
- Positive-domain restrictions and boundary terms are explicit. The radial
  force equality is a dust equilibrium, not a statement about a warm or neutral
  multispecies halo.
- The vector Laplacian has the -2P/r^2 term; retaining it is essential to the
  stiffness ratio.
- The static kinetic Hessian is zero and the dust replacement's Hessian is
  positive only for physical rho_c>0. The negative-divergence witness is off
  shell; it is not advertised as a negative-density physical solution.
- The exact maximum and crossing bracket repair a numerical interpretation,
  with G4=false and all raw source outputs unchanged. The diagnostic is a
  residual on a gamma-zero profile, not a finite-gamma solution estimate.
- The algebraic Lean artifact is pinned and inspected as source evidence; this
  audit does not claim a fresh Lean execution or that Lean certifies dynamics.

No external theorem or novelty claim is needed for these elementary local
identities. The proof is in REPORT.md; the executable assertions support its
implementation and the source-record discrepancy, and do not replace the
stated hypotheses or physical interpretation.
