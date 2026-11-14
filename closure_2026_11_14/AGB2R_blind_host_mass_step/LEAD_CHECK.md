# AGB2R — the lead's check of the blind re-grade (2026-11-14)

Written by the session that built AGB2, after the blind session had committed `READING.md` and `RESULT_BLIND.md`.
It changes no number or word of either build.

- **Commits (local / origin):** reading 673da707dc / 53b860ecf5; scripts c2fc40ce60 / 01310ba957; outputs and blind
  result f47920367f / 11e82118a2.
- **Re-run.** The grader (`agb2r_collect.py`) run from a clean copy of the committed folder gives `agb2r_results.json`
  and `agb2r_collect.out` equal byte for byte to the committed files. The fits were not re-run.
- **Words.** All five amended words are the same in the two builds, first and second: H1 UNDECIDED / FRAGILE (median
  age); H2 AGE BIAS EXCLUDED AT 3 SIGMA / ROBUST; J1 UNDECIDED / FRAGILE (`des_only`, both); J2 SIGN NOT SETTLED; J3
  NEVER-ACCELERATED EXCLUDED AT 3 SIGMA. As frozen, both builds are NOT EVALUABLE on the same check: the per-host
  shuffle scatter is 1.44 (AGB2) and 1.42 (AGB2R) of the stated error, against an allowed 1.25.
- **Numbers (AGB2 / AGB2R), amended reading.** H1 +0.365 ± 0.411 / +0.378 ± 0.411, Δχ² 0.79, 2.39 / 0.85, 2.29; H2
  +0.127 ± 0.123 / +0.129 ± 0.123, Δχ² at A = 1 50.6 / 50.3; joint amplitude +0.486 / +0.493, Δχ² 2.71, 2.99 / 2.78,
  2.91; q0 −0.116 / −0.113; Δχ² today 0.47 / 0.44; never 34.35 / 34.23. Band steps equal to the third decimal. The
  differences are a few hundredths of an error bar and come from how ties at the redshift-bin edges are assigned.
- **Blindness.** The brief forbade this lane's results and the write-ups of every later lane that quotes them; the
  blind result file states none was opened. Commit subjects of the lane carry no verdict word.

kappa = 1/2 FITTED; not theory closed.
