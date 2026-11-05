# CQ8_caustic_robust_solver: FROZEN CRITERIA (committed alone, before any script or number)

κ = ½ FITTED; not theory closed. Owner go 2026-11-04 ("swing them now"). Not blind: CQ6's numbers (blow-up at the first
bounce, t ≈ 3.1–3.2; its explicit diagnostic's max|a| growing with N) were read before freezing. Adopts nothing. No
particle; the cold sector stays retired. No data are used, so nothing here can say the data favour the framework. a0 does
not enter, so both footings give identical numbers and nothing is pooled.

## 0. Question

CQ6 (`cq_lanes_2026_11_04/CQ6_past_first_caustic/`) ran v3s's P(X) dust limit with AZ14's quartic regulator
F = λ∫|ρ'|⁴/ρ³ (astra's lane, read only) in planar 1D and was NOT EVALUABLE: its fixed-step implicit midpoint blew up at
the first bounce and its time-step control failed. **With a solver built for the bounce, is the regulated collapse
SETTLES, OSCILLATES WITHOUT SETTLING, or ILL-POSED?**

## 1. Equations, discretization, initial conditions: CQ6's, unchanged

CQ6 FROZEN_CRITERIA §1–2: Lagrangian sheets, m = 1/N, AZ17's discrete F_d, exact planar gravity with background
subtracted, periodic L = 1, 4πGρ̄ = 1, x = q − A sin 2πq with 2πA = 1/cosh 3 (Zel'dovich caustic at t_c = 3 τ exactly),
t_× = 2π, t_end = t_c + 10 t_× = 65.832, W5 = [34.416, 65.832], samples every 0.05 τ. CQ6's `cq6.py` is imported for the
model (forces, Jacobian, diagnostics); it is not edited.

## 2. Solver (the change)

- **Adaptive implicit midpoint** (symplectic, time-symmetric), Newton with CQ6's banded complex-step Jacobian and the
  positivity line search, initial guess from an explicit velocity-Verlet predictor.
- **Step control:** local error estimate err = max|x_impl − x_pred| / min_c Δ_c (displacement in units of the smallest
  cell). Accept if err ≤ tol; dt ← dt · clip(0.9 (tol/err)^{1/3}, 0.2, 2), dt ≤ 1e-2. Newton failure: halve dt and retry.
- **Canonical tol = 1e-4.** Time-step ladder: tol 1e-3 and 1e-5 at N 512, λ = 1e-8.
- **Run ends:** REACHED t_end; CROSSED (a cell width ≤ 0; only expected at λ = 0); BLOW-UP if dt < 1e-9 τ is needed;
  WALL if the run hits its wall cap of 180 s (label-neutral: the run's samples up to its last time are used).
- One thread, `nice -n 10`, < 1 GB. Each run writes its own JSON on completion (restart skips done runs), and SIGTERM
  writes a partial JSON (status SIGTERM).

## 3. Runs

- λ ∈ {1e-8 (CQ6's, FITTED), 1e-7, 1e-6} × N ∈ {256, 512, 1024} at tol 1e-4. N 2048 is not run (cost).
- Ladder: N 512, λ 1e-8, tol 1e-3 and 1e-5.
- MUTATE twin: λ = 0, N 256/512/1024, tol 1e-4.
- K-CQ6: `cq6.run` itself at its frozen settings (N 256, λ 1e-8, dt 1e-3), to t = 3.4.

## 4. Controls (known answers)

- **K-ZEL:** each λ = 0 run's first crossing within 1 % of t_c = 3. MUTATE passes if all three cross (none passes t_c).
- **K-CQ6a:** `cq6.run` reproduces CQ6's BLOW-UP at t = 3.216 (to 1e-3).
- **K-CQ6b:** this solver's ρ_c(t_c) at λ = 1e-8 within 1 % of CQ6's 5.561 / 5.596 / 5.600 (N 256 / 512 / 1024).
- **K-dt (ladder converged):** tol 1e-3, 1e-4, 1e-5 at N 512 agree on every common sample time t ≤ t*_L (the last time all
  three reach): ρ_c and R_v within 2 %, max|a| within 10 %; and if all blow up, t_fail within 2 %. Assessed on the
  tol 1e-4 vs 1e-5 pair (tol 1e-3 is reported).
Any control failing → NOT EVALUABLE.

## 5. Per-λ lines (frozen)

Let t* be the last sample time reached by all three N at that λ, and A_N = max_i |a_i| at t*.
- **ILL-POSED(λ)** if, with K-dt passed, either (i) all three N end in BLOW-UP with t_fail(256) > t_fail(512) >
  t_fail(1024), or (ii) t* ≥ 3.3 and A_512/A_256 ≥ 1.5 and A_1024/A_512 ≥ 1.5 (grid-scale acceleration growing with N).
- **SETTLES(λ)** if N 512 and 1024 both REACH t_end with energy error max|ΔE|/K_max ≤ 1e-3, R_v ∈ [0.9, 1.1] at every
  W5 sample on both, and W5 means of ρ_c, w_0.25, w_0.5, w_0.75, w_0.9, R_v agree 512 vs 1024 within 5 %.
- **OSCILLATES WITHOUT SETTLING(λ)** if as SETTLES but R_v leaves [0.9, 1.1] in W5.
- Otherwise **NOT EVALUABLE(λ)** (wall-limited or unconverged).

## 6. Label

Failed control → NOT EVALUABLE. ILL-POSED (the task's line) only if ILL-POSED(λ) at every λ. If all three per-λ labels
agree, that is the label. Otherwise the label is MIXED with the per-λ labels listed (e.g. "MIXED: ILL-POSED at 1e-8,
1e-7; SETTLES at 1e-6"). No amendment after numbers; post-result readings carry no label weight.

## 7. Caveats fixed in advance

One amplitude, planar 1D, static background, no expansion. λ is FITTED and tied to no galaxy. The regulator has no
covariant realization, so even SETTLES would not complete v3s's action. The wall cap makes "NOT EVALUABLE(λ)" likely
wherever the step collapses without a dt-floor blow-up.

κ = ½ FITTED; not theory closed.
