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
