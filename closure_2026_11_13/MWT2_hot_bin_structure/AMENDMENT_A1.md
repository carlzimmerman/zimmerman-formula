# MWT2 AMENDMENT A1 (2026-11-13): a footprint-robust sky test and a bounded group in the mixture f

POST HOC. Written after a debug smoke run of `mwt2.py` with B = 30 (not graded; its numbers were seen) and while
the graded run as frozen (B = 1,000) was running. The as-frozen reading is reported first in RESULT.md; this
amendment gives a second, clearly marked reading. It does not change FROZEN_CRITERIA.md.

What the smoke run showed (and why):
1. Mutation G (40 planted stars, +150 km/s, 15 km/s, on one sky patch) was found by step (a) but NOT by step (b):
   SKY family p 0.15. The DESI footprint is itself concentrated (mostly the northern cap), so the difference of
   mean sky vectors between a patch and the rest is small, and KS on |B_Sgr| is not a clustering test. As frozen,
   that makes the label NO POWER. The frozen identity test lacks power for a real group.
2. The mixture f (c1) is degenerate where the second component is not a cold group: the "group" component can
   grow and take the halo's role, giving sigma_f of 1.7 to 2.8 in the forced bins and in the mutated bin.
3. Seen in the smoke run for 30-40 (forced identity, before this amendment): a cold component at about
   -168 km/s, dispersion about 20 km/s, weight 0.12; its forced family p values (SKY 0.11, DISTANCE 0.17,
   CHEMISTRY 0.25, TANGENTIAL 0.58). This amendment is therefore not blind to the 30-40 bin.

Changes (A1 reading only):
- SKY family gains two tests and becomes four (Bonferroni x 4): (i) clustering: the mean angular distance from
  each core-group star to its 5 nearest other core-group stars, against 2,000 label permutations (one-sided,
  small = clustered); (ii) KS on the Sagittarius longitude Lambda_Sgr (RAW1's frame). The mean-vector and
  |B_Sgr| tests stay.
- (c1) and (c2): the group dispersion is bounded above by half the bin's one-Gaussian dispersion (a cold group
  cannot become a second halo). (c3) unchanged.
- Everything else as frozen: thresholds, families, the two-family rule, brackets, controls, labels. Mutation G
  must bite under A1 (found by (a) and (b), smooth f within 0.03), or the A1 label is NO POWER.
- Outputs: `mwt2_A1.py` (a copy of mwt2.py with only these changes), `mwt2_A1.out`, `mwt2_A1_results.json`,
  `mwt2_A1_MUTATE.out`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
