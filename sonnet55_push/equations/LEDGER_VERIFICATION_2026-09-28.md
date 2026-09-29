# Independent re-run of the closure-map equation ledger, 2026-09-28

Target: `campaign_fresh_gravity/closure_map/EQUATION_LEDGER_2026-09-28.md` (written by the orchestrating session, commit
f1eced0db). That file was NOT edited. This report is an independent second run of its 11 rows by a different session.
No equation was added and no label (DERIVED / POSTULATED / FITTED) was changed; kappa = 1/2 stays FITTED.

## Method
- Rows 1-10: `ledger_rerun.py` copies CFG43_fluid_tie, CFG44_fluid_target, CFG47_unruh_matching and CFG50_tidal_closure to a
  scratch directory (no committed output file in those lanes was touched), runs each script's main mode and each MUTATE
  control with the environment variable the script documents, and compares the exit code with the ledger's stated
  expectation. Output: `ledger_rerun.out` (26 runs).
- Row 11 (ChainCert, Lean): `bash ChainCert/verify_chain.sh` and `MUTATE=1 bash ChainCert/verify_chain.sh`, run in place
  (the 8 GB `.lake` cache is not copied); it builds into the git-ignored `.lake/`. Afterwards `git status` showed no
  tracked file changed and `ChainCert/_Mutate.lean` was removed.

## Result: every row reproduces
| row | script | main | controls | check counts vs ledger |
|---|---|---|---|---|
| 1, 2, 3, 4 | `CFG43_fluid_tie/A1_...`, `A2_...` | exit 0 | MUTATE=1, 2 exit 1 | A1 11/11, A2 5/5 (ledger 11, 5) |
| 5, 6 | `A3_cap_entry_form_and_obstruction.py` | exit 0 | MUTATE=1, 2 exit 1 | 11/11 (ledger 11) |
| 7 | `CFG44_fluid_target/B1_target_and_hydrostatics.py` | exit 0 | MUTATE=1 exit 1 | 14/14 (ledger 14) |
| 8 | `B2`, `B3`, `B4` | exit 0 | MUTATE=1 exit 1 (each) | 9/9, 9/9, 8/8 (ledger 9, 9, 8) |
| 9 | `CFG50_tidal_closure/D1_action_reciprocity.py`, `D2_wellposed_nogo.py` | exit 0 | D1: MUTATE=a exit 1, b exit 0; D2: a exit 0, b exit 1 | 6/6, 6/6 (ledger 6, 6) |
| 10 | `CFG47_unruh_matching/CFG47_unruh_matching.py` | exit 0 | MUTATE=1, 2 exit 1 | 9/9 (ledger 9) |
| 11 | `ChainCert/verify_chain.sh` | PASS, 75 theorems, 0 non-standard axioms, 0 `sorry` | MUTATE=1: FAIL, exit 1 | see note 1 |

26 script runs, 0 exit codes differ from the ledger's stated expectation.

Quoted numbers spot-checked against the re-run outputs: column bound 106.9 / 129.2 Msun/pc^2 (A3) and a0/(4 pi G) = 53.44,
a0/(2 pi G) = 106.9 (B1); kappa_match = sqrt(8 pi/3) = 2.894405 and Z = 5.788810, n = 2 -> kappa 1.4472, "measured: 12.9 sigma"
(CFG47); largest ghost-free outward force 0.505 g_tot for all four masses and the required coupling spread x64.0 (CFG50 D2).

## Two wording discrepancies (neither changes a verdict)
1. **Row 11 theorem count is stale.** The ledger (and the ChainCert README) say 52 theorems; the library now checks **75**.
   The source declares 75 (Certificates 15, PointMass 24, Profile 23, Chain 5, Fluid 5, Kernel 3), and 52 + 23 = 75: the
   difference is the Profile module added after the ledger was written (commit 15ea44952). The row was marked "not re-run".
2. **Row 4 "a0(z) flat to 6e-11 for z <= 10"** quotes the wrong quantity. A2's output gives max |dlog a0| (z <= 10) =
   1.5e-12 dex, while 5.68e-11 is the spread of Lambda_eff. The flatness claim itself reproduces (a0(z)/a0(0) = 1 to 1e-10).

