# CFG943: Gaia DR4 wide-binary scoring readiness (inventory, hashes, rule reconciliation, MOCK dry run)

Block CFG940-949. Criteria `FROZEN_CRITERIA.md` (47afa80c7), committed alone before any script or mock. Readiness lane: no new
physics, no download, no archive query. Nothing in `prep_2026/gaia_dr4_prep/`, CFG740, CFG800, the CFG825 directory
(`CFG816_dr4_r_statistic_scoring/`) or any sealed file was edited; frozen code was imported read-only and CFG825's once-only `--dr4`
slot was never touched (checked by sha256 before and after every run). kappa = 1/2 is FITTED; the footings are never pooled. Not
theory closed. **Every mock number below is a MOCK, not a measurement.** Nothing here says the data favour the framework.

## Verdict

**READY (code paths), with a POWER GAP against a MOND-size boost and open owner items.**
- Hashes: all 22 `AMENDMENT*_HASH.txt` digests match committed versions of `PREREGISTRATION_DR4.md`; the working tree equals
  Amendment 22's "after" digest; no hash file was ever edited. **0 unexplained mismatches.** One DOCUMENTED DRIFT, reported here
  prominently: the freeze-manifest row for `wide_binary_pipeline.py` (669fecc4..., 2026-07-16) no longer matches the file
  (7c884e0e..., 8 retarget commits recorded in Amendments 10(g), 11(h) and the 2026-09-22 Amendment-12 catch-up). The operative hash
  7c884e0e is pinned by RELEASE_DAY_CHECKLIST section 3 and `edge_table_dr4.json`, and it matches.
- MOCK classes A0 (Newton), A1 (Newton with catalogue cuts 4 and 15) and C (the CFG740 envelope at L* = 5.754 pc) score **framework
  consistent** in 100/100 repeats (R label UNDECIDED, never KILLED; prereg gamma-hat in Arm C's consistent row). Arm A is falsified in
  100/100 Newtonian repeats, as the prereg says it must be.
- **A MOND-size boost does NOT reliably trigger a kill at the plan's sample size** (POWER GAP in all three MOND-size classes:
  44%, 2% and 59% of repeats). Details and reasons in section 4; this is a property of the frozen rules, not a code fault.
