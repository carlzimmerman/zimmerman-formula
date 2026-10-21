# Provenance: summary_figure (working note, 2026-10-21)

Plot only. Every plotted number is read by `make_figure.py` from the committed file named below and written, with its source
and field, to `plotted_numbers.json`. `figure_audit.py` re-reads each source with its own code and checks every number
(output: `figure_audit.out`). "Commit" is the last commit that touched the source file (`git log -1 -- <file>`). Paths are
repo-relative. κ = ½ is fitted; the two a0 footings (canonical 9.3603e-11, alt 1.1312e-10 m s⁻²) are never pooled.

Conversions (the only arithmetic besides the SPARC rebuild): ln → dex is x / ln 10; a lensing amplitude A becomes log10 A
with error σ_A / (A ln 10); the implied-a0 scale s* (relative to 9.3603e-11) becomes a0(z)/a0(footing) by × 1 (canonical)
or × 9.3603e-11 / 1.1312e-10 (alt).

| Panel | Plotted number(s) | Field / conversion | Source file | Commit |
|---|---|---|---|---|
| (a) | 3389 SPARC points from 175 rotation curves (g_bar > 0, g_obs > 0, disc M/L 0.60, bulge 1.4×); binned medians and 16–84% in 0.25 dex bins (≥ 10 points), for each footing at its own M/L | rebuilt with CFG695's recipe (the CFG4 statistic); file set sha256 equals the one in `real_research/data/SPARC_table.README.md` | `real_research/data/sparc_data` | `999f94dfee` |
| (a) | a0 used to reproduce CFG695's rms: 9.36032e-11 / 1.1312e-10 (equal to the rounded footings to < 1e-15) | `numbers.a0_canonical`, `numbers.a0_rho_total` | `real_research/derivation_chain_2026/FP0_core_postulates_results.json` | `6123bd25b5` |
| (a), (b) | weighted rms about the law 0.1009 (disc M/L 0.60) canonical, 0.0994 (0.55) alt; printed as 0.101 / 0.099 dex; the ± rms shading | `numbers.S2.<footing>.rms`, `.U` | `campaign_fresh_gravity/CFG695_saturating_vacuum/cfg695_results.json` | `9c762dc8d1` |
| (b) | SPARC large discs +0.001 ± 0.022 / −0.023 ± 0.022; SPARC small discs +0.059 ± 0.037 / +0.025 ± 0.036; Local Group dSphs (83) +0.372 ± 0.044 / +0.332 ± 0.044 dex | `byfoot.<f>.V0.class_summary.{SL,SS,DW}` (dex; se / ln 10) | `campaign_fresh_gravity/CFG919_pressure_support_selector/cfg919_results.json` | `8c46b7a2e1` |
| (b) | Coma UDGs (9) +0.330 ± 0.114 / +0.291 ± 0.114 dex | `byfoot.<f>.primary.samples.coma.mean_Eobs_dex`, `se_obs` / ln 10 | `campaign_fresh_gravity/CFG933_udg_sealed_test/cfg933_results.json` | `87b15752ee` |
| (b) | eRASS1 cores A_MID 1.910 ± 0.119 / 1.754 ± 0.109 → +0.281 ± 0.027 / +0.244 ± 0.027 dex; outskirts A_OUTER 1.012 ± 0.087 / 0.927 ± 0.080 → +0.005 ± 0.037 / −0.033 ± 0.037 dex | `A.<f>\|b0.67\|rc0.15\|f0.20.{MID,OUTER}` (the primary bracket: β 2/3, r_c 0.15 R500, f* 0.20) | `campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_results.json` | `a84425a1d5` |
| (b) | cross-check only (not plotted): CFG922's K1 copy of the same A_MID / A_OUTER | `K.K1.A_can`, `K.K1.A_alt` | `campaign_fresh_gravity/CFG922_cluster_core_baryon_recheck/cfg922_K.json` | `e10ff47a22` |
| (b) | tidal dwarfs (6) −0.690 ± 0.078 / −0.728 ± 0.079 dex, zero-supply (Newton) expectation −0.745 / −0.782; NGC 1052-DF2/DF4 −0.842 ± 0.209 / −0.881 ± 0.209 dex, expectation −0.852 / −0.891 | `S1.<f>.mean`, `.se`; `routes.<f>.law.U.stats.rbar`, `.se` / ln 10; `routes.<f>.route_i.{T,U}.per_object[*]` means of `Delta_pred`, `E_pred` / ln 10 | `campaign_fresh_gravity/CFG936_below_law_systems/cfg936_results.json` | `92ee16f2dd` |
| (c) | T1x −7.70 (robustness −10.96 … −4.60), T2x −7.18 (−10.22 … −4.28); class CONSISTENT | `runs.L100_N1024_{canonical,alt}.surveys.KiDS.dchi2`, `.robust` (widen2, noIA, held, DESI) | `campaign_fresh_gravity/CFG650_theory_v2_combined_pm/cfg650_native_results.json` | `0576674906` |
| (c) | class lines: TENSION Δχ² ≥ 4; EXCLUDED Δχ² ≥ 9 | criteria § Classes | `campaign_fresh_gravity/CFG650_theory_v2_combined_pm/FROZEN_CRITERIA.md` | `3087298c7b` |
| (c) | NC1x −10.08 (robustness −13.78 … −6.13); χ²_min 144.68 | `surveys.KiDS.dchi2`, `.robust` (widen2, noIA, held, LOC), `.chi2_F` | `campaign_fresh_gravity/CFG654_independent_inputs/cfg654_native_results_NC1x.json` | `b2ccd976dc` |
| (c) | NC2x −9.39 (robustness −12.85 … −5.69); χ²_min 145.38; matched control 154.76; 108 kept points; DES Y3 −2.15 (CONSISTENT, diagnostic) | `surveys.KiDS.*`, `surveys.DES.dchi2` | `campaign_fresh_gravity/CFG654_independent_inputs/cfg654_native_results_NC2x.json` | `8e1f1763c4` |
| (c) | projection-Ω_m range (0.2806–0.3308), T1x −11.93 … −0.94, T2x −11.09 … −0.92 | `variants.OM_*` (as-scored kept set) `.results.<f>.KiDS.dchi2` | `campaign_fresh_gravity/CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_T.json` | `6e7ac5154e` |
| (c) | projection-Ω_m range, NC1x −15.80 … −3.11 | same | `campaign_fresh_gravity/CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC1x.json` | `b2ccd976dc` |
| (c) | projection-Ω_m range, NC2x −14.69 … −2.93 | same | `campaign_fresh_gravity/CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC2x.json` | `dcc30c8981` |
| (d) | framework's native BAO-ruler band, a0(z)/a0(0) median [68%]: z 1.0 0.913 [0.762, 1.027]; 1.2 0.925 [0.762, 1.048]; 1.5 0.942 [0.706, 1.115]; 2.0 0.922 [0.561, 1.155]; 2.33 0.909 [0.325, 1.212] (extended flat to 2.5, marked "extrap."); decisive-target error 0.100 dex at z 2.5 | `BAO+SN.P1.<z>.sqrtX_q`, `BAO+SN.P6.2.0.sqrtX_q`, `BAO+SN.P6.2.5.DM14.e20_close` (primary rows only; θ* rows not used, K9 failed as frozen) | `campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json` | `6c064b83a3` |
| (d) | rival a0 ∝ H(z): the E(z) curve of the 2026-10-01 chart (1.79 at z 1, 3.03 at z 2, 8.29 at z 5); CFG689's native-background E(z) is 0.6–1.7% lower at its nodes | `curves["H(z)"]` | `campaign_fresh_gravity/CFG223_a0_over_cosmic_time/cfg223_results.json` | `155eb31e67` |
| (d) | ALESS 122.1 (z 2.024): s* 8.82, 68% 4.20–14.37, 95% 1.51–22.64; ALPINE 6 pooled (z 4.564): 4.33, 2.93–5.55, 0.32–9.21 | rows `ALESS_122.1`, `ALPINE6 pooled` | `campaign_fresh_gravity/CHART_a0z_combined_2026-09-30/chart_a0z_points.csv` | `4d7b44787c` |
| (d) | RC100 native route B: z 0.81 1.48 [1.30, 2.26]; z 1.36 1.01 [0.61, 1.68]; z 2.01 0.84 [–, 1.67]; Q4 (z 2.26) no root, 95% upper bound 0.48. CRISTAL native (z 5.26): R_e 2.01 [0.24, 7.27], R_out 1.95 [0.42, 5.05] (95% bars in the JSON) | `points.RC100["B Q1".."B Q4"]`, `points.CRISTAL[...]` | `campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_rc100_cristal_LCDMFREE_results.json` | `2d9bdc1b92` |
| (d) | MeerKAT MIGHTEE-HI: s* 1.401, 68% 1.360–1.515, 95% 1.289–1.784 | `frame.s`, `frame.q_a0` / 9.3603e-11 | `campaign_fresh_gravity/CFG309_mightee_width_frame/cfg309_cfg301chain_FRAME_summary.json` | `53f8fa937e` |
| (d) | MeerKAT redshift 0.067 (median of the three window medians) | `numbers.results.W1..W3.z_med` | `campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain/cfg301_stageB_results.json` | `6b10c01c00` |
| (d) | "53 further galaxies … no a0 solution" | last "The floor count is now N" | `campaign_fresh_gravity/CHART_a0z_rar_z0_5_2026-10-01/README.md` | `55d09ea036` |