## Not covered
- CFG48 and CFG49 (not in the ledger, not committed when it was written).
- Row 6's independent referee (commit 6e706019b) and the README-quoted numbers in rows not tied to a script output.
- Whether the scripts' hypotheses are physically right; only that the committed scripts reproduce their stated results and
  that each control fails as declared.

---

# Part 2 -- CFG48 (G1-G6), CFG58, CFG59 (HEAD 2415e303b)

Requested by the orchestrating session as independent duplicates of its own referee notes. Nothing in those lanes was edited.

## Method
`ledger_rerun2.py`: `git archive HEAD` of the needed directories into a scratch directory, then each script in its main mode
and with `MUTATE=1`, comparing exit codes with the lanes' own declared expectations (CFG48 referee note; CFG58 README).
**My first two exports were incomplete and raised tracebacks; those were faults in my export, not in the lanes.** CFG58/59
import `real_research/derivation_chain_2026` results, `hunt_2026` code, `real_research/data` tables and
`fable_independent_2026/L23_udg_verify.py`; once those were archived both scripts ran. (This is the same failure mode the
CFG48 referee note warns about for incomplete scratch copies.)

## Result: 16 runs, 0 differ from the stated expectations, no tracebacks
| script | main | MUTATE=1 | tally (main) |
|---|---|---|---|
| CFG48 G1_gauss_noether | exit 0 | exit 1 | 7/7 |
| G2_boundness_and_top_level | exit 0 | exit 1 | 8/8 |
| G3_history_action_causality | exit 0 | exit 1 | 2/2 |
| G4_exchange_action | exit 0 | exit 1 | 7/7 |
| G5_edge_stress_mediator_wall | exit 0 | exit 1 | 6/6 |
| G6_nonlocal_gate_stiffness | exit 1 (declared) | exit 1 | 5/9, four pre-declared H failures |
| CFG58_rule_more_populations | exit 1 (declared: control C1 failed and is kept) | exit 1 | 7/8, one load-bearing failure |
| CFG59_universal_debris_fraction | exit 0 | exit 1 | 5/5 |

- G1 exits 0, agreeing with the referee note's correction of the README (my runner initially had no reason to expect otherwise).
- CFG58's main run exits 1 by its own README's statement, and I first wrote the runner's expectation as 0 -- that was my
  error, corrected before the final run.
- Spot-checked against my own outputs: CFG58 LV field dwarfs S = -3.47 | -2.70 sigma (change 0.061 dex; -1.43 sigma in L's
  error); CFG59 "ANSWER: NO" on both footings (intersection of all ten intervals empty).

