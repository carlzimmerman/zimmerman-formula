# CFG216 — RC100 (Nestor Shachar+2023, 100 massive discs at z 0.61–2.52): a WITHIN-SAMPLE δ(z) test with velocities. FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, before any CFG216 number. **κ = ½ FITTED, NOT DERIVED.** Author decompositions, not a direct a₀ measurement.

## Why

- CFG215 could not diagnose a trend ACROSS samples, because the route biases differ. Within ONE homogeneous sample, the route is uniform: RC100 is one analysis (3D forward modelling, prior-anchored M_bar) covering z 0.61–2.52.
- Its table gives V_c(R_e) and f_DM(R_e) per galaxy, so no geometry assumption is needed: g_obs = V_c²/R_e and g_bar = (1 − f_DM) g_obs.
- If the flat law is right, δ_flat ≈ 0 with no trend in z. If the rival a₀ ∝ H(z) is right, δ_rival ≈ 0 and δ_flat drifts upward with z.

## Exposure, disclosed

- The committed CFG52, CFG54 and CFG90 counts and pooled offsets. They used RC100 with a g_bar < a₀ selection. The pooled z ≥ 1.5 sample (N = 14) had flat +0.135 and rival −0.037.
- CFG215's RC41 δ. **RC100 contains the RC41 galaxies:** the names match (e.g. EGS3 10098, U3 21388, EGS4 21351, GS4 13143).
- The RC100 table's header, its z range (0.61–2.52), the first row's ID and z, and the first names. No RC100 δ, D or g_bar value has been computed or seen.
- **Hand expectation:** the RC41 subset repeats CFG215's positive δ_flat (~+0.1). Beyond that, the sign of the slope is unknown to me.

## Data and quantities

- **Data:** `real_research/data/rc100_nestorshachar2023_table3.csv`: name, z, log M_bar, R_e, f_DM(R_e), V_c(R_e), σ₀.
- **Sample:** all rows with finite z, R_e, V_c and 0 < f_DM < 1. The exclusions are counted.
- **Quantities:**
  - D_obs = 1/(1 − f_DM);
  - g_obs = V_c²/R_e;
  - g_bar = g_obs/D_obs = (1 − f_DM) g_obs.
  - The table's own g_Re and M_bar columns are used only in the controls and variants below.
- **δ_L = log₁₀(D_obs/ν(g_bar/a₀,L)).** The laws are flat A0_f and rival A0_f E(z), with Ω_m 0.315. Kernels: ν_mono (primary) and P2. Footings: canonical decides; alt is reported.

## Statistic and decision rows

- **Within-sample slope:** the Theil–Sen slope of δ_L on z, with a 95% bootstrap CI (10,000 resamples of galaxies, seed 216).
- **Outcomes** for the pair (slope of δ_flat, slope of δ_rival):
  - **W-flat:** the CI of δ_flat's slope contains 0 and δ_rival's slope CI is < 0. Flat-like drift structure; the rival's z-dependence is not in the data.
  - **W-rival:** δ_flat's slope CI is > 0 and δ_rival's slope CI contains 0. Rival-like.
  - **W-none:** both CIs contain 0. No z-dependence detectable.
  - **W-mixed:** anything else, reported as is.
- **Expected slopes.**
  - With each hypothesis exactly true (g_obs and z held at the sample's own values, baryons from that law's inversion), the slope of δ_flat is computed: 0 if flat is true, s_R if the rival is true. Likewise the slope of δ_rival: 0 if the rival is true, −s_F if flat is true.
  - The observed slopes are reported against those expectations as z-scores from the bootstrap (σ of the slope).
- **Level, reported:** the median δ_L in the two z-halves (split at the median z) with 95% CIs and CFG213's verdict labels.
- **Sensitivities, reported beside the primary, never substituted:**
  - (a) the 41 RC41 galaxies only;
  - (b) the other galaxies only (n = 100 minus the RC41 subset);
  - (c) the g_bar< 3 a₀ subset, where the laws differ most;
  - (d) g_bar from the table's M_bar and R_e through a thin exponential disc (R_d = R_e/1.678), with D_ind = g_obs/g_bar,geom, for the galaxies with a finite M_bar.
- **Route and selection statement.** M_bar is prior-anchored in RC100's fits. Any z-dependence of the gas-scaling prior or of the sample selection enters the slope. A slope is labelled "route- or selection-dependent" wherever (d) or the halves disagree in sign with the primary.
- **Language:** no sentence says the data favour the framework.

## Controls

- **C1.** A synthetic galaxy placed exactly on each law returns δ = 0.
- **C2 (cross-check of CFG215's geometry).** For the RC41 galaxies found in RC100 by name (space ↔ underscore), the median of δ_flat(RC100: V_c, f_DM) − δ_flat(CFG215: my disc + bulge geometry from the RC41 table) is reported.
  - Pass line: |median| < 0.05 dex.
  - A fail is reported plainly, with the size of the shift for CFG215's RC41 verdict.
- **C3.** Recovery of an injected slope: δ_flat + 0.2 (z − z_med) shifts Theil–Sen's slope by 0.2 to 1e-9.
- **MUTATE=1.** D_obs × 10^{0.2 (z − z_med)}. Both laws' slopes must change by exactly the injected amount, plus the kernel's response. The δ_flat slope must move by at least +0.19. Outputs are written separately.
