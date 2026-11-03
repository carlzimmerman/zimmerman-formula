# TX1_temperature_leaf: FROZEN CRITERIA, committed alone before any script of this lane or any graded number

Owner's go, 2026-11-02. **Not blind.** Read before this freeze: BK2 (README, criteria, A1, A2, lib, search, read, stage2, gates, dear, checks), TG1, KS1, BF2, SR3 READMEs, BF3 criteria and `bf3_common.py`, LW1's key path, UX6's Bullet hook. I know BK2's closest rows, that gas fraction acts as a sample label in SR3 and BF2, that BF2's control read 0, 15, 266. Of the new data I have seen only headers and first rows: units, bin counts, and the ratio KT / T_X per cluster. No law residual against T has been computed. A description: no action, no field equation. kappa = 1/2 FITTED. Cold sector stays retired; nothing here reinstates it. No particle. No LCDM input. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2 searched and reported apart, never pooled. Not theory closed. Nothing here says the data favour the framework.

## Question
With T(r) as a leaf, does any form do better on galaxies and clusters than forms without it, and beat scrambled T?

## Units, how they are established
Leaf **s2 = k T / (mu m_p)**, dimension L^2 T^-2, mu = 0.6 (the convention of the header's T500, checked below), k T in joules.
- **k T in keV: `spectral_results_<cluster>.fits` column KT, TUNIT keV,** the direct measurement; errors from KT_LO, KT_HI, read as offsets. T_X in `<cluster>_temperature.fits` has TUNIT T/T500 and header T500 "Self-similar T500 in keV".
- **Radius: RW_X x header R500** ("Hydrostatic-equilibrium R500 in kpc"), TUNIT R/R500, bin for bin with spectral_results where lengths match; a mismatch or a non-constant KT / T_X (seen: A2029, ZW1215) is printed per cluster. Checked: KT / (T_X T500) per cluster; RADIUS (arcmin) against RW_X R500; header R500 against the hydro file's on disk; T500 against 8.85 keV (M500/1e15)^(2/3) E(z)^(2/3), Ghirardini+19, recalled, PROVISIONAL, E(z) used for this unit check only and for nothing graded.
- **These are projected X-ray temperatures,** T_SZ (x T500) is P_SZ/n_e, three-dimensional, and starts near 0.5 R500. Primary is KT. T_SZ, x >= 0.5, is reported beside on the plain question and X-COP rows of finalists.
- All 12 files get a sha256 in the lane's `SOURCES_USED.txt`, with the tar's sha256. `wb/` is not used. The directory stays untracked.

## The crux: mapping T where none is measured
**Primary mapping M0: s2 = 0 on every row with no measured hot-gas T:** Solar System, SPARC, LITTLE THINGS, dwarfs, IC 1613, Milky Way, DiskMass, galaxy lensing, groups. Consequences, stated now:
1. A form with T in a denominator or a negative power is infinite there, so it's NOT EVALUABLE and excluded, structurally. That is a cost of M0.
2. **A T term can act only on clusters. So on all those rows a T form equals its T = 0 part, whose failures it inherits, and T can act as a "this is a cluster" label.** It can't lift dwarfs or IC 1613. M0 is therefore the reading most exposed to the label danger; the label arm below measures that.
3. Groups do have hot gas in nature. No T for them is on disk: T = 0 there is a reading, tagged.

**Rejected:** any T built from observed g or observed sigma on the target row: circular.
**M1, sensitivity, finalists only, no vote:** s2 = r g_b on galaxy rows, built from baryons. It adds no information, since Phi_b is already a leaf. **M2, sensitivity, finalists only, no vote:** discs' and LITTLE THINGS' cold gas at sigma 10 km/s, PROVISIONAL, recalled.

**Clusters.** X-COP rows use their own measured T, log-interpolated in r, held at the ends. On the 7 with stellar files (BK2's rows): train positions 0, 2, 4, 6, holdout the rest.

**Keys, 326 clusters, no T(r).** T_i(r) = KT_i tau(r/R500_i), R500_i as the path's. KT_i: eRASS1 KT where > 0, the KT clusters the key definitions already use; TG1 measured its scatter as noise-dominated, rms 0.325 dex. **Clusters lacking KT (printed count, expected about 220 of 326) are FILLED from an OLS fit lg KT on lg Mgas500 on those with KT,** so their T is gas in disguise, no independent information; stated in every key row. tau(x) = median over the 12 X-COP clusters of T_X/T_ew, T_ew the mean spectral KT over x <= 1, weighted by NORM x annulus area; T_SZ/T_ew extends it to its end near 1.7; held constant inside the first and beyond the last node. Sensitivities, top 3 only, no vote: lacking clusters at median KT; tau = 0 beyond 1.7 R500.
**Bullet.** s2 = s2(14 keV) x g_gas/g_b, on the gas by construction; 14 keV PROVISIONAL, recalled. No map on disk. **Expected kill, stated now: T sits on the gas, so a T term peaks on the gas; the verdict line says so whatever it reads.**

## The main danger: self-fitting
**X-COP's M_HSE comes from T and the gas** by hydrostatic equilibrium, M ~ s2 r/G x (log slopes). So a form c s2/r can reach M_HSE by identity, not by physics. Therefore:
- **A pass on any X-COP gate by a form with an effective T term carries the tag SELF-FIT EXPOSED and is not evidence.** It remains a required gate, not a sufficient one.
- **The real test is non-hydrostatic: 15 shear keys.** KT there is pointed-free survey temperature, independent of the shear apart from the catalogue's M500 calibration, which M500 is not used for T.
- K5 below prints how close the pure identity forms get, no baryons in them, as the measure of the danger.
- **Effective:** median |log10(F / F(T=0))| >= 0.05 dex on X-COP train. A form with s2 in it below that is T DECORATIVE and counted as T-free.

## Grammar
BK2's, reused by import, with **s2 added to LEAF and DIM (2, -2, 0)**: same exponents, constants, D, A, interpolations, top forms T1-T4. **T5 is not run: no fitted float.** BK2's search and read code are imported, monkeypatched only for leaves, train rows and chunk directory; nothing in BK2 is edited.
- **Pool selection:** BK2's closure is called at twice the cap, then half the cap goes to the cheapest T-bearing members and half to the cheapest T-free, because T-free forms are BK2's ground already. Caps real, closure sizes reported.
- **Levels: TL0, cap 15,000 each, every arm below. TL1, cap 30,000 each, real and C1, C2, both footings.** T0, cap 1,500, planted and rerun.
- BK2's inside-search G3 test (A2) applies at all levels, with Z_shape as below, so hits are bounded. Hits capped 150 MB per arm; a binding cap is reported.

## Gates, per footing
Each has **LINE and ERR**, as BK2. Tolerances fixed here. Unchanged from BK2's table unless stated: G1a Newton, G1b Cassini, G4/G6 (LT), G7 groups, G8 keys, G9 dwarfs, G10 IC 1613, G11 MW, G12 DiskMass, G13 Bullet. Under M0 all but keys and Bullet read the T = 0 part.
- **G2' SPARC:** owner's path: FG1's free-Upsilon S line, rms <= 0.110, median U 0.50-0.80, on the odd names for train; tilt <= 0.15; ERR: Z_U <= 2 and rms <= 0.110. BF2 showed this line generous; said beside any pass, with the law's 0.054. Cheap prefilter, looser, as BK2's: subsample rms <= 1.3 x law, |median| <= 0.10 at Upsilon 0.5. Fixed-Upsilon G2 reported beside.
- **G4' SPARC even names:** same S line.
- **G3, G5 X-COP train, holdout:** LINE as BK2, |mean| <= 0.05, rms <= 0.10. ERR Z_mean as BK2 (0.12 dex HSE). **Z_shape amended from BK2, which flagged its own as too strict:** sigma_i^2 = EM_FORW^2 + model spread^2 + (eT/T/ln 10)^2 + s_c^2. **s_c is cluster scatter, by rule: rms over the 7 clusters and five x of the residual of lg M_HSE on lg M_b fitted at each x. Computed from data and printed before any search, not chosen.** The eT term is applied to all forms, including T-free. This widens ERR against BK2's, and I'll report BK2's strict tally beside.
- **G5b cluster splits:** each of 7 clusters' mean residual, Z = mean_c / sqrt(se_c^2 + 0.12^2), |Z| <= 2; and low-mass half against high-mass half by M500, difference Z, |Z| <= 2, with se from the rows' scatter by cluster.
- **G14 galaxy lensing:** BF3's Gate L arithmetic on F: L-abs chi^2_sys <= 77.2 and L-law <= law's + 21.2, s = 0.125, PROVISIONAL as BF3. Reported on cov-only too.
- **Clusters lacking T on any gate:** none on X-COP's 7; all 12 have T. Stars on 7 only, so 5 only reach the plain question. Keys as above. A leaf undefined means NOT EVALUABLE, never a pass.

## The plain question first, cheap, no search
Across the 12: y = lg(M_HSE / M_law) at x 0.3, 0.5, 0.7 and their mean, M_b gas + stars, the 5 lacking stars at the 7's median M*/M_gas at that x, [READING]. t = lg kT(x) residual on lg M_b(x). Also at fixed M500, using lg M500 in place of lg M_b. OLS slope b, se bootstrap over clusters, permutation p, 20000 draws. Joint y on t and lg M_b as TG1's, Z_T, Z_G.
- **PQ NONE:** |b|/se < 3 or p > 0.01, on the mean row.
- **PQ IDENTITY:** passes that and |b - 1| < 2 se, since at fixed gas M_HSE ~ T gives slope about 1. No physical reading.
- **PQ BEYOND IDENTITY:** significant and differs from 1 by >= 2 se.
Printed per footing, X-ray and SZ T. Compared with TG1, in words: TG1 is shear and noisy KT, this is hydrostatic and pointed T, so they don't test the same thing.

## Controls, same gates, same tolerances
- **Scrambled T, seeds C1 20261102, C2 1, C3 2:** s2 permuted across rows inside X-COP train and inside holdout, all else real, target real; on keys, KT permuted across all 326 clusters at the same seed. Three seeds at TL0, both footings; C1, C2 at TL1.
- **Label arm:** every X-COP row, and every key cluster, gets the same s2: the median of X-COP train's. It holds "is a cluster" and nothing else. Both footings at TL0.
- Counts per gate, per arm, per expressions tried, T-effective only. Top forms for keys below, same rule per arm.
- **Look-elsewhere:** expressions enumerated, passing G1a, distinct; p_local and Sidak for any ERR passer, as BK2; real over each control.
- **Planted:** P1 g = I5(g_b, a0) + pi s2/r; P2 g = I5(g_b, a0) (1 + pi s2/Phi_b), targets replaced on train and holdout: must be returned by the search's own output with residual rms < 1e-6, and pass G3, G5 LINE; P1 at TL0 and T0, P2 at T0. **If recovery fails, "nothing found" is not proof of absence and the title says so.**

## Dear gates
Top 10 T-effective per arm and footing by Z, ranked as BK2 on train gates G2', G3, go through keys at the primary cell (gas +0.005, f* 0.034, both h), plus T-free references: the same run's best T-free by Z, and BK2's row (a). The real arm's top 10 also through G5, G5b, G4', LT, groups, G14, dwarfs, IC 1613, DiskMass; top 5 through MW, Bullet (present and carried, as BK2). A form passing all up to keys gets the other three cells. If wall-time forces fewer, I report it.

## Labels, per footing, frozen
- **T DOES BETTER, ABOVE CONTROL:** a T-effective form with G1, G2', G3, G4', G5, G5b, LT, groups, and keys 15 of 15, p >= 0.05, M3 Z_tot < 2 at both h, on ERR; **and** passes strictly more gates than the best T-free reference without failing one it passes; **and** the real count of forms meeting this is above 3 x the largest control count, label arm included, per expression. Second implementation owed before any further word.
- **T DOES BETTER, NOT ABOVE CONTROL:** first two parts hold, control comes as close. T acts as a label.
- **SELF-FIT ONLY:** T forms reach X-COP, with keys not better than T-free references.
- **NO T GAIN:** none of the above, including nothing past train.
Dwarfs, IC 1613, MW, DiskMass, lensing, Bullet don't block the first two labels because they read the T = 0 part, but they're reported beside, and "SURVIVOR" as BK2's meaning, every line, is said only if they all pass.

## Checks
K1 law row through this lane's leaves equals BK2's K1 on X-COP, SPARC, LT, groups, S; K2 any form at s2 = 0 equals its T-free string to 1e-12; K3 units: KT/(T_X T500) within 0.95-1.05 for each cluster's median, 5 keV gives sqrt(s2) 893 km/s within 1 km/s; K4 dimension, BK2's unit test with s2; K5 identity rows c s2/r for BK2's constants, X-COP rms printed; K6 keys law row through the T patch: M3 +4.76, chi^2 65.0 as BK2's; K7 Bullet law row -0.068, -0.111; K8 tau positive and finite, normalisation printed.
**MUTATE twin, must fail, separate outputs:** a0 x 1.5 and s2 x 1000 (the eV-keV slip) in checks, exit 1; X-COP tolerance 1e-6, zero hits; T-scramble in K3's pairing fails K3.
**Rerun byte-identical** at T0.

## Expectation, mine, on record
PQ IDENTITY 45 %, PQ NONE 45 %, BEYOND 10 %. T forms pass X-COP LINE: 95 %, by identity. T-effective form with keys 15/15: 25 %. T DOES BETTER, ABOVE CONTROL on a footing: 3 %. Label arm as close as real: 70 %. Planted recovered: 90 %. Bullet fails with wrong sign on every T form: 90 %. Most likely verdict: SELF-FIT ONLY or NO T GAIN.

## Compute
nice 19, at most 2 processes, one thread, under 1 GB each, as measured by me; chunks gitignored; about 17 GB free, so outputs small. BF1, BK2, BF3, RS1, WA1 jobs and files untouched. No downloads. Lane directory only; commit by explicit path; no push.
