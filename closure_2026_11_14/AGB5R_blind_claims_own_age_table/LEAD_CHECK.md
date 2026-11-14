# AGB5R — the lead's check of the blind re-grade (2026-11-14)

Written by the session that built AGB5, after the blind session had committed `READING.md`, stage 1 and stage 2.
It changes no number or word of either build.

- **Commits (local / origin):** reading 16480890a1 / 13db1b5671; stage 1 (as frozen) 627eb1aede / 7e444e8861;
  stage 2 (amendment applied) 3030ae11b4 / 3d9496ca0d.
- **Order.** The blind build graded from the frozen criteria and committed that before opening the amendment,
  because the amendment was written after AGB5's numbers were seen and quotes one of them.
- **Re-run.** Both graders (`agb5r_collect.py`, `agb5r_collect_stage2.py`) run from a clean copy give result files
  and logs equal byte for byte to the committed ones. The fits were not re-run.
- **Words.** The same in the two builds at both stages. As frozen: NOT EVALUABLE, the error-bar check failing on
  table 2 in both (shuffle scatter 1.43 in AGB5, 1.35 in AGB5R, allowed 1.25; the blind build shows it fails for
  every seed convention it tried). Amended: AGE BIAS REQUIRED AT 3 SIGMA / FRAGILE (table 1 alone; structural fit).
- **Numbers (AGB5 / AGB5R).** As frozen, primary +0.819 ± 0.167 / +0.8195 ± 0.1666, and all six forks equal to the
  third decimal. Amended, primary +0.793 ± 0.190 / +0.812 ± 0.187, Δχ² 17.5, 1.2 / 18.8, 1.0; table 1 alone
  +0.532 ± 0.245 / +0.532 ± 0.249. The amended primaries differ by 0.02 because the two bootstraps draw different
  resamples and the tables are weighted by the bootstrap errors. The published slopes reproduce in both
  (−0.0385, −0.0246, combined −0.0304).
- **Its remarks** agree with AGB5's README and amendment: the stated least-squares errors are 11 to 17 % small;
  "table 1 alone" changes the word by losing power; the structural fork is heavy-tailed under resampling because
  the stated age errors exceed the spread of true ages.

kappa = 1/2 FITTED; not theory closed.
