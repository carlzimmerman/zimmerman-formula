# D8b_sigma_universality: FROZEN CRITERIA (committed alone, before any script, copy or correlation)

## What is tested

D8 (`doors_push_2026_10_22/D8_Lstar_value/`, commit f1da138742) found that L* = σ_c²/a0 can only live in the
tethered state, and that applying one L* to gas-free globulars (CFG820) and gas-poor dSphs (CFG821) needs ONE
universal σ_c. On Stilp+2013's 23 dwarfs (200 pc beam) the second-moment median 9.30 km/s gives L* = 29.95 pc
(canonical) / 24.80 pc (alt), with 84/16 = 1.995.

The tethered reading predicts: **per-galaxy σ does not track the galaxy's own energy injection or mass.** Two tests:

- **T1 (tracking):** does σ correlate with star formation or mass across the 23 dwarfs?
- **T2 (noise-only):** is the per-galaxy spread consistent with measurement error around one σ?

σ is footing-free. Any L* number is reported on both footings (canonical a0 = 9.36e-11, alt 1.13e-10 m/s²),
never pooled. κ = ½ is FITTED. No particle. Not "theory closed".

## Data (no downloads)

Only the Stilp+2013 (arXiv:1301.1989v2) LaTeX source already on disk under
`_external_data/d8_stilp2013_2026_10_22/src/` (owner-OK'd fetch, provenance in D8's PROVENANCE.md). Copies of
`table-derived-properties.tex`, `table-sample.tex` and (for K4 only) `table-correlations.tex` will be committed in
this lane with sha256. The σ table is D8's committed copy (`D8_Lstar_value/stilp2013_table-measurements.tex`,
sha 155d780c...).

**Matching rule (frozen):** join by the galaxy name string exactly as printed in column 1 of each Stilp table,
after stripping whitespace and LaTeX markup (`~`, `$...$`, `\,`) and lower-casing. Same paper, same names, same
aperture. No external catalogue (SPARC, LITTLE THINGS) is joined: Stilp's aperture-matched quantities are the
cleanest; an external join would add aperture mismatch. A galaxy with a missing value (`\nodata`, `...`, `--`) or
an upper limit (`<`) in a variable is dropped from that variable's test only; n is reported per test.

## Variables (frozen before looking at any value)

