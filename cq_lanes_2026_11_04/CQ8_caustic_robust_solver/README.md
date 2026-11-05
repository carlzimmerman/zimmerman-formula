# CQ8_caustic_robust_solver: NOT EVALUABLE (control failed: K-dt, grid-scale acceleration not converged in the time step)

κ = ½ FITTED; not theory closed. Criteria `FROZEN_CRITERIA.md` (2b11436345, committed alone first); script `cq8.py`
(81d7037208, committed before any graded number). No amendments; the frozen label stands.
- Not blind (CQ6's numbers were read first). Adopts nothing.
- a0 does not enter, so both footings give the same numbers and nothing is pooled.
- No particle. The cold sector stays retired. No data are used; nothing here says the data favour the framework.

## Plain statement

The adaptive implicit midpoint gets every regulated run through the first bounce without a blow-up or a crossing, on
every grid and every λ (CQ6's fixed-step solver died at t ≈ 3.1–3.2). But no run gets far past it within the frozen
180 s wall cap (t_last 3.15–4.35, against t_end = 65.8), the step collapses to ~1e-6–1e-7 τ after the bounce, and the
time-step control fails on the grid-scale acceleration. So neither SETTLES nor OSCILLATES can be graded, and the
ILL-POSED line cannot be certified. Row 12 ("past the first caustic no") is unchanged.

## Controls

| Check | Result | Line | Pass? |
|---|---|---|---|
| K-ZEL (λ = 0) | crossing t = 3.0000008 / 2.999982 / 2.999978 (N 256/512/1024) | 1 % of 3 | pass |
| MUTATE (λ = 0) | crosses on all three grids | must cross | pass |
| K-CQ6a | `cq6.run` at its settings: BLOW-UP at t = 3.216 | 3.216 ± 1e-3 | pass |
| K-CQ6b | ρ_c(t_c) 5.551 / 5.614 / 5.600 vs CQ6 5.561 / 5.596 / 5.600 | 1 % | pass |
| **K-dt** (N 512, λ 1e-8, tol 1e-4 vs 1e-5, t ≤ 3.25) | ρ_c 0.35 %, R_v 0.10 %, **max\|a\| 62 %** | 2 %, 2 %, 10 % | **FAIL** |
| (reported) tol 1e-3 vs 1e-4, t ≤ 3.3 | ρ_c 0.55 %, R_v 0.25 %, max\|a\| 131 % | — | — |

The core (ρ_c, R_v) is converged in the step to < 1 %; the largest sheet acceleration is not.

## Per-λ outcome (`cq8_results.json`; all regulated runs end WALL at 180 s, none BLOW-UP)

| λ | t_last N 256/512/1024 | t* | max\|a\| at t*, N 256/512/1024 | ratio per doubling | energy max\|ΔE\|/K_max | per-λ |
|---|---|---|---|---|---|---|
| 1e-8 | 3.60 / 3.30 / 3.15 | 3.15 | 400 / 1057 / 3858 | 2.6, 3.7 | 0.15 / 1.5e-3 / 6.4e-5 | NOT EVALUABLE (t* < 3.3) |
| 1e-7 | 3.85 / 3.45 / 3.25 | 3.25 | 340 / 754 / 2311 | 2.2, 3.1 | 0.18 / 4.6e-4 / 6.3e-5 | NOT EVALUABLE (t* < 3.3) |
| 1e-6 | 4.35 / 3.70 / 3.45 | 3.45 | 37 / 281 / 1070 | 7.6, 3.8 | 0.44 / 2.5e-4 / 4.8e-5 | NOT EVALUABLE (growth line met, K-dt failed) |

ρ_c(t_c) falls with λ: 5.60 / 4.02 / 2.89. The N 256 runs lose energy conservation after the bounce (0.15–0.44 K_max);
the N 512/1024 runs hold it to ≤ 1.5e-3.

## Reading (no label weight)

At every λ the grid-scale acceleration grows by 2–8× per grid doubling once past t_c, the pattern CQ6's explicit
diagnostic showed, and ×100 in λ does not stop it. That leans toward ILL-POSED (the quartic regulator vanishes where ρ'
= 0 and does not cap gradient steepening at the grid scale), but the frozen machinery cannot certify it: the step ladder
does not converge max|a|, and the 180 s cap holds the common time at or below t ≈ 3.45.

## What would decide it

A run to t ≳ 4 at N 512/1024 with the step ladder converged on max|a| (or a grid-scale statistic smoother than a single
sheet's acceleration, frozen in advance), which at the observed post-bounce dt ~1e-6 τ needs ≳ 1e6 implicit steps per
run, hours on one thread with checkpointing. AZ16's nondegenerate |∇ρ|²/ρ add-on remains a pointer, not adopted.

## Files

| File | Contents |
|---|---|
| `FROZEN_CRITERIA.md` | the frozen criteria |
| `cq8.py` | the script; `nice -n 10 python3 cq8.py all` (one thread, < 1 GB, about 37 min) |
| `cq8.out` | run log |
| `cq8_results.json` | controls, per-λ analysis, label |
| `runs/*.json`, `runs/*_series.npz` | per-run summaries and 0.05 τ series (KCQ6_R256 is cq6.py's own run) |

κ = ½ FITTED; not theory closed.
