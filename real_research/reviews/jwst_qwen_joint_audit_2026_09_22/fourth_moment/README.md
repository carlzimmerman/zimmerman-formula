# Static-spectrum challenge: the frozen pair is distinguishable

The existing pair's matched width and mean delay do not imply matching static
line profiles. Fresh samples find a 22.15% fourth-moment difference and a
22.11% normalized-kurtosis difference. Thus this pair does not demonstrate
information that can only be obtained through timing. The earlier 16.4% mixed
moment result remains valid within its narrower scope.

For the same frozen A and B parameters as the parent README, run three fresh
200,000-photon batches per cloud and an independently seeded identical-A null:
1.8 million paths total. No parameter was refitted. The conditional fourth
moment is 3*(2*angular)^2; direct v^4 from actual Gaussian electron draws is an
additional check. The kurtosis uncertainty uses the delta-method influence
function including covariance of the estimated second and fourth moments.

| Comparison B minus A | Difference | Monte Carlo SE | Relative difference |
|---|---:|---:|---:|
| Conditional fourth moment | 74.5164 | 1.5913 | 22.15% |
| Normalized kurtosis | 1.37245 | 0.01408 | 22.11% |
| Direct Doppler fourth moment | 80.1296 | 5.6793 | 24.18% |

The independent identical-A null is within 1.93 standard errors for every
reported statistic. Direct/conditional paired calibrations pass the declared
six-SE checks. All declared checks pass and the manifest validates input and
output hashes. This is sampling replication plus independent analysis of the
same transport engine, not an independent transport solver. Intervals are
approximate Monte Carlo estimates; they omit model and observational error.
Detectability with finite astronomical data has not been assessed.

The stronger conditional difference estimate and noisier direct estimate are
consistent within their sampling uncertainty. Neither proves novelty or a new
equation. No new literature claim is made; the parent README preserves the
bounded prior-art check.

## Audit of Qwen evidence

Attempt b13df86f78d44092b7521eec20aff52e's main conditional fourth-moment
calculation suggested the same difference, but its checks mixed mode-dependent
predicates, and h=0 in cloud B does not make B identical to A. The referee's
claim that the positive-null z was -5.68 was also mistaken: that number was the
main comparison printed in every mode; its separate null was not printed.
Attempt 45b2151cadea46279d2a5fe168440fd0 switched the predicate from |z|>3
to |z|<3 across modes. Its referee incorrectly called z=-2.09 significant at
a three-SE threshold. These reviews cannot substitute for examining code.

This independent script uses a separately computed identical-cloud null,
explicit conditional and direct moments, and unchanged comparison formulas.
The frozen-pair fourth-moment target is now finished at the stated finite
precision. Repeating it is not the next research objective. Qwen should pursue
the queued transport-equation/moment-closure target and use these moments as
counterexample fixtures for unjustified closure.
