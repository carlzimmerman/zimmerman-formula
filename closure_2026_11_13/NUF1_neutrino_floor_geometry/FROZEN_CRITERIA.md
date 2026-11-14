# NUF1 — the neutrino-mass floor against DESI DR2 BAO + the compressed CMB prior, geometry only (FROZEN, before any number)

2026-11-13. A test of flat ΛCDM on its own terms. It adopts nothing and edits no ledger.

## Why
A literature sweep found one place where the two recent survey drops put flat ΛCDM at about 3σ: DESI DR2 BAO + CMB
prefers a neutrino-mass sum below the laboratory oscillation floor. DESI quotes Σm_ν,eff = −0.101 +0.047/−0.056 eV (68 %)
and a 3.0σ tension with the normal-ordering floor (arXiv:2503.14744, Eq. baseline_negnu and Sec. on effective neutrinos;
read from the TeX source). The effective-mass method is arXiv:2407.10965. This lane reproduces the **geometry** part of
that tension ourselves, from the published BAO distances plus DESI's compressed CMB prior.

**What this lane is and is not.**
- It tests ΛCDM on its own terms. The inherited ingredients are the compressed CMB prior (standard early-universe
  physics, marginalised over late-time effects by DESI) and the laboratory floor.
- It leaves out the CMB-lensing channel and every other late-time CMB effect (ISW, lensing smoothing of the peaks,
  damping tail), so it can come out weaker than DESI's 3.0σ. DESI itself says lensing carries much of the neutrino
  information (arXiv:2503.14744, Sec. on sources of information).
- It is the same BAO-against-CMB mismatch that drives the evolving-dark-energy hint, not an independent anomaly.
- It says nothing about whether the repository's own framework is favoured. Framework footings (canonical / alt a0) do
  not enter; no a0 and no framework quantity is used anywhere.
- It adopts nothing and edits no ledger.

