# W4-24 AMENDMENT A1 (committed alone, after the first run, before the second)

**2026-11-09.** Criteria: `FROZEN_CRITERIA.md` (180b1ff772). Append-only; nothing in that file is edited.

## What happened

The first run ended **CHECK FAILED** by the frozen rule. One check failed: **K1b**, at one of the six rows.

| swt1.json row | its "closed" | its "quad" | here (30 digits) | rel. to "closed" | rel. to "quad" |
|---|---|---|---|---|---|
| y = 1e-6 | 6.664167165684736e-10 | 6.664167166666642e-10 | 6.664167166666644e-10 | 1.47e-10 | 3e-16 |

The other five rows agree with "closed" to 1.3e-13 or better. Every other check passed (K1a, K1c, K2, K3, K4, K5, K6, I1, I3,
I8). The first run's outputs are kept unchanged as `w4_24_firstrun_K1bfail.out` and `w4_24_results_firstrun_K1bfail.json`.

## Cause

The line I froze (1e-10 relative at all six rows) was wrong for the y = 1e-6 row. At that row u₁ ≈ 1e-3, and W is the
difference of two terms near 5e-7 that leaves 6.7e-10. `swt1.json` stores its closed form in double precision, so that row
carries a rounding error of order 1e-10. The file itself records this: its own quadrature at the same row differs from its
closed form by 1.47e-10, the same number found here. The value computed here agrees with its quadrature to 3e-16. So the
disagreement is the stored double's rounding, not a difference in the formula.

## Change (K1b only)

- Rows with y ≥ 1e-3 (five rows): unchanged, 1e-10 relative to "closed".
- Row y = 1e-6: the line against "closed" becomes **1e-9**, and a second line is added: **1e-12 relative to the file's
  "quad"** value at that row. Both must hold.

## What does not change

No gate, bound, hand value, branch, window, mutation arm, label or verdict rule changes. K1b is a known-answer check on the
inherited wall-pressure formula; no bound in K3 to K5 uses the y = 1e-6 row. The numbers printed by the first run for K3 to
K5 are already disclosed in its kept output: κ_min 5.2006 and 139.8882, and the first label's conditions were met apart
from K1b.

κ = ½ FITTED; not theory closed.
