# ET6_core_shape: the rise does not depend on the core chosen; no cell of 72 reconciles the flat floor; canonical's containment depends on how S is defined

Criteria: `FROZEN_CRITERIA.md` (1311529245, committed alone). Numbers: `et6.out`, `et6_results.json`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework, a footing or a shape.

## Frozen verdicts
- **Rise: RISE IS SHAPE-FREE.** ρ +0.556 SMOOTH, +0.563 BURKERT, +0.518 PISO, +0.558 STEEP, all p < 5e-5.
- **Fit guard:** all four count. Median mse relative to SMOOTH: BURKERT 0.91, PISO 0.83, STEEP 1.35. Not read as evidence for a shape.
- **Canonical: DEFINITION-DEPENDENT.** Literal S: FLOOR CONSISTENT, RISE REMAINS, only through PISO with σ 12 and the 30″ cut (s 0, 0.25 and 0.5). Normalised to equal gravity at r₀: NOT RECONCILED.
- **Alt: FLOOR CONSISTENT, RISE REMAINS** under both definitions, every containing cell having σ 12 and the 30″ cut.
- **No cell is RECONCILED** on either footing, either definition, or any shape. In every containing cell the rise stays significant.
- **Forward, truth shape fitted with SMOOTH:** none of 12 FAKED; PARTIAL 8, NOT FAKED 4.

| Literal S, base cell | 20–60 | 60–100 | 100–150 | Top / bottom |
|---|---|---|---|---|
| SMOOTH | 70.2 | 107.7 | 157.5 | 2.2 |
| BURKERT | 93.4 | 150.2 | 241.6 | 2.6 |
| PISO | 51.6 | 81.0 | 130.2 | 2.5 |
| STEEP | 79.1 | 130.2 | 190.5 | 2.4 |

## How this reads
1. Changing the core moves S up or down as a whole and leaves the rise at about ×2.2–2.6.
2. Canonical's one route to containing the floor needs the outer r⁻² core, the literal S reading, the upper-bound pressure term and the beam cut together. Whether the floor carries to another shape at the same number is a choice, not derived, and the normalised reading removes it.
3. Shape mismatch alone can tilt: flat PISO truth fitted with SMOOTH reads 81.0, 93.4, 112.9, ρ +0.421, about ×1.4. Same size as the other systematics, short of ×2.2.

## ET1–ET6 taken together
S rises by about ×2 from V_flat 20–60 to 100–150 km/s. It survives removing M200, beam, pressure, inclination, distance and quality cuts, a Υ trend, their joint grid, and four core shapes. No tested combination removes it, and systematics reproduce at most about ×1.4 from a flat truth, each failing to match both ends together.

It does **not** reject the flat floor outright: the frozen floor grade stays MIXED at the uncorrected base on SMOOTH, intervals are wide, and generous corners contain alt's floor. It identifies no mechanism, and it says nothing about route E's other keys. Not tested: real per-galaxy beams, 3D modelling, non-circular motions, or core families outside these four.

## Checks
K1 equals ET2; K2 1.8e-14; K3 2.6e-14, no saturated halos; K4 exact: all pass. MUTATE Burkert truth fitted with Burkert: 107.7 in all bins, ρ +0.066, p 0.59.
