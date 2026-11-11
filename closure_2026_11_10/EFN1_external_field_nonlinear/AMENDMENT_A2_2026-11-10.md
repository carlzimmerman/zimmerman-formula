# EFN1 amendment A2 (2026-11-10): the amplitude measure and the run length; committed alone, before any graded run

Post hoc with respect to the criteria (98364c8d20) and A1 (c3e466efbf). Committed before any graded route-D run (R2-R4),
any route-W number, or any mutation.

## What was seen first (one code test, not a graded grid)

Route D on R1 (not a graded grid), canonical expo log M_b 9.4, g_e = 0.1 a0, eps = 1e-4, A1 reading, to 14 e-folds
(700 steps, 10 s):
- **The frozen a(t) = max|n| / |min N0| is not the instability's amplitude.** From the first e-fold on, its maximum sits in
  the first dynamic shell (r = 0.417 r_e) next to the static plane rows, theta 89.8-90.2 degrees, where N0 is positive and
  about 100 times |min N0|: a stable region driven by the growing potential. There a rose from 1.0e-3 to 4.9 at 14 e-folds
  (fitted rate 0.43 Gamma_ref over the last 3 e-folds) while |n|/N0 there stays of order 1e-2 to 5e-2. Graded as frozen,
  F1 (a >= 10) would fire at the edge of the frozen region, not in the unstable shell.
- In the negative-D.P region the largest |n|/|min N0| sits at 0.885 r_e, theta 135-139 degrees (route L's maximum on that
  grid is at 0.885 r_e, 138.8 degrees). It grew from 4.0e-4 to 1.28 over 14 e-folds, at about 0.65-0.68 Gamma_ref (the smooth
  seed approaches the continuum edge from below, as the criteria's section 7 said), and was still growing at 14 e-folds.
  So at eps = 1e-4 the frozen t_end of 14 e-folds ends just as the perturbation reaches order unity: the outcome is not
  reached.

## The changes (reading A2; applies on top of A1)

1. **Amplitude.** c(t) = max over dynamic cells with |N0| >= 0.2 |min N0 over the dynamic cells| of |n| / |N0|: the local
   relative change of the law's phantom density (for the conserved clock current, N/N0 = 1/J along the flow, so a fold is
   |n|/|N0| -> infinity). It replaces a(t) in the stop line F1 (now c >= 10), in the SATURATES / RESHAPES / unbounded-growth
   lines of section 4 (c(t_end) >= 1 with fitted rate >= 0.3 Gamma_ref is unbounded growth; SATURATES needs c over the last
   3 e-folds with max/min <= 1.5 and fitted rate <= 0.1 Gamma_ref), in KA-b3 (fitted early rate of c over the window
   1 e-fold to c = 1e-2, inside [0.5, 1.10] Gamma_ref), KA-c (c(t) <= 2 c(0)), KA-d (c_noseed(t) <= 0.1 c_primary(t)) and M1
   (c(t_end) within 20 %). a(t) and the negative-region amplitude max |n|/|min N0| over N0 < 0 cells are reported beside it.
2. **Run length.** t_end = 30 / Gamma_ref (was 14), or a stop line. The state at 14 e-folds is reported, and so is the time
   in Gyr: 30 e-folds is 22-60 Gyr at 0.1 a0, beyond t_H = 13.8 Gyr (14 e-folds is 10-28 Gyr). RESULT.md says how many
   e-folds fit in t_H for each background, and what the outcome is at t_H for the primary seed and for M1's tenfold seed.
3. The refinement lines (t_F within 0.5 / Gamma_ref between R3 and R4; within 0.1 / Gamma_ref under dt halving) and every
   other rule are unchanged.

The frozen and A1 readings (a(t), 14 e-folds) are computed from the same runs (the histories record a(t) and the state at
14 e-folds) and reported first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
