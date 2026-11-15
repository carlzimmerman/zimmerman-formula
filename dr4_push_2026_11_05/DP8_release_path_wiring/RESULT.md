# DP8: the owner decision of 2026-11-15b wired into the Gaia DR4 release-day path, checked on DR3

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

Criteria: `FROZEN_CRITERIA.md`, committed alone at 4caa8bc91f before any code, edit or number of this lane; AMENDMENT A1 (one
added check, C6(f)) committed alone at dd18067f7c before its run. The edits of the wrapper, the runbook and `dp3_sigma_sys.py`
are commit cdd71a3246 (separate from this folder). Authority: `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md`
("Accept all recommended"), with 11-05c (filed 2026-11-08) and `OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md`. Run date
2026-11-15. DR3 only: every DR3 number below is a code-path test, never a result (Amendment 7(e)). No network, no archive query,
no DR4 byte; no frozen file edited (the 30 pinned files are unchanged before and after, `checks/pins_before.txt` = `pins_after.txt`).
Nothing pushed.

## 1. Labels, one per item

| item | label | what changed | checks |
|---|---|---|---|
| Q1 seed-mean entry wired | **WIRED** | new gated step G11S runs DP7's K = 50 sweep (cones-literal, pipeline fit, extract fallback for the rung) through a new read-only launcher, `dp8_seed_mean_release.py`, under `dp6_with_a17.py`; O12 passes `--nss-off-seed-mean`; `dp3_sigma_sys.py` text corrected (filed 2026-11-08) | C1, C2, C3, C6, C7(a) |
| Q2 cone fallback, with counts | **WIRED** | G11 passes `--missing-cones extract-fallback`; G11S passes `--rung-missing-cones extract-fallback`; `dp8_fallback_count.py` writes the number of fallback pairs (G11's rung and the sweep's k = 0 rung) | C3 (D5b), C7(b) |
| Q5 the (b) rungs | **WIRED** | O12's main call carries the D2 recipe's three entries; new O12r runs RUWE < 1.2 as a separate information call | C4 |
| Q8 Amendment 14(c) statistic | **WIRED** | new O16 after the label step runs `dp8_sepbins.py` report-only; it reads `q8_code_path_check` and prints NOT RUN unless PASS | C5 (the Q8 code-path check: PASS) |
| Pins | **WIRED** | 11-15 (3641f7de...) and 11-15b (dad0d100...) in HASHES (28 -> 30) and in the prereg-directory cleanliness check | C1 |
| Q3 R label | **WIRED TEXT ONLY** | runbook section 2 and the result template; final log line | - |
| Q4 one verdict line per footing | **WIRED TEXT ONLY** | runbook section 2 and the result template; final log line | - |
| Q7 September ridge rows | **WIRED TEXT ONLY** | runbook sections 1-3 (`dr4_scorer.py` not run; one information sentence per row) | - |
| Q9 Milky Way rows | **WIRED TEXT ONLY** | runbook sections 1-3; final log line | - |
| Q10 optional neighbour tables | **WIRED TEXT ONLY** | runbook G1 / G7 rows and template; wrapper STOP texts of G1 and G7 | - |
| T3 anonymous access | **WIRED TEXT ONLY** | runbook G2 row and O3; wrapper G2 STOP text asks for `SKIP G2` | - |
| O3, O6, cone coverage marked decided | **WIRED TEXT ONLY** | runbook section 5, each with a pointer to 11-15b | - |
| 11-15b section 4 (G11S cannot run on the day while G11 built the rung; or DP8's launcher check not PASS) | **NEEDS OWNER** | not decided here. The wrapper stops (exit 7, "NEEDS OWNER") at G11S or O12 and never computes (b) with the single-seed entry; a dated owner decision is needed before the data | C6(c pre), C6(f) |

## 2. Finding recorded before any code

`dp7_seed_mean.py` installs a socket guard at import and its `main()` exits on `--allow-network` ("DR4 path: not run in DP7").
The DR4 command in DP7 RESULT section 7 therefore could not run as written. The launcher `dp8_seed_mean_release.py` imports it
read-only and changes nothing on DR3 except where outputs go (C7(a): bit-identical to DP7). On DR4 it lifts the refusal and the
import-time guard only with `--release dr4 --allow-network` and a "GO G11S" line; anything else exits 2 (C6(d)). Its DR4 network
path (DP7's own `rung_build` with `allow_network = True`, the driver's delta correlation fetch) cannot be tested before release.

## 3. Checks, with numbers and mutations (`dp8_checks.json`, detail `dp8_grade_detail.json`, outputs in `checks/`)

| id | result | the check | its mutation twin |
|---|---|---|---|
| C1 | PASS | real `--check`: "hashes: all 30 pinned files OK", "SUMMARY hashes OK"; scratch mirror (55 files, `git init`) with the real wrapper unchanged: OK | one byte added to the mirror's 11-15b copy: HASH MISMATCH a19491d0... (pinned dad0d100...), "prereg directory NOT clean", "SUMMARY hashes FAIL"; same for 11-15 (51974cc9... vs 3641f7de...) |
| C2 | PASS | `dp3_sigma_sys.py --nss-off-seed-mean <DP7 dp7.json>` on the release-day path (DP1's DR3 rung, the registered catalogue, the G50 manifest; DP7's K = 50 sweep **reused, not re-run**): 77 of 77 numbers equal DP7's `dp3_seedmean_releasepath.json` exactly, standalone and in the dry run (D6c); (b) 0.0200 / 0.0200. Only the three corrected note strings differ. Text-only proof: AST with strings blanked identical to HEAD; option off = DP7's `dp3_d6_replay.json` in every leaf (74 numbers, strings too); option on with D6 inputs = DP7's `dp3_seedmean_d6inputs.json` (93 numbers) | option dropped: (b) 0.0225 / 0.0287, which is exactly DP7's `b_single_seed`; comparison fails (25 numbers differ). AST of a copy with 0.020 -> 0.021: DIFFERENT |
| C3 | PASS | the test copy's `--dry-run-dr3`: all 29 D steps that passed on 2026-11-05 PASS again, plus 12 new (D5b x3, D5c x3, D6c x2, D6d x2, D8c, D9); exit 0, "every D step PASS". Same numbers: 6,210 / 6fff64d964ebaa72, 6,180 / c5cb89e8f95bfe3d, canonical 1.0750, D6 shifts max diff 0.0000 and (b) 0.0375 / 0.0412, R 0.972839 N_R 348; both outcome-map outputs byte-identical to DP3's (UNDECIDED both footings). `dr4_outcome_map.py --self-test` 20/20, output byte-identical to the committed one | the comparator, fed DP3's committed log with "PASS D7 R reproduces ..." turned into FAIL, reports it. Outcome-map DP3_MUTATE=1: 13/20, exit 1; DP3_MUTATE=2: 19/20, exit 1 (as committed) |
| C4 | PASS | the main O12-form JSON has sha256 7ee1bdef... before and after the RUWE call, and a fresh main call gives the same bytes; the RUWE call writes only its own file. In the dry run (D6d): byte-identical, 82752ea8... | `--stage-a` on the main call: bytes d9391a99..., (e) 0.0067 -> 0.0058 canonical, 0.0085 -> 0.0078 alt ((b) 0.0200 in both) |
| C5 | PASS (= `q8_code_path_check: PASS`) | (i) XR22's own `sepbins` (source sha256 5cccbd82..., taken by `ast`, unedited) and DP8's data-side function: all 7 bins bit-identical on the model population (716,117 pairs, B = 1); edges = XR22's SEPBINS. (ii) DR3 registered catalogue: finite r_b, sigma_b in all 7 bins; two runs byte-identical (7d567bb9...). (iii) the dry run's D9 output, after the label steps, is the same bytes as a standalone run | edges with 6 kAU for 5: self-test FAIL, exit 1; catalogue minus its last row: b8608313..., different |
| C6 | PASS | (a) real `--run` today: "STOP: DR4 not yet available", exit 3, before any step. (b) test copy, date moved, no GO line: "STOP at G1", exit 10. (c) markers to G11, GO for every gated step but G11S: "STOP at G11S", exit 10; before `dp8_checks.json` existed the same run read "G11S: NEEDS OWNER", exit 7. (d) launcher refusals, exit 2, three cases (D5c). (e) sandbox control: a python connect to 192.0.2.1:443 is denied. (f, A1) no G11S output: "O12: NEEDS OWNER", exit 7; a well-formed output: O12 goes on to `dp3_sigma_sys.py` (fails offline on the missing DR4 catalogue, exit 7) | GO G11S given: "G11S: GO on record", then the step fails offline on the missing DR4 manifest (FileNotFoundError), exit 7. (f) K = 8 in the sweep output: "O12: NEEDS OWNER", exit 7 |
| C7 | PASS (C7(a) = `q1_launcher_check: PASS`) | (a) launcher DR3 pass-through, cones-literal, pipeline fit, K = 2, `--no-fit-cache`: 42 of 42 values bit-identical to DP7's committed `parts/dp7_k00..k02` (N, sha256 of base and rung; base, rung, delta, both sigma_fit, both footings); DP7's own K3, K5 (35 files) and K6 pass inside it. (b) fallback counts: G11 form 139 pairs without a cone, 0 flagged by the fallback; the sweep's k = 0 rung 139, 0 (= DP7's bias_bound) | (a) `--keep-nss`: rung bytes = base bytes, every delta 0, 23 of 42 identical: fails. (b) the DR3 rung with `--missing-cones error`: "ConeCoverageError: 139 of 10370 pairs ... have NO neighbour cone", exit 1; the count helper on a manifest with no cones block: exit 1 |

