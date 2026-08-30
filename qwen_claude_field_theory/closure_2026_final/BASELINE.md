# BASELINE — IMMUTABLE

This file is the immutable baseline for the `closure_2026_final` audit. It must never
be overwritten or edited. All work in this directory is measured against the state
recorded here.

## Repository identity

- Repository: `/Users/carlzimmerman/new_physics/zimmerman-formula`
- `git rev-parse HEAD` (starting commit): `597d23c1ae8aad91907a8cd7fc544b5de0df7578`
- Current branch: `main`
- Main branch (PR target): `main`

## Environment

- Platform: darwin (macOS), Darwin 25.5.0
- Date/time at baseline: Sun Aug 23 22:29:10 EDT 2026
- Python: 3.13.9
- Symbolic packages: sympy 1.13.1
- Numerical packages: numpy 1.26.4, scipy 1.14.1, mpmath 1.3.0
- NOT installed: numba, autograd, jax

## git status --short at baseline

```
 M ai_slop/carl_journal_8.7.26
 M qwen_38_experiment/ESCALATE.md
 M qwen_38_experiment/LEDGER.md
 M qwen_38_experiment/NEGATIVE_RESULTS.md
 M qwen_38_experiment/REFUTATION_DUTY.md
 M qwen_38_experiment/REGISTRY_FDR.md
?? DeltaL2s_checkpoint.txt
?? L2s_checkpoint.txt
?? nbody_2026/stage77_reaudit_lensing_source_2026.py
?? nbody_2026/stage78_reaudit_stage7_warmdust_2026.py
?? nbody_2026/stage79_reaudit_polytrope_halo_2026.py
?? nbody_2026/stage80_reaudit_massconserved_rar_2026.py
?? qwen_38_experiment/ESCALATION_DIGEST.md
?? qwen_38_experiment/T011_EQUIV_TABLE.md
?? qwen_38_experiment/T012_BETA_STABILITY.md
?? qwen_38_experiment/runs/D001_filter_calibration.py
?? qwen_38_experiment/runs/D002_noncharge_pressure.py
?? qwen_38_experiment/runs/d001_specs/
?? qwen_38_experiment/runs/d002_specs/
?? qwen_38_experiment/runs/t013_a0z_beta_interval.py
?? real_research/reviews/mi_ghost_condensate_spherical_collapse_2026.out
?? real_research/reviews/typeII_direct_variation_2026.py
?? run2.pid
```

All pre-existing modifications and untracked files are OUT OF SCOPE. This audit creates
only files under `qwen_claude_field_theory/closure_2026_final/`.

## Active candidate (FROZEN)

The active candidate is the **REPAIRED NORMALIZATION** relativistic MOND field theory.

### Action

```
S_tot = S_m[g,psi]
      + (c^3 / 16 pi G) * int d^4x sqrt(-g) [ R - 2 Lambda - (a_0^2 / c^4) M[g] ]
```

The factor `-(a_0^2/c^4) M[g]` (NOT `-(2 a_0^2/c^4) M`) is the repaired normalization.
The earlier factor of two is REJECTED because it produced `mu_wrong = 1 - 4 F'(Z)` and
therefore `mu -> -1` in the deep-MOND limit. The repaired coefficient gives the intended
structure `mu(y) = 1 - 2 F'(Z)`.

### Functional chain (FROZEN)

```
g_{mu nu} -> T[g] -> U_mu[g] -> Phi[g] -> Z[g] -> M[g]
```

1. Timelike scalar: `U_mu = -nabla_mu T`, with `nabla_mu T nabla^mu T = -1` (unit normalization).
2. Retarded curvature response: `Box_ret Phi = R_{mu nu} U^mu U^nu` (retarded solution).
3. Constitutive scalar: `Z = (4 c^4 / a_0^2) nabla_mu Phi nabla^mu Phi`.
4. Constitutive function (for Z >= epsilon):
   `F_+(Z) = 4 [ 1 - (1 + sqrt(Z)/2) e^{-sqrt(Z)/2} ]`,
   `F_+'(Z) = (1/2) e^{-sqrt(Z)/2}`.
   With `Z = 4 y^2`, `y >= 0`: `F_+'(Z) = (1/2) e^{-y}`, hence `mu(y) = 1 - 2 F'(Z) = 1 - e^{-y}`.
5. C^2 regulator: `F_epsilon` matches value, F', F'' at both endpoints `|Z| = epsilon`.
6. Transport definition of M:
   `nabla_mu [ U^mu (M + F_epsilon(Z)) ] = 0`.
   Intended isolated stationary branch: `M ~= -F_epsilon(Z)` (a TARGET, not an axiom).

### Established (starting point, do not re-prove)

- repaired factor-of-two normalization;
- exponential constitutive branch;
- MOND asymptotic algebra (`mu(y) = 1 - e^{-y}`);
- C^2 regulator constructibility (to be independently verified);
- existence of the naive mixed auxiliary Hessian warning (to be analyzed, not yet a proof).

### NOT established (to be determined)

- complete causal variational formulation;
- physical ghost absence;
- complete constraint structure;
- complete metric equations;
- lensing;
- PPN;
- cosmological closure;
- nonlinear consistency.

## Isolation rule

All new work MUST remain inside `qwen_claude_field_theory/closure_2026_final/`.
Previous generations (`closure_2026/`, `gates_2026/`, `theory_2026/`, `qwen_38_experiment/`,
etc.) may be READ for context but must NOT be modified. They analyzed a DIFFERENT
candidate (Deffayet-Woodard form with a different f(Z)); their conclusions are NOT
imported.
