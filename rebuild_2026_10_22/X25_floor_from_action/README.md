# X25_floor_from_action: X24's velocity floor is NOT the v3s held medium's sound speed

Criteria: `FROZEN_CRITERIA.md` (230c922864, committed alone; one envelope number disclosed). κ = ½ FITTED. Footings never
pooled. No new constant. Not "theory closed". Nothing here says the data favour the framework.

## Verdict: WRONG SIGN (both footings)

The action's own small-scale term goes the wrong way on all three counts:

| test | canonical | alt | needed |
|---|---|---|---|
| D2 sign: median ΔE from switching L★ on, 69 dwarfs | −0.063 / −0.075 / −0.341 dex (L★ floor / 24 / 90) | −0.074 / −0.081 / −0.366 | > 0 (a floor) |
| D1 size: c_s = √(2πGρ₀) L★ at 24 pc, by class | 0.60–0.90 km/s | 0.62–0.95 | c₀ 4.6 [4.0, 5.1] / 4.1 [3.4, 4.7] |
| L★ needed to reach c₀ | 123–182 pc | 102–156 pc | (and D2 is worse there) |
| D3: c_s(UFD) / c_s(others) at 24 pc | 1.45 | 1.44 | < 1 (UFDs want 3.5 vs 4.6) |

- **Sign.** The held medium's pressure is the screening that makes v3s Newtonian inside L★. It removes phantom mass at
  small radii, so the predicted σ goes down, not up. The larger L★, the worse every dwarf class gets (UFDs −0.53 dex at
  90 pc).
- **Size.** At the allowed L★ the sound speed is 5–7 × too small.
- **Direction.** c_s² ∝ phantom density, and the ultra-faints are the densest (0.05 M☉ pc⁻³), so they get the largest c_s.
  They need the smallest.

**Checks 5/5** (K0 X24 and X19 reproduced; K1 ZT11's c_s at R₀ to 3 %; K2 the deep-MOND density identity; K3 0.04 GB).
`--mutate` (c_s² × 2) fails K1, exit 1.

## Parameter-space consequences

1. **c₀ is not in the action.** X24's floor stays a phenomenological lead with one new constant. It is not adopted. No v3s
   term can produce it: the only small-scale term, γ_L, has the wrong sign. Any floor needs a different sector,
   temperature-keyed rather than density-keyed, and that is a new constant.
2. **The dwarfs push L★ to its floor.** Every increase of L★ lowers every dwarf prediction monotonically, by 0.06 dex at the
   floor and 0.34–0.37 dex at 90 pc, while the dwarfs already sit above the law. This agrees with CFG821 (dSphs want
   L★ ≤ 22 pc). With the outer-globular floor 21.7 / 22.9 pc (D10), L★ is squeezed from a lower bound to a narrow band
   at the floor. **L★ is effectively fixed, not free.** (A frozen joint bound is not computed here.)
3. **Hosted vs field (X24) stands.** The dwarf rows need no host selector. What remains is a mass-graded excess that no
   term of v3s supplies.

## Files

`FROZEN_CRITERIA.md`, `x25_floor_from_action.py`, `.out` / `_results.json`, `_MUTATE` outputs.

    OMP_NUM_THREADS=1 python3 x25_floor_from_action.py            # exit 0, 5/5
    OMP_NUM_THREADS=1 python3 x25_floor_from_action.py --mutate   # exit 1, K1 fails
