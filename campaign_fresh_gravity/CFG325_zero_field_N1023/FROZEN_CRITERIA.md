# CFG325 FROZEN CRITERIA: N = 1023 decider for the zero-field nonlinear question (recipe G5/G10)

**Lane:** orchestrator. The owner asked to push the local machine on computations that move the programme toward closure.
**Question:** CFG322 (16139a770, results 89ef1f50f) left CFG321's FAIL OPEN. At ε = 1e-3, λ(N) almost levels off at N = 511 (ratios 0.86, 0.23). At ε = 1e-4 it is still rising (ratios 0.98, 0.80). CFG322 named N = 1023 as the decider.

## Method (no changes beyond the grid)
- **Engine:** cfg325_engine.py is byte-identical to CFG321's engine. The script checks its sha256 (bde2fbb6…) against CFG321's.
- **Unchanged from CFG322:** the ν_mono kernel, data class, seeds, perturbation pairs (δ = 0, 1e-3, 1e-5), T1D, the Lyapunov window, ZERO = 0.005, and the regularity rows.
- **Grids:** NS = (63, 127, 255, 511, 1023).
- **Reuse:** the N ≤ 511 runs are reused from CFG322's committed-run work arrays, copied under the cfg325_ prefix (CFG325_REUSE=1). Only the N = 1023 runs (and the cheap GR control at 1023) are new.
- **Only change to the statistic:** the frozen ratio rule is evaluated on the four finest grids, NA = (127, 255, 511, 1023):
  - increments Δ1 = λ255 − λ127, Δ2 = λ511 − λ255, Δ3 = λ1023 − λ511;
  - ratios r2 = Δ2/Δ1, r3 = Δ3/Δ2.

## Decision rule (CFG322's, shifted one grid finer)
Per ε set (1e-3, 1e-4):
- **RESOLVED-CONVERGENT:** |r2| ≤ 0.6, |r3| ≤ 0.6, and a finite λ_∞.
- **CONFIRMED-FAIL:** Δ3 ≥ 0.005 and r3 ≥ 0.9.
- **OPEN:** anything else.

Lane verdict:
- **CONVERGENT** if both sets are RESOLVED-CONVERGENT. G5/G10 nonlinear dependence then becomes CONDITIONAL, scoped to data class D and 1-D.
- **FAIL** if either set is CONFIRMED-FAIL.
- **OPEN** otherwise.

## Controls
- **C1:** reused N ≤ 511 λ values reproduce CFG322's printed λ table exactly (by construction; printed).
- **C2:** the GR control (MOND off) converges at order ≈ 2 through N = 1023.
- **Regularity:** every ν_mono run is regular (zero indefinite Hessians, leaf residual ≤ 1e-8).
- **MUTATE:** CFG322's μ_exp MUTATE stands as the discrimination control (it branched at every N). It is not re-run, which is disclosed.

## Scope
This says nothing about growth. The chassis growth failure (L341 + AUDIT_SIGMA8) stands regardless.

## Pre-freeze disclosure
Before this freeze, no N = 1023 run was performed by this lane. The CFG322 agent's timing probes estimated 2–3 h at ε = 1e-3 and 6–8 h at ε = 1e-4.
