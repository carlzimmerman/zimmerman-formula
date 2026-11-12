# EUC6R (blind re-grade of EUC6): PROTOCOL

Committed alone, before any EUC6R script exists and before any neighbour count is retrieved. 2026-11-12.

κ = ½ FITTED. Not "theory closed". No outcome may be described as the data favouring the framework. This lane is a
blind re-grade; it does not relabel EUC6.

## 1. What I read, and what I do not

**Read before my numbers are committed:**
- `closure_2026_11_12/EUC6_wide_lens_environment/FROZEN_CRITERIA.md` (the frozen samples, measurement, statistic, words
  and checks);
- `closure_2026_11_12/EUC1_eclipse_saturation_ceiling/FROZEN_CRITERIA.md` (only for what EUC6 inherits: sample S, the
  validity conditions, the cosmology; and §3–§4 so that I can compute the source-free `b∞` myself);
- `_external_data/euclid_dr1_eclipse/README.txt` and `README_eclipse_dr1_catalogue_key_v20261103.md`;
- the directory listing of `closure_2026_11_12/` (names only, to check that EUC6R is free);
- the ESA Euclid archive's `TAP_SCHEMA.columns` rows for `dr1.mer_catalogue_wide_survey` and its `/capabilities`
  document (column names, types and limits; no count of anything).

**Not opened until my script and outputs are committed:** everything else in `EUC6_wide_lens_environment/` (its
`RESULT.md`, scripts, `euc6_rings.json`, `euc6_targets.csv`, every output); every other `EUC*` lane's result or code
(EUC1's outputs included: I compute `b∞` from EUC1's criteria text with my own code); any EUC entry in the project
memory files; `git log`. A sibling hand-over note in the session group's notes folder (`EUC4R_blind_regrade_done.md`)
stays unopened until unblinding.

**Seen by accident before this note (disclosed).** The session context showed the project memory index, whose one-line
entries summarise EUC1 (NO VERDICT / NO VERDICT, lenses at the law's saturation ceiling) and EUC2 / EUC3 (NOT
EVALUABLE). The task brief states EUC4's finding (wide lenses need mass the law cannot supply from their stars) and that
EUC6 "has landed with a verdict" without naming the word. The session context also showed five recent commit subjects
(audits and Milky Way external-field decisions); none mentions EUC6. No EUC6 word, count, median or interval has been
seen.

## 2. Data

ECLIPSE key catalogue and object catalogue, sha256 checked against EUC1's criteria before use (both match:
`65338917…9fa9ab`, `8247a4d5…786b2`). The key catalogue is the source of every lens quantity and of `ra`, `dec`; the
object catalogue supplies `large_system_warning`, joined on the identifier. The largest offset between the two files'
positions is reported.

## 3. How I resolve each ambiguity (fixed here, before any count)

**Sample S.** EUC1 §2 with grades A and B: `lens_grade ∈ {A, B}`, `lens_model_success == True`, `final_sample == True`,
`large_system_warning == False`, `eclipse_effective_einstein_radius > 0`, `eclipse_effective_radius > 0`,
`0.6 ≤ eclipse_sersic_index ≤ 10`, `eclipse_median_phz > 0`, `eclipse_log_survived_mass_med > 0`.

**θ_E** = `eclipse_effective_einstein_radius` (EUC1's `R_E`). **W** = S with θ_E ≥ 1.7″. The criteria say 316 (192 A,
124 B); if my count differs I keep my construction from the text and report the difference, traced at unblinding.

**Matching (C).** Pool = S with θ_E < 1.0″ (strict). `z` = `eclipse_median_phz`, `log M★` =
`eclipse_log_survived_mass_med`, `d² = (Δz/0.05)² + (Δlog M★/0.1)²`. W lenses in identifier order (the identifiers are
fixed-width, so string order is numeric order); each takes the unused pool lens with the smallest `d²`; an exact tie
goes to the lower identifier. "Inside distance² 4" is read as `d² ≤ 4` (equality has measure zero; reported if it
occurs). A W lens whose nearest unused control has `d² > 4` is dropped, consumes no control, and is counted.

**L.** Rows of the key catalogue (all grade A/B) with `large_system_warning == True` and `eclipse_median_phz > 0`
(−99 = no photo-z); no other cut (not `final_sample`, not the lens-model condition, flat-zPDF photo-z kept); the first 40
in identifier order, each counted at its own photo-z.

**R.** The first 60 lenses of W in identifier order (taken from all of W, before any matching or edge drop), at
(`ra`, `dec + 0.30°`), RA unchanged, counted with that W lens's photo-z.

**Cosmology and distances.** Flat ΛCDM, H₀ = 67.74 km/s/Mpc, Ω_m = 0.3089, radiation neglected; comoving distance by
numerical quadrature; `D_A = χ/(1+z)`. Projected radius = proper transverse separation `R = θ D_A(z_l)` with θ the exact
great-circle separation from the target position.

