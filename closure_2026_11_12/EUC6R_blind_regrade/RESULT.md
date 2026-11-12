# EUC6R: blind re-grade of EUC6 (wide-lens environment); does not relabel EUC6

2026-11-12. Protocol fb8e35b2f7 (committed alone, before any script or count). Own script, own queries and outputs
9155c8da36 (committed before EUC6's result was opened). This file was written after unblinding.

κ = ½ FITTED. Not "theory closed". No outcome favours the framework.

## Word: WIDE LENSES SIT IN RICHER ENVIRONMENTS (same as EUC6)

Paired difference in richness, wide minus control: **median +3.59 [+2.28, +4.70] galaxies, 242 pairs, one-sided
Wilcoxon p = 6.7e-7**. EUC6: +3.38 [+2.28, +4.62], 243 pairs, p = 1.06e-6. The medians differ by +0.21 galaxies; the
lower bounds are identical; the upper bounds differ by +0.08. N1 and N2 pass; the label-shuffle twin returns NO RICHER
and exits 1.

The difference has one cause, traced target by target (§3). The archive stores missing values as NaN, not NULL.
PostgreSQL ranks NaN above every number, so EUC6's server-side `flux_h_templfit > 5.75` counted objects with no H-band
flux. My protocol's local cut drops them. With EUC6's NaN handling, my rows reproduce EUC6's ring counts for every one
of the 598 targets the two lanes share (115,194 objects each), and every EUC6 number to all printed digits.

## 1. My numbers

Richness δ = N(30–300 kpc) − 0.13922 × N(600–1000 kpc), neighbours with `flux_h_templfit > 5.75`, `spurious_flag = 0`,
`det_quality_flag < 4`, `point_like_prob < 0.7`, a missing (NaN) value failing its cut.

| Sample | N used | median δ |
|---|---|---|
| Wide lenses W (θ_E ≥ 1.7″), in surviving pairs | 242 | +6.31 |
| Matched controls C (θ_E < 1.0″) | 242 | +2.92 |
| Expert-flagged large systems L | 40 of 40 | +11.81 |
| Blank fields R | 56 of 60 | +0.11 |

- **Samples.** S = 6,173 (26 removed for Sérsic n outside 0.6–10). W = 316 (192 A, 124 B), as the criteria state.
  Control pool 3,993. 249 pairs matched (67 W lenses had no control at d² ≤ 4; no exact ties; no d² = 4; largest
  kept d² 3.89). Edge reference: median N_bg 135 over all 605 lens positions queried (316 W, 249 C, 40 L), threshold
  54; 7 pairs dropped.
- **Statistic.** Median D +3.59, 95 % bootstrap [+2.28, +4.70], mean +3.54, p = 6.74e-7. RICHER condition met, NO
  RICHER condition not met.
- **N1:** median δ(R) = +0.11 (56 fields above the edge threshold; +0.00 with all 60). Pass.
- **N2:** median δ(L) − median δ(C) = 11.81 − 2.92 = +8.89. Pass.
- **MUTATE (shuffle, seed 20261113):** 121 of 242 pairs swapped; median +0.09 [−2.21, +1.82], p = 0.50: NO RICHER;
  exit 1. Pass.
- **Reported, no word.** 29.8 % of W above C's 84th percentile (+10.50). Split at W's median photo-z 0.52: below,
  125 pairs, δ_W +7.39, D +3.75; above, 117 pairs, δ_W +5.57, D +3.56. Spearman of δ with source-free `b∞` (law S, my
  code from EUC1 §3–§4): inside W 0.120 (p = 0.062) canonical, 0.118 (p = 0.066) alt; across W ∪ C 0.251 / 0.250
  (p ≈ 2e-8). Median `b∞`: W +0.378 / +0.355, C −0.211 / −0.236 dex.
- **Robustness (cannot change the word):** edge reference from W ∪ C only: same 242 pairs and numbers. No edge cut:
  249 pairs, +3.75 [+2.33, +4.71]. Merging qualifying objects closer than 0.2″ (5 objects in all): unchanged. W grade A
  only: 142 pairs, +3.84 [+1.91, +5.80], p = 1.3e-5 (fewer than 150 pairs, so NOT EVALUABLE by the frozen floor if it
  were the sample). PostgreSQL NaN handling (added after I found the NaN values; disclosed in the script): 243 pairs,
  +3.38 [+2.28, +4.62], p = 1.06e-6, the same word.

## 2. Comparison with EUC6

| | EUC6R (mine) | EUC6 | Difference traced to |
|---|---|---|---|
| Pairs kept | 242 | 243 | NaN rule (pair 128's control has no H flux) |
| Median δ W / C | +6.31 / +2.92 | +6.12 / +2.84 | NaN rule |
| Median δ L / R | +11.81 / +0.11 | +10.73 / +0.11 | NaN rule (L002198) |
| R fields used in N1 | 56 | 58 | NaN rule (L000948, L001132) |
| Median D | **+3.59** | **+3.38** | NaN rule |
| 95 % interval | **[+2.28, +4.70]** | **[+2.28, +4.62]** | NaN rule |
| Wilcoxon p | 6.7e-7 | 1.06e-6 | NaN rule |
| Mean D | +3.54 | +3.64 | NaN rule |
| W above C's 84th pct | 29.8 % | 28.8 % | NaN rule |
| Spearman δ–b∞ inside W (alt) | 0.118 (p 0.066) | 0.069 (p 0.29) | NaN rule only; `b∞` codes agree to 1.1e-4 dex |
| Spearman across W ∪ C (alt) | 0.250 | 0.233 | NaN rule |
| N2 (L − C) | +8.89 | +7.89 | NaN rule |
| MUTATE | +0.09 [−2.21, +1.82], NO RICHER | +0.94 [−1.84, +1.94], NO RICHER | same draw on different D (n and counts) |
| Word | RICHER | RICHER | none |

## 3. Traced causes

1. **The instrument agrees object for object.** EUC6 sent one server-side binned count per target: 10 kpc rings, its
   four cuts in the `WHERE`. I fetched object rows in a cone with only a looser flux pre-cut (> 5.0 μJy) and applied
   the cuts locally. Counting a NaN flux as passing reproduces EUC6's N_in and N_bg exactly for all 598 shared
   targets. Same positions (key and object catalogues agree to 0.0″), same proper-kpc annuli, same great-circle
   distances.
2. **NaN, not NULL, and PostgreSQL's ordering.** At the non-target test cone: `flux_h_templfit IS NULL` 0,
   `flux_h_templfit > 1e9` 517, `point_like_prob > 2` 6,735 (`euc6r_nan_and_density.json`). A server-side
   `flux_h_templfit > 5.75` therefore keeps objects with no H flux, and `point_like_prob < 0.7` drops those with no
   probability. EUC6 counted 3,726 such objects (3.2 % of 115,194) over 35 targets. They gather in patches without
   H-band flux, where VIS detections with no H measurement pass:
   - the control in pair 128 (L007170): 0 / 0 by my rule, 257 / 1,569 in EUC6, δ_C = +38.6;
   - W lens L000324 (pair 6): 15 / 126 by my rule, 120 / 383 in EUC6, δ_W = +66.7 in EUC6 against −2.5 here;
   - blank fields L000948 and L001132: N_bg 0 and 1 by my rule (edge-dropped), 149 and 80 in EUC6 (kept);
   - large system L002198: N_bg 76 by my rule, 224 in EUC6 (δ +13.4 against −7.2).

   Such objects are not "H_E < 22.0" galaxies, which is what the criteria define, so EUC6's count is contaminated
   there. My count leaves holes there instead: partly unmeasured annuli, caught by the edge rule only when severe. On
   average they add more to controls than to wide lenses (mean extra objects at 30–300 kpc: C 1.12, W 0.42), which is
   why EUC6's median D is 0.21 lower. Post hoc, both rules agree once the gaps are removed. Excluding every pair with a
   member whose annulus count is more than 5 % NaN-flux leaves 227 pairs: +3.49 [+2.28, +4.62] by my rule, +3.47
   [+2.28, +4.66] by EUC6's, both RICHER (`euc6r_trace_decomposition.json`).
3. **Edge reference set.** EUC6 queried only the matched W lenses: median 133 over 538 positions. I queried all 316:
   median 135 over 605. On my counts, EUC6's reference keeps one more pair (L001481, control N_bg 53, between the
   thresholds 52.6 and 54): 243 pairs, +3.62 [+2.33, +4.71]. On EUC6's counts the reference changes nothing.
4. **Matching.** EUC6 keeps d² < 4, I keep d² ≤ 4. No pair sits at 4, and the 249 pairs are identical.
5. **Bootstrap.** EUC6 draws 2,000 sequential `integers(0, n, n)`; I draw one (2000, n) array from the same seed. That
   is the same stream: on EUC6's counts my code returns EUC6's interval to every printed digit.
6. **`b∞`.** My Prugniel–Simien and projection code agrees with EUC1's `Engine.solve_b` to 1.1e-4 dex per lens. The
   difference is the solar mass constant: 1.98892e30 here, 1.98847e30 in EUC1. With the same counts, both codes give
   the same Spearman ρ, so the gap in ρ inside W comes from the counts alone.
7. **Disclosed field density (not traced).** EUC6's criteria size the noise from a pre-freeze cone: "about 26 per
   arcmin²" brighter than H_E = 22. Measured with all four cuts in the 600–1000 kpc annuli: median 9.2 per arcmin² in R
   (12.3 with the flux cut alone; W 10.0, C 9.5). That pre-freeze number set only the rationale for the 3.0 line, not
   the statistic. EUC6's files do not record that cone, so I cannot trace it further.

## 4. Ambiguities that could move the word

None of the ambiguities found moves it. The RICHER condition's lower bound is +2.28 against 0 under every reading, and
p is more than a thousand times below 0.001.
- **NaN handling** (the criteria give the cut as a column comparison and as "H_E < 22.0"): moves the median by 0.21.
- **Edge reference set and edge rule on R / L:** one pair, ≤ 0.03 in the median; N1 and N2 pass either way.
- **"Inside distance² 4":** no effect. **Word order when both conditions hold:** did not arise.

Shared by both lanes, and not settled by a re-grade:
- 67 of 316 wide lenses (21 %) have no control. They are the most massive: median log M★ 11.84 against 11.66 for the
  matched ones, median δ +8.5. The word speaks for the 249 matchable wide lenses.
- No mask or NIR-coverage correction exists in either lane.
- Photo-z errors enter both W and C.
- A neighbour count is a proxy, not a halo mass.

## 5. Reading

The re-grade reproduces EUC6's word. Once the NaN handling is aligned it reproduces every EUC6 number. What it adds:
EUC6's server-side cut admitted about 3 % of objects with no H-band flux, concentrated in a few coverage gaps. Removing
them raises the median paired difference by 0.21 galaxies and leaves the word unchanged. EUC6 §5's reading stands as
EUC6 wrote it. RICHER places EUC4's wide-lens residual with the group / cluster rows on average. It does not show that
the law holds in isolated galaxies. Seven in ten wide lenses fall inside the controls' range, so the proxy cannot place
lenses one by one. A dated note on EUC6 recording the NaN finding is the owner's call; this lane edits nothing of EUC6.

## 6. Files

`PROTOCOL.md`, `euc6r.py` (subcommands `targets`, `selftest`, `fetch`, `grade`; `EUC6R_MUTATE=shuffle` for the twin),
`euc6r_targets.csv`, `euc6r_samples.json`, `euc6r_selftest.json` (completeness: 3,504 rows against a server count of
3,504 at a non-target cone), `euc6r_manifest.csv` (665 queries, row counts, sha256 of each raw response),
`euc6r_counts.csv`, `euc6r_result.json`, `euc6r_counts_mutate_shuffle.csv`, `euc6r_result_mutate_shuffle.json`,
`euc6r_nan_and_density.json`, `euc6r_trace_decomposition.json` (written after unblinding). Raw responses (13 MB,
gzipped CSV) are kept outside git under `_external_data/euclid_dr1_mer_cones_euc6r/`; `euc6r.py fetch` rebuilds them
and the manifest's hashes check them.
