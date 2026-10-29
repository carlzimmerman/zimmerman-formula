# Original catalogue interpolation and stacking

catalogue_001 completes the next numerical-map obligation. All181431 selected
lenses are retained. Exact rational ideal interpolation weights sum to1 in
each bin and have exactly the saved positive support. The original rounded
weight construction reproduces all saved weights bit for bit. Maximum exact
L1 discrepancy from ideal aggregate weights is1.914797023e-15.

The frozen operation-count budget uses N=2*n+32 per bin, u=2^-50 and
eta=2^-1022. The count covers interpolation slope arithmetic, weight products,
dot/reduction, denominator reduction and normalization. The numerator has
positive majorant3*B; numerator and denominator error combine under the
conservative N budget. Additive underflow amplification includes grid-step
and weight-sum divisions. B is derived from absolute interval projection
coefficients and covered mass profiles, plus an individual evaluation-error
bound obtained from the previous positive aggregate majorant. B is at most
1083.645; maximum resulting stack error2.607694418e-7 native units. No budget
was chosen from the likelihood score.

All29 run controls pass, including12 signed/constant/smooth stress cases and
a wrong-weight mutation. The independent self/adversarial review regroups
lenses by interpolation interval before accumulating their exact first
moments; it reproduces all ideal weights. It also verifies every one of60
projection majorants and60 error budgets using exact rational arithmetic.
All16 review controls pass. The runner manifest validates as completed and
source/input hashes are stable.

NumPy again emitted divide/overflow/invalid floating-status warnings from
matmul although the returned values were finite. These warnings are preserved
in stderr. Every stress result is converted to Fraction, which rejects any
nonfinite value; every output bound has an explicit finite check. The exact
certificate recomposition does not use BLAS. This does not independently
authenticate the installed BLAS/C binary: reviewed implementation and standard
basic-operation semantics remain assumptions.

Adding the catalogue error once to the prior anchor/projection budgets and
propagating through the unchanged exact covariance dual gives conditional
lower569.5338626102013, versus exact feasible-law upper+9=163.34346325076024.
This remains a conditional local result on[3.75,3.751], not a certified real-L
exclusion. Catalogue x and w are the same deterministic binary64 inputs as
the original map; their log/distance/initial-reduction construction is frozen,
not an analytic-transcendental assertion. Nonlinear mass construction and
column/branch/continuum coverage remain. See NONLINEAR_DOMAIN_ROUTE.md for
the next original-source obligation; do not rerun completed map stages.

Native finals remain seeds1,3,7,8,9. Source snapshot/done/final-log hashes and
published copies agree. All four pending rolling checkpoints are recent.
No aggregate NL1 output or new native measurement is published this turn.
