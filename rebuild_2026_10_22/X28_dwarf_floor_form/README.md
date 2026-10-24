# X28_dwarf_floor_form: the dwarf extra does not key to acceleration. Swapping c₀ for η a₀ fails.

Criteria: `FROZEN_CRITERIA.md` (32d4323f88, committed alone; **POST-HOC**, envelope disclosed). κ = ½ FITTED. Footings
never pooled. One constant per form, calibrated on the 13 LG field dwarfs only. Not "theory closed". Nothing here says the
data favour the framework.

## Verdict (frozen rule): UNDECIDED (labels differ only by the [SPARC-COST] tag)

The core class is **VELOCITY FLOOR on both footings**. Canonical carries [SPARC-COST], alt does not, so the frozen
both-footings rule returns UNDECIDED. In substance the result is not in doubt: the acceleration floor loses by a wide
margin.

| | canonical | alt |
|---|---|---|
| F_v c₀ (field) | 4.59 [4.01, 5.14] km/s | 4.05 [3.41, 4.66] |
| F_g η (field) | 0.027 [0.017, 0.037] | 0.011 [0.003, 0.019] |
| χ²_H: law / F_v / F_g (N 61, out of sample) | 637 / **217** / 327 | 559 / **195** / 389 |
| Δχ²_H (F_v − F_g) | **−110** | **−195** |
| UFD residual under F_g | +0.35 ± 0.10 (Z +3.4, undershoot) | +0.42 ± 0.11 (Z +4.0) |
| M31 others under F_g | Z +2.2 | Z +2.2 |
| η in-sample on H vs field | 0.070 vs 0.027: **no overlap** | 0.054 vs 0.011: **no overlap** |
| power law g_floor ∝ r₁₂^(−n), all 82 (reported) | **n = 0.78 [0.73, 0.83]** | **n = 0.80 [0.75, 0.85]** |
| SPARC cost of F_g at 0.1 a₀ | 0.10 dex [SPARC-COST] | 0.045 dex |

**Checks 7/7** (K0 X24 c₀ and X19 medians; K1 the law limit; K2 recovers an injected η = 0.1; K3 0.12 GB). `--mutate`
fails K0, exit 1.

## Reading

- **No parameter reduction here.** An acceleration floor on the theory's own a₀ cannot replace c₀:
  - the field dwarfs want 2.5–5 × less η than the hosted ones;
  - the ultra-faints are then undershot by 3–4σ, so the overshoot just flips sign;
  - on canonical it costs SPARC's outskirts 0.1 dex.
- **Neither pure form is right.** The free power law prefers n ≈ 0.8 (68 %: 0.73–0.85) on both footings. That excludes
  n = 0 (acceleration) and also n = 1 (velocity). The extra scales between the two, as g_floor ∝ r^−0.8. That is the
  same tension as X24's UFD overshoot, now stated as an exponent.
- **My envelope (§5) was wrong:** it used the hosted classes, not the field dwarfs, and the field wants much less η. The
  frozen calibration-on-field design caught this. That is what it is for.
- **Parameter status unchanged:** the dwarf rows need one dimensionful velocity-like constant, c₀ ≈ 4–5 km/s. It is not
  in the action (X25), not a₀-scaled (X28), and its scaling exponent is about 0.8, not 1. It stays a lead, not adopted.

## Files

`FROZEN_CRITERIA.md`, `x28_dwarf_floor_form.py`, `.out` / `_results.json`, `_MUTATE`.

    OMP_NUM_THREADS=1 python3 x28_dwarf_floor_form.py            # exit 0, 7/7
    OMP_NUM_THREADS=1 python3 x28_dwarf_floor_form.py --mutate   # exit 1, K0 fails
