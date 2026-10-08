# Claim match: MNRAS submission + PAPER41–45 (2026-10-08)

`claim_match_tex.py` takes every sentence or table row with a digit in each paper. Each was checked by independent reviewers
(none of them wrote the papers) against committed outputs. Verdicts are in `<paper>.claim_review.json`, keyed to the hash of
each source file. **No paper text was edited.** MNRAS MN-26-3158-P is under review, so these findings go into the revision. PAPER41–45
are published on Zenodo, so a correction needs a new version, on the owner's go. Items marked ✔ were re-checked by the coordinating session against the
files; the rest are reviewer findings.

| paper | claims | MATCH | CONTEXT | WRONG | OVERSTATES | UNSUPPORTED |
|---|---|---|---|---|---|---|
| MNRAS v3.4 (submitted) | 466 | 330 | 125 | 2 | 4 | 5 |
| PAPER41 | 47 | 31 | 9 | 0 | 5 | 2 |
| PAPER42 | 51 | 32 | 8 | 6 | 5 | 0 |
| PAPER43 | 55 | 37 | 9 | 2 | 5 | 2 |
| PAPER44 | 31 | 18 | 10 | 2 | 1 | 0 |
| PAPER45 | 45 | 34 | 6 | 2 | 1 | 2 |

## Most consequential
- ✔ **PAPER44**: "WALLABY gives −1.7σ" is wrong. −1.70 ± 2.12 is the stacked amplitude Â, on a scale where AQUAL = +1. Its significance is Z = −0.57, and the sample
  cannot reach a verdict (`prep_2026/wallaby_firing/fire_wallaby.out`). The error favours the framework. Also, the Chae range mixes two kernels, and the Milky Way 2.5σ is
  the end of a range computed with ν_RAR.
- ✔ **PAPER42**: the headline band "55.3–91.1, y_t 71–117 at 2σ" is a **1σ** band. Λ/a0² ∝ a0⁻², so the 12% error on a0 becomes 24%, and
  `make_paper42_figures.py` mislabels obs × (1 ± 2×0.122) (p30: 73.19 ± 17.86). The true 2σ is ≈45–119. Four sentences and the caption are affected.
- **PAPER42**: the Λ match depends on the worse-fitting kernel. With the RAR kernel the vacuum term is 12.99 a0², 5.6× below the observed value (p21); this is omitted.
- **PAPER41/42**: "a direct fit bounds y_t only from below" omits that with Υ free the best fit is y_t = 5 at Δχ² −53.2 (p36). Calling the turn-off
  "testable content" contradicts p38, which needs about 878× better calibration.
- **PAPER43**: "needs distances good to ~3–5%, not more galaxies" contradicts p44, which needs 217–1137 galaxies and 1.8–4.1% in a0. The "~3% kernel systematic" is an
  assumed input; p41b reports 15.6%. p41b's own robustness and calibration checks failed (0/2), yet the text calls the result "mass-to-light-robust".
- **PAPER45**: the largest catchment share at 256³ is 37% (MIXB), not 30%. "57% at 512³" is in no committed output.
- ✔ **MNRAS**: "injection tests show that each returns a known a0" (Conclusions). I1–I3 cover the standard fit, the shape-only and the deep-band estimators; estimator C has
  none, and estimator A has only a sensitivity test.
- ✔ **MNRAS**: "on either common footing Milgrom's 2π form is at least as close to the data as 1/2" (Conclusions). Check S3i itself says "estimators A and C".
  Estimator B is closer to 1/2, with likelihood ratio +0.12.
- ✔ **MNRAS**: abstract, "Inferring a0 amplifies errors unless g_bar < 0.3a0". Errors are amplified at every acceleration (A_obs ≥ 2.1); the body text is right.
- ✔ **MNRAS**: "12 per cent higher" should be 13 per cent higher (1.190 vs 1.049; −11.9% is the drop the other way). Table tab:laws, z = 2 row: +0.25 → +0.24,
  −0.07 → −0.06 (double rounding of 0.2445 and −0.0645).
- **MNRAS**: unsupported by any committed output: "no independent calibration is known to reach 0.1 dex"; "an independent Υ outside 0.45–0.75 would
  exclude it"; "nothing changes for κ in 0.4–0.6" (the gate threshold moves with a0); "CO→H2 rarely known to 0.06 dex"; the MIGHTEE "median 0.35"
  (the committed Table 5 median is 0.36, a different median, so check the paper text). "Factors of two to five" is actually 2.0–5.5.
- ✔ **MNRAS reproducibility**: about 20 estimator-A numbers exist only in git-ignored `reproduce_outputs/estimator_A.out`. They are reproducible with `reproduce_all.sh`
  but not committed.

The full list, with sources and the suggested minimal wording, is in each `.claim_review.json`.
