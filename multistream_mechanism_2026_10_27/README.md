# Multistream core mechanism, 2026-10-27

Read [RESULTS.md](RESULTS.md) for the result and its limits, then
[NEXT.md](NEXT.md) for the unresolved physical implication. The original target
and route ownership are in [TARGET.md](TARGET.md).

Working conditional ingredients:

- [Logarithmic core response, stable mode and reciprocal outlet](eos_route/DERIVATION.md).
- [Energy-transfer plot](energy_transfer.png), from the audited finite-source
  simulation in synthetic units.
- [Independent core stability calculation](gravothermal_route/REPORT.md).
- [Conserving kinetic construction and its stopping failure](kinetic_route/DERIVATION.md).
- [Field activation, compulsory reaction terms and coefficient obstruction](field_route/REPORT.md).

The full mechanism is not derived: the microscopic phase response, exact
Lambda coefficient, live envelope and nonlinear cold formation remain open.
The results do not upgrade any existing observational lane.

Current bounded evidence records:

| Record | Scope |
|---|---|
| eos_route/run/manifest.json | Equilibrium, radial mode and ideal half-line outlet |
| eos_route/run_wave_audited/manifest.json | Reciprocal finite-source wave transfer, refinement and incoming-wave check |
| gravothermal_route/eos_review_run/manifest.json | Independent finite-element stability review |
| gravothermal_route/run/manifest.json | Heat-capacity and gravity-only obstructions |
| kinetic_route/run_001/manifest.json | Collision invariants, entropy sign, ballistic flux, stop-valve counterexamples |
| field_route/run/manifest.json | Full stress-gate variation, healthy local scalar branch and missing normalization |
| eos_route/run_homology/manifest.json | Failed below-barrier assertion; two finite variational-radius trajectories retained |

Each manifest records the command, inputs, limits, software and actual status.
Validate a current record from the repository root with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py multistream_mechanism_2026_10_27/eos_route/run_wave_audited/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Historical wave records preserve the source snapshots that generated them.
Later instrumentation changed the live script's input hash. Those originals
are historical evidence, not freshness certificates for the current script.
Failed runs retain their failures; see RESULTS.md and eos_route/DERIVATION.md.

No background job or automation was created. All calculations were bounded
local diagnostics; no production halo evolution was attempted.
