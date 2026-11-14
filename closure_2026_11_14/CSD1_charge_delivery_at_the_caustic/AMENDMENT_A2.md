# CSD1 AMENDMENT A2 (2026-11-14, 15:00 EST by the clock; POST HOC)

Committed alone, after the first grader run had been read in full (every S-seed, S-cos and S-ref number and the first
label lines). It changes no gate, tolerance, label rule or known-answer line.

**What was seen.** KA7 printed "nan -> FAIL". The S-seed series hold NaN by design in columns that have no shell to
read at early times (for example v_out at 0.5 R_fold before shells reach it, and R_eq while R_ta < 1 kpc). The grader
took max(|a - b| / |b|) over all columns, and NaN - NaN is NaN, so the line could never pass. Compared with NaN treated as
equal to NaN in the same place (`numpy.array_equal(..., equal_nan=True)`), the A = 0 run and the S-seed run are identical
in all 667 x 72 entries, NaN positions included. Because KA7 failed, the frozen rule set S-cos to NOT EVALUABLE.

**Change.** KA7 is evaluated as: identical NaN positions, and max relative deviation over the finite entries <= 1e-12.
The grader is changed in that line only (committed after this file, before it is re-run). As A1 item 3 says, KA7 checks
only that the inserted text is inert at A = 0; S-cos's label rests on it and on the accepted tuning.

**Tuning, for the record (not an amendment; criteria section 2 allows more points when the target is not bracketed).**
A = 4 / 7 / 10 gave 21.9 / 37.1 / 52.3 M_b turned around, below 59.49; A = 12 and 15 were added (63.0, 78.3 M_b); A* =
11.3; the confirming N 2400 law-off run holds 59.32 M_b (-0.3 %).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
