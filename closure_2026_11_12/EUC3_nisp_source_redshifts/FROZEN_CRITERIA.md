# EUC3 (NISP SOURCE REDSHIFTS): FROZEN CRITERIA

Committed alone, before any EUC3 script exists and before the grism (NISP) redshift or line tables have been queried for
any ECLIPSE lens or grade-X object. 2026-11-12.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not "theory
closed". No outcome of this lane may be described as the data favouring the framework: the gate it feeds (EUC1-F) is
one-sided.

## 0. What this lane is

EUC1 (`../EUC1_eclipse_saturation_ceiling/RESULT.md`) found Euclid's strong lenses at the law's ceiling and froze a
prospective gate, EUC1-F (its §8), to be graded when true source redshifts exist for at least 10 lenses of its sample P.
EUC2 looked for them in DESI fibre spectra and was NOT EVALUABLE (its automatic search failed its own purity null
twice). This lane looks in Euclid's own public DR1 red-grism redshift and line tables. A lensed source's Hα falls in the
red grism for 0.84 < z_s < 1.88; the arcs lie inside or beside the lens galaxy's slitless extraction; most deflectors are
quiescent and below z = 0.84, so an emission line in the lens object's grism spectrum is usually the source's.

EUC1-F is not redesigned here. This lane only supplies the source redshifts, under a rule and gates frozen below.

## 1. Data (frozen)

- ECLIPSE catalogue files, as EUC1 (same two CSVs, same sha256, checked on every run).
- IRSA TAP, anonymous, `https://irsa.ipac.caltech.edu/TAP/sync`, tables
  `euclid_dr1_mer_catalogue_wide_survey` (object_id, ra, dec and descriptive columns),
  `euclid_dr1_phz_photo_z_wide` (phz_median, phz_70_int_1, phz_70_int_2),
  `euclid_dr1_spectro_z_spe_galaxy_candidates_wide_survey` (spe_rank, spe_z, spe_z_err, spe_z_prob, spe_z_rel),
  `euclid_dr1_spectro_z_spe_quality_wide_survey` (spe_npix, spe_n_dith_med, spe_error_flag, spe_gal_error_flag),
  `euclid_dr1_spectro_line_features_spe_line_features_wide_survey` (spe_line_name, spe_line_flux_gf, spe_line_snr_gf,
  spe_line_fwhm_gf, spe_line_qual_gf, spe_line_central_wl_gf), and
  `euclid_dr1_spectro_z_spe_classification_wide_survey` (spe_class; recorded, not used by the rule).
  Column names were confirmed in `TAP_SCHEMA.columns`. Rows of the spectro tables are paired on `object_id`, the
  solution rank, and the observation key they share (patch / calibration-block list); an object observed more than once
  contributes each spectrum separately. Requests are paced, one stream, generic client name. Tables stay outside git.
- Performance paper: Le Brun et al., Euclid DR1 "Performance of the redshift measurement and spectroscopic analysis".

**Seen before freezing (disclosed).** The table schemas. The performance paper (cuts and warnings used in §3). The first
8 rows the candidates table returned and the line / quality / classification rows of three of those objects (to learn
line names, sentinels and flag values); a timing test on 300 objects in a 0.05° box at RA 140.50, Dec +71.05, of which
only row counts and response times were read. None of these objects was chosen from, or matched to, ECLIPSE. From
ECLIPSE itself: the photo-z interval widths and Einstein-radius percentiles of samples P and S, and the fraction of the
Hα window each candidate own-line guard leaves open (computed from lens photo-z's only). EUC1's and EUC2's results,
including EUC2's four confirmed lens–source pairs and its b for EUCL-DR1-L015763. **No grism redshift, line or quality
row of any ECLIPSE lens or grade-X object has been queried.**

## 2. Systems and association (frozen)

**Lens systems searched:** every grade A or B row of the key catalogue with `eclipse_effective_einstein_radius` > 0
(14,958 rows). This contains EUC1's samples P (3,192) and S (6,173), the not-quality-cut set U (usable inputs, EUC1's
five validity conditions, any flags; 14,040), and EUC2's three in-window truth lenses.

**Null systems:** every grade X row of the object catalogue (2,580 systems the experts judged not lenses; same parent
selection). X rows have no Einstein radius. Each is given one from sample S: with both lists sorted by identifier, the
i-th X system takes the Einstein radius of S's lens number ⌊i · N_S / N_X⌋.

