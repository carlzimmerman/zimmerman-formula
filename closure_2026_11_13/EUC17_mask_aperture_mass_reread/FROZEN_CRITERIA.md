# EUC17 (MASK-APERTURE STELLAR MASS, EUCLID LENS ROWS RE-READ): FROZEN CRITERIA

Committed alone, before any mask file is fetched for this lane and before any EUC17 script or number exists.
2026-11-13.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not "theory
closed". A re-read: it adopts nothing, edits no ledger or scorecard, and no outcome is a pass of the lensing gate.

## 0. What this lane is

EUC1 and every lane built on it take the ECLIPSE catalogue's stellar mass (`eclipse_log_survived_mass_med`) as the
**total** mass of an infinite Sérsic body (EUC1 criteria §3: "a spherical Sérsic body of total mass M★").

The catalogue paper (ECLIPSE-D, Nersesian et al.) defines the flux behind that mass differently. Sect. 3.1: the total
lens flux is "the sum of this unconvolved model over all pixels within the circular mask used in the lens modelling".
Sect. 3.2: the SED fit uses "the unconvolved Sérsic model summed within the circular mask". Sect. 6.1: for lenses
whose light extends beyond the mask "this flux is a lower limit on the true total flux" and the stellar masses "may be
underestimated". So the catalogued mass is the mass of the model **inside the modelling circle**, and EUC1's body
holds too few stars at every radius by the factor `f` = the share of the Sérsic model's light inside that circle.

The convention was found by another agent's single-lens work (branch `codex/euclid-desi-handoff-2026-11-13`, commit
dc5b24fe6f, `euclid_for_j0332_followup_2026_11_13/mass_convention/`). The quotations above were read from its cached
page text of the paper. No house lane mentions the convention.

This lane re-reads the Euclid lens rows that are graded on the per-lens boost `b` with that one change, on the same
lenses, with the same thresholds. It is a red-team of a data-side convention behind a failing row (EUC4) and behind
the rows that sit at the lines (EUC1, EUC1-F). The correction can only lower `b` (f ≤ 1), so it can only move a row
toward the law. The guards against a one-way reading are in §6.

## 1. Data (frozen)

**Catalogue files:** EUC1's two files, same sha256 (EUC1 criteria §1).

**Committed per-lens boosts** (read, never recomputed, except in check K2):
- `closure_2026_11_12/EUC1_eclipse_saturation_ceiling/euc1_per_lens.csv` (sample P, source at infinity);
- `closure_2026_11_12/EUC4_wide_lenses/euc4_per_lens.csv` (grade B, source at infinity);
- `closure_2026_11_13/EUC16_better_arc_finder_source_redshifts/euc16_sources.csv` (certified source redshifts);
- `closure_2026_11_12/EUC10_published_source_redshifts/euc10_per_lens.csv` (published source redshifts).

**New download (owner's go, 2026-11-13):** for every lens in the union of those four files, the released modelling
record `https://euclid-eclipse-lenses.org/files/<lens_model_tile_id>/dataset/info.json` (about 134 bytes each:
`pixel_scale`, `mask_radius` in arcsec, `mask_centre`). `lens_model_tile_id` is the key catalogue's column. Fetched
one stream, paced, generic client name, three tries. Raw files stay outside git with a manifest; the lane commits one
table (`euc17_masks.csv`: identifier, tile id, mask radius, mask centre, pixel scale, HTTP status, sha256 of the body).

**No mask.** A lens whose file cannot be fetched, or has no positive `mask_radius`, is "no mask". It is dropped from
the primary statistics and counted. A row with more than 5 % of its lenses in "no mask" is NOT EVALUABLE.

**Seen before freezing (disclosed).** The committed numbers of EUC1, EUC4, EUC10 and EUC16. Two mask files already on
disk from the other agent's work: FOR J0332 (L014994) radius 4.770″ and L015780 radius 6.913″, and its in-mask
fractions for those two lenses (0.804 and 0.587). EUC1's per-lens rows for those two lenses (b = +0.0215 and +0.5304,
law S canonical). No other mask radius has been read and no population number has been computed. Hand estimate, not
verified: f ≈ 0.8 to 0.9 for a typical lens; R1's f₂₅ falls to about 0.08–0.12; R2 stays above 0.25; R3's median
falls to about +0.25 to +0.33 and stays NO VERDICT.

