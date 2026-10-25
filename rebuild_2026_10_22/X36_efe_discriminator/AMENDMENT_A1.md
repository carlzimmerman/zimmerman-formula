# X36 AMENDMENT A1 (2026-10-25; written after the first run's step 0 fired the stop rule, before any slope, model residual or verdict number existed)

κ = ½ FITTED. Footings never pooled. Not "theory closed".

## What happened

First run: S0a PASS (EM1 scratch rerun reproduces every quoted EM1 number), S0b PASS (X33 ρ to 1e-9). **S0c FAILED as
frozen**: my per-galaxy residuals differ from the atlas column `resid_dex_can/alt` by at most 4.8e-7 / 4.9e-7 dex (175 of 175
galaxies compared), against a frozen tolerance of 1e-9. The script then crashed in S0d on a key-path bug (P4's JSON nests the
tiles under `"tiles"`; X33 reads it the same way). No S0d, S0e, slope, model residual, confound or verdict number was produced.

## Mechanism (checked, not assumed)

`x33_atlas.csv` stores floats with 6 significant digits (for example CamB `-0.832815`, D512-2 `-0.128114`). A residual of order
0.1–0.8 dex is therefore rounded at 5e-8 to 5e-7. The observed maximum difference (4.9e-7) is at that rounding scale. The
frozen 1e-9 compared a full-precision recomputation with a 6-digit printout, so it could never pass. S0b passed at 1e-9 because
ranks do not see the rounding.

## Change (check definition only; no threshold, class, statistic, sample, model or analysis line changes)

- **S0c (graded, replaces the frozen tolerance):** |mine − atlas| ≤ half a unit in the 6th significant digit of the atlas value,
  i.e. 0.5 × 10^(⌊log₁₀|atlas|⌋ − 5), for every SPARC row, both footings. Reported alongside: the maximum absolute difference.
- **Script bug (not a criterion):** S0d reads `p4_v3_galaxy_tiles_results.json["tiles"]["T1"]`.
- The e_ext axis is X33's stored (6-digit) column, as frozen; S0b confirms it reproduces X33's ρ exactly.

The stop rule is otherwise unchanged; the rerun recomputes everything from scratch.