- MUTATE bites (a planted x1.2 step at N_cat = 300,000 gives R = 1.204 and KILLED in 20/20); the release-day chain ran end to end on mock CSVs (classes A0, B1, B3, C: frozen pipeline exit 0 with its self-test PASS, both footings fitted, `amdt14_distances.py` and `arm_c_rows.py` exit 0, CFG825's CSV reader and scorer run; K2 exact to 4e-16).

## 1. Inventory: the frozen DR4 plan

**Documents in force.** `PREREGISTRATION_DR4.md` (frozen 2026-07-16) plus **22 filed amendments**, every one with a hash file
(`AMENDMENT1..22_HASH.txt`) and its text inline in the prereg. The `AMENDMENT{9,12,15,16,17,18,19,20,21,22}_DRAFT_NOT_FILED.md`
files are retained pre-filing drafts and are **not** part of the plan. Note on the brief: amendments 12, 15 and 16 themselves **are
filed** (hash files 779e76934, 9f60163d3, 304affce5); only their draft files are non-operative. Where draft and filed text differ
(Amendment 15's cut-9 clause, corrected by 16), the filed text governs.

**Two scored statistics (never pooled, Amendment 7(c), 22(c)(4)).**
1. **gamma-hat** (prereg section 1.3): median v-tilde in 8 bins of log10 y_proj (edges -1.5 ... 2.2), bins < 80 pairs dropped, cap
   v-tilde < 6, 200-resample bootstrap; Newtonian Kepler forward model (3,000,000-pair master, thermal e, DR4 noise x0.372 / x0.718, 5%
   mass scatter); 1-parameter fit of gamma_inf on GRID 0.90-1.50 step 0.0025 with the EFE-saturated shape; kappa anchored on log y >= 0.5,
   window [0.95, 1.05]. sigma_tot = sqrt(sigma_fit^2 + 0.02^2), sigma_fit = 0.019 sqrt(30000/N) at the frozen N = 30,000. z-rule:
   consistent |z| < 2, disfavoured |z| > 3. Rows: Arm A band 1.1614-1.1814 / 1.1917-1.2267 (falsified > 3 sigma_tot below its floor);
   Arm B 1.0000, not testable, killed from above at 1.084; **Arm C and the settling model (Amendment 21): gamma = 1.000, falsified at
   z_C >= 3 (1.084 at sigma_tot 0.028) only if the stability requirements pass** (every ladder rung within 1 sigma_fit, kappa in window,
   the NSS-off probe moving gamma-hat toward the verdict); the chain ceiling 1.0725 / 1.0900 (Amendment 14); **> 1.23 = guard zone, no
   verdict for any arm.** Reporting: raw gamma-hat, sigma_fit and distances, never a verdict word (Amendment 7(e)).
2. **R** (CFG800 rule, made executable by Amendment 22 and CFG825 `FROZEN_CRITERIA.md` d9eed26eb): R = median v-tilde (x = r_sky/r_M > 1,
   s <= 50 kAU, r_M at a0 = 1.2e-10) / median v-tilde (x < 0.3), Cookson checklist primary (d < 130 pc, parallax <= 2.5%, RUWE < 1.25,
   ipd = 0, dRV < 10, v-tilde <= 2.5, sigma(v-tilde) < 0.1). sigma_R = max(sigma_tot(N_R), bootstrap), **N_R = pairs entering R**.
   KILLED (= CFG740's stiffness construction only) needs R - 1 >= 0.01 and >= 3 sigma_R; CONSISTENT needs 2 sigma_R <= 0.01
   (unreachable: sigma_R >= 0.02); else UNDECIDED; a KILLED that fails the NSS-screened branch or the f_tail test is relabelled
   CONTAMINATION-LIMITED.

**Cuts.** The 16-row table of prereg section 1.2 (|b| > 15; G < 17; d < 250 pc; parallax S/N >= 40; parallax consistency; 2 < s < 30 kAU;
RUWE < 1.4; ipd_frac_multi_peak <= 2; A_V < 0.5; 0.464 < M_tot < 4.31; RV screen; NSS screen; resolved-triple search G < 20 within 30 kAU;
R_chance < 0.01; sigma(v-tilde) <= 0.1 max(1, v-tilde/2); no catalogue v-tilde cap), mapped onto DR4 tables by Amendment 15, cut 9 =
SFD98 primary / `ap_*` variant and cut 13 = literal 5-sigma over `all_source_astrometry` primary / orbit-aware variant (Amendment 16),
cut 12 = union over the counted `nss_*` tables with the own-pair linear exemption, variants V17a/V17b (Amendment 17). Strictness ladder:
RUWE 1.2; R_chance 0.001; 3-20 kAU; RV-screened only; NSS off. Amendment 18: build-seed sweep and a "seed-sensitive" label;
Amendment 19: sync fallback for stage G's correlation fetch; Amendment 20: the anisotropy split only when no orientation fit sits on
a grid edge.

**Code.** `wide_binary_pipeline.py` (7c884e0e; estimator, error model, `FROZEN_DR4_CUTS`, `[7(e)]` report); `catalog_builder/`
(`fetch_extract.py`, `build_catalog.py` 46452daf); `dr4_ready_1/` (driver `dry_run_driver.py`, `dr4_archive_fetch.py`,
`q1_cones_dr4.py`, `cut12_nss_union.py`, `cut13_allsource.py`, `cones_cut13.py`, `join_columns.py`, `seed_sweep.py`, `seed_label.py`,
`edge_table_dr4.json`, `amdt14_distances.py`, `arm_c_rows.py`, `manifest_template_dr4.json`); CFG825 (`cfg816_r.py`,
`make_pair_table.py`, `build_variant_catalogue.py`); `real_research/reviews/mi_dr4_readiness_audit_2026.py`.

**Missing or not testable before release** (from the record, confirmed here): every DR4 query form and table/column name; the real
`nss_*` union; the curated-base vs all-source comparison (variant 15(c)); `ap_*` extinction (never read by any code); the ladder rungs
"RV-screened only" and "NSS off" (NOT IMPLEMENTED by design in the sweep tooling); a statistic for CFG740's falsifiers beyond about
37 kAU and for its log-slope; the owner's decision on the R input catalogue (registered vs `build_variant_catalogue.py`); a
registered Gaia archive account.

## 2. Hash verification (`cfg943_hashes.py`, exit 0)
Every digest in all 22 hash files matches the sha256 of the prereg at a commit (A1 1a018751e ... A22 a553a4a66); each "before" digest
equals the previous "after"; Amendment 4's stamp is honestly recorded as NOT RECORDED (the two intermediate 07-31 versions carry no
digest, as A4 itself states). Each hash file has exactly one commit. The prereg directory is clean. Freeze manifest: 4 of 5 files match;
the pipeline row is the documented drift above. Checklist section 3 (4 files), the edge table, the CFG740 seal 5336fd99, CFG825's
criteria 558e03f0, CFG800's criteria (unchanged since aa71ca510) and THEORY_CANONICAL_2026-10-14 all match.

## 3. Rule reconciliation

| pair of rules | class | why |
|---|---|---|
| CFG740 falsifier "gamma_v >= 1.01 at s <= 50 kAU" vs THEORY_CANONICAL 10-14 section 2 (prediction <= 8.9e-4 at 50 kAU; kill "a MOND-size boost") | CONSISTENT (nested) | same envelope; the prose kill set (MOND, ~15-20%) lies inside CFG740's (>= 1%) |
| CFG800 (R - 1 >= 0.01 at 3 sigma) vs Amendment 22 + CFG825 | CONSISTENT (the same rule, made executable) | A22 supplies the sigma CFG800 lacked and narrows "FRAMEWORK" to CFG740; with sigma_R >= 0.02 the 0.01 thresholds are inert and CONSISTENT can never be issued |
| CFG740 falsifier vs the operative R rule | CONSISTENT (nested), with a large gap and blind spots | every R kill has R - 1 >= 3 sigma_R >= 0.06 > 0.01, so no outcome is killed by the rule and survived by the falsifier. But at the plan's N the rule needs R >~ 1.22 (MOCK), so 1.01-1.22 reads UNDECIDED where CFG740's prose says killed; a separation-independent boost cancels in R; falsifier 1 beyond ~37 kAU and falsifier 2 (slope) have no registered statistic. The record already says the quantitative rule governs (corrections note C8); its sentence that the rule is "much stricter than the prose" is no longer true after Amendment 22 |
| **THEORY_CANONICAL kill line "a MOND-size wide-binary boost" vs the governing rules at the plan's N** | **CONFLICT** | MOCK MOND-size skies are not killed in 56%, 98% and 41% of repeats (classes B1, B2, B3; criterion: > 5%) |
| R rule (CFG740) vs prereg gamma-hat rows (Arm C / settling) | CONSISTENT (different models, never pooled) | split outcomes occur: B3 falsifies Arm C / settling on gamma-hat (row reached 100%) while R stays UNDECIDED (100%) |
| prereg guard zone (> 1.23, no verdict) vs any "MOND kills" reading | CONFLICT in effect | the registered MOND benchmark 1.33 lands in the guard zone in 100% of repeats, so gamma-hat kills nothing for a no-EFE MOND sky |

The 8.9e-4 bound is a prediction (the envelope at L* = 5.754 pc), not a kill threshold. CFG820's L* >= 24 pc (conditional) makes the
envelope >= 17x smaller (about 5e-5 at 50 kAU) and changes no rule. CFG832 put the Saturn-gate edge at 5.650 pc, 1.8% below the sealed
5.754 pc (envelope 3.7% higher there); moot under CFG820 and not a scoring issue.

## 4. MOCK dry run (`cfg943_mock_dryrun.py`; N_cat = 30,000 = the prereg's frozen N; K = 100 per class)

Generator: an exact replica of the frozen `make_population` (K1: byte-identical on all 10 returned fields; K1b: the class-boost path
equals the frozen `vtilde_of`). gamma-hat: frozen `bin_medians` / `fit_gamma` / GRID against a frozen-function master of 3,000,000
pairs (1,430,504 after selection). R: CFG825's own `score()`. Rows: the release-day tools' own `arm_c_rows.report` and
`amdt14_distances.report`.

| class (MOCK) | R mean (sigma_R; N_R) | R labels | gamma-hat canonical (sigma_fit; kappa in window) | Arm C row | kill, any route | verdict |
|---|---|---|---|---|---|---|
| A0 Newton | 1.0035 (0.0746; 2,095) | UNDECIDED 100% | 1.0037 +- 0.0168 (0.0141; 100%) | consistent 100%; Arm A falsified 100% | 0% | **PASS** |
| A1 Newton + cuts 4, 15 | 1.0036 (0.0742; 2,122) | UNDECIDED 100% | 1.0018 (0.0143; 100%) | consistent 100% | 0% | **PASS**; shift vs A0 -0.0019 (bound 0.0070) |
| B1 MOND benchmark 1.33 | 1.2229 (0.0746; 2,097) | KILLED 44% | 1.3362 (0.0193; 100%) | **guard zone 100%** (no verdict) | **44%** | **POWER GAP** |
| B2 MOND step x1.15 at x > 1 | 1.1499 (0.0745; 2,102) | KILLED 2% | 1.2375 (0.0181; **23%**) | falsification row 44% (0% with stability), guard 56% | **2%** | **POWER GAP** |
| B3 Arm A floor 1.1614 (AQUAL-EFE) | 1.1134 (0.0746; 2,095) | UNDECIDED 100% | 1.1650 (0.0167; 100%) | falsification row 100% (**59%** with stability) | **59%** | **POWER GAP** |
| C CFG740 envelope, L* = 5.754 pc | 1.0035 (0.0745; 2,106) | UNDECIDED 100% | 1.0062 (0.0141; 100%) | consistent 100% | 0% | **PASS** |
| D falsifier edge x1.01 at x > 1 | 1.0208 (0.0748; 2,087) | UNDECIDED 100% | 1.0224 (0.0146; 100%) | consistent 96% | 0% | information |

(alt footing within 0.007 of canonical in every class; R footing branches within 0.005 of the primary.)

**Why a MOND-size sky escapes (all three mechanisms are frozen rules, not code faults):**
1. **R sample size.** At the prereg's catalogue N = 30,000 only about 2,100 pairs enter R (the d < 130 pc checklist; the DR3 ratio
   348/6,210 would give about 1,700). With Amendment 22's sigma_R = sigma_tot(N_R) = 0.075, KILLED needs **R >= 1.224**, above the
   registered MOND range 1.15-1.20. R power scan below: a MOND-size R is killed reliably only from N_cat ~ 1e5 (N_R ~ 7,000), about 3x the prereg's assumed DR4 N.
2. **Guard zone.** gamma-hat > 1.23 is "no verdict" for every arm; the no-EFE MOND benchmark lands there every time.
3. **Stability requirements.** The 3-20 kAU ladder rung moves gamma-hat by more than 1 sigma_fit in about 40% of repeats **even under a
   correct model** (Newton: mean shift +0.005, SD 0.016 against sigma_fit 0.014; the subsample's own sigma is 0.021), which alone caps a
   gamma-hat kill at about 60% (B3). A boost whose shape differs from the fit shape (B2) also pushes kappa out of [0.95, 1.05] (77%) and
   fails the rung (97%): "systematic-limited, no verdict". The NSS-off rung is not evaluable on a clean mock and is NOT IMPLEMENTED in
   the sweep tooling.

**R power scan** (`cfg943_scan.out`; K = 100 per cell; R only; MOCK). Kill rate = R label KILLED.

| N_cat (N_R entering R) | sigma_R -> KILLED needs | A0 Newton (R 1.003-1.007) | B1 (R 1.22) | B2 (R 1.15) | B3 (R 1.11) |
|---|---|---|---|---|---|
| 30,000 (2,100) | 0.0746 -> R >= 1.224 | 0% | 47% | 6% | 1% |
| 100,000 (7,000) | 0.0441 -> R >= 1.132 | 0% | 100% | 90% | 23% |
| 300,000 (21,000) | 0.0303 -> R >= 1.091 | 0% | 100% | 100% | 98% |

Also on R, at the plan's N a perfectly Newtonian sky cannot exclude standard MOND at 3 sigma_R (Amendment 22(c)(5)): z = -1.96 to
R = 1.15 and -2.63 to R = 1.20 (A0); that needs N_cat ~ 1e5. On gamma-hat, the no-EFE MOND benchmark 1.33 sits 11.6 sigma_tot (at 0.028) from a
Newtonian 1.004, but that region is the guard zone. The Newtonian mock carries a small positive R bias, +0.003 to +0.007 (measurement noise inflates the outer, wider
pairs more), far below any threshold.

**MUTATE** (`cfg943_mock_dryrun_MUTATE.out`, separate outputs): a planted x1.2 step at x > 1 at N_cat = 300,000 (N_R = 20,962) gives
R = 1.2040 and the label KILLED in 20 of 20 repeats: the kill path works on mocks, so the dry run is DIAGNOSTIC.

**A1 (data/model selection asymmetry).** Applying cuts 4 and 15 to the mock catalogue (which the frozen forward model does not do)
shifts gamma-hat by -0.0019 / -0.0022 (canonical / alt), under the 0.5 sigma_fit bound, and R by +0.00003: PASS. Limitation: the
mock's sigma(v-tilde) is leading order (PM noise, parallax, 5.5% mass); the builder's Monte Carlo also carries a line-of-sight /
perspective term that the frozen population model cannot represent (no systemic proper motion), so the real asymmetry is untested.

**End-to-end release-day chain on MOCK CSVs** (`cfg943_e2e.py`; one 30,000-pair catalogue per class; logs `e2e_<class>_pipeline.log`,
blocks `e2e_<class>.out`; the full pipeline logs are git-ignored by the repo's `*.log` rule and stay local, the `.out` files carry their
`[7(e)]`, `[gated]`, `[aniso]` lines and every tool's output). For each class: K2 PASS (the frozen `ingest_csv` v-tilde equals the in-memory one to 4e-16); the frozen
pipeline (through `cfg943_frozen_harness.py`, memory-only patches) exits 0 with **PIPELINE SELF-TEST: PASS** and prints its `[7(e)]`,
`[gated]` and `[aniso]` lines (`[aniso]` declines loudly: a mock carries no sky positions, so Amendment 20's path is not exercised here;
it was on DR3, 2026-10-03/09); `amdt14_distances.py` and `arm_c_rows.py` exit 0 on the log; CFG825's `read_table` + `score` (B = 2000)
read the pair CSV (blank dRV handled) and print the full block. Harness peak RSS 708-771 MB.

| class (MOCK, one catalogue) | gamma-hat canonical / alt (sigma_fit) | Arm C row (z_C canonical) | A14 interval canonical | R (sigma_R; N_R) | R label |
|---|---|---|---|---|---|
| A0 Newton | 1.0125 / 1.0075 (0.0125) | consistent (+0.53) | <= 1.0725 | 0.9968 (0.0757; 2,032) | UNDECIDED |
| B1 MOND benchmark | 1.3350 / 1.3225 (0.0187) | guard zone > 1.23 (+12.2) | > 1.23 | 1.2220 (0.0744; 2,109) | UNDECIDED |
| B3 Arm A floor | 1.1725 / 1.1650 (0.0162) | falsification row, if stability passes (+6.70) | >= 1.157 | 1.1248 (0.0759; 2,018) | UNDECIDED |
| C CFG740 envelope | 1.0250 / 1.0250 (0.0150) | consistent (+1.00) | <= 1.0725 | 0.9701 (0.0741; 2,129) | UNDECIDED |

These single catalogues reproduce the ensemble picture: B1 (a full MOND-benchmark sky) gets no kill on either statistic.

**Controls.** K1, K1b PASS; K3 (CFG825's class arithmetic through the import) PASS; K4 (37 frozen files and CFG825's official outputs
unchanged, DR4 slot absent) PASS in every run; K5 peak RSS 702 MB (classes), model build 601 MB, scan and MUTATE workers <= 850 MB; K6 (added) the memory-lean model medians
give grid medians identical to the frozen `model_medians` and bootstrap sigmas within the expected 100-resample scatter (0.74-1.13).

## 5. Release-day command list (proposal; every archive step needs the owner's go; nothing here changes a frozen choice)
0. **Before the archive opens:** `git status --short prep_2026/gaia_dr4_prep` (clean); `python3 -B
   campaign_fresh_gravity/CFG943_dr4_readiness/cfg943_hashes.py` (0 unexplained mismatches; latest "after" digest = prereg);
   `python3 real_research/reviews/mi_dr4_readiness_audit_2026.py`; self-tests: `dry_run_driver.py --self-test`,
   `amdt14_distances.py --self-test`, `arm_c_rows.py --self-test`, `CFG816_dr4_r_statistic_scoring/make_pair_table.py --self-test`,
   `cfg816_r.py` (controls). **Memory:** the unpatched frozen pipeline needs about 2.1 GB for its master plus about 0.7 GB for the
   master bootstrap: run it with >= 4 GB free and no 1024^3 job live (this lane needed `cfg943_frozen_harness.py` to stay under 1 GB).
   Record every owner decision of section 7 before the data are opened.
1. Save the published DR4 data model (URL, time, sha256); fill `dr4_ready_1/manifest_template_dr4.json` (names only; `--spec-json`).
2. Candidates and cones (N = owner go): `dry_run_driver.py --release dr4 --manifest M.json --allow-network --cut13 extract-builder
   --dump-candidates C.csv`; `dr4_q1_estimate.py --pairs-csv C.csv`; `q1_cones_dr4.py --print-count-queries`; `q1_cones_dr4.py --spec
   dr4_all_source ... --plan-only`; then the fetch (N) and, if decided, the optional `gaia_source_environment` / `crowded_field_source` tables.
3. **Primary build:** `dry_run_driver.py --release dr4 --manifest M.json --allow-network --cut13 cones-literal --neighbours F
   --neighbour-pairs C --out-csv wide_binaries_dr4.csv` (**not** the driver's default `--cut13 extract-literal`, which searches only the
   extract and is not Amendment 16(b)'s primary); `--corr-transport sync` only if the async fetch fails, recorded (Amendment 19).
   Variants beside it, never substituted: `--cut13 cones-orbit`; `--variant allsource_15c`; V17a / V17b; the `ap_*` A_V route.
4. **gamma-hat:** `python3 prep_2026/gaia_dr4_prep/wide_binary_pipeline.py --catalog wide_binaries_dr4.csv > pipeline_dr4.log`, then
   `python3 prep_2026/gaia_dr4_prep/dr4_ready_1/amdt14_distances.py --log pipeline_dr4.log` and `... /arm_c_rows.py --log pipeline_dr4.log`.
5. **Ladder and seeds:** `seed_sweep.py --release dr4 --mode g-only --K 50 --fit --ladder`, then `seed_label.py --evaluate <manifest>`
   (note: `seed_sweep.py` accepts only `extract-*` cut-13 modes); the NSS-off rung and the RV-screened rung per the owner's decision.
6. **R (CFG825):** the R input catalogue per the owner's decision (registered `wide_binaries_dr4.csv`, or `build_variant_catalogue.py
   --release dr4 --manifest M.json --allow-network --out V.csv`); `make_pair_table.py --catalogue <csv> --per-star <npz> --out
   pairs_dr4.csv` (add `--declare-neutral non_single_star` if the NSS-screened registered catalogue is used, or the converter refuses);
   then **once**, on the owner's yes: `python3 cfg816_r.py --dr4 pairs_dr4.csv`.
7. **Report:** the `[7(e)]`, `[A14]`, `[A20]`, `[ArmC]` lines, the R block (primary and branches), sigma_build and the seed label. No
   verdict word; the two statistics side by side, never pooled.

**Expected DR4 names** (ESA draft data model 2026-06-26, `manifest_template_dr4.json`; confirm on the day): `gaiadr4.gaia_source`
(source_id, ra, dec, parallax, parallax_error, parallax_over_error, pmra, pmdec, pmra_error, pmdec_error, pmra_pmdec_corr,
parallax_pmra_corr, parallax_pmdec_corr, phot_g_mean_mag, bp_rp, ruwe, ipd_frac_multi_peak, radial_velocity, radial_velocity_error);
`all_source_astrometry`, `all_source_photometry` (cut 13 cones, G); `all_source_flags` (non_single_star); `all_source_rvs`; counted NSS
tables `nss_acceleration_astro`, `nss_multiple_orbits`, `nss_non_linear_spectro`, `nss_resolved_pair` (source_id, source_id_secondary,
solution_type), `nss_two_body_orbit`, `nss_vim_fl`; not counted `nss_masses`, `nss_multiplicity`, `nss_epoch_flags` (DataLink),
`optical_pair`; `ap_xp` (ag_gspphot / ebpminrp_gspphot, A_V variant only); optional `crowded_field_source`, `gaia_source_environment`.
The draft says `astrometric_gof_al` may be preferred to ruwe from DR4 on; the frozen cut reads ruwe.

## 6. Departures and disclosures
- **Memory (1 GB cap).** The frozen 3,000,000-pair master is built by the frozen function in 50,000-pair chunks (criteria said 12 x
  250,000; changed after the RSS guard tripped) and its 100-resample bootstrap is drawn in batches of 2 (K6). Both are memory-only;
  medians are identical. The master and model medians are built in a separate process (`--build-model`, `cfg943_model_medians.npz`).
- **Aborted attempts, no outputs kept** (all stopped below the 1 GB cap by the in-script guard at 900 MB, or by me): classes run 1 tripped
  the guard at 934 MB while building model medians (no class computed); classes run 2 was stopped by me after class A0 (peak 840 MB;
  only its A0 verdict line, PASS, was seen; its master was chunked differently, so its numbers are not the kept run's); scan attempts 1 and 2 completed the four 30k rows (reproduced exactly
  by the kept scan) and tripped the guard at 904 / 900 MB at 100k; MUTATE attempts 1 and 2 tripped it at 947 / 915 MB. Cause: heap
  growth over many repeats in one process. Fix: each block of scan / MUTATE repeats runs in a fresh worker process, one at a time
  (`--scan-worker`), with 50,000-pair generator chunks above N_cat = 30,000; the classes run keeps 250,000-pair chunks (N_cat = 30,000).
- The four local `e2e_<class>_pipeline.log` files had the scratch directory of the mock CSVs replaced by `<scratch>/` after the run
  (one line each, the frozen pipeline's `[catalog]` echo; no number changed); `cfg943_e2e.py` now writes it that way.
- K6 was added (not in the criteria). MUTATE ran K = 20 (the criteria named no K).
- The mock is clean (no triples, no NSS flags, RUWE = 1, no RVs): contamination, the NSS legs and the f_tail leg are not exercised
  (0 pairs with v-tilde > 2 in either regime in every repeat: a bound, noise-light orbit population barely exceeds v-tilde = 1.5).

## 7. NOTE for the owner (dated 2026-10-20): ambiguities that could cause a dispute, with proposed clarification text
Proposals only. Filing any of them is an amendment and needs the owner's go; no frozen file was touched.
**N1. Which N sets sigma_R (dispute risk: high).** CFG825 froze N = the pairs entering R; the CFG800 addendum (2026-10-18) quotes
"expected DR4 sigma_R = 0.0276 at the prereg's frozen N = 30,000" and its 5.4-7.3 sigma_R distances on that basis. At the prereg's
catalogue N = 30,000 only about 1,700 (DR3 ratio) to 2,100 (MOCK) pairs enter R, so sigma_R is 0.075-0.083. *Proposed text:* "For the R
statistic, N in sigma_tot(N) of Amendment 22(c)(1) is the number of pairs entering R (CFG825 section 2), never the gamma-hat catalogue's N.
The CFG800 addendum's sigma_R = 0.0276 is not the operative value."

**N2. The canonical kill line vs the governing rule (CONFLICT, section 3).** *Proposed text:* "THEORY_CANONICAL section 2's DR4 kill
line ('a MOND-size wide-binary boost') is read only through Amendment 22: CFG740 is killed iff R - 1 >= max(0.01, 3 sigma_R). At the
expected DR4 R sample this needs R >~ 1.22. A MOND-size R (1.15-1.20) labelled UNDECIDED is reported as UNDECIDED: it is neither a kill
nor a survival of CFG740." Options the owner may weigh (none chosen here): accept the gap as stated; register, before DR4 and with its
own criteria committed alone, a better-powered statistic; or state which gamma-hat row (Arm C / settling) speaks for the framework.

**N3. The guard zone.** *Proposed text:* "A gamma-hat above 1.23 is 'no verdict' for every arm, Arm C and the settling model included,
whatever R says; it is never read as survival." (The no-EFE MOND benchmark lands there in 100% of MOCK repeats.)

**N4. The stability requirements on boost-side verdicts.** (a) The NSS-off rung is NOT IMPLEMENTED in the sweep tooling, and
`build_variant_catalogue.py` exposes the NSS switch only together with the 50 kAU cap on its command line (`build(drop_nss=True,
smax_kau=30)` exists in code). (b) "Moves gamma-hat toward the verdict value" is undefined when the shift is zero or within noise. (c) The
"within 1 sigma_fit" rule fails for the 3-20 kAU rung in about 40% of MOCK repeats under a correct model. *Proposed text:* "The NSS-off
rung is run as `build(drop_nss=True, smax_kau=30)` [or: is NOT IMPLEMENTED and does not block a verdict]; a shift smaller than 1 sigma_fit
counts as passing the NSS-off condition; the ladder rule is applied as written, and the expected false-failure rate (~40% for the
separation rung, MOCK) is stated beside any 'systematic-limited' outcome."

**N5. The R input catalogue.** The registered stage G is NSS-screened and capped at 30 kAU, so CFG825's NSS-screened branch equals its
primary and the 50 kAU cap is moot; `build_variant_catalogue.py` (declared 2026-10-18, not filed) fixes both. *Proposed text:* "The DR4 R
input is [the registered catalogue | the CFG825 variant catalogue], decided on <date> before the data are opened; with the registered
catalogue `make_pair_table.py` is run with `--declare-neutral non_single_star`."

**N6. What 'the framework' means on DR4 day.** CFG740 is scored by R; the settling model (Amendment 21) and Arm C by gamma-hat; Arm A is
falsified by any Newtonian sky (100% of MOCK repeats). MOCK class B3 gives a split (gamma-hat falsification row 100%, R UNDECIDED 100%).
*Proposed text:* "The DR4 report lists CFG740 (R), the settling model and Arm C (gamma-hat rows) and Arm A separately; a split outcome is
reported as a split and never merged into one framework verdict." Whether the canonical theory's wide-binary prediction includes the
settling model is the owner's call.

**N7. CFG740 falsifiers with no registered statistic.** Falsifier 1 beyond ~37 kAU (the registered stage G stops at 30 kAU, the variant's
chance-alignment screen at ~37 kAU) and falsifier 2 (log-slope 2) are not scoreable by any registered DR4 statistic; a
separation-independent boost is invisible to both (it cancels in R; the anchored kappa absorbs it in gamma-hat, giving
"systematic-limited"). *Proposed text:* "These falsifiers are not scored in the DR4 confrontation; any test of them needs its own criteria
committed alone before use."

**N8. The pipeline hash.** *Proposed text:* "The operative frozen pipeline is `wide_binary_pipeline.py` sha256 7c884e0e... (RELEASE_DAY_CHECKLIST
section 3, edge table); the freeze-manifest row 669fecc4... (2026-07-16) is historical, superseded by the retargets recorded in Amendments
10(g), 11(h) and commit 2a18b570e."

**N9. Tooling defaults.** `dry_run_driver.py` defaults to `--cut13 extract-literal` (extract only), not Amendment 16(b)'s primary
(`cones-literal` over `all_source_astrometry`); `seed_sweep.py` accepts only `extract-*` cut-13 modes, so Amendment 18's sweep cannot use
the primary's cut 13. *Proposed text:* "The primary build is run with `--cut13 cones-literal`; Amendment 18's sweep uses [extract-builder |
a cones option added as new code before release], recorded in the manifest."

**N10. A sentence in the record that no longer holds.** THEORY_CANONICAL_2026-10-14_CORRECTIONS item C8 says the frozen quantitative rule is
"much stricter than the prose". After Amendment 22 it is weaker in kill power at the expected N (it needs R >~ 1.22). A dated correction
note, not an edit, would fix it.

**N11. Memory.** The unpatched frozen pipeline needs about 3 GB peak; run it on release day with that headroom (no 1024^3 job live).

## Files
`FROZEN_CRITERIA.md`; `cfg943_hashes.py` (+ `.out`, `.json`); `cfg943_common.py`; `cfg943_mock_dryrun.py` (+ `cfg943_build_model.out`,
`cfg943_model_medians.npz`, `cfg943_mock_dryrun.out`, `_results.json`, `cfg943_scan.out`, `_results.json`,
`cfg943_mock_dryrun_MUTATE.out`, `_results.json`); `cfg943_frozen_harness.py`; `cfg943_e2e.py` (+ `e2e_<class>.out`,
`cfg943_e2e_results.json`; `e2e_<class>_pipeline.log` local only, git-ignored). Mock CSVs were written to a scratch directory and are not committed (sha256 in
`cfg943_e2e_results.json`).
