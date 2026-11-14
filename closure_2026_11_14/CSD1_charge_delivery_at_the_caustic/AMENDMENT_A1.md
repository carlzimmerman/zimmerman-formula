# CSD1 AMENDMENT A1 (2026-11-14, 14:39 EST by the clock)

Committed alone, after FROZEN_CRITERIA.md (127a25a942) and before any graded number of this lane exists. Written while the
scripts were being written; it changes no gate, label, tolerance or known answer.

1. **S-ref equal-charge radius.** The frozen text ("the largest r <= r_ta with C_R >= C_B") is degenerate: both of FRZ1's
   galaxy layouts hold the same cold total (1 - f_b) M_ta at r_ta by construction, so the condition always holds there.
   R_eq for S-ref is therefore the outermost sign change of C_R - C_B on 4000 log points in [1e-4, 0.999] r_ta (0 if
   none), in units of R_fold; C_R / C_B at 0.999 r_ta is reported beside it.
2. **P1c masses.** P1c names log M_b 10.825 (XJ1's Milky Way mass), which is not one of the nine masses. Two S-seed runs
   at log M_b 10.825 (canonical, alt) are added. FLD1 and XJ1 hold no stored run there, so they carry no KA3; they are
   used for P1c only.
3. **KA7 is weak.** With A = 0 the S-cos insertion is a branch not taken, so KA7 checks only that the inserted text is
   inert. It is kept and reported as such.
4. **A development smoke run, disclosed.** Before the scripts were committed, `csd1_shells.py` was run once at N = 100
   (log M_b 10.45 canonical) to catch errors. Seen: the printed line (R_fold at the end 133.0 kpc, turned-around charge
   1.027 M_b, 18 s), the column count (72) and which columns hold NaN at early times. No delivery ratio, density,
   speed or equal-charge radius was read. The file was moved out of the lane folder and is not used.
5. **P1c details fixed in the grader before any run:** the gamma_L piece uses Delta N = |N_in - N_out| across a layer of
   width w and divides by max(N_in, N_out); "available / missing flux" is c lambda_0 P(C_law) / (N_out |v_req - v_out|).
6. **S-cos tuning file name.** The tuning runs are named `csd1_canonical_M10.45_N1200_A<A>_lawoff.json`; `csd1_tune.py`
   reads every such file present.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
