# CFG405: does the Genzel+2017 residual tension survive outskirt cuts and inclination shifts? ROBUST (frozen reading)

Criteria `FROZEN_CRITERIA.md` were committed alone, with the LEDGER row, in 217aaa88ea. The script `cfg405_robustness.py` was committed before its first run, in 41824ba7d5. It ran once: single thread, niced, 33 s, peak RSS 0.41 GB. CFG402's statistic and the CFG401 primary shape (stars + gas at 2 R_d) are unchanged. κ = ½ FITTED; not theory closed. This is not an a0(z) measurement, and nothing here says the data favour the framework.

## Frozen result
**Controls 3/3 PASS:**
- K2: the rebuild equals CFG401's data bit for bit.
- K1: CFG402 is reproduced (max per-galaxy difference 0.0049; sums 7.987 / 9.634).
- K3: the planted outskirt defect is caught, 10.77 → −0.009 canonical (alt reported, 13.49 → 0.185).

**MUTATE** (errors halved) scales S ×4.00 on both footings (rc 1).

| variant | S_DE canonical | S_DE alt | class (can / alt) | zC 406690 alone (can / alt) | S_RIVAL can / alt |
|---|---|---|---|---|---|
| V0 baseline (= CFG402) | 7.99 | 9.63 | WEAK / REAL | 5.94 / 7.18 | 21.31 / 23.31 |
| V1 drop outermost point | 6.84 | 7.37 | WEAK / WEAK | 2.85 / 3.49 | 13.51 / 14.45 |
| V2 fold to the common two-sided extent | 5.34 | 5.54 | WEAK / WEAK | 1.35 / 1.65 | 9.96 / 10.67 |
| V3− inclination −10° | 4.56 | 5.24 | WEAK / WEAK | 2.50 / 2.97 | 16.48 / 18.73 |
| V3+ inclination +10° | 8.41 | 9.71 | WEAK / REAL | 6.51 / 7.43 | 18.24 / 19.77 |
| V4 zC 400569 at Lelli's 54.5° (reported) | 8.06 | 9.73 | WEAK / REAL | 5.94 / 7.18 | 21.34 / 23.32 |

**Nulls (200 draws each):**
- **N1 (random single drop, not the outermost):** 5th percentile 6.16 / 7.50. V1 sits at 6.84 / 7.37, below 21.5% / 4.5% of the draws. **V1 is NOT SPECIAL** (not below the 5th percentile on both footings).
- **N2 (random drops matched in count to V2):** 5th percentile 5.75 / 6.93. V2 sits at 5.34 / 5.54, below 2.0% / 0.5% of the draws. **V2 is SPECIAL.**

**Reading (frozen): ROBUST.** No graded variant reaches NOISE (S < 4) on either footing; the lowest is V3− canonical at 4.56. By the frozen statement-change rule, STANDING keeps "one ~2σ outlier (zC 406690)" and adds "robust to outskirt cuts and ±10° inclination".

## Selections (what each variant removed)
Five of the six galaxies have one side that reaches further than the other, and that side's last point is the outermost point. For those five, V1 and V2 remove the same single point. **V1 and V2 differ only for zC 406690:** V1 removes −1.207″, and V2 removes −1.018″ and −1.207″, the approaching-side tail beyond the receding side's last point at 0.922″.

## Post-hoc observations (labelled; do not change the frozen reading)
1. **Under V2 the residual is no longer one galaxy.** zC 406690's own penalty falls from 5.94 / 7.18 to 1.35 / 1.65 once its one-sided tail is folded out, and the matched null says that is more than random point loss. But dropping the outermost point *raises* the other five galaxies' summed penalty from 2.05 / 2.46 (CFG402) to 3.99 / 3.88. Their outermost points had been pulling *toward* the DE-tracking law: COS4 01351 best a0 goes x1.45 → x2.63, GS4 43501 x0.96 → x2.40, D3a 15504 x0.07 → x0.001. So the outskirts are not uniformly biased toward falling curves. The WEAK sum that survives V2 is spread over the sample, not carried by one object.
2. **Inclination.** zC 406690's penalty depends strongly on how the inclination is changed. With CFG401's construction (V and eV both divided by sin i, as frozen), it is 1.81 / 2.50 / 5.94 / 6.21 at 13 / 15 / 25 / 37°. CFG402's post-freeze check (V backed out of g_obs, errors held at 25°) gave 4.01 / 5.94 / 4.58 at 13 / 25 / 37°, and that construction was reproduced exactly here. The difference is the error treatment alone. At a lower inclination, zC 406690's penalty falls below 2.5.
3. **The rival a0 ∝ H(z)** still pays more than the DE-tracking law in every variant (S_RIVAL 9.96–23.32 vs S_DE 4.56–9.73). Pure Newton is penalised 13.6–17.8, so these discs still need a boost of about the local size.
4. **The Lelli inclination for zC 400569 (V4)** changes nothing (its penalty is 0.46 / 0.59).

## What this means for the record
- The frozen reading stands: **ROBUST.** The Genzel+2017 residual stays WEAK under every pre-registered cut and shift, never NOISE.
- The labelled post-hoc nuance: zC 406690's outlier status rests largely on its one-sided outer tail, the regime arXiv:2507.10544 flags. That tail is SPECIAL against matched random drops. Removing it does not remove the residual; it spreads it.
- Nothing here measures a0(z). The shapes are declared, there are 6–12 points per disc, CFG401's gate failed, and the kpc/″ scale, DE w0/wa and rival E(z) are inherited inputs.

## Files
`FROZEN_CRITERIA.md`, `cfg405_robustness.py` (run plainly, then with `MUTATE=1`), `cfg405.out`, `cfg405_results.json` (every variant, row, null draw and selection), `cfg405_MUTATE.out`, `cfg405_results_MUTATE.json`.
