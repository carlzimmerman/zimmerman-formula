# AGB7R — the lead's check of the blind re-grade (2026-11-14)

Written by the session that built AGB7, after the blind session had committed `READING.md` and `RESULT_BLIND.md`.
It changes no number or word of either build.

- **Commits (local / origin):** reading 38b3610272 / fb710016d2; harness, outputs and blind result 6e15612cc9 /
  e6da174d37.
- **Re-run.** The grader (`agb7r_collect.py`) run from a clean copy gives `agb7r_results.json` and
  `agb7r_collect.out` equal byte for byte to the committed files. The 21 runs were not repeated; the two lane folders
  under `campaign_fresh_gravity/` are unchanged.
- **Labels.** Every label is the same in the two builds, first and second word: CFG684 A1 NOT BROKEN / ROBUST, A2
  ROBUST / FRAGILE (0.35: AGE-DEPENDENT), A3 FLOOR HOLDS (`full`) and FLOOR LOST (`des_only`) / ROBUST; CFG689 B1
  STABLE / ROBUST in all sixteen cases and B2 CLASS UNCHANGED / ROBUST in all four. H1, H2 and H3 pass with zero
  difference in both.
- **Numbers.** Identical to every printed digit (flat-a0 Ω_m 0.3166, shift 0.0099 against 0.0105 on `full`; the
  tracking quantiles; P2 and native H0). The runs use the lanes' own seeds, so two correct harnesses must agree
  exactly, and they do.
- **Its remarks.** It read "within the two sd added in quadrature" as one combined sd, which is AGB1's rule and what
  AGB7 used; read as twice that, A2 would be ROBUST at both amplitudes. It also says, as AGB7's README does, that
  the constant-dark-energy test (P2) on the whole sample is the number that moves and that any summary should say so.

kappa = 1/2 FITTED; not theory closed.
