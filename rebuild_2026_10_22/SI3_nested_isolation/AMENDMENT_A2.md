# SI3_nested_isolation AMENDMENT A2 (POST-RESULT; changes no frozen line)

Written after the frozen run (b832059eca) and after A1's run, before any number from the diagnostic below.

**The frozen result stands.** K_H3 failed, so the verdict is NO VERDICT. Nothing here can change that.

**A1's reading was wrong.** A1 blamed thinly covered sky. Matching I to the lenses on source coverage barely moved anything: lens/I in O2 went from 1.121 to 1.091 on S10 and from 1.392 to 1.350 on S_x300, and every Δχ² moved by at most 9.4, and by at most 1.7 on S_strict and S_x300 (`si3_a1.out`). Coverage is not it. Median c is 0.99 for lenses and about 1 for I points.

**The cause is my frozen clone rule.** I drew a lens with replacement, then kept the point only if it passed the veto. The veto's acceptance depends on the clone's z and mass, so the accepted points do not keep the lenses' distribution. They skew to high z and to the massive bins. Mean z in mass bin 1 goes from 0.235 for lenses to 0.269 for I on S10, and from 0.325 to 0.409 on S_x300. The share of points in mass bin 4 goes from 0.249 to 0.324 on S10 and from 0.519 to 0.651 on S_x300.

Using each clone's parent lens's own source weight, this skew alone predicts these lens/I ratios in O2, read from catalogues with no shear:

| sample | predicted from skew | measured |
|---|---|---|
| S10 | 1.101 | 1.121 |
| S20 | 1.164 | 1.189 |
| S30 | 1.202 | 1.230 |
| S_strict | 1.244 | 1.284 |
| S_x300 | 1.327 | 1.392 |

So K_H3 caught a real flaw in I. It was not a threshold set too tight.

P2, SI1 and SI2 use the same draw-then-veto rule. P2's ratio at 2.6 Mpc was 1.05. Whether this skew contributes there has not been tested.

**Diagnostic: per-lens clones, I_c.**
- Every lens in the sample gets exactly 4 accepted points, carrying its own z, χ, lg M★, M_gal and mass bin. The footprint rule and the veto are the frozen ones. That removes the skew by construction, and the rule has no free parameter.
- Draws stop at 100,000 per lens. Any lens left short keeps what it has, and the count is printed.
- New seed stream: `SeedSequence(20261031 + 3)`. The plain randoms R stay as frozen, because they have no veto to skew them and lens/R is within 5 % of 1 in O2.

**Grading.** `si3_grade.py`'s own text, with I replaced by I_c and nothing else changed: same statistic, covariance, models, rungs, footings, classes, labels and Argon lines, and K_H3, K_H4, K_H5 recomputed on I_c. K_H1 and K_H2 carry over, since the estimator and the veto are the same.

**How to read it.**
- If I_c passes K_H3, K_H4 and K_H5, the frozen verdict rule applied to Δ_c = L − I_c is reported as the **A2 reading**. It is not the lane's frozen verdict.
- It is post-result. I have seen the frozen Δ lines and A1's before writing this. The rule was chosen from the catalogues' z and mass distributions, not from any Δχ², and it has no knob. Whether to adopt it is the owner's call.
- If I_c fails K_H3 as well, that is reported too, and the A2 reading is NO READING.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle.
