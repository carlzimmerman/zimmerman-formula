# AGB1R — blind re-grade of AGB1: how I read the frozen rules (committed before any real-data number)

2026-11-14. A blind, independent re-grade of `closure_2026_11_13/AGB1_progenitor_age_bias/FROZEN_CRITERIA.md`.
Read so far: that criteria file, the data constants in `closure_2026_11_13/NUF1_neutrino_floor_geometry/nuf1_run.py`
(DESI DR2 BAO vector, compressed CMB prior; I also saw NUF1's CAMB and BAO helper functions next to them), and the files
in `_external_data/cfg684_inputs/des5/` (HD table, STAT+SYS inverse covariance, the DES likelihood file, README).
Nothing else of AGB1 has been opened. All code here is written from scratch. Adopts nothing; edits no ledger.

## Data
- **Supernovae.** `DES-Dovekie_HD.csv` in file order (the order of the covariance). μ_th = 5 log10[(1 + zHEL) D_M(zHD) / Mpc] + 25
  (the DES likelihood file's `(1+zcmb)(1+zhel) D_A(zcmb)` with D_A = D_M/(1+zcmb)). Inverse covariance from
  `STAT+SYS.npz`: upper triangle in `np.triu_indices` order, reflected. `full` uses it as given. A sample that drops rows
  uses W = inv( inv(W_full)[keep, keep] ).
- **Offset ℳ.** "Marginalised analytically" is read as the DES formula without its constant: χ²_SN = rᵀWr − (1ᵀWr)²/(1ᵀW1),
  r = μ_obs − μ_th − A T. The DES file adds log(1ᵀW1 / 2π); that is one constant per sample, changes no Δχ², and must be
  left out for K3's χ²_min ≤ 10⁻³ to be meaningful. When A is free it is profiled with ℳ by linear least squares.
- **BAO.** The 13-number DESI DR2 vector of `nuf1_run.py` (BGS D_V/r_d; five galaxy bins and Lyα with D_M/r_d, D_H/r_d and
  their correlation r_MH), bins independent. D_V = (z D_M² D_H)^{1/3}.
- **CMB prior (Part C).** (θ* in radians, ω_b, ω_bc) mean and covariance as in `nuf1_run.py`; θ* = CAMB `thetastar`/100.
- **Counts check** before any fit: 1,820 rows; 1,623 with IDSURVEY 10 (z range and median printed); 197 others.

## Templates
- **T_S.** ψ(z) Behroozi et al. (2013) as written; Φ(τ) = (τ/t_p)^α / ((τ/t_p)^{α−s} + 1), t_p 0.3 Gyr, α 20, s −1.
  Weight per unit τ at redshift z: ψ(z_form(t(z) − τ)) Φ(τ), τ in (0, t(z)). Cosmic time t(z) = ∫_z^∞ dz'/[(1+z')H(z')]
  for flat w0–wa, H0 63.6, Ω_m 0.353, w0 −0.42, wa −1.75, no radiation (as the Part A model). z_form by inverting t(z) on a
  fine grid. Median of the weight on a log-τ grid. T_S(z) = 0.030 × [age(0) − age(z)] mag, tabulated on a z grid and
  interpolated to each zHD with a cubic spline.
- **T_W.** ψ(z) Madau & Dickinson (2014) = 0.015 (1+z)^2.7 / (1 + ((1+z)/2.9)^5.6); Φ(τ) ∝ τ^−1.13 for τ ≥ 0.04 Gyr, 0
  below; same background, median, slope.
- **Sign.** Model μ_th + ℳ + A T(zHD). A = 1 is the same as fitting the corrected moduli μ − T_S. A is unbounded.

## Part A model and minimiser
- E²(z) as written; distances by cumulative Simpson quadrature of 1/E on a uniform grid (step 2.5 × 10⁻⁴ to z 2.4),
  cubic interpolation to the data redshifts. BAO scale s = c/(H0 r_d) profiled linearly (h r_d = c / (100 s) Mpc, c in km/s).
- Box: 0.05 < Ω_m < 0.7, −3 ≤ w0 ≤ 1, −3 ≤ wa ≤ 2, w0 + wa < 0; outside the box the objective returns 10¹⁰.
- **Starts.** The four fixed (Ω_m, w0, wa) starts, plus the best fit at the neighbouring grid point. I read "neighbouring"
  as either neighbour: the grid is swept upward and then downward, each point taking the neighbour already done in that
  sweep as a fifth start, and the lower of the two sweeps is kept. For A free and the A = 0 / A = 1 forks the fifth start
  is the grid best fit at that A (nearest grid point for A free). Every Nelder–Mead run is restarted once from its own end
  point ("polished"). Lowest χ² kept.
- **q0 = 0 imposed** by substitution w0 = −1/(3(1 − Ω_m)); fitted (Ω_m, wa) (plus A profiled in the A-free fork). Starts:
  the four fixed starts' (Ω_m, wa) and the fork's unconstrained best fit.
- **q(z) ≥ 0 on [0, 2.33] imposed** by the penalty λ [max(0, −min_z q(z))]², min over a grid of step 0.005 including both
  ends, λ staged 10², 10⁴, 10⁶, 10⁸ (each stage starting from the last). The reported χ² is the unpenalised one; the point
  must have min q ≥ −10⁻³, else the fit is flagged CONSTRAINT NOT MET. Starts: the four fixed starts and the fork's
  unconstrained best fit.
- **q(z) = ½ + (3/2) w(z) Ω_DE(z)**, Ω_DE(z) = (1 − Ω_m) f_DE(z) / E²(z); q0 = ½ + (3/2) w0 (1 − Ω_m).
- **AT PRIOR EDGE** if a best fit lies within 0.003 of an Ω_m bound or within 0.01 of a w0, wa or w0 + wa = 0 bound.
- **A profile.** Grid −1.0 … 3.0 step 0.1 (41 points), plus A free (profiled exactly). Best A = A-free fit. Δχ²(A) =
  χ²_grid(A) − χ²_free. Intervals: crossings of Δχ² = 1 and 4 of a cubic spline through the grid profile (with the A-free
  point as reference); a crossing outside the grid is reported as open at that end.

## Words (judged on `full`)
- **W1** from Δχ²(A=0) and Δχ²(A=1), the six-way table as written (thresholds 4 and 9; "≥" at the upper edge as written).
  Second word: ROBUST if `des_only` and `bao_overlap` give the same first word as `full`, else FRAGILE naming which.
- **W2 per fork** (A = 0, A = 1, A free): Δχ²_today = χ²(q0 = 0 imposed) − χ²(fork best fit).
- **W3 per fork:** Δχ²_never = χ²(q ≥ 0 imposed) − χ²(fork best fit).
- W2 and W3 printed for `des_only` without a second word. `bao_overlap` gets the profile and the forks, numbers only.
- `rand197`: the A profile only. **Ambiguity:** the criteria name LGS1's draw (seed 20261113 over the DES rows in file
  order) but not the call, and LGS1's code is not on my reading list. I use
  `np.random.default_rng(20261113).choice(des_row_positions, 197, replace=False)`. If LGS1 drew differently my 197 differ
  from AGB1's; this control carries no word of its own.

## Checks (Part A words NOT EVALUABLE if any of KT, K1, K2, K3, K4, KA fails)
- **KT** Δage_S(1.0) ∈ [5.0, 5.6] Gyr, T_S(1.0) ∈ [0.15, 0.17] mag, Δage_W(1.2) ∈ [1.7, 2.1] Gyr.
- **K1** BAO only, flat ΛCDM (Part A model, no radiation): |Ω_m − 0.2975| ≤ 0.003, |h r_d − 101.54| ≤ 0.3 Mpc.
- **K2** `full` supernovae only, flat ΛCDM, A = 0: |Ω_m − 0.330| ≤ 0.0075.
- **K4** my D_M, D_H at z 0.5, 1.0, 2.33 for (0.32, −0.8, −0.7), h 0.68, against CAMB 1.6.6 PPF, massless neutrinos
  (N_eff 3.044, ω_b 0.0224, ω_c from Ω_m h²): every relative difference ≤ 10⁻³.
- **K3** two twins on `full` with all BAO bins: data replaced by the model at (0.31, −0.8, −0.6), h r_d 101.6 Mpc, μ shifted
  by A_true T_S, A_true = 1 and 0, covariances unchanged, no noise. A-free fit: |A − A_true| ≤ 0.01, |w0 + 0.8| ≤ 0.01,
  |wa + 0.6| ≤ 0.05, χ²_min ≤ 10⁻³; and χ²(wrong A, minimised) − χ²_min > 0. Script exits 3 if both pass, 4 otherwise.
- **KA** on `full`: |spline minimum of the grid profile − A_free| ≤ 0.03 and |spline minimum χ² − χ²_free| ≤ 0.05.

## Part C
- Fitted (h, ω_b, ω_bc, w0, wa); Σm_ν 0.06 eV in one massive state, N_eff 3.044, flat; CAMB 1.6.6 `get_background`, PPF,
  set by H0. D_M at the supernova redshifts and BAO redshifts, H(z), r_d = `rdrag`, θ* from CAMB. χ² = BAO + prior + SN,
  ℳ and A profiled. Box: w0, wa as Part A; h in (0.4, 1.0); Ω_m = (ω_bc + 0.06/93.14)/h² in (0.05, 0.7).
- Starts: each of the four fixed starts' (w0, wa) with ω_b, ω_bc at the prior mean and h set so θ* equals the prior mean
  (CAMB `thetastar` solve); plus the neighbouring grid point (both sweeps), restart polish as in Part A.
- A grid −1.0 … 3.0 step 0.25 (17 points) plus A free; forks, q0 = 0 by substitution with Ω_m from (h, ω_bc), never by the
  same staged penalty on the Part A flat formula for q(z) with that Ω_m.
- **K5** BAO + prior, no SN: χ²(w0–wa) − χ²(ΛCDM) within −8.0 ± 1.0. **K6** BAO + prior + `full`, A = 0: |w0 + 0.803| ≤ 0.040,
  |wa + 0.72| ≤ 0.16. Either failing makes W1c–W3c NOT EVALUABLE. W1c's second word from `des_only` alone.

## What I run
Parts A and C in full, plus the reported-only `tmpl_W`, `legacy_offset`, smallest-q and χ² splits if time allows.
**Part B is not run**: it executes CFG684 and CFG689 sources and reads LGS1's outputs, which are outside the files this
blind lane may open.

kappa = 1/2 FITTED; not theory closed.
