# X27_joint_lstar_band: the dwarfs do not pin L★ independently. The "pin" is the dwarf shortfall.

Criteria: `FROZEN_CRITERIA.md` (4bf6612dc5, committed alone). `A1` (post-result, reported only): one extra printed line
(error-scaled M0 bound). RUN1 is kept, identical apart from that line. κ = ½ FITTED. Footings never pooled. Not "theory
closed". Nothing here says the data favour the framework.

## Verdict (frozen rule): PINNED [SHORTFALL-DRIVEN], both footings

| | canonical | alt |
|---|---|---|
| lower: outer-globular floor (D10, read) | 21.682 pc | 22.849 pc |
| M0 literal v3s: L★,up | 21.80 pc | 22.97 pc |
| M0 fit quality | χ²/N **53.3** | χ²/N **50.8** |
| A1: M0 with errors scaled by √(χ²/N) | 26.6 pc (in the coarse 24–90 segment) | 27.1 pc |
| M1 v3s + floor (c₀ profiled 5.8–6.3 km/s): L★,up | **none to 90 pc** (χ² 643.9 → 645.6) | **none** (alt prefers 90: 695.7 → 690.0) |

## Reading

- **The frozen label overstates it.** M0's band is set by a model that fails the dwarfs at χ²/N ≈ 51–53. A Δχ² = 3.84
  bound on such a fit measures how fast a bad fit gets worse, not where L★ is. Even with the errors scaled up 7×, the
  bound (≈ 27 pc) comes entirely from the shortfall. Screening deepens a deficit that is already 0.3–1.5 dex.
- **Supply the shortfall and the bound disappears.** Once a floor (or any extra) absorbs the excess, χ² is flat in L★
  to 90 pc on both footings. CFG821's warning is confirmed quantitatively: the dwarf "upper bound" on L★ is the mass
  shortfall in disguise.
- **Parameter-space result: no reduction from the dwarfs.** L★ stays a one-sided bound, ≥ 21.7 / 22.9 pc from the outer
  globulars. The dwarfs can pin it only in a theory that also explains their excess. In v3s it is pinned only if one
  accepts v3s failing them by 50× in χ².
- Grid caveat: X1 carries L★ ∈ {floor, 24, 90} only. Anything between 24 and 90 pc is interpolated linearly in log L★.
  The class medians show the screening is nearly flat to 24 pc and rises steeply toward 90.

**Checks 9/9** (K0 X19 medians, N = 82 and the doc floor; K1 grid round trip; K2 M1 at c₀ = 0 equals M0; K3 0.07 GB; K4
χ² non-decreasing from the floor to 24 pc). `--mutate` (screening sign flipped) fails K4 on both footings, exit 1.

## Files

`FROZEN_CRITERIA.md`, `x27_joint_lstar_band.py`, `.out` / `_results.json`, `_RUN1` (before A1), `_MUTATE`.

    OMP_NUM_THREADS=1 python3 x27_joint_lstar_band.py            # exit 0, 9/9
    OMP_NUM_THREADS=1 python3 x27_joint_lstar_band.py --mutate   # exit 1, K4 fails
