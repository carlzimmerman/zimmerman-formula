# X53 AMENDMENT A1 (post-result; REPORTED ONLY; no graded line, class or criterion changes)

Written after the frozen result (64af8eb1cf) to check the win as hard as a fail would be checked: is the LAW class
driven by the halo **edge** (the outer shape the question asks about), or by the **normalisation** of route E's halos
(EM1's SPARC M200 relation)?

Script `x53_diag_A1.py` executes `x53_outer_lensing.py`'s definitions read-only and re-scores (H2H) with a profiled
shift Δlog M200 on a 0.05-dex grid from −0.3 to +1.2 (common to all bins, then per bin by coordinate descent), with the
halo truncated at R200 and untruncated (Burkert continued to 100 R200), both with CFG805's two-halo term (b_eff ≥ 0 per
bin). c_f = 4. (L2H) keeps zero mass freedom, so these comparisons favour (H). Outputs: `x53_diag_A1.out`,
`x53_diag_A1_results.json`.

The c_f treatment requested by the coordinator was frozen in the criteria before any run (§3); nothing about it is
amended here.

Implementation note: the first diagnostic run stopped on a KeyError (the read-only slice ended before `H_PRIMARY` was
defined). The slice end was moved to the start of the scoring loop. No number had been produced.
