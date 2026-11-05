# astra goal, 2026-11-05: run every lane handed over on 2026-11-04, rigorously, to a verdict

Written at the owner's request for an unattended astra run: "do it rigorously and run all the computations". This file is the brief. It is not a result, and nothing in it says the data favour the framework. κ = ½ FITTED. Not theory closed.

**The job:** take every lane in `ASTRA_HANDOFF_2026-11-04_INDEX.md` (19 lanes plus three owner-gated items) and drive each one to a labelled verdict with committed, rerunnable computations. A lane is done when it has frozen criteria, a script, its outputs, a MUTATE twin that bites, a known-answer check, and a README that leads with its label. "Read the brief and summarised it" is not done.

**Owner's go for this run:**
- It covers the mechanism lanes 6 and 7 (a0/κ from the action; a covariant source for FN6's window), which the briefs marked as needing a go.
- It covers lane 19, the C'' disc-fold variant (axisymmetric run, 40-80 CPU h), **only** through `compute_queue/heavyq.py`, preemptible, after the light lanes are done.
- The MW/DiskMass vertical-force choice is made: **explore both forms, A and R, and pick neither** (lane 3).
- v3s stays adopted, scoped (7ac515f958). The cold sector stays retired. A result here is a candidate or a verdict; only the owner adopts anything.

## Read first, in this order
1. `ASTRA_HANDOFF_2026-11-04_INDEX.md`: the lane list, the corrections that win over older briefs, dated events, rules.
2. The five source briefs it names (M, F, B, C, S). Each lane below says which section holds its full spec.
3. `finish_2026_11_04/FN1_action_call/OWNER_DECISION_2026-11-04_ADOPT_V3S_SCOPED.md` and the last STANDING.md addendum.
4. `FAILURES_EXECUTIVE_SUMMARY_2026-09-28.md` section F, and `complete_theory_2026_11_04/CT14_Cpp_health/README.md` (C'' fails G0).
5. `git log --oneline -120` and `ls` of every folder a lane touches. Other sessions write in parallel; check nobody has already started a lane before you do.

## Where to write, and lane ids
- All new work goes in `astra_goal_2026_11_05/<LANE_ID>_<short_name>/`. Don't edit other lanes' folders (LW1, V3X, FN*, CT*, CQ*, BK2, W1's frozen files). A lane that extends one gets a new folder and cites it.
- Ids: continue your `AZ` prefix from the next free number (AZ30 is the highest on record at writing). Check `git log --all` and `ls` for the number before using it.
- Exception: the status board lives in `explainers/make_status_board.py` and its md/png. Lane 3 edits those, following the board's own guards.

## Order of work
Run lanes in this order. Within a tier, run independent light lanes back to back; don't start heavy compute until tiers 1-3 are labelled.

### Tier 1: weak spots in the adopted action (small; do these first)
1. **V3X W2.** New lane: K1 graded only at the graded radius, tolerance stated before running, both footings. Never amend V3X. (M A1)
2. **V3X W4c(b).** Find and cite a source for the tensor line (1e-10 or another) **before** rerunning; run the l = 1-4 spectral ladder at ≥ 24 cells per decade with a convergence pair. (M A1)
3. **Status board: LW1 fold, both vertical-force forms, PAPER67 footer.** (B, section B1)
   - Fold LW1's K, X, Dw, DM lines per B1's table (X-COP FAIL both, keys 10 of 15, dwarfs worse with E1's field).
   - MW and DiskMass: grade forms A and R separately, both footings. Start from LW1: MW form A FAIL INFEASIBLE, form R PASS on 1/6 cells with K_z scale length off by +3.9 to +4.4σ; DiskMass form A NO LABEL (r 1.477), form R FAIL (r 1.239 / 1.204). If either form needs runs beyond LW1, that is its own AZ lane with frozen criteria. State where the forms disagree and why.
   - Each tile shows both forms. New selftests that must be caught: X-COP back to grey; an LW1 FAIL coloured PASS; a tile that drops either form.
   - Footer: PAPER67 v1.2 is deposited (DOI 10.5281/zenodo.23968171); the board still says v1.1 (`make_status_board.py:638`, md line 29).
   - Keep `MUST_STAY_RED` and the column-0 guards. `--selftest` must pass, `--mutate` must exit 1. Save the pre-fold image as `status_board_2026-11-04v3s.png`.
4. **Regrade the six carried relativity tiles on v3s with the switch on.** Binary pulsars (C8's 3.2e-14), strong-coupling loop factor (P3's 1.3e-3 at Eot-Wash, L* 90 pc), static black-hole shifts (P3's ≤ 2.9e-11), plus leaf, causality and G9. MUTATE = switch inverted. Use CQ7's L* window (21.68-27.00 pc canonical, 22.85-24.60 pc alt) where L* enters, and report the edges as well as a central value. Don't cite X15/X16. A tile changes colour only on this lane's result. (B, section B2)

### Tier 2: what v3s still asserts, and the action questions
5. **v3s's asserted items, one lane each:** (a) nonlinear well-posedness; (b) the PN-order sign of corrections; (c) the Sun moving in the khronon frame (moving-source check, model on AS3's α1 branch); (d) a realistic solar interior instead of uniform density; (e) constraint causality, given that C5's cone criterion fails. Each states up front what would count as a proof, a counterexample, or NO VERDICT. (M A2)
6. **a0 and κ from the action.** Read `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CLOSURE_2026-11-03.md` and its reopen conditions first; a route that doesn't meet one is not started. Main question after CT14: is there a coupling that keeps C'''s rest-frame tie stable **with the khronon velocity in the perturbations**, or a proof that none exists in v3s + a canonical φ? Then: does any term fix ξ (κ² = ξ) rather than leave it free? Rerun CT14's static weak-field check on every candidate as gate G0. (M A3, C lanes 1-2)
7. **A covariant source for FN6's window.** L ∝ M^p with p 0.30-0.45 passes the five static gates. Find a mechanism whose screening radius scales that way (a Vainshtein radius goes as M^(1/3); treat that as a lead, not a result). For each candidate: derive L(M) from its own equations, not FN6's Gaussian stand-in; rerun FN6's five gates with FN6's engines; check C6P's Q2 margin and c_T = c. A candidate that needs p fitted is FITTED. (M A4, F 1)
8. **C'' a0(z) pre-registration.** Only if lane 6 finds a healthy tie: freeze its a0(z) = κ c √(Gρ_φ(z)) against the AT1 rule as a sealed prediction. Otherwise write one paragraph saying the prediction has no healthy carrier, and stop. (C lane 3)

### Tier 3: data already on disk
9. **FN6 canonical robustness.** Finer cell grid around the one passing MW cell (mass 7.65e10, L 1.61-1.65 kpc), and a p, L_MW grid between 0.25 and 0.5, both footings. Does the canonical window survive, shrink to nothing, or widen? Grid spacing is set before running; it is a robustness check, not a search for a pass. (F 2)
10. **FN4e HI-selected lens stack, stage 0.** Power forecast on ALFALFA, FASHI, KiDS-1000 shear (17.7 GB, read in chunks; FN4c hit 25 GB) and DESI BGS, under criteria c03a803b3b. Report what S/N a stack reaches and whether it can separate the law from the measured gap. (F 3)
11. **a0(z) S/N forecast.** K2''-style synthetic scan over S/N and sample size on `finish_2026_11_04/FN3_musedark_law_refit/fn3_cube.py`: what does a future IFU sample need to separate the flat band from the rise? Recompute MUTATE lines from the lane's own levers (FN3b's was copied). (F 4)
12. **IC 1613 cube redo.** Data in `_external_data/fn4a_ic1613_2026_11/`. First find why the cube's HI mass is 0.716 of Oh+15's and the drift-corrected velocity is 20.85 vs 16.9 km/s (masking, primary beam, drift form); then freeze a new lane, e.g. against LITTLE THINGS's published fluxes. The record's FAIL stays whatever you find; a new lane adds a row. (F 5)
13. **BK2 G3.** Measure cluster-to-cluster scatter from data on disk, freeze it, then regrade in a new lane. Never widen BK2. (M A8)
14. **FA1 leftovers.** SLACS rotation class per lens (I2); the 15 shear keys at selector level for I1 and I2; I6's Bullet in a 3D nonlinear solve (heavy: queue it). Record-completion only; all three are already killed elsewhere. (M A6)

### Tier 4: your own runs
15. **W1.** Run the canonical 128³ A4 reruns (`W1_pmedium_3d_scaleup/ENQUEUE_A4_commands.txt`) through the queue, then the convergence and binding verdicts on both footings. Alt's strong-seed peak already converged (ac0e22f6e1).
16. **X1.** Finish the final analysis; state the abundance verdict and the isocurvature failure in the README.

### Tier 5: hard walls, test lanes only (adopt nothing)
17. **Clusters.** Requirement sheet: FAILURES section F plus FA1's README; closed selectors are listed in M A5. Don't repeat any of them. A new route has to state a principle outside baryon geometry and kinematics, with its radial shape (X-COP's need falls as x^-0.33), before it sees the 15 keys, X-COP or the Bullet.
18. **Held/free switch and cold abundance origin.** These concern the cold sector retired on 11-01. A test lane may reopen it under the owner's rule, but every README must say "retired sector, adopts nothing". (S 1, S 3)
19. **C'' disc-fold variant.** C'' plus X14's β K² term (β 2e-6 to 1e-5), axisymmetric (R, z), with a convergence pair, through the queue only. Since C'' fails G0 (CT14), first check whether the β K² term changes that; if it doesn't, record that and skip the run. (C lane 4)

### Not to run: put these in NEEDS_OWNER.md
- a0(z) proposal sample (M A7): proposal work, not computation.
- MW thick share (F 6): needs APOGEE's selection function.
- FN4d Local Group star counts (F 7): needs PHATTER and VizieR downloads.
- Anything else that needs a download, a deposit or sending.

## Dated events during the run
- **2026-11-06 03:15 UTC, ALMA U4_28473.** The scheduled task `alma-release-scoring-2026-11-06` runs `finish_2026_11_04/FN2_dated_tests/fn2_release_day.sh --run`. If its outputs aren't there by 06:00 UTC, run it by hand under `FN2_dated_tests/OWNER_APPROVAL_2026-11-04_ALMA.md`, then runbook step 9. Grade only against the frozen seals.
- **GS4 (11-28) and Gaia DR4 (~12-02)** are owner-triggered. Don't run them; never edit the seals or `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`.

## How to work (standing rules; breaking one voids a result)
1. **Raw data and framework-native inputs only.** No ΛCDM background or Planck-derived numbers, no "passes by construction". No dark-matter particle; say "cold dark energy".
2. **Freeze first.** `FROZEN_CRITERIA.md` committed alone, before any script that produces a graded number: hypothesis, data, gates, pass/fail lines, tolerances from stated measurement or numerical errors. Later changes go in a dated `AMENDMENTS.md`, marked post-result if they are. Never widen a tolerance after seeing a number.
3. **Two footings, never pooled:** canonical a0 9.3603e-11, alt 1.1312e-10 m/s².
4. **Controls in every lane:** a known-answer check, and a MUTATE twin that writes to separate outputs and must bite. Read margins from the JSON output, not from prose.
5. **Derive, don't scan.** A grid is allowed for robustness or a stated bracket, never to hunt a passing value. Every free number is labelled FITTED.
6. **Numerics:** a convergence pair (or ladder with Richardson) for every graded PDE or N-body number; state the change between steps against the frozen line.
7. **Verify a fail as hard as a pass.** Labels: PASS / FAIL / WINDOW / NO VERDICT / NOT EVALUABLE / UNDECIDED. "Survives these gates" for partial passes. Every result carries "κ = ½ FITTED; not theory closed".
8. **Compute limits.** Light jobs: 1 thread (`OMP_NUM_THREADS=1`), under ~1 GB RSS, minutes. Anything heavier goes through `compute_queue/heavyq.py` per `compute_queue/JOB_CONTRACT.md`: checkpoint on SIGTERM, resume. Check `ps` for a live 1024³ run first. The queue is held by L1 jobs; don't delete their checkpoints.
9. **Git.** Commit as you go, with explicit paths only (`git commit -m ... -- <paths>`): several sessions share one index. Report your own commit hash. No home paths, personal names or tokens in committed files; run the usual leak check on the added lines first. Don't push, and never rewrite history.
10. **Converge.** After about six lanes on one hard-wall problem with no new survivor, write its STATUS and move on. Tiers 1-4 are run to their labels regardless.
11. **Stop and leave a note, don't act,** for downloads, Zenodo deposits, emails or posts, pushes, or anything that edits a deposited paper. Put it in `astra_goal_2026_11_05/NEEDS_OWNER.md` and carry on with another lane.

## What done looks like
- One folder per lane, each with frozen criteria, script, outputs, MUTATE, known-answer check, and a README that leads with its label and lists its failed checks.
- The status board rebuilt with LW1 folded, both forms on MW and DiskMass, the six carried tiles regraded or marked as still carried with the reason, `--selftest` passing and `--mutate` exiting 1.
- `astra_goal_2026_11_05/SUMMARY.md`: one row per lane 1-19 with label, both footings, commit, every free number, and the exact next calculation. A section on what changes for v3s's scoped adoption: which weak spots closed, which opened.
- `astra_goal_2026_11_05/NEEDS_OWNER.md`: every decision, download or deposit the run needs, each with name, source, size and why.

κ = ½ FITTED; not theory closed.
