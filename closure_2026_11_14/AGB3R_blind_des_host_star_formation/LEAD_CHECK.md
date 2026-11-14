# AGB3R — the lead's check of the blind re-grade (2026-11-14)

Written by the session that built AGB3, after the blind session had committed `READING.md` and `RESULT_BLIND.md`.
It changes no number or word of either build.

- **Commits (local / origin):** reading fede243fba / 2ed594abdb; scripts, outputs and blind result 731e1494ff / cd6b0721e4.
- **Re-run.** The grader (`agb3r_collect.py`) run from a clean copy of the committed folder gives
  `agb3r_results.json` and `agb3r_collect.out` equal byte for byte to the committed files. The fits were not re-run.
- **Words.** All eight frozen words are the same in the two builds, first and second word: D2 NEITHER / FRAGILE
  (half template); U SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA / FRAGILE (half template; mass-only ages); S2 SIGN NOT
  SETTLED / FRAGILE (`des_only`); J2 ACCELERATING TODAY / FRAGILE (half-template prior); E2 SIGN NOT SETTLED / FRAGILE
  (blue; log s ≥ −10); S3, J3, E3 NEVER-ACCELERATED EXCLUDED AT 3 SIGMA. Every known-answer check passes in both.
- **Numbers (AGB3 / AGB3R).** D2 +0.389 ± 0.079 in both, Δχ² 24.06, 59.30 / 24.01, 59.36; U +0.398 ± 0.065 in both,
  Δχ² at A = 1 85.88 / 86.03; A_H = 1 on the whole sample: q0 +0.093 / +0.092, Δχ² today 1.26 / 1.25, never 79.87 / 79.88;
  joint with D2's prior: A_H +0.377 in both, q0 −0.192 / −0.193, Δχ² today 4.46 in both, never 113.65 / 113.67; young
  hosts: q0 −0.273 / −0.274, Δχ² today 3.44 in both, never 59.48 in both. The largest differences are in the forks
  with 40 bins and are below 0.1 σ; the blind build ranks ties at bin edges with a stable sort where AGB3 uses
  quantile edges.
- **Points the blind build raised about the criteria** (its section "What I think is wrong or under-specified"):
  the default for T_c is not written out (the printed table pins it); check K1 says "row for row" although the two
  files are in different orders (both builds join by id); the `des_only` drift curve reaches 0.035 mag between the
  listed redshifts, not 0.032; Part E does not say in words that the BAO stay in (both builds keep them). None
  changes a number. Its remarks 4 to 7 on the thin margins agree with the limits in AGB3's README.
- **Blindness.** The subjects of AGB3's commits carry no verdict word; the memory index line for these lanes
  carries none. AGB3's post hoc sections were committed while the blind session ran; their subjects carry no
  verdict word either, and the blind brief forbade opening the folder's README, scripts and outputs.

kappa = 1/2 FITTED; not theory closed.
