# OG1_outer_gas_slope: FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** ZN4's native halos pass all 15 cluster keys only on a gas scale of +0.111. Pointed data measure +0.005 ± 0.017 at R500 (GS4), and the SZ route gives no such offset either (GS5), so raising the gas inside R500 is not a measured option. But the keys' budget also counts gas beyond R500, where it is an extrapolation at one slope, s = 2.777, from 11 massive X-COP clusters (GS1). X73 noted that the outer keys measure this tail. With gas at R500 held at its measured value, can a slope the data allow do the same job?

**Standing rules.** Native inputs only. κ = ½ FITTED. Cold dark energy is a gravitating field component, never a particle. Footings never pooled. Not theory closed. Nothing here may say the data favour the framework. No zoom is run and no shape changes.

**Seen before freezing (disclosed):** GS4's and ZN4's tables at s 2.777; GS1's slope range; X73's G-OUT-M3 moving by about 3.4 in Z across s 2.676–3.071, on a different rule.

## Method
ZN4's grader text and shapes (`ZN4_cluster_resolution/zn4_shapes.json`, ng 80 at 1e14 and 1e15), read-only, with GS4's measured gas +0.005. The only change is one slope for every cluster beyond R500:

s = 2.04, 2.2, 2.4, 2.5, 2.676, 2.777, 3.071, at f★ 0.034 and 0.0615, both h values, same class rule as GS4.

2.676 and 3.071 are GS1's bootstrap 16–84 % limits. 2.04 is its lowest cluster (A2319). No finer scan follows, and no value is added after a result.

## Verdict (frozen)
Take the graded s values whose class is Z0 PROFILE PASSES BOTH (all 15 keys and X-COP, both f★).

| verdict | condition |
|---|---|
| **RESCUED WITHIN THE MEASURED SLOPE** | a passing s lies in [2.676, 3.071] |
| **NEEDS A SHALLOWER TAIL THAN MEASURED** | no pass there, but a pass in [2.04, 2.676) |
| **NOT REACHED** | no pass at any graded s |

A shallower-tail verdict is a target for measurement, not a pass: the median slope is what was measured, and one slope is being assigned to every cluster.

## Reported, not graded
- For each s: keys passed, worst key, G-OUT-M3, X-COP mean and rms, which keys fail and in which direction.
- X-COP's slope against M500, from GS1's per-cluster values, as a rank correlation, if GS1's results hold both. Eleven massive clusters can't measure the slope at the lensing sample's median mass, and this is said wherever the number appears.

## Prediction on record
From X73's sensitivity, about 8.6 in Z per unit s on G-OUT-M3, getting from +4.41 to +2 needs s near 2.5. So: NEEDS A SHALLOWER TAIL THAN MEASURED, unless other keys go over first, which would make it NOT REACHED. This is a rough scaling from another rule.

## Checks
- **K1.** s 2.777 reproduces `ZN4_cluster_resolution/zn4_results.json`'s "gas +0.005" jobs: predictions and X-COP to 1e-9, at both f★.
- **K2.** G-OUT-M3 changes between s 2.04 and 3.071 by more than 0.1 in Z: the slope reaches the keys.
- **Rerun.** Results JSON byte-identical.
- **MUTATE (`OG1_MUTATE=1`, separate outputs).** The slope is pinned at 2.777 on every grid row. K2 must fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 og1.py`
