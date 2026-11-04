# CW3_cz1_defect_sweep: ONE LABEL FLIPS (KT30 canonical, dwarfs), three graded lanes move but hold, and the DR4 pipeline and banked target are correct

κ = ½ FITTED; not theory closed. This is a correctness audit, not a physics verdict. Footings are never pooled. No cold component, no particle. Nothing here says the data favour the framework.

Criteria: `FROZEN_CRITERIA.md` (3ca990f6d6), committed alone before any sweep output. Departures are in `AMENDMENTS.md` (A1 to A6), each written before use. The full table is `CW3_TABLE.md`.

## The defect, in one line
In QUMOND, ν takes the Newtonian field, so the host's external field there must be Newtonian. The defect (DEFECT-Q) is an observed or MOND field in that slot. Its mirror image (DEFECT-A) is a Newtonian field at AQUAL's boundary.

## How to run
All commands run from this folder with `OMP_NUM_THREADS=1 nice -n 10 python3 -I <script>`.
- `cw3_triage.py` runs the frozen grep and the ν/μ filter, and reads every ν/μ call. It writes `cw3_grep_hits.txt`, `cw3_triage.json` and `cw3_triage.out`.
- `cw3_taint.py` runs the A6 trace on the literal-only rows and writes `cw3_taint.*`.
- `cw3_table.py` writes `CW3_TABLE.md`.
- The reruns are copies of the original scripts. The originals are not edited. In each copy only the external field changes. Set `CW3_FIELD=orig` (K1) or `CW3_FIELD=newton` (corrected), and `CW3_MUTATE=1` for the ν ≡ 1 twin:
  - `h8_cw3.py`: hunt item 8, the 09-03 Local Group dwarfs. Seconds.
  - `cfg478_cw3.py` and `cm14b_cw3.py`: the cluster satellites. Under 1 s each, 0.12 GB.
  - `kt30_cw3.py`: KT30's Cassini, dwarf and SPARC rows. About 5 min and 0.21 GB per run (`*.time`).

## Summary of the table
- **Audited.** The frozen grep finds 3,274 tracked files. Of these, 1,731 call ν or μ or a named interpolating function (A2).
- **Flagged and read by hand: 295 files.** The triage flagged these: a ν call carrying an external-field name, a μ call carrying one, or an observed literal that reaches a ν argument.
- **Machine triage: 1,423 files**, labelled CORRECT. No ν/μ argument in them carries an external-field name, and no observed literal reaches one (A3, A6). Most of these grep hits are incidental, for example `GE` used for Newton's constant or "EFE" in a string.
- **Labels on the hand-audited rows, counted by file:**
  - DEFECT-Q: 51
  - AMBIGUOUS: 12
  - FIXED: 10 (KT15 to KT28, and the IC 1613 lever)
  - CORRECT: 35 in the named-lane and record rows, plus 217 more of the flagged files
  - DEFECT-A: 0. Every AQUAL row sets its boundary to an observed total, or builds the total from a Newtonian value first.
- **Most DEFECT-Q rows are priority 3.** They are exploratory wide-binary, solar-system and modified-inertia scripts. Most put the Galactic V²/R, 1.8e-10 or 1.778e-10 into the framework's ν. None of them sits behind a requirement row, the closing ledger or PAPER67.
- **The current record carries no DEFECT-Q.** That covers REQUIREMENTS rows 5 to 7, FG1's Dw cell, LW1, X1, Z2, UX4, D10, and E2 (PAPER67's Solar System line). Their AQUAL solves take the MOND field of the host's baryons, which is correct for AQUAL. Their QUMOND rows invert the field first.

