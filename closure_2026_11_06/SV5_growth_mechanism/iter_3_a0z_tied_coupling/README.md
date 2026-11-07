# SV5 iter_3: Jeans scale tied to a0(z) ~ sqrt(rho_DE(z)). H-flat NO-GO FOR CLASS; H-native FAIL; H-CPL FAIL (reported)

Kappa = 1/2 FITTED; not theory closed. Criteria FROZEN_CRITERIA.md (247d2eaa2f). Script ../sv5_t0_iter3.py; outputs sv5_iter3.json,
sv5_iter3_MUTATE.json.

- Host need lambda_J >= 20 Mpc on z 0-0.5 (T0.3; both footings give 19.95 Mpc on the grid).
- H-flat: a0 constant, so F is one constant: dchi^2 543.65 (line 4). NO-GO FOR CLASS (every F is that one value).
- H-native (CFG689 medians): r(z) rises to 1.12 at z 0.7 and falls back through 1 near z 0.9. The host image is [1.000, 1.054], so
  the most generous member M* is stiff on z 0-0.88: dchi^2 876.66. Power laws q -6..6: best +3, dchi^2 301. K-mono FAILED (adding
  stiffness on z 1-2 lowers dchi^2 to 541.7, because the amplitude refit absorbs uniform suppression), so the frozen label is FAIL,
  not a class claim.
- H-CPL (DESI DR2, CDM-family fit, reported only): M* 780.66, best power law (q -1) 108.66: FAIL.
- MUTATE M1 (F == dust): G5 4.23, KiDS -0.374 / -0.372, bites. M2 (F == 20 Mpc always): 543.6, bites.
- Lean: `time_only_coincidence`, `stiff_on_preimage`, `ivt_crossing` (written, NOT COMPILED).
