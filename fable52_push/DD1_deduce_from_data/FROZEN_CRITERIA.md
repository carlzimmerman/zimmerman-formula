# DD1 FROZEN CRITERIA: deduce the rule from the data (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled (canonical a0
9.3603e-11, alt 1.1312e-10 m/s^2). Committed alone, before any DD1 script exists or any DD1 number is computed.
The id DD1 was checked free (`ls -d fable52_push/DD1*`, and no commit subject names DD1).

## Question

Using only measured quantities, across every class of system on disk, does the non-baryonic mass follow ONE rule, and
if so in which variable? If not, which class breaks every candidate, and by how much? The lane assumes no theory.

The statistic (SHP1's): X = g_obs / g_bar - 1 = M_C(<r) / M_b(<r), the enclosed non-baryonic mass over the enclosed
baryonic mass, spherical equivalent. Every fit and score is done in Y = log10(g_obs / g_bar) = log10(1 + X), so a
residual is dex in g_obs at fixed g_bar. A rule X = F(v) is the same as Y = log10(1 + F(v)).

## Step 0: the table (frozen before any fit)

One row per point: system, class, r (kpc), g_bar, g_obs, e_lgbar, e_lgobs, e_Y (dex), z, and the variables below.
`dd1_table.py` builds it and writes `dd1_table.csv`; the table is frozen when committed, before `dd1.py` runs.
Raw data only. No halo masses, concentrations, NFW-based masses, abundance matching or simulation results.

| class | source on disk (loader reused) | point(s) | g_bar contains | main systematic |
|---|---|---|---|---|
| SPARC | `real_research/data/sparc_data`, `SPARC_Lelli2016c.mrt` (SHP1 / FLD1 loader and cuts) | every point passing SHP1's cuts | stars (Upsilon 0.5 / 0.7 at 3.6 um), HI x 1.33 | Upsilon, distance, inclination |
| faint rotators | `faint_rotators_mcquinn2022/` t1, t2 (McQuinn+2022) | one, at Rmax; Vcor | stars + HI (logMbary, total taken as enclosed) | asymmetric drift, total vs enclosed |
| tidal dwarfs | `tidal_dwarfs/lelli2015_tdg.csv` (Lelli+2015) | one, at R_out; V_circ | HI + H2 + stars (M_bar, total as enclosed) | inclination, equilibrium |
| massive spirals | `diteodoro2023_*` (Di Teodoro+2023) | last tabulated point | stars (W1) + gas 1.36 HI (totals) | curves read off figures; flagged pair dropped |
| ATLAS3D | `atlas3d_fj_table.tsv` (Cappellari+2013 XV, XX), qual >= 1 | one, at r12 (3D half light) | stars: SPS Salpeter M/L x 0.61 (Chabrier) | IMF (Salpeter bracket reported), JAM mass-follows-light |
| RC100 | `data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv` (FLD1's input) | one, at Re: g_obs = Vc^2/Re, g_bar = G (Mbar/2)/Re^2 | stars + cold gas (paper's Mbar) | Mbar, pressure correction; no errors on disk |
| KiDS | B21 Fig-9 Massbin-1..4 with covariance (SHP1 / SNP1 conversion) | 15 per mass bin; a bin is a system | stars + B21 cold gas, no hot gas | stellar masses, SIS conversion, host leakage, calibration |
| groups | `lovisari2015_groups.tsv` (RB1 / QX5 loader) | one, at R500 | hot gas + stars from KVM18 (RB1's stated import) | hydrostatic bias, stars by scaling relation |
| X-COP | `real_research/data/xcop/` (RB1 / HL3 loader), the 7 with measured stars | log grid, 0.1 dex steps, 30 kpc (or first gas radius) to last gas radius | hot gas + measured stars | hydrostatic bias, M_FORW form |
| CLASH | `clash_rar_tian2020_fig2.tsv` (HL3 loader), z from `_external_data/hl3/umetsu16/src/table1.tex` | 84 points as published | hot gas + BCG (Tian+2020) | lensing model, satellites' stars missing |
| MW bright dwarfs | `dsph/lvd_dwarf_mw.csv` (RB2 loader) | one, at r12 = 4/3 r_h (Wolf) | stars (M/L_V 2) | equilibrium, tides, binaries |
| MW ultra-faints | same, M_V > -7.7 | same | same | same |
| M31 dwarfs | `dsph/lvd_dwarf_m31.csv` | same | same | same |
| LG field dwarfs | `dsph/lvd_dwarf_local_field.csv` | same | stars only; their HI is not counted | gas omitted |
| Coma UDGs | `freundlich2022_coma_udgs.tsv` (RB2 loader) | one, at 4/3 R_e | stars (L x M/L) | membership, anisotropy |
| NGC 1052 UDGs | DF2, DF4 values as RB2 copies them | one, at 4/3 R_e | stars | distance, tides |

Details, frozen:
- SPARC: r = R; e_lgobs = sqrt((2 eV/V)^2 + (2 eInc / tan inc)^2 + (eD/D)^2) / ln10; e_lgbar = sqrt((0.11 f_s)^2 +
  (0.04 (1 - f_s))^2), f_s the stellar share of g_bar. z = 73 D / c (SPARC's H0). M_b(<r) = g_bar r^2 / G.
- Dwarfs: RB2's `load_lvd` and its default construction at central values: binary factor as RB2's `build` default
  (`binmode="free"`), M_* = 10^mass_stellar, g_obs = 3 sigma^2 / r12, g_bar = G (M_*/2) / r12^2. Rows whose sigma is an
  upper limit are dropped (not a measurement); LMC, SMC, M 32 and Sagittarius are dropped. MW rows with M_V > -7.7 are
  ultra-faints, the rest bright. e_Y = sqrt((2 e_sigma/sigma)^2 + (e_r/r)^2 + (e_D/D)^2) / ln10 (+) 0.1 dex (M/L).
- Faint rotators: galaxies that are also SPARC files are dropped (kept in SPARC).
- ATLAS3D: r12 from logr12 (arcsec) and Dist; M_dyn(<r12) = L 10^logML_JAM / 2, M_b(<r12) = 0.61 L 10^logML_Salp / 2
  (logML_stars is a decomposition with a halo and is not used). e_lgobs 0.05, e_lgbar 0.10 (stated; none on disk).
- RC100: e_lgobs 0.087 (Vc 10 %), e_lgbar 0.20 (stated; none on disk). A thin exponential disc at Re gives
  v_bar^2 Re / (G M) = 0.497, so G (Mbar/2)/Re^2 is also the disc's own field there (to 1 %).
- KiDS: g_obs = 4 G ESD / bias (SHP1, SNP1); e_lgobs from the covariance diagonal; e_lgbar 0.20 (B21's stellar-mass
  systematic, stated). r = sqrt(G M_rep / g_bar) with SNP1's log M_rep 9.4 / 10.45 / 10.7 / 10.9. z = median z of
  `lr_lenses.npz` (KO1's lens catalogue) in each B21 mass bin. Points with g_obs <= 0 keep Y = -inf (medians handle it).
  Hot-gas bracket: B21's Nobins hot-gas file as one system replaces the four bins in a bracket run (reported). No
  per-bin hot-gas file exists on disk.
- Groups: g_obs = G M500 / R500^2, g_bar = G (Mgas500 + M_*) / R500^2, M_* = KVM18(M500) as RB1; e from eM500,
  eMgas500, 0.2 dex on M_*.
- X-COP: M_dyn = M_FORW, M_b = MGAS + MSTAR, log-log interpolated; errors EM_FORW and (HI - LO)/2. The 5 clusters
  without a stellar file are left out (stars not measured).
- Coma UDGs: every row with a dispersion; e_Y from esig, 0.2 dex on M_*, 10 % on R_e. z 0.0231.
- Left out, with the reason recorded in RESULT.md: SLACS (projected aperture masses only), LITTLE THINGS (no errors,
  LaTeX only), KMOS3D / KROSS / MSA3D (no radius or no gas), globular clusters (masses from N-body fits to the
  dynamics: no independent baryonic mass), Milky Way curve (no baryon model on disk), Collins+2013 M31 (duplicates
  LVD), group / cluster catalogues with scaling-relation or NFW masses, eRASS1, eFEDS, PSZ2.

## Step 1: SHP1 reproduced (KA1)

## Step 2: candidates (frozen before any fit)

Variables per point (log10 throughout): lgb = g_bar; lgo = g_obs; dep = g_obs r / c^2 (local depth: V_obs^2, 3 sigma^2
for Wolf points, 4 G ESD R for lensing, G M_HSE / r for clusters); dsys = the system's largest dep (system depth);
Sig = baryonic mass inside the half-light radius over pi R_h^2 (Msun/pc^2; SPARC: g_bar(R_eff)/(pi G) interpolated on
its own curve; RC100: (Mbar/2)/(pi Re^2); ATLAS3D: (M_b/2)/(pi Re^2); dwarfs and UDGs: (M_*/2)/(pi r_h^2); other
classes have no measured half-light radius and are NOT COVERED); Mb = g_bar r^2 / G; r (kpc); zz = log10(z + 0.001).
Note: Mb(<r)/(pi r^2) = g_bar/(pi G), so an enclosed surface density is variable (a) itself; (d) is the system's own.
Note: x = sqrt(a0/g_bar) and g_obs/a0 are lgb and lgo shifted by a constant, so free-F rules in them do not depend on
a0 (Lean `law_scale`); a0 enters only the law rows L0 and the synthetic law answer.

One-variable rules Y = F(v), F free: (a) lgb, (b) lgo, (c) dep, (c') dsys, (d) Sig [partial], (e) Mb, (f) r,
(g) zz (control: must fail).

Fit of F: bins 0.2 dex wide on a fixed grid (edges at multiples of 0.2); a bin with at least 5 training points gives
a node at the weighted median of v and of Y, each system's points weighted 1 / N_points(system). Prediction: linear
interpolation between nodes; beyond the end nodes, the least-squares line through the three end nodes. Bin medians
that are -inf are dropped.

Two-variable rules Y = F(v1, v2), physically distinct pairs: P1 (lgb, r) = field and size (the same plane as field and
enclosed baryon mass); P2 (lgb, zz) = field and epoch; P3 (lgb, dsys) = field and system depth. Cells 0.4 x 0.4 dex on
a fixed grid, nodes as above (at least 5 points), linear interpolation on the nodes (scipy LinearNDInterpolator),
nearest node outside their hull.

The law's curve: L0 X = X_L(g_bar; a0) = (sqrt(1 + 4 a0/g_bar) - 1)/2 at the footing's a0 (no fit); L1 the same with
one free a0 for every class, fit so the system-weighted median training residual is 0 (unique: Lean `law_mono_a`);
L2 one free a0 per class, fit the same way on each class (a diagnostic of shape and of how far the scales differ: it
is one rule only if L1 passes; it cannot be scored leave-one-class-out).

Conservation readings, on each system's outermost point only (SPARC last radius, KiDS last R, groups R500, X-COP and
CLASH last point, single-point classes their point): CONS0 X_last = C (C = weighted median); CONS1 X_last =
C (dsys)^p (C, p by least absolute deviation, systems weighted equally). No model is behind either.

## Step 3: the test

Split: systems, not points, into halves A and B, stratified by class, seed 20261110 (shuffle each class, first
ceil(n/2) to A). Fit on A, score on B; fit on B, score on A; and leave-one-class-out (fit on every other class, score
the class left out).

Scoring on held-out points: residual d = Y - F. Per system: d_sys = median of its d; e_sys = median of its finite e_Y.
Per class: off = median of d_sys over held-out systems; se = max(1.2533 x 1.4826 MAD(d_sys) / sqrt(n),
sqrt(sum e_sys^2) / n) for n >= 2, e_sys for n = 1. A class passes when |off| <= 0.10 dex AND |off| <= 3 se. (3 sigma,
not 2: with 16 classes and 3 tests a correct rule fails somewhere 89 % of the time at 2 sigma, 12 % at 3 sigma.)
Scatter: class-balanced robust scatter (1.4826 weighted MAD, each class weight 1, each system equal within its class);
plain point scatter reported. Scatter line (splits only): the rule's held-out scatter must not exceed that of the
class-constant reference (each class predicted by its own training median), so a variable that only labels classes
cannot pass. A class with no held-out system in a direction is not scored there.

A candidate PASSES if, in split A->B, split B->A and leave-one-class-out, every class passes, and it holds the scatter
line in both splits. A class FAILS a candidate if it fails in any of the three tests.

## Labels (per footing where a0 enters; free-F rules give the same label on both)

- **ONE RULE ORGANIZES EVERY CLASS**: a candidate covering every class (not (d), not L2) PASSES. Name the variable and
  its held-out scatter.
- **ONE RULE EXCEPT**: none passes, but a candidate covering every class fails in at most 2 classes and holds the
  scatter line in both splits. Name the classes and their offsets.
- **NO RULE AMONG THE CANDIDATES**: otherwise. Name the class that breaks most candidates and by how much.
- **NO VERDICT**: a known answer fails.

The lead table: candidate, held-out scatter, failing classes, worst class and its offset (dex and in se).
Reported, not graded: the KiDS hot-gas bracket run; ATLAS3D at Salpeter; 50 other seeds (fraction passing); L2's
per-class a0 / a0_footing with a bootstrap interval; noisy synthetic answers.

## Known answers (must pass, else NO VERDICT)

- KA1 SHP1: 175 SPARC files, 2700 points, 149 galaxies; SHP1's R1 bin medians (both footings) to 1e-9; B21 Nobins
  mean ratio - 1 and chi^2 (published and hot gas, both footings) to 1e-6 of `shp1.json`.
- KA2 synthetic, noise free (Y replaced by the rule's exact value at each real point; se from the real errors):
  (i) the law at each footing's a0: (a) PASSES and L0 PASSES; (g) does not pass.
  (ii) a constant X = 5: CONS0 PASSES with C within 1 %; (a) PASSES.
  (iii) a depth rule X = A dep^(1/2), A = c / (150 km/s), solved per point with g_obs = g_bar (1 + X) (one root; bracket
  checked): (c) PASSES; (a) does not pass; (g) does not pass.
- KA3 loaders: counts equal the source tables (CLASH 84 points / 20 clusters; RC100 100; groups 20; X-COP 7 with stars;
  TDG 6; Coma rows with a dispersion); the Coma UDGs' own lgbar / lgobs columns agree with the table within 0.10 dex.
- KA4 Lean identities numerically: on law points X g_obs = a0 and g_bar (g + a0) = g^2 to 1e-12.

## MUTATE (separate outputs `dd1_MUTATE.*`; each must change its stated outcome, else disclosed)

- M1 class labels shuffled across systems (seeded): (a)'s worst |class offset| in split A->B moves by >= 0.05 dex.
- M2 g_bar x 2 for every CLASH point: CLASH's offset under (a) in split A->B moves by >= 0.10 dex.
- M3 every error halved: the count of failing (candidate, test, class) triples rises.
- M4 a0 x 2 in L0: SPARC fails L0 in split A->B.

## Lean (`DD1.lean`, with a twin of false statements that must fail to compile)

X_is_mass_ratio; law_curve (X_L and g = g_bar (1 + X_L) solve the law); law_in_gobs (on the law X = a0 / g_obs);
law_scale (X_L depends on g_bar / a0 only); law_mono_a and law_one_a0 (X_L strictly increases with a0, so L1 / L2 have
one root). A draft of these was compiled in a scratch folder before this file (algebra only, no data).

## Step 4

For each rule that passes or nearly passes: what it would require of any theory, in plain words; which closed routes
of the record it is compatible with; one measurement that separates it from the next best rule. No theory claim beyond
that, and none of the standard picture's vocabulary or recipes.

## Disclosures (seen before this file)

- From the record: SHP1, RB1, RB2, CLOSURE.md and EQUATIONS.md as written (SPARC on the law within 0.06 dex; KiDS 1.40
  / 1.28 x the law; X-COP +0.47 / +0.43 dex short under the law; groups' retention near 0.6; MW ultra-faints +0.63 dex
  and bright M31 +0.27 above form B, DF2 / DF4 0.7-1.0 dex below; Coma UDGs +0.33).
- Structure only, no DD1 number: X-COP files hold 50 gas radii (0.02-2.1 R500) and 100 hydro radii; B21 Massbin-1
  rows (its innermost ESD is negative); a read-only survey of `real_research/data/` and `_external_data/` (columns and
  counts only).
- Hand estimates (before any DD1 number): (a) and L0 hold SPARC and the rotators but fail clusters (X-COP, CLASH, by
  0.3-0.5 dex), groups (0.2 dex) and the MW ultra-faints (0.5 dex), with DF2 / DF4 low; KiDS fails (a) only when left
  out (0.1-0.15 dex). (b) behaves like (a). (c), (e), (f) fail SPARC's own structure. (g) fails. Two-variable rules pass
  the splits more often but fail leave-one-class-out where a class sits alone in its plane. CONS0 and CONS1 fail.
  Expected label: NO RULE AMONG THE CANDIDATES, clusters and ultra-faints breaking most candidates.

## Operational

One thread, small memory, minutes. `dd1_table.py` -> `dd1_table.csv` / `dd1_table.out`; `dd1.py` -> `dd1.json` /
`dd1.out`; `dd1.py --mutate` -> `dd1_MUTATE.json` / `dd1_MUTATE.out`. Lean via `lake env lean` in the record's build;
`compile.txt` with no home paths. Commit with explicit paths; push by a temporary sparse worktree.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
