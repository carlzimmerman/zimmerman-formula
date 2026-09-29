# MUSE-DARK II and III (plus their parent paper, MUSE-DARK I): what the arXiv tables hold (data front, 2026-09-29)

**Bottom line: neither paper has a per-galaxy table.**
- MUSE-DARK III (arXiv:2604.22613v1) has no tables at all.
- MUSE-DARK II (arXiv:2603.28856v1) has four tables: two lists of priors, the sample-level TFR fits and an observing log.
- None of the three items that decide III's circularity (fitted against SED M*, a₀ across halo families, a baryon-only fit) is tabulated in either paper.
- The parent paper, MUSE-DARK I (arXiv:2506.19721v3), holds the closest material:
  - the halo-model comparison counts, for its 127 galaxies rather than III's 79;
  - which parameters each model fits, and its M* priors;
  - one per-galaxy table covering only 3 galaxies, with halo parameters and no M*.
- Everything per galaxy is stated to be on the DARK data-release site, which was not visited.

**How this was read:**
- The arXiv HTML pages were read in a browser pane. The table cells and equation values were taken from the page DOM, so no summariser sits between the page and the numbers.
- A page summariser (WebFetch) was used only to get oriented and to read the version histories on the abstract pages.
- Nothing was downloaded: no PDF, no source tarball, and not the DARK site. No one was contacted.
- `checks.py` re-parses `raw_table_cells.txt` (the DOM cells) against every CSV and runs consistency checks against the papers' text. 21 of 21 pass (`checks.txt`).
- Standing rules apply. This is data only: no fit and no verdict. Nothing here says the data favour any law.

## Files
| file | paper, table | per galaxy? |
|---|---|---|
| `musedarkII_table3_tfr_fits.csv` | II Table 3, "TFR best-fit parameters". Six fits: sTFR and bTFR, free or fixed slope, v₁.₈ or v₂.₀, v/σ₀ > 1 or > 2 | no (N = 95 or 79) |
| `musedarkII_table1_kinematic_priors.csv`, `musedarkII_table2_sed_priors.csv` | II Tables 1 and 2: the priors of the kinematic and SED models | no |
| `musedarkII_table4_observations.csv` | II Table 4: the four lensing clusters' MUSE pointings, depth, PSF and photometric filters | no (per cluster) |
| `musedarkI_table2_3_halo_model_comparison.csv` | I Tables 2 and 3: galaxy counts for which each model is more likely than DC14, inconclusive, or less likely, by Bayesian evidence. 127 galaxies, and 44 with S/N_eff > 50 | no (counts) |
| `musedarkI_table4_free_parameters_by_model.csv` | I Table 4: which parameters each of URC, DC14, NFW, Dekel–Zhao, Burkert, coreNFW, Einasto and baryons-only fits | no |
| `musedarkI_table5_bestfit_halo_params_3galaxies.csv` | I Table 5 (App. H): V_vir, log M_vir, c_vir, r_s, ρ_s, log X and α_Einasto, each with its 95% CI | **yes, 3 galaxies (MUSE IDs 26, 6877, 958) × 6 halo models; no M* column** |
| `musedarkI_table1_mock_initial_conditions.csv` | I Table 1: two SIMULATED galaxies used for mock validation | simulated only |
| `musedarkIII_stated_results_NOT_A_TABLE.csv` | **compiled by me** from III's equations and text: every a₀, a₁ and scatter value, the MOND and mixed-halo variants, the M*-shift tests, and the error convention as stated | no |
| `provenance.csv` | for every CSV: URL, version, table label, caption, DOM element, rendering, rows | |
| `raw_table_cells.txt` | every table's cells, caption and note as read from the DOM | |

## The three items that decide III's circularity
**(a) Fitted M* and photometric (SED) M* per galaxy: NOT TABULATED anywhere.**
- III only cites the parent paper. I's Fig. 11 (left panel) shows DC14 dynamical M* against SED M* per galaxy, as a **raster PNG** (`MsMdc14.png`), for the parent sample. The text does not state how many galaxies are plotted, and it is not III's 79 separately. The text of I (Sect. 5.2.3) summarises it:
  - the dynamical M* is on average 0.11 dex lower;
  - "the majority" lie within ±0.5 dex;
  - the slope is about 0.82 ± 0.1 once perturbed galaxies are excluded.
