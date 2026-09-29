# Verifier report E (campaign_fresh_gravity CFG92-CFG96, CFG99)

Export: `git archive` of HEAD 4fa9f54e3 (rerun5/HEAD.txt). All runs from each lane's own directory; committed outputs read with `git show HEAD:`; timing fields ignored. Logs in rerun5/logsE/. 22 runs executed; the machine was heavily loaded by other sessions, but no run hit the 25-min timeout.

| lane | script | mode | exit | expected exit and source | tally | equals committed .out? |
|---|---|---|---|---|---|---|
| CFG92 | cfg92.py | main | 0 | 0 (README: "rc 0") | 12 PASS / 0 FAIL, FAILED CONTROLS none, H1 pass (0.0619 dex) | yes (0 diff lines) |
| CFG92 | cfg92.py | MUTATE=1 | 1 | 1 (README: "rc 1", H1 fails) | 13 PASS / 0 FAIL controls, H1 FAIL (0.0000 dex) | yes |
| CFG92 | explore2 / explore3 / explore_gext | main only (no control) | 0 / 0 / 0 | none stated; rc 0 | n/a (data exploration) | yes (stdout = committed .out, all 3) |
| CFG92 | post1_crossings / post2_diag / post3_omega | main only (no control) | 0 / 0 / 0 | none stated | n/a (post hoc) | yes (all 3) |
| CFG93 | cfg93.py | main | 1 | 1 by design (README: 7 frozen third-decimal lines + C3b fail; docstring: exit 1 if any line fails) | lines failed: 7 of 37 (R3 Boo I x3, R5 x3, C3b) | yes |
| CFG93 | cfg93.py | MUTATE=1 | 1 | 1 (README: 26 of 34 fail, H1 fails) | lines failed: 26 of 34 | yes |
| CFG93 | cfg93_post.py | main only (post hoc, no control, no committed .out) | 0 | none stated | Tuc II >=2-epoch cleaned N=7 sigma 2.31, offset +0.220 +/- 0.142 (1.55 sig): matches README text | no committed .out to compare; README numbers match |
| CFG93 | FIRSTRUN_cfg93.py (archived pre-fix first run; header: frozen before first run) | main only (no control) | 1 | 1 (committed FIRSTRUN out: 8 failed) | lines failed: 8 of 37 | yes (0 diff lines vs FIRSTRUN_cfg93.out) |
| CFG94 | cfg94.py | main | 1 | 1 by design (README: "rc 1 by design", one rounding-level gate) | controls failed: none; reproduction 16/17 (non-matching: R1 P x=0.3) | yes |
| CFG94 | cfg94.py | MUTATE=1 | 1 | 1 (README: all 17 gates fail) | controls none; reproduction 0/17 | yes |
| CFG94 | cfg94.py | MUTATE=2 | 1 | 1 (README: reaction gates and C3 fail) | controls failed: C3; reproduction 7/17 | yes |
| CFG94 | posthoc.py | main only (post hoc, no control) | 0 | none stated | 15 lines | first 15 lines identical; committed posthoc.out has 5 extra lines (see Findings 4) |
| CFG95 | CFG95_kids_split_own_calibration.py | main | 1 | 1 (README: H1 and H2 fail, exits 1) | 9/11 pass, 2 load-bearing failures (H1, H2) | yes |
| CFG95 | same | MUTATE=1 | 1 | 1 (README: fails H1 and H2) | 9/11 pass, 2 failures (H1, H2) | yes |
| CFG96 | CFG96_kids_split_isolation.py | main | 0 | 0 (committed out) | 8/8 pass | yes |
| CFG96 | same | MUTATE=1 | 1 | 1 (H1 must fail) | 7/8 pass, 1 failure (H1) | yes |
| CFG96 | CFG96_stage_stack.py | NOT RUN | - | - | needs git-ignored data: real_research/data/lensing_rar/KiDS_DR4.1_SOM_gold_WL_cat.fits 17.7 GB (plus KiDS_DR4_brightsample.fits 89 MB, KiDS_DR4_brightsample_LePhare.fits 258 MB) | not compared |
| CFG99 | cfg89_kmos3d_outer_rc.py | main, WITHOUT cubes | 1 | 1 (README: main exit 1; C1c, H1-can, H1-alt fail) | 16/25 pass, 9 failures (C1a-d, C2, C3, D1, H1-can, H1-alt); committed: 22/25, 3 failures | NO (cubes absent, see Findings 1) |
| CFG99 | same | MUTATE=1, WITHOUT cubes | 1 | 1 (README: C1c, D1, H1-can, H1-alt fail) | 16/25 pass, same 9 failures; committed: 21/25, 4 failures | NO |

