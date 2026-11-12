# EUC11 (DEEP-FIELD LENSES): FROZEN CRITERIA

2026-11-12. Committed alone, before any script of this lane exists and before any deep-field row of a lens or control
galaxy has been queried. A test lane; it adopts nothing. κ = ½ FITTED. Footings (canonical 9.3603e-11, alt 1.132e-10
m/s²) graded separately, never pooled. One-sided: no outcome favours the framework.

## 0. Why this lane, and why a different lens sample

The Euclid Deep Fields have about 20 grism dithers per object against 4 in the wide survey, and both the blue and the
red grism. The ECLIPSE lens catalogue used by EUC1–EUC9 has no lenses there: no grade A/B lens lies within 2.4–3.0° of
any deep-field centre, with 2–7 per square degree just outside. The lenses of those fields are in the earlier Q1
Strong Lensing Discovery Engine catalogue (Zenodo 10.5281/zenodo.15025832): 576 grade A/B systems, 326 with a lens
model. This lane uses them. It is therefore **not** EUC1-F (which is written for ECLIPSE sample P) and **not** EUC5-F.

- **Part 1** repeats EUC1's and EUC4's source-free ceiling test on this independent lens sample.
- **Part 2** looks for lensed-source redshifts in the DR1 deep grism tables, with EUC3's rule and a matched-control null.

## 1. Data (frozen)

- Q1 lens tables, sha256: `q1_discovery_engine_lens_catalog.csv` ee5e60cd…26877; `modeling_lens_mass.csv`
  f2a52616…9db5; `modeling_lens_sersic.csv` c0b05783…d5c2; `modeling_sersic_magnitude.csv` 7c7506af…94f2 (full
  hashes are checked by the script). Outside git.
- IRSA TAP, anonymous, paced, generic client name: `euclid_dr1_mer_catalogue_deep_survey`,
  `euclid_dr1_phz_photo_z_deep_survey`, `euclid_dr1_spectro_z_spe_quality_deep`,
  `euclid_dr1_spectro_z_spe_galaxy_candidates_deep`, `euclid_dr1_spectro_line_features_spe_line_features_deep`,
  `euclid_dr1_spectro_z_spe_classification_deep`. Tables stay outside git.
- For the mass predictor: the ECLIPSE catalogue (EUC1's files and hashes) and EUC3's cached wide-survey MER and
  photo-z rows of ECLIPSE lens objects.
- Code: EUC1's `euc1.py` (cosmology, engine, statistics); EUC3's TAP helpers (`euc3_fetch.py`, imported, not edited).

**Seen before freezing (disclosed).** The Q1 catalogue's grade counts (309 A, 267 B, 2,008 C) and how many have a model
by grade (193 A, 133 B, 8 C); the positions (to find that ECLIPSE avoids the deep fields). The deep tables' column
lists. Forty rows of the deep quality table as the service returned them, and the line and candidate rows of four of
those objects, to learn flag values: grism labels `BGS+RGS` / `RGS`; line quality codes whose last digit is the grism
(1 blue, 2 red, 3 combined) and whose middle digit is 1 for a good fit; Hα rows exist at every solution rank. None of
those objects was chosen from or matched to a lens list. EUC3's result and diagnostics (wide survey: the rule passes
as often on non-lenses as on lenses; the one known pair has its true redshift at rank 1). **No deep-table row of any
Q1 lens has been queried, and no Einstein radius, Sérsic value or magnitude of the Q1 models has been summarised.**

## 2. Systems (frozen)

