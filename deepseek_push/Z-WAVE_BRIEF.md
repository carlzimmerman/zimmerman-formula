# Z-WAVE BRIEF — spawned by the conductor tick 2026-09-26 (3 lanes, conductor-run, detached)

House rules: deepseek_push/LOOP_CONDUCTOR.md 1-10 verbatim (append-only, no fabrication,
honest FAILs verbatim, pre-registered kills, no leaf-lane commits, raw data untracked,
no lane collisions, dedup vs register). Context numbers cited below are on disk at the
paths named; each lane re-loads them at run time. Spawn evidence: Zwave_launch.py
(detached, start_new_session — the V03c silent-death fix), verified live by ps + .out appends.

## Doors (distinct, OPEN per register §6 + 2026-09-25 ops note; barred list respected)

### QF1 — Q-functional closure probe (door: L02 Q-functional, MEASURED-ONLY)
Context: L02_results.json publishes E[Q](tau0,q) with SEs; best family F5 max_resid_SE = 21.08
(disk). L02's own kill, pre-registered: "claimed closed forms must reproduce table within 3 SE".
Goal: test NEW closed-form candidate families (F8 rational-power, F9 stretched-exponential,
F10 two-power, F11 Pade-2) on the published tables, weighted LS, per-q fits; leave-one-tau0-out
holdout. Deliverables: QF1_q_closure.py/.out/.json.
Kill (pre-registered, L02 verbatim): a family BANKED only if in-fit max <= 3 SE AND holdout max
<= 5 SE across central+volume; otherwise exit 1 with "closure remains OPEN" and the best
residual recorded honestly. No re-tuning of SEs (rule 3).

### OB1 — JWST observation design (door: L05/K09, register row 66 IN FLIGHT)
Context on disk: L05_results.json power grid (central_N{1,10,30}_SN{10,30,100}_f{10,15,20}),
L03_results.json jwst_reach_summary = pair S/N 50 (q0/q2) and reach formulas in register row 47,
K11_results.json consolidated_tests T1-T5 (falsifier schedule, verbatim).
Goal: registered program statement: minimal (N, per-object S/N) configurations reaching
P >= 0.95 on the 2x-radius 3-sigma program, folded with L03's S/N=50 pair reach and K11's
T1-T5 schedule into OB1_JWST_PROGRAM.md + OB1_results.json; every number recomputed in-script
from the loaded files (no transcription).
Kill (pre-registered): if the minimal registered configuration requires per-object S/N > 50
(the L03-tested JWST pair reach) -> INFEASIBLE-JWST, exit 1, recorded honestly; else exit 0
with the margin 50/SN_req stated.

### MR1 — RAR moment-discipline transfer on the D-audit-corrected footing
Context: D02_rerun_outputs/<variant>/L06_results.json for variants std05_cut, std06_cut,
std07_cut, std05_nocut (disk, exit codes in exit_codes.json); register correction rows
(2026-09-25): the SPARC-deep deficit was a corpus artefact; corrected deep band = EXCESS.
Goal: re-run the pre-registered moment-discipline gates (M1, 5-SE bar) per ensemble per
variant from the corrected result files; record deep-band z per variant and its spread.
Kills (pre-registered): (i) any real-ensemble M1_pass = false in any variant ->
DISCIPLINE-KILL-UNDER-CORRECTION (exit 1, honest); (ii) if the deep-band z flips sign across
variants -> UNSTABLE-UNDER-M/L flagged; (iii) mismatch vs the register's corrected deep
z-values (+9.1/+7.1/+5.7/+8.1) beyond 1.0 sigma-of-variants -> MISMATCH flagged for re-audit.
Deliverables: MR1_corrected_discipline.py/.out/.json.

Barred doors respected: SPARC-deep deficit sizing (premise moot), V04 factorized N=1 route
(refuted by V04b), N01 density-locality (KILLED).
