# GS5 AMENDMENT A1 (written after the numbers, so it can't be blind)

**What failed.** The frozen MUTATE reads "corr(log Y, log Mg) must fall from above 0.5 to |r| < 0.15, else the lane stops." Unshuffled, that statistic is −0.17, because Y is a flux and the massive qualified clusters sit at higher z. So its first half can't be met. I wrote the statistic without thinking through the distance term. With D² included, the physical correlation is +0.79, but shuffling leaves +0.47 ± 0.08 since D² carries z with it. As frozen, the lane stops.

**What replaces it.** The same shuffle with z taken out: corr(log Y D² E^(−2/3), log Mg) with a quadratic in log z removed from each. Must be above 0.5 unshuffled, |mean| < 0.15 over 500 shuffles, under 1 % of shuffles at or above the unshuffled value. Result: +0.756; +0.006 ± 0.149; 0.000: bites.

**Weight.** This changes a check, after seeing it fail on its wording. No number in any route moves. The verdict is conditional on this amendment, and is marked so in the README. Shuffling also can't test d's amplitude, since a ratio of sums keeps its expectation (shuffled mean +0.031 ± 0.059), so an injection was added: eRASS1's Mg lowered 0.100 dex moves route (d) by +0.100.
