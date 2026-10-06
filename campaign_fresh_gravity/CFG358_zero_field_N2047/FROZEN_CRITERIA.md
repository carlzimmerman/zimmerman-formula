# CFG358 FROZEN CRITERIA: N = 2047, the final grid for the zero-field nonlinear question (recipe G5/G10)

**Lane:** orchestrator. The owner said "take this the final mile".

**State of the question.**
- CFG321 printed FAIL.
- CFG322 (N = 511) and CFG325 (N = 1023, independently recomputed MATCH) left it OPEN by the frozen letter.
- At ε = 1e-4, λ = 0.0762 / 0.0916 / 0.0875 for N = 255 / 511 / 1023.
- Increments: Δ = +0.0154 (255 → 511), then −0.0041 (511 → 1023).
- CFG328 (ε = 1e-5) levels off one grid earlier.

## Method
Everything is unchanged from CFG325: the engine (byte-identical to CFG321's, hash checked), the ν_mono kernel, data class D, the seeds, the δ pairs, T1D and the Lyapunov window. Only two things differ:
- **Grids:** NS = (63, 127, 255, 511, 1023, 2047).
- **Reuse:** runs with N ≤ 1023 are reused from CFG325's committed-run work arrays, copied under the cfg358_ prefix (CFG358_REUSE=1). Only the N = 2047 runs are new.

The frozen ratio rule is evaluated on the four finest grids, NA = (255, 511, 1023, 2047):
- increments Δ1 = λ511 − λ255, Δ2 = λ1023 − λ511, Δ3 = λ2047 − λ1023;
- ratios r2 = Δ2/Δ1 and r3 = Δ3/Δ2.

## Decision (CFG322's frozen rule, one grid finer)
Per ε set:
- **RESOLVED-CONVERGENT:** |r2| ≤ 0.6, |r3| ≤ 0.6 and a finite λ_∞;
- **CONFIRMED-FAIL:** Δ3 ≥ 0.005 and r3 ≥ 0.9;
- **OPEN:** anything else.

Lane verdict:
- **CONVERGENT** if both sets are RESOLVED-CONVERGENT. G5/G10's nonlinear-dependence item then becomes CONDITIONAL, scoped to data class D and 1-D.
- **FAIL** if either set is CONFIRMED-FAIL.
- **OPEN** otherwise.

## Controls
- **C1:** CFG321's ε = 1e-3 rows are reproduced (via reuse).
- **C2:** the GR control converges at order ≈ 2 through N = 2047.
- **Regularity:** every ν_mono run is regular.
- **MUTATE:** CFG322's μ_exp MUTATE stands; it is not re-run, which is disclosed.

## Scope
Nothing about growth: the bare-chassis growth failure (L341 + AUDIT_SIGMA8) stands.

## Pre-freeze disclosure
No N = 2047 run has been performed. Estimated cost: about 15–20 h at ε = 1e-4 and about 6 h at ε = 1e-3, in parallel.
