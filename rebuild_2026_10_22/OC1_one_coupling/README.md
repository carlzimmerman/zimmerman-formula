# OC1_one_coupling: INTERVALS OVERLAP ONLY (Reading 2) on both footings. One number for all dissipation misses by about 60×. The apparent match needs two fractions on two sources, and it drifts with mass inside SPARC

Criteria: `FROZEN_CRITERIA.md` (27fb623314, committed alone). `oc1.py`, `oc1.out`, `oc1_results.json`, `oc1_MUTATE.out`, `oc1_MUTATE_results.json`. κ = ½ FITTED; not theory closed. Cold dark energy, never a particle. Nothing here says the data favour the framework. **Energy bookkeeping only:** no mechanism, and no grade on SPARC, groups, the keys or X-COP.

E_BH/E_SN per M★ on CL4's inputs is 89.4, which sets Reading 1.

## Results, galaxy job "both" (soften + undo contraction), clusters on A4's η
| Footing, reading | galaxy ε, median [16–84 %] | cluster ε, range; gm at 14.3 | ratio | CONST | OVERLAP | RATIO |
|---|---|---|---|---|---|---|
| canonical, **1 one number** | 0.00128 [0.00079, 0.00159] | 0.030–0.316; 0.078 | **61** | no | **no** | no |
| alt, **1 one number** | 0.00135 [0.00096, 0.00161] | 0.030–0.316; 0.078 | **57** | no | **no** | no |
| canonical, 2 two sources | 0.116 [0.071, 0.143] | 0.030–0.320; 0.078 | 1.5 | no | yes | yes |
| alt, 2 two sources | 0.122 [0.087, 0.146] | 0.030–0.320; 0.078 | 1.6 | no | yes | yes |

Reading 1 stays disjoint within the bands (canonical galaxies to 0.0026, clusters from 0.017).

## What this says
1. **There is no one coupling.** If dissipation means all dissipation, galaxies need about 1/60 of what clusters do.
2. **The overlap is real but weak.** It's Reading 2: supernova energy in galaxies, black-hole energy in clusters. That needs two fractions that happen to agree, and an account of why spirals' black-hole energy doesn't count. The cluster interval spans a factor of 10, so overlap is easy to get.
3. **Job choice sets the agreement.** Soften alone gives a ratio of 4.6, undo alone 1.2, both 1.5. Undo is CN1's post-result number, with Blumenthal contraction.
4. **ε rises with mass inside SPARC:** Spearman +0.88, +0.82, with Reading 2 medians 0.056, 0.093, 0.138 from lg M₂₀₀ 11–11.5 up past 12 (canonical). That's what fails G-CONST. **The rms alone (0.14, 0.10 dex) would pass,** so this failure rests on the trend, over about a dex in mass.
5. **A4 raises the cluster need more than Argon said:** × 2.5–2.7 at target 14.3, not × 1.4. Worst case goes from 0.075 to about 0.2. Its expected band of 0.07–0.10 isn't what comes out.
6. **Zero-need galaxies:** 101 of 175 (canonical), 119 (alt) have zero need here but E_SN > 0. One coupling gives them energy they don't need. "Zero need" inherits the floor you've removed, so this is a count, not a verdict.
7. **Dwarfs, sign only:** S_min 46–64 against native S 44.2 at 1e10, 79.1 at 1e11. Heating lowers S, so it's not needed at 1e11 and the wrong way at 1e10.

## Limits
All on the idea's own premises: CL4's provisional black-hole and stellar inputs, stipulated cluster targets from the old core rule, c_f-era needs. ZN3's clusters don't need coring for X-COP, and the current miss is in the outskirts, which this idea leaves alone. M_BH = 0.005 M★ applied to spirals too is CL4's rule, not measured here, and a lower disc-galaxy value moves Reading 1 toward Reading 2. A4's η is ng 64; ZN4 is still running. No galaxies below lg M₂₀₀ 11 are active.

## Checks
K1 CL4's 0.0751, 6.711 reproduced. K2 BE1's 0.0171 reproduced; Reading 2 undo returns CN1's 0.094. K3 PASS. MUTATE E_BH × 0 multiplies Reading 1's ε by 90.4 at both ends and gives Reading 1 = SN only. Rerun identical. CN1's Blumenthal response and BE1's η 21.2 are taken as committed.
