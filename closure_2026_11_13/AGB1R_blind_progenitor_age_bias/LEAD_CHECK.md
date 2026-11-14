# AGB1R — the lead's check of the blind re-grade (2026-11-14)

Written by the session that built AGB1, after the blind session had committed `READING.md`, `RESULT_BLIND.md` and
`COMPARISON.md`. It changes no number or word of either build.

- **Commits (local / origin):** reading 9090ca051c / 2c8a4eb40a; blind result, scripts and outputs 632add7214 /
  7f492afde9; comparison 4fae0b7b2b / e09768cf26.
- **Re-run.** The grader (`agb1r_collect.py`) run from a copy of the folder gives `agb1r_results.json` and
  `agb1r_collect.out` equal byte for byte to the committed files. The fits were not re-run.
- **Numbers read straight from the two builds' output files** (AGB1 / AGB1R): `full` best A 0.6182 / 0.6182,
  Δχ²(A=0) 2.1002 / 2.1004, Δχ²(A=1) 0.7854 / 0.7853; q0 = 0 at A = 0, 1, free: 18.638, 3.415, 0.045 / 18.639, 3.414,
  0.045; never accelerated: 168.141, 37.523, 28.707 / 168.145, 37.526, 28.708. `des_only` best A 0.3457 / 0.3457,
  Δχ² 0.5449, 1.9586 / 0.5449, 1.9585.
- **Blindness, commit-list route.** The subjects of AGB1's four commits carry no verdict word; the blind session
  reports that the commit list it was shown held no AGB1 subject and that the memory index line it saw was cut off
  before any number or word.
- **Words.** Every frozen word of Parts A and C is the same in the two builds. Part B was outside the blind reading
  list and rests on AGB1 alone.
- **Two defects the re-grade found on AGB1's side, neither moving a word** (both now noted in AGB1's README):
  Part C interpolates CAMB distances from a 601-point grid, worth up to 0.005 in χ²; and the short-delay template
  T_W (reported only) is 3 to 7 × 10⁻⁵ mag high, so its reported Δχ² should read 1.86 / 1.50 / 0.59 where AGB1
  printed 1.84 / 1.49 / 0.58.

kappa = 1/2 FITTED; not theory closed.
