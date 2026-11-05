# CC2_flat_condensation_grade: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Owner 11-04: pursue critical condensation. CC1 found the spec's threshold sits in (1e12, 1e13) only at constant eta. CSM1 graded the consistent selector only with S9's mass-dependent c_f. The one ungraded consistent variant is **flat c_f = 4 everywhere**: eta = 10.82 in the core and in the switch, halo iff eta Sigma_coll(M) > Sigma_a0, else the law. No fitted number: c_f = 4 is EXTERNAL, kappa = 1/2 FITTED. Table crossings 12.66 canonical, 13.00 alt; the harness reports its own EPS roots.

**Harness.** CSM1's calibrate.py, read-only, executed as a copy with two changes only: the level tag `shpS9_L` becomes `shpFLAT_L` (CL3's existing FLAT shape, cf_table = L for all M), and the repo root path is fixed for the new folder. Level L = 4 only. Baseline reproduction of CL3 L 3.75 and X53 cf4 runs first; STOP if it fails.

**Pass, per footing (never pooled).**
- SPARC line passes on both backgrounds, basin flags (primary) and own mass (reported).
- 63 groups |Z| <= 2.
- All 15 cluster keys |Z| <= 2 in both h cells.
- Lensing: H2H minus law <= 9 and better than pure halos.
- **CONDENSATION PASSES CALIBRATION** if all four hold; otherwise **FAILS**, naming each failing line.

**Known in advance, not rerun.** The LG basin is 12.39 and the MW's own M200 11.88, both below either crossing, so the MW takes the law branch. HO2 graded that: 0/175 box cells, McMillan K_z z +12.0 / +14.1. A calibration pass here does not remove that failure. IC 1613 fails under every switch on record.

**Checks.** Baseline reproduces (CL3 315 leaves, X53 cf4). flags_expected (no decision violations). rss < 1 GB. Reported: harness EPS roots vs 12.66 / 13.00.

kappa = 1/2 FITTED; c_f EXTERNAL; core shape empirical. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
