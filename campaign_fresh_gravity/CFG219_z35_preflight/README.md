# CFG219 — a pre-flight power forecast for the z > 3.5 decisive test (independent-baryon discs only)

- **Criteria:** `FROZEN_CRITERIA.md` (e62ce4cff), committed before any number. **κ = ½ is FITTED, NOT DERIVED.** A forecast, not a measurement: nothing here says the data favour a framework.
- **Run:** `python3 campaign_fresh_gravity/CFG219_z35_preflight/cfg219_preflight.py` (about 80 s; `MUTATE=1` runs the response controls), then `cfg219_plot.py` for the chart. 8 of 8 controls pass. The first run (`*_firstrun*`) failed one control that was my own error, see Disclosures.
- **Inputs (z, radius, baryon masses and errors only; no velocities, no f_DM):** the six CRISTAL discs with a dust-DETECTED gas mass (02, 03, 07a, 11, 19, 20; z 4.4 to 5.7) from the tables on disk. A labelled provisional scenario S8 adds GN20 and REBELS-25 with mid-range published values (REBELS-25's radius is a placeholder). Laws: Z1's flat, H(z), particle horizon and ΛCDM-native, each pair its own test, never pooled.

## Bottom line

- **Expected separation.** For the primary pair (flat vs the rival H(z)) the six discs' pooled δ shifts by **−0.27 dex** (flat true, H(z) tested) or **+0.22 dex** (H(z) true, flat tested) at R_e, and by −0.33 / +0.30 dex at the radius reached (R_out, 1.4 to 3.0 R_e). Per disc it runs from −0.15 to −0.32 dex for the CRISTAL discs; the two provisional S8 discs give only about −0.07 because they are near-Newtonian at R_e (g_bar/a₀ = 19 and 45).
- **Statistical power alone** (baryon errors, no calibration systematic; the frozen n_σ, median over 500 mocks; Monte Carlo error 0.1 to 0.2σ, see `cfg219_mc_error.out`):
  - flat vs H(z): **2.5σ with the six discs at R_e (3.9σ at R_out); 3σ needs about 9 discs at R_e (6 or fewer at R_out)**;
  - flat vs particle-horizon: 3.4σ with six, 3σ at 6 discs; flat vs ΛCDM-native: 1.8σ, about 17 discs; horizon vs ΛCDM-native: about 16 discs;
  - **H(z) vs horizon needs about 54 discs, and H(z) vs ΛCDM-native is not separated by N = 100** (n_σ 1.0 and 0.8 at N = 6).
- **The calibration limit (post hoc, see Disclosures 1): this is the finding that matters.** A gas-mass calibration systematic τ shared by every disc of a tracer class does not average down. With systematic-inclusive n_tot = |shift| / (total scatter of the pooled δ) and the baseline τ = 0.25 dex on the gas mass (about 0.15 dex on the baryon mass at these gas fractions):
  - **flat vs H(z) never reaches 3σ at R_e for any N ≤ 20** (n_tot 1.6 to 1.9; 2.4 at N = 100), and reaches 3.1 ± 0.2σ (borderline) at N = 20 at R_out;
  - the largest τ at which 3σ survives (both directions), at N = 6 / 13 / 20 / 100: **R_e none / 0.08 / 0.16 / 0.21 dex, R_out 0.19 / 0.21 / 0.26 / 0.27 dex**. Even with unlimited discs the shared gas calibration must be known to about 0.2 to 0.3 dex on the gas mass, roughly 0.1 to 0.15 dex on the baryon mass;
  - flat vs horizon is the most robust pair (τ_max 0.14 / 0.20 / 0.23 / 0.26 at R_e, 0.29 / 0.32 / 0.33 / 0.38 at R_out).
- **Which pairs can a 13 to 20 disc sample separate?** (S6 properties resampled, R_e; ✓ = n ≥ 3):

| pair | statistical only, N = 13 / 20 | with τ = 0.25 (n_tot), N = 13 / 20 | with τ = 0.25 at R_out (n_tot), N = 13 / 20 |
|---|---|---|---|
| flat vs H(z) | 3.6σ ✓ / 4.4σ ✓ | 1.9 / 1.9 | 2.4 / 3.1 ± 0.2 (borderline) |
| flat vs horizon | 4.3σ ✓ / 5.9σ ✓ | 2.6 / 2.8 | 3.7 ✓ / 3.8 ✓ |
| flat vs ΛCDM-native | 2.8σ / 3.4σ ✓ | 1.5 / 1.3 | 2.2 / 2.2 |
| horizon vs ΛCDM-native | 2.5σ / 3.4σ ✓ | 1.2 / 1.5 | 1.9 / 1.9 |
| H(z) vs horizon | 1.5σ / 1.8σ | 0.7 / 0.6 | 0.9 / 1.0 |
| H(z) vs ΛCDM-native | 1.0σ / 1.2σ | 0.4 / 0.5 | 0.6 / 0.6 |

  So with the baseline calibration only flat vs horizon is separable by 13 to 20 such discs, and only if the outer radius is used; flat vs H(z) needs the calibration held to about 0.2 dex or better. **Using the radius reached instead of R_e raises every flat-vs-X significance** (the discs are deeper in the MOND regime there).
- **GN20 and REBELS-25 (provisional) do not help at R_e:** both are near-Newtonian there, so the flat-vs-H(z) N for 3σ rises from about 9 to about 15 (statistical only) when they are added. Their outer radii are what they would need.

## Sensitivities (flat vs H(z), N = 6, statistical only; Monte Carlo error about 0.1σ here)

| cell | n_σ |
|---|---|
| ν_mono canonical (primary) | 2.54 |
| ν_mono alt footing | 2.72 |
| P2 canonical / alt | 2.17 / 2.35 |
| σ★ = 0.10 / 0.25 dex (baseline 0.15; a separate stream gave 2.40 to 2.52) | 2.51 / 2.22 |
| S8, REBELS-25 R_e × ½ / × 2 (baseline 2.15) | 2.09 / 2.44 |

The kernel and the footing move n_σ by about ±0.3σ (P2 is lower); the frozen classes for flat vs H(z), flat vs horizon and flat vs ΛCDM-native change between cells (kernel/footing/radius-dependent), and the borderline 3σ ones are within the Monte Carlo error. The two H(z) pairs with horizon and ΛCDM-native are not separated in any cell.

## Disclosures

1. **The frozen n_σ is blind to a shared calibration systematic, and the frozen classes CALIBRATION-ROBUST / CALIBRATION-LIMITED mean nothing.** n_σ is the median over mocks of |median δ| / the bootstrap sd inside the mock. A calibration offset shared by all discs moves each mock's median δ by the same amount but is not in the bootstrap sd, and its sign is symmetric across mocks, so the median over mocks does not move: Result 2 is flat in τ by construction (flat vs H(z), N = 6: 2.5, 2.5, 2.2, 2.7 at τ = 0, 0.10, 0.25, 0.40), and the frozen control C5 (saturation) passes trivially. I noticed this after the first numbers and added, labelled POST HOC, the systematic-inclusive n_tot = |μ| / sd over mocks (Result 6) and a discriminating control C5b (n_tot falls by ≥ 20% between τ = 0 and 0.25 at N = 100 for at least five of the six pairs: passes). Every calibration statement above uses n_tot, not the frozen classes. The frozen results are all in `cfg219_preflight.out`.
2. **A control of mine was wrong in the first run:** C0 compared the disc formula's peak V² with 0.6238 G M / R_d; the peak is 0.3872 G M / R_d (0.6238 is its square root, V_max = 0.622 √(G M / R_d)). The formula was right (0.387 reproduced); the first run is kept as `cfg219_preflight_firstrun.out` and `_MUTATE_firstrun.out`.
3. **Monte Carlo noise:** 500 mocks per cell. Ten reseeded reruns of the primary pairs (`cfg219_mc_error.py`, post hoc) give a standard deviation of 0.07 to 0.23σ on n_σ and 0.05 to 0.28σ on n_tot (largest at N ≥ 13 and τ = 0.25), so the borderline 3σ statements (flat vs H(z) at N = 20 at R_out: 3.1 ± 0.2; flat vs horizon at N = 20 at R_e, τ = 0.25: 2.7 ± 0.2) are within about one to two Monte Carlo errors of the line. The R_out block was recomputed on the full N and τ grids in the final run (the first run had only N = 6, 13, 20 and τ = 0, 0.25); its n_σ moved by up to 0.3σ (flat vs horizon, N = 6, τ = 0: 5.26 to 4.95).
4. **Optimistic in these ways:** no velocity or f_DM measurement error (it would add to every disc's scatter); a thin exponential disc carrying all M_b with no bulge (CRISTAL's fits carry B/T of 0.1 to 0.3); the gas follows the stars; σ★ = 0.15 dex is an assumption (the tables carry no M★ errors); two tracer classes, each with one shared τ; the f_molgas errors are treated as gas-mass errors independent of M★; "N discs" means N resampled from these properties, not N new galaxies; the ΛCDM-native law is extrapolated beyond z = 5 (REBELS-25 only).
5. **S8 is provisional:** GN20 (z 4.055, R_e 3.6 kpc, M★ 1.6e11, M_gas 1.0e11) and REBELS-25 (z 7.3065, M★ 8e9, M_gas 1.0e11, **R_e = 1.5 kpc a placeholder**) use mid-range published values from the data chat's list, which extracted no per-disc tables; they are replaced when the data chat reads the papers. Class B and every dust upper limit are outside the forecast (a one-sided limit cannot be simulated as a value).

## Chart

`cfg219_power_forecast.png`, from `cfg219_plot.py` (no new statistic): the systematic-inclusive significance against N for flat vs H(z) and flat vs horizon at each shared gas calibration τ (R_e solid, R_out dashed), and the largest τ that keeps 3σ for every pair.

## Post hoc note from CFG220 (appended 2026-09-30; the text above is unchanged)

- The first real-data use of these six discs at the outer radius on the independent route (`../CFG220_cristal_outer_independent/`, lane bfb27770a) gives a disc-to-disc scatter of the realised δ of **0.24 to 0.25 dex**, against **0.14 per disc** from this forecast's baryon-error-only noise at R_out (the rms of the per-disc noise over the six discs, plus the 0.04 spread of the noiseless separations): about **1.8× larger**. The excess is what the forecast omitted (velocity and f_DM errors, bulge, geometry, the fit's baryon shape). **Read every number of discs for 3σ above as a lower bound;** if the excess is random the N grows by about 1.8² ≈ 3. Six discs make the ratio uncertain by about ±30%.
- The realised pooled δ at R_out (flat +0.106, rival −0.203) lies between the forecast's flat-true (0, −0.34) and rival-true (+0.28, 0) points, closer to flat-true; the independent route at that radius is BOTH-CONSISTENT and calibration-limited (the class flips at a +0.07 dex gas-mass offset).
