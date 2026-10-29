# MV28: a calculable microscopic vacuum sector

User target: calculate vacuum stiffness and full gravitating vacuum energy
from one microscopic model, and commit/push substantive results as work
proceeds. Base revision and prior source hashes are in INPUTS.json.

Try the explicit renormalizable R-symmetric O'Raifeartaigh model

    W=fX+lambda X phi1 phi2+m1 phi1 phi3+(m2/2)phi2^2,
    K=|X|^2+sum_i |phi_i|^2,

with f,lambda,m1,m2>0, no independent superpotential constant at the declared
matching scale, and R charges (X,phi1,phi2,phi3)=(2,-1,1,3).
This known model has a calculable one-loop metastable radial minimum for
some parameters. It is a new test model, not an established microscopic
completion of PN28. It has a runaway and an R-Goldstone mode; neither may
be suppressed in the claims.

## Portfolio and first discriminators

1. Spectrum route: derive boson/fermion mass matrices from W, compute the
   Coleman-Weinberg potential, and compare a source benchmark before extracting
   a radial stiffness. Freeze the finite grid and tolerances before execution.
2. Gravity route: insert the same W and K into the N=1 supergravity potential.
   Compute the full tree vacuum energy on the radial valley, then quantify
   the roles of a superpotential constant and allowed K corrections. Rigid
   SUSY alone must not be advertised as a determination of cosmological energy.
3. Halo route: identify s=ln(|X|/v) at a nonzero radial minimum and try the
   invariant coupling Z=|X|^2/v^2. Derive the actual total pressure response
   from the computed potential; do not substitute the PN28 exponential
   potential or its log-pressure law. Test loss of transverse stability as
   matter moves the scalar minimum.

Success would calculate B_curv=U_ss(0)/9 and V_total in the same specified
model with controlled corrections, derive the mapping to physical gravity,
and retain viable matter/halo behavior. A formula in terms of model couplings
is progress but not a universal numerical ratio. Choosing couplings to hit
the old 0.002329458 target is prohibited as a claimed derivation.

The finite experiment will use r=m2/m1 in {3,4,5},
y=lambda f/(m1 m2) in {0.05,0.1,0.2}, and lambda in {0.3,0.6,1} for
ratio rescaling. The benchmark r=4,y=0.2,lambda=1 is specified by the checked
primary source. All tree transverse eigenvalues at candidate minima must
be positive. Stable-interval limits, full numerical methods, orthogonal
invariants and resource caps will be recorded in contract.json.

No delegation is authorized. New files stay in this folder; earlier
checkpoints and active Claude work are preserved. No claim of worldwide
novelty or a completed theory will be made.
