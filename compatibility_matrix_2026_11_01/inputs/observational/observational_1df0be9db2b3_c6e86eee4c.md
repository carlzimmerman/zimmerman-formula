# UR2_response_mass_pinch: PINCHED. With the adiabatic response, Υ reaches 0.50 only at δ −0.30, three times past blue lensing's limit, and every other SPARC-side gate wants the opposite direction

Criteria: `FROZEN_CRITERIA.md` (7d8174a855), committed alone first. `ur2.py`, `ur2_tail_add.py`, `ur2_read.py`, `ur2.out`, `ur2_results.json`. δ is an inversion, **FITTED**, never derived. κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. NR2 unread: rerun when it lands.

## Result, Blumenthal, canonical, lg M200 = EM1 + δ
| δ | Υ A/B | rms | tilt | groups Z | LITTLE THINGS |
|---|---|---|---|---|---|
| −0.30 | 0.53/0.50 | 0.0765 | +0.45 | +4.26 ABOVE LAW | +0.229 |
| −0.10 (blue's 2σ edge) | 0.39/0.39 | 0.0630 | +0.19 | +2.43 ABOVE LAW | +0.147 |
| 0 (UR1) | 0.35/0.35 | 0.0671 | +0.16 | +1.50 | +0.105 |
| +0.10 | 0.32/0.33 | 0.0780 | +0.10 | +0.55 | +0.052 |
| +0.15 | 0.30/0.31 | 0.0852 | +0.06 | +0.08 | +0.026 |

- **δ_Υ = −0.30** against blue's 2σ lower bound −0.10 (blue +0.03; red +0.32; all +0.26). **Frozen label: PINCHED.** Gates at δ_Υ also fail: tilt, groups, LITTLE THINGS.
- **Gnedin (alternate):** δ_Υ −0.22, also PINCHED.
- **Off (comparator):** Υ 0.67–1.12 over the whole grid, tilt +0.46 to +0.59 everywhere.
- **By V_flat, Υ 0.50 crossing, Blumenthal, background A:** −0.09, +0.03, −0.03, none on the grid, −0.41, −0.13. The 150–200 km/s bin never reaches 0.50 down to δ −0.50. So the miss is concentrated at 150–250 km/s.

My expectation was δ about −0.1, near the edge. **That was wrong:** the pinch is wider than I expected. Tilt and LITTLE THINGS failing at δ_Υ was as expected.

Keys and X-COP don't read this map and stay at UR1's values, 14/15 with G-IN-Mall −2.05 and X-COP −0.097, 0.146. No row here passes as a whole.

## Reported after the result, not graded
- **Opposite pulls.** Lower δ raises Υ. Higher δ improves tilt, groups and LITTLE THINGS, and is the direction KiDS wants. Near δ +0.10 to +0.15, inside or just above blue's +0.14 and below red's and all's, tilt, rms, groups and LITTLE THINGS all clear their lines, and Υ alone fails at 0.30–0.33. That is a δ picked after seeing the table, on a fitted line.
- **So the SPARC-side miss of EM1 + response is one number:** too much cold mass inside the stars, worst at 150–250 km/s. This does not rescue anything: moving the Υ line isn't allowed, and whether a measured stellar mass-to-light could sit near 0.3 isn't tested here.
- Lensing is read across from BL1 on FC1's core, not regraded, and BL1's shape misfit stands (χ² 109 against the law's 27.5 for blue).

## Limits
One global offset, slope unchanged; a mass-dependent δ could split bins but adds a fitted number. Adiabatic response and baryons starting as tracers are assumed. Core shape by hand; ANCHOR-DEPENDENT low masses.

## Checks
K1 off, δ 0 vs UR1's row (= NR1 PRIMARY): |d| 0. K2 Blumenthal, δ 0 vs UR1, including groups: |d| 0. K3 Υ monotonic in δ: yes on the Blumenthal grid. MUTATE M_b × 2 in the response only: Υ never reaches 0.50 on the grid, so δ_Υ moves.