## FLIPS and MOVES (reruns; K1 and MUTATE passed for each)
| lane | label before → after | numbers before → after | class |
|---|---|---|---|
| **KT30** trace-free tidal rule, canonical | T1-T3 "FAILS: dwarfs, SPARC" → "FAILS: SPARC" | dwarfs 13 → 15/24 (the line is 15; plain 18); Fornax 8.3 → 10.4 km/s; Cassini 0.090 → 0.167× ceiling, PASS | **FLIPS** |
| KT30, alt | "T1-T3 PASS" holds | dwarfs 15 → 17/24; Fornax 8.7 → 11.0 km/s; Cassini 0.169 → 0.35×, PASS | MOVES |
| hunt item 8, 09-03 Local Group dwarfs | "item 8 does not close" holds | MW +0.641 → +0.372 dex (alt +0.632 → +0.352); M31 +0.294 → +0.106 (alt +0.284 → +0.086); all 46 +0.363 → +0.284; centring Υ_V 23.8 → 11.1 (alt 22.4 → 9.9) | MOVES |
| hunt item 42, DF2 and DF4 | check 42 holds | simple-EFE σ: DF2 14.9 → 22.5 km/s, DF4 16.6 → 25.2 (canonical) | MOVES |
| CFG478, cluster satellites, exact QUMOND | FORCE+EFE EXCLUDED (robust) holds | χ²/5: Q1 94.6-106.9 → 70.7-92.7; Q2 78.4-92.3 → 53.2-74.9; Q3 61.0-74.5 → 36.6-55.8. Boost Q1 1.4-1.8 → 1.6-2.6, against 10-20 needed. Largest p 7e-7 | MOVES |
| cm14b, reading B (CFG447 cites its 99.7) | EXCLUDED holds | χ²/5 99.7 → 83.9; mean offset +0.81 → +0.74 dex | MOVES |

- **KT30 still fails overall.** Its Milky Way arm carries no external field and fails on both footings. Canonical now fails on MW and SPARC only.
- **KT30's corrected dwarf count sits exactly on the line.** It is 15/24 against plain QUMOND's 18, so a strict ≥ plain test would fail, as CZ2 found for LOC.
- **The FLIPS row is a reading, not a re-grade.** It needs its own frozen re-grade before anyone cites it, as CZ1 needed CZ2.
- **The source of item 8's numbers was not updated.** `hunt_2026/WHAT_THE_HUNT_TAUGHT.md:93-94` still cites the old ones. The hunt had already found the slot error elsewhere: `h43`, `h93` and `u02` flag it, and `g05` fixes it in `f09`. Item 8's own row and the synthesis line were never redone. That file is outside this folder, so it is left as is.
- **A geometry issue in item 8 is left unchanged.** It uses McConnachie's heliocentric D as the distance to M31 for M31's satellites. Only the external field was changed.
- **The cluster rows have no host baryon model.** Their corrected field is the measured NFW field inverted through each kernel's ν (A4). Clusters keep the law's mass deficit, so the baryon-only field would be smaller still. Even at a quarter of the corrected field the boost stays 2-8× short of what the lensing masses need.

## DEFECT rows not rerun, and why (details in the table)
- **KT20 and KT21** are recomputed in lane CW1 (`cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4`).
- **KT29.** The defect is in the dwarf and Cassini rows it carries beside its MW arm. Its frozen label comes from the MW cells, which carry no external field, so it is UNCHANGED.
- **Corrected elsewhere on record.**
  - hunt h9, the Coma UDGs: u02 regraded it with the kernel-inverted field. The offset goes from +1.195 to +1.083 with the flux theorem, or +0.942 with the baryon field, and the kill still fires.
  - hunt f09 was fixed by g05: −0.418 dex.
- **CFG331 R-efe cannot flip.** In this 1D form a host field only lowers the boost, so the corrected offset lies between the K0 +0.224 and +0.295.
- **hunt h47, item 47e (a reading, not a rerun).** With the Newtonian field the LMC–SMC EFE speed rises from 46 to about 68 km/s. That is still below the isolated 75 and the observed 128, so the statement holds.
- **The other priority-3 rows** (wide-binary, solar-system, modified-inertia, fable SW-series, cluster EFE channel) are not cited by the current record. Most are superseded by the DR4 banked target, which inverts the field.

