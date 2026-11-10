# RB1: form B on the hot systems (groups, X-COP, the Bullet). FROZEN CRITERIA

Committed alone, before any RB1 script exists and before any RB1 number is computed. TEST lane: it relabels nothing, adopts
nothing and is not registered. kappa = 1/2 FITTED; not theory closed. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt
(a0 = 1.1312e-10 m/s^2), graded separately and never pooled. Cold dark energy is a gravitating field component with w about 0,
never a particle; it is never called cold dark matter. Nothing here says the data favour the framework.

## 0. Form B as graded here (frozen once)

- A group or cluster holds R times the baryons that fell into it as cold dark energy. The cold component is collisionless, so it
  stays when gas is expelled or stripped. The central galaxy's phantom is part of that same component, not an addition. There is
  no law boost on the hot gas and no external field effect: gravity is Newtonian with the total mass.
- So M_dyn(<r) = M_b,obs(<r) + M_cold(<r), and at a system's edge M_cold = R x (baryons that fell in) >= R x M_b,obs.
- **Retained fraction:** f_ret(<r) = R M_b,obs(<r) / [M_dyn(<r) - M_b,obs(<r)]. Under B it can never exceed 1 at the edge.
  If M_dyn <= M_b,obs the system counts as f_ret = +infinity (above 1).
- **R = 5.41** (lane F1; the QX15 footings give omega_d / omega_b = 5.409 / 5.411). Bracket R = 5.562 (SWT1).
- **Where a0 enters.** Gates 1, 2 and 4 contain no a0: B's cold mass is real mass and the masses are measured. Both footings are
  still run and reported; their gate 1, 2 and 4 numbers are expected to be identical, and the script checks that. a0 enters only
  through (i) the comparison with the law in TR1's statistic (gate 3), (ii) the law-only and PD1 known answers, and (iii) one
  reported inner row: the central galaxy's phantom inside the innermost X-COP bins against the measured cold mass there (B needs
  measured cold >= the stars' own law phantom; reported, not graded).

## 1. Gate 1, conservation (HARD, ONE-SIDED)

Statistic per class: the median f_ret at the class's outermost measured aperture, with a 95 % interval from 10,000 bootstrap
resamples of the systems (seed 1109). Per-system errors are propagated (lognormal, 4,000 draws) only for the reported count of
systems individually above 1 at more than 2 sigma; they do not enter the class interval (the spread among systems already holds them).

