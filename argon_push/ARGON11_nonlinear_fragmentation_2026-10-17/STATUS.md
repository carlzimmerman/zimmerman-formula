# ARGON11 status (2026-10-17 13:55)

**QUEUED, NOT RUN.** Criteria frozen (2153ca9e0); solver `frag3d.c` + launcher committed; analysis script `argon11_analyze.py` written but **not yet executed**.
Reason: the machine rebooted at ~13:44; `chain6.sh` restarted and began the T1x paper's alternative-footing 1024³ run (T2x) at 13:47. Rule: no other
computation while the T1x reruns run (T2x then NCS0/NC1x, about 3 days; `project_t1x_paper_reruns`). The launcher stopped my runs within seconds (the watchdog worked as designed).

**State on disk (outside the repo, `_external_data/argon11_work/`)**: checkpoints for R1/R2/R4 at t = 25 and R6 at t = 50 (killed by the app quit/reboot); logs repeat a few
lines after a resume (the analysis keeps the last entry per time). R3, R5, R7, R8 have not started.

**Waiters armed** (detached `argon11_run.py R1 resume`, `R2 resume`, `R4 resume`, `R6 resume`, `R3`, `R5`, `R7`, `R8`): each polls every 30 s and starts only when no
1024³-type run and no `overnight_chain/chain*.sh` script is alive; if one appears it stops its job within ~5 s and resumes from the last checkpoint later.
If the machine reboots they must be re-armed:
`python3 - <<'PY'` … `subprocess.Popen(["python3","argon11_run.py",R,("resume" if R in (R1,R2,R4,R6) else None)], start_new_session=True)` (see the session log), or simply
`cd argon_push/ARGON11_nonlinear_fragmentation_2026-10-17 && nohup python3 argon11_run.py R3 &` for a fresh run, `… R1 resume` to continue from a checkpoint.

**Expected cost once allowed**: 8 runs, single thread each, 8 cores, about 25–40 min wall, < 1.2 GB in total (R1 reached t=102 in 40 s of wall time).
**After the runs**: `python3 argon11_analyze.py` (refuses to run while the chain is alive) prints K1–K8 and the M5 reading; then write REPORT.md and HANDOFF_TO_ASTRA.md.
The analysis script was written without being run; bugs found on its first run will be fixed and disclosed (no gate or definition changes).

## Update 2026-10-18 17:55
Owner chose **leave queued** (options offered: SIGSTOP-pause the T2x engine for ~35 min / run capped beside it / leave queued). Nothing was run or touched.
T2x (relaunched 10-18 10:15 after the owner added rolling checkpoint + exact resume to the 1024³ engines, commit 269b18e50) is at step 25/150 at ~290 s/step and rising;
NCS0/NC1x follow, so the first window for these jobs is the end of chain6, around 10-20/21 at the earliest. The eight waiters have been alive since 10-17 13:49; they do not survive a reboot.
Engine guards, for the record (run_650.py): RSS > 52 GB, system swap growth > 4 GB, disk free; no wall-clock or stall detection.

## RESULT (2026-10-18 22:20; analysis run beside T2x on owner request, 1 core, nice 19)
All 8 runs reached t_end (R3/R8 finished unsupervised at 22:02 after the owner had them run beside the resumed T2x; their
watchdog wrappers were removed so the job would not stop). `argon11_analyze.py` ran unchanged except an env override of its
busy-guard (`ARGON11_ALLOW_BESIDE=1`, owner 10-18). Output: `argon11_analysis.out`, `argon11_results.json`.
- **K1 conservation PASS** in all runs (|dQ/Q| ≤ 3e-13, |dE/E| ≤ 9e-7). **K2 linear growth PASS** (γ within 2–4% of prediction).
- **K3, s = 0.1: FRAGMENTS** in R1, R2, R3 (and R6, R7, R8): the coherent charged state breaks into 24–156 bound lumps
  (Q-ball-like: n_in ≈ 0.85 n*, E/Q ≈ 0.95 < 1) at t_A = 325–450; the lumps then merge slowly (N_lump falls ×2–3 by t_end).
- **K3, s = 0.5 (R4): NO STABLE FRAGMENTS** — one dominant lump (median |n_in/n* − 1| = 0.52); **K4 REVISED** there
  (r_Q = 136, r_S = 0.20): σ/m drops to 0.17 cm²/g at ε = 1e-3 (LOW-EDGE).
- **K4, s = 0.1: F2 estimate SURVIVES** over the full run range (r_Q 0.59–0.88, r_S 0.86–0.91): S ≈ 4.2–4.8e-3,
  σ/m ≈ 1.0–1.1 cm²/g at ε = 1e-3 (ABOVE-LOW), ~1e3 (EXCLUDED) at ε = 1, ~1e-3 (BELOW) at ε = 1e-6.
- **K5: NOT CONVERGED** on resolution (R3 vs R1: t_A +23%, Q_med 30%) → numbers are quoted as ranges (above); seed OK;
  box (R8) changes the lump count ×2 (reported only).
- **K6:** amplitude ε 1e-4 vs 1e-6 changes Q_med ×1.17 (within 1.5). **MUTATE M5 bites** (repulsive quartic: no lumps).
- **Reading:** at s = 0.1 the ARGON10 F2 self-interaction estimate holds in full 3+1D nonlinear evolution (within the
  resolution range); at s = 0.5 it does not fragment and the F2 estimate is revised downward. Handoff to astra; astra's files untouched.
