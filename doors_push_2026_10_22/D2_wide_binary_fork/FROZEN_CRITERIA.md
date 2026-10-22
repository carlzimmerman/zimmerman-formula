# D2_wide_binary_fork — FROZEN CRITERIA (written before any script or number of this lane)

Lane: `doors_push_2026_10_22/D2_wide_binary_fork/`. Door: law-first (canonical law at every scale,
read as QUMOND/AQUAL with the Galactic external field, EFE) vs medium-first (P-sector crossover
λ = 17 pc, M_crit = 3.87e5 M☉; Newtonian wide binaries and ultra-faints). κ = ½ is FITTED; both
footings (a₀ = 9.36e-11, 1.13e-10 m/s²) are reported and never pooled.

Record read before writing this (see README for the list): DSF-21 A24, A26, A71, FINAL_THEORY §5b/§6 P5,
CANDIDATE_LAWS_REGISTER "Law-first vs medium-first", PREREGISTRATION_DR4.md §1.1 (read only, FROZEN,
not edited), wide_binary_pipeline.py (read only), CFG800, CFG816/CFG825 R statistic, CFG478, CFG332,
CFG821/828, catalog_builder README and DRY_RUN notes, memory notes on the gate fork / DR4 prereg.

## Q1. Is γ_v = 1.18 at 20 kAU the canonical law's number with the Milky Way field?

