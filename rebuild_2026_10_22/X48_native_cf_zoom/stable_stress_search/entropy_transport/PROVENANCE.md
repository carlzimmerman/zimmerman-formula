# Bounded experiments and provenance

Phase base: X48-TRANSPORT-2026-11-01-A, revision
`c4b97598e8b6b408dd75d724ea469a81a2bd4ea9`, with a dirty shared worktree.
Every run records its actual execution revision and dirty state. This phase
adds experimental material/transport code and data under this directory;
frozen X48 production engines, jobs, acceptance criteria and grades are not
replaced. The inherited material, mechanics and static solver remain inputs.

For each directory NAME below, `NAME_contract.json` declares the mathematics,
finite range, conventions, non-claims, software and complete supplied input
list before execution. `NAME/manifest.json` records the command, limits,
before/after input hashes and output hashes; `result.json`, `stdout.txt`, and
`stderr.txt` are retained. Source and result files pinned by those manifests
must remain unchanged. Interpret process status together with the physical
driver's status: a wall-limited run is a valid record of an incomplete attempt.

| Records | Interpretation |
| --- | --- |
| `n32_D01_t4`, `n64_D01_t4`, `n32_D01_t16` | Persistent thermal transport controls; continued central contraction, not stable settling |
| `n32_D0_t4` | Damping-only control; tiny motion does not repair adverse entropy ordering |
| `thermal_branch` | Bounded regular isothermal-branch exploration; no exhaustive energy-minimum theorem |
| `conv_n32_t8`, `conv_n64_t8` | First fixed-coefficient gated transport runs; extended because t8 settling criteria were not all met |
| `floor_n32_t32`, `floor_n64_t32` | Identity continuations of matching t8 records; original-energy error includes ancestors |
| `floor_n128_t32`, `floor_n256_t32` | Virgin collapse, exact cold invariant phase then full transport; completed t32 |
| `steady_n64_t64`, `entropy_mode_n64_t64` | Completed baseline and prepared energy-neutral entropy perturbation |
| `compress_n64_t64`, `compress_n64_finish` | Wall-limited compression attempt, then exact-state continuation to t64 |
| `expand_n64_t64`, `expand_n64_finish` | Two historical wall-limited Radau expansion attempts |
| `bdf_switch_check`, `bdf_expand_t64` | Actual BDF with unchanged RHS/parameters; exact-state expansion continuation to t64 |
| `tight_n256_t32`, `tight_n256_finish` | Tighter-time Radau attempt, wall-limited at t28.1267; exact-state completion to t32 |
| `isentropic_prediction` | Independent continuum mass/energy-only regular stationary prediction |
| `analysis` | Immutable v1 data analysis; energy bounds concern accepted states, despite the less explicit field names |
| `analysis_v2` | Current analysis: accepted-state ancestry bounds and dense-output sample maxima reported separately |

The [methods note](NUMERICS.md) gives exact handoffs, caps, tolerances, sample
windows, and preparation energies. The continuation chains use the same law
and fixed material coefficients. A new integrator segment receives only the
recorded state, with no energy or entropy reset. Deliberate radius/entropy
perturbations are applied once before integration and their preparation work
is separate from evolution.

The analysis contracts' phrase “no interpolated observations” means the
analyzers introduce no new interpolation or synthetic t24/t56 observations.
The underlying solver diagnostics themselves include dense interpolation;
v2 explicitly audits their energy errors. The current tight-chain energy
numbers are separately reviewed outputs; the automatic tight-time gate tests
profile agreement, not those energy fields. All reported tests and inequalities
are finite floating-point evidence, not interval-certified error estimates.

The bounded runner is
`/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py`.
It ran under Python 3.11; numerical children use Python 3.9.6, NumPy 1.26.2
and SciPy 1.11.4. Plots use Matplotlib 3.9.4 with a temporary writable cache.
Run-specific contracts and manifests are the authoritative details.

Validate an individual manifest from the repository root:

```bash
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search/entropy_transport/analysis_v2/manifest.json --root "$PWD"
```

The current result and plot are [analysis_v2/summary.json](analysis_v2/summary.json)
and [analysis_v2/settling_refinement.png](analysis_v2/settling_refinement.png).
The historical [analysis manifest](analysis/manifest.json) remains valid;
its source was preserved and wrapped by the separate
[v2 analyzer](analyze_results_v2.py). No old result was rewritten to update
an interpretation. Final scoped checks are recorded in
[VERIFICATION.md](VERIFICATION.md).
