# CFG765: pre-flight — the record's z ≈ 2–2.7 KMOS3D fits cannot tell the two formation clocks apart (NOT DIAGNOSTIC)

**Label: P1 NOT DIAGNOSTIC. MUTATE bites (a deep-regime sample would be diagnostic; exit 1).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (66b7ab21a), 2026-10-13. Block CFG760–769.
- **Script:** `python3 cfg765.py` (instant) → `cfg765.out`, `cfg765_results.json`. Input: CFG270's 72 T1 fits (read only).
- κ = ½ FITTED; not "theory closed". A pre-flight decides whether a test is possible, not which clock is right.

## Result
The fits sit at y ≈ 2.2 (16–84%: 1.1–5.0) at 2.2 r_d, inside r_M, where the law's boost is only ~30%. The separation between the
orbital clock (full law) and the universal clock at its most separable allowed τ = 3.47 Gyr:

| baryon age | f (universal) | median separation | 84th pct | max |
|---|---|---|---|---|
| 1 Gyr | 0.25 | **0.081 dex** | 0.134 | 0.218 |
| 3 Gyr | 0.58 | 0.044 dex | 0.070 | 0.109 |

The bar was 0.30 dex, twice CFG270's committed ±0.15 dex baryon band. That band is shared by all fits, so it does not average down
(the pooled statistical error of 0.038 dex is not the limit).

## Reading
- **What a decisive sample needs:** y ≤ 0.17 at the measured radius (outer rotation curves, ≳ 2.5 r_M) in discs whose baryons are
  ~1 Gyr old, with baryon masses (gas included) good to ≲ 0.15 dex.
- The KMOS3D inner-disc fits are the wrong regime. Outer high-z rotation curves (the record's RC41/RC100 lanes) are the candidate
  for a second pre-flight; their baryon side is the known limit (CFG213–229).
