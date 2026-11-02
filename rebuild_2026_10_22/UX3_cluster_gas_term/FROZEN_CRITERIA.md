# UX3_cluster_gas_term: FROZEN CRITERIA (committed alone, before any script or new number)

Owner's go, 2026-11-02. **Not blind.** Read before this: LW1, LM1, GM1, FR1, FR3 READMEs, BF1's README, code and its 18 near-miss lines, which already print X-COP holdout and SPARC holdout numbers for the family. No keys number exists for any gas term. kappa = 1/2 FITTED. The cold sector stays retired; no result here reinstates it. No particle. Footings canonical 9.3603e-11, alt 1.1312e-10, never pooled. Not theory closed. Nothing here says the data favour the framework. BF1's process and chunks/ are not touched. No downloads.

## Family
g = law(g_b, a0) x H, BF1's W3.
- **B members:** BF1's own printed H, three of its 18: (sqrt(0.5)(1+f) + pi^2 y f), (sqrt(pi) - 1/(1+f) + pi^2 y f), (1.5/(2-f) + pi^2 y f), where y f = g_gas/a0.
- **F1, graded form:** H = 1 + theta k g_gas/a0, theta the switch, k = pi^2. k has no derivation: it was picked from 2e9 tries, so **every rule below is labelled FITTED (search-picked constant)**, whatever its switch. A = 1 is my choice, so discs and the law agree when theta = 0.
- **F1k:** same, k by least squares on BF1's X-COP train clusters only (positions 0, 2, 4, 6), canonical and alt separately. FITTED.

## Part A: why discs break. Odd SPARC names only (BF1's train; Q < 3, inc >= 30, Upsilon 0.5, 0.7, fixed)
For the B members and for F1 with theta = 1: d = log10(g_obs/g), excess = d^2 - d_law^2 per point. Share of total excess, and median d, in bins of: gas share f (0-0.25, 0.25-0.5, 0.5-0.75, 0.75-1); y (terciles); galaxy Vflat (< 60, 60-120, > 120, none); radial position R/R_last (< 1/3, 1/3-2/3, > 2/3). Also rms if each bin alone is reset to the law, and the split into constant part only (A, k = 0) and term only (A = 1).

Labels, each footing:
- **GAS-RICH DWARFS** if f > 0.5 and Vflat < 120 carry >= 50 % of the excess.
- **INNER DISCS** if R/R_last < 1/3 carries >= 50 %.
- **WHOLE DISC** if neither.
Also a separation table: for each of y, ell = r a0/c^2, f, g_gas/a0, gas slope dlnM_g/dlnr, enclosed gas surface density and mean density, the overlap between SPARC train points and X-COP train rows, as AUC. A variable with AUC above 0.99 can be a switch only with a threshold, and a threshold read off this table is FITTED.

## Part B: switches, listed now
Requirement: built from locally measured quantities, physically stated, no number read from the separation.
- **C1, random-motion share:** theta = sigma_g^2 / (sigma_g^2 + V_rot^2). Statement: the term counts only gas whose kinetic energy is random, not ordered. SPARC gas is rotating: V_rot = V_obs at that radius, sigma_g = 10 km/s, adopted from memory as the usual HI value, PROVISIONAL, with 7 and 12 km/s reported. Clusters: V_rot taken as 0, theta = 1, an idealisation.
- **C1b:** theta = sigma_g / sqrt(sigma_g^2 + V_rot^2), the same with thickness h/R rather than energy. Tests whether the power matters.
- **C0, control:** theta = 0 in every disc, 1 in clusters. Says what the cluster term does alone.
- **C4, control, FITTED:** theta = step(ell > ell*), ell* the geometric mean of SPARC train's highest and X-COP train's lowest ell. The "clusters are big" rule. Reported to show what a physical switch does not add.

At most one more candidate may be added in `AMENDMENT_A1.md`, from Part A, committed alone before any holdout in Part B is read. Part A touches no holdout. **Stated now:** C1, C1b, C0 and C4 all have theta = 1 in the grader, so the keys and X-COP **cannot tell these switches apart**; and C1 passes discs largely by construction. Their only separating tests are low-velocity discs, where C1 predicts a small lift.

## Holdouts, none used to choose
1. Even SPARC names, BF1's statistic: rms <= 1.05 x law, |median| <= 0.03. Also on CRG1's `crg1_sparc.fit` per-galaxy Upsilon path, all names: rms, median Upsilon, against FG1's S line (reported per footing).
2. LITTLE THINGS, CRG1's rows: |median E| <= 0.10, V_rot = V, gas share from Mgas, MSED.
3. X-COP unseen clusters (positions 1, 3, 5): |mean| <= 0.05, rms <= 0.10; and all seven on LW1's rows, same line.
4. **15 keys through LW1's path** (DR1 tail, SL1 driver, NF1 grader), gas +0.005 primary, f* 0.034 and 0.0615, both h, both footings. Msrc = law x H, g_gas = g_b/(1 + f*) as in GM1 (Mb = gas (1 + f*) in the dump; asserted by check). Per cell: Z's, keys over 2 in either h, BA1's joint chi^2 by LW1's function, boot and jack, G-OUT-M3, Z_tot computed as LW1 does.
5. Report, no gate: M_total/M_gas at x 1 and dM/M_gas in bands against GM1's k3(x), Sun+09 and Lovisari+15 groups, Lovisari+20, read from GM1. Groups' 63-row line: the grader's group table holds no gas, so term unapplied, stated as such, not a pass.

