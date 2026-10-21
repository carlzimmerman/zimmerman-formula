# AG4d: n=2's ALMA gas predictions, SEALED 2026-10-20 (before the 2026-11-06 and 11-28 releases)

- **Seal:** `SEALED_N2.json`, sha256 `d64727b54b07b31c22386ad49afa6c0529ab1d77898b3d8aaef02d0ecc12a996` (in
  `PREDICTIONS_HASH.txt`). Never edit either file after a release.
- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (11ae8a3b6).
- **Gate:** open. AG4b and AG4c both returned "n=2 survives".
- **Run:** `python3 ag4d.py`, exit 0. `AG4D_MUTATE=1` exits 1 (Newtonian kernel; F-DESI vs R-H collapses; nothing sealed).
- **Settings:** κ = ½ fitted; not theory closed. **Sealing n=2 does not adopt it:** the canonical statement keeps n=1 unless
  the owner decides otherwise.
- **Method:** CFG571's prediction code, executed read-only as CFG778 does, with the kernel swapped to
  ν₂ = √(1 + 1/y). There are seven a₀ branches (E, E-CCBH, F-flat, F-DESI, BH-k3, R-H, L-fb), both footings, and both gas
  shapes.
- **K1:** with ν_mono the code reproduces every sealed CFG571 and CFG778 number exactly (0.0 dex over 180 entries).

## GS4_24110 (z 1.997, resolved [CI], public 2026-11-28): required total log M_gas (R_g = R_d), canonical / alt
| branch | n=2, log M* 10.89 | sealed ν_mono | n=2, log M* 10.76 | sealed ν_mono |
|---|---|---|---|---|
| F-flat | 10.12 / 9.95 | 9.46 / FLOOR | 10.52 / 10.46 | 10.36 / 10.24 |
| F-DESI | 10.21 / 10.08 | 9.82 / 9.11 | 10.56 / 10.51 | 10.43 / 10.33 |
| BH-k3 | 10.22 / 10.10 | 9.87 / 9.31 | 10.57 / 10.52 | 10.44 / 10.34 |
| E (event horizon) | 9.57 / FLOOR | FLOOR / FLOOR | 10.38 / 10.26 | 10.06 / 9.75 |
| R-H (a₀ ∝ H) | FLOOR / FLOOR | FLOOR / FLOOR | 8.42 / FLOOR | FLOOR / FLOOR |

- Under n=2 every framework branch needs about 0.1–0.6 dex more gas than the sealed ν_mono numbers, because n=2 gives less
  boost in the transition regime.
- At log M* 10.89, the rival R-H is still FLOOR in every case, so the sign of the test is unchanged.
- Reported, not sealed: under the action's own n=1 law, ν₁ (simple), the framework needs less gas than ν_mono. For example,
  F-DESI at 10.89 needs 9.53 / FLOOR. The full grid is in `ag4d_results.json`.

## U4_27928 (z 1.419, CO, public 2026-11-06)
- This target is conditional on the CO-measured V_c at 2R_e = 8.27 kpc.
- Below 225 km/s every branch is FLOOR.
- At 225 km/s, n=2's framework branches need log M_gas 9.9–10.2 (canonical), while R-H stays FLOOR.
- The full V_c grid is in `ag4d.out` and the seal.
