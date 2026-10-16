# CFG809 FROZEN CRITERIA: H-EX done right. Retained gas tethers ONLY its own cold share; the expelled share is free (committed before any script)

**Why.** CFG808 (81e53e6ce) froze the rule "free = cold energy of expelled baryons". But its implementation let the settled law
draw on the POOLED supply, so the law's phantom of all retained baryons absorbed the expelled share as well (free/supply =
0.000 in every system, seen in its logs before its score). This lane implements the stated rule:
- the settling cap is the RETAINED share, 5.364 × M_retained (in CFG637's Infall: cap = cold_turned × f_ret, in place of
  cold_turned);
- the expelled share, 5.364 × (bc − M_retained), stays in the reservoir as free collisionless mass, placed by Method A.

Everything else is identical to CFG808:
- the census catchment fixed point;
- the all-retained tethered source;
- the stellar placement;
- the data, harnesses and statistics.

## Pass rules (unchanged from CFG808; ν_s primary; both footings, never pooled)
1. **eRASS1 318:** MID and OUTER within 2σ, AND every gas-mass tercile |Z_MID| < 3.
2. **ACCEPT 8:** OUTER within 2σ.
3. **eFEDS 131:** χ² p ≥ 0.01.

**Verdict:** PASS if all 3 pass on ≥ 1 footing; PARTIAL if two pass; FAIL otherwise. KiDS early types are not scored (stated).

## Controls
- K1: the 'ALL' control (pooled cap, constant 0.90) reproduces CFG727's ALL rows within 0.01.
- K2: free mass equals 5.364 × (bc − M_retained) to within 5% (median over eRASS1). This checks that the split is implemented.

κ = ½ fitted; cold energy mass required; not theory closed.
