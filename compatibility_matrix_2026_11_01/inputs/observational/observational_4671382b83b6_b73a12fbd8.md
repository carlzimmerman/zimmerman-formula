# UR1_one_response_rule: SIGN FLIP YES, AMPLITUDE FAILS. One adiabatic response, no new number, pushes cold inward in discs and outward in cluster cores, crossing at the cosmic ratio. The primary rule fails SPARC's line, groups and LITTLE THINGS

Criteria: `FROZEN_CRITERIA.md` (7f4c82d96c), committed alone first. `ur1.py`, `ur1_tail.py`, `ur1.out`, `ur1_results.json`. No a₀, κ, ε or threshold enters. κ = ½ FITTED, unused here. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** the idea came from reading CN1, OP3 and SL2.

## The sign flip (r M_tot conserved, X39's code unchanged)
M_f/M_0 at r₀, SPARC by V_flat (f_local in brackets), EM1 map: 1.47 (0.44), 1.40 (0.38), 1.63 (0.66), 1.92 (1.08), 1.92 (1.08), 1.98 (1.24).
Clusters by radius, gas + stars (f_local): 0.05 Mpc 0.69 (0.020), 0.15 Mpc 0.80 (0.033), 0.3 Mpc 0.89 (0.052), 0.46 Mpc 0.92 (0.069), 1 Mpc 0.97 (0.112). With BCG 0.74 at 0.05 Mpc, the rest within 0.01. Cosmic ratio 0.190.

So SL2's opposite asks have one cause in sign: f_local above or below 1/R_nat. Response at a fixed radius isn't A, and it runs stronger than SL2's asks on SPARC (A about 0.8 vs Q 1.4–2.0, in different units; the Υ below is the fair comparison).

## Grades, canonical, f★ 0.034
| Map, response | Υ A/B | rms | tilt | keys | G-IN-Mall | Groups Z | X-COP mean, rms | LITTLE THINGS |
|---|---|---|---|---|---|---|---|---|
| EM1, off (K1 = NR1) | 0.72/0.75 | 0.0686 | +0.59 | 12 | −2.89 | +1.47 | −0.160, 0.186 | +0.138 |
| **EM1, Blumenthal** | **0.35/0.35** | **0.0671** | **+0.16** | **14** | **−2.05** | **+1.50** | **−0.097, 0.146** | **+0.105** |
| FAIR200, off | 1.11/1.12 | 0.0998 | +0.48 | 12 | −2.89 | +3.75 | as EM1 off | +0.484 |
| FAIR200, Blumenthal | 0.72/0.73 | 0.0931 | +0.75 | 14 | −2.05 | +3.79 | as EM1 Blum. | +0.423 |
| FAIRTA, off | 1.20/1.20 | 0.1295 | +0.44 | 12 | −2.89 | +5.30 | as EM1 off | +0.559 |
| **FAIRTA, Blumenthal (PRIMARY)** | **0.81/0.82** | **0.1228** | **+0.67** | **14** | **−2.05** | **+5.46** | **−0.097, 0.146** | **+0.521** |
| FAIRTA, Gnedin | 0.82/0.83 | 0.1208 | +0.62 | 14 | −2.09 | +5.43 | −0.102, 0.152 | +0.529 |

Υ by V_flat: EM1 Blumenthal 0.43, 0.52, 0.47, 0.30, 0.36, 0.47; FAIRTA Blumenthal 1.20, 1.20, 1.06, 0.50, 0.59, 0.66. Clusters don't depend on the map, since they always use fair share.

## Frozen label
**SIGN FLIP YES, AMPLITUDE FAILS:** SPARC line (rms and Υ), tilt, groups, LITTLE THINGS, G-IN-Mall at −2.05, X-COP. Keys, KiDS, Local Group and MW weren't reached by any passing run. My expectation (fair share too light) held on SPARC, groups and LITTLE THINGS; KiDS and LG weren't run.

## How this reads
- **Fair share on observed baryons is dead for galaxies.** Halos are too light: dwarfs pin at the Υ cap and groups go to Z +5. Galaxies aren't closed boxes in observed baryons. One sentence for both ends doesn't hold in this form.
- **EM1 + response is the interesting row, and it fails.** Tilt falls from +0.59 to +0.16 (line 0.15), rms is below no-response, LITTLE THINGS nears the 0.10 line, groups hold, and clusters miss one key by 0.05, all with no added number beyond EM1's fitted line. But Υ is 0.35, under the 0.50 line. Before anything else, this is a fail.
- **What would move Υ up.** NR1's ALT says lower low-mass η raises Υ, from 0.72 to 0.88 with no response. NR2's ng 80 runs measure that. This is a reason to rerun, not a result. Gnedin and LC1's f_Q raise it a little only.
- Adiabatic response assumes slow change. Cluster gas was heated and displaced over Gyr, and starting with baryons tracing cold is an assumption. Neither is derived here.

## Limits
EM1 is fitted, law-matched, and without response; not refitted. Core shape by hand, η measured with noise; ANCHOR-DEPENDENT low masses. Groups contracted on Hernquist baryons. LITTLE THINGS point-mass, by hand. X-COP rows without BCG, as XH1. rms and Υ are this path's; BCG is matched for 190 clusters and filled by tercile, as CN1.

## Checks
K1 EM1 off vs NR1 PRIMARY: SPARC 0, preds 0. K2 7.2e-15. K4 0. MUTATE R_nat × 2: Υ 0.81 → 0.51, bites. K3, CN1's own record on its table, not run in this path: stated, as the criteria allow.
