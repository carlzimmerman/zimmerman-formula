# Verifier report B: CFG76, CFG77, CFG78 (export commit 4fa9f54e3aa8e5104c7dce9a2c6f75be7f5a8b4c)

All runs from the scratch export, each in its lane directory, `timeout 1500`. Committed outputs read from `git show HEAD` (saved in rerun5/B_committed). Run logs in rerun5/B_runs.

| lane | script | mode | exit | expected exit (source) | tally | equals committed .out? |
|---|---|---|---|---|---|---|
| CFG76 | cfg76_sluggs_jam.py | main | 1 | 1 by design, ddof=0 G1 fails (README, script) | 14 PASS / 2 FAIL (G1 ddof=0, nu_mono and nu_rar) | yes (line-identical to cfg76_main.out incl. timings) |
| CFG76 | cfg76_sluggs_jam.py | MUTATE=1 | 1 | 1 (README) | 14 PASS / 4 FAIL (G1 all four kernel/ddof combos) | yes (identical to cfg76_MUTATE.out) |
| CFG76 | cfg76_compare.py | post hoc, no control | 0 | none stated | prints diffs vs CFG55 JSON | no committed .log to compare; numbers agree with README |
| CFG76 | cfg76_diag_distance.py | post hoc, no control | 0 | none stated | per-galaxy logM table | no committed .log; consistent with README |
| CFG76 | cfg76_posthoc_attack.py | post hoc, no control | 0 | none stated | gamma scan, LOO etc. | no committed .log; every README number matches (LOO 0.085-0.110, N=12 +0.055/+0.026, gamma zero-crossings 1.83/2.45, key-artefact 0.080) |
| CFG76 | cfg76_posthoc_dyn.py | post hoc, no control | 0 | none stated | variants table | no committed .log; README rows match (Hernquist +0.087/+0.033, w/o 7457 +0.096/+0.047, JAMx0.5 +0.216 9.11 sigma, Salpeter +0.076/+0.021 not-reproduced) |
| CFG77 | cfg77_run.py | main (contains K6 mutate check) | 0 | 0 (README) | 6/6 controls pass | yes (stdout identical to cfg77_run.out apart from timing 803 s vs 350 s and the numpy matmul RuntimeWarnings, which the committed .out has merged in from stderr); cfg77_results.json byte-identical |
| CFG77 | cfg77_cov_attack.py | post hoc, no control | 0 | 0 (posthoc_rc.txt) | n/a | yes, identical |
| CFG77 | cfg77_fhot_alt.py | post hoc, no control | 0 | 0 (posthoc_rc.txt) | n/a | yes, identical |
| CFG77 | cfg77_fhot_alt2.py | post hoc, no control | 0 | 0 | n/a | yes, identical |
| CFG77 | cfg77_fhot_alt3.py | post hoc, no control | 0 | 0 | n/a | yes, identical |
| CFG77 | cfg77_fhot_alt4.py | post hoc, no control | 0 | 0 | n/a | yes, identical |
| CFG78 | cfg78_ufd_rederivation.py | main | 0 | 0 (README) | FAILS: none (H1'/H2' PASS as agreement with CFG46's expected fail) | yes (only a trailing-newline difference) |
| CFG78 | cfg78_ufd_rederivation.py | MUTATE=1 | 0 | 0 per README (disclosed defect); script header says 1 is intended | FAILS: none | yes (only trailing-newline difference) |

Total runs: 14. Exit-code mismatches: 0. Tally mismatches: 0. Tracebacks: 0 (stderr only holds scipy IntegrationWarnings in CFG76 and numpy matmul RuntimeWarnings in CFG77).

## Findings
1. Everything reproduces; no exit-code or tally mismatch, no traceback.
2. CFG77 needs git-ignored data (real_research/data/lensing_rar/brouwer2021_rar/ 2.3 MB and lr_lenses.npz 9.7 MB; both ignored by real_research/data/lensing_rar/.gitignore, absent from the git archive). Not copied: cfg77_lib.py hardcodes REPO=/Users/carlzimmerman/new_physics/zimmerman-formula, so it read the live tree directly (read-only). The main 17 GB lensing files were not needed. So CFG77 is NOT reproducible from a clean git export without that data.
3. Absolute-path dependence: CFG76 (DATA), CFG77 (REPO) and CFG78 (REPO) hardcode the live-repo path for their inputs (all tracked files except the CFG77 lensing data), so "clean export" runs read inputs from the live working tree, not the export. cfg76_compare.py, cfg76_posthoc_dyn.py and cfg76_diag_distance.py also read the live CFG55 results JSON by absolute path (tracked). Inputs are tracked so the result stands, but a clone at another path or user would fail with FileNotFoundError.
4. Controls whose exit code cannot discriminate from the main run: CFG76 MUTATE exits 1 like main (rc 1 by design both times); the failure sets differ (main 2 FAIL, MUTATE 4 FAIL, a superset), so the tally discriminates but the exit code does not. CFG78 MUTATE has the same failure set as main (empty, FAILS: none) and rc 0 = main rc 0: the exit code cannot discriminate, as the README discloses (script header still says MUTATE exit 1 is intended; the README says rc 0: internal inconsistency). CFG77's K6 mutation is a check inside the main run and passes.
5. No control is declared "failed and kept" beyond the declared, expected CFG76 ddof=0 G1 failure (main rc 1 by design).
6. CFG76 post-hoc scripts have no committed .log (README says each writes one; none are in git, none are written by the scripts to disk: they print to stdout). Not-reproduced Salpeter row (+0.076/+0.021 vs lane +0.049/-0.033) is as disclosed in README.
7. CFG76 MUTATE must be run after main (it reads cfg76_results.json "main" written by the main run); with the tracked copy present that order is satisfied anyway.
8. CFG77 wall time was 803 s under parallel load (committed 350 s); no timeouts.
