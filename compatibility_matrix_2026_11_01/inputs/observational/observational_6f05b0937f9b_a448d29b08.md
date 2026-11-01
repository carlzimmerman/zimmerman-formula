# JC1_jeans_denominator: FAILS [NOISE-LIMITED]. M_s = M_c0 + M_c0(r₀) r/r₀ lifts 150–200 km/s only from 0.30 to 0.38, and tilt stays at +0.20 or above in every row. Its outer limit is false

Criteria: `FROZEN_CRITERIA.md` (f7d3813e8f), committed alone first. `jc1.py`, `jc1_tail_add.py`, `jc1_read.py`, `jc1.out`, `jc1_RUN_results.json`. RM1's path, NR2 MEDIAN, EM1. κ = ½ FITTED, unused; no a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

| Row | δ | Υ A/B | rms | tilt | Groups Z | LT | Υ by V_flat | Fails |
|---|---|---|---|---|---|---|---|---|
| Literal | +0.05 | 0.43/0.44 | 0.0737 | +0.22 | +0.97 | +0.093 | 0.67 0.65 0.52 0.37 0.45 0.56 | Υ, tilt |
| Literal | +0.10 | 0.43/0.44 | 0.0801 | +0.20 | +0.50 | +0.068 | 0.65 0.63 0.51 0.37 0.44 0.54 | Υ, tilt |
| Normalised | −0.05 | 0.50/0.50 | 0.0623 | +0.34 | +1.95 | +0.154 | 0.80 0.79 0.64 0.38 0.47 0.58 | tilt, LT |
| Normalised | +0.10 | 0.45/0.46 | 0.0753 | +0.26 | +0.54 | +0.077 | 0.70 0.70 0.54 0.38 0.46 0.57 | Υ, tilt |

Clusters: literal 12 of 15, X-COP −0.181; normalised 13 of 15, X-COP −0.127.

## How this reads
- **The r/r₀ dependence helps a little, and lifts dwarfs more than spirals.** Reads 2 and 3 of the criteria hold. 150–250 km/s stays at 0.37–0.48 at every δ.
- **The stated outer limit is false.** M_s/M₀ at the outer edge has median 2.11, range 1.87 to 163, not 1. So the rule weakens the whole halo, and clusters are not left alone: keys and X-COP move.
- As written the literal form over-contracts at the edge, shown by its lower X-COP and its 12 keys.

My expectation on record held. Checks: K1 M_s = M₀ equals NR3's `EM1|blum`, 1.4e-17. Read rerun byte-identical. MUTATE M_s = 2 M₀: |d| 0.11, K1 fails, exit 1.

κ = ½ FITTED. Not theory closed.
