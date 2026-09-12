# Commands, exits, and provenance

All commands ran from /Users/carlzimmerman/new_physics/zimmerman-formula. No Git mutation was performed by this agent.

## Exploratory TDD history

The exact unit command throughout development was:

```sh
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current -p 'test_*.py' -v
```

Initial tests failed with exit 1 (seven assertion failures for the missing implementation). The first implementation passed seven tests with exit 0. Additional center/time-range tests initially errored on absent dictionary fields (exit 1); assertions were adjusted to expose missing features as failures, and the expected two assertion failures were observed (exit 1). Implementation then passed eight tests (exit 0). The timelike witness, exact interval-sign certification, and charge-sign reporting were each added only after the corresponding missing-behavior test failed (exit 1), followed each time by the nine-test suite passing (exit 0). These intermediate source states and full logs are not archived; they are reported exploratory history, not independently replayable pinned runs.

## Source-pinned production run

Exact launch command:

```sh
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current/contract.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current/current_audit.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current/test_current_audit.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_002/result.json --input qwen_claude_field_theory/papers_2026/PAPER19_gradient_criticality_2026.tex --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current/run_001 --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current/run_001/result.json --timeout 120 --max-output-bytes 2097152 --max-cpu-seconds 100 --max-threads 1 -- /bin/bash -c 'python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current -p "test_*.py" -v && python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current/current_audit.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current/run_001/result.json'
```

Launcher exit 0; child exit 0; nine tests pass; runtime 1.811373 seconds. Logs, result, source hashes, software versions, limits, and actual HEAD are retained in run_001/manifest.json and its sibling artifacts. The source file remained unchanged after this run. The manifest records concurrent HEAD 9212f4498479039fb37dba5e71ef8452d28249dd, whereas initial inspection returned 73877327897db83402d32e02fe301d240cb6c113.

Exact current-input validation command:

```sh
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Exit 0: valid evidence record; mathematical interpretation requires review.

## Supplementary exact center identity

After the pinned main run, the following direct SymPy check was executed without editing executable source:

```sh
python3 -B -c "import sympy as s; PX,WY,Q,g=s.symbols('PX WY Q gamma',nonzero=True); a=-(PX-WY)/(2*g); residual=s.simplify(2*Q*(PX+3*g*a)-Q*(3*WY-PX)); print(residual); assert residual==0"
```

Exit 0, exact output 0. This supplementary command is not represented as an additional provenance-manifest run.

Independent original-source evaluation of the limiting charge sign:

```sh
python3 -B -c "import importlib.util; p='qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py'; sp=importlib.util.spec_from_file_location('source',p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); bg,flow,names,jets=m.functions(); Q=.9078321505772312; z=dict(zip(names,jets(*bg(1.,.1,.5),Q*Q,0.,1e-6))); print('PX0=',z['P_X'],'WY0=',z['W_Y'],'Jt_center=',Q*(3*z['W_Y']-z['P_X'])); assert Q*(3*z['W_Y']-z['P_X'])<0"
```

Exit 0; PX0=0.05352035108375512, WY0=0.005000000000000001, Jt_center=-0.03497001316535539. The constitutive source is the same hash pinned by run_001.

## Proofreading scope

Self-reviewed REPORT.md equations, definitions, current-sign convention, coordinate-Q/physical-Q distinction, explicit time dependence, regularity hypotheses, polynomial sign filter, and the bounded/non-Einstein interpretation. No mathematical-token correction was needed; no unrelated manuscript was edited.
