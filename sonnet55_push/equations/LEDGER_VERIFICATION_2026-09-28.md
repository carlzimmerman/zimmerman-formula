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
