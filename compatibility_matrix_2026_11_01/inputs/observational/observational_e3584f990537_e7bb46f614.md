# SR1_star_saturated_response: CLAIM FAILS narrowly, and this is the closest no-a₀ response row so far: Υ 0.47/0.46, tilt +0.10, groups CONSISTENT, LITTLE THINGS +0.105. Post hoc form; holdouts in SR2

Criteria: `FROZEN_CRITERIA.md` (f55188b729), committed alone first. `sr1.py`, `sr1_tail_add.py`, `sr1_read.py`, `sr1.out`, `sr1_results.json`. **The form was written after reading UR2, ER1 and GT1, and exponent 2 is a choice: a fit by construction until new data grade it.** No a₀ or V_obs enters. κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

| Rule, δ | Υ A/B | rms | tilt | Υ by V_flat | groups Z | LITTLE THINGS | Fails |
|---|---|---|---|---|---|---|---|
| Blumenthal, 0 | 0.35/0.35 | 0.0671 | +0.16 | 0.43 0.52 0.47 0.30 0.36 0.47 | +1.50 | +0.105 | line, tilt, LT |
| **Saturated, 0** | **0.47/0.46** | 0.0752 | **+0.10** | 0.48 0.58 0.56 **0.44 0.51** 0.68 | +1.50 | +0.105 | line, LT, narrowly |
| Saturated, +0.10 | 0.42/0.43 | 0.0893 | +0.04 | 0.40 0.51 0.52 0.41 0.47 0.60 | +0.55 | +0.052 | line |
| Literal, 0 | 0.40/0.40 | 0.0833 | +0.03 | 0.38 0.46 0.44 0.38 0.45 0.59 | +1.41 | +0.090 | line |
| Literal, +0.10 | 0.38/0.38 | 0.0983 | −0.07 | 0.30 0.42 0.43 0.36 0.43 0.54 | +0.48 | +0.039 | line |

Clusters are UR1's row by assumption: 14/15, G-IN-Mall −2.05, X-COP −0.097, 0.146. No row passes.

**Effective f and χ★ at 2.2 R_d, saturated δ 0:** 0.98, 0.2; 0.95, 0.3; 0.84, 1.0; **0.46, 3.0**; 0.59, 2.1; 0.54, 2.3.

## Reading
- **My expectation was wrong.** I expected tilt to return through dwarfs' inner χ★. Tilt stays +0.10 and dwarfs keep f near 0.95 at 2.2 R_d, as the text said. χ★ ≈ 3 at 150–200 also matches it.
- **The text's numbers are off in two ways.** f at 150–200 is 0.46, not 0.14–0.20, so the claim at that bin fails (0.44 against 0.50). Its outer identity fails as written: the literal form has f above 1 in dwarfs (1.14–1.26) because M_b/M_c0 stays nonzero at R200. X39's (1 + F) form fixes that and is the better row.
- It selects by the right variable: f falls where the need is, unlike #7 and #10. 250–400 km/s is suppressed too (0.54), where ER1 needs none; its Υ 0.68 is inside the line, so that isn't a fail here.

## Checks
K1 denominator off vs UR2: 0. MUTATE M★ × 0.1: Υ 0.42 → 0.32, f → 1.00. K2 by construction, R_max joins to 0.5 L₃₆.