| class | systems, aperture | baryons (graded) | brackets (reported) |
|---|---|---|---|
| **G-H** hydrostatic groups | Lovisari+15, 20 groups, R500 (outermost tabulated); M500, Mgas500 and their errors as transcribed | gas + stars from the Kravtsov, Vikhlinin & Meshcheryakov 2018 relation M*,500 = 1.7e12 (M500/1e14)^0.6 (an observational relation, stated import; BCG + ICL + satellites) | gas only; KVM18 x 1.5 and / 1.5; stars = gas (PD1's bracket) |
| **C-X** X-COP | the 7 clusters with measured stellar profiles, at the outermost radius where hydrostatic M_FORW, gas and stars are all tabulated (HL3's builder: the gas-profile grid, Ettori 2019 R500) | measured gas + measured stars | all 12 with HL3's imputed stars; at R500 instead of the last radius; h rescaled from 0.7 to the footing's h (f_gas scales as h^-1/2) |
| **G-DB** dynamical, X-ray bright | KT2017 groups with an eRASS1 match (HG1's builder copied: Nm >= 5, eRASS1 footprint, 14 groups), at r = 4/3 R_h (Wolf's half-mass radius), M_dyn = 3 sigma^2 r / G | 0.5 x 0.6 L_K + eRASS1 Mgas500 scaled to r by HG1's beta model (HG1's convention) | GA1's audited gas (12 groups, its PRIMARY table) |
| **G-DF** dynamical, X-ray faint | the 176 KT2017 groups without an eRASS1 match, same aperture | stars only (gas 0): **a lower bound on f_ret** | faint gas 0.1 x and 1.0 x the stars |

- **Line:** a class **FAILS** if the lower end of its 95 % interval is above 1. Otherwise it is **CONSISTENT**. A class with fewer
  than 5 systems is NOT EVALUABLE.
- **Tags:** [STAR-DEPENDENT] if a G-H label changes between KVM18 / 1.5 and KVM18 x 1.5; [INNER APERTURE] on G-DB and G-DF (Wolf's
  radius lies inside the system's edge; baryons more concentrated than the cold could exceed 1 there without breaking B, and a cold
  more concentrated than the members hides a deficit).
- **Gate 1 label per footing:** FAILS if any graded class FAILS; else CONSISTENT; NOT EVALUABLE if MUTATE M1 (R x 2) flips no class
  to FAILS (no power).
- **Stated plainly: gate 1 is one-sided.** B cannot fail it from below: f_ret < 1 is read as baryons lost, and nothing on disk
  measures where they went. The two-sided amount gate stays **FAIL as PD1 graded it** (PD1 A1 / A2: groups 0 and 9 of 20 at the
  cosmic share, the Bullet subcluster 2.6 sigma low). **The measurement that closes the gap:** an independent census of the baryons
  between R500 and the turnaround radius around the same groups (stacked thermal SZ, i.e. Compton y, plus X-ray surface brightness
  out to 3-5 R500, and the stars there), with a total mass to the same radius that does not assume hydrostatic equilibrium (stacked
  weak lensing). Under B the lost gas must be there: f_ret(<r_ta) = 1. That turns gate 1 two-sided.
- Reported beside: hydrostatic bias if M_true = M_HSE / (1 - b), b = 0.1 and 0.2 (it lowers f_ret; never graded, because the
  literature sizes of b are themselves set by assuming the cosmic baryon fraction).

## 2. Gate 2, trend with depth

- **Ladder (graded):** G-H's 20 groups and C-X's 7 clusters, both at R500 (X-COP's M500 = M_FORW at the Ettori R500), f_ret with the
  graded baryons. OLS of log10 f_ret on log10 M500; slope interval from 10,000 bootstrap resamples of the 27 systems (seed 1109).
- **T1 (does not fall with depth):** FAILS if the 97.5th percentile of the slope is below 0.
- **T2 (approaches 1 in the richest clusters):** C-X's median f_ret at its outermost radius (gate 1's number); FAILS if the upper end
  of its 95 % interval is below 0.85. The 0.85 is a frozen choice (at most 15 % of the infallen baryons missing in the deepest wells).
- **Gate 2 label:** CONSISTENT iff T1 and T2 both hold; else FAILS. Tag [STAR-DEPENDENT] if T1 changes between gas only and KVM18 x 1.5.
- **Reported, not graded:** the extended hydrostatic ladder from `rebuild_2026_10_22/GS4_pointed_gas_offset/gs4_inputs.csv`
  (FR1's line-H catalogues L20, L15, S09, L13; X-COP removed by position within 6 arcmin and |dz| <= 0.02; duplicates merged by the
  same rule, median of log M and log Mgas), gas only and with KVM18 stars; Spearman of f_ret on sigma inside G-DB and G-DF.

## 3. Gate 3, X-COP radial shape (R fixed, the record's own cold profile)

- **Cold profile:** ZN4's native shape (`rebuild_2026_10_22/ZN4_cluster_resolution/zn4_shapes.json`): the record's own collisionless
  zooms, no a0 and no LCDM input in their dynamics. This is the profile FR1's fair-share row used (ZN4's native profile). The z = 0
  snapshot (X-COP z < 0.125, ZN1's rule), m(x) = M(<x R200)/M200 interpolated in log M200 between the 1e14 and 1e15 stacks (clamped),
  M proportional to r^2 below the tabulated x, m held constant beyond x_edge (no tail; reported if any X-COP point lies there).
- **Model:** M_model(<r) = M_b,obs(<r) + f_c M200 m(r/R200), f_c = R/(1+R), M200 = 200 rho_c(z) (4 pi/3) R200^3 with the data's
  convention (h 0.7, Omega_m 0.3). **Anchor:** f_c M200 m(r_last/R200) = R M_b,obs(<r_last) at each cluster's outermost radius, i.e.
  B's minimum cold (f_ret = 1 there); R200 solved from that one equation.
- **Statistic:** per point Delta = log10(M_FORW / M_model) on HL3's grid for the 7 measured-star clusters; per-cluster medians in
  r/R500 bins [0, 0.25, 0.5, 0.75, 1, 2], then the median over clusters (TR1's cl_bin_median). A bin is graded if it holds >= 5 clusters.
- **Line:** CONSISTENT iff |bin median Delta| <= 0.10 dex in every graded bin; else FAILS.
- **Beside it, the missing-mass fraction in TR1's statistic:** f_X = (M - M_law(M_b))/M per bin, cluster medians, the model's mass in
  place of the measured, against TR1's measured 0.71 / 0.66 / 0.58 / 0.46 / 0.32 (canonical) and 0.68 / 0.63 / 0.54 / 0.41 / 0.26 (alt).
  Stated: under B the measured cold fraction is (M_dyn - M_b)/M_dyn, not TR1's law-relative fraction; both are printed for model and data.
- **Reported, not graded:** the anchor at R500 instead of r_last; R = 5.562; all 12 clusters with imputed stars; **NFW with Duffy
  2008 c200 in place of the native shape (EXTERNALLY CALIBRATED, reported separately)**; the inner row of section 0 (iii).

## 4. Gate 4, the Bullet

- **Machinery:** UX6's Bullet model as DB1's child and PD1 A2 ran it (gas and galaxy Plummer components, Clowe's apertures, the peak
  finder, DB1's tolerances: M300 observed 3.5e14 / 2.3e14, sigma 0.15 PROVISIONAL), **copied** into rb1.py (not imported).
  Gravity Newtonian (a0 -> 1e-30, as PD1 A2). The cold mass of cluster j sits with its galaxies through DB1's on="gal" placement
  (R_j x that cluster's galaxy Plummer field).
- **Cold amount:** M_cold,j = R (M_star,j + M_gas,j,infall). The model's gas totals 2.232e14 Msun; the record assigns 2.000e14 to the
  main cluster and 2.32e13 to the subcluster (its three components). **Stripped-gas assignment, frozen:**
  - **S1, graded:** both clusters entered with the same gas-to-star ratio; the total gas is shared in proportion to the stars
    (main 1.196e13, sub 4.0e12 Msun of stars). Total gas, and so the total cold, is conserved; only the split between the clusters
    moves. It uses no outside number.
  - **S0, bracket:** nothing reassigned (the record's split). This is exactly PD1 A2's galaxy-traced row (5.41 x the record's baryons
    of each cluster, all placed with the galaxies), so it is also the known answer KA-3b.
  - **S1/2, bracket:** half of S1's transfer.
- **Line:** CONSISTENT iff DB1's row label is PASS (class not FAIL and |Z_M300| <= DB1's ZL for both clusters), as PD1 graded P5;
  else FAILS. Offsets (d_gal, d_gas, Z), M300 and class are printed. Tag [STRIPPING-DEPENDENT] if S0, S1/2 and S1 disagree.
- **Reported:** the cold with ZN4's native shape centred on each cluster's galaxies instead of the galaxy Plummer (M300 only,
  projected by Abel integration; truncated at x_edge); R = 5.562; the stripped mass the subcluster would need for |Z| <= 2.

## 5. Labels (vocabulary frozen)

- Per gate and footing: **CONSISTENT / FAILS / NOT EVALUABLE**, with the tags above.
- **Overall per footing:** FAILS if any gate FAILS; otherwise **NOT FALSIFIED (ONE-SIDED)** if at least one gate is CONSISTENT and
  none FAILS; NOT EVALUABLE if none is evaluable. **The overall label is never PASS**, because gate 1 is one-sided and the two-sided
  amount gate stays FAIL as PD1 graded it.
- A known-answer failure gives NO VERDICT for the gates it feeds.

## 6. Known answers (with my own loaders; each can fail)

- **KA-1 (PD1's bracket, share 5.41, full share in the core):** X-COP mean +0.019 / +0.010; groups 0 and 9 of 20 canonical (0 and 8
  alt), medians +0.30 / +0.04 (+0.31 / +0.04 alt). Tolerance 0.002 dex on means and medians, exact counts. PD1's machinery (turnaround
  shell solver, share table, Duffy NFW core, isothermal remainder) is copied from `pd1.py`, `pd1_a1.py` and SS1's `ss1_core.halo`.
- **KA-2 (TR1's fractions):** the D-reading cluster medians of M_X / M_dyn per bin, canonical 0.71 / 0.66 / 0.58 / 0.46 / 0.32 and alt
  0.68 / 0.63 / 0.54 / 0.41 / 0.26, to 0.005.
- **KA-3 (Bullet):** (a) the law-only row Z -4.548 / -4.540 (DB1) to 0.01; (b) S0 = PD1 A2's galaxy-traced Newtonian row,
  M300 Z +0.49 / -2.58, d_gal 14 / 22 kpc, d_gas 197 / 136 kpc, to 0.02 in Z and 2 kpc.
- **KA-4 (identities):** a synthetic system with M_dyn = (1 + R) M_b gives f_ret = 1 to 1e-12; the native shape has m(1) = 1 to 1e-3;
  the anchor solver returns the anchor to 1e-8; both footings give identical gate 1, 2 and 4 numbers.
- **KA-5 (parsers):** 20 Lovisari groups; 12 X-COP clusters, 7 with measured stars; KT2017 builder 190 groups, 14 BRIGHT, 176 FAINT (HG2's K4).

## 7. MUTATE (separate output files `rb1_MUTATE.out` / `.json`)

- **M1, R x 2:** must push classes over 1 (gate 1 power). If no class flips to FAILS, gate 1 is NOT EVALUABLE.
- **M2, baryon masses scrambled across the ladder's systems** (one fixed permutation, seed 1109, plus the median slope of 1,000
  permutations): must destroy the trend; bites if the scrambled slope's 95 % interval excludes the real slope.
- **M3, native shape stretched r x 1.5:** must move gate 3's bins by >= 0.05 dex rms.
- **M4, Bullet cold placed on the gas** (DB1's on="gas"): the offsets must fail (class FAIL).
A MUTATE that does not bite is reported as such, and the gate it controls gets NOT EVALUABLE.

## 8. Seen before freezing (disclosed), and hand estimates

- **Read:** the owner decision of 2026-11-09 (form B); PD1's criteria, A1, A2, RESULT and the bracket outputs (the KA-1 numbers);
  TR1's RESULT (the five fractions); FR1's README; ZN1's and ZN4's READMEs and the keys of `zn4_shapes.json`; HX1's, GA1's and HG2's
  READMEs and the keys of GA1's PRIMARY table; DB1's Bullet tolerances; UX6's Bullet model code; HL3's printed radial ranges of the
  X-COP profiles (outermost radius 1.0 to 2.0 R500); the column names of the X-COP FITS files; the QX15 footing backgrounds. No f_ret,
  no slope, no residual and no Bullet row has been computed under RB1.
- **The brief's hand estimate (unverified):** f_ret about 0.5 to 0.9 in groups and about 0.96 in X-COP at the last bin, rising with
  depth; the Bullet subcluster closer than 2.6 sigma once its stripped gas is counted.
- **Mine:** G-H about 0.5 to 0.7 (gas only about 0.4), CONSISTENT. **C-X is the risk:** X-COP's hydrostatic gas fraction near R200 is
  about 0.15, so with stars f_ret may sit at 0.95 to 1.05; I give 30 % that C-X's class sits above 1 beyond its errors on raw
  hydrostatic masses. T1 positive (FR1 measured gas-only Y500 rising, slope +0.22), 85 % CONSISTENT. Gate 3: 55 % CONSISTENT, the
  inner bin the likely miss (ZN1 found its native profile too heavy inside 0.3 R500). Bullet S1: by hand sub Z about +1, main about
  -0.5, so 60 % CONSISTENT, with S0 failing as PD1 found: [STRIPPING-DEPENDENT] likely.

## 9. Operational

One thread, nice 10, RSS < 2 GB; caches in the scratchpad; nothing large in the repo. Files: `rb1.py` -> `rb1.out` / `rb1.json`,
`rb1_MUTATE.out` / `rb1_MUTATE.json`, `RESULT.md`. Explicit-path commits only; pushed by replaying the commits in a sparse temporary
worktree of origin/main. Other lanes' folders are read only; their code is copied, not imported.

kappa = 1/2 FITTED; not theory closed. Relabels nothing.
