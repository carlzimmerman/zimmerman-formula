# CE1_converged_eta_grade: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** X81 showed that the native zoom halos are NFW cusps and that X77's η_native depends on where the fit
starts (r_conv, pinned at 3ε). With the cut removed, η at 10¹² is 25.94 (reported). What does route E's full grader say
when every mass gets the converged-cusp η, on every line (SPARC, groups, 15 cluster keys) and on both footings?

**Converged η per run.** Each finished X48 snapshot at the highest grid available per mass:
- 10¹² at ng 64;
- 10¹³ and 10¹⁴ at ng 48 until A4 finishes. Those carry the label [ng 48].

η_conv = (4/3) a²/B_S(a), where a is X77's smooth-core fit objective applied to an exact NFW at the run's own c_nfw_fit
(X48 measure(), unchanged), sampled uniformly in enclosed mass on [x_c, 1] with x_c = 0.001. This is X81's
`a_fit_profile`, imported unchanged. Per mass: the median over seeds, with a 10 000-draw bootstrap 68 % (seed 20261030).

**Grader.** X74's `x74_native_cf.py`, unchanged, via `X74_CF` = a table of c_f-equivalents. That is c = 4 (η_conv/10.82)^{0.8},
the inverse of the rule η_S = 10.82 (c/4)^{1.25}. The same map was used in X77's grade.
- Slope 2.7774. f★ 0.034 and 0.0615.
- Medians graded; the bootstrap 16th/84th also run.
- X74's own outputs are held aside and restored, and ours are renamed CE1_*.

**Verdict** (per f★, per footing; X74's frozen lines unchanged):
- **CONVERGED NATIVE PASS:** every line passes at the median, 16th and 84th.
- **CONVERGED NATIVE FAIL:** the median fails. Name each failing line and its margin.
- **KNIFE EDGE:** the median passes, but the 16th or 84th fails.
- Headline = canonical. The alt footing is reported separately and never pooled.

**Checks.**
- **K1:** X77's own c_f-equivalent table {1e12: 6.754…, 1e13: 4.858…, 1e14: 5.026…} at f★ 0.034 reproduces X77's
  committed grade (`x77grade_x74_results_fs0.034_nat_s2.7774.json`): SPARC rms and U_median on both footings,
  exactly.
- **K2:** the 10¹² ng 64 converged median reproduces X81's 25.94 (to 0.01).
- **MUTATE:** η_conv × 0.5 at every mass. The canonical SPARC median Υ must rise by more than 0.01.

**After A4 (reported, automatic).** When all 18 A4 ng 64 snapshots exist, re-run with 10¹³ and 10¹⁴ at ng 64. Those
outputs are tagged CE1_A4_*. The same verdict rules apply, labelled post-A4.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. The zooms are
collisionless cold dark energy dust; the floor physics is not in them. The converged η is an extrapolation of the fitted
NFW inward of r_conv (X81 T2 showed every halo is NFW-shaped down to the cut).
