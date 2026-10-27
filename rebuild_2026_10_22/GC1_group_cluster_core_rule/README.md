# GC1_group_cluster_core_rule: is the universal G-OUT-M3 deficit correlated structure beyond turnaround?

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (d1da6b8185), committed alone before any script or number.
- **The record map** comes from a read of X38–X62, GR1, IC1, IB1, PS1/2, CS1/2 and IJ1. Every tested group/cluster core
  rule leaves G-OUT-M3 (the outer band of the top Mgas500 tercile) UNDER, which made it the target.
- **Two code fixes before any graded output:**
  - the copy's path resolution;
  - the CLASS k_max, capped at 140 /Mpc, where the table ends at 141.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule): **NOT REPAIRED: ROBUST on both footings**

**The term does nothing.** The zero-parameter correlated-structure term is the CLASS linear ξ with Mo & White bias
(median b = 4.1, range 0.8–10.9), added beyond r_ta. It changes the predictions by at most 1.3 %:

| key | share of the prediction from the term |
|---|---|
| G-OUT-M3 | 0.000 |
| G-OUT-M2 | −0.002 |
| G-OUT-M1 | −0.013 |

**The reason is geometric.** Mass outside r_ta (≈ 5–8 Mpc for these clusters) projects onto R < 3 Mpc as an almost flat
sheet, and a flat sheet has no tangential shear. The usual two-halo signal at ≈ 2 Mpc comes from correlated mass at ≈ 2 Mpc
in 3D, which this model already assigns to the cluster halo.

**Swapping in the native normalisation (Ω_c/Ω_b 5.2715 instead of 5.364) makes M3 slightly worse:**

| rule | inherited normalisation (Z) | native normalisation (Z) | other failing lines |
|---|---|---|---|
| R4 | +2.41 | +2.55 | — |
| R5 (c_f = 5) | +2.00 | +2.15 | M3 is the only failing line |
| RX48 (native c_f) | +1.80 | +1.96 | G-IN-Mall fails (OVER) |

No rule passes the X43 line set in any configuration. Sheth–Tormen bias, reported only, gives the same M3 (+2.55).

## Checks: 5/6

- **Passing:** S0a reproduces X43 exactly; S0b (σ₈ from pk_lin 0.82742 = EM1); S0c (b(ν = 1) = 1.000, monotone); K2
  (native ratio exact); K3 (0.62 GB).
- **K1 FAILS, honestly:** the frozen expectation "the term raises every OUTER prediction" was wrong. The term *lowers* M1
  by 1.3 %, which is the flat-sheet projection effect. It is disclosed, not repaired post hoc.
- **Pending (follow-up commit):** the MUTATE twin and the rerun-identical confirmation. The Mac was saturated by the peer
  X48 ng64 zooms.

## What this means

The missing outer shear lies inside turnaround: it is a cluster-halo budget or shape question, not environment. That led
to GC2 (the turnaround baryon budget, which overshoots) and GC3 (an infall halo normalised at R500, which undershoots). Together
the three lanes bracket the cluster cold dark energy budget.

## Files

- `gc1_two_halo.py`
- `gc1_two_halo.out` and `gc1_two_halo_results.json`
- `runs/` (per-configuration X43 copies' outputs and logs)
