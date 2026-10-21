# CFG943 FROZEN CRITERIA: Gaia DR4 wide-binary scoring readiness (inventory, hash check, rule reconciliation, MOCK dry run)

**Status.** Committed alone, before any CFG943 script exists and before any mock catalogue is generated or scored, 2026-10-20 (block
CFG940-949, reserved in the LEDGER). Readiness lane: no new physics, no download, no archive query. Nothing in
`prep_2026/gaia_dr4_prep/`, `CFG740_sealed_wb_slope2/`, `CFG800_wb_2026_scoring/`, the CFG825 lane directory
(`CFG816_dr4_r_statistic_scoring/`) or any sealed file is edited; frozen code is imported read-only. kappa = 1/2 is FITTED; the two a0
footings (9.36e-11 / 1.13e-10 m s^-2) are never pooled. Not theory closed. Every mock number is labelled MOCK and is never a result.

**Disclosed before freezing.** While reading the record I computed sha256 of `PREREGISTRATION_DR4.md` (working tree and its 23 git
versions), of the 22 `AMENDMENT*_HASH.txt` targets, of the five freeze-manifest files and of the CFG740 seal, and I ran the frozen
`make_population` at N = 1e5 and 3e5 to measure memory only (selection fraction 0.475; peak RSS about 40 MB + 0.69 kB per pair, so the
frozen 3,000,000-pair master needs about 2.1 GB). No mock R, no mock gamma-hat, no class outcome was computed.

## 1. Inventory and hash verification (task 1), script `cfg943_hashes.py`
- H1: every sha256 digest printed in every `AMENDMENT*_HASH.txt` is matched against the sha256 of `PREREGISTRATION_DR4.md` at each git
  commit that touched it; the latest filed amendment's "after" digest must equal the working tree. Each hash file must have exactly one
  commit (never edited). The prereg directory must be clean in `git status`.
- H2: the freeze-manifest table at the top of the prereg (five files) against the files today; the RELEASE_DAY_CHECKLIST section 3
  reference hashes (four files); `dr4_ready_1/edge_table_dr4.json` pipeline_sha256; CFG740 `PREDICTIONS_HASH.txt` against
  `cfg740_predictions.json`; CFG825 `FROZEN_CRITERIA.md` against the sha256 its ID notes record; CFG800 `FROZEN_CRITERIA.md` unchanged
  since aa71ca510; `THEORY_CANONICAL_2026-10-14.sha256`.
- H3: each `AMENDMENT*_DRAFT_NOT_FILED.md` is classified: FILED (its amendment header is in the prereg AND a hash file exists; the draft
  file is then a retained, non-operative draft) or DRAFT-ONLY (not part of the frozen plan).
- **Any digest mismatch is reported first, prominently, never repaired.** A mismatch that a filed amendment or a committed record
  explains (for example a documented retarget of the pipeline) is reported as DOCUMENTED DRIFT, still prominently.

