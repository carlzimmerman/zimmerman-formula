# OP1_one_profile_dwarfs: the native z = 0 profile FAILS all five Local Group classes on EM1's M200. A free M200 line passes only near one common mass around 10⁹·³–10¹⁰, where nearly every dwarf radius is inside 3ε. 1e8, 1e9 zooms QUEUED, not read

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
`run_low_zooms.sh` queued 10-31, nice 15, one thread each, preemptible; waits for the ng 80 batch and continuations to leave. **Nothing from them is read.** When `LOW_ZOOMS_DONE` exists: measure as `zn2_a1.sh`, rerun P1 and P2 with those tags, and grade SELF-SIMILAR / BREAKS as frozen.

## Checks
K1 m(0.1) at the tag 0.1398. K2 smooth core through this path against SN1, median |d| 1e-5. MUTATE r × 1.5: ultra-faint +1.251 → +1.481, BITES. 1e8 smoke, ng 32, scratch: starts and checkpoints.

**Deviation:** P3 as frozen uses EM1's mass ("the M200 used" for P1); the P2 masses are reported from ND1's count, not rerun per line.

## Limits
No baryons, tides or stripping. EM1 has no scatter. Spherical, one r₁₂. Median stack of nine seeds at one tag. Reading below the stored grid or inside 3ε is M ∝ r² by construction.