**Counted objects.** For a system at catalogue position (RA_obj, DEC_obj) with Einstein radius θ_E: every MER object
whose centroid lies within `r_a = min(θ_E + 0.7″, 3.0″)` of that position. The **lens object** is the nearest of them if
it is within 0.6″; a system without one is not evaluable.

**Lens redshift interval [z_lo, z_up]** (used only by the guards):
- a DESI deflector redshift, where the object catalogue has one: z ± 0.01;
- otherwise the union of the ECLIPSE 70 % photo-z interval (where given and > 0) and the Euclid pipeline's 70 % photo-z
  interval of the lens object (`phz_70_int_1`, `phz_70_int_2`). Grade-X systems have only the second.
A system with no interval is not evaluable. Lenses are therefore guarded at least as hard as the null.

**Evaluable system:** has a lens object, an interval, and at least one counted object with a rank-0 galaxy solution whose
spectrum passes Q1 below.

## 3. The rule for a secure source redshift (frozen)

Applied to each spectrum of each counted object, rank-0 solution of the galaxy model only. Values from Le Brun et al.
unless marked.

- **Q1 spectrum:** `spe_npix` ≥ 300 and `spe_n_dith_med` > 3 (their wide-survey high-quality sample);
  `spe_error_flag` = 0 and `spe_gal_error_flag` = 0.
- **Q2 solution:** `spe_z_prob` ≥ 0.99 and `spe_z_rel` > 0.05.
- **Q3 window:** 0.84 < `spe_z` < 1.88.
- **Q4 line:** the `Halpha` row of that solution has `spe_line_qual_gf` in {212, 252} (good or acceptable, red grism),
  `spe_line_flux_gf` ≥ 2.0e-16 erg s⁻¹ cm⁻² (the wide survey's nominal limit), `spe_line_fwhm_gf` ≤ 180 Å (my proxy for
  their velocity-dispersion < 1500 km/s cut; the model table is not at IRSA), and
  `spe_line_snr_gf` ≥ **5** (tier **T5**, primary; their wide-survey flux-validation cut) or ≥ **8** (tier **T8**).
- **G1 above the lens:** `spe_z` ≥ z_up + 0.15.
- **G2 not the deflector's own near-infrared line read as Hα.** With λ_Hα = 6564.61 Å, the solution is rejected if
  `spe_z` lies within 0.01 of the band `(1 + z)·λ/λ_Hα − 1` for z in [z_lo, z_up] and λ any of: [S III] 9533.2;
  He I 10833.3 to Pa γ 10941.1 (one band); Pa β 12821.6. These are the interloper peaks Le Brun et al. report in the
  wide survey. [S III] 9071.1 is not listed: it is 2.4 × weaker than 9533 and in range only when 9533 is, so the fit
  would take the stronger line. A solution failing only G2 is class **AMBIGUOUS-OWN**: reported, never secure.

Not applied, with reasons: their `kron_radius` < 50 and point-like cuts (they remove large foreground galaxies, which is
what a lens object is); `spe_class` = GALAXY (their extended QSO model holds quiescent-galaxy templates, so a deflector
may be classed there; the class is recorded and reported).

**System level.** A system is **SECURE** if at least one counted spectrum is secure and all its secure redshifts agree
within 0.02; z_s is that of the highest Hα S/N. Disagreeing secure redshifts make it **CONFLICT**: excluded, counted.

**Not guarded, stated:** a source at 2.0 < z < 2.78 whose [O III] 5008 is read as Hα gives a redshift too low by a
factor (1 + z) of 0.763. Le Brun et al. find this peak 12 × smaller than the correct one in the wide survey. It biases
`b` upward (against the law). §6 item 4 bounds it.

## 4. Gates on the search (frozen; any failure makes the lane NOT EVALUABLE at that tier)

- **H2 purity null.** The rule, unchanged, on the grade-X systems. With E = number of evaluable systems and n = number
  SECURE: pass if `n_X ≤ max(1, 0.20 · n_S · E_X / E_S)`, lens side = sample S. The null is not signal-free in one
  direction only: chance background emitters and misgraded lenses raise n_X, so the gate can fail wrongly but cannot
  pass wrongly. Every null hit is listed with its photo-z and line values.
- **H4 truth.** EUC2's three confirmed pairs in the window: EUCL-DR1-L015763 (z_s 1.3657), L012826 (1.1374), L014688
  (0.9926). None may be SECURE at a redshift differing by more than 0.02. The number recovered is reported, with the
  first cut that removed each one not recovered. Recovery is not a gate.
