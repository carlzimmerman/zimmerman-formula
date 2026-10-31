# ET5_joint_upsilon_pressure: canonical's flat floor is not reconciled in any of 18 cells; alt's is contained in one allowed cell, but the rise remains

Criteria: `FROZEN_CRITERIA.md` (d197332756, committed alone). Numbers: `et5.out`, `et5_results.json`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework or either footing.

## Frozen verdicts
- **Canonical (floor 106.85): NOT RECONCILED.** No cell of 18 has all three intervals containing the floor, even at the generous corners.
- **Alt (floor 129.13): FLOOR CONSISTENT, RISE REMAINS.** One allowed cell contains it: s 0.25, σ 12, 30″ cut, with intervals [74, 143], [93, 143], [124, 182]. Its rise is still ρ +0.404, p 0.0009. One cell beyond the band (s 0.5) does the same, ρ +0.371, p 0.0027.
- **Rise:** significant at p < 0.01 in all 18 cells, ρ +0.371 to +0.556. No cell is RECONCILED on either footing.
- **Forward: PARTIAL in all 16 cells, none FAKED.**

| Fit or truth | 20–60 | 60–100 | 100–150 |
|---|---|---|---|
| Real, no correction | 70.2 | 107.7 | 157.5 |
| Real, s 0.25, σ 12, 30″ | 93.4 | 115.7 | 150.2 |
| Flat canonical, s 0.5, σ 12, 30″ | 77.2 | 93.4 | 107.7 |
| Flat alt, s 0.5, σ 8, no beam | 115.7 | 124.2 | 150.2 |

## How this reads
1. **By the frozen reading, for canonical:** NOT RECONCILED with no FAKED cell means the rise stands against the flat floor given these systematics and this core shape. It identifies no mechanism and is not a rejection of route E.
2. **What sinks canonical is the top bin.** Its lower edge never falls below 118 against 107. The miss is modest, so a further error of about 10 % there could move this verdict.
3. **Alt is not a pass.** A higher floor sits inside wide intervals at one generous corner, using an upper-bound pressure term. The rise remains. This is no reason to prefer alt over canonical.
4. **Significance alone does not separate the cases.** All 16 forward cells from a flat truth give a significant tilt, ρ +0.41 to +0.75, as large as or larger than the real ρ. So ρ and p do not show physics; only the size does. Flat truth gives up to about ×1.4 across the bins, and the real curves about ×2.2 uncorrected. None reproduces both ends together: canonical reaches the bottom (77.2) with the top at 107.7; alt reaches the top (150.2) with the bottom at 115.7.

## Limits
Cell search is not corrected for multiplicity, on purpose favouring reconciliation. h = Rdisk for all, σ constant. Beams bracketed; 1D forward beam. One-parameter trend, no colour data. One core shape, the largest thing untested: every S here is defined through it. Distance and inclination errors are not in the grid (ET3 tested them alone). Combinations with Q and inclination cuts are not in the grid either.

## Checks
K1 equals ET2 per galaxy; K2 reproduces ET4 s 0.25, ET3 P12 and B30: pass. MUTATE planted canonical floor with s 0.25, σ 12, fit with exact correction: 107.7 in all bins, ρ −0.011, p 0.93.