**Annuli.** `N_in`: 30 ≤ R < 300 kpc. `N_bg`: 600 ≤ R < 1000 kpc. Area ratio `(300² − 30²)/(1000² − 600²) =
89,100/640,000 = 0.13922`, flat geometric, no mask correction (no mask information is used). `δ = N_in − 0.13922 N_bg`
(fractional).

**Neighbour cuts, exactly:** `flux_h_templfit > 5.75` (μJy, strict), `spurious_flag == 0`, `det_quality_flag < 4`,
`point_like_prob < 0.7` (strict). A NULL in any of the four columns fails that condition (SQL `WHERE` semantics); the
NULL counts are reported. No other cut: no `vis_det` condition, no tile de-duplication in the primary count. As a
diagnostic, pairs of qualifying objects closer than 0.2″ are counted and a de-duplicated variant is reported (it cannot
change the word).

**Query design (mine, not a binned count).** Per target, one ADQL sync request returning object rows:
`SELECT object_id, right_ascension, declination, flux_h_templfit, spurious_flag, det_quality_flag, point_like_prob,
tile_index FROM dr1.mer_catalogue_wide_survey WHERE 1 = CONTAINS(POINT('ICRS', right_ascension, declination),
CIRCLE('ICRS', ra, dec, r)) AND flux_h_templfit > 5.0`, with `r` = the angle of 1000 kpc at the target's redshift times
1.02. The server applies only a looser flux pre-cut; the flux, flag and radius cuts are applied locally by my code.
`MAXREC` = 1,000,000. Raw responses are kept gzipped under `_external_data/euclid_dr1_mer_cones_euc6r/` (outside git,
`*.csv.gz` is ignored); a manifest with each file's sha256, row count and query is committed. Resumable: a target with
a complete file is not re-queried. One request stream, at least 1.5 s between requests, generic client name
(`tap-client/1.0`), no personal details; on an error or timeout the request is retried after 10, 30, 90 and 270 s,
never in parallel.

**Completeness check of the service (before the run).** One cone at a position that is not a target (0.60° south of
the first lens of S in identifier order, radius 0.15°): rows returned by the row query compared with a server
`COUNT(*)` of the same cone. Used only to show the sync service does not truncate; not used in any statistic.

**Edge rule.** Reference = median `N_bg` over every lens position queried (all of W, the matched controls, and L; R
excluded, being blank fields). A pair is dropped (counted) if either member has `N_bg < 0.4 × reference`; no control is
re-drawn. For the instrument checks the same threshold is applied to each R and L position on its own (my reading:
an off-survey blank field would otherwise bias N1). The reference computed from W ∪ C alone, and the checks without the
edge cut, are reported beside the primary.

**Statistic.** `D_i = δ_W,i − δ_C,i` over surviving pairs (pair order = W identifier order). Bootstrap:
`numpy.random.default_rng(20261112)`, 2,000 resamples of pair indices with replacement
(`rng.integers(0, n, size=(2000, n))`), median of each, interval = 2.5th and 97.5th percentiles (numpy default linear
interpolation). Wilcoxon: `scipy.stats.wilcoxon(D, alternative='greater')` with scipy's defaults
(`zero_method='wilcox'`, `method='auto'`).

**Word, in this order:** NOT EVALUABLE if fewer than 150 pairs survive or N1 or N2 fails; else WIDE LENSES SIT IN RICHER
ENVIRONMENTS if the lower bound > 0 and p < 0.001; else NO RICHER if the upper bound ≤ 3.0; else NO VERDICT. (If the
RICHER and NO RICHER conditions both held, the listed order gives RICHER; the case is reported if it occurs.)

**N1:** |median δ over edge-surviving R| ≤ 2.0. **N2:** median δ(edge-surviving L) − median δ(C in surviving pairs) ≥ 3.0.

**MUTATE** (`EUC6R_MUTATE=shuffle`): per surviving pair, `swap = default_rng(20261113).random(n) < 0.5`; swapped pairs
have `D_i → −D_i`; same bootstrap seed and Wilcoxon; word computed; outputs under separate names (`*_mutate_shuffle.*`);
the script exits 1. The twin passes if its word is not RICHER.

**Reported, no word.** Median δ of W and C (surviving pairs), L, R; fraction of δ_W above the 84th percentile of δ_C;
Spearman ρ of δ with source-free `b∞` inside W and inside W ∪ C (surviving pairs), `b∞` computed by my code from EUC1
§3–§4 (law S, both footings 9.3603e-11 and 1.132e-10 m/s², z_s = 1100, r_max = 10⁶ kpc, Prugniel–Simien with
`p = 1 − 0.6097/n + 0.05463/n²` and the Ciotti–Bertin `b_n`), checked on a point mass (K1); δ_W and D split at the
median photo-z of W in surviving pairs.