Method (fixed now): an **independent** QUMOND solver (3-D FFT longitudinal projection of
S = (ν(|g_N|/a₀) − 1) g_N, g_N = binary Newtonian field + uniform Newtonian external field), not A24's
axisymmetric quadrature. Canonical kernel ν(y) = ½(1 + √(1 + 4/y)). Configuration as A24: 1 + 1 M☉,
circular, γ_v = √(a_rel/a_N), a_rel = radial (along-separation) relative acceleration. The observed
external field g_ext,obs is converted to the Newtonian external field by the law's own inversion.
External-field values (all from the record, none chosen here): 1.685e-10 m/s² (= A24's x_ext = 1.8 at
canonical a₀), 1.778e-10 (PREREG §1.1 primary), 2.078e-10 (PREREG §1.1 alt g_ext). Orientations:
θ = 0 (field along separation, A24's case), θ = 90°, and the orientation average ⟨a_rel⟩ over cos θ
(3-point Gauss–Legendre on [0, 1]). Separations 10, 20, 30 kAU.

Validity checks (script, PASS/FAIL, exit 0 iff all pass):
- **C1** FFT machinery vs analytic linear EFE: the FFT longitudinal projection of the sampled
  linear-order source reproduces the analytic linear QUMOND field at the partner star
  (B_par = ν_e, B_perp = ν_e(1 + K/2), K = d ln ν/d ln y at y_e) to ≤ 2 %.
- **C2** resolution convergence: γ_v(20 kAU, θ = 0) changes by ≤ 0.005 between the two grid
  resolutions used.
- **C3** box convergence: same, between the two box sizes used, ≤ 0.005.
- **C4** strong-field limit: a binary with y_int ≥ 300 (no external field needed) gives γ_v − 1 ≤ 0.005.
- **C5** A71 arithmetic reproduced from its own inputs: σ(κ) = 0.040 (±0.001) and joint 0.0605 (±0.001).
- **C6** A26 reproduced from `a26_rar.csv`: N = 92, 45 below M_crit, median Δ_below = +0.651 (±0.01).
- **C7** DR3 frozen-cut catalogue on disk has 6,210 pairs with 2 ≤ s < 30 kAU.
- **MUTATE** (`--mutate`): drop the longitudinal projection (use S itself as the phantom field);
  C1 must FAIL (B_perp → ν_e).

Result lines (reported, not pass/fail):
- **R1** γ_v at 20 kAU, θ = 0, g_ext = 1.685e-10, canonical: "A24 REPRODUCED" if within 0.015 of
  A24's 1.1933; otherwise "A24 DISAGREES" with the difference.
- **R1b** orientation-averaged γ_v at 20 kAU at the PREREG primary g_ext, both footings: "1.18 IS THE
  LAW'S NUMBER" if the canonical value is in [1.15, 1.21]; otherwise the corrected value is the result.
- **R2** dγ_v/d ln a₀ at fixed g_ext,obs (a₀ × (1 ± 0.05)); dγ_v/dκ in A71's convention
  (κ_canon = 0.413719) and in the κ = ½-at-canonical convention; ∂γ_v/∂ ln g_ext.
- **R3** σ(κ) from a 30,000-pair DR4 catalogue with the frozen σ_sys = 0.020 treated as **shared**
  (one systematic on the whole catalogue, not divided by √bins), plus the g_ext–a₀ degeneracy
  (σ_ln g_ext = half the ln-difference of the two frozen g_ext values). "A71's 0.040 STANDS" if the
  result is ≤ 0.050; "A71 OVERSTATED" if > 0.050. Joint error recomputed with A71's own combination rule.

## Q2. What do current data say at 20 kAU? Is the fork decided?

- **R4** fraction of pairs in 18–22 kAU in the on-disk frozen-cut DR3 catalogue
  (`real_research/data/widebinaries/dr3_extract/wide_binaries_dr3.csv`) vs log-uniform (A24's 7.41 %,
  2,223 of 30,000) and vs the registered pipeline's own a^−1.6 mock (re-implemented, not imported).
  "A24 BIN FORECAST STANDS" if the DR3 fraction ≥ 3.7 % (half of log-uniform); otherwise overstated by
  the ratio.
- **R5** separation of 1.18 vs 1.0 at N = 30,000: (i) the 18–22 kAU bin alone, (ii) the registered
  global estimator; per-pair σ from two record conventions (A24's σ_fit scaling; CFG825's DR3 R-statistic
  σ_R = 0.1775 at 175/173 pairs) and the DR3 dry-run calibration (γ̂ ± 0.055 at 6,210 pairs).
- **R6** current-data status. The fork counts as DECIDED on current wide-binary data only if a
  measurement on record that the record itself classes as scoring (not contamination-limited) excludes one
  reading at ≥ 3σ. Otherwise OPEN. The DR3 numbers are non-scoring by the frozen pre-registration and are
  quoted only as distances, never as a verdict.

## Q3. Do on-disk ultra-faints below M_crit discriminate now?

- **R7** A26's own 92 systems, with the external field of the host added to the law (QUMOND 1-D
  estimate ν(y_i + y_e)(1 + K w/3), w = y_e/(y_i + y_e); host baryonic masses MW 6.0e10 M☉ (record,
  CFG332) and M31 1.0e11 M☉ (labelled external input), distances = LVD `distance_host`; field systems
  isolated). Variants: host masses × ½ and × 2; upper bound ν(y_i + y_e) without the K term.
  Classification for the 45 sub-threshold systems:
  "DWARFS SUPPORT EFE-PRESENT LAW-FIRST" if |median Δ_EFE| ≤ 0.3 dex and ≥ 1/3 within 0.5 dex;
  "DWARFS EXCLUDE BOTH READINGS" if median Δ_EFE ≥ +0.5 dex (and medium-first is already ≥ 1.5 dex off);
  otherwise "INTERMEDIATE". Count isolated (field) systems with M* < M_crit and measured σ.

## Q4. What runs before DR4; what DR4 needs.

- **R8** N_total for a 3σ separation of the law-first global γ̂ (registered Arm A floor 1.1614 canonical
  / 1.1917 alt) from 1.000, as a curve in σ_sys ∈ {0.01, 0.02, 0.03, 0.04, 0.05}, and the σ_sys ceiling
  above which 3σ is unreachable at any N; same for the 18–22 kAU bin alone with the measured occupancy.
  Compared with the record's demonstrated inter-group γ_v disagreement 0.174.

## Verdict rule

CRISP FINDING if any of R1/R1b, R3, R4/R5 or R7 corrects a number or claim in the record by more than its
stated tolerance; RUNNABLE NOW if a decisive test can run on disk; DATA-GATED if the fork needs DR4 /
field UFDs; SCOPED NO-GO if no achievable data can separate the readings; NOTHING NEW otherwise. More than
one may apply; the README states the primary one first.

Compute: `OMP_NUM_THREADS=1 nice -n 10`, < 2 GB RSS, no network, no new data.