- III's Fig. 4 (M* against z) and Fig. 6 (M/L_K) are raster too.
- Two SED values appear in III's text: MXDF 1266 at 10^9.05 and MOSAIC 905 at 10^10.3 M☉.
- **How M* enters each fit (I Sect. 2.3 and Table 4):**
  - DC14 and Dekel–Zhao do not fit M* directly. They fit X = log(M*/M_halo), and in DC14 X sets the halo's shape parameters (α, β, γ). That is how the paper breaks the disc–halo degeneracy.
  - NFW, Burkert, Einasto and coreNFW fit M* with a Gaussian prior on the SED value, ±0.15 dex.
  - **DC14, Dekel–Zhao and baryons-only have no prior on M*.**
- **So III's main (DC14) fit has M* free of the SED, and its halo shape is tied to that same fitted M* by construction.**
- (Mine:) III's per-galaxy best-model variant (App. D, a₀ = 2.61) mixes SED-anchored fits (NFW and the like) with unanchored ones (DC14, DZ). III does not state how many of its 79 galaxies fall in each family.

**(b) a₀ or fit quality across III's halo families: PARTLY, and at sample level only.**
- III quotes only three sample-level fits, none per family (for example NFW alone):
  - DC14 for every galaxy: 2.38 (Eq. 2);
  - each galaxy's best-evidence halo: 2.61 (Eq. 8), with a₀(0) = 1.05 and a₁ = 1.63 (Eq. 9);
  - MOND: 2.19 (Eq. 13).
- Fit quality across families is in I's Tables 2 and 3 (extracted), as counts against DC14 for the 127-galaxy parent sample. It is not given for III's 79 and not per galaxy.
- Fig. 7 of III colours the RAR points by halo family, but it is a raster.

**(c) A baryon-only (no-halo) fit: NOT IN III; sample-level only in I.**
- III has no Newtonian baryons-only fit. Its halo-free fits are MOND fits (App. E), in which a_bar comes from the fitted baryonic model:
  - the per-galaxy a₀ has a median of 2.27e-10 and a range of 1.3e-11 to 9.6e-10;
  - with a₀ fixed at 1.2e-10, M* rises by about 0.28 dex over the DC14 values and lies above SED;
  - the MOND fits underperform the DM models for over 60% of the sample.
- I fitted a baryons-only model (Sect. 5.1):
  - it is less likely than DC14 in 107 of 127 galaxies (41 of 44 at high S/N);
  - its disc masses exceed SED M* by about 0.76 dex (Chabrier) or 0.53 dex (Salpeter), after molecular gas from scaling relations;
  - the per-galaxy values are "not shown".

## The other items asked for
- **III, per-galaxy a₀ or acceleration points (a_bar, a_tot): NOT TABULATED.**
  - They appear only in raster figures: Fig. 1 (`roxy_rar_fin_withVarasteanu.png`), Fig. 7 (`RAR_bestfit.png`), Fig. 9 (`RAR_MOND3.png`) and the a₁ histogram in Fig. 8.
  - The four redshift bins hold roughly equal numbers of **data points**, not galaxies. The text states neither the bin edges nor the counts.
  - Only the lowest bin (about 1.99) and the highest (2.71) are printed. The middle two appear only in Fig. 3 (raster).
- **II, per-galaxy v₁.₈ or v₂.₀, M*, gas mass, R_e, inclination and σ₀: NOT TABULATED, and no release is stated.**
  - II has no data-availability statement for its kinematic parameters.
  - The one data URL in II is the parent lensing-cluster survey's data release (Richard et al. 2021: cubes and catalogues), not these fits.
  - The 95 galaxies appear only in the raster Fig. 7 (`sTFR.png`). A few highlighted galaxies are shown in Fig. 6 (`highlights.png`), for example ID13253, ID9778 and ID12978.
