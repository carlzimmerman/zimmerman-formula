# astra goal, 2026-11-03: the hardest open problems, open for new routes

Written at the owner's request for an unattended astra run. The owner wants astra to look for **new paths to closure** on the walls below, on its own. This file is the brief. It is not a result, and nothing in it says the data favour the framework. κ = ½ FITTED. Not theory closed.

**Owner's go for this run:** the stop on new mechanism lanes (OWNER_DECISION_2026-11-01_T_ONLY.md) is lifted **for astra's lanes under this goal only**. The cold sector stays retired (OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md). A result here can be reported as a candidate; only the owner can adopt it.

## Where things stand (read these first)
- `rebuild_2026_10_22/REQUIREMENTS_2026-11-01/REQUIREMENTS_LIST.md`: the twelve rows any working rule must hold, where they collide, and every combination already tried. **Start here.**
- `rebuild_2026_10_22/RQ3_acceptance_v2/REQUIREMENTS_V2.md`: the 96-row acceptance sheet used to reject rules.
- `rebuild_2026_10_22/CLOSING_LEDGER_2026-11-01_DRAFT.md`: what closed and why.
- PAPER67 (DOI 10.5281/zenodo.23883741): the a0 law and its failure record, the current flagship.
- `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CLOSURE_2026-11-03.md`: the κ closure.
- `git log --oneline -80`: the 11-02 and 11-03 lanes (KT14–KT28, NP1/NP2, MB1, HX1, DB1, AN1/AN2, LAM1–LAM3, KU1/KU2, KC1).

**The law holds:** SPARC tightness (rms 0.054), flatness with surface brightness, LITTLE THINGS median, most of isolated-lens shape, and κ universal between slow and fast rotators (KU2). **Nothing on record holds:** IC 1613, the Milky Way, outer cluster shear, an action, and (without the retired cold sector) the CMB.

## The problems, hardest first

### P1. Clusters: Bullet, X-COP and the 15 keys at once
Every attempt splits the same way: mass placed on the galaxies passes the Bullet and fails the keys; mass placed on the gas does the reverse (MB1, DB1, BK2, FG1). X-COP needs a boost B ≈ 3.7–4.1 that **falls with radius as x^-0.33** (HX1), so no per-system scalar boost works. MaNGA ellipticals at σ 170–260 need the same B as X-COP, while groups need only 1.1–1.5, so no σ or T ladder exists (HX1). Outer shear rises with gas mass near Newton's slope (0.47 law vs 0.90 ± 0.21 measured), and no rule reproduces it on measured gas (requirement row 10).
**Closed, don't repeat:** per-member phantom halos (MB1), σ/T-keyed scalar boosts (HX1, TX1), Milgrom's CBDM and cold clouds (DB1; only 1e2–1e7 M☉ black holes survive, with no origin), `max(law, halo)` (X56), mass switch (X58), basin split / T (TD1).
**Open question:** what radial, gas-tracking extra pull is absent in isolated discs, present in cluster outskirts in proportion to gas, and still leaves the Bullet's lens peak on its galaxies? A rule must state its shape before it sees the keys.

### P2. A local filter rule for the phantom field (MW + dwarfs + Cassini + SPARC, both footings)
The live lead of 11-03. Filtered QUMOND with filter length ξ = ε √(G M_b / a0): ε ≈ 0.55 passes MW, 24 dwarfs and Cassini (KT17); ε = κ = ½ (ξ = r_M/2) passes all four on **canonical only** (KT25), alt fails Cassini 1.06×. But "system mass" isn't local. The local forms fail: ξ_loc = g²/(|∇g| g*) loses Fornax because the MW's external field flattens |g| (KT26, KT27); the tidal-tensor form ξ_tid is frozen in KT28 with no result yet and is at risk on MW and Cassini. The MW pass also needs a thick-disc share ≥ 0.20–0.26 against star counts 0.11–0.12 (KT18, KT22); the APOGEE chemical share 0.26 is a provisional lookup.
**Open question:** a field-local, equivalence-principle-respecting definition of ξ (from an action if possible) that reduces to r_M/2 for an isolated point mass, survives the MW external field on Fornax, and passes on both footings. Check KT28's state first; don't duplicate it.

### P3. Derive κ = ½ (equivalently: a length exactly c/√(Gρ))
KC1 closed this as "no derivation, no deciding measurement": 840 rows, 550 derivation attempts, every route reduces to ξ = 1, i.e. a length exactly c/√(Gρ) with G (not 8πG), which no field equation on record supplies (KF1, KT2/KT3, CFG891, CFG911, doors D1–D5). Measurement can't separate ½ from 0.461 (needs a0 to 2.8 %, floor ~5 %).
**Open question:** a field equation or action whose natural length is c/√(Gρ_DE) with coefficient exactly 1. Reopen only with a route that supplies that, per KC1's reopen conditions. Note KT26's exact identity ξ = V∞²/g*, g* = c√(Gρ) = a0/κ: P2 and P3 may be the same problem.

