# AT2_a0z_on_disk_samples: FROZEN CRITERIA (2026-11-04)

Committed alone, before any script, output or number of this lane exists. κ = ½ is FITTED. Not theory closed. Footings never
pooled. The cold sector stays retired. **Not blind:** every sample below has been read by earlier lanes (CFG140-CFG190,
CFG214-CFG224, CFG385, CFG400-405, CFG475, CFG685, AC1); their results are known to the author of these criteria.

## 0. Question

Grade every high-z kinematic sample already on disk with AT1's decision rule (`rebuild_2026_10_22/AT1_a0z_tracking_decision/`,
criteria 2d68f8e546, results 4c5c84576a), **unchanged**: does a₀(z)/a₀,ref follow the law's √X(z) (a₀ tracks ρ_DE) or the
rival E(z) = H/H₀? ρ_DE(z) and H(z) come only from CFG689's primary quantiles (`cfg689.json` → `BAO+SN.P1`), as in AT1. No
ΛCDM input, no Planck 5.364, no Ω_m = 0.315 E(z). No download.

## 1. AT1 applied unchanged

- z* ∈ {1.0, 1.2, 1.5, 2.33}; gap, σ_E, σ_X, S(e), e_3σ exactly as AT1 §0 (recomputed by the same lines, checked against
  `at1.json`).
- ȳ = log10(a₀(z*)/a₀,ref) against a **same-estimator z < 0.1 reference**; e = √(e_stat² + c²).
- Gates G1 (e ≤ e_3σ), G2 (direct cold-gas tracer for every galaxy), G3 (declared pressure correction ≤ 0.05 dex or sample
  median v/σ ≥ 6), G4 (g_bar ≤ 0.5 a₀,ref at the radius used, every galaxy), all before ȳ.
- Outcomes and order as AT1 §3 (TRACKING FAVOURED, RIVAL FAVOURED, NEITHER, INCONCLUSIVE).
- **ȳ is computed only for a (sample, bin) cell that passes the reference match and G1-G4.** A cell that fails any of them
  gets no ȳ: no a₀ ratio is formed and no a₀-like column (e.g. RC100's `a0_Vc4_over_GMbar_ms2`) is read.

**Labels reported here** (mapping to AT1): DECIDES-law = TRACKING FAVOURED; DECIDES-rival = RIVAL FAVOURED; NEITHER = AT1
NEITHER (counts against the law at that z*, AT1 §3); INCONCLUSIVE = AT1 INCONCLUSIVE; **BLOCKED** = no same-estimator reference,
or G1 fails on the common mode (AT1's NOT POWERED), or G2/G3/G4 fails. Every failing reason is listed, not only the first.
Two non-grades: **OUT OF DOMAIN** (no galaxy in any z* bin) and **ONE DISC** (CFG806/CFG809 §4 rule; AT1 does not apply).

**Bins (AT1 names the z* nodes but no width; fixed here, before any count):** z* 1.0: 0.90 ≤ z < 1.10; z* 1.2: 1.10 ≤ z <
1.35; z* 1.5: 1.35 ≤ z < 1.915; z* 2.33: 1.915 ≤ z ≤ 2.75. Each galaxy is compared with the quantiles at its bin's z* (the
within-bin change of √X and E is not modelled; disclosed).

**Pooling:** AT1 defines outcomes per z* bin for one sample and states no pooling rule. Adding one would change AT1, so
**nothing is pooled**: not across bins, not across samples, never across footings.

## 2. Reference match (before any ratio)

A z < 0.1 reference qualifies for a sample only if all hold:
- **R1** it is a per-galaxy table on disk with z < 0.1;
- **R2** same kinematic tracer phase (ionised Hα/[OII] / molecular CO-[CI] / [CII] / HI) and the same velocity definition
  (same radius in units of R_e or R_d, or the same V_flat / V_max / V₂.₂ definition);
- **R3** same baryon recipe: stellar mass by the same method class, and gas by the same route (measured tracer X on both sides);
  a side with no gas at all fails R3, because the a₀ estimator cannot be formed;
- **R4** same pressure-support recipe (or both v/σ ≥ 6);
- **R5** the source states the low-z and high-z measurements were made with the same method (same paper, or explicitly
  matched, e.g. resolution-matched).

A sample with no qualifying reference is **BLOCKED (no reference)**. No substitute is used. In particular a footing value
(9.36e-11 or 1.13e-10) is never a₀,ref (AT1 §1), and SPARC is not KURVS's reference (CFG140's "same-pipeline anchor" fails R2,
R3, R4 and R5: HI vs Hα, measured HI gas vs none, no pressure term vs a large one).

