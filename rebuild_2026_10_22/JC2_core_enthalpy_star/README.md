# JC2_core_enthalpy_star: FAILS [NOISE-LIMITED]. The stellar term adds about 0.02 at 150–200 km/s, to 0.40. The text's own drop rule fires

Criteria: `FROZEN_CRITERIA.md`, committed alone first. `jc2.py`, `jc2_tail_add.py`, `jc2_read.py`, `jc2.out`, `jc2_RUN_results.json`. RM1's path, NR2 MEDIAN, EM1. κ = ½ FITTED, unused; no a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

## The text's numbers at δ +0.10, as written (literal) and normalised
| Quantity | Text | Literal | Normalised |
|---|---|---|---|
| Υ 150–200 | 0.52–0.55 | **0.40** | **0.40** |
| Υ 200–250 | | 0.46 | 0.48 |
| Υ dwarfs, 20–60, 60–100 | 0.50–0.58 | 0.66, 0.66 | 0.71, 0.70 |
| Υ 250–400 | 0.58–0.65 | 0.57 | 0.61 |
| Tilt | ≤ 0.15 | +0.22 | +0.24 |
| LITTLE THINGS | +0.05 to +0.07 | +0.068 | +0.077 |
| Groups Z | +0.55 | +0.50 | +0.54 |
| Clusters | identical to ZN4 | 12 of 15, X-COP −0.181 | 13 of 15, X-COP −0.127 |

LITTLE THINGS and groups land near the text's numbers, but those were already there at δ +0.10 with Blumenthal: this rule doesn't produce them. The bins and tilt miss. Closest to the Υ line, normalised at δ 0: Υ 0.50/0.51, tilt +0.28, LT +0.128; bins 0.78 0.75 0.58 0.40 0.50 0.66. No row clears.

**Drop rule, adopted from the text:** 150–200 km/s stays below 0.50. Dropped, no tweak of exponents or coefficients.

## How this reads
- The stellar term barely changes 150–200 (0.37–0.38 in JC1, 0.39–0.41 here). It moves 250–400 most, by up to +0.08.
- Clusters aren't identical to ZN4: M_s/M₀ at the edge has median 2.11, as in JC1.
- Limits: M★ share from `GB` columns, median 0.71 over SPARC. LITTLE THINGS at share 0, which favoured the claim. This grades a shell map. A barotropic field response that solves hydrostatic equilibrium with the baryons is a different calculation, and is not run, so "field, not particles" as such is untested.

My expectation on record held. Checks: K1 M★ 0 equals JC1, 0. K2 share in range. K3 star row differs. Read rerun byte-identical. MUTATE M★ × 0: K3 fails, exit 1. The twin runs one δ per form, so K3 compares with JC1 at δ −0.10; the first read script crashed on the twin for want of a δ 0 row, fixed before this README.

κ = ½ FITTED. Not theory closed.