### P4. One field: dust on FRW, the a0 law in galaxies, and nonlinear wells
The one action lane the owner opened on 11-02 (OWNER_DECISION_2026-11-02_ONE_ACTION_LANE.md). AeST-class already tested in C1, C2, C7, H1, H2, S4, M1, UX1, UX2, AS2, AS3. What's uncomputed: the field in nonlinear wells beyond the hydrostatic branch. AN1 v3 and AN2 are NO VERDICT: 3D shapes fold 8–19 % before the engine's own sphere, but the sphere lags AN1's 1D reference by 16–18 % with cause not separated, and AN2's well test fires trivially at 1e15 (needs a criteria change). The central collision (requirement rows 4 and 11): whatever acts as dust in the CMB falls into galaxies, and live discs measure almost no contraction (f_Q 0.872).
**Open question:** a process that is dust at the CMB yet doesn't contract spirals, at one coupling. ER1, PG1, DR9 failed.

### P5. The Milky Way and IC 1613
The law overshoots the MW (K_z +4.7 to +6.6σ too high; 0 of 625 cells, OS1). Eight QUMOND kernels that reach the MW v_c all land K 75.0–76.3 vs 70.8 (KT13): the miss is set by baryons, not kernel shape. IC 1613 sits at E −0.593 under every rule; NP1/NP2's admissible nonparametric rules pass gates 1–5 and still fail RQ3 on IC 1613, the Υ rows and dwarfs A5–A13.
**Open question:** a selector that separates same-mass systems by something other than potential, σ, acceleration, environment, epoch, gas state, bars or surface brightness (all closed on the inputs tested).

### P6. Galaxy lensing short by ~0.09 dex
LE1: estimators disagree with no defect; the law is short ~0.09 dex in KiDS galaxy lensing under every grader. Blue vs red amplitude 0.88 vs 1.31 (BL1). Any P1–P5 rule must not widen this.

## How to work (standing rules; breaking one voids a result)
1. **Raw data and framework-native inputs only.** No ΛCDM background, no Planck-derived numbers, no "passes by construction". Data already on disk (`_external_data/`, lane folders) first.
2. **No dark matter particle.** The cold component, where it appears, is "cold dark energy", a gravitating field component, never "cold dark matter". No new particle species (HF1 was the only exception and is closed).
3. **Freeze criteria first.** Each lane gets its own folder and a `CRITERIA.md` committed **before** any script that produces a graded number: hypothesis, data, gates, pass/fail lines, tolerances taken from real measurement errors. Post-hoc changes go in a dated `AMENDMENTS.md`, marked post-result if they are.
4. **Derive, don't scan.** No knob scans to find a passing value; a free number counts as fitted and is stated as fitted. Derive the observable from the action where an action exists.
5. **Verify a fail as hard as a win.** Both footings (canonical and alt). Every lane carries a MUTATE control that must bite and a known-answer control. Report margins read from the JSON output.
6. **Report honestly.** Use PASS / FAIL / NO VERDICT / NOT EVALUABLE. Keep "κ = ½ FITTED" and "not theory closed" on every result. Never say the data favour the framework. A pass on part of the sheet is "survives these gates", not a pass of the theory.
7. **Check the record before starting a lane.** `ls` + `git log` + grep for the idea; if it's been run, cite the lane and move on. Lane IDs: use the prefix `AG` (AG1, AG2, …); check no `AG*` folder exists first.
8. **Compute limits.** Heavy jobs must checkpoint on SIGTERM and resume via `compute_queue/`. Don't run heavy jobs while a 1024³ run is live (check `ps`). Keep RSS under a few GB unless the job is queued.
9. **Don't touch:** the Gaia DR4 pre-registration, other sessions' lane folders, deposited papers, `THEORY_CANONICAL`, STANDING files. Write only in `astra_goal_2026_11_03/`.
10. **Stop and leave a note instead of:** downloading new external data, depositing on Zenodo, emailing or posting anything, pushing to the remote, rewriting git history. Put each such need in `astra_goal_2026_11_03/NEEDS_OWNER.md` and move to another problem. Commit locally as you go; no user's personal name or home paths in committed files.
11. **Converge.** After about six lanes on one problem with no new survivor, write a short status for that problem and move to the next.

## What done looks like
For each problem P1–P6 you touch, `astra_goal_2026_11_03/P<n>/STATUS.md`: routes tried (with lane IDs), what each did on the gates, any rule that survives more of the sheet than the record's best, and the exact next calculation. A top-level `astra_goal_2026_11_03/SUMMARY.md` ranks any candidate by how many of the twelve requirement rows and the RQ3 rows it holds on **both** footings, with every free number listed.

A real advance is a rule, derived rather than fitted where possible, that holds a requirement row nothing on record holds (6, 7, 10, 12) without losing rows 1, 2, 5 or 8.
