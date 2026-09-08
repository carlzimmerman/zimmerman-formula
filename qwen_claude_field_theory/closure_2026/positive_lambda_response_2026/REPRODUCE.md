# Reproduce the positive-Lambda response checkpoint

Working directory: /Users/carlzimmerman/new_physics/zimmerman-formula.
Base commit: c759c46ac02e6c09cd0c7c3cb206b8c31bbc1b97.
Python 3.13.9; SymPy 1.13.1; NumPy 1.26.4; SciPy 1.14.1.

## A. Exact checkpoint files

All 21 newly created files have this prefix:
`qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/`.

- DECISION.md
- REPRODUCE.md
- contract.json
- positive_lambda.py
- test_positive_lambda.py
- physical_initial_data.py
- test_physical_initial_data.py
- constraint_hessian.py
- test_constraint_hessian.py
- localized_auxiliary.py
- test_localized_auxiliary.py
- infrared_domain.py
- test_infrared_domain.py
- general_family.py
- test_general_family.py
- closure_extension.py
- test_closure_extension.py
- run_001/manifest.json
- run_001/result.json
- run_001/stdout.txt
- run_001/stderr.txt

No pre-existing tracked file was edited. All other dirty/untracked work is
preserved, including subsequent research in a separate screened-kernel directory.

## B–C. Exact important commands and observed exit statuses

These are the executed mathematical commands and their individual statuses.
Read-only source inspections are not reproduced exhaustively. No dependency
installation, empirical-data modification or Lean proof build was performed.

### Unit and closure regression tests

```bash
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/positive_lambda_response_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/constraint_response_gate_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/gate1_constitutive_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026 -p 'test_*.py'
```

| Suite | Tests | Exit |
| --- | ---: | ---: |
| positive_lambda_response_2026 | 55 | 0 |
| constraint_response_gate_2026 | 50 | 0 |
| lapse_braiding_gate_2026 | 32 | 0 |
| expansion_switch_gate_2026 | 22 | 0 |
| vcdm_flrw_gate_2026 | 10 | 0 |
| gate1_constitutive_2026 | 8 | 0 |
| cluster_measurement_audit_2026 | 9 | 0 |
| Total | 186 | all 0 |

The new suite was rerun after the final general-family change: positive-b
intervals now come from exact inequality solving, not interval labels chosen
from boundary roots. Its final run completed 55 tests in 25.055 seconds.

### Scientific entry points

Each row is an actual command. OPENBLAS_NUM_THREADS=1 was supplied to the
parent environment. Independent child processes were dispatched with
ThreadPoolExecutor(max_workers=3), using subprocess.run(shell=False), captured
stdout/stderr and a 90-second child timeout. Parallel suite processes were
also used. Concurrency does not alter the mathematical scope of a result.

| Command | Exit |
| --- | ---: |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/positive_lambda.py | 0 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/positive_lambda.py --require-causal-response | 2 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/physical_initial_data.py | 0 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/physical_initial_data.py --require-cauchy-locality | 2 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/constraint_hessian.py | 0 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/constraint_hessian.py --require-full-field-count | 2 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/localized_auxiliary.py | 0 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/localized_auxiliary.py --require-auxiliary-closure | 0 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/infrared_domain.py | 0 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/infrared_domain.py --require-finite-domain | 2 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/general_family.py | 0 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/general_family.py --require-cauchy-locality | 2 |
| python -B qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/closure_extension.py --require-closure | 2 |

Default exit 0 means the implemented derivations ran and their checks passed.
Exit 2 with a require flag means the requested physics gate failed or remains
unproved. The auxiliary-only closure passes; it is not a full gravity count.
The aggregate's default entry point was additionally executed by the runner
below, with the output argument shown, exit 0.

### Immutable bounded provenance run

All 19 execution artifacts are explicitly pinned, including every new script
and test, the decision report, all three imported older source modules and
the older action definition. The contract itself is also recorded by the
runner. The imported source bytes were independently compared to git show
at the base hash; all three matched. No source is authenticated merely by
printing a base_commit label. Use a fresh run directory for another run.

