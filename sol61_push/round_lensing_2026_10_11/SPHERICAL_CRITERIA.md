# Three-dimensional positivity continuation: frozen before run

2026-10-11. The preceding round-2D run passed 32/32 checks and found zero
minimax residual for all four frozen geometry/background cells. This outcome
is known; the following necessary 3D projection constraint has not been run.
Commit this file ALONE before execution. Preserve the 2D run unchanged.

For 0<R_i<R_j, nonnegative SPHERICAL three-dimensional density necessarily has

  M_2D(R_i) >= [1-sqrt(1-(R_i/R_j)^2)] * M_2D(R_j).

Prove using the pointwise ratio of the two aperture kernels for each 3D shell.
The coefficient is sharp, attained by a shell at r=R_j. Include every ordered
radius pair, plus monotonic enclosed mass. These are NECESSARY constraints,
not a claim that they characterize all positive 3D profiles. A feasible result
does not prove a physical 3D halo or the fixed repaired-kernel density.

Reuse the same 3/6 centres, 135 raw gold rows, two separately labelled distance
scenarios and Helmert basis. Parameterize by enclosed projected masses at the
probe radii (not increments) so all shape inequalities have two coefficients.
Use sparse inequalities; no centre or profile optimization outside this declared
relaxation. Same minimax and subsequent minimum-mass problems, tolerance 1e-9
then 1e-10. Report original and strengthened optimum, primal feasibility, both
minimax AND minimum-mass dual gaps and column violations. Tolerance 1e-6 in
residual/shape inequalities, 1e-7 for dual-column violations; gap <=1e-6 times
max(1,absolute objective). Negative rounding at this scale is numerical error,
not a mathematical certificate of observational exclusion.

Controls: exact shell p ratios for R_i/R_j=.01,.1,.5,.9,.999 and shell radii
R_j times .005,.05,.25,.75,1,1.001,2,10,100, with absolute slack >=-1e-12;
sharpness at r=R_j to 1e-12; positive shell mixtures obey every pair bound;
MUTATE a projected annulus with M_inner=0 and M_outer=1 must violate the
corresponding bound. Enclosed/increment deflection operators must agree for
deterministic nonnegative increments to 1e-10 relative tolerance. Repeated
solver tolerance minima must agree to 1e-6 arcsec. No astrophysical verdict,
physical mass conversion, repaired-kernel test or a0-footing inference.

Resource cap: one process and numerical thread; sparse shape matrix with at
most 60000 rows/1000 columns, <=300 MB expected working memory, wall 90 seconds,
CPU 60 seconds. No PM job. A failure stops interpretation and remains saved.