## DR4 pre-registration (read only; nothing in `prep_2026/gaia_dr4_prep/` edited, run or rehashed)
- **The frozen pipeline is CORRECT.**
  - `wide_binary_pipeline.py:186-191` inverts g_ext,obs = 1.9 a0 to a Newtonian y_extN before it enters the transition shape (`:193-201`, `:281-283`).
  - The anisotropy eigenvalues it carries are Route A's, taken at the inverted y_extN 1.28903.
- **The banked target `real_research/reviews/wb_dr4_prereg_framework_curve.py` is CORRECT.** Both its MG and MI forms use y_ext,N = 1.4647 (`:60-98`).
- **Arm A in force (Amendment 10, `aqual_efe_full_solve_2026.py`) is CORRECT.** AQUAL gets the total field and QUMOND the inverted one.
- **No `OBSERVATION_DR4` file is written.** The frozen trigger (DEFECT-Q in the frozen pipeline or the banked target) does not fire.
- **Two superseded amendment computations do carry the observed field in ν:**
  - Amendment 1's gated row and cubic rise (`real_research/reviews/mi_wb_gate_fork_2026.py:90-102`, `mi_wb_cubic_rise_2026.py:48`) apply the framework ν to V²/R. They are labelled DEFECT-Q, MI-named (A5). Amendment 6 withdrew Amendment 1's basis.
  - Amendment 2 (`prep_2026/gaia_dr4_prep/amendment2_derived_efe.py:50-77`) evaluates its eigenvalues at the observed 1.778e-10 and 2.078e-10. It is AMBIGUOUS, because its text makes the closure's argument the total four-acceleration. Amendment 8's Route A values, at the inverted field, replaced it.

## AMBIGUOUS rows that matter
- **DR4 Amendment 2, and the hunt k03 and kernel-shape items that reuse its construction.** As read, ν(observed) gives γ_perp² = ν(1.9) = 1.235. The record's own inverted reading gives ν(1.4647) = 1.297. These are superseded or exploratory.
- **The modified-inertia reading (A5).** The frozen criteria put modified inertia under NOT-QUMOND. Scripts that apply the record's ν, which is declared on g_bar, to an observed field are labelled DEFECT-Q here, marked MI-named. If an owner reads those scripts as kinematic-variable forms, 14 files move from DEFECT-Q to AMBIGUOUS. No verdict on record depends on them.
- **Field passed in but not set in the file** (5 files) and **DE02's generic η**. These have no record dependence.

## Checks
- **K1.** Each copy run with the original field reproduces the committed output. For h8, cm14b, CFG478 and KT30 the text is identical apart from the `[CW3]` header line (and the runner's trailing `rc=0` for h8).
- **K2, KT30 corrected run.** Its constant-rule references switch to CZ1/CZ2's corrected values, and they reproduce exactly: Cassini 1.179 / 2.97, dwarfs 18/24.
- **MUTATE (ν ≡ 1).**
  - In every rerun the two fields give identical predictions. Only the printed input field, or KT30's reference labels, differ.
  - KT30's MUTATE gives Cassini 0, dwarfs 3/24 and SPARC rms 0.573, matching CZ1/CZ2.
  - For item 8 the closed-form deep-MOND branch is also set to Newton (A1). The first ν-only MUTATE, disclosed in A1, left a regime-switch difference.

## What this lane can't say
- **The triage can miss a field.** It reads names and literals. A field that reaches ν under an unrecognised name passes as CORRECT. The observed-value list also misses some literals (for example 2.146e-10, 2.15e-10 and 1.8e-10 were only found by hand).
- **The 1D forms are approximations.** They ignore QUMOND's anisotropic factor, in the lanes and in these reruns alike.
- **A rerun reads the lane under the corrected field.** It does not re-grade it.
