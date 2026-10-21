# AG4e: the action's own n=1 law's ALMA gas predictions, SEALED 2026-10-20 (before the 11-06 and 11-28 releases)

- **Seal:** `SEALED_N1.json`, sha256 `9802de0d170ccaea7116af91c8a93dc05f72ca1a50bb52d46504f0ed8261538c` (in
  `PREDICTIONS_HASH.txt`). Never edit either file after a release.
- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (49a975e81). Owner's direct go; no gate.
- **Run:** `python3 ag4e.py`, exit 0; `AG4E_MUTATE=1` exits 1 (it bites; nothing sealed).
- **Settings:** κ = ½ fitted; not theory closed.
- **Method:** AG4d's method with kernel ν₁ = (1 + √(1 + 4/y))/2, the frozen S2 rest state g_N = g²/(g + a₀).
- **Controls:**
  - K1: ν_mono reproduces every sealed CFG571 and CFG778 number exactly (180 entries).
  - K2: the ν₁ identity holds.
  - K3: the grid equals AG4d's reported n=1 grid exactly.

## The three sealed laws side by side: GS4_24110, required total log M_gas (R_g = R_d), canonical / alt
| branch | log M* | n=1 (this seal) | ν_mono (CFG571/778) | n=2 (AG4d) |
|---|---|---|---|---|
| F-flat | 10.89 | FLOOR / FLOOR | 9.46 / FLOOR | 10.12 / 9.95 |
| F-DESI | 10.89 | 9.53 / FLOOR | 9.82 / 9.11 | 10.21 / 10.08 |
| F-flat | 10.76 | 10.30 / 10.18 | 10.36 / 10.24 | 10.52 / 10.46 |
| F-DESI | 10.76 | 10.37 / 10.27 | 10.43 / 10.33 | 10.56 / 10.51 |
| R-H | either | FLOOR (all) | FLOOR (all) | FLOOR, except 8.42 canonical at 10.76 |

## Reading
- The required gas is ordered by law, **n=1 < ν_mono < n=2**: the less boost a law gives in the transition regime, the more
  gas it needs.
- So GS4_24110's resolved gas is also a law-form test: little gas favours n=1, and about 10¹⁰ M☉ or more favours ν_mono or n=2.
- That reading is conditional on the stellar-mass branch, which moves every number by up to 0.6 dex.
- The rival a₀ ∝ H(z) stays FLOOR under all three laws at log M* 10.89.
- U4_27928's full V_c grid is in `ag4e.out` and the seal. Under n=1 the framework branches first need gas at V_c = 225 km/s
  (F-DESI 9.65 canonical).
