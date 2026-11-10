# FLD1 AMENDMENT A1 (post hoc; committed alone, before any production run)

**What was seen first (development runs at N = 600 on COL1's A4 grid, log M_b 10.45, canonical; kept outside the repo).**
1. COL1's A4 first-crossing times outside 10, 30 and 100 kpc are not reproducible. Re-running COL1's own code gives
   0.761 / 1.357 / 2.268 Gyr. The same equation with a different arithmetic order (r = X/11 written as (1/11) X, or the
   law term added as a separate line) gives 0.637 / 1.109 / 1.843 or 0.737 / 1.288 / 2.336 Gyr. The 3 kpc time is identical
   to 1e-15 in all of them.
2. R_fold exceeded the turnaround radius (1255 against 255 kpc at z 0): crossed shells were outside every shell still
   falling in, which needs energy no shell had.
3. **The cause is A4's reflection.** A4 reflects a shell at 1.001 r_w, where U = 500 a0, and lets a leapfrog step straddle
   that surface. In a static field with no expansion and no ramp, shells released from rest return after reflection to a
   median 36 times their starting radius (176 of 190 above 1.1; 742 at most) instead of 1.
4. **The fix.** Reflect at r_c = max(1.2 r_w, r_s), where U <= 2.27 a0, and set the outgoing speed by energy conservation
   across the step (the potential change from Simpson's rule on the smooth force between the old and new radius). In
   the same static field, shells that complete their orbit return to 1.0001 (median) and 1.0015 (largest) of their
   starting radius. The log barrier between r_w and 1.2 r_w becomes a hard wall at 1.2 r_w. For a fast shell the true
   turning point lies within r_w (1 + e^{-v^2/(a0 r_w)}), so the turning radius moves by at most 0.2 r_w.
5. With the fix (N = 600, A4 grid), R_fold at z 4 / 2 / 1 / 0 is 17.1 / 47.8 / 76.2 / 139.1 kpc and R_ta is 53.9 /
   108.4 / 164.1 / 254.6 kpc. The first crossings outside 3 / 10 / 30 / 100 kpc come at 0.290 / 0.733 / 1.597 /
   8.096 Gyr. Perturbing the start radii by 1e-15 or 1e-12 changes R_fold by at most 1.1e-6 (relative). These numbers were
   seen before this amendment.

**What changes.**
- Machinery (section 1): the reflection as in item 4, in every production row and bracket. Nothing else changes in the
  equation.
- **KA1 is replaced** (COL1's A4 outer times are an artefact and cannot be a known answer):
  - KA1a, the static-field energy test of item 3/4 at N = 200 shells. Line: for shells that complete an orbit, median
    apocentre/start within 1e-3 of 1 and the largest within 1e-2.
  - KA1b, round-off robustness on the production grid (log M_b 10.45, canonical). Line: R_fold at z 4 / 2 / 1 / 0 changes
    by at most 1e-3 when the start radii are multiplied by 1 + 1e-12.
  - KA1c, COL1's 3 kpc first-crossing times (set by the central focusing, not by reflected shells) for its 8 rows on A4's
    grid with the fix. Line: within 2 %. The corrected 10 / 30 / 100 kpc times are reported beside A4's.
- KA2, KA3, the labels, lines, brackets and MUTATE are unchanged.
- RESULT.md reports, under "anything in COL1 found wrong", that A4's first-crossing times outside 10-100 kpc and its
  z = 0 charge reads came from energy gained at the wall. Corrected values are given with this machinery. COL1's graded
  label (the central caustic) does not involve reflections and is not affected.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
