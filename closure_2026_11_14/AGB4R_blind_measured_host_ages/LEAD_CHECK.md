# AGB4R — the lead's check of the blind re-grade (2026-11-14)

Written by the session that built AGB4, after the blind session had committed `READING.md` and `RESULT_BLIND.md`.
It changes no number or word of either build.

- **Commits (local / origin):** reading 73f6016fa4 / ff70ef4b17; loaders and run script 20049979ab / fdffaa19b9;
  outputs and blind result 300e690841 / f7919c3aba.
- **Re-run.** The grading step (`agb4r_run.py words`) run from a clean copy of the committed folder leaves every
  committed JSON file unchanged and prints the same two words. The fits were not re-run.
- **Words.** Both frozen words are the same in the two builds, first and second: M0 SLOPE OVERPREDICTS THE HOSTS AT
  3 SIGMA / FRAGILE (`big`); M1 AGE BIAS EXCLUDED AT 3 SIGMA / ROBUST. Check KR fails in both (0.207 against the
  published 0.114), so the Rose rows are NOT EVALUABLE in both.
- **Numbers (AGB4 / AGB4R).** M0 +0.297 ± 0.194 / +0.299 ± 0.194, Δχ² at A = 1 13.09 / 13.03; M1 +0.194 ± 0.210 /
  +0.195 ± 0.210, Δχ² at A = 1 14.76 / 14.75; larger sample M0 +0.704 ± 0.174 / +0.707 ± 0.174, M1 +0.269 ± 0.199 /
  +0.271 ± 0.199 with a step of 0.098 / 0.099 mag; reliability of the ages 0.772 / 0.775.
- **One point the blind build found that matters.** The fork "hosts whose stated age interval is wider than ± 2.5
  Gyr" can be read two ways. Both builds took the half-width (8 hosts removed), under which M1 is ROBUST. Read as
  "either side longer than 2.5 Gyr" (38 removed) that fork gives +0.41 ± 0.24 and reads AGE BIAS DISFAVOURED, and
  M1's second word would be FRAGILE. **M1's ROBUST therefore rests on that reading of the rule.** The first words do
  not change either way. This is now noted in AGB4's README.
- Its other remarks (the published-magnitude reading is not a no-step fit; the larger sample's M0 measures the
  mass step; the reliability row is an upper bound) agree with what AGB4's README and AGB5 / AGB6 say.

kappa = 1/2 FITTED; not theory closed.
