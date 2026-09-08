# Reproduction and exact checkpoint inventory

Working directory: /Users/carlzimmerman/new_physics/zimmerman-formula.
Base revision: 92ff5f9703bfa9fccc1097fcbbc081e004b548ec.
Python 3.13.9; SymPy 1.13.1; NumPy 1.26.4; SciPy 1.14.1.
No dependency was installed, no empirical dataset changed, no Lean proof run.

## A. Exact files created

All twenty paths have prefix `qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/`:

- DECISION.md
- FORMAL_VERIFICATION_PATH.md
- REPRODUCE.md
- contract.json
- spatial_kernel_gate.py
- test_spatial_kernel_gate.py
- trace_hamiltonian.py
- test_trace_hamiltonian.py
- legacy_constraint_audit.py
- test_legacy_constraint_audit.py
- causal_response.py
- test_causal_response.py
- adaptive_endpoint.py
- test_adaptive_endpoint.py
- research_gate.py
- test_research_gate.py
- run_001/manifest.json
- run_001/result.json
- run_001/stdout.txt
- run_001/stderr.txt

No pre-existing tracked file was edited by this checkpoint. Unrelated dirty
and untracked work is preserved. Older source files are read-only inputs,
not silently corrected or re-certified.

## B–C. Important commands executed and observed exit statuses

These are the actual computational command arguments; not every read-only
file inspection is repeated. The independent CLI batch launched the listed
commands with Python subprocesses, captured stdout/stderr, and reported each
child's exit status. It did not equate a batch exit 0 with physics closure.

```bash
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/constraint_response_gate_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/gate1_constitutive_2026 -p 'test_*.py'
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026 -p 'test_*.py'
```

| Suite | Tests | Exit |
| --- | ---: | ---: |
| New constraint-response suite | 50 | 0 |
| Lapse braiding | 32 | 0 |
| Expansion switch | 22 | 0 |
| VCDM FLRW | 10 | 0 |
| Constitutive Gate 1 | 8 | 0 |
| Cluster measurement audit | 9 | 0 |
| Total | 131 | all 0 |

Every new scientific script was also run through its entry point.
With OPENBLAS_NUM_THREADS=1, these actual child commands were executed:

| Command | Exit | Meaning |
| --- | ---: | --- |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/spatial_kernel_gate.py --require-matter-gate | 0 | The displayed matter gate passes only |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/trace_hamiltonian.py | 0 | Legendre/homogeneous derivations complete |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/legacy_constraint_audit.py | 0 | Audit computes the legacy failures |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/legacy_constraint_audit.py --require-legacy-closure | 2 | Legacy closure rejected |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/causal_response.py | 0 | Both response derivations complete |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/causal_response.py --require-causal-response | 2 | Flat constant-alpha control family fails its causal gate |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/causal_response.py --require-adaptive-causal-response | 2 | Lambda=0 adaptive signed-probe causal gate fails |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/adaptive_endpoint.py | 0 | Both endpoint branches evaluated |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/adaptive_endpoint.py --require-stable-endpoint | 2 | Original b=1/4 curvature endpoint fails |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/adaptive_endpoint.py --require-stable-endpoint --use-derived-cancellation | 0 | Selected b=3/16 passes displayed curvature screen only |
| python -B qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/research_gate.py --require-closure | 2 | Same-action target remains incomplete |

The provenance run below executes the aggregate default command, exit 0.
It captures all numerical summaries and symbolic evidence in result.json.
The manifest records 18 pinned source/report artifacts, the actual dirty base,
runtime, bounds, software and output hashes. Its success does not certify a
full nonlinear theory. Use a new output directory for another recorded run;
the existing run is intentionally not overwritten.

```bash
'python' '-B' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' '/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/contract.json' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/spatial_kernel_gate.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/test_spatial_kernel_gate.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/trace_hamiltonian.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/test_trace_hamiltonian.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/legacy_constraint_audit.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/test_legacy_constraint_audit.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/causal_response.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/test_causal_response.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/adaptive_endpoint.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/test_adaptive_endpoint.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/research_gate.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/test_research_gate.py' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/DECISION.md' '--input' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/FORMAL_VERIFICATION_PATH.md' '--input' 'qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/vcdm_flrw.py' '--input' 'qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/conformal_action.py' '--input' 'qwen_claude_field_theory/closure_2026/sf58_full_nonlinear_adm_four_constraint_closure.py' '--input' 'qwen_claude_field_theory/closure_2026/elliptic_corner/constrained_hamiltonian.py' '--output' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/run_001' '--result' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/run_001/result.json' '--timeout' '60' '--max-output-bytes' '1048576' '--max-threads' '1' '--max-cpu-seconds' '45' '--' 'python' '-B' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/research_gate.py' '--output' 'qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/run_001/result.json'
python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Recorded runner exit: 0. Manifest validator exit: 0.

An original certification script was independently executed unchanged:

```bash
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/sf58_full_nonlinear_adm_four_constraint_closure.py
```

It exits 0 while printing that p_q is unconstrained despite its K p_q=0
constraint. The new audit disproves that statement within the implemented
mechanical system. This is a concrete example of why exit 0 is insufficient.

Development red/green checks were not hidden: new tests initially exited 1
for absent modules/fields; the missing zero-enthalpy and explicit-time-drift
features were implemented before the final green suite. One structural
SymPy equality check was changed to test the simplified difference; the
formula itself was unchanged. Endpoint numerics exposed amplification of an
absolute tolerance floor in decaying u_dot; an exactly equivalent evolution
of a^3 u_dot resolved it and two tolerances were compared. These development
failures are not scientific acceptance passes.

Read-only repository checks included git status, git log -6 --oneline,
git diff --check, and git ls-remote origin refs/heads/main. The first sandboxed
remote check exited 128 because name resolution was restricted; the authorized
network retry exited 0 and returned the base hash above. Lean/Lake executable
lookups found neither on PATH. No inference about a Lean proof follows.

## D–F. Result and next calculation

The strongest result is the exact signed-conserved-probe obstruction for
every finite canonical subluminal K_s>=1 in the Lambda=0 adaptive family:
the exterior Weyl amplitude obeys |E_xx|>2 exp(-4)/(3 pi m K_s) at the stated
event. The independent positive-Lambda endpoint selects b=3/16 and has
bounded displayed curvature. These are parameter-distinct members, not a
full theory assembled by inheriting incompatible results.

Full theory: OPEN. Lambda=0 arbitrary-conserved-probe causal criterion: FAIL.
No healthy physical-matter realization or fixed-positive-Lambda causal
exclusion has been proved. Next: the exact positive-Lambda retarded source
calculation and an action-derived healthy-matter realization/exclusion,
before any full closure claim. DECISION.md lists the remaining gates.

Mathbox computation/proof auditing dictated the exact-action comparisons,
separate exceptional sectors, scoped counterexamples and immutable evidence.
Final mathematical self-review covered the new report and formulas: the
review caught and corrected “speed” to “speed squared” for 1/K_s, and kept
the Lambda=0 versus positive-Lambda clock distinction explicit. No unrelated
mathematical text was rewritten. The fluid-repository check was a bounded
primary-source literature inspection, not a proof build or novelty search.
