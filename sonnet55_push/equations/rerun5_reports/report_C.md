# Verifier report C (CFG82-CFG87), export of HEAD 4fa9f54e3

Runs in the scratch export, each in its own directory, in parallel (wall times 3-4x the committed ones because of load). Raw stdout/stderr/rc in `rerun5/runsC/`. Committed outputs read with `git show HEAD:`; timing fields ignored. No Python Traceback in any of the 14 runs.

| lane | script | mode | exit | expected exit (source) | tally | equals committed .out? |
|---|---|---|---|---|---|---|
| CFG82 | cfg79_feasibility.py | main | 0 | 0 (README "both rc 0") | diagnostic table only, no tally | no committed output (README names feas.log; not in git) |
| CFG82 | cfg79_toy_selection.py | main | 0 | 0 (README) | toy sigma(gamma) 0.25/0.16/0.09/0.06 = README's numbers | no committed output (toy.log not in git); README values match |
| CFG83 | cfg80_ufd_luminosity_trend.py | main | 1 | 1 by design (README) | FAILS: [C1e] | yes (only elapsed 119 s vs 432 s) |
| CFG83 | cfg80_ufd_luminosity_trend.py | MUTATE=1 | 1 | 1 (README) | FAILS: [C1e] | yes (only elapsed 73 s vs 322 s) |
| CFG84 | cfg84.py | main | 1 | 1 by design, P2 (README) | 14/15 pass, failing [P2] | yes (identical) |
| CFG84 | cfg84.py | MUTATE=1 | 1 | 1 (README) | 12/15 pass, failing [P2, H1b, M1] | yes (identical) |
| CFG85 | cfg85_rederive.py | main | 0 | 0 (README) | CONTROLS FAILED: none | yes (only trailing newline) |
| CFG85 | cfg85_rederive.py | MUTATE=1 | 1 | 1 (README) | CONTROLS FAILED: [C5c, C3iii] (the two meant to fail) | yes (only trailing newline) |
| CFG85 | post_alt.py | main-only, no control | 0 | none stated | V3u +0.035 z +0.43; V4u +0.003 z +0.04 | yes |
| CFG86 | CFG86_lcdm_slacs_rederivation.py | main | 0 | 0 (README) | FAILED CHECKS: [] | yes (stdout identical; stderr has the same IntegrationWarnings, differing only in path prefix) |
| CFG86 | CFG86_lcdm_slacs_rederivation.py | MUTATE=1 | 1 | 1 (README) | FAILED CHECKS: [C5, H1] | yes (identical) |
| CFG86 | probe_posthoc.py | main-only, no control | 0 | none stated (post hoc) | B-LCDM min +0.023 median +0.118 max +0.266 | yes |
| CFG87 | CFG87_b_paired.py | main | 0 | 0 (README) | FAILED CHECKS (0): [] | yes (only grid/total time lines) |
| CFG87 | CFG87_b_paired.py | MUTATE=1 | 1 | 1 (README) | FAILED CHECKS (2): [C5, H2] | yes (only time lines) |

body.py and cfg86_lcdm_copy_reference.py (CFG87) are not standalone entry points: cfg86_lcdm_copy_reference.py is byte-identical to CFG86's script (cmp), and body.py is the frozen-docstring body/helper; neither was run separately.

Counts: 14 runs, 0 exit-code mismatches, 0 tally mismatches, 0 tracebacks.

## Findings

1. **Absolute-path data dependence (all six lanes).** Every script reads its inputs from the absolute working-tree path `/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/...`, not from the clean export. So the "clean export" reruns are not data-isolated. I checked that all inputs used are git-tracked and unmodified in the working tree (`git status` clean for them), so the runs match HEAD data; but the scripts would not run on another machine or path as written. CFG83 also uses `/Users/.../real_research/data/dsph/lvd_dwarf_mw.csv` (tracked).
2. **CFG83 MUTATE cannot discriminate by exit code.** Main and MUTATE have the identical failure set {C1e} and both exit 1. The README itself says the MUTATE run on the real 40-object data is uninformative and that the injection controls (C1d/C1f) carry the bite. **C1e is a control declared "failed as declared and kept"** (0.117 vs [0.02, 0.09]); it reproduces exactly.
3. **CFG84 has a control failed and kept:** P2 (rounding artefact in the target list) fails in both main and MUTATE; main exit 1 is by design. MUTATE adds {H1b, M1}, so it does discriminate from main by failure set.
4. **CFG85 and CFG86:** main exits 0 with no failures; MUTATE exits 1 with failures that are distinct from main, so exit codes discriminate. CFG85 committed .out has "DIFF" lines (V3/V4/V3u/V4u reading differences) that are reported rows, not control failures; they reproduce identically.
5. **CFG87:** main rc 0, MUTATE rc 1 (failing {C5, H2}); discriminating.
6. **CFG82 has no committed output and no MUTATE control** (README says so). README refers to `toy.log`/`feas.log`, which are not in git; I could only compare against README's stated numbers (toy sigma(gamma) values match). Naive-MLE table from the feasibility script is unverified against a committed log.
7. Stderr noise: CFG83 emits RuntimeWarnings (divide by zero/overflow at line 283 in a permutation correlation, both modes); CFG86 emits scipy IntegrationWarnings (same as the committed err_main.txt/err_mut.txt). Neither affects rc or tally.
8. Working-tree runs wrote outputs only inside the scratch export; the repo was not touched.
