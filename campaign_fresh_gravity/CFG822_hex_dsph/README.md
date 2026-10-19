# CFG822 — canonical v2 H-EX applied to the 11 MW classical dSphs

Criteria: `FROZEN_CRITERIA.md` (020ebf66d, committed before the script). Run: `python3 cfg822.py` (MUTATE: `CFG822_MUTATE=1`).
Ran 2026-10-18 beside the 1024³ T2x job on owner request (1 core, nice 19, 0.13 GB).

## Result — CLASS (canonical): **IMPROVES** by the frozen rule, but negligibly
| | χ² / 10 dof | p | unscreened law (CFG821) |
|---|---|---|---|
| canonical | 57.8 | 9.3e-9 | 58.4 |
| alt | 59.3 | 5.0e-9 | 51.8 (H-EX is **worse** on alt) |

- The free cold energy of expelled gas is large in the faint, diffuse dSphs: 4–15 M_b inside r_1/2 for Antlia II, CVn I,
  Sextans and Crater II. But their stellar masses are so small that σ_pred still falls ~2× short: Antlia II 3.5 vs 6.0,
  CVn I 4.2 vs 7.7, Draco 5.4 vs 9.6, Sextans 3.6 vs 7.9, Ursa Minor 4.9 vs 8.9 km/s.
- Fornax is over-predicted (17.1 vs 12.1); Leo I is slightly over (10.8 vs 9.3).
- The census gives f_ret = 0.10 for every dSph (the floor), so 90% of each catchment's supply is free.
- **Reading:** H-EX as written does not fix the dSphs. The shortfall pattern of CFG821 survives (CVn I, Draco, Sextans, UMi
  low; Fornax high). The free mass is placed too far out (Method A spreads it to r_ta ≈ 21–106 kpc) to raise σ at r_1/2 ≈
  0.2–1 kpc enough. Dwarfs still need bound cold mass concentrated inside r_1/2 (CFG821's conclusion stands).

## Controls
- **K1: FAIL at the 2% tolerance** (Draco, free = 0: 4.46 vs 4.61 km/s, −3.3%). The criteria declared that the Wolf and
  CFG821 estimators differ by the M/2 convention; the residual 3.3% is that convention (Wolf uses M(<r_1/2) from the settled
  profile, CFG821 uses M_b/2 with the closed-form law). It does not touch the χ² (both runs use the same estimator).
  Disclosed, not repaired.
- **MUTATE bites:** free mass uniform to r_ta → inner free mass drops to ~0 (Antlia II 14.7 → 0.04 M_b) and χ² rises to
  134.9 (both footings) → NO HELP. Outputs `cfg822_MUTATE.out`, `cfg822_results_MUTATE.json`.

κ = ½ fitted; cold energy mass required; not theory closed.
