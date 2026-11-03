# CX1_leaf_collision: FROZEN CRITERIA, committed alone before any script or number

Owner's standing go for search lanes, 2026-11-02. kappa = 1/2 FITTED. Footings a0 = 9.3603e-11 (canonical, the record's 9.360324825027975e-11) and 1.1312e-10 m/s^2 (alt), never pooled. No cold component, no particle; the cold sector is retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. A no-go here is a statement about these leaves, these inputs and these error budgets, not about all physics.

**Not blind.** Read before this: BF1's and SY1's criteria, amendments and scripts (`bf1.py`, `sy1_leaves.py`, `sy1_data.py`), RS1's criteria, README and `rs1_rows.py`, BS1's criteria, script and results JSON. No CX1 number exists. Expectation, mine, on record: the leaves separate the classes by size (ell), so X-COP has no leaf neighbour among discs or dwarfs and the line-level verdict for X-COP is NO COLLISION (70 %); any collisions found are between discs, LITTLE THINGS, IC 1613 and dwarfs (60 %), where the leaves overlap.

## Question
In the class-blind leaf space BF1 and SY1 search, do the data hold **collisions**: two measured points, from different systems, at the same leaf values within their real errors, that need different boosts beyond their real errors? If so, no rule that is a function of those leaves and varies smoothly on the scale of the leaf errors (law modification or added source alike) can pass both. Then: does one environment leaf, the basin mass, remove them?