Candidates checked (verdicts fixed here from metadata, the script re-checks R1 by counting z < 0.1 rows):
- Tiley+2019 `SAMI_matched` (Hα, V₂.₂, resolution-matched to KROSS): R1, R2, R5 pass; **R3 fails** (no gas on either side).
- Girard+2021 DYNAMO rows (CO + Hα, z 0.067-0.079 below 0.1): R1 pass; **R5 fails** (the z > 0.9 rows are a compilation from
  other papers, instruments and pipelines); R2 fails for the radius definition.
- SPARC, Di Teodoro+2023, LITTLE THINGS, ALFALFA, WALLABY (HI); DiskMass (PPak IFU + HI gas); SAMI DR3 `stelkin` (stellar
  kinematics only); ATLAS3D (early types): R2 fails against every high-z gas-kinematic sample; R5 fails for all.

## 3. Common mode c (fixed here, before any ratio)

Terms as CFG685: IMF / stellar M/L evolution, gas conversion (α_CO, [CII], dust, scaling relations), pressure support, times
the lever (1 in deep MOND, 2.5-4.8 at g_bar/a₀ = 1-4). With no same-estimator reference none of it cancels, so:
- **c_primary** = CFG685's `e_est` lower edge for the sample or its class row (CFG685 README table). **G1 uses c_primary.**
- **c_optimistic** = the lowest sample-specific number elsewhere in the record (CFG218 systematic column, CFG689 §8), reported
  beside; if none exists, c_optimistic = c_primary. It is reported only; if c_optimistic < e_3σ ≤ c_primary the cell reads
  "BLOCKED on c_primary; c_optimistic would open G1".

## 4. The registry (in-domain candidates; N and z ranges are counted by the script from the files)