## 2. The correction (frozen)

Per lens, with EUC1's own function (`M2D_frac`, the projected Sérsic share inside a radius):

    f = M2D_frac(mask_radius, eclipse_effective_radius, eclipse_sersic_index)     (both radii in arcsec)

the share of a circular Sérsic model inside a circle of the mask radius centred on the lens. EUC1's body keeps its
shape; its total mass becomes `M★ / f`. Because `b` solves `M_2D,law(<R_E; B M★) = M_min` at fixed shape, the
corrected boost is exactly

    b_corr = b + log₁₀ f

for both laws, both footings and any source redshift. The lane applies this shift to the committed per-lens values.

## 3. Rows, statistics and words (each row keeps its own frozen statistic, lines and words)

Statistics with EUC1's `stats` (2,000 bootstrap resamples, seed 20261112) and EUC1's / EUC4's word rules, imported.

| Row | Lenses | Statistic, law S, per footing | Words (unchanged lines) | Committed |
|---|---|---|---|---|
| **R1** EUC1 | P, source at infinity | f₂₅ = fraction(b > 0.25) | CEILING BROKEN (lower ≥ 0.25) / CEILING HOLDS (upper ≤ 0.10) / NO VERDICT | NO VERDICT / NO VERDICT |
| **R2** EUC4 | W_B: grade B, θ_E ≥ 1.7″, source at infinity | f₂₅ | WIDE LENSES BREAK THE CEILING (lower ≥ 0.25) / NOT CONFIRMED (upper ≤ 0.10) / NO VERDICT; N < 30 NOT EVALUABLE | BREAK / BREAK |
| **R3** EUC1-F as EUC16 graded it | lenses with `in_P` and `class_TB` = SECURE, at their certified source redshift | b_med, N ≥ 10 | LENS GATE HOLDS (upper ≤ 0.15) / LENS GATE FAILS (lower ≥ 0.25) / NO VERDICT; N < 10 NOT EVALUABLE | NO VERDICT / NO VERDICT |

Reported beside them, no word: law B for R1 and R2; f₀ and b_med for R1; EUC4's secondary (1.3″ ≤ θ_E < 1.7″) and
complement (θ_E < 1.0″) bins with EUC4's words labelled secondary; EUC10's reading on its matched lenses with valid
inputs (b_med, f₂₅; its EUC1-F line has N = 2 and stays NOT EVALUABLE whatever happens here); EUC1's alt-footing
conditional readings (z_s = 3, z_s ≈ 2) as would-be words.

**Labels, per row and footing:**
- the row's word under the corrected mass;
- **UNCHANGED** or **CHANGED** against the committed word;
- **FRAGILE** if any bracket of §5 gives a different corrected word, otherwise **ROBUST**.

There is no lane-level word.

**What the labels mean.**
- UNCHANGED on a failing row: the fail survives this correction.
- CHANGED toward the law: a hit that needs a blind re-grade. It is not a pass. CEILING HOLDS and NOT CONFIRMED say only
  that the sample does not exclude "law + stars" with the source at infinity (EUC1 criteria §4); LENS GATE HOLDS would
  rest on 11 lenses and on the premise of §4.
- The 0.25 dex margin and every line stay where their lanes froze them. Nothing is re-tuned.

## 4. Checks (frozen; a failure of K0–K4 makes the lane NOT EVALUABLE)

- **K0 harness.** With f = 1 for every lens the script reproduces every committed statistic of R1, R2, R3 and the
  reported bins: point values to 1e-9, interval bounds to 0.01 (the bootstrap stream position may differ), and every
  committed word.
- **K1 function.** `M2D_frac(R_e, R_e, n) = 0.5` to 1e-6 for n = 1, 4, 8; for n = 1 the share at any radius equals
  `1 − (1 + x) e^{−x}`, x = b₁ R / R_e, to 1e-8 at R / R_e = 0.5, 2, 5.