## Data (every value copied from the papers' TeX sources, downloaded 2026-11-13 from arxiv.org/e-print/<id>)
1. **DESI DR2 BAO**, arXiv:2503.14738, Table `tab:alphas`: BGS D_V/r_d at z 0.295 (7.942 ± 0.075); D_M/r_d, D_H/r_d and
   their correlation r_MH for LRG1 (0.510), LRG2 (0.706), LRG3+ELG1 (0.934), ELG2 (1.321), QSO (1.484) and Lyα (2.330:
   38.988 ± 0.531, 8.632 ± 0.101, −0.431). The vector is the one hard-coded in
   `closure_2026_11_12/AZ2_flat_a0_lya_ap/az2_flat_a0.py`; every value was re-checked against the TeX table and matches.
   Bins are independent of each other (DESI's baseline; Appendix `sec:corr-sys` shows cross-bin systematics do not matter).
2. **Compressed CMB prior**, arXiv:2503.14738, Appendix A, Eqs. `CMB_compression_mean` and `CMB_compression_cov`,
   verbatim: mean (θ*, ω_b, ω_bc) = (0.01041, 0.02223, 0.14208); covariance 10⁻⁹ × [[0.006621, 0.12444, −1.1929],
   [0.12444, 21.344, −94.001], [−1.1929, −94.001, 1488.4]]. θ* in radians; ω_bc = ω_b + ω_c (no neutrinos).
   **Noted before any number:** the printed θ* mean has four significant figures. The same paper's θ*-only prior
   (Eq. `thetastar_prior`) is 100θ* = 1.04110, i.e. θ* = 0.0104110, which differs from 0.01041 by 0.39 of the
   compressed prior's own θ* sd (2.57 × 10⁻⁶). The verbatim value is primary; the 1.04110 mean is a reported-only row.
3. **Laboratory floor**: Σm_ν ≥ 0.059 eV (normal ordering), ≥ 0.10 eV (inverted), as quoted by arXiv:2503.14744
   (citing NuFIT 6.0, Esteban et al., JHEP 12 (2024) 216, and Capozzi et al. 2021, de Salas et al. 2021); the two inequalities
   that give these numbers from the mass splittings are displayed in the introduction of arXiv:2407.10965.
4. **Lyα AP pair** (control only), arXiv:2607.27410, Eq. `dmdh_dr2` (sections/results.tex): D_M/r_d 39.32 ± 0.33,
   D_H/r_d 8.600 ± 0.066, correlation 0.225, z_eff 2.33; it combines the full-shape AP and isotropic BAO information from
   the same Lyα data, so it **replaces** the DR2 Lyα BAO pair, never adds to it.

## Model
Flat ΛCDM. Free: θ*, ω_b, ω_bc (equivalently h, ω_b, ω_bc: θ* ↔ h is a one-to-one map at fixed densities and m) and the
effective neutrino-mass sum m (eV), which may be negative. N_eff = 3.044. **Three degenerate massive states** (the
choice of arXiv:2407.10965 and of DESI's baseline Σm_ν runs in arXiv:2503.14744). CAMB 1.6.6 (default accuracy and
recombination), background only: D_M(z), H(z), r_d (CAMB's `rdrag`) and θ* (CAMB's `thetastar`).
Observables: D_M/r_d, D_H/r_d = c/(H r_d), D_V/r_d = (z D_M² D_H)^{1/3}/r_d, θ*.

**Effective mass definition (arXiv:2407.10965, Eq. `nu_eff_def`, the extrapolation, not the exact negative-energy
code):** for every observable X, X(m) = X(0) + sgn(m)[X(|m|) − X(0)], evaluated **at fixed sampled parameters
(θ*, ω_b, ω_bc)**. Fixed θ* is the convention of the CLASS implementation (arXiv:2503.14744 footnote to its prior table:
100θ* is sampled where CLASS is used; the CAMB/Cobaya chains sample θ_MC, an approximation to θ*). For m ≥ 0 this is
the physical model exactly and the convention does not matter; for m < 0 it does, so the same fit **at fixed
(h, ω_b, ω_bc)** (θ* then also extrapolated) is a reported-only row.

## Statistic
χ²(m) = χ²_BAO + χ²_CMB-prior, **profiled** (minimised, Nelder–Mead, warm-started from the neighbouring grid point) over
(θ*, ω_b, ω_bc) at each m on the grid −0.50 … +0.50 eV in steps of 0.01, plus the two floors 0.059 and 0.10.
A cubic spline through the profile gives the best-fit m, χ²_min, and the Δχ² = 1 (68 %) and Δχ² = 4 (95 %) intervals.
Δχ²_floor = χ²(floor) − χ²_min, with χ²(floor) the profiled value at the floor itself.

## Frozen words (primary data set: all DR2 BAO bins + the compressed CMB prior; judged on the normal-ordering floor)
- **FLOOR EXCLUDED AT 3 SIGMA** if Δχ²(0.059) ≥ 9;
- **FLOOR DISFAVOURED** if 4 ≤ Δχ²(0.059) < 9;
- **FLOOR ALLOWED** if Δχ²(0.059) < 4.
- Second word: **ROBUST** if the first word is the same in every control below, else **FRAGILE**, naming the control(s)
  that change it.
The inverted floor's Δχ² is reported for every row and carries no word.

## Controls (each a full re-fit, its own output files)
- `ctl_noLRG1`: drop LRG1.
- `ctl_noLRG2`: drop LRG2.
- `ctl_lyaAP`: replace the DR2 Lyα BAO pair with the DR2 Lyα AP pair (data item 4).
- `ctl_zgt06`: BAO bins with z_eff > 0.6 only (LRG2, LRG3+ELG1, ELG2, QSO, Lyα; BGS and LRG1 dropped).

## Known-answer checks (frozen with tolerances, judged before the words are read)
- **K1 — BAO-only ΛCDM.** Fit (Ω_m, h r_d) to the primary BAO vector, Σm_ν = 0.06 eV in one massive state (DESI's
  convention when m is fixed), h fixed at 0.68 and ω_b at 0.02218 inside CAMB (BAO-only distances depend on h only through
  the radiation and neutrino fractions, a < 0.1 % effect). Target arXiv:2503.14738 Eq. `constraints_lcdm_desi`:
  Ω_m = 0.2975 ± 0.0086, h r_d = 101.54 ± 0.73 Mpc. **Pass:** |ΔΩ_m| ≤ 0.003 and |Δ(h r_d)| ≤ 0.3 Mpc (0.35σ and 0.41σ).
  Tolerance: a best fit of a near-Gaussian 2-parameter likelihood sits within ≪ 0.1σ of the posterior mean; the h choice
  and DESI's chain noise add a few hundredths of σ; 0.35–0.4σ leaves room for both without hiding a units or r_d error
  (a wrong r_d convention moves h r_d by ≥ 1 Mpc, a wrong D_H or D_V definition moves Ω_m by ≥ 0.01).
- **K2 — as written in the brief (DESI + CMB-prior ΛCDM values at 0.06 eV): DROPPED.** arXiv:2503.14738 does not quote
  ΛCDM parameters for DESI + (θ*, ω_b, ω_bc)_CMB (its Table `tab:cosmo_constraints` lists that combination for w0waCDM
  only). Replaced by two checks the paper does quote:
  - **K2A — the compressed prior itself.** DESI + (θ*, ω_b, ω_bc)_CMB, Σm_ν = 0.06 eV one massive state: best-fit
    χ²(w0waCDM, PPF, priors w0 ∈ [−3, 1], wa ∈ [−3, 2], w0 + wa < 0) − χ²(ΛCDM). Target arXiv:2503.14738 Table
    `tab:dchisq`: Δχ²_MAP = −8.0 (uniform priors, so MAP = best fit). **Pass:** within ±1.0. Tolerance: DESI's minimiser
    and ours differ in start points and the w0wa minimum is shallow along the BAO degeneracy; a wrong θ* unit, a wrong
    sign in the covariance or ω_bc read as ω_c moves this by several units.
  - **K2B — the θ* and r_d machinery.** DESI + BBN (ω_b = 0.02218 ± 0.00055, Eq. `BBN_LCDM`) + θ* (100θ* = 1.04110 ±
    0.00053, Eq. `thetastar_prior`), ΛCDM, Σm_ν = 0.06 eV one massive state. Target Table `tab:cosmo_constraints`
    (DESI+BBN+θ*): Ω_m = 0.2967 ± 0.0045, H0 = 68.45 ± 0.47. **Pass:** within 0.5σ of each (0.00225, 0.235).
    Tolerance as K1, a little wider because three parameters are fitted and the posterior is mildly non-Gaussian in H0.
- **K3 — mutation twin.** Replace the BAO vector by the model's own prediction at m = 0.06 eV (three degenerate states)
  with (θ*, ω_b, ω_bc) at the CMB-prior mean; same covariance and prior. **Pass:** best-fit m within 0.005 eV of 0.06 and
  0.06 inside the Δχ² = 1 interval. The twin exits with code 3 on pass and 4 on fail; real modes exit 0.
If any of K1, K2A, K2B, K3 fails, the frozen words are **NOT EVALUABLE**; the numbers are still reported as a reading.

## Reported only (no frozen word)
- `ro_w0wa`: the same profile with w0 and wa also free (PPF; priors as K2A; grid step 0.02 eV plus the floors):
  does the floor become allowed (Δχ² < 4)?
- `ro_widen`: the prior's ω_bc standard deviation doubled (ω_bc row and column of the covariance scaled by 2, correlations
  kept): Δχ² at the floors.
- `ro_hfixed`: the effective-mass extrapolation at fixed (h, ω_b, ω_bc) instead of fixed (θ*, ω_b, ω_bc).
- `ro_thetamean`: the prior's θ* mean set to 0.0104110 (Eq. `thetastar_prior`) instead of the printed 0.01041.
- DESI's own numbers beside ours for comparison (arXiv:2503.14744: −0.101 +0.047/−0.056 eV, 3.0σ, which includes CMB
  lensing and the full CMB likelihood).

## Files and order
`nuf1_run.py MODE` (one mode per process; writes `nuf1_<MODE>.json`, log to `nuf1_<MODE>.out`) and `nuf1_collect.py`
(reads the JSON files, applies the checks and the words, writes `nuf1_results.json` and `nuf1_collect.out`).
This file and the scripts are committed alone before any real-data number. Before that commit only the synthetic twin
(K3) was run, in a scratch copy, to debug plumbing. Any change after this commit is a dated amendment committed alone
before the re-run, and both readings are reported.
