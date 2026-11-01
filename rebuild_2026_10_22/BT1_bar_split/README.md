# BT1_bar_split: UNBARRED SHARE THE MISS. Unbarred spirals at 150–250 km/s also sit below Υ 0.40, so bars aren't what makes the miss, on this classification. A smaller bar effect isn't excluded

Criteria: `FROZEN_CRITERIA.md` (c2bed2da87), committed alone first. `bt1.py`, `bt1_tail_add.py`, `bt1_read.py`, `bt1.out`, `bt1_RUN_results.json`. Path: EM1, δ 0, Blumenthal, NR2 MEDIAN. Bar family: Buta et al. 2015 S4G ⟨F⟩, already in the repo. κ = ½ FITTED, unused; no a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

| 150–250 km/s, median Υ, A / B | Unbarred F < 0.5, n 10 | Barred F ≥ 0.5, n 13 | p A / B |
|---|---|---|---|
| **Blumenthal, primary** | **0.38 / 0.38** (4 at floor) | **0.30 / 0.30** (7 at floor) | 0.047 / 0.074 |
| Blumenthal, F > 0.5 only, n 7 | 0.38 / 0.38 | 0.35 / 0.35 (3 at floor) | 0.71 / 0.62 |
| Response off, control | 0.66 / 0.67 | 0.58 / 0.58 | 0.52 / 0.47 |

My expectation on record held. The label needs unbarred ≥ 0.50 for a bar-carried miss; unbarred is 0.38.

## How this reads
- **The direction is the one a bar picture would not want to be sole cause of:** unbarred is already under the line. Barred is lower still, but that gap is about the size of the control's gap with the response off, so it isn't shown to come from the response.
- **The primary p is marginal and doesn't survive:** 0.047 on A, 0.074 on B, and the strict split loses it (SAB galaxies carry it).
- **Limits.** 20 of 43 band galaxies have no S4G class and aren't imputed, including NGC 0891, NGC 6946 and NGC 7331. The Υ floor censors both sides, 4 and 7 at the floor. Today's bar class isn't the disc's bar history. This tests the sign on a small sample, not a bar model.

## Checks
K1 bin medians equal NR3 MEDIAN's within 10⁻⁶. K2 43 in band, 23 classified. K3 F in range. Rerun byte-identical. MUTATE F shuffled: K2 fails, exit 1.

κ = ½ FITTED. Not theory closed.
