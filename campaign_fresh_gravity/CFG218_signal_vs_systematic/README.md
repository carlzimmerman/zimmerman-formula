# CFG218 — the signal-to-systematic ladder

- **Criteria:** `FROZEN_CRITERIA.md` (1a7550513), committed before any number. **κ = ½ FITTED, NOT DERIVED.** A forecast from quantities the record already holds; no data are scored against a law.
- **Run:** `python3 campaign_fresh_gravity/CFG218_signal_vs_systematic/cfg218_ladder.py`, under 1 s. It passes 3/3 controls. `MUTATE=1` (E ≡ 1) passes: every signal is 0 and no sample is "discriminating". The chart is `cfg218_ladder.png`.

## Bottom line

**No sample is "discriminating". The calibration of the baryon-mass scale needed for a 3σ-equivalent flat-vs-rival separation is 0.02 to 0.11 dex.**

| sample | n | z | signal S | statistical band | route bias b_s | systematic S_sys | calibration for S/3 | classification |
|---|---|---|---|---|---|---|---|---|
| MUSE-DARK (SED + H₂) | 109 | 0.86 | 0.092 | 0.111 | +0.512 | 0.300 | ±0.054 | **systematic-limited** |
| RC41 (prior-anchored) | 41 | 1.50 | 0.083 | 0.044 | +0.051 | 0.043 | ±0.032 | marginal |
| NOEMA3D (SED + CO) | 10 | 1.24 | 0.048 | 0.143 | +0.048 | 0.043 | ±0.018 | **statistics-limited** |
| ALMA-CRISTAL (SED + dust gas) | 9 | 5.23 | **0.288** | 0.226 | +0.044 | 0.038 | ±0.109 | marginal |
| RC100 (prior-anchored) | 100 | 1.53 | 0.094 | 0.028 | +0.100 | 0.080 | ±0.040 | marginal |

All values are in dex of log D or δ (ν_mono, canonical). The signal is the median rival-vs-flat separation at each galaxy's own g_bar and z. The systematic is the |median δ_flat| shift that the sample's committed baryon-mass route bias would produce. RC100's b_s = +0.100 is taken from CFG217's RC41-overlap median Δ_prior.

- **CRISTAL has the strongest signal** (0.29 dex, from z ≈ 5 and a ≈ 8× rival a₀) and a small systematic (0.04 dex). It is limited by statistics: its band is 0.23 dex on 9 galaxies. **About 13 discs** would bring the band to a 3σ-equivalent level, if the route bias stayed at 0.04 dex.
- **RC100 has the tightest statistics** (0.028) but the smallest signal-to-systematic margin: its mass calibration is only known to about 0.1 dex, against the 0.04 dex it would need.
- **MUSE-DARK is hopeless as a discriminator:** its route bias (0.51 dex) exceeds its own signal several times over, and it would need about 370 galaxies for the statistics alone.
- **NOEMA3D's signal is small** (0.048 dex; it sits at g_bar of 3–13 a₀). It would need about 210 galaxies.
- **In the lowest-g_bar quartile of each sample** the signal is 0.08 to 0.09 dex, except CRISTAL's 0.32 dex, and the calibration needed is 0.035 to 0.125 dex.
- **RC100's differential version** (from CFG217, not recomputed): the flat slope is exactly zero at −0.075 dex and the rival slope exactly zero at −0.25 dex of differential baryon-mass change between z = 0.6 and 2.5. A 3σ-equivalent separation needs the differential calibration known to about ±0.06 dex.

## What this says about the route to a decisive a₀(z) test

- **The lever is CRISTAL-like z ≳ 4 discs with more members,** because the rival's a₀ is ×8 there. The requirement is a gas and stellar mass scale good to about 0.1 dex, and more than 13 discs with both.
- **At z ≲ 2 the baryon-mass calibration must reach about 0.03 to 0.05 dex,** which no current route delivers. The best one, measured CO gas (NOEMA3D), has 0.05 dex between its fit and independent masses.

## Controls and post hoc

- **C1:** the signal is 0 at z = 0. **C2:** Y(0) = 0 and Y is monotone in |e|. **C3:** CRISTAL's signal median (12 fit-route rows) reproduces the separation implied by CFG213's printed D_flat and D_rival to their rounding (0.2355 vs 0.2355).
- **Post hoc, reported only:** the sample sizes needed for the statistical band alone (CRISTAL 13, NOEMA3D 210, MUSE-DARK 371; RC41 and RC100 already suffice), and the figure.
- **Fixes, kept:** the first MUTATE run crashed on a solver bracket when the signal is 0, and then on a division by zero in the post hoc block. Both cases are now handled (`None`). No output was written by the crashed runs.

## Input correction (appended 2026-09-29; the text above is unchanged)

- Only the RC100 row uses the corrected table. `RC100_INPUT=corrected python3 cfg218_ladder.py` writes `cfg218_ladder_corrected*`.
- **RC100:** the statistical band goes from 0.028 to 0.032 dex, b_s (computed here from the 41 corrected overlaps) from +0.100 to +0.097, and S_sys from 0.080 to 0.078. The signal (0.094) and the calibration needed (±0.040 dex) do not move, and the classification stays "marginal".
- The other four samples are unchanged by construction.

## Note appended 2026-09-30: the NOEMA3D CO masses (text above unchanged)

The data chat's multi-tracer compilation (f5769b7d2, `data_assembly/MULTI_TRACER_GAS_2026-09-30.md`) found that Table 1's CO masses of the four CO(3-2) galaxies (G4_24078, GN4_32842, G4_17555, G4_37375) are 0.24 to 0.26 dex LOWER than the paper's stated R_13 = 1.8 recipe gives from the tabulated fluxes, and that G4_23011 (CO(4-3)) is 0.149 dex lower; the reconstruction's CO control fails for exactly these five. That finding is the data chat's and is unverified against the paper. This lane reads the same masses (`logMgas_CO_P1` equals Table 1 for these five). Re-running the lane UNCHANGED except that those five CO masses are raised by the reconstruction's residuals (`CFG213_dysmalpy_two_sided/cfg213_noema_co_sensitivity.py`; control: with no offset the re-run reproduces the committed results JSON exactly) gives: **one label moves, in both RC100 modes: the NOEMA3D row goes from 'statistics-limited' to 'systematic-limited'.** Its route bias b_s goes +0.048 to +0.074, S_sys 0.043 to 0.066, the statistical band 0.143 to 0.148, and the sample size for the 3σ-equivalent separation 210 to 225. The other four samples are unchanged and the bottom line ('no sample is discriminating') stands. The committed table above is for Table 1's masses as printed.
