# UR3_direct_weighing: SPLIT. DiskMass is reached with Blumenthal (r 1.071, Υ_K 0.287); the Milky Way misses narrowly with Blumenthal and passes in priors with Gnedin, its first in-prior cells. But stress tests show both weigh inner cold mass, not the response: an uncontracted NFW start does about as well

Criteria: `FROZEN_CRITERIA.md` (a4e73c62cb), committed alone first. `ur3_table.py`, `ur3_common.py`, `ur3_diskmass.py`, `ur3_mw.py`, `ur3_*.out`, `ur3_*.json`. **SPARC's Υ line is not moved; UR1 and UR2 keep their fails.** κ = ½ FITTED, unused in route E. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

## Frozen read (EM1, δ 0, canonical, background A; B agrees)
| Mode | DiskMass r at 1.5 h_R | Υ_K | halo share of g | n | Milky Way box | McMillan V_c, K_z |
|---|---|---|---|---|---|---|
| Off | 1.365 | 0.618 | 0.20 | 30 | WIDE PRIORS ONLY, 1 cell | 197.5, 66.6 |
| **Blumenthal (primary)** | **1.071 [1.040, 1.148]: REACHED** | **0.287** | 0.61 | 28 | **V+K ONLY**, 0 cells, best D 1.01, in-prior 1.06 | 251.2, 81.2 |
| Gnedin | 1.118 | 0.320 | 0.54 | 29 | **FEASIBLE IN PRIORS**, 13 cells, 7 in prior, D 0.73 | 234.1, 76.1 |

Lines: Eilers 229.05 ± 4.64, K_z 66.4 ± 2.2. Best Gnedin cell: R_d 2.60, M★ 5.44e10, V_c 233.4, K_z 69.6.

**Frozen reading: SPLIT.** Blumenthal reaches DiskMass and misses the Milky Way. Gnedin does the opposite. My expectation (r 1.1–1.25, K_z fails) was partly right: r fell further than I said, and K_z fails on McMillan but not on the box.

## Stress, after the result. These decide how to read it
1. **The result is not about the response.** LC1's measured zoom shape, NFW c 12.95, has 3.84e10 M☉ inside R₀ against the smooth core's 1.44e10 (r₀ 15.4 kpc), × 2.7:

| Start, mode | DiskMass r, Υ_K, n | Milky Way box | McMillan V_c, K_z |
|---|---|---|---|
| NFW, off | 1.090, 0.364, 26 | FEASIBLE IN PRIORS, 16 cells, D 0.63 | 227.4, 74.3 |
| NFW, Blumenthal | 0.983, 0.175, 23 | INFEASIBLE, D 1.17 | 268.9, 86.7 |
| NFW, Gnedin | 0.998, 0.185, 23 | INFEASIBLE, D 1.03 | 259.5, 83.7 |

So the Milky Way asks for about 4e10 M☉ of cold mass inside R₀, however it gets there. Smooth core + response and NFW + none both supply it; NFW + response overshoots. c 12.95 is one 1e12 number carried across masses, by hand, and n 26 is below this lane's 27.

2. **The two starts can't both be right, and the record's baseline is the smooth core.** The response on the zoom's own shape, which LC1 measured as real, overshoots the Milky Way. Gravity-only NFW start + LC1's response is the honest native calculation, and it fails. The passing rows need either a core or a missing response, and neither is derived. This is the same wall as OP3 and CN1.

3. **Fragile details.** CFG577's Jeans integral raises r 5–7 %, so Blumenthal's 1.071 becomes about 1.13, outside the line. A young-tracer σ_z systematic would pull r down, so r ≈ 1 at DMS's σ_z is not agreement with an old-population σ_z. Two of 30 unfittable in the primary. Υ_K is not one number per galaxy: 0.287 at 1.5 h_R, 0.198 at 2.2 h_R. Milky Way Blumenthal becomes FEASIBLE IN PRIORS at spherical M_b × 0.7 (WIDE at 0.85), so the spherical approximation matters; Gnedin stays in priors at × 0.7–1.15.

4. **Not tested: whether the Milky Way's in-prior stars agree with Υ near 0.3.** Its cells use star-count masses, not a mass-to-light ratio. DiskMass supports low Υ only if its σ_z stands, against population synthesis at 0.27 dex.

## Reading
Direct weighings don't refuse a large inner cold mass: both accept halo share near 0.6. So the Υ pressure is not simply SPARC's route E being wrong, and the Milky Way no longer rules the idea out in priors. They do not single out the response. The open question is now sharper: **what is the cold mass inside 10 kpc at 1e12, and how does it get there?** Zoom shape alone or smooth core + response give about the right amount; zoom + measured response gives too much.

## Checks
K1 no halo: r 1.494, Υ_K 0.821, matching CFG576. K2 GD3 reproduced through RG1's head; off passes M0 through. K3 RG1's own McMillan 202.84, 67.90. K4 8.9e-16. MUTATE M_b × 2: DiskMass r 0.986, Υ_K 0.216; McMillan V_c 271.5, K_z 87.6. Off here reads 197.5, not RG1's 202.8, because the table is NR1 PRIMARY's ng 80, not RG1's.
