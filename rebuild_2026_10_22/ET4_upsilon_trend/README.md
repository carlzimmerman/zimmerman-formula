# ET4_upsilon_trend: Υ alone does not explain the low-mass rise; it can reach the top bin but not the bottom one

Criteria: `FROZEN_CRITERIA.md` (08a1036a74, committed alone). Numbers: `et4.out`, `et4_results.json`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## Frozen verdict: NOT EXPLAINED BY Υ
This covers Υ alone. Trend family Υ = 0.50 (V_flat / 80)^s; s = 0.25 is the largest counted as allowed by the declared ±0.11 dex yardstick.

- **Test 1, real curves with a trend:** s 0.25 ρ +0.527, SURVIVES. s 0.5 ρ +0.476, SURVIVES. s 1 ρ +0.257, p 0.031, ERASED, but with 36 galaxies clipped at the grid's end, and far beyond the band.
- **Test 2, Υ-insensitive galaxies: UNDERPOWERED.** Only 13 galaxies have f★ < 0.5 (the frozen minimum is 20), V_flat 34–86. Their ρ +0.499, p 0.083, so it decides nothing. The rest (n 57) rise at ρ +0.367, p 0.0062.
- **Test 3, needed Υ at the floor: OUT** on all three bins, both footings: canonical 0.69, 0.93, 0.75; alt 1.07, 0.68, 0.70. Weakly constrained: 26–60 % of galaxies in the two lower bins sit at a grid end. Fit is worse than free S by a median ×2.0–3.0 in those bins and ×1.1–1.2 at 100–150.
- **Test 4, forward from a flat floor:** PARTIAL in all six cases, none FAKED.

| Flat truth, fit at Υ 0.50 | 20–60 | 60–100 | 100–150 |
|---|---|---|---|
| Real curves (ET2) | 70.2 | 107.7 | 157.5 |
| Canonical, s 0.25 | 107.7 | 107.7 | 112.9 |
| Canonical, s 1 | 102.7 | 107.7 | 150.2 |
| Alt, s 0.25 | 124.2 | 130.2 | 136.6 |
| Alt, s 1 | 124.2 | 130.2 | 165.2 |

## How this reads
1. **Υ acts on the top of the rise and not the bottom.** A trend lifts 100–150 well, and alt reaches 136.6 inside the allowed band. No trend pulls 20–60 below 102, against 70 observed.
2. **This changes a line in ET3.** ET3 called the 100–150 excess the harder part. It is hard for pressure and beam, but an in-band Υ trend reaches the lower edge of its interval on alt. Canonical needs s near 1.
3. **Each systematic reaches one end.** Upper-bound pressure support softens the 20–60 deficit (ET3) and Υ softens the 100–150 excess (here). **They have not been tested together**, so this lane does not show that the floor fails against the combination. That joint test is the open door.
4. Test 3's needed Υ at 20–60 is above the band, the opposite direction from the low Υ a positive trend gives there. With so many fits at grid ends, this is a weak reading.

## Limits
One-parameter trend in V_flat, with no colour or age data. The band is a yardstick, not measured here. Test 2 lacks power. One core shape. Gas masses as given.

## Checks
K1 equals ET2 per galaxy, K2 6.7e-16, K3 exact: all pass. MUTATE truth s 0.5: correct trend ρ −0.058, p 0.625; fit at Υ 0.50 ρ +0.704: bites.
