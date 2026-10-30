# GH8 amendments

1. **Blank map regions (a real defect, also in GH7).** The first control run gave S/N 168 and **failed MUTATE** (shuffled S/N +146), so it is not a validation and
   is discarded. Diagnosis: about 12 % of lenses sit where the map is nearly blank. The 2′ CAP rms per nside 32 pixel is bimodal, near 0 vs 5–10 µK. These pixels are
   non-zero, so they passed the "zero or non-finite" stamp test, and GH7's 100 % valid stamps were a sign of this. Inverse-variance weights then blew up on them.
   Mean-offset × mean-velocity terms then dominated. **Rule, fixed before re-running: drop lenses in nside 32 pixels with 2′ CAP rms < 4 µK**, read from the histogram gap (the rms
   is even in v). 12.3 % of GH7's centrals are in such pixels; GH7's amplitudes are diluted by about that much, which does not change its void class.
2. **K2 fails:** the mock's P(k) is off by up to 16.7 % at k 0.03–0.3 (limit 10 %) after the two frozen matching iterations. Not re-tuned. R_fm 0.921 and R_cut 0.904 agree; the
   R_cut power law did not lower P at k ≈ 0.002 as intended, so R_cut is a weak test of low-k systematics.
3. **Memory:** `gh8_vel.py` peaked at 7.1 GB, above the frozen 6 GB, while other zoom jobs were running. They were not disturbed as far as I can see.

4. **Null offset (a real defect; found in the first MW-mass run, which is discarded).** Passive lenses gave A(1.8) 0.47 ± 0.12 yet shuffle p 0.08, and star-forming lenses were opposite in sign with p 0.47. So the
   shuffled A does not centre on zero. Cause: the weighted CAP mean per z bin is not zero, split samples were not re-centred, and v_rec has a non-zero mean, so
   mean CAP × mean v leaks tSZ and CIB through the even-in-v cancellation. **Fix, in both the control and the MW-mass stack, for every sample: remove the weighted CAP mean and the v mean in each z bin of that sample.**
   The control is re-run first and its frozen rule stands: S/N ≥ 4 or the lane ends VOID. The shuffled-A mean is now printed. GH7 centred CAP but not v; its class was void anyway.

5. **R must match the demeaned velocities.** Removing the z-bin mean of v_rec changed T̂ and its errors by about 2.7×, so most of the raw v_rec variance was a coherent radial mode per z shell (the same low-k excess). R is therefore recomputed on z-bin-demeaned
   v_rec in the mock: R = Cov(v_true, v_dm)/Var(v_dm). R_ctx uses the data's demeaned rms. Control re-run, for the same frozen rule, before the MW-mass stack. The earlier R values (0.921, 0.904) are superseded.

6. **The frozen β direction is inverted.** The criteria say A scales as β_true/0.44. T̂ does not depend on the true β through the assumed one, and R_true = R β_true/0.44, so **A scales as 0.44/β_true**. Corrected here, after the result; the README uses this form.
