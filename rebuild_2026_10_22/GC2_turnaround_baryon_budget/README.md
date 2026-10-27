# GC2_turnaround_baryon_budget: count the record's gas profile to the self-consistent turnaround radius

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (3db544593b).
- **A1** (0447a621c4): a code fix to S0b's per-cluster log keying.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule): **NOT REPAIRED: FRAGILE (V-R5shape repairs M3)**

**Primary configuration:** native normalisation and the record's "P" gas profile (r⁻³ beyond 2.2 R500), counted to r_ta.
It overshoots badly. R4 G-OUT-M3 is −4.77 / −4.64 (OVER), and 9 keys fail OVER.

**The frozen variant V-R5shape** uses r⁻³ from R500, the record's "R5" shape:

| rule | X43 line set | detail |
|---|---|---|
| **R5 (c_f = 5)** | **passes, on both footings** | SPARC on both backgrounds; groups Z +1.82; all 15 cluster keys, with G-OUT-M3 +0.49 / +0.33 |
| R4 | fails on groups only | all 15 keys pass; groups +2.05 |
| RX48 | fails on G-IN-Mall (OVER) | M3 +0.23 |

**The bracket.** M3 for R5 is +2.15 when baryons are counted to the 3 Mpc cut. Counted to r_ta it is −5.78 with the "P"
tail and +0.49 with the "R5" tail. The outer cluster budget is therefore set by the gas outskirt slope beyond R500.

**Budget ratios** M_b(< r_ta)/M_b(< 3 Mpc) for the primary shape: median 1.629; by Mgas500 tercile 1.296 / 1.629 / 1.994;
range 0.335–3.411. The ratio rises with gas mass, which is the predicted direction.

## Checks: 4/5

- S0a reproduces X43 exactly.
- S0b: the fixed point converges for 374 clusters, in at most 14 iterations.
- K2: the ratio rises with Mgas500.
- K3: 0.70 GB.
- **K1 FAILS, honestly:** "extended ≥ cut for every cluster" was a wrong expectation. For small clusters r_ta < 3 Mpc,
  so counting to r_ta gives fewer baryons than the 3 Mpc cut (minimum ratio 0.335). It is disclosed and not repaired.
- **Pending:** the twin and the rerun.

## What this means

This is not a pass of the theory. The verdict hinges on the gas slope beyond R500, which is a data question. The record
holds measured X-COP gas profiles, and they should decide the slope; that is the next lane. c_f = 5 remains external, and
lensing (X53) and the dwarfs (X51) are not regraded here.

## Files

- `gc2_budget.py`
- `gc2_budget.out` and `gc2_budget_results.json`
- `runs/`