## Not covered
CFG49 (`campaign_fresh_gravity/CFG49_gate_scalar/`) is not committed at HEAD. Whether the scripts' hypotheses are right is not
tested; only reproduction and control behaviour. G-lane gate thresholds were frozen by the lane before the scripts ran (per
the referee note's file-birth-time check); I did not re-check that.

---

# Part 3 -- CFG61 to CFG67 and the new ChainCert modules (HEAD 655b3a403)

Requested by the orchestrating session; run by `ledger_rerun3.py` from a `git archive HEAD` export (broad dependency set),
main + MUTATE for each lane, exit code AND the script's own final tally compared with the tally in the lane's committed `.out`.

## Result: 14 runs, 0 differ once the git-ignored data is supplied
| lane | main exit (expected) | MUTATE exit | tally (main) | equals committed .out |
|---|---|---|---|---|
| CFG61 | 1 (1: declared H1/H2) | 1 | 12/14, 2 load-bearing failures | yes |
| CFG62 | 0 (0) | 1 | 6/6 | yes |
| CFG63 (`forecast.py`; MUTATE is the argument `MUTATE`) | 0 (0) | 1 | 11/11 (per its README) | yes |
| CFG64 | 1 (1: declared C3) | 1 | 7/9, 1 load-bearing failure | yes |
| CFG65 | 0 (0) | 1 | 7/7 | yes |
| CFG66 | 0 (0) | 1 | 3/4, 0 load-bearing failures | yes |
| CFG67 | 1 (derived from its committed tally: 1 failure) | 1 | 8/9 | yes |

## Two findings
1. **CFG61 and CFG67 do not reproduce from a clean `git archive`.** They read third-party lensing data that is git-ignored
   (`real_research/data/lensing_rar/.gitignore` excludes `brouwer2021_rar/`, `*.txt`, `*.npz`): the Brouwer+2021 Fig-8 tables and
   the generated `lr_lenses.npz`. Without them both raise `FileNotFoundError`. With the local copies (the directory is 17 GB and
   only the needed files are required) both reproduce exactly (exit codes and tallies above). This is a reproducibility note
   for the lanes' READMEs, not a fault in their results.
2. **CFG61's MUTATE control does not discriminate by exit code.** The main run already fails H1 and H2 (declared), and the
   MUTATE run (early/late swapped) fails the same two checks with the same 12/14 tally, so "MUTATE must exit 1" is satisfied
   whether or not the pipeline works. I did not check whether the swapped numbers differ; a numeric comparison of the swapped
   result against the main result would give the control teeth.

## New ChainCert modules (equations chat, this session)
`ChainCert/Gauss.lean` (CFG48's Gauss lemma: the algebra of the solution check; 7 theorems) and `ChainCert/Separation.lean`
(CFG63's separation algebra S(N), N(k), cap, no-solution case, zero floor; 7 theorems). Added append-only: two import lines in
`ChainCert.lean` and `ChainCert/Axioms.lean`, 14 `#print axioms` lines, and a README section. `verify_chain.sh`: PASS,
131 theorems checked, 0 non-standard axioms, 0 `sorry`; `MUTATE=1` FAILS (exit 1) as required. Two extra semantic mutations
(a wrong solve value `2k`, a wrong cap `Delta/(2f)`) are rejected by Lean. Certified: premises => conclusions only; no
committed number and not the Euler-Lagrange derivation (sympy in G1).

## Not covered
CFG68-70 and the calc chat's CLAIMS_AUDIT (not committed when this ran); CFG49 has its own referee note (c402c10ae).

---

# Part 4 -- CFG68 to CFG74 and the CLAIMS_AUDIT (HEAD 74c0d08f4)

## Lane re-runs: 19 runs, 0 differ (exit code, traceback or tally)
Same method as Part 3 (`ledger_rerun3.py`, `git archive HEAD`, main + every named MUTATE mode, tally compared with the lane's
committed `.out`); output in `ledger_rerun3b.out`. No git-ignored data was needed for these lanes.

| lane | main exit (expected) | MUTATE exits | tally (main) | equals committed |
|---|---|---|---|---|
| CFG68 | 1 (1: H1 failed, README) | 1 | 10/11, 1 load-bearing failure | yes |
| CFG69 | 0 (0, from its tally) | 1 | 9/9 | yes |
| CFG70 | 0 (0) | a: 1, b: 1, combined: 1 | 18/19, 0 load-bearing failures | yes |
| CFG71 | 0 (0) | 1 | 10/10 | yes |
| CFG72 | 1 (1: "rc 1 by design", README) | a: 1, b: 1, c: 1, combined: 1 | 24/27, 1 load-bearing failure | yes |
| CFG73 | 1 (1: "rc 1 by design") | 1 | 11/12 | yes |
| CFG74 | 1 (1: "rc 1 by design") | 1 | 8/11 | yes |

Note on exit codes. In CFG69, CFG73 and CFG74 the exit code of 1 is produced by the lanes' own DECLARED control failures (their
READMEs say the MUTATE gate-fail control was not met and is kept). So "exit 1" there records an undemonstrated control, not a
demonstrated one; the lanes disclose this and I reproduced it. `cfg72_stability.py` (CFG72's second script) has no committed
`.out` and was not run separately.

## CLAIMS_AUDIT_2026-09-29 (the calc chat's audit), independent mechanical check
`claims_audit_check.py` / `claims_audit_check.out`, exit 0. It checks what a script can check; the REQUIRES-CORRECTION / SOFTEN /
STILL-STANDS classes are editorial judgments and were NOT checked.
- **V1 quotes:** all **61 of 61** quotes appear verbatim at their stated file:line in the files at the audit's own commit
  (8f881c7d8). At HEAD **59 of 61** still match: the two that moved are PAPER37 lines 22 and 345, and PAPER37 was edited by four
  later commits (the "referee corrections" and "brought up to date" commits). That is drift after the audit, consistent with
  the audit's own REQUIRES-CORRECTION items being applied; the audit's line numbers for PAPER37 are now stale at HEAD.
- **V2 evidence numbers:** the numbers the audit's evidence table attributes to committed lane results were found in the cited
  lanes' committed outputs (E1 CFG55, E2 CFG61, E3 CFG67, E4 CFG59, E5 CFG58, E6 CFG66 [+0.219 / +0.465, which the audit rounds to
  +0.22 / +0.47], E7 CFG56, E11 CFG48, E13 CFG47). E8-E10, E12, E14-E16 are descriptive and were not number-matched.
- **V3 control:** an altered quote and an absent number are both rejected by the same code.

## Not covered
The editorial classifications; whether a quoted sentence is correctly characterised by its "reason" cell; E8-E10/E12/E14-E16 numbers.

---

# Part 5 -- CFG75 to CFG99 (HEAD 4fa9f54e3): five parallel verifier workers

Method: one `git archive HEAD` export (campaign_fresh_gravity, real_research, prep_2026, hunt_2026, data_assembly, opus_48,
fable_independent_2026 without lean_2026); five read-only workers, each on a disjoint lane group, each reading its lanes' READMEs
for the declared exit codes and MUTATE conventions, running main plus every control from the export, and comparing exit code and
tally with the lane's COMMITTED output (`git show HEAD:`, timing fields ignored). Workers were told never to edit the repo, never to
copy git-ignored data larger than 200 MB, and to report plainly. Their reports are in `rerun5_reports/report_A.md` ... `report_E.md`
(A: CFG75, CFG57, CFG55 helpers, CFG79-81; B: CFG76-78; C: CFG82-87; D: CFG88-91; E: CFG92-96, CFG99).

## Result: 77 runs, 0 exit-code mismatches and 0 tally mismatches in every run that had its data; 2 lanes not verifiable
Every main and MUTATE run of CFG55 helpers, CFG57, CFG75-CFG95 and CFG96 (isolation) matches its declared exit code and its
committed output line for line (CFG77's results JSON is byte-identical; others identical apart from timing). No Python traceback in
any run. **Not verified:** CFG99 (its KMOS3D cubes, 739 files / 3.8 GB, are git-ignored and outside the repo; without them the
script still exits 1 as declared but with 16/25 against the committed 22/25, which is a data absence, not a reproduction) and
`CFG96_stage_stack.py` (needs a 17.7 GB KiDS catalogue; not run; CFG95 and CFG96-isolation reproduced on copies of six small
git-ignored `.npz` files, the inputs themselves not regenerated).

## Findings (none changes a verdict)
**Portability**
1. Absolute paths. CFG76, CFG77, CFG78 and CFG82-CFG87 read their inputs from the live working-tree path
   (`/Users/carlzimmerman/.../real_research/data/...`), not from wherever the script sits. The tracked inputs made the runs valid,
   but the "clean export" read them from the live tree, and a checkout elsewhere would raise FileNotFoundError.
2. Git-ignored data. CFG77 needs `brouwer2021_rar/` (2.3 MB) and `lr_lenses.npz` (9.7 MB); CFG88 needs `lr_esd_jackknife*.npz`
   (1.4 MB) and `brouwer2021_rar/`; CFG95 / CFG96-isolation need six small `.npz` (about 26 MB); CFG96_stage_stack and CFG99 need the
   large files above. None of these is in a clean archive.

**Controls that cannot discriminate by exit code (the lanes mostly disclose this)**
3. Same exit code in main and MUTATE: CFG76 (1/1, but 2 vs 4 failures), CFG79 (1/1; declared C4 fails in both; MUTATE adds H1b, M1),
   CFG83 (1/1, identical failure set {C1e}; its injection controls carry the bite), CFG93 (1/1; 7 vs 26 failed lines), CFG94 (1/1/1;
   1 vs 17 vs 7 failed gates), CFG95 (1/1; both fail exactly H1, H2; only its exact-reproduction control C1 acts as a machinery check),
   CFG78 (0/0, both failure sets empty: the README discloses the defect but the script header still says a MUTATE exit 1 is intended),
   CFG89 (0/0/0, discriminating only by asserted PASS checks C6, C6b).
4. Exit 1 guaranteed by construction: CFG80 and CFG81's MUTATE exit through a construction detector (C5), so the code says nothing
   about the science; the headline discrimination comes from C6 (CFG80) and H1 flipping to +3.30 sigma (CFG81). CFG91's MUTATE has an
   empty failed-control set like main and exits 1 from a hard-coded condition (`cfg88.py` line 295). CFG90's MUTATE exit reads the main run's
   results JSON (main must run first) and is partly by construction, as its README says.

**Committed-output artefacts (numbers reproduce; the files are stale)**
5. CFG90 `cfg90.out` and `cfg90_MUTATE.out` contain stale duplicated blocks (8 and 12 lines) and lack the trailing exit line; all
   counts and tallies are identical to a fresh run (18/31 main, 9/31 MUTATE, controls 15/15). CFG94 `posthoc.out` has 20 lines against
   the script's 15 (a duplicated tail with a truncated first line). CFG55_h50_keyfix prints one header line the committed `.out` lacks.
   CFG91 `cfg88_post.py` / `cfg88_post2.py` have no committed `.out` (only untracked `run_post*.log`); CFG82 has no committed output
   (its `toy.log` / `feas.log` are not in git; the toy sigma(gamma) values 0.25 / 0.16 / 0.09 / 0.06 match the README, the naive-MLE table is
   unverified); CFG76's post-hoc scripts have no committed log. `FIRSTRUN_cfg93.py` and `cfg93.py` write the same filenames.

**Declared failures, reproduced as declared:** CFG76 G1 at ddof=0; CFG79 C4; CFG83 C1e; CFG84 P2; CFG93 C3b and the frozen third-decimal
R3/R5 lines; CFG94 R1 P x=0.3; CFG95 H1 and H2 (a result, not a bug).

## Not covered
Whether the scripts' physics is right; the post-hoc/exploratory scripts beyond main-only reproduction (no controls exist); CFG99 and
CFG96_stage_stack (above); anything committed after 4fa9f54e3.

## Part 5 note (2026-09-29): reconciliation with the Opus chat's in-place observations -- a wording ambiguity, no discrepancy
The orchestrator's message summarising Part 5 read my one-line list as "CFG76, 78, 79, 83, 93, 94, 95 ... both 0". My wording was
ambiguous: the parenthesis "(both 0 with empty failure sets)" belonged to CFG78 only. The exit codes as recorded in the workers'
tables (`rerun5_reports/`, exact rows) are, main / MUTATE:
| lane | main rc | MUTATE rc | checks / failing set (main; MUTATE) |
|---|---|---|---|
| CFG76 | 1 | 1 | 14 pass, 2 fail (G1 at ddof=0); 14 pass, 4 fail |
| CFG78 | 0 | 0 | FAILS: none; FAILS: none (README-disclosed defect) |
| CFG83 | 1 | 1 | FAILS: [C1e]; FAILS: [C1e] |
| CFG93 | 1 | 1 | 7 of 37 lines failed; 26 of 34 lines failed |
| CFG94 | 1 | 1 (MUTATE=1), 1 (MUTATE=2) | reproduction 16/17; 0/17; 7/17 |
| CFG89 | 0 | 0 (MUTATE=1), 0 (MUTATE=nu1) | CONTROL FAILURES: none in all three modes |
This is the same as the Opus chat's in-place observation (CFG76, 83, 93, 94 exit 1 in both modes; CFG78 and CFG89 exit 0 in both). The
environment (absolute paths, git-ignored data) did not change any exit code in these six lanes. I did not repeat the runs in the live
tree: running there would overwrite tracked `.out` files, and there is no remaining difference to explain.

---

# Part 6 -- CFG110 and CFG111 (HEAD 009d87b3a)

`ledger_rerun3.py` from a `git archive HEAD` export; output in `ledger_rerun3c.out`. Both lanes read git-ignored inputs, so the
needed small files were copied into the export from the working tree (cfg110_perlens.npz 65 MB, lr_lenses.npz 10 MB,
lr_esd_jackknife.npz 1.5 MB, brouwer2021_rar/ 2.3 MB; 76 MB in all; both READMEs list these as inputs).

| lane | main exit (expected: README) | MUTATE exit | tally (main) | equals committed .out |
|---|---|---|---|---|
| CFG110 (`CFG110_kids_mass_split.py`) | 0 (0: 12/12) | 1 (fails H1) | 12/12, 0 load-bearing failures | yes |
| CFG111 (`CFG111_sluggs_literature_gamma.py`) | 0 (0: 8/8) | 1 (fails H1 and H2) | 8/8, 0 load-bearing failures | yes |

MUTATE tallies: CFG110 11/12 (1 load-bearing failure), CFG111 6/8 (2). Both controls discriminate: main passes and MUTATE fails the
headline check(s), so the exit code carries information here (unlike CFG79/83/95 in Part 5). 0 runs differ.

Not verified: `CFG110_stage_perlens.py` (one pass of the KiDS-1000 estimator over the 17.7 GB SOM-gold catalogue, 228 s) was not run;
the per-lens file it writes was taken as an input, so CFG110's result is reproduced from that file, not regenerated from the catalogue.
`data_assembly/arxiv_tables/alpaka1_digitised/digitise.py` (a data-digitisation script, not a lane) was not run.

---

# Part 7 -- CFG112-115, the independent re-derivation lanes (CFG97, CFG100-106) and the alpha-principle lanes S1/T1/U1/U2/V1 (HEAD f44735222)

Three read-only verifier workers, one `git archive HEAD` export, same rules as Part 5 (exit code and tally compared with the lane's
committed output; git-ignored data copied only if under 200 MB; live-tree paths and controls that cannot discriminate reported).
Worker W2 and W3 could not write their report files, so their tables are summarised here from their returned text (their logs
were left in the scratch export, not committed). The machine was heavily loaded (load average 30-55), so runs were 2-5x slower than
the READMEs state.

## W1 -- CFG112, CFG113, CFG114, CFG115: 8 runs, 6 reproduce, 2 not verifiable
| lane | main (exit, tally) | MUTATE (exit, tally) | committed .out |
|---|---|---|---|
| CFG112 | 1, 7/8 | 1, 7/8 | identical |
| CFG113 | 0, 10/10 | 1, 9/10 | identical (control discriminates) |
| CFG114 | 1, 5/6 | 1, 5/6 | identical |
| CFG115 | NOT VERIFIED | NOT VERIFIED | needs git-ignored KiDS files: it stops at `KiDS_DR4_brightsample_LePhare.fits` (246 MB, over the copy limit) in the CFG110/CFG61 exec prefix before any CFG115 check runs |
CFG112 and CFG114: the control's failure set equals main's (H1, exit 1 in both), so the exit code cannot discriminate; both READMEs declare it.
No absolute live-tree paths (they use HERE/REPO). Live HEAD moved after the export: for CFG112-115 only a CFG107 corrections section was appended to `CFG115_README.md`.

## W2 -- the independent re-derivation lanes: 39 runs, 0 exit-code mismatches, 0 tally mismatches, 1 reproduction failure
CFG97 (cfg97_massive_spirals_hi main 1 with 5 PASS / 3 FAIL, MUTATE 1 with 7 PASS / 1 FAIL; cfg97_selbias_mc main 1, MUTATE 1; c3a_repair 0; the referee script 0),
CFG100 (main 0, 9/9; MUTATE 0, 3/3), CFG101 (cfg101_main main / a / b: 1 / 1 / 1, 30/32, 28/32, 26/32; cfg101_attack 0 / 1; cfg101_attack2 0 / 1; referee ceiling 0.50453),
CFG103 (A1 0 / 1 / 1; A2 0 / 1 / 1; A3 1 / 1 / 1 with its declared a4 failure; grid/A3c/A3d/referee_growth 0), CFG104 (0 / 1),
CFG105 (aniso 0 / 1 / 1; posthoc 0), CFG106 (0 / 1): every exit code equals its README/committed declaration and every tally equals the committed `.out`.
1. **Reproduction failure: `posthoc_shape_weighting.py` (CFG97) crashes from a plain run** (`NameError: __file__`): it `exec()`s the
   main script, whose line 58 was edited after the runs to use `__file__`. With `ZF_REPO` set it exits 0 and matches; the README instruction
   and the committed output are stale.
2. `cfg97_selbias_mc.py` timed out at 1500 s under load on both runs, then finished in about 1200 s and matched the committed results JSON exactly.
3. Controls that cannot discriminate by exit code: CFG97's MUTATE exit 1 comes only from the C3a numerical fault, which also fails in main; in
   CFG101 main and CFG103 A3 all modes exit 1 (mutant failure sets are supersets, so only the tally discriminates); CFG100's MUTATE exits 0 like main (K9 is a passing control).
4. Declared "failed and kept" controls reproduce: CFG97 C2, C3a, C5 and MC M3; CFG101 P1 ceiling (0.5008 against 0.505) and P2 option B; CFG103 A3 a4.
5. CFG100 needs three git-ignored files (`lr_lenses.npz` 10 MB, `lr_esd_jackknife.npz` 1.5 MB, `cfg110_perlens.npz` 65 MB); with them the results were identical.
6. Cosmetic: the CFG105 `.out` embeds the repo directory name and the committed copy has an extra trailing FAILED CHECKS line; the CFG105 README says "10 checks" and the run shows 13 PASS lines.

## W3 -- alpha-principle lanes S1, T1, U1, U2, V1: 30 main runs (15 scripts x real and --mutate), 0 exit-code mismatches, 0 tracebacks
Every output byte-identical to the committed `.out` except one trailing line (finding 5). Also run: 2 clean-export `u1_9` runs, 2 V1 `--candidate` runs and 4 harness invocations
(`--only T1_`, `U2_`, `V1_`, `u1_lib`); the full harness (112 scripts, hours) was not run.
1. **Clean-export failure (a real defect):** `u1_9_graveyard.py` needs `u1_1/2/3_results.json`; none of the 8 U1 json files is committed. From a clean HEAD export `u1_9` exits 1
   (FileNotFoundError) and its `--mutate` exits 1 for the wrong reason. After `u1_1..3` have run, `u1_9` matches the committed output and the regenerated jsons equal the live-tree ones.
2. `RUN_ALL_RESULTS.md/json` are stale: they list 97 scripts with no S1/U1/U2/V1 rows; the runner now enumerates 112.
3. The harness would flag a problem at HEAD: `u1_lib.py` is not in `SKIP_FILES`, so it reports "UNDETECTED convention" and exits 1 (`--only u1_lib`); and it runs scripts in an unordered thread pool, so `u1_9` races `u1_1..3`.
4. Control power: T1 and V1 count any failed check as "control works", not the named one (only B1 fails in both); V1 B1 is a tautology in the real run; U2's control-broken exit is 0, not 3 (the runner still catches it).
5. The committed `s1_3_modesum_validation.out` has a trailing "exit 0" line that a fresh run does not write.
6. S1's final scripts enforce the re-registered checks (E1-E7, C1-C4), not the registered D1-D7; E1, E3, E5 thresholds were set post hoc (disclosed in the lane's amendments).
7. V1: the digit-count criterion is not computed; A2 checks only the relative spread; a bare decimal `--candidate` becomes a float (offset 3.75e-7 sigma instead of 0). T1's status text says "1e81 or more" but its electron shortfall at H0 is 9.79e80.
No live-tree paths or git-ignored data in these lanes.

## Not covered
CFG115 (data over the copy limit); the full alpha harness run; scripts' physics.
