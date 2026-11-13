# SRF1R AMENDMENT A1 (2026-11-12): compute budget

Committed alone, after READING.md (cc3d45432d) and before any flux-level number of this lane exists. Reason: a timing run
of one primary part (canonical, z 2.2, seed 0; one of 32 halo chunks run, its flux output not computed into any
statistic, nothing read but the wall time) took 82 s per chunk, about 11 minutes per part, about 7 hours for the primary
stage alone, against a budget of about five hours for the whole lane. The stage-0 tables (halo-model profiles, SRH1's own
R_cold at every f) were built as frozen. No statistic, label rule, known-answer tolerance or gate changes.

Changes (each a cut in compute, stated before any number):

1. **Denominator.** P1D_ref = P1D(B) only. The heavy haloes' own reference contribution at true abundance (READING
   section 3, last bullet of "Flux change") is not added. It is the most expensive piece (skewers out to r_ta + 4 lambda_P
   around every heavy halo). Expected size: haloes above 1e12 Msun/h at z 2.2 cover about 0.4 % of skewers within r200m
   (n 1.1e-3 (h/Mpc)^3, cross-section 0.18 (Mpc/h)^2, path 20 Mpc/h); listed under physics left out.
2. **Seeds for the largest f.** f = 4, 6 and inf are computed with seed 0 only, at all twelve bins. At the anchors their
   R_F is seed 0's, not a three-seed mean. Every other f keeps the frozen seeds (three at the anchors, seed 0 elsewhere).
3. **Inserted haloes per 0.1 dex bin:** K_b = 16 where the expected count is below 16, else 32 (was 24 / 48); weights
   w = N_b / K_b as frozen.
4. **Bracket f list:** 0.70, 1.00, 1.25, 1.60, 2.00, 3.00 (inf dropped). The FRAGILE rule is unchanged (f = 1 and the
   window); a bracket f_max above 3.00 is reported as "> 3".
5. **Known answer (e)** is evaluated at f = 1 and at the grid points bracketing f_max that carry three seeds (f <= 3);
   if f_max lies above 3, at f = 1, 2.5 and 3.
6. **Arithmetic:** the skewer flux of inserted haloes in float32 (sums of |FFT|^2 in float64).
7. If time still runs short, brackets are dropped from the end of the frozen order (B10, B9, B8, ...) and reported as not
   computed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
