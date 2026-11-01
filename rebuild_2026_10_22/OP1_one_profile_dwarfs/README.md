# OP1_one_profile_dwarfs: the native z = 0 profile FAILS all five Local Group classes on EM1's M200. A free M200 line passes only near one common mass around 10⁹·³–10¹⁰. The 1e8, 1e9 zooms are SELF-SIMILAR and do not rescue it

Criteria: `FROZEN_CRITERIA.md` (9544d0c865), committed alone before any script or number. `op1.py`, `op1.out`, `op1_results.json`, `op1_MUTATE.out`, `op1_k2.py`, `run_low_zooms.sh`. Written after SN1 and after seeing ZN2 A1, so not blind. κ = ½ FITTED. No a₀ enters this halo; footings differ only in Monte Carlo s, same labels. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

## Frozen verdicts
**P1, EM1's M200, FC1's mapping, canonical, E (Z):**
| shape | ultra-faint | bright M31 | M31 others | classical | LG field |
|---|---|---|---|---|---|
| **10¹⁰ tag (frozen)** | **+1.251 (+10.3)** | **+0.578 (+4.99)** | **+1.343 (+3.99)** | **+0.679 (+4.43)** | **+0.361 (+3.33)** |
| trend carried below tag | +0.903 (+7.36) | +0.427 (+3.97) | +1.081 (+3.17) | +0.551 (+4.03) | +0.291 (+3.26) |
| 10¹² tag | +1.402 (+11.8) | +0.689 (+5.77) | +1.464 (+4.38) | +0.794 (+4.97) | +0.463 (+4.03) |

**FAIL, all five, both mappings, all UNDER.** Worse than the S rule's smooth core (+0.758 to +0.338). The frozen mapping is 0.02–0.04 worse.

**P2, free line: LINE ADMITTED, MEETS EM1.** FC1: 106 lines, a 9.55–10.3, b −0.15 to +0.55, best (9.8, 0.3) max |Z| 1.36; lg M200 8.65–10.05 at lg M★ 4, 9.30–10.0 at lg M★ 6. EM1 there: 5.78 and 7.58. So: × 10³–10⁴ at the faint end. The 16 lines meeting EM1 at lg M★ 8 have b −0.15 to +0.10, nearly **one common mass** for all dwarfs, 9.25–10.05 at lg M★ 4. Frozen mapping: 110 lines, 5 meeting.

**P3, as frozen (at EM1's mass):** share with r₁₂ inside 3ε: ultra-faint 0.48, bright M31 0.08, M31 others 0.40, classical 0.75, field 0.69. Classical and field [CONTINUATION]. **At the mass P2 needs, it is worse (reported):** at lg M200 10, 31/31, 17/25, 5/5, 7/8, 8/13 lie inside 714 pc. P2's pass is a continuation of the profile, not a measurement.

## How this reads
- Not a breakthrough. EM1's M200 and this profile miss by far more than the S rule does. The trend bracket also fails all five, so the queued zooms rescue the EM1 read only if the profile breaks from its trend by a large factor.
- The common-mass result is a two-number fit, and masses that large around 10⁴ M☉ of stars, 39 of them around the Milky Way, have not been tested against anything: tides, counts, or the host's budget.
- **ZN2 A1 stands as that session's result, not mine:** BOTH FAIL on its frozen mapping, passes on FC1's. One profile is still not one rule: ZN3 needs M200 fair share within R200, FC1's normalisation uses EM1's M200.

## Zooms
`run_low_zooms.sh` queued 10-31, nice 15, one thread each, preemptible; waits for the ng 80 batch and continuations to leave. Read below.

## Checks
K1 m(0.1) at the tag 0.1398. K2 smooth core through this path against SN1, median |d| 1e-5. MUTATE r × 1.5: ultra-faint +1.251 → +1.481, BITES. 1e8 smoke, ng 32, scratch: starts and checkpoints.

**Deviation:** P3 as frozen uses EM1's mass ("the M200 used" for P1); the P2 masses are reported from ND1's count, not rerun per line.

## Limits
No baryons, tides or stripping. EM1 has no scatter. Spherical, one r₁₂. Median stack of nine seeds at one tag. Reading below the stored grid or inside 3ε is M ∝ r² by construction.

## Zoom read (`op1_low.py`, `op1_low.out`, 18 of 18 finished)
**SELF-SIMILAR at both masses, as frozen.** Ratios to the 10¹⁰–10¹² trend:
| tag | lg M200 | c₂₀₀ | c₂₀₀ trend | ratio | M/r² at 3ε, ratio |
|---|---|---|---|---|---|
| 1e8 | 7.94 | 13.75 | 16.34 | 0.84 | 0.89 |
| 1e9 | 8.93 | 12.07 | 13.53 | 0.89 | 0.88 |

Both sit below the trend, inside the frozen 20 %: the profile does not steepen toward the dwarfs. Another session's separate read of the same runs (`op1_low_zooms.out`, its file, not committed here) gets SELF-SIMILAR too, with c₂₀₀ ratios 0.81, 0.86 and M/r² 0.88, 0.86; it uses each tag's own 3ε and a different trend form. The class doesn't depend on that.

**P1, EM1's M200, tags interpolated, FC1, canonical, E (Z): FAIL, all five, both mappings, both footings, all UNDER:** ultra-faint +1.186 (+9.71), bright M31 +0.515 (+4.53), M31 others +1.266 (+3.76), classical +0.614 (+4.10), field +0.325 (+3.21). That gains 0.04–0.08 dex on the 10¹⁰ tag. Median lg M200 is 5.7–8.4, so most systems sit at or below the 1e8 tag and are clamped to it.

**P2: LINE ADMITTED, MEETS EM1, both mappings.** FC1 134 lines (106 before), 17 meeting EM1 at lg M★ 8, b −0.15 to +0.10, lg M200 9.25–10.05 at lg M★ 4; frozen map 133, 5 meeting. The near-common-mass result stands. EM1 at lg M★ 4 is 5.78, so the gap stays × 10³–10⁴.

**So the Local Group miss on this rule is a mass miss, not a shape miss.** No shape measured down to 10⁸ closes it. The admitted line is a two-number fit with no mechanism and no test against tides, counts or the host's budget.

**Correction to P3 above.** ND1's 714 pc at 10¹⁰ is already 3ε (ε 238 pc in the run's own meta). The frozen text called it ε, and `op1.py` multiplied by 3 again, so the P3 shares above are inside 9ε. Corrected, at EM1's mass: 0.00 in all five classes, no class [CONTINUATION]. This is a scaled ε, since no zoom exists below 10⁸. The README's P2 count "inside 714 pc" was right as 3ε, so P2's pass is still a continuation. `op1_low.out` prints both.

**Checks.** K1 m(0.1) at the tag 0.1398, tag10 row reproduces the table above. MUTATE r × 1.5: ultra-faint +1.186 → +1.406, BITES. First run of the self-similarity lines used a wrong x (units, x 51), the rerun x 0.017; P1 and P2 did not use it. x 0.017 is at the runs' x_conv, so the M/r² ratio is at the edge of what they resolve. Stack z = 0, no baryons, tides or stripping.