- **Lens systems L:** every Q1 catalogue row with grade A or B (576), at its catalogue position.
- **Model:** `einstein_radius_effective_median_pdf` (θ_E), `effective_radius_median_pdf` (R_e) and
  `sersic_index_median_pdf` (n), arcseconds. Usable if θ_E > 0, R_e > 0 and 0.6 ≤ n ≤ 10 (EUC1's conditions).
  A lens without a model takes, for the aperture only, the θ_E of the modelled lens number ⌊i · N_mod / N_unmod⌋
  (both lists sorted by identifier).
- **Counted objects:** every deep MER object within `r_a = min(θ_E + 0.7″, 3.0″)`. The **lens object** is the nearest
  if within 0.6″.
- **Lens redshift:** the deep pipeline photo-z of the lens object (`phz_median`, interval `phz_70_int_1/2`).
- **Controls C:** for each lens with a lens object, deep MER objects 20″–300″ away with `flux_h_templfit` within a
  factor 1.5 of the lens object's, `spurious_prob` < 0.2 and `point_like_prob` < 0.5. Six are drawn at random (seed
  20261112, sorted by object id before drawing); after their photo-z is fetched, up to three with
  |Δ phz_median| ≤ 0.15 are kept, in draw order. A control takes its lens's θ_E, and the rule is applied to it exactly
  as to a lens (its own position, its own counted objects, its own photo-z interval).
- **Evaluable system:** has a lens object, a photo-z interval, and at least one counted object with a galaxy solution
  whose spectrum passes Q1.

## 3. The rule for a secure source redshift (frozen)

EUC3's rule, with three changes for the deep tables (marked). Applied to every spectrum of every counted object.

