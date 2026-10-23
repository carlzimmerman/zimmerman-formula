# The weak-decay indicator stabilizes across eight to sixteen field shapes

The large four/eight-basis discrepancy from PV_RESULT.md does not continue when the field space is enlarged. Nested8,12,16-shape calculations give a real-axis weak-decay indicator near6.9e-5, with about .33% span at the finer action order. The candidate frequency remains near .822797. This is a substantive convergence improvement, but not a solved continuum pole or certified physical lifetime.

## Enlarged calculation

Extend the same Legendre displacement family xi_k=r P_k(2r²/R²-1) to k=0,...,15. Recompute orbital Fourier coefficients on64x64 and128x128 action grids. The first eight coefficients and stiffness submatrix reproduce the earlier eight-shape data exactly, so the new comparison genuinely nests the existing approximation.

The16-shape stiffness condition number is approximately6.93e5. It remains positive definite. The independent Hessian discrepancy is below3.75e-8 in absolute matrix entries. Conditioning and weak matrix directions remain relevant when interpreting small absorptive eigenvalues; positive definiteness alone does not establish a small relative error in every direction.

Recompute the direct resonant absorptive matrix and pole-subtracted real response with all sixteen shapes. Roots, endpoint completion, direct orbit checks and energy-quadrature comparisons follow the earlier construction. The complex-mode diagnostic then uses nested8,12,16 submatrices, with the absorptive matrix held at omega=.8228 while the real part is evaluated at .8220,.8228,.8236.

## Results

| action order | shapes | linearized real crossing | provisional decay indicator |
|---|---:|---:|---:|
|64|8|.822796241|6.90460e-5|
|64|12|.822797022|6.88296e-5|
|64|16|.822797238|6.90244e-5|
|128|8|.822796033|6.90654e-5|
|128|12|.822796824|6.88398e-5|
|128|16|.822797047|6.90506e-5|

The indicator is Im lambda/(d Re lambda/d omega) for the near-zero generalized complex eigenvalue. It is not obtained by solving an analytically continued dispersion relation at a complex frequency. Its agreement under these refinements does not remove that distinction.

The16-shape direct absorptive matrices differ by about .77% in relative Frobenius norm across action grids; the selected projections are much more stable. The real principal-value matrix energy-quadrature comparison remains below2e-6 relatively, while the selected near-zero eigenvalue changes by less than1.5e-10 under that energy refinement. Full-matrix and selected-mode error measures should not be conflated.

## Harmonic truncation is now more visible

Both calculations retain only sixteen orbital harmonics. At64 action order, the independent matrix sum-rule errors for nested spaces are:

| shapes | relative moment error |
|---|---:|
|8|1.88e-5|
|12|4.41e-4|
|16|6.76e-3|

The full16-shape error barely changes on the128 grid. This points toward unresolved harmonic/spatial representation error rather than ordinary action-grid integration as an important remaining issue. It is not proof of which truncation dominates. A global high-frequency sum-rule error does not directly equal the error of the low collective mode, but it prevents treating the table as a fully validated physical rate. Increasing the retained harmonic range is the next targeted check.

The earlier decline from four to eight shapes is therefore best interpreted as a real field-truncation effect within this calculation, rather than evidence that the indicator keeps tending toward zero. The8/12/16 comparison supplies no proof of monotone convergence or of a nonzero exact lower bound.

## Physical interpretation remains conditional

The collective mode has access to a third-harmonic kinetic absorption channel, but its complex spatial structure strongly reduces coupling. The present data support investigating a weakly damped mode rather than assuming rapid settling. If the indicator ultimately represented an amplitude decay rate, it would correspond to roughly1900 oscillation periods per amplitude e-fold. This is conditional dimensional arithmetic, not a measured lifetime or formation-time claim.

A definitive rate still requires harmonic refinement, the frequency dependence of the absorptive matrix, and an appropriate continuum pole or initial-value calculation. Even a verified perturbative decay rate would not explain why an arbitrary initial population reaches A10000, evade the phase-space occupation constraint, or complete the relativistic parent. No new interaction or phenomenological friction has been added; novelty remains unestablished.

## Evidence

Direct enlarged-basis action, resonant and principal-value results are preserved separately. basis16_run audits their pinned artifacts, confirms exact nested-prefix consistency and the complex dissipative identity, and passes seven checks with a valid completed manifest. The direct long calculations are not represented as executions within that bounded artifact audit. Interpretation is self-reviewed. Passing the audit does not certify the still-open physical rate.
