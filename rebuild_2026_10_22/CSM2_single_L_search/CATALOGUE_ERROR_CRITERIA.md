# Frozen catalogue stacking experiment

Before new arithmetic: bound the difference between the original per-lens
NumPy interpolation, weighted dot and weight normalization and the saved
aggregate-weight map, for the same binary64 catalogue x and w. Retain the
reviewed NumPy1.26.4/basic IEEE-operation assumptions. Input construction
(logs, cosmological quadrature, catalogue weight reduction) is common to both
maps and frozen; no analytic-transcendental or real-L claim follows.

Reconstruct x,w with the pinned native-matrix recipe and require exact saved
weight reproduction. Form ideal normalized interpolation weights with exact
rational arithmetic for every selected lens. Compare them to saved binary64
weights using exact L1 discrepancies. Inspect clamping, knot and positive
support cases. Both ideal and rounded maps must have identical support.

Bound every active table ordinate using the absolute interval projection map
and the coordinatewise upper covered-mass profile for each tail. Add the
previous forward-error bound divided by the minimum positive saved weight
as a conservative bound on each individual projection evaluation error.
This follows positivity of the previously derived operation majorants.
No empirical padding or physical fitted parameter is introduced.

For each bin with n lenses use u=2^-50, eta=2^-1022 and N=2*n+32,
gamma=N*u/(1-N*u). The reviewed slope interpolation needs at most8 basic
operations on a path; each ideal ordinate expression has positive majorant
3*B, where B bounds absolute table entries. Subsequent weight product,
dot/reduction, denominator sum and division are covered by the remaining
count. Conservative normalized stack error is
  3*B*gamma/(1-gamma) + eta*(2*N+32)*(1+B)*(1+sum(w)+1/sum(w))**2
    *(1+1/min_grid_step)/(1-gamma).
The latter covers additive underflow amplification by the slope division,
weight multiplication, sums and normalization, including denominator error.
Add B times the exact aggregate-weight L1 discrepancy. Derive finite normal
weight/step and no-overflow premises; retain implementation assumptions.
Use directed interval evaluation and exact-rational propagation through the
unchanged covariance dual, adding the prior projection/anchor and source
error budgets once. No refit, new cut or full-model certificate.

Controls: exact original weight reproduction; exact ideal weights sum to1;
nonnegative weights; support equality; exact Sterbenz interpolation steps;
finite output bounds; deterministic constant, alternating and smooth signed
stress tables; wrong-weight mutation; unchanged input hashes; independent
exact recomposition/review. If the bound is too loose, preserve that outcome
without choosing a smaller budget. One single-thread run, wall600/CPU480.
Nonlinear mass, column, branch and continuous-L input coverage remain open.
