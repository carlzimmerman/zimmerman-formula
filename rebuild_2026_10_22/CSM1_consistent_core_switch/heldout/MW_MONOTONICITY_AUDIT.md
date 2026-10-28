# Independent monotonicity review

Claim: for fixed positive M,R and observation radius 0<r<R, the exact compact spherical Burkert profile with its stated saturation convention gives nondecreasing enclosed mass and radial speed as core column increases. Composing with the nondecreasing L-dependent core column preserves this property while the halo branch is held on.

Primary verdict: **correct only after a stated restriction**. The source phrase “model speed” means the forced-halo profile speed. It does not mean the full switched model: crossing the Local Group law/halo threshold may jump the force. The bound protocol explicitly forces the halo branch on and separately carries the known law-branch MW failure, so its finite calculation uses the permitted restriction.

Reviewed source: MW_BURKERT_MONOTONICITY.md, SHA256 `76ad08ecfd595478413056e41ef7b07e1b94e1c378054767c6a7213a7c7a4319`. Independent reviewer: /root/one_parameter_bounds, separate from the heldout implementation author; review delivered in this session after direct source inspection.

Dependency/obligation matrix:

| Obligation | Status |
|---|---|
| Burkert derivative and positive mass integral | passed |
| g strictly increasing; weighted identity h>3-g | passed |
| h decreasing from3 to0; unique maximum of B(x)/x² | passed |
| Compact-root scale order in Sigma | passed |
| Enclosed fraction increases at fixed r/R in(0,1) | passed |
| Saturated branch linear in Sigma; continuous join | passed |
| Sigma floor and fixed finite maximum preserve nondecrease | passed |
| Full law↔halo switched-model monotonicity | out of scope; not asserted |
| Uniform floating optimizer monotonicity for all L | not certified |
| Evaluated compact brackets and R0<R200 | computationally checked in mw_bound_001 |

The independent reconstruction agrees with the h-weighted-mean argument and saturation step. Numerical optimizer/bracket checks are finite witnesses, not a uniform floating-point certificate. No external theorem or literature leaf is used. The strongest safe statement is exact-arithmetic halo-profile monotonicity under the stated compact/saturation conventions, plus the finite radial-speed relaxation in mw_bound_001. That relaxation is vacuous: its L=0 maximum already exceeds the L1 lower cut. No stronger positive lower bound follows from this particular necessary condition.
