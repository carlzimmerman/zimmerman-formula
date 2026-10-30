# GH8 amendments

1. **Blank map regions (a real defect, also in GH7).** The first control run gave S/N 168 and **failed MUTATE** (shuffled S/N +146), so it is not a validation and
   is discarded. Diagnosis: about 12 % of lenses sit where the map is nearly blank. The 2′ CAP rms per nside 32 pixel is bimodal, near 0 vs 5–10 µK. These pixels are
   non-zero, so they passed the "zero or non-finite" stamp test, and GH7's 100 % valid stamps were a sign of this. Inverse-variance weights then blew up on them.
   Mean-offset × mean-velocity terms then dominated. **Rule, fixed before re-running: drop lenses in nside 32 pixels with 2′ CAP rms < 4 µK**, read from the histogram gap (the rms
   is even in v). 12.3 % of GH7's centrals are in such pixels; GH7's amplitudes are diluted by about that much, which does not change its void class.
2. **K2 fails:** the mock's P(k) is off by up to 16.7 % at k 0.03–0.3 (limit 10 %) after the two frozen matching iterations. Not re-tuned. R_fm 0.921 and R_cut 0.904 agree; the
   R_cut power law did not lower P at k ≈ 0.002 as intended, so R_cut is a weak test of low-k systematics.
3. **Memory:** `gh8_vel.py` peaked at 7.1 GB, above the frozen 6 GB, while other zoom jobs were running. They were not disturbed as far as I can see.