- **Image or PDF only:**
  - Every figure in all three papers is a raster PNG. The digitisable vector route used for KURVS is not available.
  - No table is image-only: all of them render as HTML.
  - III simply has no tables. I did not open the PDFs, so I cannot say whether a PDF carries anything the HTML lacks. (Mine: the arXiv HTML is built from the same source, so none is expected.)

## Stated in the papers' text that bears on CFG190's inputs (arithmetic mine; for the calculation thread, not a verdict)
1. **III's errors are 95% confidence intervals.**
   - Sect. 3.1 and 3.2 say so for Eq. 2 (2.38 −0.10 +0.12) and Eq. 4 (a₀(0) = 1.0 ± 0.04, a₁ = 1.59 ± 0.10).
   - The convention for Eqs. 8, 9, 13 and 14 is not stated.
   - CFG190 took ±0.10 and ±0.04 as 1σ, so its pulls against III are about 2× too small if the errors are Gaussian.
2. **II's own comparison with models adds the ±0.16 dex statistical uncertainty of the local (Lelli et al. 2019) bTFR zero point, plus its sample's systematics (Sect. 7.3).** CFG190 used 0.06 dex.
   - With 0.06 and 0.16 in quadrature (0.17 dex), III's own law against II would give pulls of −2.4 (deep), −1.9 (y = 0.3) and −1.2 (y = 1), against CFG190's −6.9, −5.4 and −3.4.
   - Under CFG190's |pull| ≤ 2 rule, III's law would then fit both papers at y ≥ 0.3.
   - Whether the local zero-point error belongs in the comparison is a judgement for the calculation thread's frozen criteria. I have not re-run anything.
3. II Table 3 does not state its error convention.
4. **Quantities that differ from the record:**
   - II's bTFR intrinsic scatter is **0.16 dex**. The "0.10–0.12 dex" in `data_assembly/timeline/MUSE_DARK_A0Z_2026-09-29.md` is the sTFR's.
   - The fiducial sTFR offset recomputed from the table's rounded b − b_ref is −0.41, against −0.42 in the text: a rounding difference.
5. **How II builds its baryons:**
   - M_bar is stellar mass plus gas from scaling relations: H₂ from Tacconi et al. (2020); HI from the NeutralUniverseMachine model, × 1.33 for helium.
   - The atomic fraction of M_bar has a median of 22% (5th–95th percentiles: < 1% to 77%). The molecular fraction has a median of 34% (range 13–53%).
   - Each galaxy is given an M_bar error of ±0.2 dex.
   - The authors call the bTFR "more indirect".
   - v₂.₀ = v_c(2R_e) comes from the fitted arctan model, with Dalcanton–Stilp pressure support. It is not a data point.
6. **III's own robustness tests:**
   - Recovering a₀ = 1.2e-10 would need a uniform M* shift of about +0.2 dex (lowest-z bins) to +0.45 dex (highest). The authors reject a shift that large (App. C).
   - Unmodelled molecular gas is quoted as about 0.2 dex on the total disc mass.
   - III's a_bar (Eq. 6) has disc, HI and bulge terms only.
   - (Mine, unverified:) I calls the baryons-only model's fitted disc mass "M⋆+M_mol". If DC14's fitted "M*" also absorbs molecular gas, its 0.11 dex deficit against SED stars would leave no room for that gas. The papers do not say which reading holds for DC14.

## What the tables can and cannot decide (plain statement)
**What they can do:**
- show how the fits are built: DC14's M* is free, has no SED prior, and is tied to the halo shape through X;
- show that the parent paper's data prefer halo models over baryons-only by a wide margin;
- give the sample-level numbers above.

**What they cannot do:** decide III's circularity. No arXiv table gives per-galaxy fitted M* next to SED M*, a₀ per halo family, per-galaxy baryon-only masses, or the (a_bar, a_tot) points. II gives no per-galaxy data, so it cannot be refitted either.

**What would decide it:** the DARK data release. I says it holds the best-fit parameters of all seven models with 95% CIs, plus the photometry catalogue with stellar masses; I have not verified this. Other routes: digitising raster figures (low fidelity), or II's authors, whose table is not public. Each needs the owner's go.
