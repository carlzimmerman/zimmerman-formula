# SL1_symbolic_law_search: TRAIN ONLY, 0 survivors

Criteria `FROZEN_CRITERIA.md` (4c1194e933), `AMENDMENT_A1.md`. Baseline NR1 PRIMARY, train gate 10.7. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework. Inherits NR1's ANCHOR-DEPENDENT low masses; NR2 unread.

## Result
| Grammar | Exact regraded | L_gate 0 on train | Survivors | a₀-free hits |
|---|---|---|---|---|
| SPEC (has x_b, x_c, κ) | 935 | 935 | 0 | 0 |
| NATIVE (no a₀, no κ) | 20 | 0, best 0.433 | 0 | n/a |

**Frozen label: TRAIN ONLY**, from SPEC. Every SPEC hit divides by a₀ in B, against the owner's 10-31 rule, so none could be adopted even had it survived. **In the grammar the rule allows, NO HIT.**

Fails among SPEC's 935 (one pair can fail several): X-COP 925, holdout G2 879, holdout G1 872, line on 175 448, alt's keys 436, groups 2. q INERT 0. Three pairs fail X-COP alone, all with A = √(1/(1 + √q/(R_nat η))); the nearest has X-COP mean +0.038, rms 0.126 against 0.10. The ten pairs that pass X-COP fail elsewhere.

**Best NATIVE:** A = 1/(1 + (q/R_nat − √q) v), B = 1 + √f_l (R_nat f_l − 1), gate 0.433: G-IN-Mall misses by 0.03 and G1 by 0.40. Reported in `sl1_native_b.out`, Υ 0.5:
- A about 0.78–0.84 on SPARC and 1.00 on clusters.
- B on clusters 0.84–0.92, on SPARC medians 1.5–62, with a 90th percentile near 8,700 in the fastest bin. A multiplier that size where baryons dominate is not an adiabatic response. **Not a physical candidate.**

## How to read this
- **The crossing at f_l = 1/R_nat is imposed, not found.** Tier 1's outer bound fixes B = 1 there, which leaves NATIVE only 113 B trees at size ≤ 8. It is not independent support for UR1.
- **SPEC's training hits are weak evidence.** A hundred thousand distinct pairs were tried and the hits share 48 A trees and 352 B trees; X-COP and holdout then remove nearly all. That is what over-selection looks like.
- **A near 0.8 on SPARC recurs** in these trees as in SL2's inversion. This is the same post-result clue, not a new one, and the trees' leaves don't explain it.
- Exhaustive only to size 8 per tree, this grammar and these inputs: **not an impossibility theorem.**

## Correction
The first report printed "a0-free True" on its SPEC rows. That test compared clipped gate violations, which are zero at both a₀ for any hit, so it could not detect dependence. `a0_indep` now compares B itself at scaled x_b, x_c. All 935 are a₀-dependent. Gates, surrogates and regrades unaffected; rerun from stored regrades with `--noexact`.

## Checks
K1–K3, K5–K7 reproduce NR1 PRIMARY. K4 failed narrowly and the frozen branch was taken: G4 graded exact for all candidates. K8 failed first, passed after A1's GA changes, on plants that resemble the seed forms, so the NATIVE null is only as strong as that. Regrade with `sl1_report.py`, then `sl1_native_b.py`.

Rerun from a fresh harvest when NR2 lands.