DR3 code-path numbers of the new O16 step, information only (registered DR3 catalogue, 6,210 pairs; r_b = median vtilde /
model median - 1, bootstrap sigma; footing-free): 2-3 kAU +0.0471 +- 0.0161 (n 2,294); 3-5 +0.0447 +- 0.0166 (2,022); 5-7
+0.0722 +- 0.0272 (820); 7-10 +0.0109 +- 0.0345 (542); 10-15 +0.1014 +- 0.0389 (348); 15-20 +0.1131 +- 0.0701 (130); 20-30
+0.0201 +- 0.0921 (54). Amendment 14(c)'s xi reading is not computed.

## 4. What the release day now runs, in order

1. `--check` (30 pins; prereg directory incl. both 11-15 decisions clean; DP1 and DP8 states printed).
2. R0 self-tests.
3. G1 data model, spec, manifest; the manifest records the counts of `crowded_field_source` / `gaia_source_environment` and that they are not searched (Q10).
4. G2: `SKIP G2`, anonymous (T3).
5. G3 base extract; G4 stages A-F; G5 cut-12 tables; G6 candidates and pre-brief.
6. G7 cones for the post-NSS set (caps in the GO line); neighbours manifest records Q10.
7. G8 primary build, cones-literal; O9 frozen pipeline fit, A14 / Arm C lines.
8. G10 Amendment 18 sweep, seed label.
9. G11 NSS-off rung, **now with `--missing-cones extract-fallback`**, and its fallback count (Q2).
10. **G11S (new, `GO G11S`):** the K = 50 seed-mean sweep through DP8's launcher, refused unless `q1_launcher_check` is PASS; then the fallback counts of G11 and the sweep (Q1, Q2).
11. **O12:** `dp3_sigma_sys.py --nss-off-seed-mean <G11S json>`, (b) = R_chance < 0.001, 3-20 kAU, the seed-mean NSS-off entry; stops with NEEDS OWNER if the sweep output is missing or not (dr4, K 50, cones-literal, pipeline, extract-fallback, complete); then the pair table (Q1, Q5).
12. **O12r (new):** the RUWE < 1.2 information call, separate file, never read for (b) (Q5).
13. G14 once-only `cfg816_r.py --dr4`; O15 outcome map, per footing.
14. **O16 (new):** Amendment 14(c)'s statistic, report-only, or NOT RUN with the reason (Q8).
15. `RESULT_2026-12-02.md` from the runbook's template (section 3): per-footing lines, CFG816's own R label with the scorer's word beside it, ridge rows and Milky Way as information, fallback counts, sepbins status, the recorded choices.

