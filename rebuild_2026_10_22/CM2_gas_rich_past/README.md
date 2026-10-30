# CM2_gas_rich_past: CADENCE-DEPENDENT (not a pass)

Criteria: `FROZEN_CRITERIA.md` (4d982680f1), committed before any script or number. Closed-box gas tied to stars formed,
moved mass capped by each burst's supernova energy at coupling 1, all gas starting at the stellar scale (ceilings).

| run | bursts, period | moved mass / M200, first/median/last | ε_used | R at 10 Gyr (needed ≤ 0.817) |
|---|---|---|---|---|
| C40 (primary) | 40, 250 Myr | 0.0185 / 0.0185 / 0.0156 | 0.994 | **0.898** miss |
| C10 (declared bracket) | 10, 1 Gyr | 0.0773 / 0.0488 / 0.0203 | 0.603 | **0.573** reaches |
| MUTATE (C10, cap × 0.01) | 10, 1 Gyr | 0.0007 throughout | 0.010 | 0.985 |

K1 reproduces CM1 PRIMARY exactly (η 23.275). K2 ≤ 1.2e-5. K3 and MUTATE pass.

## Reading
- At 250 Myr cadence the energy cap binds, not the gas supply: a gas-richer past barely helps (0.932 → 0.898).
- At 1 Gyr cadence the same supply reaches the target within the first 1.25 Gyr (R 0.642) and overshoots. Moved mass
  sets the heating, as a second-order effect should.
- Nothing in the theory sets the cadence, so this is an undetermined input, not a derivation.
- C10's first burst lifts every baryon, the gas and all stars-to-be, from the stellar scale at coupling up to 1. That is
  a ceiling, not a galaxy history.

Same limits as CM1: one galaxy, one seed, spherical, prescribed histories, halo formed at t = 0. κ = ½ FITTED. Not theory
closed. Cold dark energy is a gravitating field component, never a particle.
