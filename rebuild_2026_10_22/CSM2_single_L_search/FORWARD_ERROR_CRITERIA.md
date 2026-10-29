# Frozen source floating-evaluation bound

Use the completed fixed-primitive ideal projection as reference. Inspect and
cache installed NumPy1.26.4 gradient and official v1.26.4 real interp source.
The model assumes those inspected implementations and IEEE binary64 basic
operations; C binary build identity is not independently authenticated. Primitive
log/hyperbolic/query values stay fixed source values, not analytic-real claims.

Derive positive absolute-operation-path majorants U(M),V for gradient,
interpolation and quadrature. U is linear in coordinatewise |M|. V accounts for
absolute underflow/flush errors: addition sums V and adds1; multiplication or
division by fixed c scales V by |c| or1/|c| and adds1. Interior gradient uses
three multiplies/two adds/divide, V=5/r+1; edge subtraction/divide/divide gives
V=(1/dx+1)/r+1. Interpolation follows the inspected difference/slope formula,
not an assumed convex floating implementation. Verify Sterbenz ratio conditions
for fixed log-coordinate differences, and normal/finite coefficient preparation.

A conservative syntactic path bound is N=2*2401+128=4930 operations: at most
2401 sum operations per integral plus gradient/interp/constant/product/scaling
paths, counting both integral branches and slack128. Freeze u=2^-50 (above
binary64 unit roundoff) and eta=2^-1022 (minimum normal, allowing flush-to-zero).
With gamma=N*u/(1-N*u), use E=gamma*U + eta*V/(1-N*u). Normal coefficient prep
rounding is included in the path count; detect zero/non-normal preparation
conditions rather than silently assume a relative model. Check all intermediate
majorants safely below binary64 overflow for the registered mass envelopes.

Aggregate positive inventory weights before applying U: separate halo/law
mass envelopes per bin use the completed upper halo endpoint and fixed law
profiles. This bounds weighted projection errors provided the actual mass
vectors are covered; column/branch/continuum membership remains an obligation.
Absolute V is multiplied by each group's exact weight sum. Use50-digit directed
interval arithmetic for majorants/error budgets and outward binary64 outputs.

Test source projection versus certified ideal intervals on full-envelope and
alternating-zero stress vectors in each8bin/tail channels (240 scalar tests),
including a1% corrupted nonzero result. Propagate the derived error into the
unchanged exact covariance dual on top of the completed coefficient/anchor
inflation; preserve exact ratios and unchanged cut. No new score fit, physical
parameter, padding selection or L sample. Wall600/CPU480/one thread. Record
source hashes before/after, finite outputs and all coverage. Preserve failed or
inconclusive conditions; do not claim full model certification from this stage.