## Findings

1. CFG99 is NOT verified. Needs git-ignored data: `../_external_data/kmos3d/cubes` (739 FITS cubes, 3.8 GB, outside the repo root, over the 200 MB limit), not copied. Without it the script runs (no traceback; "cube files missing among selected: 569", 0 rows in the per-object csv) and exits 1, so the exit code matches the README only by coincidence. The tally does not (16/25 and 9 failures against the committed 22/25 and 3; MUTATE 16/25 against 21/25). Main and MUTATE have identical failure sets in this cubeless state, so the run cannot discriminate.
2. CFG96_stage_stack.py NOT run: needs the 17.7 GB KiDS_DR4.1 SOM gold WL catalogue (plus the 258 MB LePhare file). CFG96_kids_split_isolation.py consumes the git-ignored stage_stack outputs `cfg96_isoflags.npz` and `cfg96_stack.npz`. I copied the working-tree copies (with lr_esd_jackknife.npz, lr_esd_remeasured.npz, lr_lenses.npz, lr_esd_jackknife_analysis.npz; 6 files, about 26 MB) into the export. CFG96 iso and CFG95 therefore reproduce given those inputs, but the inputs themselves (the stack and isolation flags) were not regenerated and depend on git-ignored data.
3. CFG95 MUTATE control is non-discriminating, as declared: main and MUTATE both fail exactly H1 and H2 (9/11 each, rc 1 each). The README says so ("uninformative for the headline"); only C1's exact reproduction acts as a machinery check.
4. CFG94 posthoc.py: the script's output (15 lines) equals the first 15 lines of the committed posthoc.out, but the committed file has 20 lines. The last 5 duplicate lines (3), (3b), (4)x3, with the first one truncated ("in {1e9,1e10,1e12}: ..."). This is a stale or append artefact in the committed file, not a reproduction failure.
5. Exit-code discrimination: CFG93 (main 1, MUTATE 1) and CFG94 (main 1, MUTATE1 1, MUTATE2 1) all exit 1 in every mode; the controls discriminate only by failure set (CFG93: H1 passes in main and fails in MUTATE, 7 vs 26 lines; CFG94: 1 gate vs 17 gates / C3 control fail). CFG92 (0 vs 1) and CFG96 (0 vs 1) discriminate by exit code.
6. Declared failures kept: CFG93 C3b (cleaned sigma biased high with binaries, "fails, as declared") and the 3 frozen third-decimal R3 lines and R5 lines; CFG94 R1 P x=0.3 (rounding level); CFG95 H1/H2 (result, not a bug). CFG99 C1c "failed and kept" is declared in the README but could not be re-run (Finding 1).
7. No Python traceback in any run (stderr checked). CFG94 emits scipy IntegrationWarning/overflow RuntimeWarning, also present in the design. No exit-code or tally mismatch in any run that had its data.
8. Helper scripts explore2/3, explore_gext, post1-3 (CFG92), cfg93_post, FIRSTRUN_cfg93, posthoc have no MUTATE control; run main-only. FIRSTRUN_cfg93.py and cfg93.py both write cfg93.out/cfg93_results.json in the export (the FIRSTRUN run overwrote the main outputs there after the main comparison was done; harmless, but running the two in one directory collides).
