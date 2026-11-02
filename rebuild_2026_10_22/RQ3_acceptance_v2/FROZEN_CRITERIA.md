# RQ3_acceptance_v2: FROZEN CRITERIA, committed alone, before any script or number of this lane

The owner's standing go, 2026-11-02: harden RQ2's acceptance test. RQ3 was free by `ls` and `git log`. RQ2's files are copied here and changed here; RQ2's directory isn't edited. **This grades nothing new and adopts no framework.** Candidates are harness tests. The cold halo in particular is a known-answer test: the cold sector stays retired and nothing here reinstates it; only the owner can. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, never pooled. No dark matter particle. No LCDM input or yardstick. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** Read before this freeze: RQ2's README, criteria, V2, tolerances, acceptance.py, candidates; UX3, UX6 READMEs, UX7's opening; ux3_b.json, ux3_kfit.json, keys of ux3 by name; M1's planet ratios; C1 and C6 inputs; prep_2026/planetary_doors/BOUNDS.md; CRG1's sparc, groups, dwarfs code and C1 results; GATES.md rows 1.03-1.24, 2.03, 2.04; CFG4 H5, CFG7 tdg and hierarchy, CFG31, 32, 33, 34, 38, CFG20 scripts and the numbers below. So every recorded number is known to me, and tolerances are set knowing them. What's fixed is the rule and the tolerance, before any new line runs.

## 1. Planets
Row C1 moves from a 1-sigma anomaly/bound line to the frozen rule's |Z| <= 2 on real errors. BOUNDS.md gives each planet's 1-sigma supplementary-perihelion error from two ephemerides (EPM, INPOP), and the delta-g it implies for the tighter of them. sigma_tot(planet) = that delta-g x (larger error / smaller error), so the disagreement between ephemerides is carried, not hidden. Six planets where the table has them: Mercury, Venus, Earth, Mars, Jupiter, Saturn. Z = anomaly / sigma_tot; row passes if every |Z| <= 2. The tighter-only ratio stays printed, as the old line.
Known answer: the law's anomaly at Earth, Mars, Saturn against M1's `C1_planet_ratios x 1 bound`, rescaled from M1's rounded a0 (9.36e-11, 1.13e-10) to ours; **relative tolerance 1e-5, per planet, per footing.** That replaces RQ2's order-of-magnitude check. **MUTATE, a0 x 1.5, must fail this check on all three planets, on both footings.** Line test: a stated mock, Newton plus a constant anomaly of 1.5 sigma_tot(Mars), must PASS C1 and at 2.5 sigma must FAIL.

## 2. The clause
"Pass nothing it shouldn't" fails the run. A known-answer check computes, per footing, the rows that are FAIL for the law and PASS for a mock.
- `mock_planted`, RQ2's, g x 10^0.25 below a0/10. **Allowed flips, frozen here from RQ2's printed result and no others: B6, B19 canonical; B6, B7 alt.** It lifts cluster outskirts, the direction those keys want, so the mock legitimately moves them; they stay printed as a weakness. Any other flip, on any row, new rows included, fails the run. It must still read REJECTED and must fail A9.
- `mock_down`, new, g x 10^-0.25 below a0/10. **No flip allowed.** I expect a possible flip on A2 alt, since a lower g pushes the fitted Upsilon up from 0.44 toward the line. If it happens the run fails, it is reported as CLAUSE FAIL, and any change goes in a dated amendment naming the row.
- A twin, `RQ3_TWIN=clause`, injects a false PASS into mock_down's A30; the check must catch it, exit 1.
So enforcement catches new flips and doesn't remove the four listed ones. I say so here.

## 3. FORM-DEPENDENT, now a frozen label
A row with more than one stated vertical form reads FORM-DEPENDENT if at least one form passes and one fails. It isn't a PASS, blocks ACCEPTED, and isn't a FAIL for REJECTED. The law's A15, A16 keep it. Labels otherwise as RQ2's.