## 5. Cost (tally of this lane's `/usr/bin/time -l` stage logs, `checks/cost_tally.out`)

17 timed stages, 1,090 s wall in total (18.2 min). The heaviest:
- the dry run, 581 s, peak RSS 3.99 GB; inside it each frozen pipeline fit took 31 s at 3.92-3.93 GB, and the D5b rung build 8 s at 2.61 GB;
- the launcher check, 206 s, and its mutation, 213 s; each did 9 builds and 6 fits at 3.98 GB peak.

Each `dp3_sigma_sys.py` call took about 9 s at 1.3-1.4 GB, and each sepbins run 2-5 s at up to 2.1 GB. One heavy job at a time:
the runner checked with `ps` for other python jobs above 2 GB before each heavy stage, and found none. Some light steps were not
timed and are not quoted: the `--check` and `--run` refusal runs, the count helper, and the grader.

## 6. Disclosures

- **The wrapper's guard fails open when `ps` cannot run.** Under `sandbox-exec`, `/bin/ps` is not permitted. The guard then logs
  "no python job > 2 GB live" without having looked. In this lane the runner's own `ps`, run outside the sandbox, enforced the
  one-job rule. On the day the wrapper runs unsandboxed, so this does not arise. A one-line fix (refuse when `ps` fails) is
  outside this lane's scope and is listed as a follow-up.
