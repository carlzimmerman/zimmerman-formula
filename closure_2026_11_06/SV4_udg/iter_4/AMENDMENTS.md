# SV4 iter_4 amendments

## A1 (numerical, after two variant rows had printed, before any label): solver stop at residual 3e-8

QX4's Picard solve on Malin 1 floors at a relative residual of ~1.5e-8, above its default 1e-8 stop, so every
solve runs to the 400-iteration cap (about 6 minutes each under the machine's load; 48 variant solves would take
hours). The variant solves (and the bar rows) now stop at residual 3e-8, warm-started from the baseline solution of
the same footing. The baseline itself is still run to 1e-8 / the cap (it carries KA0). Check, written into iter4.out:
the baseline solved cold at 3e-8 must match the capped run to 1e-3 in V at every ring. The two variant rows seen
before this amendment (sph_s1_f_lo: chi2 104.5 canonical, 83.5 alt) are reported in the README. Nothing about the
corners, the labels or the physics changes.
