# CFG652 FROZEN CRITERIA: hot-gas groups, Theory v2 (condensed source) vs candidate B (all-baryon source), raw KiDS lensing

Committed ALONE, after the theory commit bc0dd7975 (model and derivation, no lensing data) and BEFORE any KiDS source is staged,
any condensed mass is computed, or any excess surface density is measured. Date 2026-10-12.
κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. "Cold energy"; its mass is required; no
particle species; not "theory closed". No ΛCDM halo, mass function, concentration or standard-MOND yardstick enters any verdict.

## What was seen before this freeze (disclosed)
- The theory derivation (`cfg652_derive.out`) and its forecast.
- The eFEDS catalogue's size and coverage only: 542 entries, 96 upper limits on M_gas500; 175 entries with 0.1 ≤ z ≤ 0.5, a
  measured M_gas500 and a position in the KiDS G9 strip (median M_gas500 6.3e12 Msun, median z 0.30). No lensing or stellar
  mass of any group has been looked at.
- Column lists of the KiDS bright sample and source catalogue (no values beyond the first rows' formats).

## Data (all on disk; nothing downloaded)
- Groups: `real_research/data/efeds_bahar2022_table2.tsv` (Bahar+22, VizieR J/A+A/661/A7): position, z, R500 (arcmin, used
  ONLY as the measured X-ray aperture R_X), M_gas500 (= M_hot inside R_X).
- Sources: `real_research/data/lensing_rar/KiDS_DR4.1_SOM_gold_WL_cat.fits`, staged to `_external_data/cfg652_work` by
  `cfg652_stage.py` (box RA 124–148, Dec −5 to +7).
- Condensed mass: `KiDS_DR4_brightsample.fits` + `_LePhare.fits` (row-aligned; MASS_MED, zphot_ANNz2, masked flag).

## Sample (frozen)
0.1 ≤ z ≤ 0.5; measured (not upper-limit) M_gas500 > 0; source coverage ≥ 0.6 of the mean source density in the 0.5–1.5 Mpc
annulus (positions only).

## Condensed mass M_cond (frozen recipe)
Bright-sample galaxies with masked = 0, MASS_MED > 5, |z_phot − z| ≤ 0.05(1+z). Net stellar mass inside projected R_X minus the
area-scaled stellar mass in the 3–6 R_X annulus (same z window); floor = the most massive such galaxy inside 0.2 R_X. Cold gas
taken as zero (bracket below). f_hot = M_gas500 / (M_gas500 + M_cond).

## Measurement (frozen)
Tangential and cross ESD in 12 log bins 30–3000 kpc (physical); sources z_B > z_l + 0.2; weight w Σ_crit⁻², Σ_crit⁻¹ from point
z_B with flat (0.3, 0.7, H0 70) distances (the June estimator's convention; background geometry only). Random points: 20 per
group, uniform over occupied 0.1° source cells, z drawn from the group z's (seed 652). Corrected ESD = boost × ESD_groups −
ESD_randoms, boost = per-lens source weight sum relative to randoms. Jackknife: 30 equal-count RA patches of the groups; Hartlap
factor applied. Statistics use the 8 bins with centres 53–783 kpc; the outer band is the 4 bins 248–783 kpc.

## Models (frozen in `cfg652_model.py`, sha256 04352d4e…d60d1)
Per group, (a) Theory v2 and (b) candidate B from `cfg652_model.system` (CFG637 Method A, N = 600) with the group's M_cond,
M_hot, R_X, z; ΔΣ from core + settled + reservoir truncated at r_ta (no 2-halo term in either model). Stacked prediction =
lensing-weight (ΣWW per bin per group) average. Variants: M_cond × 10^±0.2 (stellar-mass / cold-gas / completeness bracket),
gas extent 1 R_X and 4 R_X (primary 2 R_X).

## Primary statistic and decision rule (per footing)
χ²_a, χ²_b of the measured stack vs each stacked prediction (8 bins, jackknife covariance); Δχ² = χ²_b − χ²_a.
- **(a) FAVOURED**: Δχ² ≥ +9 and χ²_a p ≥ 0.01.
- **(b) FAVOURED**: Δχ² ≤ −9 and χ²_b p ≥ 0.01.
- **BOTH EXCLUDED**: χ²_a and χ²_b both p < 0.01.
- **NOT DIAGNOSTIC**: otherwise.
- **FRAGILE**: the label changes under the M_cond ±0.2 dex variants or the gas-extent variants (the label is reported with the
  fragility named).
- Footings must agree for an unconditional label; else FOOTING-DEPENDENT.
- A (b) FAVOURED label is flagged conditional on the missing 2-halo term (its omission raises the outer data relative to both
  models and favours (b), whose outer ΔΣ is higher in the no-reservoir regime).
Reported alongside: A_out = log10(ΣΔΣ_obs/ΣΔΣ_pred) over the outer band for each model, with jackknife σ.

## Secondary (reported, no verdict weight)
Split at the median f_hot: D_obs = log10[ΔΣ_band(high f_hot) / ΔΣ_band(low f_hot)] with jackknife σ, vs the stacked
predictions D_a, D_b.

## Controls and MUTATE
- K1: cross-shear χ² over the 8 bins, p > 0.01 (PASS) — if it fails, the lane is SYSTEMATICS-LIMITED and no verdict is drawn.
- Random-point ESD reported (it is subtracted).
- **MUTATE M1** (model): (a) re-derived with the hot gas relabelled condensed must reproduce (b)'s χ² to < 0.01 (data-level run
  `MUTATE=1`); the model-level check (max |Δlog ΔΣ| < 0.01) is already in `cfg652_derive.out` (PASS, exact).
- **MUTATE M2** (data): shuffle M_hot among groups (200 permutations, seed 6520), re-split by the shuffled f_hot: the split trend
  must die (|median D_shuffle| < σ_D).

## Forecast (from `cfg652_derive.out`, declared shape-noise model n_eff 4/arcmin², σ_e 0.27)
Groups with M_b ≈ 10^13.5 Msun need ~3–6 (×4 allowance: 11–25) for 3σ between (a) and (b); M_b ≈ 10^13 with f_hot 0.6–0.8
need 340–1070 (×4: 1400–4300); f_hot 0.9 at 10^13 needs 13–16 (×4: 52–65). The eFEDS sample (median M_gas500 6e12) sits near
the hard regime, so NOT DIAGNOSTIC is a likely outcome and is stated in advance.

## Known inherited inputs (context)
Catchment rule (max of CFG543 P2 and CFG634/637 X-COP conventions), gas geometry (β = 2/3, r_c = 0.234 R_X, CFG543), Method A
infall brackets (CFG637), Σ_crit distance convention, LePhare stellar masses (Chabrier). The theory derivation shows the sign
of the (a)–(b) outer contrast depends on whether an unsettled reservoir survives, which these inputs decide.
