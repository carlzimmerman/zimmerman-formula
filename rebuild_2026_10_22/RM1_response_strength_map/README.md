# RM1_response_strength_map: NO CELL [NOISE-LIMITED ANCHOR]. No response strength f, flat or inner-only, clears all five gates at any δ on NR1's anchors

Criteria: `FROZEN_CRITERIA.md` (df19459ebe), committed alone first. `rm1.py`, `rm1_tail_add.py`, `rm1_read.py`, `rm1.out`, `rm1_G_results.json`, `rm1_I_results.json`. UR2's path, read only. A requirement map, not a mechanism: f and δ are FITTED. κ = ½ FITTED, unused. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

## Result
180 cells (G 132, I 48), none clears. My expectation on record: none in G; none in I, held without confidence. Both held.

Gates: Υ 0.50–0.80 with rms ≤ 0.110; |tilt| ≤ 0.15; groups CONSISTENT; |LITTLE THINGS| ≤ 0.10; δ in −0.10 to +0.14. All values are background A.

| Cell | Υ | tilt | Groups Z | LT | Fails |
|---|---|---|---|---|---|
| G1.0, δ +0.05 (fewest failed, first met) | 0.33 | +0.13 | +1.03 | +0.078 | Υ |
| G1.0, δ +0.10 | 0.32 | +0.10 | +0.55 | +0.052 | Υ |
| G0.4, δ +0.10 | 0.50 | +0.29 | +0.54 | +0.072 | tilt |
| G0.3, δ +0.10 | 0.54 | +0.35 | +0.54 | +0.075 | tilt |
| G0.0, δ +0.10 | 0.70 | +0.57 | +0.53 | +0.091 | tilt |
| I0.00, δ +0.10 | 0.54 | +0.58 | +0.53 | +0.077 | tilt |

## How this reads
- **Υ against tilt is the wall.** Inside the mass window with groups and LITTLE THINGS passing, lowering f raises Υ and the tilt together. Every Υ ≥ 0.50 cell there has tilt ≥ +0.29, every |tilt| ≤ 0.15 cell has Υ ≤ 0.38.
- **Restricting the weakening to the inner disc doesn't help.** Family I is worse on tilt than G at the same Υ.
- **Clusters are not improved by weakening:** keys fall from 14 at f 1 to 12 at f 0. G-IN-Mall fails in every family, at every f.
- Bins for the fewest-failed cell, 20–60 to 250–400 km/s: 0.41, 0.48, 0.42, 0.30, 0.35, 0.47. A single f per cell can't lift 150–250 alone; a mass-dependent f is outside this family.

## Checks
K1 and K2 true, K3 true. Rerun of the read byte-identical. MUTATE f → 1 − f: K1 FAIL, exit 1, as required.

**[NOISE-LIMITED ANCHOR]:** NR1 PRIMARY only, as frozen. The label text in `rm1.out` says NR2 is unread, which was true when frozen; NR2 has since landed and the criteria require a rerun on it.