- **K2 shift identity.** On 20 lenses of P chosen by fixed row index (every ⌊N/20⌋-th with a mask), EUC1's own solver
  run with `M★ / f` returns `b + log₁₀ f` to 1e-6, law S and law B, both footings.
- **K3 geometry.** Every lens with a mask has mask radius > 0 and f in (0, 1]. The count of lenses whose mask radius
  is smaller than the Einstein radius is reported (the formula is still applied).
- **K4 premise spot-check, own code.** On FOR J0332, the one lens whose released model maps are on disk
  (`euclid_for_j0332_fit_2026_11_13/inputs/`): the released unconvolved lens-light map, summed inside the mask circle
  and converted with the tile's zero point, equals the catalogue lens flux of the same band within 3 % in VIS; and
  the analytic infinite Sérsic total from the released model parameters exceeds that catalogue flux by more than
  10 %. If the catalogue flux matches the infinite total better than the in-mask sum, the premise is contradicted.
- **K5 (reported, no threshold).** f for FOR J0332 and L015780 beside the other agent's 0.804 and 0.587 (its values
  use the elliptical model, the model's own centre and the released best-fit shape, so they need not agree closely).
- **Twins**, outputs under separate names, each must exit 1:
  `EUC17_MUTATE=nomask` (f = 1): every committed word comes back;
  `EUC17_MUTATE=invert` (b − log₁₀ f): f₂₅ does not fall in R1 and R2 and b_med does not fall in R3.

**Premise, stated.** The correction rests on the paper's definition and on K4's one lens. This lane does not test it
on other lenses (that needs each lens's released maps, a larger download not asked for here). If the released
catalogue's masses are in fact infinite-profile totals, every corrected number in this lane is void.

## 5. Brackets (frozen list; reported; they set FRAGILE / ROBUST, they do not change the primary word)

1. **F1a** f with `R_e × 0.80`; **F1b** f with `R_e × 1.25` (the circularised / major-axis radius ambiguity of EUC1 §7).
2. **F2** f with n = 4 for every lens.
3. **F3a** mask radius + |mask_centre|; **F3b** mask radius − |mask_centre| (the mask is not centred on the lens; the
   offset of the mask centre from the cutout centre stands in for it).
4. **F4** "no mask" lenses kept with f = 1.
5. **F5** lenses with n > 9.5 dropped (the paper singles them out; their extrapolated wings are the least secure).

## 6. Guards against a one-way red-team (frozen)

- The same rule is applied to every lens of every row, passing or failing, both laws, both footings.
- Brackets F1a, F2 (where n > 4), F3a and F4 shrink the correction; they are reported with the same weight as those
  that enlarge it.
- **S1 plausibility (reported, no word).** The median and 16–84 % range of −log₁₀ f on P, by Einstein-radius class
  (< 1.0″, 1.0–1.3″, 1.3–1.7″, ≥ 1.7″), set beside two numbers already on the record: EUC1's note that the catalogue
  masses are 0.23 dex above the Euclid pipeline's own, and EUC12's finding that the uncorrected ECLIPSE scale already
  agrees with Auger 2009 and DESI CIGALE to about 0.05 dex. A corrected scale that sits well above scales built on
  total magnitudes is a reason to doubt the extrapolated wings, and the RESULT must say so if it happens.
- No row is called a pass. A CHANGED row is recorded as a hit awaiting a blind re-grade (EUC17R, owed if any word
  changes; not launched by this lane).

## 7. Not re-read here (open)

EUC4R, EUC5 / EUC5R (dynamics), EUC6, EUC7, EUC8, EUC12, EUC13 / EUC13R, LNJ1, ESZ1, EXR1 / EXR2. They use the same
catalogue mass as a total; this lane's mask table lets each be re-read later. CJ1's row 39 is not edited by this lane.

## 8. Not claimed

- No measurement of a₀ or κ. No statement that the catalogue is wrong: it reports what its paper says it reports.
- No statement about stars beyond the mask: `M★ / f` is EUC1's own infinite body normalised to the catalogued
  in-mask mass, an extrapolation of the fitted model, not a measurement of outer light.
- No pass of the lensing gate under any outcome.
