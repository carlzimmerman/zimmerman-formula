# EUC17R (BLIND RE-GRADE OF EUC17): READING OF THE FROZEN CRITERIA AND AMENDMENT A1

2026-11-14. Written and committed alone, before any EUC17R script exists and before any in-mask fraction, corrected
boost, statistic or check value has been computed by this session. κ = ½ FITTED. Footings 9.3603e-11 (canonical) /
1.132e-10 (alt) m/s², graded separately, never pooled. Not "theory closed". A re-grade adopts nothing and edits no
README, ledger or scorecard.

## 0. What this session read, and what it has seen that it should not have

**Read:** `../EUC17_mask_aperture_mass_reread/FROZEN_CRITERIA.md` (commit 8b31c449c9 per A1), `AMENDMENT_A1.md`, and
the data table `euc17_masks.csv` (first rows and the distribution of one centre column only; no radius statistic). The
source lanes' frozen criteria and code (EUC1, EUC4, EUC10, EUC16); their committed per-lens files; their committed
result JSON files (needed for check K0, which compares against them: EUC16's P reading b_med +0.405 / +0.385 with its
bounds, EUC10's "all matched with valid inputs" reading and its N = 2 EUC1-F line). The FOR J0332 released inputs
(file list, FITS headers, `info.json`, `coolest*.json`, the VIS row of the portal record's magnitudes). The two
catalogue files are those of EUC1 (hashes checked by EUC1's own `load`).

**Blindness check.** The recent-commit list shown at session start held no subject beginning with `EUC17`. The check
in the brief passes.

**Leaks, disclosed in full (no file of the lead's EUC17 output was opened):**
1. The project's memory index is loaded automatically into every session's context at start. Two of its lines name
   this lane. Quoted exactly:
   - "11-13 EUC17 (owner "Yes, freeze it"; origin b778402add): Euclid lens catalogue stellar masses count only light i…"
     (truncated in the index; it restates the lane's premise).
   - "Re-read lanes: per-lens CSVs hold 4 decimals and bootstrap bounds of a fraction step by 1/N; open the files before
     freezing harness tolerances (EUC17 voided itself as frozen)".
   The second line says the lead's as-frozen reading was voided by a harness-tolerance check. It names no row label,
   no number and no corrected word. It is result information and it reached this session before any work began.
2. `ls` of the EUC17 folder (to see which files exist) showed these names, none opened: `AMENDMENT_A2.md`,
   `RESULT.md`, `euc17.py`, `euc17_fetch.py`, `euc17_posthoc_T.py` (+ `.out`, `.json`), `euc17_A2.out`,
   `euc17_A2_results.json`, `euc17_MUTATE_invert*`, `euc17_MUTATE_nomask*`, `euc17_results.json`,
   `euc17_per_lens.csv`. The names say that an amendment A2 and a post hoc computation called "T" exist.

Every choice below was written after these leaks. Where a choice touches the bootstrap stream (§3), it is flagged.

## 1. The correction, read

Per lens with a mask: `f = euc1.M2D_frac(mask_radius_arcsec, eclipse_effective_radius, eclipse_sersic_index)`, both
radii in arcsec, EUC1's own function (its `b_ser` constant, circular projected Sérsic share). Corrected boost
`b_corr = b + log₁₀ f`, applied to law S and law B, both footings, every source redshift. Nothing else changes.

**Mask table.** A lens has a mask when its row in `euc17_masks.csv` has `http_status` 200, `has_mask` 1 and a finite
`mask_radius_arcsec` > 0. A lens of any row that has no line in the table is "no mask" exactly as a failed fetch is
(the criteria define "no mask" by the absence of a usable file; the table is the lane's record of the fetch).
`mask_centre_0`, `mask_centre_1` are read as arcsec offsets of the mask centre from the cutout centre (the
values are multiples of half a 0.1″ pixel, and `info.json` for FOR J0332 carries the same pair beside `mask_radius`
in arcsec); `|mask_centre| = √(c₀² + c₁²)`.

**"No mask" rule.** Counted per row and per reported bin, on that row's own lenses. More than 5 % of a row's lenses
in "no mask" makes that row (or reported bin) NOT EVALUABLE; the other rows are unaffected. Lenses with a mask are the
row's corrected sample.

## 2. Rows and inputs

- **R1 (EUC1, sample P, source at infinity).** Per A1 change 1, `b` recomputed at full precision with EUC1's imported
  `load`, `select(rows, ("A",))`, `build`, `Engine.solve_b`, `Mmin = π R_E² Σ_cr(z_l, 1100)`, laws S and B, both
  footings. Word on law S, EUC1's `word`. Reported beside it: law B, f₀, b_med.
- **R2 (EUC4, W_B).** Grade B, EUC1's cuts, `eclipse_effective_einstein_radius ≥ 1.7″`, recomputed the same way. Word
  on law S, EUC4's `word` (N < 30 → NOT EVALUABLE). Reported: law B, the secondary bin (1.3 ≤ θ_E < 1.7″) and the
  complement bin (θ_E < 1.0″) with EUC4's words labelled secondary.
- **R3 (EUC1-F as EUC16 graded it).** The rows of `euc16_sources.csv` with `in_P` True and `class_TB` SECURE (EUC16's
  reading tier was TB), at their certified source redshift: per A1 change 2, the committed columns `b_S_canonical`,
  `b_S_alt` are used, not recomputed. Statistic b_med (law S), EUC16's words (upper ≤ 0.15 HOLDS, lower ≥ 0.25
  FAILS), N < 10 NOT EVALUABLE.
- **EUC10 reading (reported, no word).** The 11 lenses of `euc10_per_lens.csv` that carry `b_S_canonical`/`b_S_alt`
  (EUC10's "all matched with valid inputs, law S" reading): b_med and f₂₅ from the committed columns (A1 change 2).
  Its EUC1-F line (the two lenses of P among them, L015871 and L016382) is reported and stays NOT EVALUABLE (N = 2).
- **EUC1's conditional readings (reported, would-be words).** Alt footing, law S, from the committed per-lens columns
  `b_S_alt_R3` (z_s = 3) and `b_S_alt_R2` (z_s = max(2, z_l + 0.5)); blank / NaN entries are EUC1's dropped lenses.
  To avoid a clash with the row names they are called **C3** and **C2** here. Would-be words with EUC1's `word`.

## 3. Statistics and the bootstrap stream (a choice; flagged)

All statistics use EUC1's `stats` (2,000 resamples, seed 20261112) and the source lanes' word functions, imported.
The criteria fix the function and the seed but not the position in the random stream ("the bootstrap stream position
may differ"). **This re-grade calls `stats` in the same sequence and with the same lens order as the lane that
committed each number**, so that with f = 1 the harness repeats the committed computation exactly:
- R1, C3, C2: one generator `default_rng(20261112)` shared, in EUC1's order: primary S-canonical, S-alt, B-canonical,
  B-alt; then z_s = 3 S-canonical, S-alt, B-canonical, B-alt; then z_s ≈ 2 the same four. Calls whose values are not
  committed per lens (the z_s = 3 and z_s ≈ 2 canonical and law-B calls) are made on placeholder arrays of the right
  length: only their consumption of the stream matters, and it depends only on N.
- R2 and its bins: one generator shared, in EUC4's order: W_B (S-can, S-alt, B-can, B-alt), secondary (same four),
  complement (same four).
- R3 and the EUC10 reading: a fresh `default_rng(20261112)` per statistic (as EUC16 and EUC10 called it), lenses in
  key-catalogue row order (the order in which EUC16's and EUC10's samples were built).
- The corrected run, the brackets and the twins repeat the same sequences on their own lens sets.

Flag: this choice was made after leak 1 above, which says the lead's as-frozen reading was voided by a harness
tolerance and that bootstrap bounds of a fraction step by 1/N. I would make the same choice without the leak (a
reproduction harness should repeat the computation it reproduces), but the reader should know the leak came first.
**The script also reports K0 under the other natural reading (a fresh generator for every statistic, lenses in the
same order).** The K0 that sets this re-grade's as-frozen word is the one under the mirrored stream; if the other
reading would fail where the mirrored one passes, both are stated in RESULT_BLIND.md's first paragraph, and the
as-frozen word is given under each.

## 4. Checks

- **K0 harness (f = 1, every lens kept, no lens dropped).** R1, R2 and its bins: every committed key of every
  committed statistic (N, f25, f0, b_med and their _lo/_hi) against `euc1_results.json` (primary, conditional) and
  `euc4_results.json` (partA): N exact, point values to 1e-9, bounds to 0.01, every committed word. R3 and the EUC10
  reading, and C3/C2 (A1 change 2): N exact, b_med to 1e-4, fractions to 1/N, bounds to 0.01, words as committed.
- **K0b.** Recomputed per-lens b against the committed four-decimal values to 6e-5, every lens: R1 against
  `euc1_per_lens.csv` (S and B, both footings); R2 against the grade-B rows of `euc4_per_lens.csv` (law S, both
  footings; the file holds no law B). The bins have no committed per-lens file and are covered by K0 only.
- **K1.** `M2D_frac(R_e, R_e, n) = 0.5` to 1e-6 for n = 1, 4, 8. Second part: `x = b₁ R/R_e` with **b₁ = the constant
  EUC1's function itself uses for n = 1** (`b_ser(1)`), to 1e-8 at R/R_e = 0.5, 2, 5. Reason: the first part is where
  the value of b_n is tested (to 1e-6); the second tests the functional form, and a 1e-8 tolerance on the form only
  makes sense with the function's own constant. The same comparison with the exact b₁ (root of γ(2, b) = ½) is
  printed beside it, no threshold.
- **K2.** Lenses of P with a mask, in P order; N = their count; indices 0, ⌊N/20⌋, 2⌊N/20⌋, … (first 20). EUC1's
  `build` with `lm − log₁₀ f` and `solve_b` (source at 1100), laws S and B, both footings, against `b + log₁₀ f` from
  the full-precision run: max |difference| ≤ 1e-6.
- **K3.** Every lens with a mask (all rows together): radius > 0 and f in (0, 1]. Count with mask radius < θ_E
  (`eclipse_effective_einstein_radius`) reported, per row and overall.
- **K4 (FOR J0332, L014994, own code).** Inputs only from `euclid_for_j0332_fit_2026_11_13/inputs/`.
  - Map: `results/pre_psf.fits`, HDU `VIS_GALAXY_0` (the unconvolved model of galaxy_0; in the released COOLEST files
    galaxy_0 carries the SIE mass and is the lens, galaxy_1 is the source). Its units are taken as the VIS cutout's
    (`VIS_BGSUB`: BUNIT ADU/s, MAGZERO 24.5 AB).
  - Catalogue flux (A1 change 3): `lens_flux_max_lh` of the VIS row of `results/magnitudes.csv`, read as μJy
    (AB: m = 23.9 − 2.5 log₁₀ F). `lens_flux` (median) printed beside it. Conversion: F[μJy] = S[ADU/s] ×
    10^(−0.4 (24.5 − 23.9)). If this unit reading is wrong the check fails by a large factor; that is reported as a
    failure, not repaired.
  - Mask circle: radius `mask_radius` and centre `mask_centre` from `dataset/info.json`, read as (y, x) arcsec in the
    modelling software's convention; a pixel is inside when its centre is within the radius; pixel centres on the
    100 × 100, 0.1″ grid centred on the cutout centre. The sign of the row axis is fixed by one rule: the orientation
    in which the map's brightest pixel falls on the same side as the catalogue's `lens_light_centre_0` (the y offset
    of the lens light). The sum under the other orientation is printed beside it.
  - Test (a): |in-mask sum (μJy) / lens_flux_max_lh − 1| ≤ 0.03.
  - Test (b): the analytic infinite Sérsic total from `results/coolest_sersic.json` galaxy_0 light (I_eff, θ_eff, n,
    q; EUC1's `b_ser`): `T = 2π I_eff θ_eff² n e^{b} b^{−2n} Γ(2n) × J`, divided by the pixel area when I_eff is per
    pixel. The two conventions the file does not state (J = 1 for an intermediate-axis radius or J = q for a
    major-axis radius; I_eff per pixel or per arcsec²) are fixed by one rule: the combination whose analytic in-mask
    sum, evaluated on the same pixel centres with the same orientation, best matches the released map's in-mask sum
    (closest ratio to 1 in log). That match ratio is printed. Pass if T (converted to μJy) > 1.10 × lens_flux_max_lh.
  - Contradiction clause: if |T/F_cat − 1| < |sum/F_cat − 1|, the premise is contradicted (reported as such).
- **K5 (no threshold).** f for L014994 and L015780 beside 0.804 and 0.587.
- **Twins**, outputs under separate names, each must exit 1 (exit 2 otherwise):
  - `EUC17R_MUTATE=nomask`: f = 1 for every lens, all lenses kept; exit 1 if every committed word (R1, R2, R3 per
    footing; and the committed words of R1/R2 law B, the R2 bins and C3/C2) comes back.
  - `EUC17R_MUTATE=invert`: `b − log₁₀ f` on the lenses with a mask; exit 1 if, per footing, law S, f₂₅ of R1 and of
    R2 is not below its committed value and b_med of R3 is not below its committed value. The same comparison against
    the f = 1 values on the same lens set is printed beside it.

A failure of K0 (as defined in §3), K0b, K1, K2, K3 or K4 makes the lane NOT EVALUABLE. The corrected numbers are then
still printed, labelled would-be.

## 5. Brackets (set FRAGILE / ROBUST; never the primary word)

Each bracket changes only f (or the lens set) and re-runs every row with its own stream sequence (§3):
F1a f with R_e × 0.80; F1b f with R_e × 1.25; F2 f with n = 4 for every lens; F3a f with mask radius + |mask_centre|;
F3b f with mask radius − |mask_centre| (a non-positive radius would make that lens "no mask" in that bracket; none is
expected); F4 the "no mask" lenses kept with f = 1; F5 lenses with catalogue n > 9.5 dropped. The body b itself is
never changed by a bracket (only the share f): the brackets are about how much of the model sits inside the circle.
FRAGILE if any bracket's corrected word differs from the primary corrected word of that row and footing; a bracket
in which a row is NOT EVALUABLE (no-mask share or N rule) counts as a different word.

## 6. Labels

Per row (R1, R2, R3) and footing: the corrected word; UNCHANGED or CHANGED against the committed word (R1 NO VERDICT /
NO VERDICT; R2 WIDE LENSES BREAK THE CEILING / same; R3 NO VERDICT / NO VERDICT); FRAGILE or ROBUST. CHANGED toward the
law is a hit awaiting a blind re-grade, never a pass. No lane-level word.

## 7. S1 plausibility (reported)

Median and 16–84 % range of −log₁₀ f on the lenses of P with a mask, by θ_E class (< 1.0, 1.0–1.3, 1.3–1.7, ≥ 1.7″),
beside EUC1's 0.23 dex (catalogue above the pipeline's masses) and EUC12's ≈ 0.05 dex agreement with Auger 2009 and
DESI CIGALE. "Well above" is read as: the median −log₁₀ f on P exceeds 0.05 dex, so the corrected scale would sit
above the total-magnitude scales by more than their present agreement; RESULT_BLIND.md then says so.

## 8. Files this session will write

`euc17r.py`; `euc17r.out`, `euc17r_results.json`, `euc17r_f.csv` (per lens: identifier, rows, mask radius, θ_E, f);
twins `euc17r_MUTATE_nomask.{out,json}`, `euc17r_MUTATE_invert.{out,json}`; `RESULT_BLIND.md`; then, after it is
committed, the comparison with the lead (`RECONCILE.md`).
