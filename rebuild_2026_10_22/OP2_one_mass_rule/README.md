# OP2_one_mass_rule: BOTH FAIL as frozen, narrowly. EM1's SPARC-fitted mass line, unrefitted, with the native profile, takes measured-gas clusters from G-OUT-M3 +4.47 to +2.30 / +2.00 and 14 of 15 keys; X-COP misses by 0.008–0.015 on the SPARC mapping. Seed noise doesn't close it

Criteria: `FROZEN_CRITERIA.md` (e1ab75e185), committed alone before any script or number. `op2.py`, `op2.out`, `op2_results.json`; post-result `op2_boot.py`, `op2_boot.out`. Not blind: the idea came from reading GS4 and LF1. κ = ½ FITTED. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

**Rule.** Native z = 0 shape. Cold mass inside R200 = 10^(11.18 + 0.90 (lg M_b(<R200) − 10)), EM1's line, fitted on SPARC, not refitted, carried 2–3 dex past SPARC's M_b. No S, r₀, a₀ or new number. On measured gas (eRASS1's own; GS4 +0.005 ± 0.017).

## Frozen read (FC1's mapping primary, the one SPARC passes on)
| job, eRASS1's gas | f★ | keys | worst, h 0.672 | X-COP mean, rms |
|---|---|---|---|---|
| fair share, frozen map (K1 = ZN3) | 0.034 | 11 | G-OUT-M3 +4.47 | −0.004, 0.076 PASS |
| fair share, FC1 map | 0.034 / 0.0615 | 12 / 12 | +4.22 / +3.93 | −0.034, 0.085 / −0.041, 0.088 PASS |
| **EM1 line, FC1 map (PRIMARY)** | **0.034** | **14** | **G-OUT-M3 +2.30** | **−0.058, 0.093 FAIL** |
| **EM1 line, FC1 map (PRIMARY)** | **0.0615** | **14** | **G-OUT-M3 +2.00** (just over) | **−0.065, 0.097 FAIL** |
| EM1 line, frozen map | 0.034 / 0.0615 | 14 / 14 | +2.64 / +2.37 | −0.028, 0.076 / −0.034, 0.078 PASS |
| EM1 line, FC1 map, X-COP's +0.111 gas | 0.034 / 0.0615 | 13 / 13 | G-OUT-all −2.43 / −2.63 (OVER), G-IN-Mall | as primary |

**VERDICT: BOTH FAIL.** No z_obs, no r_ta tail, no grader change. On X-COP's scale this rule goes heavy, so the mass line and that gas scale don't add: they're rival answers to the same shortfall.

## All gates, one rule
| gate | FC1 map | frozen map |
|---|---|---|
| SPARC (ZN2 A1) | **pass**, Υ 0.75 / 0.69 | **fail**, Υ 0.84 / 0.81 (limit 0.80) |
| Groups (ZN2 A1) | **pass**, +1.91 | **fail**, +2.08 |
| X-COP, hydrostatic | **fail**, −0.058 to −0.065 (limit 0.05) | **pass** |
| 15 keys, measured gas | **14**, M3 +2.30, +2.00 | **14**, M3 +2.64, +2.37 |

Every miss is narrow, and no one mapping passes all. The groups Z in `op2.out` (+1.62) is the grader's S-rule path, not this profile; use ZN2's. Changing the map between scales, or a radius factor in between, would be a tuned number, so it isn't taken here.

## Seed bootstrap (post-result, 100 draws, all three tags)
| map | all gates here, both f★ | 15 keys both f★ | X-COP both f★ | M3 f★ 0.034, 0.0615 (68 %) |
|---|---|---|---|---|
| FC1 | 0 | 0 | 6 | +2.30 [+2.25, +2.35], +2.00 [+1.96, +2.06] |
| frozen | 0 | 0 | 72 | +2.65 [+2.61, +2.69], +2.37 [+2.33, +2.41] |

**M3's miss is not seed noise.** X-COP's on the FC1 map mostly isn't. SPARC and groups had no seed bootstrap here.

## How this reads
- The strongest single step today: the measured-gas shortfall that stopped ZN3 falls by about half in Z from a line fitted on galaxies only. It's still a fail.
- EM1 was matched to the a₀ law, so the law enters here as an input on SPARC. This doesn't derive it. Its slope 0.90 has no origin in this lane, and neither does the galaxies' retained baryon share.
- The line crossing fair share near lg M_b 14 may be a coincidence over a 3-dex extrapolation. M3 is the tercile where the line has least excess, which is where it falls short.
- LF1's depletion is read from the same shear as the keys, so the two don't count twice.
- **Still open under this rule:** Local Group (OP1), Milky Way, KiDS, G-IN-Mall's cross-shear null, ΔV at high V_flat (−22, −49 at the frozen read), Υ running with V_flat, HS1. Not graded on z_obs.

## Next read, set now
When ZN4's ng 80 stacks finish: rerun `op2.py` with those tags, same labels, against this table. Resolution is the unbootstrapped lever (η moved × 1.3 from ng 48 to 64). A pass there would be post-OP2 and labelled so.

## Checks and deviations
K1 fair share reproduces ZN3: 11 of 15, +4.47, X-COP −0.004, 0.076. K2 EM1 at lg M_b 13.5: 14.33 against cold fair 14.22. MUTATE a + 0.2: 4 of 15, X-COP −0.186, BITES. Bootstrap identity |d| 0. First run crashed on my unescaped gas patch before printing any number; fixed and rerun. rx uses f_c 0.8405 as quoted by FC1.