## 4. Old gates to wire, from on-disk paths, each with a known answer on the law or Newton
Candidate g only, with the source's data and estimator. Known-answer tolerance in brackets; where it can't be met, it's reported as a failed known answer and the row is marked, not the tolerance moved.
| Row | Path | Line | Known answer |
|---|---|---|---|
| A20 | a_eff = g^2/g_b at g_b = 1e-4 a0 | |Z| <= 2 on 1.20 +- 0.02 +- 0.24 e-10 | law a0 itself, 1.5 % (finite-y term) |
| A21 | CFG4 H5, U fixed 0.61, 0.57 | |d_obs_law| <= 0.10 dex (H5's line); 0.053 printed | d_obs_law +0.0077, +0.0533 [1e-3]; n 124 |
| A23a | CFG7 tdg: V from g(g_i + g_e) - g(g_e), best of host x 0.5, 1, 2 per host | chi^2 <= 12.6 for 6 | law iso 131.29 and field 10.55 canonical [0.02]; Newton 1.0950 [1e-3] |
| A23b | DF2 Danieli, DF4 van Dokkum at 20 Mpc, isolated g | |Z| <= 2 each | Newton 0.0105, DF4's z_N in CFG7's JSON [2e-3]. Law's record is an external-field number, so no law known answer |
| A24 | CFG31 stars-only isolated, CFG31's recorded floor | |Z| <= 2 | law +0.3965, +0.3571 [2e-3]; Z +2.30, +2.08 [0.02]. Infall-gas reading isn't wired: it's a class rule |
| A25 | CFG7 H2, Baumgardt, boost from g at g_int + g_ext | M/L_V median inside [1.0, 2.5] within 2 sigma | law 1.037 canonical if CFG7's kernel is this law's, else that's stated; Newton 1.70 [5e-3] |
| A26a | h50 SLUGGS Jeans, outer bins | |Z| <= 2, stat | law +0.080, +0.065 [2e-3] |
| A26b | CFG32 X-ray ellipticals with floor | |Z| <= 2 | law +0.2802, +0.2536 [2e-3], Z +1.70, +1.58 [0.02] |
| B2 | CFG34 Lovisari groups R500, R2500; gas passed as gg | |Z| <= 2 each, sigma groups + stars + HSE | law log ratio +0.1616, +0.3499 canonical, +0.1237, +0.3123 alt [2e-3] |
A17 is wired only if the K_z scale-length estimator can be reused from X5 or LW1 without a heavy solve, known answer UX5's form R 3.29-3.41. **Stays NOT COMPUTABLE, reason named:** A22 unless a path is found, A26's SLACS (needs a projected phantom, not g), A27 (per-galaxy external-field refit), A28 (orbit machinery with a class rule), A29 (no environment input to g), **B3 (the path's background is Planck's H0, Omega_m, Omega_Lambda: a forbidden input)**.

Candidates may read `lgMb`, a measured baryon mass where the source has one (SPARC, LITTLE THINGS, groups). LITTLE THINGS gets its measured gas as gg. A gas-reading g gets NOT COMPUTABLE where no gas is on file; a missing input never passes.

## 5. Real candidates, must reproduce their lanes
Tolerances: per key Z 1e-6; rms 1e-3; Upsilon 0.011; tilt 0.02 (grid 0.01); LT, X-COP 2e-3; M300 and dkappa relative 1e-3; groups Z 0.01.
- **Newton.** The Newton known answers above, plus planets Z exactly 0, B23 against a direct FITS sum [1e-6], groups against CRG1's `no_halo_Newton` |Z|. It must read REJECTED.
- **The law.** All of RQ2's known answers, now with its planets check, plus the table above.
- **UX3, g = law (1 + k g_gas/a0), k = ux3_kfit.json** (13.2868, 14.2506; unswitched). Canonical **14 of 15 keys, only G-OUT-all over 2**, alt 10; every key Z against `ux3_keys_g005_f034.json`; M3 Z_tot and joint recomputed and printed. Discs against ux3_b `unswitched|kfit`: rms 0.0907, U 0.30, tilt -0.05, LT -0.084 canonical, and alt's; **A2 must FAIL**. X-COP all 7 against UX3's -0.016, 0.089 canonical. **B28 must FAIL**, M300 4.92, 2.44, dkappa -0.212, -1.158 against ux6_results `L1|canonical|fit`. Must carry no [LABEL], must read REJECTED. X-COP is its training set, marked.
- **Cold halo, CRG1's C1** (native N, background A, A1a anchors, capped form), g = g_b + G M_N(<min(r, R200))/r^2 with M200 from `lgMb`. No a0, so footings coincide and must match exactly. SPARC against C1's A4b capped S and its Tl (+0.59) and LT (+0.153), groups |Z| 1.4675. Clusters, dwarfs, Milky Way, DiskMass, lensing, planets, Bullet: its path there isn't a g(Q) (CRG1's clusters use a stacked cold profile, dwarfs a ceiling over M200), so **NOT COMPUTABLE by this harness**, and CRG1's numbers are printed as READ, never a pass. Must read REJECTED on Tl and LT.

## 6. Counts, disputes, correlation
README states rows computable from g for each candidate, and the reason for each NOT COMPUTABLE class. It lists disputed rows (V2's D marks) and correlated blocks. A file `row_marks.json` holds them, and rows are checked against it, so a new row can't go unmarked.

**Joint statistic.** No cross-block covariance is on disk, so a chi^2 summed over blocks can't respect correlation and is dropped from the headline; RQ2's stays printed as a summary only. What's reported:
1. Per block, one p: keys use BA1's chi^2 with R recomputed on the candidate's run; every other block uses Bonferroni on its Z rows, two-sided, which holds under any within-block dependence.
2. Across blocks: **p_joint = min(1, m x min p_block), Bonferroni, valid under arbitrary correlation.** It tests "this candidate is compatible with all blocks", can only reject, and is weak by design. LINE ONLY rows and READ rows stay out. PROVISIONAL-sigma rows (B28) stay out. Row and block counts are printed with it.
3. Disputed-excluded variant: the same with D rows out, since their sigma is itself argued over.
4. Stated limit: Z's rest on stated errors, many stat-only (keys), so very small p isn't a discovery claim. A candidate's fitted constants aren't subtracted: UX3's X-COP block is its training set, so it's excluded from UX3's p_joint.
Also, the SPARC rows (A3, A4, A5-A7, A9 not) share one fit; X-COP and keys share gas, per GM1. Said in README.

## Known answers and method
A failed known answer exits 1 and no scorecard is trusted. MUTATE twin: `RQ2_MUTATE=1`, a0 x 1.5 labelled the law, must exit 1 with separate outputs, and must fail planets per section 1. `RQ3_TWIN=clause` must exit 1. Rerun byte-identical (results, keys from cache). Keys caches of the law and old mocks may be copied from RQ2 to save compute; candidates' source is byte-identical and the check to LW1 at 1e-6 still runs; disclosed. One thread, nice 19, under 4 GB, no downloads. Commit only this directory, no push.

Expectation on record: planets fail hard for the law, pass for Newton and fail cold-halo as not computable. UX3 reads about 14 of 15 canonical, 70 % that every key Z is within 1e-6 and 60 % that its disc numbers match within tolerance on first try. Clause: 50 % that mock_down flips something. Newton fails the keys, SPARC rms, dwarfs, and passes TDG. At least one old gate fails its known answer on the first run, 70 %.

kappa = 1/2 FITTED; not theory closed.
