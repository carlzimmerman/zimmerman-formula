# EUC6 (WIDE-LENS ENVIRONMENT): RESULT

2026-11-12. Criteria 62dbaa183b (committed alone, before any script or neighbour count).

## Verdict: WIDE LENSES SIT IN RICHER ENVIRONMENTS

At the same redshift and stellar mass, Euclid's wide-separation lenses (θ_E ≥ 1.7″) have more neighbours than
small-separation lenses (θ_E < 1.0″): the paired difference in richness is **+3.38 [+2.28, +4.62] galaxies** (median,
243 pairs), Wilcoxon one-sided p = 1.1e-6. Both frozen conditions are met (lower bound above zero; p < 0.001). Both
instrument checks pass and the mutation twin exits 1.

The excess mass EUC4 found in wide lenses tracks environment. By the frozen reading, this places that residual with
the group / cluster rows the framework already carries, not with the galaxy law.

κ = ½ FITTED. No outcome favours the framework.

## 1. Numbers

Richness = galaxies brighter than H_E = 22 at 30–300 kpc, minus the local background from 600–1000 kpc.

| Sample | N | median richness | 16–84 % | mean |
|---|---|---|---|---|
| Wide lenses W (θ_E ≥ 1.7″) | 243 | +6.12 | −0.37 to +14.24 | +7.26 |
| Matched controls C (θ_E < 1.0″) | 243 | +2.84 | −3.59 to +10.71 | +3.62 |
| Expert-flagged group-scale systems L | 40 | +10.73 | +4.58 to +21.83 | +13.76 |
| Blank fields R | 58 | +0.11 | −6.46 to +6.16 | 0.00 |

Paired difference W − C: median +3.38 [+2.28, +4.62], mean +3.64, p = 1.06e-6. 28.8 % of wide lenses lie above the
controls' 84th percentile (16 % if alike). The difference is the same at low and high redshift (+3.47 below z = 0.52,
+3.32 above).

Match quality: median |Δz| = 0.010, median |Δ log M★| = 0.029. W: z 0.52, log M★ 11.66, θ_E 1.97″. C: z 0.54,
log M★ 11.62, θ_E 0.88″. Of 316 wide lenses, 67 had no control inside the frozen matching distance and 6 pairs were
dropped for low background coverage.

## 2. Checks

| Check | Result |
|---|---|
| N1 blank fields, median richness within ±2.0 | +0.11 (pass) |
| N2 flagged group-scale systems exceed the controls by ≥ 3.0 | +10.73 against +2.84, difference +7.89 (pass) |
| MUTATE shuffle (labels swapped at random inside pairs) | median +0.94 [−1.84, +1.94], p = 0.24: NO RICHER; exit 1 |

## 3. Reported (no word)

- **Inside the wide class richness does not track the size of the excess:** Spearman correlation of richness with the
  source-free boost `b∞` is 0.07 (p = 0.29). Across W and C together it is 0.23 (p = 2e-7), which is the class
  difference again. One lens's richness carries about ±7 galaxies of noise, against a class difference of 3.
- **A catalogue-only cross-check (post hoc, computed from the experts' lens-model labels):** the fraction of grade A/B
  lenses labelled "Multi Galaxy Lens" rises with Einstein radius: 2.9 % below 0.8″, 2.6 % at 0.8–1.0″, 3.8 % at
  1.0–1.3″, 6.5 % at 1.3–1.7″, 10.4 % at 1.7–2.5″, 24 % above 2.5″. Those systems are excluded from every sample here
  (they have no successful single-galaxy model); the trend points the same way.

## 4. What this says

1. **The wide-lens residual is environmental, on average.** Wide lenses have about twice the neighbour excess of
   matched small-separation lenses, and sit about halfway to the systems the Euclid experts flagged as group-scale.
2. **It is a statement about the class, not about each lens.** Seven in ten wide lenses fall inside the controls'
   range. The measure is noisy per lens, so this does not show that those lenses are isolated; it shows the proxy
   cannot place them one by one.
3. **For the framework.** EUC4: law plus stars cannot make wide lenses; group gas under the law cannot either. EUC5's
   reading: their stars feel the extra mass. EUC7: a different kernel does not remove it. EUC6: they live in richer
   places. Together these put the wide-lens residual with the cluster-type residual: gravitating density beyond the
   law, hosted by groups, concentrated enough to act inside 4–12 kpc of the central galaxy. The framework has no
   constructed state for that component; this is its smallest-scale data row so far.
4. **It does not show the law holds in isolated galaxies.** The controls here are lenses below 1″, whose own gate
   (EUC1-F) is still open.
5. **A count of neighbours is a proxy.** It is not a halo mass or a group catalogue, and photometric redshifts were
   not used (a join to the photo-z table timed out at the archive; the local background does that job statistically).

## 5. Files

`euc6_fetch.py` (ESA Euclid archive TAP, `dr1.mer_catalogue_wide_survey`, one binned-count query per target, paced),
`euc6_targets.csv` (the samples), `euc6_rings.json` (counts in 10 kpc rings to 1000 kpc for all 598 targets),
`euc6.py`, `euc6.out`, `euc6_results.json`, `euc6_per_target.csv`, `euc6_MUTATE_shuffle.out` / `_results.json` (exit 1).