| # | sample | file (repo) | tracer / estimator | gas route (G2) | c_primary (src) | c_optimistic (src) | G4 from the record |
|---|---|---|---|---|---|---|---|
| 1 | KURVS-CDFS rotation-supported | `data_assembly/arxiv_tables/kurvs2023_*` (10 f_DM rows) | Hα KMOS, V at R'_3D/R'_6D (authors' model at R_max) | none | 0.45 (CFG685 #1) | 0.45 | g_bar/a₀ 0.06-0.67 (CFG140): not all ≤ 0.5, FAIL |
| 2 | Genzel+2017 six deep curves | CFG401 `T1` (z), CFG400 points | Hα SINS/KMOS curves | scaling (CFG401 f_gas) | 0.45 (#3) | 0.45 | outer g ~1-3 a₀ (CFG400), FAIL |
| 3 | RC41 (Price+2021) | `data_assembly/price2021_rc41/price2021_rc41.csv` | Hα 1D/2D fits at R_e | scaling `logMgas` | 0.45 (#3) | 0.45 | at R_e, near-Newtonian (CFG685), FAIL |
| 4 | KMOS3D TF (Übler+2017) | `data_assembly/high_z_tf_tables/ubler2017.csv` | Hα, max modelled V_c | scaling (M_bar) | 0.45 (#3) | 0.45 | massive, near-Newtonian (CFG685), FAIL |
| 5 | KMOS3D raw-cube fits z ≥ 1.9 | `data_assembly/kmos3d_cubes/k3d_fits_main_final.csv` (status ok) | Hα, own 3D fits | none | 0.50 (#7-11) | 0.50 | strong-inner or weak-outer, never both (CFG386), FAIL |
| 6 | SINS/zC-SINF AO | `data_assembly/highz_literature_tables/sins_ao/` | Hα AO, V_rot | none | 0.50 (#7-11) | 0.50 | one radius (CFG386), FAIL |
| 7 | SINS 2009 | `data_assembly/high_z_tf_tables/sins2009_dynamics.csv` | Hα, mixed methods | SFR inversion | 0.45 (#3) | 0.45 | not shown, FAIL |
| 8 | RC100 (CORRECTED) | `real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv` | V_c(R_e), author decompositions | mixed, K 0.13 | 0.40 (#4) | 0.10 (CFG218 calibration) | lever 2.5-4.8 at R_e (CFG685), FAIL |
| 9 | MSA-3D | `data_assembly/arxiv_tables/msa3d_galaxies.csv` (+ `real_research/data/msa3d_2026_rotation_curves.csv` for v/σ) | NIRSpec ionised, V at R_e | depletion-time scaling | 0.60 (#5) | 0.60 | ~2 R_e, lever ~2.5 (CFG685), FAIL |
| 10 | NOEMA3D | `data_assembly/noema3d/noema3d_per_galaxy.csv` | CO, V_c at R_e,disk | CO (+ dust) | 0.40 (#2) | 0.043 (CFG218 route-bias systematic) | lever 2.5-4 at R_e (CFG685), FAIL |
| 11 | ALPAKA I | `data_assembly/arxiv_tables/alpaka1_*` (19 kinematic discs) | CO/[CI] 3D rings, V_ext | CO/[CI] L′ | 0.50 (#7-11) | 0.50 | R_ext not tabulated: not shown, FAIL |
| 12 | ALPAKA-JWST | `data_assembly/arxiv_tables/alpaka_jwst2026_data.csv` | CO/[CI] + NIRCam | CO/[CI] | 0.50 (#7-11) | 0.50 | not shown, FAIL |
| 13 | Lelli+2023 | `data_assembly/arxiv_tables/lelli2023_massmodels.csv` | CO curves | CO | 0.50 (#7-11) | 0.50 | V²/R > 3-4 a₀ (paper), FAIL |
| 14 | Amvrosiadis+2025 | `data_assembly/arxiv_tables/amvrosiadis_{parent,bestfit}.csv` (12 fits) | CO, V_c at 2 r_e | CO | 0.50 (#7-11 class) | 0.50 | ~10 a₀ (data README), FAIL |
| 15 | PHIBSS (Tacconi+2013) | `data_assembly/kmos3d_phibss/phibss13_joined.csv` | CO V_rot | CO | 0.50 (#7-11 class) | 0.50 | massive, near-Newtonian, FAIL |
| 16 | Girard+2021 compilation | `data_assembly/highz_literature_tables/girard2021/` (z ≥ 0.9 rows) | mixed Hα / CO | mixed | 0.50 (#7-11 class) | 0.50 | not shown, FAIL |
| 17 | KROSS (Harrison+2017 v2; Tiley+2019) | `data_assembly/high_z_tf_tables/kross_v2.csv` (z), `tiley2019.csv` | Hα, V₂.₂ / V_C at 2 R_½ | none | 0.45 (#3 class) | 0.45 | no g_bar without gas, FAIL |
| 18 | KROSS GS21b (Sharma+2024) | `data_assembly/arxiv_tables/sharma2024_gs21b.csv` | Hα, V at R_out ~5 R_D | scaling (Tacconi+18 H₂, stacked HI) | 0.45 (#3 class) | 0.45 | g_bar set by assumed gas, FAIL |
| 19 | Mancera Piña+2026 | `data_assembly/arxiv_tables/manceraPina2026_sample.csv` | Hα, flat V_circ | none | 0.45 (#3 class) | 0.45 | not shown, FAIL |
| 20 | ZFIRE 2018 | `data_assembly/highz_literature_tables/zfire2018/zfire_table3_kinematics.csv` | MOSFIRE slit V₂.₂ | none | 0.45 (#3 class) | 0.45 | not shown, FAIL |
| 21 | SIGMA (Simons+2016) | `data_assembly/high_z_tf_tables/simons2016_sigma.csv` | MOSFIRE slit V_rot | none | 0.45 (#3 class) | 0.45 | not shown, FAIL |
| 22 | MUSE-DARK | `data_assembly/musedark_catalogues/musedark_numeric.csv` | MUSE [OII] | modelled surface density | 0.30 (CFG218 systematic; CFG685 did not score it) | 0.30 | not shown, FAIL |

Reference candidate per sample: #17 → Tiley+2019 SAMI_matched (fails R3); #10, #16 → Girard DYNAMO rows (fail R5); #1 → SPARC
anchor (fails R2-R5); all others → none on disk.

G3 is computed per bin from a v/σ column where the table has one (median v/σ ≥ 6 passes; no sample declares a pressure
correction ≤ 0.05 dex); where no column exists G3 reads "not shown" = FAIL.

**ONE DISC (not graded, AT1 does not apply):** CFG970 Refsdal host (z 1.489; that lane is INVALID as frozen), Übler+2018 (one
disc), GS4_24110 (not on disk; public 2026-11-28), U4_27928 / U4_28473 (ALMA release 2026-11-06; not on disk), Big Wheel
(z 3.245, not in a file).

**OUT OF DOMAIN candidates (the script confirms 0 rows in any bin):** ALMA-CRISTAL (z 4.4-5.7), Roman-Oliveira+2023 (4.3-4.4),
Danhaive+2025 (3.8-5.8), ALPINE (Jones+2021; corpus_z1), MIGHTEE-HI z > 0.25 (0.25-0.5), BUDHIES (~0.2), PHIBSS2 (0.5-0.8).

## 5. Footings

The ratio cancels κ and the footing (AT1 §1). Both footings are reported: K6 builds a₀,ref and a₀(z*) from each footing value
and shows ȳ and the label are identical to 1e-12. The footing values appear only in K6 and are never passed to the grader.

## 6. Checks (a failed check means no clean label; a fail is graded as hard as a pass)

- **K1 known answer:** gap, σ_E, σ_X and e_3σ at the four z* equal `at1.json` to 1e-12 and CFG689's `e_3sigma` within one grid
  step (0.001 dex); the expected values are 0.0546 / 0.0724 / 0.0744 / 0.0843 dex.
- **K2 planted recovery** (seeded, 2000 draws per case; per-galaxy scatter s = 0.14 dex, AT1/CFG685's per-galaxy budget, the
  generous end; truth law = log10 √X₅₀(z*), rival = log10 E₅₀(z*); reference error zero):
  - K2a (must pass) powered control, N = 1000, c = 0: law → DECIDES-law and rival → DECIDES-rival in ≥ 95 % of draws in every
    bin.
  - K2b (must pass) at every in-domain (sample, bin) cell's own N and c_primary: the gate blocks 100 % of draws for both truths
    (no label is emitted).
  - K2c (reported, no pass/fail) at each cell's own N with c = 0, and K2d at c_optimistic with the gate ignored: recovery
    fractions, to show whether N or c is binding.
- **K3 MUTATE twin** (`MUTATE=1`, separate `_MUTATE` outputs): the law and rival quantile sets are swapped. It must bite: K2a
  fails (law mocks read DECIDES-rival) and the script exits non-zero. Gate labels do not depend on the swap; reported.
- **K4 byte-identical rerun:** the script reruns itself in a subprocess to a scratch directory; `.out` and `.json` must be
  byte-identical (sha256 printed).
- **K5 scrambled-z control:** in the powered control, each mock's truth is generated at one of the other three bins and scored
  at its own bin. Must hold: rival recovery < 50 % in every bin, and overall recovery (both laws, all bins) drops by ≥ 20
  points. Stated before running: √X₅₀ is nearly flat (0.91-0.94), so law mocks are **not** expected to drop; that is a
  property of the law, not a failure of the control.
- **K6 footings** as §5.
- **K7 inputs:** every registry file exists; RC100 is read only from the `_CORRECTED` file; the script contains no 5.364,
  0.315 or Planck H₀; no footing value reaches the grader.
- **K8 domain:** the OUT OF DOMAIN files have 0 rows in any bin; every registry sample has ≥ 1 row in some bin.

## 7. Expectation (stated before running, from the record)

Every in-domain sample is BLOCKED: none has a qualifying same-estimator z < 0.1 reference on disk, and every c_primary
(0.30-0.60 dex) is above the largest e_3σ (0.084 dex); most also fail G2 and G4. If that holds, no ȳ is computed anywhere and
the lane names the data that would decide (survey, size, source), without fetching anything.

## 8. Wording

README leads with a one-line verdict and a per-sample table. It states whether the record's earlier lean to the rival
(KURVS: CFG160 / CFG189, "a weak, normalisation-dependent lean; not a detection") is confirmed or changed, and the opposite
within-sample reading (RC100 CFG216 W-flat). Not blind; κ = ½ FITTED; footings never pooled; not theory closed; nothing here
says the data favour the framework unless the frozen rule says DECIDES-law, and then only "this sample, this rule"; the cold
sector stays retired.
