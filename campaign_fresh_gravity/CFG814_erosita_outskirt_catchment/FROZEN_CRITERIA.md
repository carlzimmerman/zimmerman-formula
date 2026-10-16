# CFG814 FROZEN CRITERIA: H-EX with catchment retention set by the MEASURED eROSITA outskirt slope (confirmation run; committed before any script)

**Seen before freezing (disclosed).** CFG813-diag showed that a gas density ∝ r^−3 beyond R200 gives f_eff ≈ 0.76, matching
the clusters' implied ~0.65–0.75. That n was read off a scan. Here the slope is taken from DATA instead: the 2026 SRG/eROSITA
680-cluster stack (arXiv:2509.25317) measures ≈ −3 at r200m, with signal to ≈ 2 r200m (provisional; abstract/summary
values). This is a CONFIRMATION run with a measured input, not a discovery.

## Per-cluster catchment (no fitted parameter)
- **Gas:** the harness's beta model inside r200m. It steepens to ρ ∝ r^−3 at r200m (taken as 2.2 R500; provisional
  conversion) and continues out to the framework turnaround radius r_ta (CFG654 Δ_ta(z), fixed point M_ta = bc/f_b).
- **Bracket F (filament flattening, as in the simulations cited by eROSITA):** r^−3 out to 2 r200m, then r^−2 to r_ta.
- **Retention:** bc = gas(< r_ta) + M_cond, with M_cond = λ × 10^10.7 (CFG813, provisional). f_eff = (gas < 3 Mpc +
  M_cond)/bc, capped at 1.
- **Rule:** CFG809's H-EX split with bc = retained / f_eff (in place of the census fixed point). Everything else is
  identical: retained tethers its own share, the expelled share is free, Method A placement.

**Sample.** The same 76 redMaPPer-matched eRASS1 clusters as CFG813.

## Pass rule (as CFG813; primary ν_s canonical; alt reported)
- MID and OUTER within 2σ (15-patch jackknife), AND both gas-mass halves |Z_MID| < 3.
- **CONFIRMED** if the primary passes. If it also passes under bracket F, it is ROBUST.
- **NOT CONFIRMED** otherwise.
- Report Σ Z² against the plain law, against CFG809 (fs = 0.20) and against CFG813 (census).

## Controls
- K1: the median f_eff reproduces CFG813-diag's n = 3 value (0.761) within 0.01 (primary profile).
- K2: with f_eff := the census value, the run reproduces CFG813's primary MID (1.64) within 0.01 (spot check, 5 clusters).

κ = ½ fitted; cold energy mass required; not theory closed.
