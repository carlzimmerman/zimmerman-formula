# EUC6 (WIDE-LENS ENVIRONMENT): FROZEN CRITERIA

Committed alone, before any EUC6 script exists and before any neighbour count around a lens is retrieved. 2026-11-12.
Owner, 2026-11-12: "keep swinging".

κ = ½ FITTED. Not "theory closed". No outcome may be described as the data favouring the framework.

## 0. The question

EUC4 (3ef9630a69): Euclid's wide-separation lenses (θ_E ≥ 1.7″) need mass the law cannot supply from the lens galaxy's
stars, for any source redshift. EUC5's reading: their stars feel it too. Two very different things could be true:

- **the excess is environmental**: wide lenses are central galaxies of groups, and this is the cluster-type residual
  the framework already carries, reaching down to groups;
- **the excess is intrinsic**: wide lenses are as isolated as other massive lens galaxies, and the law fails for
  single massive galaxies.

The catalogue has no environment measure. Euclid's own source catalogue does: count the neighbours.

## 1. Samples (frozen)

- **W**: every lens of EUC1's sample S with θ_E ≥ 1.7″ (the 316 lenses of EUC4's Part B: 192 grade A, 124 grade B).
- **C**: one control per W lens, drawn from the lenses of S with θ_E < 1.0″, the nearest in
  `(Δz_l / 0.05)² + (Δ log M★ / 0.1)²`, without replacement, W lenses taken in identifier order. A W lens with no control
  inside distance² 4 is dropped with its pair (counted).
- **Positive control L**: the first 40 grade-A/B lenses in identifier order with `large_system_warning = True` and a
  photo-z (the expert-flagged group / cluster-scale systems, excluded from S).
- **Blank fields R**: 60 positions, the first 60 W lenses shifted by +0.30° in declination, counted at that lens's redshift.

## 2. Measurement (frozen)

Euclid DR1 MER catalogue, ESA archive TAP (`dr1.mer_catalogue_wide_survey`), anonymous, paced. A neighbour is an object
with `flux_h_templfit > 5.75` μJy (H_E < 22.0), `spurious_flag = 0`, `det_quality_flag < 4`, `point_like_prob < 0.7`.

At the lens's catalogue photo-z, in the catalogue's cosmology:
- `N_in` = neighbours at projected 30–300 kpc (the inner 30 kpc holds the lens, the arcs and their fragments);
- `N_bg` = neighbours at 600–1000 kpc;
- **richness `δ = N_in − N_bg × (area_in / area_bg)`**.

A pair is dropped (counted) if either member has `N_bg` below 40 % of the median `N_bg` of all lenses queried (survey
edge or mask).

**Seen before freezing (disclosed).** The table's columns; one test cone at a blank position 0.3° from a lens (181
objects brighter than H_E = 22 within 1.5′, about 26 per arcmin²), used only to time the service and size the noise.
No count around any lens.

## 3. Statistic and words (frozen)

Paired difference `D_i = δ_W,i − δ_C,i`. Median `D` with a 95 % bootstrap interval over pairs (2,000 resamples, seed
20261112), and the one-sided Wilcoxon signed-rank p-value for `D > 0`.

- **WIDE LENSES SIT IN RICHER ENVIRONMENTS** if the lower bound of the median `D` > 0 and p < 0.001;
- **NO RICHER** if the upper bound of the median `D` ≤ 3.0 galaxies;
- **NO VERDICT** otherwise;
- **NOT EVALUABLE** if fewer than 150 pairs survive or an instrument check fails.

The 3.0 line: a group around a galaxy of this mass adds five to twenty neighbours brighter than H_E = 22 inside 300 kpc
at z < 0.7; the pair noise is about 11 galaxies, so 316 pairs resolve a median difference of about ±1.6.

**Reported, no word:** median `δ` of W, C, L and R; the fraction of W above C's 84th percentile; Spearman correlation of
`δ` with EUC1's source-free `b∞` inside W and inside W ∪ C; `δ` of W split at its median redshift.

## 4. Instrument checks (frozen)

- **N1 blank fields:** |median `δ` of R| ≤ 2.0 galaxies (the background subtraction is unbiased).
- **N2 positive control:** median `δ` of L exceeds median `δ` of C by at least 3.0 galaxies (the measure sees groups).
- **MUTATE** (`EUC6_MUTATE=shuffle`): with the W / C label of each pair assigned at random (seed 20261113) the word must
  not be WIDE LENSES SIT IN RICHER ENVIRONMENTS; exit 1; separate outputs.

## 5. What the words mean

- RICHER: at fixed stellar mass and redshift, wide lenses have more neighbours than small-separation lenses. The excess
  mass tracks environment. For the framework this places EUC4's residual with the group / cluster rows, not with the
  galaxy law. It does not show the law is right in isolated galaxies.
- NO RICHER: wide lenses are no richer than their controls by more than three galaxies. Then the excess is not explained
  by group membership as this measure sees it, and EUC4 reads as a failure for single massive galaxies.
- Both: a count of neighbours is a proxy. It is not a halo mass and not a group catalogue.
