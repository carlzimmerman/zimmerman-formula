# CFG224 — how well is the gas-mass calibration known? Tracer offsets and scatter against redshift

> Every a₀(z) lane ends on the gas-calibration wall (CFG219–CFG223). This lane measures the calibration from galaxies with gas masses from two or more tracers, **at the conversions each source states**. A tracer agreement does not prove an absolute mass scale; the data chat's NOEMA3D reconstructions are unverified against the paper. **κ = ½ is FITTED; no law verdict.** Criteria `FROZEN_CRITERIA.md` (99f62160b), committed before any offset was computed. Figure: `cfg224_tracer_offsets_vs_z.png`.

## Bottom line: closer to ±0.15 dex than to ±0.05–0.10 at z ≈ 1.2, better than ±0.05 only at z < 0.6, unmeasured above z ≈ 1.6
Offsets d = log₁₀(M_A/M_B) with A before B in the order CO, [CI], [CII], dust; K = √(SE² + (|μ|/2)²) is the error of a two-tracer pooled scale if either tracer is equally likely to be right.
- **z < 0.6 (Stripe82, 78 galaxies, CO–dust):** mean −0.068, SD 0.155 (0.134 after the stated measurement errors), SE 0.018, **K = 0.038: below the CFG223 range.**
- **z ≈ 1.2 (Bourne+19 nine + the five validated NOEMA3D, [CI]–dust pooled, N = 14):** mean −0.240, SD 0.166, SE 0.044, **K = 0.128: between the CFG223 and CFG221 requirements.** By source the two [CI]–dust samples disagree by 0.15 dex: Bourne+19 alone −0.294 ± 0.059 (K = 0.158, at the CFG221 level), NOEMA3D −0.142 ± 0.041 (K = 0.082). NOEMA3D (reconstructed, N = 5): **CO and dust agree** (−0.017 ± 0.060, K = 0.061) and [CI] sits 0.13 dex below CO (+0.126 ± 0.030, K = 0.070). Three-cornered hat on those five: σ_CO = 0.084 dex, σ_dust = 0.105 dex, **σ_CI not constrained** (negative variance; with N = 5, 54% of synthetic draws give one).
- **The CO convention alone moves the NOEMA3D offset by 0.23 dex:** the five galaxies whose CO control fails give CO–dust −0.235 (Table 1 CO, K = 0.167) or −0.008 (recipe CO, K = 0.116), SD 0.26.
- **z > 1.6: K is not estimated.** Only three galaxies carry stated multi-tracer masses, each at its own conversions (α_CO = 0.8, 4.5, 3.0): PKS 0529-549 (z 2.57) CO–[CI] −0.63, CO–dust −0.48, [CI]–dust +0.15; Q1700-MD94 (z 2.33) CO–dust +0.39; J081740 (z 4.26) CO–[CII] −0.05, CO–dust +0.19, [CII]–dust +0.24 (D49: [CI]–dust < +0.03, an upper limit). The per-galaxy disagreements reach 0.6 dex.
- **Secondary, conversion-free luminosity ratios at z > 2:** SMGs (20) log L′_CI/L′_CO(1-0) = −0.70, SD 0.29 (SE 0.064), and it depends on the observed CO line used to estimate L′_CO(1-0): CO(3-2) −0.89 (N = 6), CO(4-3) −0.52 (N = 11), CO(5-4) −0.94 (N = 3). The implied α_CO that reconciles the [CI] mass (X = 5.1e-5) with the CO luminosity has median 0.91 (SD 0.29 dex), so the offset is −0.008 dex for α_CO = 0.8 but **+0.645 for 3.6 and +0.729 for 4.36: the conversion choice moves the z > 2 offset by 0.7 dex.** SPT DSFGs (fluxes only): L′_[CI]2-1/L′_[CI]1-0 −0.21 ± 0.21 (N = 20), L′_[CII]/L′_[CI]1-0 +0.27 ± 0.42 (N = 10); luminosity-level, not a mass test.
- **Literature (Dunne+22, parsed from the TeX, no download):** per-galaxy scatter of the conversion factors 0.07 to 0.17 dex (α_CO 0.09 to 0.14, X_CI 0.07 to 0.15, κ_H 0.10 to 0.17), error on each sample mean 0.01 to 0.05 dex, but **the mean α_CO differs between calibration samples by 0.08 dex (high-luminosity class, N = 90, 240, 97) and 0.22 dex (low-luminosity class, N = 12, 88, 12)**; the empirical calibration table differs by 0.107 dex (α_CO), 0.051 (α_850), 0.007 (α_CI). These calibrate tracers against each other in mostly local and luminous samples; they do not measure a redshift evolution.

## What it implies for the flat-versus-H(z) test (arithmetic with declared inputs, not a forecast)
K_needed = (half the H(z)-against-flat separation) / (|lever| f_gas) from CFG223's lever table; f_gas = 0.5 (0.3 to 0.7 in brackets). Compared with the measured K of the bin containing each point's z (the frozen parenthetical assumed B2 for all four RC100 quartiles; by the rule quartiles 3 and 4, z = 2.01 and 2.26, fall in B3, where K is not estimated).