```bash
'python' '-B' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' '/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/contract.json' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/positive_lambda.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/test_positive_lambda.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/physical_initial_data.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/test_physical_initial_data.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/constraint_hessian.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/test_constraint_hessian.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/localized_auxiliary.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/test_localized_auxiliary.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/infrared_domain.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/test_infrared_domain.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/general_family.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/test_general_family.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/closure_extension.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/test_closure_extension.py' '--input' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/DECISION.md' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/causal_response.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/adaptive_endpoint.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/DECISION.md' '--input' 'qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/vcdm_flrw.py' '--output' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/run_001' '--result' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/run_001/result.json' '--timeout' '90' '--max-output-bytes' '1048576' '--max-threads' '1' '--max-cpu-seconds' '60' '--' 'python' '-B' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/closure_extension.py' '--output' 'qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/run_001/result.json'
python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/positive_lambda_response_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Runner exit: 0, status completed. Manifest validator exit: 0.
The validator expressly does not certify mathematical interpretation.
`run_001/result.json` records every derivation and the absent/failed gates.
Outputs and source hashes are not overwritten after recording.

### Development failures and audits

Tests-first development was used rather than hiding initial failures.
The first aggregate run before its module existed exited 5 (zero tests,
setUpClass import error on this Python version); its later missing-family
checks exited 1 before integration. The first homogeneous derivation suite
had an exact hyperbolic-expression simplification failure; normalizing as
rational functions of exponentials proved the residual zero without changing
the equation. The auxiliary CLI initially returned 0 even for failed algebra;
a regression test exposed it, and the CLI now returns 1 in both modes.
Other tests-first missing-module failures preceded the implementations.
These are development outcomes, not physics passes.
The initial staged whitespace check exited 2 for a trailing blank line in
this reproduction note. It stopped the commit; that line was removed before
retrying. No scientific input or recorded result changed.

Independent reviews checked the physical annular witness and homogeneous
brackets, the positive-Lambda source response, and the aggregate's separation
of hypotheses. A separate general-K derivation verified 39 exact identities.
Root inspected the final code and independently reran all reported suites.
Finite geometric checks and numerical samples are not universal proofs;
the support result additionally uses the explicit analytic energy/Green argument.

### Repository integration

Read-only checks included:

```bash
git status --short
git log -5 --oneline
git diff --check
git ls-remote origin refs/heads/main
```

All exited 0. The remote check returned the base revision above. Commit/push
are confined to the 21 files in section A; their actual result is reported
in the accompanying task response. No unrelated staged state is included.

## D–F. Strongest result, status, and next unavoidable calculation

The same positive-Lambda family derives K=9/(2b)-15. For every fixed finite
K>=1 (0<b<=9/32), a smooth annular canonical-matter initial perturbation has
the exact lower bound

    |Ehat_xy(t,0)| >= 633 epsilon q(t0)/(1600m) > 0

for 0<t-t0<=min[1/(20H(t0)), a(t0)/4], while original metric/matter canonical
data initially agree in the inner ball and light has not arrived from the
annulus. The Weyl-local term depending on K vanishes in that hole; tuning K
does not cancel the response. This is a linear original-canonical-data
Cauchy-locality obstruction, not a nonlinear lift or zero-past actuator proof.
Constrained localized inverse potentials need not agree in the ball.

The separate unprojected R3 nonlinear functional acquires a divergent
perturbation action starting at fourth order in a compact conformal amplitude.
The exact homogeneous rank is four and the auxiliary nonzero-mode rank is
six; neither is substituted for the full gravitational count.

Candidate status: DEAD at its regular finite-K>=1 linear locality gate.
Overall full-theory objective: OPEN. No universal MOND impossibility is claimed.

Next: derive a genuinely different spatial/clock kinetic structure and test
its physical retarded curvature and matter response before PPN or a full
constraint-count campaign. A screened inverse is being investigated separately;
no result from that different action is combined with this checkpoint.

Mathbox computation/proof audits enforced exact action provenance, explicit
exceptional sectors, negative controls and scoped conclusions. Self-proofreading
covered only this checkpoint's report and formulas; initial scale notation
was separated from the MOND acceleration scale. No unrelated manuscript changed.
