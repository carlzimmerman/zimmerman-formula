# Verifier report D — CFG88 (KiDS jackknife), CFG89 super spirals, CFG90 a0(z), CFG91 satellites
Export commit: 4fa9f54e3aa8e5104c7dce9a2c6f75be7f5a8b4c. 15 runs, all rc as declared, 0 tracebacks, 0 timeouts (each < 1 min). Raw stdout/stderr/rc in rerun5/runsD/.

| lane | script | mode | exit | expected exit (source) | tally | equals committed .out? |
|---|---|---|---|---|---|---|
| CFG88 | CFG88_kids_split_jackknife.py | main | 0 | 0 (README) | 12/12 checks pass; 0 load-bearing failures | yes, 0 diff lines; results.json identical except "seconds" |
| CFG88 | same | MUTATE=1 | 1 | 1 (README, FROZEN_CRITERIA) | 10/12 pass; H1, H2 fail | yes, 0 diff lines; json identical except "seconds" |
| CFG89 | cfg89.py | main | 0 | 0 (README) | CONTROL FAILURES: none; V1 H1 PASS, H2 FAIL as frozen | yes, 0 diff; cfg89_results.json byte-identical |
| CFG89 | cfg89.py | MUTATE=1 | 0 | 0 (README: "all three modes exit 0") | CONTROL FAILURES: none (C6: H1 and H2 fail, asserted) | yes, 0 diff |
| CFG89 | cfg89.py | MUTATE=nu1 | 0 | 0 (README) | CONTROL FAILURES: none (C6b) | yes, 0 diff |
| CFG89 | cfg89_post_selection_sim.py | main only (post hoc, no control) | 0 | none stated | excess +0.071 (sd 0.016), obs +0.059, P = 0.774; corrected nine +0.092 | yes, 0 diff |
| CFG90 | cfg90.py | main | 0 | 0 (README) | reproduced 18 of 31; controls 15/15 pass | numbers/tally yes; text NOT byte-equal (see F3) |
| CFG90 | cfg90.py | MUTATE=1 | 1 | 1 (README) | reproduced 9 of 31; controls 15/15; total 338 -> 477, pool 15 -> 37, PHIBSS 0 -> 11 | numbers/tally yes; text NOT byte-equal (see F3) |
| CFG90 | posthoc.py | main only (post hoc, no control) | 0 | none stated | sweep table | yes (committed copy also holds stderr warnings; stdout identical) |
| CFG90 | posthoc2.py | main only (post hoc, no control) | 0 | none stated | sensitivity table | yes (same stderr note) |
| CFG91 | cfg88.py | main | 0 | 0 (README) | H1 pass; H2 classical -1.95/-1.94; FAILED CONTROLS: none | yes, 0 diff; both results.json byte-identical |
| CFG91 | cfg88.py | MUTATE=1 | 1 | 1 (README, "by design") | UFD rule median +0.322 (+2.44 sigma); H3 fails (fraction 0.050); FAILED CONTROLS: none | yes, 0 diff |
| CFG91 | cfg88_sens.py | main only (no control) | 0 | none stated | z 0.0317: -3.37; total 0.0716: -1.49 | yes, 0 diff |
| CFG91 | cfg88_post.py | main only (no control) | 0 | none stated | UFD/classical rows match CFG42 README | matches untracked working-tree run_post.log (identical); no committed .out |
| CFG91 | cfg88_post2.py | main only (no control) | 0 | none stated | 49 lines | matches untracked working-tree run_post2.log (identical); no committed .out |

## Findings
1. No exit-code mismatch, no traceback, no tally mismatch in any run. No numeric difference from any committed .out except F3.
2. Data: CFG88 needs git-ignored data, but small. I copied real_research/data/lensing_rar/lr_esd_jackknife.npz (1.4 MB), lr_esd_jackknife_analysis.npz (24 KB) and brouwer2021_rar/ (2.3 MB). The 17 GB lensing files were not needed or copied. A truly clean clone of git-tracked files alone cannot run CFG88 (README lists this under "Data requirements (not in git)"). CFG89, CFG90 and CFG91 ran without any git-ignored file.
3. CFG90: the committed cfg90.out and cfg90_MUTATE.out are not what a fresh run writes. The committed main .out contains a stale duplicated 8-line block (a repeated PHIBSS radius sweep with a truncated "PHIBSS rpeak" line) and no trailing "exit 0" line. The committed MUTATE .out has a duplicated 12-line DIFFER block. A fresh run is 8 lines (main) and 12 lines (MUTATE) shorter than committed, plus one "exit N" line. All counts and tallies are identical. This looks like a stitched or edited file, consistent with the README's own disclosure that the script was extended after the saved output.
4. CFG90 MUTATE reads cfg90_results.json (the main run's JSON) to decide its exit, so it must run after main. My parallel run used the identical committed JSON, so no effect. The README itself says the exit code is "partly by construction" (the equality-with-main check must fail). MUTATE's own control set is different from main (main 15/15 controls; MUTATE exit depends on the direction test plus all_ctrl_mut), so the exit does discriminate.
5. CFG89: all three modes exit 0, so the exit code cannot discriminate main from MUTATE. Discrimination is by asserted PASS checks (C6, C6b). The README says so. The README also notes that MUTATE=1's nine-fastest clause alone is weak (-1.97 sigma). CFG89 has no failing-and-kept control in the final run; the two earlier failed runs (FIRSTRUN crash, SECONDRUN C1i) are kept as disclosed .out files, and not re-run.
6. CFG91: MUTATE has an empty failed-control set, the same as main ("FAILED CONTROLS: none"). Its rc 1 comes from a hard-coded exit (cfg88.py line 295: exit 1 if the mutated UFD rule closes within 2 sigma is NOT true), not from a failed check. It does discriminate (main rc 0 vs MUTATE rc 1), but only through that special case. cfg88_FIRSTRUN.out (C1b failed and kept) is a disclosed first-run failure and was not re-run.
7. CFG88 main and MUTATE fail different sets (none vs H1 and H2), so its control is informative.
8. Post-hoc scripts (CFG89 selection sim, CFG90 posthoc/posthoc2, CFG91 sens/post/post2) have no MUTATE control. CFG91 post and post2 have no committed output (their run_post*.log are untracked in the working tree; the export has none). CFG90 posthoc/posthoc2 emit RuntimeWarning "Mean of empty slice" from cfg90.py line 112 (stdout unaffected); cfg90.py also emits an IntegrationWarning at line 74.
