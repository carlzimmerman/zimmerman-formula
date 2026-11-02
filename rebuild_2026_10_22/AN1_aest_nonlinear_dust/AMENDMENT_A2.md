# AN1 AMENDMENT A2: POST-RESULT, after reading the production rows

Written after the 68 rows and K7 were read. Rows and labels are not changed by this file.

1. **Why a robustness run.** Every P1 row's fold is in cell 0 or 1, r_fold halving with N. At low mu the 1e15 fold radius (0.07 kpc, m 2e6) sits near X14's wall r_w = sqrt(G m / a0) = 0.055 kpc, and canonical and alt differ (z 0.71, 1.31) with very different step counts. So the frozen line (Delta r / a Delta q < 1e-2) may be catching a shell near a wall, not a crossing. K7's list didn't cover those rows. `an1_cf.py` reruns P1 A1, A2 on both footings at line 1e-4, output `an1_cf1e-4.jsonl`. If a row changes, both are reported, and the README says which is the frozen result. Post-hoc, not frozen.
2. **Held start.** First run had two code faults. The galaxy baryon closure was overwritten (`Md` reused), so the galaxy rows in that run are void: the start wasn't static, F/g 4.7. K4 tests E only, so it didn't catch this; K4's own number stands. Shooting failed on 1e15 mu 1 (oscillation): now scans h0 for a root positive to R_out, otherwise NOT RUN. First-run output kept as `an1_held_RUN1.*`. The start's F/g is now reported as a check on each row, with a line I set here, post-hoc: <= 1e-3 outside the first 5 cells.
3. **Correction to section 2.** The criteria said C7's Q0 = 0.1 /Mpc "will be outside" the limit; that came from an arithmetic slip of 1000 in a hand estimate (a0/c^2 is 3.4e-5 /Mpc, not 0.034). Q0_need is computed per row, and the README reports it.
kappa = 1/2 FITTED. Reinstates nothing. Not theory closed.
