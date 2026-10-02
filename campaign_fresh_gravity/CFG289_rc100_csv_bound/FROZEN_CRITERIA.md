# CFG289 — FROZEN CRITERIA: how far do the 17 wrong cells in the repo's RC100 CSV reach? (orchestrator lane, 2026-10-02)

**Written and committed before the corrected file or any re-run exists.** It closes CFG287's one MAJOR item (AUDIT.md §"The uncorrected RC100 CSV in older outputs"), which was owner-directed ("make sure those scientists didn't mess up the data … do it rigorously"). κ = ½ is FITTED. No data are fetched.

## Inputs (on disk, tracked)
- **Original:** `real_research/data/rc100_nestorshachar2023_table3.csv` (sha256 prefix 6a574c79367b268b). It is never edited.
- **Paper values:** `data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv` (sha256 prefix 56121a5550679db5; the 09-29 data-front read of arXiv:2209.12199 Table 3; `changed_cells` lists the 17 cells in 16 rows).

## The corrected copy (built by the script, then never hand-edited)
- **Output:** `real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv`, with the same columns and order as the original.
- **Primary cells:** each of the 17 cells takes the paper value. No other primary cell changes.
- **Derived columns, recomputed for changed rows only:**
  - g_Re = V_c²/R_e;
  - a0_Vc4_over_GMbar = V_c⁴/(G M_bar);
  - a0_over_1.2e-10, to 3 decimals;
  - deepMOND = (g_Re < 1.2e-10).
- **Constants:** G = 6.674e-11, kpc = 3.0857e19 m, M☉ = 1.989e30 kg. These reproduce the original's derived columns on the 84 untouched rows to ≤ 5e-5 relative (the printed 5-significant-figure precision). This was checked before this file was written; the script re-checks it as C1.
- **Controls:**
  - **C1:** the derived-column reproduction holds on the untouched rows (≤ 5e-5 relative).
  - **C2:** the untouched rows are byte-identical to the original.
  - **C3:** exactly 17 primary/name cells differ from the original, and they match `changed_cells`.
  - **C4:** the corrected copy's six primary fields equal the paper-values file in all 100 rows.

## Readers
- **Scope:** every tracked `.py` that names the CSV (`git grep -l rc100_nestorshachar2023_table3 -- '*.py'`). Shared modules (`*_common.py`) are run through their lanes' entry points. CFG287 itself is excluded, since it reads both files by design.
- **Two runs per entry point, each in its own scratch mirror of the repo:**
  - **ORIG:** with the original CSV. This is a control; it should reproduce the committed outputs.
  - **FIX:** with the corrected copy substituted at the original path.
  - Committed outputs in the repo are never overwritten. The FIX outputs that differ are copied into this lane as `<name>_RC100FIX.<ext>`, with a diff summary.
- **Classification per entry point:**
  - **NOT-RUN:** cannot run (missing input, too long; the reason is stated).
  - **NOT-REPRODUCIBLE:** ORIG differs from the committed output beyond run-time and timing lines. The FIX-vs-ORIG difference is still reported.
  - **UNCHANGED:** FIX outputs are identical to ORIG (apart from run-time fields).
  - **NUMERIC-MINOR:** numbers move, but every pass/fail row and every verdict word is the same, and each headline shift is < 1σ of that headline's own quoted error.
  - **VERDICT-MOVES:** any pass/fail row flips, any verdict word changes, or any headline moves by ≥ 1σ.
- **Consumers:** for every NUMERIC-MINOR or VERDICT-MOVES entry point, list the documents that quote it (STANDING, papers, the MNRAS manuscript), found by grep.

## MUTATE (a control that can fail)
- Run one entry point that uses V_c (CFG216's main script) with a copy in which row 1's V_c is doubled.
- Its output must differ from ORIG. If it does not, the substitution path is dead and the lane is void.

## What this lane cannot say
- It does not test whether the published ApJ 944, 78 table equals arXiv v1. CFG287 records this as open.
- It does not re-score any physics. It only bounds how far a transcription error propagates.