- **Tier ladder.** T5 is graded first. If T5 fails H2 or H4, T8 is graded by the same gates and every number is
  labelled "T8 (frozen fallback)". If T8 fails too, the lane word is NOT EVALUABLE. If T5 passes, T8 is a robustness
  row only.
- If the tables carry no usable solutions for lens objects (fewer than 30 % of S or of X evaluable), the word is
  NOT EVALUABLE and nothing is loosened.

## 5. Reading and verdict (frozen)

For every SECURE lens with usable inputs: EUC1's `b` (law S and law B, both footings) with
`M_min = π R_E² Σ_cr(z_l, z_s)`, all lens inputs exactly as EUC1's primary run (catalogue photo-z, Salpeter mass,
effective Einstein radius, measured Sérsic index), using `euc1.py`'s own functions. Beside it the same lenses'
source-free `b` (z_s = 1100). Lenses with z_l ≥ z_s − 0.2 are dropped and counted.

- **Sample P: EUC1-F, exactly as frozen in EUC1 §8**, if N(P) ≥ 10: median `b`, law S, per footing, 95 % bootstrap
  interval (`euc1.stats`: 2,000 resamples, seed 20261112). **LENS GATE HOLDS** if the upper bound ≤ 0.15;
  **LENS GATE FAILS** if the lower bound ≥ 0.25; otherwise **NO VERDICT**. The lane verdict is the pair
  canonical / alt.
- If N(P) < 10: **EARLY READING, NOT A GATE**; the numbers are printed and EUC1-F stays open.
- Sample S and set U (labelled "not quality-cut") are reported beside P and never give the verdict.

**Selection, stated.** Only sources with 0.84 < z_s < 1.88 and Hα above 2e-16 erg s⁻¹ cm⁻² at S/N ≥ 5 can enter:
bright, magnified, star-forming sources. All of them lie below EUC1's break redshift (3.6–4.3), where the law is most
stretched. G1 and G2 close part of the window lens by lens (G2 leaves about 42 % of it open for a typical lens of P). The
reading therefore describes lenses of P with a source in that window; it is a fair per-lens test of the law, and it is
not the median over all of P.

## 6. Robustness (frozen list; reported; cannot change the word)

1. Lens redshift and mass at the DESI deflector redshift where one exists (EUC1's run 4b rescaling).
2. Tier T8 only.
3. Two-line subset: a second line of the same solution ([O III] 5008, Hβ, [S II] 6718, [S III] 9530 or 9068,
   [O II] 3727) with Gaussian-fit S/N ≥ 3 and quality 212 or 252.
4. The [O III] extreme: every secure z_s above 1.29 replaced by (1 + z_s)·6564.61/5008.24 − 1.
5. AMBIGUOUS-OWN lenses added.
6. θ_E ≤ 2.5″.

## 7. Instrument checks (frozen; any failure makes the lane NOT EVALUABLE)

- **K1** EUC1 reproduced: N(P) = 3,192; source-free median `b`, law S, −0.019 / −0.044 to 0.001.
- **K2** EUC2's anchor: EUCL-DR1-L015763 at its DESI deflector redshift and z_s = 1.3657 gives +0.231 / +0.215 to 0.002.
- **K3** association: where ECLIPSE gives a `MER_object_id`, the lens object found by position carries it in ≥ 95 % of
  systems, for S and for X separately.
- **K4** like-for-like apertures: the median association radius of X is within 2 % of S's; evaluable fractions of S
  and X are printed.
- **K5** fetch complete: every counted object id was queried in every table; three fixed id chunks re-queried at the
  end return identical rows.
- **MUTATE twins**, outputs under separate names, each must exit 1:
  `EUC3_MUTATE=newton` (a₀ → 10⁻³⁰): `b` at the true source redshift must rise on both footings, on the reading sample
  and on the K2 anchor.
  `EUC3_MUTATE=noguard` (G1 and G2 removed): the number of SECURE grade-X systems must rise.

## 8. Not claimed

- No measurement of a₀ or κ. No statement about lenses whose sources lie outside the window.
- A HOLDS is not a confirmation of the law: it says the law makes these lenses with at most 1.41 × Salpeter.
- A recovered truth pair validates the redshift, not the rule's purity; H2 does that.
