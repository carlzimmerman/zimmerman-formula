# CFG812: impulsive unbinding of freed cold energy (H-UB). NULL MECHANISM (no full run needed)

**Spot check** (`spot_bound.py`, 12 eRASS1 clusters spanning gas mass, canonical ν_s): the bound fraction of the freed cold
energy is **1.000 in 11 of 12** (minimum 0.968, in the lowest-mass system). Removing the expelled baryons (≲ 8% of the mass)
leaves essentially every freed orbit bound inside 4 r_ta. As stated in the criteria before running, the effect is too small.
H-UB is therefore identical to CFG809 to < 0.1%, and its scores are CFG809's: **FAIL** (eRASS1 0.76 overshoot, ACCEPT ×2,
eFEDS pass). The full pipeline was not run, because it would reproduce CFG809.

## ⚠️ Finding that affects CFG727/808/809 (disclosed here, not re-adjudicated)
- The spot check shows **f_ret = 0.600 for every eRASS1 cluster**, not the census value.
- **Cause:** the catchment's condensed-fraction floor, bc = max(M_cond/0.10, M_ret/f_ret). The harness sets condensed =
  0.20 × M_gas (eRASS1, and ACCEPT the same way), so M_cond/0.10 = 2 M_gas always dominates, and f_ret = 1.2/2 = 0.6.
- So in eRASS1 and ACCEPT, the census f_ret(M_ta) **never acted**. CFG727 (constant 0.90) has the same pinning.
- The cluster mass trend in CFG727/808/809 therefore came from the source and placement rules, not from census retention.
- The "census by mass" mechanism has been tested only where the floor does not bind (eFEDS groups and low-mass systems).
  For eRASS1 and ACCEPT it remains **untested**.
- A fair test needs measured condensed fractions per cluster (BCG + member stellar masses), instead of the fixed 0.20.

κ fitted; not theory closed.
