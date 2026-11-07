# AK1 criteria addendum A2: MUTATE-V re-run with longer t_max (POST-RESULT, disclosed)

Filed after the AK1 grade (grade.out, GRADE.json) and before any A2 number. It does not change the frozen label:
AK1's label stays the one CRITERIA.md gives, **NO VERDICT (check failed)**. Kappa = 1/2 FITTED; not theory closed.

## What failed and why

MUTATE-V (CRITERIA.md, Checks) reruns clock-only AC2q row 1 with the stream started at v0 = 577.6 / w = 8.4016.
At t_max = 6 the row never reached the regularization level (J = 0.1; t_lev[0] = 4.23, later levels unreached,
status 0, 869,348 steps). The snapshots at t_reg + 0.25 and t_reg + 0.5 therefore never fired, and the V reading is
the sentinel -1 (-68.75 km/s). The run-wide max |v| was 8.578 w = 589.7 km/s, inside 500-650, but that is not the
frozen reading. The gate failed because there was no snapshot. The observable did not misread a 577.6 km/s stream.

## A2 (one row, both rungs)

- Same row, same v0, same scheme and resolution rungs (N 4000, 8000). The only change is t_max = 60.
- MUTATE-V passes under A2 if V lands in 500-650 km/s at both snapshots on the N 8000 rung, as frozen.
- If the row still does not reach t_reg by t_max = 60, A2 reads "MUTATE-V not evaluable", and nothing more is claimed.
- If it passes, the result is reported as a separate line beside the frozen label: "under post-result addendum A2,
  the gate set passes and the frozen line logic reads <label>". It is never the AK1 label.
- No other row, gate or band changes.
