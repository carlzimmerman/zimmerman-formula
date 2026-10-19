# CFG854 — symbolic regression (PySR) for the satellite-dwarf extra mass, blind across hosts

Criteria: `FROZEN_CRITERIA.md` (cbdcf72d5, before the script). Run: `JULIA_PKG_OFFLINE=true python3 cfg854.py [K1|MUTATE]`
(PySR 1.5.9, offline, serial, deterministic). Minutes.

## Result — frozen CLASS: **LINEAR SUFFICES**, but the power control **FAILED** → no formula is validated
- N = 19 dwarfs with an excess and both [Fe/H] and τ90 (6 dropped, listed in the .out). Split A: train MW (10) → test M31+field (9);
  split B: the reverse.
- **K1 power control FAILED:** with a planted law y = 7 + 0.5(x2 + 0.5) − 0.3(x1 − 6) + noise 0.1, PySR's selected formulas reach test
  RMSE 0.106 (A, pass) and 0.252 (B, fail; it latched onto [Fe/H]). With ~10 training systems the selection step overfits, so the
  real-data class cannot certify a law either way.
- Real data: split A selected an overfit formula (test RMSE 0.416 vs linear 0.280); split B selected **y = log r + 7.40** (test RMSE
  0.266 vs constant 0.529, linear 0.337). MUTATE (shuffled y): NO GENERALISING STRUCTURE, as required.
- **Post-hoc hint (not a verdict):** the simplest formula on the Pareto front is the SAME in both blind splits:
  **y = log10 r_1/2 + 7.31 (A) / 7.40 (B)**, i.e. M_extra(<r_1/2) ≈ 10^7.35 M_⊙ × (r_1/2 / kpc). Extra mass proportional to radius means a
  universal extra circular speed V_extra = √(G M_extra / r_1/2) ≈ 10 km/s for every dwarf, independent of stellar mass — consistent with
  CFG853's clue (fainter dwarfs need more extra mass relative to their stars). A mechanism would have to produce a ~10 km/s extra
  isothermal component in faint pressure-supported dwarfs and not in gas-rich rotating ones (CFG845).

κ = ½ fitted; cold energy mass required; not theory closed.