σ columns: **σ_m2** = ⟨σ_m2⟩ (D8's frozen primary, the one behind L* ≈ 25–30 pc) and **σ_cen** = σ_central
(secondary; it carries the table's only uncertainties).

Driver variables (all from Stilp's tables, log10 where positive):
- **Primary energy injection:** ⟨Σ_SFR⟩ (derived-properties col 7).
- **Primary mass:** M_baryon,tot (derived-properties col 2).
- Secondary: SFR (col 5), SFR/M_HI (col 6), M_HI (col 3), M_* (col 4), ⟨Σ_HI⟩ (col 8), w20 (sample col 10,
  rotation proxy).

## T1 statistic and lines

- Spearman ρ; two-sided p from 100 000 exact permutations (seed 20261022); 68 % and 95 % CI from 10 000
  bootstrap resamples (same seed).
- Slope b of log10 σ vs log10 X: OLS, with 95 % bootstrap CI; Theil–Sen reported alongside.
- **Primary tests:** 2 columns × 2 primary drivers = 4 tests. Family-wise α = 0.05 → per-test α = 0.0125
  (Bonferroni over 4). Secondary tests: Bonferroni over all 2 × 8 = 16 (α = 0.003125), reported, no verdict
  weight unless primary agrees.
- **Minimum detectable correlation:** computed in the script for each n: |ρ|_crit (permutation null quantile at
  α = 0.0125) and |ρ|_80 = the true ρ detectable with 80 % power (Fisher-z with Spearman variance 1.06/(n−3)).
  These are reported as the resolution of the test.
- **Driven benchmark slope:** b_drv = 1/3 (feedback energy balance σ³ ∝ Σ_SFR at fixed gas column). Stated, not
  fitted.

**T1 outcome lines (σ_m2 vs Σ_SFR and σ_m2 vs M_baryon decide; σ_cen must agree in sign for "crisp"):**
- **DRIVEN (against the universal floor):** any primary test with p < 0.0125. If both σ columns give it for the
  same driver: CRISP FINDING against the floor.
- **FLOOR FAVOURED:** no primary test significant AND the 95 % CI on b(σ_m2 vs Σ_SFR) excludes 1/3 (upper bound
  < 1/3).
- **UNDECIDED (low power):** no primary test significant but the 95 % CI on b includes 1/3. Then the 23-galaxy
  sample cannot tell a floor from the simple driven law; the minimum detectable ρ is quoted.

## T2: noise-only expectation for the spread

- H0: every galaxy has the same true σ (the inverse-variance weighted mean); observed σ_i = σ0 + N(0, Δ_i).
- **σ_cen:** Δ_i = the table's quoted uncertainties. Statistic χ² = Σ (σ_i − σ̄_w)²/Δ_i², dof = n − 1; and the
  84/16 ratio of L = σ²/a0 (footing-free as a ratio) compared with 100 000 Monte-Carlo draws under H0.
- **σ_m2:** the table gives no measurement error (the paper's y-bars are the pixel spread, not an error). Frozen
  assumption: Δ_m2,i = σ_m2,i × Δ_cen,i/σ_cen,i (same fractional error). Labelled CONDITIONAL on that assumption.
- **Line:** NOISE-CONSISTENT if MC p(ratio ≥ observed) ≥ 0.05 AND χ² p ≥ 0.05; otherwise INTRINSIC SCATTER
  present, with the ML intrinsic scatter σ_int (km/s and fractional) reported.
- If intrinsic scatter is present, the "floor" reading means σ_c ≤ every σ_i, not σ_c = typical σ_i. Then the
  lower envelope (minimum and the 5th percentile, plus the minimum minus 2Δ) is converted to L* on both footings
  and compared with the CFG820 floor (23.641 canonical / 24.476 alt, from D8's results json). This is reported,
  not a pass/fail.

## Checks (`d8b_sigma_universality.py`)

- K1: sha256 of all copied tables match PROVENANCE; σ table sha = D8's.
- K2: all 23 names match across the σ, derived-properties and sample tables under the frozen rule; σ values equal
  D8's committed `d8_stilp2013_results.json` rows.
- K3: planted controls: a synthetic σ = 9.3 (X/median X)^(1/3) with the frozen noise on the real X is detected
  (p < 0.0125) in ≥ 80 % of 200 noise draws, OR, if not, the script records that the driven benchmark is below
  the sample's power (the check then tests the null side only); a planted constant σ + noise gives false-positive
  rate within 0.0125 ± 0.01 over 2 000 draws.
- K4: for every pair that also appears in Stilp's own Spearman table (`table-correlations.tex`), |Δρ| ≤ 0.05
  (reproduction of the published coefficients). That table is not read until after this file is committed.
- K5: the noise MC reproduces the analytic χ² mean (n − 1) within 2 %.
- Mutate (`D8B_MUTATE=1`): σ_m2 is replaced by the planted driven σ; K2 then fails; outputs `*_MUTATE.*`.

## What each outcome means

- DRIVEN: the tethered reading's universal-σ_c premise fails on dwarfs; L* ≈ 25–30 pc loses its only on-disk
  support (crisp finding against).
- FLOOR FAVOURED and NOISE-CONSISTENT: strengthens the conditional L* ≈ 25–30 pc prediction.
- FLOOR FAVOURED with intrinsic scatter: σ is not driven but varies; the "floor" is the envelope, and its L* is
  quoted against the CFG820 floor.
- UNDECIDED: the sample cannot separate the readings; say what n is needed.
