# Sourced-clock checkpoint: results and reproduction

Full objective: **OPEN**. No complete relativistic MOND theory or new empirical
law is certified here. The current scalar action remains a hypothesis with
reconstructed coefficients, not a first-principles derivation of the framework.

## Mathematical result

The complete spherical metric/clock equations and an explicit dynamical dust
sector are now varied from the same covariant action. All third derivatives
cancel from the five spherical gravitational/chi equations. This is not a
nonlinear Dirac classification or a proof that every solution is healthy.

The exact enclosed-charge identity is

    j_chi(t,r) = -partial_t integral_0^r p_chi(t,s) ds

when the central current vanishes. The shift charge is a clock quantity, not
baryonic mass. This identifies the time-current term omitted by the earlier
restricted static obstruction, without assuming it restores MOND.

In the linear sourced reduction, baryon density generates an affine source in
both the physical scalar equation and its constraint. Lean checks the complete
sourced elimination and the matching of physical to canonical initial data.
Neither MOND nor a PPN value is a premise or an output of those Lean lemmas.

## Executed numerical result (pinned final run, exit 0)

Fixed background M2=Qc=1, I=.1, Lambda=.7, m(1)=.1, v(1)=.5;
gamma=0 or 1e-6; common u=udot=0 at ln(a)=-1; modes k=.01..800;
integration to ln(a)=.01; metric checks at -.7,-.35,0. No raw observations used.
These are dimensionless cosmological linear-response benchmarks, not an
assignment of these widths to observed galactic sizes or a CMB calculation.

For gamma=1e-6 at a=1, Gaussian mass M_b=1e-8, compare r=3R_b to
2r for a source of four times the mass and twice the width:

| R_b | force / bare-Einstein Gaussian force | matched force ratio g(4M_b,2r)/g(M_b,r) |
| --- | --- | --- |
| .02 | 1.0012986418886651 | 1.0033821196906363 |
| .04 | 1.0046851537416042 | 1.0101496378556667 |
| .08 | 1.0148823442110464 | 1.0232311269447107 |

The action-derived Phi and Psi agree to a maximum relative discrepancy
1.654e-15 over the sampled modes/epochs; they were calculated separately.
The largest DOP853/Radau Phi discrepancy is 3.798e-13 across both couplings and
all refined runs. Complex-step refinement differs by at most 2.163e-15;
the independent finite-difference derivative control differs by at most 2.881e-10.

Radial quadrature refinement, maximum relative change of reported forces and
matched ratios: 129→257 modes: 2.582e-8; 257→513: 1.688e-14.
These are empirical numerical convergence diagnostics on a fixed k interval,
not certified interval bounds or an infinite-domain truncation proof.
The earlier 65-mode control had a roughly 1e-3 radial integration error despite
excellent ODE agreement. It is superseded for numerical interpretation.

At fixed radius, four times the source produces four times the force in this
linear calculation. This is a property of the derived linear equations, not an
independent prediction obtained from a nonlinear solver. The deep-MOND target
would instead approach a factor of two. Establishing an obstruction to the
full nonlinear action would additionally require control of its small-source
limit and possible singular branches. No universal no-go is asserted.

## Verification status

The pinned aggregate run completed in 401.377 seconds, exit 0. All ten jobs
exited 0; the manifest validator also exited 0 and verified declared source
freshness and result hashes against the working tree.

| Important check | Exit |
| --- | --- |
| Sourced action variation | 0 |
| Forced response and 129/257/513-mode refinement | 0 |
| Full nonlinear spherical variation | 0 |
| Dynamical spherical dust | 0 |
| Source behavior tests | 0 |
| Independent Newtonian radial-transform control | 0 |
| SourceSchur.lean | 0 |
| Existing covariant-current regression | 0 |
| Existing homogeneous-background regression | 0 |
| Existing tensor-sector regression | 0 |

Parallel repository work advanced HEAD from the base through `019d08674` to
`d6626d97f`. None of this run's declared inputs changed in those commits;
the source-hash validation and explicit path diff confirmed that. No verdict
from the separate L169 model is imported into this action.

The source variation has 15 exact checks plus a wrong-sign source control;
the full spherical variation has 36 exact checks; the dynamical dust sector
has 32 exact checks and three negative controls. SourceSchur.lean contains five
checked algebraic theorems using only the listed standard Lean axioms.

## Commands and artifacts

All important subprocess commands, working directories, stdout, stderr and
exit statuses are recorded verbatim in run_001/checks.json. The launcher is:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/contract.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/source.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/response.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/test_source.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/test_response.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/run_checks.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/SourceSchur.lean --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/action/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/action/matter.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_finite_wavelength/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_finite_wavelength/tensor_gate.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_current_audit/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_background_completion/derive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_transport/stationary.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_evolution/inverse_entropy_clock.py --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lakefile.toml --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/run_001 --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/run_001/checks.json --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/run_001/source.json --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/run_001/response.json --timeout 1200 --max-output-bytes 2097152 --max-cpu-seconds 900 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/run_checks.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/run_001/checks.json
```

Validate its evidence record with:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Development controls were also run directly: test_source.py first failed
(exit 1, implementation absent), then passed (exit 0); test_response.py first
failed (exit 1, implementation absent), then passed its independent Newtonian
Gaussian check (exit 0). Exploratory response.py --modes 65 and
response.py --modes 129 --refine both exited 0; their scratch outputs are not
the durable evidence record. No failing physical gate was changed to a pass.

Created files are confined to this directory: README.md, PLAN.md, RESULTS.md,
source.py, response.py, test_source.py, test_response.py, run_checks.py,
contract.json, SourceSchur.lean, LEAN.md, action/derive.py, action/REPORT.md,
action/matter.py, action/MATTER.md, and generated run_001 evidence files.
No prior research files were changed by this checkpoint. All edits remain in
the displayed package; unrelated parallel work was preserved.

Independent review checked source signs, physical potentials, initial data,
third-derivative cancellation and the Ward recovery of the clock equation.
It identified the radial-quadrature issue; the refined run addresses it.
The review also requested explicit numerical thresholds, now enforced for
ODE agreement, no-slip, complex-step and final radial refinement. The
finite-difference control is recorded separately, not silently certified.

## Next unavoidable construction calculation

Canonicalize the full spherical system and solve its nonlinear lapse, metric,
clock and matter initial constraints with common cosmological boundary data.
Then evolve the exact dust and clock currents, rather than fixing either halo
profile, and compare the two finite-mass sources. A pressure-supported or
multistream matter model will be needed beyond the single-stream dust domain.
Recover the present linear response as a convergence/control limit of that
solver before testing the exponential constitutive law. The required global
constraint count, PPN, CMB, zero-field/zero-mode control and first-principles
coefficient selection remain open.
