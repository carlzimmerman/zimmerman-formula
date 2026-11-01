# CL2_native_cf_slope: the native zoom mass slope of concentration, with one external level L

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (b57ed8751f).
- **Harness:** CL1 (bfbc7af384); CF2's switch at T = 12.3 and GS1's measured cluster budget.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule): **NATIVE SLOPE CLOSES THE GAP (canonical): FRAGILE**

| shape (native c_f at 10^12/13/14, scaled to L at 10^14) | L passing on canonical | detail |
|---|---|---|
| **S9**, nine-seed crossing (primary) | **4.0 only** | groups +1.99, G-OUT-all −1.93, every line passes; 3.75 fails groups (+2.07); 4.25 fails G-OUT-all (−2.01) |
| S3, three-seed ng48 | 4.0 only | groups +1.96 |
| SN, NFW-fit | **none** | groups +2.19 / +2.11 / +2.04 at L 3.75 / 4.0 / 4.25 |

- **The pass depends on the steeper native slope.** The NFW-fit slope (ratio 5.6/5.4 between 10^13 and 10^14) is too flat
  for the groups.
- **The alt footing** fails only its known L- and T-independent lines, the SPARC line and the MW ultra-faints.

## Held-out tests of this picture (separate lanes; ALL FAIL)

- **HO3** (1cf7d31d67): the 89 LG dwarfs one by one. The class medians hold, but the individuals scatter about 0.25 dex
  beyond their errors. Leo T and Phoenix sit above the law.
- **HO2** (a3bb1e781f):
  - **SLUGGS centrals** remain under-predicted (+0.15 dex); 1 of 4 clears.
  - **The Milky Way is INFEASIBLE.** It falls below the switch, and it would need the halo, which needs T < 10^11.9.
- **HO1** (91cc5c3bd4):
  - **X-COP's 35 points** have the right mean (−0.002) but the wrong shape (rms 0.126; cores too light, outskirts too
    heavy).
  - **The hot-gas groups** come out with the opposite sign (D +0.23 against [−0.51, −0.08]).

## Reading

CL2 fits the lines it was assembled from. It does not carry over to held-out data, so it is a description, not the
mechanism. The held-out failures point to a non-mass switch key (environment or gas state) and to a halo shape that is
wrong in both directions.

## Checks: 10/10

- K0/K2 reproductions.
- S0a: the flat shape reproduces CL1.
- S0b: the shape tables.
- K1: the switch property.
- K2: c_f(M) is monotone.
- K3: 0.67 GB.
- **Pending:** the twin and the rerun.

## Files

- `cl2_native_slope.py`
- `cl2_native_slope.out` and `cl2_native_slope_results.json`
- the per-run outputs