## Quantities
- **Required boost** per row: B = g_obs / g_law(g_b), g_law = g/2 + sqrt(g^2/4 + a0 g), at each footing's a0. The record's per-row g_obs and g_b, from `RS1_required_source/rs1_rows.py` `table(foot, "U50")`, read-only.
- **Leaves, as SY1 defines them** (`sy1_leaves.py`, imported, not copied), at a0 canonical on both footings (SY1 A2 item 4): y = g_b/a0, ell = r a0/c^2, f = gas share of enclosed baryons clipped to [0, 1], s = dlog g_b/dlog r by SY1's `slope_1d` along each system's run in r (a single-radius system is SY1's point stand-in s = -2), D = rho_b/rho_DE by SY1's `D_leaf`.
- **Metric coordinates:** log10 y, log10 ell, f, s, and for the environment arms log10 M_basin. D isn't a coordinate: SY1 A2 records that D = y(2 + s)/(16 pi ell) is fixed by y, s, ell, so two rows equal in (y, ell, s) are equal in D; a collision in (y, ell, f, s) is a collision in the five leaves. Stated, not a departure.
- **Environment leaf E = log10 M_basin**, BS1's definition (EM1 R1: log M200 = 11.18 + 0.90 (log M_b - 10); sum over basin members), read from `BS1_basin_switch/bs1_basin_switch_results.json`, never recomputed from new data:
  - SPARC with a multi-member basin: BS1's stored `lgM_basin_sparc["A_c2b_refit"]` (61 galaxies). SPARC alone: own M200 from MRT M_b = 0.5 L36 + 1.33 MHI (BS1's OWN). BS1's two "no Dist" galaxies (DDO064, UGC03546): NOT COMPUTABLE.
  - Dwarfs: MW and M31 satellites take the LG basin, 12.3925. Field dwarfs at R < R0_data = 794.7 kpc (BS1's field_R) take the LG basin; others, and Antlia B (no UNGC R), are alone: own M200 on BS1's A1 M_b from M*.
  - LITTLE THINGS: the LG basin for the LG field dwarfs by identity (IC 1613; DDO 210 = Aquarius; DDO 216 = Pegasus dIrr; WLM), SPARC's value for a SPARC galaxy by identity (alias table below); others NOT COMPUTABLE (BS1 computed no basin for them).
  - Groups, X-COP, lensing bins: their own basin's central (BS1 rule d, c). Class-blind: own M200 from the EM1 relation on the system's own measured total baryons (groups logMbar; X-COP gas + stars at R500 as RS1's M_bt; lensing bin M* + assumed gas). For X-COP this extrapolates a galaxy relation to 10^13 Msun of baryons: disclosed. The catalogue or hydrostatic mass is not used, because it is built from g_obs.
  - E error: 0.15 dex, ASSUMED (EM1's rms 0.066, BS1's Upsilon_K 0.5-0.8 and R0 +-1 sigma variants), independent of the other leaves.

## Arms
- **L3:** log y, log ell, f (BF1's leaves). All rows.
- **L5:** log y, log ell, f, s (with D implied). Rows whose s is SY1's single-radius stand-in (LITTLE THINGS, groups, dwarfs, IC 1613) are **L5 NOT GRADED**, as SY1 A2 refuses them as a pass for s. L5 rows: SPARC, X-COP, lensing (lensing s is computed along its radii; its baryons are a point mass, so s = -2 and D = 0 are the model's values, stated).
- **L3+E, L5+E:** the same plus E. Rows with E NOT COMPUTABLE drop from these arms only.

## Lines and identities
Lines: S (SPARC, Q < 3, Inc >= 30), LT (LITTLE THINGS), G (63 groups), X (X-COP HSE, 7 clusters, x 0.1-0.7), L (KiDS lensing, 4 bins, R <= 0.3 Mpc), Dw-UFD (MW ultra-faint), Dw (the other dwarf classes), IC1613 (its LT and Dw rows, taken out of LT and Dw; a line of one system because the record grades it alone).
- **Groups:** one row per group, not RS1's G3/G6 pair: g_b is the same in both, so f = 0.45 +- 0.15 ASSUMED spans RS1's 0.3 and 0.6. Departure from RS1's rows, stated.
- **One system, never paired with itself:** every radius of a galaxy or cluster; every row of a lensing bin; and these identities (normalised names: upper case, spaces and leading zeros dropped, then): DDO 154 = DDO154; DDO 168 = DDO168; NGC 2366 = NGC2366; DDO 50 = UGC04305; DDO 87 = UGC05918; DDO 126 = UGC07559; Haro 29 = UGCA281; WLM (LT) = WLM (Dw) = UGCA444; IC 1613 (LT) = IC 1613 (Dw); DDO 210 = Aquarius; DDO 216 = Pegasus dIrr; a group named after a SPARC galaxy (NGC0891, NGC3877, NGC3992) = that galaxy. After the run every colliding pair's names are listed; a missed identity found there is fixed in a post-result amendment, disclosed.

## Errors, propagated by Monte Carlo
400 draws, seed 20261103, per footing. Each draw recomputes g_b, g_obs, the leaves (s along the drawn profile) and B. Per row: mean vector and covariance of (log y, log ell, f, s, log B, E). A row whose g_b <= 0 in more than 10 % of draws is dropped and counted. Variance floor: sd 0.01 on every leaf coordinate (a resolution floor). MEASURED components from files on disk; ASSUMED ones are tagged.
- **SPARC:** per galaxy D ~ N(D, e_D) and Inc ~ N(Inc, e_Inc) from `SPARC_Lelli2016c.mrt` (MEASURED); g_obs scales as (D0/D) sin^2(Inc0)/sin^2(Inc), ell as D/D0, g_b is distance-free. Upsilon_disc log-normal about 0.5, sd 0.10 dex, Upsilon_bulge = 1.4 Upsilon_disc (ASSUMED; spans the record's 0.41-0.80 at about 1 sigma). Gas mass x N(1, 0.10) (ASSUMED). Per point V ~ N(V, e_V) (MEASURED).
- **X-COP:** per cluster, one coherent draw each for M_HSE (EM_FORW / M_FORW), gas (MGAS_LO/HI) and stars (MSTAR_LO/HI), the fractional errors interpolated at each radius as RS1 interpolates the values (MEASURED). Coherent across radii, so s isn't inflated by independent noise.
- **Groups:** logSigma +- e_logSigma, logMbar +- e_logMbar (MEASURED, the table); f ASSUMED as above.
- **Lensing:** per row Delta Sigma +- its published error (MEASURED, as RS1's); per bin M* +- 0.15 dex (ASSUMED) and gas share 0.2 +- 0.1 (ASSUMED), coherent within a bin.
- **LITTLE THINGS:** V +- eV where given, else 10 % (ASSUMED); distance 10 % (ASSUMED, g_obs and ell); M_gas 10 %, M_SED 0.2 dex (ASSUMED).
- **Dwarfs, IC 1613:** log g_obs +- the row's sdMC (MEASURED, the record's); M* 0.10 dex, r_1/2 10 % (ASSUMED).
- **Footing-tagged rows** (dwarfs) are taken from each footing's own table.

## Collision definition
For a pair (i, j) from different systems, Delta = mu_i - mu_j, Sigma = Sigma_i + Sigma_j, split into the arm's leaf block l and B:
- **Leaf distance** d_L^2 = Delta_l^T Sigma_ll^-1 Delta_l. **Near pair:** d_L <= 1.
- **Conditional boost gap** m = Delta_B - Sigma_Bl Sigma_ll^-1 Delta_l, variance v = Sigma_BB - Sigma_Bl Sigma_ll^-1 Sigma_lB, z = |m|/sqrt(v). This is the boost difference the pair would show if their leaves were equal, with the leaf-boost error correlation (Upsilon, distance) carried. d_L^2 + z^2 is the joint chi^2.
- **Point collision:** near pair with z >= 3. **Strong point collision:** z >= max(3, z_LEE), z_LEE = Phi^-1(1 - 0.025/N_near), N_near the arm's cross-system near pairs (look-elsewhere: under no collision, expect 0.05 such pairs).
- **Line-level collision** between lines A != B (what the gates grade; a single point is inside a gate's tolerance): over the A-B near pairs, the 1/v-weighted mean of m, with sd from 200 bootstrap resamples over systems on both sides (seed 20261104). Needs at least 3 systems on each side (IC1613: 1). Collision iff |mean m| >= 3 sd **and** |mean m| > tol_A + tol_B, tol from the record's lines: S 0.03, X 0.05, L 0.05, LT 0.10, G 0.10, Dw-UFD 0.10, Dw 0.10, IC1613 0.10 (dex).
- **Smoothness, stated:** any two distinct leaf points can be mapped to any two boosts, so a collision excludes only rules that change by less than the boost error across the pair's leaf-error ellipse. A rule steeper than that is unresolvable by these data, not excluded.

## Verdicts, per arm and footing, line level primary
- **NO-GO IN LEAF SPACE:** at least one line-level collision on both footings, surviving the ASSUMED x 2 run (every ASSUMED sd doubled, separate MC).
- **NO-GO ON ONE FOOTING ONLY:** the same on one footing only.
- **UNDETERMINED:** no line-level collision, but some line pair with >= 3 systems a side is near with |mean m| > tol_A + tol_B below 3 sd (errors too large to decide); or the controls below fail for that arm.
- **NO COLLISION:** otherwise. Reported as the map: per line pair, near-pair count, systems, mean m; and for line pairs with no near pair, the smallest d_L and where.
The point level gets the same four labels with strong point collisions in place of line-level ones, and |m| >= 0.3 dex below z_LEE for UNDETERMINED. Within-line point collisions (two SPARC galaxies) are reported separately and don't enter a verdict: a line gate tolerates single points.

**X-COP HSE.** LF1 found HSE about 0.12 dex above lensing. Every verdict is given three ways: all rows; X-COP dropped; X-COP log B lowered by 0.12. Also reported, not a verdict: lensing (PROVISIONAL) and groups (ASSUMED-GAS) dropped; Upsilon at RS1's low reading (0.41/0.574).

## Controls, run and read before the real result
- **K units:** for the X-COP and SPARC odd train rows in SY1's `build("real")` (BF1's rows), CX1's y, ell, f, s at the U50 centre match SY1's within 1e-6 relative where the rows coincide (BF1 X-COP x 0.1-0.7 by RS1's interpolation; differences stated). Law known answer: X-COP mean log B canonical +0.467 (RS1 K1 +0.4675), LITTLE THINGS median -0.025 (RS1 -0.0252), within 0.005.
- **Smooth null:** truth at each row's mean leaves, log B_true = F(leaves), observed = truth + one draw from the row's full covariance; 20 seeds each for F1 = log10((1 + f) log1p(1/y)) (BF1's planted form, W3) and F2 = 0.1 (log y + log ell + f + s [+ E]). Strong point and line-level collisions must appear in at most 1 of 20 seeds per arm and footing; otherwise that arm reads UNDETERMINED at that level.
- **Planted class:** on the F1 truth, SPARC odd-index galaxies (sorted names) get + delta in log B, a label no leaf carries; S_odd and S_even graded as two lines. delta = 0.3: a line-level collision must be found. delta = 1.0: a strong point collision must be found. Otherwise the arm reads UNDETERMINED. Reported, not binding: LT + 0.5 against S in L3.
- **MUTATE** (outputs `_MUTATE`): log B means permuted across rows (seed 20261105), covariances kept. The point-collision count must change; if not, exit 1.

## Run and rules
`PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 10 python3 -I`, one thread, under 1 GB RSS, small outputs (JSON and text) in this directory only. BF1, SY1, RS1, BS1, CRG1, HF1 are read-only. No downloads; a line that needs data not on disk is NOT GRADED. Post-result changes go in AMENDMENT_A*.md, labelled post-result.