## 2. Rule reconciliation (task 2)
Rules compared: (i) CFG740's sealed falsifiers (any boost above 1/2 (s/5.754 pc)^2 at s <= 236 kAU; gamma_v >= 1.01 at s <= 50 kAU; a
log-slope inconsistent with 2); (ii) THEORY_CANONICAL_2026-10-14 section 2 (prediction gamma_v - 1 <= 8.9e-4 at 50 kAU; kill line "a
MOND-size wide-binary boost"); (iii) CFG800 (R - 1 >= 0.01 at >= 3 sigma kills); (iv) Amendment 22 and CFG825 (sigma_R = max(sigma_tot(N),
bootstrap), N = pairs entering R; KILLED needs R - 1 >= 0.01 and >= 3 sigma_R; CONSISTENT needs 2 sigma_R <= 0.01; CONTAMINATION-LIMITED);
(v) the prereg's own gamma-hat rows (Arm C / settling model z_C rule, Arm A rows, the 1.23 guard zone, stability requirements).
Each pair is classed **SAME** (same statistic, sigma and threshold), **CONSISTENT (nested)** (one rule's kill set contains the other's; no
outcome is killed by one and labelled consistent by the other), or **CONFLICT** (an outcome the record does not resolve gets a kill
under one and survival under the other, or a kill line the governing rule cannot deliver at the plan's N). A prose kill line counts as
CONFLICTING with the governing rule if the mock shows a sky of that description NOT killed in more than 5% of repeats at the plan's N.
Conflicts are reported for the owner; nothing frozen is edited to resolve them.

## 3. MOCK dry run (task 3), script `cfg943_mock_dryrun.py`
**Generator.** An exact replica of the frozen `make_population` (same draws in the same order, DR4 noise, thermal e, frozen selection
d < 250 pc, G < 17, 2 < s < 30 kAU) that also returns M1, M2, G1, G2, the true 3D separation and the error terms. Control K1: for the same
seed it reproduces every field the frozen function returns, byte for byte. Catalogue = N_cat pairs drawn as the frozen gate does
(oversample x2.7, random keep). Boost b multiplies the TRUE relative velocity before noise (the frozen `vtilde_of` convention).
Pair-table columns for the R scorer: d_pc = observed distance; plx_err_frac = the larger star's sigma_plx(G)/parallax; ruwe = 1, ipd = 0,
nss = 0, drv blank (a clean sky); vt_err = the converter's P3 leading-order form. Masses: M_obs split by M1/M_tot.

**Classes (both statistics on every repeat):**
| class | sky | boost b |
|---|---|---|
| A0 NEWTON | Newtonian | 1 |
| A1 NEWTON+CUTS | Newtonian, with frozen cut 4 (parallax S/N >= 40 both) and cut 15 (sigma(vt) <= 0.1 max(1, vt/2)) applied at catalogue level, as the builder applies them and the frozen forward model does not | 1 |
| B1 MOND-BENCH | the prereg's registered MOND benchmark | frozen `gamma_of_y(g_true/a0, 1.33, y_extN(a0))`, canonical a0 (the gate's injection) |
| B2 MOND-STEP | CFG800's registered MOND R range, low end | x 1.15 for pairs with x = s/r_M(a0 = 1.2e-10) > 1 |
| B3 ARM-A-FLOOR | the prereg's AQUAL-EFE (MOND-with-EFE) band floor | frozen shape with gamma_inf = 1.1614 |
| C CFG740 | the sealed envelope at the bound | 1 + 1/2 (r_3D / 5.754399 pc)^2 |
| D FALSIFIER-EDGE (information) | CFG740's prose falsifier where R can see it | x 1.01 for x > 1 |