- **Free disk was 16-17 GB at run time, below the wrapper's 20 GB.** A real `--run` would be refused today on disk alone.
  The test copy lowers the threshold. Its diff against the committed wrapper, `checks/testcopy.diff`, is exactly 6 lines: the
  APPROVAL path, RELEASE_DATE, the three OUT lines and the disk threshold. The committed wrapper was checked to be the file
  the copy was made from.
- **One network probe before the criteria.** Before the criteria were written, one probe tested the sandbox: `curl` to
  example.com under the deny profile, refused. The system resolver may have looked up that name. No other network attempt was
  made.
- **The real `--run` test created a folder, which the runner removed.** It created `DP3_release_day/release_2026_12_02/` holding
  only its `release_day.log`. The runner checked the contents first.
- **Text inside DP7's output was not changed.** DP7's sweep JSON still carries DP7's own criteria and "DR3 code-path" strings.
  On DR4 the launcher's sidecar `<out>.dp8.json` records the release, the GO line and the network state.
- **DP7's K4 cross-check will not find the G10 builds on DR4.** K4 looks for `seed_k<k>/final_g50.csv`, but G10 on DR4 writes
  under the tag `dr4_g50`, so K4 will report those builds absent. K4 is not a gate.
- **The DR4 sweep's archive load is unmeasured.** Its stage-G delta fetches can be measured only on the day. DP7's projection is
  quoted in the G11S STOP text.
- **DP8's tools are not pinned in the wrapper,** as DP1's, DP6's and DP7's are not. Their sha256 at this commit:
  `dp8_seed_mean_release.py` bb3de302..., `dp8_fallback_count.py` 2e8bee65..., `dp8_sepbins.py` 4a38669c....
- **Output folder renamed.** The runner first wrote to `out/`, which the repository's `.gitignore` ignores. The folder was renamed
  `checks/` before commit, and the scripts were changed to match. AMENDMENT A1's `out/c6f_*.out` are now `checks/c6f_*.out`.
- **Not committed:** `work/` (the C7 run folders, CSVs and the C4 / C5 second copies), `release_testcopy/`, the test copy
  itself, the dry run's CSVs and its `*.log`.

## 7. Files

This folder:
- the criteria: `FROZEN_CRITERIA.md`;
- the tools and the check machinery: `dp8_seed_mean_release.py`, `dp8_fallback_count.py`, `dp8_sepbins.py`, `dp8_checks.sh`, `dp8_grade.py`, `dp8_cost_tally.py`;
- the check states and grade: `dp8_checks.json` (read by the wrapper), `dp8_checks.out`, `dp8_grade_detail.json`;
- `RESULT.md`;
- `checks/` (every check and mutation output, `testcopy.diff`, `cost_tally.out`, the pin lists, `c7_eq/`, `c7_MUTATE/`);
- `logs/` (the stage time logs, `stages.txt`);
- `dry_run_dr3/` (the dry run's `.out`, `.json`, `.time` and manifest files).

Outside this folder, commit cdd71a3246: `dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh` (sha256 45e07a91...),
`RELEASE_DAY_RUNBOOK_DR4.md` (a89f1de7...) and `dp3_sigma_sys.py` (5fc753c0...).

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