| point | z | K needed (f_gas 0.7 / 0.5 / 0.3) | measured K in its bin |
|---|---|---|---|
| RC100 quartile 1 | 0.81 | 0.033 / **0.047** / 0.078 | B2: 0.128 |
| RC100 quartile 2 | 1.36 | 0.092 / **0.129** / 0.215 | B2: 0.128 |
| RC100 quartile 3 | 2.01 | 0.107 / **0.149** / 0.249 | B3: not estimated |
| RC100 quartile 4 | 2.26 | 0.079 / **0.110** / 0.184 | B3: not estimated |
| CRISTAL R_e fit route | 5.19 | 0.143 / **0.200** / 0.333 | B4: not estimated |
| CRISTAL R_out fit route | 5.26 | 0.213 / **0.299** / 0.498 | B4: not estimated |

In words: at z ≈ 0.8 the needed 0.05 is better than anything measured above z = 0.6 (0.13); at z ≈ 1.4 the measured 0.13 meets the needed 0.13 at f_gas = 0.5 and misses it at f_gas = 0.7; from z ≈ 2 up there is no ensemble to test it against. At z ≈ 5 the needed K is 0.2 to 0.3 (the law separation is 0.94 dex), which one galaxy cannot test. **The multi-tracer data cannot yet certify the ±0.05–0.10 dex that the RC100 range needs, and they put the z ≈ 1.2 knowledge near ±0.13 dex (0.08 to 0.16 by source).** CFG221's operating characteristics (±0.15 dex on the gas with about 50 outer-radius class-A discs at z > 3.5) are not re-run.

## Controls (`cfg224_gas_calibration.out`: 6/6 pass; `_MUTATE.out` pass)
C1 counts equal the data chat's checks file (Stripe82 78, Bourne 9, Kirkpatrick 12, SMG 20, SPT 29, NOEMA3D validated = the five with CO control pass); C2 estimator identity; C3 bootstrap coverage 0.63 (N = 9) and 0.67 (N = 78) for the 68% interval; C4 three-cornered hat recovers (0.10, 0.15, 0.20) at N = 300; C5 no Kirkpatrick or H-ATLAS row in any primary statistic (Kirkpatrick+19 is shown beside: log M_CO/M_RJ = −0.069 ± 0.152, N = 10, with RJ calibrated to CO); C6 the TeX parse reproduces α_CO 2.66, 3.08, 3.52 with N = 90, 240, 88 and the transcribed singles match the data chat's text. MUTATE (+0.30 dex on every CO mass): every CO pair shifts by +0.300 to 1e-9, others by 0, the Stripe82 K rises 0.038 to 0.117. **The first run is kept as `*_firstrun.*`:** its C6 failed because the TeX parse dropped the two rows that follow a `\midrule` (the Dunne+22 high-luminosity α_CO rows), fixed in the parse only.

## Limits
N at z ≥ 1.6 is three galaxies, so those bins are single-galaxy lines. Conversion choices differ between sources (α_CO from 0.8 to 4.5), so a CO–dust offset mixes conversion choice and astrophysics; the NOEMA3D CO, [CI] and dust masses are the data chat's reconstruction from tabulated fluxes at the paper's stated recipes (its CO control fails for five of ten); Stripe82's two masses share a metallicity dependence; Bourne+19 and NOEMA3D are pooled for the frozen [CI]–dust headline although their conversions differ (the per-source rows are beside it); K assumes two equally likely tracers and is a yardstick against the quoted requirements, not an error budget; Dunne+22's calibrations are not redshift-resolved.

## What would change the answer
Per-galaxy tables for Dunne+22 (407 galaxies, z 0 to 6, CO + [CI] + dust; CDS), the ACE survey (CO + Band 7 continuum, up to 17 at z 2 to 2.5) and the SMGs' 3 mm fluxes already on disk (20 at z 2.3 to 4.8: a [CI]–dust pair needs a stated RJ conversion, not run here) would populate the z > 1.6 bins with N ≥ 10. The CDS and survey tables are downloads that need the owner's go.

## Files
`FROZEN_CRITERIA.md`, `cfg224_gas_calibration.py` (+ `.out`, `_MUTATE.out`, `_firstrun.out`, `_results.json`, `_firstrun_results.json`), `cfg224_plot.py`, `cfg224_tracer_offsets_vs_z.png`. Run: `python3 campaign_fresh_gravity/CFG224_gas_calibration/cfg224_gas_calibration.py` (about 5 s) then `cfg224_plot.py`.

## Addendum B (2026-09-30, later)
The per-galaxy Dunne+22 tables and ACE (data chat, 6c18c4204) put tens of galaxies in the z > 1.6 bins: see `README_B.md` (criteria `FROZEN_CRITERIA_B.md`, 3b1c554e0). Headline: the optimised conversions are stable in z at fixed luminosity to about +-0.05 dex, and ACE shows un-optimised local prescriptions disagree by 0.2 to 0.7 dex at z ~ 2.2.