## Labels that differ from the request, and why
- **"Local Group dSphs (83)"**, not "Milky Way dSphs": the record's +0.372 / +0.332 dex is the class mean of the 83 Local Volume
  dwarfs (MW and M31 satellites and field dwarfs; CFG880 sample, CFG919 V0). The record finds MW and M31 satellites alike
  (CFG843, +0.055 ± 0.117 dex); no MW-only class mean with an error is committed in the same estimator.
- **Coma UDG error** is the observational standard error `se_obs` (offset from the law), not CFG933's `se_c`, which adds the
  P2 prediction's width; the two differ by < 0.001 dex.

## Left out, and why
- **Red early-type lenses** (+0.127 / +0.088 dex, CFG919): not in the requested class list; possibly a stellar-population (IMF)
  effect (CFG926 R5, conditional). **Isolated blue lenses** (A = 1.016 ± 0.086, CFG829): not requested.
- **CFG921's cell-weighted cluster fact** (+0.243 / +0.207 dex): the panel uses CFG687's A_MID, as asked.
- **Panel (c):** DES Y3 for T1x, T2x and NC1x (NOT DIAGNOSTIC, T-OWN fails). The CFG909 covariance variants (all CONSISTENT).
- **Panel (d):** the MUSE-DARK route series and the KiDS colour-class levels (route-dependent, not independent a0 values in the
  record's words); upper-bound-only discs (KMOS3D, SINS, Danhaive, ALPAKA, HZ9, zC-488879); the 53 no-root galaxies (counted in
  the panel note); the baryon-mass systematic bands (stated as not drawn); CFG689's θ* rows (K9 failed as frozen).

## Re-run
`OMP_NUM_THREADS=1 nice -n 10 python3 make_figure.py` then `OMP_NUM_THREADS=1 nice -n 10 python3 figure_audit.py` (from this
directory; one core, under 0.3 GB, seconds).
