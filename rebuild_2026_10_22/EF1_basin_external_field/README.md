# EF1_basin_external_field: the Local Group basin's external field does not rescue IC 1613

Criteria: `FROZEN_CRITERIA.md` (d9343614cc, committed alone, before any script or number). Amendment A1 is post-result
and touches the K1 check only; it was committed alone before the rerun, and the first run is kept as
`run1_K1FAIL.out`.

**Solver:** X1's exact 2D AQUAL + EFE solver (`d10_solver`, read-only). Residuals are HO3's stellar-σ E.

κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter and not a particle. Not "theory closed". Nothing here
says the data favour the framework.

## Verdict (frozen): **BASIN FIELD DOES NOT HELP** (canonical and alt)

The external field is g_e = G M_basin / R², with M_basin = 10^12.392 M☉ (BS1) and R the barycentric distance.

| dwarf | R (kpc) | x_e basin (X1's MW-only) | shift in log g_pred | E: HO3 → EF1 | Z (canonical) |
|---|---|---|---|---|---|
| **IC 1613** | 466.6 | 0.0169 (0.0130) | −0.0006 | −0.535 → −0.535 | **−6.75** |
| Pegasus dIrr | 415.2 | 0.0213 (0.0107) | −0.0035 | +0.191 → +0.195 | +2.28 |
| Leo T | 753.6 | 0.0065 (0.0230) | −0.0009 | +0.414 → +0.415 | +2.70 |
| Phoenix | 658.8 | 0.0085 (0.0232) | −0.0006 | +0.405 → +0.406 | +5.47 |
| all 13 | | | ≤ 0.0035 | | S1 fail, S2 pass, S3 fail |

- The alt footing behaves the same way (IC 1613 Z −7.45).
- With FD1's UNGC baryons (lower internal field), the shifts stay ≤ 0.0034 dex.

## Why the field is so weak

- **The external field is much smaller than the dwarfs' own fields.** The basin field is x_e ≈ 0.002–0.02, while the
  dwarfs' internal field scales are y₀ ≈ 0.02–0.22. AQUAL's external field effect matters only when x_e is comparable
  to or above the internal field.
- **IC 1613 is an especially strong case.** Its y₀ (0.14) is about 8× its x_e.
- **The basin field is not uniformly larger than X1's.** It exceeds the MW-only field for IC 1613 and Pegasus, which sit
  nearer the barycentre. For the others it is smaller, because the MW-only rule used heliocentric distance with a
  MOND-boosted host field.

## Reading

The external field cannot be the native lever for IC 1613. The criteria said in advance that this was the expected
outcome; the lane confirms it at the solver level.

IC 1613's stellar-σ over-prediction (about 0.3–0.5 dex depending on the baryon inputs) therefore stands:
- against the law;
- against its external field;
- against every data audit on disk.

The open data lever remains the stellar mass:
- X1's M★ is 1.9e8 M☉;
- the K-band value is 7e7 M☉;
- the LITTLE THINGS SED value is 2.9e7 M☉.

None of these closes the gap.

## Checks: 4/4

- **K0:** at X1's x_e, the solver reproduces X1's committed (emb − iso) for IC 1613, WLM and Leo T exactly (|d| 0.0000).
- **K1:** isolated deep-limit control, σ² = 0.00707 against 0.00703 (A1).
- **K2:** peak RSS 0.32 GB; runtime about 40 s.
- **K3:** x_e < 0.1 for every dwarf.
- **Rerun:** the results JSON is byte-identical (`12c2f1bd…6022`).
- **MUTATE twin** (`EF1_MUTATE=1`, M_basin × 100): K3 fails, checks 3/4, exit 1.