**Sizes and repeats.** N_cat = 30,000 (the prereg's frozen N; the only DR4 size the plan states). K = 100 repeats per class. R scorer:
CFG825's own `statistic`/`score` (imported read-only; never its `--dr4`/`--dr3` paths, never its output files), bootstrap B = 300 in
repeats and B = 2000 in one showcase per class. gamma-hat: the frozen `bin_medians` (boot 200) and `fit_gamma` on the frozen GRID against
a frozen-function master of 3,000,000 pairs built in 12 chunks of 250,000 (statistically identical; RNG stream differs; forced by the
1 GB cap), seed 20261216; both footings. Rows by the release-day tools' own logic (`arm_c_rows.report`, `amdt14_distances.report`).
Stability conditions evaluable on a mock: kappa in [0.95, 1.05] and the separation rung (3-20 kAU refit within 1 sigma_fit); the RUWE,
R_chance, RV and NSS-off rungs are identical on a clean sky and are reported NOT EVALUABLE. R power scan: N_cat = 30,000 / 100,000 /
300,000, classes A0, B1, B2, B3, K = 100, R only.

**Readings per repeat.** R route: the CFG825 primary label (KILLED / CONTAMINATION-LIMITED / CONSISTENT / UNDECIDED); KILLED = CFG740's
construction killed. gamma-hat route: Arm C / settling row (z_C >= 3 with gamma-hat <= 1.23 = falsification row; reported with and
without the evaluable stability conditions), the guard zone (> 1.23, no verdict), Arm A falsified below 1.056, kappa window.

**Pass criteria.**
- A0, A1, C: "framework consistent" = R label not KILLED and not CONTAMINATION-LIMITED, and gamma-hat Arm C row |z_C| < 2, in >= 95% of
  repeats on each footing; R KILLED in <= 1% (CFG825's C2 null rate). The R word CONSISTENT is expected to be impossible (sigma_R >= 0.02 >
  0.005); UNDECIDED is the expected survival label. Arm A falsified (gamma-hat < 1.056) is reported, never hidden.
- B1, B2, B3: "kill triggers" = at least one registered framework kill route fires (R KILLED, or the Arm C / settling falsification row
  with the evaluable stability conditions passing) in >= 95% of repeats. Each route's rate is reported. Below 95% = **POWER GAP** for that
  class (a property of the frozen rules at the plan's N, not a code fault), and the THEORY_CANONICAL kill line is then CONFLICTING (section 2).
- A1 vs A0: |mean gamma-hat(A1) - mean gamma-hat(A0)| < 0.5 sigma_fit and |mean R(A1) - mean R(A0)| < 0.5 sigma_R; otherwise flagged as a
  data/model selection asymmetry for the owner.
- D: information only (expected UNDECIDED).

**Hand expectations (written now).** A0/C: R about 1.00 (a +0.01-level noise bias possible), UNDECIDED; gamma-hat about 1.00, Arm C
consistent, Arm A falsified. A1: shift small, sign unknown (lean negative). B1: gamma-hat about 1.33 lands in the > 1.23 guard zone (no
verdict for any arm); R about 1.2 with N_R of order 2e3 gives sigma_R about 0.07-0.08, so KILLED in well under 95%: POWER GAP expected.
B2: R about 1.15, rarely KILLED; gamma-hat probably in the Arm C falsification row. B3: gamma-hat about 1.16, Arm C falsification row in
about 100%; R about 1.1, rarely KILLED. D: never KILLED. Scan: R kill rates rise with N_cat.

**Controls.** K1 replica = frozen `make_population` (byte-identical). K2 in-memory vt equals `ingest_csv` vt from the written CSV
(relative difference < 1e-12; CFG825 C0 analogue). K3 CFG825's class arithmetic (its C3 table) reproduced through the import. K4 sha256 of
every frozen file and of CFG825's official outputs before and after each script; `cfg816_r_dr4_results.json` absent before and after.
K5 peak RSS < 900 MB per process (in-script guard aborts above it; 1 GB is the cap). **MUTATE** (separate `_MUTATE` outputs): a planted
x 1.2 step at x > 1 at N_cat = 300,000 must come out R KILLED; if not, the dry run is NOT DIAGNOSTIC.

**End-to-end release-day chain on MOCK CSVs** (classes A0, B1, B3, C, one catalogue each): the frozen `wide_binary_pipeline.py
--catalog` run through a harness whose only change is the chunked master (memory cap), then `amdt14_distances.py --log` and
`arm_c_rows.py --log` on its log (they only print), then CFG825's `read_table` + `score` (B = 2000) on the mock pair table. Pass = every
step exits as designed and prints its block; the pipeline's own self-test result is reported as printed (it is seed-dependent, Amendment 18(f)).

## 4. Verdict words for this lane
**READY** = H1-H3 show no unexplained mismatch, every release-day code path runs end to end on mocks, A0/A1/C pass, MUTATE bites, and
K1-K5 pass. **NOT READY** otherwise. Power gaps (section 3) and conflicts (section 2) are reported beside the verdict as owner items;
they do not by themselves make the code NOT READY. Ambiguities found are written as a dated NOTE in this lane's README with proposed
clarification text for the owner; no amendment is filed and no frozen file is touched.

## 5. Compute
One process at a time, `OMP_NUM_THREADS=1 nice -n 10`, beside a live 1024^3 job; no process over 1 GB (guard at 900 MB).