## Labels, per rule and footing
- **DISCS AND CLUSTERS:** 1, 2, 3 pass, keys 15 of 15 in every cell and joint not FAIL. Still fitted, still no action, still a description.
- **KEYS FAIL:** 1, 2, 3 pass and keys don't.
- **X-COP ONLY:** X-COP passes, keys and discs not both.
- **DISC BREAK:** 1 or 2 fails.
A verdict needs both footings; if they differ the title says so. If no rule reaches DISCS AND CLUSTERS the lane says so at the top. **F1k vs F1:** if only F1k passes, it passes as FITTED to X-COP. k's sensitivity, pi^2 x 0.7, x 1.3 and x 1/1.7 and 1.7 for the survey ratio, reported on keys.

## Part C: HSC against KiDS on the shared clusters
GM1's 6.28 +- 0.56 vs 3.09 +- 1.38 compared 3D mass-based HSC with a deprojected KiDS Q, with a law subtracted. New test, shear to shear, no gas, no law, no deprojection: each of the shared clusters (GM1's selection; reproduce N 35) gets Okabe's NFW through (M500, M200), lg, h 0.7 scaled to grader h as GM1 does, as Msrc in the grader's own dvec. A = sum(n V/W)/sum(V^2/W): the KiDS amplitude against the HSC mass model. In the bands 0.18-0.38 Mpc, 0.38-1.18, 1.18-2.49 and all; bootstrap on clusters, 2000; patch jackknife. Raw Okabe masses primary, eq. 17 row reported. NFW past Okabe's R200 flagged as extrapolation. Also KiDS Q on the 35 against the other clusters matched in gas, to see if the 35 are a KiDS low fluctuation.

Labels, primary is the all-bins A, h 0.672. Each footing is irrelevant to A because no a0 enters; checked.
- **SHEAR GAP:** A below 1 at >= 3 sigma, hypot of bootstrap and M3A1-size systematic 0.1 relative, my number now.
- **NOT A SHEAR GAP:** |A - 1| < 2 sigma with sigma <= 0.15: KiDS shear agrees with HSC's mass, so GM1's factor is in the mass-to-ratio step.
- **UNRESOLVED:** otherwise, with sigma stated.
Whichever it reads, it doesn't say which survey is right unless a third mass reaches the same clusters; catalogue M500 isn't independent (partly HSC-calibrated) and is reported as such.

## Checks, before reading
K1 theta = 0 reproduces LW1's keys per key, |d| <= 1e-9, both footings and f*. K2 theta = 0, H = 1 reproduces BF1's known answer, X-COP +0.4675. K3 B members reproduce three printed lines of BF1's L3 output to 0.002. K4 grader's Mb/(1+f*) equals dump gas, to 1e-6 relative at R500 (else the f share assumed is stated wrong). K5 Part C: Msrc set to the law's mass reproduces LM1's V on those clusters, |d| <= 1e-9. K6 CRG1 fit reproduces FG1's S rms for the law. K7 bin shares sum to 1. A failed check is reported; no verdict from a failed K1, K3 or K5.
**MUTATE twin, must fail or move:** k x 3 on every grade (X-COP must fail, keys must move); Part C with HSC masses shuffled among clusters (A's scatter must rise, the band shape must change); Part A with f shuffled across points (share labels must move or say so). Output in separate files. Rerun must be byte-identical.

## Expectation, mine, on record
Part A: WHOLE DISC 60 %, GAS-RICH DWARFS 30 %, INNER DISCS 10 %. C1 passes discs 75 %. Keys 15 of 15 in all cells on any rule: 7 %: more likely it overcorrects some and fails G-IN or low-mass terciles. X-COP stays passing with A = 1: 60 %. Part C: UNRESOLVED 55 %, NOT A SHEAR GAP 30 %, SHEAR GAP 15 %. Likeliest overall: X-COP ONLY or KEYS FAIL, with the switch doing no independent work.

## Limits known now
The term has no field equation or action. A local-gas enclosed-mass form has no meaning in a merger; a gas-tied term faces the Bullet's offset between gas and lensing peaks and that is not tested here. HI sigma is not per galaxy. V_rot in clusters is idealised. X-COP is hydrostatic; LF1's 0.12 dex is reported as a bracket. Compute: one thread, nice 15, under 4 GB, preemptible by rerun.
