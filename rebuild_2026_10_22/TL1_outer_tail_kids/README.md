# TL1_outer_tail_kids: the r⁻⁹ᐟ⁴ tail does not help KiDS (NO IMPROVEMENT, both footings)

Criteria: `FROZEN_CRITERIA.md`, committed alone before any script or number. Harness: GH2, with only route E's M(r) swapped. Bins 3–4.

| k (R_vir) | canonical: GH2 / T2 / T1 / law | alt: GH2 / T2 / T1 / law |
|---|---|---|
| 1 | 437.9 / 499.5 / 621.1 / **66.2** | 433.9 / 503.1 / 620.5 / 80.8 |
| 2 | 203.3 / 267.1 / 397.5 / 298.3 | 216.4 / 284.5 / 397.2 / 429.9 |
| 3 | 140.6 / 189.8 / 232.4 / 757.8 | 178.3 / 229.0 / 234.7 / 1028.3 |
| 5 | 675.7 / 622.8 / 125.0 / 1913.7 | 681.3 / 627.6 / 125.6 / 2472.8 |

**Verdict (T2, inner core identical to GH2):** best 189.8 canonical, 229.0 alt, against GH2's 140.6 / 178.3 and the law's 66.2 / 80.8: **NO IMPROVEMENT**. At k = 1 the law still wins on both footings.

Checks pass: K1 (GH2 reproduced exactly), K2 (slope 3 gives 139.3 vs 140.6), K3, MUTATE. The first run's K2 printed nan: my tail formula divided by zero at slope 3, so that verdict read NOT DECIDED. I fixed that one line (criteria unchanged); all T2 and T1 numbers at slope 9/4 were identical in the rerun.

**Why.** At fixed M(<r_ta), a shallower tail moves mass from 100–500 kpc to beyond it (test lens at 300 kpc: ΔΣ 8.67 → 6.99). That lowers the signal where KiDS needs more. This is the opposite of the external model's ×1.7–2.1, which came from its 16/3 for 8/3 error.

**Post-result, reported only (`tl1_kscan.py`, the frozen grid jumps from 3 to 5).** GH2 best 140.6 (k 3); T2 best 189.8 (k 3); T1 best **121.9 at k 4.5** (alt 123.3). T1 is the only variant below GH2 and is not a rescue:
- it needs gas to 4.5 R_vir, beyond turnaround (about 3.3 R_vir), with no measured basis;
- it re-solves r₀, so it changes SPARC, which was not graded;
- it is still about twice the law's χ²;
- the optimum k was chosen after seeing the result.

**Limits.** KiDS only. T2's density step at r_f is not physical. c_f = 4 external. Zhang+24 gas; the cool-gas partition is not modelled. Clusters and SPARC were not rerun; there is no pass to carry over.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating field component, never a particle.
