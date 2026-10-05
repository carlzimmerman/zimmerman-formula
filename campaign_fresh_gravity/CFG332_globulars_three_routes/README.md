# CFG332: the outer-halo globulars under three routes

The four outer-halo globulars are NGC 2419, Pal 3, Pal 4 and Pal 14. The criteria were frozen first, in commit 25fdb30f6 (`FROZEN_CRITERIA.md`). κ = ½ is fitted and held fixed. Both footings are used. The statistic is T: a two-sided, M/L-marginalised Fisher combination. A route counts as a MATCH only if T < 2σ on both footings. Nothing is pooled. Nothing was downloaded.

## The ownership rule in the record
FG001 (`CFG7_hierarchy_fg001.py` header; PAPER35 §2) splits systems into two classes:
- **Class E:** "formed embedded, without a cold component (tidal dwarfs, globular clusters, …): NEWTONIAN".
- **Class A (satellites):** "the ISOLATED law of their infall baryons, with NO external-field effect".

**The record decides globulars.** It puts them in class E, by listing them by name. The criterion is formation history, and it is already written down, so it is not a new postulate. Two things would be new postulates:
- an operational test for "formed embedded";
- moving the UFDs into class E.

## Results (T in σ, canonical / alt)

| route | T | verdict |
|---|---|---|
| 1(a) owned → Newton, SPS Υ 1.6 | 2.83 / 2.83 | NOT. All of it is Pal 3 (Newton predicts 0.44× its σ). Without Pal 3 it is 0.27 (not scored). |
| 1(b-EFE) = h93 (the rival reading) | 4.13 / 4.46 | NOT |
| 1(b-B) top-level, B's isolated law | 5.07 / 5.41 | NOT |
| 2 MF-slope stellar Υ, branch S | 2.55 / 2.84 | NOT (CONDITIONAL) |
| 2 MF-slope stellar Υ, branch K | 2.17 / 2.40 | NOT (CONDITIONAL). Just above the PARTIAL line of 2.07 / 2.23. |
| 3 full QUMOND EFE | 4.28 / 4.62 | NOT. The full EFE trims the boost *less* than the algebraic EFE: σ_num/σ_alg = 1.01 for Pal 14, 1.06 for Pal 3, 1.03 for Pal 4. |

**UFD matrix.** UFD columns are offset in dex, then z.

| classification | GC T | UFD |
|---|---|---|
| (a) as written | 2.83 | +0.325 (3.77) / +0.304 (3.55) |
| (b-B) | 5.07 / 5.41 | the same UFD row |
| (b-EFE) | 4.13 / 4.46 | +0.764 (4.58) / +0.748 (4.49) |

## Controls
**C1–C5: 12/12 pass.**
- h93 is reproduced: L 4.57 / 4.90, joint Υ 0.756 and 2.144, and Υ_F per cluster.
- Deep-MOND σ⁴ = (4/81) G M a₀ is recovered by the flux method (1.00000) and by the grid (0.9977).
- The EFE limit gives ν_e(1 + L/3), and Newton is recovered for y_ext ≫ 1.
- The grid agrees with the exact flux to 0.17%. Doubling the domain changes the result by 0.06%.
- The Kroupa input returns Υ = 1.6.

**MUTATE: 6/6.** Every route's T rises. The value 37.05 is the 1e-300 floor of the statistic.

## Lean
`CFG332_certificate.lean` holds 29 theorems, all proved by norm_num. It compiles with exit 0 and contains no `sorry`. It certifies only the arithmetic on inputs rounded outward from the results JSON.

## Run
```
python3 cfg332_globulars.py                      # ~10 s
CFG332_MUTATE=1 python3 cfg332_globulars.py      # needs the real run's JSON
python3 cfg332_lean_gen.py
cd fable_independent_2026/lean_2026 && lake env lean <abs path>/CFG332_certificate.lean
```