- **Q1 spectrum:** `spe_npix` ≥ 300, `spe_n_dith_med` > 3, `spe_error_flag` = 0, `spe_gal_error_flag` = 0.
- **Q3 window (changed):** Hα inside that spectrum's own coverage: `spe_w_min` < 6564.61·(1 + z) < `spe_w_max`.
- **Q4 line (changed):** an `Halpha` row of the same object, spectrum and solution rank with `spe_line_qual_gf` in
  {211, 212, 213, 251, 252, 253}, `spe_line_fwhm_gf` ≤ 180 Å and `spe_line_snr_gf` ≥ 5; the row of highest S/N is
  used. No flux floor (the wide survey's nominal limit does not apply at this depth).
- **G1 above the lens:** `spe_z` ≥ z_up + 0.15.
- **G2 own-line guard (one line added):** rejected if `spe_z` lies within 0.01 of `(1 + z)·λ/6564.61 − 1` for z in
  [z_lo, z_up] and λ any of [S III] 9071.1 (added), [S III] 9533.2, He I 10833.3 to Pa γ 10941.1 (one band),
  Pa β 12821.6.

Two tiers:

- **Tier A (EUC3's):** rank-0 solution only, with `spe_z_prob` ≥ 0.99 and `spe_z_rel` > 0.05.
- **Tier B (any rank, two lines):** any solution rank 0–4, no probability cut, and a second line of the same rank
  among [O III] 5008, Hβ, [S II] 6718, [S III] 9530, [S III] 9068, [O II] 3727 with the same quality codes and
  S/N ≥ 3.

**System level:** SECURE if at least one counted spectrum is secure and all secure redshifts agree within 0.02 (z_s =
that of the highest Hα S/N); CONFLICT otherwise (excluded, counted).

## 4. Gates on the search (frozen)

- **H2 purity null.** The same rule on the controls. Pass if `n_C ≤ max(1, 0.20 · n_L · E_C / E_L)` (E = evaluable
  systems, n = SECURE). The null can fail wrongly (a control may be an unrecognised lens) but cannot pass wrongly.
- **Coverage.** At least 30 % of L and of C evaluable.
- **Ladder.** Tier A is graded first. If it fails H2, tier B is graded and every number is labelled "tier B (frozen
  fallback)". If both fail, Part 2's word is **NOT EVALUABLE** and nothing is loosened.

## 5. Stellar mass for the Q1 lenses (frozen)

The Q1 tables carry no stellar mass. A predictor is fitted on ECLIPSE: for sample S lenses whose lens object in
EUC3's cache has `flux_h_templfit` > 0 and a pipeline `phz_median` > 0, least squares of the catalogued
log M★ on `ℓ = log10(flux_h_templfit) + 2·log10 D_L(phz_median)` and `phz_median`:
`log M★ = α + β ℓ + γ z`. It is applied to a Q1 lens object's deep `flux_h_templfit` and `phz_median`. The residual
scatter is reported. All distances use the pipeline photo-z.

**Transfer check T1 (a gate on Part 1 and on every `b` of Part 2).** EUC1's and EUC4's source-free numbers recomputed
on ECLIPSE with the pipeline photo-z and the predicted mass in place of the catalogue's:
sample P: f25 within 0.03 of 0.156 / 0.139 and median b within 0.03 of −0.019 / −0.044; grade B with θ_E ≥ 1.7″:
f25 within 0.05 of 0.758 / 0.702. If T1 fails, Part 1 is **NOT EVALUABLE** and Part 2 reports redshifts only.

## 6. Part 1: the source-free ceiling on Q1 lenses (words)

Law S, source at z = 1100, EUC1's statistic `b` and `f25` (fraction with b > 0.25), bootstrap 95 % interval
(`euc1.stats`), on lenses with a usable model, a lens object, a photo-z and an H flux.

- **QA** (grade A; the analogue of EUC1's sample P): **CEILING BROKEN** if f25's lower bound ≥ 0.25; **CEILING
  HOLDS** if its upper bound ≤ 0.10; otherwise **NO VERDICT**. (EUC1 on P: NO VERDICT, 0.156 / 0.139.)
- **QW** (grades A and B, θ_E ≥ 1.7″; the analogue of EUC4): **WIDE LENSES BREAK THE CEILING** if f25's lower bound
  ≥ 0.25; **NOT CONFIRMED** if its upper bound ≤ 0.10; **NO VERDICT** otherwise; **NOT EVALUABLE** if N < 30.
- Reported: f25 and median b by Einstein-radius class (below 1.0″, 1.0–1.3″, 1.3–1.7″, 1.7″ and above), grade B alone,
  law B.

## 7. Part 2 reading (if the search is evaluable)

For every SECURE lens with a usable model and mass: `b` at the secure redshift (law S and B, both footings), beside the
same lens's source-free `b`. Lenses with z_l ≥ z_s − 0.2 are dropped and counted.

- **Parallel gate on grade A, N ≥ 10** (same thresholds as EUC1-F, different lenses; it does not grade EUC1-F):
  median b, law S: **Q1 LENS GATE HOLDS** if the upper bound ≤ 0.15; **FAILS** if the lower bound ≥ 0.25; otherwise
  **NO VERDICT**. With N < 10: **EARLY READING, NOT A GATE**.
- Reported: the class medians beside EUC5-F's sealed bands (a comparison on different lenses, not EUC5-F's grade);
  the two-line subset in tier A; hits on the lens object against hits on other counted objects, for L and for C.

## 8. Instrument checks and twins (frozen)

- K1 EUC1 reproduced on ECLIPSE: N(P) = 3,192, source-free median b −0.019 / −0.044 (±0.001).
- K2 association: at least 90 % of L have a lens object within 0.6″.
- K3 like-for-like: the controls' median H flux within 10 % of the lenses' and median photo-z within 0.05.
- K4 fetch: every counted object id queried in every table; one id chunk of the candidates table re-queried,
  identical.
- T1 as in §5.
- `EUC11_MUTATE=newton` (a₀ → 1e-30): f25 on QA must rise on both footings; exit 1.
- `EUC11_MUTATE=noguard` (G1 and G2 removed): the number of SECURE controls must rise in the tier in force; exit 1.

## 9. Stated in advance

- Chance emission-line galaxies inside a 3″ aperture grow in number with depth. EUC3's null failed in the wide survey
  for that reason, and it may fail here too; that would be a result.
- The Q1 lens models and the ECLIPSE models come from different runs. Part 1 on Q1 lenses is an independent sample,
  not a like-for-like copy of EUC1.
- Predicted masses carry the predictor's scatter. T1 measures what that does to the statistic.
- No part of this lane measures a₀ or κ.
